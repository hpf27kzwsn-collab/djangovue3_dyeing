"""系统管理菜单、权限和资料保留验证；仅在5440独立库执行。"""
import os
import sys
import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
import django
django.setup()
from django.apps import apps
from django.db import connection
from django.core.management import call_command
from django.test.utils import setup_test_environment
from rest_framework.test import APIClient
from system.models import Menu, MenuButton, MenuField, Role, Users, RoleMenuPermission, RoleMenuButtonPermission, FieldPermission
from system.management_layout import GROUPS, PAGES
from plugins.erp_base.foundation_catalog import DEFINITIONS

assert str(connection.settings_dict['PORT']) == '5440', '只允许在5440独立验证库执行'
setup_test_environment()
results = []


def check(name, condition, detail=None):
    assert condition, (name, detail)
    results.append({'name': name, 'passed': True, 'detail': detail})
    print('PASS', name, flush=True)


def digest(model):
    h = hashlib.sha256()
    count = 0
    for row in model.objects.order_by('pk').values_list().iterator(chunk_size=1000):
        h.update(repr(tuple(bytes(x) if isinstance(x, memoryview) else x for x in row)).encode('utf8'))
        count += 1
    return {'rows': count, 'sha256': h.hexdigest()}


def state():
    source = {m._meta.label: digest(m) for m in apps.get_models() if hasattr(m, 'SOURCE_TABLE')}
    return {'source': source, 'numbering': digest(apps.get_model('erp_base.NumberingRule')),
            'buttons': digest(MenuButton), 'fields': digest(MenuField),
            'button_grants': digest(RoleMenuButtonPermission), 'field_grants': digest(FieldPermission),
            'department_grants': digest(RoleMenuButtonPermission.dept.through)}


before = state()
menus_before = list(Menu.objects.values('id', 'component_name', 'parent_id', 'web_path', 'resource', 'name'))
call_command('rebuild_management_menus')
after = state()
check('重复整理保留全部来源行、编号配置、接口权限、字段权限及指定部门', before == after,
      {'source_models': len(before['source']), 'source_rows': sum(x['rows'] for x in before['source'].values())})
check('重复整理幂等', menus_before == list(Menu.objects.values('id', 'component_name', 'parent_id', 'web_path', 'resource', 'name')))
menus = {m.component_name: m for m in Menu.objects.select_related('parent')}


def root(menu):
    while menu.component_name not in ['erp_base','erp_sales','erp_purchase','erp_sampling','erp_production','erp_warehouse','erp_quality','system'] and menu.parent is not None:
        menu = menu.parent
    return menu.component_name


check('六分组及总览', all(menus[key].parent_id == menus['system'].pk for key, _, _ in GROUPS)
      and menus['system_overview'].web_path == '/management')
check('33个管理功能复用原模型入口', all(menus[key].parent_id == menus[folder].pk and menus[key].name == title
      for key, (folder, title) in PAGES.items()), len(PAGES))
check('全部分类资料按业务归属', all(root(menus[p['key']]) == {'基础信息':'erp_base','销售管理':'erp_sales','采购管理':'erp_purchase',
      '打样管理':'erp_sampling','生产管理':'erp_production','仓储管理':'erp_warehouse','质量管理':'erp_quality','系统管理':'system'}[p['path'][0]]
      for p in DEFINITIONS.values()), len(DEFINITIONS))
check('幅宽克重选项留在业务模块', all(root(menus['foundation_combo_' + code]) == 'erp_base' for code in ['Z001', 'Z002']))
check('业务参数留在生产管理', root(menus['erp_base_sourcebusinessparameter']) == 'erp_production')
check('质量数量来源留在质量管理', all(root(menus[key]) == 'erp_quality' for key in ['erp_quality_qualityquantitybatch','erp_quality_qualityquantitysource']))
check('三类设备配置复用', all(root(menus[p['key']]) == 'system' for p in DEFINITIONS.values()
      if p['model'] in ['erp_base.SourceDyePCommPort','erp_base.SourceDyePMachinePort','erp_base.SourceDyePMachinePoint']))
check('演示入口退出导航', not any(menus[k].visible for k in ['component_demo','chart_demo','tasks']))


def account(key, menu_keys, writable):
    role, _ = Role.objects.get_or_create(key=key, defaults={'name': key})
    user, _ = Users.objects.get_or_create(username=key, defaults={'pwd_change_count': 1})
    user.set_password('SystemVerify2026')
    user.save(update_fields=['password'])
    user.role.set([role])
    RoleMenuPermission.objects.filter(role=role).delete()
    RoleMenuButtonPermission.objects.filter(role=role).delete()
    FieldPermission.objects.filter(role=role).delete()
    for key in menu_keys:
        menu = menus[key]
        RoleMenuPermission.objects.create(role=role, menu=menu)
        # 分类资料与总表复用按钮和字段。
        canonical = Menu.objects.get(component_name=menu.resource) if menu.resource else menu
        for button in MenuButton.objects.filter(menu=canonical):
            if writable or button.method == 0:
                RoleMenuButtonPermission.objects.create(role=role, menu_button=button, data_range=3)
        for field in MenuField.objects.filter(menu=canonical):
            FieldPermission.objects.create(role=role, field=field, is_query=True, is_create=writable, is_update=writable)
    client = APIClient(HTTP_HOST='localhost')
    client.force_authenticate(user)
    return user, client


manager, cm = account('system-ui-manager', ['erp_base_numberingrule','user','role','dept','dictionary','operation_log','periodic_task'], True)
viewer, cv = account('system-ui-viewer', ['erp_base_numberingrule'], False)
business, cb = account('system-ui-business', ['foundation_unit_width'], True)
check('非超级管理员取得原有管理接口', cm.get('/api/system/user/').status_code == 200 and cm.get('/api/system/erp_base_numberingrule/').status_code == 200)
vm = cv.get('/api/account/').data['data']['menus']
check('仅叶页授权自动返回祖先且不扩展同级', {m['component_name'] for m in vm} == {'system','erp_base_numberingrule'})
bm = cb.get('/api/account/').data['data']['menus']
check('业务账号不出现系统管理或登录账号菜单', not any(m['component_name'] in ['system','user','erp_base_numberingrule'] for m in bm))
check('业务账号不能访问管理数据', cb.get('/api/system/user/').status_code == 403 and cb.get('/api/system/erp_base_numberingrule/').status_code == 403)
rule = apps.get_model('erp_base.NumberingRule').objects.order_by('pk').first()
check('只读账号可以查询编号', cv.get('/api/system/erp_base_numberingrule/').status_code == 200)
check('只读账号不能修改规则', cv.patch(f'/api/system/erp_base_numberingrule/{rule.pk}/', {'prefix':'NO'}, format='json').status_code == 403)
check('只读账号不能试算或同步', cv.post('/api/system/erp_base_numberingrule/preview/', {}, format='json').status_code == 403
      and cv.post(f'/api/system/erp_base_numberingrule/{rule.pk}/synchronize/', {}, format='json').status_code == 403)
check('未增加业务模型或旧erpID字段', not any(f.name in ['legacy_erp_id','old_erp_id'] for m in apps.get_models() for f in m._meta.fields))
report = {'database': connection.settings_dict['NAME'], 'port': 5440, 'passed': len(results), 'results': results,
          'preservation': after, 'scope': '开发验证及独立库数据保留检查；不代表正式历史数据对账或现场验收'}
(ROOT / 'docs/erp-system-management-verification-20261021.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
print('ALL', len(results), 'PASS')
