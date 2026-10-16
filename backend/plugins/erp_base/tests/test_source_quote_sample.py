from datetime import datetime,timedelta
from decimal import Decimal
from django.apps import apps
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.source_quote_functions import calculate
from plugins.erp_base.source_sample_variants import plan,apply,undo,depth_code
from plugins.erp_base.source_sample_schedule import schedule,preview as schedule_preview
from plugins.erp_base.source_trial_variants import apply as apply_trial,undo as undo_trial,preview as trial_preview
from plugins.erp_base.source_package_operations import reader
from plugins.erp_base.source_execution_state import active
from plugins.erp_base.business import snapshot


class QuoteSampleTests(TestCase):
    def setUp(self):
        self.at=timezone.make_aware(datetime(2026,10,15,12))
        self.actor=Users.objects.create_superuser(username='quote-sample',password='test')
        self.event={'at':self.at,'reason':'原报价打样试验核对'}
        self.client=APIClient();self.client.force_authenticate(self.actor)

    def old(self,name,module='erp_sampling',**values):
        model=apps.get_model(module+'.SourceDye'+name)
        if name in ['QuoteDetail','FixedPriceDetail']: values={'Width':0,'Weight':0,'PriceUnit':0,**values}
        item=model.objects.create(**{model.SOURCE_FIELDS[key]:value for key,value in values.items()});item.refresh_from_db();return item

    def quote(self,price=10,number='C123',customer='C',series='Q'):
        self.old('Quote','erp_sales',SheetSeries=series,CustomerID=customer)
        return self.old('QuoteDetail','erp_sales',SheetSeries=series,DetailNo=series,ColorNum=number,Price=price,PriceUnit=4)

    def result(self,name,**values):return calculate(name,values)['rows'][0]['value']

    def test_quote_no_customer_filter_numeric_color_and_no_candidate_zero(self):
        self.quote(customer='OTHER')
        self.assertEqual(self.result('fn_GetColorNumPrice',charging='02',color='XX123',customer='C'),10)
        self.assertEqual(self.result('fn_GetColorNumPrice',charging='01',color='XX123'),0)
        self.assertEqual(self.result('fn_GetColorNumPrice',charging='02',color=None),0)

    def adjust(self,series,date,kind,price):
        self.old('PriceAdjust','erp_sales',SheetSeries=series,StartDate=date,DateType=kind)
        self.old('PriceAdjustDetail','erp_sales',SheetSeries=series,DetailNo=series,ColorNum='123',AdjustPrice=price)

    def test_vat_adjustment_order_dispatch_second_row_only_and_null_date(self):
        self.quote();self.adjust('A',self.at,'1',20);self.adjust('B',self.at-timedelta(days=1),'0',15)
        args={'charging':'02','color':'123','weight':100,'sheet_date':self.at-timedelta(days=2),'order_date':self.at}
        self.assertEqual(self.result('fn_GetPriceListVat',**args),15)
        args['order_date']=self.at-timedelta(days=3);self.assertEqual(self.result('fn_GetPriceListVat',**args),10)
        args['sheet_date']=None;self.assertEqual(self.result('fn_GetPriceListVat',**args),0)
        self.assertEqual(self.result('fn_GetColorNumPrice',charging='02',color='123'),20)

    def test_vat_null_price_negative_and_overlapping_ranges_not_dedup(self):
        self.quote(price=None)
        for price in [2,-3]:self.old('PPriceListVat','erp_base',LengthDn=0,LengthUp=20,Price=price,PhaseID=None)
        self.old('PPriceListVat','erp_base',LengthDn=0,LengthUp=20,Price=999,PhaseID='RC07')
        self.assertEqual(self.result('fn_GetPriceListVat',charging='02',color='123',weight=Decimal('20.004')),-1)
        self.assertIsNone(self.result('fn_GetPriceListVat',charging='02',color='123',weight=Decimal('20.006')))

    def test_unit_eighty_boundary_and_customer_and_twenty_digits(self):
        self.quote()
        self.old('PPriceListVat','erp_base',LengthDn=0,LengthUp=80,Unit=1,PhaseID='RC07')
        self.assertEqual(self.result('fn_GetPriceUnit',charging='01',gray_quantity=80,phase='RC07'),1)
        self.assertEqual(self.result('fn_GetPriceUnit',charging='01',gray_quantity=81,color='123',customer='C'),4)
        self.assertEqual(self.result('fn_GetPriceUnit',charging=None,weight=None,color='123',customer='NO'),2)

    def test_original_unit_overflow_is_reported_without_replacing_raw_value(self):
        self.old('PPriceListVat','erp_base',LengthDn=0,LengthUp=80,Unit=300,PhaseID='RC07')
        result=calculate('fn_GetPriceUnit',{'weight':10,'phase':'RC07'})
        self.assertEqual(result['rows'][0]['value'],300)
        self.assertEqual(len(result['supplemental_rows']),1)

    def test_basics_price_zero_fallback_and_open_closed_endpoints(self):
        self.old('CusBasicsPrice','erp_sales',SheetSeries='S',CustomerID='C')
        self.old('CusBasicsPriceDetail','erp_sales',SheetSeries='S',GradeID='G',StuffRatio1=0,StuffRatio2=1,FormulaCost1=1,FormulaCost2=2,Price=0)
        self.old('CusBasicsPriceDetail','erp_sales',SheetSeries='S',GradeID='G',StuffRatio1=2,StuffRatio2=3,FormulaCost1=0,FormulaCost2=1,Price=2500)
        self.assertEqual(self.result('fn_ColorNum_BasicsPrice',customer='C',grade='G',cost=Decimal('.5'),dosage=1),Decimal('2.5'))
        self.assertEqual(self.result('fn_ColorNum_BasicsPrice',customer='C',grade='G',cost=2,dosage=0),0)

    def test_pack_curve_return_original_maxvalue_not_assumed_price(self):
        self.old('PProcess','erp_base',ProcessID='P',Price=-2)
        self.assertEqual(self.result('fn_GetPackPrice',process='P'),-2)
        self.assertEqual(self.result('fn_GetPackQtyPrice',process='P'),-2)
        self.old('PDyeCurve','erp_base',CurveID='C',PhaseID='P',DyePhase=1,MaxValue=4)
        self.assertEqual(self.result('fn_GetDyePrice',phase='P'),4)

    def test_extra_charge_ignores_unassigned_product_branch_and_preserves_candidates(self):
        self.old('QuoteItemPrice','erp_sales',CustomerID='C',Item='I',ProdID='P',Price=999)
        self.old('QuoteItemPrice','erp_sales',CustomerID=None,Item='I',ProdID=None,Price=3,Unit='4')
        self.assertEqual(self.result('fn_GetJObSheetNoAttePrice',customer='C',service='I'),3)
        self.assertEqual(self.result('fn_GetJObSheetNoAttePriceUnit',customer='C',service='I'),'4')
        self.old('CusBasicsPrice','erp_sales',SheetSeries='S',CustomerID='C')
        self.old('CusExtraCharge','erp_sales',SheetSeries='S',PayService='I',Price=-5,PriceUnit='2')
        self.assertEqual(self.result('fn_GetJObSheetNoAttePrice',customer='C',service='I'),-5)

    def test_remark_input_is_not_digit_normalized_and_null_resets_accumulator(self):
        for text in ['A',None,'B']:self.old('QuoteDetail','erp_sales',ColorNum='X12',Remarks=text)
        self.assertEqual(self.result('fn_GetPriceRemark',color='12'),'B')
        self.assertEqual(self.result('fn_GetPriceRemark',color='X12'),'')

    def test_six_component_price_added_deducted_special_and_overlapping_vats(self):
        self.old('JobSheet','erp_production',SheetNo='J',SheetSeries='J',CustomerID='C',ProdID='G',ColorNum='C',Weight=10)
        self.old('PGray','erp_base',GrayID='G',FabricKindID='ZN')
        self.old('DyeRecipe',ColorNum='C',ColorDepthID='01',GradeID='G',Fluorescence='F')
        self.old('FixedPrice','erp_sales',SheetSeries='P',CustomerID='C')
        self.old('FixedPriceDetail','erp_sales',SheetSeries='P',DetailNo='D',FabricKind='ZN',ColorDepthID='01',CusPrice=10)
        self.old('FixedPriceAtte','erp_sales',DetailNo='D',AtteCode='UNUSED')
        for code,price in [('EXTRA',3),('UNUSED',2),('23053104',99)]:
            self.old('QuoteItemPrice','erp_sales',SheetSeries='P',Item=code,Price=price)
        for code in ['EXTRA','23053104']:self.old('JobAtte','erp_production',SheetSeries='J',FieldType='05',AtteCode=code)
        self.old('PFieldValid','erp_base',FieldType='fluorescence',Code='F',NumValue=4)
        self.old('PFieldValid','erp_base',FieldType='ColorNumGradeID',Code='G',NumValue=5)
        for price in [6,100]:self.old('FixedCanDetail','erp_base',SheetSeries='P',FabricKindID='ZN',Weight1=0,Weight2=10,Price=price)
        for kind,expected in enumerate([26,10,3,2,4,5,6,11,15]):
            self.assertEqual(self.result('fn_NewGetDyePrice',job='J',kind=kind),expected)
        self.assertIsNone(self.result('fn_NewGetDyePrice',job='J',kind=99))

    def test_tech_price_preserves_duplicate_lines_and_null_customer_price_prevents_fallback(self):
        self.old('ProdOut','erp_warehouse',SheetSeries='S',CustomerID='C')
        self.old('ProdOutDetail','erp_warehouse',SheetSeries='S',DetailNo='D',JobSheetNo='J')
        for code in ['I','I','NULL']:
            self.old('ProdOutPriceAtte','erp_warehouse',SheetSeries='S',DetailNo='D',PriceUnit='4',FieldType='05',AtteValue=code)
        self.old('QuoteItemPrice','erp_sales',CustomerID=None,Item='I',Price=3)
        self.old('QuoteItemPrice','erp_sales',CustomerID='C',Item='NULL',Price=None)
        self.old('QuoteItemPrice','erp_sales',CustomerID=None,Item='NULL',Price=999)
        self.assertEqual(self.result('fn_GetTechPrice',job='J',detail='D'),6)
        self.assertIsNone(self.result('fn_GetTechPrice',job='NONE',detail='D'))

    def sample(self,**values):return self.old('DyeDipsRecord',**{'SheetSeries':'D','SheetNo':'D','ColorNum':'C','ColorNo':'N','SheetDate':self.at,'StuffDosage':1,**values})

    def material(self,**values):
        self.old('DyeDipsRecordPhase',SheetSeries='D',PhaseNo=1,PhaseID='P')
        self.old('DyeDipsRecordDetail',SheetSeries='D',PhaseNo=1,StuffNo=1,StuffID='M',AmountA=2,AmountB=5)
        return self.old('PStuff','erp_base',**{'StuffID':'M','Name':'普通染料','StuffType':'S','StuffKindID':'1',**values})

    def test_all_depth_thresholds_and_original_variants_distinct(self):
        for amount,expected in [(.1,'01'),(.5,'02'),(2.5,'03'),(5,'07'),(50,'OLD'),(-1,'OLD')]:
            self.assertEqual(depth_code('Sp_DyeDipsRecord','OLD',amount,None,False,True,False),expected)
        for amount,expected in [(Decimal('.199'),'01'),(Decimal('.2'),'02'),(1,'03')]:
            self.assertEqual(depth_code('Sp_DyeDipsRecord2','OLD',amount,None,False,True,False),expected)
        self.assertEqual(depth_code('Sp_DyeDipsRecord2','OLD',0,'本白洗水',False,False,False),'04')
        self.assertEqual(depth_code('Sp_DyeDipsRecord2','OLD',0,'其他',False,False,False),'07')
        self.assertEqual(depth_code('Sp_DyeDipsRecord2','OLD',0,None,False,False,False),'OLD')

    def test_modern_cost_max_columns_xml_names_and_undo_all_targets(self):
        item=self.sample();self.material()
        self.old('PFieldValid','erp_base',FieldType='DyePhase',Code='P',Name='染&色',Mnemonic='染色',Description='染色')
        color=self.old('PColorNum','erp_base',ColorNum='C',ColorNo='N',IsDoubleDye=1)
        before=snapshot(item)
        apply(item,self.actor,'Sp_DyeDipsRecord','selected',**self.event);item.refresh_from_db();color.refresh_from_db()
        self.assertEqual((item.old_cost,item.old_cost_quote,item.old_dye_phase_name),(5,5,'染&amp;色'))
        self.assertEqual(item.old_color_depth_id,'02');self.assertIsNone(color.old_is_double_dye)
        undo(item,self.actor,**self.event);item.refresh_from_db();color.refresh_from_db()
        self.assertEqual(color.old_is_double_dye,1)
        for field in item.SOURCE_FIELDS.values():self.assertEqual(snapshot(item)[field],before[field])

    def test_global_fastness_is_cross_document_and_scope_is_not_silent(self):
        item=self.sample(StuffDosage=0);other=self.sample(SheetSeries='OTHER',ColorNum='OTHER')
        self.old('DyeDipsRecordDetail',SheetSeries='OTHER',PhaseNo=99,StuffNo=1,StuffID='HIGH')
        self.old('PStuff','erp_base',StuffID='HIGH',GaoLaodu=True)
        result=apply(item,self.actor,'Sp_DyeDipsRecord','selected',**self.event)
        other.refresh_from_db();item.refresh_from_db()
        self.assertEqual(other.old_gao_laodu,'高牢度染料');self.assertIsNone(item.old_color_depth_id)
        self.assertIn(other.pk,[row['record_id'] for row in result['rows'] if row['entity']==item._meta.label])

    def test_original_batch_variant_and_double_dye_special_groups(self):
        item=self.sample(StuffDosage=0,ColorID='本白');other=self.sample(SheetSeries='OTHER',StuffDosage=0,ColorID='洗水')
        color=self.old('DyeLabColor',ColorNum='C',ColorNo='OTHER')
        apply(item,self.actor,'Sp_DyeDipsRecord10','original',**self.event)
        item.refresh_from_db();other.refresh_from_db()
        self.assertEqual((item.old_color_depth_id,item.old_is_double_dye),('04',2))
        self.assertEqual((other.old_color_depth_id,other.old_is_double_dye),('05',2))
        color.refresh_from_db();self.assertEqual(color.old_color_depth_id,'05')

    def test_people_zero_null_and_duplicate_people_slots_are_preserved(self):
        item=self.sample(EmpID='E',EmpID1='E',EmpID2='',EmpID3=None)
        apply(item,self.actor,'Sp_DyeDipsRecord_EmpID','selected',**self.event);item.refresh_from_db();self.assertEqual(item.old_num,Decimal('.5'))
        undo(item,self.actor,**self.event)
        item.old_emp_id='';item.old_emp_id1='';item.save()
        result=apply(item,self.actor,'Sp_DyeDipsRecord_EmpID','selected',**self.event);item.refresh_from_db()
        self.assertIsNone(item.old_num);self.assertEqual(len(result['supplemental_rows']),1)

    def test_variant_scope_failure_rolls_back_and_later_changes_prevent_undo(self):
        item=self.sample();self.material();color=self.old('PColorNum','erp_base',ColorNum='C')
        def query(name,module):return reader(name,module).none() if name=='PColorNum' else reader(name,module)
        with self.assertRaises(ValidationError):apply(item,self.actor,'Sp_DyeDipsRecord','selected',query=query,**self.event)
        item.refresh_from_db();self.assertIsNone(item.old_color_depth_id)
        apply(item,self.actor,'Sp_DyeDipsRecord','selected',**self.event)
        item.old_color_depth_id='LATER';item.save()
        with self.assertRaises(ValidationError):undo(item,self.actor,**self.event)

    def test_schedule_copies_actual_fields_and_allows_explicit_reprint(self):
        color=self.old('DyeLabColor',SheetSeries='L',ColorNo='N',ColorNum='C',Spec='原规格')
        self.old('DyeLabMain',SheetSeries='L',CustomerID='CUSTOMER')
        item=schedule(color,self.actor,'DyeDipsRecord','A','E','S',**self.event)
        self.assertEqual((item.old_customer_id,item.old_color_num,item.old_spec),('CUSTOMER','C','原规格'))
        self.assertIsNone(item.source_batch_id)
        self.assertFalse(schedule_preview(color)[0]['rows'][0]['original_visible'])
        second=schedule(color,self.actor,'DyeDipsRecordBulk','B','E','S',**self.event)
        self.assertNotEqual(item.old_sheet_series,second.old_sheet_series)

    def trial(self,**values):return self.old('ProdTest','erp_quality',**{'SheetSeries':'T','SheetKind':7,'EmpID':'E','JobSheetNo':'J',
        'Value38':'GX41','Value39':'M','Value40':'PH','CreateDate':self.at,**values})

    def staff(self):
        self.old('PShift','erp_base',ShiftID='S',ClassID='03',StationID='02')
        self.old('PShiftEmp','erp_base',ShiftID='S',EmpID='E')

    def test_trial_replaces_original_work_and_restores_without_deleting(self):
        item=self.trial();self.staff()
        old=self.old('WProcess','erp_production',WProcessNo='OLD',OrderSheetNo='T')
        child=self.old('WProcessStep','erp_production',WPStepNo='OLDSTEP',WProcessNo='OLD')
        result=apply_trial(item,self.actor,**self.event)
        self.assertEqual(len(result['result_rows']),3)
        work=active(reader('WProcess','erp_production')).get();self.assertEqual(work.old_process_no,67)
        step=active(reader('WProcessStep','erp_production')).get();self.assertEqual((step.old_program_id,step.old_dye_process_id),('933','加色'))
        undo_trial(item,self.actor,**self.event)
        self.assertEqual(active(reader('WProcess','erp_production')).get().pk,old.pk)
        self.assertEqual(active(reader('WProcessStep','erp_production')).get().pk,child.pk)
        self.assertEqual(reader('WProcess','erp_production').count(),2)

    def test_trial_missing_phase_keeps_originals_and_mismatch_visible(self):
        item=self.trial(Value40='',StuffID='A',CompareStuffID='B');self.staff()
        report=trial_preview(item)[0];self.assertFalse(report['rows'][0]['original_comparison_passed'])
        old=self.old('WProcess','erp_production',WProcessNo='OLD',OrderSheetNo='T')
        self.assertEqual(apply_trial(item,self.actor,**self.event)['result_rows'],[])
        self.assertTrue(active(reader('WProcess','erp_production')).filter(pk=old.pk).exists())

    def test_trial_other_process_uses_readdition_and_scope_is_complete(self):
        item=self.trial(Value38='GX42');self.staff()
        result=apply_trial(item,self.actor,**self.event)
        work=active(reader('WProcess','erp_production')).get();self.assertEqual(work.old_process_no,68)
        step=active(reader('WProcessStep','erp_production')).get();self.assertEqual(step.old_program_id,'934')

    def test_trial_same_series_all_candidates_and_reverse_dependency(self):
        first=self.trial();self.staff()
        second=self.trial(JobSheetNo='J2',Value38='GX42')
        result=apply_trial(first,self.actor,**self.event)
        self.assertEqual(len(result['candidate_rows']),2)
        work=active(reader('WProcess','erp_production')).get();self.assertEqual(work.old_job_sheet_no,'J2')
        apply_trial(second,self.actor,**self.event)
        with self.assertRaises(ValidationError):undo_trial(first,self.actor,**self.event)
        undo_trial(second,self.actor,**self.event);undo_trial(first,self.actor,**self.event)
        self.assertEqual(active(reader('WProcess','erp_production')).count(),0)

    def test_seven_trial_entries_preserve_values_and_addcolor_save_hook_rebuilds(self):
        from plugins.erp_base.source_services import write
        self.staff();model=reader('ProdTest','erp_quality').model
        for entry in ['ProdTest_All','ProdTest_ColorFastness','ProdTest_PH','ProdTest_Shrinkage','ProdTest_Strength','ProdTest_WaterQuality']:
            item=write(model,{'_entry':entry,'old_value1':'异常原值-0','old_stuff_id':'A','old_compare_stuff_id':'B'},actor=self.actor)
            self.assertEqual(item.old_value1,'异常原值-0')
        item=write(model,{'_entry':'ProdTest_AddColorProduct','old_emp_id':'E','old_value38':'GX41','old_value40':'P','old_job_sheet_no':'J'},actor=self.actor)
        self.assertEqual(active(reader('WProcess','erp_production')).get().old_process_no,67)
        write(model,{'old_value38':'GX42'},instance=item,actor=self.actor)
        self.assertEqual(active(reader('WProcess','erp_production')).get().old_process_no,68)
        undo_trial(item,self.actor,**self.event)
        self.assertEqual(active(reader('WProcess','erp_production')).count(),0)

    def test_http_actions(self):
        response=self.client.post('/api/system/erp_sales_sourcedyequote/quote_function/',{'function':'fn_GetPackPrice','process':'GX'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        item=self.sample();root=f'/api/system/erp_sampling_sourcedyedyedipsrecord/{item.pk}/'
        data={'variant':'Sp_DyeDipsRecord','scope':'selected','at':self.at.isoformat(),'reason':'接口核对'}
        for name,body in [('preview_sample_variant',{key:data[key] for key in ['variant','scope']}),
                          ('apply_sample_variant',data),('undo_sample_variant',{key:data[key] for key in ['at','reason']})]:
            response=self.client.post(root+name+'/',body,format='json');self.assertEqual(response.status_code,200,response.data)

    def test_http_schedule_and_trial_actions(self):
        color=self.old('DyeLabColor',ColorNum='C',ColorNo='N')
        root=f'/api/system/erp_sampling_sourcedyedyelabcolor/{color.pk}/'
        response=self.client.post(root+'sample_schedule_options/',{},format='json');self.assertEqual(response.status_code,200,response.data)
        body={'entry':'DyeDipsRecord','version':'A','at':self.at.isoformat(),'reason':'接口排单'}
        response=self.client.post(root+'schedule_sample/',body,format='json');self.assertEqual(response.status_code,200,response.data)
        item=self.trial();self.staff();root=f'/api/system/erp_quality_sourcedyeprodtest/{item.pk}/'
        event={'at':self.at.isoformat(),'reason':'试验接口'}
        for action,body in [('preview_trial_work',{}),('apply_trial_work',event),('undo_trial_work',event)]:
            response=self.client.post(root+action+'/',body,format='json');self.assertEqual(response.status_code,200,response.data)
