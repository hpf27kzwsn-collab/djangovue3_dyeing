"""缺列查询、原转单、游标自动联动及分组原版式的非空回归。"""
from decimal import Decimal
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase, SimpleTestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from .test_phase_report_audit import create
from .test_source_phase6 import reader
from plugins.erp_base.source_phase3_operations import model, source
from plugins.erp_base.source_phase6_entries import run
from plugins.erp_base.source_phase6_transfers import purchase_to_arrival
from tools.development_archive.customer_boundary_20261024.backend.source_phase6_api import templates
from plugins.erp_base.source_phase6_rendering import render, requirements
from plugins.erp_base.source_context import SourceDocumentContext
from plugins.erp_base import source_services as services


class ContinuationTests(TestCase):
    def setUp(self):
        self.actor = get_user_model().objects.create(username='phase6-continuation', is_superuser=True)
        self.client = APIClient();self.client.force_authenticate(self.actor)

    def test_purchase_formula_save_edit_null_and_explicit_original_amount(self):
        from plugins.erp_base.source_phase6_forms import extend
        resources = {'SourceDyePurDetail':{'crud_fields':list(model('PurDetail').SOURCE_FIELDS.values()),
            'workflow':{'actions':[]}}}
        extend(resources)
        configured = next(r for r in resources['SourceDyePurDetail']['workflow']['entries'] if r['value']=='PurDetail')
        self.assertIn('old_amount', configured['generated_fields'])
        item = services.write(model('PurDetail'), {'_entry':'PurDetail','old_sheet_series':'P',
            'old_qty':Decimal('-2.5'),'old_price':Decimal('3')}, actor=self.actor)
        self.assertEqual(item.old_amount, Decimal('-7.5'))
        item = services.write(type(item), {'old_qty':Decimal('4')}, item, actor=self.actor)
        self.assertEqual(item.old_amount, Decimal('12'))
        item = services.write(type(item), {'old_price':None}, item, actor=self.actor)
        self.assertIsNone(item.old_amount)
        item = services.write(type(item), {'old_price':Decimal('8'),'old_amount':Decimal('-99')}, item, actor=self.actor)
        self.assertEqual(item.old_amount, Decimal('-99'))
        item = services.write(type(item), {'old_remarks':'保留异常录入结果'}, item, actor=self.actor)
        self.assertEqual(item.old_amount, Decimal('-99'))

    def test_missing_projection_keeps_original_job_filter_and_distinct(self):
        for _ in range(2):create('JobSheet', SheetSeries='J', SheetNo='JN', ColorNum='C')
        create('JobProcess', SheetSeries='J', ProcessNo='1', ProcessID='GX', Status=None)
        create('JobProcess', SheetSeries='J', ProcessNo='2', ProcessID='GX', Status='Y')
        create('JobProcess', SheetSeries='J', ProcessNo='3', ProcessID='', Status=None)
        result = run('qry_CraftPreCheckJobSheet', {}, reader, load_records=True)
        self.assertEqual(result['count'], 1)
        names = [c['name'].lower() for c in result['columns']]
        self.assertIsNone(result['rows'][0][names.index('isnew')])
        self.assertEqual(result['reconstruction']['missing_columns'][0]['source'], 'a.IsNew')
        self.assertEqual(model('JobSheet').objects.count(), 2)

    def test_missing_return_fields_keep_tautological_join_duplicates_and_negative_quantity(self):
        for series in ['A','B']:create('GrayOut', SheetSeries=series, SheetNo=series)
        for _ in range(2):create('GrayOutDetail', SheetSeries='UNRELATED', WeightQty=-2, Remarks='原重复')
        result = run('vwGrayOutQueryBySaleBack', {}, reader, load_records=True)
        names = [c['name'].lower() for c in result['columns']]
        self.assertEqual(result['count'], 4)
        for row in result['rows']:
            self.assertEqual(row[names.index('weightqty')], -2)
            self.assertIsNone(row[names.index('structure')]);self.assertIsNone(row[names.index('jobdetailno')])
        self.assertEqual(len(result['reconstruction']['missing_columns']), 2)

    def test_purchase_transfer_preserves_duplicates_null_and_negative_and_runs_finish_once(self):
        head = services.write(model('ArrivalNotice'), {'_entry':'ArrivalNotice'}, actor=self.actor)
        selected = [create('PurDetail', DetailNo='DUP', FabricID='F', Qty=Decimal('-2.5'),
                           Rolls=-1, ColorID=None, ColorNum='', Spec='原规格') for _ in range(2)]
        with patch.object(services, 'finish', wraps=services.finish) as finish:
            result = purchase_to_arrival(head, selected, self.actor)
        self.assertEqual(finish.call_count, 1)
        lines = list(model('ArrivalNoticeDetail').objects.order_by('pk'))
        self.assertEqual(len(lines), 2);self.assertNotEqual(lines[0].old_detail_no, lines[1].old_detail_no)
        for original, line in zip(selected, lines):
            self.assertEqual(line.old_pur_detail_no, 'DUP');self.assertEqual(line.old_qty, Decimal('-2.5'))
            self.assertEqual(line.old_rolls, -1);self.assertIsNone(line.old_color_id);self.assertEqual(line.old_color_num, '')
            self.assertEqual(line.source_parent_1_id, head.pk)
            context = SourceDocumentContext.objects.get(entity=line._meta.label, object_id=line.pk)
            self.assertEqual(context.effects['field_copy_origin']['source_id'], original.pk)
        self.assertEqual(len(result['rows']), 2)
        self.assertEqual(model('PurDetail').objects.count(), 2)

    def test_gray_in_out_keeps_left_join_false_and_each_receipt_match(self):
        create('GrayIn', SheetSeries='IN', SheetNo='IN001')
        create('GrayInDetail', SheetSeries='IN', ReceSheetNo='R', WeightQty=10)
        create('GrayOut', SheetSeries='IN', SheetNo='NOT_JOINED')
        for _ in range(2):create('GrayOutDetail', ReceSheetNo='R', WeightQty=3)
        result = run('vwGrayInAndOutDetailQuery', {}, reader, load_records=True)
        names = [c['name'].lower() for c in result['columns']]
        self.assertEqual(result['count'], 2)
        for row in result['rows']:
            self.assertEqual(row[names.index('remainweightqty')], 7)
            self.assertIsNone(row[names.index('outsheetdate')])
        self.assertEqual(len(result['reconstruction']['missing_columns']), 4)

    def test_reconstructed_query_api_keeps_difference_and_csv_nulls(self):
        create('JobSheet', SheetSeries='J', SheetNo='J')
        create('JobProcess', SheetSeries='J', ProcessID='GX', ProcessNo='1')
        path = '/api/system/erp_production_sourcedyejobsheet/'
        body = {'entry':'qry_CraftPreCheckJobSheet','load_records':True}
        response = self.client.post(path+'phase6_query/', body, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(len(response.data['data']['reconstruction']['missing_columns']), 1)
        csv = self.client.post(path+'phase6_export/', body, format='json')
        self.assertEqual(csv.status_code, 200);self.assertIn('\\N', csv.content.decode('utf-8-sig'))

    def test_transfer_repeated_source_is_not_silently_removed_and_http_works(self):
        head = services.write(model('ArrivalNotice'), {'_entry':'ArrivalNotice'}, actor=self.actor)
        original = create('PurDetail', DetailNo='D', FabricID='F', Qty=None, Rolls=None)
        response = self.client.post('/api/system/erp_base_sourcedyearrivalnotice/'+str(head.pk)+'/phase6_purchase_to_arrival/',
            {'selected':[original.pk, original.pk]}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(model('ArrivalNoticeDetail').objects.count(), 2)
        self.assertTrue(all(line.old_qty is None for line in model('ArrivalNoticeDetail').objects.all()))

    def test_transfer_rolls_back_whole_batch_on_write_failure(self):
        head = services.write(model('ArrivalNotice'), {'_entry':'ArrivalNotice'}, actor=self.actor)
        original = create('PurDetail', DetailNo='D', FabricID='F')
        with self.assertRaises(ValidationError):purchase_to_arrival(head, [original, head], self.actor)
        self.assertEqual(model('ArrivalNoticeDetail').objects.count(), 0)

    def test_missing_required_target_material_reports_source_without_discarding_batch(self):
        head = services.write(model('ArrivalNotice'), {'_entry':'ArrivalNotice'}, actor=self.actor)
        good = create('PurDetail', DetailNo='A', FabricID='F')
        missing = create('PurDetail', DetailNo='B', FabricID=None)
        with self.assertRaisesMessage(ValidationError, str(missing.pk)):
            purchase_to_arrival(head, [good, missing], self.actor)
        self.assertEqual(model('ArrivalNoticeDetail').objects.count(), 0)
        self.assertEqual(model('PurDetail').objects.count(), 2)

    def test_auto_trial_cursor_executes_each_candidate_retains_intermediate_and_can_undo(self):
        from plugins.erp_base.source_trial_variants import undo
        from plugins.erp_base.source_package_operations import effect
        create('p_Shift', ShiftID='S', StationID='02', ClassID='C')
        for _ in range(2):create('p_ShiftEmp', ShiftID='S', EmpID='E')
        item = services.write(model('ProdTest'), {'_entry':'ProdTest_AddColorProduct', 'old_emp_id':'E',
            'old_job_sheet_no':'J', 'old_value38':'GX41', 'old_value40':'P'}, actor=self.actor)
        self.assertEqual(source('WProcess').count(), 1)
        self.assertEqual(model('WProcess').objects.count(), 2)
        self.assertEqual(model('WProcessStep').objects.count(), 2)
        value = effect(item, 'trial_work')
        self.assertEqual(len(value['intermediate']), 3);self.assertEqual(len(value['created']), 3)
        self.assertEqual(len(value['report']['candidate_rows']), 2)
        undo(item, self.actor, timezone.now(), '核对整链撤销')
        self.assertEqual(source('WProcess').count(), 0)
        self.assertEqual(model('WProcess').objects.count(), 2)
        self.assertEqual(source('WProcessStep').count(), 0)


class GroupPrintTests(SimpleTestCase):
    def result(self, rows):
        return {'entry':'DyeLabColor', 'columns':[{'name':n} for n in
            ['CustomerID','SheetNo','ProdID_R','ColorID','ColorNum','CustomerID_R','Remarks']], 'rows':rows}

    def test_original_group_header_breaks_per_customer_and_keeps_duplicates(self):
        row = templates()[3]
        self.assertEqual(requirements(row), [])
        a = ['A','A001','纱线','红','C','甲客户','重复保留']
        b = ['B','B001','纱线','蓝','C2','乙客户','<原值>']
        result = render(row, self.result([b,a,a]))
        self.assertEqual(result['page_count'], 2);self.assertEqual(result['record_count'], 3)
        self.assertEqual(result['html'].count('A001'), 2)
        self.assertLess(result['html'].index('A001'),result['html'].index('B001'))
        self.assertIn('&lt;原值&gt;',result['html'])

    def test_group_overflow_has_no_blank_page_or_lost_row(self):
        a = ['A','A001','纱线','红','C','甲客户','']
        result = render(templates()[3], self.result([a]*40))
        self.assertEqual(result['page_count'], 2);self.assertEqual(result['record_count'], 40)
        self.assertEqual(result['html'].count('A001'), 40)

    def test_null_empty_and_text_group_values_stay_separate(self):
        rows = [[key, str(index),'','','','客户',''] for index,key in enumerate([None,'','a','A'])]
        result = render(templates()[3], self.result(rows))
        self.assertEqual(result['page_count'], 4)
        empty = render(templates()[3], self.result([]))
        self.assertEqual(empty['page_count'], 0)
