"""21条原配置落到原字段，覆盖真实保存、重复、NULL和查询上下文。"""
from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .test_phase_report_audit import create, at
from .test_source_phase6 import reader
from plugins.erp_base import source_services as services
from plugins.erp_base.source_phase3_operations import model
from plugins.erp_base.source_phase6_editors import options


class FieldBindingTests(TestCase):
    def setUp(self):
        self.actor=get_user_model().objects.create(username='binding-21',is_superuser=True)
        for _ in range(2):
            create('h_Employee',EmpID='E',LoginName=self.actor.username,Name='员工',DeptID='D',PosID='P')

    def test_nine_login_bindings_preserve_original_position_default(self):
        for table,entry in [('StuffWeight','DStuffWeight'),('StuffWeight','qry_QuoteRelaStuff'),
                            ('DyeRecipe','qry_QuoteRelaRecipe'),('DyeDipsRecord','DyeLabColorColorNumNoPrice')]:
            with self.subTest(entry=entry):
                item=services.write(model(table),{'_entry':entry},actor=self.actor)
                self.assertEqual(item.old_dept_id,'D')
                if table=='StuffWeight':self.assertEqual(item.old_creater,'员工')
        item=services.write(model('h_Employee'),{'_entry':'qry_Employee'},actor=self.actor)
        self.assertEqual((item.old_emp_id,item.old_creater,item.old_modifyer),('P','binding-21','binding-21'))
        explicit=services.write(model('h_Employee'),{'_entry':'qry_Employee','old_emp_id':'E','old_creater':None},actor=self.actor)
        self.assertEqual(explicit.old_emp_id,'E');self.assertIsNone(explicit.old_creater)
        self.assertEqual(model('h_Employee').objects.count(),4)

    def test_six_gray_code_aliases_copy_one_physical_field_and_keep_duplicates(self):
        previous=create('GrayInDetail',GrayID='G',Remarks='原备注')
        for entry in ['GrayInDetail','GrayInWorkDetail','JiaNianGrayInDetail','KeTuiGrayInDetail','SemiToGrayInDetail','TuiHuoGrayInDetail']:
            for explicit in [False,True]:
                data={'_entry':entry,'_entry_copy_from':previous}
                if explicit:data['old_gray_id']=None
                item=services.write(model('GrayInDetail'),data,actor=self.actor)
                self.assertEqual(item.old_gray_id,None if explicit else 'G')
        self.assertEqual(model('GrayInDetail').objects.count(),13)

    def test_six_packaging_copy_bindings_write_selected_original_records(self):
        previous=create('RecordYield',BarCode='DUP',AddQty=-2,Unit='3',SpecDefects='原疵点',Weight='120',Width='150')
        specs={'QC_RecordYield':['AddQty'],'qry_RecordYield':['AddQty','Unit'],
               'QueryRecordCheck':['SpecDefects','Weight','Width']}
        for entry,fields in specs.items():
            item=services.write(model('RecordYield'),{'_entry':entry,'_entry_copy_from':previous,'old_bar_code':'DUP'},actor=self.actor)
            for field in fields:self.assertEqual(getattr(item,item.SOURCE_FIELDS[field]),getattr(previous,previous.SOURCE_FIELDS[field]))
        self.assertEqual(model('RecordYield').objects.filter(old_bar_code='DUP').count(),4)

    def test_purchase_list_formula_null_negative_and_explicit_override(self):
        item=services.write(model('PurDetail'),{'_entry':'PurDetailList','old_price':3,'old_qty':-2},actor=self.actor)
        self.assertEqual(item.old_amount,-6)
        item=services.write(type(item),{'old_qty':None},item,actor=self.actor)
        self.assertEqual(item.old_amount,0)
        item=services.write(type(item),{'old_qty':-2,'old_amount':None},item,actor=self.actor)
        self.assertIsNone(item.old_amount)

    def test_review_selectors_filter_by_job_not_review_number_keep_duplicates(self):
        for kind,entry,field in [('内部评审','qry_OriPrintJobSheet','ToLossStr'),('客退评审','JobSheet','LossStr')]:
            for _ in range(2):create('WDefect',Kind=kind,SheetNo=kind,JobSheetNo='J')
            create('WDefect',Kind=kind,SheetNo='OTHER',JobSheetNo='OTHER')
            result=options(entry,field,'',reader,{'SheetNo':'J'})
            self.assertEqual([row['id'] for row in result['rows']].count(kind),2)
            self.assertNotIn('OTHER',[row['id'] for row in result['rows']])

    def test_original_newfuban_delete_and_request_designated_approval_execute(self):
        from django.apps import apps
        from plugins.erp_base.source_entry_registry import ENTRY_RULES
        target=apps.get_model(next(label for label,rules in ENTRY_RULES.items() if 'NewFuBan' in rules))
        item=services.write(target,{'_entry':'NewFuBan'},actor=self.actor)
        with self.assertRaisesMessage(ValidationError,'不能删除'):
            services.delete_documents(type(item).objects.filter(pk=item.pk),self.actor)
        item=services.write(model('RequestLimit'),{'_entry':'RequestLimit','old_sheet_series':'R','old_designee_id':'OTHER'},actor=self.actor)
        create('h_Employee',EmpID='OTHER',Name='他人')
        with self.assertRaisesMessage(ValidationError,'指定审核人'):
            services.approve(services.confirm(item,self.actor),self.actor)

    def test_new_binding_formulas_preserve_explicit_values_and_null_arithmetic(self):
        for entry in ['DStuffWeight','qry_QuoteRelaStuff']:
            item=services.write(model('StuffWeight'),{'_entry':entry,'old_cloth_qty_kg':-10,'old_sub_rate':Decimal('.2')},actor=self.actor)
            self.assertEqual(item.old_cloth_net_kg,-8)
            item=services.write(type(item),{'old_sub_rate':None},item,actor=self.actor)
            self.assertIsNone(item.old_cloth_net_kg)
        employee=services.write(model('h_Employee'),{'_entry':'qry_Employee','old_emp_id':'ORIGINAL'},actor=self.actor)
        self.assertEqual((employee.old_login_name,employee.old_password),(None,None))
        employee=services.write(type(employee),{'old_emp_id':'CHANGED'},employee,actor=self.actor)
        self.assertEqual((employee.old_login_name,employee.old_password),(None,None))
        editor=get_user_model().objects.create(username='edit-21',is_superuser=True)
        employee=services.write(type(employee),{'old_name':'修改员工'},employee,actor=editor)
        self.assertEqual(employee.old_modifyer,'edit-21')
        self.assertEqual(employee.old_creater,'binding-21')
        employee=services.write(type(employee),{'old_name':'保留空修改人','old_modifyer':None},employee,actor=editor)
        self.assertIsNone(employee.old_modifyer)
        item=services.write(model('RecordYield'),{'_entry':'QueryRecordCheck','old_kg':-10,'old_addkg':2,
            'old_tube_weight':1,'old_meter':-5,'old_add_qty':2,'old_grade_id':'D'},actor=self.actor)
        self.assertEqual((item.old_cust_qty,item.old_net_kg,item.old_real_qty,item.old_tubes),(-8,-11,-7,0))
        item=services.write(type(item),{'old_kg':None,'old_cust_qty':None,'old_grade_id':None},item,actor=self.actor)
        self.assertIsNone(item.old_cust_qty);self.assertIsNone(item.old_net_kg);self.assertEqual(item.old_tubes,1)

    def test_newfuban_shift_guard_checks_actual_login_and_shift(self):
        item=services.write(model('WProcess'),{'_entry':'NewFuBan'},actor=self.actor)
        with patch('plugins.erp_base.source_phase6_guards.timezone.localtime',return_value=at(2,10)):
            with self.assertRaisesMessage(ValidationError,'没有排班'):
                services.approve(services.confirm(item,self.actor),self.actor)
            create('p_Shift',ShiftID='S',StationID='09',ClassID='01',StratDate=at(1),EndDate=at(3))
            create('p_ShiftEmp',ShiftID='S',EmpID='E')
            item=services.approve(item,self.actor)
        self.assertEqual(item.approval_stage,'approved')

    def test_packaging_defect_totals_include_duplicate_and_negative_children(self):
        head=services.write(model('RecordYield'),{'_entry':'QueryRecordCheck'},actor=self.actor)
        rows=[services.write(model('RecordDefect'),{'source_parent_1':head,'_entry':'QueryRecordDefect2',
            'old_dots':-2,'old_times':1,'old_sum_dots':-2},actor=self.actor) for _ in range(2)]
        head.refresh_from_db();self.assertEqual(head.old_dots,-4)
        services.delete(type(rows[0]).objects.filter(pk=rows[0].pk),self.actor)
        head.refresh_from_db();self.assertEqual(head.old_dots,-2)

    def test_request_limit_reopen_replays_designated_employee_guard(self):
        item=services.write(model('RequestLimit'),{'_entry':'RequestLimit','old_sheet_series':'R','old_sheet_no':'R','old_designee_id':'E'},actor=self.actor)
        item=services.approve(services.confirm(item,self.actor),self.actor)
        other=get_user_model().objects.create(username='other-binding',is_superuser=True)
        create('h_Employee',EmpID='OTHER',LoginName=other.username,Name='另一员工')
        with self.assertRaisesMessage(ValidationError,'指定审核人'):services.reopen(item,other,'验证原指定人')
        item=services.reopen(item,self.actor,'指定人反审核')
        self.assertEqual(item.approval_stage,'draft')

    def test_two_original_linked_delete_guards_keep_duplicate_details(self):
        from django.apps import apps
        from plugins.erp_base.source_entry_registry import ENTRY_RULES
        create('GrayMaterial',SheetSeries='G')
        for _ in range(2):create('GrayMaterialDetail',Sheetseries='G',DetailNo='D')
        create('OrderMain',SheetSeries='O')
        for _ in range(2):create('OrderColor',SheetSeries='O',CheckNo='CHECK')
        for entry,data,message in [('qry_Winding_ToCustomer',{'old_sheetseries':'G'},'不允许删除'),
                                    ('qry_Order_ToCustomer',{'old_check_no':'CHECK'},'不允许删除')]:
            target=apps.get_model(next(label for label,rules in ENTRY_RULES.items() if entry in rules))
            item=services.write(target,{'_entry':entry,**data},actor=self.actor)
            with self.subTest(entry=entry),self.assertRaisesMessage(ValidationError,message):
                services.delete_documents(target.objects.filter(pk=item.pk),self.actor)
        self.assertEqual(model('GrayMaterialDetail').objects.count(),3)
        self.assertEqual(model('OrderColor').objects.count(),3)

    def test_retained_transfer_is_visible_and_readonly_without_new_model_field(self):
        from rest_framework.test import APIClient
        from plugins.erp_base.source_phase6_transfers import purchase_to_arrival,reverse_line_transfer
        client=APIClient();client.force_authenticate(self.actor)
        head=services.write(model('ArrivalNotice'),{'_entry':'ArrivalNotice','old_sheet_series':'A','old_sheet_no':'A'},actor=self.actor)
        original=create('PurDetail',DetailNo='P',Qty=-3,FabricID='F')
        purchase_to_arrival(head,[original],self.actor)
        target=model('ArrivalNoticeDetail').objects.get(source_parent_1=head)
        reverse_line_transfer(target,self.actor,at(3),'浏览器留档标识',reader)
        entity=target._meta.label_lower.replace('.','_')
        response=client.get('/api/system/'+entity+'/'+str(target.pk)+'/')
        self.assertEqual(response.data['data']['transfer_retained'],'已撤回留档')
        meta=client.get('/api/meta/'+entity+'/').data['data']
        self.assertIn('transfer_retained',meta['workflow']['freeze_when'])
        self.assertEqual(meta['workflow']['parent_bindings'],[{'relation':'source_parent_1',
            'fields':[{'field':'old_sheet_series','parent_original_field':'SheetSeries'}]}])
        self.assertNotIn('transfer_retained',[f.name for f in target._meta.fields])
