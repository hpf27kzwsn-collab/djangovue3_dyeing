"""第三阶段原查询及采购库存办理的执行和结果验证。"""
from datetime import datetime
from decimal import Decimal
from django.test import TestCase
from django.db import transaction
from django.utils import timezone
from .test_phase_report_audit import create,at
from plugins.erp_base.source_phase3_reports import report,QUERIES


class Phase3QueryTests(TestCase):
    def test_all_registered_queries_execute_on_original_schema(self):
        for name in QUERIES:
            with self.subTest(name=name),transaction.atomic():
                result=report(name,{'startdate':at(),'enddate':at(3),'dtinputdate':at(3),'dtinputenddate':at(),'size':20})
                self.assertIn('rows',result)

    def test_supplier_current_and_previous_prices_keep_all_duplicate_receipts(self):
        for day,price in [(2,4),(3,5),(3,-1)]:
            create('StuffIn',SheetSeries=str(day)+str(price),SheetNo=str(price),SheetKind=13,SheetDate=at(day),SupplierID='S')
            create('StuffInDetail',SheetSeries=str(day)+str(price),DetailNo='D',StuffID='A',Price=price)
        latest=report('Sp_AppQuerySupplierPrice',{'size':20})['rows']
        previous=report('Sp_AppQuerySupplierOriPrice',{'size':20})['rows']
        self.assertEqual(len(latest),1);self.assertEqual(len(previous),2)
        self.assertEqual(sorted(r['price'] for r in latest+previous),[-1,4,5])

    def test_purchase_view_preserves_negative_returns_and_duplicate_joins(self):
        for weight in [5,-8]:
            create('GrayIn',SheetSeries='G',SheetKind=18)
            create('GrayInDetail',SheetSeries='G',ReceSheetNo='R',PurDetailNo='P',WeightQty=weight)
        result=report('A_PurDetailNo',{})['rows']
        self.assertEqual(len(result),1)
        self.assertIn(-6,list(result[0].values()))

    def test_moving_price_uses_carry_and_signed_current_receipts(self):
        create('ArticleStock',StockDate=at(),CarryDate=at(),WareHouseID='W',ArticleID='A',PreMonthQty=10,PreMonthMoney=20)
        create('ArticleStockBook',BookNo=1,BookDate=at(3),WareHouseID='W',ArticleID='A',BookKind=13,InQty=5,InMoney=20)
        create('ArticleStockBook',BookNo=2,BookDate=at(3),WareHouseID='W',ArticleID='A',BookKind=16,InQty=-2,InMoney=-8)
        result=report('fn_ArticlePriceMovingAverage',{'articlecode':'A','warehouseid':'W','dtinputdate':at(3)})['rows'][0]
        self.assertEqual(result['qty'],13);self.assertEqual(result['money'],32)
        self.assertEqual(result['result'],Decimal('2.461538'))

    def test_product_stock_does_not_drop_negative_or_empty_original_groups(self):
        create('ProdStockBook',BookNo=1,JobSheetNo='J',ProdID='P',CustomerID='C',InRolls=1,OutRolls=3,InWeightQty=4,OutWeightQty=9)
        create('ProdStockBook',BookNo=2,JobSheetNo='J',ProdID='P',CustomerID='C',InRolls=1,OutRolls=3,InWeightQty=4,OutWeightQty=9)
        data=report('Sp_AppQueryProdStock',{'size':1})
        self.assertEqual(data['rows'][0]['weightqty'],-10)
        self.assertEqual(data['pagination']['sumrolls'],-4)


