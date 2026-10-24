"""销售与生产业务入口归属；目录变更复用原资源、地址与授权。"""
import json
from pathlib import Path
from django.db import transaction

RESOURCES = json.loads(Path(__file__).with_suffix('.json').read_text(encoding='utf8'))['resources']
RESOURCES['erp_base.SourceDyeGetJobSheetReceive']={'entity':'erp_base_sourcedyegetjobsheetreceive',
    'title':'部门接收登记','table':'GetJobSheetReceive','module':'erp_production'}
RESOURCES['erp_production.SourceDyeTightTube']['title']='紧筒取消与平账'
RESOURCES['erp_production.SourceDyeTightTubeDetail']['title']='紧筒业务明细'
RESOURCES['erp_warehouse.SourceDyeRecordYield']['title']='包装细码与实称'
MODULES = {'erp_technology': '工艺设计', 'erp_scheduling': '排产管理', 'erp_production': '生产管理'}


def configure_resources(options, app):
    titles = {item['entity']: item['title'] for item in RESOURCES.values()}
    for name, config in options.items():
        label = app + '.' + name
        if label in RESOURCES:
            config['title'] = RESOURCES[label]['title']
        for child in config.get('workflow', {}).get('children', []):
            if child['entity'] in titles and not child.get('parent_field'):
                child['title'] = titles[child['entity']]
    defaults = {
        'erp_sales': {'SourceDyeOrderMain':'OrderMain','SourceDyeOrderColor':'OrderColor','SourceDyeFixedPrice':'Quote','SourceDyeFixedPriceDetail':'QuoteDetail'},
        'erp_sampling': {'SourceDyeDyeRecipe':'DyeRecipe','SourceDyeDyeRecipePhase':'DyeRecipePhase','SourceDyeDyeRecipeDetail':'DyeRecipeDetail'},
        'erp_production': {'SourceDyeProcessCraft':'ProcessCraft','SourceDyeStandCraft':'StandCraft','SourceDyeJobSheet':'JobSheet','SourceDyeJobProcess':'JobProcess','SourceDyeProcessSchedule':'ProcessSchedule','SourceDyeWProcess':'WProcessEdit','SourceDyeStuffWeight':'StuffWeight'},
        'erp_warehouse': {'SourceDyeRecordYield':'RecordYield'},
    }
    for name,entry in defaults.get(app,{}).items():
        options[name]['workflow']['default_entry'] = entry
    from .customer_resources import configure
    configure(options)


@transaction.atomic
def ensure_roots():
    from system.models import Menu
    root = Menu.objects.get(component_name='erp')
    for index, (key, title) in enumerate(MODULES.items(), 5):
        Menu.objects.update_or_create(component_name=key, defaults={
            'name': title, 'is_catalog': True, 'parent': root, 'visible': True, 'status': True,
            'sort': index, 'web_path': '/erp/' + key.removeprefix('erp_')})


@transaction.atomic
def load():
    from system.models import Menu
    from system.management_layout import grant_ancestors
    ensure_roots()
    menus = {m.component_name: m for m in Menu.objects.all()}
    folders = {}
    for module in MODULES:
        for suffix, title, sort in [('documents', '业务办理', 10), ('details', '业务明细', 90)]:
            key = module + '_' + suffix
            folders[(module, suffix)], _ = Menu.objects.update_or_create(component_name=key, defaults={
                'name': title, 'parent': menus[module], 'is_catalog': True, 'visible': True, 'status': True,
                'sort': sort, 'web_path': '/erp/navigation/' + key})
    for key, title in [('sales_main', '染整订单与报价'), ('sales_details', '订单与报价明细'), ('sales_quote_rules', '报价加价与克重规则'), ('sales_other', '其他订单与报价')]:
        folders[('erp_sales', key)], _ = Menu.objects.update_or_create(component_name='erp_' + key, defaults={
            'name': title, 'parent': folders[('erp_sales','sales_main')] if key in ['sales_details','sales_quote_rules'] else menus['erp_sales'], 'is_catalog': True, 'visible': True, 'status': True,
            'sort': {'sales_main': 5, 'sales_details': 30, 'sales_quote_rules': 40, 'sales_other': 85, 'sales_organized': 95}[key], 'web_path': '/erp/navigation/' + key})
    from system.catalog import ENTITIES
    from .foundation_catalog import DEFINITIONS
    profiles = {p['entity'] for p in DEFINITIONS.values()}
    primary = {'JobSheet','ProcessSchedule','ProcessCraft','StandCraft','DyeRecipe','WProcess','StuffWeight','RecordYield','OutWorkApply','ReworkOrder','GetJobSheetReceive'}
    for label, spec in RESOURCES.items():
        if spec['entity'] not in ENTITIES:
            continue
        menu = menus[spec['entity']]
        menu.name = spec['title']
        module, model = spec['module'], ENTITIES[spec['entity']]
        if module == 'erp_sales':
            group = 'sales_organized' if not hasattr(model, 'SOURCE_TABLE') else 'sales_other' if model.SOURCE_TABLE in ['Quote','QuoteDetail','QuoteAtte','OrderInfo','OrderInfoProcess'] else 'sales_main'
            if spec['table'] in ['OrderColor','OrderAtte','OrderProcess','OrderProcessPre','FixedPriceDetail','FixedPriceAtte','FixedPriceProcess']:
                group = 'sales_details'
            elif spec['table'] in ['QuoteItemPrice','QuotePriceAtte','QuotePriceProcess','FixedCanRecord','FixedCanDetail']:
                group = 'sales_quote_rules'
            menu.parent = folders[(module, group)]
            if spec['table'] in ['OrderMain','FixedPrice']:
                menu.sort = {'OrderMain':10,'FixedPrice':20}[spec['table']]
        elif spec['entity'] not in profiles:
            group = 'organized' if not hasattr(model, 'SOURCE_TABLE') else 'documents' if model.SOURCE_TABLE in primary else 'details'
            menu.parent = folders[(module, group)]
        # 原隐藏明细保留隐藏，所有来源模型/路由均不删除或复制。
        menu.save(update_fields=['name', 'parent', 'sort'])
    for menu in Menu.objects.select_related('parent').exclude(is_catalog=True):
        grant_ancestors(menu)
    return {'classified_resources': len(RESOURCES), 'modules': list(MODULES.values())}
