from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers
from rest_framework.decorators import action
from core.api import CoreSerializer
from core.responses import success
from system.views import ResourceViewSet
from . import numbering


class DecimalTextInteger(serializers.IntegerField):
    def to_representation(self, value):
        return str(value)


class NumberingSerializer(CoreSerializer):
    start_number = DecimalTextInteger(min_value=0, max_value=999999999999999999, required=False)
    last_number = DecimalTextInteger(read_only=True, allow_null=True)

    def get_fields(self):
        fields = super().get_fields()
        from .numbering_registry import registry
        fields['target_model'] = serializers.ChoiceField(choices=sorted({label for label, key in registry()}))
        for field in ['scope_filters', 'entry_name', 'last_number']:
            fields[field].read_only = True
        return fields

    def get_validators(self):
        return []

    def to_internal_value(self, data):
        denied = set(data).intersection(['last_number', 'scope_filters', 'entry_name'])
        if denied:
            raise serializers.ValidationError({key: '此字段由编号服务维护。' for key in denied})
        return super().to_internal_value(data)

    def create(self, validated_data):
        return numbering.save_rule(validated_data, self.context['request'].user)

    def update(self, instance, validated_data):
        return numbering.save_rule(validated_data, self.context['request'].user, instance)


class NumberingViewSet(ResourceViewSet):
    @action(methods=['get'], detail=False)
    def catalog(self, request):
        from .numbering_registry import catalog
        return success(catalog())

    @action(methods=['post'], detail=False)
    def preview(self, request):
        data = dict(request.data)
        pk = data.pop('_id', None)
        instance = None if pk is None else self.get_queryset().get(pk=pk)
        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        rule = numbering.save_rule(serializer.validated_data, request.user, instance, commit=False)
        return success(numbering.preview(rule))

    @action(methods=['post'], detail=True)
    @transaction.atomic
    def synchronize(self, request, pk=None):
        from django.apps import apps
        from .business import record, snapshot
        instance = self.get_object()
        numbering.lock_model(apps.get_model(instance.target_model))
        instance.refresh_from_db()
        before = snapshot(instance)
        numbering.sync_model(apps.get_model(instance.target_model))
        instance.refresh_from_db()
        record(instance, 'numbering_synchronize', before, request.user, '按实际已存编号同步上限；不修改原编号')
        return success(self.get_serializer(instance).data, '流水上限已同步')

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        from django.apps import apps
        from .business import record, snapshot
        item = self.get_object()
        numbering.lock_model(apps.get_model(item.target_model))
        item.refresh_from_db()
        if numbering.baseline(item) is not None:
            raise ValidationError('已使用的编号规则请保留流水上限；可关闭自动编号，不能删除后重新取旧号。')
        record(item, 'numbering_delete', snapshot(item), request.user, '删除尚未使用的规则')
        item.delete()
        return success([], '已删除未使用规则')

    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request):
        raise ValidationError('请逐条处理编号规则，已使用规则需保留流水上限。')
