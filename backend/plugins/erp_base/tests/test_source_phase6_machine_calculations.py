"""染机本地资料、盘点差额、部门申请转采购及原版式计算字段。"""
import base64
from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase,SimpleTestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .test_phase_report_audit import create
from .test_source_phase6 import reader
from .test_source_phase6_stock_print import dictionaries
from plugins.erp_base.source_phase3_operations import model


class MachineCalculationTests(TestCase):
    def setUp(self):self.actor=get_user_model().objects.create(username='p6-calcs',is_superuser=True)

    def test_dye_machine_preserves_local_filter_duplicate_and_null_codes(self):
        from plugins.erp_base.source_phase6_entries import run
        for _ in range(2):create('p_Machine',MachineType=50,MachineID='DUP',MachineNo=17,MaxWaitVats=-2)
        create('p_Machine',MachineType=50,MachineID='EMPTY',MachineNo=None)
        create('p_Machine',MachineType=20,MachineID='OTHER')
        rows=dictionaries(run('vw_DyeMachine',{},reader,True))
        self.assertEqual(len(rows),3)
        self.assertTrue(all(r['lx_machineid'] is None for r in rows))
        self.assertEqual(len([r for r in rows if r['machineid']=='DUP' and r['maxwaitvats']==-2]),2)

    def test_three_stock_adjust_variants_match_original_and_preserve_manual_and_history(self):
        from plugins.erp_base import source_services as services
        from plugins.erp_base.source_phase6_auto_values import AUTO_NULL_DIFFERENCES,before_save
        from plugins.erp_base.source_entry_registry import ENTRY_RULES
        for entry in ['GrayStockAdjustDetail','ProdStockAdjustDetail','SemiStockAdjustDetail']:
            m=model(entry);data={'_entry':entry,'old_sheet_series':'S'}
            for target,left,right in AUTO_NULL_DIFFERENCES[entry]:
                self.assertEqual(ENTRY_RULES[m._meta.label][entry]['formula_fields'][target]['expression'],f'ISNULL([{left}],0)-ISNULL([{right}],0)')
                data[m.SOURCE_FIELDS[left]]=None;data[m.SOURCE_FIELDS[right]]=5
            item=services.write(m,data,actor=self.actor)
            for target,_,_ in AUTO_NULL_DIFFERENCES[entry]:self.assertEqual(getattr(item,m.SOURCE_FIELDS[target]),-5)
            item=services.write(m,{'old_real_rolls':-2,'old_adjust_rolls':None},item,actor=self.actor)
            self.assertIsNone(item.old_adjust_rolls)
            item=services.write(m,{'old_remarks':'unrelated'},item,actor=self.actor)
            self.assertIsNone(item.old_adjust_rolls)
            historical=m(source_batch_id=1,old_adjust_rolls=77)
            before_save(historical,{},entry,True);self.assertEqual(historical.old_adjust_rolls,77)

    def test_department_purchase_variants_preserve_selected_headers_and_repeat_source(self):
        from plugins.erp_base import source_services as services
        from plugins.erp_base.source_phase6_transfers import department_apply_to_purchase
        from plugins.erp_base.source_context import SourceDocumentContext
        from plugins.erp_base.source_phase6_entries import run
        for prefix in ['Article','Stuff']:
            source=create(prefix+'DeptApply',SheetSeries='S',SheetNo='SOURCE',RightStatus=10)
            create(prefix+'DeptApply',SheetSeries='S',SheetNo='OTHER',RightStatus=0)
            line=create(prefix+'DeptApplyDetail',SheetSeries='S',DetailNo='D',Name='物料',Unit='箱',Qty=10,Amount=99,
                **{prefix+'ID':'A',prefix+'KindID':'K'})
            head=services.write(model(prefix+'PurMain'),{'_entry':prefix+'PurMain','old_sheet_series':prefix,'old_sheet_no':prefix},actor=self.actor)
            before=run(prefix+'PurApplyToPur',{},reader,True)['count'];self.assertEqual(before,1)
            first=department_apply_to_purchase(line,source,head,Decimal('-2'),Decimal('3'),self.actor)
            self.assertEqual(first.old_apply_sheet_no,'SOURCE');self.assertEqual(first.old_amount,-6)
            self.assertEqual(getattr(first,'old_'+prefix.lower()+'_unit'),'箱')
            self.assertEqual(run(prefix+'PurApplyToPur',{},reader,True)['count'],0)
            second=department_apply_to_purchase(line,source,head,None,None,self.actor)
            self.assertNotEqual(first.pk,second.pk);self.assertIsNone(second.old_amount)
            origin=SourceDocumentContext.objects.get(entity=first._meta.label,object_id=first.pk).effects['department_purchase_origin']
            self.assertEqual(origin['application']['id'],source.pk)
            self.assertEqual(Decimal(origin['line']['old_amount']),99)
            wrong=create(prefix+'DeptApply',SheetSeries='WRONG')
            with self.assertRaises(ValidationError):department_apply_to_purchase(line,wrong,head,1,1,self.actor)
            head.approval_stage='approved';head.save(update_fields=['approval_stage'])
            with self.assertRaises(ValidationError):department_apply_to_purchase(line,source,head,1,1,self.actor)
        self.assertEqual(model('PurDetail').objects.count(),4)

    def test_department_purchase_api(self):
        from plugins.erp_base import source_services as services
        from rest_framework.test import APIClient
        line=create('StuffDeptApplyDetail',SheetSeries='S',StuffID='D')
        source=create('StuffDeptApply',SheetSeries='S',SheetNo='A')
        head=services.write(model('StuffPurMain'),{'_entry':'StuffPurMain','old_sheet_series':'P','old_sheet_no':'P'},actor=self.actor)
        client=APIClient();client.force_authenticate(self.actor)
        path='/api/system/'+line._meta.label_lower.replace('.','_')+'/'+str(line.pk)+'/phase6_department_apply_to_purchase/'
        response=client.post(path,{'application':source.pk,'head':head.pk,'quantity':-2,'price':3},format='json')
        self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(model('PurDetail').objects.get().old_amount,-6)
        with patch('core.permissions.ApiPermission.has_permission',return_value=False):
            response=client.post(path,{'application':source.pk,'head':head.pk,'quantity':2,'price':3},format='json')
        self.assertEqual(response.status_code,403)
        self.assertEqual(model('PurDetail').objects.count(),1)


