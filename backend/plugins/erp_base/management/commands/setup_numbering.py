from django.core.management.base import BaseCommand
from django.db import transaction
from system.models import Menu, MenuButton, MenuField, Role, RoleMenuPermission, RoleMenuButtonPermission, FieldPermission
from system.actions import resource_actions
from system.views import view_for
from plugins.erp_base.numbering_models import NumberingRule
from plugins.erp_base.numbering_registry import SUGGESTIONS
from plugins.erp_base.numbering import save_rule


class Command(BaseCommand):
    help = '安装编号管理入口及29条建议规则；不导入旧业务资料，不覆盖现有配置'

    @transaction.atomic
    def handle(self, *args, **options):
        from system.models import Users
        actor = Users.objects.filter(is_superuser=True).order_by('id').first()
        created = 0
        for suggestion in SUGGESTIONS:
            data = {key: value for key, value in suggestion.items() if key != 'source_filters'}
            if not NumberingRule.objects.filter(target_model=data['target_model'], target_field=data['target_field'], scope_key=data['scope_key']).exists():
                save_rule(data, actor)
                created += 1
        parent, _ = Menu.objects.get_or_create(component_name='system', defaults={'name': '管理设置', 'is_catalog': True, 'web_path': '/system'})
        entity = 'erp_base_numberingrule'
        menu, _ = Menu.objects.update_or_create(component_name=entity, defaults={'name': '编号管理', 'parent': parent,
            'web_path': '/management/numbering', 'component': 'pages/Numbering', 'resource': entity, 'visible': True})
        for key, title, method, api in resource_actions(entity, view_for(entity, NumberingRule)):
            MenuButton.objects.get_or_create(value=entity + ':' + key, defaults={'menu': menu, 'name': title, 'method': method, 'api': api})
        for field in NumberingRule._meta.fields:
            MenuField.objects.get_or_create(menu=menu, model=NumberingRule._meta.label, field_name=field.name, defaults={'title': str(field.verbose_name)})
        for role in Role.objects.filter(key='admin'):
            RoleMenuPermission.objects.get_or_create(role=role, menu=menu)
            for button in MenuButton.objects.filter(menu=menu):
                RoleMenuButtonPermission.objects.get_or_create(role=role, menu_button=button, defaults={'data_range': 3})
            for column in MenuField.objects.filter(menu=menu):
                FieldPermission.objects.get_or_create(role=role, field=column)
        self.stdout.write(f'新增{created}条建议规则，已登记{len(SUGGESTIONS)}条建议；未导入旧业务资料。')
