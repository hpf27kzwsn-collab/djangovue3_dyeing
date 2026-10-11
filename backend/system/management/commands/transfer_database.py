"""离线搬迁到空目标数据库；配置切换本身不触发此命令。"""
from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import datetime, time
from contextlib import contextmanager
from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.signals import pre_save, post_save
from django.db import connections
from django_celery_beat.models import PeriodicTasks, PeriodicTask, IntervalSchedule, CrontabSchedule, SolarSchedule, ClockedSchedule
from application.database_config import database_settings


class TransferEncoder(DjangoJSONEncoder):
    def default(self, value):
        if isinstance(value, (datetime, time)):
            return value.isoformat()
        return super().default(value)


@contextmanager
def loading_schedule_fixture():
    # beat 的接收器忽略 raw/using，会写默认库。搬迁保留 fixture 中的调度时间，不触发这些写入。
    receivers = [(pre_save, PeriodicTasks.changed, PeriodicTask)] + [
        (post_save, PeriodicTasks.update_changed, model)
        for model in [IntervalSchedule, CrontabSchedule, SolarSchedule, ClockedSchedule]]
    disconnected = [(signal, receiver, model) for signal, receiver, model in receivers
                    if signal.disconnect(receiver, sender=model)]
    try:
        yield
    finally:
        for signal, receiver, model in disconnected:
            signal.connect(receiver, sender=model)


class Command(BaseCommand):
    help = '将源配置的数据复制到空目标库；先停止网页、worker、beat。附件仍使用原 media 目录。'

    def add_arguments(self, parser):
        parser.add_argument('--source-config', required=True)
        parser.add_argument('--target-config', required=True)

    def handle(self, *args, **options):
        for alias, key in [('transfer_source', 'source_config'), ('transfer_target', 'target_config')]:
            path = Path(options[key]).resolve(strict=True)
            database = database_settings(settings.BASE_DIR, path, use_environment=False)
            connections.databases[alias] = {**connections.databases['default'], **database}
        source, target = 'transfer_source', 'transfer_target'
        source_db, target_db = connections.databases[source], connections.databases[target]
        identity = lambda db: (db['ENGINE'], str(db['NAME']), db.get('HOST', ''), str(db.get('PORT', '')))
        if identity(source_db) == identity(target_db):
            raise CommandError('源库和目标库相同，不能向自身搬迁。')
        # ContentType/Permission 由 migrate 创建，使用自然键重新关联其主键。
        excluded = {'contenttypes.ContentType', 'auth.Permission'}
        models = [model for model in apps.get_models() if model._meta.managed and not model._meta.proxy
                  and model._meta.label not in excluded]
        try:
            call_command('migrate', database=target, interactive=False, stdout=self.stdout)
            populated = [model._meta.label for model in models if model._base_manager.using(target).exists()]
            if populated:
                raise CommandError('目标库已有数据，请使用空目标库：' + '、'.join(populated))
            counts = {model._meta.label: model._base_manager.using(source).count() for model in models}
            with TemporaryDirectory(prefix='database-transfer-') as directory:
                fixture = Path(directory) / 'records.json'
                app_models = [(app, [model for model in models if model._meta.app_config is app])
                              for app in apps.get_app_configs()]
                ordered = serializers.sort_dependencies(app_models, allow_cycles=True)
                records = (record for model in ordered for record in
                           model._base_manager.using(source).order_by(model._meta.pk.name).iterator())
                with fixture.open('w', encoding='utf-8') as stream:
                    serializers.serialize('json', records, use_natural_foreign_keys=True,
                                          stream=stream, cls=TransferEncoder)
                with loading_schedule_fixture():
                    call_command('loaddata', str(fixture), database=target, stdout=self.stdout)
            actual = {model._meta.label: model._base_manager.using(target).count() for model in models}
            if counts != actual:
                raise CommandError('搬迁后的表记录数不同，请核对目标库；未修改源库或切换配置。')
            self.stdout.write(self.style.SUCCESS(f'搬迁完成：{sum(counts.values())} 条记录，{len(counts)} 张模型表。源库和配置未改动。'))
        finally:
            connections[source].close()
            connections[target].close()
