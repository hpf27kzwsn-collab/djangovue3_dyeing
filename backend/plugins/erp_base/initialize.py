"""登记基础资料菜单与专用角色；重复执行保留已有授权设置。"""
from django.db import transaction
from core.api import AUDIT_FIELDS
from system.catalog import ENTITIES
from system.models import (Menu, MenuButton, MenuField, Role, RoleMenuPermission,
                           RoleMenuButtonPermission, FieldPermission)
from .resource_options import MODEL_FIELDS


CHILD_MODELS = {'PartyRole', 'PartyContact', 'PartyAddress', 'YarnSpecification',
                'ChemicalSpecification', 'CustomerMaterial', 'StorageLocation',
                'MachineProcess', 'RouteVersion', 'RouteStep'}
ACTION_NAMES = {'approve-post': '审核', 'activate-post': '启用', 'retire-post': '停用', 'clone-post': '复制新版本','rows-get':'完整原始数据','compare-get':'逐字段旧新对照'}


@transaction.atomic
def load():
    root, _ = Menu.objects.get_or_create(component_name='erp', defaults={
        'name': '染色ERP', 'is_catalog': True, 'web_path': '/erp', 'sort': 0, 'icon': 'Goods'})
    catalog, _ = Menu.objects.get_or_create(component_name='erp_base', defaults={
        'name': '基础信息', 'is_catalog': True, 'web_path': '/erp/base', 'parent': root, 'sort': 1})
    roles = [Role.objects.get_or_create(key=key, defaults={'name': name}) for key, name in
             [('erp_base_manager', '基础资料维护'), ('erp_base_viewer', '基础资料查询')]]
    for sort, name in enumerate(MODEL_FIELDS, 1):
        entity = 'erp_base_' + name.lower()
        model = ENTITIES[entity]
        menu = Menu.objects.get(component_name=entity)
        menu.parent = catalog
        menu.web_path = '/erp/base/' + model._meta.model_name
        menu.component = 'plugins/erp/MasterData'
        if name.startswith('Legacy'):menu.component='plugins/erp/LegacyArchive'
        menu.resource = entity
        menu.sort = sort
        menu.visible = name not in CHILD_MODELS
        menu.save(update_fields=['parent', 'web_path', 'component', 'resource', 'sort', 'visible'])
        for action, title in ACTION_NAMES.items():
            MenuButton.objects.filter(value=entity + ':' + action).update(name=title)
        for index, (role, created) in enumerate(roles):
            if not created or name.startswith('Legacy'):
                continue
            for directory in (root, catalog, menu):
                RoleMenuPermission.objects.get_or_create(role=role, menu=directory)
            buttons = MenuButton.objects.filter(menu=menu)
            if index == 1:
                buttons = buttons.filter(method=0)
            for button in buttons:
                RoleMenuButtonPermission.objects.get_or_create(role=role, menu_button=button, defaults={'data_range': 3})
            for column in MenuField.objects.filter(menu=menu, model=model._meta.label):
                writable = index == 0 and column.field_name not in [*AUDIT_FIELDS]
                if name == 'RouteVersion' and column.field_name == 'status':
                    writable = False
                if name == 'ColorStandard' and column.field_name == 'source_sample':
                    writable = False
                FieldPermission.objects.get_or_create(role=role, field=column,
                    defaults={'is_query': True, 'is_create': writable, 'is_update': writable})
    legacy_role,legacy_created=Role.objects.get_or_create(key='erp_legacy_viewer',defaults={'name':'完整旧资料与导入对照查询'})
    if legacy_created:
        for directory in (root,catalog):RoleMenuPermission.objects.get_or_create(role=legacy_role,menu=directory)
        for menu in Menu.objects.filter(component_name__startswith='erp_base_legacy'):
            RoleMenuPermission.objects.get_or_create(role=legacy_role,menu=menu)
            for button in MenuButton.objects.filter(menu=menu,method=0):RoleMenuButtonPermission.objects.get_or_create(role=legacy_role,menu_button=button,defaults={'data_range':3})
            for column in MenuField.objects.filter(menu=menu):FieldPermission.objects.get_or_create(role=legacy_role,field=column,defaults={'is_query':True,'is_create':False,'is_update':False})
    # 选择部门、登录账号和附件时使用平台已有接口，只授予所需操作。
    for index, (role, created) in enumerate(roles):
        if not created:
            continue
        for entity, names in [('dept', ['name', 'parent', 'status']),
                              ('user', ['name', 'username']),
                              ('file', ['name', 'url', 'size', 'file_type', 'upload_method', 'mime_type'])]:
            for button in MenuButton.objects.filter(menu__component_name=entity, method=0):
                RoleMenuButtonPermission.objects.get_or_create(role=role, menu_button=button, defaults={'data_range': 3})
            if entity == 'file' and index == 0:
                button = MenuButton.objects.get(value='file:add')
                RoleMenuButtonPermission.objects.get_or_create(role=role, menu_button=button, defaults={'data_range': 3})
            for column in MenuField.objects.filter(menu__component_name=entity):
                FieldPermission.objects.get_or_create(role=role, field=column, defaults={
                    'is_query': column.field_name in names,
                    'is_create': entity == 'file' and index == 0, 'is_update': False})
