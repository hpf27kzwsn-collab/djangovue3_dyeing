from datetime import timedelta
from decimal import Decimal
from django.test import TestCase
from django.db import transaction
from .test_phase_report_audit import create,at
from plugins.erp_base.source_phase4_reports import report
from plugins.erp_base.source_phase4_api import inputs
from plugins.erp_base.source_phase3_operations import source


def params(**values):return {**{k:f.get_default() for k,f in inputs([]).items() if k!='name'},**values}


class Phase4RemainingTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.actor=get_user_model().objects.create(username='phase4-remaining',is_superuser=True)

    def test_attendance_variants_keep_duplicate_employee_and_replaced_rows(self):
        from plugins.erp_base.source_phase4_attendance import perform
        for _ in range(2):create('h_Employee',EmpID='E',DeptID='D',IsOut=False,IsNotKQ=False)
        create('h_Leave',SheetSeries='I',SheetKind=5,EmpID='E',BeginDate=at(2,8))
        create('h_Leave',SheetSeries='O',SheetKind=6,EmpID='E',BeginDate=at(2,20))
        old=create('EmpShiftClock',EmpID='OLD',dtDate=at(1).date())
        for name in ['sp_EmpID_CHECKINOUT','sp_EmpID_CHECK_Query','qry_Static_EmpTotal','sp_Static_Emp','sp_DPWorkQty_Query']:
            with self.subTest(name=name):
                r=perform(name,params(dtdate=at(2),eddate=at(2,23)),self.actor,now=at(3))
                self.assertEqual(source('EmpShiftClock').count(),2)
                self.assertTrue(type(old).objects.filter(pk=old.pk).exists())
                self.assertIn('rows',r)
                if name=='sp_EmpID_CHECKINOUT':
                    self.assertEqual(len(r['rows']),1)
                    self.assertEqual(r['rows'][0]['worktime'],24)
                    self.assertEqual(r['rows'][0]['workcount'],1)

    def test_pack_work_split_counts_duplicate_staff_and_keeps_negative_source(self):
        from plugins.erp_base.source_phase4_attendance import perform
        create('h_Employee',EmpID='E',DeptID='D',IsOut=False)
        create('RecordYield',BarCode='B',JobSheetNo='J',ShiftID='S',CustQty=-12,PackTime=at(2,10))
        for _ in range(2):create('RecordEmp',BarCode='B',EmpID='E')
        create('p_Shift',ShiftID='S');create('p_Process',ProcessID='GX20',Price=100)
        create('JobSheet',SheetSeries='J',SheetNo='J')
        r=perform('sp_DPWorkQty_Query',params(dtdate=at(2),eddate=at(2,23)),self.actor,now=at(3))
        self.assertEqual(source('PackWorkQtyDetail').get().old_qty,-12)
        self.assertEqual(source('RecordEmp').count(),2)
        self.assertEqual(source('PackWorkQty').get().old_qty,-12)
        self.assertTrue(r['notes'])

    def test_cross_card_progress_changes_all_duplicate_cards_and_keeps_next_process(self):
        from plugins.erp_base.source_phase4_operations import perform
        create('ProcessSchedule',JobSheetNo='MAIN',ProcessNo=1,CombineSheetNos='CHILD:2;')
        jobs=[create('JobSheet',SheetSeries=s,SheetNo='CHILD') for s in ['A','B']]
        for s in ['A','B']:
            create('JobProcess',SheetSeries=s,ProcessNo=2,ProcessID='GX20',StationID='12')
            create('JobProcess',SheetSeries=s,ProcessNo=3,ProcessID='GX99',StationID='29')
        perform('Sp_UpdateJobSheetAndJobProcessNT',params(sheetno='MAIN',processno=1,dpkind=0,worktime=at(2),workstatus=1,machineid='M'),self.actor)
        for job in jobs:job.refresh_from_db();self.assertEqual(job.old_curr_process_no,2);self.assertEqual(job.old_next_process_id,'GX99')
        self.assertEqual(source('JobProcess').filter(old_status=1).count(),2)

    def test_craft_rebuild_keeps_old_and_selects_max_fields_independently(self):
        from plugins.erp_base.source_phase4_operations import perform
        old=create('StandCraft',SheetSeries='OLD')
        for series,assign in [('A',9),('B',1)]:
            create('JobSheet',SheetSeries=series,ProdID='P',CustomerID='C',ColorNum='X')
            create('JobAssign',SheetSeries=series,AssignNo=assign)
            create('JobProcess',SheetSeries=series,ProcessNo=1,ProcessID=series,PPName01='温度',TheoryValue01='80')
        r=perform('GetCustProdstandcraft',params(),self.actor)
        self.assertEqual(source('StandCraft').get().old_spec,'9')
        self.assertEqual(source('StandCraftDetail').get().old_process_id,'B')
        self.assertTrue(type(old).objects.filter(pk=old.pk).exists());self.assertEqual(len(r['retained']),1)

    def test_fault_count_month_zero_spine_and_duplicate_status_join(self):
        for n in range(2):create('p_MachineFaultStatus',StatusID=n,StatusName='处理中',CompleteStatus='未完成')
        create('MachineFault',SheetSeries='M',SheetDate=at(2),MachineID='MC',FlowStatus='处理中')
        r=report('SP_APP_QueryFaultBillCount',params(starttime=at(1),endtime=at(3),counttype='月',machinelist='全部'))
        self.assertEqual(r['rows'][0]['billcount'],2)
        self.assertEqual(r['result_sets'][0]['rows'][-1]['billcount'],2)

    def test_equipment_usage_eight_results_keep_negative_and_duplicate_details(self):
        create('ArticleOut',SheetSeries='A',SheetDate=at(2))
        for qty in [-2,3]:create('ArticleOutDetail',SheetSeries='A',DetailNo='D',ArticleID='P',MachineID='M',OutQty=qty,Total=qty*10)
        r=report('sp_App_QueryMachineArticleUseTotal',params(startdate=at(1),enddate=at(3),machineid='M',totalmode=0))
        self.assertEqual(len(r['result_sets']),7)
        self.assertEqual(r['rows'][-1]['totalcount'],1)
        self.assertEqual(source('ArticleOutDetail').count(),2)

    def test_defect_ratios_include_duplicate_job_join(self):
        for s in ['A','B']:create('JobSheet',SheetSeries=s,SheetNo='J')
        create('WDefect',SheetSeries='D',SheetNo='D',SheetDate=at(2),SheetType=0,JobSheetNo='J',DefectQty=10,DefectKind='K',Defects='dt003')
        r=report('SP_WDefectList',params(startdate=at(1),enddate=at(3)))
        self.assertEqual(r['rows'][0]['bl1'],'100.00%')
        self.assertEqual(r['rows'][0]['bl2'],'染部责任100.00%')

    def test_wages_three_versions_return_nonempty_quantity_and_amount(self):
        create('JobSheet',SheetSeries='J',SheetNo='J',ProdID='P',AssignUnit=1)
        create('p_Gray',GrayID='P',FabricKindID='F')
        create('p_ProcessPrice',ProcessID='GX00',ProdKindID='F',Price=100)
        create('p_Shift',ShiftID='S',StationID='01')
        create('WProcess',WProcessNo='W',JobSheetNo='J',ProcessNo=1,ProcessID='GX00',StationID='01',ShiftID='S',CurrKg=100,CurrMeter=0,CurrDosage=100,CreateDate=at(2,10))
        create('JobShiftEmp',WProcessNo='W',JobSheetNo='J',ProcessNo=1,ProcessID='GX00',ShiftID='S',EmpID='E',Post='01')
        for name in ['Sp_OLD_QueryWagesStatisticsInfo1','Sp_OLD_QueryWagesStatisticsInfo2','Sp_QueryWagesStatisticsInfo']:
            with self.subTest(name=name),transaction.atomic():
                r=report(name,params(newstime=at(1),newetime=at(3),shiftid='S'))
                self.assertEqual(r['result_sets'][-1]['rows'][0]['empidqty'],100)
                self.assertEqual(r['result_sets'][-1]['rows'][0]['empidamount'],10)
                self.assertTrue(r['rows'])
