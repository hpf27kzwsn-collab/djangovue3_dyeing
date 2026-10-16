from datetime import datetime
from decimal import Decimal
from django.apps import apps
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from system.models import Users
from plugins.erp_base import source_services as services


class OriginalSamplingLinksTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='sampling-links', password='test')

    def model(self, table, module='erp_sampling'):
        return apps.get_model(module + '.SourceDye' + table)

    def write(self, table, **data):
        return services.write(self.model(table), data, actor=self.actor)

    def test_trial_version_updates_existing_color_and_delete_returns_latest_remaining(self):
        master = self.model('PColorNum', 'erp_base').objects.create(old_color_no='COLOR', old_color_num='C1', legacy_id='old-color')
        previous = self.model('DyeRecipe').objects.create(old_sheet_series='R0', old_sheet_kind=1,
            old_color_num='C1', old_color_version='V0', old_sheet_date=timezone.make_aware(datetime(2026, 1, 1)), legacy_id='old-recipe')
        current = self.write('DyeRecipe', _entry='TrialDyeRecipe', old_sheet_series='R1', old_sheet_kind=1,
            old_color_num='c1 ', old_color_version='V1', old_sheet_date=timezone.make_aware(datetime(2026, 2, 1)))
        master.refresh_from_db(); self.assertEqual(master.old_color_num_no, 'V1')
        self.assertEqual(master.legacy_id, 'old-color')
        services.delete_documents(type(current).objects.filter(pk=current.pk), self.actor)
        master.refresh_from_db(); self.assertEqual(master.old_color_num_no, 'V0')
        self.assertEqual(timezone.localtime(master.old_oktime).month, 1)
        self.assertTrue(type(previous).objects.filter(pk=previous.pk).exists())

    def test_last_trial_delete_uses_original_blank_version_and_1900_date(self):
        master = self.model('PColorNum', 'erp_base').objects.create(old_color_no='C', old_color_num='C1')
        recipe = self.write('DyeRecipe', _entry='TrialDyeRecipe', old_sheet_series='R1', old_sheet_kind=1,
                            old_color_num='C1', old_color_version='V1')
        services.delete_documents(type(recipe).objects.filter(pk=recipe.pk), self.actor)
        master.refresh_from_db(); self.assertEqual(master.old_color_num_no, '')
        self.assertEqual(timezone.localtime(master.old_oktime).year, 1900)

    def test_cost_sums_actual_phase_detail_amounts_including_negative_and_null(self):
        recipe = self.write('DyeRecipe', old_sheet_series='R1')
        phase = self.write('DyeRecipePhase', source_parent_1=recipe, old_phase_no='01', old_phase_id='P1')
        self.write('DyeRecipeDetail', source_parent_1=phase, old_stuff_id='S1', old_stuff_no='01', old_amount=Decimal('10.12'))
        negative = self.write('DyeRecipeDetail', source_parent_1=phase, old_stuff_id='S2', old_stuff_no='02', old_amount=Decimal('-2.12'))
        self.write('DyeRecipeDetail', source_parent_1=phase, old_stuff_id='S3', old_stuff_no='03', old_amount=None)
        recipe.refresh_from_db(); self.assertEqual(recipe.old_cost, 8)
        services.delete(type(negative).objects.filter(pk=negative.pk), self.actor)
        recipe.refresh_from_db(); self.assertEqual(recipe.old_cost, Decimal('10.12'))

    def test_phase_duplicates_follow_old_rule_and_null_phase_ids_are_not_equal(self):
        recipe = self.write('DyeRecipe', old_sheet_series='R1')
        first = self.write('DyeRecipePhase', source_parent_1=recipe, old_phase_no='01', old_phase_id='P1', old_remarks="剂'量'")
        self.assertEqual(first.old_remarks, '剂’量’')
        with self.assertRaisesMessage(ValidationError, '染程不能重复'):
            self.write('DyeRecipePhase', source_parent_1=recipe, old_phase_no='02', old_phase_id='p1 ')
        for number in ['03', '04']:
            self.write('DyeRecipePhase', source_parent_1=recipe, old_phase_no=number, old_phase_id=None)
        self.assertEqual(self.model('DyeRecipePhase').objects.count(), 3)

    def test_disabled_material_rule_does_not_reject_or_rewrite_imported_recipe(self):
        self.model('PStuff', 'erp_base').objects.create(old_stuff_id='STOP', old_status=1)
        recipe = self.write('DyeRecipe', old_sheet_series='R1')
        phase = self.write('DyeRecipePhase', source_parent_1=recipe, old_phase_no='01')
        with self.assertRaisesMessage(ValidationError, '已停用'):
            self.write('DyeRecipeDetail', source_parent_1=phase, old_stuff_id='stop ', old_stuff_no='01')
        old = self.model('DyeRecipeDetail').objects.create(old_sheet_series='OLD', old_phase_no='01',
            old_stuff_no='01', old_stuff_id='STOP', legacy_id='original-stopped-stuff')
        services.write(type(old), {'old_remarks': '历史说明'}, old, self.actor)
        old.refresh_from_db(); self.assertEqual(old.old_stuff_id, 'STOP')

    def test_creating_recipe_keeps_orphan_phases_and_details(self):
        phase = self.model('DyeRecipePhase').objects.create(old_sheet_series='MISSING', old_phase_no='01', legacy_id='orphan-phase')
        detail = self.model('DyeRecipeDetail').objects.create(old_sheet_series='MISSING', old_phase_no='01',
            old_stuff_no='01', old_stuff_id='S1', legacy_id='orphan-detail')
        self.write('DyeRecipe', old_sheet_series='NEW')
        self.assertTrue(type(phase).objects.filter(pk=phase.pk).exists())
        self.assertTrue(type(detail).objects.filter(pk=detail.pk).exists())

    def test_sample_color_delete_keeps_referenced_sample_and_historical_master(self):
        color = self.write('DyeLabColor', old_sheet_series='LAB', old_color_no='C', old_color_num='A1')
        master = self.model('PColorNum', 'erp_base').objects.create(old_sheet_series='LAB', old_color_no='C', legacy_id='old-color')
        trial = self.model('DyeDipsRecord').objects.create(old_sheet_series='DIPS', old_color_no='C')
        with self.assertRaisesMessage(ValidationError, '已有打样配方'):
            services.delete(type(color).objects.filter(pk=color.pk), self.actor)
        trial.delete()
        services.delete(type(color).objects.filter(pk=color.pk), self.actor)
        self.assertTrue(type(master).objects.filter(pk=master.pk).exists())

    def test_dips_phase_and_material_rules_and_historical_duplicate_preservation(self):
        head = self.write('DyeDipsRecord', old_sheet_series='D1')
        self.write('DyeDipsRecordPhase', source_parent_1=head, old_phase_no=1, old_phase_id='P1')
        with self.assertRaisesMessage(ValidationError, '染程不能重复'):
            self.write('DyeDipsRecordPhase', source_parent_1=head, old_phase_no=2, old_phase_id='p1 ')
        old = self.model('DyeDipsRecordPhase').objects.create(old_sheet_series='D1', old_phase_no=2,
            old_phase_id='P1', legacy_id='historical-duplicate')
        self.assertTrue(type(old).objects.filter(pk=old.pk).exists())
        self.model('PStuff', 'erp_base').objects.create(old_stuff_id='STOP', old_status=1)
        with self.assertRaisesMessage(ValidationError, '已停用'):
            self.write('DyeDipsRecordDetail', old_sheet_series='D1', old_phase_no=1, old_stuff_no=1, old_stuff_id='STOP')

    def test_recipe_delete_prefers_dated_version_over_null_date(self):
        master = self.model('PColorNum', 'erp_base').objects.create(old_color_no='C', old_color_num='C1')
        for series, when in [('DATED', timezone.make_aware(datetime(2026, 1, 1))), ('UNDATED', None)]:
            self.model('DyeRecipe').objects.create(old_sheet_series=series, old_sheet_kind=1,
                old_color_num='C1', old_color_version=series, old_sheet_date=when, legacy_id=series)
        recipe = self.write('DyeRecipe', old_sheet_series='NEW', old_sheet_kind=1, old_color_num='C1')
        services.delete_documents(type(recipe).objects.filter(pk=recipe.pk), self.actor)
        master.refresh_from_db(); self.assertEqual(master.old_color_num_no, 'DATED')
