from datetime import datetime
from decimal import Decimal
from django.apps import apps
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.source_services import write,delete_documents
from plugins.erp_base.source_phase2_orders import save,check_modify,original_lists,DETAIL_FIELDS
from plugins.erp_base.source_phase2_functions import dosage,confirmed_price,color_price,previous_material_price
from plugins.erp_base.source_phase2_operations import auto_phase,reprint,material_adjustment,order_prices
from plugins.erp_base.source_phase2_reports import report,QUERIES
from plugins.erp_base.source_quality_reports import rows
from plugins.erp_base.source_execution_state import active
from plugins.erp_base.tests.source_fixtures import historical_batch


def model(table,module='erp_sales'):
    return apps.get_model(module,'SourceDye'+table)


def at(day):
    return timezone.make_aware(datetime(2026,1,day))


class PhaseTwoTests(TestCase):
    def setUp(self):
        self.actor=Users.objects.create_superuser(username='phase2',password='test-only')

    def test_fixed_price_duplicate_rows_remain_but_original_approval_edit_rule_applies(self):
        head=model('FixedPrice').objects.create(old_sheet_series='F',old_customer_id='C')
        data=dict(old_sheet_series='F',old_color_num='RED1',old_prod_id='P',old_width=0,old_weight=0)
        a=write(model('FixedPriceDetail'),dict(data,old_detail_no='D1'),actor=self.actor)
        b=write(model('FixedPriceDetail'),dict(data,old_detail_no='D2'),actor=self.actor)
        self.assertEqual(model('FixedPriceDetail').objects.count(),2)
        write(type(a),{'old_right_status':10},a,self.actor)
        with self.assertRaises(ValidationError):write(type(a),{'old_cus_price':5},a,self.actor)
        with self.assertRaises(ValidationError):delete_documents(type(a).objects.filter(pk=a.pk),self.actor)
        b.refresh_from_db();self.assertEqual(b.old_color_num,'RED1')

    def test_order_list_protocol_preserves_empty_duplicate_and_negative_items(self):
        p={f+'List':'x,x' for f in DETAIL_FIELDS}
        p.update(DlvDateList='2026-01-01,',OrderQtyList='-3.25,-3.25',OrderRollsList='1,1',LotNoList='')
        result=original_lists(p,DETAIL_FIELDS,'ColorID')
        self.assertEqual(len(result),2);self.assertEqual(result[0]['OrderQty'],Decimal('-3.25'))
        self.assertIsNone(result[1]['LotNo']);self.assertEqual(result[1]['DlvDate'].year,1900)

    def test_app_replacement_keeps_original_duplicates_and_recreates_all_members(self):
        model('HEmployee','erp_base').objects.create(old_emp_id='E',old_name='张',old_is_customer=True,old_customer_id='C')
        model('PCustomer','erp_base').objects.create(old_customer_id='C',old_saler_id='S',old_label_id='L',old_deposit=3)
        p=dict(EmpID='E',CustomerIDMain='IGNORED',AssignUnit=-1,DetailCustName='',CustSelfNo='PO',ContractNo='K')
        detail=dict(ColorID='红',ColorNum='R1',CustColorNum='',CustFabricName='',CustSelfProduct='',LotNo='',DlvDate=at(2),OrderQty=Decimal('-2'),OrderRolls=1)
        first=save(p,self.actor,details=[detail,detail],requirements=[])
        self.assertEqual(first.old_customer_id,'C');self.assertIsNone(first.old_assign_unit)
        before=list(model('OrderColor').objects.order_by('pk'))
        newer=save(p,self.actor,first,details=[detail,detail],requirements=[])
        self.assertNotEqual(first.pk,newer.pk)
        self.assertEqual(model('OrderMain').objects.count(),2)
        self.assertEqual(model('OrderColor').objects.count(),4)
        self.assertEqual(active(model('OrderColor').objects.all()).count(),2)
        for old in before:
            old.refresh_from_db();self.assertEqual(old.old_order_qty,Decimal('-2'))
        self.assertEqual(check_modify(newer.old_sheet_series)['Code'],0)

    def test_order_info_insert_update_delete_preserves_retired_targets(self):
        info=write(model('OrderInfo'),dict(old_sheet_series='OI',old_check_no='D',old_prod_id='P'),actor=self.actor)
        self.assertEqual(model('OrderMain').objects.count(),1)
        write(type(info),{'old_color_id':'蓝'},info,self.actor)
        self.assertEqual(model('OrderColor').objects.get().old_color_id,'蓝')
        delete_documents(type(info).objects.filter(pk=info.pk),self.actor)
        self.assertEqual(model('OrderColor').objects.count(),1)
        self.assertEqual(active(model('OrderColor').objects.all()).count(),0)

    def test_dosage_cost_uses_numeric_color_but_dosage_joins_exact_color(self):
        model('PColorNum','erp_base').objects.create(old_sheet_series='L',old_color_no='X',old_color_num='A001')
        samples=model('DyeDipsRecord','erp_sampling')
        samples.objects.create(old_sheet_series='D1',old_color_num='B001',old_cost=8,old_stuff_dosage=7)
        samples.objects.create(old_sheet_series='D2',old_color_num='A001',old_cost=2,old_stuff_dosage=-3)
        self.assertEqual(dosage('C001',0),8);self.assertEqual(dosage('C001',1),-3)
        self.assertIsNone(dosage(None,0));self.assertIsNone(dosage('C001',2))

    def test_confirmed_price_preserves_repeated_charge_join(self):
        model('FixedPrice').objects.create(old_sheet_series='F',old_customer_id='C',old_sheet_date=at(1))
        model('FixedPriceDetail').objects.create(old_sheet_series='F',old_detail_no='D',old_prod_id='P',old_yarn_category='Y',old_cus_price=10,old_width=0,old_weight=0)
        model('OrderAtte').objects.create(old_sheet_series='O',old_check_no='X',old_field_type='05',old_atte_code='A')
        for _ in range(2):model('PFieldValidSub','erp_base').objects.create(old_field_type='AtteKind',old_code='A',old_sub_code='A',old_num_value2=-2,old_num_value3=1,old_sort_value=0)
        self.assertEqual(confirmed_price('X','unused','C','P','Y',0),6)

    def test_phase_cursor_updates_all_same_entry_keys_without_removing_duplicates(self):
        m=model('SmpPrescriptEntry','erp_sampling')
        a=m.objects.create(old_finter_id=1,old_fentry_id=1,old_fparent_id=1,old_ftech_id=7)
        b=m.objects.create(old_finter_id=1,old_fentry_id=1,old_fparent_id=2,old_ftech_id=7)
        c=m.objects.create(old_finter_id=1,old_fentry_id=2,old_fparent_id=1,old_ftech_id=8)
        auto_phase(self.actor)
        a.refresh_from_db();b.refresh_from_db();c.refresh_from_db()
        self.assertEqual((a.old_phase_no,a.old_stuff_no),(1,2));self.assertEqual(b.old_stuff_no,2)
        self.assertEqual((c.old_phase_no,c.old_stuff_no),(2,1));self.assertEqual(m.objects.count(),3)

    def test_reprint_four_positions_count_duplicate_employee_and_zero_fails_atomically(self):
        m=model('DyeReprint','erp_sampling')
        a=m.objects.create(old_sheet_series='R',old_emp_id='E',old_emp_id1='E')
        reprint(a,self.actor);a.refresh_from_db();self.assertEqual(a.old_num,0.5)
        empty=m.objects.create(old_sheet_series='EMPTY')
        with self.assertRaises(ZeroDivisionError):reprint(empty,self.actor)
        empty.refresh_from_db();self.assertIsNone(empty.old_num)

    def test_report_views_and_multiple_results_execute_on_empty_authorized_scope(self):
        p=dict(current=1,size=10,startdate='2026-01-01',enddate='2026-02-01',confilter='',empid='',customerid='',sheetseries='',sheetno='',prodid='',fabrickind='',colordepthid='',bisaccept=False)
        for name in QUERIES:
            with self.subTest(name=name):
                result=report(name,p,query=lambda t,m:rows(t,m).none())['rows']
                if name=='Sp_QueryDyeingOrder':
                    self.assertEqual(len(result),31);self.assertTrue(all(r['orderqty']==0 for r in result))
                else:self.assertEqual(result,[])

    def test_report_duplicate_customer_joins_and_page_detail_sets(self):
        for _ in range(2):model('PCustomer','erp_base').objects.create(old_customer_id='C',old_name_c='客',old_short_name='客',old_cust_kind_id='0',old_right_status=10)
        model('Quote').objects.create(old_sheet_series='Q',old_customer_id='C',old_sheet_date=at(2))
        model('QuoteDetail').objects.create(old_sheet_series='Q',old_detail_no='D',old_width=0,old_weight=0,old_price_unit=0,old_price=-2)
        result=report('Sp_AppQueryColorQuote',dict(current=1,size=1,startdate='2026-01-01',enddate='2026-02-01',confilter=''))
        self.assertEqual(result['pagination']['total'],2);self.assertEqual(len(result['rows']),1)
        self.assertEqual(len(result['result_sets'][0]['rows']),1)
        self.assertEqual(result['result_sets'][0]['rows'][0]['price'],Decimal('-2'))

    def test_shared_sales_limit_repeated_receipts_and_customer_joins(self):
        from plugins.erp_base.source_phase2_limits import limit,report as limit_report
        for _ in range(2):model('PCustomer','erp_base').objects.create(old_customer_id='C',old_short_name='客',old_settle_id='01')
        m=model('FARMain','erp_quality')
        m.objects.create(old_sheet_series='A',old_customer_id='C',old_sheet_date=at(1),**{m.SOURCE_FIELDS['ARMoney']:100})
        m=model('FMoneyInDetail','erp_base')
        for _ in range(2):m.objects.create(old_sheet_series='R',old_detail_no='D',old_write_off_money=-5,**{m.SOURCE_FIELDS['ARDetailNo']:'A'})
        future=at(1).replace(month=3)
        self.assertEqual(limit('C',future),Decimal('220.00'))
        self.assertIsNone(limit('MISSING',future))
        self.assertEqual(limit_report(now=future)['rows'][0]['CurrentNotWriteOffMoney'],220)

    def test_label_remarks_preserves_duplicate_labels_and_customer_default(self):
        from plugins.erp_base.source_phase2_functions import label_remarks
        model('OrderMain').objects.create(old_sheet_series='O',old_customer_id='000')
        color=model('OrderColor').objects.create(old_sheet_series='O',old_check_no='C',old_color_remarks='经纱送甲仓')
        for _ in range(2):model('PFieldValid','erp_base').objects.create(old_field_type='LabelWareHouse',old_code='A',old_name='甲仓',old_sort_value=0)
        self.assertEqual(label_remarks(0,'C'),'甲仓甲仓')
        self.assertIsNone(label_remarks(1,'C'));self.assertIsNone(label_remarks(2,'C'))
        color.old_color_remarks=None;color.save()
        self.assertEqual(label_remarks(0,'C'),'东莞')

    def test_recipe_cost_multiplies_duplicate_heads_and_phases_with_negative_amount(self):
        from plugins.erp_base.source_phase2_operations import recipe_costs
        for _ in range(2):model('DyeRecipe','erp_sampling').objects.create(old_sheet_series='R')
        for _ in range(2):model('DyeRecipePhase','erp_sampling').objects.create(old_sheet_series='R',old_phase_no=1)
        model('DyeRecipeDetail','erp_sampling').objects.create(old_sheet_series='R',old_phase_no=1,old_stuff_no=1,old_amount=-3)
        model('DyeRecipeDetail','erp_sampling').objects.create(old_sheet_series='R',old_phase_no=9,old_stuff_no=1,old_amount=100)
        recipe_costs(self.actor)
        self.assertEqual(list(model('DyeRecipe','erp_sampling').objects.values_list('old_cost',flat=True)),[-12,-12])
        self.assertEqual(model('DyeRecipeDetail','erp_sampling').objects.count(),2)

    def test_sample_book_preserves_negative_duplicate_sources_and_original_out_delete_scope(self):
        from plugins.erp_base.source_phase2_operations import sample_book
        h=model('SampleIn','erp_sampling').objects.create(old_sheet_series='I',old_sheet_no='IN',old_fact_id='F')
        for _ in range(2):model('SampleInDetail','erp_sampling').objects.create(old_sheet_series='I',old_detail_no='D',old_qty=-3,old_price=1)
        sample_book(h,self.actor,'IN','D',1)
        book=model('SampleStockBook','erp_sampling')
        self.assertEqual(book.objects.get().old_in_qty,Decimal('-3'))
        self.assertEqual(book.objects.get().old_customer_id,'F')
        self.assertIsNotNone(book.objects.get().old_book_no)
        model('SampleOut','erp_sampling').objects.create(old_sheet_series='O',old_sheet_no='OUT')
        book.objects.create(old_book_no=999,old_sheet_no='IN',old_detail_no='D',old_book_kind=2,old_out_qty=-4)
        sample_book(h,self.actor,'IN','D',2)
        self.assertEqual(book.objects.count(),2);self.assertEqual(active(book.objects.all()).count(),0)
        self.assertEqual(model('SampleInDetail','erp_sampling').objects.count(),2)

    def test_quote_adjustment_all_duplicate_details_and_reverse_original_values(self):
        from plugins.erp_base.source_phase2_operations import quote_adjustment
        head=model('PriceAdjust').objects.create(old_sheet_series='A',old_date_type=2,old_start_date=at(1))
        model('PriceAdjustDetail').objects.create(old_sheet_series='A',old_detail_no='AD',old_quote_detail_no='D',old_adjust_price=-5)
        for _ in range(2):model('QuoteDetail').objects.create(old_sheet_series='Q',old_detail_no='D',old_width=0,old_weight=0,old_price_unit=0)
        quote_adjustment(head,self.actor,True)
        self.assertEqual(list(model('QuoteDetail').objects.values_list('old_adjust_price',flat=True)),[-5,-5])
        quote_adjustment(head,self.actor,False)
        self.assertEqual(list(model('QuoteDetail').objects.values_list('old_date_type',flat=True)),[0,0])
        self.assertTrue(all(timezone.localtime(r.old_start_date).year==1900 for r in model('QuoteDetail').objects.all()))

    def test_global_feel_cursor_preserves_previous_customer_when_orphan_has_no_header(self):
        head=model('OrderMain').objects.create(old_sheet_series='O',old_customer_id='C')
        model('OrderColor').objects.create(old_sheet_series='O',old_check_no='D',old_prod_id='P')
        for series in ['O','ORPHAN']:model('OrderAtte').objects.create(old_sheet_series=series,old_atte_value='软手感',old_field_type='05')
        model('QuoteItemPrice').objects.create(old_item='软手感',old_customer_id='C',old_prod_id='P',old_price=9,old_unit='0')
        order_prices(head,self.actor,feel_only=True,all_orders=True)
        self.assertEqual(list(model('OrderAtte').objects.values_list('old_price',flat=True)),[9,9])

    def test_duplicate_sample_phases_are_saved_with_original_violation_audit(self):
        m=model('DyeRecipePhase','erp_sampling')
        for n in [1,2]:write(m,dict(old_sheet_series='R',old_phase_no=n,old_phase_id='D'),actor=self.actor)
        self.assertEqual(m.objects.count(),2)

    def test_sales_limit_source_rejects_write_requests(self):
        from plugins.erp_base.source_api import SourceSalesLimitReadOnlyViewSet
        self.assertEqual(SourceSalesLimitReadOnlyViewSet.http_method_names,['get','head','options'])

    def test_material_adjustment_repeated_rebuild_retains_old_versions(self):
        m=model('StuffIn','erp_warehouse');d=model('StuffInDetail','erp_warehouse')
        m.objects.create(old_sheet_series='OLD',old_sheet_no='OLD',old_sheet_date=at(1),old_supplier_id='S',old_sheet_kind=13,old_right_status=10)
        d.objects.create(old_sheet_series='OLD',old_detail_no='OLD1',old_stuff_id='X',old_price=2)
        head=m.objects.create(old_sheet_series='SI12345678',old_sheet_no='SI12345678',old_sheet_date=at(2),old_supplier_id='S')
        for n in range(2):d.objects.create(old_sheet_series=head.old_sheet_series,old_detail_no=head.old_sheet_series+'-01',old_stuff_id='X',old_price=3)
        material_adjustment(head,self.actor)
        self.assertEqual(rows('MaterialPriceAdjustDetail','erp_base').count(),2)
        material_adjustment(head,self.actor)
        self.assertEqual(model('MaterialPriceAdjustDetail','erp_base').objects.count(),4)
        self.assertEqual(rows('MaterialPriceAdjustDetail','erp_base').count(),2)

    def test_printing_sixteen_slots_and_string_row_number(self):
        from plugins.erp_base.source_phase2_printing import pastedetails
        model('OrderMain').objects.create(old_sheet_series='O',old_sheet_no='N',old_sheet_kind=40,old_print_code='P',old_unit=1)
        model('OrderColor').objects.create(old_sheet_series='O',old_check_no='C',old_color_plate_id='A',old_order_qty=-10)
        model('PrintColorSeparate','erp_sampling').objects.create(old_sheet_series='PS',old_print_code='P')
        model('PrintColorSeparateDetail','erp_sampling').objects.create(old_sheet_series='PS',old_detail_no='PS-01',old_color_plate_id='A',old_color_count=1)
        model('PrintColorSeparateRecord','erp_sampling').objects.create(old_sheet_series='PS',old_detail_no='PS-01',old_color_plate_id='A',old_row_no='1',old_color_name='红',old_rate=100)
        result=pastedetails('PA','N')
        names=next(r for r in result['rows'] if r['Kind']=='色名')
        self.assertEqual(names['Value1'],'红');self.assertEqual(names['Value16'],'')
        self.assertEqual(names['OrderDosage'],-10);self.assertEqual(len(result['rows']),2)

    def test_print_weight_uses_float_ratio_and_negative_dosage(self):
        from plugins.erp_base.source_phase2_printing import print_weight
        model('OrderMain').objects.create(old_sheet_series='O',old_sheet_no='N',old_print_code='P')
        model('PPasteDosage','erp_base').objects.create(old_sheet_series='PA',old_order_no='N',old_right_status=10,old_sheet_date=at(1))
        for kind,value in [('色名','红'),('用量','-2.50')]:
            model('PPasteDosageDetail','erp_base').objects.create(old_sheet_series='PA',old_detail_no=kind,old_color_plate_id='A',old_kind=kind,old_value1=value)
        model('PrintingTest','erp_sampling').objects.create(old_sheet_series='PT',old_print_code='P')
        model('PrintingTestDetail','erp_sampling').objects.create(old_sheet_series='PT',old_wpserial_number=1,old_color_plate_id='A',old_sample_sign='A')
        model('PrintingTestColor','erp_sampling').objects.create(old_sheet_series='PT',old_wpserial_number=1,old_serial_number=1,old_color_name='红')
        for n in range(2):model('PrintingTestStuff','erp_sampling').objects.create(old_sheet_series='PT',old_wpserial_number=1,old_serial_number=1,old_dye_stuff_serial_number=n,old_dye_stuff_code='D',old_ratio=1.5,old_print_code='P',old_color_name='红')
        result=print_weight('N')
        self.assertEqual(len(result['rows']),2);self.assertTrue(all(r['dosage']==-37.5 for r in result['rows']))

    def test_new_api_actions_execute_with_structured_detail_payload(self):
        from types import SimpleNamespace
        from rest_framework.test import APIRequestFactory,force_authenticate
        from plugins.erp_base.source_api import SourceRecordViewSet,SourceRecordSerializer
        class OrderSerializer(SourceRecordSerializer):
            class Meta:
                model=model('OrderMain');fields='__all__'
        class OrderView(SourceRecordViewSet):
            queryset=model('OrderMain').objects.all()
            serializer_class=OrderSerializer
            permission_classes=[]
        p=dict(EmpID='',CustomerIDMain='C',AssignUnit=-1,DetailCustName='',CustSelfNo='',ContractNo='',
            details=[dict(ColorID='红',OrderQty='-1.25')],requirements=[])
        request=APIRequestFactory().post('/',p,format='json');force_authenticate(request,user=self.actor)
        result=OrderView.as_view({'post':'app_order_save'})(request)
        self.assertEqual(result.status_code,200);self.assertEqual(model('OrderColor').objects.get().old_order_qty,Decimal('-1.25'))

    def test_original_sample_insert_maps_every_parameter_without_extra_id(self):
        from plugins.erp_base.source_phase2_sampling import add,ADD_FIELDS
        p=dict.fromkeys(ADD_FIELDS,None);p.update(SheetSeries='S',ColorNum='R',Weight=-1,Cost=-2)
        item=add(p,self.actor)
        self.assertEqual(len(ADD_FIELDS),49)
        self.assertEqual(item.old_weight,-1);self.assertEqual(item.old_cost,-2)
        self.assertNotIn('legacy_id',{f.name for f in item._meta.fields})

    def test_recipe_insert_archives_orphan_rows_without_dropping_them(self):
        phase=model('DyeRecipePhase','erp_sampling').objects.create(old_sheet_series='MISSING',old_phase_no=1)
        detail=model('DyeRecipeDetail','erp_sampling').objects.create(old_sheet_series='MISSING',old_phase_no=1,old_stuff_no=1,old_amount=-3)
        write(model('DyeRecipe','erp_sampling'),{'old_sheet_series':'NEW'},actor=self.actor)
        self.assertTrue(type(phase).objects.filter(pk=phase.pk).exists())
        self.assertTrue(type(detail).objects.filter(pk=detail.pk).exists())
        self.assertFalse(rows('DyeRecipeDetail','erp_sampling').filter(pk=detail.pk).exists())

    def test_null_sales_limit_date_has_original_null_result(self):
        from plugins.erp_base.source_phase2_limits import limit
        self.assertIsNone(limit('C',None))

    def test_original_noop_check_and_color_selection_do_not_allocate_or_write(self):
        from plugins.erp_base.source_phase2_orders import check_save
        from plugins.erp_base.source_phase2_functions import produce_color
        self.assertEqual(check_save(),{'Code':0,'Msg':''})
        for value in [None,'','  ']:self.assertEqual(produce_color('A',value)['ColorNum'],'A')
        self.assertEqual(produce_color(None,'B')['ColorNum'],'B')
        self.assertEqual(model('DyeLabColor','erp_sampling').objects.count(),0)

    def test_page_action_permission_names_match_registered_endpoints(self):
        from plugins.erp_sales.source_resources import RESOURCE_OPTIONS
        from plugins.erp_base.source_api import SourceOrderViewSet
        from system.views import view_for
        from system.catalog import ENTITIES
        entity='erp_sales_sourcedyeordermain'
        methods={a.__name__:a for a in view_for(entity,ENTITIES[entity]).get_extra_actions()}
        actions=RESOURCE_OPTIONS['SourceDyeOrderMain']['workflow']['actions']
        for action in actions:
            if action['key'] in ['phase2_report','app_order_save','app_order_modify','app_order_check','refresh_order_prices']:
                self.assertEqual(methods[action['key']].url_name,action['key'])

    def test_daily_report_api_accepts_dates_and_normalizes_offset_to_local_day(self):
        from rest_framework.test import APIRequestFactory,force_authenticate
        from plugins.erp_base.source_api import SourceRecordViewSet
        view=SourceRecordViewSet.as_view({'post':'phase2_report'},permission_classes=[])
        request=APIRequestFactory().post('/',{'name':'Sp_QueryDyeingOrder','startdate':'2026-01-01T16:00:00Z','enddate':'2026-01-02T16:00:00Z'},format='json')
        force_authenticate(request,user=self.actor)
        response=view(request)
        self.assertEqual(response.status_code,200)
        self.assertEqual([r['sheetdate'] for r in response.data['data']['rows']],['2026-01-02'])