class Phase3OperationTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.actor=get_user_model().objects.create(username='phase3',name='第三阶段')

    def test_fixed_mutation_projections_resolve_latest_schema(self):
        from plugins.erp_base.source_phase3_operations import SPECS,query,staging_sql
        from plugins.erp_base.source_phase3_posting import SPECS as POSTS
        from sqlglot import parse_one,exp
        definitions=[(d,{**s['temps'],**({'t':staging_sql([])} if n=='235' else {})}) for n,s in SPECS.items() if n in ['235','238','302','303','304','338','394','299','372','92'] for d in s['inserts']]
        definitions.extend((d,{}) for name,specs in POSTS.items() if name!='GrayStockAllot' for d in specs)
        for index,(spec,temps) in enumerate(definitions):
            with self.subTest(index=index,table=spec['table']),transaction.atomic():
                text=spec['sql']+' '+' '.join(temps.values())
                import re
                parameters={p.lower():'none' for p in re.findall(r'@(\w+)',text)}
                parameters.update(sheetkind=30,sheetdate=at(),currdate=at())
                query(spec['sql'],parameters,temps)

    def test_gray_staging_keeps_duplicate_barcode_and_negative_weight(self):
        from plugins.erp_base.source_phase3_operations import staging,source
        values=[dict(SheetSeries='G',SheetDate=at(),RollNo='01',BarCode='DUP',
                CustomerID='C',GrayID='P',Rolls=1,WeightQty=weight,LengthQty=0,GUnit='1') for weight in [5,-2]]
        staging('235',self.actor,values)
        self.assertEqual(source('GrayInRecord').count(),2)
        self.assertEqual(source('GrayInDetail').get().old_weight_qty,3)
        self.assertEqual(source('GrayStockBook').get().old_in_weight_qty,3)

    def test_transfers_retain_previous_receipt_and_all_duplicate_detail_joins(self):
        from plugins.erp_base.source_phase3_operations import transfer,source,model
        create('GrayOut',SheetSeries='G',SheetKind=26,CustomerID='C',SheetDate=at())
        for weight in [5,-2]:create('GrayOutDetail',SheetSeries='G',ReceSheetNo='R',GrayID='P',WeightQty=weight)
        transfer('299','G',self.actor)
        self.assertEqual(source('SemiInDetail').count(),2)
        self.assertEqual(sorted(source('SemiStockBook').values_list('old_in_weight_qty',flat=True)),[-2,5])
        transfer('299','G',self.actor)
        self.assertEqual(model('SemiInDetail').objects.count(),4)
        self.assertEqual(source('SemiInDetail').count(),2)

    def test_product_record_remainders_and_duplicate_barcodes_are_recorded(self):
        from plugins.erp_base.source_phase3_operations import records,source
        create('ProdIn',SheetSeries='P',Rolls=3,SumAssignedLengthQty=10,GaryWeight=11)
        for code in ['A','B','C']:create('ProdInRecord',SheetSeries='P',BarCode=code,RollNo=code)
        records('302',{'sheetseries':'P'},self.actor)
        self.assertEqual(sum(source('ProdInRecord').values_list('old_length_qty',flat=True)),10)
        self.assertEqual(sum(source('ProdInRecord').values_list('old_gray_qty',flat=True)),11)

    def test_negative_carry_and_reverse_keep_original_rows(self):
        from plugins.erp_base.source_phase3_carry import carry
        from plugins.erp_base.source_phase3_operations import source,model
        create('GrayStockBook',BookNo=1,BookDate=at(2),WareHouseID='W',GrayID='G',OutWeightQty=5,OutRolls=1)
        carry('Sp_UpdateGrayStock',0,at(1),at(1),at(3),self.actor)
        self.assertEqual(source('GrayStock').count(),1)
        carry('Sp_UpdateGrayStock',1,at(3),at(1),at(3),self.actor)
        self.assertEqual(source('GrayStock').count(),0)
        self.assertEqual(model('GrayStock').objects.count(),1)

    def test_duplicate_materials_and_overdraw_are_retained_with_trigger_audit(self):
        from plugins.erp_base.source_phase3_operations import create as save,source
        save('p_Gray',{'GrayID':'G','NameC':'重复'},self.actor)
        save('p_Gray',{'GrayID':'G','NameC':'重复'},self.actor)
        create('ArticleInDetail',DetailNo='D',InQty=1)
        save('ArticleOutDetail',{'InDetailNo':'D','OutQty':9},self.actor)
        self.assertEqual(source('p_Gray').count(),2)
        self.assertEqual(source('ArticleOutDetail').get().old_out_qty,9)

    def test_auto_small_uses_real_or_need_and_preserves_negative_values(self):
        from plugins.erp_base.source_phase3_auto import stuff
        from plugins.erp_base.source_phase3_operations import source
        create('StuffWeight',SheetSeries='W',SheetNo='WN',JobSheetNo='J')
        create('StuffWeightPhase',SheetSeries='W',PhaseNo=1,PhaseID='P')
        create('p_Stuff',StuffID='S',WOF=2,Price=4)
        for number,actual in [(1,-2000),(2,0)]:
            create('StuffWeightDetail',SheetSeries='W',PhaseNo=1,StuffNo=number,StuffID='S',WeightUnit='G',NeedQty=4000,RealQty=actual)
        stuff('244','J',self.actor)
        self.assertEqual(sorted(source('StuffOutDetail').values_list('old_qty',flat=True)),[-1,2])
        stuff('244','J',self.actor)
        self.assertEqual(source('StuffOutDetail').count(),2)

    def test_reverse_transfer_rebuild_keeps_outgoing_and_links_original_receipt(self):
        from plugins.erp_base.source_phase3_operations import transfer,source,model
        head=create('GrayIn',SheetSeries='G',SheetKind=20,CustomerID='C',SheetDate=at())
        create('GrayInDetail',SheetSeries='G',ReceSheetNo='G-01',TrunReceSheetNo='S-01',GrayID='P',WeightQty=-3,Rolls=2)
        transfer('338','G',self.actor)
        head.refresh_from_db();self.assertTrue(head.old_semi_out_sheet_no)
        self.assertEqual(source('SemiStockBook').get().old_out_weight_qty,-3)
        transfer('338','G',self.actor,2)
        self.assertEqual(model('SemiOutDetail').objects.count(),2)
        self.assertEqual(source('SemiOutDetail').count(),1)

    def test_area_merge_retains_duplicate_sources_and_xml_escapes(self):
        from plugins.erp_base.source_phase3_misc import positions
        from plugins.erp_base.source_phase3_operations import source,model
        create('GrayIn',SheetSeries='G',CustomerID='C')
        for area in ['B;A','A;&']:create('GrayInDetail',SheetSeries='G',GrayID='P',ReceSheetNo='R',Area=area)
        positions('98','G',self.actor)
        self.assertEqual(source('GrayPostionUp').get().old_new_area,'&amp;;A;B')
        positions('98','G',self.actor)
        self.assertEqual(source('GrayInDetail').count(),2)
        self.assertEqual(model('GrayPostionUp').objects.count(),2)

    def test_scan_reports_duplicate_barcode_quantities_without_dropping_negative_stock(self):
        create('GrayIn',SheetSeries='G',CustomerID='C')
        for weight in [4,-9]:create('GrayInDetail',SheetSeries='G',InputCode='B',GrayID='P',LotNo='L',WeightQty=weight,Rolls=1)
        create('JobSheet',SheetSeries='J',SheetNo='JN',JobSheetType=1)
        create('JobAssign',SheetSeries='J',AssignNo=1,GrayID='P',LotNo='L')
        value=report('Sp_GrayStockToJobOut',{'barcode':'B','jobsheetno':'JN'})
        self.assertEqual(value['rows'][0]['code'],0)
        self.assertEqual(value['rows'][0]['weightqty'],-5)
        self.assertEqual(len(value['result_sets'][0]['rows']),2)

    def test_all_carry_variants_execute_with_signed_current_stock(self):
        from plugins.erp_base.source_phase3_carry import SPECS,carry
        for name,spec in SPECS.items():
            with self.subTest(name=name),transaction.atomic():
                family=spec['table'].removesuffix('Stock')
                if family in ['Article','Stuff']:
                    create(family+'StockBook',BookNo=len(name),BookDate=at(2),WareHouseID='12' if name=='Sp_UpdateBigStuffStock' else '13',
                        **{family+'ID':'P'},InQty=1,OutQty=4,InMoney=2,OutMoney=8)
                else:
                    create(family+'StockBook',BookNo=len(name),BookDate=at(2),WareHouseID='W',**{('GrayID' if family=='Gray' else 'ProdID'):'P'},
                        InRolls=1,OutRolls=3,InWeightQty=2,OutWeightQty=8)
                value=carry(name,0,at(1),at(1),at(3),self.actor)
                self.assertGreater(len(value['rows']),0)

    def test_original_book_and_new_book_keep_negative_return_and_versioned_rows(self):
        from plugins.erp_base.source_phase3_old_stock import gray
        from plugins.erp_base.source_phase3_posting import post
        from plugins.erp_base.source_phase3_operations import source,model
        head=create('GrayIn',SheetSeries='G',SheetNo='GN',SheetKind=11,RightStatus=10,SheetDate=at())
        create('GrayInDetail',SheetSeries='G',ReceSheetNo='R',OriReceSheetNo='OLD',WeightQty=-5,Rolls=-1)
        gray('GrayIn','G',0,self.actor)
        self.assertEqual(source('GrayStockBook').get().old_in_weight_qty,-5)
        gray('GrayIn','G',2,self.actor)
        self.assertEqual(source('GrayStockBook').count(),0)
        head.old_sheet_kind=16;head.save()
        post('GrayIn','G',self.actor)
        self.assertEqual(source('GrayStockBook').get().old_rece_sheet_no,'OLD')
        self.assertEqual(model('GrayStockBook').objects.count(),2)

    def test_old_semi_preserves_original_unit_and_repeat_updates(self):
        from plugins.erp_base.source_phase3_old_stock import semi
        from plugins.erp_base.source_phase3_operations import source
        create('SemiIn',SheetSeries='S',StockUnit=2,CreateDate=at())
        create('SemiInDetail',SheetSeries='S',ReceSheetNo='R',InRolls=2,InQty=-7,FabricID='F',NewLotNo='L')
        semi('R',1,self.actor);semi('R',1,self.actor)
        self.assertEqual(source('SemiStockBook').count(),1)
        self.assertEqual(source('SemiStockBook').get().old_in_length_qty,-7)

    def test_day_report_preserves_duplicate_customer_join_and_original_same_stock_sources(self):
        create('GrayIn',SheetSeries='G',SheetDate=at(2,8),CustomerID='C',SheetKind=11,DlvRolls=2,DlvWeightQty=-8)
        for i in range(2):create('p_Customer',CustomerID='C',NameC=str(i))
        create('GrayStockBook',BookNo=1,CustomerID='C',InRolls=3,OutRolls=1,InWeightQty=8,OutWeightQty=1)
        data=report('JF_sparDayReportTest',{'ymdate':at()})['rows'][0]
        self.assertEqual(data['dlvweightqty'],-16)
        self.assertEqual(data['pbweightqty'],7);self.assertEqual(data['cpweightqty'],7)

    def test_daily_snapshots_do_not_overwrite_repeated_runs(self):
        from plugins.erp_base.source_phase3_dispatch import perform
        a=perform('sp_zhenzhiribaobiao',{},self.actor);b=perform('sp_zhenzhiribaobiao',{},self.actor)
        self.assertNotEqual(a['snapshot_id'],b['snapshot_id'])

    def test_planned_automatic_issue_keeps_zero_factor_and_negative_does_not_disappear(self):
        from plugins.erp_base.source_phase3_auto import planned
        from plugins.erp_base.source_phase3_operations import source
        create('StuffWeight',SheetSeries='W',SheetNo='WN',SheetDate=at(),WareHouseID='12')
        create('StuffWeightDetail',SheetSeries='W',PhaseNo=1,StuffNo=1,StuffID='S',WeightUnit='G',NeedQty=1000,Price=2)
        create('p_Stuff',StuffID='S',WOF=0,Price=2)
        planned(self.actor)
        self.assertEqual(source('StuffOutDetail').count(),1)
        self.assertIsNone(source('StuffOutDetail').get().old_qty)

    def test_gray_auto_out_keeps_duplicate_fine_records_and_reverse_source(self):
        from plugins.erp_base.source_phase3_auto import gray
        from plugins.erp_base.source_phase3_operations import source
        create('JobSheet',SheetSeries='J',SheetNo='JN',AssignUnit=0,CustomerID='C')
        create('GrayInDetail',SheetSeries='G',ReceSheetNo='R',GrayID='P')
        for i,weight in enumerate([4,-1]):
            create('JobGrayRecord',SheetSeries='J',ReceSheetNo='R',GrayBarCode='B',RollNo='1',WeightQty=weight,LengthQty=0)
        gray('JN',self.actor)
        self.assertEqual(source('GrayOutRecord').count(),2)
        self.assertEqual(source('GrayOutDetail').get().old_weight_qty,3)
        self.assertEqual(source('JobSheet').get().old_sum_assigned_weight_qty,3)

    def test_product_carry_staging_keeps_duplicate_and_empty_original_barcodes(self):
        from plugins.erp_base.source_phase3_operations import staging,source
        for i,barcode in enumerate(['B','B','']):
            create('ProdIn_to',SheetSeries='P',SheetDate=at(),BarCode=barcode,RollNo=str(i),WeightQty=2,GrayQty=1)
        staging('238',self.actor)
        self.assertEqual(source('ProdInRecord').count(),3)
        self.assertEqual(source('ProdIn').get().old_rolls,3)

    def test_phase3_metadata_and_api_paths_are_registered(self):
        from plugins.erp_base.source_phase3_actions import OPERATIONS
        from plugins.erp_base.source_phase3_dispatch import OPERATIONS as CALLS
        from plugins.erp_warehouse.source_resources import RESOURCE_OPTIONS
        self.assertEqual({name for name,title in OPERATIONS},set(CALLS))
        actions=RESOURCE_OPTIONS['SourceDyeGrayIn']['workflow']['actions']
        self.assertTrue(any(a['key']=='phase3_operation' for a in actions))

    def test_api_executes_report_carry_and_operation(self):
        from rest_framework.test import APIClient
        self.actor.is_superuser=True;self.actor.save();client=APIClient();client.force_authenticate(self.actor)
        endpoint='/api/system/erp_warehouse_sourcedyegraystockbook/'
        response=client.post(endpoint+'phase3_report/',{'name':'Sp_AppQueryProdStock'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        response=client.post(endpoint+'phase3_carry/',{'name':'Sp_UpdateGrayStock','kind':0,
            'maxstockdate':at(1).isoformat(),'startdate':at(1).isoformat(),'enddate':at(3).isoformat()},format='json')
        self.assertEqual(response.status_code,404)
        response=client.post(endpoint+'phase3_operation/',{'name':'Sp_Stuffin_Price'},format='json')
        self.assertEqual(response.status_code,404)

    def test_semi_scan_uses_receipt_and_workcard_paths(self):
        create('SemiIn',SheetSeries='S',CustomerID='C')
        create('SemiInDetail',SheetSeries='S',ReceSheetNo='R',InputCode='B',ProdID='P',LotNo='L',Rolls=2,WeightQty=3)
        create('CarryMaterialDetail',JobSheetNo='J',ProdID='P',LotNo='L')
        value=report('Sp_SemiStockToJobOut',{'barcode':'B','jobsheetno':'J'})
        self.assertEqual(value['rows'][0]['code'],0)
        self.assertEqual(value['rows'][0]['weightqty'],3)
        value=report('Sp_SemiStockToJobOut',{'barcode':'J','jobsheetno':'J'})
        self.assertIsNone(value['rows'][0]['weightqty'])

    def test_prices_keep_negative_existing_price_and_previous_cursor_value(self):
        from plugins.erp_base.source_phase3_misc import prices
        from plugins.erp_base.source_phase3_operations import source
        for stuff in ['A','B']:create('p_Stuff',StuffID=stuff,Price=-1)
        create('StuffIn',SheetSeries='S',SheetKind=13,SheetDate=at())
        create('StuffInDetail',SheetSeries='S',StuffID='A',Price=4)
        prices('',self.actor,True)
        self.assertEqual(list(source('p_Stuff').order_by('pk').values_list('old_price',flat=True)),[4,4])
        create('StuffStockBook',BookNo=1,SheetSeries='BK',StuffID='A',Price=-2)
        create('StuffStockBook',BookNo=2,SheetSeries='BK',StuffID='A',Price=0,InQty=3,OutQty=1)
        prices('BK',self.actor)
        self.assertEqual(source('StuffStockBook').get(old_book_no=1).old_price,-2)
        self.assertEqual(source('StuffStockBook').get(old_book_no=2).old_in_money,12)

    def test_article_delete_reference_and_gray_delete_process_effect(self):
        from plugins.erp_base.source_phase3_triggers import removing
        from plugins.erp_base.source_phase3_operations import source,model
        from django.core.exceptions import ValidationError
        line=create('ArticleInDetail',DetailNo='D')
        create('ArticleOutDetail',InDetailNo='D',OutQty=-1)
        with self.assertRaises(ValidationError):removing(line,self.actor)
        head=create('GrayOut',SheetSeries='G',WProcessNo='W')
        create('WProcess',WProcessNo='W',JobSheetNo='J')
        create('JobShiftEmp',WProcessNo='W',EmpID='E',ProcessNo=1)
        removing(head,self.actor)
        # GrayOut_Delete 的两个关联变量没有赋值，旧有效体不删除报工或员工行。
        self.assertEqual(source('WProcess').count(),1)
        self.assertEqual(source('JobShiftEmp').count(),1)
        self.assertEqual(model('WProcess').objects.count(),1)

    def test_unusual_receipts_trigger_return_work_and_barcode_without_deduplication(self):
        from plugins.erp_base.source_phase3_operations import create as save,source
        create('JobSheet',SheetNo='J',SheetStatus=0)
        create('GrayIn',SheetSeries='G',SheetKind=14)
        save('GrayInDetail',{'SheetSeries':'G','ReceSheetNo':' R ','OriJobsheetNo':'J','LotNo':' \tL '},self.actor)
        for i in range(2):save('GrayInRecord',{'ReceSheetNo':' R ','RollNo':'01','BarCode':''},self.actor)
        self.assertEqual(source('JobSheet').get().old_sheet_status,9)
        self.assertEqual(list(source('GrayInRecord').values_list('old_bar_code',flat=True)),['R01','R01'])
        self.assertEqual(source('GrayInDetail').get().old_lot_no,'L')

    def test_allot_uses_raw_detail_keys_and_retains_earlier_versions(self):
        from plugins.erp_base.source_phase3_posting import post
        from plugins.erp_base.source_phase3_operations import source,model
        create('StuffAllot',SheetSeries='AL12345678',WareHouseID='12',ToWareHouseID='13',SheetDate=at())
        create('StuffAllotDetail',SheetSeries='AL12345678',StuffID='A',Qty=-3,Price=2,Amount=-6)
        create('p_Stuff',StuffID='A',WOF=2)
        post('StuffAllot','AL12345678',self.actor)
        self.assertEqual(source('StuffInDetail').get().old_qty,-6)
        self.assertEqual(source('StuffOutDetail').get().old_qty,-3)
        post('StuffAllot','AL12345678',self.actor)
        self.assertEqual(source('StuffInDetail').count(),1)
        self.assertEqual(model('StuffInDetail').objects.count(),2)


    def test_gray_and_semi_record_allocation_rounding_and_replay(self):
        from plugins.erp_base.source_phase3_operations import records,source,model
        create('GrayIn',SheetSeries='G',SheetKind=11)
        create('GrayInDetail',SheetSeries='G',ReceSheetNo='R')
        create('JobAssign',SheetSeries='J',AssignNo=1,ReceSheetNo='R',WeightQty=10)
        create('GrayOutDetail',SheetSeries='O',AssignedNo='O-1',ReceSheetNo='R',Rolls=2,WeightQty=10)
        for i in range(3):create('GrayInRecord',ReceSheetNo='R',BarCode=str(i),RollNo=str(i),Rolls=1)
        records('303',{'jobsheetseries':'J','grayoutsheetseries':'O'},self.actor)
        self.assertEqual(source('GrayOutRecord').count(),2)
        self.assertEqual(sum(source('GrayOutRecord').values_list('old_weight_qty',flat=True)),10)
        create('SemiIn',SheetSeries='S',SheetKind=11)
        create('SemiInDetail',SheetSeries='S',ReceSheetNo='SR')
        create('SemiOutDetail',SheetSeries='SO',AssignedNo='SO-1',ReceSheetNo='SR',Rolls=2,WeightQty=7)
        for i in range(3):create('SemiInRecord',ReceSheetNo='SR',BarCode=str(i),RollNo=str(i),Rolls=1,Packs=1,WeightQty=4)
        records('304',{'semioutsheetseries':'SO'},self.actor)
        self.assertEqual(sum(source('SemiOutRecord').values_list('old_weight_qty',flat=True)),7)
        records('304',{'semioutsheetseries':'SO'},self.actor)
        self.assertEqual(source('SemiOutRecord').count(),2)
        self.assertEqual(model('SemiOutRecord').objects.count(),4)

    def test_semi_to_gray_forward_and_reverse_replace_preserve_rows(self):
        from plugins.erp_base.source_phase3_operations import transfer,source,model
        create('SemiOut',SheetSeries='S',SheetKind=30,SheetDate=at())
        create('SemiOutDetail',SheetSeries='S',AssignedNo='S-01',ReceSheetNo='R',ProdID='P',WeightQty=-3)
        transfer('372','S',self.actor)
        self.assertEqual(source('GrayInDetail').get().old_weight_qty,-3)
        create('SemiIn',SheetSeries='I',SheetKind=24,SheetDate=at())
        create('SemiInDetail',SheetSeries='I',ReceSheetNo='I-01',TrunReceSheetNo='R',ProdID='P',WeightQty=-5)
        transfer('394','I',self.actor);transfer('394','I',self.actor,2)
        self.assertEqual(source('GrayOutDetail').get().old_weight_qty,-5)
        self.assertEqual(model('GrayOutDetail').objects.count(),2)

    def test_old_weighted_carry_reprices_returns_and_keeps_opening_rows(self):
        from plugins.erp_base.source_phase3_carry import carry
        from plugins.erp_base.source_phase3_operations import source
        create('s_SysParams',ParamName='CostMethodOfStuff',ParamValue='W')
        create('StuffStockBook',BookNo=1,BookDate=at(2),WareHouseID='13',StuffID='A',InQty=10,OutQty=0,InMoney=20,OutMoney=0,BookKind=13)
        create('StuffIn',SheetSeries='R',SheetKind=15,SheetDate=at(2),WareHouseID='13')
        create('StuffInDetail',SheetSeries='R',StuffID='A',Qty=-3,Price=9,Amount=-27)
        carry('Sp_UpdateStuffStock_Old',0,at(1),at(1),at(3),self.actor)
        self.assertEqual(source('StuffInDetail').get().old_price,2)
        self.assertEqual(source('StuffInDetail').get().old_amount,-6)
        self.assertEqual(source('StuffStock').get().old_pre_month_money,20)
        carry('Sp_UpdateStuffStock_Old',0,at(1),at(1),at(3),self.actor)
        self.assertEqual(source('StuffStock').count(),1)

    def test_removed_receipts_and_return_to_work_refresh_job_state(self):
        from plugins.erp_base.source_phase3_posting import post
        from plugins.erp_base.source_phase3_operations import source
        create('JobSheet',SheetNo='J',PreRolls=3,IsProdInFinished=True)
        create('ProdStockBook',BookNo=1,SheetSeries='P',BookKind=11,JobSheetNo='J')
        post('ProdIn','P',self.actor)
        self.assertFalse(source('JobSheet').get().old_is_prod_in_finished)
        create('GrayStockBook',BookNo=1,SheetSeries='G',BookKind=29,JobSheetNo='J')
        post('GrayOut','G',self.actor)
        self.assertEqual(source('JobSheet').get().old_sheet_status,9)

    def test_storage_raw_keys_moves_and_reverses_exact_rows(self):
        from plugins.erp_base.source_phase3_posting import post
        from plugins.erp_base.source_phase3_operations import source,model
        from plugins.erp_base.source_entry_registry import ENTRY_RULES
        create('GrayIn',SheetSeries='G',SheetKind=11,SheetDate=at())
        original=create('GrayInDetail',SheetSeries='G',ReceSheetNo='R',Rolls=5,WeightQty=10,LengthQty=0)
        create('GrayInRecord',ReceSheetNo='R',BarCode='B',RollNo='1',Rolls=1)
        head=create('GrayStorageAdjust',SheetSeries='A',RightStatus=10)
        create('GrayStorageAdjustDetail',SheetSeries='A',ReceSheetNo='R',LotNo='G',Rolls=1,WeightQty=2,LengthQty=0,ToArea='N')
        create('GrayStorageAdjustRecord',SheetSeries='A',FromReceSheetNo='R',ReceSheetNo='B')
        post('GrayStorageAdjust','A',self.actor)
        original.refresh_from_db();self.assertEqual(original.old_weight_qty,8)
        self.assertNotEqual(source('GrayInRecord').get().old_rece_sheet_no,'R')
        post('GrayStorageAdjust','A',self.actor)
        original.refresh_from_db();self.assertEqual(original.old_weight_qty,8)
        self.assertEqual(source('GrayStockBook').count(),1)
        self.assertEqual(model('GrayStockBook').objects.count(),2)


    def test_dye_order_replays_duplicates_and_retains_cancelled_versions(self):
        from plugins.erp_base.source_phase3_misc import dye_order
        from plugins.erp_base.source_phase3_operations import source,model
        create('StuffOut',SheetSeries='D',SheetKind=29,RightStatus=0)
        create('p_Stuff',StuffID='A',StockUnit='K')
        for qty in [2,-3]:create('StuffOutDetail',SheetSeries='D',DetailNo='D-1',StuffID='A',Qty=qty)
        dye_order('D',self.actor)
        self.assertEqual(sorted(source('DyeStuffOutDetail').values_list('old_qty',flat=True)),[-3,2])
        dye_order('D',self.actor)
        self.assertEqual(model('DyeStuffOutDetail').objects.count(),4)
        dye_order('D',self.actor,True)
        self.assertEqual(source('DyeStuffOutDetail').count(),0)

    def test_remaining_triggers_keep_source_anomalies_and_update_production(self):
        from plugins.erp_base.source_phase3_operations import create as save,source,model
        from plugins.erp_base.source_phase3_triggers import saved
        job=create('JobSheet',SheetSeries='J',SheetNo='JN',CurrProcessID='退仓待处理',SheetStatus=9)
        create('GrayOut',SheetSeries='G',SheetKind=29)
        save('GrayOutDetail',{'SheetSeries':'G','JobSheetSeries':'JN'},self.actor)
        job.refresh_from_db();self.assertEqual(job.old_sheet_status,0)
        create('JobProcess',SheetSeries='J',ProcessID='GX98',ProcessNo=1)
        create('ProcessSchedule',JobSheetNo='JN')
        save('ProdIn',{'SheetSeries':'P','JobSheetNo':'JN','SheetDate':at()},self.actor)
        self.assertEqual(source('ProcessSchedule').count(),0)
        self.assertEqual(model('ProcessSchedule').objects.count(),1)
        self.assertEqual(source('JobProcess').get().old_end_time,at())
        save('SemiInDetail',{'ReceSheetNo':'S','LotNo':' X\t '},self.actor)
        self.assertEqual(source('SemiInDetail').get().old_lot_no,' X ')
        for i in range(2):save('p_Stuff',{'StuffID':str(i),'Name':'相同材料'},self.actor)
        self.assertEqual(source('p_Stuff').count(),2)
        create('SemiOutWorkApplyDetail',DetailNo='A',CustomerID='C',ProdID='P')
        create('SemiOutDetail',SheetSeries='O',JobSheetNo='B',ProdID='Q')
        head=save('SemiOut',{'SheetSeries':'O','CustomerID':'D'},self.actor)
        self.assertEqual(source('SemiOut').count(),1)
        future=timezone.now()+__import__('datetime').timedelta(days=1)
        head=save('StuffOut',{'SheetSeries':'F','SheetKind':21,'OutDate':future},self.actor)
        self.assertEqual(head.old_out_date,future)
        create('StuffIn',SheetSeries='SI',SheetKind=13,SheetDate=at())
        create('StuffInDetail',SheetSeries='SI',StuffID='A',Price=3)
        item=save('StuffStockBook',{'BookNo':1,'StuffID':'A','Price':0,'InQty':2,'OutQty':-1},self.actor)
        self.assertEqual(item.old_in_money,6);self.assertEqual(item.old_out_money,-3)

    def test_article_weighted_original_unassigned_price_remains_null(self):
        from plugins.erp_base.source_phase3_carry import carry
        from plugins.erp_base.source_phase3_operations import source
        create('s_SysParams',ParamName='CostMethodOfArticle',ParamValue='W')
        create('p_Article',ArticleID='A',Price=5)
        create('ArticleIn',SheetSeries='I',SheetKind=13)
        create('ArticleInDetail',SheetSeries='I',DetailNo='D',ArticleID='A',Price=2)
        create('ArticleStockBook',BookNo=1,BookDate=at(2),WareHouseID='W',ArticleID='A',InDetailNo='D',InQty=3,OutQty=0,InMoney=6,OutMoney=0)
        create('ArticleOut',SheetSeries='O',SheetDate=at(2),WareHouseID='W')
        create('ArticleOutDetail',SheetSeries='O',ArticleID='A',OutQty=1,Price=2,Total=2)
        carry('Sp_UpdateArticleStock',0,at(1),at(1),at(3),self.actor)
        self.assertIsNone(source('ArticleOutDetail').get().old_price)
        self.assertIsNone(source('p_Article').get().old_price)
        self.assertIsNone(source('ArticleStock').get().old_pre_month_money)

    def test_auto_allot_original_noop_and_job_approval_variants(self):
        from plugins.erp_base.source_phase3_dispatch import perform
        from plugins.erp_base.source_phase3_operations import source
        create('StuffAllot',SheetSeries='A')
        perform('Sp_AUTO_StuffAllot',{},self.actor)
        self.assertEqual(source('StuffStockBook').count(),0)
        create('s_SysParams',ParamName='JobReProdIn',ParamValue='1')
        job=create('JobSheet',SheetNo='J',PreRolls=3)
        receipt=create('ProdIn',SheetSeries='P',JobSheetNo='J',SheetKind=11,RightStatus=10,Rolls=2)
        perform('Sp_UpdateJobSheetByProdIn',{'jobsheetno':'J'},self.actor)
        job.refresh_from_db();self.assertTrue(job.old_is_prod_in_finished)
        create('ProdIn',SheetSeries='R',JobSheetNo='J',SheetKind=16,RightStatus=10,Rolls=-1)
        perform('Sp_UpdateJobSheetByProdIn',{'jobsheetno':'J'},self.actor)
        job.refresh_from_db();self.assertFalse(job.old_is_prod_in_finished)


    def test_inventory_area_and_print_date_use_explicit_latest_source_mapping(self):
        create('GrayStockBook',BookNo=1,GrayID='G',ReceSheetNo='R',InWeightQty=2)
        create('GrayInDetail',GrayID='G',ReceSheetNo='R',Area='A;B')
        self.assertEqual(report('Sp_AppQueryGrayStock',{})['rows'][0]['area'],'A;B')
        create('SemiStockBook',BookNo=1,BookDate=at(2),ProdID='G',WareHouseID='W',CustomerID='C',LotNo='L',InRolls=2,InWeightQty=4)
        p={'ischecked4':'Y','ischecked5':'Y','startdate':at(1),'enddate':at(3)}
        self.assertEqual(len(report('qry_PrintGrayStockBook',p)['rows']),1)
        self.assertEqual(len(report('qry_PrintGrayStockBook',{**p,'startdate':at(3)})['rows']),0)

    def test_old_return_cleanup_is_retained_instead_of_erased(self):
        from plugins.erp_base.source_phase3_old_stock import gray
        from plugins.erp_base.source_phase3_operations import source,model
        create('GrayIn',SheetSeries='G',SheetNo='GN',SheetKind=16,SheetDate=at())
        create('GrayInDetail',SheetSeries='G',ReceSheetNo='NEW',OriReceSheetNo='OLD',WeightQty=-5)
        gray('GrayIn','G',0,self.actor)
        self.assertEqual(source('GrayStockBook').count(),0)
        self.assertEqual(model('GrayStockBook').objects.get().old_in_weight_qty,-5)
