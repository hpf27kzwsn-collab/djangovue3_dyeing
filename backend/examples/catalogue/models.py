from django.db import models
from core.models import CoreModel, SoftDeleteModel, SoftDeleteManager


class Entry(CoreModel):
    code = models.CharField('编码', primary_key=True, max_length=32)
    name = models.CharField('名称', max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField('金额', max_digits=16, decimal_places=2, default=0)
    date = models.DateField('日期', null=True, blank=True)
    detail = models.JSONField('明细', default=dict, blank=True)

    class Meta:
        verbose_name = '模型接入示例'
        ordering = ['code']


class Note(CoreModel, SoftDeleteModel):
    objects = SoftDeleteManager()
    name = models.CharField(max_length=100)


class NoteLine(CoreModel, SoftDeleteModel):
    objects = SoftDeleteManager()
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
