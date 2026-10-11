from unittest.mock import patch
from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient
from system.models import Users, Dept, Role, Dictionary, Menu, MenuButton, RoleMenuButtonPermission, MessageCenterTargetUser


class ReauditTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('init_data', verbosity=0)

    def setUp(self):
        self.client = APIClient()
        self.admin = Users.objects.get(username='superadmin')
        self.client.force_authenticate(self.admin)

    def test_dictionary_child_creation_and_root_list(self):
        root = Dictionary.objects.create(label='测试字典',value='reaudit-root')
        result = self.client.post('/api/system/dictionary/', {'parent':root.pk,'label':'子项','value':'first'}, format='json')
        self.assertEqual(result.status_code,200,result.data)
        child = Dictionary.objects.get(pk=result.data['data']['id'])
        self.assertTrue(child.is_value)
        self.assertIn('first',[row['value'] for row in self.client.get('/api/dictionary/',{'key':root.value}).data['data']])
        self.assertEqual(self.client.get('/api/system/dictionary/',{'parent':root.pk}).data['total'],1)
        self.assertNotIn(child.pk,[row['id'] for row in self.client.get('/api/system/dictionary/',{'limit':100}).data['data']])

    def test_protected_delete_preserves_department_users_and_dictionary_children(self):
        dept = Dept.objects.create(name='有用户的部门')
        user = Users.objects.create_user(username='protected-member',dept=dept)
        root = Dictionary.objects.create(value='protected-root')
        child = Dictionary.objects.create(parent=root,value='child',is_value=True)
        for entity,item in [('dept',dept),('dictionary',root)]:
            result=self.client.delete(f'/api/system/{entity}/{item.pk}/')
            self.assertEqual(result.status_code,400,result.data)
        user.refresh_from_db()
        self.assertEqual(user.dept,dept)
        self.assertTrue(Dictionary.objects.filter(pk=child.pk).exists())

    def test_patch_does_not_change_password_and_reset_is_explicit(self):
        user=Users.objects.create_user(username='password-member',password='old',pwd_change_count=4)
        result=self.client.patch(f'/api/system/user/{user.pk}/',{'name':'新姓名','password':'unexpected'},format='json')
        self.assertEqual(result.status_code,200,result.data)
        user.refresh_from_db()
        self.assertTrue(user.check_password('old'))
        self.assertEqual(user.pwd_change_count,4)
        result=self.client.post(f'/api/system/user/{user.pk}/reset_password/',{'password':'new','password_confirm':'new'},format='json')
        self.assertEqual(result.status_code,200,result.data)
        user.refresh_from_db()
        self.assertTrue(user.check_password('new'))
        self.assertEqual(user.pwd_change_count,4)
        fields=self.client.get('/api/meta/user/').data['data']['fields']
        self.assertFalse(next(row for row in fields if row['key']=='password')['is_update'])

    def test_user_list_excludes_root_and_searches_relation_names_without_duplicates(self):
        dept=Dept.objects.create(name='研发检索部门')
        user=Users.objects.create_user(username='search-member',dept=dept)
        user.role.set([Role.objects.create(name='研发检索甲',key='search-a'),Role.objects.create(name='研发检索乙',key='search-b')])
        result=self.client.get('/api/system/user/',{'search':'研发检索'})
        self.assertEqual(result.data['total'],1)
        self.assertEqual(result.data['data'][0]['id'],user.pk)
        self.assertNotIn('is_superuser',result.data['data'][0])
        self.assertEqual(self.client.get('/api/system/user/',{'username':'superadmin'}).data['total'],0)

    def test_account_mobile_unique_and_organization_fields(self):
        other=Users.objects.create_user(username='phone-owner',mobile='12345')
        result=self.client.patch('/api/account/',{'mobile':other.mobile},format='json')
        self.assertEqual(result.status_code,400,result.data)
        account=self.client.get('/api/account/').data['data']['user']
        self.assertEqual(account['dept_name'],'总公司')
        self.assertEqual(account['role_info'][0]['key'],'admin')

    def test_nullable_profile_organization_and_dictionary_fields(self):
        result=self.client.patch('/api/account/',{'email':None,'mobile':None,'avatar':None,'gender':None},format='json')
        self.assertEqual(result.status_code,200,result.data)
        dept=self.client.post('/api/system/dept/',{'name':'空资料部门','key':None,'owner':None,'phone':None,'email':None,'status':None},format='json')
        self.assertEqual(dept.status_code,200,dept.data)
        result=self.client.post('/api/system/dictionary/',{'label':None,'value':None,'color':None,'remark':None,'sort':None},format='json')
        self.assertEqual(result.status_code,200,result.data)
        user=Users.objects.create_user(username='default-display-name')
        self.assertEqual(user.name,user.username)
        self.client.post('/api/system/dept/',{'name':'编码一','key':'same-code'},format='json')
        duplicate=self.client.post('/api/system/dept/',{'name':'编码二','key':'same-code'},format='json')
        self.assertEqual(duplicate.status_code,400,duplicate.data)

    def test_button_generation_uses_actual_resource_and_keeps_creator(self):
        menu=Menu.objects.create(name='自定义入口',component_name='custom-post',web_path='/custom/positions')
        result=self.client.post('/api/system/menu_button/batch_create/',{'menu':menu.pk,'entity':'post'},format='json')
        self.assertEqual(result.status_code,200,result.data)
        button=MenuButton.objects.get(value='custom-post:batch-update-put')
        self.assertEqual(button.api,'/api/system/post/batch_update/')
        creator=Users.objects.create_user(username='button-creator')
        button.creator=creator;button.save()
        self.client.post('/api/system/menu_button/batch_create/',{'menu':menu.pk,'entity':'post'},format='json')
        button.refresh_from_db();self.assertEqual(button.creator,creator)
        role=Role.objects.create(name='批量权限',key='batch-permission')
        creator.role.add(role)
        RoleMenuButtonPermission.objects.create(role=role,menu_button=button,data_range=3)
        self.client.force_authenticate(creator)
        self.assertEqual(self.client.put('/api/system/post/batch_update/',[],format='json').status_code,200)

    def test_runtime_dictionary_changes_metadata_label_value_and_color(self):
        child=Dictionary.objects.get(parent__value='gender',value='1')
        child.label='字典中的男';child.color='#123456';child.save()
        fields=self.client.get('/api/meta/user/').data['data']['fields']
        gender=next(row for row in fields if row['key']=='gender')
        self.assertEqual(next(option for option in gender['options'] if option['value']==1),{'label':'字典中的男','value':1.0,'color':'#123456'})
        self.assertEqual(next(row for row in fields if row['key']=='role')['options'],[])
        self.assertEqual(next(row for row in fields if row['key']=='role')['remote']['entity'],'role')
        models=self.client.get('/api/system/column/get_models/')
        self.assertEqual(models.status_code,200,models.data)
        resources=self.client.get('/api/meta/menu_button/').data['data']['resources']
        self.assertIn('post',[row['entity'] for row in resources])

    def test_creator_display_respects_creator_field_permission(self):
        from system.models import Post, MenuField, FieldPermission
        menu=Menu.objects.get(component_name='post')
        field=MenuField.objects.create(menu=menu,model='system.Post',field_name='creator',title='创建人')
        role=Role.objects.create(name='创建人不可见',key='creator-hidden')
        user=Users.objects.create_user(username='creator-reader')
        user.role.add(role)
        RoleMenuButtonPermission.objects.create(role=role,menu_button=MenuButton.objects.get(value='post:list'),data_range=3)
        FieldPermission.objects.create(role=role,field=field,is_query=False,is_create=False,is_update=False)
        Post.objects.create(name='权限展示',code='private-creator',creator=self.admin)
        self.client.force_authenticate(user)
        row=self.client.get('/api/system/post/').data['data'][0]
        self.assertNotIn('creator',row)
        self.assertNotIn('creator_name',row)
        self.assertNotIn('creator_label',row)

    def test_receipt_sender_audit_and_detail_read(self):
        user=Users.objects.create_user(username='inbox-recipient')
        with patch('system.notifications.Redis.from_url'):
            message=self.client.post('/api/system/message_center/',{'title':'审计消息','content':'正文','target_user':[user.pk]},format='json')
        self.assertEqual(message.status_code,200,message.data)
        receipt=MessageCenterTargetUser.objects.get(users=user)
        self.assertEqual(receipt.creator,self.admin)
        self.assertEqual(receipt.dept_belong,self.admin.dept)
        self.client.force_authenticate(user)
        inbox=self.client.get('/api/inbox/',{'id':receipt.pk}).data['data']
        self.assertEqual(inbox['messages'][0]['sender'],'超级管理员')
        self.assertFalse(inbox['messages'][0]['is_read'])
        with patch('system.notifications.Redis.from_url'):
            self.client.post('/api/inbox/',{'ids':[receipt.pk]},format='json')
        receipt.refresh_from_db()
        self.assertTrue(receipt.is_read)
        self.assertEqual(receipt.modifier,user)
        self.client.force_authenticate(self.admin)
        self.assertEqual(self.client.get('/api/inbox/',{'id':receipt.pk}).status_code,404)
