from datetime import datetime,timedelta
from decimal import Decimal
from unittest.mock import patch
from django.apps import apps
from django.test import TestCase,SimpleTestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.source_package_operations import reader,effect
from plugins.erp_base.source_quality_reports import rows
from plugins.erp_base.source_context import SourceBusinessParameter
from plugins.erp_base.source_services import write,delete_documents
from plugins.erp_base.source_equipment_projects import project_plan,case_projects,record_projects,save_projects,split_rows,sql_numeric
from plugins.erp_base.source_equipment_faults import perform,actions,check_action,save_fault,fault_check
from plugins.erp_base.source_equipment_operations import undo
from plugins.erp_base.source_site_work import create_record,job_records


class EquipmentPureTests(SimpleTestCase):
    def test_split_keeps_empty_and_whitespace_rules(self):
        self.assertEqual(split_rows(None),[]);self.assertEqual(split_rows(''),[''])
        self.assertEqual(split_rows(' A\t` B\r\n`'),['A',' B',''])
        self.assertEqual(split_rows('A`\\'),['A'])
        with self.assertRaises(ValueError):split_rows('汉'*51)

    def test_sql_numeric_verified_boundaries(self):
        for v in ['.',',','\\','$','¥','￥','+','-','1,000','1,2','1e2','1d2','$1']:
            self.assertTrue(sql_numeric(v),v)
        for v in [None,'',' ','1$','1-','１２','1.2.3','1e999']:
            self.assertFalse(sql_numeric(v),v)


