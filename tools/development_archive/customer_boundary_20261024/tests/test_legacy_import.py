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

    def archive(self,root,data,key,copies=1):
        from plugins.erp_base.source_models import SourceDyePFieldValid
        data={**dict.fromkeys(SourceDyePFieldValid.SOURCE_FIELDS),**data}
        path=root/'dye.p_FieldValid.jsonl'
        text=''.join(json.dumps({'row':index,'key':key,'values':data},ensure_ascii=True,separators=(',',':'))+'\n' for index in range(1,copies+1))
        path.write_text(text,encoding='utf-8');Path(str(path)+'.index').write_text('0,0\n',encoding='utf-8')
        manifest={'database':'Textile_GXHFRS','started_at':timezone.now().isoformat(),'finished_at':timezone.now().isoformat(),
            'tables':[{'schema':'dye','table':'p_FieldValid','modules':['base'],'columns':[{'field_name':name,'data_type':'decimal' if name=='NumValue' else 'nvarchar'} for name in data],
                'primary_key':['FieldType','Code'] if key is not None else [],'rows':copies,'bytes':path.stat().st_size,
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
            self.assertEqual(LegacyObjectMap.objects.get(target_model=item._meta.label).source_key,source['key'])
            self.assertEqual(register_snapshot(root/'manifest.json',self.actor).pk,batch.pk)
            self.assertEqual(import_row(batch,table,source,self.actor).pk,item.pk)
            self.assertEqual(BusinessChoice.objects.count(),1)
            mapping=LegacyObjectMap.objects.get(target_model=item._meta.label)
            response=self.client.get(f'/api/system/erp_base_legacyobjectmap/{mapping.pk}/compare/')
            self.assertEqual(response.status_code,200,response.data);self.assertTrue(all(row['matches'] for row in response.data['data']['rows']))
            item.name='人工新名称';item.save()
            response=self.client.get(f'/api/system/erp_base_legacyobjectmap/{mapping.pk}/compare/')
            self.assertFalse(next(row for row in response.data['data']['rows'] if row['field']=='name')['matches'])

    def test_no_primary_key_stays_archive_and_does_not_fabricate_old_id(self):
        with tempfile.TemporaryDirectory() as directory:
            data={'FieldType':'DyeClass','Code':'0001','Name':'实际名称','NumValue':None,'SortValue':'0','IsStop':False,'ParentCode':None}
            batch,table=self.archive(Path(directory),data,None)
            original=import_row(batch,table,rows(table,1,1)[0],self.actor)
            self.assertEqual(original.old_code,'0001');self.assertEqual(original.source_batch_id,batch.pk)
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

    def test_duplicate_original_keys_are_stored_as_separate_source_rows(self):
        from plugins.erp_base.source_models import SourceDyePFieldValid
        with tempfile.TemporaryDirectory() as directory:
            data={'FieldType':'DyeClass','Code':'0001','Name':'相同原值','NumValue':None,'SortValue':None,'IsStop':None,'ParentCode':None}
            batch,table=self.archive(Path(directory),data,{'FieldType':'DyeClass','Code':'0001'})
            first=rows(table,1,1)[0]
            import_row(batch,table,first,self.actor)
            duplicate=import_row(batch,table,{**first,'row':2},self.actor)
            self.assertIsInstance(duplicate,SourceDyePFieldValid)
            self.assertEqual(SourceDyePFieldValid.objects.count(),2)
            self.assertEqual(BusinessChoice.objects.count(),1)
            self.assertTrue(LegacyImportIssue.objects.filter(category='duplicate_source_key',row_number=2).exists())

    def test_master_import_counts_separate_original_rows_from_adopted_masters(self):
        from plugins.erp_base.legacy_import import RULES,import_masters
        from plugins.erp_base.legacy_models import LegacySourceTable
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            data={'FieldType':'DyeClass','Code':'0001','Name':'重复原行','NumValue':None,'SortValue':None,'IsStop':None,'ParentCode':None}
            batch,table=self.archive(root,data,{'FieldType':'DyeClass','Code':'0001'},copies=2)
            for name,(_,fields,_) in RULES.items():
                if name=='p_FieldValid':continue
                path=root/(name+'.jsonl');path.write_text('',encoding='utf-8')
                LegacySourceTable.objects.create(batch=batch,schema_name='dye',table_name=name,modules=['base'],
                    columns=[{'field_name':name} for name in fields.values()],primary_key=[],row_count=0,
                    byte_count=0,sha256=hashlib.sha256(b'').hexdigest(),file_path=str(path))
            result=import_masters(batch,self.actor)
            self.assertEqual(result['p_FieldValid'],{'original_rows':2,'adopted_rows':1,'original_only_rows':1,'excluded_finance':0})

    def test_new_batch_uses_existing_map_and_keeps_changed_original_value(self):
        from plugins.erp_base.source_models import SourceDyePFieldValid
        with tempfile.TemporaryDirectory() as first_dir,tempfile.TemporaryDirectory() as second_dir:
            data={'FieldType':'DyeClass','Code':'0001','Name':'原名称','NumValue':None,'SortValue':None,'IsStop':None,'ParentCode':None}
            key={'FieldType':'DyeClass','Code':'0001'}
            first,first_table=self.archive(Path(first_dir),data,key)
            master=import_row(first,first_table,rows(first_table,1,1)[0],self.actor)
            second,second_table=self.archive(Path(second_dir),{**data,'Name':'新原名称'},key)
            changed=import_row(second,second_table,rows(second_table,1,1)[0],self.actor)
            self.assertIsInstance(changed,SourceDyePFieldValid)
            self.assertEqual(changed.old_name,'新原名称')
            master.refresh_from_db();self.assertEqual(master.name,'原名称')
            self.assertEqual(SourceDyePFieldValid.objects.count(),2)
            self.assertEqual(BusinessChoice.objects.count(),1)
            self.assertTrue(LegacyImportIssue.objects.filter(batch=second,category='changed_source').exists())
