from plugins.erp_base.tests.source_fixtures import historical_batch
from datetime import datetime, timedelta
from decimal import Decimal
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.business import snapshot
from plugins.erp_base.source_context import SourceDocumentContext
from plugins.erp_base.source_continuation import view_effects, save_effect
from plugins.erp_base.source_cross_card import reprocess, issue_receipt, transfer_issue, reprocess_links
from plugins.erp_base.source_chain_reverse import discover, cancel, undo, reader
from plugins.erp_base.source_card_reverse import reverse_card
from plugins.erp_base.source_job_flow import merge_cards
from plugins.erp_base.source_purchase_flow import receive_material, return_purchase, material_receipts
from plugins.erp_base.source_outwork_flow import dispatch, receive_product
from plugins.erp_base.source_outwork_trace import trace
from plugins.erp_base.source_delivery_flow import factory_quality, return_material
from plugins.erp_base.source_rework_reports import statistics


class CrossCardTests(TestCase):
    def setUp(self):
        self.actor=Users.objects.create_superuser(username='cross-card',password='test')
        self.client=APIClient();self.client.force_authenticate(self.actor)
        self.at=timezone.make_aware(datetime(2026,10,15,12))
        self.event={'at':self.at,'reason':'跨卡实际接续验收'}
        self.move=dict(weight=Decimal('-2.5'),length=None,rolls=Decimal('1.5'),warehouse='W',unit=1,sheet_kind=34,**self.event)

    def model(self,name,module='erp_warehouse'):return apps.get_model(module+'.SourceDye'+name)
    def old(self,name,module='erp_warehouse',**values):
        row=self.model(name,module).objects.create(**values);row.refresh_from_db();return row
    def job(self,number='J',**values):
        return self.old('JobSheet','erp_production',old_sheet_no=number,old_sheet_series=number,
            old_pre_vat_qty=100,old_pre_rolls=10,old_assign_unit=1,source_batch=historical_batch(),**values)
    def redo(self,job,review=None,processes=()):
        return reprocess(job,self.actor,review,Decimal('-3'),None,1,10,'02',processes,**self.event)
    def cancel(self,job,query=reader):
        return cancel(job,self.actor,mode='execution_only',work_mode='trigger_then_maintenance',query=query,**self.event)
    def purchase(self,entry='StuffIn',quantity=Decimal('-2')):
        item=self.old('PurApplyDetail','erp_purchase',old_sheet_series='PA',old_detail_no='D',old_qty=40,
            old_price=3,old_stuff_id='DYE',old_article_id='PART',old_stuff_unit='KG',old_article_unit='BOX',source_batch=historical_batch())
        head=receive_material(item,self.actor,entry,quantity,'W','SUP',12,**self.event)
        line=self.model(head.SOURCE_TABLE+'Detail').objects.get(source_parent_1=head)
        return item,head,line
    def transfer(self,table='GrayOutDetail',source_number='J',target_number='T'):
        source=self.job(source_number);target=self.job(target_number)
        line=self.old(table,old_sheet_series='OLD',old_job_sheet_no=source_number,old_weight_qty=8,old_price=2,source_batch=historical_batch(),
            **({'old_assigned_no':'D'} if table=='GrayOutDetail' else {'old_detail_no':'D'}))
        values={key:value for key,value in self.move.items() if key!='sheet_kind'}
        result=transfer_issue(line,self.actor,source,target,return_kind=16,issue_kind=34,customer='C',issue_number='NEW-1',**values)
        return source,target,line,result

    def test_reprocess_preserves_source_plan_and_actuals_and_uses_review(self):
        job=self.job(old_sum_process_weight_qty=55,old_pkg=30)
        review=self.old('WDefect','erp_quality',old_sheet_no='REVIEW',old_sheet_series='Q',old_kind='未知类别',source_batch=historical_batch())
        before=snapshot(job);target=self.redo(job,review)
        job.refresh_from_db();self.assertEqual(snapshot(job),before)
        self.assertEqual((target.old_loss_str,target.old_sheet_kind,target.old_job_kind_id),('REVIEW',10,'02'))
        self.assertEqual(target.old_pre_vat_qty,-3);self.assertIsNone(target.old_sum_process_weight_qty)
        self.assertIsNone(target.old_pkg);self.assertIsNone(target.source_batch_id)
        self.assertEqual(view_effects(target)['card_adoption']['review']['source']['source_batch'],historical_batch().pk)
        self.assertEqual(view_effects(target)['card_adoption']['review']['source']['id'],review.pk)

    def test_reprocess_route_has_theory_but_no_execution(self):
        job=self.job()
        route=self.old('JobProcess','erp_production',old_sheet_series='J',old_process_no=7,old_process_id='RARE',
            old_theory_value01='15',old_actual_value01='12',old_wprocess_no='OLD',old_status='1')
        target=self.redo(job,processes=[route])
        new=self.model('JobProcess','erp_production').objects.get(source_parent_1=target)
        self.assertEqual(new.old_theory_value01,'15');self.assertIsNone(new.old_actual_value01)
        self.assertIsNone(new.old_wprocess_no);self.assertEqual(new.old_status,'0')

    def test_reprocess_without_review_and_reverse_does_not_credit_source(self):
        job=self.job();target=self.redo(job)
        self.assertIsNone(target.old_loss_str)
        reverse_card(target,self.actor,'unstarted',**self.event)
        job.refresh_from_db();target.refresh_from_db()
        self.assertEqual(job.old_pre_vat_qty,100);self.assertEqual(target.old_pre_vat_qty,0)

    def test_same_number_parent_uses_explicit_reprocess_id(self):
        job=self.job();other=self.job();target=self.redo(job)
        self.assertEqual([row.pk for row in reprocess_links(job,reader)],[target.pk])
        self.assertTrue(discover(job)['issues']);self.assertFalse(discover(other)['issues'])

    def test_merge_nonfirst_member_has_child_dependency(self):
        first=self.job();second=self.job('B')
        target=merge_cards(first,self.actor,[second],10,1,1,self.at,'合卡',[])
        self.assertIn(target.pk,[row.pk for row in reprocess_links(second,reader)])
        with self.assertRaises(ValidationError):self.cancel(second)
        self.cancel(target);self.cancel(second)

    def test_hidden_child_cannot_be_bypassed_by_scoped_reverse(self):
        job=self.job();child=self.redo(job)
        def scoped(name,module):
            query=reader(name,module)
            return query.exclude(pk=child.pk) if name=='JobSheet' else query
        with self.assertRaises(ValidationError):self.cancel(job,query=scoped)

    def test_actual_issue_both_families_keeps_negative_null_and_old_row(self):
        job=self.job()
        for family in ['Gray','Semi']:
            row=self.old(family+'InDetail',old_sheet_series=family,old_rece_sheet_no=family,old_weight_qty=99,old_price=2,source_batch=historical_batch())
            before=snapshot(row);head=issue_receipt(row,self.actor,job,**self.move)
            line=self.model(family+'OutDetail').objects.get(source_parent_1=head)
            self.assertEqual(line.old_weight_qty,Decimal('-2.5'));self.assertIsNone(line.old_length_qty)
            self.assertEqual(line.old_amount,-5);self.assertEqual(line.old_job_sheet_no,'J')
            row.refresh_from_db();self.assertEqual(snapshot(row),before)
            self.assertEqual(view_effects(head)['cross_card_issue']['source']['source']['source_batch'],historical_batch().pk)
            self.assertEqual(view_effects(head)['cross_card_issue']['source']['source']['id'],row.pk)

    def test_issue_to_reversed_plan_rolls_back(self):
        target=self.redo(self.job());reverse_card(target,self.actor,'unstarted',**self.event)
        row=self.old('GrayInDetail',old_sheet_series='R',old_rece_sheet_no='R')
        with self.assertRaises(ValidationError):issue_receipt(row,self.actor,target,**self.move)
        self.assertEqual(self.model('GrayOut').objects.count(),0)

    def test_transfer_creates_return_and_issue_without_changing_old_source(self):
        for family in ['Gray','Semi']:
            source,target,line,head=self.transfer(family+'OutDetail',family+'S',family+'T')
            fact=view_effects(head)['cross_card_transfer'];returned=self.model(family+'In').objects.get(pk=fact['return']['source']['id'])
            incoming=self.model(family+'InDetail').objects.get(source_parent_1=returned)
            self.assertEqual(incoming.old_weight_qty,Decimal('-2.5'))
            line.refresh_from_db();self.assertEqual(line.old_weight_qty,8);self.assertEqual(line.source_batch_id,historical_batch().pk)
            self.assertIsNone(head.source_batch_id);self.assertEqual(returned.old_customer_id,'C')
            self.assertIn(target.pk,[row['record_id'] for row in discover(source)['issues']])

    def test_transfer_inverse_requires_downstream_first_and_restore_upstream_first(self):
        source,target,line,head=self.transfer()
        with self.assertRaises(ValidationError):self.cancel(source)
        self.cancel(target);self.cancel(source)
        with self.assertRaises(ValidationError):undo(target,self.actor,**self.event)
        undo(source,self.actor,**self.event);undo(target,self.actor,**self.event)
        self.assertEqual(view_effects(target)['execution_chain']['state'],'reversed')

    def test_duplicate_job_number_explicit_issue_is_not_cancelled_by_other_card(self):
        first=self.job();second=self.job()
        row=self.old('GrayInDetail',old_sheet_series='R',old_rece_sheet_no='R')
        head=issue_receipt(row,self.actor,second,**self.move)
        line=self.model('GrayOutDetail').objects.get(source_parent_1=head)
        self.assertNotIn((line._meta.label,line.pk),discover(first)['nodes'])
        self.assertIn((line._meta.label,line.pk),discover(second)['nodes'])

    def test_all_four_purchase_entries_create_source_links_and_original_quantity(self):
        for entry in ['StuffIn','SmallStuffIn','ArticleIn','FabricArticleIn']:
            item,head,line=self.purchase(entry)
            self.assertEqual(line.old_pur_detail_no,'D')
            self.assertEqual(getattr(line,'old_qty' if head.SOURCE_TABLE=='StuffIn' else 'old_in_qty'),-2)
            self.assertEqual(line.old_amount,-6)
            self.assertEqual(head.old_supplier_id,'SUP')
            self.assertEqual(view_effects(head)['purchase_origin']['source']['source_batch'],historical_batch().pk)
            self.assertEqual(view_effects(head)['purchase_origin']['source']['id'],item.pk)
            item.refresh_from_db();self.assertEqual(item.old_qty,40)

    def test_purchase_null_quantity_not_replaced_with_plan(self):
        for entry in ['StuffIn','ArticleIn']:
            item,head,line=self.purchase(entry,None)
            self.assertIsNone(getattr(line,'old_qty' if entry=='StuffIn' else 'old_in_qty'))
            self.assertIsNone(line.old_amount)

    def test_purchase_return_families_keep_different_signed_rules(self):
        for entry,expected in [('StuffIn',Decimal('-2')),('ArticleIn',Decimal('2'))]:
            item,head,line=self.purchase(entry)
            returned=return_purchase(line,self.actor,Decimal('-2'),'W','SUP',**self.event)
            new=type(line).objects.get(source_parent_1=returned)
            self.assertEqual(returned.old_sheet_kind,16)
            self.assertEqual(getattr(new,'old_ori_in_detail_no' if entry=='StuffIn' else 'old_ori_detail_no'),line.old_detail_no)
            data=material_receipts(item,reader)['rows']
            self.assertEqual(next(row for row in data if row['record_id']==new.pk and row['entity']==new._meta.label)['stock_quantity_rule'],expected)
            self.assertEqual(view_effects(returned)['purchase_return_origin']['source']['id'],line.pk)
            book=self.model('StuffStockBook' if entry=='StuffIn' else 'ArticleStockBook').objects.get(old_sheet_series=returned.old_sheet_series)
            self.assertEqual(book.old_in_qty,expected)
            self.assertEqual(book.old_in_money,expected*3)
            self.assertEqual(book.old_ware_house_id,'W')

    def test_purchase_report_keeps_duplicate_and_missing_headers(self):
        item=self.old('PurApplyDetail','erp_purchase',old_detail_no='P',old_stuff_unit='KG')
        for unused in range(2):self.old('StuffIn',old_sheet_series='D',old_sheet_kind=16)
        self.old('StuffInDetail',old_sheet_series='D',old_detail_no='D',old_pur_detail_no='p ',old_qty=-5)
        self.old('StuffInDetail',old_sheet_series='MISSING',old_detail_no='M',old_pur_detail_no='P',old_qty=None)
        data=material_receipts(item,reader)['rows']
        self.assertEqual(len(data),3);self.assertEqual(sum(row['missing_header'] for row in data),1)
        self.assertEqual([row['stock_quantity_rule'] for row in data if not row['missing_header']],[-5,-5])

    def test_purchase_report_respects_scope_and_excludes_cancelled(self):
        item,head,line=self.purchase()
        from plugins.erp_base.source_quality_reports import rows
        save_effect(line,'chain_cancelled',{'active':True},self.actor,'原单留档')
        self.assertEqual(material_receipts(item,rows)['rows'],[])
        self.assertEqual(len(material_receipts(item,reader)['rows']),1)

    def outwork(self):
        app=self.old('OutWorkApply','erp_production',old_sheet_series='A',old_sheet_no='A')
        line=self.old('OutWorkApplyDetail','erp_production',old_sheet_series='A',old_detail_no='D',source_parent_1=app)
        sent=dispatch(line,self.actor,quantity=2,rolls=1,warehouse='W',unit=1,sheet_kind=32,happened_at=self.at,job_number='J')
        detail=self.model('GrayOutDetail').objects.get(source_parent_1=sent)
        received=receive_product(detail,self.actor,quantity=-1,rolls=None,warehouse='W',unit=1,sheet_kind=14,happened_at=self.at,job_number=None)
        return app,detail,received

    def test_outwork_trace_follows_actual_and_quality_without_exposing_review_snapshot(self):
        app,line,received=self.outwork()
        review=self.old('WDefect','erp_quality',old_sheet_no='SECRET')
        factory_quality(received,self.actor,'F','concession',review,self.at,'让步')
        returned=return_material(line,self.actor,customer='C',**self.move)
        data=trace(app,reader)
        self.assertIn((received._meta.label,received.pk),[(row['entity'],row['record_id']) for row in data['rows']])
        self.assertIn(returned.pk,[row['record_id'] for row in data['rows'] if row['entity']==returned._meta.label])
        quality=next(row['factory_quality'] for row in data['rows'] if row['entity']==received._meta.label)
        self.assertEqual(quality['result'],'concession');self.assertNotIn('SECRET',str(quality))

    def test_outwork_orphans_and_retained_rows_visible(self):
        app,line,received=self.outwork()
        orphan=self.old('OutWorkApplyDetail','erp_production',old_sheet_series='A',old_detail_no='UNMATCHED')
        save_effect(received,'chain_cancelled',{'active':True},self.actor,'留档')
        data=trace(app,reader)
        self.assertIn(orphan.pk,[row['record_id'] for row in data['supplemental_rows']])
        row=next(row for row in data['rows'] if row['entity']==received._meta.label)
        self.assertFalse(row['active'])

    def test_outwork_receipt_without_job_number_included_in_source_card_reverse(self):
        job=self.job();app,line,received=self.outwork()
        self.assertIn((received._meta.label,received.pk),discover(job)['nodes'])

    def test_api_reprocess(self):
        job=self.job();payload={'at':self.at.isoformat(),'reason':'API验收'}
        response=self.client.post(f'/api/system/erp_production_sourcedyejobsheet/{job.pk}/reprocess/',
            {**payload,'sheet_kind':10,'processes':[]},format='json')
        self.assertEqual(response.status_code,200,response.data)

    def test_number_failure_rolls_back_return_and_new_issue_together(self):
        source=self.job();target=self.job('T')
        line=self.old('GrayOutDetail',old_assigned_no='NONNUMERIC',old_sheet_series='OLD',old_job_sheet_no='J')
        values={key:value for key,value in self.move.items() if key!='sheet_kind'}
        with self.assertRaises(ValidationError):
            transfer_issue(line,self.actor,source,target,return_kind=16,issue_kind=34,customer='C',**values)
        self.assertEqual(self.model('GrayIn').objects.count(),0);self.assertEqual(self.model('GrayOut').objects.count(),0)
        line.refresh_from_db();self.assertEqual(line.old_assigned_no,'NONNUMERIC')

    def test_api_transfer_trace_and_purchase_readonly_reports(self):
        source=self.job();target=self.job('T')
        line=self.old('GrayOutDetail',old_assigned_no='UNUSUAL',old_sheet_series='OLD',old_job_sheet_no='J')
        response=self.client.post(f'/api/system/erp_warehouse_sourcedyegrayoutdetail/{line.pk}/transfer_to_job/',
            {'source_job':source.pk,'target':target.pk,'issue_number':'NEW-1','return_kind':16,'issue_kind':34,
                'at':self.at.isoformat(),'reason':'罕见编号接续','weight':'-1'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        app=self.old('SemiOutWorkApply','erp_production',old_sheet_series='A')
        response=self.client.post(f'/api/system/erp_production_sourcedyesemioutworkapply/{app.pk}/trace_outwork/',{},format='json')
        self.assertEqual(response.status_code,200,response.data)
        item,head,line=self.purchase()
        response=self.client.post(f'/api/system/erp_purchase_sourcedyepurapplydetail/{item.pk}/material_receipts/',{},format='json')
        self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(len(response.data['data']['rows']),1)

    def test_api_issue_and_purchase_actions(self):
        job=self.job();payload={'at':self.at.isoformat(),'reason':'API验收'}
        incoming=self.old('SemiInDetail',old_sheet_series='I',old_rece_sheet_no='I')
        response=self.client.post(f'/api/system/erp_warehouse_sourcedyesemiindetail/{incoming.pk}/issue_to_job/',
            {**payload,'target':job.pk,'sheet_kind':36},format='json')
        self.assertEqual(response.status_code,200,response.data)
        item,head,line=self.purchase()
        response=self.client.post(f'/api/system/erp_purchase_sourcedyepurapplydetail/{item.pk}/receive_material/',
            {**payload,'entry':'ArticleIn','sheet_kind':12},format='json')
        self.assertEqual(response.status_code,200,response.data)
        response=self.client.post(f'/api/system/erp_warehouse_sourcedyestuffindetail/{line.pk}/return_purchase/',payload,format='json')
        self.assertEqual(response.status_code,200,response.data)


class ReworkReportTests(TestCase):
    def setUp(self):self.at=timezone.make_aware(datetime(2026,10,15,12))
    def old(self,name,module,**values):return apps.get_model(module+'.SourceDye'+name).objects.create(**values)
    def work(self,code='W',station='05',**values):
        return self.old('WProcess','erp_production',old_wprocess_no=code,old_station_id=station,
            old_job_sheet_no='J',old_create_date=self.at,**values)
    def review(self,kind='内部评审',**values):
        return self.old('WDefect','erp_quality',old_sheet_no='Q',old_kind=kind,old_defect_dept='07',**values)
    def job(self):return self.old('JobSheet','erp_production',old_sheet_no='J',old_loss_str='Q',old_prod_id='G')
    def report(self,station='05',**values):return statistics(self.at,self.at,station,**values)

    def test_weighted_rounded_kg_to_tonnes_and_same_day_month(self):
        self.job();self.review();self.work(old_curr_dosage=50,old_curr_kg=2000)
        data=self.report();self.assertEqual(data['rows'],[dict(month='2026-10',AllNum=1,AllKg=Decimal('1.00'),N_Num=1,K_Num=0,N_RKg=Decimal('1.00'),K_RKg=0)])

    def test_negative_null_and_nonpositive_dosage_preserved(self):
        self.job();self.review()
        self.work('A',old_curr_dosage=100,old_curr_kg=-1000)
        self.work('B',old_curr_dosage=100,old_curr_kg=None)
        self.work('C',old_curr_dosage=0,old_curr_kg=1000)
        self.work('D',old_curr_dosage=None,old_curr_kg=1000)
        data=self.report();row=data['rows'][0]
        self.assertEqual(row['AllNum'],4);self.assertEqual(row['AllKg'],-1);self.assertEqual(row['N_Num'],2)
        self.assertEqual(row['N_RKg'],-1);self.assertEqual(len(data['supplemental_rows']),2)

    def test_duplicate_work_number_cross_station_join_and_review_multiplicity(self):
        self.job();self.review();self.review('客退评审')
        self.work('SAME','05',old_curr_dosage=100,old_curr_kg=1000)
        self.work('same ','06',old_curr_dosage=100,old_curr_kg=2000)
        a,b=self.report('05'),self.report('06')
        for result in [a,b]:
            self.assertEqual(result['rows'][0]['AllNum'],4)
            self.assertEqual(result['rows'][0]['N_Num'],2);self.assertEqual(result['rows'][0]['N_RKg'],3)
        self.assertEqual(a['rows'][0]['AllKg'],4);self.assertEqual(b['rows'][0]['AllKg'],8)

    def test_dictionary_duplicates_not_deduplicated(self):
        self.job();self.review();self.work(old_curr_dosage=100,old_curr_kg=1000)
        self.old('PGray','erp_base',old_gray_id='G',old_fabric_kind_id='F')
        for unused in range(2):self.old('PFieldValid','erp_base',old_field_type='FabricKind',old_code='F')
        self.assertEqual(self.report()['rows'][0]['AllNum'],2)

    def test_unknown_kind_classifies_zero_and_empty_work_number_is_preserved(self):
        self.job();self.review('罕见评审')
        self.work(old_curr_dosage=100,old_curr_kg=1000)
        self.work('',old_curr_dosage=100,old_curr_kg=1000)
        result=self.report();self.assertEqual(result['rows'][0]['AllNum'],2)
        self.assertEqual(result['rows'][0]['N_Num'],0)
        self.assertEqual(result['result_rows'][1]['WProcessNo'],'')
        self.assertEqual(result['result_rows'][1]['repair_source']['Kind'],'罕见评审')

    def test_calendar_empty_months_and_end_inclusive(self):
        self.work(old_curr_dosage=100,old_curr_kg=1000)
        result=statistics(self.at.replace(month=9),self.at,'05')
        self.assertEqual([row['month'] for row in result['rows']],['2026-09','2026-10'])
        self.assertIsNone(result['rows'][0]['AllNum']);self.assertEqual(result['rows'][1]['AllNum'],1)
        self.assertIsNone(statistics(self.at-timedelta(days=1),self.at-timedelta(seconds=1),'05')['rows'][0]['AllNum'])

    def test_scoped_reviews_are_not_leaked_into_report(self):
        self.job();self.review();self.work(old_curr_dosage=100,old_curr_kg=1000)
        def scoped(name,module):
            query=reader(name,module)
            return query.none() if name=='WDefect' else query
        result=self.report(query=scoped)
        self.assertIsNone(result['rows'][0]['N_Num']);self.assertEqual(len(result['supplemental_rows']),1)

    def test_api_rework_report_collection(self):
        actor=Users.objects.create_superuser(username='report',password='test')
        client=APIClient();client.force_authenticate(actor)
        response=client.post('/api/system/erp_quality_sourcedyewdefect/rework_statistics/',
            {'start':self.at.isoformat(),'end':self.at.isoformat(),'station':'06'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(response.data['data']['report'],'Sp_ReworkCloth3')
