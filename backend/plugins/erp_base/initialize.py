"""客户业务目录；岗位授权由business_initialize统一登记。"""
from django.db import transaction
from system.models import Menu


@transaction.atomic
def load():
    root, _ = Menu.objects.get_or_create(component_name='erp', defaults={
        'name': '染色ERP', 'is_catalog': True, 'web_path': '/erp', 'sort': 0, 'icon': 'Goods'})
    Menu.objects.get_or_create(component_name='erp_base', defaults={
        'name': '基础信息', 'is_catalog': True, 'web_path': '/erp/base', 'parent': root, 'sort': 1})
