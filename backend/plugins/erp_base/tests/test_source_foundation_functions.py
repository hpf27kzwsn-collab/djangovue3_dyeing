import json
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from django.apps import apps
from django.db import IntegrityError
from django.test import SimpleTestCase, TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base import source_foundation_functions as functions
from plugins.erp_base import source_foundation_queries as queries
from plugins.erp_base.source_daily_numbers import allocate
from plugins.erp_base.source_foundation import correspondence
from plugins.erp_base.legacy_models import LegacyImportBatch


def model(name):
    return apps.get_model('erp_base', 'SourceDye'+name)


class FoundationFunctionTests(SimpleTestCase):
    """期望值来自2026-10-16只读执行旧函数，包含原函数转换错误。"""
    def test_all_scalar_sql_results_and_errors(self):
        evidence = json.loads(Path(__file__).with_name('foundation_function_results.json').read_text(encoding='utf8'))
        for probe in evidence['probes']:
            with self.subTest(function=probe['name'], value=probe['input']):
                if not probe['ok']:
                    with self.assertRaises((ValueError, OverflowError)):
                        functions.FUNCTIONS[probe['name']](probe['input'])
                else:
                    expected = probe['value']
                    actual = functions.FUNCTIONS[probe['name']](probe['input'])
                    if isinstance(actual, Decimal):
                        expected = Decimal(str(expected))
                    self.assertEqual(actual, expected)

    def test_all_sql_calendar_groups(self):
        evidence = json.loads(Path(__file__).with_name('foundation_function_results.json').read_text(encoding='utf8'))
        for probe in evidence['dates']:
            with self.subTest(kind=probe['kind'], previous=probe['prev'], following=probe['next']):
                actual = functions.continuous_dates(date(2024, 2, 29), probe['kind'], probe['prev'], probe['next'])
                for row in actual:
                    row['DataDate'] = row['DataDate'].isoformat()
                self.assertEqual(actual, probe['rows'])


class FoundationQueryTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='functions-test', password=None)
        self.client = APIClient(); self.client.force_authenticate(self.actor)
        self.at = timezone.make_aware(datetime(2026, 10, 16, 9, 30))

    def test_parameter_name_and_value_truncate_but_source_does_not(self):
        source = model('SSysParams')
        source.objects.create(old_param_name='X'*20, old_param_value='中文'*20)
        long_name = 'MachineFault_UseFaultClass'
        row = source.objects.create(old_param_name=long_name, old_param_value='YES-LONG-VALUE')
        self.assertEqual(queries.parameter_value('X'*30), '中文'*5)
        self.assertIsNone(queries.parameter_value(long_name))
        self.assertEqual(queries.system_parameters()['rows'][0][long_name], 'YES-LONG-V')
        row.refresh_from_db(); self.assertEqual(row.old_param_value, 'YES-LONG-VALUE')
        self.assertEqual(str(source._meta.get_field('legacy_id').verbose_name), '旧erpID')

    def test_combo_keeps_duplicates_nulls_wildcards_and_unsorted_indexes(self):
        source = model('SDBComboValue')
        for index, code, label in [(9, 'A', '同名'), (1, 'A', '同名'), (None, '', None)]:
            source.objects.create(old_combo_id='C', old_display_index=index, old_key_value=code, old_display_value=label)
        self.assertEqual([r['index'] for r in queries.combo('c ', '')['rows']], [9, 1, None])
        self.assertEqual(len(queries.combo('C', '%')['rows']), 3)
        self.assertEqual(queries.combo('C', None)['rows'], [])
        self.assertEqual(queries.combo(None, '')['rows'], [])

    def test_dictionary_and_gray_use_original_name_keys_and_keep_stopped(self):
        model('PFieldValid').objects.create(old_field_type='ArticleUnit', old_code='KG', old_name='公斤', old_is_stop=True)
        model('PGray').objects.create(old_gray_id='G1', old_name_c='母规格', old_stock_unit=1, old_is_stop=True)
        child = model('PGray').objects.create(old_gray_id='G2', old_name_c='子规格', old_father_gray_id='母规格')
        self.assertEqual(queries.lookup('B049')['rows'], [{'id': '公斤', 'text': '公斤'}])
        self.assertEqual(queries.lookup('B405', '母', ['unit'])['rows'], [{'id': '母规格', 'text': '母规格', 'unit': 1}])
        row = next(r for r in correspondence(child)['rows'] if r['field'] == 'FatherGrayID')
        self.assertEqual(row['matched_count'], 1)

    def test_customer_query_retains_contact_multiplication_and_original_right_status(self):
        source = model('PCustomer')
        source.objects.create(old_customer_id='C', old_short_name='未审核客户', old_cust_kind_id='0', old_right_status=0)
        source.objects.create(old_customer_id='P', old_short_name='主客户', old_cust_kind_id='0', old_right_status=10)
        source.objects.create(old_customer_id='S', old_short_name='供应商', old_cust_kind_id='1')
        source.objects.create(old_customer_id='STOP', old_short_name='停用客户', old_cust_kind_id='0', old_is_stop=True)
        for name in ['甲', '乙']:
            model('PCustLinker').objects.create(old_customer_id='C', old_row_no=1, old_name=name)
        result = queries.lookup('B001', '', ['Linker', 'EbOd'])['rows']
        self.assertEqual([r['Linker'] for r in result if r['id'] == 'C'], ['甲', '乙'])
        self.assertEqual([r['id'] for r in result], ['C', 'C', 'P'])
        self.assertEqual(queries.lookup('A002')['rows'], [{'id': 'P', 'text': '主客户'}])

    def test_employee_variants_keep_departed_and_department_join_multiplication(self):
        for name in ['部门一', '同码部门']:
            model('PDept').objects.create(old_dept_id='D', old_name=name)
        model('HEmployee').objects.create(old_emp_id='E', old_name='在职', old_dept_id='D')
        model('HEmployee').objects.create(old_emp_id='L', old_name='离职', old_is_out=True)
        self.assertEqual(len(queries.lookup('B006', '', ['DeptIDName'])['rows']), 2)
        self.assertEqual(len(queries.lookup('B154')['rows']), 3)
        with self.assertRaises(KeyError):
            queries.lookup('B006', '', ['BusinessUnitID'])

    def test_external_lookup_explicitly_reports_missing_source(self):
        self.assertTrue(all(row['adapter'] is not None for row in queries.LOOKUPS.values()))
        report = queries.lookup('B153')
        self.assertFalse(report['implemented'])
        self.assertEqual(report['status'],'external_source_required')
        self.assertTrue(report['supplemental_rows'][0]['issue'])

    def test_daily_short_long_and_rollover_do_not_share_counters(self):
        self.assertEqual(allocate('ORDER', 3, False, self.actor, self.at)['rows'][0]['code'], '261016001')
        self.assertEqual(allocate('order ', 3, False, self.actor, self.at)['rows'][0]['code'], '261016002')
        self.assertEqual(allocate('ORDER', 3, True, self.actor, self.at)['rows'][0]['code'], '20261016001')
        tomorrow = self.at.replace(day=17)
        self.assertEqual(allocate('ORDER', 3, False, self.actor, tomorrow)['rows'][0]['code'], '261017001')

    def test_daily_negative_duplicate_and_null_counters_are_not_normalized(self):
        source = model('SAutoID')
        a = source.objects.create(old_idobject='D', old_idvalue='261016', old_idcounter=9)
        b = source.objects.create(old_idobject='D', old_idvalue='261016', old_idcounter=-2)
        self.assertEqual(allocate('D', 3, False, self.actor, self.at)['rows'][0]['code'], '2610160-2')
        a.refresh_from_db(); b.refresh_from_db()
        self.assertEqual((a.old_idcounter, b.old_idcounter), (10, -1))
        null = source.objects.create(old_idobject='N', old_idvalue='261016', old_idcounter=None)
        self.assertIsNone(allocate('N', 3, False, self.actor, self.at)['rows'][0]['code'])
        null.refresh_from_db(); self.assertIsNone(null.old_idcounter)
        with self.assertRaises(IntegrityError):
            allocate(None, 3, False, self.actor, self.at)
        self.assertFalse(source.objects.filter(old_idobject__isnull=True).exists())

    def test_daily_width_expands_null_digits_still_increment_and_overflow_rolls_back(self):
        source = model('SAutoID')
        row = source.objects.create(old_idobject='W', old_idvalue='261016', old_idcounter=999)
        self.assertEqual(allocate('W', 2, False, self.actor, self.at)['rows'][0]['code'], '261016999')
        self.assertIsNone(allocate('W', None, False, self.actor, self.at)['rows'][0]['code'])
        row.refresh_from_db(); self.assertEqual(row.old_idcounter, 1001)
        row.old_idcounter = 2147483647; row.save()
        self.assertEqual(allocate('W', 3, False, self.actor, self.at)['rows'][0]['code'], '2610162147483647')
        with self.assertRaises(OverflowError):
            allocate('W', 3, False, self.actor, self.at)
        row.refresh_from_db(); self.assertEqual(row.old_idcounter, 2147483648)

    def test_adopted_counter_leaves_historical_source_and_id_unchanged(self):
        now = timezone.now()
        batch = LegacyImportBatch.objects.create(number='NUMBER-TRIAL', database_name='Textile_GXHFRS',
            started_at=now, finished_at=now, manifest_sha256='d'*64, source_directory='test-only',
            table_count=1, row_count=1, byte_count=0, verified_at=now)
        original = model('SAutoID').objects.create(source_batch=batch, source_row=1,
            old_idobject='H', old_idvalue='261016', old_idcounter=17)
        result = allocate('H', 3, False, self.actor, self.at)
        self.assertEqual(result['rows'][0]['code'], '261016017')
        self.assertEqual(result['source_ids'], [original.pk])
        original.refresh_from_db(); self.assertEqual(original.old_idcounter, 17)
        self.assertEqual(allocate('H', 3, False, self.actor, self.at)['rows'][0]['code'], '261016018')

    def test_new_api_routes_and_original_numeric_error(self):
        root = '/api/system/erp_base_sourcedyepfieldvalid/'
        for action, data in [('original_function', {'function': 'SafeVarToInt', 'value': '12.5'}),
                             ('continuous_dates', {'value': '2024-02-29', 'kind': 'md', 'previous': 26, 'following': 25}),
                             ('original_combo', {'combo_id': 'C', 'filter_text': ''}),
                             ('original_lookup', {'lookup_id': 'B049', 'filter_text': ''})]:
            response = self.client.post(root+action+'/', data, format='json')
            self.assertEqual(response.status_code, 200, response.data)
        response = self.client.post(root+'original_function/', {'function': 'SafeVarToFloat', 'value': '1..2'}, format='json')
        self.assertEqual(response.status_code, 400, response.data)
        response = self.client.post('/api/system/erp_base_sourcedyesautoid/allocate_number/',
            {'object_name': 'API', 'digits': 3, 'long_date': False}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        response = self.client.post('/api/system/erp_base_sourcedyessysparams/system_parameters/', {}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
