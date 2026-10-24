"""系统管理的菜单归属；保留菜单ID、原地址与既有操作/字段授权。"""
from django.db import transaction
from system.models import Menu, RoleMenuPermission
from plugins.erp_base.foundation_catalog import DEFINITIONS


GROUPS = [
    ('system_identity', '账号与权限', 10),
    ('system_configuration', '系统设置', 30),
    ('system_records', '操作与导入记录', 40),
    ('system_devices', '设备接入设置', 50),
    ('system_runtime', '运行维护', 60),
    ('system_archives', '审批、变更与通知', 70),
]
PAGES = {
    'user': ('system_identity', '登录账号'),
    'dept': ('system_identity', '账号归属部门'),
    'post': ('system_identity', '账号岗位'),
    'role': ('system_identity', '角色与权限'),
    'menu': ('system_identity', '菜单与按钮'),
    'api_white_list': ('system_identity', '接口访问白名单'),
    'menu_button': ('system_identity', '按钮权限定义'),
    'column': ('system_identity', '字段权限定义'),
    'field_permission': ('system_identity', '字段授权记录'),
    'role_menu_permission': ('system_identity', '菜单授权记录'),
    'role_menu_button_permission': ('system_identity', '操作授权记录'),
    'erp_base_numberingrule': ('system', '编号管理'),
    'system_config': ('system_configuration', '系统参数'),
    'dictionary': ('system_configuration', '系统选项'),
    'area': ('system_configuration', '行政区域'),
    'file': ('system_configuration', '附件管理'),
    'message_center': ('system_configuration', '系统通知'),
    'operation_log': ('system_records', '接口操作日志'),
    'login_log': ('system_records', '登录日志'),
    'download_center': ('system_records', '下载记录'),
    'erp_base_businessaction': ('system_records', '业务操作记录'),
    'erp_base_legacyimportbatch': ('system_records', '资料导入批次'),
    'periodic_task': ('system_runtime', '计划任务'),
    'task_result': ('system_runtime', '任务执行记录'),
    'interval_schedule': ('system_runtime', '间隔计划配置'),
    'crontab_schedule': ('system_runtime', '日历计划配置'),
    'clocked_schedule': ('system_runtime', '指定时间配置'),
}


def grant_ancestors(menu):
    """只补目录和总览可见性，不增加任何业务接口或字段权限。"""
    role_ids = list(RoleMenuPermission.objects.filter(menu=menu).values_list('role_id', flat=True))
    parent = menu.parent
    while parent is not None:
        for role_id in role_ids:
            RoleMenuPermission.objects.get_or_create(role_id=role_id, menu=parent)
        parent = parent.parent
    return role_ids


@transaction.atomic
def load():
    root = Menu.objects.get(component_name='system')
    root.name, root.parent, root.sort, root.visible, root.status, root.icon = '系统管理', None, 90, True, True, 'Setting'
    root.save(update_fields=['name', 'parent', 'sort', 'visible', 'status', 'icon'])
    folders = {'system': root}
    for key, name, sort in GROUPS:
        folders[key], _ = Menu.objects.update_or_create(component_name=key, defaults={
            'name': name, 'parent': root, 'is_catalog': True, 'visible': True,
            'status': True, 'sort': sort, 'web_path': '/management/group/' + key})
    overview, _ = Menu.objects.update_or_create(component_name='system_overview', defaults={
        'name': '系统管理总览', 'parent': root, 'is_catalog': False, 'visible': True, 'status': True,
        'sort': 0, 'web_path': '/management', 'component': 'pages/Management', 'cache': True})
    menus = {m.component_name: m for m in Menu.objects.select_related('parent')}
    for key, (folder, name) in PAGES.items():
        menu = menus[key]
        menu.parent, menu.name = folders[folder], name
        menu.sort = 20 if key == 'erp_base_numberingrule' else list(PAGES).index(key) + 1
        menu.save(update_fields=['parent', 'name', 'sort'])
    numbering = menus['erp_base_numberingrule']
    numbering.web_path, numbering.component, numbering.resource = '/management/numbering', 'pages/Numbering', 'erp_base_numberingrule'
    numbering.save(update_fields=['web_path', 'component', 'resource'])
    # 分类基础资料以唯一目录为准；共表中的业务选项不会随原配置总表搬进系统管理。
    for profile in DEFINITIONS.values():
        if profile['path'][0] != '系统管理':
            continue
        if profile['key'] not in menus:
            continue
        menu = menus[profile['key']]
        menu.parent = folders['system_devices' if profile['path'][1] == '设备接入设置' else 'system_archives']
        menu.save(update_fields=['parent'])
    from system.catalog import ENTITIES
    business_models = {p['model'] for p in DEFINITIONS.values() if p['path'][0] != '系统管理'}
    for entity, model in ENTITIES.items():
        table = getattr(model, 'SOURCE_TABLE', '')
        if model._meta.label not in business_models and table.startswith('s_'):
            menu = menus[entity]
            menu.parent = folders['system_archives']
            menu.save(update_fields=['parent'])
    parameters = menus['erp_base_sourcebusinessparameter']
    parameters.parent = menus['erp_production']
    parameters.name = '生产业务参数'
    parameters.save(update_fields=['parent', 'name'])
    for key in ['erp_quality_qualityquantitybatch', 'erp_quality_qualityquantitysource']:
        menu = menus[key]
        menu.parent = menus['erp_quality']
        menu.save(update_fields=['parent'])
    for menu in Menu.objects.select_related('parent').exclude(is_catalog=True):
        role_ids = grant_ancestors(menu)
        parent = menu.parent
        while parent is not None and parent.pk != root.pk:
            parent = parent.parent
        if parent is not None:
            for role_id in role_ids:
                RoleMenuPermission.objects.get_or_create(role_id=role_id, menu=overview)
    # 演示页保留原定义，退出业务导航；旧任务根目录的实际页面已归运行维护。
    Menu.objects.filter(component_name__in=['component_demo', 'chart_demo']).update(visible=False, status=False)
    Menu.objects.filter(component_name='tasks').update(visible=False)
    return {'root': root.pk, 'overview': overview.pk, 'groups': len(GROUPS), 'reused_pages': len(PAGES)}
