from django.core.management import call_command
from django.test import TransactionTestCase
from rest_framework.test import APIClient
from system.catalog import ENTITIES
from system.models import Menu, MenuField, Users
from datetime import timedelta
from unittest.mock import patch
from celery import Celery
from django.conf import settings
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django_celery_beat.schedulers import DatabaseScheduler


class SeedAndTaskFieldTests(TransactionTestCase):
    def setUp(self):
        # 调度器会清理连接并提交调度状态，需要真实事务而非 TestCase 的外层回滚事务。
        call_command('init_data',verbosity=0)
        self.client=APIClient()
        self.client.force_authenticate(Users.objects.get(username='superadmin'))

    def test_dispatched_schedule_state_survives_new_scheduler_instance(self):
        interval=IntervalSchedule.objects.create(every=60,period='seconds')
        task=PeriodicTask.objects.create(name='ninth-persist-dispatch',task='ninth.persistence.test',interval=interval,last_run_at=timezone.now()-timedelta(minutes=2))
        app=Celery('ninth-persistence')
        app.conf.beat_sync_every=settings.CELERY_BEAT_SYNC_EVERY
        scheduler=DatabaseScheduler(app=app,lazy=True)
        with patch.object(scheduler,'send_task') as send:
            scheduler.apply_async(scheduler.schedule[task.name])
        send.assert_called_once()
        task.refresh_from_db()
        self.assertEqual(task.total_run_count,1)
        reopened=DatabaseScheduler(app=app,lazy=True)
        restored=reopened.schedule[task.name]
        self.assertEqual(restored.last_run_at,task.last_run_at)
        self.assertFalse(restored.is_due().is_due)

    def test_seed_catalog_can_be_saved_through_required_route_form(self):
        self.assertEqual(dict(Menu.objects.filter(component_name__in=['system','tasks']).values_list('component_name','web_path')),{'system':'/system','tasks':'/tasks'})

    def test_registered_task_models_can_list_edit_and_match_field_permissions(self):
        catalogue=self.client.get('/api/system/column/get_models/').data['data']
        labels={item['key'] for item in catalogue}
        meta=self.client.get('/api/meta/column/').data['data']
        options={option['value'] for field in meta['fields'] if field['key']=='model' for option in field['options']}
        for entity in ['periodic_task','interval_schedule','crontab_schedule','clocked_schedule','solar_schedule','task_result']:
            with self.subTest(entity=entity):
                model=ENTITIES[entity]
                self.assertIn(model._meta.label,labels)
                self.assertIn(model._meta.label,options)
                field=MenuField.objects.filter(model=model._meta.label).first()
                response=self.client.patch(f'/api/system/column/{field.pk}/',{'description':'实际任务字段可编辑'},format='json')
                self.assertEqual(response.status_code,200,response.data)
                response=self.client.post('/api/system/column/auto_match_fields/',{'menu':field.menu_id,'model':model._meta.label},format='json')
                self.assertEqual(response.status_code,200,response.data)
