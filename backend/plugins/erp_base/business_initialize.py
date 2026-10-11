"""登记已实施业务菜单；已有角色授权由用户配置，重复初始化不扩大。"""
from django.db import transaction
from core.api import AUDIT_FIELDS
from system.catalog import ENTITIES
from system.models import (Menu, MenuButton, MenuField, Role, RoleMenuPermission,
                           RoleMenuButtonPermission, FieldPermission)
from plugins.erp_sales.resource_options import MODEL_FIELDS as SALES
from plugins.erp_sampling.resource_options import MODEL_FIELDS as SAMPLING
from plugins.erp_purchase.resource_options import MODEL_FIELDS as PURCHASE
from plugins.erp_warehouse.resource_options import MODEL_FIELDS as WAREHOUSE
from plugins.erp_production.resource_options import MODEL_FIELDS as PRODUCTION
from .business_api import policy_for

DOMAINS = [('erp_sales', '销售管理', SALES), ('erp_sampling', '打样管理', SAMPLING),
           ('erp_purchase', '采购管理', PURCHASE), ('erp_warehouse', '仓储管理', WAREHOUSE),
           ('erp_production', '生产管理', PRODUCTION)]
MAIN = {'CommercialPrice', 'SalesOrder', 'SalesOrderChange', 'SampleRequest', 'Recipe', 'ProcessCurveVersion',
        'PurchaseRequest', 'PurchaseOrder', 'PurchaseReturn', 'InventoryLot', 'StockReceipt', 'StockIssue',
        'StockTransfer', 'StockCount', 'StockAdjustment', 'InventoryMovement', 'StockBalance',
        'WorkCard', 'DyeBatch', 'ScheduleAssignment', 'ProductionRecipe','WeighingOrder',
        'QualityInspection','QualityDefect','ReworkOrder','LotTransformation','Package','LabelPrint',
        'Delivery','SalesReturn','CustomerComplaint'}
TITLES = {'confirm-post': '确认', 'receive-post': '收样', 'assign-post': '分配人员',
          'start-post': '开工', 'complete-post': '完成', 'send-post': '送版', 'reply-post': '客户回复',
          'approve-post': '审核', 'activate-post': '启用', 'retire-post': '停用',
          'clone-post': '复制新版本', 'save-document-post': '保存表头与明细',
          'post-post': '库存过账', 'reverse-post': '冲销', 'begin-post': '开始盘点', 'adjust-post': '应用盘点差异',
          'prepare-post': '展开路线', 'release-post': '下达', 'cancel-post': '取消',
          'schedule-post': '人工排程', 'reschedule-post': '改排', 'publish-post': '发布安排',
          'adopt-recipe-post': '采用生产配方','weigh-post':'记录实际称量','void-post':'作废采用','judge-post':'检验判定',
          'dispose-post':'数量处置','correct-post':'实际事实更正','close-post':'业务结案','skip-post':'明确跳过',
          'pause-post':'暂停','resume-post':'恢复','create-order-post':'建立计划料单','pack-post':'确认实际包装',
          'request-print-post':'请求打印或重打','deliver-post':'客户实际交付','handle-post':'开始处理'}


