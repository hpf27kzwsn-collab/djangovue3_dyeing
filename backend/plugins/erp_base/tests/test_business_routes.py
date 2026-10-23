"""全部样本路线结构往返及各实际序列的末次报工联动；不冒充历史整单重放。"""
import json
from pathlib import Path
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from system.models import Users
from plugins.erp_base.source_phase3_operations import model
from plugins.erp_base.source_work_progress import refresh


class RouteGroupTests(TestCase):
    def test_all_17_plan_and_364_actual_sequences_keep_order_duplicates_and_null(self):
        cases=json.loads(Path(__file__).with_name('business_route_cases.json').read_text(encoding='utf8'))
        actor=Users.objects.create(username='all-route-groups',is_superuser=True);at=timezone.now()
        self.assertEqual(sum(c['id'].startswith('P') for c in cases),17)
        self.assertEqual(sum(c['id'].startswith('A') and c['id']!='A0000' for c in cases),364)
        for case in cases:
            with self.subTest(route=case['id']):
                code=case['id'];seq=case['sequence']
                job=model('JobSheet').objects.create(old_sheet_series=code,old_sheet_no=code)
                model('JobProcess').objects.bulk_create([model('JobProcess')(source_parent_1=job,old_sheet_series=code,
                    old_process_no=i,old_process_id=p,old_status='0') for i,p in enumerate(seq,1)])
                self.assertEqual(list(model('JobProcess').objects.filter(source_parent_1=job).order_by('old_process_no').values_list('old_process_id',flat=True)),seq)
                if not code.startswith('A'):continue
                works=[model('WProcess')(old_job_sheet_no=code,old_wprocess_no=code+'-'+str(i),old_process_no=i,old_process_id=p,
                    old_create_date=at+timedelta(seconds=i),old_start_time=at,old_end_time=at-timedelta(seconds=1),old_curr_kg=-1)
                    for i,p in enumerate(seq,1)]
                model('WProcess').objects.bulk_create(works)
                self.assertEqual(list(model('WProcess').objects.filter(old_job_sheet_no=code).order_by('old_process_no').values_list('old_process_id',flat=True)),seq)
                if works:
                    refresh(works[-1],actor)
                    plan=model('JobProcess').objects.get(source_parent_1=job,old_process_no=len(seq))
                    self.assertEqual(plan.old_status,'1' if seq[-1] is not None else '0')
                    self.assertEqual(model('WProcess').objects.filter(old_job_sheet_no=code).count(),len(seq))
                else:self.assertFalse(model('JobProcess').objects.filter(source_parent_1=job).exists())
