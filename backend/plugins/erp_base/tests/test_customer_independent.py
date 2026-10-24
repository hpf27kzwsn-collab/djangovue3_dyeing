"""从空业务库启用：客户导入、本地关联、实际查询以及非业务接口退出。"""
from io import BytesIO
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from system.catalog import ENTITIES
from system.views import view_for
from system.excel import write_workbook
from plugins.erp_base.source_phase3_operations import model
from plugins.erp_base.source_excel_history import columns
from plugins.erp_base.legacy_models import LegacyImportBatch
from plugins.erp_base.reports import REPORTS
from plugins.erp_base.source_services import stage, editable
from plugins.erp_base.customer_resources import DEVELOPMENT_ACTIONS

class CustomerIndependentTests(TestCase):

    def setUp(self):
        self.actor = get_user_model().objects.create(username='customer-only', is_superuser=True)
        self.client = APIClient()
        self.client.force_authenticate(self.actor)

    def upload(self, table, originals, package=None):
        target = model(table)
        data = [{new: row.get(old) for old, new in target.SOURCE_FIELDS.items()} for row in originals]
        stream = BytesIO()
        context = {'导入方式': '原值导入'}
        if package:
            context['资料批次号'] = package
        write_workbook(data, columns(target), stream, 'create', context)
        return self.client.post('/api/system/' + target._meta.label_lower.replace('.', '_') + '/import/', {'file': SimpleUploadedFile(table + '.xlsx', stream.getvalue())}, format='multipart')

    def test_development_and_parallel_business_resources_are_not_exposed(self):
        for entity in ['erp_base_legacysourcetable', 'erp_base_legacyobjectmap', 'erp_sales_salesorder', 'erp_warehouse_stockbalance', 'erp_base_sourcedyesfunctions']:
            self.assertNotIn(entity, ENTITIES)
            self.assertEqual(self.client.get('/api/system/' + entity + '/').status_code, 404)

    def test_development_and_unrelated_order_actions_have_no_routes(self):
        warehouse = 'erp_warehouse_sourcedyegrayin'
        for action in [*DEVELOPMENT_ACTIONS, 'app_order_save']:
            self.assertEqual(self.client.post('/api/system/' + warehouse + '/' + action + '/').status_code, 404)
        for entity, target in ENTITIES.items():
            self.assertFalse(DEVELOPMENT_ACTIONS.intersection((a.__name__ for a in view_for(entity, target).get_extra_actions())))

    def test_customer_import_needs_no_snapshot_or_old_database_name(self):
        response = self.upload('p_Customer', [{'CustomerID': 'C001', 'NameC': '新客户', 'Num': None}])
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(model('p_Customer').objects.get().old_customer_id, 'C001')
        self.assertNotIn('database_name', {f.name for f in LegacyImportBatch._meta.fields})
        self.assertNotIn('LegacyObjectMap', [m.__name__ for m in apps.get_models()])
        self.assertNotIn('LegacySourceTable', [m.__name__ for m in apps.get_models()])

    def test_identical_rows_and_repeated_file_are_not_silently_deduplicated(self):
        rows = [{'CustomerID': 'C001', 'NameC': '同名客户'}, {'CustomerID': 'C001', 'NameC': '同名客户'}]
        self.assertEqual(self.upload('p_Customer', rows).status_code, 200)
        response = self.upload('p_Customer', rows)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(model('p_Customer').objects.count(), 4)
        self.assertEqual(LegacyImportBatch.objects.count(), 2)

    def test_customer_portal_fields_are_not_generated_but_imported_values_are_preserved(self):
        response = self.client.post('/api/system/erp_base_sourcedyepcustomer/', {'_entry': 'p_Customer', 'old_customer_id': 'NEW', 'old_name_c': '新建客户'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        item = model('p_Customer').objects.get(old_customer_id='NEW')
        self.assertFalse(item.old_password)
        self.assertFalse(item.old_login_name)
        response = self.upload('p_Customer', [{'CustomerID': 'ARCHIVE', 'PASSWORD': '历史原值', 'LoginName': '原账号'}])
        self.assertEqual(response.status_code, 200, response.data)
        item = model('p_Customer').objects.get(old_customer_id='ARCHIVE')
        self.assertEqual((item.old_password, item.old_login_name), ('历史原值', '原账号'))

    def test_later_parent_import_backfills_local_child_without_reimport(self):
        self.assertEqual(self.upload('p_Fabric_Cust', [{'FabricID': 'LATE', 'CustomerID': 'C', 'Kind': 0}]).status_code, 200)
        child = model('p_Fabric_Cust').objects.get()
        relation = next((r for r in child.SOURCE_RELATIONS if r['target_fields'] == ['GrayID']))
        self.assertIsNone(getattr(child, relation['field'] + '_id'))
        self.assertEqual(self.upload('p_Gray', [{'GrayID': 'LATE', 'NameC': '后导入物料'}]).status_code, 200)
        child.refresh_from_db()
        self.assertEqual(getattr(child, relation['field']).old_gray_id, 'LATE')

    def test_employee_number_does_not_create_unused_portal_credentials(self):
        from plugins.erp_base.source_services import write
        item = write(model('h_Employee'), {'_entry': 'qry_Employee', 'old_emp_id': 'EMP001'}, actor=self.actor)
        self.assertIsNone(item.old_login_name)
        self.assertIsNone(item.old_password)
        self.assertEqual(item.creator, self.actor)
        self.assertEqual(item.old_creater, self.actor.username[:10])
        item = write(type(item), {'old_login_name': 'local-user', 'old_password': '历史原值'}, item, actor=self.actor)
        item = write(type(item), {'old_emp_id': 'EMP002'}, item, actor=self.actor)
        self.assertEqual((item.old_login_name, item.old_password), ('local-user', '历史原值'))

    def test_site_record_api_quantities_use_actual_document_precision(self):
        job = model('JobSheet').objects.create(old_sheet_no='LOCAL-JOB', old_sheet_series='LOCAL-JOB')
        response = self.client.post('/api/system/erp_production_sourcedyejobsheet/' + str(job.pk) + '/create_site_record/', {'entry': 'WProcessEdit', 'process_no': 1, 'process': 'GX01', 'rolls': '2', 'weight': '10', 'length': '0', 'auto_shift': False}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        item = model('WProcess').objects.get(pk=response.data['data']['id'])
        self.assertEqual((item.old_curr_rolls, item.old_curr_kg, item.old_curr_meter), (2, 10, 0))

    def test_import_links_local_master_across_separate_upload_batches(self):
        self.assertEqual(self.upload('p_Gray', [{'GrayID': '001', 'NameC': '客户纱线'}]).status_code, 200)
        response = self.upload('p_Fabric_Cust', [{'FabricID': '001', 'CustomerID': 'C', 'Kind': 0}])
        self.assertEqual(response.status_code, 200, response.data)
        child = model('p_Fabric_Cust').objects.get()
        relation = next((r for r in child.SOURCE_RELATIONS if r['target_fields'] == ['GrayID']))
        self.assertEqual(getattr(child, relation['field']).old_gray_id, '001')

    def test_multiple_local_parents_preserve_all_rows_without_guessing(self):
        self.assertEqual(self.upload('p_Gray', [{'GrayID': '001'}, {'GrayID': '001'}]).status_code, 200)
        response = self.upload('p_Fabric_Cust', [{'FabricID': '001', 'CustomerID': 'C', 'Kind': 0}])
        self.assertEqual(response.status_code, 200, response.data)
        child = model('p_Fabric_Cust').objects.get()
        relation = next((r for r in child.SOURCE_RELATIONS if r['target_fields'] == ['GrayID']))
        self.assertIsNone(getattr(child, relation['field'] + '_id'))
        self.assertEqual(model('p_Gray').objects.count(), 2)

    def test_new_customer_has_no_confirmation_step(self):
        response = self.client.post('/api/system/erp_base_sourcedyepdept/', {'old_dept_id': 'D001', 'old_name': '页面新增'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        item = model('p_Dept').objects.get()
        self.assertIsNone(stage(item))
        self.assertIsNone(stage(item))
        item.old_right_status = 0
        editable([item])

    def test_imported_original_approval_drives_business_state(self):
        item = model('OrderMain').objects.create(old_sheet_series='ORDER', old_right_status=10)
        self.assertEqual(stage(item), 'approved')
        item.old_right_status = 0
        self.assertEqual(stage(item), 'unreviewed')

    def test_all_business_reports_run_on_empty_database(self):
        for key in REPORTS:
            response = self.client.get('/api/plugins/erp/reports/' + key + '/')
            self.assertEqual(response.status_code, 200, (key, response.data))
            self.assertEqual(response.data['data']['count'], 0, key)

    def test_prices_and_orders_read_customer_local_records(self):
        model('FixedPriceDetail').objects.create(old_detail_no='Q1', old_cus_price='12.34', old_prod_id='Y1', old_width=0, old_weight=0)
        model('OrderColor').objects.create(old_check_no='O1', old_sheet_series='ORDER', old_order_qty='20', old_price='12.34', old_amount='246.80')
        for key, field, value in [('prices', 'DetailNo', 'Q1'), ('orders', 'CheckNo', 'O1')]:
            result = self.client.get('/api/plugins/erp/reports/' + key + '/').data['data']
            self.assertEqual(result['count'], 1)
            self.assertEqual(result['rows'][0][field], value)

    def test_scan_local_employee_card_and_duplicate_package_labels(self):
        model('h_Employee').objects.create(old_emp_id='E1', old_name='本地员工', old_rfid='CARD1')
        response = self.client.get('/api/plugins/erp/identify/employee/', {'key': 'card_identifier', 'value': 'CARD1'})
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['data']['matches'][0]['code'], 'E1')
        model('RecordYield').objects.create(old_guid='P1', old_bar_code='SAME')
        model('RecordYield').objects.create(old_guid='P2', old_bar_code='SAME')
        model('GrayRecord').objects.create(old_bar_code='SAME')
        matches = self.client.get('/api/plugins/erp/identify/package/', {'key': 'barcode', 'value': 'SAME'}).data['data']['matches']
        self.assertEqual(len(matches), 3)
        self.assertEqual(len({(r['entity'], r['id']) for r in matches}), 3)