@transaction.atomic
def load():
    root = Menu.objects.get(component_name='erp')
    from .reports import REPORTS
    report_catalog,_=Menu.objects.get_or_create(component_name='erp_reports',defaults={'name':'业务查询','is_catalog':True,'parent':root,'web_path':'/erp/reports','sort':8})
    report_menus=[]
    for index,(key,spec) in enumerate(REPORTS.items(),1):
        menu,_=Menu.objects.get_or_create(component_name='erp_report_'+key,defaults={'name':spec['title'],'parent':report_catalog,
            'resource':'erp_report_'+key,'web_path':'/erp/reports/'+key,'component':'plugins/erp/Reports','sort':index})
        for suffix,label,path in [('query-get','查询',''),('export-get','导出','export/')]:
            MenuButton.objects.get_or_create(value='erp_report_'+key+':'+suffix,defaults={'menu':menu,'name':label,'method':0,'api':'/api/plugins/erp/reports/'+key+'/'+path})
        report_menus.append(menu)
    scan_menu,_=Menu.objects.get_or_create(component_name='erp_scanning',defaults={'name':'扫码识别与业务办理','parent':root,'resource':'erp_scanning','web_path':'/erp/scanning','component':'plugins/erp/Scanning','sort':9})
    for kind,title in [('employee','员工识别'),('workcard','工卡识别'),('package','包装识别')]:
        MenuButton.objects.get_or_create(value='erp_scanning:'+kind+'-get',defaults={'menu':scan_menu,'name':title,'method':0,'api':'/api/plugins/erp/identify/'+kind+'/'})
    report_menus.append(scan_menu)
    specs = [('erp_business_manager', 'ERP业务办理', {d[0] for d in DOMAINS}),
             ('erp_business_viewer', 'ERP业务查询', set()),
             ('erp_purchase_manager', '采购业务办理', {'erp_purchase'}),
             ('erp_purchase_viewer', '采购业务查询', set()),
             ('erp_warehouse_manager', '仓储业务办理', {'erp_warehouse'}),
             ('erp_warehouse_viewer', '仓储业务查询', set()),
             ('erp_production_manager', '生产业务办理', {'erp_production'}),
             ('erp_production_viewer', '生产业务查询', set()),
             ('erp_production_operator', '生产实际报工', {'erp_production','erp_warehouse'}),
             ('erp_quality_manager', '质量检验与处置', {'erp_production','erp_warehouse'}),
             ('erp_reports_viewer','ERP业务报表查询',set())]
    roles = [(Role.objects.get_or_create(key=key, defaults={'name': name}), writable) for key, name, writable in specs]
    for sort, (app, title, fields) in enumerate(DOMAINS, 2):
        catalog, _ = Menu.objects.get_or_create(component_name=app, defaults={
            'name': title, 'is_catalog': True, 'web_path': '/erp/' + app.removeprefix('erp_'),
            'parent': root, 'sort': sort})
        for index, name in enumerate(fields, 1):
            entity = app + '_' + name.lower()
            menu = Menu.objects.get(component_name=entity)
            menu.parent, menu.resource = catalog, entity
            menu.web_path, menu.component = catalog.web_path + '/' + name.lower(), 'plugins/erp/Business'
            menu.visible, menu.sort = name in MAIN, index
            menu.save(update_fields=['parent', 'resource', 'web_path', 'component', 'visible', 'sort'])
            for action, label in TITLES.items():
                MenuButton.objects.filter(value=entity + ':' + action).update(name=label)
    log = Menu.objects.get(component_name='erp_base_businessaction')
    log.parent, log.resource, log.web_path, log.component = root, log.component_name, '/erp/actions', 'plugins/erp/Business'
    log.save(update_fields=['parent', 'resource', 'web_path', 'component'])
    for (role, created), writable_apps in roles:
        if not created:
            continue
        field_grants=[];button_grants=[]
        for menu in [report_catalog,*report_menus]:
            RoleMenuPermission.objects.get_or_create(role=role,menu=menu)
            for button in MenuButton.objects.filter(menu=menu):button_grants.append(RoleMenuButtonPermission(role=role,menu_button=button,data_range=3))
        for menu in Menu.objects.filter(component_name__in=['erp', *[d[0] for d in DOMAINS]]):
            RoleMenuPermission.objects.get_or_create(role=role, menu=menu)
        for entity, model in ENTITIES.items():
            if model.__name__.startswith('Legacy'):continue
            if not model._meta.app_label.startswith('erp_') and entity not in ['dept', 'user', 'file']:
                continue
            menu = Menu.objects.get(component_name=entity)
            query_only = model._meta.app_label not in writable_apps
            if role.key=='erp_production_operator':
                query_only = model.__name__ not in {'WorkCardOperation','OperationExecution','ExecutionWorker',
                    'ExecutionMeasurement','PhysicalBatchExecution','ProductionRecipe','WeighingOrder','WeighingStage',
                    'WeighingLine','WeighingRecord','InventoryLot','StockIssue','StockIssueLine','StockReceipt','StockReceiptLine',
                    'LotTransformation','LotTransformationLine'}
            if role.key=='erp_quality_manager':
                query_only = model.__name__ not in {'QualityInspection','InspectionResultLine','QualityDisposition',
                    'QualityDefect','ReworkOrder','StockAdjustment','StockAdjustmentLine'}
            if model.__name__ in ['InventoryMovement', 'StockBalance']:
                query_only = True
            if model._meta.app_label != 'erp_base':
                RoleMenuPermission.objects.get_or_create(role=role, menu=menu)
            buttons = MenuButton.objects.filter(menu=menu)
            if query_only:
                buttons = buttons.filter(method=0)
            for button in buttons:
                button_grants.append(RoleMenuButtonPermission(role=role,menu_button=button,data_range=3))
            owned = set() if query_only else policy_for(model)['owned'][model]
            for column in MenuField.objects.filter(menu=menu):
                writable = not query_only and column.field_name not in {*AUDIT_FIELDS, 'legacy_id', *owned}
                field_grants.append(FieldPermission(role=role,field=column,
                    is_query=True,is_create=writable,is_update=writable))
        FieldPermission.objects.bulk_create(field_grants)
        RoleMenuButtonPermission.objects.bulk_create(button_grants)
        RoleMenuPermission.objects.get_or_create(role=role, menu=log)
