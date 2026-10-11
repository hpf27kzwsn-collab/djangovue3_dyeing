from datetime import timedelta
from unittest.mock import patch
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users, Dept, Role, Menu, MenuField, MenuButton, RoleMenuPermission, RoleMenuButtonPermission, FieldPermission, Area


class AuditTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('init_data', verbosity=0)

    def setUp(self):
        self.client=APIClient()
        self.root=Users.objects.get(username='superadmin')
        self.client.force_authenticate(self.root)

    def test_login_updates_time_and_username_wins_identity_collision(self):
        old=timezone.now()-timedelta(days=1)
        self.root.last_login=old
        self.root.save(update_fields=['last_login'])
        Users.objects.create_user(username='collision',email='superadmin',password='other')
        self.client.force_authenticate(None)
        result=self.client.post('/api/login/',{'username':'superadmin','password':'admin123456'},format='json')
        self.assertEqual(result.status_code,200)
        self.root.refresh_from_db()
        self.assertGreater(self.root.last_login,old)
        Users.objects.create_user(username='duplicate1',email='shared@example.com',password='other')
        Users.objects.create_user(username='duplicate2',email='shared@example.com',password='other')
        result=self.client.post('/api/login/',{'username':'shared@example.com','password':'other'},format='json')
        self.assertEqual(result.status_code,400)
        self.assertIn('多个账号',result.data['msg'])

    def test_department_children_statistics_paths_and_append_order(self):
        parent=Dept.objects.create(name='父部门',sort=10)
        child=self.client.post('/api/system/dept/',{'name':'子部门','parent':parent.pk},format='json').data['data']
        another=self.client.post('/api/system/dept/',{'name':'后续部门','parent':parent.pk},format='json').data['data']
        self.assertEqual((child['sort'],another['sort']),(1,2))
        first=Users.objects.create_user(username='parent-user',dept=parent,dept_belong=parent,gender=1)
        second=Users.objects.create_user(username='child-user',dept_id=child['id'],dept_belong_id=child['id'],gender=2)
        result=self.client.get('/api/system/user/',{'dept':parent.pk,'include_children':'true'}).data['data']
        self.assertEqual({row['id'] for row in result},{first.pk,second.pk})
        self.assertEqual(next(row for row in result if row['id']==second.pk)['dept_path'],'父部门 / 子部门')
        self.assertEqual(self.client.get(f'/api/system/dept/{parent.pk}/info/').data['data']['count'],1)
        summary=self.client.get(f'/api/system/dept/{parent.pk}/info/',{'include_children':'true'}).data['data']
        self.assertEqual(summary['count'],2)
        self.assertEqual(summary['gender'],{'0':0,'1':1,'2':1})

    def test_role_name_and_menu_field_business_unique_rules(self):
        result=self.client.post('/api/system/role/',{'name':'同名角色','key':'unique-one'},format='json')
        self.assertEqual(result.status_code,200)
        result=self.client.post('/api/system/role/',{'name':'同名角色','key':'unique-two'},format='json')
        self.assertEqual(result.status_code,400)
        menu=Menu.objects.get(component_name='post')
        data={'menu':menu.pk,'model':'system.Post','field_name':'name','title':'岗位名'}
        self.assertEqual(self.client.post('/api/system/column/',data,format='json').status_code,400)
        data.update(model='AbsentModel',field_name='new_field')
        self.assertEqual(self.client.post('/api/system/column/',data,format='json').status_code,400)

    def test_role_users_paginate_and_increment_without_affecting_other_members(self):
        role=Role.objects.create(name='授权验收角色',key='audit-role')
        users=[Users.objects.create_user(username=f'grantee-{n}',name=f'姓名{n}') for n in range(3)]
        users[0].role.add(role)
        path=f'/api/system/role/{role.pk}/users/'
        result=self.client.get(path,{'authorized':'0','limit':1}).data
        self.assertEqual(result['total'],2)
        self.assertEqual(len(result['data']),1)
        self.assertEqual(self.client.put(path,{'operation':'add','ids':[users[1].pk]},format='json').status_code,200)
        self.assertTrue(users[0].role.filter(pk=role.pk).exists())
        self.assertTrue(users[1].role.filter(pk=role.pk).exists())
        self.client.put(path,{'operation':'remove','ids':[users[0].pk]},format='json')
        self.assertFalse(users[0].role.filter(pk=role.pk).exists())
        self.assertTrue(users[1].role.filter(pk=role.pk).exists())
        self.assertEqual(self.client.put(path,{'operation':'add','ids':[self.root.pk]},format='json').status_code,404)

    def test_unchanged_grants_retain_identity_and_timestamps(self):
        role=Role.objects.create(name='差量授权',key='grant-diff')
        menu=Menu.objects.get(component_name='post')
        button=MenuButton.objects.get(value='post:list')
        field=MenuField.objects.get(menu=menu,model='system.Post',field_name='name')
        mg=RoleMenuPermission.objects.create(role=role,menu=menu)
        bg=RoleMenuButtonPermission.objects.create(role=role,menu_button=button,data_range=2)
        fg=FieldPermission.objects.create(role=role,field=field)
        payload={'menus':[menu.pk],'buttons':[{'id':button.pk,'data_range':2,'dept':[]}],
                 'fields':[{'id':field.pk,'is_query':True,'is_create':True,'is_update':True}]}
        original=[(row.pk,row.create_datetime,row.update_datetime) for row in [mg,bg,fg]]
        self.assertEqual(self.client.put(f'/api/system/role/{role.pk}/permissions/',payload,format='json').status_code,200)
        for row,expected in zip([mg,bg,fg],original):
            row.refresh_from_db()
            self.assertEqual((row.pk,row.create_datetime,row.update_datetime),expected)

    def test_region_lazy_children_and_health_and_initializer_hook(self):
        parent=Area.objects.create(code='A',name='上级区域')
        Area.objects.create(code='B',name='子区域',pcode=parent)
        rows=self.client.get('/api/system/area/children/').data['data']
        self.assertEqual(rows[0]['children_count'],1)
        self.assertTrue(rows[0]['has_children'])
        child=self.client.get('/api/system/area/children/',{'pcode':'A'}).data['data'][0]
        self.assertEqual(child['code'],'B')
        self.assertEqual(child['pcode_name'],'上级区域')
        parent_field=next(row for row in self.client.get('/api/meta/area/').data['data']['fields'] if row['key']=='pcode')
        self.assertEqual(parent_field['options'],[])
        self.assertEqual(parent_field['remote']['pk'],'code')
        self.assertEqual(self.client.get('/healthz').json(),{'status':'ok'})
        from django.db import connection
        self.assertEqual(self.client.get('/readiness').json()['database'],connection.vendor)
        with patch('application.plugins.INITIALIZERS',['example.load']),patch('django.utils.module_loading.import_string') as loader:
            call_command('init_data',verbosity=0)
            loader.assert_called_once_with('example.load')
            loader.return_value.assert_called_once_with()
