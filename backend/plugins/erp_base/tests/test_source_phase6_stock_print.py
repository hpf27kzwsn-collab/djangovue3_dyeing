"""原数量维度明确替代、报价转单、八入口自动金额与报告汇总的非空验证。"""
from decimal import Decimal
from copy import deepcopy
from django.test import TestCase,SimpleTestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from .test_phase_report_audit import create
from .test_source_phase6 import reader
from plugins.erp_base.source_phase3_operations import model
from plugins.erp_base.source_phase6_entries import run
from plugins.erp_base.source_phase6_transfers import quote_to_order
from plugins.erp_base.source_context import SourceDocumentContext
from plugins.erp_base import source_services as services


def dictionaries(result):
    names=[r['name'].lower() for r in result['columns']]
    return [dict(zip(names,row)) for row in result['rows']]


class QuantityAndTransferTests(TestCase):
    def setUp(self):
        self.actor=get_user_model().objects.create(username='phase6-stock-print',is_superuser=True)
        self.client=APIClient();self.client.force_authenticate(self.actor)

    def test_product_stock_check_requires_explicit_dimension_keeps_duplicate_heads(self):
        for _ in range(2):create('ProdIn',SheetSeries='P',SheetNo='N',StockUnit=2)
        create('ProdStockBook',BookNo=1,SheetNo='N',BookKind=11,InRolls=5,OutRolls=0,InWeightQty=10,
               OutWeightQty=0,InLengthQty=100,OutLengthQty=0)
        create('ProdStockBook',BookNo=1,SheetNo='N',BookKind=21,InRolls=0,OutRolls=1,InWeightQty=0,
               OutWeightQty=3,InLengthQty=0,OutLengthQty=25)
        for basis,qty in [('weight',7),('length',75)]:
            rows=dictionaries(run('vwProdStockByCheck',{'QuantityBasis':basis},reader,load_records=True))
            self.assertEqual(len(rows),2)
            for row in rows:
                self.assertEqual(row['paperqty'],qty);self.assertEqual(row['realqty'],qty)
                self.assertEqual(row['paperrolls'],4);self.assertIsNone(row['prodkindid'])
        for value in [None,'','kg']:
            with self.assertRaises(ValidationError):run('vwProdStockByCheck',{'QuantityBasis':value},reader,load_records=True)

    def test_gray_check_preserves_original_union_filter_and_null_arithmetic(self):
        create('GrayIn',SheetSeries='G',SheetNo='GN')
        for _ in range(2):create('GrayInDetail',SheetSeries='G',ReceSheetNo='R',GrayID='Y')
        create('GrayStockBook',BookNo=1,ReceSheetNo='R',BookKind=11,InPacks=2,OutPacks=0,InRolls=3,OutRolls=0,
               InWeightQty=10,OutWeightQty=0,InLengthQty=20,OutLengthQty=0)
        create('GrayStockBook',BookNo=1,ReceSheetNo='R',BookKind=11,InPacks=0,OutPacks=0,InRolls=0,OutRolls=0,
               InWeightQty=99,OutWeightQty=1,InLengthQty=30,OutLengthQty=0)
        create('GrayStockBook',BookNo=1,ReceSheetNo='R',BookKind=21,InPacks=0,OutPacks=1,InRolls=0,OutRolls=1,
               InWeightQty=None,OutWeightQty=3,InLengthQty=0,OutLengthQty=4)
        weight=dictionaries(run('vwGrayStockByCheck',{'QuantityBasis':'weight'},reader,load_records=True))
        length=dictionaries(run('vwGrayStockByCheck',{'QuantityBasis':'length'},reader,load_records=True))
        self.assertEqual(len(weight),2);self.assertEqual(len(length),2)
        self.assertEqual(weight[0]['paperqty'],10)  # 原 NULL-3 不计入 SUM，不能擅自变成-3。
        self.assertEqual(length[0]['paperqty'],46)
        self.assertIsNone(weight[0]['fabricid']);self.assertEqual(weight[0]['paperpacks'],1)

    def test_product_stock_selection_keeps_positive_filter_and_duplicate_column_positions(self):
        for _ in range(2):create('ProdIn',SheetSeries='P',SheetNo='N')
        create('ProdStockBook',BookNo=1,SheetNo='N',InRolls=3,OutRolls=1,InWeightQty=2,
               OutWeightQty=4,InLengthQty=10,OutLengthQty=1)
        weight=run('ProdStockToProdOut',{'QuantityBasis':'weight'},reader,load_records=True)
        length=run('ProdStockToProdOut',{'QuantityBasis':'length'},reader,load_records=True)
        self.assertEqual(weight['count'],0);self.assertEqual(length['count'],2)
        self.assertEqual([c['name'].lower() for c in length['columns']].count('sheetno'),2)
        self.assertEqual(length['rows'][0][1],9)

    def test_quantity_http_export_preserves_duplicate_columns_and_requires_basis(self):
        import csv,io
        for _ in range(2):create('ProdIn',SheetSeries='P',SheetNo='N')
        create('ProdStockBook',BookNo=1,SheetNo='N',InRolls=3,OutRolls=1,
               InWeightQty=10,OutWeightQty=1)
        path='/api/system/erp_production_sourcedyejobsheet/'
        body={'entry':'ProdStockToProdOut','load_records':True,'parameters':{}}
        response=self.client.post(path+'phase6_query/',body,format='json')
        self.assertEqual(response.status_code,400,response.data)
        body['parameters']={'QuantityBasis':'weight'}
        response=self.client.post(path+'phase6_export/',body,format='json')
        self.assertEqual(response.status_code,200,response.content)
        rows=list(csv.reader(io.StringIO(response.content.decode('utf-8-sig'))))
        self.assertEqual(len(rows),3);self.assertEqual(rows[1],rows[2])
        self.assertEqual([v.lower() for v in rows[0]].count('sheetno'),2)

    def test_monthly_and_delivery_proof_from_nonempty_original_queries(self):
        create('p_FieldValid',FieldType='RecipeKind',Code='0',NumValue=1)
        create('h_Employee',EmpID='E',Name='原员工')
        for _ in range(2):create('DyeDipsRecord',EmpID='E',IsDoubleDye=0,ColorVersion='A',Num=-3)
        create('p_Customer',CustomerID='C',ShortName='原客户',NameC='原客户')
        for _ in range(2):create('OrderMain',SheetSeries='S',SheetNo='订单原号',CustomerID='C')
        create('OrderColor',SheetSeries='S',CheckNo='CK',OrderQty=-2)
        path='/api/system/erp_production_sourcedyejobsheet/phase6_template/'
        for index,count,text in [(155,1,'原员工')]:
            with self.subTest(index=index):
                response=self.client.post(path,{'index':index,'format':'Proof','load_records':True},format='json')
                self.assertEqual(response.status_code,200,response.data)
                data=response.data['data'];self.assertEqual(data['record_count'],count)
                self.assertIn(text,data['html'])
        response=self.client.post(path,{'index':276,'format':'Proof','load_records':True},format='json')
        self.assertEqual(response.status_code,400,response.data)
        self.assertIn('AssignUnit_R',str(response.data))

    def test_gray_current_stock_keeps_view_join_multiplicity_and_separate_gray_id(self):
        for _ in range(2):create('GrayIn',SheetSeries='G',SheetNo='GN')
        for _ in range(2):create('GrayInDetail',SheetSeries='G',ReceSheetNo='R',GrayID='Y')
        create('GrayStockBook',BookNo=1,ReceSheetNo='R',InPacks=2,OutPacks=0,InRolls=1,OutRolls=0,
               InWeightQty=10,OutWeightQty=0,InLengthQty=20,OutLengthQty=0)
        rows=dictionaries(run('GrayCurrentStockQuery',{'QuantityBasis':'weight'},reader,load_records=True))
        self.assertEqual(len(rows),1);self.assertEqual(rows[0]['saveqty'],160)
        self.assertEqual(rows[0]['grayid'],'Y');self.assertIsNone(rows[0]['fabricid'])
        self.assertIsNone(rows[0]['structure'])

    def test_quote_transfer_explicit_duplicate_head_source_and_all_snapshots(self):
        first=create('Quote',SheetSeries='Q',CustomerID='A',BusinessUnitID='BU',CurrencyID='RMB',ExchangeRate=1)
        second=create('Quote',SheetSeries='Q',CustomerID='B',BusinessUnitID='BU',CurrencyID='RMB',ExchangeRate=1)
        line=create('QuoteDetail',Width=0,Weight=0,SheetSeries='Q',DetailNo='D',ProdID='OWN-PRODUCT',Spec='原规格',
                    Price=-3,PriceUnit=2,Structure='原组织')
        for _ in range(2):
            order=quote_to_order(line,second,None,self.actor)
            self.assertEqual(order.old_customer_id,'B');self.assertEqual(order.old_price_unit,2)
            child=model('OrderColor').objects.get(source_parent_1=order)
            self.assertEqual(child.old_price,-3);self.assertIsNone(child.old_fabric_id)
            context=SourceDocumentContext.objects.get(entity=order._meta.label,object_id=order.pk)
            self.assertEqual(context.effects['quote_transfer_origin']['quote']['id'],second.pk)
            self.assertEqual(context.effects['quote_transfer_origin']['missing_target_fields']['OrderColor.Structure'],'原组织')
        self.assertEqual(model('OrderMain').objects.count(),2)
        self.assertEqual(model('Quote').objects.count(),2);first.refresh_from_db();self.assertEqual(first.old_customer_id,'A')

    def test_quote_wrong_header_atomic_and_http_explicit_fabric(self):
        quote=create('Quote',SheetSeries='Q',CustomerID='C');wrong=create('Quote',SheetSeries='OTHER')
        line=create('QuoteDetail',Width=0,Weight=0,PriceUnit=1,SheetSeries='Q',DetailNo='D',Price=2)
        with self.assertRaises(ValidationError):quote_to_order(line,wrong,'FAB',self.actor)
        self.assertEqual(model('OrderMain').objects.count(),0)
        response=self.client.post('/api/system/erp_sales_sourcedyequotedetail/'+str(line.pk)+'/phase6_quote_to_order/',
            {'quote':quote.pk,'fabric_id':'FAB'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(model('OrderColor').objects.get().old_fabric_id,'FAB')

    def test_all_eight_product_entry_formulas_match_original_and_preserve_explicit_values(self):
        from plugins.erp_base.source_phase6_auto_values import PRODUCT_ENTRIES
        from plugins.erp_base.source_entry_registry import ENTRY_RULES
        from django.apps import apps
        for entry in PRODUCT_ENTRIES:
            label=next(k for k,v in ENTRY_RULES.items() if entry in v)
            with self.subTest(entry=entry):
                self.assertEqual(ENTRY_RULES[label][entry]['formula_fields']['Amount']['expression'],'[Qty]*[Price]')
                item=services.write(apps.get_model(label),{'_entry':entry,'old_sheet_series':'S'+entry,
                    'old_qty':Decimal('-2'),'old_price':Decimal('3')},actor=self.actor)
                self.assertEqual(item.old_amount,Decimal('-6'))
                item=services.write(type(item),{'old_qty':Decimal('5'),'old_amount':Decimal('-99')},item,actor=self.actor)
                self.assertEqual(item.old_amount,Decimal('-99'))
                item=services.write(type(item),{'old_price':None},item,actor=self.actor)
                self.assertIsNone(item.old_amount)


class ReportSummaryTests(SimpleTestCase):
    def test_original_monthly_report_sums_duplicates_negative_and_null(self):
        from plugins.erp_base.source_phase6_api import templates
        from plugins.erp_base.source_phase6_rendering import render,requirements
        row=templates()[155];self.assertEqual(requirements(row),[])
        result={'entry':'qryDyeDipsRecord','columns':[{'name':n} for n in ['EmpID_R','DNum','WNum','TNum','MNum']],
                'rows':[['甲',7,None,-1,2],['甲',7,None,-1,2],['乙',1,3,None,0]]}
        output=render(row,result)
        self.assertEqual(output['record_count'],3)
        self.assertIn('>15</div>',output['html']);self.assertIn('>-2</div>',output['html'])
        self.assertEqual(output['html'].count('>甲</div>'),2)

    def test_summary_function_and_null_policy(self):
        from plugins.erp_base.source_phase6_print_rules import summarize
        self.assertEqual(summarize([2,2,None,-1],{'Func':'Sum','IgnoreNullValues':'true'}),3)
        self.assertEqual(summarize([2,2,None,-1],{'Func':'Count','IgnoreNullValues':'true'}),3)
        self.assertEqual(summarize([2,2,None,-1],{'Func':'Count'}),4)
        self.assertEqual(summarize([2,2,None,-1],{'Func':'Avg'}),Decimal('.75'))
        self.assertEqual(summarize([2,2,None,-1],{'Func':'Min'}),-1)
        self.assertEqual(summarize([2,2,None,-1],{'Func':'Max'}),2)
        self.assertEqual(summarize(['1.5',2],{'Func':'Sum','TreatStringsAsNumerics':'true'}),Decimal('3.5'))
        self.assertEqual(summarize(['1.5',2],{'Func':'Sum'}),Decimal('3.5'))
        self.assertEqual(summarize(['10','2'],{'Func':'Min','TreatStringsAsNumerics':'false'}),'10')
        with self.assertRaises(ValidationError):summarize(['原异常',1],{'Func':'Sum'})

    def test_unused_calculations_are_retained_but_not_required_for_order_delivery(self):
        from plugins.erp_base.source_phase6_api import templates
        from plugins.erp_base.source_phase6_layouts import parse_xml
        from plugins.erp_base.source_phase6_print_rules import calculation_usage
        from plugins.erp_base.source_phase6_rendering import render,requirements
        import base64
        row=templates()[276];before=deepcopy(row);root,_=parse_xml(base64.b64decode(row['TemplateXml']))
        self.assertEqual(calculation_usage(root),{'active':[],'unreferenced':['PKG','calculatedField3']})
        issues=requirements(row)
        self.assertFalse(any('CalculatedFields' in issue for issue in issues))
        self.assertTrue(any('AssignUnit_R' in issue for issue in issues))
        self.assertTrue(any('ReturnOutWeightQty' in issue for issue in issues))
        self.assertEqual(row,before)

    def test_calculated_dependency_and_optional_zero_format(self):
        from xml.etree.ElementTree import fromstring
        from plugins.erp_base.source_phase6_print_rules import calculation_usage
        from plugins.erp_base.source_phase6_rendering import formatted
        root=fromstring('<Report><DataBindings><Item DataMember="X.a"/></DataBindings><CalculatedFields><A Name="a" Expression="[b]+1"/><B Name="b" Expression="[c]+2"/><C Name="unused" Expression="1/0"/></CalculatedFields></Report>')
        self.assertEqual(calculation_usage(root),{'active':['a','b'],'unreferenced':['unused']})
        self.assertEqual(formatted(0,'{0:#####}'),'');self.assertEqual(formatted(0,'{0:0}'),'0')
