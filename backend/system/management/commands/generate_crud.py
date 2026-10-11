import json
from pathlib import Path
from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '基于 Django 模型生成序列化、CRUD 接口、路由和 Vue 页面源码'

    def add_arguments(self, parser):
        parser.add_argument('model', help='app_label.ModelName')
        parser.add_argument('--output', default='generated')

    def handle(self, *args, **options):
        model = apps.get_model(options['model'])
        name = model.__name__
        from system.catalog import ENTITIES
        entity = next(key for key,value in ENTITIES.items() if value is model)
        output = Path(options['output']) / entity
        output.mkdir(parents=True, exist_ok=True)
        (output/'views.py').write_text(f'from {model.__module__} import {name}\nfrom core.api import serializer_for\nfrom system.views import ResourceViewSet\n\nclass {name}ViewSet(ResourceViewSet):\n    queryset = {name}.objects.all()\n    serializer_class = serializer_for({name})\n', encoding='utf-8')
        (output/'urls.py').write_text(f'from rest_framework.routers import DefaultRouter\nfrom .views import {name}ViewSet\nrouter = DefaultRouter()\nrouter.register("{entity}", {name}ViewSet, basename="{entity}")\nurlpatterns = router.urls\n', encoding='utf-8')
        fields = [{'key':f.name,'title':str(f.verbose_name),'type':f.get_internal_type(),'required':not f.blank} for f in model._meta.fields]
        (output/'fields.json').write_text(json.dumps(fields,ensure_ascii=False,indent=2),encoding='utf-8')
        (output/'resource_options.py').write_text('RESOURCE_OPTIONS = '+repr({name:{'fields':{field['key']:{'title':field['title']} for field in fields}}})+'\n',encoding='utf-8')
        (output/'index.vue').write_text(f'<script setup lang="ts">\nimport Resource from "../../pages/Resource.vue"\n</script>\n<template><Resource entity="{entity}"/></template>\n',encoding='utf-8')
        (output/'接入说明.md').write_text(f'# {name} CRUD\n\n将模型应用 AppConfig 加到 application/plugins.py 的 APPS。系统会自动登记该应用模型，生成文件可用于有专用逻辑的接口。\n\n如需使用系统的自动表单，实体键为 `{entity}`，执行 init_data 创建菜单与按钮。可在菜单中修改可见状态并按角色授权。无需修改 system/catalog.py。自动表单读取模型字段，不读取数据库专属 SQL。\n',encoding='utf-8')
        self.stdout.write(f'源码已生成：{output.resolve()}')
        with (output/'接入说明.md').open('a',encoding='utf-8') as document:
            document.write('\n字段和页面覆盖：把 resource_options.py 放入模型应用，在 AppConfig 中导入 RESOURCE_OPTIONS，并设置 resource_options = RESOURCE_OPTIONS。fields 中可配置 title、kind、column、form；crud_fields 指定有序界面字段；exclude_fields 只排除 CRUD 界面字段；serializer_exclude_fields 排除 API 字段；fields 可用 source 增加只读虚拟字段；crud_options 深层覆盖 FastCrud 配置；search_fields 配置关键词查询路径。菜单的 resource 选择接口资源，component_name 仍作权限前缀。fields.json 是模型快照，修改快照不会改变运行页面。字段权限继续由后端权限配置决定。\n')
