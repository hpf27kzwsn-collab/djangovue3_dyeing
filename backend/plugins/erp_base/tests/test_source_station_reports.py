from datetime import datetime,timedelta
from decimal import Decimal
from django.apps import apps
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.source_station_quality import dye_rate,color_matching_dashboard,color_depth_dashboard,periods,ratio
from plugins.erp_base.source_station_yield import package_yield,work_quantity
from plugins.erp_base.source_station_schedule import existing_schedules,schedule_rank,process_status


class StationReportTests(TestCase):
    def setUp(self):
        self.at=timezone.make_aware(datetime(2026,8,15,12))
        self.actor=Users.objects.create_superuser(username='station-reports',password='test')
        self.client=APIClient();self.client.force_authenticate(self.actor)

    def old(self,name,module='erp_production',**values):
        item=apps.get_model(module+'.SourceDye'+name).objects.create(**values)
        item.refresh_from_db();return item

    def dye(self,**values):
        return self.old('DyeCheckout','erp_quality',**{'old_end_time':self.at,'old_process_id':'GX07',
            'old_days':'2026-08-15','old_tmonth':'2026-08','old_cloth_qty_kg':10,'old_tnum':2,'old_znum':1,'old_rnum':1,**values})

    def dictionary(self,kind,code,name):
        return self.old('PFieldValid','erp_base',old_field_type=kind,old_code=code,old_name=name)

    def package(self,**values):
        model=apps.get_model('erp_warehouse.SourceDyeRecordYield')
        return self.old('RecordYield','erp_warehouse',**{'old_guid':'G'+str(model.objects.count()),'old_roll_no':'1',
            'old_check_no':'C','old_job_sheet_no':'J','old_sheet_date':self.at,'old_emp_id':'E',
            'old_prod_id':'P','old_color_num':'C','old_net_kg':Decimal('2.00'),'old_rolls':1,**values})

    def test_rate_group_null_negative_total_and_original_ratio(self):
        a=self.dye(old_shift_id=None,old_class_id=None,old_znum=1,old_tnum=3,old_cloth_qty_kg=-2)
        self.dye(old_shift_id='S',old_class_id='03',old_tnum=0,old_znum=2,old_cloth_qty_kg=None)
        report=dye_rate(self.at,self.at)
        self.assertEqual(len(report['rows']),3)
        self.assertEqual(report['rows'][0]['Rate'],Decimal('33.3333333333300'))
        self.assertIsNone(report['rows'][1]['Rate']);self.assertIsNotNone(report['rows'][1]['ratio_issue'])
        self.assertEqual(report['rows'][-1]['TotalKg'],-2)
        self.assertIn(a.pk,report['rows'][-1]['source_ids'])

    def test_sql_decimal_division_truncates_before_percent_multiplication(self):
        self.assertEqual(ratio(22,135),Decimal('16.2962962962900'))

    def test_empty_and_inclusive_range_and_matching_jtimes(self):
        empty=dye_rate(self.at,self.at)
        self.assertEqual(len(empty['rows']),1);self.assertIsNone(empty['rows'][0]['TNum'])
        self.dye(old_jtimes=3);self.dye(old_end_time=self.at+timedelta(microseconds=1000))
        self.assertEqual(dye_rate(self.at,self.at,'matching')['rows'][-1]['JTimes'],3)

    def test_eight_oclock_boundary_and_month_rollover(self):
        at=timezone.make_aware(datetime(2026,3,1,7,59,59))
        self.assertEqual(periods(at)['today'],'2026-02-28')
        self.assertEqual(periods(at)['last'],'2026-01')
        self.assertEqual(periods(at+timedelta(seconds=1))['today'],'2026-03-01')

    def test_matching_employee_duplicate_missing_and_addition_source(self):
        for _ in range(2):self.old('HEmployee','erp_base',old_emp_id='E',old_name='同名')
        self.dye(old_color_matching='E');orphan=self.dye(old_color_matching='NO',old_cloth_qty_kg=-3)
        self.old('StuffWeight',old_sheet_series='S',old_sheet_kind=2,old_recipe_type=1,old_sheet_date=self.at,old_color_matching='E')
        self.old('StuffWeight',old_sheet_series='OTHER',old_sheet_kind=2,old_recipe_type=2,old_sheet_date=self.at,old_color_matching='E')
        result=color_matching_dashboard(self.at)
        today=next(row for row in result['rows'] if row['DayType']=='今日')
        self.assertEqual(today['TotalKg'],20);self.assertEqual(today['DyeAdd'],1)
        total=next(row for row in result['rows'] if row['DayType']=='本月总合计')
        self.assertEqual(total['TotalKg'],7)
        self.assertIn(orphan.pk,[row['record_id'] for row in result['supplemental_rows']])

    def test_matching_dashboard_stored_date_not_inferred_from_end(self):
        item=self.dye(old_days=None,old_tmonth=None)
        result=color_matching_dashboard(self.at)
        self.assertEqual(result['rows'],[])
        self.assertEqual(result['supplemental_rows'][0]['record_id'],item.pk)

    def test_matching_dashboard_returns_more_than_old_hundred_rows(self):
        for index in range(101):
            code=str(index);self.old('HEmployee','erp_base',old_emp_id=code,old_name=code);self.dye(old_color_matching=code)
        result=color_matching_dashboard(self.at)
        self.assertGreater(len(result['rows']),100)
        self.assertEqual(result['rows'][-1]['rowindex'],len(result['rows']))

    def test_depth_legacy_month_mismatch_and_explicit_corrected_month(self):
        self.dictionary('Class','03','甲班');self.dictionary('ColorDepth','01','浅色')
        self.dye(old_class_id='03',old_color_depth_id='01',old_tmonth='2026-07',old_days='2026-07-15')
        legacy=color_depth_dashboard(self.at)
        self.assertTrue(all(row['ShangYueZongHeJi'] is None for row in legacy['rows']))
        self.assertTrue(any(row['Type']=='上月ZongHeJi' for row in legacy['supplemental_rows']))
        fixed=color_depth_dashboard(self.at,'matched_month')
        self.assertEqual(next(row for row in fixed['rows'] if row['original_depth_code']=='01')['ShangYueZongHeJi'],10)

    def test_depth_duplicate_class_and_code_ten_collision_preserved(self):
        for _ in range(2):self.dictionary('Class','03','甲班')
        self.dictionary('ColorDepth','10','实际10')
        self.dye(old_class_id='03',old_color_depth_id='10')
        result=color_depth_dashboard(self.at)
        # 原字典连接两倍，深度10和总量10两路，再乘两条同名框架。
        self.assertEqual(next(row for row in result['rows'] if row['ColorDepthName']=='实际10')['JinRiJiaBan'],80)
        self.assertEqual(next(row for row in result['rows'] if row['ColorDepthName']=='汇总')['BenYueZongHeJi'],40)

    def test_depth_unknown_class_and_depth_retained(self):
        item=self.dye(old_class_id='X',old_color_depth_id='Z',old_cloth_qty_kg=-5)
        result=color_depth_dashboard(self.at)
        self.assertTrue(any(item.pk in row['source_ids'] for row in result['supplemental_rows']))
        self.assertEqual(result['rows'][0]['BenYueZongHeJi'],-5)

    def test_employee_package_duplicate_dictionary_and_null_sum(self):
        self.old('PGray','erp_base',old_gray_id='P',old_rskind='R')
        for _ in range(2):self.old('SDBComboValue','erp_base',old_combo_id='Z017',old_key_value='R',old_display_value='纱线')
        self.package(old_net_kg=None,old_rolls=None,old_cust_qty=None)
        row=package_yield(self.at,self.at)['rows'][0]
        self.assertEqual(row['Packs'],2);self.assertEqual(row['CustQty'],0)
        self.assertIsNone(row['NetKg']);self.assertIsNone(row['Rolls']);self.assertEqual(row['pinzhong'],'纱线')

    def test_package_multivalue_subquery_includes_outside_period_but_not_weight(self):
        self.package(old_color_id='A');self.package(old_color_id='B')
        outside=self.package(old_sheet_date=self.at-timedelta(days=100),old_color_id='C',old_net_kg=-99)
        result=package_yield(self.at,self.at)
        self.assertEqual(result['rows'][0]['ColorID'],'A;B;C');self.assertEqual(result['rows'][0]['NetKg'],4)
        self.assertEqual(result['supplemental_rows'][0]['record_id'],outside.pk)

    def test_package_null_group_not_merged_with_real_zero_and_null_correlation(self):
        self.package(old_emp_id=None,old_color_id='A');self.package(old_emp_id=None,old_color_id='B')
        self.package(old_emp_id='0',old_color_id='C')
        result=package_yield(self.at,self.at)
        self.assertEqual(len(result['rows']),2)
        null=next(row for row in result['rows'] if row['original_group']['EmpID'] is None)
        self.assertIsNone(null['ColorID']);self.assertEqual(null['EmpID'],'0')

    def test_winding_multiple_workers_names_and_duplicate_employee_all_preserved(self):
        self.package(old_winding_id='W',old_emp_id='A');self.package(old_winding_id='W',old_emp_id='B',old_net_kg=-1)
        for code,name in [('A','甲'),('A','丙'),('B','乙')]:self.old('HEmployee','erp_base',old_emp_id=code,old_name=name)
        result=package_yield(self.at,self.at,'winding')
        self.assertEqual(set(result['rows'][0]['EmpID'].split(';')),{'甲','乙','丙'})
        self.assertEqual(result['rows'][0]['NetKg'],1);self.assertEqual(len(result['supplemental_rows']),1)

    def test_package_non_numeric_exact_filter_and_source_range(self):
        self.package(old_emp_id='e-甲',old_prod_id='p-纱')
        self.package(old_emp_id='OTHER')
        row=package_yield(self.at,self.at,filters={'EmpID':'e-甲','ProdID':'P-纱'})['rows'][0]
        self.assertEqual(row['Packs'],1);self.assertEqual(row['EmpID'],'e-甲');self.assertEqual(row['ProdID'],'p-纱')

    def work(self,**values):
        return self.old('WProcess',**{'old_wprocess_no':'W','old_job_sheet_no':'J','old_shift_id':'S',
            'old_process_no':1,'old_process_id':'GX01','old_station_id':'01','old_end_time':self.at,
            'old_curr_kg':-3,'old_curr_rolls':2,**values})

    def assignment(self,**values):
        return self.old('JobShiftEmp',**{'old_job_sheet_no':'J','old_shift_id':'S','old_process_no':1,
            'old_process_id':'GX01','old_wprocess_no':'W','old_emp_id':'E',**values})

    def test_work_distinct_keeps_all_source_ids_and_seven_fifty_boundary(self):
        first=self.work(old_end_time=self.at.replace(hour=7,minute=49));second=self.work(old_end_time=self.at.replace(hour=7,minute=49))
        self.assignment();self.assignment(old_emp_id='E2')
        self.old('JobSheet',old_sheet_series='J',old_sheet_no='J')
        self.old('PProcess','erp_base',old_process_id='GX01')
        result=work_quantity(self.at-timedelta(days=1),self.at)
        self.assertEqual(len(result['rows']),1);self.assertEqual(result['rows'][0]['Days'],'2026-08-14')
        self.assertEqual(result['rows'][0]['source_ids'],[first.pk,second.pk]);self.assertEqual(result['rows'][0]['CurrKg'],-3)
        self.assertEqual(len(result['result_rows'][0]['employee_ids']),2)

    def test_work_missing_inner_links_station_two_null_and_process_number_kept(self):
        first=self.work(old_station_id='02');second=self.work(old_station_id=None);third=self.work(old_process_no=None)
        result=work_quantity(self.at,self.at)
        self.assertEqual(result['rows'],[]);self.assertEqual(len(result['supplemental_rows']),3)
        self.assertEqual({row['record_id'] for row in result['supplemental_rows']},{first.pk,second.pk,third.pk})

    def plan(self,**values):
        model=apps.get_model('erp_production.SourceDyeProcessSchedule')
        return self.old('ProcessSchedule',**{'old_id':'P'+str(model.objects.count()),'old_job_sheet_no':'J',
            'old_stereotypes_name':'机类','old_plan_date':self.at,**values})

    def test_existing_schedule_duplicates_quote_and_empty(self):
        self.plan(old_job_sheet_no="J'1");self.plan(old_job_sheet_no="J'1")
        result=existing_schedules(["j'1"])
        self.assertEqual(result['rows'][0]['Code'],1);self.assertEqual(len(result['result_rows']),2)
        self.assertEqual(existing_schedules(['missing'])['rows'][0]['Code'],0)

    def test_schedule_dense_rank_priority_and_latest_ties(self):
        self.plan(old_job_sheet_no='J',old_plan_date=self.at-timedelta(days=2))
        self.plan(old_job_sheet_no='K',old_plan_date=self.at,old_is_not=True)
        for code in ['W1','W2']:self.work(old_wprocess_no=code,old_station_id='06',old_start_time=self.at-timedelta(hours=2),old_machine_id='M',old_dye_state='5')
        self.old('StuffWeight',old_sheet_series='SW',old_sheet_kind=2,old_recipe_type=1,old_wprocess_no='W1')
        result,_=schedule_rank(self.at)
        j=[row for row in result if row['JobSheetNo']=='J']
        self.assertEqual(len(j),2);self.assertTrue(all(row['latest_time_tied'] for row in j))
        self.assertEqual(next(row for row in j if row['STWProcessNo']=='W1')['NUM'],1)
        self.assertEqual(next(row for row in result if row['JobSheetNo']=='K')['NUM'],1)

    def test_process_gx03_missing_plan_and_queue_rules(self):
        self.assertEqual(process_status('J','GX03','1',self.at)['rows'][0]['rule'],'A')
        self.plan(old_job_sheet_no='FIRST',old_plan_date=self.at-timedelta(days=1));self.plan()
        report=process_status('J','GX03','1',self.at)
        self.assertEqual(report['rows'][0]['rule'],'D');self.assertEqual(report['rows'][0]['MinNUM'],1)
        self.work(old_job_sheet_no='FIRST',old_process_id='GX03')
        self.assertEqual(process_status('J','GX03','1',self.at)['rows'][0]['CmOk'],0)

    def test_process_gx07_interval_receive_and_priority(self):
        self.old('JobSheet',old_sheet_series='J',old_sheet_no='J')
        self.old('JobProcess',old_sheet_series='J',old_process_no=1,old_process_id='GX07',old_start_time=self.at-timedelta(minutes=239,seconds=59))
        self.assertEqual(process_status('J','GX07','3',self.at)['rows'][0]['CmOk'],0) # DATEDIFF跨240个分钟边界
        item=apps.get_model('erp_production.SourceDyeJobProcess').objects.get()
        item.old_start_time=self.at-timedelta(minutes=239);item.save()
        self.assertEqual(process_status('J','GX07','3',self.at)['rows'][0]['rule'],'B')
        self.old('GetJobSheetReceive','erp_base',old_sheet_series='R',old_job_sheet_no='J')
        self.assertEqual(process_status('J','GX07','3',self.at)['rows'][0]['CmOk'],0)
        self.plan(old_job_sheet_no='FIRST',old_plan_date=self.at-timedelta(days=1));self.plan()
        self.assertEqual(process_status('J','GX07','1',self.at)['rows'][0]['rule'],'C')

    def test_process_multiple_original_start_candidates_all_returned(self):
        self.old('JobSheet',old_sheet_series='J',old_sheet_no='J')
        for minutes in [1,300]:self.old('JobProcess',old_sheet_series='J',old_process_no=1,old_process_id='GX07',old_start_time=self.at-timedelta(minutes=minutes))
        report=process_status('J','GX07','3',self.at)
        self.assertTrue(report['ambiguous']);self.assertEqual({row['CmOk'] for row in report['rows']},{0,1})

    def test_six_api_actions_and_original_data_not_mutated(self):
        self.dye();self.package();self.plan();self.work()
        arguments=[('erp_quality_sourcedyedyecheckout','dye_rate',{'by':'shift','start':self.at.isoformat(),'end':self.at.isoformat()}),
            ('erp_quality_sourcedyedyecheckout','station_dashboard',{'report':'depth','as_of':self.at.isoformat()}),
            ('erp_warehouse_sourcedyerecordyield','package_yield',{'by':'employee','start':self.at.isoformat(),'end':self.at.isoformat()}),
            ('erp_production_sourcedyewprocess','work_quantity',{'start':self.at.isoformat(),'end':self.at.isoformat()}),
            ('erp_production_sourcedyewprocess','process_status',{'number':'J','process':'GX07','state':'1','as_of':self.at.isoformat()}),
            ('erp_production_sourcedyeprocessschedule','existing_schedules',{'numbers':'J'})]
        for entity,action,args in arguments:
            response=self.client.post(f'/api/system/{entity}/{action}/',args,format='json')
            self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(apps.get_model('erp_quality.SourceDyeDyeCheckout').objects.count(),1)

    def quantity_batch(self):
        from plugins.erp_quality.quantity_models import QualityQuantityBatch
        return QualityQuantityBatch.objects.create(sha256='f'*64,database_name='test',captured_at=self.at,
            row_count=0,length_available=False,evidence={})

    def test_ten_day_automatic_denominator_distinct_codes_all_kinds_negative_and_null(self):
        from plugins.erp_quality.quantity_models import QualityQuantityBatch,QualityQuantitySource
        from plugins.erp_quality.quantity_services import ten_day_denominators
        batch=self.quantity_batch()
        for i,(day,code,qty,kind) in enumerate([(1,'J',10,30),(11,'j ',5,99),(20,None,-3,None),(21,'OUT',100,30),(15,'',None,40),(15,'J',2,30)],1):
            QualityQuantitySource.objects.create(batch=batch,source_row=i,sheet_date=self.at.replace(day=day),job_number=code,quantity=qty,sheet_kind=kind)
        result,sources,_,_=ten_day_denominators(self.at.date(),QualityQuantityBatch.objects.all(),QualityQuantitySource.objects.all())
        self.assertEqual(result,{'DayAllNum':2,'DayAllKg':4,'MonthAllNum':2,'MonthAllKg':14})
        self.assertEqual(len(sources),5)

    def test_ten_day_missing_batch_and_known_empty_are_different(self):
        from plugins.erp_quality.quantity_models import QualityQuantityBatch,QualityQuantitySource
        from plugins.erp_quality.quantity_services import ten_day_denominators
        def report():return ten_day_denominators(self.at.date(),QualityQuantityBatch.objects.all(),QualityQuantitySource.objects.all())
        self.assertIsNone(report()[0]['DayAllNum'])
        self.quantity_batch()
        self.assertEqual(report()[0]['DayAllNum'],0);self.assertIsNone(report()[0]['DayAllKg'])

    def test_ten_day_api_automatic_and_manual_denominator_separation(self):
        from plugins.erp_quality.quantity_models import QualityQuantitySource
        batch=self.quantity_batch()
        QualityQuantitySource.objects.create(batch=batch,source_row=1,sheet_date=self.at,job_number='J',quantity=7)
        root='/api/system/erp_quality_sourcedyewdefect/quality_statistics/'
        args={'report':2,'as_of':'2026-08-15'}
        response=self.client.post(root,args,format='json');self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(response.data['data']['denominator']['DayAllKg'],'7.00')
        response=self.client.post(root,{**args,'quantity_source':'automatic','DayAllKg':'10'},format='json')
        self.assertEqual(response.status_code,400)
        response=self.client.post(root,{**args,'quantity_source':'manual','DayAllKg':'10','denominator_reference':'明确原来源'},format='json')
        self.assertEqual(response.status_code,200);self.assertEqual(response.data['data']['denominator']['DayAllKg'],'10.000000')

    def test_package_historical_string_sources_respect_query_scope(self):
        from plugins.erp_base.source_quality_reports import rows
        self.package(old_color_id='A');self.package(old_color_id='B')
        hidden=self.package(old_sheet_date=self.at-timedelta(days=1),old_color_id='SECRET')
        def visible(name,module):
            query=rows(name,module)
            return query.exclude(pk=hidden.pk) if name=='RecordYield' else query
        result=package_yield(self.at,self.at,query=visible)
        self.assertEqual(result['rows'][0]['ColorID'],'A;B');self.assertEqual(result['supplemental_rows'],[])

    def test_dye_rates_do_not_include_retained_replaced_quality(self):
        from plugins.erp_base.source_context import SourceDocumentContext
        first=self.dye();second=self.dye(old_cloth_qty_kg=999)
        SourceDocumentContext.objects.create(entity=second._meta.label,object_id=second.pk,
            entry_name='',effects={'quality_replaced':{'active':True}})
        report=dye_rate(self.at,self.at)
        self.assertEqual(report['rows'][-1]['source_ids'],[first.pk])
