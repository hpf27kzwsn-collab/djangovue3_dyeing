from django.db import models
from .models import ErpModel


class NumberingRule(ErpModel):
    name = models.CharField('规则名称', max_length=100)
    target_model = models.CharField('业务模型', max_length=100)
    target_field = models.CharField('编号字段', max_length=100)
    scope_key = models.CharField('适用类别', max_length=200)
    scope_filters = models.JSONField('类别条件', default=dict, blank=True)
    entry_name = models.CharField('业务入口', max_length=100, blank=True)
    prefix = models.CharField('固定前缀', max_length=64, blank=True)
    digits = models.PositiveSmallIntegerField('流水位数', default=3)
    start_number = models.PositiveBigIntegerField('起始流水', default=1)
    last_number = models.PositiveBigIntegerField('已用流水上限', null=True, blank=True)
    auto_enabled = models.BooleanField('自动编号', default=True)
    allow_manual_input = models.BooleanField('允许手工录入', default=True)
    allow_code_change = models.BooleanField('允许更改编号', default=False)
    notes = models.TextField('规则说明', blank=True)

    class Meta:
        db_table = 'erp_base_numberingrule'
        verbose_name = verbose_name_plural = '编号管理'
        ordering = ['id']
        constraints = [models.UniqueConstraint(fields=['target_model', 'target_field', 'scope_key'], name='erp_numbering_scope_unique')]
