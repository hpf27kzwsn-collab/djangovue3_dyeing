"""第四阶段使用非空、重复、负数及原NULL结果核验，另做全部固定查询的结构执行。"""
from decimal import Decimal
from django.test import TestCase
from django.db import transaction
from .test_phase_report_audit import create,at
from plugins.erp_base.source_phase4_reports import QUERIES,report
from plugins.erp_base.source_phase4_functions import calculate,weighted_price


class Phase4QueryTests(TestCase):
    def test_registered_reports_execute(self):
        from plugins.erp_base.source_phase4_api import inputs
        p={k:f.get_default() for k,f in inputs([]).items() if k!='name'}
        for name in QUERIES:
            with self.subTest(name=name),transaction.atomic():
                value=report(name,{**p,'startdate':at(),'enddate':at(3)})
                self.assertIn('rows',value)

    def test_registered_functions_execute(self):
        from plugins.erp_base.source_phase4_functions import NAMES
        from plugins.erp_base.source_phase4_api import inputs
        p={k:f.get_default() for k,f in inputs([]).items() if k!='name'}
        for name in NAMES:
            with self.subTest(name=name),transaction.atomic():self.assertIn('rows',calculate(name,p))

    def test_weighted_price_uses_all_latest_carries_and_only_original_receipts(self):
        for family in ['Stuff','Article']:
            create(family+'Stock',StockDate=at(1),CarryDate=at(1),WareHouseID='W',**{family+'ID':'A'},PreMonthQty=100,PreMonthMoney=999)
            for money in [20,30]:
                create(family+'Stock',StockDate=at(2),CarryDate=at(2),WareHouseID='W',**{family+'ID':'A'},PreMonthQty=10,PreMonthMoney=money)
            for n,kind,qty,money in [(1,13,5,25),(2,16,-2,-10),(3,21,1000,9999)]:
                create(family+'StockBook',BookNo=n,BookDate=at(3),WareHouseID='W',**{family+'ID':'A'},BookKind=kind,InQty=qty,InMoney=money,OutQty=500,OutMoney=100)
            result=weighted_price(family,'A','W')
            self.assertEqual(result,{'qty':23,'money':65,'result':Decimal('2.83')})
        self.assertEqual(weighted_price('Stuff','missing','W')['result'],0)

    def test_attribute_concatenation_keeps_duplicate_rows_and_null_reset(self):
        create('JobSheet',SheetSeries='J',SheetNo='N')
        create('JobAtte',SheetSeries='J',FieldType='00',AtteValue='纸筒',Description='0.2kg')
        create('JobAtte',SheetSeries='J',FieldType='00',AtteValue='纸筒',Description='0.2kg')
        value=calculate('fn_ConcatJobAtte',{'jobsheetno':'N','ischarge':0})
        self.assertEqual(value['rows'][0]['result'],'纸筒 0.2kg+纸筒 0.2kg')
        self.assertEqual(calculate('fn_GetPaperTubeByJobNo',{'jobsheetno':'N'})['rows'][0]['result'],.4)
        create('JobAtte',SheetSeries='J',AtteValue=None)
        create('JobAtte',SheetSeries='J',AtteValue='末行')
        self.assertEqual(calculate('fn_JobAttelect',{'jobseries':'J'})['rows'][0]['result'],'末行')

    def test_equipment_results_keep_all_original_header_detail_sets(self):
        create('GetClothNotice',SheetSeries='G',Driver='D')
        create('GetClothNoticeDetail',SheetSeries='G',DetailNo='1',Rolls=-2)
        create('GetClothNoticeDetail',SheetSeries='G',DetailNo='1',Rolls=3)
        r=report('SP_SheetNoQueryGetClothNotice',{'sheetseries':'G'})
        self.assertEqual(len(r['rows']),1);self.assertEqual(len(r['result_sets'][0]['rows']),2)
        r=report('SP_APP_SheetNoQueryGetClothNotice',{'sheetseries':'G','detailno':'1'})
        self.assertEqual(len(r['result_sets'][0]['rows']),1)
        self.assertEqual(r['result_sets'][0]['rows'][0]['rolls'],3)

    def test_employee_names_preserve_duplicate_dictionary_and_null_reset(self):
        from plugins.erp_base.source_static_lookup import execute
        from plugins.erp_base.source_quality_reports import rows
        for code,name in [('A','甲'),('A','甲'),('B',None),('C','丙')]:create('h_Employee',EmpID=code,Name=name)
        self.assertEqual(execute("SELECT dye.ChangeIDListToEmpName('A;B;C',';') AS value",rows)[0]['value'],'丙')

    def test_shift_clock_crosses_day_and_view_counts_duplicate_steps(self):
        create('ShiftPlan',SheetSeries='S',ShiftID='2026-01',ClassID='C',BeginDate=1,EndDate=31)
        create('ShiftPlanDetail',SheetSeries='S',DetailNo='D',ShiftDay='02',BeginTime='20',EndTime='8')
        r=report('v_ShiftClock',{})['rows'][0]
        self.assertEqual(r['begintime'].day,2);self.assertEqual(r['endtime'].day,3)

    def test_external_program_mapping_preserves_local_rows_and_duplicate_matches(self):
        create('StuffWeight',SheetSeries='S',SheetNo='W',JobSheetNo='J',MachineId=1,RecipeType=0)
        create('StuffWeightPhase',SheetSeries='S',PhaseNo=1,ProgramID='P')
        r=report('v_StuffWeightQuery_To_LX',{})
        self.assertEqual(len(r['rows']),1);self.assertIsNone(r['rows'][0]['progid'])
        r=report('v_StuffWeightQuery_To_LX',{'machine_programs':[{'ProgNo':'P','ProgId':'1','MachineId':'1'}]*2})
        self.assertEqual(len(r['rows']),2)


