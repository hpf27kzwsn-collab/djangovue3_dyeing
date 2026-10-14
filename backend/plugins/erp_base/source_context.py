"""新办理明确采用的旧入口；历史未知入口保持未知。"""
from django.db import models
from .models import ErpModel


class SourceDocumentContext(ErpModel):
    entity = models.CharField('业务模型', max_length=100)
    object_id = models.BigIntegerField('业务记录ID')
    entry_name = models.CharField('原业务入口', max_length=100)
    effects = models.JSONField('业务生成及回写对应', default=dict, blank=True)

    class Meta:
        db_table = 'erp_base_sourcedocumentcontext'
        verbose_name = verbose_name_plural = '单据办理入口'
        constraints = [models.UniqueConstraint(fields=['entity', 'object_id'], name='erp_source_document_context_uniq')]


class SourceBusinessParameter(ErpModel):
    name = models.CharField('原业务参数名称', max_length=100, unique=True)
    value = models.TextField('原业务参数值', null=True, blank=True)
    captured_at = models.DateTimeField('原参数核对时间', null=True, blank=True)

    class Meta:
        db_table = 'erp_base_sourcebusinessparameter'
        verbose_name = verbose_name_plural = '原业务参数'
