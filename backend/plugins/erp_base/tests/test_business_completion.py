from decimal import Decimal
from datetime import timedelta,datetime
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.source_phase3_operations import model
from plugins.erp_base.source_context import SourceDocumentContext
from plugins.erp_base.source_execution_state import active


class CompletionTests(TestCase):
    def setUp(self):
        self.actor=Users.objects.create(username='completion',is_superuser=True)
        self.client=APIClient();self.client.force_authenticate(self.actor);self.at=timezone.now()

    def url(self,table,pk=None):return '/api/system/'+model(table)._meta.label_lower.replace('.','_')+'/'+(str(pk)+'/' if pk else '')
    def ok(self,r):self.assertEqual(r.status_code,200,r.data);return r.data['data']
    def create(self,table,entry=None,**data):
        if entry:data['_entry']=entry
        result=self.ok(self.client.post(self.url(table),data,format='json'));return model(table).objects.get(pk=result['id'])
    def action(self,item,name,**data):return self.client.post(self.url(item.SOURCE_TABLE,item.pk)+name+'/',data,format='json')
    def event(self):return {'at':self.at.isoformat(),'reason':'开发独立验证'}
    def order(self):
        head=self.create('OrderMain','OrderMain',old_customer_id='C')
        line=self.create('OrderColor','OrderColor',source_parent_1=head.pk,old_prod_id='P',old_order_qty='10',old_unit='KG')
        return head,line
    def route(self):
        route=model('p_FieldValid').objects.create(old_field_type='Production',old_code='PT01',old_name='测试路线')
        for n,p in [(1,'GX01'),(2,'GX06'),(3,'GX98')]:
            model('p_FieldValidSub').objects.create(old_field_type='Production',old_code='PT01',old_sub_code=p,old_sort_value=n,source_parent_1=route)
        return route
    def open(self,line,head,route=None,**extra):
        return self.action(line,'open_first_card',head=head.pk,quantity='10',rolls=None,unit=1,yarn='客户来纱',
            route=None if route is None else route.pk,**self.event(),**extra)

    def test_b01_first_card_members_preallocation_and_route_are_one_transaction(self):
        head,line=self.order();route=self.route()
        result=self.ok(self.open(line,head,route,assignments=[{'ReceSheetNo':'R','GrayID':'G','Rolls':-1,'WeightQty':0}]))
        job=model('JobSheet').objects.get(pk=result['id'])
        self.assertEqual(job.old_check_no,line.old_check_no)
        # 原F110：工卡预投量汇总JobAssign.WeightQty；订单分配量保留在合单明细。
        self.assertEqual(job.old_pre_vat_qty,Decimal('0'))
        member=model('JobCombineOrder').objects.get()
        self.assertEqual(member.source_parent_1,job);self.assertEqual(member.old_combine_qty,Decimal('10'))
        self.assertEqual(model('JobAssign').objects.get().old_rolls,Decimal('-1'))
        self.assertEqual(list(model('JobProcess').objects.order_by('pk').values_list('old_process_id',flat=True)),['GX01','GX06','GX98'])
        self.assertEqual(model('StuffStockBook').objects.count(),0)
        self.assertEqual(SourceDocumentContext.objects.get(entity=job._meta.label,object_id=job.pk).effects['first_card_origin']['line']['source']['id'],line.pk)

    def test_b01_bad_last_preallocation_rolls_back_card_and_members(self):
        head,line=self.order()
        response=self.open(line,head,assignments=[{'GrayID':'G'},{'NO_FIELD':'x'}]);self.assertEqual(response.status_code,400,response.data)
        self.assertFalse(model('JobSheet').objects.exists());self.assertFalse(model('JobCombineOrder').objects.exists())

    def test_b01_multi_order_qty_null_negative_and_duplicate_source_records(self):
        head,line=self.order()
        second=self.create('OrderColor','OrderColor',source_parent_1=head.pk,old_prod_id='P',old_unit='KG',old_order_qty='-2')
        data=self.ok(self.open(line,head,members=[{'line_id':second.pk,'quantity':'-2'}]))
        job=model('JobSheet').objects.get(pk=data['id']);self.assertEqual(job.old_pre_vat_qty,Decimal('8'))
        self.assertEqual(model('JobCombineOrder').objects.count(),2)
        self.assertEqual(self.open(line,head,members=[{'line_id':line.pk,'quantity':0}]).status_code,400)

    def test_b01_empty_optional_inputs_are_null_not_zero_or_order_qty(self):
        head,line=self.order()
        result=self.ok(self.action(line,'open_first_card',head=head.pk,yarn='客户来纱',**self.event()))
        job=model('JobSheet').objects.get(pk=result['id'])
        self.assertIsNone(job.old_assign_unit);self.assertIsNone(model('JobCombineOrder').objects.get().old_combine_qty)
        self.assertEqual(job.old_sheet_no,job.old_new_sheet_no)

    def test_b01_explicit_number_prefix_uses_original_format_and_complete_sequence(self):
        from plugins.erp_base import source_services
        head,line=self.order()
        day=timezone.localtime(self.at).strftime('%y%m%d')
        model('JobSheet').objects.create(old_new_sheet_no='J01-'+day+'99')
        result=self.ok(self.open(line,head,self.route(),number_prefix='J01'))
        job=model('JobSheet').objects.get(pk=result['id'])
        self.assertEqual(job.old_new_sheet_no,'J01-'+day+'100');self.assertEqual(job.old_sheet_no,day+'J01100')
        source_services.write(type(job),{'old_remarks':'再保存不截断完整号'},job,self.actor);job.refresh_from_db()
        self.assertEqual(job.old_sheet_no,day+'J01100')

    def test_b01_route_duplicate_and_null_process_rows_are_not_filtered(self):
        job=self.create('JobSheet','JobSheet');route=self.route()
        model('p_FieldValidSub').objects.create(old_field_type='Production',old_code='PT01',old_sub_code='GX06',old_sort_value=2,source_parent_1=route)
        self.ok(self.action(job,'adopt_route',route=route.pk,**self.event()))
        self.assertEqual(model('JobProcess').objects.count(),4)
        r=self.action(job,'adopt_route',route=route.pk,**self.event());self.assertEqual(r.status_code,400,r.data)

    def test_b02_carry_and_both_tighttube_variants_bind_original_series(self):
        for table,entry,child,child_entry in [('CarryMaterial','CarryMaterial','CarryMaterialDetail','CarryMaterialDetail'),
            ('TightTube','CancelTightTube','TightTubeDetail','CancelTightTubeDetail'),('TightTube','TightTubeBalance','TightTubeDetail','TightTubeBalanceDetail')]:
            with self.subTest(entry=entry):
                head=self.create(table,entry)
                detail=self.create(child,child_entry,source_parent_1=head.pk,old_detail_no=entry+'-01',old_qty='-1')
                self.assertEqual(detail.old_sheetseries,head.old_sheet_series);self.assertEqual(detail.source_parent_1,head)
                entity=model(child)._meta.label_lower.replace('.','_')
                r=self.action(head,'save_document',head={'old_remarks':'整单'},children={entity:{'upsert':[{'id':detail.pk,'old_qty':None},{'old_detail_no':entry+'-01','old_qty':0}],'delete':[]}})
                self.ok(r);detail.refresh_from_db();self.assertIsNone(detail.old_qty)
                self.assertEqual(model(child).objects.filter(source_parent_1=head).count(),2)

    def test_b03_completed_work_auto_updates_plan_and_delete_rebuilds(self):
        job=self.create('JobSheet','JobSheet')
        plan=self.create('JobProcess','JobProcess',source_parent_1=job.pk,old_process_no=1,old_process_id='GX01',old_status='0')
        work=self.create('WProcess','WProcessEdit',old_job_sheet_no=job.old_sheet_no,old_process_no=1,old_process_id='GX01',old_start_time=self.at,old_end_time=self.at-timedelta(seconds=2),old_curr_kg='-1')
        plan.refresh_from_db();self.assertEqual(plan.old_status,'1');self.assertEqual(plan.old_end_time,self.at-timedelta(seconds=2))
        self.assertEqual(plan.old_wprocess_no,work.old_wprocess_no)
        self.ok(self.client.delete(self.url('WProcess',work.pk)));plan.refresh_from_db();self.assertEqual(plan.old_status,'0');self.assertIsNone(plan.old_end_time)

    def test_b03_explicit_start_then_end_without_extra_confirmation(self):
        job=self.create('JobSheet','JobSheet')
        plan=self.create('JobProcess','JobProcess',source_parent_1=job.pk,old_process_no=1,old_process_id='GX01',old_status='0')
        work=self.create('WProcess','WProcessEdit',old_job_sheet_no=job.old_sheet_no,old_process_no=1,old_process_id='GX01',old_start_time=self.at,old_end_time=None,old_status='4')
        self.assertIsNone(work.old_end_time);plan.refresh_from_db();self.assertEqual(plan.old_status,'4')
        job.refresh_from_db();self.assertEqual(job.old_curr_process_id,'GX01')
        self.ok(self.client.patch(self.url('WProcess',work.pk),{'old_end_time':self.at.isoformat(),'old_status':'1'},format='json'))
        plan.refresh_from_db();self.assertEqual(plan.old_status,'1')

    def test_b03_original_empty_end_sentinel_is_not_completion_and_is_retained(self):
        job=self.create('JobSheet','JobSheet')
        plan=self.create('JobProcess','JobProcess',source_parent_1=job.pk,old_process_no=1,old_process_id='GX07',old_status='0')
        sentinel=timezone.make_aware(datetime(1900,1,1))
        work=self.create('WProcess','WProcessEdit',old_job_sheet_no=job.old_sheet_no,old_process_no=1,old_process_id='GX07',old_start_time=self.at,old_end_time=sentinel,old_status='4')
        plan.refresh_from_db();self.assertEqual(plan.old_status,'4');self.assertIsNone(plan.old_end_time)
        self.assertEqual(work.old_end_time,sentinel);self.assertEqual(work.old_status,'4')
        self.assertFalse(model('dyeCheckout').objects.exists())

    def test_b03_explicit_running_status_without_time_is_preserved(self):
        job=self.create('JobSheet','JobSheet')
        plan=self.create('JobProcess','JobProcess',source_parent_1=job.pk,old_process_no=1,old_process_id='GX01',old_status='0')
        self.create('WProcess','WProcessEdit',old_job_sheet_no=job.old_sheet_no,old_process_no=1,old_process_id='GX01',old_start_time=None,old_end_time=None,old_status='5')
        plan.refresh_from_db();self.assertEqual(plan.old_status,'5');self.assertIsNone(plan.old_start_time);self.assertIsNone(plan.old_end_time)

    def test_b04_flat_material_views_keep_canonical_atomic_phase_path(self):
        for table in ['DyeRecipe','StuffWeight']:
            entity=model(table)._meta.label_lower.replace('.','_')
            workflow=self.ok(self.client.get('/api/meta/'+entity+'/'))['workflow']
            self.assertTrue(any(child.get('parent_field')=='old_sheet_series' and child['atomic'] is False for child in workflow['children']))
            self.assertTrue(any(child.get('parent_field')=='old_sheet_series' and '所有染程' in child['title'] for child in workflow['children']))
            self.assertTrue(any(child['atomic'] is True for child in workflow['children']))

    def test_b04_dye_quality_rebuild_after_completed_work_keeps_previous_versions(self):
        job=self.create('JobSheet','JobSheet',old_prod_id='P',old_customer_id='C',old_job_kind_id='01')
        plan=self.create('JobProcess','JobProcess',source_parent_1=job.pk,old_process_no=1,old_process_id='GX06',old_status='0')
        work=self.create('WProcess','WProcessEdit',old_job_sheet_no=job.old_sheet_no,old_process_no=1,old_process_id='GX06',old_start_time=self.at,old_end_time=self.at,old_curr_kg='10')
        self.assertEqual(model('dyeCheckout').objects.count(),1)
        self.ok(self.client.patch(self.url('WProcess',work.pk),{'old_curr_kg':'12'},format='json'))
        self.assertEqual(model('dyeCheckout').objects.count(),2)
        from plugins.erp_base.source_dye_rebuild import active as current_quality
        self.assertEqual(list(current_quality(model('dyeCheckout').objects.all()).values_list('old_cloth_qty_kg',flat=True)),[12])

    def test_b05_ordinary_work_auto_combines_and_replaces_current_quality(self):
        first=self.create('JobSheet','JobSheet',old_job_kind_id='01')
        second=self.create('JobSheet','JobSheet',old_job_kind_id='01')
        for job in [first,second]:self.create('JobProcess','JobProcess',source_parent_1=job.pk,old_process_no=1,old_process_id='GX07',old_status='0')
        self.create('ProcessSchedule',old_job_sheet_no=first.old_sheet_no,old_process_no=1,old_process_id='GX07',old_combine_sheet_nos=second.old_sheet_no+':1')
        work=self.create('WProcess','WProcessEdit',old_job_sheet_no=first.old_sheet_no,old_process_no=1,old_process_id='GX07',old_end_time=self.at,old_curr_kg='10')
        target=model('JobProcess').objects.get(source_parent_1=second);self.assertEqual(target.old_status,'1')
        from plugins.erp_base.source_dye_rebuild import active as current_quality
        count=current_quality(model('dyeCheckout').objects.all()).count();self.assertGreater(count,0)
        self.ok(self.client.patch(self.url('WProcess',work.pk),{'old_curr_kg':'12'},format='json'))
        self.assertEqual(current_quality(model('dyeCheckout').objects.all()).count(),count)
        self.assertGreater(model('dyeCheckout').objects.count(),count)

    def test_b03_unmatched_null_and_non_numeric_status_remain_readable(self):
        job=self.create('JobSheet','JobSheet')
        self.create('JobProcess','JobProcess',source_parent_1=job.pk,old_process_no=1,old_process_id='停用工序',old_status='异')
        work=self.create('WProcess','WProcessEdit',old_job_sheet_no=job.old_sheet_no,old_process_no=None,old_process_id=None,old_curr_kg=None)
        self.assertIsNone(work.old_process_id)
        context=SourceDocumentContext.objects.get(entity=work._meta.label,object_id=work.pk)
        self.assertTrue(context.effects['work_plan_progress']['unmatched'])

    def test_b04_review_entry_creates_rework_and_keeps_original_review(self):
        job=self.create('JobSheet','JobSheet')
        plan=self.create('JobProcess','JobProcess',source_parent_1=job.pk,old_process_no=1,old_process_id='GX15')
        for entry in ['WDefectJudgeBack','WDefectJudgeInterior','WDefectOther']:
            review=self.create('WDefect',entry,old_job_sheet_no=job.old_sheet_no,old_kind='原少用类别')
            result=self.ok(self.action(review,'open_rework_card',job=job.pk,processes=[plan.pk],quantity='-2',rolls=None,unit=1,sheet_kind=10,job_kind='02',**self.event()))
            target=model('JobSheet').objects.get(pk=result['id'])
            self.assertEqual(target.old_loss_str,review.old_sheet_no)
            self.assertEqual(model('JobProcess').objects.get(source_parent_1=target).old_process_id,'GX15')
        self.assertEqual(model('WDefect').objects.count(),3)

    def test_b04_recipe_explicit_references_keep_duplicate_codes_and_snapshot(self):
        color=self.create('DyeLabColor',old_color_no='同来样码')
        original=self.create('DyeRecipe',old_sheet_no='同配方号')
        standard=self.create('DyeRecipe',old_sheet_no='同配方号')
        target=self.create('DyeRecipe')
        self.ok(self.action(target,'adopt_recipe_references',color=color.pk,original=original.pk,standard=standard.pk,**self.event()))
        target.refresh_from_db()
        self.assertEqual((target.old_color_no,target.old_ori_recipe_sheet_no,target.old_stand_recipe_no),('同来样码','同配方号','同配方号'))
        context=SourceDocumentContext.objects.get(entity=target._meta.label,object_id=target.pk)
        selected=context.effects['recipe_reference_origin']['selected']
        self.assertEqual(selected['original']['source']['id'],original.pk);self.assertEqual(selected['standard']['source']['id'],standard.pk)
        self.ok(self.action(target,'adopt_recipe_references',color=None,**self.event()))
        target.refresh_from_db();self.assertIsNone(target.old_color_no);self.assertEqual(target.old_ori_recipe_sheet_no,'同配方号')
        context.refresh_from_db();self.assertEqual(context.effects['recipe_reference_origin']['selected']['standard']['source']['id'],standard.pk)

    def test_b04_flat_material_filter_uses_header_series_and_keeps_duplicates(self):
        for table in ['DyeRecipe','StuffWeight']:
            head=self.create(table,old_sheet_series=table)
            phase=self.create(table+'Phase',source_parent_1=head.pk,old_phase_no='01',old_phase_id='TEST')
            for _ in range(2):self.create(table+'Detail',source_parent_1=phase.pk,old_stuff_no=1,old_stuff_id='RAW')
            other=self.create(table,old_sheet_series='OTHER'+table)
            p=self.create(table+'Phase',source_parent_1=other.pk,old_phase_no='01')
            self.create(table+'Detail',source_parent_1=p.pk,old_stuff_no=1,old_stuff_id='RAW')
            response=self.client.get(self.url(table+'Detail'),{'old_sheet_series':head.old_sheet_series})
            self.ok(response);self.assertEqual(response.data['total'],2,response.data)

    def test_b04_department_receive_saves_and_reverses_current_process(self):
        job=self.create('JobSheet','JobSheet')
        receipt=self.create('GetJobSheetReceive','GetJobSheetReceive',old_job_sheet_no=job.old_sheet_no,old_dept_id='DT036',old_create_date=self.at)
        job.refresh_from_db();self.assertEqual(job.old_curr_process_id,'染部收单')
        self.ok(self.client.delete(self.url('GetJobSheetReceive',receipt.pk)))
        job.refresh_from_db();self.assertIsNone(job.old_curr_process_id)

    def test_b06_loading_selects_actual_duplicate_codes_without_stock(self):
        head=self.create('ProdLoading','ProdLoading')
        lines=[self.create('ProdOutDetail',old_detail_no='同号',old_weight_qty=qty) for qty in ['-2','0']]
        result=self.ok(self.action(head,'add_outgoing_lines',lines=[x.pk for x in lines],**self.event()))
        self.assertEqual(len(result['created_line_ids']),2)
        self.assertEqual(list(model('ProdLoadingDetail').objects.order_by('pk').values_list('old_out_detail_no',flat=True)),['同号','同号'])
        self.assertEqual(model('ProdStockBook').objects.count(),0)

    def test_b06_job_warehouse_register_keeps_source_and_no_inventory(self):
        incoming=self.create('JobInWareEdit','JobInWareEdit',old_job_sheet_no='原卡',old_weight_qty=10)
        result=self.ok(self.action(incoming,'register_outgoing',rolls=None,weight='-2',**self.event()))
        outgoing=model('JobOutWareEdit').objects.get(pk=result['id'])
        self.assertEqual(outgoing.old_in_ware_sheet_no,incoming.old_sheet_no)
        self.assertEqual(outgoing.old_weight_qty,-2);incoming.refresh_from_db();self.assertEqual(incoming.old_weight_qty,10)
        self.assertEqual(model('ProdStockBook').objects.count(),0)
        response=self.client.patch(self.url('JobInWareEdit',incoming.pk),{'old_remarks':'出仓后尝试改原进仓'},format='json')
        self.assertEqual(response.status_code,400,response.data)

    def test_b06_complaint_detail_uses_original_sheetseries_spelling_and_number(self):
        head=self.create('CustomerTS','CustomerTS')
        for entry in ['CustomerTSDetail','CustomerTSSumInfo']:
            line=self.create('CustomerTSDetail',entry,source_parent_1=head.pk,old_job_sheet_no='未匹配原卡')
            self.assertEqual(line.old_sheetseries,head.old_sheet_series)
            if entry=='CustomerTSDetail':self.assertTrue(line.old_detail_no.startswith(head.old_sheet_series+'-'))
            else:self.assertEqual(line.old_detail_no,'')  # 原汇总查询入口无DetailNo取号规则。
        self.assertEqual(model('CustomerTSDetail').objects.count(),2)

    def test_b06_series_row_numbers_are_local_to_each_complaint_head(self):
        orphan=model('CustomerTSDetail').objects.create(old_sheetseries='',old_detail_no='未匹配旧号')
        first=self.create('CustomerTS','CustomerTS',old_sheet_series='BC-A')
        second=self.create('CustomerTS','CustomerTS',old_sheet_series='BC-B')
        a=self.create('CustomerTSDetail','CustomerTSDetail',source_parent_1=first.pk)
        b=self.create('CustomerTSDetail','CustomerTSDetail',source_parent_1=second.pk)
        c=self.create('CustomerTSDetail','CustomerTSDetail',source_parent_1=first.pk)
        self.assertEqual([a.old_detail_no,b.old_detail_no,c.old_detail_no],['BC-A-01','BC-B-01','BC-A-02'])
        orphan.refresh_from_db();self.assertEqual(orphan.old_detail_no,'未匹配旧号');self.assertEqual(orphan.old_sheetseries,'')

    def test_b05_shared_material_head_and_explicit_loading_cancel_restore(self):
        from plugins.erp_base.source_chain_reverse import discover,cancel,undo
        from plugins.erp_base.source_execution_state import active
        first=self.create('JobSheet','JobSheet');second=self.create('JobSheet','JobSheet')
        head=self.create('CarryMaterial','CarryMaterial')
        a=self.create('CarryMaterialDetail','CarryMaterialDetail',source_parent_1=head.pk,old_job_sheet_no=first.old_sheet_no)
        b=self.create('CarryMaterialDetail','CarryMaterialDetail',source_parent_1=head.pk,old_job_sheet_no=second.old_sheet_no)
        out=self.create('ProdOutDetail',old_detail_no='DUP',old_job_sheet_no=first.old_sheet_no)
        other=self.create('ProdOutDetail',old_detail_no='DUP',old_job_sheet_no=second.old_sheet_no)
        loading=self.create('ProdLoading','ProdLoading')
        result=self.ok(self.action(loading,'add_outgoing_lines',lines=[out.pk,other.pk],**self.event()))
        x,y=[model('ProdLoadingDetail').objects.get(pk=pk) for pk in result['created_line_ids']]
        found=discover(first)
        self.assertIn((a._meta.label,a.pk),found['nodes']);self.assertNotIn((b._meta.label,b.pk),found['nodes'])
        self.assertIn((x._meta.label,x.pk),found['nodes']);self.assertNotIn((y._meta.label,y.pk),found['nodes'])
        cancel(first,self.actor,mode='execution_only',work_mode='trigger_then_maintenance',at=self.at,reason='独立共享撤回')
        for row in [a,x]:self.assertFalse(active(type(row).objects.filter(pk=row.pk)).exists())
        for row in [head,b,loading,y]:self.assertTrue(active(type(row).objects.filter(pk=row.pk)).exists())
        undo(first,self.actor,at=self.at,reason='独立共享恢复')
        for row in [a,b,x,y]:self.assertTrue(active(type(row).objects.filter(pk=row.pk)).exists())
