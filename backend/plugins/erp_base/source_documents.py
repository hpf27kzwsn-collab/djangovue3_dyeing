"""旧业务原形记录的公共身份；具体字段在七模块静态声明。"""
from django.db import models
from .models import ErpModel


class SourceRecord(ErpModel):
    source_batch=models.ForeignKey('erp_base.LegacyImportBatch',verbose_name='来源批次',null=True,blank=True,on_delete=models.PROTECT)
    source_row=models.PositiveBigIntegerField('来源提取行号',null=True,blank=True)
    approval_stage=models.CharField('办理阶段',max_length=16,null=True,blank=True,choices=[('draft','草稿'),('confirmed','已确认'),('approved','已审核')])
    confirmed_at=models.DateTimeField('确认时间',null=True,blank=True)
    confirmed_by=models.ForeignKey('system.Users',verbose_name='确认人',null=True,blank=True,on_delete=models.PROTECT,related_name='%(app_label)s_%(class)s_confirmed')
    approved_at=models.DateTimeField('审核时间',null=True,blank=True)
    approved_by=models.ForeignKey('system.Users',verbose_name='审核人',null=True,blank=True,on_delete=models.PROTECT,related_name='%(app_label)s_%(class)s_approved')

    @property
    def entry_name(self):
        from .source_entry_services import entry_for
        return entry_for(self)

    class Meta:
        abstract=True
        constraints=[models.UniqueConstraint(fields=['source_batch','source_row'],name='%(app_label)s_%(class)s_srcrow_uniq')]
