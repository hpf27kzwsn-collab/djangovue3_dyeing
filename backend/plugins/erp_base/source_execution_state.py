"""整链撤销的活动范围；原单据列表始终保留全部原行。"""
from django.core.exceptions import ValidationError
from django.db.models import Q
from .source_context import SourceDocumentContext


def active(query):
    cancelled=SourceDocumentContext.objects.filter(Q(effects__chain_cancelled__active=True) |
        Q(effects__package_retained__active=True) | Q(effects__work_archived__active=True) |
        Q(effects__trial_retained__active=True) | Q(effects__shift_retained__active=True) |
        Q(effects__calendar_retained__active=True) | Q(effects__equipment_retained__active=True) |
        Q(effects__foundation_retained__active=True), entity=query.model._meta.label).values('object_id')
    return query.exclude(pk__in=cancelled)


def require_available(item):
    context=SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk).first()
    if context is not None and context.effects.get('equipment_retained',{}).get('active'):
        raise ValidationError({'source':'本设备记录已替换或撤回留档，请先撤回对应设备办理。'})
    if context is not None and context.effects.get('calendar_retained',{}).get('active'):
        raise ValidationError({'source':'本日历明细已替换或撤回留档，请先撤回对应日历办理。'})
    if context is not None and context.effects.get('shift_retained',{}).get('active'):
        raise ValidationError({'source':'本人员记录已由班组调整替换留档，请先撤回对应调整。'})
    if context is not None and context.effects.get('trial_retained',{}).get('active'):
        raise ValidationError({'source':'本记录为试验报工替换留档，请先撤回该次办理。'})
    if context is not None and context.effects.get('work_archived',{}).get('active'):
        raise ValidationError({'source':'本工位记录已归档留存，请先撤回对应归档再继续办理。'})
    if context is not None and context.effects.get('package_retained',{}).get('active'):
        raise ValidationError({'source':'本包装已替换或撤回并留档，请使用当前包装或撤回对应替换操作。'})
    if context is not None and (context.effects.get('chain_cancelled',{}).get('active') or
            context.effects.get('chain_container',{}).get('active') or 'chain_compensation' in context.effects):
        raise ValidationError({'source':'本单已参与整链撤销；原行留档。继续办理前请撤回该次整链撤销，避免重复生效。'})
