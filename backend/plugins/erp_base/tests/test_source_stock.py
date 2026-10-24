from plugins.erp_base.tests.source_fixtures import historical_batch
from django.test import TestCase
from django.apps import apps
from django.core.exceptions import ValidationError
from system.models import Users
from plugins.erp_base import source_services as services
from plugins.erp_base.source_context import SourceDocumentContext, SourceBusinessParameter
from plugins.erp_base import source_stock_services as stock
from plugins.erp_base.source_entry_registry import ENTRY_RULES
from plugins.erp_warehouse.source_models import SourceDyeStuffIn, SourceDyeStuffInDetail, SourceDyeStuffStockBook, SourceDyeProdIn, SourceDyeProdStockBook

class OriginalStockPostingTests(TestCase):

    def setUp(self):
        self.actor = Users.objects.create_superuser(username='native-stock', password='test-password')

    def test_saved_stuff_receipt_and_return_follow_original_sign_without_double_posting(self):
        head = services.write(SourceDyeStuffIn, {'_entry': 'StuffIn', 'old_sheet_kind': 16, 'old_ware_house_id': '13'}, actor=self.actor)
        line = services.write(SourceDyeStuffInDetail, {'source_parent_1': head, 'old_detail_no': 'RETURN-1', 'old_stuff_id': 'S1', 'old_qty': 2, 'old_amount': 6, 'old_price': 3}, actor=self.actor)
        book = SourceDyeStuffStockBook.objects.get()
        self.assertEqual(book.old_in_qty, -2)
        self.assertEqual(book.old_in_money, -6)
        self.assertIsNone(book.source_batch_id)
        services.write(type(line), {'old_qty': 3, 'old_amount': 9}, line, self.actor)
        self.assertEqual(SourceDyeStuffStockBook.objects.count(), 1)
        self.assertEqual(SourceDyeStuffStockBook.objects.get().old_in_qty, -3)
        services.approve(head, self.actor)
        services.reopen(head, self.actor, '修改退货明细')
        self.assertEqual(SourceDyeStuffStockBook.objects.count(), 1)
        services.delete(type(line).objects.filter(pk=line.pk), self.actor)
        self.assertFalse(SourceDyeStuffStockBook.objects.exists())

    def test_approval_mode_product_inbound_is_reversed_when_reopened(self):
        head = services.write(SourceDyeProdIn, {'_entry': 'ProdInEdit', 'old_sheet_series': 'PROD-IN', 'old_sheet_no': 'PROD-IN', 'old_rolls': -2, 'old_weight_qty': -10}, actor=self.actor)
        self.assertFalse(SourceDyeProdStockBook.objects.exists())
        head = services.approve(head, self.actor)
        self.assertEqual(head.old_right_status, 10)
        book = SourceDyeProdStockBook.objects.get()
        self.assertEqual(book.old_in_rolls, -2)
        self.assertEqual(book.old_in_weight_qty, -10)
        services.reopen(head, self.actor, '反审入库')
        self.assertFalse(SourceDyeProdStockBook.objects.exists())
        head.refresh_from_db()
        self.assertEqual(head.old_right_status, 0)

    def test_root_delete_cleans_only_its_new_effects_and_keeps_historical_book(self):
        historical = SourceDyeStuffStockBook.objects.create(old_book_no=5, source_batch=historical_batch(), old_in_qty=-20)
        head = services.write(SourceDyeStuffIn, {'_entry': 'StuffIn'}, actor=self.actor)
        services.write(SourceDyeStuffInDetail, {'source_parent_1': head, 'old_detail_no': 'ROW-1', 'old_stuff_id': 'S1', 'old_qty': 2, 'old_amount': 6}, actor=self.actor)
        services.delete(SourceDyeStuffInDetail.objects.filter(source_parent_1=head), self.actor)
        services.delete(SourceDyeStuffIn.objects.filter(pk=head.pk), self.actor)
        self.assertEqual(list(SourceDyeStuffStockBook.objects.values_list('pk', flat=True)), [historical.pk])
        self.assertFalse(SourceDocumentContext.objects.filter(entity=head._meta.label, object_id=head.pk).exists())

    def test_every_stock_family_uses_present_physical_columns_and_replaces_only_own_rows(self):
        details = {'StuffIn': 'StuffInDetail', 'StuffOut': 'StuffOutDetail', 'StuffStockAdjust': 'StuffStockAdjustDetail', 'ProdIn': None, 'ProdOut': 'ProdOutDetail', 'ProdStockAdjust': 'ProdStockAdjustDetail', 'ArticleIn': 'ArticleInDetail', 'ArticleOut': 'ArticleOutDetail', 'ArticleStockAdjust': 'ArticleStockAdjustDetail', 'GrayIn': 'GrayInDetail', 'GrayOut': 'GrayOutDetail', 'GrayStockAdjust': 'GrayStockAdjustDetail', 'GrayBalance': 'GrayBalanceDetail', 'GrayStockSpecUp': 'GrayStockSpecUpDetail', 'GrayStockAllot': None, 'SemiIn': 'SemiInDetail', 'SemiOut': 'SemiOutDetail', 'SemiStockAdjust': 'SemiStockAdjustDetail', 'SemiStockSpecUp': 'SemiStockSpecUpDetail'}
        expected_counts = {'GrayStockSpecUp': 2, 'GrayStockAllot': 2, 'SemiStockSpecUp': 2}
        for table, detail in details.items():
            with self.subTest(table=table):
                model = apps.get_model('erp_warehouse.SourceDye' + table)
                head = model.objects.create(old_right_status=10)
                if detail is not None:
                    child = apps.get_model('erp_warehouse.SourceDye' + detail)
                    values = {child.SOURCE_FIELDS[key]: 1 for key in ['AdjustRolls', 'AdjustQty', 'Qty', 'InQty', 'OutQty', 'Rolls', 'Packs', 'Piece', 'Amount', 'Total'] if key in child.SOURCE_FIELDS}
                    child.objects.create(source_parent_1=head, **values)
                entry = next(iter(ENTRY_RULES[model._meta.label]))
                context = SourceDocumentContext.objects.create(entity=model._meta.label, object_id=head.pk, entry_name=entry)
                stock.refresh(head, self.actor)
                context.refresh_from_db()
                self.assertEqual(sum(map(len, context.effects['stock_rows'].values())), expected_counts.get(table, 1))
                stock.refresh(head, self.actor)
                context.refresh_from_db()
                self.assertEqual(sum(map(len, context.effects['stock_rows'].values())), expected_counts.get(table, 1))
                stock.clear_effects(context, self.actor)

    def test_article_return_negates_original_value_instead_of_stuff_absolute_return(self):
        head = services.write(apps.get_model('erp_warehouse.SourceDyeArticleIn'), {'_entry': 'ArticleIn', 'old_sheet_kind': 16}, actor=self.actor)
        services.write(apps.get_model('erp_warehouse.SourceDyeArticleInDetail'), {'source_parent_1': head, 'old_in_qty': -2, 'old_total': -6}, actor=self.actor)
        book = apps.get_model('erp_warehouse.SourceDyeArticleStockBook').objects.get()
        self.assertEqual(book.old_in_qty, 2)
        self.assertEqual(book.old_in_money, 6)

    def test_stuff_allot_generates_both_documents_and_keeps_save_mode_after_reopen(self):
        SourceBusinessParameter.objects.create(name='CostMethodOfStuff', value='M')
        material = apps.get_model('erp_base.SourceDyePStuff').objects.create(old_stuff_id='S1', old_wof=2, old_price=2, source_batch=historical_batch())
        head = services.write(apps.get_model('erp_warehouse.SourceDyeStuffAllot'), {'_entry': 'StuffAllot', 'old_sheet_series': 'ALLOT-00000001', 'old_sheet_no': 'ALLOT-1', 'old_ware_house_id': '12', 'old_to_ware_house_id': '13'}, actor=self.actor)
        line = services.write(apps.get_model('erp_warehouse.SourceDyeStuffAllotDetail'), {'source_parent_1': head, 'old_detail_no': 'ALLOT-L1', 'old_stuff_id': 'S1', 'old_qty': 2, 'old_price': 3, 'old_amount': 6}, actor=self.actor)
        self.assertEqual(SourceDyeStuffStockBook.objects.count(), 2)
        material.refresh_from_db()
        self.assertIsNone(material.old_price)
        self.assertEqual(material.source_batch_id, historical_batch().pk)
        head = services.approve(head, self.actor)
        incoming = apps.get_model('erp_warehouse.SourceDyeStuffIn').objects.get(old_sheet_series='SR00000001')
        outgoing = apps.get_model('erp_warehouse.SourceDyeStuffOut').objects.get(old_sheet_series='TO00000001')
        self.assertEqual(incoming.old_sheet_kind, 15)
        self.assertEqual(outgoing.old_sheet_kind, 24)
        self.assertEqual(SourceDyeStuffStockBook.objects.get(old_book_kind=15).old_in_qty, 4)
        self.assertEqual(SourceDyeStuffStockBook.objects.get(old_book_kind=24).old_out_qty, 2)
        self.assertEqual(SourceDyeStuffStockBook.objects.count(), 2)
        with self.assertRaisesMessage(ValidationError, '请修改实际来源单据'):
            services.write(type(incoming), {'old_remarks': '不应绕过来源'}, incoming, self.actor)
        services.reopen(head, self.actor, '撤回调拨')
        self.assertEqual(SourceDyeStuffStockBook.objects.count(), 2)
        services.write(type(line), {'old_qty': 3}, line, self.actor)
        self.assertEqual(SourceDyeStuffStockBook.objects.get(old_book_kind=15).old_in_qty, 6)
        self.assertEqual(SourceDyeStuffStockBook.objects.get(old_book_kind=24).old_out_qty, 3)
        self.assertEqual(type(incoming).objects.count(), 1)
        self.assertEqual(type(outgoing).objects.count(), 1)
        self.assertTrue(type(line).objects.filter(pk=line.pk).exists())
