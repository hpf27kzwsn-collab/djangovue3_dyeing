"""基础资料保存与路线版本的业务操作。"""
from copy import copy
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Max
from django.db.models.deletion import RestrictedError
from django.utils import timezone
from . import models as m
from .choices import VersionStatus, LocationKind


CHILD_PARENTS = {
    m.PartyRole: 'party', m.PartyContact: 'party', m.PartyAddress: 'party',
    m.YarnSpecification: 'material', m.ChemicalSpecification: 'material',
    m.CustomerMaterial: 'material', m.StorageLocation: 'warehouse',
    m.MachineProcess: 'machine', m.RouteVersion: 'route', m.RouteStep: 'route_version',
}


def require_draft(version):
    if version.status != VersionStatus.DRAFT:
        raise ValidationError({'status': '已审核、使用中或停用的路线版本不能改写，请复制为新版本。'})


def has_references(instance):
    return any(relation.related_model.objects.filter(**{relation.field.name: instance}).exists()
               for relation in instance._meta.related_objects)


def validate_hierarchy(instance):
    ancestor = instance.parent
    while ancestor is not None:
        if ancestor.pk == instance.pk:
            raise ValidationError({'parent': '上级关系不能形成循环。'})
        ancestor = ancestor.parent


def validate_business(instance, original):
    if isinstance(instance, (m.Party, m.BusinessChoice, m.StorageLocation)):
        validate_hierarchy(instance)
    if isinstance(instance, m.BusinessChoice) and instance.pk:
        if m.BusinessChoice.objects.filter(parent=instance).exclude(namespace=instance.namespace).exists():
            raise ValidationError({'namespace': '已有下级字典项，数据类型必须与下级一致。'})
    if isinstance(instance, m.StorageLocation):
        if instance.kind == LocationKind.ZONE and instance.parent_id is not None:
            raise ValidationError({'parent': '库区不设置上级，实际库位可归属库区。'})
        if instance.parent_id is not None and instance.parent.kind != LocationKind.ZONE:
            raise ValidationError({'parent': '实际库位的上级必须是同仓库的库区。'})
        if instance.pk and m.StorageLocation.objects.filter(parent=instance).exists():
            if instance.kind != LocationKind.ZONE:
                raise ValidationError({'kind': '已有下级库位，当前记录必须保留为库区。'})
            if m.StorageLocation.objects.filter(parent=instance).exclude(warehouse=instance.warehouse).exists():
                raise ValidationError({'warehouse': '已有下级库位，不能迁移到其他仓库。'})
    if isinstance(instance, m.Unit) and original is not None:
        changed = any(getattr(instance, key) != getattr(original, key)
                      for key in ('dimension', 'base_unit_id', 'factor_to_base'))
        if changed and has_references(original):
            raise ValidationError({'factor_to_base': '单位已被引用，不能改变维度、基准或倍率；请建立新单位。'})
    if isinstance(instance, m.Material) and original is not None:
        if instance.kind != original.kind and has_references(original):
            raise ValidationError({'kind': '物料已被引用，不能改变类型；请建立新物料。'})
        if instance.stock_unit_id != original.stock_unit_id and has_references(original):
            raise ValidationError({'stock_unit': '物料已被引用，不能改变库存单位；请建立新物料。'})
    if isinstance(instance, m.Machine) and instance.number == '':
        instance.number = None
    if isinstance(instance, m.Machine) and original is not None and instance.factory_id != original.factory_id:
        if has_references(original):
            raise ValidationError({'factory': '机台已被引用，不能迁移工厂。'})
    if isinstance(instance, m.WorkCenter) and original is not None and instance.factory_id != original.factory_id:
        if has_references(original):
            raise ValidationError({'factory': '工作中心已被引用，不能迁移工厂。'})
    if isinstance(instance, m.RouteVersion):
        require_draft(instance)
        if instance.valid_from and instance.valid_to and instance.valid_to <= instance.valid_from:
            raise ValidationError({'valid_to': '失效时间必须晚于生效时间。'})
    if isinstance(instance, m.RouteStep):
        require_draft(instance.route_version)
        if instance.standard_minutes is not None and instance.standard_minutes < 0:
            raise ValidationError({'standard_minutes': '标准时长不能为负数。'})
        if instance.pk and m.RouteStep.objects.filter(predecessor=instance, sequence__lte=instance.sequence).exists():
            raise ValidationError({'sequence': '工序号必须早于引用它的后续节点。'})


