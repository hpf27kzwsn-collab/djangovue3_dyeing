from django.apps import apps
from django.test import TestCase, SimpleTestCase
from plugins.erp_base.tests.source_fixtures import historical_batch
from plugins.erp_base.source_documents import SourceRecord
from plugins.erp_base.source_provenance import reference
from plugins.erp_base.source_phase3_operations import model

class FieldCleanupTests(TestCase):
    def test_original_customer_and_composite_keys_are_retained(self):
        customer=model('p_Customer').objects.create(old_customer_id='000012',source_batch=historical_batch())
        option=model('p_FieldValid').objects.create(old_field_type='DyeClass',old_code='0001',source_batch=historical_batch())
        self.assertEqual(reference(customer)['key'],{'CustomerID':'000012'})
        self.assertEqual(reference(option)['key'],{'FieldType':'DyeClass','Code':'0001'})

class FieldStructureTests(SimpleTestCase):
    def test_all_original_models_retained_without_generic_review_or_extra_text(self):
        originals=[m for m in apps.get_models() if issubclass(m,SourceRecord)]
        self.assertEqual(len(originals),655)
        self.assertEqual(sum(len(m.SOURCE_FIELDS) for m in originals),12606)
        removed={'approval_stage','confirmed_at','confirmed_by','approved_at','approved_by','description','remarks','legacy_id'}
        for m in originals:self.assertFalse(removed.intersection(f.name for f in m._meta.fields),m._meta.label)
