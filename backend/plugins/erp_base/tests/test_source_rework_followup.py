from plugins.erp_base.tests.source_fixtures import historical_batch
from datetime import datetime,timedelta
from decimal import Decimal
from django.apps import apps
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.business import snapshot
from plugins.erp_base.source_context import SourceDocumentContext
from plugins.erp_base.source_chain_reverse import reader
from plugins.erp_base.source_continuation import view_effects
from plugins.erp_base.source_rework_extended import daily,combined,comparison,responsibility,previous_year
from plugins.erp_base.source_outwork_close import close,closure,reopen
from plugins.erp_base.source_outwork_followup import review
from plugins.erp_base.source_outwork_flow import dispatch,receive_product
from plugins.erp_base.source_delivery_flow import return_material,dispatch_product
from plugins.erp_base.source_purchase_flow import return_raw_purchase,raw_receipts


class ReworkExtendedTests(TestCase):
    def setUp(self):
        self.at=timezone.make_aware(datetime(2026,8,15,12))
        self.actor=Users.objects.create_superuser(username='rework-extra',password='test')
        self.client=APIClient();self.client.force_authenticate(self.actor)
    def old(self,name,module,**values):
        row=apps.get_model(module+'.SourceDye'+name).objects.create(**values);row.refresh_from_db();return row
    def job(self,number='J',review='Q'):
        return self.old('JobSheet','erp_production',old_sheet_series=number,old_sheet_no=number,old_loss_str=review,old_prod_id='G')
    def defect(self,number='Q',dept='02',kind='内部评审',shift='03'):
        return self.old('WDefect','erp_quality',old_sheet_no=number,old_sheet_series=number,old_kind=kind,old_defect_dept=dept,old_defect_class_id=shift)
    def work(self,number='W',job='J',station='06',kg=1000,dosage=100,at=None):
        return self.old('WProcess','erp_production',old_wprocess_no=number,old_job_sheet_no=job,old_station_id=station,
            old_curr_kg=kg,old_curr_dosage=dosage,old_create_date=at or self.at)
    def far(self,**extra):
        value={'detail_no':'D','header_sheet_series':'H','sheet_date':self.at,'sheet_kind':30,'job_number':'J',
            'quantity':Decimal(1000),'metres':None,'zero_amount':True};value.update(extra);return value

    def test_daily_original_subtotals_sum_repeated_denominator_and_rates(self):
        self.job();self.defect();self.defect(dept='07');self.work()
        report=daily(self.at.date());detail=[row for row in report['rows'] if row['Num']=='A'];subtotal=report['rows'][-1]
        self.assertEqual(len(detail),2);self.assertEqual({row['Workshop'] for row in detail},{'本车间','外车间'})
        self.assertEqual(subtotal['ZNum'],2);self.assertEqual(subtotal['ZKg'],2);self.assertEqual(subtotal['Rate'],200)
        self.assertEqual(subtotal['N_NumDay'],2);self.assertEqual(subtotal['N_RKgMonth'],2)

    def test_daily_month_and_day_are_separate_and_include_997_boundary(self):
        self.job();self.defect()
        self.work('PAST',at=self.at-timedelta(days=1))
        self.work('END',at=self.at.replace(hour=23,minute=59,second=59,microsecond=997000))
        self.work('LATE',at=self.at.replace(hour=23,minute=59,second=59,microsecond=998000))
        row=daily(self.at.date())['rows'][0]
        self.assertEqual(row['N_NumDay'],1);self.assertEqual(row['N_NumMonth'],2);self.assertEqual(row['ZNum'],2)

    def test_daily_zero_denominator_retains_group_and_reason(self):
        self.job();self.defect(dept='07');self.work(station='05',kg=0)
        data=daily(self.at.date());self.assertIsNone(data['rows'][0]['Rate'])
        self.assertEqual(data['rows'][0]['N_NumMonth'],1);self.assertTrue(data['supplemental_rows'])

    def test_daily_duplicate_fabric_dictionary_and_unknown_review_kept(self):
        self.job();self.defect(kind='非常规评审');self.work()
        self.old('PGray','erp_base',old_gray_id='G',old_fabric_kind_id='F')
        for unused in range(2):self.old('PFieldValid','erp_base',old_field_type='FabricKind',old_code='F',old_description='布种')
        data=daily(self.at.date());self.assertEqual(len(data['result_rows']),2)
        self.assertEqual(data['rows'][0]['N_NumMonth'],0);self.assertEqual(data['rows'][0]['FabricName'],'布种')

    def test_combined_uses_original_null_to_zero_only_for_combined_totals(self):
        self.work(kg=1000,dosage=None)
        result=combined(self.at,self.at,[],'')
        row=result['rows'][0];self.assertEqual(row['AllNum'],1);self.assertEqual(row['AllKg'],0)
        self.assertIsNone(row['N_RKg06']);self.assertIsNone(row['FARKg'])

    def test_combined_far_duplicate_negative_and_null_quantities(self):
        inputs=[self.far(quantity=Decimal(-1000)),self.far(quantity=None),self.far(quantity=Decimal(-1000)),self.far(sheet_kind=99)]
        row=combined(self.at,self.at,inputs,'明确原连接行')['rows'][0]
        self.assertEqual(row['FARNum'],3);self.assertEqual(row['FARKg'],-2)

    def test_comparison_legacy_current_repair_join_and_explicit_same_period(self):
        self.job();self.defect();self.work(kg=2000)
        self.work(at=self.at.replace(year=2025),kg=1000)
        inputs=[self.far(),self.far(sheet_date=self.at.replace(year=2025),quantity=Decimal(3000))]
        old=comparison(self.at,self.at,'06','legacy',inputs,'明确来源')['rows'][0]
        fixed=comparison(self.at,self.at,'06','same_period',inputs,'明确来源')['rows'][0]
        self.assertEqual(old['N_RKg1'],2);self.assertEqual(fixed['N_RKg1'],1)
        self.assertEqual(old['NRate1'],200);self.assertEqual(fixed['NRate1'],100)
        self.assertIsNone(old['FARKg1']);self.assertEqual(fixed['FARKg1'],3)

    def test_comparison_inner_join_empty_month_is_reported_in_supplement(self):
        data=comparison(self.at,self.at,'05','legacy',[],'')
        self.assertEqual(data['rows'],[]);self.assertEqual(data['supplemental_rows'][0]['month'],'2026-08')

    def test_comparison_legacy_last_far_requires_current_far_join_in_multi_year_range(self):
        self.work()
        start=self.at.replace(year=2025)
        inputs=[self.far(sheet_date=start)]
        result=comparison(start,self.at,'06','legacy',inputs,'跨年原来源')['rows']
        self.assertIsNone(result[0]['FARKg1'])
        result=comparison(start,self.at,'06','same_period',inputs,'跨年原来源')['rows']
        self.assertEqual(result[0]['FARKg1'],1)

    def test_comparison_leap_day_sql_year_shift(self):
        value=self.at.replace(year=2024,month=2,day=29)
        self.assertEqual(previous_year(value),value.replace(year=2023,day=28))

    def test_comparison_legacy_supplement_keeps_actual_prior_rows_and_period(self):
        current=self.work('CURRENT',dosage=None)
        previous=self.work('OLD',at=self.at.replace(year=2025),dosage=None)
        data=comparison(self.at,self.at,'06','legacy',[],'')
        identities={(row['period'],row['record_id']) for row in data['supplemental_rows']}
        self.assertEqual(identities,{('current',current.pk),('previous',previous.pk)})

    def test_responsibility_all_departments_and_shifts(self):
        inputs=[]
        for index,(dept,shift) in enumerate([('07','03'),('07','08'),('02','05'),('04','08'),('12','01'),('14','01'),('99','01')]):
            number=str(index);self.job(number,number);self.defect(number,dept,shift=shift)
            inputs.append(self.far(job_number=number,metres=Decimal(10000)))
        row=responsibility(self.at,self.at,inputs,'来源')['rows'][0]
        for name in ['JQty1','YQty1','JQty2','YQty2','Qty3','Qty4','Qty5']:self.assertEqual(row[name],1)
        self.assertEqual(row['AllQty'],7);self.assertEqual(row['AllMeter'],7)

    def test_responsibility_missing_current_premeter_stays_null(self):
        self.job();self.defect(dept='07')
        row=responsibility(self.at,self.at,[self.far(quantity=Decimal(-2000))],'无原长度')['rows'][0]
        self.assertEqual(row['JQty1'],-2);self.assertIsNone(row['JMeter1']);self.assertIsNone(row['AllMeter'])

    def test_responsibility_duplicate_jobs_and_reviews_are_all_joined(self):
        self.job();self.job();self.defect();self.defect()
        data=responsibility(self.at,self.at,[self.far()],'原重复关系')
        self.assertEqual(len(data['result_rows']),4);self.assertEqual(data['rows'][0]['AllQty'],4)

    def test_responsibility_unknown_department_class_and_nonzero_amount_not_lost(self):
        self.job();self.defect(dept=None,shift=None)
        data=responsibility(self.at,self.at,[self.far(),self.far(zero_amount=False),self.far(sheet_date=None)],'来源')
        self.assertEqual(len(data['supplemental_rows']),3);self.assertIsNone(data['rows'][0]['AllQty'])

    def test_reports_respect_scoped_review_rows(self):
        self.job();self.defect();self.work()
        def scoped(name,module):return reader(name,module).none() if name=='WDefect' else reader(name,module)
        self.assertEqual(daily(self.at.date(),scoped)['rows'],[])
        self.assertIsNone(responsibility(self.at,self.at,[self.far()],'来源',scoped)['rows'][0]['AllQty'])

    def test_extended_api_all_reports_and_far_source_reference(self):
        root='/api/system/erp_quality_sourcedyewdefect/'
        response=self.client.post(root+'rework_daily/',{'as_of':'2026-08-15'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        for name in ['Sp_ReworkCloth4','Rework_Comparison1','Rework_Comparison2','Rework_Comparison3']:
            response=self.client.post(root+'rework_extended/',{'start':self.at.isoformat(),'end':self.at.isoformat(),'report':name},format='json')
            self.assertEqual(response.status_code,200,response.data);self.assertEqual(response.data['data']['report'],name)
        response=self.client.post(root+'rework_extended/',{'start':self.at.isoformat(),'end':self.at.isoformat(),
            'report':'Sp_ReworkCloth4','far_rows':[self.far()]},format='json')
        self.assertEqual(response.status_code,400,response.data)


class FollowupPurchaseTests(TestCase):
    def setUp(self):
        self.actor=Users.objects.create_superuser(username='followup',password='test')
        self.client=APIClient();self.client.force_authenticate(self.actor)
        self.at=timezone.make_aware(datetime(2026,10,15,12));self.event={'at':self.at,'reason':'实际后续业务'}
    def model(self,name,module='erp_warehouse'):return apps.get_model(module+'.SourceDye'+name)
    def old(self,name,module='erp_warehouse',**values):
        row=self.model(name,module).objects.create(**values);row.refresh_from_db();return row
    def setup_chain(self,family='Gray'):
        table='OutWorkApply' if family=='Gray' else 'SemiOutWorkApply'
        app=self.old(table,'erp_production',old_sheet_series='A',old_sheet_no='A')
        line=self.old(table+'Detail','erp_production',old_sheet_series='A',old_detail_no='A1',source_parent_1=app)
        sent=dispatch(line,self.actor,quantity=10,rolls=1,warehouse='W',unit=1,sheet_kind=32,happened_at=self.at,job_number=None)
        out=self.model(family+'OutDetail').objects.get(source_parent_1=sent)
        received=receive_product(out,self.actor,quantity=8,rolls=1,warehouse='W',unit=1,sheet_kind=14,happened_at=self.at,job_number=None)
        close(app,self.actor,[out],[received],[],self.at,'初次结案')
        return app,out,received

    def test_after_close_receipt_allowed_marks_review_and_keeps_original_snapshot(self):
        for family in ['Gray','Semi']:
            app,out,received=self.setup_chain(family);before=closure(app)['reconciliation']
            target=receive_product(out,self.actor,quantity=-2,rolls=None,warehouse='W',unit=1,sheet_kind=14,happened_at=self.at,job_number=None)
            value=closure(app);self.assertEqual(value['state'],'needs_review');self.assertEqual(value['reconciliation'],before)
            data=review(app,reader);self.assertTrue(any(row['after_closure'] and row['record_id']==target.pk for row in data['rows']))

    def test_material_and_product_returns_reclose_net_quantities_and_version(self):
        app,out,received=self.setup_chain()
        back=return_material(out,self.actor,weight=1,length=None,rolls=0,warehouse='W',unit=1,sheet_kind=16,customer='C',**self.event)
        backline=self.model('GrayInDetail').objects.get(source_parent_1=back)
        returned=dispatch_product(received,self.actor,weight=2,length=None,rolls=0,warehouse='W',sheet_kind=22,
            purpose='factory_return',receiver='F',price=None,records=[],**self.event)
        returnline=self.model('ProdOutDetail').objects.get(source_parent_1=returned)
        result=close(app,self.actor,[out],[received],[],self.at,'重新核对',returned_material=[backline],returned_product=[returnline])
        row=next(row for row in result['rows'] if row['measure']=='WeightQty')
        self.assertEqual(row['net_dispatched'],9);self.assertEqual(row['net_received'],6);self.assertEqual(row['difference'],3)
        self.assertIsNone(row['confirmed_loss']);self.assertEqual(closure(app)['state'],'closed')
        self.assertEqual(review(app,reader)['closure_versions'],2)
        self.assertFalse(any(row['after_closure'] for row in review(app,reader)['rows']))

    def test_reopen_needs_review_retains_previous_loss(self):
        app,out,received=self.setup_chain()
        receive_product(out,self.actor,quantity=None,rolls=None,warehouse='W',unit=1,sheet_kind=99,happened_at=self.at,job_number=None)
        value=reopen(app,self.actor,'复核');self.assertEqual(value['state'],'open');self.assertEqual(value['losses'],[])

    def test_legacy_selected_dispatch_without_origin_still_tracks_new_receipt(self):
        app=self.old('OutWorkApply','erp_production',old_sheet_series='A')
        line=self.old('GrayOutDetail',old_assigned_no='OLD',old_sheet_series='UNKNOWN')
        close(app,self.actor,[line],[],[],self.at,'原明确选择')
        receive_product(line,self.actor,quantity=1,rolls=1,warehouse='W',unit=1,sheet_kind=14,happened_at=self.at,job_number=None)
        self.assertEqual(closure(app)['state'],'needs_review')

    def test_after_close_source_change_detected_without_overwriting_snapshot(self):
        app,out,received=self.setup_chain()
        self.model('ProdIn').objects.filter(pk=received.pk).update(old_weight_qty=99)
        data=review(app,reader);self.assertEqual(data['closure_state'],'needs_review')
        self.assertEqual(data['supplemental_rows'][0]['changed_fields'],['old_weight_qty'])
        self.assertEqual(Decimal(closure(app)['reconciliation']['sources'][1]['source']['old_weight_qty']),Decimal('8'))

    def test_null_return_and_unknown_units_are_not_summed_as_zero(self):
        app,out,received=self.setup_chain()
        head=self.old('GrayIn',old_sheet_series='NULL',old_stock_unit=1)
        line=self.old('GrayInDetail',old_sheet_series='NULL',old_rece_sheet_no='NULL',old_weight_qty=None,source_parent_1=head)
        data=close(app,self.actor,[out],[received],[],self.at,'空量退回',returned_material=[line])
        row=next(row for row in data['rows'] if row['measure']=='WeightQty')
        self.assertIsNone(row['material_return']);self.assertIsNone(row['difference'])

    def test_header_unit_change_detected_and_original_unit_retained(self):
        app,out,received=self.setup_chain()
        self.model('GrayOut').objects.filter(pk=out.source_parent_1_id).update(old_stock_unit=2)
        data=review(app,reader)
        self.assertEqual(data['closure_state'],'needs_review')
        self.assertEqual(data['supplemental_rows'][0]['changed_fields'],['old_stock_unit'])
        self.assertEqual(closure(app)['reconciliation']['sources'][0]['unit'],1)

    def test_followup_query_respects_visible_targets(self):
        app,out,received=self.setup_chain()
        data=review(app,lambda table,module:reader(table,module).none())
        self.assertEqual(data['rows'],[])
        self.assertEqual(data['closure_state'],'needs_review')
        self.assertTrue(all('changed_fields' not in row for row in data['supplemental_rows']))

    def test_purchase_raw_return_both_families_actual_signed_stock_and_source(self):
        for family in ['Gray','Semi']:
            row=self.old(family+'InDetail',old_sheet_series='OLD',old_rece_sheet_no='R',old_pur_detail_no='P',old_price=2,old_weight_qty=10,source_batch=historical_batch())
            before=snapshot(row)
            head=return_raw_purchase(row,self.actor,weight=Decimal('-3'),length=None,rolls=-1,warehouse='W',unit=1,supplier='S',receipt_number='NEW-RETURN',**self.event)
            line=type(row).objects.get(source_parent_1=head)
            self.assertEqual(line.old_ori_rece_sheet_no,'R');self.assertEqual(line.old_pur_detail_no,'P')
            self.assertEqual(line.old_weight_qty,-3);self.assertIsNone(line.old_length_qty)
            book=self.model(family+'StockBook').objects.get(old_sheet_series=head.old_sheet_series)
            self.assertEqual(book.old_in_weight_qty,-3);self.assertEqual(book.old_supplier_id,'S')
            row.refresh_from_db();self.assertEqual(snapshot(row),before)
            self.assertEqual(view_effects(head)['purchase_return_origin']['source']['source_batch'],historical_batch().pk)
            self.assertEqual(view_effects(head)['purchase_return_origin']['source']['id'],row.pk)

    def test_purchase_other_kind_and_orphan_receipts_all_visible(self):
        item=self.old('PurDetail','erp_purchase',old_detail_no='P')
        head=self.old('GrayIn',old_sheet_series='R',old_sheet_kind=99,old_stock_unit=None)
        self.old('GrayInDetail',old_rece_sheet_no='R1',old_sheet_series='R',old_pur_detail_no='P',old_weight_qty=-2)
        self.old('SemiInDetail',old_rece_sheet_no='R2',old_sheet_series='MISSING',old_pur_detail_no='P',old_weight_qty=None)
        data=raw_receipts(item,reader)['rows'];self.assertEqual(len(data),2)
        self.assertEqual(data[0]['SheetKind'],99);self.assertTrue(data[1]['missing_header'])

    def test_api_purchase_return_followup_and_reclose_fields(self):
        item=self.old('GrayInDetail',old_rece_sheet_no='R',old_sheet_series='R')
        response=self.client.post(f'/api/system/erp_warehouse_sourcedyegrayindetail/{item.pk}/return_raw_purchase/',
            {'weight':'-1','at':self.at.isoformat(),'reason':'原退货','receipt_number':'NEW-RETURN'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        app,out,received=self.setup_chain();root=f'/api/system/erp_production_sourcedyeoutworkapply/{app.pk}/'
        response=self.client.post(root+'review_followup/',{},format='json');self.assertEqual(response.status_code,200,response.data)
        response=self.client.post(root+'close_outwork/',{'dispatched':[out.pk],'received':[received.pk],
            'returned_material':[],'returned_product':[],'losses':[],'closed_at':self.at.isoformat(),'reason':'重新结案'},format='json')
        self.assertEqual(response.status_code,200,response.data)
