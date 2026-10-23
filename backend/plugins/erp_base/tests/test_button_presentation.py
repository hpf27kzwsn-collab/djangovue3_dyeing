from decimal import Decimal
from datetime import datetime
from pathlib import Path
import json
from django.utils import timezone
from django.apps import apps
from django.test import TestCase, SimpleTestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from system.models import Users, Role, Menu, MenuButton, RoleMenuButtonPermission
from system.catalog import ENTITIES
from system.views import view_for
from system.actions import workflow_actions
from core.resources import resource_options
from plugins.erp_base.button_presentation import POLICIES, DEFERRED
from plugins.erp_base.source_services import write, apply_defaults, approve, reopen
from plugins.erp_base.source_package_operations import effect
from plugins.erp_base.source_continuation import save_effect


class ButtonMetadataTests(SimpleTestCase):
    def test_every_audited_action_keeps_its_service_and_permission(self):
        identities=[];maintenance=[]
        for entity,model in ENTITIES.items():
            if not entity.startswith('erp_'):
                continue
            original=resource_options(model).get('workflow',{})
            actual=workflow_actions(entity,view_for(entity,model),original)
            if any(a['placement'] in ['maintenance','automatic'] for a in actual['actions']):maintenance.append(entity)
            self.assertEqual([a['key'] for a in original.get('actions',[])],[a['key'] for a in actual['actions']])
            for action in actual['actions']:
                identities.append(entity+':'+action['key'])
                self.assertIn(action['placement'],['business','automatic','maintenance','deferred'])
                self.assertTrue(action['permission'].startswith(entity+':'))
                self.assertTrue(action['display_title'])
        self.assertEqual(set(identities),set(POLICIES))
        self.assertEqual(len(identities),1457)
        index=Path(__file__).resolve().parents[4]/'web/src/plugins/erp/maintenance-resources.json'
        self.assertEqual(json.loads(index.read_text(encoding='utf-8')),maintenance)

    def test_order_approval_direct_from_draft_without_extra_confirmation(self):
        model=ENTITIES['erp_sales_sourcedyeordermain']
        result=workflow_actions('erp_sales_sourcedyeordermain',view_for('erp_sales_sourcedyeordermain',model),resource_options(model)['workflow'])
        actions={a['key']:a for a in result['actions']}
        self.assertEqual(actions['confirm']['placement'],'maintenance')
        self.assertEqual(actions['approve']['states'],['draft','confirmed'])
        self.assertEqual(actions['approve']['placement'],'business')

    def test_print_pause_does_not_pause_printing_or_loose_winding_business(self):
        self.assertEqual(len(DEFERRED['queries']),35)
        for entry in ['PrintOrderColor','PrintingTestStuff','PrintJobSheet','DyeReprint']:
            self.assertNotIn(entry,DEFERRED['printing'])
        for entity,key in [('erp_warehouse_package','request_print'),('erp_warehouse_labelprint','confirm')]:
            model=ENTITIES[entity]
            actual=workflow_actions(entity,view_for(entity,model),resource_options(model)['workflow'])
            self.assertEqual(next(a for a in actual['actions'] if a['key']==key)['placement'],'deferred')

    def test_preview_execute_and_reverse_share_business_topic(self):
        entity='erp_production_sourcedyejobsheet';model=ENTITIES[entity]
        actual=workflow_actions(entity,view_for(entity,model),resource_options(model)['workflow'])
        topics={a['topic'] for a in actual['actions'] if a['key'] in ['preview_execution_reverse','reverse_execution_chain','undo_execution_reverse']}
        self.assertEqual(topics,{'执行整链撤销'})


