"""质量报告的原数量投影；不建立应收、付款或账务模型。"""
from django.db import models
from plugins.erp_base.models import ErpModel


class QualityQuantityBatch(ErpModel):
    sha256=models.CharField('来源文件SHA256',max_length=64,unique=True)
    database_name=models.CharField('原数据库',max_length=128)
    captured_at=models.DateTimeField('原数量抽取时间')
    row_count=models.PositiveIntegerField('原连接行数')
    length_available=models.BooleanField('原PreMeter字段存在')
    evidence=models.JSONField('原字段、查询及表头证据')

    class Meta:
        verbose_name=verbose_name_plural='质量数量来源批次'


class QualityQuantitySource(ErpModel):
    batch=models.ForeignKey(QualityQuantityBatch,on_delete=models.PROTECT,related_name='quantity_rows',verbose_name='数量来源批次')
    source_row=models.PositiveIntegerField('原连接行序号')
    detail_no=models.CharField('原FAR明细号',max_length=36,null=True,blank=True)
    detail_sheet_series=models.CharField('原明细表头流水',max_length=20,null=True,blank=True)
    header_sheet_series=models.CharField('原匹配表头流水',max_length=20,null=True,blank=True)
    sheet_date=models.DateTimeField('原表头日期',null=True,blank=True)
    sheet_kind=models.SmallIntegerField('原单据类型',null=True,blank=True)
    business_unit=models.CharField('原经营单位编码',max_length=10,null=True,blank=True)
    job_number=models.CharField('原工卡号',max_length=50,null=True,blank=True)
    out_detail_no=models.CharField('原出库明细号',max_length=20,null=True,blank=True)
    quantity=models.DecimalField('原Qty',max_digits=10,decimal_places=2,null=True,blank=True)
    stock_unit=models.SmallIntegerField('原StockUnit',null=True,blank=True)
    zero_amount=models.BooleanField('原ARMoney是否为零',null=True,blank=True)
    metres=models.DecimalField('有原字段依据的PreMeter',max_digits=24,decimal_places=6,null=True,blank=True)

    class Meta:
        verbose_name=verbose_name_plural='质量报告原数量'
        constraints=[models.UniqueConstraint(fields=['batch','source_row'],name='quality_quantity_batch_row')]
        indexes=[models.Index(fields=['batch','sheet_date'],name='quality_quantity_period')]
