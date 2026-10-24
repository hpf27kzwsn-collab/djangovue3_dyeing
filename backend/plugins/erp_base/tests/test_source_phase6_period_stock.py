"""明确库存期间、采购候选、交期锁定、抄表计算与分组尾打印。"""
import base64
from decimal import Decimal
from django.test import TestCase, SimpleTestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .test_phase_report_audit import create, at
from .test_source_phase6 import reader
from .test_source_phase6_stock_print import dictionaries
from plugins.erp_base.source_phase6_entries import run
from plugins.erp_base.source_phase3_operations import model


class PeriodStockTests(TestCase):
    def test_selected_opening_and_nonoverlapping_periods_preserve_negative_and_duplicates(self):
        for _ in range(2):
            create('ProdStock',StockDate=at(1),CarryDate=at(1),CustomerID='C',WareHouseID='W',JobSheetNo='J',PreMonthRolls=3,PreMonthWeightQty=10,PreMonthLengthQty=100)
        create('ProdStock',StockDate=at(2),CarryDate=at(2),WareHouseID='W',JobSheetNo='J',PreMonthRolls=999,PreMonthWeightQty=999)
        for day,qty in [(1,2),(2,3),(3,-7),(4,99)]:
            create('ProdStockBook',BookNo=day,BookDate=at(day),CustomerID='C',WareHouseID='W',JobSheetNo='J',
                InRolls=qty,OutRolls=0,InWeightQty=qty,OutWeightQty=0,InLengthQty=qty*10,OutLengthQty=0)
        p={'StockDate':'2026-01-01','FromDate':'2026-01-02','UntilDate':'2026-01-04','QuantityBasis':'weight'}
        rows=dictionaries(run('vwProdStockTotal',p,reader,True))
        self.assertEqual(len(rows),1)
        row=rows[0]
        self.assertEqual((row['premonthqty'],row['thismonthinqty'],row['thismonthoutqty'],row['residualqty']),(22,-4,0,18))
        self.assertEqual(row['residualrolls'],4)
        self.assertIsNone(row['residualpacks']);self.assertIsNone(row['fabricid'])
        p['QuantityBasis']='length'
        self.assertEqual(dictionaries(run('vwProdStockTotal',p,reader,True))[0]['residualqty'],180)
        for _ in range(2):create('JobSheet',SheetNo='J')
        del p['FromDate']
        rows=dictionaries(run('vwProdStock',p,reader,True))
        self.assertEqual([r['paperqty'] for r in rows],[180,180])
        p['UntilDate']='2025-12-31'
        with self.assertRaises(ValidationError):run('vwProdStock',p,reader,True)

    def test_unknown_opening_location_is_not_spread_and_zero_balance_kept(self):
        create('ProdStock',StockDate=at(1),CarryDate=at(1),WareHouseID='W',PreMonthRolls=0,PreMonthWeightQty=0)
        create('ProdStockBook',BookNo=1,BookDate=at(2),WareHouseID='W',StorageUnitIDs='A',CheckNo='C',
            InRolls=0,OutRolls=1,InWeightQty=0,OutWeightQty=5)
        p={'StockDate':'2026-01-01','FromDate':'2026-01-02','UntilDate':'2026-01-03','QuantityBasis':'weight'}
        rows=dictionaries(run('vwProdStockTotal',p,reader,True));self.assertEqual(len(rows),2)
        self.assertEqual(sorted(r['residualqty'] for r in rows),[-5,0])
        self.assertIsNone(next(r['checkno'] for r in rows if r['storageunitids'] is None))

    def test_positive_stock_candidates_keep_duplicate_headers_and_original_qty_basis(self):
        for _ in range(2):create('ProdIn',SheetNo='I',StockUnit=7,FabricID='F')
        for _ in range(2):create('ProdStockBook',BookNo=1,SheetNo='I',InRolls=2,OutRolls=0,
            InWeightQty=3,OutWeightQty=0,InLengthQty=0,OutLengthQty=1)
        rows=dictionaries(run('ProdStockToOutPlanList',{'QuantityBasis':'weight'},reader,True))
        self.assertEqual([r['qty'] for r in rows],[6,6])
        self.assertEqual([r['stockunit'] for r in rows],[7,7])
        self.assertEqual(run('ProdStockToOutPlanList',{'QuantityBasis':'length'},reader,True)['count'],0)

    def test_purchase_candidates_do_not_hide_duplicate_or_previously_transferred_details(self):
        for _ in range(2):create('PurMain',SheetSeries='P',SheetNo='PN')
        for _ in range(2):create('PurDetail',SheetSeries='P',DetailNo='D',Qty=-2)
        create('ProdIn',SheetNo='OLD')
        rows=dictionaries(run('PurToProdIn',{},reader,True))
        self.assertEqual(len(rows),4);self.assertTrue(all(r['qty']==-2 and r['sheetseries']=='P' for r in rows))

    def test_delivery_apply_retains_original_null_arithmetic_and_duplicate_locks(self):
        for status,qty in [(0,3),(0,3),(2,-1),(1,99)]:
            create('OrderDlvApply',ApplyKindID='A',ApplyDlvDate=at(2),Status=status,LengthQty=qty,Rolls=1)
        for qty in [8,9]:create('OrderDlvApplyLock',ApplyKindID='A',ApplyDlvDate=at(2),Status=1,LengthQty=qty)
        create('OrderDlvApply',ApplyKindID='B',ApplyDlvDate=at(2),Status=2,LengthQty=4)
        rows=dictionaries(run('qry_OrderDlvApply',{},reader,True))
        self.assertEqual(len(rows),3)
        a=[r for r in rows if r['applykindid']=='A']
        self.assertEqual([r['sumlength'] for r in a],[5,5]);self.assertEqual([r['sumlengapprove'] for r in a],[-1,-1])
        self.assertEqual(sorted(r['maxplanlength'] for r in a),[8,9])
        b=next(r for r in rows if r['applykindid']=='B')
        self.assertIsNone(b['sumlengapprove']);self.assertIsNone(b['maxplanlength'])

    def test_energy_readings_compute_in_order_and_explicit_values_win(self):
        from plugins.erp_base import source_services as services
        actor=get_user_model().objects.create(username='p6-energy',is_superuser=True)
        m=model('EnergyConsumptionDetail')
        item=services.write(m,{'_entry':'EnergyConsumptionDetail','old_sheet_series':'E',
            'old_this_read_qty':5,'old_last_read_qty':8,'old_price':2},actor=actor)
        self.assertEqual((item.old_use_qty,item.old_amount),(-3,-6))
        item=services.write(m,{'old_this_read_qty':None},item,actor=actor)
        self.assertEqual((item.old_use_qty,item.old_amount),(-8,-16))
        item=services.write(m,{'old_this_read_qty':20,'old_use_qty':None},item,actor=actor)
        self.assertIsNone(item.old_use_qty);self.assertIsNone(item.old_amount)
        item=services.write(m,{'old_this_read_qty':30,'old_amount':Decimal('-99')},item,actor=actor)
        self.assertEqual((item.old_use_qty,item.old_amount),(22,-99))



