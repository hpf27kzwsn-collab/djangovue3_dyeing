from decimal import Decimal
from datetime import timedelta
from django.apps import apps
from django.test import TestCase, SimpleTestCase
from django.core.management import call_command
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.source_documents import SourceRecord
from plugins.erp_warehouse.source_models import SourceDyeRecordYield
from plugins.erp_production.source_models import SourceDyeWProcess
from django.db import migrations, models
from django.db.migrations.state import ProjectState
from plugins.erp_base.source_migrations import CreateSourceModels, AddSourceIndexes
from plugins.erp_sampling.source_models import SourceDyeColorCardDetail
from system.models import Role, Menu, MenuField, FieldPermission, RoleMenuButtonPermission
from plugins.erp_base.source_models import SourceDyeSFlow, SourceDyeSFlowStep, SourceDyeSFlowStepEmp
from plugins.erp_base.legacy_models import LegacyImportBatch
from plugins.erp_quality.source_models import SourceDyeWDefectPenalty

class SourceMigrationStateTests(SimpleTestCase):

    def test_batch_has_the_same_functional_index_state_as_standard_operations(self):
        from django.db.models.functions import Upper, RTrim
        initial = migrations.CreateModel(name='SourceOne', fields=[('id', models.BigAutoField(primary_key=True)), ('original_code', models.CharField(max_length=20))])
        standard = ProjectState()
        initial.state_forwards('migration_test', standard)
        batched = standard.clone()
        batched.apps
        operations = [migrations.AddIndex(model_name='sourceone', index=models.Index(Upper(RTrim('original_code')), name='test_ci_source_code'))]
        for operation in operations:
            operation.state_forwards('migration_test', standard)
        AddSourceIndexes(operations).state_forwards('migration_test', batched)
        self.assertEqual(standard, batched)

    def test_batch_has_the_same_model_state_as_standard_create_operations(self):
        operations = [migrations.CreateModel(name=name, fields=[('id', models.BigAutoField(primary_key=True)), ('original_amount', models.DecimalField(max_digits=38, decimal_places=8, null=True))]) for name in ['SourceOne', 'SourceTwo']]
        standard = ProjectState()
        batched = ProjectState()
        for operation in operations:
            operation.state_forwards('migration_test', standard)
        batched.apps
        batch = CreateSourceModels(operations)
        batch.state_forwards('migration_test', batched)
        self.assertEqual(standard, batched)
        self.assertEqual(len(list(batched.apps.get_models())), 2)

