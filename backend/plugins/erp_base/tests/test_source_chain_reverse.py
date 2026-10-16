from plugins.erp_base.tests.source_fixtures import historical_batch
from datetime import datetime,timedelta
from decimal import Decimal
from django.apps import apps
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db.models import Sum
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.business import snapshot
from plugins.erp_base.source_chain_reverse import discover,preview,cancel,undo
from plugins.erp_base.source_execution_state import active,require_available
from plugins.erp_base.source_continuation import save_effect,origin
from plugins.erp_base.source_context import SourceDocumentContext
from plugins.erp_base import source_services


class ExecutionChainTests(TestCase):
    def setUp(self):
        self.actor=Users.objects.create_superuser(username='chain-reverse',password='test')
        self.client=APIClient();self.client.force_authenticate(self.actor)
        self.at=timezone.make_aware(datetime(2026,10,15,10))
        self.event={'at':self.at,'reason':'整链撤销验收'}
        self.job=self.old('JobSheet','erp_production',old_sheet_series='JS',old_sheet_no='JOB',old_sheet_status=0,
            old_pre_rolls=5,old_pre_vat_qty=20,source_batch=historical_batch())

    def model(self,name,module='erp_warehouse'):return apps.get_model(module+'.SourceDye'+name)
    def old(self,name,module='erp_warehouse',**values):
        row=self.model(name,module).objects.create(**values);row.refresh_from_db();return row
    def execute(self,**extra):
        values=dict(mode='execution_only',work_mode='trigger_then_maintenance',**self.event);values.update(extra)
        return cancel(self.job,self.actor,**values)
    def book(self,table='ProdStockBook',series='IN',**values):
        return self.old(table,old_book_no=100+self.model(table).objects.count(),old_sheet_series=series,
            old_ware_house_id='WH',old_lot_no='LOT',old_storage_unit_ids='BIN',source_batch=historical_batch(),**values)
    def inbound(self):return self.old('ProdIn',old_sheet_series='IN',old_sheet_no='PI',old_job_sheet_no='JOB',old_rolls=5,old_weight_qty=20,source_batch=historical_batch())
    def work(self):
        process=self.old('JobProcess','erp_production',old_sheet_series='JS',old_process_no=1,old_process_id='GX07',
            old_status='1',old_start_time=self.at,old_end_time=self.at,old_station_id='06')
        work=self.old('WProcess','erp_production',old_wprocess_no='W',old_job_sheet_no='JOB',old_process_id='GX07',
            old_process_no=1,old_status='1',old_station_id='06',old_class_id='03',old_end_time=self.at,old_curr_kg=-2,source_batch=historical_batch())
        return process,work

    def test_preview_readonly_and_complete_old_ids(self):
        inbound=self.inbound();book=self.book(old_in_weight_qty=-2,old_out_weight_qty=None)
        before=SourceDocumentContext.objects.count();data=preview(self.job)
        self.assertTrue(any(row['record_id']==inbound.pk and row['source']['batch_id']==historical_batch().pk for row in data['rows']))
        self.assertEqual(data['result_rows'][0]['InWeightQty'],Decimal('-2'))
        self.assertEqual(SourceDocumentContext.objects.count(),before)
        self.assertEqual(self.model('ProdStockBook').objects.count(),1)

    def test_inventory_inverse_preserves_null_negative_dimensions_and_original(self):
        inbound=self.inbound();book=self.book(old_in_weight_qty=-2,old_out_weight_qty=None,old_in_rolls=Decimal('1.5'))
        before=snapshot(book);self.execute();book.refresh_from_db()
        self.assertEqual(snapshot(book),before)
        other=self.model('ProdStockBook').objects.exclude(pk=book.pk).get()
        self.assertEqual(other.old_in_weight_qty,Decimal('2'));self.assertIsNone(other.old_out_weight_qty)
        self.assertEqual((other.old_ware_house_id,other.old_lot_no,other.old_storage_unit_ids),('WH','LOT','BIN'))
        self.assertIsNone(other.source_batch_id);self.assertEqual(other.old_book_date,self.at)
        self.assertEqual(self.model('ProdStockBook').objects.aggregate(q=Sum('old_in_weight_qty'))['q'],0)
        self.assertFalse(active(type(inbound).objects.filter(pk=inbound.pk)).exists())

    def test_cancel_repeat_rejected_and_undo_restores_with_new_counter_entry(self):
        inbound=self.inbound();book=self.book(old_in_weight_qty=20)
        self.execute()
        with self.assertRaises(ValidationError):self.execute()
        self.assertEqual(self.model('ProdStockBook').objects.count(),2)
        undo(self.job,self.actor,**self.event)
        self.assertEqual(self.model('ProdStockBook').objects.count(),3)
        self.assertEqual(self.model('ProdStockBook').objects.aggregate(q=Sum('old_in_weight_qty'))['q'],20)
        self.assertTrue(active(type(inbound).objects.filter(pk=inbound.pk)).exists())
        self.execute();self.assertEqual(self.model('ProdStockBook').objects.count(),4)
        self.assertEqual(self.model('ProdStockBook').objects.aggregate(q=Sum('old_in_weight_qty'))['q'],0)

    def test_work_and_steps_are_retained_progress_restored_on_undo(self):
        process,work=self.work();before=snapshot(process)
        step=self.old('WProcessStep','erp_production',old_wprocess_no='W')
        self.execute();process.refresh_from_db();work.refresh_from_db()
        self.assertEqual(process.old_status,'0');self.assertEqual(work.old_curr_kg,Decimal('-2'))
        self.assertTrue(type(step).objects.filter(pk=step.pk).exists());self.assertFalse(active(type(step).objects.all()).exists())
        undo(self.job,self.actor,**self.event);process.refresh_from_db()
        for field in process.SOURCE_FIELDS.values():self.assertEqual(getattr(process,field),process._meta.get_field(field).to_python(before[field]))

    def test_unknown_work_status_does_not_drop_history(self):
        process,work=self.work();type(process).objects.filter(pk=process.pk).update(old_status='旧态')
        self.execute();self.assertTrue(type(work).objects.filter(pk=work.pk).exists())

    def test_shared_outbound_head_only_selected_job_line_and_book_cancelled(self):
        head=self.old('ProdOut',old_sheet_series='OUT',old_sheet_no='PO')
        first=self.old('ProdOutDetail',old_detail_no='D1',old_sheet_series='OUT',old_job_sheet_no='JOB',source_parent_1=head)
        second=self.old('ProdOutDetail',old_detail_no='D2',old_sheet_series='OUT',old_job_sheet_no='OTHER',source_parent_1=head)
        one=self.book(series='OUT',old_detail_no='D1',old_out_weight_qty=3)
        two=self.book(series='OUT',old_detail_no='D2',old_out_weight_qty=9)
        self.execute()
        self.assertFalse(active(type(first).objects.filter(pk=first.pk)).exists())
        self.assertTrue(active(type(second).objects.filter(pk=second.pk)).exists())
        self.assertTrue(active(type(head).objects.filter(pk=head.pk)).exists())
        self.assertEqual(self.model('ProdStockBook').objects.count(),3)
        self.assertEqual(self.model('ProdStockBook').objects.aggregate(q=Sum('old_out_weight_qty'))['q'],9)
        with self.assertRaises(ValidationError):source_services.write(type(head),{'old_remarks':'修改'},head,self.actor)

    def test_old_missing_foreign_keys_expand_by_original_owner_keys(self):
        head=self.old('StuffOut',old_sheet_series='SO',old_sheet_no='OUT',old_job_sheet_no='JOB')
        line=self.old('StuffOutDetail',old_sheet_series='SO',old_detail_no='SD',old_qty=2)
        self.book('StuffStockBook','SO',old_detail_no='SD',old_out_qty=2)
        self.execute();self.assertFalse(active(type(line).objects.filter(pk=line.pk)).exists())
        self.assertEqual(self.model('StuffStockBook').objects.aggregate(q=Sum('old_out_qty'))['q'],0)

    def test_weight_to_actual_outbound_uses_weight_number_even_no_job_number(self):
        weight=self.old('StuffWeight','erp_production',old_sheet_series='SW',old_sheet_no='WEIGH',old_job_sheet_no='JOB')
        phase=self.old('StuffWeightPhase','erp_production',old_sheet_series='SW',old_phase_no=1)
        detail=self.old('StuffWeightDetail','erp_production',old_sheet_series='SW',old_phase_no=1,old_stuff_no=1,old_need_qty=0,old_real_qty=-3)
        out=self.old('StuffOut',old_sheet_series='SO',old_weight_sheet_no='WEIGH')
        self.book('StuffStockBook','SO',old_out_qty=-3)
        self.execute()
        for row in [weight,phase,detail,out]:self.assertFalse(active(type(row).objects.filter(pk=row.pk)).exists())
        detail.refresh_from_db();self.assertEqual(detail.old_real_qty,-3)

    def test_explicit_package_receipt_dispatch_return_chain(self):
        package=self.old('RecordYield',old_guid='P',old_job_sheet_no='JOB',old_bar_code='DUP',old_kg=20)
        inbound=self.old('ProdIn',old_sheet_series='IN',old_sheet_no='PI',old_job_sheet_no=None)
        save_effect(inbound,'package_receipt_origin',origin(package),self.actor,'明确来源')
        out=self.old('ProdOut',old_sheet_series='OUT',old_sheet_no='PO')
        save_effect(out,'product_dispatch_origin',origin(inbound),self.actor,'明确来源')
        line=self.old('ProdOutDetail',old_sheet_series='OUT',old_detail_no='OD',source_parent_1=out)
        returned=self.old('ProdIn',old_sheet_series='RET',old_sheet_no='R')
        save_effect(returned,'product_dispatch_origin',origin(line),self.actor,'退货')
        for series,amount in [('IN',20),('OUT',-20),('RET',20)]:self.book(series=series,old_in_weight_qty=amount)
        other=self.old('RecordYield',old_guid='OTHER',old_job_sheet_no='OTHER',old_bar_code='DUP',old_kg=100)
        self.execute()
        for row in [package,inbound,out,line,returned]:self.assertFalse(active(type(row).objects.filter(pk=row.pk)).exists())
        self.assertTrue(active(type(other).objects.filter(pk=other.pk)).exists())
        self.assertEqual(self.model('ProdStockBook').objects.aggregate(q=Sum('old_in_weight_qty'))['q'],0)

    def test_package_totals_and_start_cleared_but_original_measurements_remain(self):
        package=self.old('RecordYield',old_guid='P',old_job_sheet_no='JOB',old_kg=-1,old_yard=None,old_bar_code='X')
        process=self.old('JobProcess','erp_production',old_sheet_series='JS',old_process_no=1,old_process_id='GX98',old_status='1',old_start_time=self.at)
        self.execute();self.job.refresh_from_db();process.refresh_from_db();package.refresh_from_db()
        self.assertEqual(package.old_kg,-1);self.assertEqual(self.job.old_prolls,0);self.assertIsNone(self.job.old_pkg)
        self.assertEqual(process.old_status,'0');self.assertIsNone(process.old_start_time)

    def test_missing_ledger_never_uses_plan_quantity(self):
        self.inbound();result=self.execute()
        self.assertEqual(self.model('ProdStockBook').objects.count(),0)
        self.assertTrue(any('没有匹配原库存流水' in text for text in result['notes']))

    def test_later_child_card_reported_and_atomic_not_silently_skipped(self):
        self.inbound();self.book(old_in_weight_qty=20)
        child=self.old('JobSheet','erp_production',old_sheet_series='CHILD',old_sheet_no='C',old_ori_source_job_no='JOB')
        data=preview(self.job);self.assertEqual(data['supplemental_rows'][0]['record_id'],child.pk)
        with self.assertRaises(ValidationError):self.execute()
        self.assertEqual(self.model('ProdStockBook').objects.count(),1)
        self.assertFalse(SourceDocumentContext.objects.filter(effects__chain_cancelled__active=True).exists())

    def test_no_plan_snapshot_rolls_back_entire_execution_and_inventory(self):
        inbound=self.inbound();self.book(old_in_weight_qty=20)
        with self.assertRaises(ValidationError):self.execute(mode='execution_and_plan')
        self.assertEqual(self.model('ProdStockBook').objects.count(),1)
        self.assertTrue(active(type(inbound).objects.filter(pk=inbound.pk)).exists())

    def test_undo_detects_changed_projection_and_keeps_cancellation_atomic(self):
        self.inbound();self.book(old_in_weight_qty=20)
        self.execute();type(self.job).objects.filter(pk=self.job.pk).update(old_is_prod_in_finished=True)
        with self.assertRaises(ValidationError):undo(self.job,self.actor,**self.event)
        self.assertEqual(self.model('ProdStockBook').objects.count(),2)

    def test_cancelled_source_and_compensation_cannot_be_edited_or_deleted(self):
        inbound=self.inbound();self.book(old_in_weight_qty=20);self.execute()
        with self.assertRaises(ValidationError):source_services.write(type(inbound),{'old_remarks':'X'},inbound,self.actor)
        correction=self.model('ProdStockBook').objects.order_by('-pk').first()
        with self.assertRaises(ValidationError):source_services.write(type(correction),{'old_in_weight_qty':2},correction,self.actor)
        with self.assertRaises(ValidationError):source_services.delete_documents(type(correction).objects.filter(pk=correction.pk),self.actor)

    def test_scope_query_is_used_for_sources(self):
        inbound=self.inbound()
        def limited(name,module):
            query=self.model(name,module).objects.all()
            return query.none() if name=='ProdIn' else query
        self.assertFalse(any(row['table']=='ProdIn' for row in preview(self.job,limited)['rows']))

    def test_http_preview_cancel_and_undo(self):
        self.inbound();self.book(old_in_weight_qty=20)
        path=f'/api/system/erp_production_sourcedyejobsheet/{self.job.pk}/'
        response=self.client.post(path+'preview_execution_reverse/',{},format='json');self.assertEqual(response.status_code,200,response.data)
        response=self.client.post(path+'reverse_execution_chain/',dict(mode='execution_only',work_mode='trigger_only',at=self.at.isoformat(),reason='验收'),format='json')
        self.assertEqual(response.status_code,200,response.data)
        response=self.client.post(path+'undo_execution_reverse/',dict(at=self.at.isoformat(),reason='撤回'),format='json')
        self.assertEqual(response.status_code,200,response.data)

    def test_shared_head_two_cards_cancel_and_restore_in_operation_order(self):
        other=self.old('JobSheet','erp_production',old_sheet_series='J2',old_sheet_no='OTHER')
        head=self.old('ProdOut',old_sheet_series='OUT')
        for code,detail,quantity in [('JOB','D1',3),('OTHER','D2',9)]:
            self.old('ProdOutDetail',old_detail_no=detail,old_sheet_series='OUT',old_job_sheet_no=code,source_parent_1=head)
            self.book(series='OUT',old_detail_no=detail,old_out_weight_qty=quantity)
        self.execute()
        cancel(other,self.actor,mode='execution_only',work_mode='trigger_only',**self.event)
        self.assertEqual(self.model('ProdStockBook').objects.aggregate(q=Sum('old_out_weight_qty'))['q'],0)
        with self.assertRaises(ValidationError):undo(self.job,self.actor,**self.event)
        undo(other,self.actor,**self.event);undo(self.job,self.actor,**self.event)
        self.assertEqual(self.model('ProdStockBook').objects.aggregate(q=Sum('old_out_weight_qty'))['q'],12)

    def test_shared_head_orphan_book_is_reported_without_partial_cancellation(self):
        head=self.old('ProdOut',old_sheet_series='OUT')
        for code,detail in [('JOB','D1'),('OTHER','D2')]:
            self.old('ProdOutDetail',old_detail_no=detail,old_sheet_series='OUT',old_job_sheet_no=code,source_parent_1=head)
        self.book(series='OUT',old_detail_no='UNKNOWN',old_out_weight_qty=3)
        self.assertTrue(discover(self.job)['issues'])
        with self.assertRaises(ValidationError):self.execute()
        self.assertEqual(self.model('ProdStockBook').objects.count(),1)

    def test_orphan_line_keeps_identity_and_reverses_its_exact_ledger(self):
        line=self.old('ProdOutDetail',old_detail_no='D1',old_sheet_series='MISSING',old_job_sheet_no='JOB',source_batch=historical_batch())
        self.book(series='MISSING',old_detail_no='D1',old_out_weight_qty=-7)
        self.execute();self.assertTrue(type(line).objects.filter(pk=line.pk,source_batch=historical_batch()).exists())
        self.assertEqual(self.model('ProdStockBook').objects.aggregate(q=Sum('old_out_weight_qty'))['q'],0)

    def test_complete_header_orphan_ledger_is_not_skipped(self):
        self.old('StuffOut',old_sheet_series='SO',old_job_sheet_no='JOB')
        self.book('StuffStockBook','SO',old_detail_no='NO-LINE',old_out_qty=-8)
        self.execute();self.assertEqual(self.model('StuffStockBook').objects.aggregate(q=Sum('old_out_qty'))['q'],0)

    def test_gray_issue_releases_exact_tag_and_assignment_and_restores_on_undo(self):
        head=self.old('GrayOut',old_sheet_series='GO',old_sheet_no='OUT',old_sheet_kind=21,old_right_status=10)
        line=self.old('GrayOutDetail',old_assigned_no='ASSIGNED',old_sheet_series='GO',old_rece_sheet_no='RECEIPT',old_job_sheet_no='JOB',source_parent_1=head)
        output=self.old('GrayOutRecord',old_assigned_no='ASSIGNED',old_sheet_series='GO',old_rece_sheet_no='RECEIPT',old_roll_no='1',old_bar_code='DUP',source_parent_1=line)
        tag=self.old('GrayInRecord',old_rece_sheet_no='RECEIPT',old_roll_no='1',old_bar_code='DUP',old_assigned_no='ASSIGNED',old_job_sheet_no='JS')
        other=self.old('GrayInRecord',old_rece_sheet_no='RECEIPT',old_roll_no='2',old_bar_code='DUP',old_assigned_no='OTHER')
        assignment=self.old('JobAssign','erp_production',old_sheet_series='JS',old_assign_no=1,old_rece_sheet_no='RECEIPT',old_status=1)
        self.book('GrayStockBook','GO',old_detail_no='ASSIGNED',old_out_weight_qty=3)
        self.execute();tag.refresh_from_db();other.refresh_from_db();assignment.refresh_from_db()
        self.assertIsNone(tag.old_assigned_no);self.assertEqual(other.old_assigned_no,'OTHER');self.assertEqual(assignment.old_status,0)
        self.assertEqual(self.model('GrayStockBook').objects.aggregate(q=Sum('old_out_weight_qty'))['q'],0)
        undo(self.job,self.actor,**self.event);tag.refresh_from_db();assignment.refresh_from_db()
        self.assertEqual(tag.old_assigned_no,'ASSIGNED');self.assertEqual(assignment.old_status,1)

    def test_execution_and_split_plan_cancel_and_restore_together(self):
        from plugins.erp_base.source_job_flow import split_card
        source=self.job
        self.job=split_card(source,self.actor,quantity=4,rolls=1,unit=None,processes=[],**self.event)
        self.old('ProdIn',old_sheet_series='IN',old_job_sheet_no=self.job.old_sheet_no,old_rolls=1)
        self.book(old_in_weight_qty=4)
        self.execute(mode='execution_and_plan');self.job.refresh_from_db()
        self.assertEqual(self.job.old_pre_vat_qty,0)
        undo(self.job,self.actor,**self.event);self.job.refresh_from_db();source.refresh_from_db()
        self.assertEqual(self.job.old_pre_vat_qty,4);self.assertTrue(source.old_is_splited)

    def test_partial_scope_cannot_mutate_half_chain(self):
        self.inbound();self.book(old_in_weight_qty=20)
        def limited(name,module):
            query=self.model(name,module).objects.all()
            return query.none() if name=='ProdStockBook' else query
        with self.assertRaises(ValidationError):self.execute(query=limited)
        self.assertEqual(self.model('ProdStockBook').objects.count(),1)

    def test_quality_rows_exit_statistics_and_reappear_after_undo(self):
        from plugins.erp_base.source_quality_reports import rows
        quality=self.old('DyeCheckout','erp_quality',old_job_sheet_no='JOB',old_process_id='GX07',old_cloth_qty_kg=-4)
        self.execute();self.assertFalse(rows('DyeCheckout','erp_quality').filter(pk=quality.pk).exists())
        self.assertTrue(type(quality).objects.filter(pk=quality.pk).exists())
        undo(self.job,self.actor,**self.event);self.assertTrue(rows('DyeCheckout','erp_quality').filter(pk=quality.pk).exists())

    def test_explicit_orphan_ledger_link_resolves_shared_header_without_faking_fields(self):
        from plugins.erp_base.source_chain_reverse import link_source
        head=self.old('ProdOut',old_sheet_series='OUT')
        for code,detail in [('JOB','D1'),('OTHER','D2')]:
            self.old('ProdOutDetail',old_detail_no=detail,old_sheet_series='OUT',old_job_sheet_no=code,source_parent_1=head)
        book=self.book(series='OUT',old_detail_no='UNKNOWN',old_out_weight_qty=-4)
        before=snapshot(book)
        link_source(self.job,self.actor,'ProdStockBook',book.pk,**self.event)
        self.execute();book.refresh_from_db()
        self.assertEqual(snapshot(book),before)
        self.assertEqual(self.model('ProdStockBook').objects.aggregate(q=Sum('old_out_weight_qty'))['q'],0)

    def test_explicit_missing_job_reference_preserves_original_null(self):
        from plugins.erp_base.source_chain_reverse import link_source
        work=self.old('WProcess','erp_production',old_wprocess_no='NO-JOB',old_job_sheet_no=None,old_curr_kg=-1)
        link_source(self.job,self.actor,'WProcess',work.pk,**self.event)
        self.execute();work.refresh_from_db();self.assertIsNone(work.old_job_sheet_no)
        self.assertFalse(active(type(work).objects.filter(pk=work.pk)).exists())

    def test_http_missing_explicit_source_returns_not_found(self):
        path=f'/api/system/erp_production_sourcedyejobsheet/{self.job.pk}/link_execution_source/'
        response=self.client.post(path,dict(source_table='WProcess',record_id=99999999,at=self.at.isoformat(),reason='核对'),format='json')
        self.assertEqual(response.status_code,404,response.data)

    def test_delivery_factory_and_material_issue_facts_reversed_and_restored(self):
        inbound=self.inbound()
        save_effect(inbound,'factory_quality',{'result':'concession','reason':'原放行'},self.actor,'原事实')
        out=self.old('StuffWeight','erp_production',old_sheet_series='SW',old_job_sheet_no='JOB')
        save_effect(out,'material_issue',{'outgoing_id':123,'rows':[]},self.actor,'原事实')
        dispatch=self.old('ProdOut',old_sheet_series='OUT')
        self.old('ProdOutDetail',old_detail_no='D1',old_sheet_series='OUT',old_job_sheet_no='JOB')
        save_effect(dispatch,'delivery_confirmation',{'result':'delivered','receiver':'原签收人'},self.actor,'原事实')
        self.execute()
        def facts(item):return SourceDocumentContext.objects.get(entity=item._meta.label,object_id=item.pk).effects
        self.assertEqual(facts(inbound)['factory_quality']['result'],'withdrawn')
        self.assertEqual(facts(out)['material_issue']['state'],'reversed')
        self.assertEqual(facts(dispatch)['delivery_confirmation']['result'],'withdrawn')
        undo(self.job,self.actor,**self.event)
        self.assertEqual(facts(inbound)['factory_quality']['result'],'concession')
        self.assertEqual(facts(out)['material_issue'],{'outgoing_id':123,'rows':[]})
        self.assertEqual(facts(dispatch)['delivery_confirmation']['result'],'delivered')

    def test_cancelled_job_cannot_generate_new_work_or_inbound(self):
        self.execute()
        with self.assertRaises(ValidationError):source_services.write(self.model('WProcess','erp_production'),
            {'old_wprocess_no':'NEW','old_job_sheet_no':'JOB'},actor=self.actor)
        with self.assertRaises(ValidationError):source_services.write(self.model('ProdIn'),
            {'old_sheet_series':'NEW','old_job_sheet_no':'JOB'},actor=self.actor)

    def test_explicit_ledger_owner_overrides_old_line_match_and_freezes_shared_header(self):
        from plugins.erp_base.source_chain_reverse import link_source
        other=self.old('JobSheet','erp_production',old_sheet_series='J2',old_sheet_no='OTHER')
        head=self.old('ProdOut',old_sheet_series='OUT')
        line=self.old('ProdOutDetail',old_detail_no='D1',old_sheet_series='OUT',old_job_sheet_no='JOB',source_parent_1=head)
        book=self.book(series='OUT',old_detail_no='D1',old_out_weight_qty=8)
        link_source(other,self.actor,'ProdStockBook',book.pk,**self.event)
        self.execute();self.assertEqual(self.model('ProdStockBook').objects.count(),1)
        self.assertTrue(active(type(head).objects.filter(pk=head.pk)).exists())
        cancel(other,self.actor,mode='execution_only',work_mode='trigger_only',**self.event)
        with self.assertRaises(ValidationError):undo(self.job,self.actor,**self.event)
        self.assertEqual(self.model('ProdStockBook').objects.aggregate(q=Sum('old_out_weight_qty'))['q'],0)
        undo(other,self.actor,**self.event);undo(self.job,self.actor,**self.event)
        self.assertEqual(self.model('ProdStockBook').objects.aggregate(q=Sum('old_out_weight_qty'))['q'],8)
        line.source_parent_1=None;line.save(update_fields=['source_parent_1']);head.delete()
        count=self.model('ProdStockBook').objects.count()
        self.execute();self.assertEqual(self.model('ProdStockBook').objects.count(),count)
        undo(self.job,self.actor,**self.event)
        cancel(other,self.actor,mode='execution_only',work_mode='trigger_only',**self.event)
        self.assertEqual(self.model('ProdStockBook').objects.aggregate(q=Sum('old_out_weight_qty'))['q'],0)
        undo(other,self.actor,**self.event)
