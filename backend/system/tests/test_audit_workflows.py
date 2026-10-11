from unittest.mock import patch
from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient
from system.models import Users, Dept, SystemConfig, MessageCenter, MessageCenterTargetUser


class AuditWorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('init_data',verbosity=0)

    def setUp(self):
        self.client=APIClient()
        self.user=Users.objects.get(username='superadmin')
        self.client.force_authenticate(self.user)

    def test_config_group_create_edit_delete_and_rollback(self):
        group=SystemConfig.objects.create(title='分组',key='audit-group')
        other=SystemConfig.objects.create(title='其他分组',key='audit-other')
        existing=SystemConfig.objects.create(title='旧项',key='old',parent=group,value=1)
        foreign=SystemConfig.objects.create(title='其他项',key='other',parent=other,value=2)
        result=self.client.put(f'/api/system/system_config/{group.pk}/content/',{'deleted':[existing.pk],'rows':[{'title':'新项','key':'new','value':False}]},format='json')
        self.assertEqual(result.status_code,200,result.data)
        new=SystemConfig.objects.get(parent=group,key='new')
        self.assertEqual(new.value,False)
        self.assertEqual(new.creator,self.user)
        self.assertFalse(SystemConfig.objects.filter(pk=existing.pk).exists())
        result=self.client.put(f'/api/system/system_config/{group.pk}/content/',{'deleted':[new.pk],'rows':[{'id':foreign.pk,'value':7}]},format='json')
        self.assertEqual(result.status_code,404)
        self.assertTrue(SystemConfig.objects.filter(pk=new.pk).exists())
        result=self.client.put(f'/api/system/system_config/{group.pk}/content/',{'deleted':[],'rows':[{'id':new.pk,'value':0}]},format='json')
        self.assertEqual(result.status_code,200,result.data)
        new.refresh_from_db()
        self.assertEqual(new.value,0)

    def test_association_configured_search_and_lazy_children(self):
        parent=Dept.objects.create(name='目标目录',key='search-parent')
        child=Dept.objects.create(name='匹配名称',key='different-key',parent=parent)
        item=SystemConfig.objects.create(title='关联',key='audit-association',setting={'table':'dept','treeField':'parent','searchField':[{'field':'name','search':True},{'field':'key','search':False}]})
        base=f'/api/system/system_config/{item.pk}/table_data/'
        result=self.client.get(base,{'search':'different-key'})
        self.assertEqual(result.status_code,200,result.data)
        self.assertEqual(result.data['total'],0)
        self.assertEqual(self.client.get(base,{'search':'匹配'}).data['data'][0]['id'],child.pk)
        roots=self.client.get(base,{'parent':'null'}).data['data']
        self.assertTrue(next(row for row in roots if row['id']==parent.pk)['has_children'])

    def test_actual_recipient_pagination_read_and_transaction_notification(self):
        message=MessageCenter.objects.create(title='明细',content='正文',target_type=3,creator=self.user)
        other=Users.objects.create_user(username='recipient')
        with patch('system.notifications.Redis.from_url') as factory:
            with self.captureOnCommitCallbacks(execute=True):
                MessageCenterTargetUser.objects.create(users=other,messagecenter=message)
                MessageCenterTargetUser.objects.create(users=self.user,messagecenter=message)
            self.assertEqual(factory.return_value.__enter__.return_value.publish.call_count,2)
        result=self.client.get(f'/api/system/message_center/{message.pk}/recipients/',{'limit':1})
        self.assertEqual(result.data['total'],2)
        self.assertEqual(len(result.data['data']),1)
        inbox=self.client.get('/api/inbox/',{'search':'明细','read':'false'}).data['data']
        self.assertEqual(inbox['total'],1)
        with patch('system.notifications.Redis.from_url') as factory:
            with self.captureOnCommitCallbacks(execute=True):
                self.client.post('/api/inbox/',{'ids':[inbox['messages'][0]['id']]},format='json')
            factory.return_value.__enter__.return_value.publish.assert_called_once_with(f'messages:{self.user.pk}','changed')
        self.assertEqual(self.client.get('/api/inbox/',{'read':'true'}).data['data']['total'],1)
