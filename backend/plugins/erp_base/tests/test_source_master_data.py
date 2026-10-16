from django.apps import apps
from django.core.exceptions import ValidationError
from django.test import TestCase
from system.models import Users
from plugins.erp_base.source_services import write, delete
from plugins.erp_base.source_stock_services import raw
from plugins.erp_base.source_quality_reports import rows
from plugins.erp_base.source_context import SourceDocumentContext


def model(name):
    return apps.get_model('erp_base', 'SourceDye'+name)


class MasterTriggerTests(TestCase):
    def setUp(self):
        self.actor = Users.objects.create_superuser(username='master-trigger', password='test-only')

    def test_department_original_name_join_and_update(self):
        model('PDept').objects.create(old_dept_id='OLD', old_name='同名')
        dept = write(model('PDept'), {'old_dept_id':'NEW', 'old_name':'同名'}, actor=self.actor)
        self.assertEqual(set(rows('DEPARTMENTS', 'erp_base').values_list('old_code', flat=True)), {'OLD','NEW'})
        write(model('PDept'), {'old_name':'新名称'}, actor=self.actor, instance=dept)
        self.assertEqual(raw(rows('DEPARTMENTS','erp_base').get(old_code='NEW'),'DEPTNAME'), '新名称')

    def test_departed_employee_last_department_assignment_and_retained_members(self):
        write(model('PDept'), {'old_dept_id':'D', 'old_name':'部门'}, actor=self.actor)
        department_id = raw(rows('DEPARTMENTS','erp_base').get(old_code='D'),'DEPTID')
        employee = model('HEmployee').objects.create(old_emp_id='E', old_name='姓名', old_dept_id='D', old_rfid='CARD')
        account = write(model('USERINFO'), {'old_ssn':'E', 'old_card_no':'CARD'}, actor=self.actor)
        member = model('PShiftEmp').objects.create(old_emp_id='E')
        write(model('HEmployee'), {'old_is_out':True}, actor=self.actor, instance=employee)
        account.refresh_from_db(); employee.refresh_from_db()
        self.assertEqual(raw(account,'DEFAULTDEPTID'), department_id)
        self.assertEqual(raw(account,'CardNo'), '')
        self.assertEqual(raw(employee,'RFID'), '')
        self.assertTrue(model('PShiftEmp').objects.filter(pk=member.pk).exists())
        self.assertFalse(rows('PShiftEmp','erp_base').filter(pk=member.pk).exists())

    def test_employee_delete_retains_attendance_source(self):
        employee = model('HEmployee').objects.create(old_emp_id='E')
        account = write(model('USERINFO'), {'old_ssn':'E'}, actor=self.actor)
        delete(model('HEmployee').objects.filter(pk=employee.pk), self.actor)
        self.assertTrue(model('USERINFO').objects.filter(pk=account.pk).exists())
        self.assertFalse(rows('USERINFO','erp_base').filter(pk=account.pk).exists())

    def test_empty_ssn_is_saved_but_excluded_from_active(self):
        item = write(model('USERINFO'), {'old_ssn':' '}, actor=self.actor)
        self.assertTrue(model('USERINFO').objects.filter(pk=item.pk).exists())
        self.assertFalse(rows('USERINFO','erp_base').filter(pk=item.pk).exists())

    def test_customer_duplicate_retained_and_original_update_column_rule(self):
        for code in ['A','B']:
            item = write(model('PCustomer'), {'old_customer_id':code,'old_cust_kind_id':'0','old_short_name':'同名'}, actor=self.actor)
        self.assertEqual(model('PCustomer').objects.count(),2)
        with self.assertRaises(ValidationError):
            write(model('PCustomer'), {'old_customer_id':'B'}, actor=self.actor, instance=item)
        supplier = write(model('PCustomer'), {'old_customer_id':'S','old_cust_kind_id':'1'}, actor=self.actor)
        write(model('PCustomer'), {'old_customer_id':'S2'}, actor=self.actor, instance=supplier)

    def test_feel_quote_cross_customer_duplicates_and_price_code(self):
        model('FeelOfferMain').objects.create(old_sheet_series='A', old_customer_id='C')
        model('FeelOfferMain').objects.create(old_sheet_series='B', old_customer_id='D')
        for series in ['A','B']:
            item = write(model('FeelOfferDetail'), {'old_sheet_series':series,'old_detail_no':series,
                'old_prod_id':'P','old_feel_code':'F','old_price':'.85'}, actor=self.actor)
            self.assertEqual(raw(item,'SGDH'),'09')
        self.assertEqual(model('FeelOfferDetail').objects.count(),2)
        negative=write(model('FeelOfferDetail'),{'old_sheet_series':'A','old_detail_no':'N',
            'old_prod_id':'P2','old_feel_code':'F2','old_price':'-.01'},actor=self.actor)
        self.assertEqual(raw(negative,'SGDH'),'00')
        write(model('FeelOfferDetail'), {'old_right_status':10}, actor=self.actor, instance=item)
        with self.assertRaises(ValidationError):
            write(model('FeelOfferDetail'), {'old_price':2}, actor=self.actor, instance=item)
        with self.assertRaises(ValidationError):
            delete(model('FeelOfferDetail').objects.filter(pk=item.pk), self.actor)

    def test_limit_duplicate_and_null_records_remain(self):
        for name, field, value in [('KindLimit','old_kind',1),('NoLimit','old_kind',2),('Limit','old_emp_id','E')]:
            for _ in range(2):
                write(model(name), {field:value}, actor=self.actor)
            self.assertEqual(model(name).objects.count(),2)