class FullSourceModelTests(TestCase):


    def test_defect_responsibility_quantities_and_penalty_values_are_business_facts(self):
        item = SourceDyeWDefectPenalty.objects.create(old_sheet_series='D-1', old_wdefect_no='DEF-1', old_row_no=1, old_emp_id='OLD-E', old_rolls=Decimal('-6'), old_qty=Decimal('1.5'), old_penalty=Decimal('-100'), old_reward=None)
        item.refresh_from_db()
        self.assertEqual(item.old_rolls, Decimal('-6'))
        self.assertEqual(item.old_qty, Decimal('1.5'))
        self.assertEqual(item.old_penalty, Decimal('-100'))
        self.assertIsNone(item.old_reward)
        self.assertEqual(item._meta.app_label, 'erp_quality')


    def test_original_binary_picture_is_editable_and_round_trips_as_base64(self):
        actor = Users.objects.create_superuser(username='source-binary', password='test-password')
        client = APIClient()
        client.force_authenticate(actor)
        response = client.post('/api/system/erp_sampling_sourcedyecolorcarddetail/', {'old_sheet_series': 'BINARY-1', 'old_work_sheet_kind': 0, 'old_data_table_name': 'ColorCard', 'old_process_id': 'GX03', 'old_photo': 'AP+AQQ=='}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        item = SourceDyeColorCardDetail.objects.get(pk=response.data['data']['id'])
        self.assertEqual(bytes(item.old_photo), b'\x00\xff\x80A')
        self.assertEqual(response.data['data']['old_photo'], 'AP+AQQ==')

    def test_every_business_model_keeps_original_fields_without_extra_legacy_id(self):
        models = [model for model in apps.get_models() if model._meta.app_label.startswith('erp_')]
        originals = [model for model in models if issubclass(model, SourceRecord)]
        self.assertEqual(len(originals), 655)
        self.assertEqual(sum((len(model.SOURCE_FIELDS) for model in originals)), 12606)
        for model in models:
            self.assertNotIn('legacy_id', {f.name for f in model._meta.fields})
        self.assertNotIn('QualityInspection', [m.__name__ for m in apps.get_models()])

    def test_two_packages_with_same_barcode_and_negative_pieces_are_both_stored(self):
        one = SourceDyeRecordYield(old_guid='SOURCE-1', old_job_sheet_no='CARD-1', old_check_no='LINE-1', old_roll_no='002', old_bar_code='SHARED', old_rolls=Decimal('-6'))
        two = SourceDyeRecordYield(old_guid='SOURCE-2', old_job_sheet_no='CARD-2', old_check_no='LINE-2', old_roll_no='003', old_bar_code='SHARED', old_rolls=Decimal('0.1'))
        one.full_clean()
        one.save()
        two.full_clean()
        two.save()
        self.assertEqual(SourceDyeRecordYield.objects.filter(old_bar_code='SHARED').count(), 2)
        self.assertEqual(SourceDyeRecordYield.objects.get(pk=one.pk).old_rolls, Decimal('-6'))
        self.assertEqual(SourceDyeRecordYield.objects.get(pk=two.pk).old_rolls, Decimal('0.1'))

    def test_reversed_source_times_and_unresolved_original_codes_are_preserved(self):
        now = timezone.now()
        item = SourceDyeWProcess(old_wprocess_no='SOURCE-TIME', old_job_sheet_no='NO-PARENT', old_start_time=now, old_end_time=now - timedelta(seconds=11), old_work_qty=Decimal('0'))
        item.full_clean()
        item.save()
        item.refresh_from_db()
        self.assertLess(item.old_end_time, item.old_start_time)
        self.assertEqual(item.old_work_qty, 0)
        self.assertEqual(item.old_job_sheet_no, 'NO-PARENT')

    def test_source_document_approve_keeps_original_state(self):
        actor = Users.objects.create_superuser(username='source-operator', password='test-password')
        client = APIClient()
        client.force_authenticate(actor)
        entity = 'erp_production_sourcedyewprocess'
        response = client.post('/api/system/' + entity + '/', {'old_wprocess_no': 'API-SOURCE', 'old_job_sheet_no': 'NO-PARENT', 'old_status': '7'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        pk = response.data['data']['id']
        self.assertIsNone(response.data['data']['review_state'])
        for action, stage in [('approve', 'approved')]:
            response = client.post(f'/api/system/{entity}/{pk}/{action}/', {}, format='json')
            self.assertEqual(response.status_code, 200, response.data)
            self.assertEqual(response.data['data']['review_state'], stage)
            self.assertEqual(response.data['data']['old_status'], '7')
        response = client.patch(f'/api/system/{entity}/{pk}/', {'old_work_qty': '1'}, format='json')
        self.assertEqual(response.status_code, 400)
        response = client.post(f'/api/system/{entity}/{pk}/reopen/', {'reason': '明确修改'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['data']['review_state'], 'unreviewed')

class OriginalModelInitializationTests(TestCase):

    def test_reinitialization_keeps_custom_titles_and_existing_role_permissions(self):
        call_command('init_data', verbosity=0)
        quantity_menus = ['erp_quality_qualityquantitybatch', 'erp_quality_qualityquantitysource']
        quantity_fields = FieldPermission.objects.filter(role__key='erp_business_manager', field__menu__component_name__in=quantity_menus)
        self.assertTrue(quantity_fields.exists())
        self.assertTrue(quantity_fields.filter(is_create=True).exists())
        self.assertTrue(quantity_fields.filter(is_update=True).exists())
        self.assertTrue(RoleMenuButtonPermission.objects.filter(role__key='erp_business_manager', menu_button__menu__component_name__in=quantity_menus).exclude(menu_button__method=0).exists())
        menu = Menu.objects.get(component_name='erp_production_sourcedyewprocess')
        column = MenuField.objects.get(menu=menu, field_name='old_work_qty')
        column.title = '现场数量名称'
        column.save(update_fields=['title'])
        role = Role.objects.get(key='erp_business_manager')
        permission = FieldPermission.objects.get(role=role, field=column)
        permission.is_update = False
        permission.save(update_fields=['is_update'])
        grant = RoleMenuButtonPermission.objects.filter(role=role, menu_button__menu=menu).first()
        button_id = grant.menu_button_id
        grant.delete()
        call_command('init_data', verbosity=0)
        column.refresh_from_db()
        permission.refresh_from_db()
        self.assertEqual(column.title, '现场数量名称')
        self.assertFalse(permission.is_update)
        self.assertFalse(RoleMenuButtonPermission.objects.filter(role=role, menu_button_id=button_id).exists())
