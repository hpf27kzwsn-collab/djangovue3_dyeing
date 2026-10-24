"""成品金额/实数自动联动、报价转调价、条件版式与成品出仓原校样。"""
import base64
from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase,SimpleTestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .test_phase_report_audit import create,at
from plugins.erp_base.source_phase3_operations import model


class DispatchTests(TestCase):
    def setUp(self):self.actor=get_user_model().objects.create(username='p6-dispatch',is_superuser=True)

    def test_product_out_amount_then_total_and_explicit_null(self):
        from plugins.erp_base import source_services as services
        for entry in ['ProdOutDetail','ProdOutDetailUpdate']:
            m=model('ProdOutDetail')
            item=services.write(m,{'_entry':entry,'old_sheet_series':entry,'old_weight_qty':None,'old_price':None},actor=self.actor)
            self.assertEqual((item.old_amount,item.old_total),(0,0))
            item=services.write(m,{'old_weight_qty':-2,'old_price':3},item,actor=self.actor)
            self.assertEqual((item.old_amount,item.old_total),(-6,-6))
            item=services.write(m,{'old_weight_qty':4,'old_amount':None},item,actor=self.actor)
            self.assertIsNone(item.old_amount);self.assertEqual(item.old_total,0)
            item=services.write(m,{'old_price':5,'old_total':None},item,actor=self.actor)
            self.assertEqual(item.old_amount,20);self.assertIsNone(item.old_total)
            item=services.write(m,{'old_remarks':'无关修改'},item,actor=self.actor)
            self.assertIsNone(item.old_total)

    def test_product_record_real_quantity_and_original_formula_and_history(self):
        from plugins.erp_base import source_services as services
        from plugins.erp_base.source_phase6_auto_values import before_save
        from plugins.erp_base.source_entry_registry import ENTRY_RULES
        for entry in ['ProdInRecord','ProdInRecordWork']:
            m=model('ProdInRecord')
            self.assertEqual(ENTRY_RULES[m._meta.label][entry]['formula_fields']['RealQty']['expression'],'ISNULL([WeightQty],0)')
            item=services.write(m,{'_entry':entry,'old_sheet_no':'S','old_weight_qty':None},actor=self.actor)
            self.assertEqual(item.old_real_qty,0)
            item=services.write(m,{'old_weight_qty':-2},item,actor=self.actor)
            self.assertEqual(item.old_real_qty,-2)
            item=services.write(m,{'old_weight_qty':9,'old_real_qty':None},item,actor=self.actor)
            self.assertIsNone(item.old_real_qty)
            history=m(source_batch_id=1,old_real_qty=77)
            before_save(history,{},entry,True);self.assertEqual(history.old_real_qty,77)
        for entry in ['ProdOutDetail','ProdOutDetailUpdate']:
            rules=ENTRY_RULES[model('ProdOutDetail')._meta.label][entry]['formula_fields']
            self.assertEqual(rules['Amount']['expression'],'IsNull([Price]*[WeightQty],0)')
            self.assertEqual(rules['Total']['expression'],'IsNull([Amount],0)')

    def test_quote_transfer_preserves_selected_source_and_original_color_writeback(self):
        from plugins.erp_base import source_services as services
        from plugins.erp_base.source_phase6_transfers import quote_to_price_adjustment
        from plugins.erp_base.source_context import SourceDocumentContext
        quote=create('Quote',SheetSeries='Q',SheetNo='QN',CustomerID='C',SheetDate=at(1))
        create('Quote',SheetSeries='Q',SheetNo='OTHER',CustomerID='OTHER')
        line=create('QuoteDetail',Width=1,Weight=1,PriceUnit=1,SheetSeries='Q',DetailNo='QD',ColorNum='X123',Price=10,AdjustPrice=99)
        other=create('QuoteDetail',Width=1,Weight=1,PriceUnit=1,SheetSeries='X',DetailNo='OTHER',ColorNum='X123',Price=88)
        head=services.write(model('PriceAdjust'),{'_entry':'PriceAdjust','old_sheet_series':'A','old_sheet_no':'A',
            'old_adjust_money':-3,'old_adjust_ratio':999,'old_start_date':at(2),'old_date_type':1},actor=self.actor)
        first=quote_to_price_adjustment(line,quote,head,self.actor)
        self.assertEqual((first.old_old_price,first.old_adjust_price,first.old_customer_id),(10,7,'C'))
        self.assertEqual((first.old_quote_detail_no,first.old_sheet_no),('QD','QN'))
        other.refresh_from_db();self.assertEqual(other.old_adjust_price,7)
        context=SourceDocumentContext.objects.get(entity=first._meta.label,object_id=first.pk)
        self.assertEqual(Decimal(context.effects['quote_adjustment_origin']['line']['old_adjust_price']),99)
        self.assertNotEqual(first.pk,quote_to_price_adjustment(line,quote,head,self.actor).pk)
        wrong=create('Quote',SheetSeries='WRONG')
        with self.assertRaises(ValidationError):quote_to_price_adjustment(line,wrong,head,self.actor)
        self.assertEqual(model('PriceAdjustDetail').objects.count(),2)

    def test_quote_transfer_null_price_api_and_atomic_failure(self):
        from plugins.erp_base import source_services as services
        from rest_framework.test import APIClient
        quote=create('Quote',SheetSeries='Q',SheetNo='QN')
        line=create('QuoteDetail',Width=1,Weight=1,PriceUnit=1,SheetSeries='Q',DetailNo='D',ColorNum='X1',Price=None)
        head=services.write(model('PriceAdjust'),{'_entry':'PriceAdjust','old_sheet_series':'A','old_sheet_no':'A','old_adjust_money':2},actor=self.actor)
        client=APIClient();client.force_authenticate(self.actor)
        path='/api/system/erp_sales_sourcedyequotedetail/'+str(line.pk)+'/phase6_quote_to_price_adjustment/'
        body={'quote':quote.pk,'head':head.pk}
        response=client.post(path,body,format='json');self.assertEqual(response.status_code,200,response.data)
        self.assertIsNone(model('PriceAdjustDetail').objects.get().old_adjust_price)
        with patch('plugins.erp_base.source_services.finish',side_effect=ValidationError('不能完成办理')):
            response=client.post(path,body,format='json')
        self.assertEqual(response.status_code,400);self.assertEqual(model('PriceAdjustDetail').objects.count(),1)

    def test_original_r013_api_keeps_duplicate_outgoing_and_returns(self):
        from rest_framework.test import APIClient
        create('p_Customer',CustomerID='C',ShortName='客户',NameC='客户')
        create('ProdOut',SheetSeries='O',SheetNo='OUT',CustomerID='C',SheetDate=at(1))
        create('ProdOutDetail',SheetSeries='O',JobSheetNo='J',Rolls=3,GrayQty=4,WeightQty=5)
        for _ in range(2):
            create('JobSheet',SheetNo='J',JobKindID='02')
            create('ProdIn',SheetKind=16,CustomerID='C',SheetNo='RET',SheetDate=at(2),Rolls=2,GaryWeight=3,WeightQty=4)
        client=APIClient();client.force_authenticate(self.actor)
        response=client.post('/api/system/erp_production_sourcedyejobsheet/phase6_template/',{'index':152,'format':'Proof','load_records':True},format='json')
        self.assertEqual(response.status_code,200,response.data)
        data=response.data['data'];self.assertEqual(data['record_count'],4)
        self.assertEqual(data['html'].count('>OUT</div>'),2)
        self.assertEqual(data['html'].count('>退车间</div>'),2)
        self.assertIn('返工布',data['html'])


