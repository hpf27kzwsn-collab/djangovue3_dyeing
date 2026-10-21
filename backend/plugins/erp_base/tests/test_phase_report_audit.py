"""用明确期望的非空来源核验原报表；重复连接、负数和原筛选分别断言。"""
from datetime import datetime
from decimal import Decimal
from django.apps import apps
from django.test import TestCase
from django.utils import timezone
from plugins.erp_base.source_phase2_reports import report
from plugins.erp_base.source_foundation_view_reports import report as foundation_report


def create(table, **values):
    model = next(m for m in apps.get_models() if getattr(m, 'SOURCE_TABLE', None)==table)
    return model.objects.create(**{model.SOURCE_FIELDS[k]:v for k,v in values.items()})


def at(day=2, hour=0):
    return timezone.make_aware(datetime(2026,1,day,hour))


class PhaseReportAuditTests(TestCase):
    def test_inline_color_extractors_match_original_byte_vectors_and_correlated_columns(self):
        import json
        from pathlib import Path
        from sqlglot import exp
        from plugins.erp_base.source_static_lookup import execute
        from plugins.erp_base.source_quality_reports import rows
        from plugins.erp_base.source_foundation_functions import extract_number
        vectors=json.loads(Path(__file__).with_name('foundation_number_extractor_results.json').read_text(encoding='utf-8-sig'))
        for probe in vectors:
            with self.subTest(probe=probe):
                sql='SELECT dye.'+probe['name']+'('+exp.convert(probe['input']).sql(dialect='tsql')+') AS value'
                self.assertEqual(execute(sql,rows)[0]['value'],probe['result'])
        for value in [None,'','中'*49+'１','１２３４５６７８９０１２','😀'*47+'12','A①②3']:
            create('OrderColor',ColorNum=value)
        for name,width in [('F_Get_No',10),('Fn_Get_No',20)]:
            result=execute('SELECT ColorNum, dye.'+name+'(ColorNum) AS value FROM dye.OrderColor',rows)
            self.assertEqual(len(result),6)
            for row in result:self.assertEqual(row['value'],extract_number(row['colornum'],width))

    def order(self, quantity=-10, prepare=0):
        head=create('OrderMain', SheetSeries='O', SheetNo='ON', SheetDate=at(), SheetKind=1,
            SheetStatus=0, RightStatus=10, CustomerID='039', AssignUnit=0)
        line=create('OrderColor', SheetSeries='O', CheckNo='C', ProdID='P', OrderQty=quantity,
            OrderRolls=3, CardQty=2, ColorNum='R123', PrepareVats=prepare, WeightDn=-2, WeightUp=3)
        return head,line

    def test_order_projection_repairs_keep_duplicates_nulls_and_negative_quantities(self):
        head,line=self.order()
        create('OrderColor',SheetSeries='O',CheckNo='C',ProdID='P',OrderQty=-10)
        for name in ['vw_OrderColor','vw_OrderQuery','vwOrderInfo','vwOrder','vw_Newview','vwOrderToJob','vwOrderGrayPreemption']:
            with self.subTest(name=name):
                data=report(name,{})['rows']
                if name=='vwOrderGrayPreemption':
                    self.assertEqual(len(data),1)
                    self.assertEqual(data[0]['orderpreeqty'],-20)
                else:
                    self.assertEqual(len(data),2)
                if name=='vwOrder':
                    self.assertTrue(all(r['orderup'] is None and r['orderdn'] is None for r in data))
                elif name=='vw_Newview':
                    self.assertTrue(all(r['chayishu']==-10 for r in data))
                elif name=='vwOrderToJob':
                    self.assertTrue(all(r['lastqty']==-10 for r in data))
        self.assertEqual(len(report('vwNoOrderSettleData',{})['rows']),1)
        head.old_sheet_status=10;head.save()
        self.assertEqual(report('vwNoOrderSettleData',{})['rows'],[])

    def test_preparation_and_plan_variants_use_distinct_quantities(self):
        head,line=self.order(quantity=20)
        create('PlanDetail',SequenceNo=1,OrderSheetNo='ON',CheckNo='C',Qty=7,Rolls=2,Vats=1)
        create('PlanDetail',SequenceNo=2,OrderSheetNo='ON',CheckNo='C',Qty=-2,Rolls=0,Vats=0)
        create('Quote',SheetSeries='Q',RightStatus=10)
        create('QuoteDetail',SheetSeries='Q',ColorNum='B123',Width=0,Weight=0,PriceUnit=0)
        self.assertEqual(report('vwPreTransOrderColor',{})['rows'][0]['lastqty'],20)
        self.assertEqual(report('vwPreTransOrderColor_New',{})['rows'][0]['lastqty'],20)
        self.assertEqual(report('vwPreTransOrderColorByPlan',{})['rows'][0]['lastqty'],5)
        self.assertEqual(report('vwPreTransOrderColorPrepare',{})['rows'],[])
        line.old_prepare_vats=1;line.save()
        self.assertEqual(report('vwPreTransOrderColorByPlan',{})['rows'],[])
        self.assertEqual(report('vwPreTransOrderColorPrepare',{})['rows'][0]['lastqty'],20)
        self.assertEqual(report('vwPreTransOrderColorPrepareByPlan',{})['rows'][0]['lastqty'],5)

    def test_occupancy_deducts_actual_issues_and_preserves_negative_balance(self):
        self.order()
        for _ in range(2):create('OrderAssign',AssignNo=1,CheckNo='C',ReceSheetNo='R',Packs=1,Rolls=2,WeightQty=-3,LengthQty=4)
        create('GrayOutDetail',CheckNo='C',ReceSheetNo='R',Packs=1,Rolls=1,WeightQty=2,LengthQty=3)
        data=report('vwGrayOrderOccupy',{})['rows']
        self.assertEqual(len(data),1)
        self.assertEqual((data[0]['occpacks'],data[0]['occrolls'],data[0]['occweightqty'],data[0]['occlengthqty']),(1,3,-8,5))

    def test_job_order_allocation_zero_denominator_and_delivery_status(self):
        create('JobSheet',SheetSeries='J',SheetNo='JN',JobSheetType=0,SumAssignedWeightQty=12)
        first=create('JobCombineOrder',SheetSeries='J',CheckNo='C',CombineQty=1)
        second=create('JobCombineOrder',SheetSeries='J',CheckNo='D',CombineQty=-1)
        data=report('Order_Jobsheet',{})['rows']
        self.assertEqual(len(data),2)
        self.assertTrue(all(r['semiorderweightqty'] is None for r in data))
        second.old_combine_qty=2;second.save()
        create('ProdIn',JobSheetNo='JN',SheetKind=11)
        data=report('Order_Jobsheet',{})['rows']
        self.assertEqual(sorted(r['semiorderweightqty'] for r in data),[4,8])
        self.assertTrue(all(r['currstatus']=='成品入库' for r in data))
        create('ProdIn',JobSheetNo='JN',SheetKind=16)
        self.assertTrue(all(r['currstatus']=='退车间回修' for r in report('Order_Jobsheet',{})['rows']))
        create('ProdLoading',SheetSeries='L',RightStatus=10)
        create('ProdLoadingDetail',SheetSeries='L',JobSheetNo='JN')
        self.assertTrue(all(r['currstatus']=='已出货' for r in report('Order_Jobsheet',{})['rows']))
        create('JobSheetReceive',SheetSeries='RC',JobSheetNo='JN',WeightQty=-2)
        self.assertEqual([r['weightqty'] for r in report('Order_Jobsheet_Detail',{})['rows']],[-2,-2])

    def test_sample_view_filters_and_quote_approval_date_are_explicit(self):
        for _ in range(2):create('DyeDipsRecord',SheetSeries='S',SheetDate=at(),Times=2,EmpID='E',CheckerID='K',ColorVersion='A',Num=-1)
        create('DyeDipsRecord',SheetSeries='OLD',SheetDate=timezone.make_aware(datetime(2020,1,1)),Times=2)
        for name in ['DyeDipsRecordBulkCheckerID','DyeDipsRecordCheckerID','vw_DyeDipsRecord_EmpID']:
            self.assertEqual(len(report(name,{})['rows']),2,name)
        create('Quote',SheetSeries='Q',ApproveDate=at())
        for _ in range(2):create('QuoteDetail',SheetSeries='Q',Price=-3,ApproveDate=at(3),Width=0,Weight=0,PriceUnit=0)
        result=report('vwDyeDipsRecord',{})['rows']
        self.assertEqual(len(result),2)
        self.assertTrue(all(r['price']==-3 and str(r['approvedate']).startswith('2026-01-02') for r in result))

    def test_sample_receipts_issues_keep_dictionary_join_multiplicity(self):
        for _ in range(2):create('p_Fabric',FabricID='F',Spec='原规格')
        for table in ['SampleIn','SampleOut']:
            create(table,SheetSeries='S',SheetDate=at())
            create(table+'Detail',SheetSeries='S',DetailNo='D',FabricID='F',Qty=-3,Price=None)
            result=report('vw'+table+'Query',{})['rows']
            self.assertEqual(len(result),2)
            self.assertTrue(all(r['qty']==-3 and r['price'] is None for r in result))

    def test_customer_progress_variants_keep_negative_order_and_issue_totals(self):
        self.order()
        for _ in range(2):create('ProdOutDetail',CheckNo='C',NetKg=-2)
        parameters={'startdate':at(1),'enddate':at(3)}
        for name in ['sp_Order_ToCustomer','sp_Order_ToCustomer1','sp_Order_ToCustomer2']:
            data=report(name,parameters)['rows']
            self.assertEqual(len(data),1,name)
            self.assertEqual(data[0]['prodoutqty'],-4,name)
            if name!='sp_Order_ToCustomer':self.assertEqual(data[0]['chorderqty'],-6,name)

    def test_attendance_makeup_uses_original_seven_and_nine_hour_day_boundaries(self):
        for kind in [5,6]:
            for _ in range(2):create('h_Leave',SheetKind=kind,EmpID='E',BeginDate=at(2,8))
        incoming=foundation_report('v_KQ_InRecord')['rows']
        outgoing=foundation_report('v_KQ_OutRecord')['rows']
        self.assertEqual(len(incoming),2);self.assertEqual(len(outgoing),2)
        self.assertTrue(all(r['checkdate']=='2026-01-02' for r in incoming))
        self.assertTrue(all(r['checkdate']=='2026-01-01' for r in outgoing))

    def test_original_gray_union_and_product_mapping_keep_duplicate_matches(self):
        create('p_Gray',GrayID='G',NameC='坯料')
        create('p_Fabric_Cust',FabricID='G',CustFabricName='坯料',Kind='G')
        for _ in range(2):create('p_Product',ProdID='PG')
        self.assertEqual(len(foundation_report('A_GrayID')['rows']),2)
        self.assertEqual(len(foundation_report('V_GrayToProduct')['rows']),2)

    def test_cook_source_subtotals_include_negative_duplicate_lines(self):
        from plugins.erp_base.source_foundation_app_reports import cook_query
        create('CookIn',SheetSeries='C',SheetDate=at(),BuyerID='E')
        create('p_FieldValid',FieldType='Cook',Code='K',Name='厨房材料')
        for _ in range(2):create('CookInDetail',SheetSeries='C',ArticleKindID='K',Total=-3)
        data=cook_query(at(1),at(3))['rows']
        self.assertEqual(len(data),4)
        self.assertEqual(next(r for r in data if r['uindex']==0)['SumARMoney'],-6)
        self.assertEqual(next(r for r in data if r['uindex']==3)['Total'],-6)

    def test_order_page_variants_apply_customer_scope_and_keep_negative_totals(self):
        self.order()
        create('OrderAtte',SheetSeries='O',AtteValue='原要求')
        p=dict(current=1,size=1,startdate=at(1),enddate=at(3),confilter='',customerid='039',
            sheetseries='O',sheetno='',prodid='',empid='',bisaccept=False)
        for name in ['SP_APP_QueryOrderMain','Sp_AppOrderQuery','Sp_AppQueryOrderInfo']:
            data=report(name,p)
            self.assertEqual(data['pagination']['total'],1,name)
            if name=='Sp_AppOrderQuery':self.assertEqual(data['pagination']['SumOrderQty'],-10)
            if name=='Sp_AppQueryOrderInfo':self.assertEqual(data['result_sets'][0]['rows'][0]['attevalue'],'原要求')
        create('h_Employee',EmpID='E',IsCustomer=True,CustomerID='OTHER')
        self.assertEqual(report('SP_APP_QueryOrderMain',{**p,'empid':'E'})['rows'],[])

    def test_customer_quote_page_includes_all_match_children_not_only_current_page(self):
        create('FixedPrice',SheetSeries='F',CustomerID='C')
        for number in [1,2]:
            create('FixedPriceDetail',SheetSeries='F',DetailNo=str(number),Width=0,Weight=0,CusPrice=-number)
            create('FixedPriceAtte',DetailNo=str(number),AtteCode='X',AtteValue='原加工要求')
        create('QuoteItemPrice',SheetSeries='F',Item='X',Price=2)
        create('FixedCanDetail',SheetSeries='F',Price=-1)
        data=report('Sp_APPCustQueryQuotePrice',dict(current=1,size=1,customerid='C',fabrickind='',colordepthid=''))
        self.assertEqual(data['pagination']['total'],2);self.assertEqual(len(data['rows']),1)
        self.assertEqual([len(r['rows']) for r in data['result_sets']],[2,1,1])

    def test_urgent_order_status_uses_actual_shipped_rolls(self):
        create('JobSheet',SheetSeries='J',SheetNo='JN',SheetDate=at(),IsHurry=True,SumAssignedRolls=3)
        p=dict(current=1,size=10,startdate=at(1),enddate=at(3),confilter='')
        create('ProdIn',JobSheetNo='JN',SheetKind=11)
        self.assertEqual(report('SP_APP_UrgentOrderInfo',p)['rows'][0]['currstatus'],'成品入库')
        create('ProdOutDetail',JobSheetNo='JN',Rolls=1)
        self.assertIn('余2',report('SP_APP_UrgentOrderInfo',p)['rows'][0]['currstatus'])
        create('ProdOutDetail',JobSheetNo='JN',Rolls=2)
        self.assertEqual(report('SP_APP_UrgentOrderInfo',p)['rows'][0]['currstatus'],'已出货')

    def test_daily_report_separates_order_actual_weighing_issue_and_scheduling(self):
        self.order()
        create('JobSheet',SheetNo='J',JobSheetType=0)
        create('JobSheetRegister',JobSheetNo='J',SheetDate=at(),WeightQty=-7)
        create('RecordYield',JobSheetNo='J',PackTime=at(),NetKg=-2)
        create('ProdOut',SheetSeries='OUT',SheetDate=at())
        create('ProdOutDetail',SheetSeries='OUT',CheckNo='C',NetKg=-3)
        create('GrayMaterial',SheetSeries='G',SheetDate=at())
        for _ in range(2):create('GrayMaterialDetail',Sheetseries='G',JobSheetNo='J',Qty=5)
        data=report('Sp_QueryDyeingOrder',{'startdate':at(),'enddate':at(3)})
        row=data['rows'][0]
        self.assertEqual((row['orderqty'],row['yarnweightqty'],row['orderweightqty'],row['netkg'],row['schedulingqty']),(-10,-7,-3,-2,10))
        self.assertEqual(row['unwindingqty'],12)
        self.assertEqual(data['supplemental_rows'][0]['NetKg'],-4)

    def test_unfinished_order_month_query_has_nonempty_negative_order_source(self):
        head,line=self.order()
        setattr(line,line.SOURCE_FIELDS['GWName'],'缸位');line.save()
        create('OrderColor',SheetSeries='O',CheckNo='D',GWName='缸位',OrderQty=-4)
        result=report('Sp_QueryNotEndOrder',{'startdate':at()})['rows']
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['bcordernum'],2)
        self.assertEqual(result[0]['notoutsumnum'],0)

    def test_dropper_recipe_views_keep_versions_duplicate_material_and_negative_dosage(self):
        create('CptLabRecipe',ID=1,bAddWater=False,strCode='A.1',lVersion=2,strName='原配方',dtModifyDate=at(),dwCostPerKg=-1)
        create('CptLabRecipeDetail',ID=1,bManualSel=False,strCode='A.1',lVersion=2,lDetSeq=1,strProdCode='D',dwRate=-3,dtModifyDate=at())
        for _ in range(2):create('p_Stuff',StuffID='D')
        head=report('vwCptLabRecipe',{})['rows'][0]
        self.assertEqual(head['sheetseries'],'A.1-2');self.assertEqual(head['cost'],-1)
        detail=report('vwCptLabRecipeDetail',{})['rows']
        self.assertEqual(len(detail),2);self.assertTrue(all(r['dosage']==-3 for r in detail))

    def test_gray_update_retains_duplicate_specs_but_obeys_original_key_update_rule(self):
        from django.core.exceptions import ValidationError
        from system.models import Users
        from plugins.erp_base.source_services import write
        actor=Users.objects.create_superuser(username='gray-audit',password='test')
        first=create('p_Gray',GrayID='A',NameC='重复规格')
        create('p_Gray',GrayID='B',NameC='重复规格')
        write(type(first),{'old_name_c':'重复规格'},first,actor)
        self.assertEqual(type(first).objects.count(),2)
        with self.assertRaises(ValidationError):write(type(first),{'old_gray_id':'A'},first,actor)

    def test_foundation_app_choices_keep_duplicate_people_posts_and_original_feel_choice(self):
        from plugins.erp_base.source_foundation_views import report as original
        from plugins.erp_base.source_foundation_scalars import feel_code,employee_names
        for _ in range(2):
            create('h_Employee',EmpID='E',Name='同名',Mobile=None)
            create('p_FieldValid',FieldType='Station',Code='P',Name='工位')
        create('s_DBComboValue',ComboID='MF_EmpG',KeyValue='G',DisplayIndex=2)
        self.assertEqual(len(original('sp_App_GetEmployeePhone',value='E')['rows']),2)
        self.assertEqual(len(original('sp_App_O_GetPostList')['rows']),2)
        self.assertEqual(original('sp_App_sysGetMFEmpGroup')['rows'][0]['KeyValue'],'G')
        self.assertEqual(employee_names('E',';'),'同名;同名')
        create('p_Product',ProdID='P')
        for code in ['F1','F2']:create('p_FeelCode',ProdID='P',FeelCode=code)
        self.assertEqual(feel_code('P'),'F1')

    def test_original_app_navigation_uses_employee_roles_and_original_distinct(self):
        from plugins.erp_base.source_foundation_views import report as original
        create('s_Functions',FuncNo='900001',RelaFuncNo='900002')
        create('s_Functions',FuncNo='900002',FullName='查询',AppURL='/query',IconName='icon')
        for _ in range(2):
            create('h_EmpRole',EmpID='E',RoleNo='R')
            create('s_Permission',RoleNo='R',FuncNo='900002')
        data=original('sp_App_GetAppChildFunctions',value='900001',employee='E')['rows']
        self.assertEqual([r['FuncNo'] for r in data],['900002','000000'])
        self.assertEqual(len(original('sp_App_GetAppChildFunctions',value='900001',employee='OTHER')['rows']),1)
        self.assertEqual(len(original('sp_App_GetAppChildFunctions',value='900001',employee='0000')['rows']),2)

    def test_customer_deadline_keeps_negative_days_and_duplicate_limit_join(self):
        from plugins.erp_base.source_foundation_views import report as original
        create('RequestLimit',CustomerID='C',DesigneeID='E',SheetDate=at())
        create('RequestLimit',CustomerID='C',DesigneeID='E',SheetDate=at(1))
        create('Limit',EmpID='E',Kind=1)
        for days in [-2,10]:create('KindLimit',Kind=1,DeliveryDay=days)
        data=original('MaxSavePlease',now=at())['rows']
        self.assertEqual(len(data),2)
        self.assertEqual(sorted(r['DeliveryDay'] for r in data),[-2,10])
        self.assertTrue(any(r['SavePleaseDate']<r['SheetDate'] for r in data))
