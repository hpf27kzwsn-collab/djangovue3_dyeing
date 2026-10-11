from importlib import import_module
from io import BytesIO
from django.apps import apps
from django.core.management import call_command
from django.test import TestCase
from openpyxl import load_workbook
from rest_framework.test import APIClient
from core.permissions import field_access
from system.models import Users, Role, Menu, MenuField, FieldPermission, RoleMenuButtonPermission, MenuButton
from unittest import skipUnless


class IdentityMigrationTests(TestCase):
    def test_qualifying_existing_definition_keeps_grant_primary_keys(self):
        menu=Menu.objects.create(name='迁移菜单')
        role=Role.objects.create(name='迁移角色',key='identity-migration')
        field=MenuField.objects.create(menu=menu,model='Post',field_name='name',title='岗位名称')
        grant=FieldPermission.objects.create(role=role,field=field)
        migrate=import_module('system.migrations.0017_model_identity').qualify_models
        class Schema:
            connection=type('Connection',(),{'alias':'default'})()
        migrate(apps,Schema())
        field.refresh_from_db();grant.refresh_from_db()
        self.assertEqual(field.model,'system.Post')
        self.assertEqual(grant.field_id,field.pk)
        self.assertEqual(MenuField.objects.count(),1)


@skipUnless(apps.is_installed('system.tests.twin_a'),'requires extension_settings')
class TwinApplicationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('init_data',verbosity=0)

    def test_actual_apps_crud_field_permissions_and_xlsx_are_isolated(self):
        from system.tests.twin_a.models import Twin as A
        from system.tests.twin_b.models import Twin as B
        client=APIClient();admin=Users.objects.get(username='superadmin');client.force_authenticate(admin)
        for entity,key,field in [('identity_a_twin','identity_a.Twin','only_a'),('identity_b_twin','identity_b.Twin','only_b')]:
            menu=Menu.objects.get(resource=entity)
            matched=client.post('/api/system/column/auto_match_fields/',{'menu':menu.pk,'model':key},format='json')
            self.assertEqual(matched.status_code,200,matched.data)
            self.assertTrue(MenuField.objects.filter(menu=menu,model=key,field_name=field).exists())
            created=client.post(f'/api/system/{entity}/',{'name':key,field:field},format='json')
            self.assertEqual(created.status_code,200,created.data)
        role=Role.objects.create(name='独立模型',key='identity-role')
        actor=Users.objects.create_user(username='identity-actor');actor.role.add(role)
        field=MenuField.objects.get(model='identity_a.Twin',field_name='name')
        FieldPermission.objects.create(role=role,field=field,is_query=True,is_create=True,is_update=True)
        self.assertTrue(field_access(actor,A)['name']['is_query'])
        self.assertFalse(field_access(actor,B)['name']['is_query'])
        for entity in ['identity_a_twin','identity_b_twin']:
            for action in ['list','export-get']:
                RoleMenuButtonPermission.objects.create(role=role,menu_button=MenuButton.objects.get(value=f'{entity}:{action}'),data_range=3)
        client.force_authenticate(actor)
        a=client.get('/api/system/identity_a_twin/').data['data'][0]
        b=client.get('/api/system/identity_b_twin/').data['data'][0]
        self.assertIn('name',a);self.assertNotIn('name',b)
        response=client.get('/api/system/identity_b_twin/export/')
        book=load_workbook(BytesIO(b''.join(response.streaming_content)))
        self.assertNotIn('名称',list(book['数据'].values)[0])
        book.close()

    def test_tree_target_code_differs_from_selected_business_name(self):
        from examples.catalogue.models import Entry
        admin=Users.objects.get(username='superadmin')
        client=APIClient();client.force_authenticate(admin)
        parent=Entry.objects.create(code='parent-code',name='parent-name')
        Entry.objects.create(code='child-code',name='child-name',parent=parent)
        from system.models import SystemConfig
        item=SystemConfig.objects.create(title='编码树',key='code-tree',form_item_type=13,
            setting={'table':'example_catalogue_entry','primarykey':'name','field':'name','treeField':'parent'})
        url=f'/api/system/system_config/{item.pk}/table_data/'
        row=client.get(url,{'parent':'null'}).data['data'][0]
        self.assertEqual(row['_tree_id'],'parent-code')
        self.assertTrue(row['has_children'])
        children=client.get(url,{'parent':row['_tree_id']}).data['data']
        self.assertEqual(children[0]['name'],'child-name')
