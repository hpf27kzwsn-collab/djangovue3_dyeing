from datetime import datetime
from decimal import Decimal
from django.apps import apps
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.business import snapshot
from plugins.erp_base.source_context import SourceDocumentContext
from plugins.erp_base.source_continuation import save_effect
from plugins.erp_base.source_execution_state import active
from plugins.erp_base.source_package_operations import (reader, effect, preview_replace, replace_package,
    undo_replace, preview_pairing, apply_pairing, undo_pairing)
from plugins.erp_base.source_packaging_flow import adopt_gray_record, undo_gray_record, qc_totals
from plugins.erp_base import source_services


class PackageOperationsTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='package-operations', password='test')
        self.at = timezone.make_aware(datetime(2026, 10, 15, 15))
        self.event = {'at': self.at, 'reason': '包装替换及排序核对'}
        self.client = APIClient(); self.client.force_authenticate(self.actor)
        self.job = self.old('JobSheet', 'erp_production', old_sheet_series='JS', old_sheet_no='JOB', legacy_id='OLDJOB')

    def model(self, name, module='erp_warehouse'):
        return apps.get_model(module + '.SourceDye' + name)

    def old(self, name, module='erp_warehouse', **values):
        row = self.model(name, module).objects.create(**values); row.refresh_from_db(); return row

    def package(self, **values):
        defaults = dict(old_guid=str(self.model('RecordYield').objects.count()), old_job_sheet_no='JOB',
            old_roll_no='01', old_bar_code='B', old_kg=20, legacy_id='OLDPACK')
        defaults.update(values)
        return self.old('RecordYield', **defaults)

    def gray(self, **values):
        defaults = dict(old_sheet_series='JS', old_rece_sheet_no='R', old_roll_no='01',
            old_bar_code='G', old_gray_bar_code='GRAY', old_weight_qty=-2, legacy_id='OLDGRAY')
        defaults.update(values)
        return self.old('JobGrayRecord', 'erp_production', **defaults)

    def replace(self, row, **values):
        return replace_package(row, self.actor, **self.event, **values)

    def test_replace_all_matching_rows_keeps_originals_and_new_identity(self):
        first = self.package(old_qty=Decimal('-1.123456'), old_pack_bag=Decimal('-0.125'), old_add_weigth='原文')
        second = self.package(old_job_sheet_no='job ', old_roll_no='01 ', old_kg=None)
        unrelated = self.package(old_roll_no='02')
        before = [snapshot(row) for row in [first, second, unrelated]]
        preview = preview_replace(first)
        self.assertEqual([row['record_id'] for row in preview['rows']], [first.pk, second.pk])
        self.assertEqual(SourceDocumentContext.objects.count(), 0)
        result = self.replace(first, old_kg=Decimal('-3.25'))
        self.assertIsNone(result.legacy_id); self.assertNotEqual(result.old_guid, first.old_guid)
        self.assertEqual((result.old_bar_code, result.old_kg, result.old_qty, result.old_pack_bag),
            ('JOB01', Decimal('-3.25'), Decimal('-1.123456'), Decimal('-0.125')))
        self.assertEqual(result.old_add_weigth, '原文')
        self.assertEqual(set(active(self.model('RecordYield').objects.all()).values_list('pk', flat=True)), {unrelated.pk, result.pk})
        for row in [first, second, unrelated]: row.refresh_from_db()
        self.assertEqual([snapshot(row) for row in [first, second, unrelated]], before)
        self.assertEqual(self.model('ProdStockBook').objects.count(), 0)

    def test_procedure_parameter_columns_only_and_latest_precision(self):
        row = self.package(old_net_kg=-8, old_status=88, old_check_no='OLD', old_print_times=12,
            old_spec='长' * 400, old_color_id='色' * 130, old_weight_spec='重' * 140)
        result = self.replace(row, old_kg=None, old_scroll='手工序号')
        self.assertIsNone(result.old_net_kg); self.assertIsNone(result.old_status)
        self.assertEqual(result.old_check_no, 'OLD'); self.assertIsNone(result.old_print_times)
        self.assertIsNone(result.old_kg)
        self.assertEqual(result.old_spec, row.old_spec); self.assertEqual(result.old_color_id, row.old_color_id)
        self.assertEqual(result.old_scroll, '1')  # 原触发器对可转整数RollNo重写Scroll。

    def test_non_numeric_roll_preserves_scroll_and_empty_identity_uses_barcode_numbering(self):
        row = self.package(old_roll_no='异常卷', old_scroll='原序号')
        result = self.replace(row)
        self.assertEqual(result.old_scroll, '原序号'); self.assertEqual(result.old_bar_code, 'JOB异常卷')
        blank = self.package(old_roll_no='', old_job_sheet_no='')
        result = self.replace(blank)
        self.assertFalse(active(type(blank).objects.filter(pk=blank.pk)).exists())
        self.assertRegex(result.old_bar_code, r'^[0-9]{11,}$')

    def test_undo_restores_all_original_rows_and_keeps_replacement(self):
        first = self.package(); second = self.package(old_kg=-9)
        result = self.replace(first)
        undo_replace(result, self.actor, **self.event)
        self.assertEqual(set(active(type(first).objects.all()).values_list('pk', flat=True)), {first.pk, second.pk})
        self.assertTrue(type(first).objects.filter(pk=result.pk).exists())
        self.assertEqual(effect(result, 'package_replacement')['state'], 'reversed')
        with self.assertRaises(ValidationError): undo_replace(result, self.actor, **self.event)

    def test_repeated_replace_undo_in_reverse_order(self):
        row = self.package(); first = self.replace(row); second = self.replace(first, old_kg=-2)
        with self.assertRaises(ValidationError): undo_replace(first, self.actor, **self.event)
        undo_replace(second, self.actor, **self.event)
        undo_replace(first, self.actor, **self.event)
        self.assertEqual(list(active(type(row).objects.all()).values_list('pk', flat=True)), [row.pk])

    def test_retained_rows_cannot_be_edited_deleted_or_received_again(self):
        row = self.package(); result = self.replace(row)
        with self.assertRaises(ValidationError): source_services.write(type(row), {'old_kg': 30}, row, self.actor)
        with self.assertRaises(ValidationError): source_services.require_operation_retention(result)
        from plugins.erp_base.source_delivery_flow import receive_package
        with self.assertRaises(ValidationError):
            receive_package(row, self.actor, weight=1, length=None, rolls=1, warehouse='W', unit=1, sheet_kind=1, **self.event)

    def test_undo_restores_gx98_start_and_current_projection(self):
        process = self.old('JobProcess', 'erp_production', old_sheet_series='JS', old_process_no=1,
            old_process_id='GX98', old_status='0', old_start_time=None)
        before = snapshot(process)
        result = self.replace(self.package())
        process.refresh_from_db(); self.assertIsNotNone(process.old_start_time)
        undo_replace(result, self.actor, **self.event)
        process.refresh_from_db()
        for key in process.SOURCE_FIELDS.values(): self.assertEqual(getattr(process, key), before[key])

    def test_existing_receipts_remain_and_later_receipt_requires_own_reversal(self):
        row = self.package(old_bar_code='JOB01')
        old_receipt = self.old('ProdInRecord', old_sheet_series='OLD', old_prod_bar_code='JOB01', old_weight_qty=12, legacy_id='PI')
        before = snapshot(old_receipt)
        result = self.replace(row)
        undo_replace(result, self.actor, **self.event)
        old_receipt.refresh_from_db(); self.assertEqual(snapshot(old_receipt), before)
        result = self.replace(row)
        later = self.old('ProdInRecord', old_sheet_series='NEW', old_prod_bar_code='JOB01')
        with self.assertRaises(ValidationError): undo_replace(result, self.actor, **self.event)
        save_effect(later, 'chain_cancelled', {'active': True}, self.actor, '已撤回实际入库')
        undo_replace(result, self.actor, **self.event)

    def test_undo_changed_replacement_does_not_overwrite_or_partly_restore(self):
        row = self.package(); result = self.replace(row)
        type(result).objects.filter(pk=result.pk).update(old_kg=99)
        with self.assertRaises(ValidationError): undo_replace(result, self.actor, **self.event)
        self.assertFalse(active(type(row).objects.filter(pk=row.pk)).exists())
        self.assertEqual(effect(result, 'package_replacement')['state'], 'applied')

    def test_replace_scope_missing_same_roll_rolls_back(self):
        first = self.package(); hidden = self.package()
        def query(name, module):
            source = reader(name, module)
            return source.exclude(pk=hidden.pk) if name == 'RecordYield' else source
        with self.assertRaises(ValidationError): self.replace(first, query=query)
        self.assertEqual(type(first).objects.count(), 2); self.assertEqual(SourceDocumentContext.objects.count(), 0)

    def test_invalid_new_fields_roll_back_retirement(self):
        row = self.package()
        with self.assertRaises(ValidationError): self.replace(row, old_qty=Decimal('9999999.123456'))
        self.assertEqual(type(row).objects.count(), 1); self.assertEqual(SourceDocumentContext.objects.count(), 0)

    def test_qc_totals_and_chain_only_count_active_package(self):
        row = self.package(old_kg=100); result = self.replace(row, old_kg=Decimal('-3.5'))
        qc_totals(result, self.actor)
        self.job.refresh_from_db(); self.assertEqual(self.job.old_pkg, Decimal('-3.5'))
        from plugins.erp_base.source_chain_reverse import discover
        included = [item.pk for item in discover(self.job)['nodes'].values() if item.SOURCE_TABLE == 'RecordYield']
        self.assertEqual(included, [result.pk])

    def test_pair_lexical_roll_order_and_null_quantity(self):
        a = self.package(old_roll_no='2', old_bar_code='B2')
        b = self.package(old_roll_no='10', old_bar_code='B10')
        g1 = self.gray(old_roll_no='10', old_weight_qty=None, old_gray_bar_code='G10')
        g2 = self.gray(old_roll_no='2', old_weight_qty=-3, old_gray_bar_code='G2')
        preview = preview_pairing(self.job)
        self.assertEqual([r['source_id'] for r in preview['rows']], [g1.pk, g2.pk])
        self.assertEqual(SourceDocumentContext.objects.count(), 0)
        apply_pairing(self.job, self.actor, **self.event)
        a.refresh_from_db(); b.refresh_from_db()
        self.assertEqual((a.old_gray_weight, a.old_gray_bar_code), (Decimal('-3'), 'G2'))
        self.assertIsNone(b.old_gray_weight); self.assertEqual(b.old_gray_bar_code, 'G10')

    def test_duplicate_barcode_expands_all_candidates_and_stable_last_choice(self):
        a = self.package(old_bar_code='SAME', old_roll_no='01')
        b = self.package(old_bar_code='same ', old_roll_no='02')
        first = self.gray(old_roll_no='01'); second = self.gray(old_roll_no='02', old_gray_bar_code='SECOND')
        result = apply_pairing(self.job, self.actor, **self.event)
        for entry in result['rows']:
            self.assertEqual(entry['candidate_count'], 2); self.assertEqual(entry['source_id'], second.pk)
            self.assertEqual([g['record_id'] for g in entry['candidates']], [first.pk, second.pk])
        a.refresh_from_db(); b.refresh_from_db()
        self.assertEqual(a.old_gray_bar_code, 'SECOND'); self.assertEqual(b.old_gray_bar_code, 'SECOND')

    def test_null_barcode_unmatched_retains_old_values_and_unused_gray(self):
        row = self.package(old_bar_code=None, old_gray_weight=99, old_gray_bar_code='ORIGINAL')
        gray = self.gray()
        result = apply_pairing(self.job, self.actor, **self.event)
        row.refresh_from_db(); self.assertEqual((row.old_gray_weight, row.old_gray_bar_code), (99, 'ORIGINAL'))
        self.assertFalse(result['rows'][0]['matched']); self.assertEqual(result['supplemental_rows'][0]['record_id'], gray.pk)

    def test_empty_gray_table_is_listed_and_does_not_clear_packaging(self):
        row = self.package(old_gray_weight=-5)
        result = apply_pairing(self.job, self.actor, **self.event)
        self.assertEqual(len(result['rows']), 1); self.assertEqual(result['rows'][0]['candidate_count'], 0)
        row.refresh_from_db(); self.assertEqual(row.old_gray_weight, -5)
        undo_pairing(self.job, self.actor, **self.event)

    def test_duplicate_job_number_and_duplicate_series_join_rows_preserved(self):
        second_job = self.old('JobSheet', 'erp_production', old_sheet_series='JS', old_sheet_no='job ')
        third_job = self.old('JobSheet', 'erp_production', old_sheet_series='OTHER', old_sheet_no='JOB')
        self.package(); self.package(old_roll_no='02', old_bar_code='B2')
        self.gray(); self.gray(old_sheet_series='OTHER')
        rows = preview_pairing(self.job)['rows']
        self.assertEqual(rows[0]['candidate_count'], 2)
        self.assertEqual(rows[1]['candidate_count'], 1)
        self.assertEqual(rows[1]['candidates'][0]['job_id'], second_job.pk)
        self.assertIn(third_job.pk, [c['job_id'] for c in rows[0]['candidates']])

    def test_pair_undo_restores_fields_and_previous_explicit_source(self):
        row = self.package(old_gray_weight=9, old_gray_bar_code='BEFORE')
        gray = self.gray(); adopt_gray_record(row, self.actor, gray, **self.event)
        original_effect = effect(row, 'package_gray_origin')
        apply_pairing(self.job, self.actor, **self.event)
        with self.assertRaises(ValidationError): apply_pairing(self.job, self.actor, **self.event)
        undo_pairing(self.job, self.actor, **self.event)
        self.assertEqual(effect(row, 'package_gray_origin'), original_effect)
        undo_gray_record(row, self.actor, **self.event)
        row.refresh_from_db(); self.assertEqual((row.old_gray_weight, row.old_gray_bar_code), (9, 'BEFORE'))

    def test_later_explicit_adoption_must_be_undone_before_pairing(self):
        row = self.package(old_gray_weight=8); gray = self.gray()
        apply_pairing(self.job, self.actor, **self.event)
        other = self.gray(old_roll_no='02', old_weight_qty=33)
        adopt_gray_record(row, self.actor, other, **self.event)
        with self.assertRaises(ValidationError): undo_pairing(self.job, self.actor, **self.event)
        undo_gray_record(row, self.actor, **self.event)
        undo_pairing(self.job, self.actor, **self.event)
        row.refresh_from_db(); self.assertEqual(row.old_gray_weight, 8)

    def test_pair_scope_cannot_silently_skip_hidden_gray(self):
        row = self.package(); gray = self.gray()
        def query(name, module):
            source = reader(name, module)
            return source.none() if name == 'JobGrayRecord' else source
        with self.assertRaises(ValidationError): apply_pairing(self.job, self.actor, query=query, **self.event)
        row.refresh_from_db(); self.assertIsNone(row.old_gray_weight)
        self.assertEqual(SourceDocumentContext.objects.count(), 0)

    def test_retained_packaging_and_consumed_gray_excluded_from_pairing(self):
        old = self.package(); new = self.replace(old)
        consumed = self.gray(); remaining = self.gray(old_roll_no='02', old_weight_qty=7)
        save_effect(consumed, 'gray_consumed', {'active': True}, self.actor, '已合并留档')
        result = preview_pairing(self.job)['rows']
        self.assertEqual([row['record_id'] for row in result], [new.pk])
        self.assertEqual(result[0]['source_id'], remaining.pk)

    def test_more_than_999_uses_full_ordinal_without_collision(self):
        model = self.model('RecordYield')
        model.objects.bulk_create([model(old_guid=str(i), old_job_sheet_no='JOB', old_roll_no=str(i).zfill(4), old_bar_code='B'+str(i)) for i in range(1001)])
        gray_model = self.model('JobGrayRecord', 'erp_production')
        gray_model.objects.bulk_create([gray_model(old_sheet_series='JS', old_rece_sheet_no='R', old_roll_no=str(i).zfill(4),
            old_weight_qty=i, old_gray_bar_code='G'+str(i)) for i in range(1001)])
        result = preview_pairing(self.job)['rows']
        self.assertEqual(len(result), 1001); self.assertEqual(result[-1]['rank'], 1001)
        self.assertEqual(result[-1]['GrayBarCode'], 'G1000')
        self.assertTrue(all(row['candidate_count'] == 1 for row in result))

    def test_changed_pair_field_rolls_back_undo(self):
        a = self.package(old_roll_no='01'); b = self.package(old_roll_no='02', old_bar_code='B2')
        self.gray(); self.gray(old_roll_no='02')
        apply_pairing(self.job, self.actor, **self.event)
        type(a).objects.filter(pk=a.pk).update(old_gray_weight=31)
        with self.assertRaises(ValidationError): undo_pairing(self.job, self.actor, **self.event)
        b.refresh_from_db(); self.assertEqual(b.old_gray_weight, -2)
        self.assertEqual(effect(self.job, 'package_pairing')['state'], 'applied')

    def test_package_pairing_and_execution_chain_cancel_restore(self):
        from plugins.erp_base.source_chain_reverse import cancel, undo
        old = self.package(); result = self.replace(old); self.gray()
        apply_pairing(self.job, self.actor, **self.event)
        cancel(self.job, self.actor, mode='execution_only', work_mode='trigger_only', **self.event)
        self.assertFalse(active(type(result).objects.all()).exists())
        with self.assertRaises(ValidationError): undo_pairing(self.job, self.actor, **self.event)
        undo(self.job, self.actor, **self.event)
        self.assertEqual(list(active(type(result).objects.all()).values_list('pk', flat=True)), [result.pk])
        undo_pairing(self.job, self.actor, **self.event)
        undo_replace(result, self.actor, **self.event)
        self.assertEqual(list(active(type(result).objects.all()).values_list('pk', flat=True)), [old.pk])

    def test_chain_follows_replaced_package_receipts_with_missing_job_number(self):
        from plugins.erp_base.source_chain_reverse import discover, cancel, undo
        from plugins.erp_base.source_continuation import origin
        old = self.package(); first = self.replace(old); new = self.replace(first)
        receipt = self.old('ProdIn', old_sheet_series='PI', old_sheet_no='PI', old_job_sheet_no=None, legacy_id='OLDPI')
        save_effect(receipt, 'package_receipt_origin', origin(old), self.actor, '明确旧包装入库来源')
        book = self.old('ProdStockBook', old_book_no=1, old_sheet_series='PI', old_in_weight_qty=-3, legacy_id='OLDBOOK')
        data = discover(self.job)
        self.assertIn((receipt._meta.label, receipt.pk), data['nodes'])
        self.assertNotIn((old._meta.label, old.pk), data['nodes'])
        self.assertIn((book._meta.label, book.pk), data['ledgers'])
        cancel(self.job, self.actor, mode='execution_only', work_mode='trigger_only', **self.event)
        undo(self.job, self.actor, **self.event)
        self.assertTrue(active(type(receipt).objects.filter(pk=receipt.pk)).exists())
        self.assertEqual(list(active(type(new).objects.all()).values_list('pk', flat=True)), [new.pk])

    def test_http_actions_and_parameter_metadata(self):
        row = self.package(); self.gray()
        package_url = '/api/system/erp_warehouse_sourcedyerecordyield/'
        job_url = f'/api/system/erp_production_sourcedyejobsheet/{self.job.pk}/'
        event = {'at': self.at.isoformat(), 'reason': 'HTTP验证'}
        response = self.client.post(package_url+f'{row.pk}/preview_package_replace/', {}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        response = self.client.post(package_url+f'{row.pk}/replace_package/', {**event, 'old_kg': '-2.25', 'old_pack_bag': '-0.001'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        new = self.model('RecordYield').objects.latest('pk')
        self.assertEqual(new.old_pack_bag, Decimal('-0.001'))
        for action, data in [('preview_package_pairing', {}), ('apply_package_pairing', event), ('undo_package_pairing', event)]:
            response = self.client.post(job_url+action+'/', data, format='json')
            self.assertEqual(response.status_code, 200, response.data)
        response = self.client.post(package_url+f'{new.pk}/undo_package_replace/', event, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        response = self.client.get('/api/meta/erp_warehouse_sourcedyerecordyield/')
        inputs = next(action['inputs'] for action in response.data['data']['workflow']['actions'] if action['key'] == 'replace_package')
        self.assertEqual(next(field['source_field'] for field in inputs if field['key'] == 'old_pack_bag'), 'old_pack_bag')