class CalculatedPrintTests(SimpleTestCase):
    def template(self,formula='Abs([Name])',extra='',field='result'):
        xml=f'''<Report ControlType="XtraReport" DataMember="h_Employeelit" PageWidth="100" PageHeight="70" Dpi="100" Margins="0,0,0,0">
        <CalculatedFields>{extra}<F Name="result" DataMember="h_Employeelit" Expression="{formula}"/></CalculatedFields>
        <Bands><D ControlType="DetailBand" HeightF="20"><Controls><L ControlType="XRLabel" SizeF="100,20"><DataBindings><B PropertyName="Text" DataMember="h_Employeelit.{field}"/></DataBindings></L></Controls></D>
        <PF ControlType="PageFooterBand" HeightF="10"><Controls><L ControlType="XRLabel" SizeF="100,10"><DataBindings><B PropertyName="Text" DataMember="h_Employeelit.{field}"/></DataBindings><Summary Running="Page" IgnoreNullValues="true"/></L></Controls></PF></Bands></Report>'''
        return {'RptID':'CALC','RptTitle':'计算','TemplateXml':base64.b64encode(xml.encode()).decode()}

    def proof(self,rows,**kwargs):
        from plugins.erp_base.source_phase6_rendering import render
        return render(self.template(**kwargs),{'entry':'h_Employeelit','columns':[{'name':'Name'}],'rows':[[v] for v in rows]})

    def test_calculated_abs_keeps_duplicate_and_null_then_page_summary(self):
        result=self.proof([-2,-2,None,-3])
        self.assertEqual(result['record_count'],4);self.assertEqual(result['page_count'],2)
        self.assertEqual(result['html'].count('>2</div>'),2)
        self.assertIn('>4</div>',result['html'].split('</section>')[0])
        self.assertEqual(result['html'].split('</section>')[1].count('>3</div>'),2)

    def test_calculated_dependencies_case_insensitive_and_unused_unsupported_kept(self):
        extra='<A Name="base" DataMember="h_Employeelit" Expression="IsNull([Name],0)-1"/><U Name="unused" Expression="Unknown()"/>'
        result=self.proof([None,-2],formula='[BASE]*2',extra=extra,field='RESULT')
        self.assertEqual(result['calculated_fields'],['base','result'])
        self.assertIn('>-2</div>',result['html']);self.assertIn('>-6</div>',result['html'])
        self.assertEqual(result['calculation_usage']['unreferenced'],['unused'])

    def test_zero_denominator_non_numeric_and_ambiguous_input_are_explicit_errors(self):
        from plugins.erp_base.source_phase6_rendering import render
        with self.assertRaises(ValidationError):self.proof([1,0,2],formula='1/[Name]')
        with self.assertRaises(ValidationError):self.proof(['not numeric'])
        with self.assertRaises(ValidationError):render(self.template(),{'entry':'h_Employeelit','columns':[{'name':'Name'},{'name':'Name'}],'rows':[[1,2]]})

    def test_cycles_cross_relations_and_unsupported_functions_remain_differences(self):
        from plugins.erp_base.source_phase6_rendering import requirements
        self.assertTrue(any('循环' in s for s in requirements(self.template('[result]+1'))))
        self.assertTrue(any('未实现原计算字段' in s for s in requirements(self.template('UnknownFunction([Name],2)'))))
        with self.assertRaises(ValidationError):self.proof([1],formula='Abs([Missing])')

    def test_original_r127_arithmetic_plan(self):
        from plugins.erp_base.source_phase6_api import templates
        from plugins.erp_base.source_phase6_layouts import parse_xml
        from plugins.erp_base.source_phase6_calculated_print import apply
        root,_=parse_xml(base64.b64decode(templates()[244]['TemplateXml']))
        result=apply(root,{'columns':[{'name':'Rolls'},{'name':'WeightQty'}],'rows':[[-2,Decimal('-1.25')],[-2,None]]})
        self.assertEqual(result['rows'],[[-2,Decimal('-1.25'),2,Decimal('1.25')],[-2,None,2,None]])

    def test_calculated_float_arithmetic_and_string_output_preserve_source(self):
        from plugins.erp_base.source_phase6_layouts import parse_xml
        from plugins.erp_base.source_phase6_calculated_print import apply
        root,_=parse_xml(base64.b64decode(self.template('[Name]*2')['TemplateXml']))
        source={'columns':[{'name':'Name'}],'rows':[[1.25],[None]]}
        self.assertEqual(apply(root,source)['rows'],[[1.25,Decimal('2.50')],[None,None]])
        self.assertEqual(source['rows'],[[1.25],[None]])
        root,_=parse_xml(base64.b64decode(self.template("[Name]+'原文'")['TemplateXml']))
        self.assertEqual(apply(root,{'columns':[{'name':'Name'}],'rows':[['<重复>'],['<重复>'],[None]]})['rows'],
            [['<重复>','<重复>原文'],['<重复>','<重复>原文'],[None,None]])
