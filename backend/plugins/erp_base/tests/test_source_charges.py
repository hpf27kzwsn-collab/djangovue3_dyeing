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
from plugins.erp_base.source_charge_services import job_charge_total, selected_item_price


class OriginalChargeTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='charges', password='test')
        self.head = self.write('OrderMain', old_sheet_series='O', old_customer_id='C')
        self.color = self.write('OrderColor', source_parent_1=self.head, old_check_no='CHECK', old_prod_id='P')

    def model(self, name, module='erp_sales'):
        return apps.get_model(module + '.SourceDye' + name)

    def write(self, name, **data):
        return services.write(self.model(name), data, actor=self.actor)

    def basic(self, code, name, price, unit='2', tax=False, tax_price=None, date=None):
        head = self.model('CusBasicsPrice').objects.create(old_sheet_series=code, old_customer_id='C', old_is_tax=tax, old_sheet_date=date)
        return self.model('CusExtraCharge').objects.create(old_sheet_series=code, old_detail_no=code, old_pay_service=name,
            old_price=price, old_tax_price=tax_price, old_price_unit=unit, source_parent_1=head)

    def charge(self, code, name):
        return self.write('OrderAtte', source_parent_1=self.color, old_field_type='05', old_atte_code=code, old_atte_value=name)

    def test_tax_price_and_explicit_null_are_adopted_without_fallback(self):
        self.basic('B1', '加捻', 10, tax=True, tax_price=12)
        line = self.charge('1', '加捻')
        self.assertEqual(line.old_price, 12)
        self.basic('B2', '翻松', 20, tax=True, tax_price=None)
        line = self.charge('2', '翻松')
        self.assertIsNone(line.old_price)
        self.color.refresh_from_db(); self.assertEqual(self.color.old_process_price, 12)

    def test_untaxed_priority_latest_date_and_all_same_item_targets(self):
        self.basic('B1', '松筒', 1, date=timezone.make_aware(datetime(2026, 1, 1)))
        self.basic('B2', '松筒', 2, date=timezone.make_aware(datetime(2026, 2, 1)))
        self.basic('B3', '松筒', 30, tax=True, tax_price=33, date=timezone.make_aware(datetime(2026, 3, 1)))
        existing = self.model('OrderAtte').objects.create(old_sheet_series='O', old_check_no='OLD',
            old_field_type='06', old_atte_code='1', old_atte_value='松筒', old_price=99, source_batch=historical_batch())
        line = self.charge('1', '松筒')
        existing.refresh_from_db(); self.assertEqual(line.old_price, 2)
        self.assertEqual(existing.old_price, 2)
        self.assertEqual(existing.source_batch_id, historical_batch().pk)

    def test_latest_unit_controls_whole_sum_and_feel_is_excluded(self):
        self.basic('B1', '包装', 100, unit='4')
        self.basic('B2', '翻松', 5)
        self.basic('B3', '手感处理', 8)
        self.charge('1', '包装')
        self.color.refresh_from_db(); self.assertIsNone(self.color.old_process_price)
        self.charge('2', '翻松')
        self.color.refresh_from_db(); self.assertEqual(self.color.old_process_price, 105)
        self.charge('3', '手感处理')
        self.color.refresh_from_db(); self.assertEqual(self.color.old_process_price, 105)

    def test_unregistered_new_charge_rolls_back_but_historical_record_is_preserved(self):
        with self.assertRaisesMessage(ValidationError, '尚未登记'):
            self.charge('1', '稀有加工')
        self.assertFalse(self.model('OrderAtte').objects.exists())
        old = self.model('OrderAtte').objects.create(old_sheet_series='O', old_check_no='CHECK', old_field_type='05',
            old_atte_code='1', old_atte_value='稀有加工', source_batch=historical_batch(), old_price=-2)
        services.write(type(old), {'old_description': '历史异常仍保存'}, old, self.actor)
        old.refresh_from_db(); self.assertEqual(old.old_price, -2)

    def test_item_price_independent_if_overrides_and_null_matches_empty_product(self):
        model = self.model('QuoteItemPrice')
        specific = model.objects.create(old_detail_no='P1', old_customer_id='C', old_prod_id='P', old_item='加工', old_price=20)
        general = model.objects.create(old_detail_no='P2', old_customer_id='C', old_prod_id=None, old_item='加工', old_price=10)
        public = model.objects.create(old_detail_no='P3', old_customer_id=None, old_prod_id=None, old_item='加工', old_price=5)
        self.assertEqual(selected_item_price('C', 'P', '加工').pk, general.pk)
        general.delete()
        self.assertEqual(selected_item_price('C', 'P', '加工').pk, public.pk)
        public.delete()
        self.assertEqual(selected_item_price('C', 'P', '加工').pk, specific.pk)

    def test_dictionary_registration_keeps_non_numeric_old_codes_and_does_not_duplicate_name(self):
        dictionary = self.model('PFieldValidSub', 'erp_base')
        old = dictionary.objects.create(old_field_type='AtteKind', old_code='05', old_sub_code='旧项', old_sort_value=3,
            old_name='旧项目', source_batch=historical_batch())
        dictionary.objects.create(old_field_type='AtteKind', old_code='05', old_sub_code='9', old_sort_value=4)
        first = self.write('QuoteItemPrice', old_detail_no='Q1', old_item='新加工')
        self.write('QuoteItemPrice', old_detail_no='Q2', old_item='新加工')
        item = dictionary.objects.get(old_name='新加工')
        self.assertEqual(item.old_sub_code, '10'); self.assertEqual(item.old_sort_value, 5)
        self.assertTrue(dictionary.objects.filter(pk=old.pk, source_batch=historical_batch()).exists())

    def test_job_quote_keeps_original_distinct_and_confirmed_gate_not_row_filter(self):
        job = self.model('JobSheet', 'erp_production').objects.create(old_sheet_series='J', old_customer_id='C', old_cust_self_product='P')
        atte = self.model('JobAtte', 'erp_production')
        for code, name in [('1','翻松'), ('2','手感')]:
            atte.objects.create(old_sheet_series='J', old_field_type='05', old_atte_code=code, old_atte_value=name)
        model = self.model('QuoteItemPrice')
        model.objects.create(old_detail_no='A', old_customer_id='C', old_prod_id='P', old_item='翻松', old_price=3, old_is_confirmed=1)
        model.objects.create(old_detail_no='B', old_customer_id='C', old_prod_id='P', old_item='翻松', old_price=7, old_is_confirmed=0)
        self.basic('BASE1', '手感', 2); self.basic('BASE2', '手感', 2)
        self.assertEqual(job_charge_total(job), 12)
        self.assertEqual(job_charge_total(job, without_feel=True), Decimal('0.01'))
        client = APIClient(); client.force_authenticate(self.actor)
        response = client.post(f'/api/system/erp_production_sourcedyejobsheet/{job.pk}/charge_quote/', {}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertIn('不含手感', response.data['msg'])
