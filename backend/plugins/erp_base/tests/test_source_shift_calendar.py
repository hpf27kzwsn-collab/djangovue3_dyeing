from datetime import datetime,timedelta
from django.test import TestCase,SimpleTestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.source_shift_calendar import calendar_plan,select_shift,preview,generate,resolve,undo,lookup
from plugins.erp_base.source_package_operations import reader,effect
from plugins.erp_base.source_quality_reports import rows
from plugins.erp_base.source_services import write,delete_documents


DATE=datetime(2026,10,1)


def config(id=1,**values):
    return {'record_id':id,'ID':id,'BeginDate':DATE,'CycleDays':'1天','Mode':'3',
        **{f'{p}{n:02}':'' for n in range(1,4) for p in ['ShiftID','ClassID','DateBetween']},
        'ShiftID01':'甲班','ClassID01':'早','DateBetween01':'07:50-19:50',
        'ShiftID02':'乙班','ClassID02':'晚','DateBetween02':'19:50-07:50',**values}


def detail(id=1,**values):
    data=config(id);data.pop('CycleDays');data.pop('Mode')
    return {**data,'CurrDate':DATE,**{f'{p}04':'' for p in ['ShiftID','ClassID','DateBetween']},**values}


class CalendarCalculationTests(SimpleTestCase):
    def test_first_day_null_previous_and_next_day_carries_night(self):
        r=calendar_plan([config()],[],2)
        self.assertFalse(r['blocked']);a,b=r['rows']
        self.assertIsNone(a['ShiftID02']);self.assertEqual(b['ShiftID02'],'乙班')
        self.assertEqual(a['DateBetween04'],'19:50-23:59:59')
        self.assertEqual(a['DateBetween02'],'00:00-07:50')

    def test_midnight_seed_uses_last_nonempty_third_slot(self):
        old=config(9,BeginDate=DATE-timedelta(days=1),ShiftID03='丙班',ClassID03='中')
        r=calendar_plan([old,config(DateBetween01='00:00-08:00',DateBetween02='08:00-16:00')],[],1)
        self.assertEqual(r['rows'][0]['ShiftID01'],'丙班')
        self.assertEqual(r['rows'][0]['ClassID01'],'中')

    def test_three_cross_midnights_overwrite_fourth_and_carry_in_order(self):
        r=calendar_plan([config(ShiftID03='丙班',DateBetween01='20:00-06:00',DateBetween02='21:00-07:00',DateBetween03='22:00-08:00')],[],1)['rows'][0]
        self.assertIsNone(r['ShiftID01']);self.assertEqual(r['ShiftID02'],'甲班')
        self.assertEqual(r['ShiftID03'],'乙班');self.assertEqual(r['ShiftID04'],'丙班')

    def test_cycles_follow_original_id_and_duration(self):
        r=calendar_plan([config(2,CycleDays='2天'),config(1,CycleDays='1天')],[],7)
        self.assertEqual([x['config_id'] for x in r['rows']],[1,2,2,1,2,2,1])

    def test_numeric_cycle_excluded_from_sum_but_in_cursor(self):
        r=calendar_plan([config(1,CycleDays='2'),config(2,CycleDays='1天')],[],3)
        self.assertEqual(r['summary']['AllDays'],1)
        self.assertEqual([x['config_id'] for x in r['rows']],[1,1,1])

    def test_zero_invalid_overflow_are_explicit_without_dummy_rows(self):
        for value in ['0天','abc天','2147483648天']:
            with self.subTest(value=value):
                r=calendar_plan([config(CycleDays=value)],[],2)
                self.assertTrue(r['blocked']);self.assertTrue(r['supplemental_rows'])

    def test_null_cycle_propagates_and_no_hit_keeps_day_indices(self):
        r=calendar_plan([config(1,CycleDays=None),config(2,CycleDays='1天')],[],2)
        self.assertFalse(r['blocked']);self.assertEqual(r['rows'],[])
        self.assertEqual(len(r['supplemental_rows']),2)

    def test_null_zero_negative_create_days_still_retires_new_version(self):
        for days in [None,0,-2]:
            r=calendar_plan([config()],[detail(BeginDate=DATE-timedelta(days=5))],days)
            self.assertEqual(r['retired_ids'],[1]);self.assertEqual(r['rows'],[])

    def test_group_selection_is_not_global_max_date(self):
        r=calendar_plan([config()],[detail(1,CurrDate=DATE+timedelta(days=100)),detail(2,CurrDate=DATE+timedelta(days=2))],1)
        self.assertEqual(r['rows'][0]['ID'],3)
        self.assertEqual(r['rows'][0]['CurrDate'],DATE+timedelta(days=3))
        self.assertEqual(len(r['candidate_rows']),2)

    def test_group_max_date_and_original_id_reuse_for_version_change(self):
        a=detail(8,BeginDate=DATE-timedelta(days=5));b=detail(8,record_id=9,CurrDate=DATE+timedelta(days=2),BeginDate=DATE-timedelta(days=5))
        r=calendar_plan([config()],[a,b],1)
        self.assertEqual(r['candidate_rows'][0]['CurrDate'],b['CurrDate'])
        self.assertEqual(r['retired_ids'],[8,9]);self.assertEqual(r['rows'][0]['ID'],8)

    def test_null_last_begin_restarts_without_old_sql_delete(self):
        r=calendar_plan([config()],[detail(BeginDate=None,CurrDate=DATE+timedelta(days=2))],1)
        self.assertEqual(r['retired_ids'],[]);self.assertEqual(r['rows'][0]['CurrDate'],DATE)

    def test_negative_remainder_matches_sql_not_python(self):
        r=calendar_plan([config(CycleDays='7天')],[detail(CurrDate=DATE-timedelta(days=2))],1)
        self.assertEqual(r['rows'][0]['CycRemain'],-1)

    def test_empty_config_and_null_dates_preserved_without_generation(self):
        self.assertEqual(calendar_plan([],[],2)['rows'],[])
        self.assertFalse(calendar_plan([config(BeginDate=None)],[],1)['blocked'])

    def pick(self,details,time,shifts=None,machines=None,departments=None):
        return select_shift(details,time,'M',
            machines if machines is not None else [{'record_id':1,'MachineID':'M','DeptID':'D'}],
            departments if departments is not None else [{'record_id':1,'DeptID':'D'}],
            shifts if shifts is not None else [{'record_id':1,'ShiftID':'S','DeptID':'D','Name':'染色甲班','ClassID':'BASE'}])

    def test_boundary_inclusive_start_exclusive_end(self):
        d=detail(DateBetween02='');self.assertEqual(len(self.pick([d],DATE.replace(hour=7,minute=50))['rows']),1)
        self.assertEqual(self.pick([d],DATE.replace(hour=19,minute=50))['rows'],[])

    def test_later_matching_slot_wins_and_class_from_master(self):
        d=detail(ShiftID04='甲班',ClassID04='DIFFERENT',DateBetween04='09:00-23:59:59')
        r=self.pick([d],DATE.replace(hour=23,minute=59,second=59))
        self.assertEqual(r['rows'][0]['ClassID'],'BASE');self.assertEqual(r['rows'][0]['ClassName'],'甲班')
        self.assertEqual(r['result_rows'][3]['DateEnd'],'59:59')

    def test_datetime_parameter_rounds_into_next_day(self):
        r=self.pick([detail(CurrDate=DATE+timedelta(days=1),DateBetween01='00:00-07:50')],DATE.replace(hour=23,minute=59,second=59,microsecond=999000))
        self.assertEqual(len(r['rows']),1);self.assertEqual(r['result_rows'][0]['GatherHM'],'00:00')

    def test_same_day_last_project_row_and_no_deduplication(self):
        depts=[{'record_id':1,'DeptID':'D'},{'record_id':2,'DeptID':'d '}]
        r=self.pick([detail(2),detail(1,ShiftID01='乙班')],DATE.replace(hour=8),departments=depts)
        self.assertEqual(len(r['rows']),2);self.assertEqual(r['candidate_rows'][-1]['record_id'],2)

    def test_wildcard_pattern_and_inactive_machine_not_filtered(self):
        r=self.pick([detail(ShiftID01='[甲乙]班')],DATE.replace(hour=8),machines=[{'record_id':1,'MachineID':'m ','DeptID':'D','IsStop':True}])
        self.assertEqual(len(r['rows']),1)

    def test_missing_department_and_null_shift_name_are_retained(self):
        r=self.pick([detail()],DATE.replace(hour=8),departments=[])
        self.assertEqual(r['rows'],[]);self.assertTrue(r['supplemental_rows'])
        r=self.pick([detail()],DATE.replace(hour=8),shifts=[])
        self.assertFalse(r['blocked']);self.assertEqual(r['rows'],[]);self.assertTrue(r['supplemental_rows'])

    def test_null_time_requests_one_generation_but_matches_no_day(self):
        self.assertTrue(self.pick([detail()],None)['needs_generation'])


