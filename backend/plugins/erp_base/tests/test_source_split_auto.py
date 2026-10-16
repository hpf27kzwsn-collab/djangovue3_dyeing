from plugins.erp_base.tests.source_fixtures import historical_batch
from datetime import datetime,timedelta
from decimal import Decimal
from django.apps import apps
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base import source_services as services
from plugins.erp_base.business import snapshot
from plugins.erp_base.source_continuation import view_effects
from plugins.erp_base.source_auto_combine import choose_route,automatic_sync,remaining_steps,initialize_current
from plugins.erp_base.source_job_flow import split_card,merge_cards,transfer_allocation,adopt_combine_link
from plugins.erp_base.source_card_reverse import reverse_card,reverse_allocation,reverse_link
from plugins.erp_base.source_gray_split_merge import split_record,merge_records,undo_operation,active,operation_report


class SplitAutoTests(TestCase):
    def setUp(self):
        self.actor=Users.objects.create_superuser(username='split-auto',password='test')
        self.client=APIClient();self.client.force_authenticate(self.actor)
        self.at=timezone.make_aware(datetime(2026,10,15,12))
        self.event=dict(at=self.at,reason='原链复刻验收')

    def model(self,name,module='erp_production'):
        return apps.get_model(module+'.SourceDye'+name)

    def old(self,name,module='erp_production',**values):
        row=self.model(name,module).objects.create(**values);row.refresh_from_db();return row

    def job(self,number='A',**values):
        return self.old('JobSheet',old_sheet_series=number,old_sheet_no=number,old_pre_vat_qty=100,
            old_pre_rolls=10,old_assign_unit=1,**values)

    def process(self,job,number=1,process='P',**values):
        return self.old('JobProcess',old_sheet_series=job.old_sheet_series,old_process_no=number,old_process_id=process,**values)

    def gray(self,name='GrayInRecord',receipt='R',roll='001',code='CODE',**values):
        module='erp_warehouse' if name=='GrayInRecord' else 'erp_production'
        return self.old(name,module,old_rece_sheet_no=receipt,old_roll_no=roll,old_bar_code=code,
            old_weight_qty=Decimal('100'),old_length_qty=Decimal('200'),old_rolls=Decimal('10'),**values)

    def split(self,row,job=None,weight=Decimal('25'),length=Decimal('50'),rolls=Decimal('2.5')):
        return split_record(row,self.actor,weight,length,rolls,job,**self.event)

    def new_gray(self,log):
        value=view_effects(log)['gray_operation']['created'][0]
        return apps.get_model(value['entity']).objects.get(pk=value['source']['id'])

    def test_schedule_delay_scalar_order_and_unmatched_fragments_are_visible(self):
        a,b=self.job(),self.job('B');p=self.process(a,old_status='4');target=self.process(b,2)
        self.old('PProcess','erp_base',old_process_id='P',old_delay_hours=2)
        self.old('ProcessSchedule',old_job_sheet_no='a ',old_process_no=1,old_process_id='P',old_start_time=self.at-timedelta(hours=1),old_combine_sheet_nos='B:2|bad|MISSING:9|B:9999999999999999')
        later=self.old('ProcessSchedule',old_job_sheet_no='A',old_process_no=1,old_process_id='P',old_start_time=self.at-timedelta(hours=3),old_combine_sheet_nos='OTHER:1')
        result=choose_route(p,True,self.at)
        self.assertEqual(result['targets'],[target.pk]);self.assertEqual(len(result['rows']),4)
        self.assertEqual(sum(row['issue'] is not None for row in result['rows']),3)
        self.assertEqual(choose_route(p,False,self.at)['sources'][0]['selected']['source']['id'],later.pk)
        self.assertIsNone(result['step_processes'][0]['process_id'])

    def test_direct_stuff_route_keeps_repeated_tokens_and_selects_first_record(self):
        a,b=self.job(),self.job('B');p=self.process(a,process='G-06')
        target=self.process(b,2,'G-06');self.process(b,3,'G-06')
        first=self.old('StuffWeight',old_job_sheet_no='A',old_process_id='G-06',old_combine_sheet_nos='B|B|UNKNOWN')
        self.old('StuffWeight',old_job_sheet_no='A',old_process_id='G-06',old_combine_sheet_nos='OTHER')
        result=choose_route(p,False,self.at)
        self.assertEqual(result['targets'],[target.pk,target.pk]);self.assertEqual(len(result['rows']),3)
        self.assertEqual(result['sources'][0]['selected']['source']['id'],first.pk)
        self.assertEqual(len(result['sources'][0]['candidate_ids']),2)

    def test_reverse_stuff_membership_uses_owner_and_its_process_not_source_process(self):
        a,b,c=self.job(),self.job('B'),self.job('C');p=self.process(a,process='G-07')
        bt,ct=self.process(b,1,'OTHER'),self.process(c,2,'OTHER')
        self.old('StuffWeight',old_job_sheet_no='B',old_process_id='OTHER',old_combine_sheet_nos='a |C')
        result=choose_route(p,False,self.at)
        self.assertEqual(result['targets'],[ct.pk,bt.pk]);self.assertEqual(result['step_processes'][0]['process_id'],'OTHER')

    def test_null_identifiers_do_not_equal_sql_null(self):
        job=self.old('JobSheet',old_sheet_series='A',old_sheet_no=None)
        p=self.process(job,number=1,process='G-06')
        self.old('ProcessSchedule',old_job_sheet_no=None,old_process_no=1,old_combine_sheet_nos='B:2')
        self.assertEqual(choose_route(p,False,self.at)['targets'],[])

    def test_automatic_sync_uses_source_status_and_exact_next_then_initializes_empty_progress(self):
        a,b=self.job(),self.job('B');p=self.process(a,old_status='4');target=self.process(b,2,old_status='0')
        self.process(b,3,'NEXT',old_station_id='ST')
        self.old('ProcessSchedule',old_job_sheet_no='A',old_process_no=1,old_combine_sheet_nos='B:2|B:2')
        result=automatic_sync(p,self.actor,'M',1,False,self.at,**self.event)
        target.refresh_from_db();b.refresh_from_db()
        self.assertEqual(target.old_status,'4');self.assertEqual(target.old_machine_id,'M');self.assertEqual(target.old_start_time,self.at)
        self.assertIsNone(target.old_end_time);self.assertEqual(b.old_next_process_id,'NEXT')
        self.assertEqual(result['remaining_steps'][0]['missing'],[])
        p.refresh_from_db();self.assertEqual(p.old_status,'4')

    def test_current_initialization_handles_done_and_later_running_without_touching_unrelated_job(self):
        job=self.job();unrelated=self.job('OTHER')
        self.process(job,1,'DONE',old_status='1');self.process(job,2,'RUN',old_status='5');self.process(job,3,'WAIT',old_status='0')
        initialize_current(job,self.actor);job.refresh_from_db();unrelated.refresh_from_db()
        self.assertEqual(job.old_curr_process_id,'RUN');self.assertEqual(job.old_next_process_id,'RUN')
        self.assertIsNone(unrelated.old_curr_process_id)

    def test_remaining_steps_requires_matching_curve_and_done_program(self):
        job=self.job();p=self.process(job,process='G-06',old_status='4')
        self.old('StuffWeight',old_sheet_series='SW',old_job_sheet_no='A',old_process_id='G-06',old_sheet_status=0,old_sheet_kind=2,old_recipe_type=0)
        self.old('StuffWeightPhase',old_sheet_series='SW',old_phase_no=1,old_phase_id='PH')
        self.old('PDyeCurve','erp_base',old_curve_id='CURVE',old_phase_id='PH')
        self.old('PDyeCurveDetail','erp_base',old_curve_id='CURVE',old_step_no=1,old_dye_process_id='STEP')
        self.assertEqual(len(remaining_steps(job,'G-06',1,self.actor)),1)
        p.refresh_from_db();self.assertEqual(p.old_status,'4')
        self.old('WProcessStep',old_job_sheet_no='A',old_process_id='G-06',old_dye_process_id='STEP',old_program_id='CURVE')
        self.assertEqual(remaining_steps(job,'G-06',1,self.actor),[])
        p.refresh_from_db();self.assertEqual(p.old_status,'1')

    def test_empty_stuff_members_keep_assigned_process_for_schedule_fallback(self):
        job=self.job();process=self.process(job,process='g-06 ',old_status='4')
        self.old('StuffWeight',old_job_sheet_no='A',old_process_id='G-06',old_combine_sheet_nos='')
        report=choose_route(process,False,self.at)
        self.assertEqual(report['sources'][0]['mode'],'schedule')
        self.assertEqual(report['step_processes'][0]['process_id'],'G-06')
        automatic_sync(process,self.actor,None,2,False,self.at,**self.event)
        process.refresh_from_db();self.assertEqual(process.old_status,'1')

    def test_split_card_reverse_is_lifo_and_restores_original_plan_fields(self):
        job=self.job();before=snapshot(job)
        first=split_card(job,self.actor,Decimal('20'),Decimal('2'),1,self.at,'first',[])
        second=split_card(job,self.actor,Decimal('10'),Decimal('1'),1,self.at,'second',[])
        with self.assertRaises(ValidationError):reverse_card(first,self.actor,'unstarted',**self.event)
        reverse_card(second,self.actor,'unstarted',**self.event);reverse_card(first,self.actor,'unstarted',**self.event)
        job.refresh_from_db()
        for key in ['old_pre_vat_qty','old_pre_rolls','old_is_splited','old_split_card_reason']:self.assertEqual(snapshot(job)[key],before[key])
        first.refresh_from_db();self.assertEqual(first.old_pre_vat_qty,0)
        self.assertEqual(view_effects(first)['card_adoption']['state'],'reversed')

    def test_plan_only_reverse_preserves_real_weighing_and_manual_allocation(self):
        job=self.job();new=split_card(job,self.actor,Decimal('20'),Decimal('2'),1,self.at,'split',[])
        weight=self.old('StuffWeight',old_job_sheet_no=new.old_sheet_no,old_sheet_series='ACTUAL',old_weight=9)
        order=self.old('JobCombineOrder',old_sheet_series=new.old_sheet_series,old_combine_qty=7)
        before=snapshot(weight)
        with self.assertRaises(ValidationError):reverse_card(new,self.actor,'unstarted',**self.event)
        reverse_card(new,self.actor,'plan_only',**self.event)
        weight.refresh_from_db();order.refresh_from_db();self.assertEqual(snapshot(weight),before);self.assertEqual(order.old_combine_qty,7)
        self.assertTrue(view_effects(new)['card_adoption']['actual_records_retained'])

    def test_merge_reverse_preserves_source_cards_and_zeroes_adopted_relationships(self):
        first,second=self.job(),self.job('B');before=snapshot(first)
        new=merge_cards(first,self.actor,[second],Decimal('200'),Decimal('20'),1,self.at,'merge',[])
        reverse_card(new,self.actor,'unstarted',**self.event)
        links=self.model('JobCombine').objects.filter(source_parent_1=new)
        self.assertEqual(links.count(),2);self.assertTrue(all(row.old_qty==0 and row.old_rolls==0 for row in links))
        first.refresh_from_db();self.assertEqual(snapshot(first),before)

    def test_reverse_allocation_restores_null_and_rounded_quantity(self):
        job=self.job();source=self.old('JobCombineOrder',old_combine_qty=Decimal('50'))
        first=transfer_allocation(source,self.actor,job,Decimal('7.123456'),self.at,'transfer')
        second=transfer_allocation(source,self.actor,job,None,self.at,'unknown')
        with self.assertRaises(ValidationError):reverse_allocation(first,self.actor,**self.event)
        reverse_allocation(second,self.actor,**self.event);reverse_allocation(first,self.actor,**self.event)
        source.refresh_from_db();self.assertEqual(source.old_combine_qty,50)

    def test_reverse_adopted_link_retains_orphan_original(self):
        source=self.old('JobCombine',old_sheet_series='ORPHAN',old_qty=-3,old_rolls=None,source_batch=historical_batch())
        new=adopt_combine_link(source,self.actor,self.job(),**self.event)
        reverse_link(new,self.actor,**self.event);source.refresh_from_db();new.refresh_from_db()
        self.assertEqual(source.old_qty,-3);self.assertEqual(new.old_qty,0);self.assertEqual(new.old_rolls,0)

    def test_pre_dispatch_split_updates_roll_sum_only_and_undo_restores_exact_values(self):
        detail=self.old('GrayInDetail','erp_warehouse',old_rece_sheet_no='R',old_sheet_series='H',old_rolls=99,old_weight_qty=345,old_length_qty=678)
        book=self.old('GrayStockBook','erp_warehouse',old_book_no=1,old_rece_sheet_no='R',old_sheet_series='H',old_detail_no='R',old_in_rolls=99,old_in_weight_qty=345)
        original=self.gray(source_parent_1=detail,source_batch=historical_batch());before=snapshot(original)
        log=self.split(original);new=self.new_gray(log)
        original.refresh_from_db();detail.refresh_from_db();book.refresh_from_db()
        self.assertEqual(original.old_weight_qty,75);self.assertEqual(new.old_weight_qty,25)
        self.assertEqual(new.old_roll_no,'001-1');self.assertEqual(new.old_cbz,'剪');self.assertIsNone(new.source_batch_id)
        self.assertEqual(detail.old_rolls,10);self.assertEqual(detail.old_weight_qty,345);self.assertEqual(book.old_in_rolls,10)
        undo_operation(log,self.actor,**self.event);original.refresh_from_db();detail.refresh_from_db();book.refresh_from_db()
        for key in original.SOURCE_FIELDS.values():self.assertEqual(snapshot(original)[key],before[key])
        self.assertEqual(detail.old_rolls,99);self.assertEqual(book.old_in_rolls,99)
        self.assertTrue(self.model('GrayInRecord','erp_warehouse').objects.filter(pk=new.pk).exists())
        self.assertFalse(active(self.model('GrayInRecord','erp_warehouse').objects.all()).filter(pk=new.pk).exists())

    def test_pre_dispatch_split_also_splits_selected_job_assignment_and_counts_rows(self):
        job=self.job();original=self.gray();assigned=self.gray('JobGrayRecord',old_sheet_series='A',old_gray_bar_code='CODE',source_parent_1=job)
        allocation=self.old('JobAssign',old_sheet_series='A',old_assign_no=1,old_rece_sheet_no='R',old_rolls=55)
        log=self.split(original,job);assigned.refresh_from_db();allocation.refresh_from_db()
        self.assertEqual(assigned.old_weight_qty,75);self.assertEqual(allocation.old_rolls,2)
        self.assertEqual(len(view_effects(log)['gray_operation']['created']),2)
        undo_operation(log,self.actor,**self.event);allocation.refresh_from_db();self.assertEqual(allocation.old_rolls,55)

    def test_after_dispatch_split_uses_latest_fields_and_weight_then_length_plan(self):
        job=self.job();original=self.gray('JobGrayRecord',code='1234567890123456A',old_sheet_series='A',old_gray_bar_code='GRAY',old_assigned_no='OUT',source_parent_1=job)
        allocation=self.old('JobAssign',old_sheet_series='A',old_assign_no=1,old_rece_sheet_no='R',old_weight_qty=9)
        log=self.split(original);new=self.new_gray(log);job.refresh_from_db();allocation.refresh_from_db()
        self.assertEqual(new.old_gray_bar_code,new.old_bar_code);self.assertEqual(new.old_gunit,1);self.assertEqual(new.old_kg,25)
        self.assertEqual(job.old_pre_vat_qty,200);self.assertEqual(job.old_sum_assigned_weight_qty,100);self.assertEqual(job.old_sum_assigned_length_qty,200)
        self.assertEqual(allocation.old_weight_qty,100)
        undo_operation(log,self.actor,**self.event);job.refresh_from_db();allocation.refresh_from_db()
        self.assertEqual(job.old_pre_vat_qty,100);self.assertEqual(allocation.old_weight_qty,9)

    def test_negative_null_over_split_remains_recorded_with_issues(self):
        original=self.gray(old_assigned_no='ALREADY')
        log=self.split(original,weight=Decimal('120'),length=None,rolls=Decimal('-1'))
        original.refresh_from_db();new=self.new_gray(log)
        self.assertEqual(original.old_weight_qty,-20);self.assertIsNone(original.old_length_qty);self.assertEqual(new.old_rolls,-1)
        self.assertGreaterEqual(len(operation_report(log)['supplemental_rows']),4)

    def test_merge_keeps_duplicate_barcodes_and_updates_each_receipt_without_double_count(self):
        one=self.gray(receipt='R',roll='001',code='SAME',source_batch=historical_batch())
        two=self.gray(receipt='R2',roll='002',code='SAME',source_batch=historical_batch());two_before=snapshot(two)
        details=[]
        for receipt in ['R','R2']:
            details.append(self.old('GrayInDetail','erp_warehouse',old_rece_sheet_no=receipt,old_sheet_series=receipt,old_weight_qty=100))
        log=merge_records(one,self.actor,[two,two],None,**self.event)
        one.refresh_from_db();two.refresh_from_db()
        self.assertEqual(one.old_weight_qty,200);self.assertEqual(snapshot(two),two_before)
        self.assertEqual(active(self.model('GrayInRecord','erp_warehouse').objects.all()).count(),1)
        for detail in details:detail.refresh_from_db()
        self.assertEqual([row.old_weight_qty for row in details],[200,0])
        with self.assertRaises(ValidationError):self.split(two)
        undo_operation(log,self.actor,**self.event);one.refresh_from_db()
        self.assertEqual(one.old_weight_qty,100);self.assertEqual(active(self.model('GrayInRecord','erp_warehouse').objects.all()).count(),2)

    def test_after_dispatch_merge_refreshes_both_job_totals_and_can_reverse(self):
        a,b=self.job(),self.job('B')
        one=self.gray('JobGrayRecord',old_sheet_series='A',old_assigned_no='OUT',old_gray_bar_code='A')
        two=self.gray('JobGrayRecord',receipt='R2',roll='002',old_sheet_series='B',old_assigned_no='OUT',old_gray_bar_code='B')
        log=merge_records(one,self.actor,[two],None,**self.event);a.refresh_from_db()
        self.assertEqual(a.old_sum_assigned_weight_qty,200);self.assertEqual(a.old_pre_vat_qty,400)
        undo_operation(log,self.actor,**self.event);a.refresh_from_db();self.assertEqual(a.old_pre_vat_qty,100)

    def test_split_undo_requires_later_merge_to_be_reversed_first(self):
        original=self.gray();split=self.split(original);child=self.new_gray(split)
        other=self.gray(roll='000');merge=merge_records(other,self.actor,[child],None,**self.event)
        with self.assertRaises(ValidationError):undo_operation(split,self.actor,**self.event)
        undo_operation(merge,self.actor,**self.event);undo_operation(split,self.actor,**self.event)

    def test_reverse_rejects_changed_generated_record_without_partial_restoration(self):
        original=self.gray();log=self.split(original);child=self.new_gray(log)
        self.model('GrayInRecord','erp_warehouse').objects.filter(pk=child.pk).update(old_weight_qty=24)
        with self.assertRaises(ValidationError):undo_operation(log,self.actor,**self.event)
        original.refresh_from_db();self.assertEqual(original.old_weight_qty,75)
        self.assertEqual(view_effects(log)['gray_operation']['state'],'applied')

    def test_history_without_new_operation_facts_is_visible_and_reverse_is_explicit_error(self):
        log=self.old('GrayRecordCutLogs','erp_warehouse',old_id='OLD',old_kind=1,old_operate_date=self.at,source_batch=historical_batch())
        self.assertEqual(operation_report(log)['rows'][0]['source']['batch_id'],historical_batch().pk)
        with self.assertRaises(ValidationError):undo_operation(log,self.actor,**self.event)

    def test_generic_delete_cannot_bypass_operation_or_remove_history(self):
        job=self.job();new=split_card(job,self.actor,Decimal('20'),Decimal('2'),1,self.at,'split',[])
        with self.assertRaises(ValidationError):services.delete_documents(type(new).objects.filter(pk=new.pk),self.actor)
        original=self.gray();log=self.split(original);child=self.new_gray(log)
        for item in [original,child,log]:
            with self.assertRaises(ValidationError):services.delete_documents(type(item).objects.filter(pk=item.pk),self.actor)

    def test_http_actions_return_readable_results_and_nullable_values(self):
        original=self.gray();url=f'/api/system/erp_warehouse_sourcedyegrayinrecord/{original.pk}/'
        payload={'weight':'-2','length':None,'rolls':'1','at':self.at.isoformat(),'reason':'HTTP异常细码'}
        response=self.client.post(url+'split_gray/',payload,format='json')
        self.assertEqual(response.status_code,200,response.data)
        log_id=response.data['data']['rows'][0]['record_id']
        response=self.client.post(f'/api/system/erp_warehouse_sourcedyegrayrecordcutlogs/{log_id}/undo_gray/',
            {'at':self.at.isoformat(),'reason':'撤回'},format='json')
        self.assertEqual(response.status_code,200,response.data);self.assertEqual(response.data['data']['rows'][0]['state'],'reversed')

    def test_http_automatic_route_and_reverse_modes_validate_inputs(self):
        job=self.job();process=self.process(job)
        response=self.client.post(f'/api/system/erp_production_sourcedyejobprocess/{process.pk}/preview_auto_combine/',
            {'plan_have_time':False,'as_of':self.at.isoformat()},format='json')
        self.assertEqual(response.status_code,200,response.data)
        new=split_card(job,self.actor,Decimal('2'),Decimal('1'),1,self.at,'拆',[])
        response=self.client.post(f'/api/system/erp_production_sourcedyejobsheet/{new.pk}/reverse_card/',
            {'mode':'unstarted','at':self.at.isoformat(),'reason':'撤回'},format='json')
        self.assertEqual(response.status_code,200,response.data);self.assertEqual(Decimal(response.data['data']['old_pre_vat_qty']),0)

    def test_consumed_gray_is_excluded_from_receipt_formula_and_package_adoption(self):
        from plugins.erp_base.source_entry_calculations import entry_values
        from plugins.erp_base.source_packaging_flow import adopt_gray_record
        head=self.old('GrayIn','erp_warehouse',old_sheet_series='H',old_sheet_kind=10)
        detail=self.old('GrayInDetail','erp_warehouse',old_rece_sheet_no='R',old_sheet_series='H',source_parent_1=head)
        one=self.gray(source_parent_1=detail);two=self.gray(roll='002',source_parent_1=detail)
        merge_records(one,self.actor,[two],None,**self.event)
        # 原收料明细按细码汇总时只采用活动结果。
        values=entry_values(detail,'GrayAllotInDetail')
        self.assertEqual(values['old_weight_qty'],200)
        job=self.job();a=self.gray('JobGrayRecord',old_sheet_series='A',old_gray_bar_code='G1')
        b=self.gray('JobGrayRecord',roll='002',old_sheet_series='A',old_gray_bar_code='G2')
        merge_records(a,self.actor,[b],None,**self.event)
        package=self.old('RecordYield','erp_warehouse',old_guid='PKG')
        with self.assertRaises(ValidationError):adopt_gray_record(package,self.actor,b,**self.event)

    def test_partial_assignment_anomaly_remains_visible_and_can_be_processed(self):
        original=self.gray()
        self.old('JobGrayRecord',old_sheet_series='OTHER',old_rece_sheet_no='R',old_roll_no='001',old_gray_bar_code='CODE',old_weight_qty=20)
        log=self.split(original)
        self.assertTrue(any('assigned_ids' in row for row in operation_report(log)['supplemental_rows']))

    def test_after_dispatch_sparse_suffix_generates_distinct_next_and_keeps_legacy_codes(self):
        original=self.gray('JobGrayRecord',code='1234567890123456',old_sheet_series='A')
        other=self.gray('JobGrayRecord',roll='001-2',code='1234567890123456-2',old_sheet_series='A')
        log=self.split(original);new=self.new_gray(log)
        self.assertEqual(new.old_roll_no,'001-3');other.refresh_from_db();self.assertEqual(other.old_roll_no,'001-2')

    def test_reversed_new_plan_cannot_be_used_as_current_allocation_target(self):
        job=self.job();new=split_card(job,self.actor,Decimal('10'),Decimal('1'),1,self.at,'split',[])
        reverse_card(new,self.actor,'unstarted',**self.event)
        source=self.old('JobCombineOrder',old_sheet_series='A',old_combine_qty=20)
        with self.assertRaises(ValidationError):transfer_allocation(source,self.actor,new,Decimal('1'),**self.event)
        source.refresh_from_db();self.assertEqual(source.old_combine_qty,20)

    def test_auto_preview_requires_read_permission_on_all_used_source_tables(self):
        from unittest.mock import patch
        job=self.job();process=self.process(job)
        def permission(permission,request,view):
            return request.path!='/api/system/erp_production_sourcedyeprocessschedule/'
        with patch('core.permissions.ApiPermission.has_permission',permission):
            response=self.client.post(f'/api/system/erp_production_sourcedyejobprocess/{process.pk}/preview_auto_combine/',
                {'plan_have_time':False,'as_of':self.at.isoformat()},format='json')
        self.assertEqual(response.status_code,403)
