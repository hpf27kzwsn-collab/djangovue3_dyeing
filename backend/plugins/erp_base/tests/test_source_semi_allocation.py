from decimal import Decimal
from django.apps import apps
from django.test import TestCase
from system.models import Users
from plugins.erp_base import source_services as services
from plugins.erp_base.source_context import SourceDocumentContext


class OriginalSemiAllocationTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='semi-allocation', password='test-password')
        receipt = services.write(apps.get_model('erp_warehouse.SourceDyeSemiIn'), {'_entry': 'SemiIn',
            'old_sheet_series': 'SEMI-IN', 'old_sheet_no': 'SEMI-IN', 'old_sheet_kind': 11}, actor=self.actor)
        detail = services.write(apps.get_model('erp_warehouse.SourceDyeSemiInDetail'), {'source_parent_1': receipt,
            'old_rece_sheet_no': 'R-1', 'old_rolls': 10, 'old_weight_qty': 5}, actor=self.actor)
        incoming = apps.get_model('erp_warehouse.SourceDyeSemiInRecord')
        services.write(incoming, {'source_parent_1': detail, 'old_roll_no': '001', 'old_bar_code': 'SAME',
            'old_rolls': 4, 'old_weight_qty': 2, 'old_packs': 1}, actor=self.actor)
        services.write(incoming, {'source_parent_1': detail, 'old_roll_no': '002', 'old_bar_code': 'SAME',
            'old_rolls': 6, 'old_weight_qty': 3, 'old_packs': 1}, actor=self.actor)
        self.header = services.write(apps.get_model('erp_warehouse.SourceDyeSemiOut'), {'_entry': 'SemiOut',
            'old_sheet_series': 'SEMI-OUT', 'old_sheet_no': 'SEMI-OUT'}, actor=self.actor)
        self.detail = services.write(apps.get_model('erp_warehouse.SourceDyeSemiOutDetail'), {'source_parent_1': self.header,
            'old_assigned_no': 'A-1', 'old_detail_no': 'D-1', 'old_rece_sheet_no': 'R-1', 'old_rolls': 6,
            'old_weight_qty': 3}, actor=self.actor)

    def test_two_same_barcode_packages_remain_distinct_by_receipt_and_roll(self):
        records = apps.get_model('erp_warehouse.SourceDyeSemiOutRecord').objects.order_by('old_roll_no')
        self.assertEqual(records.count(), 2)
        rows = list(records)
        self.assertEqual([row.old_bar_code for row in rows], ['SAME', 'SAME'])
        self.assertEqual([row.old_roll_no for row in rows], ['001', '002'])
        self.assertEqual([row.old_rolls for row in rows], [4, 2])
        self.assertEqual([row.old_weight_qty for row in rows], [2, 1])
        self.assertEqual([row.old_packs for row in rows], [1, 0])
        book = apps.get_model('erp_warehouse.SourceDyeSemiStockBook').objects.get(old_book_kind=1)
        self.assertEqual(book.old_out_packs, 1)
        services.write(type(self.detail), {'old_rolls': 7}, self.detail, self.actor)
        self.assertEqual(records.count(), 2)
        self.assertEqual(sum(row.old_rolls for row in records.all()), 7)

    def test_detail_delete_clears_only_auto_records_and_rebuilds_stock(self):
        services.delete(type(self.detail).objects.filter(pk=self.detail.pk), self.actor)
        self.assertFalse(apps.get_model('erp_warehouse.SourceDyeSemiOutRecord').objects.exists())
        self.assertFalse(apps.get_model('erp_warehouse.SourceDyeSemiStockBook').objects.filter(old_book_kind=1).exists())
        self.assertEqual(apps.get_model('erp_warehouse.SourceDyeSemiInRecord').objects.count(), 2)

    def test_explicit_records_are_preserved_and_marked_instead_of_overwritten(self):
        outgoing = apps.get_model('erp_warehouse.SourceDyeSemiOutRecord')
        explicit = services.write(outgoing, {'source_parent_1': self.detail, 'old_sheet_series': 'SEMI-OUT',
            'old_assigned_no': 'A-1', 'old_roll_no': 'EXPLICIT', 'old_bar_code': 'SAME', 'old_rece_sheet_no': 'R-1',
            'old_rolls': Decimal('1.5'), 'old_weight_qty': Decimal('0.5'), 'old_packs': 0}, actor=self.actor)
        self.assertEqual(list(outgoing.objects.values_list('pk', flat=True)), [explicit.pk])
        context = SourceDocumentContext.objects.get(entity=self.header._meta.label, object_id=self.header.pk)
        self.assertEqual(context.effects['semi_allocation'][0]['mode'], 'explicit_records')
