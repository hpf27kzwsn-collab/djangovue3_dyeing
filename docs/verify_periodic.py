"""运行前启动 Redis、worker 与 beat；只创建并清理本脚本自己的任务。"""
import os
import sys
import json
import time
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'application.settings'
import django
django.setup()
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from django_celery_results.models import TaskResult

clock = ClockedSchedule.objects.create(clocked_time=timezone.now()+timedelta(seconds=5))
marker = 'djangovue3 定时调度实测-'+str(clock.pk)
task = PeriodicTask.objects.create(name='实施验证-'+str(clock.pk), task='system.tasks.demo_task',
    clocked=clock, one_off=True, kwargs=json.dumps({'text':marker}, ensure_ascii=False))
for _ in range(30):
    result = next((item for item in TaskResult.objects.filter(status='SUCCESS') if json.loads(item.result)==marker),None)
    if result:
        print('数据库定时任务执行成功：'+result.task_id)
        result.delete()
        break
    time.sleep(1)
else:
    raise RuntimeError('30 秒内没有收到定时任务结果')
task.delete()
clock.delete()