class EquipmentTests(TestCase):
    def setUp(self):
        self.actor=Users.objects.create_superuser(username='equipment-tests',password='test')
        self.at=timezone.make_aware(datetime(2026,10,15,10,30));self.client=APIClient();self.client.force_authenticate(self.actor)
        self.employee=self.old('HEmployee','erp_base',EmpID='E',Name='员工甲',MFLevel=3,MFGiveOut=True)
        for name,value in [('MachineFault_FixManGetBill','1'),('MachineFault_ReportManConfirm','0'),('MachineFault_FlowType','0')]:self.param(name,value)

    def param(self,name,value):SourceBusinessParameter.objects.update_or_create(name=name,defaults={'value':value})

    def old(self,name,module='erp_production',**values):
        model=reader(name,module).model
        from plugins.erp_base.source_services import apply_defaults
        row=model();data={model.SOURCE_FIELDS[k]:v for k,v in values.items()};apply_defaults(row,data)
        for k,v in data.items():setattr(row,k,v)
        row.save();row.refresh_from_db();return row

    def fault(self,**values):
        return self.old('MachineFault',**{'SheetSeries':'MF','SheetNo':'MF','EmpID':'E','FlowStatus':'待指派','MachineID':'M',**values})

    def act(self,item,action,**values):
        return perform(item,action,actor=self.actor,at=self.at,reason='原流程核对',**{'employee':'E','fixers':None,'remarks':'记录','score':None,**values})

    def project(self,**values):
        return self.old('MachineCaseProject',**{'SheetSeries':'CASE','DetailNo':'P1','SortNo':1,'SerialNum':'1','ProjectInfo':'温度','DefaultValue':'90',**values})

    def values(self,**values):
        return {'employee':'E','machine':'M','machine_name':'机台','location':'一楼','remarks':'原备注','sheet_date':self.at,
            'performed_at':self.at,'people':'E','survey':'巡检','idea':'意见','result':'1',**values}

    def save_project(self,kind,item=None,**kwargs):
        return save_projects(kind,item,kwargs.pop('values',self.values()),actor=self.actor,at=self.at,reason='保存项目',
            **{'case':'CASE','changed_ids':None,'changed_values':None,'changed_results':None,**kwargs})

    def fault_values(self,**values):
        return {'employee':'E','machine':'M','machine_name':'设备','location':'位置','shift':'S','fault':'漏水','business_unit':'INPUT',
            'fault_class':'C','group':'G','machine_class':'设备类','sheet_kind':'','uploads':None,'urgent':1,'remarks':'记录',**values}

    def test_projects_duplicate_changes_and_empty_value_not_defaulted(self):
        self.project();r=project_plan('CASE','P1`P1','`负值','`-3')
        self.assertEqual([x['Value'] for x in r['rows']],['','负值']);self.assertEqual([x['Result'] for x in r['rows']],[0,-3])
        self.assertEqual([x['suffix'] for x in r['rows']],['000','001'])

    def test_confirm_and_reopen_keep_original_fault_trigger(self):
        from plugins.erp_base.source_services import confirm,reopen
        row=self.fault(ResultID='3',EndTime=self.at-timedelta(days=2))
        row.approval_stage='draft';row.save(update_fields=['approval_stage'])
        with patch('plugins.erp_base.source_services.timezone.now',return_value=self.at):
            row=confirm(row,self.actor)
        self.assertEqual(row.old_end_time,self.at)
        later=self.at+timedelta(hours=2)
        with patch('plugins.erp_base.source_equipment_faults.timezone.now',return_value=later):
            row=reopen(row,self.actor,'撤回确认')
        self.assertEqual(row.old_end_time,later)

    def test_submit_truncates_input_handler_variable_and_pending_notices_visible(self):
        from plugins.erp_base.source_equipment_faults import history
        row=self.fault(HandlerIDs='E')
        self.act(row,'提交',fixers='A'*120);row.refresh_from_db()
        self.assertEqual(row.old_handler_ids,'A'*100)
        self.act(row,'重新提交')
        report=history(row)
        self.assertEqual(report['candidate_rows'][0]['delivery'],'not_connected')

    def test_projects_missing_value_uses_default_and_unmatched_changes_remain(self):
        self.project();r=project_plan('CASE','P1`MISSING',None,None)
        self.assertEqual(r['rows'][0]['Value'],'90');self.assertEqual(len(r['supplemental_rows']),1)

    def test_invalid_result_and_long_split_report_without_write(self):
        self.project()
        self.assertTrue(project_plan('CASE','P1','x','bad')['blocked'])
        self.assertTrue(project_plan('CASE','P1','A'*101,'0')['blocked'])
        with self.assertRaises(ValidationError):self.save_project('care',changed_ids='P1',changed_values='x',changed_results='bad')
        self.assertEqual(reader('MachineCareRecords','erp_production').count(),0)

    def test_case_direct_and_latest_machine_link_selection(self):
        a=self.old('MachineCase',SheetSeries='CASE',SheetDate=self.at);self.project()
        self.old('MachineCaseDetail',SheetSeries='CASE',DetailNo='D',MachineID='M')
        self.assertEqual(len(case_projects('M')['rows']),1)
        self.old('MachineCase',SheetSeries='NEW',SheetDate=self.at+timedelta(days=1))
        self.old('MachineCaseDetail',SheetSeries='NEW',DetailNo='D2',MachineID='M')
        self.assertEqual(case_projects('M')['rows'],[]);self.assertEqual(len(case_projects('CASE')['rows']),1)

    def test_care_create_with_projects_has_new_ids_and_can_reverse(self):
        self.project();head=self.save_project('care')
        child=rows('MachineCareProject','erp_production').get()
        self.assertEqual(child.old_detail_no,head.old_sheet_series+'-000');self.assertIsNone(head.legacy_id)
        undo(head,self.actor,self.at,'撤回')
        self.assertEqual(rows('MachineCareRecords','erp_production').count(),0)
        self.assertEqual(reader('MachineCareProject','erp_production').count(),1)
        self.assertEqual(rows('MachineCareProject','erp_production').count(),0)

    def test_care_update_keeps_actual_date_and_sets_modifydate_null(self):
        self.project();head=self.old('MachineCareRecords',SheetSeries='C',CareDate=self.at-timedelta(days=9),ModifyDate=self.at)
        original=self.old('MachineCareProject',SheetSeries='C',DetailNo='C-OLD',Value='原项目')
        self.save_project('care',head);head.refresh_from_db()
        self.assertEqual(head.old_care_date,self.at-timedelta(days=9));self.assertIsNone(head.old_modify_date)
        self.assertTrue(effect(original,'equipment_retained')['active'])
        undo(head,self.actor,self.at,'撤回');head.refresh_from_db()
        self.assertEqual(head.old_modify_date,self.at);self.assertEqual(rows('MachineCareProject','erp_production').get().pk,original.pk)

    def test_inspection_update_changes_sheetdate_not_inspectdate(self):
        self.project();head=self.old('InspectionLog','erp_quality',SheetSeries='I',InspectDate=self.at-timedelta(days=3))
        self.save_project('inspection',head);head.refresh_from_db()
        self.assertEqual(head.old_sheet_date,self.at);self.assertEqual(head.old_inspect_date,self.at-timedelta(days=3))
        self.assertEqual(head.old_modify_date,self.at)

    def test_new_inspection_creates_expected_header_and_default_project_values(self):
        self.project(DefaultValue=None,IsInputText=None);head=self.save_project('inspection')
        child=rows('InspectionProject','erp_quality').get()
        self.assertEqual(head.old_inspector,'E');self.assertEqual(head.old_sheet_kind,0)
        self.assertEqual(child.old_value,'');self.assertEqual(child.old_result,0)

    def test_record_fallback_requires_literal_Y_not_1_and_keeps_zero_existing_flag(self):
        self.old('MachineCase',SheetSeries='CASE');self.project()
        head=self.old('MachineCareRecords',SheetSeries='C',CarePlanDetailNo='CASE')
        self.param('IsUseMachineCase','1');self.assertEqual(record_projects(head)['rows'],[])
        self.param('IsUseMachineCase','Y');r=record_projects(head)
        self.assertEqual(len(r['rows']),1);self.assertEqual(r['summary']['IsUseMachineCase'],0)

    def test_blank_case_retires_old_projects_without_inventing_replacement(self):
        head=self.old('MachineCareRecords',SheetSeries='C')
        self.old('MachineCareProject',SheetSeries='C',DetailNo='D')
        self.save_project('care',head,case=None)
        self.assertEqual(rows('MachineCareProject','erp_production').count(),0)

    def test_scope_cannot_apply_partial_project_set(self):
        self.project()
        def limited(name,module):return reader(name,module).none() if name=='MachineCaseProject' else reader(name,module)
        with self.assertRaises(ValidationError):self.save_project('care',query=limited)

    def test_fault_flow_accept_sign_commit_reject_confirm_evaluate_and_reverse(self):
        head=self.fault(FaultID='WRONG')
        self.act(head,'受理');head.refresh_from_db();self.assertEqual(head.old_handler_ids,'E')
        self.act(head,'签到');head.refresh_from_db();self.assertEqual(head.old_severity_id,'E')
        self.assertEqual(rows('MachineFaultRecord','erp_production').order_by('pk').last().old_handler_ids,'WRONG')
        part=self.old('MachineFaultArticleInfo',SheetSeries='MF',Rounds=-1,SerialNum=1,Qty=-2)
        self.act(head,'提交');part.refresh_from_db();self.assertEqual(part.old_rounds,1)
        self.act(head,'拒绝');head.refresh_from_db();self.assertEqual(head.old_flow_status,'待维修')
        self.act(head,'确认');self.act(head,'评价',score=-8);head.refresh_from_db();self.assertEqual(head.old_flow_status,'已评价')
        undo(head,self.actor,self.at,'撤回评价');head.refresh_from_db();self.assertEqual(head.old_flow_status,'已确认')

    def test_action_checker_only_active_original_rules(self):
        head=self.fault(FlowStatus='异常状态')
        self.assertEqual(check_action(head,'提交',None)['rows'][0]['Code'],0)
        self.assertEqual(check_action(head,'签到',None)['rows'][0]['Code'],-111)
        self.assertEqual(check_action(head,'取消签到',None)['rows'][0]['Code'],-112)
        self.assertEqual(check_action(head,'指派','')['rows'][0]['Code'],-802)
        self.assertEqual(check_action(head,'陌生动作',None)['rows'][0]['Code'],-10086)

    def test_null_status_signin_not_blocked_by_sql_unknown(self):
        head=self.fault(FlowStatus=None);self.act(head,'签到')
        self.assertEqual(check_action(head,'签到',None)['rows'][0]['Code'],-112)
        self.act(head,'取消签到');head.refresh_from_db();self.assertIsNone(head.old_start_time)

    def test_simple_flow_rejection_still_confirmed(self):
        self.param('MachineFault_FlowType','1');head=self.fault()
        self.act(head,'拒绝');head.refresh_from_db();self.assertEqual(head.old_flow_status,'已确认')

    def test_return_keeps_endtime_and_logs_original_handlers(self):
        head=self.fault(HandlerIDs='E',EndTime=self.at);self.act(head,'退回');head.refresh_from_db()
        self.assertEqual(head.old_handler_ids,'');self.assertEqual(head.old_end_time,self.at)
        log=rows('MachineFaultRecord','erp_production').get();self.assertEqual(log.old_handler_ids,'E');self.assertIsNone(log.old_score)

    def test_close_restore_resubmit_original_rightstatus_and_fields(self):
        head=self.fault(HandlerIDs='E',StartTime=self.at,EndTime=self.at)
        self.old('PMachineFaultStatus','erp_base',StatusID=1,StatusName='已关闭',StatusType='已关闭')
        self.act(head,'关闭');head.refresh_from_db();self.assertEqual(head.old_right_status,10)
        self.act(head,'恢复');head.refresh_from_db();self.assertEqual(head.old_right_status,0);self.assertEqual(head.old_handler_ids,'');self.assertEqual(head.old_start_time,self.at)
        self.act(head,'重新提交');head.refresh_from_db();self.assertEqual(head.old_right_status,10)
        self.assertEqual(effect(head,'equipment_operation')['notification_delivery'],'not_connected')

    def test_comment_creates_both_logs_and_reverse_retains_both(self):
        from django.db import IntegrityError
        head=self.fault()
        with self.assertRaises(IntegrityError):self.act(head,'评论',remarks=None)
        self.assertEqual(rows('MachineFaultComment','erp_production').count(),0)
        self.act(head,'评论')
        self.assertEqual(rows('MachineFaultComment','erp_production').count(),1)
        self.assertEqual(rows('MachineFaultRecord','erp_production').get().old_action_type,'评论')
        undo(head,self.actor,self.at,'撤回')
        self.assertEqual(rows('MachineFaultComment','erp_production').count(),0)
        self.assertEqual(reader('MachineFaultComment','erp_production').count(),1)

    def test_original_actions_v2_string_and_sign_flags_differ(self):
        head=self.fault(FlowStatus='待维修',HandlerIDs='E',StartTime=self.at)
        r=actions(head,'E')['rows'][0];self.assertIn('签到',r['Action']);self.assertEqual(r['签到'],0);self.assertEqual(r['取消签到'],1)
        self.assertNotIn('签到',actions(head,'E',version=1)['rows'][0])

    def test_action_list_reporter_priority_and_duplicate_close_preserved(self):
        head=self.fault();r=actions(head,'E')['rows'][0]
        self.assertEqual(r['Action'].count('关闭'),2);self.assertEqual(r['受理'],0)

    def test_missing_employee_parameter_does_not_invent_role(self):
        head=self.fault();r=actions(head,'MISSING')['rows'][0]
        self.assertIsNone(r['MFLevel']);self.assertEqual(r['Action'],'评论')

    def test_submit_rounds_max_and_only_negative_one_updates(self):
        head=self.fault()
        a=self.old('MachineFaultArticleInfo',SheetSeries='MF',Rounds=8,SerialNum=1)
        b=self.old('MachineFaultArticleInfo',SheetSeries='MF',Rounds=-1,SerialNum=2)
        c=self.old('MachineFaultArticleInfo',SheetSeries='MF',Rounds=-2,SerialNum=3)
        self.act(head,'提交');b.refresh_from_db();c.refresh_from_db()
        self.assertEqual(b.old_rounds,9);self.assertEqual(c.old_rounds,-2)
        self.assertEqual(rows('MachineFaultRecord','erp_production').get().old_score,9)
        undo(head,self.actor,self.at,'撤回');b.refresh_from_db();self.assertEqual(b.old_rounds,-1)

    def test_update_trigger_applies_even_when_result_not_changed(self):
        head=self.fault(ResultID='尚未已修待核对')
        with patch('plugins.erp_base.source_equipment_faults.timezone.now',return_value=self.at):write(type(head),{'old_remarks':'改备注'},head,actor=self.actor)
        head.refresh_from_db();self.assertEqual(head.old_end_time,self.at)
        head.old_end_time=self.at-timedelta(days=1);head.save();self.act(head,'关闭');head.refresh_from_db();self.assertEqual(head.old_end_time,self.at)

    def test_fault_save_maps_description_machine_business_and_attachments(self):
        self.old('PMachine','erp_base',MachineID='M',Name='设备',DeptID='D',BusinessUnitID='OLD')
        attachment=self.old('APPUploadFilesInfo','erp_base',Guid='G',SheetSeries='ORIG')
        head=save_fault(None,self.fault_values(uploads='G'),self.actor,self.at,'保存')
        head.refresh_from_db();attachment.refresh_from_db()
        self.assertEqual(head.old_fault_id,'');self.assertEqual(head.old_fault_remarks,'漏水');self.assertEqual(head.old_business_unit_id,'OLD')
        self.assertEqual(attachment.old_sheet_series,head.old_sheet_series);self.assertEqual(head.old_sheet_kind,'普通报修')
        undo(head,self.actor,self.at,'撤回');attachment.refresh_from_db();self.assertEqual(attachment.old_sheet_series,'ORIG')

    def test_fault_update_does_not_change_original_remarks_or_happentime(self):
        head=self.fault(Remarks='KEEP',HappenTime=self.at-timedelta(days=4))
        save_fault(head,self.fault_values(remarks='日志备注'),self.actor,self.at,'修改');head.refresh_from_db()
        self.assertEqual(head.old_remarks,'KEEP');self.assertEqual(head.old_happen_time,self.at-timedelta(days=4))
        self.assertEqual(rows('MachineFaultRecord','erp_production').get().old_remark,'日志备注')

    def test_fault_save_check_last_failure_wins(self):
        self.param('MachineFault_UseFaultClass','2');self.param('MachineFault_UseSendTo','2')
        r=fault_check(self.fault_values(fault='',machine='',machine_name='',fault_class='',group=''))
        self.assertEqual(r['rows'][0],{'Code':-103,'Msg':'维修分组不能为空！'})

    def test_later_edit_prevents_silent_undo_and_original_log_not_deleted(self):
        head=self.fault();self.act(head,'受理');head.old_handler_ids='CHANGED';head.save()
        with self.assertRaises(ValidationError):undo(head,self.actor,self.at,'撤回')
        self.assertEqual(rows('MachineFaultRecord','erp_production').count(),1)
        with self.assertRaises(ValidationError):delete_documents(type(head).objects.filter(pk=head.pk),self.actor)

    def test_site_independent_record_stays_separate_and_normal_makeup_sets_end(self):
        job=self.old('JobSheet',SheetSeries='J',SheetNo='J')
        values={'process':'GX07','process_no':1,'employee':'E','start':self.at,'end':None,'real_value':Decimal('-1.5'),'program':'P',
            'dye_process':'DP','machine':'M','rolls':Decimal('-2'),'weight':Decimal('-5'),'remarks':'补录','shift':'S','class_id':'C','station':'06','length':None,'dye_state':'3'}
        a=create_record(job,'AddDyeWProcessStep',values,self.actor)
        self.assertEqual(a.old_real_value,Decimal('-1.5'));self.assertEqual(reader('WProcess','erp_production').count(),0)
        self.assertEqual(len(job_records(job)['supplemental_rows']),1)
        b=create_record(job,'AddWProcessEdit',values,self.actor)
        self.assertEqual(b.old_end_time,b.old_start_time);self.assertEqual(b.old_sheet_kind,'1')
        self.assertEqual(reader('AddDyeWProcessStep','erp_sampling').count(),1)

    def test_equipment_api_creation_action_and_undo(self):
        r=self.client.post('/api/system/erp_production_sourcedyemachinefault/create_fault/',{**self.fault_values(),'at':self.at.isoformat(),'reason':'测试'},format='json')
        self.assertEqual(r.status_code,200,r.data);pk=r.data['data']['id']
        r=self.client.post(f'/api/system/erp_production_sourcedyemachinefault/{pk}/perform_fault_action/',{'action':'受理','employee':'E','remarks':None,'at':self.at.isoformat(),'reason':'测试'},format='json')
        self.assertEqual(r.status_code,400)
        r=self.client.post(f'/api/system/erp_production_sourcedyemachinefault/{pk}/perform_fault_action/',{'action':'受理','employee':'E','at':self.at.isoformat(),'reason':'测试'},format='json')
        self.assertEqual(r.status_code,200,r.data)
        r=self.client.post(f'/api/system/erp_production_sourcedyemachinefault/{pk}/undo_equipment/',{'at':self.at.isoformat(),'reason':'撤回'},format='json')
        self.assertEqual(r.status_code,200,r.data)

    def test_project_api_creates_and_queries_inspection(self):
        self.project()
        r=self.client.post('/api/system/erp_quality_sourcedyeinspectionlog/create_equipment_document/',{'case':'CASE',**self.values(),
            'sheet_date':self.at.isoformat(),'performed_at':self.at.isoformat(),'at':self.at.isoformat(),'reason':'测试'},format='json')
        self.assertEqual(r.status_code,200,r.data)
        pk=r.data['data']['id'];r=self.client.post(f'/api/system/erp_quality_sourcedyeinspectionlog/{pk}/equipment_projects/',{},format='json')
        self.assertEqual(r.status_code,200,r.data);self.assertEqual(len(r.data['data']['rows']),1)
