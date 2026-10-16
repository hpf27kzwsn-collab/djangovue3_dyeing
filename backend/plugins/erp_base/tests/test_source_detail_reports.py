from datetime import datetime,timedelta
from decimal import Decimal
from django.apps import apps
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.source_services import write,apply_defaults,delete
from plugins.erp_base.source_quote_rules import inspect
from plugins.erp_base.source_sample_reports import production,checker,emp1
from plugins.erp_base.source_trial_steps import preview,sql_like
from plugins.erp_base.source_package_operations import reader,effect
from plugins.erp_base.source_business_updates import update_rows


class DetailReportsTests(TestCase):
    def setUp(self):
        self.actor=Users.objects.create_superuser(username='detail-reports',password='test')
        self.at=timezone.make_aware(datetime(2026,10,15,7,30))
        self.client=APIClient();self.client.force_authenticate(self.actor)

    def old(self,name,module='erp_sampling',**values):
        model=apps.get_model(module+'.SourceDye'+name);item=model()
        data={model.SOURCE_FIELDS[k]:v for k,v in values.items()};apply_defaults(item,data)
        for field,value in data.items():setattr(item,field,value)
        item.save();item.refresh_from_db();return item

    def quote(self,**values):
        self.old('Quote','erp_sales',SheetSeries='Q',CustomerID='C')
        return self.old('QuoteDetail','erp_sales',SheetSeries='Q',DetailNo='D',ColorNum='RED',ProdID='P',**values)

    def test_quote_duplicate_insert_modify_thresholds_preserve_all_rows(self):
        first=self.quote();model=type(first)
        second=write(model,{'old_sheet_series':'Q','old_detail_no':'D2','old_color_num':'red ','old_prod_id':'p'},actor=self.actor)
        self.assertTrue(effect(second,'quote_trigger_check')['rows'][0]['duplicate'])
        self.assertFalse(inspect(second,'update')['rows'][0]['duplicate'])
        third=write(model,{'old_sheet_series':'Q','old_detail_no':'D3','old_color_num':'RED','old_prod_id':'P'},actor=self.actor)
        self.assertTrue(inspect(third,'update')['rows'][0]['duplicate'])
        self.assertEqual(model.objects.count(),3)

    def test_quote_join_multiplicity_and_null_product(self):
        item=self.quote();self.old('Quote','erp_sales',SheetSeries='Q',CustomerID='C')
        self.assertEqual(inspect(item,'insert')['rows'][0]['join_count'],2)
        item.old_prod_id=None;item.save()
        self.assertEqual(inspect(item,'insert')['rows'][0]['join_count'],0)

    def test_quote_approved_update_statement_column_even_unchanged(self):
        item=self.quote(RightStatus=10)
        with self.assertRaises(ValidationError):write(type(item),{'old_price':4},instance=item,actor=self.actor)
        item.refresh_from_db();self.assertEqual(item.old_price,0)
        write(type(item),{'old_right_status':10,'old_price':4},instance=item,actor=self.actor)
        item.refresh_from_db();self.assertEqual(item.old_price,4)
        with self.assertRaises(ValidationError):delete(type(item).objects.filter(pk=item.pk),self.actor)

    def test_quote_orphan_update_and_delete_different_trigger_binding(self):
        item=self.old('QuoteDetail','erp_sales',SheetSeries='MISSING',DetailNo='D',RightStatus=10)
        write(type(item),{'old_remarks':'孤立原单可保存'},instance=item,actor=self.actor)
        self.assertFalse(inspect(item,'update')['rows'][0]['approved_block'])
        self.assertTrue(inspect(item,'delete')['rows'][0]['approved_block'])

    def test_quote_automatic_update_has_same_trigger_and_atomic_rollback(self):
        item=self.quote(RightStatus=10)
        with self.assertRaises(ValidationError):update_rows(type(item).objects.all(),{'Price':0},self.actor,'test','原无值变化UPDATE仍触发')
        with self.assertRaises(ValidationError):update_rows(type(item).objects.all(),{'Price':5},self.actor,'test','原调价回写')
        item.refresh_from_db();self.assertEqual(item.old_price,0)
        update_rows(type(item).objects.all(),{'Price':5,'RightStatus':10},self.actor,'test','原调价含状态列')
        item.refresh_from_db();self.assertEqual(item.old_price,5)

    def test_quote_scope_failure_is_not_partial_candidate_result(self):
        item=self.quote()
        def query(name,module):return reader(name,module).none() if name=='Quote' else reader(name,module)
        with self.assertRaises(ValidationError):inspect(item,'insert',query=query)

    def sample(self,**values):return self.old('DyeDipsRecord',**{'SheetSeries':'S','SheetDate':self.at,'EmpID':'E','IsDoubleDye':0,'ColorVersion':'A',**values})

    def dictionary(self,code,price):return self.old('PFieldValid','erp_base',FieldType='RecipeKind',Code=code,NumValue=price)

    def test_workday_boundary_and_end_exclusion_and_no_employee_null(self):
        self.sample(SheetDate=self.at-timedelta(seconds=1));self.sample();self.sample(SheetDate=self.at+timedelta(days=1))
        result=production('days',self.at-timedelta(hours=1),self.at+timedelta(days=1),'E')
        self.assertEqual(result['rows'][0]['WorkDays'],2)
        result=production('days',self.at,self.at,'E');self.assertIsNone(result['rows'][0]['WorkDays'])

    def test_details_only_main_employee_a_version_and_null_num(self):
        self.sample(Num=None,EmpID1='SECOND',ColorVersion=None)
        self.sample(ColorVersion='B');self.sample(EmpID='')
        result=production('details');self.assertEqual(len(result['rows']),1)
        self.assertEqual(result['rows'][0]['Num'],1);self.assertEqual(len(result['supplemental_rows']),2)

    def test_sql_float_round_boundary_matches_live_readonly_probes(self):
        from plugins.erp_base.source_sample_reports import float_round
        for value,expected in [(1.005,1.0),(2.675,2.67),(-1.005,-1.0),(-2.675,-2.67),(.125,.13),(-.125,-.13)]:
            self.assertEqual(float_round(value),expected)

    def test_counter6_not_paid_and_num_not_multiplier(self):
        self.dictionary('6',100);self.dictionary('1',2)
        self.old('DyeReprint',SheetDate=self.at,EmpID='E',Kind=6,Num=-3)
        self.old('DyeReprint',SheetDate=self.at,EmpID='E',Kind=1,Num=Decimal('.25'))
        row=production('summary')['rows'][0]
        self.assertEqual((row['FDNum'],row['WNum'],row['SumNum'],row['Amount']),(1,1,Decimal('-2.75'),2))

    def test_dictionary_duplicate_null_kind_and_invalid_code_are_visible(self):
        self.dictionary('0',2);self.dictionary('00 ',3);self.dictionary('BAD',9)
        self.sample(Num=Decimal('.25'));missing=self.sample(IsDoubleDye=None)
        report=production('summary');row=report['rows'][0]
        self.assertEqual((row['DNum'],row['SumNum'],row['Amount']),(2,Decimal('.5'),5))
        self.assertEqual(len(report['supplemental_rows']),2)
        self.assertEqual(len(report['result_rows']),2)

    def test_daily_grouping_does_not_change_original_global_summary(self):
        self.dictionary('0',1)
        self.sample(SheetDate=self.at-timedelta(seconds=1));self.sample()
        result=production('daily');self.assertEqual(len(result['rows']),2)
        self.assertEqual(sum(r['DNum'] for r in result['rows']),production('summary')['rows'][0]['DNum'])

    def test_emp1_variant_keeps_null_group_and_sheetkind_join(self):
        self.dictionary('4',3)
        self.sample(SheetKind=4,EmpID1=None,ColorVersion='B')
        self.old('DyeReprint',SheetKind=4,SheetDate=self.at,EmpID1=None,EmpID='',Kind=6)
        row=emp1()['rows'][0];self.assertEqual((row['EmpID1'],row['DaBan'],row['FuBan'],row['Amount']),(None,1,1,6))

    def test_checker_different_employee_fields_inclusive_end_and_rounding(self):
        for i in range(3):self.sample(Times=2 if i==0 else 1,CheckerID='R',SheetDate=self.at)
        self.sample(SheetDate=timezone.make_aware(datetime(2021,4,17)),Times=2)
        result={r['CheckerID']:r for r in checker(self.at,self.at)['rows']}
        self.assertEqual((result['E']['S'],result['E']['R'],result['R']['S'],result['R']['R']),(3,0,0,1))
        self.assertEqual(result['R']['Rate'],0)
        self.sample(EmpID='R',Times=1);self.sample(EmpID='R',Times=1);self.sample(EmpID='R',Times=1)
        row=next(r for r in checker(self.at,self.at)['rows'] if r['CheckerID']=='R');self.assertEqual(row['Rate'],Decimal('33.300'))

    def prepare_steps(self):
        job=self.old('JobSheet','erp_production',SheetNo='CHILD')
        self.old('StuffWeight','erp_production',SheetSeries='W',SheetKind=2,RecipeType=0,JobSheetNo='MASTER',CombineSheetNos='XCHILDY',ProcessID='GX')
        self.old('StuffWeightPhase','erp_production',SheetSeries='W',PhaseNo=1,PhaseID='PH',ProgramID='P1')
        self.old('PDyeCurve','erp_base',CurveID='C1',PhaseID='PH',DyePhase=True)
        self.old('PDyeCurveDetail','erp_base',CurveID='C1',StepNo=1,DyeProcessID='D',DefaultValue=3)
        return job

    def done(self,program='P1',no=1,shift='OTHER',value=99,member=True):
        step=self.old('WProcessStep','erp_production',WPStepNo='WPS',WProcessNo='W',JobSheetNo='MASTER',ProcessNo=no,ProcessID='GX',ProgramID=program,DyeProcessID='D',RecordID='PERSON',RealValue=value)
        if member:self.old('JobShiftEmp','erp_production',WProcessNo='W',JobSheetNo='MASTER',ProcessNo=no,ProcessID='GX',EmpID='PERSON',ShiftID=shift)
        return step

    def test_dp_first_selection_requires_kind2_even_if_other_expected_rows_exist(self):
        job=self.prepare_steps();reader('StuffWeight','erp_production').update(old_sheet_kind=0)
        self.assertEqual(preview(job,'GX',1,'GROUP')['rows'],[])

    def test_dp_counts_nonnull_values_not_sum_and_duplicate_members(self):
        job=self.prepare_steps();self.done(value=-100)
        self.old('JobShiftEmp','erp_production',WProcessNo='W',JobSheetNo='MASTER',ProcessNo=1,ProcessID='GX',EmpID='PERSON',ShiftID='OTHER')
        result=preview(job,'GX',1,'GROUP');row=result['rows'][0]
        self.assertEqual((row['DoneValue'],row['LimitValue']),(2,1))
        self.assertEqual(result['candidate_rows'][0]['JobSheetNo'],'MASTER')

    def test_dp_parameter_is_compared_with_shift_not_employee(self):
        job=self.prepare_steps();self.done(program='C1',shift='GROUP')
        self.assertEqual(len(preview(job,'GX',1,'GROUP')['rows']),1)
        self.assertEqual(len(preview(job,'GX',1,'PERSON')['rows']),0)

    def test_dp_correlated_temp_columns_keep_cross_curve_process_no(self):
        job=self.prepare_steps();self.done(program='C1',no=1)
        self.assertEqual(len(preview(job,'GX',2,'GROUP')['rows']),0)
        self.old('PDyeCurve','erp_base',CurveID='C2',PhaseID='PH',DyePhase=True)
        self.old('PDyeCurveDetail','erp_base',CurveID='C2',StepNo=1,DyeProcessID='D',DefaultValue=1)
        self.done(program='C2',no=2,member=False)
        result=preview(job,'GX',2,'GROUP');self.assertIn('C1',[r['CurveID'] for r in result['rows']])

    def test_dp_negative_default_null_realvalue_and_inactive_curve(self):
        job=self.prepare_steps();reader('PDyeCurveDetail','erp_base').update(old_default_value=-2)
        self.done(value=None)
        row=preview(job,'GX',1,'GROUP')['rows'][0];self.assertEqual((row['DoneValue'],row['LimitValue']),(0,0))
        reader('PDyeCurve','erp_base').update(old_is_stop=True)
        report=preview(job,'GX',1,'GROUP');self.assertEqual(report['rows'],[])
        self.assertEqual(len(report['supplemental_rows']),1)
        reader('StuffWeightPhase','erp_production').update(old_phase_id='UNMAPPED')
        self.assertIn('无对应',preview(job,'GX',1,'GROUP')['supplemental_rows'][0]['issue'])

    def test_like_original_wildcards_and_null(self):
        self.assertTrue(sql_like('aBc12','%B_[12]%'))
        self.assertFalse(sql_like(None,'%'))
        self.assertTrue(sql_like('AAA','%[^B]%'))

    def test_http_report_actions(self):
        quote=self.quote();job=self.prepare_steps()
        cases=[(f'erp_sales_sourcedyequotedetail/{quote.pk}/quote_trigger_check',{'operation':'update'}),
            (f'erp_production_sourcedyejobsheet/{job.pk}/trial_steps',{'process':'GX','process_no':1,'employee':'GROUP'}),
            ('erp_sampling_sourcedyedyedipsrecord/sample_checker_report',{'start':self.at.isoformat(),'end':self.at.isoformat()})]
        for mode in ['summary','details','daily','days','emp1']:cases.append(('erp_sampling_sourcedyedyereprint/sample_work_report',{'mode':mode}))
        for url,data in cases:
            response=self.client.post('/api/system/'+url+'/',data,format='json');self.assertEqual(response.status_code,200,response.data)
