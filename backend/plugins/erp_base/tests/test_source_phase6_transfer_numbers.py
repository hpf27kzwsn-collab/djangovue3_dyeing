"""浏览器暴露的转单编号缺口：不跳过异常原号，显式编号可重复。"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .test_phase_report_audit import create,at
from plugins.erp_base.source_phase3_operations import model
from plugins.erp_base import source_services as services


class TransferNumberTests(TestCase):
    def setUp(self):
        self.actor=get_user_model().objects.create(username='transfer',is_superuser=True)
        self.client=APIClient();self.client.force_authenticate(self.actor)

    def post(self,line,action,data):
        return self.client.post('/api/system/'+line._meta.label_lower.replace('.','_')+'/'+str(line.pk)+'/'+action+'/',data,format='json')

    def head(self,table,**extra):
        return services.write(model(table),{'_entry':table,'old_sheet_series':'H','old_sheet_no':'H',**extra},actor=self.actor)

    def test_department_non_numeric_original_survives_and_duplicate_explicit_numbers_are_saved(self):
        # SeriesAndRowNo按所属父流水检查旧号，不用另一父单或无父码原行阻断全库取号。
        bad=create('PurDetail',SheetSeries='H',DetailNo='异常原号')
        for prefix in ['Article','Stuff']:
            head=self.head(prefix+'PurMain')
            application=create(prefix+'DeptApply',SheetSeries='A',SheetNo='A')
            line=create(prefix+'DeptApplyDetail',SheetSeries='A',DetailNo='A',Unit='箱',**{prefix+'ID':'A'})
            data={'application':application.pk,'head':head.pk,'quantity':-2,'price':3}
            result=self.post(line,'phase6_department_apply_to_purchase',data)
            self.assertEqual(result.status_code,400,result.data)
            for _ in range(2):
                result=self.post(line,'phase6_department_apply_to_purchase',{**data,'detail_no':'重复原号'})
                self.assertEqual(result.status_code,200,result.data)
        self.assertEqual(model('PurDetail').objects.filter(old_detail_no='重复原号',old_qty=-2,old_amount=-6).count(),4)
        self.assertTrue(model('PurDetail').objects.filter(pk=bad.pk,old_detail_no='异常原号').exists())

    def test_care_and_adjustment_explicit_numbers_reach_original_fields(self):
        care=create('MachineCarePlanDetail',ArticleID='A')
        article=create('p_Article',ArticleID='A',Unit='件')
        head=self.head('ArticleOut')
        result=self.post(care,'phase6_care_plan_to_article_out',{'head':head.pk,'article':article.pk,
            'quantity':-2,'price':3,'detail_no':'配件原号'})
        self.assertEqual(result.status_code,200,result.data)
        self.assertEqual(model('ArticleOutDetail').objects.get(old_detail_no='配件原号').old_out_qty,-2)
        quote=create('Quote',SheetSeries='Q',SheetNo='Q')
        line=create('QuoteDetail',SheetSeries='Q',DetailNo='QD',Width=1,Weight=1,PriceUnit=1,ColorNum='X123',Price=10)
        adjust=self.head('PriceAdjust',old_adjust_money=2,old_date_type=1,old_start_date=at(2))
        result=self.post(line,'phase6_quote_to_price_adjustment',{'quote':quote.pk,'head':adjust.pk,'detail_no':'调价原号'})
        self.assertEqual(result.status_code,200,result.data)
        self.assertEqual(model('PriceAdjustDetail').objects.get(old_detail_no='调价原号').old_adjust_price,12)

    def test_header_and_child_original_numbers_and_overlength_atomicity(self):
        quote=create('Quote',SheetSeries='Q',SheetNo='Q')
        line=create('QuoteDetail',SheetSeries='Q',DetailNo='QD',Width=1,Weight=1,PriceUnit=1,Price=10)
        data={'quote':quote.pk,'sheet_no':'订单原号','sheet_series':'订单流水','check_no':'订单明细','fabric_id':'F'}
        result=self.post(line,'phase6_quote_to_order',data)
        self.assertEqual(result.status_code,200,result.data)
        head=model('OrderMain').objects.get(old_sheet_no='订单原号')
        self.assertEqual(head.old_sheet_series,'订单流水')
        self.assertEqual(model('OrderColor').objects.get(source_parent_1=head).old_check_no,'订单明细')
        result=self.post(line,'phase6_quote_to_order',{**data,'check_no':'X'*1000})
        self.assertEqual(result.status_code,400,result.data)
        self.assertEqual(model('OrderMain').objects.count(),1)
        purchase=create('PurMain',SheetSeries='P',SheetNo='P')
        detail=create('PurDetail',SheetSeries='P',DetailNo='D',Qty=-4,Rolls=2)
        result=self.post(detail,'phase6_purchase_to_product',{'purchase':purchase.pk,'quantity_basis':'weight',
            'sheet_kind':18,'stock_unit':1,'warehouse_id':'W','customer_id':'C','prod_id':'P',
            'sheet_no':'入库原号','sheet_series':'入库流水'})
        self.assertEqual(result.status_code,200,result.data)
        head=model('ProdIn').objects.get(old_sheet_no='入库原号')
        self.assertEqual((head.old_sheet_series,head.old_weight_qty),('入库流水',-4))