class Phase4OperationTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.actor=get_user_model().objects.create(username='phase4',name='第四阶段')

    def run_operation(self,name,**values):
        from plugins.erp_base.source_phase4_operations import perform
        return perform(name,values,self.actor)

    def save(self,table,values,instance=None):
        from plugins.erp_base.source_services import write
        from plugins.erp_base.source_phase3_operations import model
        m=model(table)
        return write(m,{m.SOURCE_FIELDS[k]:v for k,v in values.items()},instance,actor=self.actor)

    def test_save_triggers_keep_duplicate_processes_and_stopped_material(self):
        create('JobProcess',SheetSeries='J',ProcessNo=1,ProcessID='GX')
        item=self.save('JobProcess',{'SheetSeries':'J','ProcessNo':1,'ProcessID':'GX'})
        self.assertEqual(type(item).objects.count(),2)
        create('p_Stuff',StuffID='S',Status=1)
        line=self.save('StuffWeightDetail',{'SheetSeries':'W','StuffNo':1,'PhaseNo':1,'StuffID':'S','RealQty':-1})
        self.assertEqual(line.old_real_qty,-1)

    def test_work_trigger_machine_transfer_and_original_zero_quantity(self):
        create('WProcess',WProcessNo='OLD',JobSheetNo='J',ProcessNo=2,StationID='06',DyeState='1',MachineID='M',StartTime=at())
        work=self.save('WProcess',{'WProcessNo':'NEW','JobSheetNo':'J','ProcessNo':2,'StationID':'06','DyeState':'3'})
        self.assertEqual(work.old_machine_id,'M');self.assertIsNotNone(work.old_end_time)
        create('p_Process',ProcessID='P',IsCanAddWorkQty=True,InputQtyCheckWay=0)
        work=self.save('WProcess',{'WProcessNo':'Z','JobSheetNo':'J','ProcessID':'P','StationID':'01','CurrKg':-5,'WorkQty':10})
        self.assertEqual(work.old_curr_kg,0);self.assertEqual(work.old_work_qty,0)

    def test_schedule_keeps_retired_invalid_row_and_start_plan(self):
        item=self.save('ProcessSchedule',{'JobSheetNo':'orphan','ProcessID':'P','ProcessNo':1})
        from plugins.erp_base.source_phase3_operations import source
        self.assertEqual(source('ProcessSchedule').count(),0)
        self.assertTrue(type(item).objects.filter(pk=item.pk).exists())
        self.assertEqual(source('DyeStartDateTime').count(),1)

    def test_customer_label_and_urgent_note_update_all_duplicate_jobs(self):
        for _ in range(2):create('JobSheet',SheetSeries='J',SheetNo='N',CustomerID='C')
        customer=create('p_Customer',CustomerID='C',LabelID='A')
        self.save('p_Customer',{'LabelID':'B'},customer)
        self.save('UrgentInStructDetail',{'JobSheetNo':'N','Remarks':'紧急'})
        from plugins.erp_base.source_phase3_operations import source
        self.assertEqual(list(source('JobSheet').values_list('old_label_id','old_hurry_info')),[('B','紧急'),('B','紧急')])

    def test_phase4_api_routes_and_non_admin_mutation(self):
        from rest_framework.test import APIClient
        client=APIClient();client.force_authenticate(self.actor)
        endpoint='/api/system/erp_production_sourcedyejobsheet/'
        self.assertIn(client.post(endpoint+'phase4_operation/',{'name':'Sp_JobPackRemarks'},format='json').status_code,[400,403])
        self.actor.is_superuser=True;self.actor.save()
        for action,data in [('phase4_report',{'name':'vw_jobsheet'}),('phase4_function',{'name':'fn_StuffPriceWeightedAverage','stuffcode':'S','warehouseid':'W'}),('phase4_operation',{'name':'Sp_JobPackRemarks'})]:
            response=client.post(endpoint+action+'/',data,format='json');self.assertEqual(response.status_code,200,response.data)
        for url,data in [('/api/system/erp_production_sourcedyemachinefault/phase4_equipment/',{'name':'Sp_APP_CheckGetClothNotice','driver':'D'}),
            ('/api/system/erp_production_sourcedyewprocess/phase4_attendance/',{'name':'sp_Static_Emp','dtdate':'2026-01-01T00:00:00+08:00','eddate':'2026-01-02T00:00:00+08:00'})]:
            response=client.post(url,data,format='json');self.assertEqual(response.status_code,200,response.data)

    def test_fault_article_duplicate_rounds_and_negative_qty_are_kept(self):
        from plugins.erp_base.source_phase4_equipment import perform
        old=create('MachineFaultArticleInfo',SheetSeries='S',Rounds=-1,SerialNum=1)
        create('MachineFaultArticleInfo',SheetSeries='S',Rounds=2,SerialNum=1)
        perform('sp_App_SaveFaultArticleListBySheetSeries',dict(sheetseries='S',serialnumlist='1;1',articleidlist='A;A',articlenamelist='a;a',speclist='s;s',qtylist='-1.25;2',kindlist='1;1'),self.actor)
        from plugins.erp_base.source_phase3_operations import source
        self.assertEqual(sorted(source('MachineFaultArticleInfo').filter(old_rounds=-1).values_list('old_qty',flat=True)),[Decimal('-1.3'),2])
        self.assertEqual(type(old).objects.count(),4)

    def test_cloth_save_keeps_rows_rejected_by_old_separate_check(self):
        from plugins.erp_base.source_phase4_equipment import perform
        p=dict(upsheetseries='',driver='D',licenseplate='',empid='',remarks='',customeridlist='C,C',rollslist='-2,3',addrdlvlist='A,A',prodidlist='P,P',clothgetdetailnolist='X,X')
        response=perform('Sp_APP_SaveGetClothNotice',p,self.actor)
        from plugins.erp_base.source_phase3_operations import source
        self.assertEqual(source('GetClothNoticeDetail').count(),2)
        self.assertEqual(perform('Sp_APP_CheckGetClothNotice',p,self.actor)['rows'][0]['Code'],101)
        self.assertTrue(response['notes'])

    def test_gray_actual_and_plan_are_separate_and_duplicates_count(self):
        job=create('JobSheet',SheetSeries='J')
        for assigned,qty,length in [('A',-2,0),('A',-2,0),('',9,5)]:
            create('JobGrayRecord',SheetSeries='J',AssignedNo=assigned,WeightQty=qty,LengthQty=length)
        self.run_operation('Sp_JobGrayRecord_JobSheet_Update',sheetseries='J');job.refresh_from_db()
        self.assertEqual(job.old_sum_assigned_rolls,2);self.assertEqual(job.old_sum_assigned_weight_qty,-4)
        self.assertEqual(job.old_pre_rolls,3);self.assertEqual(job.old_pre_vat_qty,5)

    def test_add_end_steps_and_keep_existing_duplicate_rows(self):
        create('JobSheet',SheetSeries='J',SheetNo='N',SheetStatus=0)
        create('JobProcess',SheetSeries='J',ProcessNo=1,ProcessID='A')
        create('JobProcess',SheetSeries='J',ProcessNo=1,ProcessID='A')
        for name in ['sp_JobProcess_New','sp_JobProcess_New1']:
            self.run_operation(name,jobsheetno='N')
        from plugins.erp_base.source_phase3_operations import source
        self.assertEqual(list(source('JobProcess').order_by('old_process_no').values_list('old_process_id','old_process_no')),[('A',1),('A',1),('GX98',2),('GX99',3)])

    def test_record_employees_replace_only_matching_group_and_retain_old_rows(self):
        create('RecordYield',BarCode='B',ShiftID='S')
        for code in ['E','E']:create('p_ShiftEmp',ShiftID='S',EmpID=code)
        old=create('RecordEmp',BarCode='B',EmpID='E');create('RecordEmp',BarCode='B',EmpID='OTHER')
        data=self.run_operation('Up_RecordEmp1',barcode='B')
        from plugins.erp_base.source_phase3_operations import source
        self.assertEqual(source('RecordEmp').count(),3);self.assertTrue(type(old).objects.filter(pk=old.pk).exists())
        self.assertEqual(len(data['retained']),1)

    def test_original_summary_xml_escapes_and_negative_quantity(self):
        job=create('JobSheet',SheetSeries='J')
        for _ in range(2):create('JobAssign',SheetSeries='J',AssignNo=1,PreField1='A&B',PreField5='F',Area='库位',MachineID='M',Rolls=-2,LotNo='L')
        create('JobAtte',SheetSeries='J',FieldType='01',AtteCode='1',AtteValue='A&B')
        self.run_operation('Sp_Update_JobSheet_Structure',sheetseries='J');job.refresh_from_db()
        self.assertEqual(job.old_structure,'A&amp;B');self.assertEqual(job.old_pack_remarks,'A&amp;B。')
        self.run_operation('UpdateJobSheet_Field',sheetseries='J');job.refresh_from_db()
        self.assertEqual(job.old_pbxx,'L,匹数-2.0条;L,匹数-2.0条')
