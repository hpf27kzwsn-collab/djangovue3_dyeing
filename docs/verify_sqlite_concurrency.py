"""在项目内独立 SQLite 副本中重现 API 与调度模型并发写入。"""
import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import sleep

root = Path(__file__).resolve().parents[1]
work = root / 'runtime' / 'sqlite-concurrency'
work.mkdir(exist_ok=True)
shutil.copy2(root / 'backend' / 'db.sqlite3', work / 'db.sqlite3')
os.environ['DJANGO_BASE_DIR'] = str(work)
os.environ['DJANGO_SETTINGS_MODULE'] = 'application.settings'
sys.path.insert(0, str(root / 'backend'))
import django
django.setup()
from django.db import connections, transaction
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from system.models import Post

interval = IntervalSchedule.objects.create(every=1, period='days')
task = PeriodicTask.objects.create(name='SQLite 并发验收', task='system.tasks.demo_task', interval=interval)

def scheduler():
    for index in range(20):
        with transaction.atomic():
            row = PeriodicTask.objects.get(pk=task.pk)
            sleep(.005)
            row.description = str(index)
            row.save()
    connections.close_all()

def api_write():
    for index in range(20):
        with transaction.atomic():
            row = Post.objects.create(name='并发验收', code='concurrency-'+str(index))
            sleep(.005)
            row.delete()
    connections.close_all()

with ThreadPoolExecutor(max_workers=2) as pool:
    jobs = [pool.submit(scheduler), pool.submit(api_write)]
    for job in jobs:
        job.result()
print('SQLite IMMEDIATE：调度/API 各 20 次真实并发事务通过')
task.delete()
interval.delete()
connections.close_all()
