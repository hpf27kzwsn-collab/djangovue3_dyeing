"""丢失视图的非空取数、明确采购转单、生产日及连续分组原打印。"""
from datetime import datetime
from decimal import Decimal
from django.test import TestCase,SimpleTestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from .test_phase_report_audit import create
from .test_source_phase6 import reader
from .test_source_phase6_stock_print import dictionaries
from plugins.erp_base.source_phase6_entries import run
from plugins.erp_base.source_phase3_operations import model
from plugins.erp_base.source_phase6_transfers import purchase_to_product
from plugins.erp_base.source_context import SourceDocumentContext


class LocalChainsTests(TestCase):
    def setUp(self):
        self.actor=get_user_model().objects.create(username='p6-local',is_superuser=True)
        self.client=APIClient();self.client.force_authenticate(self.actor)

    def test_out_query_keeps_orphan_and_duplicate_headers_and_two_roll_fields(self):
        for _ in range(2):create('ProdOut',SheetSeries='O',SheetNo='OUT')
        create('ProdOutDetail',SheetSeries='O',DetailNo='D',OutRolls=99,Rolls=-2,WeightQty=None,InSheetNo='IN')
        create('ProdOutDetail',SheetSeries='ORPHAN',DetailNo='D',Rolls=3)
        result=run('vwProdOutDataByCheckNo',{},reader,True)
        rows=dictionaries(result);self.assertEqual(len(rows),3)
        self.assertEqual(sum(r['sheetno'] is None for r in rows),1)
        linked=[r for r in rows if r['sheetno']=='OUT']
        self.assertEqual([(r['outrolls'],r['rolls'],r['recesheetno']) for r in linked],[(99,-2,'IN')]*2)
        self.assertIsNotNone(result['reconstruction'])

    def test_full_receipts_issues_preserve_orphans_and_duplicate_sources_without_double_subtraction(self):
        for _ in range(2):create('ProdIn',SheetNo='IN',Rolls=10,WeightQty=20,LengthQty=30)
        for _ in range(2):create('ProdOut',SheetSeries='O')
        for _ in range(2):create('ProdOutDetail',SheetSeries='O',InSheetNo='IN',Rolls=2,OutRolls=100,WeightQty=3,LengthQty=4)
        create('ProdOutDetail',SheetSeries='ORPHAN',InSheetNo='NO-IN',Rolls=1)
        create('ProdIn',SheetNo='NO-OUT',Rolls=-1,WeightQty=None)
        create('ProdIn',SheetNo='NULL-OUT',Rolls=8)
        create('ProdOutDetail',InSheetNo='NULL-OUT',Rolls=None)
        rows=dictionaries(run('vwProdInAndOutDetailQuery',{},reader,True))
        self.assertEqual(len(rows),11)
        self.assertEqual([(r['remainrolls'],r['remainweightqty']) for r in rows if r['sheetno']=='IN'],[(6,14)]*8)
        self.assertEqual(next(r['remainrolls'] for r in rows if r['sheetno']=='NO-OUT'),-1)
        self.assertIsNone(next(r['remainrolls'] for r in rows if r['sheetno']=='NULL-OUT'))
        self.assertEqual(sum(r['sheetno'] is None for r in rows),1)

    def test_current_stock_keeps_fact_and_warehouse_dimensions_and_negative_zero(self):
        for wh in ['W1','W2']:
            for _ in range(2):create('ProdStockBook',BookNo=1,CustomerID='C',WareHouseID=wh,ProdID='P',FactID='F',
                InRolls=1,OutRolls=2,InWeightQty=0,OutWeightQty=3,InLengthQty=4,OutLengthQty=4)
        rows=dictionaries(run('vwProdCurrentStockQuery',{'QuantityBasis':'weight'},reader,True))
        self.assertEqual(len(rows),2);self.assertEqual([r['remainsqty'] for r in rows],[-6,-6])
        self.assertTrue(all(r['factid']=='F' and r['fabricid'] is None for r in rows))
        length=dictionaries(run('vwProdCurrentStockQuery',{'QuantityBasis':'length'},reader,True))
        self.assertEqual([r['remainsqty'] for r in length],[0,0])

    def test_machine_article_duplicate_lookup_and_orphan_remain(self):
        for _ in range(2):create('MachineFault',SheetSeries='M',MachineID='MC')
        for price in [1,2]:create('p_Article',ArticleID='A',LastPrice=price)
        create('MachineFaultArticleInfo',SheetSeries='M',ArticleID='A',Rounds=1,SerialNum=4,Qty=-2)
        create('MachineFaultArticleInfo',SheetSeries='NONE',ArticleID='NONE',Rounds=1,SerialNum=5,Qty=None)
        rows=dictionaries(run('qry_MachineArticle',{},reader,True))
        self.assertEqual(len(rows),5);self.assertEqual(sorted(r['lastprice'] for r in rows if r['articleid']=='A'),[1,1,2,2])
        self.assertEqual(sum(r['machineid'] is None for r in rows),1)


    def test_purchase_transfer_explicit_head_and_quantity_preserves_repeated_use(self):
        first=create('PurMain',SheetSeries='P',SupplierID='A',BusinessUnitID='A')
        second=create('PurMain',SheetSeries='P',SupplierID='B',BusinessUnitID='B')
        line=create('PurDetail',SheetSeries='P',DetailNo='D',FabricID='FAB',Qty=-3,Price=Decimal('1.2354'),Amount=-6,Rolls=4)
        for _ in range(2):
            head=purchase_to_product(line,second,'length',18,9,'W',None,None,self.actor)
            self.assertEqual(head.old_business_unit_id,'B');self.assertIsNone(head.old_customer_id)
            self.assertEqual(head.old_length_qty,-3);self.assertIsNone(head.old_weight_qty)
            self.assertEqual(head.old_price,Decimal('1.24'))
            c=SourceDocumentContext.objects.get(entity=head._meta.label,object_id=head.pk)
            self.assertEqual(c.effects['purchase_product_origin']['purchase']['id'],second.pk)
            self.assertEqual(Decimal(c.effects['purchase_product_origin']['line']['old_price']),Decimal('1.2354'))
        self.assertEqual(model('ProdIn').objects.count(),2)
        response=self.client.post('/api/system/erp_purchase_sourcedyepurdetail/'+str(line.pk)+'/phase6_purchase_to_product/',
            {'purchase':first.pk,'quantity_basis':'weight','sheet_kind':18,'stock_unit':2,
             'warehouse_id':'W','customer_id':'C','prod_id':'P'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(model('ProdIn').objects.count(),3)
        wrong=create('PurMain',SheetSeries='WRONG')
        with self.assertRaises(ValidationError):purchase_to_product(line,wrong,'length',18,9,'W',None,None,self.actor)
        self.assertEqual(model('ProdIn').objects.count(),3)


    def test_twenty_added_auto_entries_match_original_formula_and_manual_null_wins(self):
        from plugins.erp_base import source_services as services
        from plugins.erp_base.source_phase6_auto_values import AUTO_PRODUCTS,PRODUCT_ENTRIES
        from plugins.erp_base.source_entry_registry import ENTRY_RULES
        from django.apps import apps
        for index,entry in enumerate(sorted(AUTO_PRODUCTS.keys()-PRODUCT_ENTRIES)):
            with self.subTest(entry=entry):
                label=next(k for k,v in ENTRY_RULES.items() if entry in v);m=apps.get_model(label)
                data={'_entry':entry,'old_sheet_series':'AUTO'+str(index)}
                for target,left,right in AUTO_PRODUCTS[entry]:
                    self.assertEqual(ENTRY_RULES[label][entry]['formula_fields'][target]['expression'],f'[{left}]*[{right}]')
                    data[m.SOURCE_FIELDS[left]]=Decimal('-2');data[m.SOURCE_FIELDS[right]]=Decimal('3')
                row=services.write(m,data,actor=self.actor)
                for target,_,_ in AUTO_PRODUCTS[entry]:self.assertEqual(getattr(row,m.SOURCE_FIELDS[target]),-6)
                explicit={m.SOURCE_FIELDS[t]:None for t,_,_ in AUTO_PRODUCTS[entry]}
                row=services.write(m,explicit,row,actor=self.actor)
                for target,_,_ in AUTO_PRODUCTS[entry]:self.assertIsNone(getattr(row,m.SOURCE_FIELDS[target]))


class ContinuousPrintTests(SimpleTestCase):
    def proof(self,rows):
        from tools.development_archive.customer_boundary_20261024.backend.source_phase6_api import templates
        from plugins.erp_base.source_phase6_rendering import render
        return render(templates()[221],{'entry':'h_Employeelit','columns':[{'name':n} for n in ['DeptID_R','EmpID','Name','EmpKind_R']],
            'rows':[[dept,str(i),'同名员工','原代码：1'] for i,dept in enumerate(rows)]})

    def test_original_employee_whole_group_moves_and_small_groups_share_page(self):
        small=self.proof(['甲']*2+['乙']*2)
        self.assertEqual(small['page_count'],1);self.assertEqual(small['record_count'],4)
        large=self.proof(['甲']*25+['乙']*25)
        self.assertEqual(large['page_count'],2);self.assertEqual(large['html'].count('>同名员工</div>'),50)

    def test_original_employee_oversize_group_splits_and_repeats_header(self):
        result=self.proof(['甲']*70)
        self.assertEqual(result['page_count'],2);self.assertEqual(result['record_count'],70)
        self.assertEqual(result['html'].count('>同名员工</div>'),70)
