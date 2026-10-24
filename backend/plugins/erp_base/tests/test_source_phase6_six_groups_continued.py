import base64
from datetime import datetime
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.apps import apps
from .test_phase_report_audit import create
from plugins.erp_base.source_phase3_operations import model
from plugins.erp_base import source_phase6_entries as entries
from plugins.erp_base.source_phase6_projection_formulas import calculate
from plugins.erp_base.source_phase6_projection_context import ProjectionContext
from tools.development_archive.customer_boundary_20261024.backend.source_phase6_api import templates
from plugins.erp_base.source_phase6_rendering import render,requirements,reference_columns
from plugins.erp_base.source_phase6_layouts import parse_xml
from plugins.erp_base.source_phase6_print_sources import attach,projections


def reader(name,module):return apps.get_model(module+'.SourceDye'+name).objects.all()


def proof(code):
    report=next(r for r in templates() if r['RptID']==code)
    root,_=parse_xml(base64.b64decode(report['TemplateXml']))
    entry=root.get('DataMember')
    result=entries.run(entry,{},reader,load_records=True,additional_projection=projections(entry))
    return render(report,reference_columns(report,attach(root,result,reader,{},True),reader))


class ContinuedSixGroupsTests(TestCase):
    def test_missing_parent_cannot_recalculate_money_from_stale_need_qty(self):
        from plugins.erp_base.source_phase6_formula_runtime import apply
        item=model('StuffWeightDetail')(old_need_qty=20,old_need_money=70,old_price=3,old_dosage=2,old_weight_unit='K')
        _,pending=apply(item,{},'ProcessStuffWeightPhaseDetail',creating=True)
        self.assertEqual(item.old_need_money,70)
        self.assertIn('NeedMoney',[p['field'] for p in pending])
        self.assertIn('依赖公式NeedQty',next(p['reason'] for p in pending if p['field']=='NeedMoney'))
        apply(item,{'old_need_qty':20},'ProcessStuffWeightPhaseDetail',creating=True)
        self.assertEqual(item.old_need_money,60)

    def test_quote_related_material_price_uses_detail_not_head_and_keeps_original_columns(self):
        from plugins.erp_base.source_phase6_projection_overrides import projections as formula_projections
        create('StuffWeight',SheetSeries='CONT-PRICE',Price=999)
        create('StuffWeightPhase',SheetSeries='CONT-PRICE',PhaseNo=1)
        for qty in [2,2,-3]:create('StuffWeightDetail',SheetSeries='CONT-PRICE',PhaseNo=1,StuffNo=1,Price=3,Dosage=qty,NeedQty=4,RealQty=5)
        entry='qry_QuoteRelaStuff'
        result=entries.run(entry,{},reader,load_records=True,additional_projection=formula_projections(entry))
        self.assertEqual(sum(c['name'].lower()=='price' for c in result['columns']),2)
        fields=[f for f in entries.definition(entry)['fields'] if f['FieldName'] in ['NeedMoney','RealMoney']]
        answer=calculate(result,fields,ProjectionContext(result,reader,{},True))
        self.assertEqual(answer['formula_issues'],[])
        self.assertEqual([r[-2:] for r in answer['rows']],[[24,30],[24,30],[-36,-45]])
        self.assertEqual([r[:len(result['columns'])] for r in answer['rows']],result['rows'])

    def test_quote_recipe_parent_remarks_and_duplicate_recipe_lines(self):
        from plugins.erp_base.source_phase6_projection_overrides import projections as formula_projections
        create('JobSheet',SheetSeries='CONT-J',SheetNo='CONT-J',Remarks='明确工卡备注')
        create('DyeRecipe',SheetSeries='CONT-R')
        create('DyeRecipePhase',SheetSeries='CONT-R',PhaseNo=1)
        create('DyeRecipeJob',SheetSeries='CONT-R',JobSheetNo='CONT-J')
        for qty in [2,2,-3]:create('DyeRecipeDetail',SheetSeries='CONT-R',PhaseNo=1,StuffNo=1,Price=3,Dosage=qty)
        entry='qry_QuoteRelaRecipe'
        result=entries.run(entry,{},reader,load_records=True,additional_projection=formula_projections(entry))
        actual=calculate(result,entries.definition(entry)['fields'],ProjectionContext(result,reader,{},True))
        self.assertEqual(actual['formula_issues'],[])
        names=[c['name'] for c in actual['columns']]
        self.assertEqual([r[names.index('Remarks__formula')] for r in actual['rows']],['明确工卡备注']*3)

    def test_three_weight_print_sources_null_negative_and_ambiguous_parent(self):
        for entry,head in [('AddStuffWeightPhaseDetailPrint','AddStuffWeight'),('NormalStuffWeightPhaseDetailPrint','NormalStuffWeight'),('ReworkStuffWeightPhaseDetailPrint','ReworkStuffWeight')]:
            with self.subTest(entry=entry):
                key=entry[:5];create('StuffWeight',SheetSeries=key,RecipeType=2,Rate=-8)
                result={'entry':entry,'columns':[{'name':'SheetSeries'}],'rows':[[key],[key],[None]]}
                fields=[f for f in entries.definition(entry)['fields'] if f['FieldName']=='BathRatio']
                actual=calculate(result,fields,ProjectionContext(result,reader,{},True))
                self.assertEqual([r[-1] for r in actual['rows']],[-8,-8,None])
                self.assertEqual([e['row'] for e in actual['formula_issues']],[3])
                self.assertEqual(len(actual['formula_source_resolutions']),1)
                create('StuffWeight',SheetSeries=key,RecipeType=2,Rate=None)
                ambiguous=calculate(result,fields,ProjectionContext(result,reader,{},True))
                self.assertEqual(len(ambiguous['rows']),3)
                self.assertIn('匹配行数2',ambiguous['formula_issues'][0]['reason'])

    def test_stock_selector_expressions_preserve_codes_duplicates_and_null(self):
        for entry in ['StuffStockToCheck','StuffStockToCheckBig']:
            original=[['B093','13'],['B093','13'],[None,''],['物料-异常','未登记库']]
            result={'entry':entry,'columns':[{'name':'StuffID'},{'name':'WareHouseID'}],'rows':original}
            fields=[f for f in entries.definition(entry)['fields'] if f['FieldName'] in ['StuffID','WareHouseID']]
            actual=calculate(result,fields)
            self.assertEqual(actual['formula_issues'],[])
            self.assertEqual([r[:2] for r in actual['rows']],original)
            self.assertEqual([r[2:] for r in actual['rows']],original)
            self.assertEqual(len(actual['formula_source_resolutions']),2)

    def test_parent_print_fields_use_original_relation_and_preserve_duplicate_details(self):
        date=timezone.make_aware(datetime(2026,10,17))
        create('CarryMaterial',SheetSeries='CONT-C',SheetNo='提料原单头',SheetDate=date)
        for n in [2,-3]:create('CarryMaterialDetail',Sheetseries='CONT-C',DetailNo='DUP',Rolls=n)
        answer=proof('H007')
        self.assertEqual(answer['record_count'],2)
        self.assertIn('提料原单头',answer['html'])
        self.assertEqual(len(answer['parent_source_resolutions']),2)
        create('CarryMaterial',SheetSeries='CONT-C',SheetNo='第二个父单')
        with self.assertRaisesMessage(ValidationError,'matched_rows'):proof('H007')
        self.assertEqual(model('CarryMaterialDetail').objects.count(),2)

    def test_gray_material_print_parent_key(self):
        create('GrayMaterial',SheetSeries='CONT-G',SheetNo='原紧筒单')
        for n in [2,-3]:create('GrayMaterialDetail',Sheetseries='CONT-G',DetailNo='DUP',Rolls=n)
        answer=proof('H019')
        self.assertEqual(answer['record_count'],2)
        self.assertIn('CONT-G',answer['html'])

    def test_original_gray_nested_summary_zero_height_details(self):
        date=timezone.make_aware(datetime(2026,10,17))
        create('p_Customer',CustomerID='CONT-C',NameC='完整客户名称',ShortName='简称')
        create('GrayIn',SheetSeries='CONT-IN',SheetNo='CONT-IN',CustomerID='CONT-C',SheetKind=1,SheetDate=date)
        for material,qty in [('G1',2),('G1',2),('G2',-3)]:
            create('GrayInDetail',SheetSeries='CONT-IN',ReceSheetNo='DUP',GrayID=material,Rolls=qty,WeightQty=qty*10)
        for code in ['R014','R040']:
            with self.subTest(code=code):
                answer=proof(code)
                self.assertEqual(answer['record_count'],3)
                self.assertEqual(answer['page_count'],1)
                self.assertIn('>4</div>',answer['html'])
                self.assertIn('>-3</div>',answer['html'])
                self.assertIn('>1</div>',answer['html'])
                if code=='R014':self.assertIn('完整客户名称',answer['html'])

    def test_original_gray_out_three_levels_use_explicit_kind_code_and_duplicate_rows(self):
        create('GrayOut',SheetSeries='CONT-OUT',SheetNo='CONT-OUT',CustomerID='CONT-C',GrayKindID='原类别')
        for qty in [2,2,-3]:create('GrayOutDetail',SheetSeries='CONT-OUT',ReceSheetNo='DUP',GrayID='G',Rolls=qty,WeightQty=qty*10)
        answer=proof('R036')
        self.assertEqual(answer['record_count'],3)
        self.assertEqual(answer['page_count'],1)
        self.assertIn('>1</div>',answer['html'])
        self.assertIn('GrayKindID',answer['notes'][0])

    def test_nested_groups_separate_same_inner_key_by_outer_key_and_page_totals(self):
        xml='''<Report ControlType="XtraReport" DataMember="h_Employeelit" PageWidth="400" PageHeight="160" Margins="0,0,0,0"><Bands>
        <O ControlType="GroupHeaderBand" Name="outer" Level="1" HeightF="20" RepeatEveryPage="true"><GroupFields><F FieldName="Name"/></GroupFields><Controls><L ControlType="XRLabel" SizeF="100,20"><DataBindings><B PropertyName="Text" DataMember="h_Employeelit.Name"/></DataBindings></L></Controls></O>
        <I ControlType="GroupHeaderBand" Name="inner" HeightF="20"><GroupFields><F FieldName="EmpID"/></GroupFields></I>
        <D ControlType="DetailBand" Name="detail" HeightF="40"><Controls><L ControlType="XRLabel" SizeF="100,20"><Summary Running="Group" Func="RecordNumber"/></L></Controls></D>
        <IF ControlType="GroupFooterBand" Name="innerFooter" HeightF="20"><Controls><L ControlType="XRLabel" SizeF="100,20"><Summary Running="Group" Func="Count"/><DataBindings><B PropertyName="Text" DataMember="h_Employeelit.EmpID"/></DataBindings></L></Controls></IF>
        <OF ControlType="GroupFooterBand" Name="outerFooter" Level="1" HeightF="20"><Controls><L ControlType="XRLabel" SizeF="100,20"><Summary Running="Group" Func="Count"/><DataBindings><B PropertyName="Text" DataMember="h_Employeelit.EmpID"/></DataBindings></L></Controls></OF>
        </Bands></Report>'''
        report={'RptID':'CONT-GROUP','RptTitle':'分组分页','TemplateXml':base64.b64encode(xml.encode()).decode()}
        self.assertEqual(requirements(report),[])
        answer=render(report,{'entry':'h_Employeelit','columns':[{'name':'Name'},{'name':'EmpID'}],'rows':[['甲','同码']]*3+[['乙','同码']]})
        self.assertEqual(answer['record_count'],4)
        self.assertGreater(answer['page_count'],1)
        self.assertIn('>3</div>',answer['html'])
        self.assertIn('>1</div>',answer['html'])
        self.assertNotIn('>4</div>',answer['html'])

    def test_repeating_group_footer_reserves_page_space_and_does_not_duplicate_last_footer(self):
        xml='''<Report ControlType="XtraReport" DataMember="h_Employeelit" PageWidth="400" PageHeight="120" Margins="0,0,0,0"><Bands>
        <G ControlType="GroupHeaderBand" HeightF="20" RepeatEveryPage="true"><GroupFields><F FieldName="Name"/></GroupFields></G>
        <D ControlType="DetailBand" HeightF="40"><Controls><L ControlType="XRLabel" SizeF="100,20"><DataBindings><B PropertyName="Text" DataMember="h_Employeelit.EmpID"/></DataBindings></L></Controls></D>
        <F ControlType="GroupFooterBand" HeightF="20" RepeatEveryPage="true" PrintAtBottom="true"><Controls><L ControlType="XRLabel" SizeF="100,20"><Summary Running="Group" Func="Count" FormatString="组总数:{0}"/><DataBindings><B PropertyName="Text" DataMember="h_Employeelit.EmpID"/></DataBindings></L></Controls></F>
        </Bands></Report>'''
        report={'RptID':'CONT-REPEAT','RptTitle':'每页组尾','TemplateXml':base64.b64encode(xml.encode()).decode()}
        answer=render(report,{'entry':'h_Employeelit','columns':[{'name':'Name'},{'name':'EmpID'}],'rows':[['同组','同号'] for _ in range(5)]})
        self.assertEqual(answer['page_count'],3)
        self.assertEqual(answer['record_count'],5)
        self.assertEqual(answer['html'].count('>组总数:5</div>'),3)
        self.assertEqual(answer['html'].count('>同号</div>'),5)
