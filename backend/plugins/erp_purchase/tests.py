from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base import models as base
from . import models as m


class PurchaseWorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('init_data', verbosity=0)
        cls.root = Users.objects.get(username='superadmin')
        cls.kg = base.Unit.objects.create(code='kg', name='千克', dimension='mass', factor_to_base=1, decimal_places=6)
        cls.material = base.Material.objects.create(code='Y1', name='纱线', kind='yarn', stock_unit=cls.kg)
        cls.other = base.Material.objects.create(code='Y2', name='纱线二', kind='yarn', stock_unit=cls.kg)
        cls.supplier = base.Party.objects.create(code='S1', name='供应商')
        cls.employee = base.Employee.objects.create(code='E1', name='采购员')

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.root)

    def url(self, model, pk=None, action=None):
        return '/api/system/erp_purchase_'+model.lower()+'/' + (str(pk)+'/' if pk is not None else '') + (action+'/' if action else '')

    def request_line(self):
        request = m.PurchaseRequest.objects.create(number='PR1', document_at=timezone.now())
        line = m.PurchaseRequestLine.objects.create(request=request, line_number=1, material=self.material, quantity=100, unit=self.kg)
        return request, line

    def test_confirmed_application_and_order_details_freeze(self):
        request, source = self.request_line()
        response = self.client.post(self.url('PurchaseRequest', request.pk, 'confirm'), {'employee': self.employee.pk}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        response = self.client.patch(self.url('PurchaseRequestLine', source.pk), {'quantity': '200'}, format='json')
        self.assertEqual(response.status_code, 400, response.data)
        order = m.PurchaseOrder.objects.create(number='PO1', document_at=timezone.now(), supplier=self.supplier)
        response = self.client.post(self.url('PurchaseOrderLine'), {'order': order.pk, 'line_number': 1, 'request_line': source.pk,
            'material': self.material.pk, 'quantity': '100', 'unit': self.kg.pk}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        line = response.data['data']['id']
        response = self.client.post(self.url('PurchaseOrder', order.pk, 'confirm'), {}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        response = self.client.patch(self.url('PurchaseOrderLine', line), {'quantity': '200'}, format='json')
        self.assertEqual(response.status_code, 400, response.data)

    def test_draft_or_mismatched_application_cannot_be_adopted(self):
        request, source = self.request_line()
        order = m.PurchaseOrder.objects.create(number='PO1', document_at=timezone.now(), supplier=self.supplier)
        payload = {'order': order.pk, 'line_number': 1, 'request_line': source.pk,
            'material': self.material.pk, 'quantity': '100', 'unit': self.kg.pk}
        self.assertEqual(self.client.post(self.url('PurchaseOrderLine'), payload, format='json').status_code, 400)

        self.client.post(self.url('PurchaseRequest', request.pk, 'confirm'), {'employee': self.employee.pk}, format='json')
        payload['material'] = self.other.pk
        self.assertEqual(self.client.post(self.url('PurchaseOrderLine'), payload, format='json').status_code, 400)

    def test_explicit_request_and_partial_order_close_reopen_keep_quantities(self):
        from . import services
        request,line=self.request_line();services.confirm(request,self.root,self.employee)
        services.close(request,self.root,reason='原申请结束，不生成收货')
        request.refresh_from_db();self.assertEqual(request.status,'closed');self.assertEqual(line.quantity,100)
        services.reopen(request,self.root,reason='继续采购');request.refresh_from_db();self.assertEqual(request.status,'confirmed')
        order=m.PurchaseOrder.objects.create(number='PO-CLOSE',document_at=timezone.now(),supplier=self.supplier,status='confirmed')
        row=m.PurchaseOrderLine.objects.create(order=order,line_number=1,material=self.material,quantity=100,unit=self.kg)
        services.close(order,self.root,reason='双方终止未到货需求');order.refresh_from_db();self.assertEqual(order.status,'closed')
        self.assertEqual(row.quantity,100);self.assertEqual(services.received_quantity(row),0)
        services.reopen(order,self.root,reason='恢复采购');order.refresh_from_db();self.assertEqual(order.status,'confirmed')
