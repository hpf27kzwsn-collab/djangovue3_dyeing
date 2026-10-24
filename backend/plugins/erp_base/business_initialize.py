"""客户岗位直接授权本地业务主链；不创建旧资料/备用体系角色。"""
from django.db import transaction
from core.api import AUDIT_FIELDS
from system.catalog import ENTITIES
from system.models import (Menu, MenuButton, MenuField, Role, RoleMenuPermission,
                           RoleMenuButtonPermission, FieldPermission)
from .source_documents import SourceRecord
from .source_services import OWNED

DOMAINS = [('erp_base','基础信息'), ('erp_sales','销售管理'), ('erp_purchase','采购管理'),
           ('erp_sampling','打样管理'), ('erp_production','生产管理'),
           ('erp_warehouse','仓储管理'), ('erp_quality','质量管理')]


@transaction.atomic
def load():
    root = Menu.objects.get(component_name='erp')
    for sort, (app, title) in enumerate(DOMAINS, 1):
        Menu.objects.get_or_create(component_name=app, defaults={
            'name':title,'is_catalog':True,'parent':root,'web_path':'/erp/'+app.removeprefix('erp_'),'sort':sort})
    from .reports import REPORTS
    report_root, _ = Menu.objects.get_or_create(component_name='erp_reports', defaults={
        'name':'业务查询','is_catalog':True,'parent':root,'web_path':'/erp/reports','sort':20})
    report_menus = [report_root]
    for index, (key, spec) in enumerate(REPORTS.items(), 1):
        menu, _ = Menu.objects.update_or_create(component_name='erp_report_'+key, defaults={
            'name':spec['title'],'parent':report_root,'resource':'erp_report_'+key,
            'web_path':'/erp/reports/'+key,'component':'plugins/erp/Reports','sort':index,'status':True})
        for suffix,title,path in [('query-get','查询',''),('export-get','导出','export/')]:
            MenuButton.objects.get_or_create(value='erp_report_'+key+':'+suffix, defaults={
                'menu':menu,'name':title,'method':0,'api':'/api/plugins/erp/reports/'+key+'/'+path})
        report_menus.append(menu)
    scan, _ = Menu.objects.get_or_create(component_name='erp_scanning', defaults={
        'name':'扫码识别','parent':root,'resource':'erp_scanning','web_path':'/erp/scanning',
        'component':'plugins/erp/Scanning','sort':21})
    for kind,title in [('employee','员工识别'),('workcard','工卡识别'),('package','包装识别')]:
        MenuButton.objects.get_or_create(value='erp_scanning:'+kind+'-get', defaults={
            'menu':scan,'name':title,'method':0,'api':'/api/plugins/erp/identify/'+kind+'/'})
    report_menus.append(scan)
    specs = [('erp_business_manager','ERP业务办理',{a for a,_ in DOMAINS}),
             ('erp_business_viewer','ERP业务查询',set()),
             ('erp_reports_viewer','ERP业务报表查询',set())]
    specs += [(app+'_manager',title+'办理',{app}) for app,title in DOMAINS]
    specs += [(app+'_viewer',title+'查询',set()) for app,title in DOMAINS]
    specs += [('erp_production_operator','生产实际报工',{'erp_production','erp_warehouse'}),
              ('erp_quality_manager','质量检验与处置',{'erp_quality','erp_warehouse'})]
    # 相同岗位键只生成一次；已有手工授权不被初始化覆盖。
    roles = {key:(name,writable) for key,name,writable in specs}
    for key,(name,writable_apps) in roles.items():
        role, created = Role.objects.get_or_create(key=key, defaults={'name':name})
        if not created:
            continue
        buttons = []; fields = []
        for menu in [root,*report_menus]:
            RoleMenuPermission.objects.get_or_create(role=role,menu=menu)
            buttons.extend(RoleMenuButtonPermission(role=role,menu_button=b,data_range=3)
                           for b in MenuButton.objects.filter(menu=menu,method=0))
        for entity, model in ENTITIES.items():
            if not model._meta.app_label.startswith('erp_') and entity not in ['dept','user','file']:
                continue
            menu = Menu.objects.get(component_name=entity)
            writable = model._meta.app_label in writable_apps and (
                issubclass(model,SourceRecord) or model.__name__ in {'QualityQuantityBatch','QualityQuantitySource'})
            if key == 'erp_production_operator':
                writable = writable and model.SOURCE_TABLE in {
                    'WProcess','WProcessStep','JobShiftEmp','WProcessAdditional','StuffWeight',
                    'StuffWeightPhase','StuffWeightDetail','StuffWeightRecord','RecordYield','RecordEmp'}
            RoleMenuPermission.objects.get_or_create(role=role,menu=menu)
            permitted = MenuButton.objects.filter(menu=menu)
            if not writable:
                permitted = permitted.filter(method=0)
            buttons.extend(RoleMenuButtonPermission(role=role,menu_button=b,data_range=3) for b in permitted)
            for column in MenuField.objects.filter(menu=menu):
                edit = writable and column.field_name not in {*AUDIT_FIELDS,*OWNED,'id'}
                fields.append(FieldPermission(role=role,field=column,is_query=True,is_create=edit,is_update=edit))
        FieldPermission.objects.bulk_create(fields)
        RoleMenuButtonPermission.objects.bulk_create(buttons)
