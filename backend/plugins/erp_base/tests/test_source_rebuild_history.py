from datetime import datetime,timedelta
from decimal import Decimal
from django.apps import apps
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.business import snapshot
from plugins.erp_base.source_continuation import view_effects,save_effect
from plugins.erp_base.source_dye_rebuild import dye_sources,preview,rebuild,tail_values,active as quality_active
from plugins.erp_base.source_progress_maintenance import maintain
from plugins.erp_base.source_gray_history import preview as history_preview,recover,undo_recovery
from plugins.erp_base.source_gray_split_merge import active as gray_active
from plugins.erp_base.source_auto_combine import automatic_sync


class RebuildHistoryTests(TestCase):
    def setUp(self):
        self.actor=Users.objects.create_superuser(username='rebuild-history',password='test')
        self.client=APIClient();self.client.force_authenticate(self.actor)
        self.at=timezone.make_aware(datetime(2026,10,15,7,45))
        self.event=dict(at=self.at,reason='质量及历史逆向验收')

    def model(self,name,module='erp_production'):
        return apps.get_model(module+'.SourceDye'+name)

    def old(self,name,module='erp_production',**values):
        row=self.model(name,module).objects.create(**values);row.refresh_from_db();return row

    def job(self,number='A',**values):
        return self.old('JobSheet',old_sheet_series=number,old_sheet_no=number,old_job_kind_id='01',**values)

    def process(self,job,number=1,code='GX06',**values):
        return self.old('JobProcess',old_sheet_series=job.old_sheet_series,old_process_no=number,old_process_id=code,**values)

    def work(self,number='W',code='GX06',**values):
        return self.old('WProcess',old_wprocess_no=number,old_job_sheet_no='A',old_process_id=code,**values)

    def ready(self):
        job=self.job();process=self.process(job,old_status='1',old_end_time=self.at)
        self.work(old_end_time=self.at,old_curr_kg=Decimal('-3.25'),old_curr_rolls=Decimal('2.75'),old_class_id='03')
        return job,process

    def log(self,kind=0,status=0,**values):
        fields=dict(old_id='HISTORY',old_kind=kind,old_status=status,old_operate_date=self.at,old_data_table_name='qry_GrayStockBookRecord',
            old_ori_rece_sheet_no_list='R',old_ori_roll_no_list='001',old_ori_bar_code_list='CODE',
            old_new_roll_no_list='001,001-1',old_new_bar_code_list='CODE,CODE-1',old_ori_qty_list='重量：10；长度：20；匹数：2',
            old_new_qty_list='重量：6,4；长度：12,8；匹数：1,1',legacy_id='HISTORY')
        fields.update(values)
        return self.old('GrayRecordCutLogs','erp_warehouse',**fields)

    def gray(self,roll,code,weight,length,rolls,after=False,**values):
        return self.old('JobGrayRecord' if after else 'GrayInRecord','erp_production' if after else 'erp_warehouse',
            old_rece_sheet_no='R',old_roll_no=roll,old_bar_code=code,old_weight_qty=weight,old_length_qty=length,old_rolls=rolls,**values)

    def recovery(self,log,mode='archive',stage='before',measure='unknown',job=None,current=()):
        return recover(log,self.actor,stage,mode,measure,job,list(current),**self.event)

    def test_quality_uses_first_process_group_latest_ties_and_all_group_quantities(self):
        job=self.job();process=self.process(job,old_status='1',old_end_time=self.at)
        self.work('W1',old_end_time=self.at-timedelta(hours=1),old_curr_kg=Decimal('1.235'),old_curr_rolls=Decimal('2.9'))
        self.work('W2',old_end_time=self.at,old_curr_kg=Decimal('-3'),old_curr_rolls=Decimal('-1'))
        self.work('W3',old_end_time=self.at,old_curr_kg=None,old_curr_rolls=None)
        self.work('W4','GX07',old_end_time=self.at+timedelta(hours=1),old_curr_kg=100)
        result=preview(process,1)
        self.assertEqual(len(result['rows']),2)
        row=result['rows'][0]
        self.assertEqual(row['ClothQtyKg'],Decimal('-1.77'));self.assertEqual(row['Rolls'],1)
        self.assertEqual(row['DAYS'],'2026-10-14');self.assertEqual(row['Class'],'白班')
        self.assertEqual(row['RNum'],0);self.assertEqual(row['TNum'],1)
        self.assertEqual(len(result['supplemental_rows']),2)

    def test_quality_machine_bit4_and_missing_jobprocess_end_are_reported_not_deleted(self):
        job=self.job();process=self.process(job,old_status='1')
        work=self.work(old_end_time=self.at,old_machine_id='M')
        self.old('PMachine','erp_base',old_machine_id='M',old_bit4=True)
        result=preview(process,1);self.assertEqual(result['rows'],[]);self.assertTrue(result['supplemental_rows'])
        type(process).objects.filter(pk=process.pk).update(old_end_time=self.at)
        result=preview(process,1);self.assertEqual(result['rows'],[])
        self.assertTrue(any('bit4' in row['issue'] for row in result['supplemental_rows']))
        self.assertTrue(type(work).objects.filter(pk=work.pk).exists())

    def test_quality_add_number_and_jtimes_use_different_original_type_and_status_filters(self):
        job,process=self.ready()
        self.old('PStuff','erp_base',old_stuff_id='S',old_stuff_type='S')
        self.old('StuffWeight',old_sheet_series='SW1',old_sheet_no='ADD',old_job_sheet_no='A',old_sheet_kind=2,old_recipe_type=1,old_sheet_status=9)
        self.old('StuffWeightDetail',old_sheet_series='SW1',old_phase_no=1,old_stuff_no=1,old_stuff_id='S',old_stuff_type='A')
        self.old('StuffWeight',old_sheet_series='SW2',old_sheet_no='ADD2',old_job_sheet_no='A',old_sheet_kind=2,old_recipe_type=1,old_sheet_status=0)
        self.old('StuffWeightDetail',old_sheet_series='SW2',old_phase_no=1,old_stuff_no=1,old_stuff_id='UNKNOWN',old_stuff_type='S')
        row=preview(process,1)['rows'][0]
        self.assertEqual(row['AddNumber1'],1);self.assertEqual(row['JTimes'],1)
        self.assertEqual(row['ZNum'],0);self.assertEqual(row['JNum'],1);self.assertEqual(row['JKg'],Decimal('-3.25'))

    def test_color_digits_and_default_depth_preserve_null_empty_distinction(self):
        job,process=self.ready();type(job).objects.filter(pk=job.pk).update(old_color_num='X0012-A')
        first=self.old('PColorNum','erp_base',old_color_num='12',old_color_depth_id='01')
        second=self.old('PColorNum','erp_base',old_color_num='0012B',old_color_depth_id='')
        values,candidates=tail_values('A',lambda name,module:self.model(name,module).objects.all())
        self.assertEqual(values['ColorDepthID'],'');self.assertEqual(candidates,[second.pk])
        type(job).objects.filter(pk=job.pk).update(old_color_num=None)
        self.assertEqual(preview(process,1)['rows'][0]['ColorDepthID'],'05')

    def test_duplicate_job_and_defect_scalar_sources_are_expanded_with_evidence(self):
        job,process=self.ready();type(job).objects.filter(pk=job.pk).update(old_loss_str='LOSS')
        for index in range(2):self.old('WDefect','erp_quality',old_sheet_series=str(index),old_sheet_no='LOSS',old_defect_dept='03',old_defect_class_id='C'+str(index))
        self.old('JobSheet',old_sheet_series='B',old_sheet_no='A',old_job_kind_id=None,old_loss_str='LOSS')
        self.old('JobProcess',old_sheet_series='B',old_process_no=1,old_process_id='GX06',old_status='1',old_end_time=self.at)
        result=preview(process,1)
        self.assertEqual(len(result['rows']),4);self.assertTrue(any('标量' in note for note in result['notes']))
        self.assertEqual([row['WDNum'] for row in result['rows']],[1,1,1,1])
        self.assertEqual([row['RNum'] for row in result['rows']],[0,0,1,1])

    def test_completion_parameter_is_independent_and_unfinished_peer_blocks_original_tail(self):
        job,process=self.ready()
        self.assertEqual(preview(process,0)['rows'],[])
        peer=self.process(job,2,'GX07',old_status='4')
        self.assertEqual(preview(process,1)['rows'],[])
        type(peer).objects.filter(pk=peer.pk).update(old_status='1')
        self.assertEqual(len(preview(process,1)['rows']),1)

    def test_null_delete_variable_retains_original_rows_and_repeat_inserts_match_old_sql(self):
        job,process=self.ready()
        original=self.old('DyeCheckout','erp_quality',old_job_sheet_no='A',old_process_id='GX06',old_wprocess_no='OLD',legacy_id='OLD')
        first=rebuild(process,self.actor,1,**self.event);second=rebuild(process,self.actor,1,**self.event)
        self.assertEqual(first['retired_ids'],[]);self.assertEqual(len(first['created_ids']),1)
        self.assertEqual(self.model('DyeCheckout','erp_quality').objects.count(),3)
        original.refresh_from_db();self.assertEqual(original.legacy_id,'OLD');self.assertEqual(original.old_color_depth_id,'05')
        new=self.model('DyeCheckout','erp_quality').objects.get(pk=second['created_ids'][0]);self.assertIsNone(new.legacy_id)

    def test_explicit_delete_scope_retires_history_without_counting_it_again(self):
        job,process=self.ready()
        original=self.old('DyeCheckout','erp_quality',old_job_sheet_no='A',old_process_id='GX06',legacy_id='OLD')
        result=rebuild(process,self.actor,1,process_variable='GX06',**self.event)
        self.assertEqual(result['retired_ids'],[original.pk]);self.assertEqual(self.model('DyeCheckout','erp_quality').objects.count(),2)
        self.assertEqual(quality_active(self.model('DyeCheckout','erp_quality').objects.all()).count(),1)
        from plugins.erp_base.source_quality_reports import dye_quality_award
        report=dye_quality_award(self.at-timedelta(days=1),self.at+timedelta(days=1))
        self.assertEqual(report['source_ids'],result['created_ids'])

    def test_automatic_combine_reaches_quality_and_global_unrelated_progress(self):
        job,process=self.ready();other=self.job('OTHER');self.process(other,1,'RARE',old_status='0')
        result=automatic_sync(process,self.actor,None,2,False,self.at,completion_status=1,**self.event)
        other.refresh_from_db();self.assertEqual(other.old_next_process_id,'RARE')
        self.assertEqual(len(result['quality_rebuild']['created_ids']),1)

    def test_global_preview_is_read_only_and_apply_has_same_changes(self):
        job=self.job();self.process(job,1,'PENDING',old_status='0',old_station_id='S')
        excluded=self.job('CLOSED',old_sheet_status=9);self.process(excluded,1,'OTHER',old_status='0')
        before=snapshot(job);plan=maintain(self.actor,False,**self.event);job.refresh_from_db();self.assertEqual(snapshot(job),before)
        result=maintain(self.actor,True,**self.event);job.refresh_from_db()
        self.assertEqual(result['changed_count'],plan['changed_count']);self.assertEqual(job.old_next_process_id,'PENDING')
        self.assertEqual(len(result['rows']),1);self.assertEqual(maintain(self.actor,True,**self.event)['rows'],[])

    def test_global_empty_card_does_not_inherit_previous_card_variables(self):
        first=self.job();empty=self.job('EMPTY',old_curr_station_id='OLD',old_curr_process_no=5)
        self.process(first,1,'FIRST',old_status='0',old_station_id='S')
        result=maintain(self.actor,True,**self.event);empty.refresh_from_db()
        self.assertIsNone(empty.old_next_process_id);self.assertIsNone(empty.old_curr_process_no);self.assertIsNone(empty.old_curr_station_id)
        self.assertEqual(len(result['rows']),2)

    def test_global_done_running_unknown_and_retired_plans_all_accounted(self):
        job=self.job();self.process(job,1,'DONE',old_status='1');self.process(job,2,'RUNNING',old_status='5')
        unknown=self.job('ODD');p=self.process(unknown,1,'RARE',old_status='Z')
        retired=self.job('RETIRED');save_effect(retired,'card_adoption',{'state':'reversed'},self.actor,'保留撤回事实')
        result=maintain(self.actor,True,**self.event);job.refresh_from_db();unknown.refresh_from_db()
        self.assertEqual(job.old_curr_process_id,'RUNNING');self.assertEqual(job.old_next_process_id,'RUNNING')
        self.assertEqual(unknown.old_next_process_id,'RARE');self.assertEqual(result['supplemental_rows'][0]['process_id'],p.pk)
        self.assertEqual(result['retired_ids'],[retired.pk])

    def test_plain_old_quantity_stays_unclassified_until_explicit_measure(self):
        log=self.log(old_ori_qty_list='23.20',old_new_qty_list='20.20,3.00')
        report=history_preview(log);self.assertEqual(report['rows'][0]['unclassified_quantity'],Decimal('23.20'))
        self.assertNotIn('WeightQty',report['rows'][0]);self.assertTrue(report['supplemental_rows'])
        report=history_preview(log,'LengthQty');self.assertEqual(report['rows'][0]['LengthQty'],Decimal('23.20'))
        self.assertEqual(report['result_rows'][1]['ReceSheetNo'],'R')

    def test_archive_restores_known_fields_without_fake_legacy_id_or_stock_effects(self):
        log=self.log(old_ori_qty_list='23.20',old_new_qty_list='20.20,3.00');before=snapshot(log)
        result=self.recovery(log);row=self.model('GrayInRecord','erp_warehouse').objects.get(pk=result['result_rows'][0]['record_id'])
        self.assertIsNone(row.old_weight_qty);self.assertIsNone(row.legacy_id);self.assertEqual(row.old_bar_code,'CODE')
        self.assertEqual(gray_active(type(row).objects.all()).count(),0)
        self.assertEqual(view_effects(row)['history_gray_origin']['logged_values']['unclassified_quantity'],'23.20')
        log.refresh_from_db();self.assertEqual(snapshot(log),before)
        self.assertEqual(self.model('GrayStockBook','erp_warehouse').objects.count(),0)

    def test_failed_old_operation_is_archivable_but_never_reversed_as_success(self):
        log=self.log(status=100,old_new_rece_sheet_no_list='保存失败，事务已回滚')
        with self.assertRaises(ValidationError):self.recovery(log,mode='reverse')
        result=self.recovery(log);self.assertEqual(result['rows'][0]['created_count'],1)
        self.assertTrue(any('成功状态' in text for text in history_preview(log)['notes']))

    def test_reverse_historical_split_restores_original_layout_and_can_undo_recovery(self):
        log=self.log();a=self.gray('001','CODE',6,12,1);b=self.gray('001-1','CODE-1',4,8,1)
        detail=self.old('GrayInDetail','erp_warehouse',old_rece_sheet_no='R',old_sheet_series='H',old_weight_qty=99,old_rolls=9)
        result=self.recovery(log,'reverse',current=[a,b]);new=self.model('GrayInRecord','erp_warehouse').objects.get(pk=result['result_rows'][0]['record_id'])
        self.assertEqual(new.old_weight_qty,10);self.assertEqual(gray_active(type(a).objects.all()).count(),1)
        detail.refresh_from_db();self.assertEqual(detail.old_weight_qty,10);self.assertEqual(detail.old_rolls,2)
        undo_recovery(log,self.actor,**self.event);detail.refresh_from_db();self.assertEqual(detail.old_weight_qty,99)
        self.assertEqual(set(gray_active(type(a).objects.all()).values_list('pk',flat=True)),{a.pk,b.pk})
        self.assertTrue(type(new).objects.filter(pk=new.pk).exists())

    def test_reverse_historical_merge_restores_all_original_negative_and_null_rows(self):
        log=self.log(kind=1,old_ori_rece_sheet_no_list='R,R',old_ori_roll_no_list='001,002',old_ori_bar_code_list='SAME,SAME',
            old_ori_qty_list='重量：-2,5；长度：NULL,20；匹数：1,1',old_new_rece_sheet_no_list='R',old_new_roll_no_list='001',old_new_bar_code_list='SAME',
            old_new_qty_list='重量：3；长度：20；匹数：2')
        current=self.gray('001','SAME',3,20,2)
        result=self.recovery(log,'reverse',current=[current]);active=gray_active(type(current).objects.all()).order_by('pk')
        self.assertEqual(list(active.values_list('old_weight_qty',flat=True)),[Decimal('-2'),Decimal('5')]);self.assertIsNone(active.first().old_length_qty)
        self.assertEqual(result['rows'][0]['created_count'],2)

    def test_after_dispatch_history_requires_explicit_job_and_restores_assignment(self):
        log=self.log(old_data_table_name='JobGrayRecord');job=self.job()
        with self.assertRaises(ValidationError):self.recovery(log,stage='after')
        a=self.gray('001','CODE',6,12,1,after=True,old_sheet_series='A');b=self.gray('001-1','CODE-1',4,8,1,after=True,old_sheet_series='A')
        assigned=self.old('JobAssign',old_sheet_series='A',old_assign_no=1,old_rece_sheet_no='R',old_weight_qty=55)
        result=self.recovery(log,'reverse','after',job=job,current=[a,b]);assigned.refresh_from_db();job.refresh_from_db()
        self.assertEqual(assigned.old_weight_qty,10);self.assertEqual(job.old_pre_vat_qty,20)
        undo_recovery(log,self.actor,**self.event);assigned.refresh_from_db();self.assertEqual(assigned.old_weight_qty,55)

    def test_history_current_quantity_change_rejects_whole_operation(self):
        log=self.log();a=self.gray('001','CODE',7,12,1);b=self.gray('001-1','CODE-1',4,8,1)
        with self.assertRaises(ValidationError):self.recovery(log,'reverse',current=[a,b])
        self.assertEqual(type(a).objects.count(),2);self.assertEqual(gray_active(type(a).objects.all()).count(),2)

    def test_history_malformed_truncated_lists_are_reported_and_not_used_to_reverse(self):
        log=self.log(old_ori_qty_list='重量：12.5坏值；长度：20；匹数：2',old_ori_roll_no_list='001,002')
        report=history_preview(log);self.assertTrue(report['supplemental_rows']);self.assertEqual(len(report['rows']),2)
        with self.assertRaises(ValidationError):self.recovery(log,'reverse')

    def test_repeated_history_recovery_and_changed_recovered_result_have_explicit_errors(self):
        log=self.log();result=self.recovery(log)
        with self.assertRaises(ValidationError):self.recovery(log)
        model=self.model('GrayInRecord','erp_warehouse');model.objects.filter(pk=result['result_rows'][0]['record_id']).update(old_weight_qty=9)
        with self.assertRaises(ValidationError):undo_recovery(log,self.actor,**self.event)

    def test_http_quality_preview_rebuild_and_global_preview(self):
        job,process=self.ready();root=f'/api/system/erp_production_sourcedyejobprocess/{process.pk}/'
        response=self.client.post(root+'preview_dye_quality/',{'completion_status':1},format='json')
        self.assertEqual(response.status_code,200,response.data);self.assertEqual(len(response.data['data']['rows']),1)
        response=self.client.post(root+'rebuild_dye_quality/',{'completion_status':1,'at':self.at.isoformat(),'reason':'重建'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        response=self.client.post('/api/system/erp_production_sourcedyejobsheet/preview_progress/',{},format='json')
        self.assertEqual(response.status_code,200,response.data)

    def test_http_history_preview_archive_and_recovery_undo(self):
        log=self.log();root=f'/api/system/erp_warehouse_sourcedyegrayrecordcutlogs/{log.pk}/'
        response=self.client.post(root+'history_recovery_preview/',{'measure':'unknown'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        response=self.client.post(root+'recover_history/',{'mode':'archive','stage':'before','measure':'unknown','at':self.at.isoformat(),'reason':'留档'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        response=self.client.post(root+'undo_history_recovery/',{'at':self.at.isoformat(),'reason':'撤回'},format='json')
        self.assertEqual(response.status_code,200,response.data)

    def test_quality_shift_uses_old_second_precision_and_keeps_null_sums(self):
        job=self.job();process=self.process(job,old_status='1',old_end_time=self.at)
        end=timezone.make_aware(datetime(2026,10,15,19,30,0,500000))
        self.work(old_end_time=end,old_curr_kg=None,old_curr_rolls=None)
        result=preview(process,1)['rows'][0]
        self.assertEqual(result['Class'],'白班');self.assertIsNone(result['ClothQtyKg']);self.assertIsNone(result['Rolls'])

    def test_global_actions_require_related_process_read_permission(self):
        from unittest.mock import patch
        self.job()
        def permission(permission,request,view):return request.path!='/api/system/erp_production_sourcedyejobprocess/'
        with patch('core.permissions.ApiPermission.has_permission',permission):
            response=self.client.post('/api/system/erp_production_sourcedyejobsheet/preview_progress/',{},format='json')
        self.assertEqual(response.status_code,403)

    def test_history_archive_and_quality_generated_rows_cannot_bypass_fact_retention_by_delete(self):
        from plugins.erp_base.source_services import delete_documents
        log=self.log();result=self.recovery(log)
        row=self.model('GrayInRecord','erp_warehouse').objects.get(pk=result['result_rows'][0]['record_id'])
        for item in [log,row]:
            with self.assertRaises(ValidationError):delete_documents(type(item).objects.filter(pk=item.pk),self.actor)
        job,process=self.ready();quality=rebuild(process,self.actor,1,**self.event)
        with self.assertRaises(ValidationError):delete_documents(self.model('DyeCheckout','erp_quality').objects.filter(pk__in=quality['created_ids']),self.actor)
