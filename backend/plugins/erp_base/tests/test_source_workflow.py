from plugins.erp_base.tests.source_fixtures import historical_batch
from django.apps import apps
from django.test import TestCase
from system.models import Users
from plugins.erp_base import source_services as services
from plugins.erp_base.source_context import SourceBusinessParameter


class OriginalJobWorkflowTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='original-workflow', password='test-password')
        self.parameter = SourceBusinessParameter.objects.create(name='JobReProdIn', value='3')
        self.job_model = apps.get_model('erp_production.SourceDyeJobSheet')
        self.job = services.write(self.job_model, {'_entry': 'JobSheet', 'old_sheet_series': 'JOB-1',
            'old_sheet_no': 'J-1', 'old_pre_rolls': 4}, actor=self.actor)

    def test_process_order_progress_and_removal_use_actual_status(self):
        process = apps.get_model('erp_production.SourceDyeJobProcess')
        last = services.write(process, {'source_parent_1': self.job, 'old_process_no': 2,
            'old_process_id': 'GX02', 'old_status': '0'}, actor=self.actor)
        first = services.write(process, {'source_parent_1': self.job, 'old_process_no': 1,
            'old_process_id': 'GX01', 'old_status': '0'}, actor=self.actor)
        self.job.refresh_from_db()
        self.assertEqual(self.job.old_job_kind_id, '01')
        # 原无完成工序分支TOP 1没有ORDER BY；项目明确按原行承接顺序采用。
        self.assertEqual(self.job.old_next_process_id, 'GX02')
        services.write(process, {'old_status': '1'}, first, self.actor)
        self.job.refresh_from_db()
        self.assertEqual(self.job.old_curr_process_id, 'GX01')
        self.assertEqual(self.job.old_next_process_id, 'GX02')
        services.write(process, {'old_status': '1'}, last, self.actor)
        self.job.refresh_from_db(); self.assertIsNone(self.job.old_next_process_id)
        services.delete(process.objects.filter(pk=last.pk), self.actor)
        self.job.refresh_from_db(); self.assertEqual(self.job.old_curr_process_id, 'GX01')

    def receipt(self, series, quantity, kind=11):
        return services.write(apps.get_model('erp_warehouse.SourceDyeProdIn'), {'_entry': 'ProdInEdit',
            'old_sheet_series': series, 'old_sheet_no': series, 'old_job_sheet_no': 'J-1',
            'old_rolls': quantity, 'old_sheet_kind': kind}, actor=self.actor)

    def test_current_parameter_three_uses_total_rolls_including_signed_returns(self):
        first = self.receipt('IN-1', 3)
        self.job.refresh_from_db(); self.assertFalse(self.job.old_is_prod_in_finished)
        second = self.receipt('IN-2', 1)
        self.job.refresh_from_db(); self.assertTrue(self.job.old_is_prod_in_finished)
        returned = self.receipt('RETURN', -1, 16)
        self.job.refresh_from_db(); self.assertFalse(self.job.old_is_prod_in_finished)
        services.delete(type(returned).objects.filter(pk=returned.pk), self.actor)
        self.job.refresh_from_db(); self.assertTrue(self.job.old_is_prod_in_finished)
        services.delete(type(second).objects.filter(pk=second.pk), self.actor)
        self.job.refresh_from_db(); self.assertFalse(self.job.old_is_prod_in_finished)

    def test_parameter_one_uses_actual_approval_and_over_receipt_condition(self):
        self.parameter.value = '1'; self.parameter.save(update_fields=['value'])
        first = self.receipt('IN-1', 3)
        self.job.refresh_from_db(); self.assertFalse(self.job.old_is_prod_in_finished)

        services.confirm(first, self.actor); services.approve(first, self.actor)
        self.job.refresh_from_db(); self.assertTrue(self.job.old_is_prod_in_finished)
        second = self.receipt('IN-2', 2)
        self.job.refresh_from_db(); self.assertFalse(self.job.old_is_prod_in_finished)
        services.delete(type(second).objects.filter(pk=second.pk), self.actor)
        returned = self.receipt('RETURN', -1, 16)
        services.confirm(returned, self.actor); services.approve(returned, self.actor)
        self.job.refresh_from_db(); self.assertFalse(self.job.old_is_prod_in_finished)

    def test_null_parameter_value_and_absent_parameter_follow_distinct_original_branches(self):
        self.parameter.value = None; self.parameter.save(update_fields=['value'])
        first = self.receipt('IN-1', 4)
        self.job.refresh_from_db(); self.assertFalse(self.job.old_is_prod_in_finished)
        self.parameter.delete()
        services.write(type(first), {'old_rolls': 4}, first, self.actor)
        self.job.refresh_from_db(); self.assertTrue(self.job.old_is_prod_in_finished)

    def test_new_receipt_updates_existing_legacy_job_without_erasing_its_identity(self):
        self.job.source_batch=historical_batch(); self.job.save(update_fields=['source_batch'])
        self.receipt('IN-1', 4)
        self.job.refresh_from_db()
        self.assertTrue(self.job.old_is_prod_in_finished)
        self.assertEqual(self.job.source_batch_id, historical_batch().pk)
