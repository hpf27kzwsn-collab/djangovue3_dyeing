from django.db import transaction, models, connections
from django.db.models import Q, prefetch_related_objects
from django.utils.functional import cached_property
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from timezone_field import TimeZoneField
from timezone_field.rest_framework import TimeZoneSerializerField
from django_restql.mixins import DynamicFieldsMixin, QueryArgumentsMixin
from .responses import success
from .permissions import ApiPermission, scoped_queryset, field_access
from .resources import resource_options, relation_label

AUDIT_FIELDS = ['creator', 'modifier', 'dept_belong', 'create_datetime', 'update_datetime']


def rename_primary_key(model, old_key, new_key, renamed):
    identity = (model, old_key)
    if identity in renamed:
        return
    renamed.add(identity)
    for relation in model._meta.get_fields(include_hidden=True):
        if relation.auto_created and not relation.concrete and (relation.one_to_many or relation.one_to_one):
            field = relation.field
            if isinstance(field, models.ForeignKey) and field.target_field == model._meta.pk:
                rows = relation.related_model._base_manager.filter(**{field.attname: old_key})
                if field.primary_key:
                    for key in rows.values_list('pk', flat=True):
                        rename_primary_key(relation.related_model, key, new_key, renamed)
                else:
                    rows.update(**{field.attname: new_key})
    model._base_manager.filter(pk=old_key).update(**{model._meta.pk.attname: new_key})


class CoreSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    def get_fields(self):
        fields = super().get_fields()
        config = resource_options(self.Meta.model)
        for key, options in config.get('fields', {}).items():
            if key not in fields:
                fields[key] = serializers.ReadOnlyField(**({'source':options['source']} if options.get('source',key) != key else {}))
        fields = {key: field for key, field in fields.items() if key not in config.get('serializer_exclude_fields', [])}
        return fields

    @transaction.atomic
    def update(self, instance, validated_data):
        primary = instance._meta.pk
        value = validated_data.pop(primary.name, getattr(instance, primary.name))
        new_key = primary.target_field.value_from_object(value) if primary.is_relation else value
        instance = super().update(instance, validated_data)
        if new_key != instance.pk:
            rename_primary_key(type(instance), instance.pk, new_key, set())
            instance.pk = new_key
            instance.refresh_from_db()
        return instance

    @cached_property
    def field_permissions(self):
        return field_access(self.context['request'].user, self.Meta.model)

    def to_internal_value(self, data):
        access = self.field_permissions
        operation = 'is_create' if self.instance is None else 'is_update'
        denied = [key for key in data if key in access and not access[key][operation]]
        if denied:
            raise serializers.ValidationError({key: '无字段操作权限' for key in denied})
        return super().to_internal_value(data)

    def to_representation(self, instance):
        result = super().to_representation(instance)
        access = self.field_permissions
        for key in list(result):
            source = self.fields[key].source_attrs[0]
            if source in access and not access[source]['is_query']:
                result.pop(key, None)
        requested = self.context['request'].query_params.get('_fields')
        if requested:
            result = {key: value for key, value in result.items() if key in requested.split(',')}
        if 'creator' in result and not self.context['request'].query_params.get('query') and not requested:
            result['creator_name'] = str(instance.creator) if instance.creator else ''
        if not requested and not self.context['request'].query_params.get('query'):
            for field in instance._meta.fields + tuple(instance._meta.many_to_many):
                if field.is_relation and field.name in result:
                    value = getattr(instance, field.name)
                    result[field.name+'_label'] = '、'.join(relation_label(obj) for obj in value.all()) if field.many_to_many else relation_label(value) if value else ''
        return result


def serializer_for(model, base=CoreSerializer):
    excluded = ['password', 'groups', 'user_permissions'] if model is get_user_model() else []
    meta = type('Meta', (), {'model': model, 'exclude': excluded, 'read_only_fields': AUDIT_FIELDS})
    attributes = {'Meta': meta}
    for field in model._meta.fields:
        if isinstance(field, TimeZoneField):
            attributes[field.name] = TimeZoneSerializerField(required=not field.blank and not field.has_default())
    return type(f'{model.__name__}Serializer', (base,), attributes)


