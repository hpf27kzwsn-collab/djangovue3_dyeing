from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base import source_services as services
from plugins.erp_base.source_context import SourceDocumentContext
from plugins.erp_sales.source_models import SourceDyeOrderMain, SourceDyeOrderColor
from plugins.erp_base.source_models import SourceDyeLeaveClass1


class SourceEntryCreationTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='entry-creator', password='test-password')
        self.client = APIClient(); self.client.force_authenticate(self.actor)

    def test_order_entry_generates_its_two_distinct_original_number_prefixes(self):
        response = self.client.post('/api/system/erp_sales_sourcedyeordermain/', {'_entry': 'OrderMain'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        row = SourceDyeOrderMain.objects.get(pk=response.data['data']['id'])
        date = timezone.localtime().strftime('%y%m%d')
        self.assertEqual(row.old_sheet_series, 'K' + date + '001')
        self.assertEqual(row.old_sheet_no, 'K#' + date + '001')
        self.assertIsNone(row.legacy_id)
        self.assertEqual(SourceDocumentContext.objects.get(entity=row._meta.label, object_id=row.pk).entry_name, 'OrderMain')
        other = services.write(SourceDyeOrderMain, {'_entry': 'OrderMain'}, actor=self.actor)
        self.assertEqual(other.old_sheet_series, 'K' + date + '002')

    def test_explicit_original_number_and_null_are_not_overwritten(self):
        row = services.write(SourceDyeOrderMain, {'_entry': 'OrderMain', 'old_sheet_series': 'MANUAL',
            'old_sheet_no': None, 'old_sheet_date': None}, actor=self.actor)
        self.assertEqual(row.old_sheet_series, 'MANUAL')
        self.assertIsNone(row.old_sheet_no)
        self.assertIsNone(row.old_sheet_date)

    def test_child_inherits_declared_entry_and_existing_order_number(self):
        root = services.write(SourceDyeOrderMain, {'_entry': 'OrderMain'}, actor=self.actor)
        child = services.write(SourceDyeOrderColor, {'source_parent_1': root}, actor=self.actor)
        self.assertEqual(child.old_sheet_series, root.old_sheet_series)
        self.assertEqual(SourceDocumentContext.objects.get(entity=child._meta.label, object_id=child.pk).entry_name, 'OrderColor')
        self.assertIsNotNone(child.old_check_no)
        self.assertIsNone(child.legacy_id)

    def test_latest_sql_identity_seed_is_999_for_leave_class(self):
        row = services.write(SourceDyeLeaveClass1, {}, actor=self.actor)
        self.assertEqual(row.old_leave_id, 999)
        next_row = services.write(SourceDyeLeaveClass1, {}, actor=self.actor)
        self.assertEqual(next_row.old_leave_id, 1000)

    def test_large_parent_picker_uses_remote_query_in_metadata(self):
        response = self.client.get('/api/meta/erp_base_sourcedyezrevisiondetail/')
        self.assertEqual(response.status_code, 200, response.data)
        related = [field for field in response.data['data']['fields'] if field['key'].startswith('source_parent_')]
        self.assertTrue(related)
        self.assertTrue(all(field['remote'] is not None and field['options'] == [] for field in related))

    def test_local_prefixed_number_keeps_shift_prefix_and_independent_sequence(self):
        from plugins.erp_base.source_models import SourceDyePShift
        for entry, prefix in [('p_ShiftRB', 'D'), ('p_ShiftSC', 'B'), ('p_ShiftZJ', 'Q')]:
            first = services.write(SourceDyePShift, {'_entry': entry}, actor=self.actor)
            second = services.write(SourceDyePShift, {'_entry': entry}, actor=self.actor)
            self.assertEqual(first.old_shift_id, prefix + '001')
            self.assertEqual(second.old_shift_id, prefix + '002')