class ButtonEventTests(TestCase):
    def setUp(self):
        self.actor=Users.objects.create_superuser(username='button-events',password='test')
        self.client=APIClient();self.client.force_authenticate(self.actor)

    def old(self,name,module='erp_sales',**values):
        model=apps.get_model(module+'.SourceDye'+name);item=model();data={model.SOURCE_FIELDS[k]:v for k,v in values.items()}
        apply_defaults(item,data)
        for key,value in data.items():setattr(item,key,value)
        item.save();item.refresh_from_db();return item

    def test_source_order_approve_and_reverse_work_without_confirm_button(self):
        model=apps.get_model('erp_sales.SourceDyeOrderMain')
        head=write(model,{'_entry':'OrderMain','old_sheet_series':'BUTTON-O','old_sheet_no':'BUTTON-O'},actor=self.actor)
        self.assertEqual(head.approval_stage,'draft')
        response=self.client.post(f'/api/system/erp_sales_sourcedyeordermain/{head.pk}/approve/',{},format='json')
        self.assertEqual(response.status_code,200,response.data)
        head.refresh_from_db();self.assertEqual(head.approval_stage,'approved');self.assertEqual(head.old_right_status,10)
        reopen(head,self.actor,'恢复修改');head.refresh_from_db()
        self.assertEqual(head.approval_stage,'draft');self.assertEqual(head.old_right_status,0)
        self.assertEqual(head.confirmed_at,None)

    def test_approval_service_still_requires_original_permission(self):
        head=write(apps.get_model('erp_sales.SourceDyeOrderMain'),
            {'_entry':'OrderMain','old_sheet_series':'PERM','old_sheet_no':'PERM'},actor=self.actor)
        user=Users.objects.create_user(username='ordinary-button',password='test')
        self.client.force_authenticate(user)
        path=f'/api/system/erp_sales_sourcedyeordermain/{head.pk}/approve/'
        self.assertEqual(self.client.post(path,{},format='json').status_code,403)
        role=Role.objects.create(name='审核岗位',key='button-approve');user.role.add(role)
        menu=Menu.objects.create(name='测试订单')
        button=MenuButton.objects.create(menu=menu,name='审核',value='erp_sales_sourcedyeordermain:approve-post',
            api='/api/system/erp_sales_sourcedyeordermain/{id}/approve/',method=1)
        grant=RoleMenuButtonPermission.objects.create(role=role,menu_button=button,data_range=3)
        response=self.client.post(path,{},format='json')
        self.assertEqual(response.status_code,200,response.data)
        grant.delete()
        self.assertEqual(self.client.post(path,{},format='json').status_code,403)

    def test_inverse_buttons_only_receive_business_effect_states(self):
        job=self.old('JobSheet','erp_production',SheetSeries='STATE',SheetNo='STATE')
        path=f'/api/system/erp_production_sourcedyejobsheet/{job.pk}/'
        self.assertEqual(self.client.get(path).data['data']['action_effects'],{})
        save_effect(job,'package_pairing',{'state':'applied','private_source':'不可暴露的来源明细'},self.actor,'状态验证')
        states=self.client.get(path).data['data']['action_effects']
        self.assertEqual(states,{'package_pairing':'applied'})
        save_effect(job,'package_pairing',{'state':'reversed'},self.actor,'逆向状态')
        self.assertEqual(self.client.get(path).data['data']['action_effects'],{'package_pairing':'reversed'})

    def test_source_order_approved_sheet_status_check_runs_on_save(self):
        head=self.old('OrderMain',SheetSeries='LOCKED',SheetNo='LOCKED',SheetStatus=10)
        with self.assertRaises(ValidationError):write(type(head),{'old_remarks':'不应被写入'},instance=head,actor=self.actor)
        head.refresh_from_db();self.assertNotEqual(head.old_remarks,'不应被写入')

    def test_abnormal_fault_is_saved_and_automatic_check_fact_is_visible(self):
        model=apps.get_model('erp_production.SourceDyeMachineFault')
        item=write(model,{'old_sheet_series':'F-ABNORMAL','old_sheet_no':'F-ABNORMAL','old_fault_remarks':'','old_machine_id':None,'old_machine_name':None},actor=self.actor)
        report=effect(item,'fault_save_check')
        self.assertNotEqual(report['rows'][0]['Code'],0)
        self.assertTrue(model.objects.filter(pk=item.pk).exists())

    def test_duplicate_quote_rows_both_save_with_automatic_checks(self):
        self.old('FixedPrice',SheetSeries='BQ',CustomerID='BC')
        model=apps.get_model('erp_sales.SourceDyeFixedPriceDetail')
        first=write(model,{'old_sheet_series':'BQ','old_detail_no':'BQ1','old_prod_id':'P','old_color_num':'RED','old_price':Decimal('-2.5')},actor=self.actor)
        second=write(model,{'old_sheet_series':'BQ','old_detail_no':'BQ2','old_prod_id':'P','old_color_num':'RED','old_price':Decimal('-2.5')},actor=self.actor)
        self.assertTrue(model.objects.filter(pk__in=[first.pk,second.pk]).count()==2)
        self.assertTrue(effect(second,'quote_trigger_check')['rows'][0]['duplicate'])

    def test_finalized_sample_result_is_automatic_and_null_key_is_not_global_match(self):
        model=apps.get_model('erp_sampling.SourceDyeDyeDipsRecord')
        unrelated=self.old('DyeLabColor','erp_sampling',SheetSeries='OTHER',ColorNum=None,ColorNo='',ColorDepthID='KEEP')
        sample=write(model,{'_entry':'DyeDipsRecord','old_sheet_series':'BS','old_sheet_no':'BS','old_color_num':'BS-RED','old_color_no':'BS-C','old_color_id':'本白','old_stuff_dosage':0,'old_pre_finalized':True},actor=self.actor)
        sample.refresh_from_db();unrelated.refresh_from_db()
        self.assertEqual(sample.old_color_depth_id,'04');self.assertEqual(unrelated.old_color_depth_id,'KEEP')

    def test_site_save_resolves_shift_and_retains_duplicate_candidates(self):
        from plugins.erp_base.tests.test_source_shift_calendar import detail
        from plugins.erp_base.source_site_work import create_record
        at=timezone.make_aware(datetime(2026,10,1,8))
        model=apps.get_model('erp_base.SourceDyePShiftArrangeDetail')
        values=detail()
        data={name:timezone.make_aware(value) if isinstance(value,datetime) else value
              for name,value in values.items() if name in model.SOURCE_FIELDS}
        self.old('PShiftArrangeDetail','erp_base',**data)
        self.old('PDept','erp_base',DeptID='BD')
        self.old('PMachine','erp_base',MachineID='BM',DeptID='BD')
        self.old('PShift','erp_base',ShiftID='BS',Name='染色甲班',DeptID='BD',ClassID='BC')
        self.old('PShift','erp_base',ShiftID='BS',Name='重复甲班',DeptID='BD',ClassID='BC')
        job=self.old('JobSheet','erp_production',SheetSeries='BJ',SheetNo='BJ')
        params={'process':'GX07','process_no':1,'employee':'BE','start':at,'end':None,
            'machine':'BM','rolls':Decimal('-2'),'weight':Decimal('-5'),'remarks':'原值保留',
            'shift':None,'class_id':None,'station':'06','length':None,'dye_state':'3','auto_shift':True}
        item=create_record(job,'AddWProcessEdit',params,self.actor)
        self.assertEqual((item.old_shift_id,item.old_class_id),('BS','BC'))
        self.assertEqual(item.old_curr_kg,Decimal('-5'))
        self.assertEqual(len(effect(item,'site_shift_resolution')['rows']),2)
        self.old('PShift','erp_base',ShiftID='B2',Name='另一甲班',DeptID='BD',ClassID='BC')
        count=type(item).objects.count()
        with self.assertRaises(ValidationError):create_record(job,'AddWProcessEdit',params,self.actor)
        self.assertEqual(type(item).objects.count(),count)
        manual=create_record(job,'AddWProcessEdit',{**params,'auto_shift':False},self.actor)
        self.assertIsNone(manual.old_shift_id)