class ConditionalPrintTests(SimpleTestCase):
    def expression(self,text,values=None):
        from plugins.erp_base.source_phase6_calculated_print import expression,evaluate
        return evaluate(expression(text),values or {},at(2))

    def test_iif_multiple_branches_null_zero_and_short_circuit(self):
        self.assertEqual(self.expression("Iif([x]=1,'一',[x]=2,'二','其余')",{'x':2}),'二')
        self.assertEqual(self.expression("Iif(IsNull([x])==True,'空',1/[x])",{'x':None}),'空')
        self.assertEqual(self.expression('Iif([x]=0,7,8)',{'x':None}),7)
        self.assertEqual(self.expression("Iif([x]='A' AND [y] IN ('FS','HX'),1,2)",{'x':'A','y':'FS'}),1)
        self.assertEqual(self.expression("Iif([x] IN ('SX'),1,2)",{'x':'S'}),2)

    def test_strings_tokens_bare_fields_and_quoted_literals(self):
        self.assertEqual(self.expression("'原[x] And=''x''' + [Name]",{'name':'甲'}),"原[x] And='x'甲")
        self.assertEqual(self.expression("Substring(EmpID,2,4)",{'empid':'01234567'}),'2345')
        self.assertEqual(self.expression("Len(IsNull([x],''))",{'x':None}),0)
        with self.assertRaises(ValueError):self.expression('Substring([x],-1,3)',{'x':'ABC'})

    def test_round_dates_and_unknown_functions(self):
        self.assertEqual(self.expression('Round([x],2)',{'x':Decimal('1.245')}),Decimal('1.24'))
        self.assertEqual(self.expression('Round([x],2)',{'x':Decimal('-1.255')}),Decimal('-1.26'))
        self.assertEqual(self.expression('Now()'),at(2))
        self.assertEqual(self.expression('AddDays([x],1)',{'x':at(2)}),at(3))
        self.assertEqual(self.expression('GetDate([x])',{'x':at(2)}).hour,0)
        with self.assertRaises(ValueError):self.expression('RunProcess([x])',{'x':'anything'})

    def test_original_dye_recipe_conditions_and_dependencies(self):
        from tools.development_archive.customer_boundary_20261024.backend.source_phase6_api import templates
        from plugins.erp_base.source_phase6_layouts import parse_xml
        from plugins.erp_base.source_phase6_calculated_print import apply
        root,_=parse_xml(base64.b64decode(templates()[43]['TemplateXml']))
        names=['RecipeUnit','StuffType','PhaseID','PhaseID_R','NeedQty','StuffKindID','WeightUnit_R']
        result=apply(root,{'columns':[{'name':n} for n in names],
            'rows':[[0,'A','02','旧阶段',Decimal('.05'),'FS','克'],[1,'S','02','旧阶段',Decimal('1.255'),'X','千克']]})
        rows=[dict(zip([c['name'] for c in result['columns']],r)) for r in result['rows']]
        self.assertEqual((rows[0]['Num'],rows[0]['PhaseID_Rnew'],rows[0]['NeedQtyNew'],rows[0]['WeightUnit_RNew']),(2,'助剂',10,'ML '))
        self.assertEqual(rows[1]['NeedQtyNew'],Decimal('1.26'))

    def test_original_r010_missing_fields_are_detected_despite_star_projection(self):
        from tools.development_archive.customer_boundary_20261024.backend.source_phase6_api import templates
        from plugins.erp_base.source_phase6_rendering import requirements
        issues=requirements(templates()[149])
        self.assertIn('当前原查询未提供计算来源：KKind',issues)
        self.assertIn('当前原查询未提供版式字段：ProdInList.grayQty',issues)

    def test_bare_calculation_dependency_and_unused_literal_reference(self):
        from plugins.erp_base.source_phase6_layouts import parse_xml
        from plugins.erp_base.source_phase6_calculated_print import apply
        from plugins.erp_base.source_phase6_print_rules import calculation_usage
        root,_=parse_xml(b'''<Report DataMember="E"><CalculatedFields><B Name="base" Expression="[qty]*2"/><A Name="total" Expression="base+1"/><U Name="unused" Expression="'[total]'"/></CalculatedFields><DataBindings><B DataMember="E.total"/></DataBindings></Report>''')
        self.assertEqual(calculation_usage(root),{'active':['base','total'],'unreferenced':['unused']})
        result=apply(root,{'columns':[{'name':'qty'}],'rows':[[3],[3],[None]]})
        self.assertEqual(result['rows'],[[3,6,7],[3,6,7],[None,None,None]])
