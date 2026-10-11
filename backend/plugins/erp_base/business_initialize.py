"""登记已实施业务菜单；已有角色授权由用户配置，重复初始化不扩大。"""
from django.db import transaction
from core.api import AUDIT_FIELDS
from system.catalog import ENTITIES
from system.models import (Menu, MenuButton, MenuField, Role, RoleMenuPermission,
                           RoleMenuButtonPermission, FieldPermission)
from plugins.erp_sales.resource_options import MODEL_FIELDS as SALES
from plugins.erp_sampling.resource_options import MODEL_FIELDS as SAMPLING
from .business_api import policy_for

DOMAINS = [('erp_sales', '销售管理', SALES), ('erp_sampling', '打样管理', SAMPLING)]
MAIN = {'CommercialPrice', 'SalesOrder', 'SalesOrderChange', 'SampleRequest', 'Recipe', 'ProcessCurveVersion'}
TITLES = {'confirm-post': '确认', 'receive-post': '收样', 'assign-post': '分配人员',
          'start-post': '开工', 'complete-post': '完成', 'send-post': '送版', 'reply-post': '客户回复',
          'approve-post': '审核', 'activate-post': '启用', 'retire-post': '停用',
          'clone-post': '复制新版本', 'save-document-post': '保存表头与明细'}


@transaction.atomic
def load():
    root = Menu.objects.get(component_name='erp')
    roles = [Role.objects.get_or_create(key=key, defaults={'name': name}) for key, name in
             [('erp_business_manager', 'ERP业务办理'), ('erp_business_viewer', 'ERP业务查询')]]
    for sort, (app, title, fields) in enumerate(DOMAINS, 2):
        catalog, _ = Menu.objects.get_or_create(component_name=app, defaults={
            'name': title, 'is_catalog': True, 'web_path': '/erp/' + app.removeprefix('erp_'),
            'parent': root, 'sort': sort})
        for index, name in enumerate(fields, 1):
            entity = app + '_' + name.lower()
            menu = Menu.objects.get(component_name=entity)
            menu.parent, menu.resource = catalog, entity
            menu.web_path, menu.component = catalog.web_path + '/' + name.lower(), 'plugins/erp/Business'
            menu.visible, menu.sort = name in MAIN, index
            menu.save(update_fields=['parent', 'resource', 'web_path', 'component', 'visible', 'sort'])
            for action, label in TITLES.items():
                MenuButton.objects.filter(value=entity + ':' + action).update(name=label)
    log = Menu.objects.get(component_name='erp_base_businessaction')
    log.parent, log.resource, log.web_path, log.component = root, log.component_name, '/erp/actions', 'plugins/erp/Business'
    log.save(update_fields=['parent', 'resource', 'web_path', 'component'])
    for index, (role, created) in enumerate(roles):
        if not created:
            continue
        for menu in Menu.objects.filter(component_name__in=['erp', *[d[0] for d in DOMAINS]]):
            RoleMenuPermission.objects.get_or_create(role=role, menu=menu)
        for entity, model in ENTITIES.items():
            if not model._meta.app_label.startswith('erp_') and entity not in ['dept', 'user', 'file']:
                continue
            menu = Menu.objects.get(component_name=entity)
            query_only = index == 1 or model._meta.app_label == 'erp_base' or entity in ['dept', 'user', 'file']
            if model._meta.app_label != 'erp_base':
                RoleMenuPermission.objects.get_or_create(role=role, menu=menu)
            buttons = MenuButton.objects.filter(menu=menu)
            if query_only:
                buttons = buttons.filter(method=0)
            for button in buttons:
                RoleMenuButtonPermission.objects.get_or_create(role=role, menu_button=button, defaults={'data_range': 3})
            owned = set() if query_only else policy_for(model)['owned'][model]
            for column in MenuField.objects.filter(menu=menu):
                writable = not query_only and column.field_name not in {*AUDIT_FIELDS, 'legacy_id', *owned}
                FieldPermission.objects.get_or_create(role=role, field=column, defaults={
                    'is_query': True, 'is_create': writable, 'is_update': writable})
        RoleMenuPermission.objects.get_or_create(role=role, menu=log)
