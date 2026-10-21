"""第六阶段续行、身份默认值、原游标重建及原版式填数的非空验证。"""
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase, SimpleTestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.test import APIClient
from .test_phase_report_audit import create
from .test_source_phase6 import reader
from plugins.erp_base.source_phase3_operations import model, source
from plugins.erp_base.source_entry_identity import login_value, LOGIN_KINDS
from plugins.erp_base.source_phase6_api import templates
from plugins.erp_base.source_phase6_layouts import describe
from plugins.erp_base.source_phase6_rendering import render, requirements, formatted
from plugins.erp_base import source_services as services


class EntryBehaviorTests(TestCase):
    def setUp(self):
        self.actor=get_user_model().objects.create(username='p6-final',name='账号显示名',is_superuser=True)

    def test_all_login_kinds_use_employee_business_fields(self):
        for _ in range(2):
            create('h_Employee',EmpID='E1',Name='员工名称',LoginName='P6-FINAL ',DeptID='D',
                   BusinessUnitID='B',ShiftID='S',PosID='P')
        create('p_Dept',DeptID='D',Name='生产部');create('p_Shift',ShiftID='S',Name='日班')
        values={'LoginPeople_LoginName':'p6-final','LoginPeople_EmpName':'员工名称',
                'LoginPeople_EmpID':'E1','LoginPeople.EmpID':'E1','LoginPeople_EmpDeptID':'D',
                'LoginPeople_EmpBusinessUnitID':'B','LoginPeople_EmpShiftID':'S',
                'LoginPeople_EmpPositionID':'P','LoginPeople_EmpShift':'日班','LoginPeople_EmpDept':'生产部'}
        self.assertEqual(set(values),LOGIN_KINDS)
        for kind,value in values.items():
            with self.subTest(kind=kind):self.assertEqual(login_value(kind,self.actor),value)
        self.assertEqual(source('h_Employee').count(),2)

    def test_original_lookup_returns_each_duplicate_join_and_copies_original_code(self):
        from plugins.erp_base.source_phase6_editors import options
        for name in ['甲','乙']:create('h_Employee',EmpID='DUP',Name=name,DeptID='D',IsOut=False)
        for name in ['部门一','部门二']:create('p_Dept',DeptID='D',Name=name)
        result=options('ArticleOutDetail','EmpID','DUP',reader)
        self.assertTrue(result['implemented']);self.assertEqual(len(result['rows']),4)
        self.assertTrue(all(r['id']=='DUP' for r in result['rows']))
        client=APIClient();client.force_authenticate(self.actor)
        response=client.post('/api/system/'+model('ArticleOutDetail')._meta.label_lower.replace('.','_')+'/phase6_query/',{
            'entry':'ArticleOutDetail','editor_field':'EmpID','filter_text':'DUP'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(len(response.data['data']['rows']),4)

    def test_editor_requires_original_registered_field(self):
        from plugins.erp_base.source_phase6_editors import options
        with self.assertRaises(ValidationError):options('ArticleOutDetail','NotOriginalField','',reader)

    def test_missing_identity_stays_null_and_conflicting_values_are_not_chosen(self):
        self.assertIsNone(login_value('LoginPeople_EmpID',self.actor))
        create('h_Employee',EmpID='E1',LoginName=self.actor.username)
        create('h_Employee',EmpID='E2',LoginName=self.actor.username)
        with self.assertRaises(ValidationError):login_value('LoginPeople_EmpID',self.actor)
        self.assertEqual(source('h_Employee').count(),2)

    def test_explicit_identity_and_null_override_generated_defaults(self):
        create('h_Employee',EmpID='E',Name='员工',LoginName=self.actor.username,BusinessUnitID='B')
        from plugins.erp_base.source_entry_services import apply_new_rules
        item=model('StuffWeight')()
        apply_new_rules(item,{'old_sheet_series':'S','old_sheet_no':'N'},self.actor,'AddStuffWeight')
        self.assertEqual(item.old_business_unit_id,'B');self.assertEqual(item.old_creater,'员工')
        item=model('StuffWeight')(old_business_unit_id=None,old_creater='手填')
        apply_new_rules(item,{'old_sheet_series':'S','old_sheet_no':'N','old_business_unit_id':None,'old_creater':'手填'},self.actor,'AddStuffWeight')
        self.assertIsNone(item.old_business_unit_id);self.assertEqual(item.old_creater,'手填')

    def test_copy_prev_row_keeps_manual_null_and_only_declared_fields(self):
        old=create('ArticleOutDetail',SheetSeries='OLD',EmpID='E',ProjectNo='P',Remarks='不复制')
        item=services.write(type(old),{'_entry':'ArticleOutDetail','_entry_copy_from':old,
                'old_sheet_series':'NEW','old_emp_id':None},actor=self.actor)
        self.assertIsNone(item.old_emp_id);self.assertEqual(item.old_project_no,'P')
        self.assertIsNone(item.old_remarks);self.assertEqual(item.old_sheet_series,'NEW')
        old.refresh_from_db();self.assertEqual(old.old_emp_id,'E')
        with self.assertRaises(ValidationError):
            services.write(type(item),{'_entry_copy_from':old},item,actor=self.actor)

    def test_copy_last_row_api_and_original_negative_values(self):
        old=create('RecordYield',BarCode='SAME',Addkg=Decimal('-2.5'),ColorDiff=None)
        client=APIClient();client.force_authenticate(self.actor)
        response=client.post('/api/system/erp_warehouse_sourcedyerecordyield/',{
            '_entry':'QC_Record','_entry_copy_from':old.pk,'old_bar_code':'SAME'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        item=source('RecordYield').get(pk=response.data['data']['id'])
        self.assertEqual(item.old_addkg,Decimal('-2.5'));self.assertIsNone(item.old_color_diff)
        self.assertEqual(source('RecordYield').filter(old_bar_code='SAME').count(),2)

    def test_lab_duplicate_headers_and_null_cursor_keep_sql_multiplicity(self):
        from plugins.erp_base.source_sample_flow import sync_lab
        from plugins.erp_base.source_entry_services import save_context
        a=create('DyeLabMain',SheetSeries='L',CustomerID='A');create('DyeLabMain',SheetSeries='L',CustomerID='B')
        create('DyeLabColor',SheetSeries='L',ColorNo='C',ColorNum='N')
        create('DyeLabColor',SheetSeries='L',ColorNo='C2',ColorNum='N')
        create('DyeLabColor',SheetSeries='L',ColorNo='C3',ColorNum=None)
        save_context(a,self.actor,'ShowDyeLabMain');sync_lab(a,self.actor)
        result=source('P_ColorNum')
        # 6游标迭代，4次连接插入4行；NULL颜色编码不匹配INSERT。
        self.assertEqual(result.count(),6)
        self.assertEqual(result.filter(old_color_no='C').count(),4)
        self.assertEqual(model('P_ColorNum').objects.count(),16)

    def test_qc_duplicate_barcodes_refresh_all_jobs_and_keep_negative_null_values(self):
        from plugins.erp_base.source_packaging_flow import qc_totals
        first=create('JobSheet',SheetSeries='A',SheetNo='JA');second=create('JobSheet',SheetSeries='B',SheetNo='JB')
        value=create('RecordYield',BarCode='DUP',JobSheetNo='JA',Dots=-2,Kg=Decimal('-2.25'),Yard=None)
        create('RecordYield',BarCode='DUP',JobSheetNo='JB',Dots=3,Kg=None,Yard=4)
        create('RecordYield',BarCode=None,JobSheetNo='JA',Dots=None,Kg=1,Yard=-1)
        qc_totals(value,self.actor);first.refresh_from_db();second.refresh_from_db()
        self.assertEqual((first.old_pdots,first.old_pkg,first.old_prolls,first.old_plength_qyt),(-2,Decimal('-1.25'),1,-1))
        self.assertEqual(second.old_pdots,3);self.assertIsNone(second.old_pkg)

    def test_original_h003_api_fills_authorized_query(self):
        from plugins.erp_base import source_phase6_entries as entries
        row=templates()[4];layout=describe(row)
        columns=sorted({b['DataMember'].split('.',1)[1] for band in layout['bands'] for c in leaves(band['controls']) for b in c['bindings']})
        result={'entry':'DyeLabColor','columns':[{'name':c} for c in columns],
                'rows':[[timezone.make_aware(datetime(2026,10,17)) if c=='SheetDate' else '<数据>' for c in columns]]}
        client=APIClient();client.force_authenticate(self.actor)
        with patch.object(entries,'run',return_value=result) as run:
            response=client.post('/api/system/erp_sampling_sourcedyedyelabmain/phase6_template/',{'index':4,'format':'Proof'},format='json')
        self.assertEqual(response.status_code,200,response.data);self.assertEqual(response.data['data']['page_count'],1)
        self.assertIn('&lt;数据&gt;',response.data['data']['html']);self.assertEqual(run.call_args.args[0],'DyeLabColor')

    def test_h003_actual_projection_resolves_reference_names_and_keeps_missing_enum_code(self):
        from plugins.erp_base import source_phase6_entries as entries
        from plugins.erp_base.source_phase6_rendering import reference_columns
        create('DyeLabMain',SheetSeries='L',SheetNo='LAB',SheetKind=3,SheetDate=timezone.now())
        for _ in range(2):create('DyeLabColor',SheetSeries='L',ColorNo='C',ProdID='P',ColorID='蓝色')
        create('p_Gray',GrayID='P',NameC='棉纱')
        result=entries.run('DyeLabColor',{},reader,True)
        resolved=reference_columns(templates()[4],result,reader)
        proof=render(templates()[4],resolved)
        self.assertEqual((proof['record_count'],proof['page_count']),(2,2))
        self.assertIn('棉纱',proof['html']);self.assertIn('原代码：3',proof['html'])
        self.assertEqual({r['field'] for r in proof['reference_resolutions']},{'CustomerID_R','ProdID_R','SheetKind_R'})
        self.assertEqual(len(proof['reference_resolutions']),6)

    def test_formula_and_current_document_do_not_recount_retired_child_rows(self):
        from plugins.erp_base.source_phase6_expressions import calculate
        from plugins.erp_base.source_phase6_printing import document
        from plugins.erp_base.source_phase3_operations import retire
        head=create('GrayIn',SheetSeries='G')
        create('GrayInDetail',SheetSeries='G',ReceSheetNo='A',Rolls=-2,WeightQty=-3)
        removed=create('GrayInDetail',SheetSeries='G',ReceSheetNo='A',Rolls=9,WeightQty=10)
        retire(type(removed).objects.filter(pk=removed.pk),self.actor,'退回旧行留档')
        result=calculate(head,'GrayIn',reader,self.actor)
        values={row['field']:row.get('value') for row in result['rows']}
        self.assertEqual(values['DlvRolls'],-2);self.assertEqual(values['DlvWeightQty'],-3)
        parts=document(head,reader)
        self.assertEqual(sum(len(part['rows']) for part in parts if part['table']=='GrayInDetail'),1)
        self.assertEqual(type(removed).objects.count(),2)


def leaves(controls):
    return [leaf for control in controls for leaf in (leaves(control['children']) if control['children'] else [control])]


class OriginalProofTests(SimpleTestCase):
    def fixture(self):
        row=templates()[4];layout=describe(row)
        fields=sorted({b['DataMember'].split('.',1)[1] for band in layout['bands'] for c in leaves(band['controls']) for b in c['bindings']})
        values=[datetime(2026,10,17) if f=='SheetDate' else '重复<&>原行' for f in fields]
        return row,{'entry':'DyeLabColor','columns':[{'name':f} for f in fields],'rows':[values,values,values]}

    def test_original_fixed_page_preserves_every_duplicate_and_escapes_text(self):
        row,result=self.fixture();self.assertEqual(requirements(row),[])
        proof=render(row,result)
        self.assertEqual((proof['record_count'],proof['page_count']),(3,3))
        self.assertEqual(proof['html'].count('class="page"'),3)
        self.assertIn('2026-10-17',proof['html']);self.assertIn('重复&lt;&amp;&gt;原行',proof['html'])

    def test_missing_and_duplicate_projection_not_replaced_with_empty_text(self):
        row,result=self.fixture();result['columns'][0]['name']='MISSING'
        with self.assertRaises(ValidationError):render(row,result)
        row,result=self.fixture();result['columns'].append(result['columns'][0])
        with self.assertRaises(ValidationError):render(row,result)

    def test_unimplemented_scripts_reported_and_original_bytes_unchanged(self):
        row=next(row for row in templates() if row['RptID']=='H009');original=row['TemplateXml']
        self.assertTrue(requirements(row))
        with self.assertRaises(ValidationError):render(row,{'entry':'unused'})
        self.assertEqual(row['TemplateXml'],original)

    def test_decimal_null_and_optional_decimal_formats(self):
        self.assertEqual(formatted(Decimal('-12345678901234567890.125'),'{0:n3}'),'-12,345,678,901,234,567,890.125')
        self.assertEqual(formatted(None,'{0:0.00}'),'')
        self.assertEqual(formatted(Decimal('2.500'),'{0:0.###}'),'2.5')
        with self.assertRaises(ValidationError):formatted(1,'{0:unsupported}')

    def test_original_date_format_uses_business_local_day(self):
        from datetime import timezone as tz
        with timezone.override('Asia/Shanghai'):
            value=datetime(2026,10,16,16,30,tzinfo=tz.utc)
            self.assertEqual(formatted(value,'{0:yyyy-MM-dd HH:mm:ss}'),'2026-10-17 00:30:00')