@transaction.atomic
def save_master(model, data, instance=None):
    if model in CHILD_PARENTS:
        key = CHILD_PARENTS[model]
        parent = data[key] if key in data else getattr(instance, key)
        parent = type(parent).objects.select_for_update().get(pk=parent.pk)
    original = model.objects.select_for_update().get(pk=instance.pk) if instance is not None else None
    item = model() if original is None else copy(original)
    for key, value in data.items():
        setattr(item, key, value)
    if model in CHILD_PARENTS:
        key = CHILD_PARENTS[model]
        if original is not None and getattr(original, key + '_id') != getattr(item, key + '_id'):
            raise ValidationError({key: '不能更换明细所属主档。'})
        setattr(item, key, parent)
        item.dept_belong_id = parent.dept_belong_id
    validate_business(item, original)
    if model in (m.PartyContact, m.PartyAddress) and item.is_default:
        defaults = model.objects.filter(party=item.party, is_default=True).exclude(pk=item.pk)
        if model is m.PartyAddress:
            defaults = defaults.filter(kind=item.kind)
        defaults.update(is_default=False, modifier=item.modifier, update_datetime=timezone.now())
    item.full_clean()
    item.save()
    return item


def validate_delete(item):
    if isinstance(item, m.RouteVersion):
        require_draft(item)
    if isinstance(item, m.RouteStep):
        require_draft(item.route_version)


@transaction.atomic
def delete_masters(queryset):
    model = queryset.model
    if model in CHILD_PARENTS:
        key = CHILD_PARENTS[model]
        field = model._meta.get_field(key)
        list(field.related_model.objects.filter(pk__in=queryset.values(key)).order_by('pk').select_for_update())
    items = list(queryset.select_related(None).select_for_update())
    for item in items:
        validate_delete(item)
    try:
        queryset.filter(pk__in=[item.pk for item in items]).delete()
    except RestrictedError as error:
        raise ValidationError('资料正在被关联使用，请先处理相关记录。') from error


@transaction.atomic
def change_route_status(version, target, actor):
    item = m.RouteVersion.objects.select_for_update().get(pk=version.pk)
    allowed = {VersionStatus.APPROVED: {VersionStatus.DRAFT},
               VersionStatus.ACTIVE: {VersionStatus.APPROVED},
               VersionStatus.RETIRED: {VersionStatus.APPROVED, VersionStatus.ACTIVE}}
    if item.status not in allowed[target]:
        raise ValidationError({'status': '当前版本状态不能执行此操作。'})
    if target == VersionStatus.APPROVED:
        validate_business(item, None)
        nodes = list(m.RouteStep.objects.filter(route_version=item).order_by('sequence'))
        if not nodes:
            raise ValidationError({'status': '请先维护路线节点，再审核版本。'})
        for node in nodes:
            node.full_clean()
    item.status = target
    item.modifier = actor
    item.full_clean()
    item.save(update_fields=['status', 'modifier', 'update_datetime'])
    return item


@transaction.atomic
def clone_route(version, actor):
    route = m.Route.objects.select_for_update().get(pk=version.route_id)
    source = m.RouteVersion.objects.select_for_update().get(pk=version.pk)
    maximum = m.RouteVersion.objects.filter(route=route).aggregate(value=Max('version'))['value']
    copy = m.RouteVersion.objects.create(route=route, version=maximum + 1, remarks=source.remarks,
        creator=actor, modifier=actor, dept_belong_id=source.dept_belong_id)
    copied = {}
    for step in m.RouteStep.objects.filter(route_version=source).order_by('sequence'):
        copied[step.pk] = m.RouteStep.objects.create(route_version=copy, sequence=step.sequence,
            process=step.process, is_required=step.is_required,
            predecessor=copied[step.predecessor_id] if step.predecessor_id is not None else None,
            standard_minutes=step.standard_minutes, remarks=step.remarks,
            creator=actor, modifier=actor, dept_belong_id=copy.dept_belong_id)
    return copy
