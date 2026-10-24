from django.core.management.base import BaseCommand
from django.db import transaction, models, connection
from core.api import AUDIT_FIELDS
from system.catalog import ENTITIES, HIDDEN_ENTITIES
from system.models import *
from system.views import view_for
from system.actions import resource_actions
from plugins.erp_base.source_documents import SourceRecord


class Command(BaseCommand):
    help = '初始化管理员、菜单、按钮、字段、字典和系统配置；可重复执行'

    @transaction.atomic
    def handle(self, *args, **options):
        dept, _ = Dept.objects.get_or_create(key='company', defaults={'name': '总公司'})
        dept.dept_belong = dept
        dept.save(update_fields=['dept_belong'])
        role, role_created = Role.objects.get_or_create(key='admin', defaults={'name': '管理员'})
        user, created = Users.objects.get_or_create(username='superadmin', defaults={
            'name': '超级管理员', 'is_staff': True, 'is_superuser': True, 'dept': dept, 'dept_belong': dept})
        if created:
            user.set_password('admin123456')
            user.save(update_fields=['password'])
        user.role.add(role)
        catalog, _ = Menu.objects.get_or_create(component_name='system', defaults={'name': '系统管理', 'is_catalog': True, 'sort': 1, 'web_path': '/system'})
        task_catalog, _ = Menu.objects.get_or_create(component_name='tasks', defaults={'name': '任务管理', 'is_catalog': True, 'sort': 2, 'web_path': '/tasks'})
        for sort, (entity, model) in enumerate(ENTITIES.items(), 1):
            parent = task_catalog if entity in ['periodic_task', 'task_result', 'interval_schedule', 'crontab_schedule', 'clocked_schedule', 'solar_schedule'] else catalog
            menu, _ = Menu.objects.get_or_create(component_name=entity, defaults={'name': str(model._meta.verbose_name),
                'parent': parent, 'web_path': '/system/'+entity, 'component': 'system/Resource', 'resource':entity, 'sort': sort,
                'visible': entity not in HIDDEN_ENTITIES})
            if role_created:
                RoleMenuPermission.objects.get_or_create(role=role, menu=menu)
            actions = resource_actions(entity, view_for(entity, model))
            current_values = [f'{entity}:{key}' for key, _, _, _ in actions]
            MenuButton.objects.filter(menu=menu).exclude(value__in=current_values).delete()
            if issubclass(model, SourceRecord):
                existing={button.value for button in MenuButton.objects.filter(menu=menu)}
                MenuButton.objects.bulk_create([MenuButton(value=f'{entity}:{key}',name=title,menu=menu,method=verb,api=api)
                    for key,title,verb,api in actions if f'{entity}:{key}' not in existing])
                columns=list(MenuField.objects.filter(menu=menu,model=model._meta.label))
                existing={column.field_name for column in columns}
                MenuField.objects.bulk_create([MenuField(menu=menu,model=model._meta.label,field_name=field.name,title=str(field.verbose_name))
                    for field in model._meta.fields if field.name not in existing and field.name not in AUDIT_FIELDS and not isinstance(field,models.AutoField)])
                if role_created:
                    buttons=MenuButton.objects.filter(menu=menu)
                    RoleMenuButtonPermission.objects.bulk_create([RoleMenuButtonPermission(role=role,menu_button=button,data_range=3) for button in buttons])
                    columns=MenuField.objects.filter(menu=menu,model=model._meta.label)
                    FieldPermission.objects.bulk_create([FieldPermission(role=role,field=column) for column in columns])
                continue
            for key, title, verb, api in actions:
                button, _ = MenuButton.objects.get_or_create(value=f'{entity}:{key}', defaults={'name':title, 'menu':menu, 'method':verb, 'api':api})
                if role_created:
                    RoleMenuButtonPermission.objects.get_or_create(role=role, menu_button=button, defaults={'data_range':3})
            for field in list(model._meta.fields) + list(model._meta.many_to_many):
                if field.name in AUDIT_FIELDS or isinstance(field, models.AutoField) or (model is Users and field.name in ['password','groups','user_permissions']):
                    continue
                column, _ = MenuField.objects.get_or_create(menu=menu, model=model._meta.label, field_name=field.name,
                                                           defaults={'title':str(field.verbose_name)})
                if role_created:
                    FieldPermission.objects.get_or_create(role=role, field=column)
        groups={key:SystemConfig.objects.get_or_create(key=key,defaults={'title':title})[0] for key,title in [('site','平台设置'),('login','登录设置'),('base','基础设置')]}
        for key, title, value in [('site.title','平台名称','ERP 管理平台'), ('login.captcha','登录验证码',False),
                                 ('site.logo','平台 Logo',''),('site.subtitle','平台介绍','组织、权限、系统数据与消息任务'),
                                 ('login.first_password','首次登录修改密码',True),('login.ip_analysis','登录 IP 地理信息',False),
                                 ('login.copyright','版权信息','ERP 管理平台'),('login.keep_record','备案号',''),
                                 ('login.help_url','帮助链接',''),('login.privacy_url','隐私链接','/terms/privacy'),
                                 ('login.clause_url','条款链接','/terms/service'),
                                 ('base.default_password','用户默认密码','admin123456')]:
            group, name = key.split('.',1)
            SystemConfig.objects.get_or_create(key=name, parent=groups[group], defaults={'title':title, 'value':value,
                'status':key!='base.default_password','form_item_type':9 if isinstance(value,bool) else 0})
        root, _ = Dictionary.objects.get_or_create(value='status', is_value=False, defaults={'label':'状态'})
        for sort, (label, value) in enumerate([('启用','true'),('停用','false')]):
            Dictionary.objects.get_or_create(parent=root, value=value, defaults={'label':label,'is_value':True,'type':6,'sort':sort})
        from system.dictionaries import initialize_dictionaries
        initialize_dictionaries()
        self.stdout.write(self.style.SUCCESS('初始化完成。首次管理员：superadmin / admin123456；重复初始化保留现有密码。'))
        # 退役的是技术入口，不删除对应业务/历史数据。
        from plugins.erp_base.reports import REPORTS
        active_resources = [*ENTITIES, *['erp_report_' + key for key in REPORTS], 'erp_scanning']
        Menu.objects.exclude(resource='').exclude(resource__in=active_resources).update(status=False, visible=False)
        from application.plugins import INITIALIZERS
        from django.utils.module_loading import import_string
        for initializer in INITIALIZERS:
            import_string(initializer)()
        if connection.vendor == 'postgresql':
            # 完整ERP初始化批量增加菜单、字段和授权；及时更新统计，避免空表估算产生权限笛卡尔扫描。
            with connection.cursor() as cursor:
                for table in ['system_users', 'system_role', 'system_users_role', 'system_menu', 'system_menubutton',
                    'system_rolemenupermission', 'system_rolemenubuttonpermission', 'system_menufield', 'system_fieldpermission']:
                    cursor.execute('ANALYZE ' + connection.ops.quote_name(table))
