"""原形业务模型明确录入及草稿、确认、审核；不重演历史库存。"""
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from core.api import CoreSerializer
from core.responses import success
from system.views import ResourceViewSet
from .business import record,snapshot,persist

OWNED={'legacy_id','source_batch','source_row','approval_stage','confirmed_at','confirmed_by','approved_at','approved_by'}


class SourceRecordSerializer(CoreSerializer):
    def get_fields(self):
        fields=super().get_fields()
        for name in OWNED:fields[name].read_only=True
        for field in fields.values():
            if isinstance(field,serializers.CharField):field.trim_whitespace=False
        return fields

    def to_internal_value(self,data):
        denied=OWNED.intersection(data)
        if denied:raise ValidationError({name:'由来源导入或明确办理动作维护。' for name in denied})
        return super().to_internal_value(data)

    def create(self,validated_data):
        item=self.Meta.model(**validated_data)
        item.approval_stage='draft' if item.SOURCE_DOCUMENT else None
        return persist(item)

    def update(self,instance,validated_data):
        if instance.approval_stage in ['confirmed','approved']:raise ValidationError('请先重新办理，再修改该单据。')
        for key,value in validated_data.items():setattr(instance,key,value)
        return persist(instance)


class SourceRecordViewSet(ResourceViewSet):
    @transaction.atomic
    def advance(self,expected,target):
        current=self.get_object()
        item=type(current).objects.select_for_update().get(pk=current.pk)
        if not item.SOURCE_DOCUMENT:raise ValidationError('此对象不是独立办理的业务单据。')
        if item.approval_stage!=expected:raise ValidationError('当前办理阶段不允许此动作。')
        before=snapshot(item);item.approval_stage=target
        if target=='confirmed':item.confirmed_at=timezone.now();item.confirmed_by=self.request.user
        if target=='approved':item.approved_at=timezone.now();item.approved_by=self.request.user
        persist(item,self.request.user);record(item,target,before,self.request.user)
        return success(self.get_serializer(item).data)

    @action(methods=['post'],detail=True)
    def confirm(self,request,pk=None):return self.advance('draft','confirmed')

    @action(methods=['post'],detail=True)
    def approve(self,request,pk=None):return self.advance('confirmed','approved')

    @action(methods=['post'],detail=True)
    @transaction.atomic
    def reopen(self,request,pk=None):
        from .business_api import parameters
        from rest_framework import serializers
        data=parameters(self,{'reason':serializers.CharField()})
        current=self.get_object()
        item=type(current).objects.select_for_update().get(pk=current.pk)
        if item.approval_stage not in ['confirmed','approved']:raise ValidationError('此单据当前不在确认或审核阶段。')
        before=snapshot(item);item.approval_stage='draft';persist(item,request.user)
        record(item,'reopen',before,request.user,data['reason'])
        return success(self.get_serializer(item).data)