class GroupFooterPrintTests(SimpleTestCase):
    def template(self,union='None',bottom='false',height='80'):
        xml=f'''<Report ControlType="XtraReport" DataMember="h_Employeelit" PageWidth="200" PageHeight="{height}" Dpi="100" Margins="0,0,0,0">
        <Bands><Header ControlType="GroupHeaderBand" HeightF="10" RepeatEveryPage="true"><GroupFields><F FieldName="DeptID" /></GroupFields></Header>
        <Detail ControlType="DetailBand" HeightF="20"><SortFields><F FieldName="EmpID" SortOrder="Descending"/></SortFields><Controls><Label ControlType="XRLabel" SizeF="100,20"><DataBindings><B PropertyName="Text" DataMember="h_Employeelit.EmpID"/></DataBindings></Label></Controls></Detail>
        <Footer ControlType="GroupFooterBand" HeightF="15" GroupUnion="{union}" PrintAtBottom="{bottom}"><Controls><Total ControlType="XRLabel" SizeF="100,15"><DataBindings><B PropertyName="Text" DataMember="h_Employeelit.Name"/></DataBindings><Summary Running="Group" Func="Sum" IgnoreNullValues="true"/></Total></Controls></Footer></Bands></Report>'''
        return {'RptID':'GROUP-TEST','RptTitle':'组尾测试','TemplateXml':base64.b64encode(xml.encode()).decode()}

    def proof(self,rows,**kwargs):
        from plugins.erp_base.source_phase6_rendering import render
        return render(self.template(**kwargs),{'entry':'h_Employeelit','columns':[{'name':n} for n in ['DeptID','EmpID','Name']], 'rows':rows})

    def test_group_sum_and_sort_keep_duplicate_negative_and_null_rows(self):
        result=self.proof([['A','ONE',5],['A','TWO',5],['A','TWO',None],['B','B',-9]])
        self.assertEqual(result['record_count'],4)
        self.assertEqual(result['html'].count('>10</div>'),1);self.assertEqual(result['html'].count('>-9</div>'),1)
        self.assertEqual(result['html'].count('>TWO</div>'),2)
        self.assertLess(result['html'].index('>TWO</div>'),result['html'].index('>ONE</div>'))

    def test_footer_alone_or_with_last_detail_and_bottom(self):
        rows=[['A','3',1],['A','2',1],['A','1',1]]
        alone=self.proof(rows);joined=self.proof(rows,union='WithLastDetail')
        first_alone=alone['html'].split('</section>')[0]
        first_joined=joined['html'].split('</section>')[0]
        self.assertIn('>1</div>',first_alone);self.assertNotIn('>1</div>',first_joined)
        self.assertEqual(alone['page_count'],2);self.assertEqual(joined['page_count'],2)
        self.assertIn('top:16.51mm',self.proof([['A','ROW',7]],bottom='true')['html'])

    def test_null_and_empty_group_keys_do_not_merge_and_oversize_footer_reports_error(self):
        result=self.proof([[None,'N',2],['','E',3]])
        self.assertEqual(result['html'].count('>2</div>'),1);self.assertEqual(result['html'].count('>3</div>'),1)
        with self.assertRaises(ValidationError):self.proof([['A','A',1]],height='20')

    def test_original_r132_remains_blocked_by_missing_sort_source(self):
        from tools.development_archive.customer_boundary_20261024.backend.source_phase6_api import templates
        from plugins.erp_base.source_phase6_rendering import requirements
        self.assertIn('当前原查询未提供排序/分组字段：GrayID',requirements(templates()[249]))
