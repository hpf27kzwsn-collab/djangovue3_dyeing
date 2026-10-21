"""第五阶段以非空、重复、负数及完整恢复检验原行为。"""
from decimal import Decimal
from django.test import TestCase
from django.db import transaction
from .test_phase_report_audit import create,at
from plugins.erp_base.source_phase5_reports import report,QUERIES
from plugins.erp_base.source_phase5_functions import calculate
from plugins.erp_base.source_phase5_operations import perform
from plugins.erp_base.source_phase3_operations import source


class Phase5Tests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.actor=get_user_model().objects.create(username='phase5',name='第五阶段')

    def params(self,**values):
        from plugins.erp_base.source_phase5_api import inputs
        return {**{k:f.get_default() for k,f in inputs([]).items() if k!='name'},**values}

    def op(self,name,**p):return perform(name,self.params(**p),self.actor)

    def undo(self,result):return self.op('phase5_undo',**result['undo'])

    def test_all_registered_reports_execute(self):
        for name in QUERIES:
            with self.subTest(name=name),transaction.atomic():
                r=report(name,self.params(startdate=at(),enddate=at(3),newstime=at(),newetime=at(3)))
                self.assertIn('rows',r)

    def test_function_duplicates_and_null_propagation(self):
        create('JobSheet',SheetSeries='J',SheetNo='N')
        for n in ['A','A','B']:create('JobCombine',SheetSeries='J',JobSheetNo=n)
        r=calculate('fn_CombineSheetNos',self.params(jobsheetno='N'))
        self.assertEqual(r['rows'][0]['result'],'A|A|B');self.assertEqual(len(r['result_sets'][0]['rows']),3)
        for text in ['纸筒','纸筒']:create('JobAtte',SheetSeries='J',FieldType='05',AtteValue=text,Description='0.2')
        self.assertEqual(calculate('fn_ProdOutPriceAtte',self.params(jobsheetno='N'))['rows'][0]['result'],'纸筒-纸筒')
        self.assertEqual(calculate('fn_ProdOutPriceAtte',self.params(jobsheetno='N',ischarge=1))['rows'][0]['result'],'纸筒:0.2,纸筒:0.2')
        for n in ['疵点','疵点']:create('p_FieldValid',FieldType='DefectName',Code='D',Name=n)
        create('RecordDefect',BarCode='B',DefectNo=1,DefectID='D')
        self.assertEqual(calculate('GetRecordDefect',self.params(barcode='B'))['rows'][0]['result'],'疵点,疵点')
        self.assertEqual(calculate('get_fsplit_CombineSheetNos',self.params(text='A||B|',separator='|'))['rows'],[{'JobSheetNo':'A'},{'JobSheetNo':''},{'JobSheetNo':'B'}])

    def test_loading_keeps_repeated_overage_negative_and_restores(self):
        a=create('GetClothNoticeDetail',SheetSeries='N',DetailNo='D',Rolls=5,ReceivingRolls=1)
        b=create('GetClothNoticeDetail',SheetSeries='N',DetailNo='D',Rolls=5,ReceivingRolls=2)
        c=create('ClothGetMoneyDetail',SheetSeries='C',DetailNo='C1',ThisRolls=3)
        r=self.op('SP_APP_LoadingConCloth',updetailnolist='D,D,D',receivingrollslist='2,7,-1',rowllslist='5,5,5',clothgetdetailnolist='C1,C1,C1',addrdlvlist='甲,乙,丙')
        a.refresh_from_db();b.refresh_from_db();c.refresh_from_db()
        self.assertEqual((a.old_receiving_rolls,b.old_receiving_rolls,c.old_this_rolls),(9,10,11))
        self.assertEqual(a.old_receiving_type,'3');self.assertTrue(r['notes'])
        self.undo(r);a.refresh_from_db();b.refresh_from_db();c.refresh_from_db()
        self.assertEqual((a.old_receiving_rolls,b.old_receiving_rolls,c.old_this_rolls),(1,2,3))

    def test_split_function_null_and_case_insensitive_separator(self):
        self.assertEqual(calculate('get_fsplit_CombineSheetNos',self.params(text='AAxBBXCC',separator='x'))['rows'],[{'JobSheetNo':'AA'},{'JobSheetNo':'BB'},{'JobSheetNo':'CC'}])
        self.assertEqual(calculate('get_fsplit_CombineSheetNos',self.params(text='AA|BB',separator=None))['rows'],[{'JobSheetNo':'AA|BB'}])
        self.assertEqual(calculate('get_fsplit_CombineSheetNos',self.params(text=None,separator='|'))['rows'],[])
        self.assertEqual(calculate('get_fsplit_CombineSheetNos',self.params(text=None,separator=''))['rows'],[])

    def test_save_cloth_preserves_duplicate_negative_details_and_replacement(self):
        h=create('ClothGetMoney',SheetSeries='C',SheetNo='N',SheetDate=at(),CustomerID='OLD')
        old=create('ClothGetMoneyDetail',SheetSeries='C',DetailNo='C-001',Rolls=10)
        r=self.op('Sp_App_SaveClothGetMoney',upsheetseries='C',customerid='NEW',addrdlv='厂区收货地址'*10,prodidlist='A,A',rollslist='-2,-2')
        self.assertEqual(source('ClothGetMoney').get().old_addr_dlv,'厂区收货地址'*10)
        self.assertEqual(list(source('ClothGetMoneyDetail').values_list('old_rolls',flat=True)),[Decimal('-2')]*2)
        self.assertEqual(type(old).objects.count(),3)
        self.undo(r);self.assertEqual(list(source('ClothGetMoneyDetail').values_list('pk',flat=True)),[old.pk])
        self.assertEqual(source('ClothGetMoney').get().pk,h.pk)

    def test_upload_delete_all_same_guid_and_restore(self):
        a=create('APPUploadFilesInfo',Guid='G',SaveFileName='a.jpg');b=create('APPUploadFilesInfo',Guid='G',SaveFileName='b.jpg')
        r=self.op('sp_App_DeleteUploadFile',guid='G',empid='E')
        self.assertEqual(source('APPUploadFilesInfoDel').count(),2);self.assertEqual(source('APPUploadFilesInfo').count(),0)
        self.assertEqual(r['rows'][0]['delFileName'],'b.jpg')
        self.undo(r);self.assertEqual(source('APPUploadFilesInfo').count(),2);self.assertEqual(source('APPUploadFilesInfoDel').count(),0)

    def test_attributes_use_preinsert_snapshot_keep_duplicate_dictionary(self):
        for n in ['甲','乙']:create('p_FieldValidSub',FieldType='AtteKind',Code='05',SubCode='23053101',Name=n,SortValue=1)
        create('JobProcess',SheetSeries='J',ProcessNo=1,ProcessID='GX09')
        r=self.op('AddDeleteJobAtte',sheetseries='J')
        self.assertEqual(source('JobAtte').count(),2)
        self.undo(r);self.assertEqual(source('JobAtte').count(),0)

    def test_out_detail_loss_and_customer_yard_trigger(self):
        from plugins.erp_base.source_phase3_operations import create as save
        a=save('ProdOutDetail',{'SheetSeries':'O','DetailNo':'D','JobSheetNo':'J','GrayQty':100,'WeightQty':90,'Rolls':2,'Jobattes6':'1','Jobattes8':'2'},self.actor)
        self.assertAlmostEqual(a.old_greal_loss,-16)
        create('RecordYield',JobSheetNo='J',RollNo='1',CustomerID='064',Yard=123)
        create('RecordYield',JobSheetNo='J',RollNo='1',CustomerID='000',Yard=999)
        b=save('ProdOutRecord',{'SheetSeries':'O','DetailNo':'D','RollNo':'1'},self.actor)
        self.assertEqual(b.old_yard,123)

    def test_transfer_delete_retains_all_duplicates_then_restores(self):
        create('GrayOut',SheetSeries='O',SheetKind=26)
        for i in range(2):
            create('SemiIn',SheetSeries='I'+str(i),GrayOutSheetNo='O')
            create('SemiInDetail',SheetSeries='I'+str(i),ReceSheetNo='D',Rolls=-3)
            create('SemiStockBook',BookNo=i+1,SheetSeries='I'+str(i),InRolls=-3)
        unrelated=create('SemiIn',SheetSeries='I0',GrayOutSheetNo='OTHER')
        r=self.op('Sp_GrayOutTurn_Delete',sheetseries='O')
        self.assertEqual(source('SemiInDetail').count(),0)
        self.assertEqual(list(source('SemiIn').values_list('pk',flat=True)),[unrelated.pk])
        self.undo(r);self.assertEqual(source('SemiInDetail').count(),2);self.assertEqual(source('SemiStockBook').count(),2)

    def test_delivery_trigger_null_job_targets_blank_job_and_padded_customer(self):
        from plugins.erp_base.source_phase3_operations import create as save
        blank=create('ProdOutDetail',SheetSeries='O',DetailNo='D',JobSheetNo='',GRealLoss=9)
        null=save('ProdOutDetail',{'SheetSeries':'O','DetailNo':'D','JobSheetNo':None,'GrayQty':100,'WeightQty':90},self.actor)
        blank.refresh_from_db();self.assertEqual(blank.old_greal_loss,-10);self.assertIsNone(null.old_greal_loss)
        create('RecordYield',JobSheetNo='',RollNo='1',CustomerID='064 ',Yard=-12)
        row=save('ProdOutRecord',{'SheetSeries':'O','DetailNo':'D','RollNo':'1'},self.actor)
        self.assertEqual(row.old_yard,-12)

    def test_gray_detail_retire_restores_assignment_and_progress(self):
        job=create('JobSheet',SheetSeries='J',SheetNo='N',JobSheetType=1,SumProcessRolls=12)
        assigned=create('JobAssign',SheetSeries='J',AssignNo='1',ReceSheetNo='R',Status=2)
        gray=create('JobGrayRecord',SheetSeries='J',ReceSheetNo='R',AssignedNo='A')
        line=create('GrayOutDetail',SheetSeries='O',AssignedNo='D',JobSheetNo='N',ReceSheetNo='R')
        r=self.op('phase5_retire',table='GrayOutDetail',record_id=line.pk)
        assigned.refresh_from_db();self.assertEqual(assigned.old_status,0)
        self.undo(r);assigned.refresh_from_db();gray.refresh_from_db();job.refresh_from_db()
        self.assertEqual(assigned.old_status,2);self.assertEqual(gray.old_assigned_no,'A');self.assertEqual(job.old_sum_process_rolls,12)

    def test_cloth_queries_keep_all_children_and_negative_remaining(self):
        for i in range(2):
            create('ClothGetMoney',SheetSeries=str(i),SheetDate=at(),CustomerID='C')
            create('ClothGetMoneyDetail',SheetSeries=str(i),DetailNo='D'+str(i),ProdID='F',Rolls=5,ThisRolls=-2)
        r=report('SP_APP_QueryClothGetMoney',self.params(size=1,startdate=at(1),enddate=at(3)))
        self.assertEqual(len(r['rows']),1);self.assertEqual(len(r['result_sets'][0]['rows']),2)
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):report('SP_App_QueryClothGetMoneyInfo',self.params(size=0))
        r=report('SP_App_QueryClothGetMoneyInfo',self.params(size=1))
        self.assertEqual(len(r['rows']),2);self.assertEqual(r['rows'][0]['residuerolls'],7)

    def test_delivery_modes_use_date_and_all_duplicate_details(self):
        create('ProdOut',SheetSeries='O',SheetNo='OUT',SheetDate=at(2,12),SheetKind=22)
        for qty in [5,-2]:create('ProdOutDetail',SheetSeries='O',DetailNo='D',JobSheetNo='J',WeightQty=qty,Rolls=1)
        p=self.params(startdate=at(1),enddate=at(3),searchmode=2)
        r=report('Sp_AppQueryProdOut',p);self.assertEqual(len(r['rows']),2);self.assertEqual(r['pagination']['sumweightqty'],3)
        self.assertEqual(report('Sp_AppQueryProdOut',{**p,'searchmode':1})['rows'],[])
        create('ProdLoading',SheetSeries='L',RightStatus=10);create('ProdLoadingDetail',SheetSeries='L',DetailNo='LD',OutDetailNo='D')
        self.assertEqual(len(report('Sp_AppQueryProdOut',{**p,'searchmode':1})['rows']),2)
        self.assertEqual(report('Sp_ProdOut_Query',p,now=at(3))['rows'][0]['weightqty'],3)

    def test_yarn_loading_keeps_duplicate_employees_and_negative_output(self):
        create('JobSheet',SheetSeries='J',SheetNo='N',ProdID='P')
        create('p_Gray',GrayID='P',ZTKind='C01')
        create('s_DBComboValue',ComboID='Z016',KeyValue='C01',DisplayValue='棉')
        create('FeelOfferMain',SheetSeries='F')
        create('FeelOfferDetail',SheetSeries='F',DetailNo='FD',ProdID='P',ProcessID='GX03',Price=2)
        create('WProcess',WProcessNo='W',JobSheetNo='N',StationID='03',ProcessID='GX03',StartTime=at(2,9),CurrKg=-10)
        for e in ['A','A']:create('JobShiftEmp',ProcessNo=1,WProcessNo='W',JobSheetNo='N',EmpID=e,ProcessID='GX03')
        r=report('Sp_QueryYarnLoading',self.params(newstime=at(2,8),newetime=at(3,8)))
        self.assertEqual(r['rows'][0]['c01_q'],-10);self.assertEqual(r['rows'][0]['sum_a'],-20)
        self.assertEqual(r['rows'][0]['emp01'],-20);self.assertEqual(len(r['rows']),2)

    def test_dye_loading_uses_last_finish_and_keeps_multiple_registration(self):
        create('JobSheet',SheetSeries='J',SheetNo='N',ProdID='P')
        create('p_Gray',GrayID='P',RSKind='R01')
        create('s_DBComboValue',ComboID='Z017',KeyValue='R01',DisplayValue='棉')
        create('WProcess',WProcessNo='W',JobSheetNo='N',StationID='06',ProcessID='GX07',DyeState='3',StartTime=at(2,9))
        create('JobShiftEmp',ProcessNo=1,WProcessNo='W',JobSheetNo='N',ProcessID='GX07',EmpID='A')
        for i in range(2):create('JobSheetRegister',JobSheetNo='N',ColorMatching='C',Rolls=-2,WeightQty=-10)
        r=report('Sp_QueryDyeLoading',self.params(newstime=at(2,8),newetime=at(3,8)))
        self.assertEqual(len(r['rows']),2);self.assertEqual(r['rows'][0]['rolls'],-2)
        self.assertEqual(r['rows'][0]['emp01'],1);self.assertEqual(r['rows'][0]['emp03'],1)

    def test_original_log_and_timer_retire_are_reversible_and_keep_rows(self):
        from django.utils import timezone
        from datetime import timedelta
        old=timezone.now()-timedelta(days=121)
        a=create('z_AccessLog',ID=7,StartTime=old)
        k=create('z_RevisionKey',ID='K',ModifyDate=old)
        d=create('z_RevisionDetail',ID='k ',RecordID='R')
        t=create('s_TimerJob',ItemID='T',ItemSQL='DELETE old_table')
        r=self.op('Sp_Delete_AccessLog')
        self.assertEqual(source('z_AccessLog').count(),0);self.assertEqual(type(a).objects.count(),1)
        self.assertEqual(source('z_RevisionDetail').count(),0)
        self.undo(r);self.assertEqual(source('z_AccessLog').count(),1);self.assertEqual(source('z_RevisionDetail').count(),1)
        r=self.op('s_TimerJob_Delete',itemid='T');self.assertEqual(source('s_TimerJob').count(),0)
        self.undo(r);self.assertEqual(source('s_TimerJob').get().old_item_sql,'DELETE old_table')

    def test_print_right_delete_checks_all_employee_roles(self):
        create('s_Roles',RoleNo='R');create('h_EmpRole',RoleNo='R',EmpID='E')
        create('s_Permission',RoleNo='R',FuncNo='F',IsCanPrint=False)
        create('s_RptMenu',RptNo=1,FuncNo='F',RptID='P');create('s_RptRight',RptID='P',EmpID='E',IsEnable=True)
        r=self.op('sp_FuncNoPrint_delete');self.assertEqual(source('s_RptRight').count(),0)
        self.undo(r);create('h_EmpRole',RoleNo='R2',EmpID='E');create('s_Permission',RoleNo='R2',FuncNo='F',IsCanPrint=True)
        self.op('sp_FuncNoPrint_delete');self.assertEqual(source('s_RptRight').count(),1)

    def test_automatic_stuff_cancel_keeps_other_book_kinds(self):
        create('StuffIn',SheetSeries='I');create('StuffInDetail',SheetSeries='I',DetailNo='D')
        for i,kind in enumerate([11,13,21]):create('StuffStockBook',BookNo=i+1,SheetSeries='I',BookKind=kind,StockFlag='N')
        r=self.op('sp_AuTo_Stuff_Cancel',jobsheetno='I')
        self.assertEqual(list(source('StuffStockBook').values_list('old_book_kind',flat=True)),[21])
        self.undo(r);self.assertEqual(source('StuffStockBook').count(),3)

    def test_fault_delete_only_draft_round_and_link_cancel_all_duplicates(self):
        for i in [-1,0,1]:create('MachineFaultArticleInfo',SheetSeries='F',Rounds=i,SerialNum=1)
        r=self.op('sp_App_DeleteFaultArticleListBySheetSeries',sheetseries='F',serialnumlist='1;1')
        self.assertEqual(source('MachineFaultArticleInfo').count(),2);self.undo(r)
        for i in range(2):create('s_DataLink',LinkNo='L')
        r=self.op('SP_UpdateLinkNoCancel',tablename1='s_DataLink',tablename2='s_DataLink',linkno='L')
        self.assertEqual(list(source('s_DataLink').values_list('old_link_no',flat=True)),['',''])
        self.undo(r);self.assertEqual(list(source('s_DataLink').values_list('old_link_no',flat=True)),['L','L'])

    def test_later_change_blocks_undo_without_partial_restore(self):
        from django.core.exceptions import ValidationError
        row=create('GetClothNoticeDetail',SheetSeries='N',DetailNo='D',ReceivingRolls=0)
        r=self.op('SP_APP_LoadingConCloth',updetailnolist='D',receivingrollslist='2',rowllslist='2',clothgetdetailnolist='',addrdlvlist='甲')
        type(row).objects.filter(pk=row.pk).update(old_receiving_rolls=9)
        with self.assertRaises(ValidationError):self.undo(r)
        row.refresh_from_db();self.assertEqual(row.old_receiving_rolls,9)

    def test_missing_loading_target_still_records_full_input(self):
        from plugins.erp_base.models import BusinessAction
        self.op('SP_APP_LoadingConCloth',updetailnolist='不存在,不存在',receivingrollslist='-1,2',rowllslist='1,1')
        saved=BusinessAction.objects.filter(action='phase5_no_match').get()
        self.assertEqual(saved.after['input']['receivingrollslist'],'-1,2')

    def test_quality_retire_preserves_duplicate_staff_and_other_shift(self):
        target=create('ColoringCheck',ID=1,JobSheetNo='J',WProcessNo='W',ShiftID='S')
        for s in ['S','S','OTHER']:create('ColorShiftEmp',JobSheetNo='J',WProcessNo='W',ShiftID=s,EmpID='E')
        r=self.op('phase5_retire',table='ColoringCheck',record_id=target.pk)
        self.assertEqual(source('ColorShiftEmp').count(),1)
        self.undo(r);self.assertEqual(source('ColorShiftEmp').count(),3)

    def test_posted_reference_blocks_physical_delete_but_retirement_retains_anomaly(self):
        from plugins.erp_base.source_phase5_triggers import removing
        from django.core.exceptions import ValidationError
        gray=create('GrayInRecord',ReceSheetNo='R',BarCode='B')
        create('JobGrayRecord',SheetSeries='J',ReceSheetNo='R',GrayBarCode='B')
        with self.assertRaises(ValidationError):removing(gray,self.actor)
        r=self.op('phase5_retire',table='GrayInRecord',record_id=gray.pk)
        self.assertTrue(r['notes']);self.assertEqual(source('JobGrayRecord').count(),1)
        self.undo(r);self.assertEqual(source('GrayInRecord').count(),1)

    def test_phase5_mutations_require_admin_and_reports_obey_scope(self):
        from rest_framework.test import APIRequestFactory,force_authenticate
        from system.views import view_for
        from system.catalog import ENTITIES
        from plugins.erp_base.source_phase3_operations import model
        entity=next(k for k,m in ENTITIES.items() if m==model('ClothGetMoney'))
        view=view_for(entity,model('ClothGetMoney'));factory=APIRequestFactory()
        request=factory.post('/',{'name':'s_TimerJob_Delete','itemid':'T'},format='json');force_authenticate(request,user=self.actor)
        response=view.as_view({'post':'phase5_operation'})(request)
        self.assertEqual(response.status_code,403)
        create('ClothGetMoney',SheetSeries='VISIBLE',SheetDate=at())
        create('ClothGetMoney',SheetSeries='HIDDEN',SheetDate=at())
        from plugins.erp_base.source_quality_reports import rows
        def reader(name,module):
            q=rows(name,module)
            return q.exclude(old_sheet_series='HIDDEN') if q.model.SOURCE_TABLE in ['ClothGetMoney','ClothGetMoneyDetail'] else q
        result=report('SP_APP_QueryClothGetMoney',self.params(startdate=at(1),enddate=at(3)),reader)
        self.assertEqual([r['sheetseries'] for r in result['rows']],['VISIBLE'])

    def test_process_delete_uses_original_last_job_assignment_not_union(self):
        from plugins.erp_base.source_phase5_triggers import removal_issues
        step=create('JobProcess',SheetSeries='J',ProcessNo=1,ProcessID='GX07')
        create('JobSheet',SheetSeries='J',SheetNo='FIRST')
        create('JobSheet',SheetSeries='J',SheetNo='LAST')
        create('WProcess',WProcessNo='W1',JobSheetNo='FIRST',ProcessID='GX07')
        self.assertEqual(removal_issues(step),[])
        row=create('WProcess',WProcessNo='W2',JobSheetNo='LAST',ProcessID='GX07')
        self.assertEqual(removal_issues(step),[{'table':'WProcess','ids':[row.pk]}])

    def test_delivery_views_keep_ten_roll_paging_and_synthetic_order_branches(self):
        create('ProdOutDetail',SheetSeries='O',DetailNo='D',JobSheetNo='J',WeightQty=-10)
        for i in range(11):create('ProdOutRecord',SheetSeries='O',DetailNo='D',RollNo=str(i).zfill(2),WeightQty=-1)
        r=report('v_ProdOutRecord',self.params())['rows']
        self.assertEqual(sorted((row['num'],row['colno']) for row in r),[(0,i) for i in range(1,11)]+[(1,1)])
        create('JobSheet',SheetSeries='J',SheetNo='N',JobSheetType=0)
        r=report('v_JobCombineOrder',self.params())['rows']
        self.assertEqual({row['checkno'] for row in r},{'A0001','B0001'})

    def test_noop_gray_out_delete_does_not_retire_actual_work(self):
        from plugins.erp_base.source_phase3_triggers import removing
        work=create('WProcess',WProcessNo='W',JobSheetNo='J')
        head=create('GrayOut',SheetSeries='O',WProcessNo='W')
        removing(head,self.actor)
        self.assertTrue(source('WProcess').filter(pk=work.pk).exists())

    def test_stuff_weight_retire_children_and_inbound_gx99_are_restored(self):
        weight=create('StuffWeight',SheetSeries='S',SheetNo='W')
        create('StuffWeightJobSheetNo',AutoID=1,SheetSeries='S',JobSheetNo='J')
        create('StuffCombineSheets',StuffSheetNo='W',JobSheetNo='J')
        r=self.op('phase5_retire',table='StuffWeight',record_id=weight.pk)
        self.assertEqual(source('StuffCombineSheets').count(),0);self.undo(r)
        self.assertEqual(source('StuffCombineSheets').count(),1)
        create('JobSheet',SheetSeries='J',SheetNo='N')
        step=create('JobProcess',SheetSeries='J',ProcessNo=1,ProcessID='GX99',StartTime=at(),WPWorker='甲')
        inbound=create('ProdIn',SheetSeries='I',JobSheetNo='N')
        r=self.op('phase5_retire',table='ProdIn',record_id=inbound.pk)
        step.refresh_from_db();self.assertIsNone(step.old_start_time)
        self.undo(r);step.refresh_from_db();self.assertEqual(step.old_wpworker,'甲')

    def test_defective_stock_view_includes_orphan_negative_dispatch(self):
        create('DefectiveOutDetail',SheetSeries='MISSING',DetailNo='O',DefectiveInDetailNo='ORPHAN',Rolls=-2,WeightQty=None,LengthQty=-5)
        r=report('vwDefectiveStock',self.params())['rows']
        self.assertEqual(len(r),1);self.assertEqual(r[0]['defectiveindetailno'],'ORPHAN')
        self.assertEqual(r[0]['stockrolls'],2);self.assertIsNone(r[0]['stockweightqty'])
