from decimal import Decimal
from django.test import TestCase
from django.db import transaction
from .test_phase_report_audit import create,at
from .test_source_phase4_remaining import params
from plugins.erp_base.source_phase4_reports import report
from plugins.erp_base.source_phase4_functions import calculate
from plugins.erp_base.source_phase3_operations import source


class Phase4DetailsTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.actor=get_user_model().objects.create(username='p4detail',is_superuser=True)

    def test_process_matrix_ignores_parameter_keeps_duplicates_and_27_slots(self):
        create('JobSheet',SheetSeries='A');create('JobSheet',SheetSeries='B')
        for n in range(29):create('JobProcess',SheetSeries='A',ProcessID='GX'+str(n),ProcessNo=n)
        create('JobProcess',SheetSeries='B',ProcessID='GX1',ProcessNo=1);create('JobProcess',SheetSeries='B',ProcessID='GX1',ProcessNo=1)
        r=calculate('F_JobProcessTable',{'sheetseries':'OTHER'})['rows']
        self.assertEqual(len(r),2);self.assertEqual(r[0]['ProcessID26'],'GX26')
        self.assertEqual(r[1]['ProcessID0'],r[1]['ProcessID1']);self.assertEqual(source('JobProcess').count(),31)

    def test_price_interval_lower_exclusive_upper_inclusive_and_negative(self):
        create('JobSheet',SheetSeries='J',SheetNo='J',ProdID='P',Weight='１２３克')
        create('p_Gray',GrayID='P',FabricKindID='F')
        create('p_ProcessPrice',ProcessID='GX09',ProdKindID='F',WeightDn=100,WeightUp=123,Price=-7)
        create('p_ProcessPrice',ProcessID='GX06',ProdKindID='F',QtyDn=10,QtyUP=20,Price=80)
        self.assertEqual(calculate('fn_ProcessIDPire',params(jobsheetno='J',processid='GX09'))['rows'][0]['result'],-7)
        self.assertIsNone(calculate('fn_ProcessIDPire',params(jobsheetno='J',processid='GX06',num=10))['rows'][0]['result'])
        self.assertEqual(calculate('fn_ProcessIDPire',params(jobsheetno='J',processid='GX06',num=20))['rows'][0]['result'],80)

    def test_new_production_calendar_aggregates_order_qty_and_keeps_daily_total(self):
        create('p_Machine',MachineID='M',StationID='06',KindName='K',MaxRolls=10)
        create('p_Gray',GrayID='P',FabricKindID='F')
        create('GWName',FabricKindID='F',GWName='K',MaxQty=100,SheetDate=at(1))
        create('OrderMain',SheetSeries='O',CustomerID='000',SheetDate=at(2,10))
        for n in range(2):create('OrderColor',SheetSeries='O',CheckNo=str(n),ProdID='P',GWName='K',OrderQty=-10)
        r=report('20260731',params(startdate=at(2),enddate=at(3)))['rows']
        selected=[v for v in r if v['日期']=='2026-01-02' and v['缸型']=='K']
        self.assertEqual(selected[0]['订单数量'],-20)
        self.assertEqual(selected[0]['全部订单缸数'],2)
        self.assertTrue(any(v['缸型']=='Z-总计' for v in r))

    def test_card_speed_returns_receipts_issues_totals_and_atte(self):
        create('JobSheet',SheetSeries='J',SheetNo='J',SheetDate=at(2),SheetStatus=0,PreRolls=10,SumAssignedRolls=10,AssignUnit=1,Finish=False)
        create('JobProcess',SheetSeries='J',ProcessNo=1,ProcessID='GX1')
        create('ProdOut',SheetSeries='O',SheetNo='OUT',SheetDate=at(2))
        create('ProdOutDetail',SheetSeries='O',JobSheetNo='J',Rolls=-1,WeightQty=-2)
        create('ProdIn',SheetSeries='I',SheetNo='IN',SheetDate=at(2),JobSheetNo='J',Rolls=3,WeightQty=6)
        create('JobAtte',SheetSeries='J',AtteValue='A')
        r=report('sp_App_S_QueryJobCardSpeedList',params(startdate=at(1),enddate=at(3)))
        self.assertEqual(len(r['rows']),1);self.assertEqual(len(r['result_sets']),3)
        movements=r['result_sets'][1]['rows'];self.assertEqual(len(movements),4)
        self.assertEqual(sum(v['rolls'] for v in movements if v['showsheetdate']=='汇总'),2)

    def test_inspection_and_care_header_and_fallback_projects_both_returned(self):
        for inspection in [False,True]:
            with self.subTest(inspection=inspection):
                table='InspectionLog' if inspection else 'MachineCareRecords';field='InspectDetailNo' if inspection else 'CarePlanDetailNo'
                create(table,SheetSeries='S',SheetNo='N',**{field:'CASE'})
                from plugins.erp_base.source_context import SourceBusinessParameter
                SourceBusinessParameter.objects.create(name='IsUseMachineInspectionCase' if inspection else 'IsUseMachineCase',value='Y')
                create('MachineCase',SheetSeries='CASE');create('MachineCaseProject',SheetSeries='CASE',DetailNo='D',DefaultValue='X')
                name='sp_App_GetInspectionLogBySheetSeries' if inspection else 'sp_App_GetMachineCareRecordsBySheetSeries'
                r=report(name,params(sheetseries='S'));self.assertEqual(r['rows'][0]['sheetno'],'N')
                self.assertEqual(r['rows'][0]['isusemachinecase'],0)
                self.assertEqual(r['result_sets'][0]['rows'][0]['OriValue'],'X')

    def test_upload_duplicate_guid_and_pdf_old_image_classification(self):
        from plugins.erp_base.source_phase4_equipment import perform
        p=dict(sheetseries='F',kind=0,uiindex=1,guid='G',orifilename='proof.PDF',savefilename='proof.pdf',filenameurl='/proof.pdf',savedate=at(2),userid='U')
        for _ in range(2):perform('sp_App_SaveUploadFilesInfo',p,self.actor)
        self.assertEqual(source('APPUploadFilesInfo').count(),2)
        self.assertEqual(set(source('APPUploadFilesInfo').values_list('old_file_type',flat=True)),{'image'})

    def test_original_automatic_output_noop_and_barcode_wrap_are_explicit(self):
        from plugins.erp_base.source_phase4_operations import perform,barcode
        create('JobSheet',SheetSeries='J',CreateDate=at(2),BarCode='260102999')
        self.assertEqual(barcode(at(2)),'260102000')
        r=perform('Sp_StuffRegisterAutoOutPut',params(sheetno='ANY'),self.actor)
        self.assertEqual(r['rows'],[{'msgmark':1}]);self.assertEqual(source('StuffOut').count(),0)

    def test_current_cloth_report_summary_and_closed_card_check_do_not_hide_duplicates(self):
        for _ in range(2):create('JobSheetReceive',JobSheetNo='J',CreateDate=at(2),Rolls=-1,WeightQty=-2,LengthQty=3)
        r=report('sp_App_S_QueryJobSheetReceiveList',params(startdate=at(1),enddate=at(3)))
        self.assertEqual(len(r['rows']),2);self.assertIn('2缸|-2.0匹|-4.00kg|6.00m',r['pagination']['TotalInfo'])
        create('JobSheet',SheetNo='C',SheetStatus=10)
        self.assertEqual(report('QueryJobSheetNoIsClosed',params(jobsheetno="'C','C'"))['rows'][0]['cmdok'],99)

    def test_zero_day_defect_total_keeps_both_records_with_undefined_ratio(self):
        for n,qty in enumerate([-10,10]):create('WDefect',SheetSeries=str(n),SheetDate=at(2),SheetType=0,DefectQty=qty,DefectKind='K',Defects='dt003')
        r=report('SP_WDefectList',params(startdate=at(1),enddate=at(3)))
        self.assertEqual(len(r['rows']),2);self.assertTrue(all(v['bl1'] is None for v in r['rows']))
        self.assertTrue(r['notes'])

    def test_first_wage_version_numbers_employees_per_day_not_global_header(self):
        from unittest.mock import patch
        from plugins.erp_base.source_phase4_wages import decorate
        shared=dict(years='2026-01',shiftid='S',shifamount=30,shifscamount=0,supplements=0,
            shifsystemamount=0,subtotal=30,sumnum=2,shifotheramount=0)
        data=[dict(shared,empid=emp,rq='2026-01-'+day,rqday=day,empidsubtotal=qty)
            for day,emp,qty in [('01','A',10),('01','B',20),('02','B',30)]]
        with patch('plugins.erp_base.source_phase4_wages.sql_query',return_value=[]):
            first=decorate('Sp_OLD_QueryWagesStatisticsInfo1',{'rows':data},params(newstime=at(1),shiftid='S'),{},None)
            second=decorate('Sp_OLD_QueryWagesStatisticsInfo2',{'rows':data},params(newstime=at(1),shiftid='S'),{},None)
        self.assertEqual(first['result_sets'][1]['rows'][1]['emp01'],30)
        self.assertIsNone(first['result_sets'][1]['rows'][1]['emp02'])
        self.assertEqual(second['result_sets'][1]['rows'][1]['emp02'],30)
        self.assertEqual(len(first['rows']),3)

    def test_saved_text_process_status_updates_schedule_and_assigned_totals(self):
        from plugins.erp_base import source_services
        job=create('JobSheet',SheetSeries='J',SheetNo='J',SumAssignedRolls=-2,SumAssignedWeightQty=-10)
        process=create('JobProcess',SheetSeries='J',ProcessNo=1,ProcessID='GX06',Status='0')
        plan=create('ProcessSchedule',JobSheetNo='J',ProcessNo=1,ProcessID='GX06')
        source_services.write(type(process),{'old_status':'5'},process,self.actor,apply_effects=False)
        job.refresh_from_db();self.assertEqual(job.old_sum_process_weight_qty,-10)
        source_services.write(type(process),{'old_status':'1'},process,self.actor,apply_effects=False)
        self.assertFalse(source('ProcessSchedule').filter(pk=plan.pk).exists())
        self.assertTrue(type(plan).objects.filter(pk=plan.pk).exists())

    def test_progress_completed_running_and_empty_card_keep_original_cursor_values(self):
        from plugins.erp_base.source_phase4_operations import perform
        jobs=[create('JobSheet',SheetSeries=s,SheetNo=s) for s in ['A','B']]
        create('JobProcess',SheetSeries='A',ProcessNo=1,ProcessID='DONE',Status='1')
        create('JobProcess',SheetSeries='A',ProcessNo=2,ProcessID='RUN',Status='5',StartTime=at(2),EndTime=at(3))
        create('JobProcess',SheetSeries='A',ProcessNo=3,ProcessID='NEXT',Status='0')
        perform('Sp_JobProcessUpdate_Curr2',params(),self.actor)
        for job in jobs:job.refresh_from_db()
        self.assertEqual(jobs[0].old_curr_process_id,'RUN');self.assertEqual(jobs[0].old_next_process_id,'RUN')
        self.assertEqual(jobs[0].old_plan_date,at(3))
        self.assertIsNone(jobs[1].old_curr_process_id)
        self.assertIsNone(jobs[1].old_next_process_id)

    def test_repeated_gray_save_syncs_labels_and_captures_nested_packing_progress(self):
        from plugins.erp_base import source_services
        from plugins.erp_base.source_chain_reverse import capture
        from plugins.erp_base.source_operation_effects import restore
        from plugins.erp_base.source_phase3_operations import model
        job=create('JobSheet',SheetSeries='J',SheetNo='J',ColorNum='C')
        step=create('JobProcess',SheetSeries='J',ProcessID='GX98',ProcessNo=1,Status='0')
        package=create('RecordYield',GrayBarCode='G',BarCode='B',JobSheetNo='OLD',RollNo='1')
        before_job=job.old_pre_vat_qty
        with capture() as changes:
            for _ in range(2):
                source_services.write(model('JobGrayRecord'),{'old_sheet_series':'J','old_gray_bar_code':'G',
                    'old_weight_qty':-5,'old_length_qty':0,'old_rolls':1},actor=self.actor,apply_effects=False)
        package.refresh_from_db();step.refresh_from_db()
        self.assertEqual(source('JobGrayRecord').count(),2)
        self.assertEqual(package.old_job_sheet_no,'J');self.assertEqual(step.old_status,'1')
        restore(changes,self.actor,'验证嵌套标签及开工回写完整撤销')
        package.refresh_from_db();step.refresh_from_db();job.refresh_from_db()
        self.assertEqual(package.old_job_sheet_no,'OLD');self.assertEqual(step.old_status,'0')
        self.assertIsNone(step.old_start_time);self.assertEqual(job.old_pre_vat_qty,before_job)

    def test_work_quantity_original_ten_columns_station_filter_and_duplicate_jobs(self):
        for s in ['A','B']:create('JobSheet',SheetSeries=s,SheetNo='J',ProdID='P',AssignUnit=1)
        create('p_Gray',GrayID='P',FabricKindID='F')
        create('p_ProcessPrice',ProcessID='GX00',ProdKindID='F',Price=100)
        create('WProcess',WProcessNo='W',JobSheetNo='J',ProcessNo=1,ProcessID='GX00',StationID='01',ShiftID='S',EmpID='E',CurrKg=-10,CurrMeter=0,CurrDosage=50,CreateDate=at(2))
        r=report('Sp_WorkQtySum',params(newstime=at(1),newetime=at(3),stationid='01',shiftid='S'))
        self.assertEqual(len(r['rows']),1);self.assertEqual(len(r['rows'][0]),10)
        self.assertEqual(r['rows'][0]['currkg'],-20);self.assertEqual(r['rows'][0]['currmoney'],-2)
        self.assertEqual(report('Sp_WorkQtySum',params(newstime=at(1),newetime=at(3),stationid='07'))['rows'],[])
