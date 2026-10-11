"""完整旧业务来源与明确导入对照；归档不产生新库存或生产事实。"""
from django.db import models
from .models import ErpModel


class LegacyImportBatch(ErpModel):
    number=models.CharField('资料批次号',max_length=80,unique=True)
    database_name=models.CharField('旧数据库',max_length=128)
    started_at=models.DateTimeField('提取开始')
    finished_at=models.DateTimeField('提取结束')
    manifest_sha256=models.CharField('资料清单摘要',max_length=64,unique=True)
    source_directory=models.TextField('本地资料目录')
    table_count=models.PositiveIntegerField('来源表数')
    row_count=models.BigIntegerField('完整来源行数')
    byte_count=models.BigIntegerField('来源文件字节数')
    verified_at=models.DateTimeField('文件核对时间')
    note=models.TextField('资料说明')

    class Meta:
        db_table='erp_base_legacyimportbatch'
        verbose_name=verbose_name_plural='旧资料提取批次'


class LegacySourceTable(ErpModel):
    batch=models.ForeignKey(LegacyImportBatch,verbose_name='提取批次',on_delete=models.PROTECT,related_name='source_tables')
    schema_name=models.CharField('旧库架构',max_length=128)
    table_name=models.CharField('旧来源表',max_length=128)
    modules=models.JSONField('所属六模块')
    columns=models.JSONField('当前物理字段及精度')
    primary_key=models.JSONField('原主键列',blank=True)
    row_count=models.BigIntegerField('完整来源行数')
    byte_count=models.BigIntegerField('来源字节数')
    sha256=models.CharField('来源文件摘要',max_length=64)
    file_path=models.TextField('本地来源文件')

    class Meta:
        db_table='erp_base_legacysourcetable'
        verbose_name=verbose_name_plural='旧业务来源表'
        constraints=[models.UniqueConstraint(fields=['batch','schema_name','table_name'],name='erp_legacy_source_table_uniq')]


class LegacyObjectMap(ErpModel):
    source_table=models.ForeignKey(LegacySourceTable,verbose_name='完整旧来源',on_delete=models.PROTECT,related_name='object_maps')
    row_number=models.PositiveBigIntegerField('来源提取行号')
    source_key=models.JSONField('完整原主键',null=True,blank=True)
    target_model=models.CharField('对应新模型',max_length=100)
    target_id=models.BigIntegerField('新记录id')
    mapped_fields=models.JSONField('逐字段明确采用关系')

    class Meta:
        db_table='erp_base_legacyobjectmap'
        verbose_name=verbose_name_plural='旧新记录逐项对照'
        constraints=[models.UniqueConstraint(fields=['source_table','row_number','target_model'],name='erp_legacy_object_map_uniq')]


class LegacyImportIssue(ErpModel):
    batch=models.ForeignKey(LegacyImportBatch,verbose_name='资料批次',on_delete=models.PROTECT,related_name='import_issues')
    source_table=models.ForeignKey(LegacySourceTable,verbose_name='旧来源表',on_delete=models.PROTECT,null=True,blank=True)
    row_number=models.PositiveBigIntegerField('来源提取行号',null=True,blank=True)
    source_key=models.JSONField('原主键',null=True,blank=True)
    target_model=models.CharField('待处理新模型',max_length=100,blank=True)
    field_name=models.CharField('待处理字段',max_length=128,blank=True)
    category=models.CharField('核对类别',max_length=40)
    source_value=models.JSONField('原值',null=True,blank=True)
    detail=models.TextField('待处理原因')
    handling=models.TextField('明确处理记录',blank=True)
    is_resolved=models.BooleanField('已完成核对',default=False)

    class Meta:
        db_table='erp_base_legacyimportissue'
        verbose_name=verbose_name_plural='旧数据待核实事项'
