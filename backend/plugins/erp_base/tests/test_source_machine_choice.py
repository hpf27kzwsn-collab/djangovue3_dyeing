from datetime import datetime,timedelta
from django.test import TestCase,SimpleTestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.source_machine_choice import choices,entered_machine,split_machines
from plugins.erp_base.source_package_operations import reader


class MachineSplitTests(SimpleTestCase):
    def test_original_empty_internal_and_trailing_segments(self):
        self.assertEqual(split_machines(None),[]);self.assertEqual(split_machines('   '),[])
        self.assertEqual(split_machines(' M ; ;N;; '),['M','','N',''])


class MachineChoiceTests(TestCase):
    def setUp(self):
        self.at=timezone.make_aware(datetime(2026,10,1,8))
        self.job=self.old('JobSheet','erp_production',SheetSeries='J',SheetNo='JOB',StereotypesName='M#')
        self.machine=self.old('PMachine',MachineID='M',KindName='K',StationID='06',IsStop=True)
        self.process=self.old('PProcess',ProcessID='P',StationID='06')
        self.person=self.old('PShiftEmp',SerialNumber='E',ShiftID='S',EmpID='E',MachineID='M;')

    def old(self,name,module='erp_base',**values):
        model=reader(name,module).model
        return model.objects.create(**{model.SOURCE_FIELDS[k]:v for k,v in values.items()})

    def choose(self,**params):
        return choices(**{'number':'JOB','shift':'S','employee':'E','process':'P','as_of':self.at,**params})

    def work(self,number='W',**values):
        return self.old('WProcess','erp_production',**{'WProcessNo':number,'JobSheetNo':'JOB','MachineID':'M','StationID':'06','ProcessID':'GX07',
            'StartTime':self.at-timedelta(days=1),'CreateDate':self.at-timedelta(days=1),'DyeState':'3','RightStatus':10,**values})

    def test_inactive_machine_still_selected_when_original_rules_allow(self):
        self.assertEqual([r['MachineID'] for r in self.choose()['rows']],['M'])

    def test_recent_busy_then_latest_released_controls_selection(self):
        self.work(DyeState='1');self.assertEqual(self.choose()['rows'],[])
        self.work('NEW',StartTime=self.at,DyeState='7');self.assertEqual(len(self.choose()['rows']),1)

    def test_null_state_not_excluded_by_not_in(self):
        self.work(DyeState=None);self.assertEqual(len(self.choose()['rows']),1)

    def test_exact_30_day_start_is_outside_recent_busy_window(self):
        self.work(StartTime=self.at-timedelta(days=30),DyeState='1')
        self.assertEqual(len(self.choose()['rows']),1)

    def test_reprint_pending_is_based_on_last_create_not_last_start(self):
        self.work(DyeState='5',RightStatus=0,StartTime=self.at-timedelta(days=90))
        self.assertEqual(self.choose()['rows'],[])
        self.work('LATEST',CreateDate=self.at,DyeState='5',RightStatus=10,StartTime=self.at-timedelta(days=90))
        self.assertEqual(len(self.choose()['rows']),1)

    def test_null_machine_in_reprint_not_in_excludes_every_candidate(self):
        self.work(MachineID=None,DyeState='5',RightStatus=None)
        r=self.choose();self.assertEqual(r['rows'],[])
        self.assertIn('NULL',r['supplemental_rows'][0]['issue'])

    def test_station06_null_employee_machine_list_is_not_unrestricted(self):
        self.person.old_machine_id=None;self.person.save()
        self.assertEqual(self.choose()['rows'],[])

    def test_other_station_null_and_aa_are_unrestricted_but_empty_is_not(self):
        self.process.old_station_id='05';self.process.save();self.machine.old_station_id='05';self.machine.save()
        for value,count in [(None,1),('AA',1),('',0),(' M ;M;',1)]:
            self.person.old_machine_id=value;self.person.save()
            self.assertEqual(len(self.choose()['rows']),count,value)

    def test_schedule_kind_overrides_machine_inferred_from_job(self):
        self.old('ProcessSchedule','erp_production',ID=1,JobSheetNo='JOB',StereotypesName='OTHER')
        r=self.choose();self.assertEqual(r['rows'],[]);self.assertEqual(r['summary']['StereotypesName'],'OTHER')

    def test_empty_job_machine_text_reports_original_negative_left_length(self):
        self.job.old_stereotypes_name='';self.job.save()
        r=self.choose();self.assertTrue(r['blocked']);self.assertEqual(r['rows'],[])

    def test_latest_scalar_employee_candidate_not_union_of_machine_lists(self):
        self.old('PShiftEmp',SerialNumber='LAST',EmpID='E',ShiftID='S',MachineID='OTHER')
        r=self.choose();self.assertEqual(r['rows'],[])
        self.assertEqual(len([x for x in r['seed_rows'] if x['table']=='p_ShiftEmp']),2)

    def test_entered_machine_first_nonblank_gx07_or_last_job_prefix(self):
        self.job.old_stereotypes_name='ABCDEF';self.job.save()
        self.assertEqual(entered_machine('JOB')['rows'][0]['MachineID'],'ABC')
        self.work('EMPTY',MachineID=' ');self.work('FIRST',MachineID='FIRST');self.work('SECOND',MachineID='SECOND')
        r=entered_machine('JOB');self.assertEqual(r['rows'][0]['MachineID'],'FIRST');self.assertEqual(len(r['candidate_rows']),2)

    def test_machine_list_overflow_original_split_column_is_explicit(self):
        self.person.old_machine_id='A'*201;self.person.save()
        self.assertTrue(self.choose()['blocked'])

    def test_api_machine_actions(self):
        actor=Users.objects.create_superuser(username='machine-tests',password='test')
        client=APIClient();client.force_authenticate(actor)
        root=f'/api/system/erp_production_sourcedyejobsheet/{self.job.pk}/'
        r=client.post(root+'entered_machine/',{},format='json');self.assertEqual(r.status_code,200,r.data)
        r=client.post(root+'process_machines/',{'shift':'S','employee':'E','process':'P','as_of':self.at.isoformat()},format='json')
        self.assertEqual(r.status_code,200,r.data);self.assertEqual(len(r.data['data']['rows']),1)
