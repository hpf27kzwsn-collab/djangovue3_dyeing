"""客户本地质量统计数量；数量集明确本次报告采用的口径。"""
from django.db import models
from plugins.erp_base.models import ErpModel


class QualityQuantityBatch(ErpModel):
    name=models.CharField('数量集名称',max_length=100,blank=True)

    class Meta:
        verbose_name=verbose_name_plural='质量统计数量集'


class QualityQuantitySource(ErpModel):
    batch=models.ForeignKey(QualityQuantityBatch,on_delete=models.PROTECT,related_name='quantity_rows',verbose_name='数量集')
    detail_no=models.CharField('来源明细号',max_length=36,null=True,blank=True)
    header_sheet_series=models.CharField('来源单号',max_length=20,null=True,blank=True)
    sheet_date=models.DateTimeField('单据日期',null=True,blank=True)
    sheet_kind=models.SmallIntegerField('业务类型编码',null=True,blank=True)
    business_unit=models.CharField('经营单位编码',max_length=10,null=True,blank=True)
    job_number=models.CharField('工卡号',max_length=50,null=True,blank=True)
    out_detail_no=models.CharField('出库明细号',max_length=20,null=True,blank=True)
    quantity=models.DecimalField('数量',max_digits=10,decimal_places=2,null=True,blank=True)
    stock_unit=models.SmallIntegerField('计量单位编码',null=True,blank=True)
    zero_amount=models.BooleanField('是否零价业务',null=True,blank=True)
    metres=models.DecimalField('长度',max_digits=24,decimal_places=6,null=True,blank=True)

    class Meta:
        verbose_name=verbose_name_plural='质量统计数量'
        indexes=[models.Index(fields=['batch','sheet_date'],name='quality_quantity_period')]
