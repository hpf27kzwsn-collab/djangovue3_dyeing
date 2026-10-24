from types import SimpleNamespace
from django.core.exceptions import ValidationError as ModelValidationError
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from core.api import CoreSerializer, serializer_for
from core.permissions import ApiPermission, scoped_queryset
from core.responses import success
from system.catalog import ENTITIES
from system.views import ResourceViewSet
from .business_policies import policy_for,document_children
from .document_services import save_document


class ActionInput(serializers.Serializer):
    def get_fields(self):
        fields = super().get_fields()
        request = self.context['request']
        for field in fields.values():
            if isinstance(field, serializers.ManyRelatedField):
                field = field.child_relation
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


class BusinessSerializer(CoreSerializer):
    def get_fields(self):
        fields = super().get_fields()
        for key in policy_for(self.Meta.model)['owned'][self.Meta.model]:
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
        owned = policy_for(self.Meta.model)['owned'][self.Meta.model] | {'id'}
        denied = {key: '此字段由专用业务操作维护。' for key in owned if key in data}
        if denied:
            raise serializers.ValidationError(denied)
        return super().to_internal_value(data)


class BusinessViewSet(ResourceViewSet):


    def performed(self, service, parameters):
        item = service(self.get_object(), self.request.user, **parameters)
        return success(self.get_serializer(item).data, '操作成功')

    @action(methods=['post'], detail=True)
    def save_document(self, request, pk=None):
        """校验参数及权限；整单保存交给明确的主从服务。"""
        payload = DocumentInput(data=request.data)
        payload.is_valid(raise_exception=True)
        payload = payload.validated_data
        item = self.get_object()
        head = self.get_serializer(item, data=payload['head'], partial=True)
        head.is_valid(raise_exception=True)
        allowed = document_children(type(item))
        if set(payload['children']) - {name for name,model in ENTITIES.items() if model in allowed}:
            raise serializers.ValidationError({'children': '明细类型不属于本表头。'})
        prepared = {}
        for entity, changes in payload['children'].items():
            model = ENTITIES[entity]
            parent_key = allowed[model]
            prepared[model] = {'upsert': [], 'delete': changes['delete']}
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
                from .source_api import SourceRecordSerializer
                serializer_class = SourceRecordSerializer
                # 归属由整单服务写入；验证新明细时只注入实际父项，不接收用户指定父项。
                if previous is None:data[parent_key] = item.pk
                serializer = serializer_for(model, serializer_class)(previous, data=data, partial=previous is not None, context={'request': request})
                serializer.is_valid(raise_exception=True)
                values = dict(serializer.validated_data)
                if previous is None:
                    from .source_entry_registry import ENTRY_RULES
                    from .source_entry_services import resolve_entry
                    from .source_services import parents
                    candidate=model(**{k:v for k,v in values.items() if not k.startswith('_')})
                    if ENTRY_RULES.get(model._meta.label) and resolve_entry(candidate,values.get('_entry'),parents(candidate)) is None:
                        raise serializers.ValidationError({'children':{entity:{'_entry':'本明细没有唯一可继承的业务类型，请明确选择；本次整单未保存。'}}})
                values.pop(parent_key,None)
                prepared[model]['upsert'].append({'instance':previous,'data':values})
            if changes['delete']:
                scope.method, scope.path = 'DELETE', f'/api/system/{entity}/{{id}}/'
                if not ApiPermission().has_permission(scope, None):
                    raise serializers.ValidationError({'children': '没有明细删除权限。'})
                for key in changes['delete']:
                    get_object_or_404(scoped_queryset(model.objects.all(), scope), pk=key, **{parent_key: item})
        item = save_document(item,request.user,head.validated_data,prepared)
        return success(self.get_serializer(item).data, '表头与明细已保存')


class BusinessActionViewSet(ResourceViewSet):
    http_method_names = ['get', 'head', 'options']
