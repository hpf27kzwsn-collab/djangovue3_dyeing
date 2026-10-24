"""客户本地文件导入批次；保留文件定位，不连接旧数据库。"""
from django.db import models
from .models import ErpModel


class LegacyImportBatch(ErpModel):
    number=models.CharField('资料批次号',max_length=80,unique=True)
    started_at=models.DateTimeField('导入开始')
    finished_at=models.DateTimeField('导入结束')
    manifest_sha256=models.CharField('资料文件摘要',max_length=64)
    source_directory=models.TextField('上传文件名称')
    row_count=models.BigIntegerField('完整来源行数')
    byte_count=models.BigIntegerField('来源文件字节数')
    note=models.TextField('资料说明')

    class Meta:
        db_table='erp_base_legacyimportbatch'
        verbose_name=verbose_name_plural='资料导入批次'
