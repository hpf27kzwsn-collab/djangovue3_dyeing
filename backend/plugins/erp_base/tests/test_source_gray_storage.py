from plugins.erp_base.tests.source_fixtures import historical_batch
from django.apps import apps
from django.core.exceptions import ValidationError
from django.test import TestCase
from system.models import Users
from plugins.erp_base import source_services as services
from plugins.erp_base.source_context import SourceDocumentContext


class OriginalGrayStorageTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='gray-transfer', password='test')
        self.model = lambda table: apps.get_model('erp_warehouse.SourceDye' + table)
        self.receipt = self.model('GrayIn').objects.create(old_sheet_series='GIN-01', old_sheet_no='GIN-01',
            old_sheet_kind=11, old_customer_id='C01', old_ware_house_id='W01', source_batch=historical_batch())
        self.detail = self.model('GrayInDetail').objects.create(source_parent_1=self.receipt,
            old_sheet_series='GIN-01', old_rece_sheet_no='ABCDEF0001', old_gray_id='Y01',
            old_rolls=10, old_weight_qty=100, old_length_qty=200, old_storage_unit_ids='A01', source_batch=historical_batch())
        self.tag = self.model('GrayInRecord').objects.create(source_parent_1=self.detail,
            old_rece_sheet_no='ABCDEF0001', old_roll_no='01', old_bar_code='TAG-1',
            old_weight_qty=20, old_length_qty=40, old_dlv_qty=7, source_batch=historical_batch())
        self.book = self.model('GrayStockBook').objects.create(old_book_no=900,
            old_sheet_series='GIN-01', old_rece_sheet_no='ABCDEF0001', old_detail_no='ABCDEF0001',
            old_in_rolls=10, old_in_weight_qty=100, old_in_length_qty=200, source_batch=historical_batch())
        self.head = services.write(self.model('GrayStorageAdjust'), {'_entry': 'GrayStorageAdjust'}, actor=self.actor)
        self.line = services.write(self.model('GrayStorageAdjustDetail'), {'source_parent_1': self.head,
            'old_detail_no': 'MOVE-1', 'old_rece_sheet_no': 'ABCDEF0001', 'old_from_rece_sheet_no': 'ORIGINAL',
            'old_lot_no': 'GIN-01', 'old_to_storage_unit_ids': 'B02', 'old_to_area': 'B',
            'old_rolls': 2, 'old_weight_qty': 20, 'old_length_qty': 40}, actor=self.actor)
        services.write(self.model('GrayStorageAdjustRecord'), {'source_parent_1': self.line,
            'old_rece_sheet_no': 'TAG-1', 'old_roll_no': '01'}, actor=self.actor)

    def approve(self):
        self.head = services.confirm(self.head, self.actor)
        self.head = services.approve(self.head, self.actor)

    def test_actual_transfer_moves_tag_and_stock_and_reverse_restores_all_original_values(self):
        self.approve()
        self.detail.refresh_from_db(); self.book.refresh_from_db(); self.tag.refresh_from_db(); self.line.refresh_from_db()
        self.assertEqual(self.detail.old_rolls, 8)
        self.assertEqual(self.book.old_in_weight_qty, 80)
        split = self.model('GrayInDetail').objects.get(old_rece_sheet_no=self.line.old_spec)
        self.assertEqual(split.old_storage_unit_ids, 'B02')
        self.assertEqual(self.tag.source_parent_1_id, split.pk)
        self.assertEqual(self.tag.old_dlv_qty, 7)
        self.assertEqual(self.tag.source_batch_id, historical_batch().pk)
        self.assertIsNone(split.source_batch_id)
        self.assertEqual(self.model('GrayStockBook').objects.count(), 2)
        services.reopen(self.head, self.actor, '反审转仓')
        self.detail.refresh_from_db(); self.book.refresh_from_db(); self.tag.refresh_from_db(); self.line.refresh_from_db()
        self.assertEqual((self.detail.old_rolls, self.detail.old_weight_qty, self.detail.old_length_qty), (10, 100, 200))
        self.assertEqual(self.book.old_in_weight_qty, 100)
        self.assertEqual(self.tag.source_parent_1_id, self.detail.pk)
        self.assertEqual(self.tag.old_dlv_qty, 7)
        self.assertIsNone(self.line.old_spec)
        self.assertEqual(self.model('GrayInDetail').objects.count(), 1)
        self.assertEqual(self.model('GrayStockBook').objects.count(), 1)

    def test_second_approval_does_not_duplicate_prior_transfer(self):
        self.approve()
        services.reopen(self.head, self.actor, '调整后重审')
        self.head.refresh_from_db()
        services.write(type(self.line), {'old_weight_qty': 30}, self.line, self.actor)
        self.approve()
        self.detail.refresh_from_db()
        self.assertEqual(self.detail.old_weight_qty, 70)
        self.assertEqual(self.model('GrayInDetail').objects.count(), 2)
        self.assertEqual(self.model('GrayStockBook').objects.count(), 2)

    def test_following_change_requires_reversing_that_business_first(self):
        self.approve()
        self.book.old_in_weight_qty = 75
        self.book.save()
        with self.assertRaisesMessage(ValidationError, '后续业务'):
            services.reopen(self.head, self.actor, '已经发生下游改变')
        self.head.refresh_from_db()
        self.assertEqual(self.head.approval_stage, 'approved')

    def test_missing_receipt_keeps_draft_and_no_partial_side_effect(self):
        services.write(type(self.line), {'old_lot_no': 'MISSING'}, self.line, self.actor)
        services.confirm(self.head, self.actor)
        with self.assertRaisesMessage(ValidationError, '实际收料'):
            services.approve(self.head, self.actor)
        self.detail.refresh_from_db()
        self.assertEqual(self.detail.old_rolls, 10)
        self.assertEqual(self.model('GrayInDetail').objects.count(), 1)
        self.assertFalse(SourceDocumentContext.objects.get(entity=self.head._meta.label, object_id=self.head.pk).effects.get('gray_storage_changes'))

    def test_null_original_and_negative_movement_keep_old_arithmetic_and_reverse_null(self):
        self.detail.old_weight_qty = None
        self.detail.old_rolls = None
        self.detail.save()
        services.write(type(self.line), {'old_weight_qty': -20, 'old_rolls': -2}, self.line, self.actor)
        self.approve()
        self.detail.refresh_from_db(); self.line.refresh_from_db()
        split = self.model('GrayInDetail').objects.get(old_rece_sheet_no=self.line.old_spec)
        self.assertEqual(split.old_weight_qty, -20)
        self.assertIsNone(self.detail.old_rolls)
        self.assertEqual(self.detail.old_weight_qty, 0)  # 原ISNULL(WeightQty-转出量,0)
        services.reopen(self.head, self.actor, '撤销负数转移')
        self.detail.refresh_from_db()
        self.assertIsNone(self.detail.old_weight_qty)
        self.assertIsNone(self.detail.old_rolls)
