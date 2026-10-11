from types import SimpleNamespace
from django.core.exceptions import ValidationError as ModelValidationError
from rest_framework import serializers
from core.api import CoreSerializer
from core.permissions import ApiPermission, scoped_queryset
from system.catalog import ENTITIES
from .models import RouteVersion, ColorStandard
from .services import save_master


class MasterDataSerializer(CoreSerializer):
    def get_fields(self):
        fields = super().get_fields()
        fields['legacy_id'].read_only = True
        if self.Meta.model is RouteVersion:
            fields['status'].read_only = True
        if self.Meta.model is ColorStandard:
            fields['source_sample'].read_only = True
        for field in fields.values():
            if isinstance(field, serializers.CharField):
                field.trim_whitespace = False
        request = self.context.get('request')
        if request is not None:
            for key, field in fields.items():
                if isinstance(field, serializers.PrimaryKeyRelatedField) and not field.read_only:
                    model = field.queryset.model
                    entity = next(name for name, target in ENTITIES.items() if target is model)
                    query_request = SimpleNamespace(user=request.user, method='GET', path=f'/api/system/{entity}/')
                    field.queryset = scoped_queryset(field.queryset, query_request) if ApiPermission().has_permission(query_request, None) else field.queryset.none()
        return fields

    def get_validators(self):
        # 默认联系人/地址先切换旧默认，再由模型校验所有唯一约束。
        return []

    def to_internal_value(self, data):
        owned = ['legacy_id', *(['status'] if self.Meta.model is RouteVersion else []),
                 *(['source_sample'] if self.Meta.model is ColorStandard else [])]
        denied = {key: '此字段由导入或专用业务操作维护。' for key in owned if key in data}
        if denied:
            raise serializers.ValidationError(denied)
        return super().to_internal_value(data)

    def create(self, validated_data):
        return self.write(validated_data)

    def update(self, instance, validated_data):
        return self.write(validated_data, instance)

    def write(self, data, instance=None):
        try:
            return save_master(self.Meta.model, data, instance)
        except ModelValidationError as error:
            raise serializers.ValidationError(error.message_dict) from error
