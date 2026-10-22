"""应用已验证的菜单整理，审计写入范围为菜单及其已有角色的目录可见性。"""
import os
import sys
import json
import re
import hashlib
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','application.settings')
import django
django.setup()
from django.apps import apps
from django.db import connection,transaction
from django.core.management import call_command
from system.models import Menu,RoleMenuPermission,MenuButton,MenuField,RoleMenuButtonPermission,FieldPermission

assert str(connection.settings_dict['PORT'])=='5439' and connection.settings_dict['NAME']=='erp_full_trial_20261014'
allowed={Menu._meta.db_table,RoleMenuPermission._meta.db_table}
writes=Counter()
def audit(execute,sql,params,many,context):
    match=re.match(r'\s*(?:INSERT\s+INTO|UPDATE|DELETE\s+FROM)\s+"?([\w]+)',sql,re.I)
    if match:
        table=match[1]
        assert table in allowed,('菜单整理不应写入此表',table)
        writes[table]+=1
    return execute(sql,params,many,context)
def digest(model):
    h=hashlib.sha256();count=0
    for row in model.objects.order_by('pk').values_list().iterator(chunk_size=1000):
        h.update(repr(tuple(bytes(v) if isinstance(v,memoryview) else v for v in row)).encode());count+=1
    return {'rows':count,'sha256':h.hexdigest()}
authorizations=[MenuButton,MenuField,RoleMenuButtonPermission,FieldPermission,RoleMenuButtonPermission.dept.through]
business=[apps.get_model(label) for label in ['erp_sales.SourceDyeOrderMain','erp_sales.SourceDyeFixedPrice','erp_sales.SourceDyeFixedPriceDetail','erp_base.NumberingRule']]
before={m._meta.label:digest(m) for m in authorizations+business}
menus={m.component_name:(m.pk,m.web_path,m.resource,m.visible) for m in Menu.objects.all()}
with transaction.atomic(),connection.execute_wrapper(audit):
    call_command('rebuild_business_navigation')
    after={m._meta.label:digest(m) for m in authorizations+business}
    assert before==after
    current={m.component_name:(m.pk,m.web_path,m.resource,m.visible) for m in Menu.objects.all()}
    assert all(current[k]==v for k,v in menus.items())
report={'database':connection.settings_dict['NAME'],'port':5439,'only_configuration_writes':dict(writes),
        'business_and_authorization_unchanged':before,'original_menus_preserved':len(menus),'new_menus':len(current)-len(menus),'formal_business_rows_imported':0}
(ROOT/'docs/erp-sales-production-menu-apply-20261022.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('PASS 仅菜单配置写入',dict(writes),'业务及授权摘要保持一致')
