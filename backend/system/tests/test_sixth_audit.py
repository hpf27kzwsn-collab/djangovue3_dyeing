from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient
from system.models import Users, Dept, Menu, Dictionary, SystemConfig, Role, MenuButton, RoleMenuButtonPermission, MenuField, FieldPermission


class SixthAuditTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('init_data',verbosity=0)

    def setUp(self):
        self.user=Users.objects.get(username='superadmin')
        self.client=APIClient()
        self.client.force_authenticate(self.user)

    def test_first_password_empty_and_mismatch_do_not_write_or_count(self):
        original=self.user.password
        for password,confirm in [('', ''),('new','other')]:
            response=self.client.post('/api/password/first/',{'new_password':password,'new_password_confirm':confirm},format='json')
            self.assertEqual(response.status_code,400,response.data)
            self.user.refresh_from_db()
            self.assertEqual(self.user.password,original)
            self.assertEqual(self.user.pwd_change_count,0)
        response=self.client.post('/api/password/first/',{'new_password':' x ','new_password_confirm':' x '},format='json')
        self.assertEqual(response.status_code,200,response.data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(' x '))
        self.assertEqual(self.user.pwd_change_count,1)

    def test_personal_password_normal_rules(self):
        for new in ['', 'admin123456']:
            response=self.client.post('/api/password/',{'old_password':'admin123456','new_password':new,'new_password_confirm':new},format='json')
            self.assertEqual(response.status_code,400,response.data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('admin123456'))
        self.assertEqual(self.user.pwd_change_count,0)
        response=self.client.post('/api/password/',{'old_password':'admin123456','new_password':'new','new_password_confirm':'new'},format='json')
        self.assertEqual(response.status_code,200,response.data)

    def test_dictionary_declared_type_save_and_public_read(self):
        group=Dictionary.objects.create(label='测试',value='sixth-dictionary')
        endpoint='/api/system/dictionary/'
        for value in ['', 'abc']:
            response=self.client.post(endpoint,{'parent':group.pk,'label':'数字','value':value,'type':1},format='json')
            self.assertEqual(response.status_code,400,response.data)
            self.assertIn('value',response.data['data'])
        number=self.client.post(endpoint,{'parent':group.pk,'label':'零','value':'0','type':1},format='json')
        self.assertEqual(number.status_code,200,number.data)
        boolean=self.client.post(endpoint,{'parent':group.pk,'label':'否','value':'false','type':6},format='json')
        self.assertEqual(boolean.status_code,200,boolean.data)
        values=self.client.get('/api/dictionary/',{'key':group.value}).data['data']
        self.assertEqual([row['value'] for row in values],[0.0,False])
        text=Dictionary.objects.create(parent=group,is_value=True,label='文本',value='text')
        response=self.client.patch(f'{endpoint}{text.pk}/',{'type':1},format='json')
        self.assertEqual(response.status_code,400,response.data)
        text.refresh_from_db()
        self.assertEqual(text.type,0)

    def test_business_key_tree_nodes_are_separate_from_selection_value(self):
        parent=Dept.objects.create(name='业务父级',key='business-parent')
        child=Dept.objects.create(name='业务子级',key='business-child',parent=parent)
        item=SystemConfig.objects.create(key='sixth-tree',title='树',form_item_type=13,
            setting={'table':'dept','primarykey':'key','field':'name','treeField':'parent'})
        url=f'/api/system/system_config/{item.pk}/table_data/'
        roots=self.client.get(url,{'parent':'null'}).data['data']
        row=next(row for row in roots if row['key']==parent.key)
        self.assertEqual(row['_tree_id'],parent.pk)
        self.assertTrue(row['has_children'])
        children=self.client.get(url,{'parent':row['_tree_id']}).data['data']
        self.assertEqual(children[0]['key'],child.key)
        selected=self.client.get(url,{'key__in':child.key}).data['data']
        self.assertEqual(selected[0]['id'],child.pk)

    def test_department_default_explicit_root_and_actual_parent_append(self):
        parent=Dept.objects.create(name='父级',key='sixth-parent')
        Dept.objects.create(name='末尾',parent=parent,sort=25)
        self.user.dept=parent;self.user.save(update_fields=['dept'])
        created=self.client.post('/api/system/dept/',{'name':'默认部门','key':'sixth-default'},format='json')
        self.assertEqual(created.status_code,200,created.data)
        row=Dept.objects.get(pk=created.data['data']['id'])
        self.assertEqual((row.parent_id,row.dept_belong_id,row.sort),(parent.pk,row.pk,26))
        root=self.client.post('/api/system/dept/',{'name':'顶级部门','key':'sixth-root','parent':None},format='json')
        self.assertIsNone(root.data['data']['parent'])

    def test_sparse_sort_and_equal_sort_for_both_models(self):
        for entity,model in [('dept',Dept),('menu',Menu)]:
            parent=model.objects.create(name='排序父级')
            items=[model.objects.create(name=str(value),parent=parent,sort=value) for value in [10,20,20,90]]
            response=self.client.post(f'/api/system/{entity}/move_up/',{'id':items[1].pk},format='json')
            self.assertEqual(response.status_code,200,response.data)
            self.assertEqual(list(model.objects.filter(parent=parent).order_by('pk').values_list('sort',flat=True)),[20,10,20,90])
            self.client.post(f'/api/system/{entity}/move_down/',{'id':items[1].pk},format='json')
            self.assertEqual(list(model.objects.filter(parent=parent).order_by('pk').values_list('sort',flat=True)),[10,20,20,90])

    def test_ordinary_department_subtree_creation_stays_visible(self):
        parent=Dept.objects.create(name='普通角色部门',key='scoped-parent')
        role=Role.objects.create(name='部门管理',key='sixth-dept-manager')
        actor=Users.objects.create_user(username='scoped-actor',dept=parent,dept_belong=parent)
        actor.role.add(role)
        for action in ['list','add']:
            RoleMenuButtonPermission.objects.create(role=role,menu_button=MenuButton.objects.get(value=f'dept:{action}'),data_range=1)
        for field in MenuField.objects.filter(model='system.Dept'):
            FieldPermission.objects.create(role=role,field=field)
        self.client.force_authenticate(actor)
        response=self.client.post('/api/system/dept/',{'name':'新下级','key':'scoped-child'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        child=Dept.objects.get(key='scoped-child')
        self.assertEqual(child.parent_id,parent.pk)
        rows=self.client.get('/api/system/dept/').data['data']
        self.assertIn(child.pk,[row['id'] for row in rows])

    def test_menu_parent_catalog_and_qualified_model_metadata(self):
        menu=Menu.objects.create(name='普通叶子',web_path='/sixth-leaf')
        metadata=self.client.get('/api/meta/menu/').data['data']['fields']
        options=next(row for row in metadata if row['key']=='parent')['options']
        self.assertNotIn(menu.pk,[row['value'] for row in options])
        options=next(row for row in self.client.get('/api/meta/column/').data['data']['fields'] if row['key']=='model')['options']
        self.assertIn('system.Post',[row['value'] for row in options])