class ModelViewSet(QueryArgumentsMixin, viewsets.ModelViewSet):
    permission_classes = [ApiPermission]

    def initial(self, request, *args, **kwargs):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            request._request.audit_data = request.data
        return super().initial(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        relations = [field for field in queryset.model._meta.fields if field.is_relation]
        many = [field.name for field in queryset.model._meta.many_to_many]
        return scoped_queryset(queryset.select_related(*(field.name for field in relations)).prefetch_related(*many), self.request)

    def filter_queryset(self, queryset):
        serializer = self.get_serializer()
        fields = {f.name:f for f in list(queryset.model._meta.fields)+list(queryset.model._meta.many_to_many)
                  if f.name in serializer.fields and not serializer.fields[f.name].write_only}
        access = field_access(self.request.user, queryset.model)
        for key, value in self.request.query_params.items():
            field = key.split('__')[0]
            if field in fields and (field not in access or access[field]['is_query']):
                terminal = fields[field]
                many = terminal.many_to_many
                for part in key.split('__')[1:]:
                    if not terminal.is_relation:
                        break
                    related_fields = {f.name: f for f in terminal.related_model._meta.get_fields()}
                    if part not in related_fields:
                        break
                    terminal = related_fields[part]
                    many = many or terminal.many_to_many or terminal.one_to_many
                if value == 'null':
                    value = None
                elif key.endswith('__in'):
                    value = value.split(',')
                    if isinstance(terminal, models.BooleanField):
                        value = [item.lower() == 'true' for item in value]
                elif isinstance(terminal, models.BooleanField) or key.endswith('__isnull'):
                    value = value.lower() == 'true'
                queryset = queryset.filter(**{key: value})
                if many:
                    queryset = queryset.distinct()
        search = self.request.query_params.get('search')
        if search:
            predicate = Q(pk__in=[])
            searchable = getattr(self, 'search_fields', resource_options(queryset.model).get('search_fields', [key for key, field in fields.items()
                                 if isinstance(field, (models.CharField, models.TextField))])
            )
            for key in searchable:
                source = key.split('__')[0]
                if source in fields and (source not in access or access[source]['is_query']):
                    predicate |= Q(**{key + '__icontains': search})
            queryset = queryset.filter(predicate).distinct()
        order = self.request.query_params.get('ordering')
        if order:
            queryset = queryset.order_by(*[key for key in order.split(',') if key.lstrip('-') in fields and
                                           (key.lstrip('-') not in access or access[key.lstrip('-')]['is_query'])])
        return queryset

    def audit(self):
        fields = {f.name for f in self.queryset.model._meta.fields}
        return {key: value for key, value in {'creator': self.request.user, 'modifier': self.request.user,
                'dept_belong_id': self.request.user.dept_id}.items() if key.removesuffix('_id') in fields}

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        serializer.save(**self.audit())
        return success(serializer.data, '新增成功')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset.prefetch_related(None))
        if page:
            batch_size = connections[queryset.db].features.max_query_params or len(page)
            for offset in range(0, len(page), batch_size):
                prefetch_related_objects(page[offset:offset + batch_size], *queryset._prefetch_related_lookups)
        return self.get_paginated_response(self.get_serializer(page, many=True).data)

    def retrieve(self, request, *args, **kwargs):
        return success(self.get_serializer(self.get_object()).data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        audit = self.audit()
        audit.pop('creator', None)
        audit.pop('dept_belong_id', None)
        serializer.save(**audit)
        return success(serializer.data, '更新成功')

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return success([], '删除成功')

    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request):
        self.get_queryset().filter(pk__in=request.data['keys']).delete()
        return success([], '删除成功')

    @action(methods=['post'], detail=False)
    def get_by_ids(self, request):
        return success(self.get_serializer(self.get_queryset().filter(pk__in=request.data['ids']), many=True).data)

    @action(methods=['get'], detail=False)
    def field_permission(self, request):
        return success(field_access(request.user, self.queryset.model))
