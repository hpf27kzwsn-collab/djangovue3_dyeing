from plugins.erp_base.tests.source_fixtures import historical_batch
from datetime import datetime
from decimal import Decimal
from django.apps import apps
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base import source_services as services
from plugins.erp_base.source_purchase_flow import receive, receipt_progress
from plugins.erp_base.source_outwork_flow import apply, remaining, dispatch, receive_product
from plugins.erp_base.source_quality_flow import defective_balance
from plugins.erp_base.source_context import SourceDocumentContext


class PurchaseQualityChainTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='pq-flow', password='test')
        self.at = timezone.make_aware(datetime(2026, 10, 15, 9))

    def model(self, name, module):
        return apps.get_model(module + '.SourceDye' + name)

    def old(self, name, module, **data):
        return self.model(name, module).objects.create(**data)

    def write(self, name, module, **data):
        return services.write(self.model(name, module), data, actor=self.actor)

    def test_purchase_link_fields_are_distinct_and_nulls_negative_receipts_kept(self):
        head = self.write('PurMain', 'erp_purchase', _entry='PurMain', old_sheet_series='P')
        line = self.write('PurDetail', 'erp_purchase', source_parent_2=head, old_detail_no='PD', old_qty=10)
        for index, (table, kind, weight) in enumerate([('GrayIn',18,Decimal('-2.5')),('SemiIn',20,None),('GrayIn',16,99)]):
            self.old(table, 'erp_warehouse', old_sheet_series=str(index), old_sheet_kind=kind)
            self.old(table+'Detail', 'erp_warehouse', old_sheet_series=str(index), old_rece_sheet_no=str(index),
                     old_pur_detail_no='PD', old_weight_qty=weight, source_batch=historical_batch())
        result = receipt_progress(line)
        self.assertEqual(result['received_weight_18_20'], Decimal('-2.5'))
        self.assertEqual(len(result['source_rows']), 2)
        self.assertFalse(result['old_gray_selection_available'])
        services.write(type(head), {'old_remarks':'可改：只有PurDetailNo'}, head, self.actor)
        self.old('GrayInDetail','erp_warehouse',old_sheet_series='ORPHAN',old_rece_sheet_no='R',old_purchase_orders='PD')
        with self.assertRaises(ValidationError):
            services.write(type(head), {'old_remarks':'不允许'}, head, self.actor)
        with self.assertRaises(ValidationError):
            services.delete_documents(type(head).objects.filter(pk=head.pk), self.actor)
        head.refresh_from_db();self.assertEqual(head.old_remarks,'可改：只有PurDetailNo')

    def test_apply_reference_checks_all_lines_and_reopen_is_atomic(self):
        for prefix, incoming in [('Article','ArticleInDetail'),('Stuff','StuffInDetail')]:
            head=self.write('PurApplyMain','erp_purchase',_entry=prefix+'PurApplyMain',old_sheet_series=prefix)
            for suffix in ['A','Z']:
                self.write('PurApplyDetail','erp_purchase',source_parent_1=head,old_detail_no=prefix+suffix)
            services.confirm(head,self.actor);services.approve(head,self.actor)
            self.old(incoming,'erp_warehouse',old_detail_no=prefix,old_pur_detail_no=prefix+'A')
            with self.assertRaises(ValidationError):services.reopen(head,self.actor,'回退')
            head.refresh_from_db();self.assertEqual(head.approval_stage,'approved')

    def test_receipt_adopts_explicit_partial_negative_null_and_keeps_history(self):
        head=self.old('PurMain','erp_purchase',old_sheet_series='P',old_supplier_id='S',old_right_status=10,source_batch=historical_batch())
        line=self.old('PurDetail','erp_purchase',old_sheet_series='P',old_detail_no='PD',old_fabric_id='F',
            old_qty=100,old_price=Decimal('2.50'),source_batch=historical_batch())
        targets=[]
        for entry,quantity in [('PurGrayIn',Decimal('-2.25')),('PurSemiIn',None)]:
            target=receive(line,self.actor,entry,self.at,quantity,Decimal('1.25'),'W','1')
            targets.append(target)
            self.assertEqual(target.approval_stage,'draft');self.assertIsNone(target.source_batch_id)
            detail=self.model(target.SOURCE_TABLE+'Detail','erp_warehouse').objects.get(source_parent_1=target)
            self.assertEqual(detail.old_weight_qty,quantity);self.assertEqual(detail.old_rolls,Decimal('1.25'))
            self.assertEqual(detail.old_purchase_orders,'PD');self.assertEqual(detail.old_pur_detail_no,'PD')
            self.assertEqual(detail.old_amount,None if quantity is None else Decimal('-5.63'))
            context=SourceDocumentContext.objects.get(entity=target._meta.label,object_id=target.pk)
            self.assertEqual(context.effects['purchase_origin']['source']['source_batch'],historical_batch().pk)
            self.assertEqual(context.effects['purchase_origin']['source']['id'],line.pk)
        line.refresh_from_db();self.assertEqual(line.old_qty,100);self.assertEqual(line.source_batch_id,historical_batch().pk)
        self.assertEqual(receipt_progress(line)['received_weight_18_20'],Decimal('-2.25'))
        services.delete_documents(type(targets[0]).objects.filter(pk=targets[0].pk),self.actor)
        self.assertIsNone(receipt_progress(line)['received_weight_18_20'])

    def test_receipt_api_optional_nulls_and_missing_parent_still_preserve_line(self):
        line=self.old('PurDetail','erp_purchase',old_sheet_series='ORPHAN',old_detail_no='P',old_price=None,source_batch=historical_batch())
        client=APIClient();client.force_authenticate(self.actor)
        response=client.post(f'/api/system/erp_purchase_sourcedyepurdetail/{line.pk}/receive/',
            {'entry':'PurGrayIn','received_at':self.at.isoformat()},format='json')
        self.assertEqual(response.status_code,200,response.data)
        self.assertIn('已生成单据',response.data['msg'])
        self.assertTrue(type(line).objects.filter(pk=line.pk,source_batch=historical_batch()).exists())

    def test_outwork_original_balance_exclusions_negative_and_orphan_applications(self):
        self.old('OrderMain','erp_sales',old_sheet_series='O',old_sheet_no='ORDER')
        color=self.old('OrderColor','erp_sales',old_sheet_series='O',old_check_no='C',old_order_qty=10,
                       old_out_qty=-2,old_card_qty=2,old_order_rolls=4,source_batch=historical_batch())
        for index, (kind,no,status,qty) in enumerate([(1,'NORMAL',0,9),(10,'EXCLUDED',0,99),(1,'JOBX1',0,99),(1,'NINE',9,99)]):
            self.old('JobSheet','erp_production',old_sheet_series=str(index),old_sheet_no=no,old_sheet_kind=kind,old_sheet_status=status)
            self.old('JobCombineOrder','erp_production',old_sheet_series=str(index),old_order_sheet_no='ORDER',old_check_no='C',old_combine_qty=qty)
        self.old('SemiOutWorkApply','erp_production',old_sheet_series='A')
        self.old('SemiOutWorkApplyDetail','erp_production',old_sheet_series='A',old_detail_no='A',old_check_no='C',old_qty=-3)
        self.old('SemiOutWorkApplyDetail','erp_production',old_sheet_series='MISSING',old_detail_no='B',old_check_no='C',old_qty=99)
        result=remaining(color)[0]
        self.assertEqual(result['last_qty'],2);self.assertEqual(len(result['allocations']),1)
        self.assertTrue(result['old_selection_available'])
        target=apply(color,self.actor,Decimal('5'),Decimal('-1.5'),'FACT','PROCESS',self.at)
        self.assertEqual(remaining(color)[0]['last_qty'],-3)
        detail=self.model('SemiOutWorkApplyDetail','erp_production').objects.get(source_parent_1=target)
        self.assertEqual(detail.old_check_no,'C');self.assertEqual(detail.old_order_sheet_no,'ORDER')
        self.assertEqual(detail.old_rolls,Decimal('-1.5'));self.assertIsNone(detail.source_batch_id)
        services.delete_documents(type(target).objects.filter(pk=target.pk),self.actor)
        self.assertEqual(remaining(color)[0]['last_qty'],2)

    def test_outwork_selection_hidden_does_not_discard_or_block_explicit_source(self):
        self.old('OrderMain','erp_sales',old_sheet_series='O',old_sheet_no='ORDER',old_is_finished=True)
        color=self.old('OrderColor','erp_sales',old_sheet_series='O',old_check_no='C',old_remarks02='旧备注')
        self.assertFalse(remaining(color)[0]['old_selection_available'])
        target=apply(color,self.actor,None,None,None,None,self.at)
        line=self.model('SemiOutWorkApplyDetail','erp_production').objects.get(source_parent_1=target)
        self.assertIsNone(line.old_qty)

    def test_coloring_curve_total_and_regenerated_staff_keep_original_history(self):
        old=self.old('ColorShiftEmp','erp_production',old_wprocess_no='W',old_emp_id='OLD',source_batch=historical_batch())
        self.old('PDyeCurveDetail','erp_base',old_curve_id='C',old_step_no=1,old_dye_process_id='A',old_default_value=Decimal('-2'))
        self.old('PDyeCurveDetail','erp_base',old_curve_id='C',old_step_no=2,old_dye_process_id='B',old_default_value=3)
        self.old('PShiftEmp','erp_base',old_shift_id='S',old_serial_number=1,old_emp_id='E')
        target=self.write('ColoringCheck','erp_quality',_entry='ColoringCheck',old_job_sheet_no='J',old_wprocess_no='W',old_shift_id='S',old_curve_id='C',old_dye_process_id='B')
        self.assertEqual(target.old_real_value,1)
        services.write(type(target),{'old_dye_process_id':'MISSING'},target,self.actor)
        target.refresh_from_db();self.assertIsNone(target.old_real_value)
        self.assertEqual(self.model('ColorShiftEmp','erp_production').objects.count(),2)
        services.delete(type(target).objects.filter(pk=target.pk),self.actor)
        self.assertEqual(self.model('ColorShiftEmp','erp_production').objects.count(),1)
        self.assertTrue(type(old).objects.filter(pk=old.pk,source_batch=historical_batch()).exists())

    def test_defective_insert_only_positive_rolls_and_delete_restores_process(self):
        job=self.old('JobSheet','erp_production',old_sheet_series='J',old_sheet_no='JOB',source_batch=historical_batch())
        self.old('JobProcess','erp_production',old_sheet_series='J',old_process_no=2,old_process_id='DONE',old_status='1',old_end_time=self.at)
        self.old('JobProcess','erp_production',old_sheet_series='J',old_process_no=7,old_process_id='NEXT',old_status='0')
        head=self.write('DefectiveIn','erp_quality',old_sheet_series='D')
        line=self.write('DefectiveInDetail','erp_quality',source_parent_1=head,old_detail_no='D',old_job_sheet_no='JOB',old_rolls=1)
        job.refresh_from_db();self.assertEqual(job.old_sheet_status,9)
        services.write(type(line),{'old_rolls':-2},line,self.actor)
        job.refresh_from_db();self.assertEqual(job.old_sheet_status,9)
        services.delete(type(line).objects.filter(pk=line.pk),self.actor)
        job.refresh_from_db();self.assertEqual(job.old_sheet_status,0);self.assertEqual(job.old_curr_process_id,'DONE')
        self.assertEqual(job.old_next_process_id,'NEXT');self.assertEqual(job.source_batch_id,historical_batch().pk)

    def test_defective_balance_includes_negative_null_and_orphan_outgoing(self):
        line=self.old('DefectiveInDetail','erp_quality',old_sheet_series='MISSING',old_detail_no='D',old_rolls=1,old_weight_qty=None,old_length_qty=5)
        self.old('DefectiveOutDetail','erp_quality',old_detail_no='OUT',old_defective_in_detail_no='D',old_rolls=3,old_weight_qty=None,old_length_qty=-2)
        balance=defective_balance(line)
        self.assertEqual(balance['Rolls'],-2);self.assertIsNone(balance['WeightQty']);self.assertEqual(balance['LengthQty'],7)
        self.assertFalse(balance['old_stock_visible'])

    def test_wprocess_machine_from_latest_start_and_original_zero_rule(self):
        self.old('WProcess','erp_production',old_wprocess_no='START',old_job_sheet_no='J',old_station_id='06',old_dye_state='1',old_process_no=1,old_machine_id='M',old_start_time=self.at,source_batch=historical_batch())
        line=self.write('WProcess','erp_production',old_wprocess_no='END',old_job_sheet_no='J',old_station_id='06',old_dye_state='2',old_process_no=1)
        self.assertEqual(line.old_machine_id,'M');self.assertIsNotNone(line.old_end_time)
        self.old('PProcess','erp_base',old_process_id='P',old_is_can_add_work_qty=True,old_input_qty_check_way=0)
        counted=self.write('WProcess','erp_production',old_wprocess_no='COUNT',old_job_sheet_no='J',old_station_id='02',old_process_id='P',old_curr_kg=-5,old_work_qty=20)
        self.assertEqual(counted.old_curr_kg,0);self.assertEqual(counted.old_work_qty,0)
        history=self.old('WProcess','erp_production',old_wprocess_no='HISTORY',old_station_id='02',old_process_id='P',old_curr_kg=-5,source_batch=historical_batch())
        services.write(type(history),{'old_memo':'备注'},history,self.actor)
        history.refresh_from_db();self.assertEqual(history.old_curr_kg,-5);self.assertIsNone(history.old_end_time)

    def test_both_outwork_families_dispatch_and_partial_return_preserve_actual_quantities(self):
        color=self.old('OrderColor','erp_sales',old_sheet_series='ORPHAN',old_check_no='C',old_order_qty=50,old_price=2,source_batch=historical_batch())
        for entry in ['OutWorkApply','SemiOutWorkApply']:
            application=apply(color,self.actor,Decimal('20'),Decimal('2'),'FACT','P',self.at,entry)
            line=self.model(entry+'Detail','erp_production').objects.get(source_parent_1=application)
            output=dispatch(line,self.actor,Decimal('8'),Decimal('1'),'W','1',21,self.at,None)
            outgoing=self.model(output.SOURCE_TABLE+'Detail','erp_warehouse').objects.get(source_parent_1=output)
            self.assertEqual(outgoing.old_weight_qty,8);self.assertIsNone(outgoing.source_batch_id)
            services.confirm(output,self.actor);services.approve(output,self.actor)
            output_context=SourceDocumentContext.objects.get(entity=output._meta.label,object_id=output.pk)
            self.assertTrue(output_context.effects['stock_rows'])
            returns=[]
            for qty in [Decimal('3'),Decimal('-0.5'),None]:
                received=receive_product(outgoing,self.actor,qty,None,'FINISHED','1',18,self.at,None)
                returns.append(received)
                self.assertEqual(received.old_weight_qty,qty);self.assertIsNone(received.old_rolls)
                context=SourceDocumentContext.objects.get(entity=received._meta.label,object_id=received.pk)
                self.assertEqual(context.effects['outwork_receipt_origin']['source']['id'],outgoing.pk)
            services.confirm(returns[1],self.actor);services.approve(returns[1],self.actor)
            book=self.model('ProdStockBook','erp_warehouse').objects.get(old_sheet_series=returns[1].old_sheet_series)
            self.assertEqual(book.old_in_weight_qty,Decimal('-0.5'))
            services.reopen(returns[1],self.actor,'本次回货撤审')
            self.assertFalse(type(book).objects.filter(pk=book.pk).exists())
            self.assertEqual(type(book).objects.get(old_sheet_series=returns[1].old_sheet_series).old_in_weight_qty,Decimal('-0.5'))
            line.refresh_from_db();outgoing.refresh_from_db()
            self.assertEqual(line.old_qty,20);self.assertEqual(outgoing.old_weight_qty,8)
            services.delete_documents(type(returns[0]).objects.filter(pk=returns[0].pk),self.actor)
            self.assertEqual(type(returns[1]).objects.filter(pk__in=[r.pk for r in returns[1:]]).count(),2)
            services.reopen(output,self.actor,'发出撤审')
            output_context.refresh_from_db();self.assertTrue(output_context.effects['stock_rows'])
            generated=output_context.effects['stock_rows']
            services.delete_documents(type(output).objects.filter(pk=output.pk),self.actor)
            for label,ids in generated.items():self.assertFalse(apps.get_model(label).objects.filter(pk__in=ids).exists())

    def test_failed_outwork_dispatch_rolls_back_whole_document(self):
        line=self.old('OutWorkApplyDetail','erp_production',old_sheet_series='MISSING',old_detail_no='D',old_qty=-1,source_batch=historical_batch())
        before=self.model('GrayOut','erp_warehouse').objects.count()
        with self.assertRaises(ValidationError):
            dispatch(line,self.actor,Decimal('8'),None,'X'*1000,'1',21,self.at,None)
        self.assertEqual(self.model('GrayOut','erp_warehouse').objects.count(),before)
        self.assertTrue(type(line).objects.filter(pk=line.pk,source_batch=historical_batch()).exists())

    def test_return_and_internal_reviews_with_repair_cards_cannot_be_deleted(self):
        for entry in ['WDefectJudgeBack','WDefectJudgeInterior']:
            item=self.write('WDefect','erp_quality',_entry=entry,old_sheet_series=entry,old_sheet_no=entry)
            self.old('JobSheet','erp_production',old_sheet_series=entry,old_loss_str=entry)
            with self.assertRaises(ValidationError):services.delete_documents(type(item).objects.filter(pk=item.pk),self.actor)
            self.assertTrue(type(item).objects.filter(pk=item.pk).exists())
