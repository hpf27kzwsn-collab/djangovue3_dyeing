from rest_framework import serializers
from rest_framework.decorators import action
from .business_api import parameters
from .source_order_card_api import row,target_create


class RecipeReferencesMixin:
    @action(methods=['post'],detail=True,url_name='adopt_recipe_references')
    def adopt_recipe_references(self,request,pk=None):
        from .source_registration_flow import recipe_references
        from .source_api import event_fields,created_document
        data=parameters(self,{**event_fields(),'color':row('DyeLabColor',allow_null=True,required=False),
            'original':row('DyeRecipe',allow_null=True,required=False),'standard':row('DyeRecipe',allow_null=True,required=False)})
        return created_document(recipe_references(self.get_object(),actor=request.user,**data))


class LoadingMixin:
    @action(methods=['post'],detail=True,url_name='add_outgoing_lines')
    def add_outgoing_lines(self,request,pk=None):
        from .source_registration_flow import load_lines
        from .source_api import event_fields
        from core.responses import success
        target_create(request,'ProdLoadingDetail')
        data=parameters(self,{**event_fields(),'lines':row('ProdOutDetail',many=True)})
        return success(load_lines(self.get_object(),actor=request.user,**data),'已添加装车明细')


class JobWarehouseMixin:
    @action(methods=['post'],detail=True,url_name='register_outgoing')
    def register_outgoing(self,request,pk=None):
        from .source_registration_flow import out_of_job_warehouse
        from .source_api import event_fields,number_field,created_document
        target_create(request,'JobOutWareEdit')
        data=parameters(self,{**event_fields(),'rolls':number_field(),'weight':number_field()})
        return created_document(out_of_job_warehouse(self.get_object(),actor=request.user,**data))
