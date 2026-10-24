"""完整原业务模型入口；首次建立专用角色，后续保留已有授权。"""
from django.apps import apps
from django.db import transaction
from system.models import Menu,MenuButton,MenuField,Role,RoleMenuPermission,RoleMenuButtonPermission,FieldPermission
from .source_documents import SourceRecord
from system.catalog import ENTITIES
from core.resources import resource_options


@transaction.atomic
def load():
    root=Menu.objects.get(component_name='erp')
    modules={'erp_base':'基础信息','erp_sales':'销售管理','erp_purchase':'采购管理','erp_sampling':'打样管理',
             'erp_production':'生产管理','erp_warehouse':'仓储管理','erp_quality':'质量管理'}
    folders={}
    for app,title in modules.items():
        catalog,_=Menu.objects.get_or_create(component_name=app,defaults={'name':title,'is_catalog':True,'parent':root,'web_path':'/erp/'+app.removeprefix('erp_')})
        folder,_=Menu.objects.get_or_create(component_name=app+'_original',defaults={'name':'业务资料','is_catalog':True,'parent':catalog,'web_path':catalog.web_path+'/original','sort':90})
        folders[app]=folder
    records=[model for model in ENTITIES.values() if issubclass(model,SourceRecord)]
    for index,model in enumerate(records,1):
        entity=model._meta.app_label+'_'+model._meta.model_name
        menu=Menu.objects.get(component_name=entity)
        menu.name=resource_options(model).get('title',str(model._meta.verbose_name))
        menu.parent=folders[model._meta.app_label];menu.resource=entity;menu.web_path=menu.parent.web_path+'/'+model._meta.model_name
        menu.component='plugins/erp/Business';menu.visible=True;menu.sort=index
        menu.save(update_fields=['name','parent','resource','web_path','component','visible','sort'])
