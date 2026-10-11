import json
from pathlib import Path
from types import SimpleNamespace
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction
from system.models import Users
from system.catalog import ENTITIES
from system.views import view_for


class Command(BaseCommand):
    help = '导入 init_data 导出的业务 JSON，按主键或指定唯一字段创建/更新；--reset 明确重建该模型数据'

    def add_arguments(self, parser):
        parser.add_argument('model', help='app_label.ModelName')
        parser.add_argument('file')
        parser.add_argument('--unique-fields', nargs='+')
        parser.add_argument('--reset', action='store_true')
        parser.add_argument('--user', default='superadmin')

    @transaction.atomic
    def handle(self, *args, **options):
        model = apps.get_model(options['model'])
        entity = next(key for key, value in ENTITIES.items() if value is model)
        user = Users.objects.get(username=options['user'])
        request = SimpleNamespace(user=user, query_params={})
        serializer_class = view_for(entity, model).serializer_class
        records = json.loads(Path(options['file']).read_text(encoding='utf-8'))
        keys = options['unique_fields'] or [model._meta.pk.name]
        if options['reset']:
            model.objects.all().delete()
        created = updated = 0
        for row in records:
            lookup = {key: row[key] for key in keys}
            instance = model.objects.filter(**lookup).get() if model.objects.filter(**lookup).exists() else None
            serializer = serializer_class(instance, data=row, partial=instance is not None, context={'request':request})
            serializer.is_valid(raise_exception=True)
            audit = {}
            if hasattr(model, 'creator'):
                audit = {'modifier':user}
                if instance is None:
                    audit.update(creator=user, dept_belong_id=user.dept_id)
            if instance is None and model._meta.pk.name in row:
                audit[model._meta.pk.name] = row[model._meta.pk.name]
            serializer.save(**audit)
            if instance is None: created += 1
            else: updated += 1
        self.stdout.write(f'导入完成：新增 {created}，更新 {updated}')
