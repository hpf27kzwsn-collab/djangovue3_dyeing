from plugins.erp_base.tests.source_fixtures import historical_batch
from datetime import datetime, date
from decimal import Decimal
from django.apps import apps
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base import source_services as services
from plugins.erp_base.document_services import save_document
from plugins.erp_base.source_sales_services import numeric_color


class OriginalSalesLinksTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='sales-links', password='test')

    def model(self, table, module='erp_sales'):
        return apps.get_model(module + '.SourceDye' + table)

    def write(self, table, **data):
        return services.write(self.model(table), data, actor=self.actor)

    def quote(self, **data):
        return self.model('QuoteDetail').objects.create(old_width=0, old_weight=0, old_price_unit=0, **data)

    def test_order_changes_reach_every_job_and_only_sql_update_columns(self):
        head = self.write('OrderMain', old_sheet_series='ORDER1', old_sheet_no='ORDER1', old_customer_id='CUS1')
        line = self.write('OrderColor', source_parent_1=head, old_check_no='CHECK1', old_order_qty=10)
        combos = [self.model('JobCombineOrder', 'erp_production').objects.create(
            old_sheet_series='JOB' + str(i), old_check_no='check1 ', old_color_remarks='old',
            old_order_qty=99, source_batch=historical_batch()) for i in [1, 2]]
        original_batches = {combo.pk: combo.source_batch_id for combo in combos}
        jobs = [self.model('JobSheet', 'erp_production').objects.create(
            old_sheet_series='JOB' + str(i), old_sheet_no='JN' + str(i), old_check_no='CHECK1',
            old_pre_rolls=99, old_prod_id='KEEP', source_batch=historical_batch()) for i in [1, 2]]
        tags = [self.model('GrayMaterialDetail', 'erp_warehouse').objects.create(
            old_detail_no='G' + str(i), old_job_sheet_no='JN' + str(i)) for i in [1, 2]]
        self.model('JobCombineOrder', 'erp_production').objects.create(
            old_sheet_series='JOB1', old_check_no='CHECK0', old_color_remarks='前色')
        services.write(type(line), {'old_order_qty': Decimal('-3.5'), 'old_remarks': None,
            'old_color_remarks': '<用途&>', 'old_cust_fabric_name': '客户品名'}, line, self.actor)
        services.write(type(head), {'old_customer_id': 'CUS2', 'old_cust_self_no': 'PO2'}, head, self.actor)
        for job, combo, tag in zip(jobs, combos, tags):
            job.refresh_from_db(); combo.refresh_from_db(); tag.refresh_from_db()
            self.assertEqual(job.old_customer_id, 'CUS2')
            self.assertEqual(job.old_prod_id, 'KEEP')  # 未提交 ProdID 不回写。
            self.assertEqual(job.old_pre_rolls, 99)  # 订单量不伪造工卡计划量。
            self.assertEqual(job.old_cust_self_product, '客户品名')
            self.assertEqual(combo.old_order_qty, Decimal('-3.5'))
            self.assertEqual(combo.old_cust_self_no, 'PO2')
            self.assertEqual(combo.source_batch_id, original_batches[combo.pk])
        self.assertEqual(tags[0].old_color_remarks, '前色,<用途&>')
        self.assertEqual(tags[1].old_color_remarks, '<用途&>')

    def test_historical_source_save_does_not_replay_new_order_trigger(self):
        head = self.model('OrderMain').objects.create(old_sheet_series='OLD', source_batch=historical_batch())
        self.model('OrderColor').objects.create(old_sheet_series='OLD', old_check_no='CHECK')
        job = self.model('JobSheet', 'erp_production').objects.create(old_sheet_series='J', old_check_no='CHECK', old_customer_id='KEEP')
        services.write(type(head), {'old_customer_id': 'NEW'}, head, self.actor)
        job.refresh_from_db()
        self.assertEqual(job.old_customer_id, 'KEEP')

    def test_order_delete_checks_original_codes_even_without_extra_foreign_key(self):
        head = self.write('OrderMain', old_sheet_series='O', old_sheet_no='ORDER')
        line = self.write('OrderColor', source_parent_1=head, old_check_no='CHECK')
        self.model('JobCombineOrder', 'erp_production').objects.create(
            old_sheet_series='JOB', old_check_no='check ', old_order_sheet_no='order ')
        with self.assertRaisesMessage(ValidationError, '不能删除'):
            services.delete_documents(type(head).objects.filter(pk=head.pk), self.actor)
        self.assertTrue(type(line).objects.filter(pk=line.pk).exists())

    def test_expiry_is_selected_action_and_does_not_close_unrelated_history(self):
        at = timezone.make_aware(datetime(2024, 1, 1))
        old = self.model('OrderMain').objects.create(old_sheet_series='OLD', old_sheet_date=at, source_batch=historical_batch())
        head = self.write('OrderMain', old_sheet_series='NEW', old_sheet_date=at)
        old.refresh_from_db(); self.assertIsNone(old.old_sheet_status)
        client = APIClient(); client.force_authenticate(self.actor)
        response = client.post(f'/api/system/erp_sales_sourcedyeordermain/{head.pk}/close_expired/',
                               {'as_of': '2024-06-29'}, format='json')
        self.assertEqual(response.status_code, 400)  # 正好180天不结单。
        response = client.post(f'/api/system/erp_sales_sourcedyeordermain/{head.pk}/close_expired/',
                               {'as_of': '2024-06-30'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        head.refresh_from_db(); old.refresh_from_db()
        self.assertEqual(head.old_sheet_status, 10)
        self.assertIsNone(old.old_sheet_status)

    def test_expiry_permission_key_matches_page_and_non_admin_can_use_granted_action(self):
        from system.actions import resource_actions
        from system.views import view_for
        from system.models import Role, Menu, MenuButton, RoleMenuButtonPermission
        entity = 'erp_sales_sourcedyeordermain'
        model = self.model('OrderMain')
        actions = resource_actions(entity, view_for(entity, model))
        key, title, verb, path = next(row for row in actions if row[0] == 'close_expired-post')
        menu, _ = Menu.objects.get_or_create(component_name=entity, defaults={'name': '订单'})
        button, _ = MenuButton.objects.get_or_create(value=entity + ':' + key,
            defaults={'name': title, 'menu': menu, 'method': verb, 'api': path})
        role = Role.objects.create(key='expiry-operator', name='订单结单员')
        user = Users.objects.create_user(username='expiry-operator', password='test')
        user.role.add(role)
        RoleMenuButtonPermission.objects.create(role=role, menu_button=button, data_range=3)
        head = self.write('OrderMain', old_sheet_series='PERMISSION', old_sheet_date=timezone.make_aware(datetime(2024, 1, 1)))
        client = APIClient(); client.force_authenticate(user)
        response = client.post(f'/api/system/{entity}/{head.pk}/close_expired/', {'as_of': '2024-06-30'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        head.refresh_from_db(); self.assertEqual(head.old_sheet_status, 10)

    def test_adjustment_save_audit_and_reopen_have_distinct_original_scopes(self):
        first = self.quote(old_detail_no='Q1', old_color_num='A12-3', source_batch=historical_batch())
        other = self.quote(old_detail_no='Q2', old_color_num='B123', source_batch=historical_batch())
        unrelated = self.quote(old_detail_no='Q3', old_color_num='A124', old_adjust_price=99)
        at = timezone.make_aware(datetime(2026, 10, 1))
        head = self.write('PriceAdjust', old_sheet_series='ADJ1', old_start_date=at, old_date_type='1')
        self.write('PriceAdjustDetail', source_parent_1=head, old_detail_no='D1', old_quote_detail_no='Q1', old_color_num='123', old_adjust_price=Decimal('-2.50'))
        for quote in [first, other]:
            quote.refresh_from_db(); self.assertEqual(quote.old_adjust_price, Decimal('-2.50'))
            self.assertEqual(quote.old_job_sheet_no, 'D1')
        services.confirm(head, self.actor); services.approve(head, self.actor)
        services.reopen(head, self.actor, '测试反审')
        first.refresh_from_db(); other.refresh_from_db(); unrelated.refresh_from_db()
        self.assertEqual(first.old_adjust_price, 0)
        self.assertEqual(timezone.localtime(first.old_start_date).date(), date(1900, 1, 1))
        self.assertEqual(first.old_date_type, 0)
        self.assertEqual(first.old_job_sheet_no, 'D1')
        self.assertEqual(first.source_batch_id, historical_batch().pk)
        self.assertEqual(other.old_adjust_price, Decimal('-2.50'))
        self.assertEqual(unrelated.old_adjust_price, 99)

    def test_adjustment_delete_uses_remaining_latest_date_but_keeps_date_fields(self):
        quote = self.quote(old_detail_no='Q', old_color_num='A99')
        heads = [self.write('PriceAdjust', old_sheet_series='A' + str(i), old_start_date=timezone.make_aware(datetime(2026, i, 1))) for i in [1, 2]]
        lines = [self.write('PriceAdjustDetail', source_parent_1=head, old_detail_no='D' + str(i),
                            old_color_num='99', old_adjust_price=i) for i, head in enumerate(heads, 1)]
        services.delete(type(lines[1]).objects.filter(pk=lines[1].pk), self.actor)
        quote.refresh_from_db()
        self.assertEqual(quote.old_adjust_price, 1)
        self.assertEqual(quote.old_job_sheet_no, 'D1')
        self.assertEqual(timezone.localtime(quote.old_start_date).month, 2)
        services.delete(type(lines[0]).objects.filter(pk=lines[0].pk), self.actor)
        quote.refresh_from_db(); self.assertIsNone(quote.old_adjust_price)
        self.assertIsNone(quote.old_job_sheet_no)

    def test_numeric_color_preserves_null_empty_and_ten_digit_truncation(self):
        self.assertIsNone(numeric_color(None))
        self.assertEqual(numeric_color('ABC'), '')
        self.assertEqual(numeric_color('A12345678901B'), '1234567890')
        from plugins.erp_base.source_sales_services import same_numeric_color
        values = [None, 'ABC', '', 'A12345678901B', 'X1234567890Z', 'A1234567899']
        for index, value in enumerate(values):
            self.quote(old_detail_no=str(index), old_color_num=value)
        query = self.model('QuoteDetail').objects.all()
        self.assertEqual(same_numeric_color(query, '无数字').count(), 2)
        self.assertEqual(same_numeric_color(query, '12345678902').count(), 2)
        self.assertFalse(same_numeric_color(query, None).exists())

    def test_confirm_only_reopen_keeps_saved_adjustment_and_header_change_waits_for_audit(self):
        quote = self.quote(old_detail_no='Q1', old_color_num='A1')
        at = timezone.make_aware(datetime(2026, 1, 1))
        later = timezone.make_aware(datetime(2026, 2, 1))
        head = self.write('PriceAdjust', old_sheet_series='A1', old_start_date=at)
        self.write('PriceAdjustDetail', source_parent_1=head, old_detail_no='D1', old_quote_detail_no='Q1', old_color_num='A1', old_adjust_price=2)
        services.write(type(head), {'old_start_date': later}, head, self.actor)
        quote.refresh_from_db(); self.assertEqual(quote.old_start_date, at)
        services.confirm(head, self.actor); services.reopen(head, self.actor, '只退确认')
        quote.refresh_from_db(); self.assertEqual(quote.old_adjust_price, 2)
        self.assertEqual(quote.old_start_date, at)
        services.confirm(head, self.actor); services.approve(head, self.actor)
        quote.refresh_from_db(); self.assertEqual(quote.old_start_date, later)

    def test_adjustment_same_day_and_null_dates_have_explicit_order(self):
        quote = self.quote(old_detail_no='Q1', old_color_num='A1')
        at = timezone.make_aware(datetime(2026, 1, 1))
        for index, when in enumerate([at, at, None, at], 1):
            head = self.write('PriceAdjust', old_sheet_series='A' + str(index), old_start_date=when)
            line = self.write('PriceAdjustDetail', source_parent_1=head, old_detail_no='D' + str(index),
                              old_color_num='A1', old_adjust_price=index)
        services.delete(type(line).objects.filter(pk=line.pk), self.actor)
        quote.refresh_from_db(); self.assertEqual(quote.old_job_sheet_no, 'D2')

    def test_whole_document_failure_rolls_back_upstream_and_downstream_changes(self):
        head = self.write('OrderMain', old_sheet_series='O')
        line = self.write('OrderColor', source_parent_1=head, old_check_no='CHECK', old_order_qty=5)
        combo = self.model('JobCombineOrder', 'erp_production').objects.create(old_sheet_series='J', old_check_no='CHECK', old_order_qty=5)
        with self.assertRaises(ValidationError):
            save_document(head, self.actor, {'old_customer_id': 'CHANGED'}, {type(line): {
                'upsert': [{'instance': line, 'data': {'old_order_qty': 9}}], 'delete': [99999999]}})
        head.refresh_from_db(); line.refresh_from_db(); combo.refresh_from_db()
        self.assertEqual(head.old_customer_id, '')
        self.assertEqual(line.old_order_qty, 5)
        self.assertEqual(combo.old_order_qty, 5)
