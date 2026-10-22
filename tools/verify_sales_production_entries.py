"""在指定独立库验证最终导航及日常保存；新增单据全部回滚。"""
import os
import sys
import json
from pathlib import Path
from decimal import Decimal

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','application.settings')
import django
django.setup()
from django.apps import apps
from django.db import connection,transaction
from django.test.utils import setup_test_environment
from rest_framework.test import APIClient
from system.models import Menu,Users
from plugins.erp_base.business_navigation import RESOURCES
from plugins.erp_base.source_entry_services import entry_for

assert str(connection.settings_dict['PORT'])=='5440' and connection.settings_dict['NAME']=='erp_master_xlsx_verify_20261021'
setup_test_environment()
client=APIClient(HTTP_HOST='localhost');client.force_authenticate(Users.objects.get(username='xlsx-update-20261021'))
checks=[]
def check(name,valid,detail=None):
    assert valid,(name,detail)
    checks.append({'name':name,'passed':True,'detail':detail})
    print('PASS',name,flush=True)
def module(menu):
    while menu.parent_id is not None and menu.parent.component_name!='erp':menu=menu.parent
    return menu.component_name
menus={m.component_name:m for m in Menu.objects.select_related('parent')}
for label,spec in RESOURCES.items():check('最终归属 '+label,module(menus[spec['entity']])==spec['module'])
heads=Menu.objects.filter(parent__component_name='erp_sales_main',is_catalog=False).order_by('sort')
check('销售主入口仅染整订单与染整报价且先订单',list(heads.values_list('name',flat=True))==['染整订单','染整报价'])
for key in ['erp_sales_details','erp_sales_quote_rules']:
    check('明细及加价规则可展开 '+key,menus[key].parent.component_name=='erp_sales_main')
for entity in ['erp_sales_sourcedyeordermain','erp_sales_sourcedyefixedprice','erp_sampling_sourcedyedyerecipe','erp_production_sourcedyejobsheet','erp_warehouse_sourcedyerecordyield']:
    r=client.get('/api/meta/'+entity+'/')
    check('最终资源元数据可访问 '+entity,r.status_code==200)
with transaction.atomic():
    for entity,entry in [('erp_sales_sourcedyeordermain','OrderMain'),('erp_sales_sourcedyefixedprice','Quote')]:
        model=apps.get_model('erp_sales.'+('SourceDyeOrderMain' if entry=='OrderMain' else 'SourceDyeFixedPrice'))
        before=model.objects.count()
        r=client.post('/api/system/'+entity+'/',{'_entry':entry,'old_customer_id':'000','old_remarks':'独立验证-事务回滚-20261022'},format='json')
        check('日常保存 '+entry,r.status_code==200,str(r.data)[:800])
        item=model.objects.get(old_remarks='独立验证-事务回滚-20261022')
        check('原业务入口及编号 '+entry,entry_for(item)==entry and bool(item.old_sheet_no) and bool(item.old_sheet_series))
        if entry=='Quote':
            line_model=apps.get_model('erp_sales.SourceDyeFixedPriceDetail')
            r=client.post('/api/system/erp_sales_sourcedyefixedpricedetail/',{'_entry':'QuoteDetail','source_parent_1':item.pk,'old_cus_price':'123.45','old_price':None},format='json')
            check('日常报价主从保存',r.status_code==200,str(r.data)[:800])
            line=line_model.objects.get(source_parent_1=item)
            check('日常对客价不被零总价覆盖',line.old_cus_price==Decimal('123.45') and line.old_price is None and line.old_pricesum==0)
            check('报价明细继承表头流水',line.old_sheet_series==item.old_sheet_series and entry_for(line)=='QuoteDetail')
        check('日常新增恰好一张表头 '+entry,model.objects.count()==before+1)
    transaction.set_rollback(True)
check('日常验证单据已全部回滚',not apps.get_model('erp_sales.SourceDyeOrderMain').objects.filter(old_remarks='独立验证-事务回滚-20261022').exists() and not apps.get_model('erp_sales.SourceDyeFixedPrice').objects.filter(old_remarks='独立验证-事务回滚-20261022').exists())
report={'database':connection.settings_dict['NAME'],'port':5440,'passed':len(checks),'checks':checks,'formal_imported':0}
(ROOT/'docs/erp-sales-production-entries-verification-20261022.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('ALL PASS',len(checks))
