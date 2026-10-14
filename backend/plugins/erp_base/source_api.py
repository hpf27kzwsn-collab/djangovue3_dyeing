"""原形业务模型明确录入及草稿、确认、审核；不重演历史库存。"""
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from core.responses import success
from . import source_services as services
from .source_services import OWNED
from .business_api import BusinessViewSet,BusinessSerializer


class SourceRecordSerializer(BusinessSerializer):
    def get_fields(self):
        fields=super().get_fields()
        for name in OWNED:fields[name].read_only=True
        for name in self.Meta.model.SOURCE_DEFAULTS:fields[name].required=False
        if self.Meta.model.SOURCE_TABLE=='RecordYield':fields['old_guid'].required=False
        for field in fields.values():
            if isinstance(field,serializers.CharField):field.trim_whitespace=False
        return fields

    def to_internal_value(self,data):
        denied=OWNED.intersection(data)
        if denied:raise ValidationError({name:'由来源导入或明确办理动作维护。' for name in denied})
        return super().to_internal_value(data)

    def create(self,validated_data):
        actor=validated_data.pop('modifier',None)
        return services.write(self.Meta.model,validated_data,actor=actor)

    def update(self,instance,validated_data):
        actor=validated_data.pop('modifier',None)
        return services.write(self.Meta.model,validated_data,instance,actor=actor)


class SourceRecordViewSet(BusinessViewSet):
    def performed(self,service,values):
        item=service(self.get_object(),self.request.user,**values)
        return success(self.get_serializer(item).data)

    @action(methods=['post'],detail=True)
    def confirm(self,request,pk=None):return self.performed(services.confirm,{})

    @action(methods=['post'],detail=True)
    def approve(self,request,pk=None):return self.performed(services.approve,{})

    @action(methods=['post'],detail=True)
    def reopen(self,request,pk=None):
        from .business_api import parameters
        from rest_framework import serializers
        data=parameters(self,{'reason':serializers.CharField()})
        return self.performed(services.reopen,data)

    def destroy(self,request,*args,**kwargs):
        item=self.get_object()
        services.delete(self.get_queryset().filter(pk=item.pk),request.user)
        return success([], '删除成功')

    @action(methods=['delete'],detail=False)
    def multiple_delete(self,request):
        services.delete(self.get_queryset().filter(pk__in=request.data['keys']),request.user)
        return success([], '删除成功')

    @action(methods=['post'],detail=True)
    def calculate(self,request,pk=None):
        from .business_api import parameters
        entries = services.ENTRY_METHODS.get(self.get_queryset().model.SOURCE_TABLE, {})
        data=parameters(self,{'method':serializers.ChoiceField(choices=[
            'fields','amount_to_price',*services.PACK_METHODS,*['entry:'+entry for entry in entries]])})
        return self.performed(services.calculate,data)
