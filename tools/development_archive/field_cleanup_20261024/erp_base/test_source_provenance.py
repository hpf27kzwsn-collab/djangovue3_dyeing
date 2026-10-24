import json
import tempfile
from pathlib import Path
from django.apps import apps
from django.test import TestCase, SimpleTestCase
from django.db import migrations, models
from django.db.migrations.state import ProjectState
from system.models import Users
from plugins.erp_base.legacy_models import LegacySourceTable, LegacyImportBatch
from tools.development_archive.customer_boundary_20261024.backend.source_import import import_table, compare_table
from plugins.erp_base.source_models import SourceDyeSAutoID, SourceDyePFieldValid
from plugins.erp_base.source_provenance import reference
from plugins.erp_base.source_migrations import RemoveSourceFields
from plugins.erp_base.tests.source_fixtures import historical_batch


class OriginalProvenanceTests(TestCase):
    def setUp(self):
        self.actor=Users.objects.create_superuser(username='provenance-test',password='test')
        self.directory=tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)

    def table(self,model,values,batch=None):
        batch=batch or historical_batch()
        path=Path(self.directory.name)/(str(batch.pk)+model.__name__+'.jsonl')
        rows=[]
        for index,overrides in enumerate(values,1):
            raw=dict.fromkeys(model.SOURCE_FIELDS);raw.update(overrides)
            rows.append({'row':index,'key':{k:raw[k] for k in model.SOURCE_KEY} if model.SOURCE_KEY else None,'values':raw})
        path.write_text(''.join(json.dumps(row)+'\n' for row in rows),encoding='utf-8')
        return LegacySourceTable.objects.create(batch=batch,schema_name=model.SOURCE_SCHEMA,table_name=model.SOURCE_TABLE,
            modules=[],columns=[],primary_key=list(model.SOURCE_KEY),row_count=len(rows),byte_count=path.stat().st_size,
            sha256='test',file_path=str(path))

    def test_keyless_exact_duplicates_negative_null_and_empty_survive_copy_and_comparison(self):
        values={'IDObject':'','IDCounter':-2,'IDDate':None}
        table=self.table(SourceDyeSAutoID,[values,values])
        self.assertEqual(import_table(table,self.actor),2)
        self.assertEqual(compare_table(table)['rows'],2)
        rows=list(SourceDyeSAutoID.objects.order_by('source_row'))
        self.assertNotEqual(rows[0].pk,rows[1].pk)
        self.assertEqual([r.source_row for r in rows],[1,2])
        self.assertEqual(rows[0].old_idcounter,-2)
        self.assertEqual(reference(rows[0])['key'],{})
        with self.assertRaisesRegex(ValueError,'已经承接'):import_table(table,self.actor)
        self.assertEqual(SourceDyeSAutoID.objects.count(),2)
        SourceDyeSAutoID.objects.filter(pk=rows[1].pk).update(old_idcounter=-3)
        with self.assertRaisesRegex(ValueError,'原字段不一致'):compare_table(table)

    def test_composite_key_duplicates_and_same_keys_in_another_batch_are_not_merged(self):
        values={'FieldType':'DyeClass','Code':'0001','Name':'原文  '}
        first=self.table(SourceDyePFieldValid,[values,values])
        import_table(first,self.actor)
        source=historical_batch()
        source.pk=None;source.number='second';source.manifest_sha256='second';source.save()
        second=self.table(SourceDyePFieldValid,[{**values,'Name':'第二次值'}],source)
        import_table(second,self.actor)
        self.assertEqual(SourceDyePFieldValid.objects.count(),3)
        self.assertEqual(compare_table(first)['rows'],2)
        self.assertEqual(compare_table(second)['rows'],1)
        self.assertEqual(reference(SourceDyePFieldValid.objects.filter(source_batch=first.batch).first())['key'],
            {'FieldType':'DyeClass','Code':'0001'})

    def test_original_columns_and_current_api_models_have_no_extra_identifier(self):
        for model in apps.get_models():
            if model._meta.app_label.startswith('erp_'):
                self.assertTrue({'legacy_id','header_legacy_id'}.isdisjoint(f.name for f in model._meta.fields))


class RemovalMigrationStateTests(SimpleTestCase):
    def test_bulk_removal_matches_standard_migration_state(self):
        state=ProjectState()
        migrations.CreateModel(name='SourceOne',fields=[('id',models.BigAutoField(primary_key=True)),
            ('legacy_id',models.TextField(null=True)),('code',models.CharField(max_length=20))]).state_forwards('example',state)
        standard=state.clone();batched=state.clone();batched.apps
        operations=[migrations.RemoveField('sourceone','legacy_id')]
        operations[0].state_forwards('example',standard)
        RemoveSourceFields(operations).state_forwards('example',batched)
        self.assertEqual(standard,batched)
