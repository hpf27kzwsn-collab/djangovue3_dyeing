from datetime import timedelta
from decimal import Decimal
from django.test import TestCase
from system.models import Users,Role,RoleMenuButtonPermission,FieldPermission,Dept,MenuButton,MenuField
from plugins.erp_warehouse import test_packing as fixtures
from plugins.erp_production import models as production


class BusinessReportTests(TestCase):
    setUpTestData=fixtures.PackingDeliveryTests.__dict__['setUpTestData']
    setUp=fixtures.PackingDeliveryTests.setUp
    card=fixtures.PackingDeliveryTests.card
    allocate=fixtures.PackingDeliveryTests.allocate
    output=fixtures.PackingDeliveryTests.output
    prepare=fixtures.PackingDeliveryTests.prepare
    packed=fixtures.PackingDeliveryTests.packed
    receive=fixtures.PackingDeliveryTests.receive
    delivered=fixtures.PackingDeliveryTests.delivered

    def test_order_progress_keeps_demand_package_and_delivery_separate(self):
        values,delivery,line,source=self.delivered()
        response=self.client.get('/api/plugins/erp/reports/orders/')
        self.assertEqual(response.status_code,200,response.data)
        row=response.data['data']['rows'][0]
        self.assertEqual(Decimal(row['ordered']),100);self.assertEqual(Decimal(row['packed']),80)
        self.assertEqual(Decimal(row['delivered']),80);self.assertEqual(Decimal(row['remaining']),20)
        for report in ['production','materials','quality','stock','packages','prices','sampling','purchases','schedules','rework','lineage']:
            response=self.client.get('/api/plugins/erp/reports/'+report+'/')
            self.assertEqual(response.status_code,200,response.data)
        response=self.client.get('/api/plugins/erp/reports/orders/export/')
        self.assertEqual(response.status_code,200);self.assertTrue(response.content.startswith(b'\xef\xbb\xbf'))
        self.assertIn('SO',response.content.decode('utf-8-sig'))

    def test_report_respects_root_department_and_required_field_permissions(self):
        self.prepare()
        department=Dept.objects.create(name='报表范围',key='REP')
        other=Dept.objects.create(name='其他范围',key='OTHER')
        production.WorkCard.objects.filter(number='WC').update(dept_belong=department)
        card=self.card(number='HIDDEN');card.dept_belong=other;card.save()
        user=Users.objects.create_user(username='reporter',password='test-password',dept=department)
        role=Role.objects.get(key='erp_reports_viewer');user.role.add(role)
        button=MenuButton.objects.get(value='erp_production_workcard:list')
        RoleMenuButtonPermission.objects.filter(role=role,menu_button=button).update(data_range=2)
        self.client.force_authenticate(user)
        response=self.client.get('/api/plugins/erp/reports/production/')
        self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(response.data['data']['count'],1)
        self.assertTrue(all(row['number']=='WC' for row in response.data['data']['rows']))
        field=MenuField.objects.get(model='erp_production.OperationExecution',field_name='output_mass_kg')
        FieldPermission.objects.filter(role=role,field=field).update(is_query=False)
        response=self.client.get('/api/plugins/erp/reports/production/')
        self.assertEqual(response.status_code,403,response.data)
        execution=production.OperationExecution.objects.first()
        response=self.client.get(f'/api/system/erp_production_operationexecution/{execution.pk}/')
        self.assertEqual(response.status_code,200,response.data)
        self.assertNotIn('output_mass_kg',response.data['data'])
        self.assertNotIn('output_mass_kg',response.data['data']['effective_facts'])
