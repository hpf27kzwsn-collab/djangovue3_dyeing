import json
from types import SimpleNamespace
from django.apps import apps
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from core.permissions import ApiPermission,scoped_queryset,field_access
from core.responses import success
from system.views import ResourceViewSet
from .legacy_services import rows


class LegacyReadViewSet(ResourceViewSet):
    http_method_names=['get','head','options']


class LegacySourceViewSet(LegacyReadViewSet):
    @action(methods=['get'],detail=True)
    def rows(self,request,pk=None):
        source=self.get_object()
        fields=field_access(request.user,type(source))
        if not request.user.is_superuser and (not fields['columns']['is_query'] or not fields['primary_key']['is_query']):raise PermissionDenied('未授权读取完整旧来源字段及主键。')
        Input=type('SourcePage',(serializers.Serializer,),{'page':serializers.IntegerField(min_value=1,default=1),'limit':serializers.IntegerField(min_value=1,max_value=200,default=50)})
        data=Input(data=request.query_params);data.is_valid(raise_exception=True);data=data.validated_data
        first=(data['page']-1)*data['limit']+1
        result=[] if first>source.row_count else rows(source,first,data['limit'])
        return success({'table':source.schema_name+'.'+source.table_name,'count':source.row_count,'columns':source.columns,'primary_key':source.primary_key,'rows':result})


class LegacyMapViewSet(LegacyReadViewSet):
    @action(methods=['get'],detail=True)
    def compare(self,request,pk=None):
        mapping=self.get_object();model=apps.get_model(mapping.target_model)
        scope=SimpleNamespace(user=request.user,method='GET',path='/api/system/'+model._meta.app_label+'_'+model._meta.model_name+'/')
        if not ApiPermission().has_permission(scope,None):raise PermissionDenied('未授权查询对应新记录。')
        target=get_object_or_404(scoped_queryset(model.objects.all(),scope),pk=mapping.target_id)
        fields=field_access(request.user,model)
        if not request.user.is_superuser and any(not fields[key]['is_query'] for key in mapping.mapped_fields):raise PermissionDenied('对应新记录的对照字段未全部授权。')
        original=rows(mapping.source_table,mapping.row_number,1)[0]
        data=[]
        from .legacy_import import comparison_value
        for field,spec in mapping.mapped_fields.items():
            old=original['values'][spec['source']];new=getattr(target,field)
            if spec['conversion']=='foreign_code':
                if new is not None:
                    related_model=type(new);related_scope=SimpleNamespace(user=request.user,method='GET',path='/api/system/'+related_model._meta.app_label+'_'+related_model._meta.model_name+'/')
                    related_fields=field_access(request.user,related_model)
                    if not ApiPermission().has_permission(related_scope,None) or not scoped_queryset(related_model.objects.all(),related_scope).filter(pk=new.pk).exists() or not request.user.is_superuser and not related_fields[spec['target_attribute']]['is_query']:
                        raise PermissionDenied('未授权读取关联记录的对照代码。')
                expected=old;new=None if new is None else getattr(new,spec['target_attribute'])
            else:expected=comparison_value(model._meta.get_field(field),old,spec['conversion'])
            data.append({'field':field,'title':str(model._meta.get_field(field).verbose_name),'old_field':spec['source'],'old_value':old,
                'new_value':str(new) if new is not None else None,'matches':new==expected})
        return success({'old_key':original['key'],'source_table':mapping.source_table_id,'source_row':mapping.row_number,'target':mapping.target_model,'rows':data})
