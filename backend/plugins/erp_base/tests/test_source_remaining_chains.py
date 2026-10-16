from plugins.erp_base.tests.source_fixtures import historical_batch
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import patch
from django.apps import apps
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base import source_services as services
from plugins.erp_base.business import snapshot
from plugins.erp_base.models import BusinessAction
from plugins.erp_base.source_context import SourceDocumentContext, SourceBusinessParameter
from plugins.erp_base.source_outwork_close import close, reopen, closure, reconciliation
from plugins.erp_base.source_work_delete import check_shift_delete, maintain_removed, delete_shift_record
from plugins.erp_base.source_quality_reports import quality_statistics, dye_quality_award, period_dates


class RemainingChainTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='remaining-flow', password='test')
        self.at = timezone.make_aware(datetime(2026, 10, 15, 9))
        self.client = APIClient(); self.client.force_authenticate(self.actor)

    def old(self, name, module='erp_production', **data):
        return apps.get_model(module + '.SourceDye' + name).objects.create(**data)

    def work(self, number='W', **data):
        values = dict(old_wprocess_no=number, old_job_sheet_no='J', old_process_no=2, old_process_id='P2',
            old_station_id='02', old_shift_id='S', old_class_id='03', old_end_time=self.at, old_create_date=self.at)
        values.update(data)
        return self.old('WProcess', **values)

    def process(self, number, **data):
        values = dict(old_sheet_series='J', old_process_no=number, old_process_id='P'+str(number), old_station_id='02',
            old_status='1', old_start_time=self.at, old_end_time=self.at, old_wpworker='原人员', old_wprocess_no='W', old_machine_id='M', old_team_name='原班组')
        values.update(data)
        return self.old('JobProcess', **values)

    def job(self, **data):
        values = dict(old_sheet_series='J', old_sheet_no='J'); values.update(data)
        return self.old('JobSheet', **values)

    def test_closure_preserves_source_fields_and_explicit_losses(self):
        application = self.old('OutWorkApply', old_sheet_series='A', source_batch=historical_batch(), old_sheet_status=-7)
        before = snapshot(application)
        self.old('GrayOut', 'erp_warehouse', old_sheet_series='G', old_stock_unit='1')
        lines = [self.old('GrayOutDetail', 'erp_warehouse', old_sheet_series='G', old_assigned_no='D', old_weight_qty=value, source_batch=historical_batch()) for i,value in enumerate([Decimal('10'),Decimal('-2'),None])]
        receipt = self.old('ProdIn', 'erp_warehouse', old_sheet_series='R', old_stock_unit='1', old_weight_qty=Decimal('6.5'), source_batch=historical_batch())
        losses = [{'unit':1,'measure':'WeightQty','quantity':Decimal('-0.25'),'reason':'明确负损耗'}]
        result = close(application, self.actor, lines + [lines[0]], [receipt], losses, self.at, '实际核对')
        row = next(row for row in result['rows'] if row['unit']==1 and row['measure']=='WeightQty')
        self.assertEqual(row['dispatched'],8);self.assertEqual(row['difference'],Decimal('1.5'))
        self.assertEqual(row['confirmed_loss'],Decimal('-0.25'));self.assertEqual(row['unexplained_difference'],Decimal('1.75'))
        self.assertEqual(row['dispatch_nulls'],1);self.assertEqual(len(result['sources']),4)
        application.refresh_from_db();self.assertEqual(snapshot(application),before)
        self.assertEqual(closure(application)['state'],'closed')
        reopen(application,self.actor,'继续核对');self.assertEqual(closure(application)['state'],'open')
        self.assertEqual(BusinessAction.objects.filter(action__in=['outwork_closed','outwork_closure_reopened']).count(),2)
        with self.assertRaises(ValidationError):reopen(application,self.actor,'不可重复撤回')

    def test_orphan_and_duplicate_headers_do_not_multiply_or_guess_unit(self):
        for _ in range(2):self.old('SemiOut','erp_warehouse',old_sheet_series='S',old_stock_unit='1')
        orphan=self.old('SemiOutDetail','erp_warehouse',old_sheet_series='NONE',old_detail_no='X',old_weight_qty=-2)
        duplicate=self.old('SemiOutDetail','erp_warehouse',old_sheet_series='S',old_detail_no='Y',old_weight_qty=3)
        result=reconciliation([orphan,duplicate],[],[])
        weights=[row for row in result['rows'] if row['measure']=='WeightQty']
        self.assertEqual([row['dispatched'] for row in weights],[-2,3])
        for weight in weights:
            self.assertIsNone(weight['unit']);self.assertIsNone(weight['difference']);self.assertIsNone(weight['confirmed_loss'])
        self.assertEqual([len(source['headers']) for source in result['sources']],[0,2])

    def test_empty_semi_outwork_closure_api_and_loss_validation(self):
        application=self.old('SemiOutWorkApply',old_sheet_series='S',source_batch=historical_batch())
        url=f'/api/system/erp_production_sourcedyesemioutworkapply/{application.pk}/'
        payload={'dispatched':[],'received':[],'losses':[],'closed_at':self.at.isoformat(),'reason':'原零明细业务'}
        result=self.client.post(url+'close_outwork/',payload,format='json')
        self.assertEqual(result.status_code,200,result.data);self.assertEqual(result.data['data']['rows'],[])
        result=self.client.post(url+'outwork_closure/',{},format='json')
        self.assertEqual(result.data['data']['closure']['state'],'closed')
        payload['losses']=[{'unit':None,'measure':'猜测','quantity':2,'reason':'错误类型'}]
        self.assertEqual(self.client.post(url+'close_outwork/',payload,format='json').status_code,400)
        self.assertEqual(closure(application)['losses'],[])

    def test_closure_does_not_invent_original_entry_for_unbound_new_application(self):
        application=self.old('OutWorkApply',old_sheet_series='NEW')
        close(application,self.actor,[],[],[],self.at,'明确结案')
        self.assertIsNone(application.entry_name)
        services.write(type(application),{'old_remarks':'继续保留原编辑能力'},application,self.actor)
        services.write(type(application),{'_entry':'OutWorkApply'},application,self.actor)
        self.assertEqual(application.entry_name,'OutWorkApply')
        self.assertEqual(closure(application)['state'],'closed')

    def test_last_work_deletion_resets_process_and_retains_history_children(self):
        job=self.job();self.process(1);process=self.process(2)
        work=self.work()
        old=self.old('JobShiftEmp',old_job_sheet_no='J',old_process_no=2,old_process_id='P2',old_shift_id='S',old_wprocess_no='W',source_batch=historical_batch())
        new=self.old('JobShiftEmp',old_job_sheet_no='J',old_process_no=2,old_process_id='P2',old_shift_id='S',old_wprocess_no='W')
        services.delete(type(work).objects.filter(pk=work.pk),self.actor)
        process.refresh_from_db();job.refresh_from_db()
        self.assertEqual(process.old_status,'0');self.assertIsNone(process.old_machine_id);self.assertIsNone(process.old_start_time)
        self.assertEqual(job.old_curr_process_id,'P1');self.assertEqual(job.old_next_process_id,'P2')
        self.assertTrue(type(old).objects.filter(pk=old.pk,source_batch=historical_batch()).exists())
        self.assertFalse(type(new).objects.filter(pk=new.pk).exists())
        self.assertTrue(BusinessAction.objects.filter(action='work_delete_keep_source',object_id=old.pk).exists())

    def test_remaining_work_uses_latest_number_and_duplicate_join_names(self):
        self.job();process=self.process(2)
        gone=self.work('GONE');self.work('REMAIN',old_emp_id='E',old_create_date=self.at+timedelta(seconds=1))
        self.old('PShift','erp_base',old_shift_id='S',old_name='组甲')
        for _ in range(2):self.old('HEmployee','erp_base',old_emp_id='E',old_name='张工')
        services.delete(type(gone).objects.filter(pk=gone.pk),self.actor)
        process.refresh_from_db()
        self.assertEqual(process.old_wprocess_no,'REMAIN');self.assertEqual(process.old_wpworker,'张工;张工')
        self.assertEqual(process.old_team_name,'组甲;组甲');self.assertEqual(process.old_status,'1')
        self.assertEqual(process.old_machine_id,'M');self.assertIsNone(process.old_end_time)

    def test_non_special_station_preserves_team_and_gap_preserves_job_fields(self):
        job=self.job(old_curr_process_id='ORIGINAL',old_next_process_id='NEXT')
        process=self.process(5,old_process_id='P2')
        gone=self.work(old_process_no=5,old_station_id='01')
        self.work('R',old_process_no=5,old_station_id='01')
        services.delete(type(gone).objects.filter(pk=gone.pk),self.actor)
        process.refresh_from_db();job.refresh_from_db()
        self.assertEqual(process.old_team_name,'原班组');self.assertEqual(job.old_curr_process_id,'ORIGINAL')
        self.assertEqual(job.old_next_process_id,'NEXT')

    def test_day_night_delete_boundaries_and_latest_dye_state(self):
        work=self.work(old_station_id='06')
        check_shift_delete(work,self.at.replace(hour=20,minute=0))
        with self.assertRaises(ValidationError):check_shift_delete(work,self.at.replace(hour=20,second=1))
        with self.assertRaises(ValidationError):check_shift_delete(work,self.at.replace(hour=7))
        latest=self.work('LATEST',old_station_id='06',old_end_time=self.at+timedelta(minutes=1))
        with self.assertRaises(ValidationError):check_shift_delete(work,self.at)
        check_shift_delete(latest,self.at)
        night=self.work('NIGHT',old_class_id='04',old_end_time=self.at.replace(hour=1),old_station_id='02')
        check_shift_delete(night,self.at.replace(hour=7))
        # 原夜班在08点改用当天20点起算，并非昨夜夜班的结束瞬间。
        with self.assertRaises(ValidationError):check_shift_delete(night,self.at.replace(hour=8))

    def test_added_foreign_keys_unlinked_without_erasing_old_step_fields(self):
        work=self.work(old_class_id=None)
        step=self.old('WProcessStep',old_wpstep_no='STEP',old_wprocess_no='W',source_batch=historical_batch(),source_parent_1=work)
        staff=self.old('JobShiftEmp',old_job_sheet_no='J',old_process_no=2,old_process_id='P2',old_shift_id='S',old_wprocess_no='W',source_batch=historical_batch(),source_parent_1=work,source_parent_2=work)
        services.delete_documents(type(work).objects.filter(pk=work.pk),self.actor)
        step.refresh_from_db();staff.refresh_from_db()
        self.assertIsNone(step.source_parent_1_id);self.assertEqual(step.old_wprocess_no,'W');self.assertEqual(step.source_batch_id,historical_batch().pk)
        self.assertIsNone(staff.source_parent_1_id);self.assertIsNone(staff.source_parent_2_id);self.assertEqual(staff.old_wprocess_no,'W')
        self.assertEqual(BusinessAction.objects.filter(action='work_delete_unlink').count(),3)

    def test_maintenance_gx07_preserves_start_and_worker_and_uses_exact_next(self):
        job=self.job();self.process(1);target=self.process(3,old_process_id='GX07')
        item=self.work(old_process_no=3,old_process_id='GX07')
        step=self.old('WProcessStep',old_wprocess_no='W',old_wpstep_no='STEP')
        maintain_removed(item,self.actor)
        target.refresh_from_db();job.refresh_from_db()
        self.assertEqual(target.old_start_time,self.at);self.assertEqual(target.old_wpworker,'原人员')
        self.assertEqual(target.old_status,'0');self.assertIsNone(target.old_end_time)
        self.assertEqual(job.old_curr_process_id,'P1');self.assertIsNone(job.old_next_process_id)
        self.assertEqual(job.old_sheet_status,0);self.assertFalse(type(step).objects.filter(pk=step.pk).exists())
        SourceBusinessParameter.objects.create(name='EndProcessID',value='P1;')
        maintain_removed(item,self.actor);job.refresh_from_db();self.assertEqual(job.old_sheet_status,10)

    def test_maintenance_no_active_clears_totals_and_other_work_retains_job(self):
        job=self.job(old_sum_process_weight_qty=5,old_curr_process_id='OLD')
        self.process(2)
        item=self.work();maintain_removed(item,self.actor)
        job.refresh_from_db();self.assertIsNone(job.old_sum_process_weight_qty);self.assertIsNone(job.old_curr_process_id)
        self.process(1);self.work('SURVIVOR',old_status='1')
        job.old_curr_process_id='KEEP';job.save()
        maintain_removed(item,self.actor);job.refresh_from_db();self.assertEqual(job.old_curr_process_id,'KEEP')

    def test_shift_api_success_and_history_rolls_back(self):
        work=self.work(old_class_id=None)
        url=f'/api/system/erp_production_sourcedyewprocess/{work.pk}/delete_shift_record/'
        result=self.client.post(url,{'mode':'trigger_then_maintenance','reason':'实际撤回'},format='json')
        self.assertEqual(result.status_code,200,result.data);self.assertFalse(type(work).objects.filter(pk=work.pk).exists())
        historical=self.work('H',old_class_id=None,source_batch=historical_batch())
        before=BusinessAction.objects.count()
        with self.assertRaises(ValidationError):delete_shift_record(historical,self.actor,'trigger','不可删除原行')
        self.assertEqual(BusinessAction.objects.count(),before)

    def dictionary(self):
        for code,name in [('03','甲班'),('04','乙班'),('05','其他班')]:
            self.old('PFieldValid','erp_base',old_field_type='Class',old_code=code,old_name=name)
        for code in ['01','02','03','07','09','99']:
            self.old('PFieldValid','erp_base',old_field_type='Defects',old_code=code,old_name='部门'+code,old_description='一级',old_mnemonic='二级'+code)

    def defect(self, **data):
        values=dict(old_sheet_series='D',old_sheet_no='D',old_job_sheet_no='J',old_kind='内部评审',old_sheet_date=self.at,
            old_defect_dept='03',old_defect_class_id='03',old_defect_qty=Decimal('2'),old_defect_length_qty=Decimal('3'))
        values.update(data)
        return self.old('WDefect','erp_quality',**values)

    def test_daily_duplicate_jobs_negative_and_original_dept_bug(self):
        self.dictionary();self.job(old_assign_unit=1);self.job(old_sheet_series='J2',old_assign_unit=1)
        defect=self.defect(old_defect_dept='01',old_defect_class_id='05',old_defect_qty=-2)
        result=quality_statistics(1,self.at.date())
        row=next(row for row in result['supplemental_rows'] if row['UnitName']=='数量')
        self.assertEqual(row['Day_N_Qty'],-4);self.assertEqual(row['ClassName'],'甲班')
        self.assertTrue(all(row['Day_N_Qty'] is None for row in result['rows'] if row['DefectDept']=='01'))
        self.assertEqual(next(row for row in result['rows'] if row['DefectDept']=='合计')['Day_N_Qty'],-4)
        self.assertEqual(result['source_ids'],[defect.pk])

    def test_report_end_boundaries_nulls_unclassified_and_grade(self):
        self.dictionary();self.job(old_assign_unit=0)
        end=period_dates(self.at.date(),1)[1]
        self.defect(old_sheet_date=end,old_defect_qty=-1)
        odd=self.defect(old_kind='旧其他类型');undated=self.defect(old_sheet_date=None)
        result=quality_statistics(1,self.at.date())
        qty=next(row for row in result['supplemental_rows'] if row['UnitName']=='数量')
        cards=next(row for row in result['supplemental_rows'] if row['UnitName']=='卡数')
        self.assertIsNone(qty['Day_N_Qty']);self.assertEqual(qty['Month_N_Qty'],-1)
        self.assertEqual(cards['Day_N_LengthQty'],1);self.assertIsNone(cards['Month_N_LengthQty'])
        self.assertEqual({row['id'] for row in result['unclassified_rows']},{odd.pk,undated.pk})
        grade=quality_statistics(3,self.at.date())['rows'][0]
        self.assertEqual(grade['Day_N_Qty'],-1);self.assertEqual(grade['OneGrade'],'一级')
        self.assertTrue(all(row['UnitName']=='数量' for row in quality_statistics(3,self.at.date())['supplemental_rows']))

    def test_numeric_class_conversion_and_non_numeric_class_survive(self):
        self.dictionary();self.job(old_assign_unit=1)
        self.defect(old_defect_class_id='005');self.defect(old_defect_class_id='未知')
        result=quality_statistics(1,self.at.date())
        quantities=[row for row in result['supplemental_rows'] if row['UnitName']=='数量']
        self.assertEqual({row['ClassName'] for row in quantities},{'甲班',None})
        self.assertEqual(sum(row['Day_N_Qty'] for row in quantities),4)

    def test_ten_day_month_and_zero_missing_denominators(self):
        self.dictionary();self.job(old_assign_unit=1)
        self.defect(old_sheet_date=self.at.replace(day=11));self.defect(old_sheet_date=self.at.replace(day=1))
        result=quality_statistics(2,self.at.date())
        row=next(row for row in result['rows'] if row['TowGrade']=='二级03')
        self.assertEqual(row['Day_N_Qty'],1);self.assertEqual(row['Month_N_Qty'],2);self.assertIsNone(row['N1'])
        result=quality_statistics(2,self.at.date(),{'DayAllNum':0,'DayAllKg':None,'MonthAllNum':Decimal(4),'MonthAllKg':None})
        row=next(row for row in result['rows'] if row['TowGrade']=='二级03')
        self.assertEqual(row['N1'],0);self.assertEqual(row['N2'],50)
        for day,endday in [(10,10),(11,20),(20,20),(21,31),(31,31)]:
            self.assertEqual(period_dates(date(2026,10,day),2)[1].day,endday)
        self.assertEqual(period_dates(date(2024,2,29),2)[1].day,29)

    def test_award_duplicate_repair_join_and_responsible_class_without_output(self):
        self.job(old_loss_str='REPAIR');self.defect(old_sheet_no='REPAIR');self.defect(old_sheet_no='REPAIR')
        self.old('DyeCheckout','erp_quality',old_wprocess_no='W',old_class_id='A',old_defect_class_id='B',old_job_sheet_no='J',old_wdnum=3,old_end_time=self.at)
        rows=dye_quality_award(self.at,self.at)['rows'];byclass={row['ClassID']:row for row in rows}
        self.assertEqual(byclass['A']['AClassIDNum'],1);self.assertEqual(byclass['A']['Moeny'],2000)
        self.assertEqual(byclass['B']['BClassIDNum'],6);self.assertEqual(byclass['B']['KFMoeny'],50)
        self.assertIsNone(byclass['B']['Rate']);self.assertIsNone(byclass['B']['Moeny'])

    def test_award_rate_threshold_negative_and_all_empty(self):
        self.job(old_loss_str='REPAIR');self.defect(old_sheet_no='REPAIR')
        for code,num in [('A',1),('B',-2)]:
            self.old('DyeCheckout','erp_quality',old_wprocess_no=code,old_class_id=code,old_defect_class_id=code,old_job_sheet_no='J',old_wdnum=num,old_end_time=self.at)
        rows={row['ClassID']:row for row in dye_quality_award(self.at,self.at)['rows']}
        self.assertEqual(rows['A']['Rate'],100);self.assertEqual(rows['A']['Moeny'],0)
        self.assertEqual(rows['B']['Rate'],-200);self.assertEqual(rows['B']['Moeny'],1000)
        self.assertEqual(dye_quality_award(self.at+timedelta(days=1),self.at+timedelta(days=2))['rows'],[])

    def test_collection_report_api_works_without_any_business_rows(self):
        url='/api/system/erp_quality_sourcedyewdefect/quality_statistics/'
        result=self.client.post(url,{'report':1,'as_of':'2026-10-15'},format='json')
        self.assertEqual(result.status_code,200,result.data);self.assertEqual(result.data['data']['source_ids'],[])
        result=self.client.post(url,{'report':2,'as_of':'2026-10-15','DayAllNum':'1'},format='json')
        self.assertEqual(result.status_code,400)
        result=self.client.post('/api/system/erp_quality_sourcedyedyecheckout/quality_award/',{'start':self.at.isoformat(),'end':self.at.isoformat()},format='json')
        self.assertEqual(result.status_code,200,result.data);self.assertEqual(result.data['data']['rows'],[])

    def test_report_source_permission_required(self):
        from types import SimpleNamespace
        from rest_framework.exceptions import PermissionDenied
        from plugins.erp_base.source_api import report_query
        actor=Users.objects.create_user(username='limited',password='test')
        with self.assertRaises(PermissionDenied):quality_statistics(1,self.at.date(),query=report_query(SimpleNamespace(user=actor)))
