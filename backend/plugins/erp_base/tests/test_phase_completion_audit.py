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
                    if action['key'] in ['business_query','machine_board']:
                        self.assertEqual((verb,action['permission']),(0,entity+':list'))
                    else:
                        self.assertEqual(verb,1)
                        self.assertTrue(api.endswith('/'+action['key']+'/'))


class PhaseCompletionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.actor = Users.objects.create_superuser(username='phase-audit', password='test')
        self.client.force_authenticate(self.actor)



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
