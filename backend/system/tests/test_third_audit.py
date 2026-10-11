from unittest.mock import patch
from django.apps import apps
from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient
from system.models import Users, Role, Dept, Menu, MenuButton, MenuField, RoleMenuButtonPermission, Post, SystemConfig


class ThirdAuditTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('init_data', verbosity=0)

    def setUp(self):
        self.client=APIClient()
        self.admin=Users.objects.get(username='superadmin')
        self.client.force_authenticate(self.admin)

    def test_custom_menu_keeps_prefix_and_records_actual_resource(self):
        menu=Menu.objects.create(name='自定义岗位',component='system/Resource',component_name='custom_post',web_path='/custom-post')
        result=self.client.post('/api/system/menu_button/batch_create/',{'menu':menu.pk,'entity':'post'},format='json')
        self.assertEqual(result.status_code,200,result.data)
        menu.refresh_from_db()
        self.assertEqual(menu.resource,'post')
        self.assertEqual(menu.component_name,'custom_post')
        self.assertEqual(menu.modifier,self.admin)
        button=MenuButton.objects.get(value='custom_post:list')
        self.assertEqual(button.api,'/api/system/post/')
        self.assertEqual(self.client.get('/api/meta/'+menu.resource+'/').status_code,200)
        self.assertTrue(any(row['value']=='post' for row in next(row for row in self.client.get('/api/meta/menu/').data['data']['fields'] if row['key']=='resource')['options']))

    def test_child_list_is_usable_without_parent_detail(self):
        actor=Users.objects.create_user(username='child-only')
        role=Role.objects.create(key='child-only',name='子页面角色')
        actor.role.add(role)
        button=MenuButton.objects.get(value='menu_button:list')
        RoleMenuButtonPermission.objects.create(role=role,menu_button=button,data_range=3)
        self.client.force_authenticate(actor)
        self.assertEqual(self.client.get('/api/system/menu_button/',{'menu':button.menu_id}).status_code,200)
        self.assertEqual(self.client.get(f'/api/system/menu/{button.menu_id}/').status_code,403)

    def test_multi_relation_query_returns_union_once_and_empty_query_is_unfiltered(self):
        one=Role.objects.create(key='multi-a',name='甲')
        two=Role.objects.create(key='multi-b',name='乙')
        both=Users.objects.create_user(username='multi-both');both.role.set([one,two])
        first=Users.objects.create_user(username='multi-first');first.role.add(one)
        Users.objects.create_user(username='unrelated')
        result=self.client.get('/api/system/user/',{'role__in':f'{one.pk},{two.pk}'})
        self.assertEqual(result.status_code,200,result.data)
        self.assertEqual(result.data['total'],2)
        self.assertEqual({row['id'] for row in result.data['data']},{both.pk,first.pk})

    def test_boolean_in_and_isnull_queries(self):
        active=Role.objects.create(key='bool-active',name='活跃',status=True)
        inactive=Role.objects.create(key='bool-inactive',name='停用',status=False)
        result=self.client.get('/api/system/role/',{'status__in':'true,false','key__in':'bool-active,bool-inactive'})
        self.assertEqual(result.status_code,200,result.data)
        self.assertEqual({row['id'] for row in result.data['data']},{active.pk,inactive.pk})
        self.assertEqual(self.client.get('/api/system/role/',{'status__in':'false','key__in':'bool-active,bool-inactive'}).data['total'],1)
        self.assertEqual(self.client.get('/api/system/menu/',{'parent__isnull':'true'}).status_code,200)

    def test_departments_are_marked_per_actor_button(self):
        actor=Users.objects.create_user(username='department-actor')
        role=Role.objects.create(key='department-actor',name='授权者')
        actor.role.add(role)
        dept=Dept.objects.create(name='指定部门')
        target=Role.objects.get(key='admin')
        RoleMenuButtonPermission.objects.create(role=role,menu_button=MenuButton.objects.get(value='role:permissions-get'),data_range=3)
        grant=RoleMenuButtonPermission.objects.create(role=role,menu_button=MenuButton.objects.get(value='post:list'),data_range=4)
        grant.dept.add(dept)
        self.client.force_authenticate(actor)
        result=self.client.get(f'/api/system/role/{target.pk}/permissions/')
        self.assertEqual(result.status_code,200,result.data)
        buttons={row['id']:row for row in result.data['data']['buttons']}
        self.assertEqual(buttons[grant.menu_button_id]['assignable_departments'],[dept.pk])
        self.assertEqual(buttons[MenuButton.objects.get(value='post:detail').pk]['assignable_departments'],[])

    def test_menu_field_model_is_selected_from_directory(self):
        field=next(row for row in self.client.get('/api/meta/column/').data['data']['fields'] if row['key']=='model')
        self.assertEqual(field['kind'],'select')
        self.assertTrue(any(row['value']=='system.Post' for row in field['options']))
        menu=Menu.objects.create(name='手工字段测试',component_name='manual-field')
        result=self.client.post('/api/system/column/',{'menu':menu.pk,'model':'system.Post','field_name':'code','title':'手工代码'},format='json')
        self.assertEqual(result.status_code,200,result.data)

    def test_crud_order_virtual_and_ui_exclusion_do_not_remove_api_fields(self):
        options={'Post':{'crud_fields':['alias','name','code'],'exclude_fields':['code'],'fields':{'alias':{'title':'岗位别名','source':'name'}},'crud_options':{'table':{'stripe':True}}}}
        with patch.object(apps.get_app_config('system'),'resource_options',options,create=True):
            post=Post.objects.create(name='研发岗',code='THIRD')
            meta=self.client.get('/api/meta/post/').data['data']
            self.assertEqual([field['key'] for field in meta['fields']],['alias','name'])
            self.assertTrue(meta['fields'][0]['readonly'])
            self.assertTrue(meta['crud_options']['table']['stripe'])
            record=self.client.get(f'/api/system/post/{post.pk}/').data['data']
            self.assertEqual(record['code'],'THIRD')
            self.assertEqual(record['alias'],'研发岗')
            actor=Users.objects.create_user(username='virtual-reader')
            role=Role.objects.create(key='virtual-reader',name='只读接口')
            actor.role.add(role)
            RoleMenuButtonPermission.objects.create(role=role,menu_button=MenuButton.objects.get(value='post:detail'),data_range=3)
            self.client.force_authenticate(actor)
            record=self.client.get(f'/api/system/post/{post.pk}/').data['data']
            self.assertNotIn('alias',record)
            self.assertNotIn('name',record)

    def test_configuration_reverse_relation_matches_scalar_and_array_only_for_bound_table(self):
        post=Post.objects.create(name='反查岗',code='REL')
        groups=[SystemConfig.objects.create(key='reverse-'+str(i),title='反查'+str(i)) for i in range(3)]
        SystemConfig.objects.create(parent=groups[0],key='linked',form_item_type=13,setting={'table':'post'},value=post.pk)
        SystemConfig.objects.create(parent=groups[1],key='linked',form_item_type=14,setting={'table':'post'},value=[post.pk])
        SystemConfig.objects.create(parent=groups[2],key='linked',form_item_type=13,setting={'table':'dept'},value=post.pk)
        result=self.client.get('/api/system/system_config/relation_info/',{'var_name':'linked','table':'post','relation_ids':str(post.pk)})
        self.assertEqual(result.status_code,200,result.data)
        self.assertEqual({row['group']['id'] for row in result.data['data']},{groups[0].pk,groups[1].pk})
        self.assertEqual(len(result.data['data'][0]['children']),1)
