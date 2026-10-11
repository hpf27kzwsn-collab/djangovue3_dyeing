from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base import models as base
from . import models as m


class SamplingWorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('init_data', verbosity=0)
        cls.root = Users.objects.get(username='superadmin')
        cls.kg = base.Unit.objects.create(code='kg', name='千克', dimension='mass', factor_to_base=1, decimal_places=6)
        cls.party = base.Party.objects.create(code='C1', name='客户')
        cls.material = base.Material.objects.create(code='Y1', name='纱线', kind='yarn', stock_unit=cls.kg)
        cls.chemical = base.Material.objects.create(code='D1', name='染料', kind='chemical', stock_unit=cls.kg)
        cls.employee = base.Employee.objects.create(code='E1', name='打样员')

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.root)

    def url(self, model, pk=None, action=None):
        return '/api/system/erp_sampling_' + model.lower() + '/' + (str(pk)+'/' if pk is not None else '') + (action+'/' if action else '')

    def create(self, model, data, expected=200):
        response = self.client.post(self.url(model), data, format='json')
        self.assertEqual(response.status_code, expected, response.data)
        return response.data['data']

    def post(self, model, pk, action, data, expected=200):
        response = self.client.post(self.url(model, pk, action), data, format='json')
        self.assertEqual(response.status_code, expected, response.data)
        return response.data['data']

    def recipe(self):
        recipe = self.create('Recipe', {'code': 'R1', 'name': '配方', 'purpose': 'trial', 'customer': self.party.pk, 'material': self.material.pk})
        version = self.create('RecipeVersion', {'recipe': recipe['id'], 'version': 1})
        stage = self.create('RecipeStage', {'version': version['id'], 'sequence': 1})
        ingredient = self.create('RecipeIngredient', {'stage': stage['id'], 'sequence': 1, 'material': self.chemical.pk, 'dosage': '1.250000', 'dosage_basis': 'owf_percent'})
        return version, stage, ingredient

    def request_line(self):
        request = self.create('SampleRequest', {'number': 'S1', 'document_at': timezone.now().isoformat(), 'customer': self.party.pk})
        line = self.create('SampleLine', {'request': request['id'], 'line_number': 1, 'material': self.material.pk})
        self.post('SampleRequest', request['id'], 'receive', {'at': timezone.now().isoformat()})
        self.post('SampleLine', line['id'], 'assign', {'employee': self.employee.pk})
        return request, line

    def trial(self, line, version, number):
        trial = self.create('SampleTrial', {'sample_line': line['id'], 'trial_number': number, 'recipe_version': version['id'], 'operator': self.employee.pk})
        self.post('SampleTrial', trial['id'], 'start', {'at': timezone.now().isoformat()})
        self.post('SampleTrial', trial['id'], 'complete', {'at': timezone.now().isoformat(), 'result_text': '实测记录'})
        return trial

    def test_version_freeze_clone_and_original_detail_precision(self):
        version, stage, ingredient = self.recipe()
        self.post('RecipeVersion', version['id'], 'approve', {'employee': self.employee.pk})
        response = self.client.patch(self.url('RecipeIngredient', ingredient['id']), {'dosage': '2'}, format='json')
        self.assertEqual(response.status_code, 400, response.data)
        clone = self.post('RecipeVersion', version['id'], 'clone', {})
        self.assertEqual(clone['version'], 2)
        self.assertEqual(clone['status'], 'draft')
        copied = m.RecipeIngredient.objects.get(stage__version_id=clone['id'])
        self.assertEqual(copied.dosage, m.RecipeIngredient.objects.get(pk=ingredient['id']).dosage)
        self.assertIsNone(copied.legacy_id)
        response = self.client.delete(self.url('RecipeStage', stage['id']))
        self.assertEqual(response.status_code, 400, response.data)

    def test_multiple_trials_rejection_then_confirmation_preserves_history(self):
        version, _, _ = self.recipe()
        self.post('RecipeVersion', version['id'], 'approve', {'employee': self.employee.pk})
        request, line = self.request_line()
        first = self.trial(line, version, 1)
        confirmation = self.create('SampleConfirmation', {'sample_line': line['id'], 'trial': first['id']})
        self.post('SampleConfirmation', confirmation['id'], 'send', {'at': timezone.now().isoformat()})
        self.post('SampleConfirmation', confirmation['id'], 'reply', {'result': 'rejected', 'at': timezone.now().isoformat(), 'customer_reply': '偏深'})
        second = self.trial(line, version, 2)
        color = base.ColorStandard.objects.create(code='CL1', color_number='001', customer=self.party, material=self.material)
        accepted = self.create('SampleConfirmation', {'sample_line': line['id'], 'trial': second['id'], 'confirmed_color': color.pk, 'confirmed_recipe': version['id']})
        self.post('SampleConfirmation', accepted['id'], 'send', {'at': timezone.now().isoformat()})
        self.post('SampleConfirmation', accepted['id'], 'reply', {'result': 'accepted', 'at': timezone.now().isoformat(), 'customer_reply': '确认'})
        self.assertEqual(m.SampleTrial.objects.filter(sample_line_id=line['id']).count(), 2)
        self.assertEqual(m.SampleConfirmation.objects.get(pk=confirmation['id']).result, 'rejected')
        self.assertEqual(m.SampleRequest.objects.get(pk=request['id']).status, 'confirmed')
        color.refresh_from_db()
        self.assertEqual(color.source_sample_id, line['id'])

    def test_cannot_complete_before_start_or_confirm_unfinished_trial(self):
        version, _, _ = self.recipe()
        _, line = self.request_line()
        trial = self.create('SampleTrial', {'sample_line': line['id'], 'trial_number': 1, 'recipe_version': version['id'], 'operator': self.employee.pk})
        self.post('SampleTrial', trial['id'], 'complete', {'at': timezone.now().isoformat(), 'result_text': '结果'}, 400)
        confirmation = self.create('SampleConfirmation', {'sample_line': line['id'], 'trial': trial['id']})
        self.post('SampleConfirmation', confirmation['id'], 'send', {'at': timezone.now().isoformat()}, 400)

    def test_receive_freezes_sample_header_and_cannot_reparent_trial(self):
        version, _, _ = self.recipe()
        request, line = self.request_line()
        response = self.client.patch(self.url('SampleRequest', request['id']), {'customer': self.party.pk}, format='json')
        self.assertEqual(response.status_code, 400, response.data)
        self.create('SampleTrial', {'sample_line': line['id'], 'trial_number': 1, 'recipe_version': version['id'], 'operator': self.employee.pk, 'status': 'completed'}, 400)
