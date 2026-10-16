from plugins.erp_base.tests.source_fixtures import historical_batch
from datetime import datetime, timedelta
from decimal import Decimal
from django.apps import apps
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.business import snapshot
from plugins.erp_base.source_package_operations import reader, effect
from plugins.erp_base.source_package_labels import preview, synchronize, undo, label_code, varchar
from plugins.erp_base.source_package_people import latest_packers, shared_yield
from plugins.erp_base.source_work_archive import archive, undo as undo_archive, preview as archive_preview, cutoff
from plugins.erp_base.source_execution_state import active


class PackageLabelTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='label-tests', password='test')
        self.at = timezone.make_aware(datetime(2026, 10, 15, 12))
        self.event = {'at': self.at, 'reason': '自动标签与工位变体核对'}
        self.client = APIClient(); self.client.force_authenticate(self.actor)
        self.job = self.old('JobSheet', old_sheet_series='S', old_sheet_no='J', old_cust_self_product='P', old_cust_color_num='12345')
        self.old('PProduct', 'erp_base', old_prod_id='P', old_name_c='AB#纱线')

    def old(self, name, module='erp_production', **values):
        item = apps.get_model(module + '.SourceDye' + name).objects.create(**values)
        item.refresh_from_db(); return item

    def package(self, **values):
        return self.old('RecordYield', 'erp_warehouse', **dict({'old_guid': str(reader('RecordYield','erp_warehouse').count()),
            'old_roll_no': '1', 'old_bar_code': 'B', 'old_job_sheet_no': 'BEFORE', 'old_gray_bar_code': 'G',
            'old_customer_id': '', 'old_cust_qty': Decimal('12.3'), 'old_net_kg': Decimal('9.5'),
            'old_cust_color_num': '9876', 'old_db2_code': 'OLD', 'source_batch': historical_batch()}, **values))

    def gray(self, **values):
        return self.old('JobGrayRecord', **dict({'old_sheet_series': 'S', 'old_gray_bar_code': 'G'}, **values))

    def sync(self):
        return synchronize(self.job, self.actor, **self.event)

    def test_preview_no_mutation_and_full_cross_card_duplicate_target_undo(self):
        first = self.package(); other = self.package(old_gray_bar_code='OTHER',old_job_sheet_no='OTHER',old_customer_id='CUSTOMER')
        self.gray(); before = [snapshot(item) for item in [first, other]]
        report = preview(self.job)
        self.assertEqual(len(report['rows']),2)
        self.assertTrue(report['rows'][1]['outside_gray_scope'])
        first.refresh_from_db(); self.assertEqual(snapshot(first),before[0])
        self.sync()
        first.refresh_from_db(); other.refresh_from_db()
        self.assertEqual(first.old_db2_code,'AB00001234123J001')
        self.assertEqual(other.old_db2_code,'AB00009876123OTHER001')
        self.assertEqual(first.old_customer_gray_name,'AB#纱线'); self.assertEqual(first.source_batch_id,historical_batch().pk)
        self.assertEqual(other.old_job_sheet_no,'OTHER')
        undo(self.job,self.actor,**self.event)
        for item, previous in zip([first,other],before):
            item.refresh_from_db()
            for field in item.SOURCE_FIELDS.values():self.assertEqual(snapshot(item)[field],previous[field])

    def test_duplicate_gray_and_candidates_retained_with_last_documented_choice(self):
        item = self.package(); self.gray(); self.gray()
        last = self.old('JobSheet', old_sheet_series='s ',old_sheet_no='J2',old_cust_self_product='P2')
        self.old('PProduct','erp_base',old_prod_id='P2',old_name_c='ZZ#二')
        result = self.sync(); item.refresh_from_db()
        self.assertEqual(len(result['result_rows']),2);self.assertEqual(len(result['candidate_rows']),2)
        self.assertEqual(item.old_job_sheet_no,'J2');self.assertEqual(item.old_customer_gray_name,'ZZ#二')
        self.assertIsNone(item.old_db2_code)

    def test_null_gray_does_not_match_blank_gray_does(self):
        null = self.package(old_gray_bar_code=None); blank = self.package(old_gray_bar_code='',old_bar_code=None)
        self.gray(old_gray_bar_code=' ')
        result = self.sync();null.refresh_from_db();blank.refresh_from_db()
        self.assertEqual([row['record_id'] for row in result['rows']],[blank.pk])
        self.assertEqual(null.old_job_sheet_no,'BEFORE');self.assertEqual(blank.old_job_sheet_no,'J')
        self.assertEqual(blank.old_db2_code,'OLD')

    def test_null_customer_not_empty_and_empty_barcode_global(self):
        item = self.package(old_customer_id=None,old_bar_code=''); self.gray()
        self.sync();item.refresh_from_db();self.assertEqual(item.old_db2_code,'OLD')
        undo(self.job,self.actor,**self.event)
        item.old_customer_id='   ';item.save()
        outside=self.package(old_bar_code=' ',old_gray_bar_code='outside')
        self.sync();outside.refresh_from_db();self.assertNotEqual(outside.old_db2_code,'OLD')

    def test_missing_product_sets_null_name_but_uses_default_code(self):
        reader('PProduct','erp_base').delete();item=self.package();self.gray();self.sync();item.refresh_from_db()
        self.assertIsNone(item.old_customer_gray_name);self.assertTrue(item.old_db2_code.startswith('000000'))

    def test_original_quantity_scale_truncation_negative_and_null(self):
        values={'CustColorNum':' A12Z','JobSheetNo':'J','RollNo':'12345','ShipMentType':None,'CustQty':Decimal('123.4'),'NetKg':Decimal('-1.2')}
        self.assertEqual(label_code(values,'LONGCODE'),'LONGCO0A12234J345')
        values['ShipMentType']='2';self.assertEqual(label_code(values,'P')[-7:],'-12J345')
        values['NetKg']=None;self.assertIsNone(label_code(values,'P'))
        self.assertEqual(varchar('纱'*101,200),'纱'*100)

    def test_only_original_first_update_fields_not_customer_or_quantity(self):
        item=self.package(old_customer_id='C',old_prod_id='KEEP',old_qty=-5);self.gray();self.sync();item.refresh_from_db()
        self.assertEqual((item.old_customer_id,item.old_prod_id,item.old_qty,item.old_db2_code),('C','KEEP',-5,'OLD'))

    def test_scope_cannot_partially_update_global_barcode(self):
        item=self.package();other=self.package(old_gray_bar_code='outside');self.gray()
        def query(name,module):return reader(name,module).exclude(pk=other.pk) if name=='RecordYield' else reader(name,module)
        with self.assertRaises(ValidationError):synchronize(self.job,self.actor,query=query,**self.event)
        item.refresh_from_db();self.assertEqual(item.old_job_sheet_no,'BEFORE')

    def test_repeat_requires_actual_reverse_and_later_edit_is_not_overwritten(self):
        item=self.package();self.gray();self.sync()
        with self.assertRaises(ValidationError):self.sync()
        item.refresh_from_db();item.old_db2_code='LATER';item.save()
        with self.assertRaises(ValidationError):undo(self.job,self.actor,**self.event)
        item.refresh_from_db();self.assertEqual(item.old_db2_code,'LATER')

    def test_latest_people_global_max_ties_duplicate_employees_and_null(self):
        self.package(old_detail_no='D',old_pack_time=self.at,old_job_sheet_no='J',old_emp_id='E')
        self.package(old_detail_no='d ',old_pack_time=self.at,old_job_sheet_no='OTHER',old_emp_id='E')
        self.package(old_detail_no=None,old_pack_time=self.at)
        self.package(old_detail_no='OLD',old_pack_time=None)
        for _ in range(2):self.old('HEmployee','erp_base',old_emp_id='E',old_name='工人')
        self.assertEqual(len(latest_packers()['rows']),4)
        self.assertEqual(len(latest_packers(number='J')['rows']),2)
        self.package(old_detail_no='D',old_pack_time=self.at+timedelta(seconds=1),old_job_sheet_no='LATER')
        self.assertEqual(latest_packers(number='J')['rows'],[])

    def test_shared_duplicate_staff_negative_null_and_zero_match_preserved(self):
        self.package(old_job_sheet_no='J',old_cust_qty=Decimal('1.0'),old_shift_id='S')
        for employee in ['E','E','F']:self.old('RecordEmp',old_bar_code='B',old_emp_id=employee)
        self.package(old_job_sheet_no='J',old_cust_qty=None,old_shift_id='S')
        report=shared_yield();groups={row['EmpID']:row for row in report['rows']}
        self.assertEqual(groups['E']['Qty'],Decimal('0.666666666666'))
        self.assertEqual(len(groups['E']['sources']),4)
        reader('RecordYield','erp_warehouse').update(old_cust_qty=-1)
        self.assertEqual(shared_yield()['rows'][0]['Qty'],Decimal('-1.333333333332'))

    def test_original_view_and_guid_entry_are_distinct_explicit_modes(self):
        item=self.package(old_guid='GUID',old_bar_code='LABEL')
        staff=self.old('RecordEmp',old_bar_code='GUID',old_emp_id='E')
        report=shared_yield();self.assertEqual(report['rows'],[])
        self.assertEqual(report['supplemental_rows'][0]['source_ids'],[item.pk])
        self.assertEqual(report['supplemental_rows'][1]['source_ids'],[staff.pk])
        self.assertEqual(shared_yield(mode='entry_guid')['rows'][0]['Qty'],Decimal('12.3'))

    def test_archive_cutoff_existing_backup_expands_scope_and_preserves_process_no(self):
        old=self.old('WProcess',old_wprocess_no='W',old_end_time=cutoff(self.at)-timedelta(seconds=1),source_batch=historical_batch())
        recent=self.old('WProcess',old_wprocess_no='W',old_end_time=self.at)
        boundary=self.old('WProcess',old_wprocess_no='BOUNDARY',old_end_time=cutoff(self.at))
        blank=self.old('WProcess',old_wprocess_no='NULL',old_end_time=None)
        self.old('WProcessBak',old_wprocess_no='EXIST')
        expanded=self.old('WProcess',old_wprocess_no='EXIST',old_end_time=self.at)
        child=self.old('JobShiftEmp',old_job_sheet_no='J',old_shift_id='S',old_emp_id='E',old_process_no=7,old_wprocess_no='W',source_batch=historical_batch())
        self.old('WProcessStep',old_wpstep_no='STEP',old_wprocess_no='W')
        result=archive(old,self.actor,**self.event)
        self.assertEqual(result['rows'][0]['copy_count'],1);self.assertEqual(result['rows'][0]['retire_count'],3)
        copied=reader('JobShiftEmpBak','erp_production').get();self.assertEqual(copied.old_process_no,7);self.assertIsNone(copied.source_batch_id)
        from plugins.erp_base.source_provenance import is_historical
        self.assertTrue(is_historical(copied))
        self.assertEqual(set(active(reader('WProcess','erp_production')).values_list('pk',flat=True)),{boundary.pk,blank.pk})
        self.assertEqual(reader('WProcess','erp_production').count(),5)
        undo_archive(old,self.actor,**self.event)
        self.assertEqual(active(reader('WProcess','erp_production')).count(),5)
        self.assertEqual(active(reader('JobShiftEmp','erp_production')).get().pk,child.pk)
        self.assertEqual(active(reader('WProcessBak','erp_production')).get().old_wprocess_no,'EXIST')

    def test_archive_empty_and_year_rollover(self):
        self.assertEqual(cutoff(self.at.replace(month=2)).date().isoformat(),'2025-08-01')
        self.assertEqual(archive_preview(self.at)['rows'][0]['copy_count'],0)

    def test_archive_batch_trigger_only_last_row_and_undo_projections(self):
        process=self.old('JobProcess',old_sheet_series='S',old_process_no=1,old_process_id='GX',old_station_id='06',old_status='1')
        work=self.old('WProcess',old_wprocess_no='W',old_job_sheet_no='J',old_process_no=1,old_process_id='GX',old_end_time=cutoff(self.at)-timedelta(days=1))
        archive(work,self.actor,**self.event);process.refresh_from_db();self.assertEqual(process.old_status,'0')
        undo_archive(work,self.actor,**self.event);process.refresh_from_db();self.assertEqual(process.old_status,'1')

    def test_archive_scope_failure_rolls_back(self):
        work=self.old('WProcess',old_wprocess_no='W',old_end_time=cutoff(self.at)-timedelta(days=1))
        child=self.old('WProcessStep',old_wpstep_no='STEP',old_wprocess_no='W')
        def query(name,module):return reader(name,module).none() if name=='WProcessStep' else reader(name,module)
        with self.assertRaises(ValidationError):archive(work,self.actor,query=query,**self.event)
        self.assertEqual(reader('WProcessBak','erp_production').count(),0)
        self.assertTrue(active(reader('WProcess','erp_production')).filter(pk=work.pk).exists())

    def test_chain_reverse_also_reverses_cross_card_label_targets_and_restores(self):
        from plugins.erp_base.source_chain_reverse import cancel,undo as undo_chain
        item=self.package();other=self.package(old_gray_bar_code='OUT',old_job_sheet_no='OTHER');self.gray();self.sync()
        cancel(self.job,self.actor,mode='execution_only',work_mode='trigger_only',**self.event)
        other.refresh_from_db();self.assertEqual(other.old_db2_code,'OLD')
        self.assertEqual(effect(self.job,'package_label_sync')['state'],'reversed')
        undo_chain(self.job,self.actor,**self.event)
        other.refresh_from_db();self.assertNotEqual(other.old_db2_code,'OLD')
        self.assertEqual(effect(self.job,'package_label_sync')['state'],'applied')

    def test_http_label_people_and_archive_actions(self):
        self.package();self.gray()
        root=f'/api/system/erp_production_sourcedyejobsheet/{self.job.pk}/'
        event={'at':self.at.isoformat(),'reason':'HTTP测试'}
        for action,data in [('preview_package_labels',{}),('synchronize_package_labels',event),('undo_package_labels',event)]:
            response=self.client.post(root+action+'/',data,format='json');self.assertEqual(response.status_code,200,response.data)
        for report in ['latest','shared']:
            response=self.client.post('/api/system/erp_warehouse_sourcedyerecordyield/package_people/',{'report':report},format='json')
            self.assertEqual(response.status_code,200,response.data)
        work=self.old('WProcess',old_wprocess_no='W',old_end_time=cutoff(self.at)-timedelta(days=1))
        root='/api/system/erp_production_sourcedyewprocess/'
        response=self.client.post(root+'preview_work_archive/',{'as_of':self.at.isoformat()},format='json');self.assertEqual(response.status_code,200,response.data)
        for action in ['archive_work','undo_work_archive']:
            response=self.client.post(root+str(work.pk)+'/'+action+'/',event,format='json');self.assertEqual(response.status_code,200,response.data)

    def test_label_update_trigger_starts_gx98_and_undo_restores_progress(self):
        process=self.old('JobProcess',old_sheet_series='S',old_process_no=1,old_process_id='GX98',old_station_id='98',old_status='0')
        item=self.package(old_roll_no='004',old_scroll='OLD',old_net_kg=-2,old_emp_id='E')
        self.old('HEmployee','erp_base',old_emp_id='E',old_name='包装工');self.gray()
        before=snapshot(process);self.sync();process.refresh_from_db();item.refresh_from_db()
        self.assertEqual((process.old_status,process.old_wpworker),('1','包装工'))
        self.assertIsNotNone(process.old_start_time)
        self.assertEqual((item.old_scroll,item.old_net_kg,item.old_customer_gray_name),('4',Decimal('-2'),'AB#纱线'))
        undo(self.job,self.actor,**self.event);process.refresh_from_db();item.refresh_from_db()
        self.assertEqual(item.old_scroll,'OLD')
        for name in process.SOURCE_FIELDS.values():self.assertEqual(snapshot(process)[name],before[name])

    def test_label_abnormal_roll_and_weight_retained_and_progress_scope_atomic(self):
        item=self.package(old_roll_no='手工卷',old_scroll='保留',old_kg=151,old_net_kg=-3)
        self.gray()
        process=self.old('JobProcess',old_sheet_series='S',old_process_no=1,old_process_id='GX98',old_status='0')
        def query(name,module):return reader(name,module).none() if name=='JobProcess' else reader(name,module)
        with self.assertRaises(ValidationError):synchronize(self.job,self.actor,query=query,**self.event)
        item.refresh_from_db();self.assertEqual(item.old_job_sheet_no,'BEFORE')
        self.sync();item.refresh_from_db()
        self.assertEqual((item.old_roll_no,item.old_scroll,item.old_kg,item.old_net_kg),('手工卷','保留',151,-3))

    def test_label_target_delete_requires_reverse(self):
        from plugins.erp_base.source_services import delete_documents
        item=self.package(source_batch=None);self.gray();self.sync()
        with self.assertRaises(ValidationError):delete_documents(type(item).objects.filter(pk=item.pk),self.actor)
        self.assertTrue(type(item).objects.filter(pk=item.pk).exists())

    def test_missing_job_header_can_sync_original_cursor_without_fabricating_parent(self):
        item=self.package(old_customer_gray_name='ORP#原品名',old_scroll='KEEP')
        self.gray(old_sheet_series='ORPHAN')
        result=synchronize(self.job,self.actor,series='ORPHAN',**self.event);item.refresh_from_db()
        self.assertEqual(result['candidate_rows'],[])
        self.assertEqual(item.old_job_sheet_no,'BEFORE')
        self.assertEqual(item.old_customer_gray_name,'ORP#原品名')
        self.assertEqual(item.old_db2_code,'ORP0009876123BEFORE001')
        self.assertFalse(reader('JobSheet','erp_production').filter(old_sheet_series='ORPHAN').exists())
        undo(self.job,self.actor,**self.event);item.refresh_from_db();self.assertEqual(item.old_scroll,'KEEP')

    def test_missing_job_header_nonempty_customer_has_no_update_trigger(self):
        item=self.package(old_customer_id='CUSTOMER',old_scroll='KEEP',old_job_detail_no='DETAIL')
        self.gray(old_sheet_series='ORPHAN')
        result=synchronize(self.job,self.actor,series='ORPHAN',**self.event);item.refresh_from_db()
        self.assertEqual(result['rows'][0]['after'],{})
        self.assertEqual((item.old_scroll,item.old_job_detail_no,item.old_db2_code),('KEEP','DETAIL','OLD'))
