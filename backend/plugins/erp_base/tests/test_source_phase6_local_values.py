"""原入口保存联动：真实持久化、修改时机、重复及显式NULL。"""
from django.apps import apps
from django.test import TestCase
from django.contrib.auth import get_user_model
from plugins.erp_base import source_services as services
from plugins.erp_base.source_entry_registry import ENTRY_RULES
from .source_fixtures import historical_batch


class LocalEntryValuesTests(TestCase):
    def setUp(self):self.actor=get_user_model().objects.create(username='localtest',is_superuser=True)

    def save(self,entry,**fields):
        label=next(label for label,rules in ENTRY_RULES.items() if entry in rules)
        model=apps.get_model(label)
        return services.write(model,{'_entry':entry,**{model.SOURCE_FIELDS[k]:v for k,v in fields.items()}},actor=self.actor)

    def edit(self,item,**fields):
        return services.write(type(item),{item.SOURCE_FIELDS[k]:v for k,v in fields.items()},item,actor=self.actor)

    def test_customer_supplier_original_numbers_and_duplicates(self):
        for _ in range(2):
            customer=self.save('p_Customer',CustomerID='C1',ShortName='重复客户',CustKindID='0')
            self.assertEqual(customer.old_num,'KC1')
            supplier=self.save('p_Supplier',Num='SUP-A',ShortName='重复供方',CustKindID='1')
            self.assertEqual(supplier.old_customer_id,'SUP-A')
        self.assertEqual(type(customer).objects.count(),4)
        supplier=self.edit(supplier,Num='SUP-B')
        self.assertEqual(supplier.old_customer_id,'SUP-A') # 原GenerateTime=1采用仅新增时计算。
        explicit=self.save('p_Customer',CustomerID='C2',Num=None)
        self.assertIsNone(explicit.old_num)

    def test_stuff_creation_and_edit_timing_with_explicit_overrides(self):
        item=self.save('p_Stuff',StuffID='A',StuffType='A')
        self.assertEqual((item.old_recipe_unit,item.old_stock_unit,item.old_weight_unit),(1,'K','K'))
        item=self.edit(item,StuffType='B')
        self.assertEqual((item.old_recipe_unit,item.old_stock_unit,item.old_weight_unit),(0,'K','K'))
        other=self.save('p_Stuff',StuffID='A',StuffType='B',StockUnit=None,WeightUnit='X',RecipeUnit=-2)
        self.assertEqual((other.old_recipe_unit,other.old_stock_unit,other.old_weight_unit),(-2,None,'X'))
        self.assertEqual(type(item).objects.filter(old_stuff_id='A').count(),2)

    def test_lab_color_dependency_order_and_manual_null(self):
        for entry in ['DyeLabColor','ShowDyeLabColor']:
            item=self.save(entry,SheetSeries='L',ColorNo=entry,OrderNum='AB123',ColorMarkt='M',ColorAfter='Z')
            self.assertEqual((item.old_color_num,item.old_ori_color_no,item.old_markt,item.old_khshorptsh),('M123Z','M123Z','123','M'))
            item=self.edit(item,ColorNumInput='显式色号',CustColorNum='客户色号')
            self.assertEqual((item.old_color_num,item.old_ori_color_no,item.old_khshorptsh),('显式色号','显式色号','客户色号'))
            item=self.edit(item,ColorNumInput='另一个',ColorNum=None)
            self.assertIsNone(item.old_color_num);self.assertIsNone(item.old_ori_color_no)
            item=self.edit(item,OrderNum=None,ColorNumInput=None,ColorMarkt=None,ColorAfter=None)
            self.assertEqual(item.old_color_num,'');self.assertIsNone(item.old_markt)

    def test_rgb_retains_out_of_range_numbers_and_null_formula(self):
        for entry in ['p_ColorNum','p_ColorNumSup']:
            item=self.save(entry,SheetSeries=entry,ColorNo='DUP',R=-1,G=256,B=None)
            self.assertEqual(item.old_rgb,(-1-255)*65536+(256-255)*256-256)
            item=self.edit(item,R=255,G=255,B=255)
            self.assertEqual(item.old_rgb,-1)
            item=self.edit(item,R=-9,RGB=None);self.assertIsNone(item.old_rgb)

    def test_quote_headers_detail_costs_and_nulls(self):
        for entry in ['Quote','FixedPrice']:
            item=self.save(entry,SheetSeries=entry,SheetNo=entry,CustomerID='C')
            self.assertEqual(item.old_customer_code,'C')
            item=self.edit(item,CustomerID=None);self.assertIsNone(item.old_customer_code)
        item=self.save('QuoteDetail',DetailNo='QD',Width=1,Weight=1,Price=-2,ProcessPrice=3,ChengBen0=-4,ChengBen5=1)
        self.assertEqual((item.old_is_confirmed,item.old_pricesum,item.old_sum_cheng_ben),(1,1,-3))
        item=self.edit(item,Price=4,ChengBen1=2)
        self.assertEqual((item.old_is_confirmed,item.old_pricesum,item.old_sum_cheng_ben),(2,7,-1))
        item=self.edit(item,Price=None,Pricesum=None)
        self.assertIsNone(item.old_pricesum);self.assertEqual(item.old_is_confirmed,1)

    def test_four_order_variants_keep_negative_and_explicit_null(self):
        for entry in ['OrderColor','OrderColorChange','OrderColorSup','PrintOrderColor']:
            item=self.save(entry,SheetSeries=entry,CheckNo=entry,GrayQty=-3)
            self.assertEqual(item.old_order_qty,-3)
            item=self.edit(item,GrayQty=6);self.assertEqual(item.old_order_qty,6)
            item=self.edit(item,GrayQty=7,OrderQty=None);self.assertIsNone(item.old_order_qty)

    def test_historical_rows_are_not_recalculated(self):
        model=apps.get_model('erp_base.SourceDyePStuff')
        item=model.objects.create(old_stuff_id='H',old_stuff_type='A',old_recipe_unit=-7,source_batch=historical_batch(),source_row=1)
        from plugins.erp_base.source_phase6_local_values import before_save
        before_save(item,{'old_stuff_type':'B'},'p_Stuff',False)
        self.assertEqual(item.old_recipe_unit,-7)
        from plugins.erp_base.source_phase6_local_values import prepare_numbers
        supplier=apps.get_model('erp_base.SourceDyePCustomer')(old_customer_id=None,old_num='H-SUP',source_batch=historical_batch(),source_row=2)
        data={'old_num':'H-SUP'}
        prepare_numbers(supplier,data,'p_Supplier')
        self.assertIsNone(supplier.old_customer_id)
        self.assertEqual(data,{'old_num':'H-SUP'})
