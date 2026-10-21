"""按核查方案登记分类菜单；只更新平台配置，不采用或导入业务资料。"""
from hashlib import sha1
from django.db import transaction
from system.models import Menu, MenuButton, Role, RoleMenuPermission, RoleMenuButtonPermission, FieldPermission, MenuField
from .foundation_catalog import DEFINITIONS
from .source_api import OWNED

ROOTS = {'基础信息': 'erp_base', '销售管理': 'erp_sales', '采购管理': 'erp_purchase',
         '打样管理': 'erp_sampling', '生产管理': 'erp_production', '仓储管理': 'erp_warehouse',
         '质量管理': 'erp_quality', '系统管理': 'system'}


def folder(path):
    parent = Menu.objects.get(component_name=ROOTS[path[0]])
    for end in range(2, len(path) + 1):
        key = 'foundation_folder_' + sha1('/'.join(path[:end]).encode()).hexdigest()[:18]
        parent, _ = Menu.objects.update_or_create(component_name=key, defaults={
            'name': path[end - 1], 'parent': parent, 'is_catalog': True, 'visible': True,
            'status': True, 'sort': 20, 'web_path': '/erp/foundation/group/' + key})
    return parent


def grant_path(role_id, menu):
    while menu is not None:
        RoleMenuPermission.objects.get_or_create(role_id=role_id, menu=menu)
        menu = menu.parent


@transaction.atomic
def load():
    # 原“完整旧业务资料”角色原本覆盖全部来源：新增表补齐同等权限，其他角色保留现有范围。
    for key, writable in [('erp_original_manager', True), ('erp_original_viewer', False)]:
        role = Role.objects.get(key=key)
        for item in DEFINITIONS.values():
            if not item.get('canonical'):
                continue
            menu = Menu.objects.get(component_name=item['entity'])
            if RoleMenuPermission.objects.filter(role=role, menu=menu).exists():
                continue
            RoleMenuPermission.objects.create(role=role, menu=menu)
            buttons = MenuButton.objects.filter(menu=menu)
            if not writable:
                buttons = buttons.filter(method=0)
            RoleMenuButtonPermission.objects.bulk_create([
                RoleMenuButtonPermission(role=role, menu_button=b, data_range=3) for b in buttons])
            FieldPermission.objects.bulk_create([FieldPermission(role=role, field=f, is_query=True,
                is_create=writable and f.field_name not in OWNED, is_update=writable and f.field_name not in OWNED)
                for f in MenuField.objects.filter(menu=menu)])
    count = 0
    for item in DEFINITIONS.values():
        canonical = Menu.objects.get(component_name=item['entity'])
        parent = folder(item['path'][:-1])
        roles = list(RoleMenuPermission.objects.filter(menu=canonical).values_list('role_id', flat=True))
        values = {'name': item['title'], 'parent': parent, 'resource': item['entity'],
                  'component': 'plugins/erp/FoundationEntry', 'is_catalog': False, 'visible': True, 'status': True}
        if item.get('canonical'):
            for name, value in values.items():
                setattr(canonical, name, value)
            canonical.save(update_fields=list(values))
            menu = canonical
        else:
            menu, _ = Menu.objects.update_or_create(component_name=item['key'], defaults={
                **values, 'web_path': '/erp/foundation/' + item['key'], 'sort': 30})
        for role_id in roles:
            grant_path(role_id, menu)
        # 元数据入口只复制已有查询权限，不给查询角色增加新增/修改/删除权。
        button = MenuButton.objects.get(value=item['entity'] + ':foundation_entry-get')
        list_button = MenuButton.objects.get(value=item['entity'] + ':list')
        for grant in RoleMenuButtonPermission.objects.filter(menu_button=list_button):
            added, created = RoleMenuButtonPermission.objects.get_or_create(role_id=grant.role_id, menu_button=button,
                defaults={'data_range': grant.data_range})
            if created:
                added.dept.set(grant.dept.all())
        count += 1
    # 整理主档不自动采用原资料，独立分组，避免与原表资料混成两套可随意替换的入口。
    from .resource_options import MODEL_FIELDS
    for name in MODEL_FIELDS:
        if name.startswith('Legacy') or name == 'SourceBusinessParameter':
            continue
        menu = Menu.objects.get(component_name='erp_base_' + name.lower())
        menu.parent = folder(['基础信息', '整理主档（按需采用）'])
        menu.save(update_fields=['parent'])
        for role_id in RoleMenuPermission.objects.filter(menu=menu).values_list('role_id', flat=True):
            grant_path(role_id, menu)
    return count

