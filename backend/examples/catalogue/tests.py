import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from django.test import TestCase
from django.core.management import call_command
from rest_framework.test import APIClient
from system.models import Users, Menu, SystemConfig
from system.catalog import ENTITIES
from system.model_catalog import project_models
from .models import Entry, Note, NoteLine


class ExtensionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('init_data', verbosity=0)

    def setUp(self):
        self.user = Users.objects.get(username='superadmin')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_model_to_metadata_crud_permissions_association_and_generator(self):
        self.assertIs(ENTITIES['example_catalogue_entry'],Entry)
        self.assertNotIn(Note,list(project_models()))
        self.assertTrue(Menu.objects.filter(component_name='example_catalogue_entry').exists())
        meta=self.client.get('/api/meta/example_catalogue_entry/').data['data']
        self.assertEqual(meta['pk'],'code')
        self.assertEqual(next(row for row in meta['fields'] if row['key']=='date')['kind'],'date')
        response=self.client.post('/api/system/example_catalogue_entry/',{'code':'alpha','name':'测试','amount':'123.45','detail':{'count':0}},format='json')
        self.assertEqual(response.status_code,200,response.data)
        entry=Entry.objects.get(pk='alpha')
        self.assertEqual(entry.creator,self.user)
        renamed=self.client.patch('/api/system/example_catalogue_entry/alpha/',{'code':'renamed'},format='json')
        self.assertEqual(renamed.status_code,200,renamed.data)
        self.assertEqual(Entry.objects.count(),1)
        self.assertFalse(Entry.objects.filter(pk='alpha').exists())
        item=SystemConfig.objects.create(title='关联',key='example-link',setting={'table':'example_catalogue_entry'})
        rows=self.client.get(f'/api/system/system_config/{item.pk}/table_data/').data['data']
        self.assertEqual(rows[0]['code'],'renamed')
        with TemporaryDirectory() as directory:
            call_command('generate_crud','example_catalogue.Entry',output=directory)
            self.assertIn('example_catalogue_entry',(Path(directory)/'example_catalogue_entry'/'index.vue').read_text(encoding='utf-8'))

    def test_explicit_request_audit_and_soft_hard_cascade(self):
        request=SimpleNamespace(user=self.user)
        note=Note.objects.create(request=request,name='父项')
        child=NoteLine.objects.create(request=request,note=note,name='子项')
        self.assertEqual(note.creator,self.user)
        old_time=note.update_datetime
        Note.objects.filter(pk=note.pk).update(request=request,name='更新')
        updated=Note.objects.get(pk=note.pk)
        self.assertEqual(updated.modifier,self.user)
        self.assertGreater(updated.update_datetime,old_time)
        count,labels=Note.objects.filter(pk=note.pk).delete()
        self.assertEqual(count,2)
        self.assertFalse(Note.objects.exists())
        self.assertTrue(NoteLine.all_objects.get(pk=child.pk).is_deleted)
        Note.all_objects.get(pk=note.pk).delete(soft_delete=False)
        self.assertFalse(NoteLine.all_objects.exists())

    def test_business_json_restore_preserves_pk_and_updates_unique_key(self):
        with TemporaryDirectory() as directory:
            path=Path(directory)/'entry.json'
            path.write_text(json.dumps([{'code':'restored','name':'第一次','amount':'0.00'}]),encoding='utf-8')
            call_command('load_init_data','example_catalogue.Entry',str(path))
            path.write_text(json.dumps([{'code':'restored','name':'第二次'}]),encoding='utf-8')
            call_command('load_init_data','example_catalogue.Entry',str(path),unique_fields=['code'])
            self.assertEqual(Entry.objects.get(pk='restored').name,'第二次')
            self.assertEqual(Entry.objects.count(),1)

    def test_batch_update_string_pk_decimal_metadata_and_delete_timestamp(self):
        Entry.objects.create(code='string-key',name='旧名称',amount='1.00')
        result=self.client.put('/api/system/example_catalogue_entry/batch_update/',[{'code':'string-key','amount':'99999999.99','name':'新名称'}],format='json')
        self.assertEqual(result.status_code,200,result.data)
        self.assertEqual(str(Entry.objects.get(pk='string-key').amount),'99999999.99')
        meta=self.client.get('/api/meta/example_catalogue_entry/').data['data']
        field=next(row for row in meta['fields'] if row['key']=='amount')
        self.assertEqual(field['kind'],'decimal')
        self.assertEqual(field['column']['minWidth'],180)
        note=Note.objects.create(name='逻辑删除时间')
        previous=note.update_datetime
        note.delete()
        self.assertGreater(Note.all_objects.get(pk=note.pk).update_datetime,previous)
