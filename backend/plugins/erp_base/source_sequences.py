"""新业务在原自增字段上的明确编号；旧行导入不调用本服务。"""
from django.db import models
from .models import ErpModel


class SourceIdentitySequence(ErpModel):
    namespace = models.CharField('原表及自增字段', max_length=200, unique=True)
    last_number = models.BigIntegerField('已采用号码', default=0)

    class Meta:
        db_table = 'erp_base_sourceidentitysequence'
        verbose_name = verbose_name_plural = '原字段新业务自增序列'


def allocate(item, actor):
    from .business import persist, locked
    for key in item.SOURCE_IDENTITIES:
        seed, step = item.SOURCE_IDENTITY_RULES[key]
        sequence, created = SourceIdentitySequence.objects.get_or_create(
            namespace=item._meta.label + '.' + key, defaults={'last_number': seed - step, 'creator': actor, 'modifier': actor})
        sequence = locked(sequence)
        if created:
            maximum = type(item).objects.aggregate(number=models.Max(key))['number']
            sequence.last_number = seed - step if maximum is None else max(maximum, seed - step)
        sequence.last_number += step
        persist(sequence, actor)
        setattr(item, key, sequence.last_number)
