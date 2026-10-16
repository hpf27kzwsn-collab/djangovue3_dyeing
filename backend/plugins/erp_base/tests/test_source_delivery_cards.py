from datetime import datetime
from decimal import Decimal
from django.apps import apps
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base import source_services as services
from plugins.erp_base.business import snapshot
from plugins.erp_base.models import BusinessAction
from plugins.erp_base.source_context import SourceDocumentContext
from plugins.erp_base.source_continuation import view_effects
from plugins.erp_base.source_delivery_flow import (return_material, factory_quality, receive_package,
    dispatch_product, receive_delivery_return, confirm_delivery)
from plugins.erp_base.source_job_flow import split_card, merge_cards, transfer_allocation, combine_members, sync_combined_process


class DeliveryCardTests(TestCase):
    def setUp(self):
        self.actor=Users.objects.create_superuser(username='delivery-cards',password='test')
        self.client=APIClient();self.client.force_authenticate(self.actor)
        self.at=timezone.make_aware(datetime(2026,10,15,12))
        self.movement=dict(weight=Decimal('-2.5'),length=None,rolls=Decimal('1.5'),warehouse='W',
            unit=1,sheet_kind=16,at=self.at,reason='原异常负量接续')

    def model(self,name,module='erp_warehouse'):
        return apps.get_model(module+'.SourceDye'+name)

    def old(self,name,module='erp_warehouse',**values):
        item=self.model(name,module).objects.create(**values)
        item.refresh_from_db()
        return item

    def write(self,name,module='erp_warehouse',**values):
        return services.write(self.model(name,module),values,actor=self.actor)

    def job(self,**values):
        return self.old('JobSheet','erp_production',old_sheet_series='J',old_sheet_no='JOB',
            old_pre_vat_qty=Decimal('100'),old_pre_rolls=10,old_assign_unit=1,legacy_id='J',**values)

    def test_material_return_both_families_keep_negative_null_and_source(self):
        for table,key,incoming in [('GrayOutDetail','old_assigned_no','GrayIn'),('SemiOutDetail','old_detail_no','SemiIn')]:
            source=self.old(table,old_sheet_series='ORPHAN',**{key:table},old_weight_qty=100,old_price=Decimal('2.50'),legacy_id=table)
            before=snapshot(source)
            result=return_material(source,self.actor,customer='C',**self.movement)
            line=self.model(incoming+'Detail').objects.get(source_parent_1=result)
            self.assertEqual(line.old_weight_qty,Decimal('-2.5'));self.assertIsNone(line.old_length_qty)
            self.assertEqual(line.old_amount,Decimal('-6.25'));self.assertEqual(result.old_customer_id,'C')
            self.assertEqual(view_effects(result)['material_return_origin']['source']['legacy_id'],table)
            source.refresh_from_db();self.assertEqual(snapshot(source),before)
            self.assertIsNone(result.legacy_id)

    def test_factory_dispositions_have_audit_and_do_not_change_old_quality_or_stock(self):
        source=self.old('ProdIn',old_sheet_series='R',old_right_status=99,old_weight_qty=-4,legacy_id='R')
        inspection=self.old('WDefect','erp_quality',old_sheet_series='Q',old_sheet_no='Q',legacy_id='Q')
        before=snapshot(source)
        for result in ['released','concession','hold','return','withdrawn']:
            factory_quality(source,self.actor,'FACT',result,inspection,self.at,'明确质量处置')
        source.refresh_from_db();self.assertEqual(snapshot(source),before)
        self.assertEqual(view_effects(source)['factory_quality']['result'],'withdrawn')
        self.assertEqual(BusinessAction.objects.filter(action='factory_quality').count(),5)
        self.assertEqual(self.model('ProdStockBook').objects.count(),0)

    def test_duplicate_packaging_labels_use_selected_row_and_actual_receipt(self):
        first=self.old('RecordYield',old_guid='A',old_bar_code='SAME',old_kg=123,old_net_kg=-9,legacy_id='A')
        second=self.old('RecordYield',old_guid='B',old_bar_code='SAME',old_kg=99,legacy_id='B')
        target=receive_package(second,self.actor,**self.movement)
        line=self.model('ProdInRecord').objects.get(source_parent_1=target)
        self.assertEqual(target.old_weight_qty,Decimal('-2.5'));self.assertEqual(line.old_prod_bar_code,'SAME')
        self.assertIsNone(line.old_net_kg)
        self.assertEqual(view_effects(target)['package_receipt_origin']['source']['legacy_id'],'B')
        first.refresh_from_db();self.assertEqual(first.old_net_kg,-9)
        stock=self.model('ProdStockBook').objects.get(old_sheet_series=target.old_sheet_series)
        self.assertEqual(stock.old_in_weight_qty,Decimal('-2.5'))
        services.confirm(target,self.actor);services.approve(target,self.actor)
        self.assertEqual(self.model('ProdStockBook').objects.filter(old_sheet_series=target.old_sheet_series).count(),1)
        services.reopen(target,self.actor,'继续办理')
        self.assertEqual(self.model('ProdStockBook').objects.filter(old_sheet_series=target.old_sheet_series).count(),1)

    def dispatch(self,source,records=(),purpose='customer_delivery'):
        values={key:value for key,value in self.movement.items() if key!='unit'}
        return dispatch_product(source,self.actor,**values,purpose=purpose,receiver='RCV',price=Decimal('3'),records=records)

    def test_factory_return_and_delivery_price_signed_and_reverse_are_separate(self):
        source=self.old('ProdIn',old_sheet_series='R',old_sheet_no='RECEIPT',old_customer_id='C',old_stock_unit=1,old_price=2,old_right_status=10,legacy_id='R')
        out=self.dispatch(source,purpose='factory_return')
        self.assertEqual(out.old_fact_id,'RCV');self.assertEqual(out.old_customer_id,'C')
        self.assertNotEqual(out.old_right_status,10)
        detail=self.model('ProdOutDetail').objects.get(source_parent_1=out)
        self.assertEqual(detail.old_in_sheet_no,'RECEIPT');self.assertEqual(detail.old_price,3)
        self.assertEqual(detail.old_amount,Decimal('-7.50'));self.assertEqual(detail.old_total,Decimal('-7.50'))
        self.assertEqual(view_effects(out)['product_dispatch_origin']['original_price'],'2.00')
        count=self.model('ProdStockBook').objects.count()
        for result in ['delivered','refused','withdrawn']:
            confirm_delivery(out,self.actor,result,'现场接收',self.at,'交付记录')
        self.assertEqual(self.model('ProdStockBook').objects.count(),count)
        returned=receive_delivery_return(detail,self.actor,customer='C',**self.movement)
        self.assertEqual(returned.old_prod_out_sheet_series,out.old_sheet_series)
        self.assertEqual(returned.old_customer_id,'C')
        self.assertEqual(view_effects(returned)['product_dispatch_origin']['purpose'],'delivery_return')

    def test_delivery_fine_records_selected_by_id_not_barcode_and_reject_foreign_owner(self):
        source=self.old('ProdIn',old_sheet_series='R',old_sheet_no='R',legacy_id='R')
        records=[self.old('ProdInRecord',old_sheet_series='r ',old_roll_no=str(i),old_bar_code='SAME',old_in_rolls=-1,legacy_id=str(i)) for i in range(2)]
        out=self.dispatch(source,records=records)
        detail=self.model('ProdOutDetail').objects.get(source_parent_1=out)
        self.assertEqual(self.model('ProdOutRecord').objects.filter(source_parent_1=detail).count(),2)
        alien=self.old('ProdInRecord',old_sheet_series='OTHER',old_roll_no='1',old_bar_code='SAME')
        count=self.model('ProdOut').objects.count()
        with self.assertRaises(ValidationError):self.dispatch(source,records=[alien])
        self.assertEqual(self.model('ProdOut').objects.count(),count)

    def test_split_plan_transfers_quantity_and_only_adopts_route_theory(self):
        job=self.job(old_curr_process_id='DONE',old_sum_process_weight_qty=88,old_pkg=70,old_prod_id='YARN')
        route=self.old('JobProcess','erp_production',old_sheet_series='J',old_process_no=9,old_process_id='RARE',
            old_ppname01='特殊参数',old_theory_value01='55',old_actual_value01='60',old_status='1',old_start_time=self.at,old_wprocess_no='OLD')
        new=split_card(job,self.actor,Decimal('25'),Decimal('2'),1,self.at,'拆卡生产',[route])
        job.refresh_from_db();self.assertEqual(job.old_pre_vat_qty,75);self.assertEqual(job.old_pre_rolls,8)
        self.assertEqual(job.old_sum_process_weight_qty,88);self.assertTrue(job.old_is_splited)
        self.assertIsNone(new.old_sum_process_weight_qty);self.assertIsNone(new.old_pkg)
        self.assertEqual(new.old_prod_id,'YARN');self.assertEqual(new.old_ori_source_job_no,'JOB')
        planned=self.model('JobProcess','erp_production').objects.get(source_parent_1=new)
        self.assertEqual(planned.old_theory_value01,'55');self.assertIsNone(planned.old_actual_value01)
        self.assertIsNone(planned.old_start_time);self.assertIsNone(planned.old_wprocess_no)
        self.assertEqual(planned.old_status,'0');self.assertIsNone(planned.legacy_id)
        self.assertTrue(view_effects(new)['card_adoption']['quantity_deducted'])

    def test_split_cross_unit_null_and_negative_kept_with_explicit_difference(self):
        job=self.job()
        new=split_card(job,self.actor,Decimal('-4'),None,2,self.at,'明确异单位',[])
        job.refresh_from_db();self.assertEqual(job.old_pre_vat_qty,100)
        self.assertEqual(new.old_pre_vat_qty,-4);self.assertIsNone(new.old_pre_rolls)
        self.assertFalse(view_effects(new)['card_adoption']['quantity_deducted'])
        unknown=split_card(job,self.actor,None,None,1,self.at,'原数量未知',[])
        job.refresh_from_db();self.assertIsNone(job.old_pre_vat_qty)
        self.assertIsNone(unknown.old_pre_vat_qty)

    def test_merge_keeps_duplicate_job_numbers_and_all_original_actuals(self):
        first=self.job(old_sum_process_weight_qty=20)
        second=self.old('JobSheet','erp_production',old_sheet_series='OTHER',old_sheet_no='JOB',old_pre_vat_qty=-2,old_pre_rolls=None,legacy_id='B')
        before=[snapshot(first),snapshot(second)]
        target=merge_cards(first,self.actor,[second,second],Decimal('30'),None,1,self.at,'合卡',[])
        data=combine_members(target)['rows']
        self.assertEqual(len(data),2);self.assertEqual([row['JobSheetNo'] for row in data],['JOB','JOB'])
        self.assertEqual([row['Qty'] for row in data],[100,-2])
        first.refresh_from_db();second.refresh_from_db();self.assertEqual([snapshot(first),snapshot(second)],before)
        self.assertEqual(self.model('JobCombineOrder','erp_production').objects.count(),0)

    def test_order_allocation_partial_transfer_preserves_total_and_unknown(self):
        job=self.job()
        source=self.old('JobCombineOrder','erp_production',old_sheet_series='OTHER',old_check_no='C',old_order_qty=100,old_combine_qty=Decimal('20'),legacy_id='allocation')
        target=transfer_allocation(source,self.actor,job,Decimal('5.25'),self.at,'部分转移')
        source.refresh_from_db();self.assertEqual(source.old_combine_qty+target.old_combine_qty,20)
        self.assertEqual(target.old_order_qty,100);self.assertIsNone(target.legacy_id)
        self.assertEqual(view_effects(target)['order_transfer_origin']['source']['source']['legacy_id'],'allocation')
        unknown=transfer_allocation(source,self.actor,job,None,self.at,'原分配未知')
        source.refresh_from_db();self.assertIsNone(source.old_combine_qty);self.assertIsNone(unknown.old_combine_qty)

    def test_packaging_starts_gx98_and_preserves_exceptional_facts(self):
        job=self.job()
        process=self.old('JobProcess','erp_production',old_sheet_series='J',old_process_no=7,old_process_id='GX98',old_status='0')
        self.old('HEmployee','erp_base',old_emp_id='E',old_name='人员')
        package=self.write('RecordYield',_entry='QC_Record',old_job_sheet_no='JOB',old_emp_id='E',old_bar_code='DUP',
            old_roll_no='ABC',old_kg=151,old_net_kg=-3,old_customer_gray_name='原品名',old_dots=2,old_yard=3)
        self.assertEqual(package.old_net_kg,-3);self.assertEqual(package.old_kg,151)
        self.assertEqual(package.old_customer_gray_name,'原品名');self.assertEqual(package.old_job_detail_no,'JOB')
        process.refresh_from_db();self.assertEqual(process.old_status,'1');self.assertEqual(process.old_wpworker,'人员')
        job.refresh_from_db();self.assertEqual(job.old_curr_process_id,'GX98');self.assertEqual(job.old_pdots,2)
        self.assertEqual(job.old_pkg,151);self.assertEqual(job.old_prolls,1)
        self.write('RecordYield',_entry='QFQC_Record',old_job_sheet_no='JOB',old_bar_code='DUP',old_kg=-1,old_dots=-1,old_roll_no='009')
        job.refresh_from_db();self.assertEqual(job.old_pkg,150);self.assertEqual(job.old_prolls,2)

    def test_automatic_barcode_keeps_given_duplicates_and_imported_rows_unchanged(self):
        original=self.old('RecordYield',old_guid='OLD',old_bar_code=None,old_roll_no='123',old_net_kg=-7,legacy_id='old')
        before=snapshot(original)
        a=self.write('RecordYield',_entry='RecordYield',old_roll_no='001',old_bar_code=None)
        b=self.write('RecordYield',_entry='RecordYield',old_roll_no='001',old_bar_code=None)
        self.assertNotEqual(a.old_bar_code,b.old_bar_code);self.assertEqual(a.old_scroll,'1')
        self.assertEqual(len(a.old_bar_code),11)
        services.write(type(original),{'old_remarks':'仅备注'},original,self.actor)
        original.refresh_from_db()
        for key in ['old_bar_code','old_roll_no','old_net_kg']:self.assertEqual(snapshot(original)[key],before[key])

    def test_weigh_delete_guard_is_entry_specific(self):
        weigh=self.write('RecordYield',_entry='WeighRecordYield',old_bar_code='SAME')
        other=self.write('RecordYield',_entry='RecordYield',old_bar_code='SAME')
        self.old('ProdInRecord',old_sheet_series='R',old_roll_no='1',old_bar_code='IN',old_prod_bar_code='SAME')
        with self.assertRaises(ValidationError):services.delete(type(weigh).objects.filter(pk=weigh.pk),self.actor)
        services.delete(type(other).objects.filter(pk=other.pk),self.actor)
        self.assertTrue(type(weigh).objects.filter(pk=weigh.pk).exists())

    def test_api_optional_nulls_quality_and_generated_action_metadata(self):
        receipt=self.old('ProdIn',old_sheet_series='R',legacy_id='R')
        root=f'/api/system/erp_warehouse_sourcedyeprodin/{receipt.pk}/'
        response=self.client.post(root+'factory_quality/',{'result':'hold','at':self.at.isoformat(),'reason':'原无质检'},format='json')
        self.assertEqual(response.status_code,200,response.data)

        response=self.client.post(root+'continuation/',{},format='json')
        self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(response.data['data']['rows'][0]['result'],'hold')
        self.assertNotIn('source',str(response.data['data']['rows']))
        response=self.client.post(root+'dispatch_product/',{'at':self.at.isoformat(),'reason':'原空数量',
            'sheet_kind':22,'purpose':'customer_delivery','records':[]},format='json')
        self.assertEqual(response.status_code,200,response.data)
        package=self.old('RecordYield',old_guid='P',old_bar_code='P',legacy_id='P')
        response=self.client.post(f'/api/system/erp_warehouse_sourcedyerecordyield/{package.pk}/receive_package/',
            {'at':self.at.isoformat(),'reason':'原空数量','sheet_kind':10},format='json')
        self.assertEqual(response.status_code,200,response.data)

    def test_combined_process_uses_source_status_exact_next_and_time_way(self):
        job=self.job(old_curr_process_id='BEFORE')
        source=self.old('JobProcess','erp_production',old_sheet_series='OTHER',old_process_no=1,old_process_id='GX07',old_status='5',legacy_id='S')
        target=self.old('JobProcess','erp_production',old_sheet_series='J',old_process_no=3,old_process_id='RARE',old_start_time=self.at,legacy_id='T')
        sync_combined_process(source,self.actor,[target],None,2,self.at,'原结束分支')
        target.refresh_from_db();job.refresh_from_db()
        self.assertEqual(target.old_status,'5');self.assertEqual(target.old_end_time,self.at)
        self.assertEqual(target.old_start_time,self.at);self.assertEqual(job.old_curr_process_id,'BEFORE')
        self.old('JobProcess','erp_production',old_sheet_series='J',old_process_no=4,old_process_id='NEXT')
        sync_combined_process(source,self.actor,[target],'M',0,self.at,'原双时间分支')
        job.refresh_from_db();target.refresh_from_db()
        self.assertEqual(job.old_curr_process_id,'RARE');self.assertEqual(job.old_next_process_id,'NEXT')
        self.assertEqual(target.old_machine_id,'M');self.assertEqual(target.legacy_id,'T')

    def test_barcode_five_digit_overflow_keeps_old_row_and_extends_new_number(self):
        prefix=timezone.localtime().strftime('%y%m%d')
        old=self.old('RecordYield',old_guid='MAX',old_bar_code=prefix+'99999',legacy_id='max')
        result=self.write('RecordYield',old_bar_code=None)
        self.assertEqual(result.old_bar_code,prefix+'100000')
        old.refresh_from_db();self.assertEqual(old.old_bar_code,prefix+'99999')

    def test_api_split_and_transfer_actions(self):
        job=self.job()
        response=self.client.post(f'/api/system/erp_production_sourcedyejobsheet/{job.pk}/split_card/',
            {'at':self.at.isoformat(),'reason':'API拆卡','quantity':'10','rolls':'1','unit':1,'processes':[]},format='json')
        self.assertEqual(response.status_code,200,response.data)
        source=self.old('JobCombineOrder','erp_production',old_sheet_series='J',old_check_no='C',old_combine_qty=10)
        response=self.client.post(f'/api/system/erp_production_sourcedyejobcombineorder/{source.pk}/transfer_allocation/',
            {'at':self.at.isoformat(),'reason':'API分配','target':job.pk,'quantity':'2'},format='json')
        self.assertEqual(response.status_code,200,response.data)

    def test_related_selection_requires_source_read_permission(self):
        from types import SimpleNamespace
        from rest_framework import serializers
        from rest_framework.exceptions import ValidationError as ApiValidationError
        from plugins.erp_base.business_api import parameters
        user=Users.objects.create_user(username='restricted-delivery',password='test')
        record=self.old('ProdInRecord',old_sheet_series='R',old_bar_code='B',old_roll_no='1')
        view=SimpleNamespace(request=SimpleNamespace(user=user,data={'records':[record.pk]}))
        with self.assertRaises(ApiValidationError):
            parameters(view,{'records':serializers.PrimaryKeyRelatedField(queryset=type(record).objects.all(),many=True)})

    def test_continuation_without_original_entry_stays_editable_then_binds(self):
        item=self.old('ProdIn',old_sheet_series='R',old_sheet_no='R')
        factory_quality(item,self.actor,None,'hold',None,self.at,'待处理')
        self.assertIsNone(item.entry_name)
        services.write(type(item),{'old_remarks':'补充'},item,self.actor)
        services.write(type(item),{'_entry':'ProdIn'},item,self.actor)
        self.assertEqual(item.entry_name,'ProdIn')
        self.assertEqual(view_effects(item)['factory_quality']['result'],'hold')

    def test_packaging_gray_adoption_keeps_duplicate_rows_and_precise_source(self):
        source=self.old('JobGrayRecord','erp_production',old_sheet_series='ORPHAN',old_gray_bar_code='G',old_weight_qty=-8,legacy_id='G')
        selected=self.old('RecordYield',old_guid='A',old_bar_code='SAME',old_gray_weight=99,legacy_id='A')
        other=self.old('RecordYield',old_guid='B',old_bar_code='SAME',old_gray_weight=77,legacy_id='B')
        response=self.client.post(f'/api/system/erp_warehouse_sourcedyerecordyield/{selected.pk}/adopt_gray_record/',
            {'source':source.pk,'at':self.at.isoformat(),'reason':'明确对应原行'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        selected.refresh_from_db();other.refresh_from_db()
        self.assertEqual(selected.old_gray_weight,-8);self.assertEqual(selected.old_gray_bar_code,'G')
        self.assertEqual(other.old_gray_weight,77);self.assertEqual(selected.legacy_id,'A')
        self.assertEqual(Decimal(view_effects(selected)['package_gray_origin']['package_before']['source']['old_gray_weight']),99)

    def test_split_and_allocation_round_once_before_subtracting(self):
        job=self.job()
        new=split_card(job,self.actor,Decimal('0.005'),Decimal('0.005'),1,self.at,'原字段精度',[])
        job.refresh_from_db()
        self.assertEqual(job.old_pre_vat_qty+new.old_pre_vat_qty,100)
        self.assertEqual(job.old_pre_rolls+new.old_pre_rolls,10)
        source=self.old('JobCombineOrder','erp_production',old_sheet_series='OTHER',old_check_no='C',old_combine_qty=20)
        result=transfer_allocation(source,self.actor,job,Decimal('5.255'),self.at,'原字段精度')
        source.refresh_from_db();self.assertEqual(source.old_combine_qty+result.old_combine_qty,20)

    def test_package_receipt_keeps_different_original_header_and_record_precision(self):
        source=self.old('RecordYield',old_guid='A',old_bar_code='A',legacy_id='A')
        values={**self.movement,'weight':Decimal('1.235'),'rolls':Decimal('2.345')}
        result=receive_package(source,self.actor,**values)
        detail=self.model('ProdInRecord').objects.get(source_parent_1=result)
        self.assertEqual(result.old_weight_qty,Decimal('1.24'))
        self.assertEqual(detail.old_weight_qty,Decimal('1.2'))
        self.assertEqual(view_effects(result)['package_receipt_origin']['requested_amounts']['weight'],'1.235')

    def test_orphan_combine_group_can_be_read_and_adopted_without_deleting_sources(self):
        first=self.old('JobCombine','erp_production',old_sheet_series='MISSING',old_job_sheet_no='DUP',old_qty=-2,legacy_id='A')
        second=self.old('JobCombine','erp_production',old_sheet_series='MISSING',old_job_sheet_no='DUP',old_qty=None,legacy_id='B')
        root=f'/api/system/erp_production_sourcedyejobcombine/{first.pk}/'
        result=self.client.post(root+'combine_group/',{},format='json')
        self.assertEqual(result.status_code,200,result.data)
        self.assertEqual([row['id'] for row in result.data['data']['rows']],[first.pk,second.pk])
        target=self.job()
        result=self.client.post(root+'adopt_combine_link/',{'target':target.pk,'at':self.at.isoformat(),'reason':'原表头缺失明确采用'},format='json')
        self.assertEqual(result.status_code,200,result.data)
        link=type(first).objects.get(pk=result.data['data']['id'])
        self.assertEqual(link.source_parent_1,target);self.assertEqual(link.old_qty,-2)
        self.assertEqual(link.old_job_sheet_no,'DUP');self.assertIsNone(link.legacy_id)
        first.refresh_from_db();second.refresh_from_db()
        self.assertEqual(first.old_sheet_series,'MISSING');self.assertEqual(second.old_sheet_series,'MISSING')
        self.assertEqual(view_effects(link)['combine_link_origin']['source']['source']['legacy_id'],'A')
