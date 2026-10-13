"""完整原业务模型入口；首次建立专用角色，后续保留已有授权。"""
from django.apps import apps
from django.db import transaction
from system.models import Menu,MenuButton,MenuField,Role,RoleMenuPermission,RoleMenuButtonPermission,FieldPermission
from .source_documents import SourceRecord
from .source_api import OWNED


@transaction.atomic
def load():
    root=Menu.objects.get(component_name='erp')
    modules={'erp_base':'基础信息','erp_sales':'销售管理','erp_purchase':'采购管理','erp_sampling':'打样管理',
             'erp_production':'生产管理','erp_warehouse':'仓储管理','erp_quality':'质量管理'}
    folders={}
    for app,title in modules.items():
        catalog,_=Menu.objects.get_or_create(component_name=app,defaults={'name':title,'is_catalog':True,'parent':root,'web_path':'/erp/'+app.removeprefix('erp_')})
        folder,_=Menu.objects.get_or_create(component_name=app+'_original',defaults={'name':'完整旧业务资料','is_catalog':True,'parent':catalog,'web_path':catalog.web_path+'/original','sort':90})
        folders[app]=folder
    records=[model for model in apps.get_models() if issubclass(model,SourceRecord)]
    for index,model in enumerate(records,1):
        entity=model._meta.app_label+'_'+model._meta.model_name
        menu=Menu.objects.get(component_name=entity)
        menu.parent=folders[model._meta.app_label];menu.resource=entity;menu.web_path=menu.parent.web_path+'/'+model._meta.model_name
        menu.component='plugins/erp/Business';menu.visible=True;menu.sort=index
        menu.save(update_fields=['parent','resource','web_path','component','visible','sort'])
    for rolekey,title,write in [('erp_original_manager','完整旧业务资料办理',True),('erp_original_viewer','完整旧业务资料查询',False)]:
        role,created=Role.objects.get_or_create(key=rolekey,defaults={'name':title})
        if not created:continue
        button_grants=[];fields=[]
        for folder in folders.values():
            RoleMenuPermission.objects.get_or_create(role=role,menu=folder)
            RoleMenuPermission.objects.get_or_create(role=role,menu=folder.parent)
        RoleMenuPermission.objects.get_or_create(role=role,menu=root)
        for model in records:
            entity=model._meta.app_label+'_'+model._meta.model_name;menu=Menu.objects.get(component_name=entity)
            RoleMenuPermission.objects.get_or_create(role=role,menu=menu)
            buttons=MenuButton.objects.filter(menu=menu)
            if not write:buttons=buttons.filter(method=0)
            button_grants.extend(RoleMenuButtonPermission(role=role,menu_button=button,data_range=3) for button in buttons)
            for field in MenuField.objects.filter(menu=menu):
                writable=write and field.field_name not in OWNED|{'creator','modifier','dept_belong','create_datetime','update_datetime','id'}
                fields.append(FieldPermission(role=role,field=field,is_query=True,is_create=writable,is_update=writable))
        FieldPermission.objects.bulk_create(fields);RoleMenuButtonPermission.objects.bulk_create(button_grants)
