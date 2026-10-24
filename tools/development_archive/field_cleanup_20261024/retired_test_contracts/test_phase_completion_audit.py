"""第一、二阶段入口复核：实际授权、原输出参数、完整原字段录入。"""
from datetime import datetime
from decimal import Decimal
from django.apps import apps
from django.test import SimpleTestCase, TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from core.resources import resource_options
from system.actions import resource_actions, workflow_actions
from system.catalog import ENTITIES
from system.models import Users, Role, Menu, MenuButton, RoleMenuButtonPermission
from system.views import view_for


class WorkflowContractTests(SimpleTestCase):
    def test_every_page_action_uses_registered_permission_and_keeps_configuration(self):
        for entity, model in ENTITIES.items():
            options = resource_options(model)
            if 'workflow' not in options:
                continue
            view = view_for(entity, model)
            registered = {entity+':'+key: (verb, api) for key, _, verb, api in resource_actions(entity, view)}
            workflow = workflow_actions(entity, view, options['workflow'])
            for original, action in zip(options['workflow'].get('actions', []), workflow['actions']):
                with self.subTest(entity=entity, action=action['key']):
                    self.assertNotIn('permission', original)
                    verb, api = registered[action['permission']]
                    self.assertEqual(verb, 1)
                    self.assertTrue(api.endswith('/'+action['key']+'/'))


class PhaseCompletionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.actor = Users.objects.create_superuser(username='phase-audit', password='test')
        self.client.force_authenticate(self.actor)

    def test_existing_foundation_grant_can_use_displayed_action(self):
        entity = 'erp_base_sourcedyepfieldvalid'
        actor = Users.objects.create_user(username='foundation-operator')
        role = Role.objects.create(key='foundation-audit', name='基础查询')
        actor.role.add(role)
        menu = Menu.objects.create(component_name=entity, name='基础资料', resource=entity)
        button = MenuButton.objects.create(menu=menu, name='换算', value=entity+':convert-unit-post',
            method=1, api='/api/system/'+entity+'/convert_unit/')
        RoleMenuButtonPermission.objects.create(role=role, menu_button=button, data_range=3)
        self.client.force_authenticate(actor)
        metadata = self.client.get('/api/meta/'+entity+'/')
        self.assertEqual(metadata.status_code, 200)
        action = next(a for a in metadata.data['data']['workflow']['actions'] if a['key']=='convert_unit')
        self.assertEqual(action['permission'], button.value)
        response = self.client.post(button.api, {'source_unit':1, 'destination_unit':3, 'quantity':'-2'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(Decimal(str(response.data['data']['rows'][0]['result'])), Decimal('-4.41'))
        self.assertEqual(self.client.post('/api/system/'+entity+'/calendar_days/',
            {'start':'2024-01-01','end':'2024-01-02'}, format='json').status_code, 403)

    def test_period_output_parameters_survive_no_match_without_changing_functions(self):
        response = self.client.post('/api/system/erp_base_sourcedyesaccmonth/original_period/',
            {'value':None,'begin':'2024-01-01T00:00:00+08:00','end':'2024-02-01T00:00:00+08:00'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        row = response.data['data']['rows'][0]
        self.assertIsNone(row['GetAccBeginDate'])
        self.assertIsNone(row['GetAccEndDate'])
        self.assertIn('2024-01-01', str(row['Sp_GetAccDate_BeginDate']))
        self.assertIn('2024-02-01', str(row['Sp_GetAccDate_EndDate']))

    def test_sample_create_endpoint_keeps_duplicate_original_keys_and_all_49_fields(self):
        from plugins.erp_base.source_phase2_sampling import ADD_FIELDS
        model = apps.get_model('erp_sampling', 'SourceDyeDyeDipsRecord')
        payload = {model.SOURCE_FIELDS[name]: None for name in ADD_FIELDS}
        payload.update(old_sheet_series='DUPLICATE', old_sheet_no='DUPLICATE', old_weight='-1.25', old_cost='-2.50')
        for _ in range(2):
            response = self.client.post('/api/system/erp_sampling_sourcedyedyedipsrecord/', payload, format='json')
            self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(model.objects.count(), 2)
        for item in model.objects.all():
            for original in ADD_FIELDS:
                field = model.SOURCE_FIELDS[original]
                with self.subTest(record=item.pk, field=original):
                    expected = payload[field]
                    if original in ['Weight','Cost']:
                        expected = Decimal(expected)
                    self.assertEqual(getattr(item,field), expected)
        self.assertNotIn('legacy_id', {f.name for f in model._meta.fields})
