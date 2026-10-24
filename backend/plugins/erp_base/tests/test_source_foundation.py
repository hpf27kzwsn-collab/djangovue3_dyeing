from plugins.erp_base.tests.source_fixtures import historical_batch
from datetime import date
from decimal import Decimal
from django.apps import apps
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base import source_foundation as service
from plugins.erp_base.source_services import write
from plugins.erp_base.source_provenance import reference
from plugins.erp_base.legacy_models import LegacyImportBatch
from plugins.erp_base.source_entry_registry import ENTRY_RULES

def model(module, name):
    return apps.get_model(module, 'SourceDye' + name)

class OriginalUnitTests(SimpleTestCase):
    """convertUnit及dbo/dye.fn_GetDays的有效分支和边界。"""

    def test_original_factors_input_and_output_rounding(self):
        self.assertEqual(service.convert_unit(0, 2, '1.005'), Decimal('1.10'))
        self.assertEqual(service.convert_unit(2, 0, '1'), Decimal('.91'))
        self.assertEqual(service.convert_unit(1, 3, '-10.125'), Decimal('-22.33'))
        self.assertEqual(service.convert_unit(3, 1, '99.99'), Decimal('45.36'))

    def test_unknown_cross_dimension_and_null_units_keep_original_behavior(self):
        for pair in [(4, 1), (0, 1), (255, 2), (None, 3), (1, None), (None, None)]:
            self.assertEqual(service.convert_unit(*pair, '-1.005'), Decimal('-1.01'))
        self.assertIsNone(service.convert_unit(1, 3, None))
        with self.assertRaises(OverflowError):
            service.convert_unit(1, 3, '99999999.99')

    def test_both_date_functions_keep_old_day_source_limit_and_leap_day(self):
        self.assertEqual(service.get_days(date(2024, 2, 28), date(2024, 3, 1)), [{'days': date(2024, 2, 28)}, {'days': date(2024, 2, 29)}, {'days': date(2024, 3, 1)}])
        self.assertEqual(len(service.get_days(date(2000, 1, 1), date(2026, 1, 1))), 2048)
        self.assertEqual(service.get_days(date(2026, 1, 1), date(2025, 1, 1)), [])
        self.assertEqual(service.get_days(None, date(2026, 1, 1)), [])
        self.assertEqual(service.get_days(date.max, date.max), [{'days': date.max}])
        self.assertEqual(service.get_days(date(9999, 12, 30), date.max), [{'days': date(9999, 12, 30)}, {'days': date.max}])

