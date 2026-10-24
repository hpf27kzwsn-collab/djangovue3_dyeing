from decimal import Decimal
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users, Role, FieldPermission, RoleMenuButtonPermission
from plugins.erp_base import models as base
from plugins.erp_sampling import models as sampling
from . import models as m


class CommercialOrderTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('init_data', verbosity=0)
        cls.root = Users.objects.get(username='superadmin')
        cls.kg = base.Unit.objects.create(code='kg', name='千克', dimension='mass', factor_to_base=1, decimal_places=6)
        cls.party = base.Party.objects.create(code='C1', name='客户一')
        cls.other = base.Party.objects.create(code='C2', name='客户二')
        cls.material = base.Material.objects.create(code='Y1', name='纱线', kind='yarn', stock_unit=cls.kg)
        cls.employee = base.Employee.objects.create(code='E1', name='员工一')

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.root)

    def url(self, model, pk=None, action=None):
        return '/api/system/erp_sales_' + model.lower() + '/' + (str(pk)+'/' if pk is not None else '') + (action+'/' if action else '')

    def create(self, model, data, expected=200):
        response = self.client.post(self.url(model), data, format='json')
        self.assertEqual(response.status_code, expected, response.data)
        return response.data['data']

    def post(self, model, pk, action, data=None, expected=200):
        response = self.client.post(self.url(model, pk, action), {} if data is None else data, format='json')
        self.assertEqual(response.status_code, expected, response.data)
        return response

    def order(self):
        order = self.create('SalesOrder', {'number': 'SO1', 'document_at': timezone.now().isoformat(), 'customer': self.party.pk})
        return order['id']

    def price(self):
        price = self.create('CommercialPrice', {'number': 'P1', 'kind': 'agreed', 'customer': self.party.pk})
        line = self.create('CommercialPriceLine', {'price_document': price['id'], 'line_number': 1,
            'material': self.material.pk, 'unit_price': '1.234567', 'unit': self.kg.pk,
            'confirmed_base_price': None, 'additional_price': '0'})
        self.post('CommercialPrice', price['id'], 'confirm')
        return price['id'], line['id']

    def order_line(self, order, **extra):
        return self.create('SalesOrderLine', {'order': order, 'line_number': 1, 'material': self.material.pk,
            'ordered_quantity': '100', 'ordered_unit': self.kg.pk, **extra})

    def test_price_adoption_preserves_six_decimal_places_and_null_components(self):
        price, source = self.price()
        order = self.order()
        line = self.order_line(order, price_source=source)
        self.assertEqual(Decimal(line['adopted_price_snapshot']), Decimal('1.234567'))
        self.assertIsNone(line['unit_price'])
        self.assertIsNone(m.CommercialPriceLine.objects.get(pk=source).confirmed_base_price)
        self.assertIsNone(m.CommercialPriceLine.objects.get(pk=source).calculated_unit_price)
        self.post('SalesOrder', order, 'confirm', {'employee': self.employee.pk})
        self.assertEqual(m.SalesOrder.objects.get(pk=order).status, 'confirmed')
        self.assertEqual(base.BusinessAction.objects.filter(action='confirm').count(), 2)
        response = self.client.patch(self.url('CommercialPriceLine', source), {'unit_price': '2'}, format='json')
        self.assertEqual(response.status_code, 400, response.data)
        response = self.client.patch(self.url('SalesOrderLine', line['id']), {'ordered_quantity': '200'}, format='json')
        self.assertEqual(response.status_code, 400, response.data)

    def test_confirmation_requires_real_price_source_or_manual_reason(self):
        order = self.order()
        line = self.order_line(order)
        self.post('SalesOrder', order, 'confirm', {'employee': self.employee.pk}, 400)
        self.assertEqual(m.SalesOrder.objects.get(pk=order).status, 'draft')
        response = self.client.patch(self.url('SalesOrderLine', line['id']), {'unit_price': '0', 'price_unit': self.kg.pk, 'manual_price_reason': '免费返修'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.post('SalesOrder', order, 'confirm', {'employee': self.employee.pk})

    def test_price_customer_mismatch_rejected(self):
        _, source = self.price()
        order = self.create('SalesOrder', {'number': 'SO2', 'document_at': timezone.now().isoformat(), 'customer': self.other.pk})
        self.create('SalesOrderLine', {'order': order['id'], 'line_number': 1, 'material': self.material.pk,
            'ordered_quantity': '100', 'ordered_unit': self.kg.pk, 'price_source': source}, 400)

    def test_atomic_document_rolls_back_head_and_earlier_lines(self):
        order = self.order()
        payload = {'head': {'brand_name': '新品牌'}, 'children': {'erp_sales_salesorderline': {'upsert': [
            {'line_number': 1, 'material': self.material.pk, 'ordered_quantity': '100', 'ordered_unit': self.kg.pk},
            {'line_number': 2, 'material': self.material.pk, 'ordered_quantity': '-1', 'ordered_unit': self.kg.pk}], 'delete': []}}}
        self.post('SalesOrder', order, 'save_document', payload, 400)
        self.assertEqual(m.SalesOrderLine.objects.filter(order_id=order).count(), 0)
        self.assertIsNone(m.SalesOrder.objects.get(pk=order).brand_name)
        payload['children']['erp_sales_salesorderline']['upsert'][1]['ordered_quantity'] = '50'
        self.post('SalesOrder', order, 'save_document', payload)
        self.assertEqual(m.SalesOrderLine.objects.filter(order_id=order).count(), 2)

    def test_order_change_saves_before_values_without_changing_original_order_confirmation(self):
        order = self.order()
        line = self.order_line(order, unit_price='1.25', price_unit=self.kg.pk, manual_price_reason='客户协议价')
        self.post('SalesOrder', order, 'confirm', {'employee': self.employee.pk})
        original_date = m.SalesOrder.objects.get(pk=order).confirmed_at
        change = self.create('SalesOrderChange', {'order': order, 'change_number': 'CH1', 'requested_at': timezone.now().isoformat(), 'reason': '客户增量'})
        detail = self.create('SalesOrderChangeLine', {'change': change['id'], 'order_line': line['id'], 'new_quantity': '120'})
        self.post('SalesOrderChange', change['id'], 'confirm', {'employee': self.employee.pk})
        detail = m.SalesOrderChangeLine.objects.get(pk=detail['id'])
        self.assertEqual(Decimal(detail.before_values['ordered_quantity']), 100)
        self.assertEqual(detail.order_line.ordered_quantity, 120)
        self.assertEqual(m.SalesOrder.objects.get(pk=order).confirmed_at, original_date)

    def test_owned_fields_and_foreign_detail_document_are_rejected(self):
        self.create('SalesOrder', {'number': 'SO1', 'document_at': timezone.now().isoformat(), 'customer': self.party.pk, 'status': 'completed'}, 400)
        order = self.order()
        self.post('SalesOrder', order, 'save_document', {'head': {}, 'children': {'erp_sampling_sampleline': {'upsert': [], 'delete': []}}}, 400)
        self.post('SalesOrder', order, 'confirm', {'employee': self.employee.pk, 'unknown': 'x'}, 400)

    def test_business_role_initialization_preserves_custom_permissions(self):
        role = Role.objects.get(key='erp_business_manager')
        grant = RoleMenuButtonPermission.objects.filter(role=role, menu_button__value='erp_sales_salesorder:confirm-post').get()
        grant.delete()
        column = FieldPermission.objects.filter(role=role, field__model='erp_sales.SalesOrderLine',field__field_name='manual_price_reason').get()
        column.is_update = False
        column.save()
        call_command('init_data', verbosity=0)
        self.assertFalse(RoleMenuButtonPermission.objects.filter(role=role, menu_button__value='erp_sales_salesorder:confirm-post').exists())
        column.refresh_from_db()
        self.assertFalse(column.is_update)
