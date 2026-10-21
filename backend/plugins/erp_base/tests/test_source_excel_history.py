"""历史基础资料通过真实Excel接口保留原主键、原值、重复行及批次关系。"""
from io import BytesIO
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from plugins.erp_base.source_phase3_operations import model
from plugins.erp_base.source_excel_history import columns
from plugins.erp_base.legacy_models import LegacyImportBatch
from plugins.erp_base.models import BusinessAction
from plugins.erp_base.source_sequences import SourceIdentitySequence
from system.excel import write_workbook


class HistoryExcelTests(TestCase):
    def setUp(self):
        self.client=APIClient();self.client.force_authenticate(get_user_model().objects.create(username='history-xlsx',is_superuser=True))

    def upload(self,name,rows,ordinals=None,package=None):
        m=model(name);data=[]
        for values in rows:
            if name=='DEPARTMENTS':values={'SUPDEPTID':0,'DefaultSchId':0,**values}
            if name=='p_Fabric_Cust':values={'Kind':0,**values}
            data.append({key:values.get(old) for old,key in m.SOURCE_FIELDS.items()})
        content=BytesIO();context={'导入方式':'历史基础资料原值承接'}
        if package:context.update(资料批次号=package,批次摘要='a'*64,原表数=2)
        write_workbook(data,columns(m),content,'create',context)
        return self.client.post('/api/system/'+m._meta.label_lower.replace('.','_')+'/import/',{'file':SimpleUploadedFile(name+'.xlsx',content.getvalue())},format='multipart')

    def test_original_identity_and_duplicate_values_are_preserved(self):
        response=self.upload('DEPARTMENTS',[{'DEPTID':91,'DEPTNAME':'原部门'},{'DEPTID':91,'DEPTNAME':'原部门'}])
        self.assertEqual(response.status_code,200,response.data)
        rows=list(model('DEPARTMENTS').objects.order_by('pk'))
        self.assertEqual([r.old_deptid for r in rows],[91,91])
        self.assertEqual([r.source_row for r in rows],[1,2])
        self.assertEqual(LegacyImportBatch.objects.get().row_count,2)
        self.assertFalse(SourceIdentitySequence.objects.exists())
        self.assertFalse(BusinessAction.objects.exists())

    def test_historical_customer_keeps_null_num_and_does_not_run_formula(self):
        response=self.upload('p_Customer',[{'CustomerID':'0007','Num':None,'Remarks':'#NULL','ShortName':''}])
        self.assertEqual(response.status_code,200,response.data)
        item=model('p_Customer').objects.get()
        self.assertIsNone(item.old_num);self.assertEqual(item.old_remarks,'#NULL');self.assertEqual(item.old_short_name,'')
        self.assertIsNone(item.approval_stage);self.assertIsNotNone(item.source_batch_id)

    def test_invalid_second_row_rolls_back_first_row_and_batch(self):
        response=self.upload('DEPARTMENTS',[{'DEPTID':91},{'DEPTID':None}])
        self.assertEqual(response.status_code,400,response.data)
        self.assertFalse(model('DEPARTMENTS').objects.exists());self.assertFalse(LegacyImportBatch.objects.exists())

    def test_shared_package_links_original_codes_across_tables(self):
        self.assertEqual(self.upload('p_Gray',[{'GrayID':'001'}],package='同一资料包').status_code,200)
        response=self.upload('p_Fabric_Cust',[{'FabricID':'001','CustomerID':'C'}],package='同一资料包')
        self.assertEqual(response.status_code,200,response.data)
        child=model('p_Fabric_Cust').objects.get()
        relation=next(r for r in child.SOURCE_RELATIONS if r['target_fields']==['GrayID'])
        self.assertEqual(getattr(child,relation['field']).old_gray_id,'001')
        self.assertEqual(LegacyImportBatch.objects.count(),1)

    def test_reserved_serial_caption_is_a_real_original_field(self):
        response=self.upload('BaseCaseDetail',[{'SheetSeries':'S','DetailNo':'D','SerialNum':'0008'}])
        self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(model('BaseCaseDetail').objects.get().old_serial_num,'0008')

    def test_encoded_original_text_preserves_carriage_return_and_literal_markers(self):
        from base64 import b64encode
        expected='嫩芽黄\r\n#NULL\x01'
        encoded='#UTF8:'+b64encode(expected.encode()).decode()
        response=self.upload('p_Customer',[{'CustomerID':'001','Remarks':encoded}])
        self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(model('p_Customer').objects.get().old_remarks,expected)
