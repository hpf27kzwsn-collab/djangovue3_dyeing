from types import SimpleNamespace
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from core.permissions import ApiPermission
from .business_api import parameters
from .source_phase3_operations import model


def target_create(request,table):
    entity=model(table)._meta.label_lower.replace('.','_')
    if not ApiPermission().has_permission(SimpleNamespace(user=request.user,method='POST',path='/api/system/'+entity+'/'),None):
        raise PermissionDenied('没有目标业务单据的新增权限。')


def row(table,**kwargs):return serializers.PrimaryKeyRelatedField(queryset=model(table).objects.all(),**kwargs)


class OrderCardMixin:
    @action(methods=['post'],detail=True,url_name='open_first_card')
    def open_first_card(self,request,pk=None):
        from .source_order_card import open_card
        from .source_api import created_document
        from .reports import Reader
        for table in ['JobSheet','JobCombineOrder']:target_create(request,table)
        data=parameters(self,{'head':row('OrderMain'),
            'quantity':serializers.DecimalField(max_digits=10,decimal_places=2,allow_null=True,required=False,default=None),
            'rolls':serializers.DecimalField(max_digits=10,decimal_places=2,allow_null=True,required=False,default=None),
            'unit':serializers.IntegerField(allow_null=True,required=False,default=None),'yarn':serializers.ChoiceField(choices=['本厂采购','客户来纱']),
            'route':row('p_FieldValid',allow_null=True,required=False,default=None),
            'number_prefix':serializers.CharField(min_length=3,max_length=3,allow_null=True,allow_blank=True,required=False,default=None,trim_whitespace=False),
            'members':serializers.ListField(child=serializers.DictField(),default=list),
            'assignments':serializers.ListField(child=serializers.DictField(),default=list),
            'at':serializers.DateTimeField(),'reason':serializers.CharField()})
        selected=[]
        for member in data.pop('members'):
            class Member(serializers.Serializer):
                line_id=serializers.IntegerField()
                quantity=serializers.DecimalField(max_digits=10,decimal_places=2,allow_null=True)
            s=Member(data=member);s.is_valid(raise_exception=True)
            line=get_object_or_404(Reader(request).source(model('OrderColor'),list(model('OrderColor').SOURCE_FIELDS.values())),pk=s.validated_data['line_id'])
            selected.append({'line':line,'quantity':s.validated_data['quantity']})
        if data['route'] is not None:target_create(request,'JobProcess')
        if data['assignments']:target_create(request,'JobAssign')
        return created_document(open_card(self.get_object(),request.user,members=selected,**data))


class RouteMixin:
    @action(methods=['post'],detail=True,url_name='adopt_route')
    def adopt_route(self,request,pk=None):
        from .source_order_card import adopt_route
        from .source_api import created_document
        target_create(request,'JobProcess')
        data=parameters(self,{'route':row('p_FieldValid'),'at':serializers.DateTimeField(),'reason':serializers.CharField()})
        return created_document(adopt_route(self.get_object(),actor=request.user,**data))


class ReviewCardMixin:
    @action(methods=['post'],detail=True,url_name='open_rework_card')
    def open_rework_card(self,request,pk=None):
        from django.core.exceptions import ValidationError
        from .source_api import card_fields,nullable_text,created_document
        from .source_cross_card import reprocess
        from .source_stock_services import raw
        for table in ['JobSheet','JobProcess']:target_create(request,table)
        data=parameters(self,{**card_fields(),'job':row('JobSheet'),
            'sheet_kind':serializers.IntegerField(),'job_kind':nullable_text()})
        review=self.get_object();job=data.pop('job')
        number=raw(review,'JobSheetNo')
        if number and number.rstrip().upper()!=(raw(job,'SheetNo') or '').rstrip().upper():
            raise ValidationError({'job':'所选工卡与评审单原工卡号不一致。'})
        for process in data['processes']:
            if process.source_parent_1_id is not None:
                belongs=process.source_parent_1_id==job.pk
            else:
                series=raw(process,'SheetSeries');target=raw(job,'SheetSeries')
                belongs=series is not None and target is not None and series.rstrip().upper()==target.rstrip().upper()
            if not belongs:raise ValidationError({'processes':'回修采用的工序必须来自所选来源工卡。'})
        return created_document(reprocess(job,request.user,review=review,**data))
