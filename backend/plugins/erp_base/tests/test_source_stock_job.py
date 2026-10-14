from django.apps import apps
from django.test import TestCase
from system.models import Users
from plugins.erp_base import source_services as services


class OriginalStockJobTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='stock-job', password='test-password')
        self.job_model = apps.get_model('erp_production.SourceDyeJobSheet')
        self.jobs = [self.job_model.objects.create(old_sheet_series='OLD-J' + str(index), old_sheet_no='J' + str(index),
            legacy_id='OLD-J' + str(index)) for index in [1, 2]]

    def test_gray_job_receipt_assignments_follow_actual_approval_and_each_job_total(self):
        assignment = apps.get_model('erp_production.SourceDyeJobAssign')
        allocations = [assignment.objects.create(source_parent_1=job, old_sheet_series=job.old_sheet_series,
            old_assign_no=index, old_rece_sheet_no='R' + str(index)) for index, job in enumerate(self.jobs, 1)]
        head = services.write(apps.get_model('erp_warehouse.SourceDyeGrayOut'), {'_entry': 'GrayOutJob',
            'old_sheet_series': 'GRAY-OUT', 'old_sheet_no': 'GRAY-OUT', 'old_sheet_kind': 21, 'old_stock_unit': 1}, actor=self.actor)
        detail = apps.get_model('erp_warehouse.SourceDyeGrayOutDetail')
        for index in [1, 2]:
            services.write(detail, {'source_parent_1': head, 'old_assigned_no': 'OUT-A' + str(index),
                'old_job_sheet_no': 'J' + str(index), 'old_rece_sheet_no': 'R' + str(index),
                'old_rolls': index, 'old_weight_qty': index * 3, 'old_packs': 1}, actor=self.actor)
        for index, job in enumerate(self.jobs, 1):
            job.refresh_from_db(); self.assertEqual(job.old_sum_assigned_rolls, index)
            self.assertEqual(job.old_curr_process_id, '胚纱出库')
            self.assertEqual(job.legacy_id, 'OLD-J' + str(index))
        services.confirm(head, self.actor); services.approve(head, self.actor)
        for row in allocations:
            row.refresh_from_db(); self.assertEqual(int(row.old_status), 1)
        services.reopen(head, self.actor, '修订配纱')
        for row in allocations:
            row.refresh_from_db(); self.assertEqual(int(row.old_status), 0)

    def test_semi_job_uses_current_save_hook_name_and_keeps_null_totals(self):
        head = services.write(apps.get_model('erp_warehouse.SourceDyeSemiOut'), {'_entry': 'SemiOutJob',
            'old_sheet_series': 'SEMI-OUT', 'old_sheet_no': 'SEMI-OUT', 'old_sheet_kind': 21}, actor=self.actor)
        services.write(apps.get_model('erp_warehouse.SourceDyeSemiOutDetail'), {'source_parent_1': head,
            'old_assigned_no': 'SEMI-A', 'old_detail_no': 'SEMI-D', 'old_job_sheet_no': 'J1'}, actor=self.actor)
        self.jobs[0].refresh_from_db()
        self.assertEqual(self.jobs[0].old_curr_process_id, '发纱出库')
        self.assertIsNone(self.jobs[0].old_sum_assigned_rolls)
