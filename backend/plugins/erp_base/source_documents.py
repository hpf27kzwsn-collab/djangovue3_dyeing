"""旧业务原形记录的公共身份；具体字段在七模块静态声明。"""
from django.db import models
from core.models import CoreModel


class SourceRecord(CoreModel):
    description = None
    source_batch=models.ForeignKey('erp_base.LegacyImportBatch',verbose_name='来源批次',null=True,blank=True,on_delete=models.PROTECT)
    source_row=models.PositiveBigIntegerField('来源提取行号',null=True,blank=True)

    @property
    def entry_name(self):
        from .source_entry_services import entry_for
        return entry_for(self)

    @property
    def transfer_retained(self):
        from .source_context import SourceDocumentContext
        retained=SourceDocumentContext.objects.filter(entity=self._meta.label,object_id=self.pk,
            effects__transfer_retained__active=True).exists()
        return '已撤回留档' if retained else ''

    class Meta:
        abstract=True
        constraints=[models.UniqueConstraint(fields=['source_batch','source_row'],name='%(app_label)s_%(class)s_srcrow_uniq')]
