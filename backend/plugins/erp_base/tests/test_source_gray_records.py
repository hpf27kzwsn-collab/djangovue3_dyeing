from plugins.erp_base.tests.source_fixtures import historical_batch
from django.apps import apps
from django.test import TestCase
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base import source_services as services
from plugins.erp_base.source_context import SourceDocumentContext

class OriginalGrayRecordsTests(TestCase):

    def setUp(self):
        self.actor = Users.objects.create_superuser(username='gray-records', password='test')
        self.model = lambda table, module='erp_warehouse': apps.get_model(module + '.SourceDye' + table)

    def test_receipt_actual_unit_updates_each_tag_without_rewriting_old_identity(self):
        head = services.write(self.model('GrayIn'), {'_entry': 'GrayIn', 'old_stock_unit': 1}, actor=self.actor)
        line = services.write(self.model('GrayInDetail'), {'source_parent_1': head, 'old_rece_sheet_no': 'R01'}, actor=self.actor)
        tag = self.model('GrayInRecord').objects.create(source_parent_1=line, old_rece_sheet_no='R01', old_roll_no='01', old_gunit=2, source_batch=historical_batch())
        services.write(type(line), {'old_weight_qty': 10}, line, self.actor)
        tag.refresh_from_db()
        self.assertEqual(tag.old_gunit, 1)
        self.assertEqual(tag.source_batch_id, historical_batch().pk)

    def test_removing_actual_return_changes_each_related_job_and_keeps_other_jobs(self):
        jobs = self.model('JobSheet', 'erp_production')
        job = jobs.objects.create(old_sheet_series='JOB-1', old_sheet_no='JOB-1', source_batch=historical_batch())
        other = jobs.objects.create(old_sheet_series='JOB-2', old_sheet_no='JOB-2', old_sheet_status=1)
        head = services.write(self.model('GrayOut'), {'_entry': 'GrayOut', 'old_sheet_kind': 29}, actor=self.actor)
        line = services.write(self.model('GrayOutDetail'), {'source_parent_1': head, 'old_assigned_no': 'RETURN-1', 'old_job_sheet_series': 'JOB-1', 'old_rolls': 2}, actor=self.actor)
        services.delete_documents(self.model('GrayOut').objects.filter(pk=head.pk), self.actor)
        job.refresh_from_db()
        other.refresh_from_db()
        self.assertEqual(job.old_curr_process_id, '退仓待处理')
        self.assertEqual(job.old_sheet_status, 9)
        self.assertEqual(job.source_batch_id, historical_batch().pk)
        self.assertEqual(other.old_sheet_status, 1)
        self.assertFalse(type(line).objects.filter(pk=line.pk).exists())

    def test_api_deletes_selected_new_master_and_owned_lines_as_one_document(self):
        head = services.write(self.model('GrayOut'), {'_entry': 'GrayOut'}, actor=self.actor)
        line = services.write(self.model('GrayOutDetail'), {'source_parent_1': head, 'old_assigned_no': 'DELETE-1', 'old_rolls': -2}, actor=self.actor)
        client = APIClient()
        client.force_authenticate(self.actor)
        response = client.delete(f'/api/system/erp_warehouse_sourcedyegrayout/{head.pk}/')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertFalse(type(head).objects.filter(pk=head.pk).exists())
        self.assertFalse(type(line).objects.filter(pk=line.pk).exists())
        self.assertFalse(self.model('GrayStockBook').objects.exists())

    def test_historical_child_stays_and_whole_deletion_rolls_back(self):
        head = services.write(self.model('GrayOut'), {'_entry': 'GrayOut'}, actor=self.actor)
        line = services.write(self.model('GrayOutDetail'), {'source_parent_1': head, 'old_assigned_no': 'KEEP-1', 'old_rolls': -2}, actor=self.actor)
        line.source_batch = historical_batch()
        line.save(update_fields=['source_batch'])
        client = APIClient()
        client.force_authenticate(self.actor)
        response = client.delete(f'/api/system/erp_warehouse_sourcedyegrayout/{head.pk}/')
        self.assertEqual(response.status_code, 400, response.data)
        self.assertTrue(type(head).objects.filter(pk=head.pk).exists())
        self.assertTrue(type(line).objects.filter(pk=line.pk).exists())
        self.assertEqual(self.model('GrayStockBook').objects.get().old_out_rolls, -2)

    def test_duplicate_barcode_rolls_use_actual_outgoing_receipt_and_roll(self):
        receipt = self.model('GrayIn').objects.create(old_sheet_series='GIN-01')
        line = self.model('GrayInDetail').objects.create(source_parent_1=receipt, old_sheet_series='GIN-01', old_rece_sheet_no='R01')
        tags = [self.model('GrayInRecord').objects.create(source_parent_1=line, old_rece_sheet_no='R01', old_roll_no=roll, old_bar_code='SAME-TAG', source_batch=historical_batch()) for roll in ['01', '02']]
        job = self.model('JobSheet', 'erp_production').objects.create(old_sheet_series='JOB-SERIES', old_sheet_no='JOB-01')
        allocated = self.model('JobGrayRecord', 'erp_production').objects.create(source_parent_1=job, old_sheet_series='JOB-SERIES', old_roll_no='01', old_rece_sheet_no='R01', old_gray_bar_code='SAME-TAG')
        head = services.write(self.model('GrayOut'), {'_entry': 'GrayOut', 'old_sheet_kind': 21}, actor=self.actor)
        outgoing = services.write(self.model('GrayOutDetail'), {'source_parent_1': head, 'old_assigned_no': 'OUT-1', 'old_rece_sheet_no': 'R01', 'old_job_sheet_no': 'JOB-01'}, actor=self.actor)
        services.write(self.model('GrayOutRecord'), {'source_parent_1': outgoing, 'old_roll_no': '01', 'old_bar_code': 'SAME-TAG'}, actor=self.actor)
        services.approve(head, self.actor)
        tags[0].refresh_from_db()
        tags[1].refresh_from_db()
        allocated.refresh_from_db()
        self.assertEqual(tags[0].old_assigned_no, 'OUT-1')
        self.assertEqual(tags[0].old_job_sheet_no, 'JOB-SERIES')
        self.assertIsNone(tags[1].old_assigned_no)
        self.assertEqual(allocated.old_assigned_no, 'OUT-1')
        self.assertEqual(tags[0].source_batch_id, historical_batch().pk)
        services.reopen(head, self.actor, '反审出库')
        tags[0].refresh_from_db()
        self.assertEqual(tags[0].old_assigned_no, 'OUT-1')
        self.assertEqual(SourceDocumentContext.objects.get(entity=head._meta.label, object_id=head.pk).effects['gray_record_unresolved'], [])
