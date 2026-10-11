from types import SimpleNamespace
from django.core.exceptions import ValidationError as ModelValidationError
from django.db import transaction
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from core.api import CoreSerializer, serializer_for
from core.permissions import ApiPermission, scoped_queryset
from core.responses import success
from system.catalog import ENTITIES
from system.views import ResourceViewSet
from . import business


class ActionInput(serializers.Serializer):
    def get_fields(self):
        fields = super().get_fields()
        request = self.context['request']
        for field in fields.values():
            if isinstance(field, serializers.PrimaryKeyRelatedField):
                entity = next(name for name, target in ENTITIES.items() if target is field.queryset.model)
                scope = SimpleNamespace(user=request.user, method='GET', path=f'/api/system/{entity}/')
                field.queryset = scoped_queryset(field.queryset, scope) if ApiPermission().has_permission(scope, None) else field.queryset.none()
        return fields

    def to_internal_value(self, data):
        unknown = set(data) - set(self.fields)
        if unknown:
            raise serializers.ValidationError({key: '该操作不接收此字段。' for key in unknown})
        return super().to_internal_value(data)


def parameters(view, fields):
    serializer = type('BusinessInput', (ActionInput,), fields)(data=view.request.data, context={'request': view.request})
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


class ChildChanges(serializers.Serializer):
    upsert = serializers.ListField(child=serializers.DictField(), default=list)
    delete = serializers.ListField(child=serializers.IntegerField(min_value=1), default=list)


class DocumentInput(serializers.Serializer):
    head = serializers.DictField()
    children = serializers.DictField(child=ChildChanges())


def policy_for(model):
    from plugins.erp_sales.services import POLICY as sales
    from plugins.erp_sampling.services import POLICY as sampling
    from plugins.erp_purchase.services import POLICY as purchase
    from plugins.erp_warehouse.services import POLICY as warehouse
    return {'erp_sales': sales, 'erp_sampling': sampling, 'erp_purchase': purchase,
            'erp_warehouse': warehouse}[model._meta.app_label]


class BusinessSerializer(CoreSerializer):
    def get_fields(self):
        fields = super().get_fields()
        for key in policy_for(self.Meta.model)['owned'][self.Meta.model] | {'legacy_id'}:
            fields[key].read_only = True
        for field in fields.values():
            if isinstance(field, serializers.CharField):
                field.trim_whitespace = False
        request = self.context.get('request')
        if request is not None:
            for field in fields.values():
                if isinstance(field, serializers.PrimaryKeyRelatedField) and not field.read_only:
                    entity = next(name for name, target in ENTITIES.items() if target is field.queryset.model)
                    scope = SimpleNamespace(user=request.user, method='GET', path=f'/api/system/{entity}/')
                    field.queryset = scoped_queryset(field.queryset, scope) if ApiPermission().has_permission(scope, None) else field.queryset.none()
        return fields

    def get_validators(self):
        return []

    def to_internal_value(self, data):
        owned = policy_for(self.Meta.model)['owned'][self.Meta.model] | {'legacy_id', 'id'}
        denied = {key: '此字段由专用业务操作维护。' for key in owned if key in data}
        if denied:
            raise serializers.ValidationError(denied)
        return super().to_internal_value(data)

    def create(self, validated_data):
        return self.write(validated_data)

    def update(self, instance, validated_data):
        return self.write(validated_data, instance)

    def write(self, data, instance=None):
        try:
            return business.write(self.Meta.model, data, instance, policy_for(self.Meta.model))
        except ModelValidationError as error:
            raise serializers.ValidationError(serializers.as_serializer_error(error)) from error


class BusinessViewSet(ResourceViewSet):
    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        business.delete(self.get_queryset().filter(pk=item.pk), policy_for(type(item)))
        return success([], '删除成功')

    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request):
        business.delete(self.get_queryset().filter(pk__in=request.data['keys']), policy_for(self.queryset.model))
        return success([], '删除成功')

    def performed(self, service, parameters):
        item = service(self.get_object(), self.request.user, **parameters)
        return success(self.get_serializer(item).data, '操作成功')

    @action(methods=['post'], detail=True)
    @transaction.atomic
    def save_document(self, request, pk=None):
        """一次提交本层表头和明细；新增、修改、删除均在父锁内完成。"""
        payload = DocumentInput(data=request.data)
        payload.is_valid(raise_exception=True)
        payload = payload.validated_data
        item = business.locked(self.get_object())
        policy = policy_for(type(item))
        policy['editable'](item)
        head = self.get_serializer(item, data=payload['head'], partial=True)
        head.is_valid(raise_exception=True)
        item = head.save(modifier=request.user)
        allowed = {name for name, model in ENTITIES.items() if model in policy['parents']
                   and policy['parents'][model][1] == ''
                   and model._meta.get_field(policy['parents'][model][0]).related_model is type(item)}
        if set(payload['children']) - allowed:
            raise serializers.ValidationError({'children': '明细类型不属于本表头。'})
        for entity, changes in payload['children'].items():
            model = ENTITIES[entity]
            parent_key, root_path = policy_for(model)['parents'][model]
            if root_path or model._meta.get_field(parent_key).related_model is not type(item):
                raise serializers.ValidationError({'children': '明细类型不属于本表头。'})
            scope = SimpleNamespace(user=request.user, method='PATCH', path=f'/api/system/{entity}/{{id}}/')
            for row in changes['upsert']:
                data = dict(row)
                key = data.pop('id', None)
                verb = 'PATCH' if key is not None else 'POST'
                scope.method = verb
                scope.path = f'/api/system/{entity}/' + (f'{key}/' if key is not None else '')
                if not ApiPermission().has_permission(scope, None):
                    raise serializers.ValidationError({'children': '没有明细保存权限。'})
                previous = get_object_or_404(scoped_queryset(model.objects.all(), scope), pk=key, **{parent_key: item}) if key is not None else None
                if parent_key in data:
                    raise serializers.ValidationError({parent_key: '所属表头由整单保存确定，不接收明细中的父关联。'})
                if previous is None:
                    data[parent_key] = item.pk
                serializer = serializer_for(model, BusinessSerializer)(previous, data=data, partial=previous is not None, context={'request': request})
                serializer.is_valid(raise_exception=True)
                audit = {'modifier': request.user} if previous is not None else {'creator': request.user, 'modifier': request.user, 'dept_belong_id': item.dept_belong_id}
                serializer.save(**audit)
            if changes['delete']:
                scope.method, scope.path = 'DELETE', f'/api/system/{entity}/{{id}}/'
                if not ApiPermission().has_permission(scope, None):
                    raise serializers.ValidationError({'children': '没有明细删除权限。'})
                for key in changes['delete']:
                    get_object_or_404(scoped_queryset(model.objects.all(), scope), pk=key, **{parent_key: item})
                business.delete(scoped_queryset(model.objects.all(), scope).filter(pk__in=changes['delete'], **{parent_key: item}), policy_for(model))
        return success(self.get_serializer(item).data, '表头与明细已保存')


class BusinessActionViewSet(ResourceViewSet):
    http_method_names = ['get', 'head', 'options']