class FoundationSourceTests(TestCase):
    """原来源、SalaryChanges_InUp、fn_ConcatBusinessUnitID和fn_ConcatBusinessUnitName。"""

    def setUp(self):
        self.actor = Users.objects.create_superuser(username='foundation-test', password='test-only')
        self.client = APIClient()
        self.client.force_authenticate(self.actor)

    def test_all_mixed_sources_are_recordable_without_finance_workflows(self):
        for module, name in [('erp_base', 'HSalaryAttend'), ('erp_base', 'ZKAttendanceMonthStatistics'), ('erp_production', 'HSalaryWorkQty'), ('erp_production', 'HSalaryWorkShift'), ('erp_quality', 'FARMain'), ('erp_quality', 'FARDetail'), ('erp_quality', 'FARRecord')]:
            source = model(module, name)
            self.assertNotIn('legacy_id', {f.name for f in source._meta.fields})
            self.assertFalse(source.SOURCE_DOCUMENT)
        for name in ['FARMain', 'FARDetail', 'FARRecord']:
            self.assertNotIn('erp_quality.SourceDye' + name, ENTRY_RULES)
        row = model('erp_production', 'HSalaryWorkQty').objects.create(old_id=1, old_calc_month='202610', old_work_qty=-3, old_amount=Decimal('-100.25'), old_emp_id='ORIGINAL-UNKNOWN')
        row.refresh_from_db()
        self.assertEqual(row.old_work_qty, -3)
        self.assertEqual(row.old_amount, Decimal('-100.25'))

    def test_new_delivery_header_and_child_use_original_entry_numbers_and_parent(self):
        head = write(model('erp_sales', 'ClothGetMoney'), {'_entry': 'ClothGetMoney', 'old_customer_id': 'ORIGINAL-CUSTOMER'}, actor=self.actor)
        child = write(model('erp_sales', 'ClothGetMoneyDetail'), {'source_parent_1': head, 'old_prod_id': 'OLD-PROD', 'old_rolls': -2, 'old_this_rolls': 1}, actor=self.actor)
        self.assertIsNotNone(head.old_sheet_series)
        self.assertEqual(child.old_sheet_series, head.old_sheet_series)
        self.assertIsNotNone(child.old_detail_no)
        self.assertIsNone(head.source_batch_id)
        self.assertEqual(model('erp_warehouse', 'ProdOut').objects.count(), 0)

    def test_adjustment_uses_only_original_kind_three_four_job_check(self):
        source = model('erp_production', 'SalaryChanges')
        with self.assertRaises(ValidationError):
            write(source, {'old_sheet_series': 'BAD', 'old_kind': 3, 'old_job_sheet_no': 'MISSING'}, actor=self.actor)
        self.assertFalse(source.objects.exists())
        row = write(source, {'old_sheet_series': 'OTHER', 'old_kind': 1, 'old_job_sheet_no': 'MISSING'}, actor=self.actor)
        self.assertEqual(row.old_job_sheet_no, 'MISSING')
        model('erp_production', 'JobSheet').objects.create(old_sheet_series='J', old_sheet_no='JOB')
        row = write(source, {'old_sheet_series': 'OK', 'old_kind': 4, 'old_job_sheet_no': 'job  '}, actor=self.actor)
        self.assertEqual(row.old_kind, 4)
        self.assertEqual(model('erp_production', 'WProcess').objects.count(), 0)
        original = source.objects.create(old_sheet_series='HIST', old_kind=3, old_job_sheet_no='MISSING', source_batch=historical_batch())
        service.salary_changes_saved(original)


    def test_business_unit_strings_keep_empty_source_suffix_matching_and_stopped_rows(self):
        dictionary = model('erp_base', 'PFieldValid')
        self.assertEqual(service.business_units('MISSING')['unit_ids'], None)
        self.assertEqual(service.business_units('MISSING')['unit_names'], '')
        dictionary.objects.create(old_field_type='BusinessUnit', old_code='1', old_name='一厂', old_is_stop=True)
        dictionary.objects.create(old_field_type='BusinessUnit', old_code='11', old_name='十一厂')
        model('erp_base', 'HEmployee').objects.create(old_emp_id='E', old_business_unit_id='11')
        actual = service.business_units('E')
        self.assertEqual(actual['unit_ids'], '11')
        self.assertEqual(actual['unit_names'], '一厂;十一厂')
        self.assertEqual(service.business_units('MISSING')['unit_ids'], '1;11')

    def test_factory_lookup_is_department_and_article_unit_key_is_name(self):
        departments = model('erp_base', 'PDept')
        departments.objects.create(old_dept_id='00', old_name='原排除根部门')
        departments.objects.create(old_dept_id='A', old_name='部门工厂', old_is_stop=True)
        dictionary = model('erp_base', 'PFieldValid')
        dictionary.objects.create(old_field_type='BusinessUnit', old_code='A', old_name='另一个主体')
        dictionary.objects.create(old_field_type='ArticleUnit', old_code='U1', old_name='只', old_is_stop=True)
        machine = model('erp_base', 'PMachine').objects.create(old_machine_id='M', old_business_unit_id='A', old_dept_id='BAD')
        mapping = service.correspondence(machine)['rows']
        self.assertEqual(mapping[0]['matches'][0]['label'], '部门工厂')
        self.assertEqual(mapping[1]['matched_count'], 0)
        self.assertEqual([r['value'] for r in service.lookup('B062')['rows']], ['A'])
        self.assertEqual(service.lookup('B049')['rows'][0]['value'], '只')


    def test_machine_keeps_previous_calendar_actions(self):
        from plugins.erp_base.source_resources import RESOURCE_OPTIONS
        from plugins.erp_base.source_foundation_api import SourceMachineFoundationViewSet
        names = {a['key'] for a in RESOURCE_OPTIONS['SourceDyePMachine']['workflow']['actions']}
        self.assertTrue({'lookup_shift', 'resolve_shift'} <= names)
        self.assertTrue(hasattr(SourceMachineFoundationViewSet, 'lookup_shift'))
