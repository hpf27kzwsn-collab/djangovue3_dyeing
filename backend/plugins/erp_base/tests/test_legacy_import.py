import hashlib,json,tempfile
from pathlib import Path
from django.test import TestCase
from django.core.management import call_command
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users
from plugins.erp_base.legacy_services import register_snapshot,rows
from plugins.erp_base.legacy_import import import_row
from plugins.erp_base.legacy_models import LegacyObjectMap,LegacyImportIssue
from plugins.erp_base.models import BusinessChoice,Machine,Party,Employee,Shift


class LegacyImportTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('init_data',verbosity=0);cls.actor=Users.objects.get(username='superadmin')

    def setUp(self):self.client=APIClient();self.client.force_authenticate(self.actor)

    def archive(self,root,data,key):
        path=root/'dye.p_FieldValid.jsonl'
        text=json.dumps({'row':1,'key':key,'values':data},ensure_ascii=True,separators=(',',':'))+'\n'
        path.write_text(text,encoding='utf-8');Path(str(path)+'.index').write_text('0,0\n',encoding='utf-8')
        manifest={'database':'Textile_GXHFRS','started_at':timezone.now().isoformat(),'finished_at':timezone.now().isoformat(),
            'tables':[{'schema':'dye','table':'p_FieldValid','modules':['base'],'columns':[{'field_name':name,'data_type':'decimal' if name=='NumValue' else 'nvarchar'} for name in data],
                'primary_key':['FieldType','Code'] if key is not None else [],'rows':1,'bytes':path.stat().st_size,
                'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'file':path.name}]}
        manifest_path=root/'manifest.json';manifest_path.write_text(json.dumps(manifest),encoding='utf-8')
        batch=register_snapshot(manifest_path,self.actor)
        return batch,batch.source_tables.get()

    def test_composite_old_id_decimal_null_and_trailing_spaces_compare(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            data={'FieldType':'DyeClass','Code':'0001','Name':'实际名称  ','NumValue':'123.123456','SortValue':None,'IsStop':None,'ParentCode':None}
            batch,table=self.archive(root,data,{'FieldType':'DyeClass','Code':'0001'})
            source=rows(table,1,1)[0];item=import_row(batch,table,source,self.actor)
            self.assertEqual(item.name,'实际名称  ');self.assertIsNone(item.is_active);self.assertIsNone(item.sort)
            self.assertEqual(str(item.numeric_value),'123.123456')
            identity=json.loads(item.legacy_id);self.assertEqual(identity['key'],source['key'])
            self.assertEqual(register_snapshot(root/'manifest.json',self.actor).pk,batch.pk)
            self.assertEqual(import_row(batch,table,source,self.actor).pk,item.pk)
            self.assertEqual(BusinessChoice.objects.count(),1)
            mapping=LegacyObjectMap.objects.get()
            response=self.client.get(f'/api/system/erp_base_legacyobjectmap/{mapping.pk}/compare/')
            self.assertEqual(response.status_code,200,response.data);self.assertTrue(all(row['matches'] for row in response.data['data']['rows']))
            item.name='人工新名称';item.save()
            response=self.client.get(f'/api/system/erp_base_legacyobjectmap/{mapping.pk}/compare/')
            self.assertFalse(next(row for row in response.data['data']['rows'] if row['field']=='name')['matches'])

    def test_no_primary_key_stays_archive_and_does_not_fabricate_old_id(self):
        with tempfile.TemporaryDirectory() as directory:
            data={'FieldType':'DyeClass','Code':'0001','Name':'实际名称','NumValue':None,'SortValue':'0','IsStop':False,'ParentCode':None}
            batch,table=self.archive(Path(directory),data,None)
            self.assertIsNone(import_row(batch,table,rows(table,1,1)[0],self.actor))
            self.assertEqual(BusinessChoice.objects.count(),0);self.assertEqual(LegacyImportIssue.objects.get().category,'no_primary_key')
            response=self.client.get(f'/api/system/erp_base_legacysourcetable/{table.pk}/rows/')
            self.assertEqual(response.status_code,200,response.data);self.assertIsNone(response.data['data']['rows'][0]['key'])
            response=self.client.post('/api/system/erp_base_legacyimportbatch/',{},format='json')
            self.assertEqual(response.status_code,405)

    def test_latest_master_nulls_and_duplicate_machine_number_are_preserved(self):
        for model,field in [(BusinessChoice,'sort'),(Party,'name'),(Shift,'name'),(Employee,'name'),(Machine,'name'),(Machine,'capacity_description')]:
            self.assertTrue(model._meta.get_field(field).null)
        for code in ['OLD-1','OLD-2']:
            machine=Machine(code=code,number='',name=None,factory=None,capacity_description=None,is_active=None)
            machine.full_clean();machine.save()
        self.assertEqual(Machine.objects.filter(number='').count(),2)
