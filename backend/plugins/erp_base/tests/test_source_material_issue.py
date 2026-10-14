from decimal import Decimal
from django.apps import apps
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from system.models import Users
from plugins.erp_base import source_services as services
from plugins.erp_base.source_material_issue import issue
from plugins.erp_base.source_context import SourceDocumentContext


class OriginalMaterialIssueTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='original-material-issue', password='test-password')
        material = apps.get_model('erp_base.SourceDyePStuff')
        self.material = material.objects.create(old_stuff_id='S1', old_price=3, old_wof=2)
        material.objects.create(old_stuff_id='S2', old_price=4, old_wof=1)
        self.weight = services.write(apps.get_model('erp_production.SourceDyeStuffWeight'),
            {'_entry': 'NormalStuffWeight', 'old_sheet_series': 'WEIGHT-1', 'old_sheet_no': 'WEIGHT-1',
             'old_job_sheet_no': 'JOB-1'}, actor=self.actor)
        self.phase = services.write(apps.get_model('erp_production.SourceDyeStuffWeightPhase'),
            {'source_parent_1': self.weight, 'old_phase_no': 1}, actor=self.actor)
        detail = apps.get_model('erp_production.SourceDyeStuffWeightDetail')
        self.measured = services.write(detail, {'source_parent_1': self.phase, 'old_stuff_no': 1,
            'old_stuff_id': 'S1', 'old_need_qty': 1000, 'old_real_qty': 500, 'old_weight_unit': 'G'}, actor=self.actor)
        self.planned = services.write(detail, {'source_parent_1': self.phase, 'old_stuff_no': 2,
            'old_stuff_id': 'S2', 'old_need_qty': 2, 'old_real_qty': 0, 'old_weight_unit': 'K'}, actor=self.actor)

    def execute(self):
        return issue(self.weight, self.actor, timezone.now(), 'weighing_finished', '原称量完成记录 W-1')

    def test_material_issue_preserves_plan_and_measured_and_posts_adopted_quantity_once(self):
        self.execute()
        out = apps.get_model('erp_warehouse.SourceDyeStuffOut').objects.get()
        self.assertEqual(out.old_sheet_kind, 21)
        self.assertEqual(out.old_ware_house_id, '13')
        self.assertEqual(out.old_dept_id, '08')
        rows = apps.get_model('erp_warehouse.SourceDyeStuffOutDetail').objects
        measured = rows.get(old_stuff_id='S1'); planned = rows.get(old_stuff_id='S2')
        self.assertEqual(measured.old_qty, Decimal('0.25'))
        self.assertEqual(measured.old_amount, Decimal('0.75'))
        self.assertEqual(planned.old_qty, 2)
        self.assertEqual(planned.old_amount, 8)
        self.measured.refresh_from_db(); self.planned.refresh_from_db()
        self.assertEqual(self.measured.old_need_qty, 1000)
        self.assertEqual(self.measured.old_real_qty, 500)
        self.assertEqual(self.planned.old_real_qty, 0)
        self.execute()
        self.assertEqual(type(out).objects.count(), 1)
        self.assertEqual(apps.get_model('erp_warehouse.SourceDyeStuffStockBook').objects.count(), 2)
        context = SourceDocumentContext.objects.get(entity=self.weight._meta.label, object_id=self.weight.pk)
        self.assertEqual([row['basis'] for row in context.effects['material_issue']['rows']], ['RealQty', 'NeedQty'])

    def test_zero_wof_rolls_back_automatic_issue_without_discarding_source(self):
        self.material.old_wof = 0; self.material.save(update_fields=['old_wof'])
        with self.assertRaisesMessage(ValidationError, '原WOF为0'):
            self.execute()
        self.assertFalse(apps.get_model('erp_warehouse.SourceDyeStuffOut').objects.exists())
        self.assertTrue(type(self.measured).objects.filter(pk=self.measured.pk).exists())

    def test_negative_quantity_is_saved_and_explicitly_reported_as_not_auto_generated(self):
        services.write(type(self.measured), {'old_real_qty': -500}, self.measured, self.actor)
        self.execute()
        self.measured.refresh_from_db(); self.assertEqual(self.measured.old_real_qty, -500)
        context = SourceDocumentContext.objects.get(entity=self.weight._meta.label, object_id=self.weight.pk)
        self.assertEqual(context.effects['material_issue']['not_generated'][0]['source_id'], self.measured.pk)
        self.assertEqual(apps.get_model('erp_warehouse.SourceDyeStuffOutDetail').objects.count(), 1)