class CalendarServiceTests(TestCase):
    def setUp(self):
        self.actor=Users.objects.create_superuser(username='calendar-tests',password='test')
        self.at=timezone.make_aware(DATE);self.client=APIClient();self.client.force_authenticate(self.actor)
        self.config=self.old('PShiftArrange',config())

    def old(self,name,values):
        model=reader(name,'erp_base').model
        data={field:timezone.make_aware(values[n]) if isinstance(values[n],datetime) else values[n] for n,field in model.SOURCE_FIELDS.items() if n in values}
        return model.objects.create(**data)

    def run_generation(self,days=2,item=None):
        return generate(item or self.config,days,self.actor,self.at,'测试原日历')

    def test_generate_and_undo_retains_rows_and_does_not_invent_legacy_id(self):
        report=self.run_generation();self.assertEqual(len(report['rows']),2)
        self.assertEqual(rows('PShiftArrangeDetail','erp_base').count(),2)
        self.assertFalse(reader('PShiftArrangeDetail','erp_base').exclude(source_batch=None).exists())
        undo(self.config,self.actor,self.at,'撤回')
        self.assertEqual(rows('PShiftArrangeDetail','erp_base').count(),0)
        self.assertEqual(reader('PShiftArrangeDetail','erp_base').count(),2)

    def test_version_replace_zero_days_and_restore_original(self):
        item=self.old('PShiftArrangeDetail',detail(BeginDate=DATE-timedelta(days=1)))
        self.run_generation(0);self.assertTrue(effect(item,'calendar_retained')['active'])
        undo(self.config,self.actor,self.at,'撤回');self.assertEqual(rows('PShiftArrangeDetail','erp_base').count(),1)

    def test_blocked_generation_is_atomic_and_preserves_original(self):
        old=self.old('PShiftArrangeDetail',detail(BeginDate=DATE-timedelta(days=1)))
        self.config.old_cycle_days='0天';self.config.save()
        with self.assertRaises(ValidationError):self.run_generation()
        self.assertIsNone(effect(old,'calendar_retained'));self.assertEqual(rows('PShiftArrangeDetail','erp_base').count(),1)

    def test_scope_cannot_partially_generate(self):
        self.old('PShiftArrange',config(2))
        def limited(name,module):
            q=reader(name,module)
            return q.filter(pk=self.config.pk) if name=='PShiftArrange' else q
        with self.assertRaises(ValidationError):generate(self.config,1,self.actor,self.at,'测试',query=limited)
        self.assertEqual(reader('PShiftArrangeDetail','erp_base').count(),0)

    def test_missing_date_only_generates_365_once_even_still_missing(self):
        r=resolve(self.config,self.at+timedelta(days=800),'M',self.actor,self.at,'测试')
        self.assertTrue(r['needs_generation']);self.assertEqual(len(r['generation']['rows']),365)
        self.assertEqual(rows('PShiftArrangeDetail','erp_base').count(),365)

    def test_existing_date_does_not_generate(self):
        self.old('PShiftArrangeDetail',detail())
        r=resolve(self.config,self.at,'M',self.actor,self.at,'测试')
        self.assertNotIn('generation',r);self.assertIsNone(effect(self.config,'calendar_generation'))

    def test_cross_anchor_reverse_requires_latest_generation_first(self):
        machine=self.old('PMachine',{'MachineID':'M'})
        self.run_generation(1);self.run_generation(1,item=machine)
        with self.assertRaises(ValidationError):undo(self.config,self.actor,self.at,'过早撤回')
        undo(machine,self.actor,self.at,'撤回后次');undo(self.config,self.actor,self.at,'撤回前次')
        self.assertEqual(rows('PShiftArrangeDetail','erp_base').count(),0)

    def test_same_anchor_repeated_generation_and_reverse(self):
        self.run_generation(1);self.run_generation(1)
        undo(self.config,self.actor,self.at,'后次');self.assertEqual(rows('PShiftArrangeDetail','erp_base').count(),1)
        undo(self.config,self.actor,self.at,'前次');self.assertEqual(rows('PShiftArrangeDetail','erp_base').count(),0)

    def test_edited_or_retained_rows_not_silently_overwritten(self):
        self.run_generation(1);row=rows('PShiftArrangeDetail','erp_base').get()
        row.old_shift_id01='修改';row.save()
        with self.assertRaises(ValidationError):undo(self.config,self.actor,self.at,'撤回')
        row.old_shift_id01='甲班';row.save();undo(self.config,self.actor,self.at,'撤回')
        with self.assertRaises(ValidationError):write(type(row),{'old_shift_id01':'再改'},row,actor=self.actor)
        with self.assertRaises(ValidationError):delete_documents(type(row).objects.filter(pk=row.pk),self.actor)

    def test_api_preview_generation_lookup_reverse(self):
        root='/api/system/erp_base_sourcedyepshiftarrange/'
        def post(path,data):
            result=self.client.post(root+path,data,format='json');self.assertEqual(result.status_code,200,result.data);return result.data['data']
        self.assertEqual(len(post('preview_calendar/',{'create_days':2})['rows']),2)
        post(f'{self.config.pk}/generate_calendar/',{'create_days':2,'at':self.at.isoformat(),'reason':'测试'})
        r=post('lookup_shift/',{'curr_time':self.at.isoformat(),'machine':'M'});self.assertFalse(r['needs_generation'])
        post(f'{self.config.pk}/resolve_shift/',{'curr_time':self.at.isoformat(),'machine':'M','at':self.at.isoformat(),'reason':'测试'})
        post(f'{self.config.pk}/undo_calendar/',{'at':self.at.isoformat(),'reason':'撤回'})
        self.assertEqual(rows('PShiftArrangeDetail','erp_base').count(),0)
