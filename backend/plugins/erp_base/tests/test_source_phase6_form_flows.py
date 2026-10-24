"""补绑原UpdateSQL入口：登录、续行、主从保存和转调价撤回的非空联调。"""
from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from .test_phase_report_audit import create, at
from .test_source_phase6 import reader
from plugins.erp_base import source_services as services
from plugins.erp_base.source_phase3_operations import model
from plugins.erp_base.source_context import SourceDocumentContext
from plugins.erp_base.source_entry_registry import ENTRY_RULES
from plugins.erp_base.source_phase6_transfers import quote_to_price_adjustment, reverse_quote_adjustment

class FormFlowTests(TestCase):

    def setUp(self):
        self.actor = get_user_model().objects.create(username='phase6-form-flow', is_superuser=True)
        self.client = APIClient()
        self.client.force_authenticate(self.actor)

    def test_explicit_update_sql_bindings_are_all_exposed_in_form_metadata(self):
        from django.apps import apps
        from plugins.erp_base.source_phase6_forms import extend
        count = 0
        for label, rules in ENTRY_RULES.items():
            selected = {name for name, rule in rules.items() if rule['write_binding']['source'] == 'explicit_UpdateSQL'}
            if not selected:
                continue
            m = apps.get_model(label)
            resources = {m.__name__: {'crud_fields': list(m.SOURCE_FIELDS.values()), 'workflow': {'actions': []}}}
            extend(resources)
            self.assertTrue(selected.issubset({r['value'] for r in resources[m.__name__]['workflow']['entries']}))
            count += len(selected)
        self.assertEqual(count, 37)

    def test_request_limit_login_defaults_keep_duplicate_employee_rows(self):
        for _ in range(2):
            create('h_Employee', EmpID='E', LoginName=self.actor.username)
        item = services.write(model('RequestLimit'), {'_entry': 'RequestLimit'}, actor=self.actor)
        self.assertEqual((item.old_applicant_id, item.old_designee_id), ('E', 'E'))
        self.assertEqual(model('h_Employee').objects.count(), 2)

    def test_station_fabric_copy_keeps_explicit_null_and_duplicate_records(self):
        previous = create('GWName', FabricKindID='FAB', GWName='SAME')
        for _ in range(2):
            item = services.write(model('GWName'), {'_entry': 'GWNameZC', '_entry_copy_from': previous, 'old_gwname': 'SAME'}, actor=self.actor)
            self.assertEqual(item.old_fabric_kind_id, 'FAB')
        item = services.write(model('GWName'), {'_entry': 'GWNameZC', '_entry_copy_from': previous, 'old_fabric_kind_id': None}, actor=self.actor)
        self.assertIsNone(item.old_fabric_kind_id)
        self.assertEqual(model('GWName').objects.count(), 4)

    def test_twisting_master_detail_copy_and_explicit_quantity(self):
        head = services.write(model('ProdIn'), {'_entry': 'TwistingIn', 'old_sheet_series': 'TIN', 'old_sheet_no': 'TIN'}, actor=self.actor)
        previous = create('ProdInRecord', InPacks=2, InRolls=3, PackBag=Decimal('1.5'), SheetSeries='OTHER')
        item = services.write(model('ProdInRecord'), {'source_parent_1': head, '_entry_copy_from': previous, 'old_weight_qty': -5, 'old_in_packs': None}, actor=self.actor)
        self.assertEqual(item.entry_name, 'TwistingInRecord')
        self.assertEqual(item.old_sheet_series, 'TIN')
        self.assertIsNone(item.old_in_packs)
        self.assertEqual((item.old_in_rolls, item.old_pack_bag), (3, Decimal('1.5')))
        self.assertEqual(item.old_weight_qty, -5)
        self.assertEqual(item.old_real_qty, -5)
        head.refresh_from_db()
        self.assertEqual((head.old_weight_qty, head.old_rolls), (-5, 3))
        book = model('ProdStockBook').objects.get(old_sheet_series='TIN')
        self.assertEqual((book.old_in_weight_qty, book.old_in_rolls), (-5, 3))
        item = services.write(type(item), {'old_weight_qty': None, 'old_in_rolls': -2}, item, actor=self.actor)
        self.assertEqual(item.old_real_qty, 0)
        head.refresh_from_db()
        self.assertIsNone(head.old_weight_qty)
        self.assertEqual(head.old_rolls, -2)
        book = model('ProdStockBook').objects.get(old_sheet_series='TIN')
        self.assertIsNone(book.old_in_weight_qty)
        self.assertEqual(book.old_in_rolls, -2)

    def prepare_adjustment(self):
        quote = create('Quote', SheetSeries='Q', SheetNo='QN', CustomerID='C')
        line = create('QuoteDetail', Width=1, Weight=1, PriceUnit=1, SheetSeries='Q', DetailNo='QD', ColorNum='X123', Price=10)
        duplicate = create('QuoteDetail', Width=1, Weight=1, PriceUnit=1, SheetSeries='OTHER', DetailNo='QD', ColorNum='X123', Price=20)
        head = services.write(model('PriceAdjust'), {'_entry': 'PriceAdjust', 'old_sheet_series': 'A', 'old_sheet_no': 'A', 'old_adjust_money': 2, 'old_start_date': at(2), 'old_date_type': 1}, actor=self.actor)
        return (quote, line, duplicate, head)

    def test_duplicate_transfers_reverse_in_original_order_and_keep_all_records(self):
        from plugins.erp_base.source_execution_state import active
        quote, line, other, head = self.prepare_adjustment()
        first = quote_to_price_adjustment(line, quote, head, self.actor)
        second = quote_to_price_adjustment(line, quote, head, self.actor)
        reverse_quote_adjustment(second, self.actor, at(3), '第二次转单撤回', reader)
        for row in [line, other]:
            row.refresh_from_db()
            self.assertEqual(row.old_adjust_price, 12)
            self.assertEqual(row.old_job_sheet_no, first.old_detail_no)
        reverse_quote_adjustment(first, self.actor, at(3), '第一次转单撤回', reader)
        for row in [line, other]:
            row.refresh_from_db()
            self.assertIsNone(row.old_adjust_price)
            self.assertIsNone(row.old_job_sheet_no)
            self.assertEqual(row.old_date_type, 1)
            self.assertEqual(row.old_start_date, at(2))
        self.assertEqual(model('PriceAdjustDetail').objects.count(), 2)
        self.assertEqual(active(model('PriceAdjustDetail').objects.all()).count(), 0)
        self.assertEqual(model('QuoteDetail').objects.count(), 2)
        with self.assertRaises(ValidationError):
            reverse_quote_adjustment(first, self.actor, at(3), '重复撤回', reader)
        with self.assertRaises(ValidationError):
            services.delete_documents(model('PriceAdjustDetail').objects.filter(pk=first.pk), self.actor)

    def test_reverse_api_and_failure_rolls_back_retention_and_writeback(self):
        quote, line, other, head = self.prepare_adjustment()
        created = quote_to_price_adjustment(line, quote, head, self.actor)
        path = '/api/system/erp_sales_sourcedyepriceadjustdetail/' + str(created.pk) + '/phase6_reverse_quote_adjustment/'
        data = {'at': at(3).isoformat(), 'reason': '撤回转单'}
        with patch('plugins.erp_base.source_sales_services.removed', side_effect=ValidationError('回写失败')):
            result = self.client.post(path, data, format='json')
        self.assertEqual(result.status_code, 400, result.data)
        context = SourceDocumentContext.objects.get(entity=created._meta.label, object_id=created.pk)
        self.assertNotIn('transfer_retained', context.effects)
        line.refresh_from_db()
        self.assertEqual(line.old_adjust_price, 12)
        result = self.client.post(path, data, format='json')
        self.assertEqual(result.status_code, 200, result.data)
        line.refresh_from_db()
        self.assertIsNone(line.old_adjust_price)

    def test_purchase_arrival_reverse_only_selected_duplicate_line_via_api(self):
        from plugins.erp_base.source_phase6_transfers import purchase_to_arrival
        from plugins.erp_base.source_execution_state import active
        head = services.write(model('ArrivalNotice'), {'_entry': 'ArrivalNotice', 'old_sheet_series': 'A', 'old_sheet_no': 'A'}, actor=self.actor)
        original = create('PurDetail', DetailNo='D', FabricID='F', Qty=-3, Price=2)
        result = purchase_to_arrival(head, [original, original], self.actor)
        target = model('ArrivalNoticeDetail')
        first, second = list(target.objects.order_by('pk'))
        response = self.client.post('/api/system/' + target._meta.label_lower.replace('.', '_') + '/' + str(first.pk) + '/phase6_reverse_line_transfer/', {'at': at(3).isoformat(), 'reason': '撤回其中一条'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(target.objects.count(), 2)
        self.assertEqual(list(active(target.objects.all()).values_list('pk', flat=True)), [second.pk])
        self.assertEqual(model('PurDetail').objects.count(), 1)

    def test_department_purchase_reversal_preserves_both_kinds_and_repeated_transfers(self):
        from plugins.erp_base.source_phase6_transfers import department_apply_to_purchase, reverse_line_transfer
        from plugins.erp_base.source_execution_state import active
        for prefix in ['Article', 'Stuff']:
            application = create(prefix + 'DeptApply', SheetSeries=prefix, SheetNo=prefix)
            original = create(prefix + 'DeptApplyDetail', SheetSeries=prefix, DetailNo='D', Unit='箱', **{prefix + 'ID': 'A'})
            head = services.write(model(prefix + 'PurMain'), {'_entry': prefix + 'PurMain', 'old_sheet_series': prefix, 'old_sheet_no': prefix}, actor=self.actor)
            first = department_apply_to_purchase(original, application, head, Decimal('-2'), Decimal('3'), self.actor)
            second = department_apply_to_purchase(original, application, head, None, None, self.actor)
            reverse_line_transfer(first, self.actor, at(3), '撤回', reader)
            self.assertFalse(active(model('PurDetail').objects.filter(pk=first.pk)).exists())
            self.assertTrue(active(model('PurDetail').objects.filter(pk=second.pk)).exists())
        self.assertEqual(model('PurDetail').objects.count(), 4)

    def test_care_issue_approve_reopen_cancel_and_reapprove_excludes_retained_line(self):
        from plugins.erp_base.source_phase6_transfers import care_plan_to_article_out, reverse_line_transfer
        head = services.write(model('ArticleOut'), {'_entry': 'ArticleOut', 'old_sheet_series': 'O', 'old_sheet_no': 'O'}, actor=self.actor)
        original = create('MachineCarePlanDetail', SheetSeries='PLAN', ArticleID='A')
        article = create('p_Article', ArticleID='A', Unit='件')
        first = care_plan_to_article_out(original, head, article, Decimal('-2'), Decimal('3'), None, None, self.actor)
        second = care_plan_to_article_out(original, head, article, Decimal('5'), Decimal('4'), None, None, self.actor)
        head = services.approve(head, self.actor)
        self.assertEqual(sorted(model('ArticleStockBook').objects.values_list('old_out_qty', flat=True)), [-2, 5])
        with self.assertRaises(ValidationError):
            reverse_line_transfer(first, self.actor, at(3), '审核中撤回', reader)
        head = services.reopen(head, self.actor, '撤回一条转单')
        reverse_line_transfer(first, self.actor, at(3), '撤回负数原行', reader)
        services.approve(head, self.actor)
        self.assertEqual(list(model('ArticleStockBook').objects.values_list('old_out_qty', flat=True)), [5])
        self.assertEqual(model('ArticleOutDetail').objects.count(), 2)

    def test_quote_order_reverse_keeps_head_children_and_original_open_card_block(self):
        from plugins.erp_base.source_phase6_transfers import quote_to_order, reverse_head_transfer
        from plugins.erp_base.source_execution_state import active
        quote, line, _, _ = self.prepare_adjustment()
        first = quote_to_order(line, quote, 'F', self.actor)
        second = quote_to_order(line, quote, 'F', self.actor)
        detail = model('OrderColor').objects.get(source_parent_1=first)
        allocation = create('JobCombineOrder', CheckNo=detail.old_check_no, OrderSheetNo=first.old_sheet_no)
        with self.assertRaises(ValidationError):
            reverse_head_transfer(first, self.actor, at(3), '已有开卡', reader)
        allocation.delete()
        reverse_head_transfer(first, self.actor, at(3), '撤回第一张', reader)
        self.assertEqual(model('OrderMain').objects.count(), 2)
        self.assertEqual(model('OrderColor').objects.count(), 2)
        self.assertEqual(list(active(model('OrderMain').objects.all()).values_list('pk', flat=True)), [second.pk])
        self.assertFalse(active(model('OrderColor').objects.filter(pk=detail.pk)).exists())

    def test_purchase_product_reverse_preserves_new_ledger_snapshot_and_original_delete_progress(self):
        from plugins.erp_base.source_phase6_transfers import purchase_to_product
        from plugins.erp_base.source_execution_state import active
        purchase = create('PurMain', SheetSeries='P', SheetNo='P')
        line = create('PurDetail', SheetSeries='P', DetailNo='D', Qty=Decimal('-4'), Rolls=2)
        head = purchase_to_product(line, purchase, 'weight', 18, 1, 'W', 'C', 'P', self.actor)
        job = create('JobSheet', SheetSeries='J', SheetNo='J', PreRolls=2)
        process = create('JobProcess', SheetSeries='J', ProcessNo='1', ProcessID='GX99', StartTime=at(2), WPWorker='E')
        head = services.write(type(head), {'old_job_sheet_no': 'J'}, head, actor=self.actor)
        job.refresh_from_db()
        self.assertTrue(job.old_is_prod_in_finished)
        self.assertEqual(model('ProdStockBook').objects.filter(old_sheet_series=head.old_sheet_series).count(), 1)
        path = '/api/system/' + head._meta.label_lower.replace('.', '_') + '/' + str(head.pk) + '/phase6_reverse_head_transfer/'
        data = {'at': at(3).isoformat(), 'reason': '撤回采购入库'}
        with patch('plugins.erp_base.source_phase5_triggers.removed', side_effect=ValidationError('删除回写失败')):
            result = self.client.post(path, data, format='json')
        self.assertEqual(result.status_code, 400, result.data)
        self.assertTrue(active(type(head).objects.filter(pk=head.pk)).exists())
        self.assertEqual(model('ProdStockBook').objects.filter(old_sheet_series=head.old_sheet_series).count(), 1)
        result = self.client.post(path, data, format='json')
        self.assertEqual(result.status_code, 200, result.data)
        self.assertTrue(type(head).objects.filter(pk=head.pk).exists())
        self.assertFalse(active(type(head).objects.filter(pk=head.pk)).exists())
        self.assertFalse(model('ProdStockBook').objects.filter(old_sheet_series=head.old_sheet_series).exists())
        context = SourceDocumentContext.objects.get(entity=head._meta.label, object_id=head.pk)
        self.assertEqual(len(context.effects['transfer_retained']['stock_before']), 1)
        process.refresh_from_db()
        self.assertIsNone(process.old_start_time)
        self.assertIsNone(process.old_wpworker)
        job.refresh_from_db()
        self.assertFalse(job.old_is_prod_in_finished)
