"""静态旧业务字段；由tools/legacy_models生成，逐表来源见source_catalog.json。"""
from django.db import models
from plugins.erp_base.source_documents import SourceRecord


class SourceDboAA(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='AA'
    SOURCE_FIELDS={'库存位置': 'old_库存位置', '重量': 'old_重量', '类别': 'old_类别', '规格': 'old_规格', '供应商': 'old_供应商', '批号/等级': 'old_批号_等级', '剩余库存': 'old_剩余库存', '类别1': 'old_类别1'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_库存位置=models.CharField('库存位置', null=True, blank=True, max_length=255)
    old_重量=models.FloatField('重量', null=True, blank=True)
    old_类别=models.CharField('类别', null=True, blank=True, max_length=255)
    old_规格=models.CharField('规格', null=True, blank=True, max_length=255)
    old_供应商=models.CharField('供应商', null=True, blank=True, max_length=255)
    old_批号_等级=models.CharField('批号/等级', null=True, blank=True, max_length=255)
    old_剩余库存=models.FloatField('剩余库存', null=True, blank=True)
    old_类别1=models.CharField('类别1', null=True, blank=True, max_length=255)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_aa'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（AA，待确认）'
        ordering=["-id"]

class SourceDboAAA(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='AAA'
    SOURCE_FIELDS={'编号': 'old_编号', '名称': 'old_名称', '供应商': 'old_供应商', '单价': 'old_单价', '数量': 'old_数量', '金额': 'old_金额'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_编号=models.CharField('编号', null=True, blank=True, max_length=255)
    old_名称=models.CharField('名称', null=True, blank=True, max_length=255)
    old_供应商=models.CharField('供应商', null=True, blank=True, max_length=255)
    old_单价=models.FloatField('单价', null=True, blank=True)
    old_数量=models.FloatField('数量', null=True, blank=True)
    old_金额=models.FloatField('金额', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_aaa'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（AAA，待确认）'
        ordering=["-id"]

class SourceDboAAKC1(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='AAKC1'
    SOURCE_FIELDS={'入库类別': 'old_入库类別', '客户': 'old_客户', '本厂规格': 'old_本厂规格', '供应商': 'old_供应商', '批号': 'old_批号', '锭重': 'old_锭重', '粒数': 'old_粒数', '重量': 'old_重量', '实际重量': 'old_实际重量', '实际区域': 'old_实际区域', '半成品颜色': 'old_半成品颜色', '区域': 'old_区域', '半成品缸号': 'old_半成品缸号', '采购单号': 'old_采购单号', 'A_B': 'old_a_b', '件数': 'old_件数'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_入库类別=models.CharField('入库类別', null=True, blank=True, max_length=255)
    old_客户=models.CharField('客户', null=True, blank=True, max_length=255)
    old_本厂规格=models.CharField('本厂规格', null=True, blank=True, max_length=255)
    old_供应商=models.CharField('供应商', null=True, blank=True, max_length=255)
    old_批号=models.CharField('批号', null=True, blank=True, max_length=255)
    old_锭重=models.FloatField('锭重', null=True, blank=True)
    old_粒数=models.CharField('粒数', null=True, blank=True, max_length=255)
    old_重量=models.FloatField('重量', null=True, blank=True)
    old_实际重量=models.FloatField('实际重量', null=True, blank=True)
    old_实际区域=models.FloatField('实际区域', null=True, blank=True)
    old_半成品颜色=models.CharField('半成品颜色', null=True, blank=True, max_length=255)
    old_区域=models.CharField('区域', null=True, blank=True, max_length=255)
    old_半成品缸号=models.CharField('半成品缸号', null=True, blank=True, max_length=255)
    old_采购单号=models.CharField('采购单号', null=True, blank=True, max_length=255)
    old_a_b=models.CharField('A_B', null=True, blank=True, max_length=255)
    old_件数=models.CharField('件数', null=True, blank=True, max_length=255)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_aakc1'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（AAKC1，待确认）'
        ordering=["-id"]

class SourceDboABC(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='ABC'
    SOURCE_FIELDS={'库存位置': 'old_库存位置', '重量': 'old_重量', '类别': 'old_类别', '规格': 'old_规格', '供应商': 'old_供应商', '批号/等级': 'old_批号_等级', '8月结存': 'old_8月结存', '本月松筒进仓': 'old_本月松筒进仓', '剩余库存': 'old_剩余库存'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_库存位置=models.CharField('库存位置', null=True, blank=True, max_length=255)
    old_重量=models.FloatField('重量', null=True, blank=True)
    old_类别=models.CharField('类别', null=True, blank=True, max_length=255)
    old_规格=models.CharField('规格', null=True, blank=True, max_length=255)
    old_供应商=models.CharField('供应商', null=True, blank=True, max_length=255)
    old_批号_等级=models.CharField('批号/等级', null=True, blank=True, max_length=255)
    old_8月结存=models.FloatField('8月结存', null=True, blank=True)
    old_本月松筒进仓=models.FloatField('本月松筒进仓', null=True, blank=True)
    old_剩余库存=models.FloatField('剩余库存', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_abc'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（ABC，待确认）'
        ordering=["-id"]

class SourceDboADD(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='ADD'
    SOURCE_FIELDS={'入库类別': 'old_入库类別', '客户': 'old_客户', '本厂规格': 'old_本厂规格', '供应商': 'old_供应商', '批号': 'old_批号', '锭重': 'old_锭重', '粒数': 'old_粒数', '重量': 'old_重量', '实际重量': 'old_实际重量', '实际区域': 'old_实际区域', '半成品颜色': 'old_半成品颜色', '区域': 'old_区域', '半成品缸号': 'old_半成品缸号', '采购单号': 'old_采购单号', 'A_B': 'old_a_b', '件数': 'old_件数'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_入库类別=models.CharField('入库类別', null=True, blank=True, max_length=255)
    old_客户=models.CharField('客户', null=True, blank=True, max_length=255)
    old_本厂规格=models.CharField('本厂规格', null=True, blank=True, max_length=255)
    old_供应商=models.CharField('供应商', null=True, blank=True, max_length=255)
    old_批号=models.CharField('批号', null=True, blank=True, max_length=255)
    old_锭重=models.FloatField('锭重', null=True, blank=True)
    old_粒数=models.CharField('粒数', null=True, blank=True, max_length=255)
    old_重量=models.FloatField('重量', null=True, blank=True)
    old_实际重量=models.FloatField('实际重量', null=True, blank=True)
    old_实际区域=models.FloatField('实际区域', null=True, blank=True)
    old_半成品颜色=models.CharField('半成品颜色', null=True, blank=True, max_length=255)
    old_区域=models.CharField('区域', null=True, blank=True, max_length=255)
    old_半成品缸号=models.CharField('半成品缸号', null=True, blank=True, max_length=255)
    old_采购单号=models.CharField('采购单号', null=True, blank=True, max_length=255)
    old_a_b=models.CharField('A_B', null=True, blank=True, max_length=255)
    old_件数=models.CharField('件数', null=True, blank=True, max_length=255)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_add'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（ADD，待确认）'
        ordering=["-id"]

class SourceDboAEE(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='AEE'
    SOURCE_FIELDS={'编码': 'old_编码', '名称': 'old_名称', '产地': 'old_产地', '单价': 'old_单价', '数量': 'old_数量', '金额': 'old_金额', 'F7': 'old_f7', 'F8': 'old_f8', 'F9': 'old_f9', 'F10': 'old_f10', 'F11': 'old_f11', 'F12': 'old_f12', 'F13': 'old_f13', 'F14': 'old_f14', 'F15': 'old_f15', 'F16': 'old_f16', 'F17': 'old_f17', 'F18': 'old_f18', 'F19': 'old_f19', 'F20': 'old_f20'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_编码=models.CharField('编码', null=True, blank=True, max_length=255)
    old_名称=models.CharField('名称', null=True, blank=True, max_length=255)
    old_产地=models.CharField('产地', null=True, blank=True, max_length=255)
    old_单价=models.DecimalField('单价', null=True, blank=True, max_digits=19, decimal_places=4)
    old_数量=models.FloatField('数量', null=True, blank=True)
    old_金额=models.DecimalField('金额', null=True, blank=True, max_digits=19, decimal_places=4)
    old_f7=models.CharField('F7', null=True, blank=True, max_length=255)
    old_f8=models.CharField('F8', null=True, blank=True, max_length=255)
    old_f9=models.CharField('F9', null=True, blank=True, max_length=255)
    old_f10=models.CharField('F10', null=True, blank=True, max_length=255)
    old_f11=models.CharField('F11', null=True, blank=True, max_length=255)
    old_f12=models.CharField('F12', null=True, blank=True, max_length=255)
    old_f13=models.CharField('F13', null=True, blank=True, max_length=255)
    old_f14=models.CharField('F14', null=True, blank=True, max_length=255)
    old_f15=models.CharField('F15', null=True, blank=True, max_length=255)
    old_f16=models.CharField('F16', null=True, blank=True, max_length=255)
    old_f17=models.CharField('F17', null=True, blank=True, max_length=255)
    old_f18=models.CharField('F18', null=True, blank=True, max_length=255)
    old_f19=models.CharField('F19', null=True, blank=True, max_length=255)
    old_f20=models.CharField('F20', null=True, blank=True, max_length=255)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_aee'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（AEE，待确认）'
        ordering=["-id"]

class SourceDboC(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='C'
    SOURCE_FIELDS={'CODE': 'old_code', 'NAME': 'old_name'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_code=models.CharField('CODE', null=True, blank=True, max_length=50)
    old_name=models.CharField('NAME', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_c'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（C，待确认）'
        ordering=["-id"]

class SourceDboCbbz1109(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='cbbz1109'
    SOURCE_FIELDS={'kh': 'old_kh', 'bz': 'old_bz'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_kh=models.CharField('kh', null=True, blank=True, max_length=50)
    old_bz=models.CharField('bz', null=True, blank=True, max_length=250)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_cbbz1109'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（cbbz1109，待确认）'
        ordering=["-id"]

class SourceDboCkpd20221024(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='ckpd20221024'
    SOURCE_FIELDS={'kh': 'old_kh', 'qy': 'old_qy', 'kw': 'old_kw', 'card': 'old_card', 'ys': 'old_ys', 'rolls': 'old_rolls', 'bz': 'old_bz', 'bz1': 'old_bz1', 'bz2': 'old_bz2', 'bz3': 'old_bz3', 'bz4': 'old_bz4', 'sumrolls': 'old_sumrolls'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_kh=models.CharField('kh', null=True, blank=True, max_length=50)
    old_qy=models.CharField('qy', null=True, blank=True, max_length=50)
    old_kw=models.CharField('kw', null=True, blank=True, max_length=50)
    old_card=models.CharField('card', null=True, blank=True, max_length=50)
    old_ys=models.CharField('ys', null=True, blank=True, max_length=50)
    old_rolls=models.DecimalField('rolls', null=True, blank=True, max_digits=18, decimal_places=2)
    old_bz=models.CharField('bz', null=True, blank=True, max_length=150)
    old_bz1=models.CharField('bz1', null=True, blank=True, max_length=150)
    old_bz2=models.CharField('bz2', null=True, blank=True, max_length=150)
    old_bz3=models.CharField('bz3', null=True, blank=True, max_length=150)
    old_bz4=models.CharField('bz4', null=True, blank=True, max_length=150)
    old_sumrolls=models.DecimalField('sumrolls', null=True, blank=True, max_digits=18, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_ckpd20221024'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（ckpd20221024，待确认）'
        ordering=["-id"]

class SourceDboCkpd20221024bak(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='ckpd20221024bak'
    SOURCE_FIELDS={'kh': 'old_kh', 'qy': 'old_qy', 'kw': 'old_kw', 'card': 'old_card', 'ys': 'old_ys', 'rolls': 'old_rolls', 'bz': 'old_bz', 'bz1': 'old_bz1', 'bz2': 'old_bz2', 'bz3': 'old_bz3', 'bz4': 'old_bz4', 'sumrolls': 'old_sumrolls'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_kh=models.CharField('kh', null=True, blank=True, max_length=50)
    old_qy=models.CharField('qy', null=True, blank=True, max_length=50)
    old_kw=models.CharField('kw', null=True, blank=True, max_length=50)
    old_card=models.CharField('card', null=True, blank=True, max_length=50)
    old_ys=models.CharField('ys', null=True, blank=True, max_length=50)
    old_rolls=models.DecimalField('rolls', null=True, blank=True, max_digits=18, decimal_places=2)
    old_bz=models.CharField('bz', null=True, blank=True, max_length=150)
    old_bz1=models.CharField('bz1', null=True, blank=True, max_length=150)
    old_bz2=models.CharField('bz2', null=True, blank=True, max_length=150)
    old_bz3=models.CharField('bz3', null=True, blank=True, max_length=150)
    old_bz4=models.CharField('bz4', null=True, blank=True, max_length=150)
    old_sumrolls=models.DecimalField('sumrolls', null=True, blank=True, max_digits=18, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_ckpd20221024bak'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（ckpd20221024bak，待确认）'
        ordering=["-id"]

class SourceDboCkpd20221027(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='ckpd20221027'
    SOURCE_FIELDS={'kh': 'old_kh', 'qy': 'old_qy', 'kw': 'old_kw', 'card': 'old_card', 'ys': 'old_ys', 'rolls': 'old_rolls', 'bz': 'old_bz', 'bz1': 'old_bz1', '类型': 'old_类型'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_kh=models.CharField('kh', null=True, blank=True, max_length=50)
    old_qy=models.CharField('qy', null=True, blank=True, max_length=50)
    old_kw=models.CharField('kw', null=True, blank=True, max_length=50)
    old_card=models.CharField('card', null=True, blank=True, max_length=50)
    old_ys=models.CharField('ys', null=True, blank=True, max_length=50)
    old_rolls=models.DecimalField('rolls', null=True, blank=True, max_digits=18, decimal_places=2)
    old_bz=models.CharField('bz', null=True, blank=True, max_length=150)
    old_bz1=models.CharField('bz1', null=True, blank=True, max_length=150)
    old_类型=models.CharField('类型', null=True, blank=True, max_length=150)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_ckpd20221027'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（ckpd20221027，待确认）'
        ordering=["-id"]

class SourceDboCksgz20221024(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='cksgz20221024'
    SOURCE_FIELDS={'xh': 'old_xh', 'rkrq': 'old_rkrq', 'kh': 'old_kh', 'card': 'old_card', 'cp': 'old_cp', 'ys': 'old_ys', 'sh': 'old_sh', 'qy': 'old_qy', 'kw': 'old_kw', 'rolls': 'old_rolls', 'pz': 'old_pz', 'cz': 'old_cz', 'pdrolls': 'old_pdrolls', 'bz': 'old_bz', 'bz1': 'old_bz1', 'bz2': 'old_bz2', 'bz33': 'old_bz33'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_xh=models.CharField('xh', null=True, blank=True, max_length=50)
    old_rkrq=models.DateField('rkrq', null=True, blank=True)
    old_kh=models.CharField('kh', null=True, blank=True, max_length=50)
    old_card=models.CharField('card', null=True, blank=True, max_length=50)
    old_cp=models.CharField('cp', null=True, blank=True, max_length=150)
    old_ys=models.CharField('ys', null=True, blank=True, max_length=50)
    old_sh=models.CharField('sh', null=True, blank=True, max_length=50)
    old_qy=models.CharField('qy', null=True, blank=True, max_length=50)
    old_kw=models.CharField('kw', null=True, blank=True, max_length=50)
    old_rolls=models.DecimalField('rolls', null=True, blank=True, max_digits=18, decimal_places=2)
    old_pz=models.DecimalField('pz', null=True, blank=True, max_digits=18, decimal_places=2)
    old_cz=models.DecimalField('cz', null=True, blank=True, max_digits=18, decimal_places=2)
    old_pdrolls=models.DecimalField('pdrolls', null=True, blank=True, max_digits=18, decimal_places=2)
    old_bz=models.CharField('bz', null=True, blank=True, max_length=250)
    old_bz1=models.CharField('bz1', null=True, blank=True, max_length=250)
    old_bz2=models.CharField('bz2', null=True, blank=True, max_length=250)
    old_bz33=models.CharField('bz33', null=True, blank=True, max_length=250)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_cksgz20221024'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（cksgz20221024，待确认）'
        ordering=["-id"]

class SourceDboCpdqkc20221024(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='cpdqkc20221024'
    SOURCE_FIELDS={'xh': 'old_xh', 'rkrq': 'old_rkrq', 'kh': 'old_kh', 'card': 'old_card', 'pb': 'old_pb', 'cp': 'old_cp', 'sh': 'old_sh', 'ksh': 'old_ksh', 'ys': 'old_ys', 'rolls': 'old_rolls', 'pz': 'old_pz', 'cz': 'old_cz', 'bz': 'old_bz', 'bz1': 'old_bz1', 'bz2': 'old_bz2'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_xh=models.CharField('xh', null=True, blank=True, max_length=50)
    old_rkrq=models.DateField('rkrq', null=True, blank=True)
    old_kh=models.CharField('kh', null=True, blank=True, max_length=50)
    old_card=models.CharField('card', null=True, blank=True, max_length=50)
    old_pb=models.CharField('pb', null=True, blank=True, max_length=150)
    old_cp=models.CharField('cp', null=True, blank=True, max_length=150)
    old_sh=models.CharField('sh', null=True, blank=True, max_length=50)
    old_ksh=models.CharField('ksh', null=True, blank=True, max_length=50)
    old_ys=models.CharField('ys', null=True, blank=True, max_length=50)
    old_rolls=models.DecimalField('rolls', null=True, blank=True, max_digits=18, decimal_places=2)
    old_pz=models.DecimalField('pz', null=True, blank=True, max_digits=18, decimal_places=2)
    old_cz=models.DecimalField('cz', null=True, blank=True, max_digits=18, decimal_places=2)
    old_bz=models.CharField('bz', null=True, blank=True, max_length=150)
    old_bz1=models.CharField('bz1', null=True, blank=True, max_length=150)
    old_bz2=models.CharField('bz2', null=True, blank=True, max_length=150)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_cpdqkc20221024'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（cpdqkc20221024，待确认）'
        ordering=["-id"]

class SourceDboDXCHANLIANG(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='DXCHANLIANG'
    SOURCE_FIELDS={'日期': 'old_日期', '机台': 'old_机台', '数量': 'old_数量', '工序': 'old_工序'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_日期=models.CharField('日期', null=True, blank=True, max_length=50)
    old_机台=models.CharField('机台', null=True, blank=True, max_length=50)
    old_数量=models.DecimalField('数量', null=True, blank=True, max_digits=9, decimal_places=2)
    old_工序=models.CharField('工序', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_dxchanliang'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（DXCHANLIANG，待确认）'
        ordering=["-id"]

class SourceDboHypf(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='hypf'
    SOURCE_FIELDS={'RQ': 'old_rq', 'G_SH': 'old_g_sh', 'D_YS': 'old_d_ys', 'G_PFH': 'old_g_pfh', 'G_GXH': 'old_g_gxh', 'G_PH': 'old_g_ph', 'YL': 'old_yl', 'CZY': 'old_czy', 'BZ': 'old_bz', 'G_ID': 'old_g_id', 'G_UP': 'old_g_up', 'G_UPID': 'old_g_upid', 'G_ROW': 'old_g_row'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_rq=models.DateTimeField('RQ', null=True, blank=True)
    old_g_sh=models.CharField('G_SH', null=True, blank=True, max_length=255)
    old_d_ys=models.CharField('D_YS', null=True, blank=True, max_length=255)
    old_g_pfh=models.CharField('G_PFH', null=True, blank=True, max_length=255)
    old_g_gxh=models.CharField('G_GXH', null=True, blank=True, max_length=255)
    old_g_ph=models.CharField('G_PH', null=True, blank=True, max_length=255)
    old_yl=models.FloatField('YL', null=True, blank=True)
    old_czy=models.CharField('CZY', null=True, blank=True, max_length=255)
    old_bz=models.CharField('BZ', null=True, blank=True, max_length=255)
    old_g_id=models.CharField('G_ID', null=True, blank=True, max_length=255)
    old_g_up=models.BooleanField('G_UP', null=False, blank=False)
    old_g_upid=models.FloatField('G_UPID', null=True, blank=True)
    old_g_row=models.FloatField('G_ROW', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_hypf'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（hypf，待确认）'
        ordering=["-id"]

class SourceDboItbak20221120(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='itbak20221120'
    SOURCE_FIELDS={'ID': 'old_id', 'FENCHANG': 'old_fenchang', 'BUMEN': 'old_bumen', 'NAME': 'old_name', 'LEIXING': 'old_leixing', 'CPU': 'old_cpu', 'NEICUN': 'old_neicun', 'YINGPAN': 'old_yingpan', 'MACADDRESS': 'old_macaddress', 'USER': 'old_user', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'IsStop': 'old_is_stop', 'StopDate': 'old_stop_date', 'BZ': 'old_bz', 'sjbm': 'old_sjbm'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.IntegerField('ID', null=False, blank=False)
    old_fenchang=models.CharField('FENCHANG', null=True, blank=True, max_length=50)
    old_bumen=models.CharField('BUMEN', null=True, blank=True, max_length=50)
    old_name=models.CharField('NAME', null=True, blank=True, max_length=250)
    old_leixing=models.CharField('LEIXING', null=True, blank=True, max_length=250)
    old_cpu=models.CharField('CPU', null=True, blank=True, max_length=250)
    old_neicun=models.CharField('NEICUN', null=True, blank=True, max_length=250)
    old_yingpan=models.CharField('YINGPAN', null=True, blank=True, max_length=250)
    old_macaddress=models.CharField('MACADDRESS', null=True, blank=True, max_length=250)
    old_user=models.CharField('USER', null=True, blank=True, max_length=250)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=50)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=50)
    old_is_stop=models.BooleanField('IsStop', null=True, blank=True)
    old_stop_date=models.DateTimeField('StopDate', null=True, blank=True)
    old_bz=models.CharField('BZ', null=True, blank=True, max_length=500)
    old_sjbm=models.CharField('sjbm', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_itbak20221120'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（itbak20221120，待确认）'
        ordering=["-id"]

class SourceDboItbak20221121(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='itbak20221121'
    SOURCE_FIELDS={'ID': 'old_id', 'FENCHANG': 'old_fenchang', 'BUMEN': 'old_bumen', 'NAME': 'old_name', 'LEIXING': 'old_leixing', 'CPU': 'old_cpu', 'NEICUN': 'old_neicun', 'YINGPAN': 'old_yingpan', 'MACADDRESS': 'old_macaddress', 'USER': 'old_user', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'IsStop': 'old_is_stop', 'StopDate': 'old_stop_date', 'BZ': 'old_bz', 'sjbm': 'old_sjbm'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.IntegerField('ID', null=False, blank=False)
    old_fenchang=models.CharField('FENCHANG', null=True, blank=True, max_length=50)
    old_bumen=models.CharField('BUMEN', null=True, blank=True, max_length=50)
    old_name=models.CharField('NAME', null=True, blank=True, max_length=250)
    old_leixing=models.CharField('LEIXING', null=True, blank=True, max_length=250)
    old_cpu=models.CharField('CPU', null=True, blank=True, max_length=250)
    old_neicun=models.CharField('NEICUN', null=True, blank=True, max_length=250)
    old_yingpan=models.CharField('YINGPAN', null=True, blank=True, max_length=250)
    old_macaddress=models.CharField('MACADDRESS', null=True, blank=True, max_length=250)
    old_user=models.CharField('USER', null=True, blank=True, max_length=250)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=50)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=50)
    old_is_stop=models.BooleanField('IsStop', null=True, blank=True)
    old_stop_date=models.DateTimeField('StopDate', null=True, blank=True)
    old_bz=models.CharField('BZ', null=True, blank=True, max_length=500)
    old_sjbm=models.CharField('sjbm', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_itbak20221121'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（itbak20221121，待确认）'
        ordering=["-id"]

class SourceDboJxtbzyq(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='jxtbzyq'
    SOURCE_FIELDS={'kh': 'old_kh', 'ddh': 'old_ddh', 'bzyq': 'old_bzyq'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_kh=models.CharField('kh', null=True, blank=True, max_length=255)
    old_ddh=models.CharField('ddh', null=True, blank=True, max_length=255)
    old_bzyq=models.CharField('bzyq', null=True, blank=True, max_length=255)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_jxtbzyq'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（jxtbzyq，待确认）'
        ordering=["-id"]

class SourceDboJxtkckh(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='jxtkckh'
    SOURCE_FIELDS={'kh': 'old_kh'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_kh=models.CharField('kh', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_jxtkckh'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（jxtkckh，待确认）'
        ordering=["-id"]

class SourceDboNHTJ(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='NHTJ'
    SOURCE_FIELDS={'日期': 'old_日期', '序号': 'old_序号', '类别': 'old_类别', '机台编号': 'old_机台编号', '编号': 'old_编号', '部门': 'old_部门', '区域位置': 'old_区域位置', '使用说明': 'old_使用说明', '开始': 'old_开始', '中间': 'old_中间', '结束': 'old_结束', '早班能耗': 'old_早班能耗', '晚班能耗': 'old_晚班能耗', '当天能耗': 'old_当天能耗', '系统开始': 'old_系统开始', '系统中间': 'old_系统中间', '系统结束': 'old_系统结束', '系统早班能耗': 'old_系统早班能耗', '系统晚班能耗': 'old_系统晚班能耗', '系统当天能耗': 'old_系统当天能耗', '早班差异': 'old_早班差异', '晚班差异': 'old_晚班差异', '当天能耗差异': 'old_当天能耗差异', '当天读数差异': 'old_当天读数差异'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_日期=models.CharField('日期', null=True, blank=True, max_length=50)
    old_序号=models.CharField('序号', null=True, blank=True, max_length=10)
    old_类别=models.CharField('类别', null=True, blank=True, max_length=50)
    old_机台编号=models.CharField('机台编号', null=True, blank=True, max_length=50)
    old_编号=models.CharField('编号', null=True, blank=True, max_length=10)
    old_部门=models.CharField('部门', null=True, blank=True, max_length=50)
    old_区域位置=models.CharField('区域位置', null=True, blank=True, max_length=50)
    old_使用说明=models.CharField('使用说明', null=True, blank=True, max_length=250)
    old_开始=models.DecimalField('开始', null=True, blank=True, max_digits=18, decimal_places=0)
    old_中间=models.DecimalField('中间', null=True, blank=True, max_digits=18, decimal_places=0)
    old_结束=models.DecimalField('结束', null=True, blank=True, max_digits=18, decimal_places=0)
    old_早班能耗=models.DecimalField('早班能耗', null=True, blank=True, max_digits=18, decimal_places=0)
    old_晚班能耗=models.DecimalField('晚班能耗', null=True, blank=True, max_digits=18, decimal_places=0)
    old_当天能耗=models.DecimalField('当天能耗', null=True, blank=True, max_digits=18, decimal_places=0)
    old_系统开始=models.DecimalField('系统开始', null=True, blank=True, max_digits=18, decimal_places=0)
    old_系统中间=models.DecimalField('系统中间', null=True, blank=True, max_digits=18, decimal_places=0)
    old_系统结束=models.DecimalField('系统结束', null=True, blank=True, max_digits=18, decimal_places=0)
    old_系统早班能耗=models.DecimalField('系统早班能耗', null=True, blank=True, max_digits=18, decimal_places=0)
    old_系统晚班能耗=models.DecimalField('系统晚班能耗', null=True, blank=True, max_digits=18, decimal_places=0)
    old_系统当天能耗=models.DecimalField('系统当天能耗', null=True, blank=True, max_digits=18, decimal_places=0)
    old_早班差异=models.DecimalField('早班差异', null=True, blank=True, max_digits=18, decimal_places=0)
    old_晚班差异=models.DecimalField('晚班差异', null=True, blank=True, max_digits=18, decimal_places=0)
    old_当天能耗差异=models.DecimalField('当天能耗差异', null=True, blank=True, max_digits=18, decimal_places=0)
    old_当天读数差异=models.DecimalField('当天读数差异', null=True, blank=True, max_digits=18, decimal_places=0)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_nhtj'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（NHTJ，待确认）'
        ordering=["-id"]

class SourceDboPbpd20230422(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='pbpd20230422'
    SOURCE_FIELDS={'客户': 'old_客户', '针厂': 'old_针厂', '布种': 'old_布种', '条数': 'old_条数', '备注': 'old_备注'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_客户=models.CharField('客户', null=True, blank=True, max_length=50)
    old_针厂=models.CharField('针厂', null=True, blank=True, max_length=50)
    old_布种=models.CharField('布种', null=True, blank=True, max_length=50)
    old_条数=models.DecimalField('条数', null=True, blank=True, max_digits=18, decimal_places=2)
    old_备注=models.CharField('备注', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_pbpd20230422'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（pbpd20230422，待确认）'
        ordering=["-id"]

class SourceDboPS20221218(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='PS20221218'
    SOURCE_FIELDS={'STUFFID': 'old_stuffid', 'AUTOSYSID': 'old_autosysid'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_stuffid=models.CharField('STUFFID', null=True, blank=True, max_length=50)
    old_autosysid=models.CharField('AUTOSYSID', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_ps20221218'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（PS20221218，待确认）'
        ordering=["-id"]

class SourceDboRansechugangtongji(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='ransechugangtongji'
    SOURCE_FIELDS={'MachName': 'old_mach_name', 'bb': 'old_bb', 'NameC': 'old_name_c', 'PM': 'old_pm', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'SheetNo': 'old_sheet_no', 'MachineID': 'old_machine_id', 'Rolls': 'old_rolls', 'WeightQty': 'old_weight_qty', 'Note1': 'old_note1', 'StartTime': 'old_start_time', 'EndTime': 'old_end_time', 'timecost': 'old_timecost', 'TLSJ': 'old_tlsj'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_mach_name=models.CharField('MachName', null=True, blank=True, max_length=50)
    old_bb=models.CharField('bb', null=True, blank=True, max_length=50)
    old_name_c=models.CharField('NameC', null=True, blank=True, max_length=50)
    old_pm=models.CharField('PM', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=50)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=50)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=150)
    old_machine_id=models.CharField('MachineID', null=True, blank=True, max_length=50)
    old_rolls=models.DecimalField('Rolls', null=True, blank=True, max_digits=18, decimal_places=2)
    old_weight_qty=models.DecimalField('WeightQty', null=True, blank=True, max_digits=18, decimal_places=2)
    old_note1=models.CharField('Note1', null=True, blank=True, max_length=50)
    old_start_time=models.DateTimeField('StartTime', null=True, blank=True)
    old_end_time=models.DateTimeField('EndTime', null=True, blank=True)
    old_timecost=models.CharField('timecost', null=True, blank=True, max_length=50)
    old_tlsj=models.CharField('TLSJ', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_ransechugangtongji'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（ransechugangtongji，待确认）'
        ordering=["-id"]

class SourceDboRansetongji(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='ransetongji'
    SOURCE_FIELDS={'客户': 'old_客户', '布种': 'old_布种', '机型': 'old_机型', '直通': 'old_直通', '缸号': 'old_缸号', '匹数': 'old_匹数', '重量': 'old_重量', '色号': 'old_色号', '颜色': 'old_颜色', '进缸时间': 'old_进缸时间', '出缸时间': 'old_出缸时间', '耗时': 'old_耗时', '停留时间': 'old_停留时间'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_客户=models.CharField('客户', null=True, blank=True, max_length=50)
    old_布种=models.CharField('布种', null=True, blank=True, max_length=250)
    old_机型=models.CharField('机型', null=True, blank=True, max_length=50)
    old_直通=models.CharField('直通', null=True, blank=True, max_length=50)
    old_缸号=models.CharField('缸号', null=True, blank=True, max_length=150)
    old_匹数=models.DecimalField('匹数', null=True, blank=True, max_digits=18, decimal_places=2)
    old_重量=models.DecimalField('重量', null=True, blank=True, max_digits=18, decimal_places=2)
    old_色号=models.CharField('色号', null=True, blank=True, max_length=50)
    old_颜色=models.CharField('颜色', null=True, blank=True, max_length=150)
    old_进缸时间=models.DateTimeField('进缸时间', null=True, blank=True)
    old_出缸时间=models.DateTimeField('出缸时间', null=True, blank=True)
    old_耗时=models.CharField('耗时', null=True, blank=True, max_length=150)
    old_停留时间=models.CharField('停留时间', null=True, blank=True, max_length=150)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_ransetongji'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（ransetongji，待确认）'
        ordering=["-id"]

class SourceDboRCDDZJB(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='RCDDZJB'
    SOURCE_FIELDS={'CustSelfNo': 'old_cust_self_no', 'ProdID': 'old_prod_id', 'CustFabricName': 'old_cust_fabric_name', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'CustColorNum': 'old_cust_color_num', 'Width': 'old_width', 'WidthUnit': 'old_width_unit', 'Weight': 'old_weight', 'WeightKindID': 'old_weight_kind_id', 'OrderRolls': 'old_order_rolls', 'TubeWeight': 'old_tube_weight', 'AddWeigth': 'old_add_weigth', 'DlvDate': 'old_dlv_date'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_cust_self_no=models.CharField('CustSelfNo', null=True, blank=True, max_length=500)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=20)
    old_cust_fabric_name=models.CharField('CustFabricName', null=True, blank=True, max_length=250)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=150)
    old_cust_color_num=models.CharField('CustColorNum', null=True, blank=True, max_length=20)
    old_width=models.CharField('Width', null=True, blank=True, max_length=200)
    old_width_unit=models.CharField('WidthUnit', null=True, blank=True, max_length=20)
    old_weight=models.CharField('Weight', null=True, blank=True, max_length=200)
    old_weight_kind_id=models.CharField('WeightKindID', null=True, blank=True, max_length=20)
    old_order_rolls=models.DecimalField('OrderRolls', null=True, blank=True, max_digits=10, decimal_places=2)
    old_tube_weight=models.FloatField('TubeWeight', null=True, blank=True)
    old_add_weigth=models.FloatField('AddWeigth', null=True, blank=True)
    old_dlv_date=models.DateTimeField('DlvDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_rcddzjb'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（RCDDZJB，待确认）'
        ordering=["-id"]

class SourceDboShda(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='shda'
    SOURCE_FIELDS={'RQ': 'old_rq', 'SJ': 'old_sj', 'G_SH': 'old_g_sh', 'D_YS': 'old_d_ys', 'G_PFH': 'old_g_pfh', 'G_LBH': 'old_g_lbh', 'D_YSLB': 'old_d_yslb', 'G_KHSH': 'old_g_khsh', 'G_KH': 'old_g_kh', 'G_PH': 'old_g_ph', 'D_PM': 'old_d_pm', 'D_PBLB': 'old_d_pblb', 'PBKZ': 'old_pbkz', 'TSLJJ': 'old_tsljj', 'D_RLLB': 'old_d_rllb', 'LD': 'old_ld', 'SC': 'old_sc', 'HB': 'old_hb', 'DSGY': 'old_dsgy', 'G_JY': 'old_g_jy', 'F_YB': 'old_f_yb', 'G_GYH': 'old_g_gyh', 'F_GY': 'old_f_gy', 'F_LCMC': 'old_f_lcmc', 'F_DY': 'old_f_dy', 'F_KLD': 'old_f_kld', 'F_DABH': 'old_f_dabh', 'DYY': 'old_dyy', 'CZY': 'old_czy', 'BZ': 'old_bz', 'G_ID': 'old_g_id', 'G_UP': 'old_g_up', 'G_UPID': 'old_g_upid', 'G_ROW': 'old_g_row'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_rq=models.DateTimeField('RQ', null=True, blank=True)
    old_sj=models.CharField('SJ', null=True, blank=True, max_length=255)
    old_g_sh=models.CharField('G_SH', null=True, blank=True, max_length=255)
    old_d_ys=models.CharField('D_YS', null=True, blank=True, max_length=255)
    old_g_pfh=models.CharField('G_PFH', null=True, blank=True, max_length=255)
    old_g_lbh=models.CharField('G_LBH', null=True, blank=True, max_length=255)
    old_d_yslb=models.CharField('D_YSLB', null=True, blank=True, max_length=255)
    old_g_khsh=models.CharField('G_KHSH', null=True, blank=True, max_length=255)
    old_g_kh=models.CharField('G_KH', null=True, blank=True, max_length=255)
    old_g_ph=models.CharField('G_PH', null=True, blank=True, max_length=255)
    old_d_pm=models.CharField('D_PM', null=True, blank=True, max_length=255)
    old_d_pblb=models.CharField('D_PBLB', null=True, blank=True, max_length=255)
    old_pbkz=models.CharField('PBKZ', null=True, blank=True, max_length=255)
    old_tsljj=models.CharField('TSLJJ', null=True, blank=True, max_length=255)
    old_d_rllb=models.CharField('D_RLLB', null=True, blank=True, max_length=255)
    old_ld=models.CharField('LD', null=True, blank=True, max_length=255)
    old_sc=models.CharField('SC', null=True, blank=True, max_length=255)
    old_hb=models.CharField('HB', null=True, blank=True, max_length=255)
    old_dsgy=models.CharField('DSGY', null=True, blank=True, max_length=255)
    old_g_jy=models.FloatField('G_JY', null=True, blank=True)
    old_f_yb=models.FloatField('F_YB', null=True, blank=True)
    old_g_gyh=models.CharField('G_GYH', null=True, blank=True, max_length=255)
    old_f_gy=models.CharField('F_GY', null=True, blank=True, max_length=255)
    old_f_lcmc=models.CharField('F_LCMC', null=True, blank=True, max_length=255)
    old_f_dy=models.CharField('F_DY', null=True, blank=True, max_length=255)
    old_f_kld=models.CharField('F_KLD', null=True, blank=True, max_length=255)
    old_f_dabh=models.CharField('F_DABH', null=True, blank=True, max_length=255)
    old_dyy=models.CharField('DYY', null=True, blank=True, max_length=255)
    old_czy=models.CharField('CZY', null=True, blank=True, max_length=255)
    old_bz=models.CharField('BZ', null=True, blank=True, max_length=255)
    old_g_id=models.CharField('G_ID', null=True, blank=True, max_length=255)
    old_g_up=models.BooleanField('G_UP', null=False, blank=False)
    old_g_upid=models.CharField('G_UPID', null=True, blank=True, max_length=255)
    old_g_row=models.FloatField('G_ROW', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_shda'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（shda，待确认）'
        ordering=["-id"]

class SourceDboSHIFT(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='SHIFT'
    SOURCE_FIELDS={'SHIFTID': 'old_shiftid', 'NAME': 'old_name', 'USHIFTID': 'old_ushiftid', 'STARTDATE': 'old_startdate', 'ENDDATE': 'old_enddate', 'RUNNUM': 'old_runnum', 'SCH1': 'old_sch1', 'SCH2': 'old_sch2', 'SCH3': 'old_sch3', 'SCH4': 'old_sch4', 'SCH5': 'old_sch5', 'SCH6': 'old_sch6', 'SCH7': 'old_sch7', 'SCH8': 'old_sch8', 'SCH9': 'old_sch9', 'SCH10': 'old_sch10', 'SCH11': 'old_sch11', 'SCH12': 'old_sch12', 'CYCLE': 'old_cycle', 'UNITS': 'old_units'}
    SOURCE_KEY=('SHIFTID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_ushiftid': ('literal', -1), 'old_startdate': ('literal', '1900-1-1'), 'old_enddate': ('literal', '1900-12-31'), 'old_runnum': ('literal', 0), 'old_sch1': ('literal', 0), 'old_sch2': ('literal', 0), 'old_sch3': ('literal', 0), 'old_sch4': ('literal', 0), 'old_sch5': ('literal', 0), 'old_sch6': ('literal', 0), 'old_sch7': ('literal', 0), 'old_sch8': ('literal', 0), 'old_sch9': ('literal', 0), 'old_sch10': ('literal', 0), 'old_sch11': ('literal', 0), 'old_sch12': ('literal', 0), 'old_cycle': ('literal', 0), 'old_units': ('literal', 0)}
    SOURCE_IDENTITIES=('old_shiftid',)
    old_shiftid=models.IntegerField('SHIFTID', null=False, blank=False)
    old_name=models.CharField('NAME', null=True, blank=True, max_length=20)
    old_ushiftid=models.IntegerField('USHIFTID', null=True, blank=True)
    old_startdate=models.DateTimeField('STARTDATE', null=False, blank=False)
    old_enddate=models.DateTimeField('ENDDATE', null=True, blank=True)
    old_runnum=models.IntegerField('RUNNUM', null=True, blank=True)
    old_sch1=models.IntegerField('SCH1', null=True, blank=True)
    old_sch2=models.IntegerField('SCH2', null=True, blank=True)
    old_sch3=models.IntegerField('SCH3', null=True, blank=True)
    old_sch4=models.IntegerField('SCH4', null=True, blank=True)
    old_sch5=models.IntegerField('SCH5', null=True, blank=True)
    old_sch6=models.IntegerField('SCH6', null=True, blank=True)
    old_sch7=models.IntegerField('SCH7', null=True, blank=True)
    old_sch8=models.IntegerField('SCH8', null=True, blank=True)
    old_sch9=models.IntegerField('SCH9', null=True, blank=True)
    old_sch10=models.IntegerField('SCH10', null=True, blank=True)
    old_sch11=models.IntegerField('SCH11', null=True, blank=True)
    old_sch12=models.IntegerField('SCH12', null=True, blank=True)
    old_cycle=models.IntegerField('CYCLE', null=True, blank=True)
    old_units=models.IntegerField('UNITS', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_shift'
        indexes=[models.Index(fields=['source_batch', 'old_shiftid'],name='src_645c3bd2d222ebf7')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（SHIFT，待确认）'
        ordering=["-id"]

class SourceDboSHLEIXING(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='SHLEIXING'
    SOURCE_FIELDS={'CODE': 'old_code', 'lx': 'old_lx', 'LXNAME': 'old_lxname'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_code=models.CharField('CODE', null=True, blank=True, max_length=20)
    old_lx=models.CharField('lx', null=True, blank=True, max_length=20)
    old_lxname=models.CharField('LXNAME', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_shleixing'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（SHLEIXING，待确认）'
        ordering=["-id"]

class SourceDboTmp20221104(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='tmp20221104'
    SOURCE_FIELDS={'JobSheetNo': 'old_job_sheet_no'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_tmp20221104'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（tmp20221104，待确认）'
        ordering=["-id"]

class SourceDboXxtcbkc20221023(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='xxtcbkc20221023'
    SOURCE_FIELDS={'kh': 'old_kh', 'qy': 'old_qy', 'kw': 'old_kw', 'card': 'old_card', 'ys': 'old_ys', 'ps': 'old_ps', 'bz1': 'old_bz1', 'bz2': 'old_bz2', 'bj': 'old_bj'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_kh=models.CharField('kh', null=True, blank=True, max_length=50)
    old_qy=models.CharField('qy', null=True, blank=True, max_length=50)
    old_kw=models.CharField('kw', null=True, blank=True, max_length=50)
    old_card=models.CharField('card', null=True, blank=True, max_length=50)
    old_ys=models.CharField('ys', null=True, blank=True, max_length=50)
    old_ps=models.DecimalField('ps', null=True, blank=True, max_digits=18, decimal_places=2)
    old_bz1=models.CharField('bz1', null=True, blank=True, max_length=250)
    old_bz2=models.CharField('bz2', null=True, blank=True, max_length=250)
    old_bj=models.CharField('bj', null=True, blank=True, max_length=250)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_xxtcbkc20221023'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（xxtcbkc20221023，待确认）'
        ordering=["-id"]

class SourceDboXxtzzp20221024(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='xxtzzp20221024'
    SOURCE_FIELDS={'KH': 'old_kh', 'CARD': 'old_card', 'OLDCARD': 'old_oldcard', 'PB': 'old_pb', 'CP': 'old_cp', 'SH': 'old_sh', 'YS': 'old_ys', 'PS': 'old_ps', 'PBSL': 'old_pbsl', 'JINDU': 'old_jindu', 'PT': 'old_pt', 'BZ1': 'old_bz1', 'BZ2': 'old_bz2', 'BZ3': 'old_bz3'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_kh=models.CharField('KH', null=True, blank=True, max_length=50)
    old_card=models.CharField('CARD', null=True, blank=True, max_length=50)
    old_oldcard=models.CharField('OLDCARD', null=True, blank=True, max_length=50)
    old_pb=models.CharField('PB', null=True, blank=True, max_length=150)
    old_cp=models.CharField('CP', null=True, blank=True, max_length=150)
    old_sh=models.CharField('SH', null=True, blank=True, max_length=50)
    old_ys=models.CharField('YS', null=True, blank=True, max_length=50)
    old_ps=models.DecimalField('PS', null=True, blank=True, max_digits=18, decimal_places=2)
    old_pbsl=models.DecimalField('PBSL', null=True, blank=True, max_digits=18, decimal_places=2)
    old_jindu=models.CharField('JINDU', null=True, blank=True, max_length=150)
    old_pt=models.DateTimeField('PT', null=True, blank=True)
    old_bz1=models.CharField('BZ1', null=True, blank=True, max_length=150)
    old_bz2=models.CharField('BZ2', null=True, blank=True, max_length=150)
    old_bz3=models.CharField('BZ3', null=True, blank=True, max_length=150)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_xxtzzp20221024'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（xxtzzp20221024，待确认）'
        ordering=["-id"]

class SourceDboZhenzhibaobiao(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='zhenzhibaobiao'
    SOURCE_FIELDS={'日期': 'old_日期', '下单': 'old_下单', '下单匹数': 'old_下单匹数', '下单数量': 'old_下单数量', '正常开卡': 'old_正常开卡', '预配匹数': 'old_预配匹数', '预配数量': 'old_预配数量', '回修开卡': 'old_回修开卡', '回修预配匹数': 'old_回修预配匹数', '回修预配数量': 'old_回修预配数量', '在制品缸数': 'old_在制品缸数', '在制品匹数': 'old_在制品匹数', '在制品数量': 'old_在制品数量', '出缸数': 'old_出缸数', '出缸匹数': 'old_出缸匹数', '出缸数量': 'old_出缸数量', '成定缸数': 'old_成定缸数', '成定匹数': 'old_成定匹数', '成定数量': 'old_成定数量', '打卷缸数': 'old_打卷缸数', '打卷坯重': 'old_打卷坯重', '打卷成品重': 'old_打卷成品重', '入库单数': 'old_入库单数', '入库匹数': 'old_入库匹数', '入库坯重': 'old_入库坯重', '入库成品重': 'old_入库成品重', '库存成品匹数': 'old_库存成品匹数', '库存成品坯重': 'old_库存成品坯重', '库存成品重量': 'old_库存成品重量', '库存坯布匹数': 'old_库存坯布匹数', '库存坯重': 'old_库存坯重'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_日期=models.DateField('日期', null=True, blank=True)
    old_下单=models.IntegerField('下单', null=True, blank=True)
    old_下单匹数=models.DecimalField('下单匹数', null=True, blank=True, max_digits=38, decimal_places=2)
    old_下单数量=models.DecimalField('下单数量', null=True, blank=True, max_digits=38, decimal_places=2)
    old_正常开卡=models.IntegerField('正常开卡', null=True, blank=True)
    old_预配匹数=models.DecimalField('预配匹数', null=True, blank=True, max_digits=38, decimal_places=2)
    old_预配数量=models.DecimalField('预配数量', null=True, blank=True, max_digits=38, decimal_places=2)
    old_回修开卡=models.IntegerField('回修开卡', null=True, blank=True)
    old_回修预配匹数=models.DecimalField('回修预配匹数', null=True, blank=True, max_digits=38, decimal_places=2)
    old_回修预配数量=models.DecimalField('回修预配数量', null=True, blank=True, max_digits=38, decimal_places=2)
    old_在制品缸数=models.IntegerField('在制品缸数', null=True, blank=True)
    old_在制品匹数=models.DecimalField('在制品匹数', null=True, blank=True, max_digits=38, decimal_places=2)
    old_在制品数量=models.DecimalField('在制品数量', null=True, blank=True, max_digits=38, decimal_places=2)
    old_出缸数=models.IntegerField('出缸数', null=True, blank=True)
    old_出缸匹数=models.DecimalField('出缸匹数', null=True, blank=True, max_digits=38, decimal_places=2)
    old_出缸数量=models.DecimalField('出缸数量', null=True, blank=True, max_digits=38, decimal_places=2)
    old_成定缸数=models.IntegerField('成定缸数', null=True, blank=True)
    old_成定匹数=models.DecimalField('成定匹数', null=True, blank=True, max_digits=38, decimal_places=3)
    old_成定数量=models.DecimalField('成定数量', null=True, blank=True, max_digits=38, decimal_places=3)
    old_打卷缸数=models.IntegerField('打卷缸数', null=True, blank=True)
    old_打卷坯重=models.DecimalField('打卷坯重', null=True, blank=True, max_digits=38, decimal_places=2)
    old_打卷成品重=models.DecimalField('打卷成品重', null=True, blank=True, max_digits=38, decimal_places=2)
    old_入库单数=models.IntegerField('入库单数', null=True, blank=True)
    old_入库匹数=models.DecimalField('入库匹数', null=True, blank=True, max_digits=38, decimal_places=2)
    old_入库坯重=models.DecimalField('入库坯重', null=True, blank=True, max_digits=38, decimal_places=2)
    old_入库成品重=models.DecimalField('入库成品重', null=True, blank=True, max_digits=38, decimal_places=2)
    old_库存成品匹数=models.DecimalField('库存成品匹数', null=True, blank=True, max_digits=38, decimal_places=2)
    old_库存成品坯重=models.DecimalField('库存成品坯重', null=True, blank=True, max_digits=38, decimal_places=2)
    old_库存成品重量=models.DecimalField('库存成品重量', null=True, blank=True, max_digits=38, decimal_places=2)
    old_库存坯布匹数=models.DecimalField('库存坯布匹数', null=True, blank=True, max_digits=38, decimal_places=2)
    old_库存坯重=models.DecimalField('库存坯重', null=True, blank=True, max_digits=38, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_zhenzhibaobiao'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（zhenzhibaobiao，待确认）'
        ordering=["-id"]

class SourceDboZJHXMXBB(SourceRecord):
    SOURCE_SCHEMA='dbo'
    SOURCE_TABLE='ZJHXMXBB'
    SOURCE_FIELDS={'序号': 'old_序号', '日期': 'old_日期', '客户': 'old_客户', '缸号': 'old_缸号', '布种': 'old_布种', '颜色': 'old_颜色', '原缸条数': 'old_原缸条数', '抽疋条数': 'old_抽疋条数', '异常原因': 'old_异常原因', '责任部门': 'old_责任部门', '责任人': 'old_责任人', '处理方案': 'old_处理方案', '完成时间': 'old_完成时间', '备注': 'old_备注', '处罚金额': 'old_处罚金额'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_序号=models.CharField('序号', null=True, blank=True, max_length=10)
    old_日期=models.DateField('日期', null=True, blank=True)
    old_客户=models.CharField('客户', null=True, blank=True, max_length=50)
    old_缸号=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_布种=models.CharField('布种', null=True, blank=True, max_length=50)
    old_颜色=models.CharField('颜色', null=True, blank=True, max_length=50)
    old_原缸条数=models.DecimalField('原缸条数', null=True, blank=True, max_digits=9, decimal_places=1)
    old_抽疋条数=models.DecimalField('抽疋条数', null=True, blank=True, max_digits=9, decimal_places=1)
    old_异常原因=models.CharField('异常原因', null=True, blank=True, max_length=500)
    old_责任部门=models.CharField('责任部门', null=True, blank=True, max_length=50)
    old_责任人=models.CharField('责任人', null=True, blank=True, max_length=50)
    old_处理方案=models.CharField('处理方案', null=True, blank=True, max_length=500)
    old_完成时间=models.CharField('完成时间', null=True, blank=True, max_length=50)
    old_备注=models.CharField('备注', null=True, blank=True, max_length=500)
    old_处罚金额=models.CharField('处罚金额', null=True, blank=True, max_length=500)

    class Meta(SourceRecord.Meta):
        db_table='src_dbo_zjhxmxbb'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（ZJHXMXBB，待确认）'
        ordering=["-id"]

class SourceDyeACGroup(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ACGroup'
    SOURCE_FIELDS={'GroupID': 'old_group_id', 'Name': 'old_name', 'TimeZone1': 'old_time_zone1', 'TimeZone2': 'old_time_zone2', 'TimeZone3': 'old_time_zone3', 'holidayvaild': 'old_holidayvaild', 'verifystyle': 'old_verifystyle'}
    SOURCE_KEY=('GroupID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_time_zone1': ('literal', 0), 'old_time_zone2': ('literal', 0), 'old_time_zone3': ('literal', 0)}
    SOURCE_IDENTITIES=()
    old_group_id=models.IntegerField('GroupID', null=False, blank=False)
    old_name=models.CharField('Name', null=True, blank=True, max_length=30)
    old_time_zone1=models.IntegerField('TimeZone1', null=True, blank=True)
    old_time_zone2=models.IntegerField('TimeZone2', null=True, blank=True)
    old_time_zone3=models.IntegerField('TimeZone3', null=True, blank=True)
    old_holidayvaild=models.BooleanField('holidayvaild', null=True, blank=True)
    old_verifystyle=models.IntegerField('verifystyle', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_acgroup'
        indexes=[models.Index(fields=['source_batch', 'old_group_id'],name='src_f15c663ff31d92b2')]
        verbose_name=verbose_name_plural='其他或待确认相关表（ACGroup，待确认）'
        ordering=["-id"]

class SourceDyeAcholiday(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='acholiday'
    SOURCE_FIELDS={'begindate': 'old_begindate', 'enddate': 'old_enddate', 'holidayid': 'old_holidayid', 'primaryid': 'old_primaryid', 'timezone': 'old_timezone'}
    SOURCE_KEY=('primaryid',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=('old_primaryid',)
    old_begindate=models.DateTimeField('begindate', null=True, blank=True)
    old_enddate=models.DateTimeField('enddate', null=True, blank=True)
    old_holidayid=models.IntegerField('holidayid', null=True, blank=True)
    old_primaryid=models.IntegerField('primaryid', null=False, blank=False)
    old_timezone=models.IntegerField('timezone', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_acholiday'
        indexes=[models.Index(fields=['source_batch', 'old_primaryid'],name='src_ff6e234cd529c1fc')]
        verbose_name=verbose_name_plural='其他或待确认相关表（acholiday，待确认）'
        ordering=["-id"]

class SourceDyeACUnlockComb(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ACUnlockComb'
    SOURCE_FIELDS={'UnlockCombID': 'old_unlock_comb_id', 'Name': 'old_name', 'Group01': 'old_group01', 'Group02': 'old_group02', 'Group03': 'old_group03', 'Group04': 'old_group04', 'Group05': 'old_group05'}
    SOURCE_KEY=('UnlockCombID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_unlock_comb_id=models.IntegerField('UnlockCombID', null=False, blank=False)
    old_name=models.CharField('Name', null=True, blank=True, max_length=30)
    old_group01=models.IntegerField('Group01', null=True, blank=True)
    old_group02=models.IntegerField('Group02', null=True, blank=True)
    old_group03=models.IntegerField('Group03', null=True, blank=True)
    old_group04=models.IntegerField('Group04', null=True, blank=True)
    old_group05=models.IntegerField('Group05', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_acunlockcomb'
        indexes=[models.Index(fields=['source_batch', 'old_unlock_comb_id'],name='src_f5f4aa954a668ede')]
        verbose_name=verbose_name_plural='其他或待确认相关表（ACUnlockComb，待确认）'
        ordering=["-id"]

class SourceDyeAPPUploadFilesInfo(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='APPUploadFilesInfo'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'Kind': 'old_kind', 'uiIndex': 'old_ui_index', 'Guid': 'old_guid', 'OriFileName': 'old_ori_file_name', 'SaveFileName': 'old_save_file_name', 'FileNameUrl': 'old_file_name_url', 'SaveDate': 'old_save_date', 'UserID': 'old_user_id', 'fileType': 'old_file_type'}
    SOURCE_KEY=('Guid',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=50)
    old_kind=models.IntegerField('Kind', null=True, blank=True)
    old_ui_index=models.IntegerField('uiIndex', null=True, blank=True)
    old_guid=models.CharField('Guid', null=False, blank=True, max_length=50)
    old_ori_file_name=models.CharField('OriFileName', null=True, blank=True, max_length=100)
    old_save_file_name=models.CharField('SaveFileName', null=True, blank=True, max_length=200)
    old_file_name_url=models.CharField('FileNameUrl', null=True, blank=True, max_length=200)
    old_save_date=models.DateTimeField('SaveDate', null=True, blank=True)
    old_user_id=models.CharField('UserID', null=True, blank=True, max_length=20)
    old_file_type=models.CharField('fileType', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_appuploadfilesinfo'
        indexes=[models.Index(fields=['source_batch', 'old_guid'],name='src_9bf59442d4edc802')]
        verbose_name=verbose_name_plural='其他或待确认相关表（APPUploadFilesInfo，待确认）'
        ordering=["-id"]

class SourceDyeAPPUploadFilesInfoDel(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='APPUploadFilesInfoDel'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'Kind': 'old_kind', 'uiIndex': 'old_ui_index', 'Guid': 'old_guid', 'OriFileName': 'old_ori_file_name', 'SaveFileName': 'old_save_file_name', 'FileNameUrl': 'old_file_name_url', 'SaveDate': 'old_save_date', 'UserID': 'old_user_id', 'DeletePerson': 'old_delete_person', 'DeleteDate': 'old_delete_date', 'fileType': 'old_file_type'}
    SOURCE_KEY=('Guid',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=50)
    old_kind=models.IntegerField('Kind', null=True, blank=True)
    old_ui_index=models.IntegerField('uiIndex', null=True, blank=True)
    old_guid=models.CharField('Guid', null=False, blank=True, max_length=50)
    old_ori_file_name=models.CharField('OriFileName', null=True, blank=True, max_length=100)
    old_save_file_name=models.CharField('SaveFileName', null=True, blank=True, max_length=200)
    old_file_name_url=models.CharField('FileNameUrl', null=True, blank=True, max_length=200)
    old_save_date=models.DateTimeField('SaveDate', null=True, blank=True)
    old_user_id=models.CharField('UserID', null=True, blank=True, max_length=20)
    old_delete_person=models.CharField('DeletePerson', null=True, blank=True, max_length=20)
    old_delete_date=models.DateTimeField('DeleteDate', null=True, blank=True)
    old_file_type=models.CharField('fileType', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_appuploadfilesinfodel'
        indexes=[models.Index(fields=['source_batch', 'old_guid'],name='src_9cccb9564ab58f59')]
        verbose_name=verbose_name_plural='其他或待确认相关表（APPUploadFilesInfoDel，待确认）'
        ordering=["-id"]

class SourceDyeArrivalNotice(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ArrivalNotice'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'BusinessUnitID': 'old_business_unit_id', 'SupplierID': 'old_supplier_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_sheet_no': ('literal', ''), 'old_sheet_date': ('literal', '1900-01-01'), 'old_sheet_kind': ('literal', 0), 'old_business_unit_id': ('literal', ''), 'old_supplier_id': ('literal', ''), 'old_sheet_status': ('literal', 0), 'old_right_status': ('literal', 0), 'old_print_times': ('literal', 0), 'old_revisions': ('literal', 0), 'old_remarks': ('literal', ''), 'old_creater': ('literal', ''), 'old_create_date': ('literal', '1900-01-01'), 'old_modifyer': ('literal', ''), 'old_modify_date': ('literal', '1900-01-01')}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类别', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_supplier_id=models.CharField('供应商代码', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_arrivalnotice'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_e2fca3b8cae25533')]
        verbose_name=verbose_name_plural='其他或待确认相关表（ArrivalNotice，待确认）'
        ordering=["-id"]

class SourceDyeArrivalNoticeDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ArrivalNoticeDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'FabricID': 'old_fabric_id', 'Spec': 'old_spec', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'ColorE': 'old_color_e', 'Rolls': 'old_rolls', 'Qty': 'old_qty', 'StockUnit': 'old_stock_unit', 'CheckNo': 'old_check_no', 'Remarks': 'old_remarks', 'JobDetailNo': 'old_job_detail_no', 'PurDetailNo': 'old_pur_detail_no'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：ArrivalNotice', 'target': 'erp_base.SourceDyeArrivalNotice', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 ArivalNoticeDetail → ArrivalNotice']}]
    SOURCE_DEFAULTS={'old_fabric_id': ('literal', ''), 'old_spec': ('literal', ''), 'old_color_id': ('literal', ''), 'old_color_num': ('literal', ''), 'old_color_e': ('literal', ''), 'old_rolls': ('literal', 0), 'old_qty': ('literal', 0), 'old_stock_unit': ('literal', 0), 'old_check_no': ('literal', ''), 'old_remarks': ('literal', '')}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('表单明细号（子表）', null=False, blank=True, max_length=20)
    old_fabric_id=models.CharField('客户规格', null=False, blank=True, max_length=10)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=10)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=20)
    old_color_e=models.CharField('颜色英文名', null=True, blank=True, max_length=20)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_stock_unit=models.IntegerField('库存单位', null=True, blank=True)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_job_detail_no=models.CharField('加工作业号', null=True, blank=True, max_length=20)
    old_pur_detail_no=models.CharField('采购单明细号', null=True, blank=True, max_length=20)
    source_parent_1=models.ForeignKey('erp_base.SourceDyeArrivalNotice', verbose_name='原关系：ArrivalNotice', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_arrivalnoticedetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_42bea92c9e9e4c15')]
        verbose_name=verbose_name_plural='其他或待确认相关表（ArrivalNoticeDetail，待确认）'
        ordering=["-id"]

class SourceDyeAttachment(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='Attachment'
    SOURCE_FIELDS={'ID': 'old_id', 'RowNo': 'old_row_no', 'DataTableName': 'old_data_table_name', 'FieldValues': 'old_field_values', 'FilePath': 'old_file_path', 'FileName': 'old_file_name', 'FileType': 'old_file_type', 'FileSize': 'old_file_size', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'Description': 'old_description'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.CharField('ID', null=False, blank=True, max_length=50)
    old_row_no=models.IntegerField('RowNo', null=True, blank=True)
    old_data_table_name=models.CharField('DataTableName', null=True, blank=True, max_length=50)
    old_field_values=models.CharField('FieldValues', null=True, blank=True, max_length=1000)
    old_file_path=models.CharField('FilePath', null=True, blank=True, max_length=500)
    old_file_name=models.CharField('FileName', null=True, blank=True, max_length=100)
    old_file_type=models.CharField('FileType', null=True, blank=True, max_length=10)
    old_file_size=models.IntegerField('FileSize', null=True, blank=True)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_description=models.CharField('Description', null=True, blank=True, max_length=500)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_attachment'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_ee1c00d3ffa6cfac')]
        verbose_name=verbose_name_plural='其他或待确认相关表（Attachment，待确认）'
        ordering=["-id"]

class SourceDyeAttParam(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='AttParam'
    SOURCE_FIELDS={'PARANAME': 'old_paraname', 'PARATYPE': 'old_paratype', 'PARAVALUE': 'old_paravalue'}
    SOURCE_KEY=('PARANAME',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_paraname=models.CharField('PARANAME', null=False, blank=True, max_length=20)
    old_paratype=models.CharField('PARATYPE', null=True, blank=True, max_length=2)
    old_paravalue=models.CharField('PARAVALUE', null=False, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_attparam'
        indexes=[models.Index(fields=['source_batch', 'old_paraname'],name='src_283ac1238344b0f7')]
        verbose_name=verbose_name_plural='系统平台与配置相关表（AttParam，待确认）'
        ordering=["-id"]

class SourceDyeAuditedExc(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='AuditedExc'
    SOURCE_FIELDS={'AEID': 'old_aeid', 'UserId': 'old_user_id', 'CheckTime': 'old_check_time', 'NewExcID': 'old_new_exc_id', 'IsLeave': 'old_is_leave', 'UName': 'old_uname', 'UTime': 'old_utime'}
    SOURCE_KEY=('AEID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=('old_aeid',)
    old_aeid=models.IntegerField('AEID', null=False, blank=False)
    old_user_id=models.IntegerField('UserId', null=True, blank=True)
    old_check_time=models.DateTimeField('CheckTime', null=False, blank=False)
    old_new_exc_id=models.IntegerField('NewExcID', null=True, blank=True)
    old_is_leave=models.IntegerField('IsLeave', null=True, blank=True)
    old_uname=models.CharField('UName', null=True, blank=True, max_length=20)
    old_utime=models.DateTimeField('UTime', null=False, blank=False)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_auditedexc'
        indexes=[models.Index(fields=['source_batch', 'old_aeid'],name='src_56d74ec422483e75')]
        verbose_name=verbose_name_plural='其他或待确认相关表（AuditedExc，待确认）'
        ordering=["-id"]

class SourceDyeAUTHDEVICE(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='AUTHDEVICE'
    SOURCE_FIELDS={'ID': 'old_id', 'USERID': 'old_userid', 'MachineID': 'old_machine_id'}
    SOURCE_KEY=('USERID', 'MachineID')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=('old_id',)
    old_id=models.IntegerField('ID', null=False, blank=False)
    old_userid=models.IntegerField('USERID', null=False, blank=False)
    old_machine_id=models.IntegerField('MachineID', null=False, blank=False)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_authdevice'
        indexes=[models.Index(fields=['source_batch', 'old_userid', 'old_machine_id'],name='src_9e74a95bfd99f5b8')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（AUTHDEVICE，待确认）'
        ordering=["-id"]

class SourceDyeBalancingConditions(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='BalancingConditions'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'Rolls': 'old_rolls', 'WeightQty': 'old_weight_qty', 'LengthQty': 'old_length_qty', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=30)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=30)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_rolls=models.DecimalField('Rolls', null=True, blank=True, max_digits=7, decimal_places=2)
    old_weight_qty=models.DecimalField('WeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('LengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=20)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=20)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_balancingconditions'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_83c089663f46e4d3')]
        verbose_name=verbose_name_plural='其他或待确认相关表（BalancingConditions，待确认）'
        ordering=["-id"]

class SourceDyeBaseCase(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='BaseCase'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'CaseName': 'old_case_name', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'RightStatus': 'old_right_status', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('类型', null=True, blank=True)
    old_case_name=models.CharField('方案名称', null=True, blank=True, max_length=50)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('制单人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('制单日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_basecase'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_d078d8dc1e4fe523')]
        verbose_name=verbose_name_plural='其他或待确认相关表（BaseCase，待确认）'
        ordering=["-id"]

class SourceDyeBaseCaseDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='BaseCaseDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'SortNo': 'old_sort_no', 'SerialNum': 'old_serial_num', 'ProjectInfo': 'old_project_info', 'DefaultValue': 'old_default_value', 'Remarks': 'old_remarks', 'IsInputText': 'old_is_input_text'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：BaseCase', 'target': 'erp_base.SourceDyeBaseCase', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 BaseCaseDetail → BaseCase']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=36)
    old_sort_no=models.IntegerField('排序序号', null=True, blank=True)
    old_serial_num=models.CharField('序号', null=True, blank=True, max_length=10)
    old_project_info=models.CharField('项目内容', null=True, blank=True, max_length=200)
    old_default_value=models.CharField('常规值', null=True, blank=True, max_length=100)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_is_input_text=models.BooleanField('是否输入文本', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_base.SourceDyeBaseCase', verbose_name='原关系：BaseCase', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_basecasedetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_194611fd42f6ce7d')]
        verbose_name=verbose_name_plural='其他或待确认相关表（BaseCaseDetail，待确认）'
        ordering=["-id"]

class SourceDyeBiotemplate(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='Biotemplate'
    SOURCE_FIELDS={'ID': 'old_id', 'USER_ID': 'old_user_id', 'user_pin': 'old_user_pin', 'create_operator': 'old_create_operator', 'create_time': 'old_create_time', 'valid_flag': 'old_valid_flag', 'is_duress': 'old_is_duress', 'bio_type': 'old_bio_type', 'version': 'old_version', 'data_format': 'old_data_format', 'template_no': 'old_template_no', 'template_no_index': 'old_template_no_index', 'Template_Data': 'old_template_data', 'nOldType': 'old_n_old_type'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=('old_id',)
    old_id=models.IntegerField('ID', null=False, blank=False)
    old_user_id=models.IntegerField('USER_ID', null=True, blank=True)
    old_user_pin=models.CharField('user_pin', null=True, blank=True, max_length=50)
    old_create_operator=models.CharField('create_operator', null=True, blank=True, max_length=50)
    old_create_time=models.DateTimeField('create_time', null=True, blank=True)
    old_valid_flag=models.IntegerField('valid_flag', null=True, blank=True)
    old_is_duress=models.IntegerField('is_duress', null=True, blank=True)
    old_bio_type=models.IntegerField('bio_type', null=True, blank=True)
    old_version=models.CharField('version', null=True, blank=True, max_length=50)
    old_data_format=models.IntegerField('data_format', null=True, blank=True)
    old_template_no=models.IntegerField('template_no', null=True, blank=True)
    old_template_no_index=models.IntegerField('template_no_index', null=True, blank=True)
    old_template_data=models.TextField('Template_Data', null=True, blank=True)
    old_n_old_type=models.IntegerField('nOldType', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_biotemplate'
        indexes=[]
        verbose_name=verbose_name_plural='基础主数据相关表（Biotemplate，待确认）'
        ordering=["-id"]

class SourceDyeClockShift(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ClockShift'
    SOURCE_FIELDS={'EmpID': 'old_emp_id', 'ShiftCode': 'old_shift_code', 'CreateTime': 'old_create_time'}
    SOURCE_KEY=('EmpID', 'ShiftCode')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_create_time': ('now', None)}
    SOURCE_IDENTITIES=()
    old_emp_id=models.CharField('EmpID', null=False, blank=True, max_length=20)
    old_shift_code=models.CharField('ShiftCode', null=False, blank=True, max_length=20)
    old_create_time=models.DateTimeField('CreateTime', null=False, blank=False)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_clockshift'
        indexes=[models.Index(fields=['source_batch', 'old_emp_id', 'old_shift_code'],name='src_2e3134f68b390dbb')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（ClockShift，待确认）'
        ordering=["-id"]

class SourceDyeCompensatedetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='compensatedetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'JobSheetNo': 'old_job_sheet_no', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'CustomerProdName': 'old_customer_prod_name', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'CustColorNum': 'old_cust_color_num', 'Weight': 'old_weight', 'Width': 'old_width', 'Rolls': 'old_rolls', 'WeightQty': 'old_weight_qty', 'LengthQty': 'old_length_qty', 'Description': 'old_description', 'Remarks': 'old_remarks', 'QualityDeductionSheetNo': 'old_quality_deduction_sheet_no', 'GrayQty': 'old_gray_qty', 'qy': 'old_qy', 'kw': 'old_kw', 'PayMoney': 'old_pay_money', 'PayQTY': 'old_pay_qty'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：compensatemain', 'target': 'erp_base.SourceDyeCompensatemain', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 compensatedetail → compensatemain']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=20)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=20)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=20)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=200)
    old_customer_prod_name=models.CharField('CustomerProdName', null=True, blank=True, max_length=200)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=150)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=20)
    old_cust_color_num=models.CharField('CustColorNum', null=True, blank=True, max_length=150)
    old_weight=models.CharField('Weight', null=True, blank=True, max_length=256)
    old_width=models.CharField('Width', null=True, blank=True, max_length=256)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_weight_qty=models.DecimalField('WeightQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('LengthQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_description=models.CharField('Description', null=True, blank=True, max_length=512)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_quality_deduction_sheet_no=models.CharField('QualityDeductionSheetNo', null=True, blank=True, max_length=32)
    old_gray_qty=models.DecimalField('GrayQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_qy=models.CharField('qy', null=True, blank=True, max_length=150)
    old_kw=models.CharField('kw', null=True, blank=True, max_length=150)
    old_pay_money=models.DecimalField('PayMoney', null=True, blank=True, max_digits=7, decimal_places=2)
    old_pay_qty=models.DecimalField('PayQTY', null=True, blank=True, max_digits=7, decimal_places=2)
    source_parent_1=models.ForeignKey('erp_base.SourceDyeCompensatemain', verbose_name='原关系：compensatemain', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_compensatedetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_710bc7c7e7e084a1')]
        verbose_name=verbose_name_plural='其他或待确认相关表（compensatedetail，待确认）'
        ordering=["-id"]

class SourceDyeCompensatemain(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='compensatemain'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'PendOutSheetSeries': 'old_pend_out_sheet_series', 'CustomerID': 'old_customer_id'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_pend_out_sheet_series=models.CharField('PendOutSheetSeries', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_compensatemain'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_35cccf9b9056eb4d')]
        verbose_name=verbose_name_plural='其他或待确认相关表（compensatemain，待确认）'
        ordering=["-id"]

class SourceDyeCookIn(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='CookIn'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'InKindID': 'old_in_kind_id', 'BuyerID': 'old_buyer_id', 'WareHouseID': 'old_ware_house_id', 'SupplierID': 'old_supplier_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'StepNo': 'old_step_no', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'BusinessUnitID': 'old_business_unit_id', 'Keeper': 'old_keeper', 'Reason': 'old_reason', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'Settle': 'old_settle', 'deliverynum': 'old_deliverynum', 'APMoney': 'old_apmoney', 'APQty': 'old_apqty', 'UnClearQty': 'old_un_clear_qty', 'UnClearMoney': 'old_un_clear_money', 'UnClearInvoiceQty': 'old_un_clear_invoice_qty', 'UnClearInvoiceMoney': 'old_un_clear_invoice_money', 'DiscountMoney': 'old_discount_money', 'SumAmount': 'old_sum_amount', 'InvoiceClearStatus': 'old_invoice_clear_status', 'MoneyClearStatus': 'old_money_clear_status'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_in_kind_id=models.CharField('入库类别', null=True, blank=True, max_length=10)
    old_buyer_id=models.CharField('采购员', null=True, blank=True, max_length=50)
    old_ware_house_id=models.CharField('仓库代码', null=True, blank=True, max_length=10)
    old_supplier_id=models.CharField('结算方式', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_step_no=models.IntegerField('流程节点号', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_keeper=models.CharField('仓管员', null=True, blank=True, max_length=10)
    old_reason=models.CharField('Reason', null=True, blank=True, max_length=256)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_settle=models.CharField('Settle', null=True, blank=True, max_length=50)
    old_deliverynum=models.CharField('deliverynum', null=True, blank=True, max_length=50)
    old_apmoney=models.DecimalField('APMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_apqty=models.DecimalField('APQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_un_clear_qty=models.DecimalField('UnClearQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_un_clear_money=models.DecimalField('UnClearMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_un_clear_invoice_qty=models.DecimalField('UnClearInvoiceQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_un_clear_invoice_money=models.DecimalField('UnClearInvoiceMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_discount_money=models.DecimalField('DiscountMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sum_amount=models.DecimalField('SumAmount', null=True, blank=True, max_digits=10, decimal_places=2)
    old_invoice_clear_status=models.IntegerField('InvoiceClearStatus', null=True, blank=True)
    old_money_clear_status=models.IntegerField('MoneyClearStatus', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_cookin'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_46b13062e1faf98e')]
        verbose_name=verbose_name_plural='其他或待确认相关表（CookIn，待确认）'
        ordering=["-id"]

class SourceDyeDEPARTMENTS(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DEPARTMENTS'
    SOURCE_FIELDS={'DEPTID': 'old_deptid', 'DEPTNAME': 'old_deptname', 'SUPDEPTID': 'old_supdeptid', 'InheritParentSch': 'old_inherit_parent_sch', 'InheritDeptSch': 'old_inherit_dept_sch', 'InheritDeptSchClass': 'old_inherit_dept_sch_class', 'AutoSchPlan': 'old_auto_sch_plan', 'InLate': 'old_in_late', 'OutEarly': 'old_out_early', 'InheritDeptRule': 'old_inherit_dept_rule', 'MinAutoSchInterval': 'old_min_auto_sch_interval', 'RegisterOT': 'old_register_ot', 'DefaultSchId': 'old_default_sch_id', 'ATT': 'old_att', 'Holiday': 'old_holiday', 'OverTime': 'old_over_time', 'Code': 'old_code'}
    SOURCE_KEY=('DEPTID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_supdeptid': ('literal', 1), 'old_inherit_parent_sch': ('literal', 1), 'old_inherit_dept_sch': ('literal', 1), 'old_inherit_dept_sch_class': ('literal', 1), 'old_auto_sch_plan': ('literal', 1), 'old_in_late': ('literal', 1), 'old_out_early': ('literal', 1), 'old_inherit_dept_rule': ('literal', 1), 'old_min_auto_sch_interval': ('literal', 24), 'old_register_ot': ('literal', 1), 'old_default_sch_id': ('literal', 1), 'old_att': ('literal', 1), 'old_holiday': ('literal', 1), 'old_over_time': ('literal', 1)}
    SOURCE_IDENTITIES=('old_deptid',)
    old_deptid=models.IntegerField('DEPTID', null=False, blank=False)
    old_deptname=models.CharField('DEPTNAME', null=True, blank=True, max_length=30)
    old_supdeptid=models.IntegerField('SUPDEPTID', null=False, blank=False)
    old_inherit_parent_sch=models.IntegerField('InheritParentSch', null=True, blank=True)
    old_inherit_dept_sch=models.IntegerField('InheritDeptSch', null=True, blank=True)
    old_inherit_dept_sch_class=models.IntegerField('InheritDeptSchClass', null=True, blank=True)
    old_auto_sch_plan=models.IntegerField('AutoSchPlan', null=True, blank=True)
    old_in_late=models.IntegerField('InLate', null=True, blank=True)
    old_out_early=models.IntegerField('OutEarly', null=True, blank=True)
    old_inherit_dept_rule=models.IntegerField('InheritDeptRule', null=True, blank=True)
    old_min_auto_sch_interval=models.IntegerField('MinAutoSchInterval', null=True, blank=True)
    old_register_ot=models.IntegerField('RegisterOT', null=True, blank=True)
    old_default_sch_id=models.IntegerField('DefaultSchId', null=False, blank=False)
    old_att=models.IntegerField('ATT', null=True, blank=True)
    old_holiday=models.IntegerField('Holiday', null=True, blank=True)
    old_over_time=models.IntegerField('OverTime', null=True, blank=True)
    old_code=models.CharField('Code', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_departments'
        indexes=[models.Index(fields=['source_batch', 'old_deptid'],name='src_0944dcefecf3ca0b')]
        verbose_name=verbose_name_plural='其他或待确认相关表（DEPARTMENTS，待确认）'
        ordering=["-id"]

class SourceDyeDeptUsedSchs(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DeptUsedSchs'
    SOURCE_FIELDS={'DeptId': 'old_dept_id', 'SchId': 'old_sch_id'}
    SOURCE_KEY=('DeptId', 'SchId')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_dept_id=models.IntegerField('DeptId', null=False, blank=False)
    old_sch_id=models.IntegerField('SchId', null=False, blank=False)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_deptusedschs'
        indexes=[models.Index(fields=['source_batch', 'old_dept_id', 'old_sch_id'],name='src_036082fa4dc6b859')]
        verbose_name=verbose_name_plural='其他或待确认相关表（DeptUsedSchs，待确认）'
        ordering=["-id"]

class SourceDyeDyeProcessPrice(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='DyeProcessPrice'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'GrayKindID': 'old_gray_kind_id', 'PhaseID': 'old_phase_id', 'MachineKindID': 'old_machine_kind_id', 'ColorDepthID': 'old_color_depth_id', 'Price': 'old_price', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('编号', null=False, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('时间', null=True, blank=True)
    old_gray_kind_id=models.CharField('纱类', null=True, blank=True, max_length=10)
    old_phase_id=models.CharField('染程', null=True, blank=True, max_length=10)
    old_machine_kind_id=models.CharField('机台管数', null=True, blank=True, max_length=10)
    old_color_depth_id=models.CharField('颜色深浅', null=True, blank=True, max_length=50)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_dyeprocessprice'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_72e1d77c3f847851')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（DyeProcessPrice，待确认）'
        ordering=["-id"]

class SourceDyeEmpRoom(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='Emp_Room'
    SOURCE_FIELDS={'RoomNo': 'old_room_no', 'EmpID1': 'old_emp_id1', 'EmpID2': 'old_emp_id2', 'EmpID3': 'old_emp_id3', 'EmpID4': 'old_emp_id4', 'EmpID5': 'old_emp_id5', 'EmpID6': 'old_emp_id6', 'EmpID7': 'old_emp_id7', 'EmpID8': 'old_emp_id8', 'Remarks': 'old_remarks', 'EmpID9': 'old_emp_id9', 'EmpID10': 'old_emp_id10'}
    SOURCE_KEY=('RoomNo',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_room_no=models.CharField('房间号', null=False, blank=True, max_length=10)
    old_emp_id1=models.CharField('员工1', null=True, blank=True, max_length=10)
    old_emp_id2=models.CharField('员工2', null=True, blank=True, max_length=10)
    old_emp_id3=models.CharField('员工3', null=True, blank=True, max_length=10)
    old_emp_id4=models.CharField('员工4', null=True, blank=True, max_length=10)
    old_emp_id5=models.CharField('员工5', null=True, blank=True, max_length=10)
    old_emp_id6=models.CharField('员工6', null=True, blank=True, max_length=10)
    old_emp_id7=models.CharField('员工7', null=True, blank=True, max_length=10)
    old_emp_id8=models.CharField('员工8', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=50)
    old_emp_id9=models.CharField('员工9', null=True, blank=True, max_length=10)
    old_emp_id10=models.CharField('员工10', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_emp_room'
        indexes=[models.Index(fields=['source_batch', 'old_room_no'],name='src_821f438c97a78d3e')]
        verbose_name=verbose_name_plural='基础主数据相关表（Emp_Room，待确认）'
        ordering=["-id"]

class SourceDyeEnableCard(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='EnableCard'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'FirstCard': 'old_first_card', 'SecondCard': 'old_second_card', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=30)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=30)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_first_card=models.BooleanField('FirstCard', null=True, blank=True)
    old_second_card=models.BooleanField('SecondCard', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=20)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=20)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_enablecard'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_47e85ea31fec0387')]
        verbose_name=verbose_name_plural='其他或待确认相关表（EnableCard，待确认）'
        ordering=["-id"]

class SourceDyeEXCNOTES(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='EXCNOTES'
    SOURCE_FIELDS={'USERID': 'old_userid', 'ATTDATE': 'old_attdate', 'NOTES': 'old_notes'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_userid=models.IntegerField('USERID', null=True, blank=True)
    old_attdate=models.DateTimeField('ATTDATE', null=True, blank=True)
    old_notes=models.CharField('NOTES', null=True, blank=True, max_length=200)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_excnotes'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（EXCNOTES，待确认）'
        ordering=["-id"]

class SourceDyeFaceTemp(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='FaceTemp'
    SOURCE_FIELDS={'TEMPLATEID': 'old_templateid', 'USERNO': 'old_userno', 'SIZE': 'old_size', 'pin': 'old_pin', 'FACEID': 'old_faceid', 'VALID': 'old_valid', 'RESERVE': 'old_reserve', 'ACTIVETIME': 'old_activetime', 'VFCOUNT': 'old_vfcount', 'TEMPLATE': 'old_template', 'UserID': 'old_user_id'}
    SOURCE_KEY=('TEMPLATEID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_size': ('literal', 0), 'old_pin': ('literal', 0), 'old_faceid': ('literal', 0), 'old_valid': ('literal', 0), 'old_reserve': ('literal', 0), 'old_activetime': ('literal', 0), 'old_vfcount': ('literal', 0), 'old_user_id': ('literal', 0)}
    SOURCE_IDENTITIES=('old_templateid',)
    old_templateid=models.IntegerField('TEMPLATEID', null=False, blank=False)
    old_userno=models.CharField('USERNO', null=True, blank=True, max_length=24)
    old_size=models.IntegerField('SIZE', null=True, blank=True)
    old_pin=models.IntegerField('pin', null=True, blank=True)
    old_faceid=models.IntegerField('FACEID', null=True, blank=True)
    old_valid=models.IntegerField('VALID', null=True, blank=True)
    old_reserve=models.IntegerField('RESERVE', null=True, blank=True)
    old_activetime=models.IntegerField('ACTIVETIME', null=True, blank=True)
    old_vfcount=models.IntegerField('VFCOUNT', null=True, blank=True)
    old_template=models.BinaryField('TEMPLATE', null=True, blank=True, editable=True)
    old_user_id=models.IntegerField('UserID', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_facetemp'
        indexes=[models.Index(fields=['source_batch', 'old_templateid'],name='src_f9b885e9057aa604')]
        verbose_name=verbose_name_plural='基础主数据相关表（FaceTemp，待确认）'
        ordering=["-id"]

class SourceDyeFeelOfferDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='FeelOfferDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ProdID': 'old_prod_id', 'Price': 'old_price', 'Unit': 'old_unit', 'Remarks': 'old_remarks', 'FeelCode': 'old_feel_code', 'CusPrice': 'old_cus_price', 'RightStatus': 'old_right_status', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'SGDH': 'old_sgdh', 'ProcessID': 'old_process_id'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：FeelOfferMain', 'target': 'erp_base.SourceDyeFeelOfferMain', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 FeelOfferDetail → FeelOfferMain']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=40)
    old_price=models.DecimalField('确价', null=True, blank=True, max_digits=9, decimal_places=2)
    old_unit=models.CharField('单位', null=True, blank=True, max_length=40)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_feel_code=models.CharField('手感编号', null=True, blank=True, max_length=40)
    old_cus_price=models.DecimalField('报价', null=True, blank=True, max_digits=10, decimal_places=2)
    old_right_status=models.IntegerField('状态', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=50)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_sgdh=models.CharField('SGDH', null=True, blank=True, max_length=50)
    old_process_id=models.CharField('工序', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_base.SourceDyeFeelOfferMain', verbose_name='原关系：FeelOfferMain', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_feelofferdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_e57cd1588b0bc604')]
        verbose_name=verbose_name_plural='其他或待确认相关表（FeelOfferDetail，待确认）'
        ordering=["-id"]

class SourceDyeFeelOfferMain(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='FeelOfferMain'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'CustomerID': 'old_customer_id', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'LastTime': 'old_last_time'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单号', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('单据时间', null=True, blank=True)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_last_time=models.DateTimeField('LastTime', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_feeloffermain'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_92c16d61c3855dfd')]
        verbose_name=verbose_name_plural='其他或待确认相关表（FeelOfferMain，待确认）'
        ordering=["-id"]

class SourceDyeFixedCanDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='FixedCanDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'GradeID': 'old_grade_id', 'FabricKindID': 'old_fabric_kind_id', 'ColorLevel': 'old_color_level', 'TaxPrice': 'old_tax_price', 'Price': 'old_price', 'StuffRatio1': 'old_stuff_ratio1', 'StuffRatio2': 'old_stuff_ratio2', 'FormulaCost1': 'old_formula_cost1', 'FormulaCost2': 'old_formula_cost2', 'Remarks': 'old_remarks', 'Weight1': 'old_weight1', 'Weight2': 'old_weight2'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=50)
    old_grade_id=models.CharField('GradeID', null=True, blank=True, max_length=30)
    old_fabric_kind_id=models.CharField('FabricKindID', null=True, blank=True, max_length=30)
    old_color_level=models.CharField('ColorLevel', null=True, blank=True, max_length=30)
    old_tax_price=models.DecimalField('TaxPrice', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=10, decimal_places=2)
    old_stuff_ratio1=models.DecimalField('StuffRatio1', null=True, blank=True, max_digits=10, decimal_places=2)
    old_stuff_ratio2=models.DecimalField('StuffRatio2', null=True, blank=True, max_digits=10, decimal_places=2)
    old_formula_cost1=models.DecimalField('FormulaCost1', null=True, blank=True, max_digits=10, decimal_places=2)
    old_formula_cost2=models.DecimalField('FormulaCost2', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_weight1=models.DecimalField('Weight1', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight2=models.DecimalField('Weight2', null=True, blank=True, max_digits=10, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_fixedcandetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_a0a7778df45aaf10')]
        verbose_name=verbose_name_plural='其他或待确认相关表（FixedCanDetail，待确认）'
        ordering=["-id"]

class SourceDyeFixedCanRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='FixedCanRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'RollNo': 'old_roll_no', 'GradeID': 'old_grade_id', 'FabricKindID': 'old_fabric_kind_id', 'ColorLevel': 'old_color_level', 'TaxPrice': 'old_tax_price', 'Price': 'old_price', 'StuffRatio1': 'old_stuff_ratio1', 'StuffRatio2': 'old_stuff_ratio2', 'FormulaCost1': 'old_formula_cost1', 'FormulaCost2': 'old_formula_cost2', 'Remarks': 'old_remarks', 'Weight1': 'old_weight1', 'Weight2': 'old_weight2'}
    SOURCE_KEY=('DetailNo', 'RollNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=50)
    old_roll_no=models.IntegerField('RollNo', null=False, blank=False)
    old_grade_id=models.CharField('GradeID', null=True, blank=True, max_length=30)
    old_fabric_kind_id=models.CharField('FabricKindID', null=True, blank=True, max_length=30)
    old_color_level=models.CharField('ColorLevel', null=True, blank=True, max_length=30)
    old_tax_price=models.DecimalField('TaxPrice', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=10, decimal_places=2)
    old_stuff_ratio1=models.DecimalField('StuffRatio1', null=True, blank=True, max_digits=10, decimal_places=2)
    old_stuff_ratio2=models.DecimalField('StuffRatio2', null=True, blank=True, max_digits=10, decimal_places=2)
    old_formula_cost1=models.DecimalField('FormulaCost1', null=True, blank=True, max_digits=10, decimal_places=2)
    old_formula_cost2=models.DecimalField('FormulaCost2', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_weight1=models.DecimalField('Weight1', null=True, blank=True, max_digits=10, decimal_places=2)
    old_weight2=models.DecimalField('Weight2', null=True, blank=True, max_digits=10, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_fixedcanrecord'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no', 'old_roll_no'],name='src_c4c2bed9f5ffffb4')]
        verbose_name=verbose_name_plural='其他或待确认相关表（FixedCanRecord，待确认）'
        ordering=["-id"]

class SourceDyeGetJobSheetReceive(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GetJobSheetReceive'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'JobSheetNo': 'old_job_sheet_no', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'ColorE': 'old_color_e', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'CustColorNum': 'old_cust_color_num', 'CustSelfNo': 'old_cust_self_no', 'CustSelfProduct': 'old_cust_self_product', 'Rolls': 'old_rolls', 'LengthQty': 'old_length_qty', 'DeptID': 'old_dept_id', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Remarks': 'old_remarks', 'WeightQty': 'old_weight_qty', 'Width': 'old_width', 'Weight': 'old_weight', 'ProgramItem': 'old_program_item', 'dyeDescription': 'old_dye_description', 'SheetType': 'old_sheet_type', 'BusinessUnitID': 'old_business_unit_id', 'CombineSheetNos': 'old_combine_sheet_nos', 'MachineNo': 'old_machine_no', 'ColorMatching': 'old_color_matching', 'Days': 'old_days', 'ShiftID': 'old_shift_id', 'Bigs': 'old_bigs', 'AddVat': 'old_add_vat', 'RTVat': 'old_rtvat', 'PassVat': 'old_pass_vat'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=36)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('客户编码', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=200)
    old_color_e=models.CharField('颜色英文名', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=200)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=100)
    old_cust_color_num=models.CharField('客户色号', null=True, blank=True, max_length=200)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=500)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=200)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_length_qty=models.DecimalField('长度', null=True, blank=True, max_digits=10, decimal_places=2)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=10)
    old_creater=models.CharField('登记人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('登记时间', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_weight_qty=models.DecimalField('重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_width=models.CharField('幅宽', null=True, blank=True, max_length=200)
    old_weight=models.CharField('克重', null=True, blank=True, max_length=200)
    old_program_item=models.CharField('单双染', null=True, blank=True, max_length=500)
    old_dye_description=models.CharField('是否首缸', null=True, blank=True, max_length=200)
    old_sheet_type=models.CharField('SheetType', null=True, blank=True, max_length=20)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=50)
    old_combine_sheet_nos=models.TextField('合缸缸号', null=True, blank=True)
    old_machine_no=models.CharField('机台', null=True, blank=True, max_length=50)
    old_color_matching=models.CharField('对色员', null=True, blank=True, max_length=50)
    old_days=models.CharField('日期', null=True, blank=True, max_length=10)
    old_shift_id=models.CharField('班别', null=True, blank=True, max_length=50)
    old_bigs=models.FloatField('Bigs', null=True, blank=True)
    old_add_vat=models.IntegerField('AddVat', null=True, blank=True)
    old_rtvat=models.FloatField('RTVat', null=True, blank=True)
    old_pass_vat=models.FloatField('PassVat', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_getjobsheetreceive'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_56a93205069693e2')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（GetJobSheetReceive，待确认）'
        ordering=["-id"]

class SourceDyeGWName(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='GWName'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'StepNo': 'old_step_no', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Keeper': 'old_keeper', 'Reason': 'old_reason', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'FabricKindID': 'old_fabric_kind_id', 'GWName': 'old_gwname', 'MinQty': 'old_min_qty', 'MaxQty': 'old_max_qty'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_keeper=models.CharField('Keeper', null=True, blank=True, max_length=10)
    old_reason=models.CharField('Reason', null=True, blank=True, max_length=256)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_fabric_kind_id=models.CharField('FabricKindID', null=True, blank=True, max_length=20)
    old_gwname=models.CharField('GWName', null=True, blank=True, max_length=20)
    old_min_qty=models.DecimalField('MinQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_max_qty=models.DecimalField('MaxQty', null=True, blank=True, max_digits=10, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_gwname'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_21ea5bfe9bcc38fa')]
        verbose_name=verbose_name_plural='其他或待确认相关表（GWName，待确认）'
        ordering=["-id"]

class SourceDyeHContract(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='h_Contract'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'Type': 'old_type', 'PartyA': 'old_party_a', 'PartyB': 'old_party_b', 'EmpID': 'old_emp_id', 'ContractNo': 'old_contract_no', 'MainMemo': 'old_main_memo', 'SignedDate': 'old_signed_date', 'StartDate': 'old_start_date', 'EndDate': 'old_end_date', 'IsCanAbort': 'old_is_can_abort', 'StopDate': 'old_stop_date', 'CycleType': 'old_cycle_type', 'Remarks': 'old_remarks', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_type=models.CharField('合同类别', null=True, blank=True, max_length=50)
    old_party_a=models.CharField('甲方', null=True, blank=True, max_length=100)
    old_party_b=models.CharField('乙方', null=True, blank=True, max_length=100)
    old_emp_id=models.CharField('员工编号', null=True, blank=True, max_length=10)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=20)
    old_main_memo=models.CharField('主要说明', null=True, blank=True, max_length=300)
    old_signed_date=models.DateTimeField('签订日期', null=True, blank=True)
    old_start_date=models.DateTimeField('生效日期', null=True, blank=True)
    old_end_date=models.DateTimeField('到期日期', null=True, blank=True)
    old_is_can_abort=models.BooleanField('能否中止', null=True, blank=True)
    old_stop_date=models.DateTimeField('中止日期', null=True, blank=True)
    old_cycle_type=models.CharField('合同中止类别', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_h_contract'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_6ded355422b9dfd4')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（h_Contract，待确认）'
        ordering=["-id"]

class SourceDyeHEmpAppNotice(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='h_EmpAppNotice'
    SOURCE_FIELDS={'EmpId': 'old_emp_id', 'ClientId': 'old_client_id', 'CreateTime': 'old_create_time', 'UpdateTime': 'old_update_time', 'UpdateEmpId': 'old_update_emp_id', 'IsDeleted': 'old_is_deleted'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_emp_id=models.CharField('员工id', null=False, blank=True, max_length=20)
    old_client_id=models.CharField('绑定app推送的clientid', null=False, blank=True, max_length=50)
    old_create_time=models.DateTimeField('创建时间', null=False, blank=False)
    old_update_time=models.DateTimeField('更新时间', null=True, blank=True)
    old_update_emp_id=models.CharField('更新员工id', null=True, blank=True, max_length=20)
    old_is_deleted=models.BooleanField('是否删除', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_h_empappnotice'
        indexes=[]
        verbose_name=verbose_name_plural='基础主数据相关表（h_EmpAppNotice，待确认）'
        ordering=["-id"]

class SourceDyeHEmpDeptPerm(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='h_EmpDeptPerm'
    SOURCE_FIELDS={'EmpID': 'old_emp_id', 'DeptKindID': 'old_dept_kind_id', 'PermValue': 'old_perm_value', 'Description': 'old_description'}
    SOURCE_KEY=('EmpID', 'DeptKindID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_emp_id=models.CharField('EmpID', null=False, blank=True, max_length=50)
    old_dept_kind_id=models.CharField('DeptKindID', null=False, blank=True, max_length=10)
    old_perm_value=models.CharField('PermValue', null=True, blank=True, max_length=100)
    old_description=models.CharField('Description', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_h_empdeptperm'
        indexes=[models.Index(fields=['source_batch', 'old_emp_id', 'old_dept_kind_id'],name='src_7ed675d8c5ec92d9')]
        verbose_name=verbose_name_plural='基础主数据相关表（h_EmpDeptPerm，待确认）'
        ordering=["-id"]

class SourceDyeHEmployee(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='h_Employee'
    SOURCE_FIELDS={'EmpID': 'old_emp_id', 'Password': 'old_password', 'Name': 'old_name', 'NameE': 'old_name_e', 'LoginName': 'old_login_name', 'InDate': 'old_in_date', 'ProbationDate': 'old_probation_date', 'OutDate': 'old_out_date', 'OutReason': 'old_out_reason', 'Sex': 'old_sex', 'IdentityNo': 'old_identity_no', 'HomeAddr': 'old_home_addr', 'HomeTel': 'old_home_tel', 'MaritalStatus': 'old_marital_status', 'OfficeTel': 'old_office_tel', 'Extension': 'old_extension', 'Mobile': 'old_mobile', 'QQ': 'old_qq', 'EducationID': 'old_education_id', 'DeptID': 'old_dept_id', 'Photo': 'old_photo', 'IsOut': 'old_is_out', 'Email': 'old_email', 'Birthday': 'old_birthday', 'PosDate': 'old_pos_date', 'PosID': 'old_pos_id', 'NativeID': 'old_native_id', 'HumanID': 'old_human_id', 'InsuranceID': 'old_insurance_id', 'InsuranceNo': 'old_insurance_no', 'StopDate': 'old_stop_date', 'EmpKind': 'old_emp_kind', 'JobKindID': 'old_job_kind_id', 'LoginStatus': 'old_login_status', 'Description': 'old_description', 'Remarks': 'old_remarks', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'NumValue1': 'old_num_value1', 'NumValue2': 'old_num_value2', 'LoginIPAddress': 'old_login_ipaddress', 'LoginNetPort': 'old_login_net_port', 'SecuritySNID': 'old_security_snid', 'IsReceiveMessage': 'old_is_receive_message', 'ChargStationID': 'old_charg_station_id', 'IsCanSendSMS': 'old_is_can_send_sms', 'FuncNo': 'old_func_no', 'IntroducerDept': 'old_introducer_dept', 'IntroducerPos': 'old_introducer_pos', 'Introducer': 'old_introducer', 'BusinessUnitID': 'old_business_unit_id', 'ShiftNameID': 'old_shift_name_id', 'IntroducerRelation': 'old_introducer_relation', 'TransferDate': 'old_transfer_date', 'TransferOutDept': 'old_transfer_out_dept', 'TransferInDept': 'old_transfer_in_dept', 'BeforeTransferPos': 'old_before_transfer_pos', 'IsSign': 'old_is_sign', 'SignDate': 'old_sign_date', 'SignNo': 'old_sign_no', 'IsInsurance': 'old_is_insurance', 'InsuranceDate': 'old_insurance_date', 'ShiftID': 'old_shift_id', 'RFID': 'old_rfid', 'BankAccount': 'old_bank_account', 'BankName': 'old_bank_name', 'fBasicSalary': 'old_f_basic_salary', 'BasicSalary': 'old_basic_salary', 'shiyongqi': 'old_shiyongqi', 'shiyonggongzi': 'old_shiyonggongzi', 'jibingshi': 'old_jibingshi', 'sushe': 'old_sushe', 'zhengshu': 'old_zhengshu', 'CurrAddr': 'old_curr_addr', 'sEmpID': 'old_s_emp_id', 'hetongnum': 'old_hetongnum', 'tijiannum': 'old_tijiannum', 'Emergencycontact': 'old_emergencycontact', 'EmergencycontactPhone': 'old_emergencycontact_phone', 'sNational': 'old_s_national', 'ExpiryDate': 'old_expiry_date', 'GinsengProtectDate': 'old_ginseng_protect_date', 'GinsengProtectType': 'old_ginseng_protect_type', 'GinsengProtectSum': 'old_ginseng_protect_sum', 'DDEmpId': 'old_ddemp_id', 'WeXinId': 'old_we_xin_id', 'RoomNo': 'old_room_no', 'Ratio': 'old_ratio', 'IsNotKQ': 'old_is_not_kq', 'PwdUsefulLife': 'old_pwd_useful_life', 'PwdExDate': 'old_pwd_ex_date', 'IsCustomer': 'old_is_customer', 'CustomerID': 'old_customer_id', 'MFLevel': 'old_mflevel', 'MFGiveOut': 'old_mfgive_out', 'EmpGroup': 'old_emp_group'}
    SOURCE_KEY=('EmpID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_mflevel': ('literal', 0), 'old_mfgive_out': ('literal', 0)}
    SOURCE_IDENTITIES=()
    old_emp_id=models.CharField('员工编码', null=False, blank=True, max_length=50)
    old_password=models.CharField('密码', null=True, blank=True, max_length=50)
    old_name=models.CharField('名称', null=True, blank=True, max_length=60)
    old_name_e=models.CharField('英文名', null=True, blank=True, max_length=128)
    old_login_name=models.CharField('登录名', null=True, blank=True, max_length=20)
    old_in_date=models.DateTimeField('进厂日期', null=True, blank=True)
    old_probation_date=models.DateTimeField('试用结束日期', null=True, blank=True)
    old_out_date=models.DateTimeField('离职日期', null=True, blank=True)
    old_out_reason=models.CharField('离职原因', null=True, blank=True, max_length=50)
    old_sex=models.CharField('性别', null=True, blank=True, max_length=6)
    old_identity_no=models.CharField('身份证号', null=True, blank=True, max_length=20)
    old_home_addr=models.CharField('家庭地址', null=True, blank=True, max_length=100)
    old_home_tel=models.CharField('家庭电话', null=True, blank=True, max_length=15)
    old_marital_status=models.CharField('婚姻状况', null=True, blank=True, max_length=16)
    old_office_tel=models.CharField('办公电话', null=True, blank=True, max_length=16)
    old_extension=models.CharField('分机号码', null=True, blank=True, max_length=15)
    old_mobile=models.CharField('移动电话', null=True, blank=True, max_length=15)
    old_qq=models.CharField('QQ号', null=True, blank=True, max_length=20)
    old_education_id=models.CharField('教育程度', null=True, blank=True, max_length=10)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=10)
    old_photo=models.BinaryField('照片', null=True, blank=True, editable=True)
    old_is_out=models.BooleanField('是否离职', null=True, blank=True)
    old_email=models.CharField('EMAIL', null=True, blank=True, max_length=60)
    old_birthday=models.DateTimeField('出生日期', null=True, blank=True)
    old_pos_date=models.DateTimeField('入职日期', null=True, blank=True)
    old_pos_id=models.CharField('职位代码', null=True, blank=True, max_length=10)
    old_native_id=models.CharField('籍贯', null=True, blank=True, max_length=10)
    old_human_id=models.CharField('户籍', null=True, blank=True, max_length=10)
    old_insurance_id=models.CharField('保险种类', null=True, blank=True, max_length=10)
    old_insurance_no=models.CharField('保险编号', null=True, blank=True, max_length=30)
    old_stop_date=models.DateTimeField('停用时间', null=True, blank=True)
    old_emp_kind=models.CharField('员工类别', null=True, blank=True, max_length=50)
    old_job_kind_id=models.CharField('工种类别', null=True, blank=True, max_length=10)
    old_login_status=models.BooleanField('登陆状态', null=True, blank=True)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_num_value1=models.DecimalField('数值1', null=True, blank=True, max_digits=10, decimal_places=2)
    old_num_value2=models.DecimalField('数值2', null=True, blank=True, max_digits=10, decimal_places=2)
    old_login_ipaddress=models.CharField('登陆IP', null=True, blank=True, max_length=25)
    old_login_net_port=models.CharField('LoginNetPort', null=True, blank=True, max_length=50)
    old_security_snid=models.CharField('安全序列号', null=True, blank=True, max_length=50)
    old_is_receive_message=models.BooleanField('IsReceiveMessage', null=True, blank=True)
    old_charg_station_id=models.CharField('ChargStationID', null=True, blank=True, max_length=50)
    old_is_can_send_sms=models.BooleanField('是否能发消息', null=True, blank=True)
    old_func_no=models.CharField('常规操作功能号', null=True, blank=True, max_length=6)
    old_introducer_dept=models.CharField('IntroducerDept', null=True, blank=True, max_length=20)
    old_introducer_pos=models.CharField('IntroducerPos', null=True, blank=True, max_length=20)
    old_introducer=models.CharField('介绍人', null=True, blank=True, max_length=20)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=50)
    old_shift_name_id=models.CharField('班别', null=True, blank=True, max_length=16)
    old_introducer_relation=models.CharField('IntroducerRelation', null=True, blank=True, max_length=50)
    old_transfer_date=models.DateTimeField('TransferDate', null=True, blank=True)
    old_transfer_out_dept=models.CharField('TransferOutDept', null=True, blank=True, max_length=20)
    old_transfer_in_dept=models.CharField('TransferInDept', null=True, blank=True, max_length=20)
    old_before_transfer_pos=models.CharField('BeforeTransferPos', null=True, blank=True, max_length=20)
    old_is_sign=models.BooleanField('IsSign', null=True, blank=True)
    old_sign_date=models.DateTimeField('SignDate', null=True, blank=True)
    old_sign_no=models.CharField('SignNo', null=True, blank=True, max_length=50)
    old_is_insurance=models.BooleanField('IsInsurance', null=True, blank=True)
    old_insurance_date=models.DateTimeField('InsuranceDate', null=True, blank=True)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=50)
    old_rfid=models.CharField('IC卡号', null=True, blank=True, max_length=64)
    old_bank_account=models.CharField('BankAccount', null=True, blank=True, max_length=50)
    old_bank_name=models.CharField('BankName', null=True, blank=True, max_length=20)
    old_f_basic_salary=models.DecimalField('fBasicSalary', null=True, blank=True, max_digits=8, decimal_places=2)
    old_basic_salary=models.CharField('BasicSalary', null=True, blank=True, max_length=30)
    old_shiyongqi=models.IntegerField('shiyongqi', null=True, blank=True)
    old_shiyonggongzi=models.IntegerField('shiyonggongzi', null=True, blank=True)
    old_jibingshi=models.CharField('jibingshi', null=True, blank=True, max_length=20)
    old_sushe=models.CharField('sushe', null=True, blank=True, max_length=20)
    old_zhengshu=models.CharField('zhengshu', null=True, blank=True, max_length=20)
    old_curr_addr=models.CharField('主前住址', null=True, blank=True, max_length=100)
    old_s_emp_id=models.CharField('sEmpID', null=True, blank=True, max_length=10)
    old_hetongnum=models.CharField('hetongnum', null=True, blank=True, max_length=30)
    old_tijiannum=models.CharField('tijiannum', null=True, blank=True, max_length=30)
    old_emergencycontact=models.CharField('Emergencycontact', null=True, blank=True, max_length=20)
    old_emergencycontact_phone=models.CharField('EmergencycontactPhone', null=True, blank=True, max_length=30)
    old_s_national=models.CharField('sNational', null=True, blank=True, max_length=20)
    old_expiry_date=models.DateTimeField('ExpiryDate', null=True, blank=True)
    old_ginseng_protect_date=models.DateTimeField('GinsengProtectDate', null=True, blank=True)
    old_ginseng_protect_type=models.CharField('GinsengProtectType', null=True, blank=True, max_length=50)
    old_ginseng_protect_sum=models.DecimalField('GinsengProtectSum', null=True, blank=True, max_digits=10, decimal_places=2)
    old_ddemp_id=models.CharField('DDEmpId', null=True, blank=True, max_length=50)
    old_we_xin_id=models.CharField('WeXinId', null=True, blank=True, max_length=50)
    old_room_no=models.CharField('宿舍号', null=True, blank=True, max_length=50)
    old_ratio=models.FloatField('工资系数', null=True, blank=True)
    old_is_not_kq=models.BooleanField('IsNotKQ', null=True, blank=True)
    old_pwd_useful_life=models.IntegerField('PwdUsefulLife', null=True, blank=True)
    old_pwd_ex_date=models.DateField('PwdExDate', null=True, blank=True)
    old_is_customer=models.BooleanField('IsCustomer', null=True, blank=True)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=32)
    old_mflevel=models.IntegerField('报修权限', null=True, blank=True)
    old_mfgive_out=models.BooleanField('报修指派', null=True, blank=True)
    old_emp_group=models.CharField('维修分组', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_h_employee'
        indexes=[models.Index(fields=['source_batch', 'old_emp_id'],name='src_d0c32c143be23c08')]
        verbose_name=verbose_name_plural='员工'
        ordering=["-id"]

class SourceDyeHEmployee2(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='h_Employee2'
    SOURCE_FIELDS={'EmpID': 'old_emp_id', 'Password': 'old_password', 'Name': 'old_name', 'NameE': 'old_name_e', 'LoginName': 'old_login_name', 'InDate': 'old_in_date', 'OutDate': 'old_out_date', 'Sex': 'old_sex', 'IdentityNo': 'old_identity_no', 'HomeAddr': 'old_home_addr', 'CurrAddr': 'old_curr_addr', 'OfficeTel': 'old_office_tel', 'Extension': 'old_extension', 'Mobile': 'old_mobile', 'HomeTel': 'old_home_tel', 'EducationID': 'old_education_id', 'DeptID': 'old_dept_id', 'Remarks': 'old_remarks', 'IsOut': 'old_is_out', 'Email': 'old_email', 'ReviseTimes': 'old_revise_times', 'Birthday': 'old_birthday', 'FromDate': 'old_from_date', 'PosID': 'old_pos_id', 'NativeID': 'old_native_id', 'HumanID': 'old_human_id', 'InsuranceID': 'old_insurance_id', 'InsuranceNo': 'old_insurance_no', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'EmpKind': 'old_emp_kind'}
    SOURCE_KEY=('EmpID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_emp_id=models.CharField('EmpID', null=False, blank=True, max_length=56)
    old_password=models.CharField('Password', null=True, blank=True, max_length=15)
    old_name=models.CharField('Name', null=True, blank=True, max_length=56)
    old_name_e=models.CharField('NameE', null=True, blank=True, max_length=56)
    old_login_name=models.CharField('LoginName', null=True, blank=True, max_length=20)
    old_in_date=models.DateTimeField('InDate', null=True, blank=True)
    old_out_date=models.DateTimeField('OutDate', null=True, blank=True)
    old_sex=models.CharField('Sex', null=True, blank=True, max_length=1)
    old_identity_no=models.CharField('IdentityNo', null=True, blank=True, max_length=20)
    old_home_addr=models.CharField('HomeAddr', null=True, blank=True, max_length=128)
    old_curr_addr=models.CharField('CurrAddr', null=True, blank=True, max_length=40)
    old_office_tel=models.CharField('OfficeTel', null=True, blank=True, max_length=30)
    old_extension=models.CharField('Extension', null=True, blank=True, max_length=15)
    old_mobile=models.CharField('Mobile', null=True, blank=True, max_length=15)
    old_home_tel=models.CharField('HomeTel', null=True, blank=True, max_length=15)
    old_education_id=models.CharField('EducationID', null=True, blank=True, max_length=4)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=4)
    old_remarks=models.BinaryField('Remarks', null=True, blank=True, editable=True)
    old_is_out=models.CharField('IsOut', null=True, blank=True, max_length=1)
    old_email=models.CharField('Email', null=True, blank=True, max_length=60)
    old_revise_times=models.DecimalField('ReviseTimes', null=True, blank=True, max_digits=2, decimal_places=0)
    old_birthday=models.DateTimeField('Birthday', null=True, blank=True)
    old_from_date=models.DateTimeField('FromDate', null=True, blank=True)
    old_pos_id=models.CharField('PosID', null=True, blank=True, max_length=10)
    old_native_id=models.CharField('NativeID', null=True, blank=True, max_length=16)
    old_human_id=models.CharField('HumanID', null=True, blank=True, max_length=2)
    old_insurance_id=models.CharField('InsuranceID', null=True, blank=True, max_length=4)
    old_insurance_no=models.CharField('InsuranceNo', null=True, blank=True, max_length=30)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=20)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=20)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_emp_kind=models.CharField('EmpKind', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_h_employee2'
        indexes=[models.Index(fields=['source_batch', 'old_emp_id'],name='src_cf45235fa6452804')]
        verbose_name=verbose_name_plural='基础主数据相关表（h_Employee2，待确认）'
        ordering=["-id"]

class SourceDyeHEmployeeIORecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='h_EmployeeIORecord'
    SOURCE_FIELDS={'ID': 'old_id', 'EmpID': 'old_emp_id', 'Name': 'old_name', 'InDate': 'old_in_date', 'OutDate': 'old_out_date', 'Creater': 'old_creater', 'CreateDate': 'old_create_date'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：h_Employee', 'target': 'erp_base.SourceDyeHEmployee', 'source_fields': ['EmpID'], 'target_fields': ['EmpID'], 'evidence': ['原界面主从 h_EmployeeIORecord → h_EmployeeEdit']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.CharField('序号', null=False, blank=True, max_length=50)
    old_emp_id=models.CharField('员工编号', null=True, blank=True, max_length=10)
    old_name=models.CharField('名称', null=True, blank=True, max_length=60)
    old_in_date=models.DateTimeField('进厂日期', null=True, blank=True)
    old_out_date=models.DateTimeField('出库日期', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_base.SourceDyeHEmployee', verbose_name='原关系：h_Employee', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_h_employeeiorecord'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_b40ae9de0dfe7900')]
        verbose_name=verbose_name_plural='基础主数据相关表（h_EmployeeIORecord，待确认）'
        ordering=["-id"]

class SourceDyeHEmpRole(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='h_EmpRole'
    SOURCE_FIELDS={'EmpID': 'old_emp_id', 'RoleNo': 'old_role_no', 'IsSuper': 'old_is_super'}
    SOURCE_KEY=('EmpID', 'RoleNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_emp_id=models.CharField('员工编号', null=False, blank=True, max_length=50)
    old_role_no=models.CharField('角色编号', null=False, blank=True, max_length=10)
    old_is_super=models.BooleanField('是否超级用户', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_h_emprole'
        indexes=[models.Index(fields=['source_batch', 'old_emp_id', 'old_role_no'],name='src_16ac768e0b123fa1')]
        verbose_name=verbose_name_plural='员工角色'
        ordering=["-id"]

class SourceDyeHLeave(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='h_Leave'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'EmpID': 'old_emp_id', 'PostID': 'old_post_id', 'DeptID': 'old_dept_id', 'MachineID': 'old_machine_id', 'BeginDate': 'old_begin_date', 'EndDate': 'old_end_date', 'DaysOffSet': 'old_days_off_set', 'Atte': 'old_atte', 'AtteValue': 'old_atte_value', 'Adjuster': 'old_adjuster', 'PrintTimes': 'old_print_times', 'RightStatus': 'old_right_status', 'SheetStatus': 'old_sheet_status', 'Remarks': 'old_remarks', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('请假类型', null=True, blank=True)
    old_emp_id=models.CharField('员工编号', null=True, blank=True, max_length=10)
    old_post_id=models.CharField('岗位编码', null=True, blank=True, max_length=10)
    old_dept_id=models.CharField('部门编码', null=True, blank=True, max_length=10)
    old_machine_id=models.CharField('机台号', null=True, blank=True, max_length=10)
    old_begin_date=models.DateTimeField('开始时间', null=True, blank=True)
    old_end_date=models.DateTimeField('结束时间', null=True, blank=True)
    old_days_off_set=models.DecimalField('请假天数', null=True, blank=True, max_digits=6, decimal_places=2)
    old_atte=models.CharField('请假原因', null=True, blank=True, max_length=100)
    old_atte_value=models.CharField('其他说明', null=True, blank=True, max_length=50)
    old_adjuster=models.CharField('顶班人', null=True, blank=True, max_length=20)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_h_leave'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_594f4314be18f98b')]
        verbose_name=verbose_name_plural='基础主数据相关表（h_Leave，待确认）'
        ordering=["-id"]

class SourceDyeHPositionChange(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='h_PositionChange'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'EmpID': 'old_emp_id', 'Type': 'old_type', 'OriDeptID': 'old_ori_dept_id', 'DeptID': 'old_dept_id', 'OriPosID': 'old_ori_pos_id', 'PosID': 'old_pos_id', 'OriPost': 'old_ori_post', 'Post': 'old_post', 'AdjustTime': 'old_adjust_time', 'Remarks': 'old_remarks', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_emp_id=models.CharField('员工编号', null=True, blank=True, max_length=10)
    old_type=models.CharField('异动类别', null=True, blank=True, max_length=50)
    old_ori_dept_id=models.CharField('原部门编码', null=True, blank=True, max_length=10)
    old_dept_id=models.CharField('部门编码', null=True, blank=True, max_length=10)
    old_ori_pos_id=models.CharField('原职务编码', null=True, blank=True, max_length=10)
    old_pos_id=models.CharField('职务编码', null=True, blank=True, max_length=10)
    old_ori_post=models.CharField('原岗位', null=True, blank=True, max_length=60)
    old_post=models.CharField('岗位', null=True, blank=True, max_length=60)
    old_adjust_time=models.DateTimeField('调整时间', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_h_positionchange'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_3674854b2f17402c')]
        verbose_name=verbose_name_plural='基础主数据相关表（h_PositionChange，待确认）'
        ordering=["-id"]

class SourceDyeHRewardPunish(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='h_RewardPunish'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'EmpID': 'old_emp_id', 'Kind': 'old_kind', 'Atte': 'old_atte', 'AtteValue': 'old_atte_value', 'Remarks': 'old_remarks', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=20)
    old_emp_id=models.CharField('员工编号', null=True, blank=True, max_length=10)
    old_kind=models.CharField('类别', null=True, blank=True, max_length=1)
    old_atte=models.CharField('奖惩原因', null=True, blank=True, max_length=100)
    old_atte_value=models.CharField('奖惩内容', null=True, blank=True, max_length=50)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_h_rewardpunish'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_f56e888fba3a5612')]
        verbose_name=verbose_name_plural='基础主数据相关表（h_RewardPunish，待确认）'
        ordering=["-id"]

class SourceDyeHOLIDAYS(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='HOLIDAYS'
    SOURCE_FIELDS={'HOLIDAYID': 'old_holidayid', 'HOLIDAYNAME': 'old_holidayname', 'HOLIDAYYEAR': 'old_holidayyear', 'HOLIDAYMONTH': 'old_holidaymonth', 'HOLIDAYDAY': 'old_holidayday', 'STARTTIME': 'old_starttime', 'DURATION': 'old_duration', 'HOLIDAYTYPE': 'old_holidaytype', 'XINBIE': 'old_xinbie', 'MINZU': 'old_minzu', 'DeptID': 'old_dept_id', 'timezone': 'old_timezone'}
    SOURCE_KEY=('HOLIDAYID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_holidayday': ('literal', 1), 'old_dept_id': ('literal', 1), 'old_timezone': ('literal', 0)}
    SOURCE_IDENTITIES=('old_holidayid',)
    old_holidayid=models.IntegerField('HOLIDAYID', null=False, blank=False)
    old_holidayname=models.CharField('HOLIDAYNAME', null=True, blank=True, max_length=20)
    old_holidayyear=models.IntegerField('HOLIDAYYEAR', null=True, blank=True)
    old_holidaymonth=models.IntegerField('HOLIDAYMONTH', null=True, blank=True)
    old_holidayday=models.IntegerField('HOLIDAYDAY', null=True, blank=True)
    old_starttime=models.DateTimeField('STARTTIME', null=True, blank=True)
    old_duration=models.IntegerField('DURATION', null=True, blank=True)
    old_holidaytype=models.IntegerField('HOLIDAYTYPE', null=True, blank=True)
    old_xinbie=models.CharField('XINBIE', null=True, blank=True, max_length=4)
    old_minzu=models.CharField('MINZU', null=True, blank=True, max_length=50)
    old_dept_id=models.IntegerField('DeptID', null=True, blank=True)
    old_timezone=models.IntegerField('timezone', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_holidays'
        indexes=[models.Index(fields=['source_batch', 'old_holidayid'],name='src_74b5ee80061b8983')]
        verbose_name=verbose_name_plural='其他或待确认相关表（HOLIDAYS，待确认）'
        ordering=["-id"]

class SourceDyeHuman(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='Human'
    SOURCE_FIELDS={'ID': 'old_id', 'Name': 'old_name', 'DeptID': 'old_dept_id', 'DeptName': 'old_dept_name', 'FactID': 'old_fact_id', 'FactName': 'old_fact_name', 'FieldType': 'old_field_type'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.CharField('ID', null=True, blank=True, max_length=50)
    old_name=models.CharField('Name', null=True, blank=True, max_length=100)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=50)
    old_dept_name=models.CharField('DeptName', null=True, blank=True, max_length=50)
    old_fact_id=models.CharField('FactID', null=True, blank=True, max_length=50)
    old_fact_name=models.CharField('FactName', null=True, blank=True, max_length=100)
    old_field_type=models.CharField('FieldType', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_human'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（Human，待确认）'
        ordering=["-id"]

class SourceDyeITMANAGE(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ITMANAGE'
    SOURCE_FIELDS={'ID': 'old_id', 'FENCHANG': 'old_fenchang', 'BUMEN': 'old_bumen', 'NAME': 'old_name', 'LEIXING': 'old_leixing', 'CPU': 'old_cpu', 'NEICUN': 'old_neicun', 'YINGPAN': 'old_yingpan', 'MACADDRESS': 'old_macaddress', 'SYR': 'old_syr', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'IsStop': 'old_is_stop', 'StopDate': 'old_stop_date', 'BZ': 'old_bz', 'sjbm': 'old_sjbm'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.IntegerField('ID', null=False, blank=False)
    old_fenchang=models.CharField('所属分厂', null=True, blank=True, max_length=50)
    old_bumen=models.CharField('部门', null=True, blank=True, max_length=50)
    old_name=models.CharField('名称', null=True, blank=True, max_length=250)
    old_leixing=models.CharField('设备类型', null=True, blank=True, max_length=250)
    old_cpu=models.CharField('CPU', null=True, blank=True, max_length=250)
    old_neicun=models.CharField('内存规格', null=True, blank=True, max_length=250)
    old_yingpan=models.CharField('硬盘规格', null=True, blank=True, max_length=250)
    old_macaddress=models.CharField('MAC地址', null=True, blank=True, max_length=250)
    old_syr=models.CharField('使用人', null=True, blank=True, max_length=250)
    old_create_date=models.DateTimeField('领用日期', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=50)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=50)
    old_is_stop=models.BooleanField('是否注销', null=True, blank=True)
    old_stop_date=models.DateTimeField('注销日期', null=True, blank=True)
    old_bz=models.CharField('备注', null=True, blank=True, max_length=500)
    old_sjbm=models.CharField('上级部门', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_itmanage'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_12b5e2bf9f05f2cb')]
        verbose_name=verbose_name_plural='其他或待确认相关表（ITMANAGE，待确认）'
        ordering=["-id"]

class SourceDyeKindLimit(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='KindLimit'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'Kind': 'old_kind', 'MinLimit': 'old_min_limit', 'MaxLimit': 'old_max_limit', 'DeliveryDay': 'old_delivery_day', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'RightStatus': 'old_right_status', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=30)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=30)
    old_kind=models.IntegerField('Kind', null=True, blank=True)
    old_min_limit=models.DecimalField('MinLimit', null=True, blank=True, max_digits=12, decimal_places=2)
    old_max_limit=models.DecimalField('MaxLimit', null=True, blank=True, max_digits=12, decimal_places=2)
    old_delivery_day=models.IntegerField('DeliveryDay', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=200)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=30)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=30)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=30)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_kindlimit'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_ba35373af3fd30db')]
        verbose_name=verbose_name_plural='其他或待确认相关表（KindLimit，待确认）'
        ordering=["-id"]

class SourceDyeKQ(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='KQ'
    SOURCE_FIELDS={'ID': 'old_id', 'EmpID': 'old_emp_id', 'EmpCode': 'old_emp_code', 'dtDate': 'old_dt_date', 'ShiftID': 'old_shift_id', 'ShiftName': 'old_shift_name', 'InTime': 'old_in_time', 'OutTime': 'old_out_time', 'BeginTime': 'old_begin_time', 'EndTime': 'old_end_time', 'LateTime': 'old_late_time', 'BeforCount': 'old_befor_count', 'BeforTime': 'old_befor_time', 'WorkCount': 'old_work_count', 'WorkTime': 'old_work_time', 'NoWork': 'old_no_work', 'IsHoliday': 'old_is_holiday', 'LeaveTime': 'old_leave_time', 'IsLeave': 'old_is_leave', 'LateCount': 'old_late_count', 'DeptID': 'old_dept_id', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.CharField('ID', null=False, blank=True, max_length=50)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=20)
    old_emp_code=models.CharField('EmpCode', null=True, blank=True, max_length=20)
    old_dt_date=models.CharField('dtDate', null=True, blank=True, max_length=10)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=32)
    old_shift_name=models.CharField('ShiftName', null=True, blank=True, max_length=7)
    old_in_time=models.DateTimeField('InTime', null=True, blank=True)
    old_out_time=models.DateTimeField('OutTime', null=True, blank=True)
    old_begin_time=models.DateTimeField('BeginTime', null=True, blank=True)
    old_end_time=models.DateTimeField('EndTime', null=True, blank=True)
    old_late_time=models.IntegerField('LateTime', null=True, blank=True)
    old_befor_count=models.IntegerField('BeforCount', null=True, blank=True)
    old_befor_time=models.FloatField('BeforTime', null=True, blank=True)
    old_work_count=models.FloatField('WorkCount', null=True, blank=True)
    old_work_time=models.FloatField('WorkTime', null=True, blank=True)
    old_no_work=models.FloatField('NoWork', null=True, blank=True)
    old_is_holiday=models.IntegerField('IsHoliday', null=True, blank=True)
    old_leave_time=models.FloatField('LeaveTime', null=True, blank=True)
    old_is_leave=models.FloatField('IsLeave', null=True, blank=True)
    old_late_count=models.FloatField('LateCount', null=True, blank=True)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_kq'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_b12a25971e3a8dd1')]
        verbose_name=verbose_name_plural='其他或待确认相关表（KQ，待确认）'
        ordering=["-id"]

class SourceDyeKQQuery(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='KQ_Query'
    SOURCE_FIELDS={'ID': 'old_id', 'EmpID': 'old_emp_id', 'EmpCode': 'old_emp_code', 'dtDate': 'old_dt_date', 'DAYS': 'old_days', 'ShiftID': 'old_shift_id', 'ShiftName': 'old_shift_name', 'InTime': 'old_in_time', 'OutTime': 'old_out_time', 'BeginTime': 'old_begin_time', 'EndTime': 'old_end_time', 'LateTime': 'old_late_time', 'BeforCount': 'old_befor_count', 'BeforTime': 'old_befor_time', 'WorkCount': 'old_work_count', 'WorkTime': 'old_work_time', 'NoWork': 'old_no_work', 'IsHoliday': 'old_is_holiday', 'LeaveTime': 'old_leave_time', 'IsLeave': 'old_is_leave', 'LateCount': 'old_late_count', 'DeptID': 'old_dept_id', 'Remarks': 'old_remarks', 'STATUS': 'old_status'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.CharField('ID', null=False, blank=True, max_length=50)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=20)
    old_emp_code=models.CharField('EmpCode', null=True, blank=True, max_length=20)
    old_dt_date=models.CharField('dtDate', null=True, blank=True, max_length=10)
    old_days=models.CharField('DAYS', null=True, blank=True, max_length=10)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=32)
    old_shift_name=models.CharField('ShiftName', null=True, blank=True, max_length=7)
    old_in_time=models.DateTimeField('InTime', null=True, blank=True)
    old_out_time=models.DateTimeField('OutTime', null=True, blank=True)
    old_begin_time=models.DateTimeField('BeginTime', null=True, blank=True)
    old_end_time=models.DateTimeField('EndTime', null=True, blank=True)
    old_late_time=models.IntegerField('LateTime', null=True, blank=True)
    old_befor_count=models.IntegerField('BeforCount', null=True, blank=True)
    old_befor_time=models.FloatField('BeforTime', null=True, blank=True)
    old_work_count=models.FloatField('WorkCount', null=True, blank=True)
    old_work_time=models.FloatField('WorkTime', null=True, blank=True)
    old_no_work=models.FloatField('NoWork', null=True, blank=True)
    old_is_holiday=models.IntegerField('IsHoliday', null=True, blank=True)
    old_leave_time=models.FloatField('LeaveTime', null=True, blank=True)
    old_is_leave=models.FloatField('IsLeave', null=True, blank=True)
    old_late_count=models.FloatField('LateCount', null=True, blank=True)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=50)
    old_status=models.CharField('STATUS', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_kq_query'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_c8f7543236779afa')]
        verbose_name=verbose_name_plural='其他或待确认相关表（KQ_Query，待确认）'
        ordering=["-id"]

class SourceDyeLeaveClass(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='LeaveClass'
    SOURCE_FIELDS={'LeaveId': 'old_leave_id', 'LeaveName': 'old_leave_name', 'MinUnit': 'old_min_unit', 'Unit': 'old_unit', 'RemaindProc': 'old_remaind_proc', 'RemaindCount': 'old_remaind_count', 'ReportSymbol': 'old_report_symbol', 'Deduct': 'old_deduct', 'Color': 'old_color', 'Classify': 'old_classify'}
    SOURCE_KEY=('LeaveId',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_min_unit': ('literal', 1), 'old_unit': ('literal', 1), 'old_remaind_proc': ('literal', 1), 'old_remaind_count': ('literal', 1), 'old_report_symbol': ('literal', '-'), 'old_deduct': ('literal', 0), 'old_color': ('literal', 0), 'old_classify': ('literal', 0)}
    SOURCE_IDENTITIES=('old_leave_id',)
    old_leave_id=models.IntegerField('LeaveId', null=False, blank=False)
    old_leave_name=models.CharField('LeaveName', null=False, blank=True, max_length=20)
    old_min_unit=models.FloatField('MinUnit', null=False, blank=False)
    old_unit=models.IntegerField('Unit', null=False, blank=False)
    old_remaind_proc=models.IntegerField('RemaindProc', null=False, blank=False)
    old_remaind_count=models.IntegerField('RemaindCount', null=False, blank=False)
    old_report_symbol=models.CharField('ReportSymbol', null=False, blank=True, max_length=4)
    old_deduct=models.FloatField('Deduct', null=False, blank=False)
    old_color=models.IntegerField('Color', null=False, blank=False)
    old_classify=models.IntegerField('Classify', null=False, blank=False)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_leaveclass'
        indexes=[models.Index(fields=['source_batch', 'old_leave_id'],name='src_617d347118c7a9f5')]
        verbose_name=verbose_name_plural='其他或待确认相关表（LeaveClass，待确认）'
        ordering=["-id"]

class SourceDyeLeaveClass1(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='LeaveClass1'
    SOURCE_FIELDS={'LeaveId': 'old_leave_id', 'LeaveName': 'old_leave_name', 'MinUnit': 'old_min_unit', 'Unit': 'old_unit', 'RemaindProc': 'old_remaind_proc', 'RemaindCount': 'old_remaind_count', 'ReportSymbol': 'old_report_symbol', 'Deduct': 'old_deduct', 'LeaveType': 'old_leave_type', 'Color': 'old_color', 'Classify': 'old_classify', 'Calc': 'old_calc'}
    SOURCE_KEY=('LeaveId',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_min_unit': ('literal', 1), 'old_unit': ('literal', 0), 'old_remaind_proc': ('literal', 2), 'old_remaind_count': ('literal', 1), 'old_report_symbol': ('literal', '_'), 'old_deduct': ('literal', 0), 'old_leave_type': ('literal', 0), 'old_color': ('literal', 0), 'old_classify': ('literal', 0)}
    SOURCE_IDENTITIES=('old_leave_id',)
    old_leave_id=models.IntegerField('LeaveId', null=False, blank=False)
    old_leave_name=models.CharField('LeaveName', null=False, blank=True, max_length=20)
    old_min_unit=models.FloatField('MinUnit', null=False, blank=False)
    old_unit=models.IntegerField('Unit', null=False, blank=False)
    old_remaind_proc=models.IntegerField('RemaindProc', null=False, blank=False)
    old_remaind_count=models.IntegerField('RemaindCount', null=False, blank=False)
    old_report_symbol=models.CharField('ReportSymbol', null=False, blank=True, max_length=4)
    old_deduct=models.FloatField('Deduct', null=False, blank=False)
    old_leave_type=models.IntegerField('LeaveType', null=False, blank=False)
    old_color=models.IntegerField('Color', null=False, blank=False)
    old_classify=models.IntegerField('Classify', null=False, blank=False)
    old_calc=models.TextField('Calc', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_leaveclass1'
        indexes=[models.Index(fields=['source_batch', 'old_leave_id'],name='src_bf7d413c4b9c237b')]
        verbose_name=verbose_name_plural='其他或待确认相关表（LeaveClass1，待确认）'
        ordering=["-id"]

class SourceDyeLimit(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='Limit'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'Kind': 'old_kind', 'EmpID': 'old_emp_id', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'RightStatus': 'old_right_status', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=30)
    old_sheet_no=models.CharField('SheetNo', null=False, blank=True, max_length=30)
    old_kind=models.IntegerField('Kind', null=True, blank=True)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=30)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=200)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=30)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=30)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=30)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_limit'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_216cb25fe9d70832')]
        verbose_name=verbose_name_plural='其他或待确认相关表（Limit，待确认）'
        ordering=["-id"]

class SourceDyeLossBill(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='LossBill'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'BusinessUnitID': 'old_business_unit_id', 'SheetDate': 'old_sheet_date', 'OrderNo': 'old_order_no', 'ContractNo': 'old_contract_no', 'LossKindIDs': 'old_loss_kind_ids', 'PreProfit': 'old_pre_profit', 'LossMoney': 'old_loss_money', 'CustomerID': 'old_customer_id', 'SalerID': 'old_saler_id', 'SalerGroupID': 'old_saler_group_id', 'GrayFactID': 'old_gray_fact_id', 'JobFactID': 'old_job_fact_id', 'OtherID': 'old_other_id', 'CustIDea': 'old_cust_idea', 'DeptIdea': 'old_dept_idea', 'JobIdea': 'old_job_idea', 'GrayIdea': 'old_gray_idea', 'OtherIdea': 'old_other_idea', 'Description': 'old_description', 'PreGrayMoney': 'old_pre_gray_money', 'PreJobMoney': 'old_pre_job_money', 'PreCustMoney': 'old_pre_cust_money', 'PreDeptMoney': 'old_pre_dept_money', 'PreOtherMoney': 'old_pre_other_money', 'RealGrayMoney': 'old_real_gray_money', 'RealJobMoney': 'old_real_job_money', 'RealCustMoney': 'old_real_cust_money', 'RealDeptMoney': 'old_real_dept_money', 'RealOtherMoney': 'old_real_other_money', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'StepNo': 'old_step_no'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('单据流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('报损单号', null=True, blank=True, max_length=20)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=10)
    old_sheet_date=models.DateTimeField('报损日期', null=True, blank=True)
    old_order_no=models.CharField('订单号', null=True, blank=True, max_length=20)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=20)
    old_loss_kind_ids=models.CharField('报损事由', null=True, blank=True, max_length=100)
    old_pre_profit=models.DecimalField('预计毛利', null=True, blank=True, max_digits=10, decimal_places=2)
    old_loss_money=models.DecimalField('损失金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_customer_id=models.CharField('客户代码', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('业务员代码', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('业务组别', null=True, blank=True, max_length=10)
    old_gray_fact_id=models.CharField('纱厂代码', null=True, blank=True, max_length=10)
    old_job_fact_id=models.CharField('染厂代码', null=True, blank=True, max_length=10)
    old_other_id=models.CharField('其他方代码', null=True, blank=True, max_length=10)
    old_cust_idea=models.CharField('客户意见', null=True, blank=True, max_length=1000)
    old_dept_idea=models.CharField('部门意见', null=True, blank=True, max_length=1000)
    old_job_idea=models.CharField('染厂意见', null=True, blank=True, max_length=1000)
    old_gray_idea=models.CharField('纱厂意见', null=True, blank=True, max_length=1000)
    old_other_idea=models.CharField('其他方意见', null=True, blank=True, max_length=1000)
    old_description=models.CharField('总结意见', null=True, blank=True, max_length=100)
    old_pre_gray_money=models.DecimalField('纱厂应承担金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pre_job_money=models.DecimalField('染厂应承担金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pre_cust_money=models.DecimalField('客户应承担额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pre_dept_money=models.DecimalField('部门应承担额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pre_other_money=models.DecimalField('其他方应承担额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_gray_money=models.DecimalField('纱厂实际承担金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_job_money=models.DecimalField('染厂实际承担金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_cust_money=models.DecimalField('客户实际承担金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_dept_money=models.DecimalField('部门实际承担金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_real_other_money=models.DecimalField('其他方实际承担金额', null=True, blank=True, max_digits=10, decimal_places=2)
    old_sheet_status=models.IntegerField('单据状态', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_print_times=models.IntegerField('打印次数', null=True, blank=True)
    old_revisions=models.IntegerField('修改次数', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_step_no=models.IntegerField('工作流节点号', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_lossbill'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_8a87a579d1215906')]
        verbose_name=verbose_name_plural='其他或待确认相关表（LossBill，待确认）'
        ordering=["-id"]

class SourceDyeMaterialPriceAdjust(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='MaterialPriceAdjust'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'WareHouseID': 'old_ware_house_id', 'SheetStatus': 'old_sheet_status', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'BusinessUnitID': 'old_business_unit_id', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'InSheetSeries': 'old_in_sheet_series', 'InSheetNo': 'old_in_sheet_no'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_ware_house_id=models.CharField('WareHouseID', null=True, blank=True, max_length=10)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)
    old_in_sheet_series=models.CharField('InSheetSeries', null=True, blank=True, max_length=20)
    old_in_sheet_no=models.CharField('InSheetNo', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_materialpriceadjust'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_2b745764db85a361')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（MaterialPriceAdjust，待确认）'
        ordering=["-id"]

class SourceDyeMaterialPriceAdjustDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='MaterialPriceAdjustDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'SupplierID': 'old_supplier_id', 'ArticleID': 'old_article_id', 'StuffID': 'old_stuff_id', 'LastUnitPrice': 'old_last_unit_price', 'CurrentUnitPrice': 'old_current_unit_price', 'Remarks': 'old_remarks', 'InDetailNo': 'old_in_detail_no', 'InSheetSeries': 'old_in_sheet_series', 'ExecutionDate': 'old_execution_date'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=20)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=36)
    old_supplier_id=models.CharField('SupplierID', null=True, blank=True, max_length=36)
    old_article_id=models.CharField('ArticleID', null=True, blank=True, max_length=100)
    old_stuff_id=models.CharField('StuffID', null=True, blank=True, max_length=100)
    old_last_unit_price=models.DecimalField('LastUnitPrice', null=True, blank=True, max_digits=10, decimal_places=4)
    old_current_unit_price=models.DecimalField('CurrentUnitPrice', null=True, blank=True, max_digits=10, decimal_places=4)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_in_detail_no=models.CharField('InDetailNo', null=True, blank=True, max_length=36)
    old_in_sheet_series=models.CharField('InSheetSeries', null=True, blank=True, max_length=20)
    old_execution_date=models.DateTimeField('ExecutionDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_materialpriceadjustdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_bcd25959910e0e06')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（MaterialPriceAdjustDetail，待确认）'
        ordering=["-id"]

class SourceDyeNoLimit(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='NoLimit'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'Kind': 'old_kind', 'NoLimitAmount': 'old_no_limit_amount', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'RightStatus': 'old_right_status', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=30)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=30)
    old_kind=models.IntegerField('Kind', null=True, blank=True)
    old_no_limit_amount=models.DecimalField('NoLimitAmount', null=True, blank=True, max_digits=12, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=200)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=30)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=30)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=30)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_nolimit'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_be57c17e52eeb47a')]
        verbose_name=verbose_name_plural='其他或待确认相关表（NoLimit，待确认）'
        ordering=["-id"]

class SourceDyeNUMRUN(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='NUM_RUN'
    SOURCE_FIELDS={'NUM_RUNID': 'old_num_runid', 'OLDID': 'old_oldid', 'NAME': 'old_name', 'STARTDATE': 'old_startdate', 'ENDDATE': 'old_enddate', 'CYLE': 'old_cyle', 'UNITS': 'old_units'}
    SOURCE_KEY=('NUM_RUNID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_oldid': ('literal', -1), 'old_startdate': ('literal', '2000-1-1'), 'old_enddate': ('literal', '2099-12-31'), 'old_cyle': ('literal', 1), 'old_units': ('literal', 1)}
    SOURCE_IDENTITIES=('old_num_runid',)
    old_num_runid=models.IntegerField('NUM_RUNID', null=False, blank=False)
    old_oldid=models.IntegerField('OLDID', null=True, blank=True)
    old_name=models.CharField('NAME', null=False, blank=True, max_length=30)
    old_startdate=models.DateTimeField('STARTDATE', null=True, blank=True)
    old_enddate=models.DateTimeField('ENDDATE', null=True, blank=True)
    old_cyle=models.IntegerField('CYLE', null=True, blank=True)
    old_units=models.IntegerField('UNITS', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_num_run'
        indexes=[models.Index(fields=['source_batch', 'old_num_runid'],name='src_c41d992b50e1d6a8')]
        verbose_name=verbose_name_plural='其他或待确认相关表（NUM_RUN，待确认）'
        ordering=["-id"]

class SourceDyeNUMRUNDEIL(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='NUM_RUN_DEIL'
    SOURCE_FIELDS={'NUM_RUNID': 'old_num_runid', 'STARTTIME': 'old_starttime', 'ENDTIME': 'old_endtime', 'SDAYS': 'old_sdays', 'EDAYS': 'old_edays', 'SCHCLASSID': 'old_schclassid', 'OverTime': 'old_over_time'}
    SOURCE_KEY=('NUM_RUNID', 'SDAYS', 'STARTTIME')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_schclassid': ('literal', -1)}
    SOURCE_IDENTITIES=()
    old_num_runid=models.IntegerField('NUM_RUNID', null=False, blank=False)
    old_starttime=models.DateTimeField('STARTTIME', null=False, blank=False)
    old_endtime=models.DateTimeField('ENDTIME', null=True, blank=True)
    old_sdays=models.IntegerField('SDAYS', null=False, blank=False)
    old_edays=models.IntegerField('EDAYS', null=True, blank=True)
    old_schclassid=models.IntegerField('SCHCLASSID', null=True, blank=True)
    old_over_time=models.IntegerField('OverTime', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_num_run_deil'
        indexes=[models.Index(fields=['source_batch', 'old_num_runid', 'old_sdays', 'old_starttime'],name='src_197fac8f72092546')]
        verbose_name=verbose_name_plural='其他或待确认相关表（NUM_RUN_DEIL，待确认）'
        ordering=["-id"]

class SourceDyePArticle(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Article'
    SOURCE_FIELDS={'ArticleID': 'old_article_id', 'Name': 'old_name', 'Spec': 'old_spec', 'NameE': 'old_name_e', 'Mnemonic': 'old_mnemonic', 'ArticleKindID': 'old_article_kind_id', 'StorageUnitID': 'old_storage_unit_id', 'FactID': 'old_fact_id', 'Brand': 'old_brand', 'SupplierID': 'old_supplier_id', 'Unit': 'old_unit', 'Price': 'old_price', 'RemainQty': 'old_remain_qty', 'SafeQty': 'old_safe_qty', 'LimitDays': 'old_limit_days', 'LeadDays': 'old_lead_days', 'IsBatch': 'old_is_batch', 'AccSubjectID': 'old_acc_subject_id', 'Status': 'old_status', 'StopDate': 'old_stop_date', 'Remarks': 'old_remarks', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'LastPrice': 'old_last_price', 'RightStatus': 'old_right_status', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date'}
    SOURCE_KEY=('ArticleID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_article_id=models.CharField('机物料代码', null=False, blank=True, max_length=20)
    old_name=models.CharField('名称', null=True, blank=True, max_length=60)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_name_e=models.CharField('英文名称', null=True, blank=True, max_length=128)
    old_mnemonic=models.CharField('助记符', null=True, blank=True, max_length=10)
    old_article_kind_id=models.CharField('物料种类代码', null=True, blank=True, max_length=20)
    old_storage_unit_id=models.CharField('仓位代码', null=True, blank=True, max_length=10)
    old_fact_id=models.CharField('包装单位', null=True, blank=True, max_length=10)
    old_brand=models.CharField('牌号', null=True, blank=True, max_length=20)
    old_supplier_id=models.CharField('供应商代码', null=True, blank=True, max_length=10)
    old_unit=models.CharField('单位（计量、计价）', null=True, blank=True, max_length=20)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=18, decimal_places=6)
    old_remain_qty=models.DecimalField('剩余数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_safe_qty=models.DecimalField('安全库存', null=True, blank=True, max_digits=10, decimal_places=2)
    old_limit_days=models.IntegerField('收款期限', null=True, blank=True)
    old_lead_days=models.IntegerField('前置天数', null=True, blank=True)
    old_is_batch=models.BooleanField('批次管理', null=True, blank=True)
    old_acc_subject_id=models.CharField('财务科目代码', null=True, blank=True, max_length=10)
    old_status=models.IntegerField('状态', null=True, blank=True)
    old_stop_date=models.DateTimeField('停用时间', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_last_price=models.DecimalField('最新采购价', null=True, blank=True, max_digits=18, decimal_places=6)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_article'
        indexes=[models.Index(fields=['source_batch', 'old_article_id'],name='src_b090c1e4d6f9c984')]
        verbose_name=verbose_name_plural='基础主数据相关表（p_Article，待确认）'
        ordering=["-id"]

class SourceDyePArticleStorageUnitID(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_ArticleStorageUnitID'
    SOURCE_FIELDS={'FieldType': 'old_field_type', 'Code': 'old_code', 'Name': 'old_name'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_field_type=models.CharField('FieldType', null=True, blank=True, max_length=50)
    old_code=models.CharField('Code', null=True, blank=True, max_length=50)
    old_name=models.CharField('Name', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_articlestorageunitid'
        indexes=[]
        verbose_name=verbose_name_plural='辅料仓位对照'
        ordering=["-id"]

class SourceDyePAtteSub(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_AtteSub'
    SOURCE_FIELDS={'Code': 'old_code', 'SubCode': 'old_sub_code', 'SortValue': 'old_sort_value', 'Name': 'old_name', 'NumValue': 'old_num_value', 'IsDefault': 'old_is_default', 'Description': 'old_description', 'Price': 'old_price', 'PriceUnit': 'old_price_unit', 'GoWith': 'old_go_with', 'RequireFields': 'old_require_fields', 'RequireTypes': 'old_require_types', 'MutexTypes': 'old_mutex_types'}
    SOURCE_KEY=('Code', 'SubCode')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_code=models.CharField('Code', null=False, blank=True, max_length=20)
    old_sub_code=models.CharField('加工要求选项', null=False, blank=True, max_length=20)
    old_sort_value=models.IntegerField('排序值', null=False, blank=False)
    old_name=models.CharField('选项名称', null=True, blank=True, max_length=50)
    old_num_value=models.DecimalField('默认值', null=True, blank=True, max_digits=18, decimal_places=2)
    old_is_default=models.BooleanField('默认加载选项', null=True, blank=True)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=18, decimal_places=2)
    old_price_unit=models.IntegerField('PriceUnit', null=True, blank=True)
    old_go_with=models.CharField('关联选项，自动带出', null=True, blank=True, max_length=50)
    old_require_fields=models.CharField('必填检查字段', null=True, blank=True, max_length=50)
    old_require_types=models.CharField('关联必选的组', null=True, blank=True, max_length=50)
    old_mutex_types=models.CharField('与之互斥的选项组', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_attesub'
        indexes=[models.Index(fields=['source_batch', 'old_code', 'old_sub_code'],name='src_988c313c08b71394')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（p_AtteSub，待确认）'
        ordering=["-id"]

class SourceDyePAtteType(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_AtteType'
    SOURCE_FIELDS={'Code': 'old_code', 'Name': 'old_name', 'SortValue': 'old_sort_value', 'AtteKind': 'old_atte_kind', 'Description': 'old_description', 'IsStop': 'old_is_stop', 'StopDate': 'old_stop_date', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'BusinessUnitID': 'old_business_unit_id', 'IsMutex': 'old_is_mutex', 'RequireNum': 'old_require_num'}
    SOURCE_KEY=('Code',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_code=models.CharField('加工要求分组编码', null=False, blank=True, max_length=20)
    old_name=models.CharField('加工要求组名', null=True, blank=True, max_length=50)
    old_sort_value=models.IntegerField('排序值', null=True, blank=True)
    old_atte_kind=models.IntegerField('AtteKind', null=True, blank=True)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    old_is_stop=models.BooleanField('是否停用', null=True, blank=True)
    old_stop_date=models.DateTimeField('停用时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=20)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=20)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=10)
    old_is_mutex=models.BooleanField('组内互斥', null=True, blank=True)
    old_require_num=models.IntegerField('必选项数', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_attetype'
        indexes=[models.Index(fields=['source_batch', 'old_code'],name='src_8b3a0f5ebc8e032b')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（p_AtteType，待确认）'
        ordering=["-id"]

class SourceDyePAuxRule(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_AuxRule'
    SOURCE_FIELDS={'ID': 'old_id', 'ProdKindID': 'old_prod_kind_id', 'StuffKindID': 'old_stuff_kind_id', 'NumValue1': 'old_num_value1', 'NumValue2': 'old_num_value2', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.CharField('ID', null=False, blank=True, max_length=50)
    old_prod_kind_id=models.CharField('ProdKindID', null=True, blank=True, max_length=10)
    old_stuff_kind_id=models.CharField('StuffKindID', null=True, blank=True, max_length=10)
    old_num_value1=models.DecimalField('NumValue1', null=True, blank=True, max_digits=10, decimal_places=2)
    old_num_value2=models.DecimalField('NumValue2', null=True, blank=True, max_digits=10, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=300)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_auxrule'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_cfe0a2830c7e2fde')]
        verbose_name=verbose_name_plural='基础主数据相关表（p_AuxRule，待确认）'
        ordering=["-id"]

class SourceDyePAuxRuleDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_AuxRuleDetail'
    SOURCE_FIELDS={'ID': 'old_id', 'StuffID': 'old_stuff_id', 'Dosage': 'old_dosage', 'RecipeUnit': 'old_recipe_unit', 'CalcWay': 'old_calc_way', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('ID', 'StuffID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.CharField('ID', null=False, blank=True, max_length=50)
    old_stuff_id=models.CharField('StuffID', null=False, blank=True, max_length=10)
    old_dosage=models.DecimalField('Dosage', null=True, blank=True, max_digits=15, decimal_places=6)
    old_recipe_unit=models.IntegerField('RecipeUnit', null=True, blank=True)
    old_calc_way=models.CharField('CalcWay', null=True, blank=True, max_length=1)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=300)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_auxruledetail'
        indexes=[models.Index(fields=['source_batch', 'old_id', 'old_stuff_id'],name='src_c27a8e6df3194af7')]
        verbose_name=verbose_name_plural='基础主数据相关表（p_AuxRuleDetail，待确认）'
        ordering=["-id"]

class SourceDyePBalanceType(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_BalanceType'
    SOURCE_FIELDS={'F_ID': 'old_f_id', 'F_Name': 'old_f_name', 'F_PayMonth': 'old_f_pay_month', 'F_PayDay': 'old_f_pay_day', 'F_Remark': 'old_f_remark', 'F_Type': 'old_f_type', 'F_Date': 'old_f_date'}
    SOURCE_KEY=('F_ID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_f_id=models.CharField('F_ID', null=False, blank=True, max_length=30)
    old_f_name=models.CharField('F_Name', null=True, blank=True, max_length=60)
    old_f_pay_month=models.IntegerField('F_PayMonth', null=True, blank=True)
    old_f_pay_day=models.IntegerField('F_PayDay', null=True, blank=True)
    old_f_remark=models.CharField('F_Remark', null=True, blank=True, max_length=80)
    old_f_type=models.IntegerField('F_Type', null=True, blank=True)
    old_f_date=models.IntegerField('F_Date', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_balancetype'
        indexes=[models.Index(fields=['source_batch', 'old_f_id'],name='src_892a390128cd15f0')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（p_BalanceType，待确认）'
        ordering=["-id"]

class SourceDyePColorNum(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='P_ColorNum'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ColorNo': 'old_color_no', 'CheckNo': 'old_check_no', 'LabDipsSource': 'old_lab_dips_source', 'ProdID': 'old_prod_id', 'LotNo': 'old_lot_no', 'Spec': 'old_spec', 'ColorDepthID': 'old_color_depth_id', 'ColorID': 'old_color_id', 'ColorNum': 'old_color_num', 'ColorE': 'old_color_e', 'CustColorNum': 'old_cust_color_num', 'ColorRGB': 'old_color_rgb', 'Price': 'old_price', 'MainStuffKindID': 'old_main_stuff_kind_id', 'IsToDoSample': 'old_is_to_do_sample', 'ColorCards': 'old_color_cards', 'Status': 'old_status', 'StartTime': 'old_start_time', 'LimitHours': 'old_limit_hours', 'OverTimeReason': 'old_over_time_reason', 'ShiftID': 'old_shift_id', 'EmpID': 'old_emp_id', 'WorkQty': 'old_work_qty', 'RedoTimes': 'old_redo_times', 'OriColorNo': 'old_ori_color_no', 'OriEmpID': 'old_ori_emp_id', 'OriShifID': 'old_ori_shif_id', 'JobSheetNo': 'old_job_sheet_no', 'Remarks': 'old_remarks', 'Width': 'old_width', 'Weight': 'old_weight', 'CustSelfProduct': 'old_cust_self_product', 'ColorMark': 'old_color_mark', 'ColorNumMark': 'old_color_num_mark', 'R': 'old_r', 'G': 'old_g', 'B': 'old_b', 'RGB': 'old_rgb', 'CustomerID': 'old_customer_id', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'OKTime': 'old_oktime', 'EndTime': 'old_end_time', 'SalerID': 'old_saler_id', 'ColorNumNO': 'old_color_num_no', 'IsOrder': 'old_is_order', 'IsOrderTime': 'old_is_order_time', 'CusRemark': 'old_cus_remark', 'IsToSampleDaTe': 'old_is_to_sample_da_te', 'VerLight1ID': 'old_ver_light1_id', 'VerLight2ID': 'old_ver_light2_id', 'StuffDosage': 'old_stuff_dosage', 'DyePhaseName': 'old_dye_phase_name', 'GaoLaodu': 'old_gao_laodu', 'Note': 'old_note', 'Daipaidaban': 'old_daipaidaban', 'Duiseluogang': 'old_duiseluogang', 'Dabanpise': 'old_dabanpise', 'KindType': 'old_kind_type', 'IsDoubleDye': 'old_is_double_dye', 'GradeID': 'old_grade_id', 'CostQuote': 'old_cost_quote'}
    SOURCE_KEY=('ColorNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=True, blank=True, max_length=50)
    old_color_no=models.CharField('ColorNo', null=False, blank=True, max_length=50)
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=50)
    old_lab_dips_source=models.IntegerField('LabDipsSource', null=True, blank=True)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=500)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=1000)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=528)
    old_color_depth_id=models.CharField('ColorDepthID', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=100)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=50)
    old_color_e=models.CharField('ColorE', null=True, blank=True, max_length=50)
    old_cust_color_num=models.CharField('CustColorNum', null=True, blank=True, max_length=100)
    old_color_rgb=models.IntegerField('ColorRGB', null=True, blank=True)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_main_stuff_kind_id=models.CharField('MainStuffKindID', null=True, blank=True, max_length=10)
    old_is_to_do_sample=models.BooleanField('IsToDoSample', null=True, blank=True)
    old_color_cards=models.IntegerField('ColorCards', null=True, blank=True)
    old_status=models.CharField('Status', null=True, blank=True, max_length=2)
    old_start_time=models.CharField('StartTime', null=True, blank=True, max_length=14)
    old_limit_hours=models.DecimalField('LimitHours', null=True, blank=True, max_digits=5, decimal_places=2)
    old_over_time_reason=models.CharField('OverTimeReason', null=True, blank=True, max_length=20)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=10)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=50)
    old_work_qty=models.DecimalField('WorkQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_redo_times=models.IntegerField('RedoTimes', null=True, blank=True)
    old_ori_color_no=models.CharField('OriColorNo', null=True, blank=True, max_length=20)
    old_ori_emp_id=models.CharField('OriEmpID', null=True, blank=True, max_length=10)
    old_ori_shif_id=models.CharField('OriShifID', null=True, blank=True, max_length=10)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)
    old_width=models.DecimalField('Width', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight=models.DecimalField('Weight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cust_self_product=models.CharField('CustSelfProduct', null=True, blank=True, max_length=200)
    old_color_mark=models.CharField('ColorMark', null=True, blank=True, max_length=10)
    old_color_num_mark=models.CharField('ColorNumMark', null=True, blank=True, max_length=10)
    old_r=models.IntegerField('R', null=True, blank=True)
    old_g=models.IntegerField('G', null=True, blank=True)
    old_b=models.IntegerField('B', null=True, blank=True)
    old_rgb=models.IntegerField('RGB', null=True, blank=True)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=100)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=20)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=20)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_oktime=models.DateTimeField('OKTime', null=True, blank=True)
    old_end_time=models.DateTimeField('EndTime', null=True, blank=True)
    old_saler_id=models.CharField('SalerID', null=True, blank=True, max_length=50)
    old_color_num_no=models.CharField('ColorNumNO', null=True, blank=True, max_length=50)
    old_is_order=models.CharField('IsOrder', null=True, blank=True, max_length=10)
    old_is_order_time=models.DateTimeField('IsOrderTime', null=True, blank=True)
    old_cus_remark=models.CharField('CusRemark', null=True, blank=True, max_length=1000)
    old_is_to_sample_da_te=models.DateTimeField('IsToSampleDaTe', null=True, blank=True)
    old_ver_light1_id=models.CharField('VerLight1ID', null=True, blank=True, max_length=50)
    old_ver_light2_id=models.CharField('VerLight2ID', null=True, blank=True, max_length=50)
    old_stuff_dosage=models.DecimalField('StuffDosage', null=True, blank=True, max_digits=10, decimal_places=6)
    old_dye_phase_name=models.CharField('DyePhaseName', null=True, blank=True, max_length=100)
    old_gao_laodu=models.CharField('GaoLaodu', null=True, blank=True, max_length=100)
    old_note=models.CharField('Note', null=True, blank=True, max_length=1000)
    old_daipaidaban=models.CharField('Daipaidaban', null=True, blank=True, max_length=10)
    old_duiseluogang=models.CharField('Duiseluogang', null=True, blank=True, max_length=10)
    old_dabanpise=models.CharField('Dabanpise', null=True, blank=True, max_length=10)
    old_kind_type=models.CharField('KindType', null=True, blank=True, max_length=10)
    old_is_double_dye=models.IntegerField('IsDoubleDye', null=True, blank=True)
    old_grade_id=models.CharField('GradeID', null=True, blank=True, max_length=50)
    old_cost_quote=models.FloatField('CostQuote', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_colornum'
        indexes=[models.Index(fields=['source_batch', 'old_color_no'],name='src_80bf469147367902')]
        verbose_name=verbose_name_plural='色号与样品'
        ordering=["-id"]

class SourceDyePCommissionRatio(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_CommissionRatio'
    SOURCE_FIELDS={'BeginOutD': 'old_begin_out_d', 'EndOutD': 'old_end_out_d', 'BeginMoneyD': 'old_begin_money_d', 'EndMoneyD': 'old_end_money_d'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_begin_out_d=models.IntegerField('BeginOutD', null=True, blank=True)
    old_end_out_d=models.IntegerField('EndOutD', null=True, blank=True)
    old_begin_money_d=models.IntegerField('BeginMoneyD', null=True, blank=True)
    old_end_money_d=models.IntegerField('EndMoneyD', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_commissionratio'
        indexes=[]
        verbose_name=verbose_name_plural='基础主数据相关表（p_CommissionRatio，待确认）'
        ordering=["-id"]

class SourceDyePCommMethod(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_CommMethod'
    SOURCE_FIELDS={'MethodID': 'old_method_id', 'Interval': 'old_interval', 'SendFormat': 'old_send_format', 'ReceFormat': 'old_rece_format', 'Error_Check': 'old_error_check', 'Remarks': 'old_remarks', 'RespondFormat': 'old_respond_format', 'Name': 'old_name'}
    SOURCE_KEY=('MethodID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_method_id=models.CharField('通讯方法编码', null=False, blank=True, max_length=10)
    old_interval=models.IntegerField('发送间隔', null=True, blank=True)
    old_send_format=models.CharField('发送格式', null=True, blank=True, max_length=100)
    old_rece_format=models.CharField('接收格式', null=True, blank=True, max_length=200)
    old_error_check=models.CharField('校验方法', null=True, blank=True, max_length=5)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_respond_format=models.CharField('响应处理格式', null=True, blank=True, max_length=100)
    old_name=models.CharField('名称', null=True, blank=True, max_length=60)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_commmethod'
        indexes=[models.Index(fields=['source_batch', 'old_method_id'],name='src_0099630f0e8039d0')]
        verbose_name=verbose_name_plural='基础主数据相关表（p_CommMethod，待确认）'
        ordering=["-id"]

class SourceDyePCommModule(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_CommModule'
    SOURCE_FIELDS={'ModuleID': 'old_module_id', 'Name': 'old_name', 'Remarks': 'old_remarks', 'Channels': 'old_channels', 'RS485s': 'old_rs485s'}
    SOURCE_KEY=('ModuleID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_module_id=models.CharField('模块编号', null=False, blank=True, max_length=10)
    old_name=models.CharField('名称', null=True, blank=True, max_length=60)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_channels=models.IntegerField('通道数', null=True, blank=True)
    old_rs485s=models.IntegerField('RS485s', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_commmodule'
        indexes=[models.Index(fields=['source_batch', 'old_module_id'],name='src_9df2a87947f41fea')]
        verbose_name=verbose_name_plural='基础主数据相关表（p_CommModule，待确认）'
        ordering=["-id"]

class SourceDyePCommPort(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_CommPort'
    SOURCE_FIELDS={'PortID': 'old_port_id', 'IPAddress': 'old_ipaddress', 'PortNum': 'old_port_num', 'StopBits': 'old_stop_bits', 'DataBits': 'old_data_bits', 'Parity': 'old_parity', 'ReadInterval': 'old_read_interval', 'WriteInterval': 'old_write_interval', 'Kind': 'old_kind', 'ModuleType': 'old_module_type', 'BaudRate': 'old_baud_rate', 'TimeOutSecond': 'old_time_out_second', 'IsStop': 'old_is_stop'}
    SOURCE_KEY=('PortID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_port_id=models.CharField('PortID', null=False, blank=True, max_length=10)
    old_ipaddress=models.CharField('IP地址', null=False, blank=True, max_length=50)
    old_port_num=models.IntegerField('端(串)口号', null=False, blank=False)
    old_stop_bits=models.IntegerField('停止位', null=True, blank=True)
    old_data_bits=models.IntegerField('数据位', null=True, blank=True)
    old_parity=models.CharField('奇偶校验位', null=True, blank=True, max_length=15)
    old_read_interval=models.IntegerField('读时间间隔', null=True, blank=True)
    old_write_interval=models.IntegerField('写时间间隔', null=True, blank=True)
    old_kind=models.IntegerField('Kind', null=True, blank=True)
    old_module_type=models.IntegerField('ModuleType', null=True, blank=True)
    old_baud_rate=models.CharField('BaudRate', null=True, blank=True, max_length=10)
    old_time_out_second=models.IntegerField('TimeOutSecond', null=True, blank=True)
    old_is_stop=models.BooleanField('IsStop', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_commport'
        indexes=[models.Index(fields=['source_batch', 'old_port_id'],name='src_1875d2d2efb97f5a')]
        verbose_name=verbose_name_plural='基础主数据相关表（p_CommPort，待确认）'
        ordering=["-id"]

class SourceDyePCook(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Cook'
    SOURCE_FIELDS={'CookID': 'old_cook_id', 'Name': 'old_name', 'Spec': 'old_spec', 'NameE': 'old_name_e', 'Mnemonic': 'old_mnemonic', 'ArticleKindID': 'old_article_kind_id', 'StorageUnitID': 'old_storage_unit_id', 'FactID': 'old_fact_id', 'Brand': 'old_brand', 'SupplierID': 'old_supplier_id', 'Unit': 'old_unit', 'Price': 'old_price', 'RemainQty': 'old_remain_qty', 'SafeQty': 'old_safe_qty', 'LimitDays': 'old_limit_days', 'LeadDays': 'old_lead_days', 'IsBatch': 'old_is_batch', 'AccSubjectID': 'old_acc_subject_id', 'Status': 'old_status', 'StopDate': 'old_stop_date', 'Remarks': 'old_remarks', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'LastPrice': 'old_last_price'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_cook_id=models.CharField('编码', null=False, blank=True, max_length=20)
    old_name=models.CharField('名称', null=True, blank=True, max_length=60)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_name_e=models.CharField('英文名称', null=True, blank=True, max_length=128)
    old_mnemonic=models.CharField('助记符', null=True, blank=True, max_length=10)
    old_article_kind_id=models.CharField('ArticleKindID', null=True, blank=True, max_length=20)
    old_storage_unit_id=models.CharField('仓位代码', null=True, blank=True, max_length=10)
    old_fact_id=models.CharField('包装单位', null=True, blank=True, max_length=10)
    old_brand=models.CharField('牌号', null=True, blank=True, max_length=20)
    old_supplier_id=models.CharField('供应商代码', null=True, blank=True, max_length=10)
    old_unit=models.CharField('单位（计量、计价）', null=True, blank=True, max_length=20)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=18, decimal_places=6)
    old_remain_qty=models.DecimalField('剩余数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_safe_qty=models.DecimalField('安全库存', null=True, blank=True, max_digits=10, decimal_places=2)
    old_limit_days=models.IntegerField('收款期限', null=True, blank=True)
    old_lead_days=models.IntegerField('前置天数', null=True, blank=True)
    old_is_batch=models.BooleanField('批次管理', null=True, blank=True)
    old_acc_subject_id=models.CharField('财务科目代码', null=True, blank=True, max_length=10)
    old_status=models.IntegerField('状态', null=True, blank=True)
    old_stop_date=models.DateTimeField('停用时间', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_last_price=models.DecimalField('最新采购价', null=True, blank=True, max_digits=18, decimal_places=6)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_cook'
        indexes=[]
        verbose_name=verbose_name_plural='基础主数据相关表（p_Cook，待确认）'
        ordering=["-id"]

class SourceDyePCraftParam(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_CraftParam'
    SOURCE_FIELDS={'ParamID': 'old_param_id', 'ParamName': 'old_param_name', 'ParamType': 'old_param_type', 'UnitStr': 'old_unit_str', 'Description': 'old_description', 'CommStr': 'old_comm_str', 'Rate': 'old_rate'}
    SOURCE_KEY=('ParamID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_param_id=models.CharField('参数编码', null=False, blank=True, max_length=10)
    old_param_name=models.CharField('参数名', null=True, blank=True, max_length=50)
    old_param_type=models.CharField('参数类型', null=True, blank=True, max_length=10)
    old_unit_str=models.CharField('计量单位名称', null=True, blank=True, max_length=6)
    old_description=models.CharField('增减率', null=True, blank=True, max_length=100)
    old_comm_str=models.CharField('串口设置字串', null=True, blank=True, max_length=200)
    old_rate=models.DecimalField('描述', null=True, blank=True, max_digits=10, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_craftparam'
        indexes=[models.Index(fields=['source_batch', 'old_param_id'],name='src_8b46caabb9f22018')]
        verbose_name=verbose_name_plural='系统平台与配置相关表（p_CraftParam，待确认）'
        ordering=["-id"]

class SourceDyePCraftPParam(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_CraftPParam'
    SOURCE_FIELDS={'ParamID': 'old_param_id', 'ParamName': 'old_param_name', 'ParamType': 'old_param_type', 'UnitStr': 'old_unit_str', 'Description': 'old_description'}
    SOURCE_KEY=('ParamID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_param_id=models.CharField('ParamID', null=False, blank=True, max_length=10)
    old_param_name=models.CharField('ParamName', null=True, blank=True, max_length=50)
    old_param_type=models.CharField('ParamType', null=True, blank=True, max_length=10)
    old_unit_str=models.CharField('UnitStr', null=True, blank=True, max_length=6)
    old_description=models.CharField('Description', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_craftpparam'
        indexes=[models.Index(fields=['source_batch', 'old_param_id'],name='src_e65fc29386e3ac28')]
        verbose_name=verbose_name_plural='系统平台与配置相关表（p_CraftPParam，待确认）'
        ordering=["-id"]

class SourceDyePCustAddress(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_CustAddress'
    SOURCE_FIELDS={'CustomerID': 'old_customer_id', 'address': 'old_address', 'zhichang': 'old_zhichang'}
    SOURCE_KEY=('CustomerID', 'address')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Customer', 'target': 'erp_base.SourceDyePCustomer', 'source_fields': ['CustomerID'], 'target_fields': ['CustomerID'], 'evidence': ['原界面主从 p_CustAddress → p_Customer']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_customer_id=models.CharField('客户编码', null=False, blank=True, max_length=10)
    old_address=models.CharField('收发地址', null=False, blank=True, max_length=500)
    old_zhichang=models.CharField('织厂', null=True, blank=True, max_length=200)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePCustomer', verbose_name='原关系：p_Customer', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_custaddress'
        indexes=[models.Index(fields=['source_batch', 'old_customer_id', 'old_address'],name='src_ce2c559d13f664cd')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（p_CustAddress，待确认）'
        ordering=["-id"]

class SourceDyePCustCategory(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_CustCategory'
    SOURCE_FIELDS={'CustomerID': 'old_customer_id', 'CustCategoryCode': 'old_cust_category_code'}
    SOURCE_KEY=('CustomerID', 'CustCategoryCode')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Customer', 'target': 'erp_base.SourceDyePCustomer', 'source_fields': ['CustomerID'], 'target_fields': ['CustomerID'], 'evidence': ['原界面主从 p_CustCategory → p_Customer', '原界面主从 p_CustCategory_Supplier → p_Supplier']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_customer_id=models.CharField('客户代码', null=False, blank=True, max_length=10)
    old_cust_category_code=models.IntegerField('客户分类码', null=False, blank=False)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePCustomer', verbose_name='原关系：p_Customer', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_custcategory'
        indexes=[models.Index(fields=['source_batch', 'old_customer_id', 'old_cust_category_code'],name='src_d46a592b91c7739e')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（p_CustCategory，待确认）'
        ordering=["-id"]

class SourceDyePCustLinker(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_CustLinker'
    SOURCE_FIELDS={'CustomerID': 'old_customer_id', 'RowNo': 'old_row_no', 'Name': 'old_name', 'Dept': 'old_dept', 'Title': 'old_title', 'Mobile': 'old_mobile', 'OfficeTel': 'old_office_tel', 'Fax': 'old_fax', 'Email': 'old_email', 'Remarks': 'old_remarks', 'Addr': 'old_addr', 'Tel': 'old_tel', 'QQ': 'old_qq'}
    SOURCE_KEY=('CustomerID', 'RowNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Customer', 'target': 'erp_base.SourceDyePCustomer', 'source_fields': ['CustomerID'], 'target_fields': ['CustomerID'], 'evidence': ['原界面主从 p_CustLinker_Supplier → p_Supplier', '原界面主从 p_CustLinker → p_Customer']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_customer_id=models.CharField('客户代码', null=False, blank=True, max_length=10)
    old_row_no=models.DecimalField('行号', null=False, blank=False, max_digits=3, decimal_places=0)
    old_name=models.CharField('名称', null=True, blank=True, max_length=60)
    old_dept=models.CharField('部门', null=True, blank=True, max_length=20)
    old_title=models.CharField('职位', null=True, blank=True, max_length=20)
    old_mobile=models.CharField('手机', null=True, blank=True, max_length=15)
    old_office_tel=models.CharField('办公室电话', null=True, blank=True, max_length=16)
    old_fax=models.CharField('传真', null=True, blank=True, max_length=20)
    old_email=models.CharField('Email', null=True, blank=True, max_length=60)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_addr=models.CharField('Addr', null=True, blank=True, max_length=160)
    old_tel=models.CharField('Tel', null=True, blank=True, max_length=16)
    old_qq=models.CharField('QQ', null=True, blank=True, max_length=20)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePCustomer', verbose_name='原关系：p_Customer', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_custlinker'
        indexes=[models.Index(fields=['source_batch', 'old_customer_id', 'old_row_no'],name='src_f74b32b54ee47262')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（p_CustLinker，待确认）'
        ordering=["-id"]

class SourceDyePCustomer(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Customer'
    SOURCE_FIELDS={'CustomerID': 'old_customer_id', 'DetailCustName': 'old_detail_cust_name', 'ShortName': 'old_short_name', 'Mnemonic': 'old_mnemonic', 'NameC': 'old_name_c', 'NameE': 'old_name_e', 'SalerID': 'old_saler_id', 'CustKindID': 'old_cust_kind_id', 'CorpKindID': 'old_corp_kind_id', 'Tel': 'old_tel', 'Fax': 'old_fax', 'Zip': 'old_zip', 'CountryID': 'old_country_id', 'Addr': 'old_addr', 'AddrE': 'old_addr_e', 'AddrDlv': 'old_addr_dlv', 'AddrInv': 'old_addr_inv', 'Charger': 'old_charger', 'CorpCode': 'old_corp_code', 'Email': 'old_email', 'WebSite': 'old_web_site', 'CreditLimit': 'old_credit_limit', 'Deposit': 'old_deposit', 'AreaID': 'old_area_id', 'CreditGrade': 'old_credit_grade', 'IsAbroad': 'old_is_abroad', 'BeginDate': 'old_begin_date', 'Market': 'old_market', 'SettleID': 'old_settle_id', 'LimitDays': 'old_limit_days', 'PaymentID': 'old_payment_id', 'BillDays': 'old_bill_days', 'BankName': 'old_bank_name', 'BankNo': 'old_bank_no', 'Bank': 'old_bank', 'BankName1': 'old_bank_name1', 'BankNo1': 'old_bank_no1', 'Bank1': 'old_bank1', 'BankName2': 'old_bank_name2', 'BankNo2': 'old_bank_no2', 'Bank2': 'old_bank2', 'IsStop': 'old_is_stop', 'StopDate': 'old_stop_date', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ParentCustID': 'old_parent_cust_id', 'Discount': 'old_discount', 'APMoney': 'old_apmoney', 'ARMoney': 'old_armoney', 'ProdCode': 'old_prod_code', 'PrintTimes': 'old_print_times', 'PASSWORD': 'old_password', 'LoginName': 'old_login_name', 'GaryPrice': 'old_gary_price', 'LabelID': 'old_label_id', 'CorpType': 'old_corp_type', 'AddQty': 'old_add_qty', 'XMLFolder': 'old_xmlfolder', 'EnableOrders': 'old_enable_orders', 'RightStatus': 'old_right_status', 'Contact': 'old_contact', 'MasterCustomer': 'old_master_customer', 'Merchandiser': 'old_merchandiser', 'PortNO': 'old_port_no', 'Num': 'old_num'}
    SOURCE_KEY=('CustomerID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_customer_id=models.CharField('客户编码', null=False, blank=True, max_length=10)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=50)
    old_short_name=models.CharField('客户简称', null=True, blank=True, max_length=50)
    old_mnemonic=models.CharField('助记符', null=True, blank=True, max_length=30)
    old_name_c=models.CharField('中文名称', null=True, blank=True, max_length=128)
    old_name_e=models.CharField('英文名称', null=True, blank=True, max_length=128)
    old_saler_id=models.CharField('业务员代码', null=True, blank=True, max_length=10)
    old_cust_kind_id=models.CharField('类别', null=True, blank=True, max_length=10)
    old_corp_kind_id=models.CharField('企业类型', null=True, blank=True, max_length=10)
    old_tel=models.CharField('电话', null=True, blank=True, max_length=50)
    old_fax=models.CharField('传真', null=True, blank=True, max_length=20)
    old_zip=models.CharField('邮编', null=True, blank=True, max_length=10)
    old_country_id=models.CharField('国家代码', null=True, blank=True, max_length=10)
    old_addr=models.CharField('地址', null=True, blank=True, max_length=160)
    old_addr_e=models.CharField('英文地址名', null=True, blank=True, max_length=160)
    old_addr_dlv=models.CharField('交货地址', null=True, blank=True, max_length=160)
    old_addr_inv=models.CharField('发票地址', null=True, blank=True, max_length=160)
    old_charger=models.CharField('负责人', null=True, blank=True, max_length=128)
    old_corp_code=models.CharField('公司代码', null=True, blank=True, max_length=30)
    old_email=models.CharField('Email', null=True, blank=True, max_length=60)
    old_web_site=models.CharField('网站', null=True, blank=True, max_length=60)
    old_credit_limit=models.BigIntegerField('信用额度', null=True, blank=True)
    old_deposit=models.DecimalField('折扣', null=True, blank=True, max_digits=8, decimal_places=2)
    old_area_id=models.CharField('区域', null=True, blank=True, max_length=10)
    old_credit_grade=models.CharField('信用等级', null=True, blank=True, max_length=10)
    old_is_abroad=models.BooleanField('自动包装', null=True, blank=True)
    old_begin_date=models.DateTimeField('初始日期', null=True, blank=True)
    old_market=models.CharField('市场区域', null=True, blank=True, max_length=100)
    old_settle_id=models.CharField('结算方式', null=True, blank=True, max_length=10)
    old_limit_days=models.IntegerField('收款期限', null=True, blank=True)
    old_payment_id=models.CharField('付款方式', null=True, blank=True, max_length=10)
    old_bill_days=models.IntegerField('票据天数', null=True, blank=True)
    old_bank_name=models.CharField('户名', null=True, blank=True, max_length=100)
    old_bank_no=models.CharField('银行卡号', null=True, blank=True, max_length=100)
    old_bank=models.CharField('开户行', null=True, blank=True, max_length=100)
    old_bank_name1=models.CharField('BankName1', null=True, blank=True, max_length=200)
    old_bank_no1=models.CharField('BankNo1', null=True, blank=True, max_length=200)
    old_bank1=models.CharField('Bank1', null=True, blank=True, max_length=200)
    old_bank_name2=models.CharField('BankName2', null=True, blank=True, max_length=200)
    old_bank_no2=models.CharField('BankNo2', null=True, blank=True, max_length=200)
    old_bank2=models.CharField('Bank2', null=True, blank=True, max_length=200)
    old_is_stop=models.BooleanField('是否停用', null=True, blank=True)
    old_stop_date=models.DateTimeField('停用时间', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_parent_cust_id=models.CharField('ParentCustID', null=True, blank=True, max_length=10)
    old_discount=models.DecimalField('Discount', null=True, blank=True, max_digits=3, decimal_places=2)
    old_apmoney=models.DecimalField('APMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_armoney=models.DecimalField('ARMoney', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prod_code=models.CharField('ProdCode', null=True, blank=True, max_length=32)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_password=models.CharField('PASSWORD', null=True, blank=True, max_length=50)
    old_login_name=models.CharField('LoginName', null=True, blank=True, max_length=50)
    old_gary_price=models.CharField('计价类别', null=True, blank=True, max_length=20)
    old_label_id=models.CharField('标签', null=True, blank=True, max_length=20)
    old_corp_type=models.CharField('供应商类别', null=True, blank=True, max_length=10)
    old_add_qty=models.FloatField('包装加重', null=True, blank=True)
    old_xmlfolder=models.CharField('XMLFolder', null=True, blank=True, max_length=1000)
    old_enable_orders=models.BooleanField('是否启用订单', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_contact=models.CharField('联系人', null=True, blank=True, max_length=50)
    old_master_customer=models.CharField('主客户名', null=True, blank=True, max_length=30)
    old_merchandiser=models.CharField('跟单员', null=True, blank=True, max_length=30)
    old_port_no=models.CharField('PortNO', null=True, blank=True, max_length=10)
    old_num=models.CharField('Num', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_customer'
        indexes=[models.Index(fields=['source_batch', 'old_customer_id'],name='src_9b03dbccacc2f29d')]
        verbose_name=verbose_name_plural='往来单位（客户/供应商）'
        ordering=["-id"]

class SourceDyePCustRelation(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_CustRelation'
    SOURCE_FIELDS={'CustomerID': 'old_customer_id', 'RowNo': 'old_row_no', 'Code': 'old_code', 'RelaCustomerID': 'old_rela_customer_id', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('CustomerID', 'RowNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Customer', 'target': 'erp_base.SourceDyePCustomer', 'source_fields': ['CustomerID'], 'target_fields': ['CustomerID'], 'evidence': ['原界面主从 p_CustRelation → p_Customer', '数据库声明 FK_p_CustAddr_p_Customer', '原界面主从 p_CustRelation_Supplier → p_Supplier']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_customer_id=models.CharField('客户编码', null=False, blank=True, max_length=10)
    old_row_no=models.DecimalField('行号', null=False, blank=False, max_digits=2, decimal_places=0)
    old_code=models.CharField('编码', null=True, blank=True, max_length=10)
    old_rela_customer_id=models.CharField('关系客户代码', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePCustomer', verbose_name='原关系：p_Customer', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_custrelation'
        indexes=[models.Index(fields=['source_batch', 'old_customer_id', 'old_row_no'],name='src_a386b13256a541ef')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（p_CustRelation，待确认）'
        ordering=["-id"]

class SourceDyePDept(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Dept'
    SOURCE_FIELDS={'DeptID': 'old_dept_id', 'Name': 'old_name', 'ParentCode': 'old_parent_code', 'ChargerID': 'old_charger_id', 'Description': 'old_description', 'StopDate': 'old_stop_date', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'DeptKindID': 'old_dept_kind_id', 'IsStop': 'old_is_stop', 'IsCostUnit': 'old_is_cost_unit'}
    SOURCE_KEY=('DeptID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_dept_id=models.CharField('部门编码', null=False, blank=True, max_length=10)
    old_name=models.CharField('名称', null=True, blank=True, max_length=60)
    old_parent_code=models.CharField('父级代码', null=True, blank=True, max_length=10)
    old_charger_id=models.CharField('部门负责人', null=True, blank=True, max_length=10)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    old_stop_date=models.DateTimeField('停用时间', null=True, blank=True)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_dept_kind_id=models.CharField('部门类型', null=True, blank=True, max_length=10)
    old_is_stop=models.BooleanField('是否停用', null=True, blank=True)
    old_is_cost_unit=models.BooleanField('成本部门', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_dept'
        indexes=[models.Index(fields=['source_batch', 'old_dept_id'],name='src_3af5592c1f698cc8')]
        verbose_name=verbose_name_plural='部门'
        ordering=["-id"]

class SourceDyePDyeCurve(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_DyeCurve'
    SOURCE_FIELDS={'CurveID': 'old_curve_id', 'Name': 'old_name', 'Description': 'old_description', 'ProgramKindID': 'old_program_kind_id', 'DyePhase': 'old_dye_phase', 'PreMinutes': 'old_pre_minutes', 'ProgramMinutes': 'old_program_minutes', 'TotalMinutes': 'old_total_minutes', 'SelfDefineImage': 'old_self_define_image', 'AutoImage': 'old_auto_image', 'Remarks': 'old_remarks', 'IsStop': 'old_is_stop', 'StopDate': 'old_stop_date', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'EffiRate': 'old_effi_rate', 'MaxValue': 'old_max_value', 'PhaseID': 'old_phase_id'}
    SOURCE_KEY=('CurveID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_curve_id=models.CharField('编号', null=False, blank=True, max_length=10)
    old_name=models.CharField('曲线名称', null=True, blank=True, max_length=60)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    old_program_kind_id=models.CharField('分类', null=True, blank=True, max_length=10)
    old_dye_phase=models.IntegerField('阶段', null=True, blank=True)
    old_pre_minutes=models.IntegerField('准备时间', null=True, blank=True)
    old_program_minutes=models.IntegerField('工艺时间', null=True, blank=True)
    old_total_minutes=models.IntegerField('合计时间', null=True, blank=True)
    old_self_define_image=models.BinaryField('自定义曲线图', null=True, blank=True, editable=True)
    old_auto_image=models.BinaryField('计算产生曲线图', null=True, blank=True, editable=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_is_stop=models.BooleanField('停用', null=True, blank=True)
    old_stop_date=models.DateTimeField('停用时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_effi_rate=models.DecimalField('EffiRate', null=True, blank=True, max_digits=6, decimal_places=4)
    old_max_value=models.DecimalField('MaxValue', null=True, blank=True, max_digits=10, decimal_places=2)
    old_phase_id=models.CharField('染色流程', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_dyecurve'
        indexes=[models.Index(fields=['source_batch', 'old_curve_id'],name='src_1cb41b3d5d14a666')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（p_DyeCurve，待确认）'
        ordering=["-id"]

class SourceDyePDyeCurveDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_DyeCurveDetail'
    SOURCE_FIELDS={'CurveID': 'old_curve_id', 'StepNo': 'old_step_no', 'DyeProcessID': 'old_dye_process_id', 'Temperature': 'old_temperature', 'SpeedRate': 'old_speed_rate', 'Minutes': 'old_minutes', 'Price': 'old_price', 'DefaultValue': 'old_default_value', 'Memo': 'old_memo'}
    SOURCE_KEY=('CurveID', 'StepNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_DyeCurve', 'target': 'erp_base.SourceDyePDyeCurve', 'source_fields': ['CurveID'], 'target_fields': ['CurveID'], 'evidence': ['原界面主从 p_DyeCurveDetailJJ → p_DyeCurveJJ', '原界面主从 p_DyeCurveDetail → p_DyeCurve']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_curve_id=models.CharField('曲线编码', null=False, blank=True, max_length=10)
    old_step_no=models.IntegerField('步号', null=False, blank=False)
    old_dye_process_id=models.CharField('染色工序', null=True, blank=True, max_length=50)
    old_temperature=models.DecimalField('温度', null=True, blank=True, max_digits=5, decimal_places=1)
    old_speed_rate=models.DecimalField('速率', null=True, blank=True, max_digits=3, decimal_places=1)
    old_minutes=models.DecimalField('分钟', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_default_value=models.DecimalField('DefaultValue', null=True, blank=True, max_digits=10, decimal_places=2)
    old_memo=models.CharField('Memo', null=True, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePDyeCurve', verbose_name='原关系：p_DyeCurve', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_dyecurvedetail'
        indexes=[models.Index(fields=['source_batch', 'old_curve_id', 'old_step_no'],name='src_47f9342cee6b0cdb')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（p_DyeCurveDetail，待确认）'
        ordering=["-id"]

class SourceDyePDyeProgram(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_DyeProgram'
    SOURCE_FIELDS={'ProgramID': 'old_program_id', 'Name': 'old_name', 'Description': 'old_description', 'ProgramKindID': 'old_program_kind_id', 'PreMinutes': 'old_pre_minutes', 'ProgramMinutes': 'old_program_minutes', 'TotalMinutes': 'old_total_minutes', 'Remarks': 'old_remarks', 'IsStop': 'old_is_stop', 'StopDate': 'old_stop_date', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'DyePhase': 'old_dye_phase', 'SelfDefineImage': 'old_self_define_image', 'AutoImage': 'old_auto_image'}
    SOURCE_KEY=('ProgramID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_program_id=models.CharField('ProgramID', null=False, blank=True, max_length=10)
    old_name=models.CharField('Name', null=True, blank=True, max_length=60)
    old_description=models.CharField('Description', null=True, blank=True, max_length=100)
    old_program_kind_id=models.CharField('ProgramKindID', null=True, blank=True, max_length=10)
    old_pre_minutes=models.IntegerField('PreMinutes', null=True, blank=True)
    old_program_minutes=models.IntegerField('ProgramMinutes', null=True, blank=True)
    old_total_minutes=models.IntegerField('TotalMinutes', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_is_stop=models.BooleanField('IsStop', null=True, blank=True)
    old_stop_date=models.DateTimeField('StopDate', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_dye_phase=models.IntegerField('DyePhase', null=True, blank=True)
    old_self_define_image=models.BinaryField('SelfDefineImage', null=True, blank=True, editable=True)
    old_auto_image=models.BinaryField('AutoImage', null=True, blank=True, editable=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_dyeprogram'
        indexes=[models.Index(fields=['source_batch', 'old_program_id'],name='src_16a76eae1008de1e')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（p_DyeProgram，待确认）'
        ordering=["-id"]

class SourceDyePDyeProgramDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_DyeProgramDetail'
    SOURCE_FIELDS={'ProgramID': 'old_program_id', 'StepNo': 'old_step_no', 'DyeProcessID': 'old_dye_process_id', 'Temperature': 'old_temperature', 'Minutes': 'old_minutes', 'Price': 'old_price', 'EffiRate': 'old_effi_rate', 'SpeedRate': 'old_speed_rate'}
    SOURCE_KEY=('ProgramID', 'StepNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_program_id=models.CharField('ProgramID', null=False, blank=True, max_length=10)
    old_step_no=models.IntegerField('StepNo', null=False, blank=False)
    old_dye_process_id=models.CharField('DyeProcessID', null=True, blank=True, max_length=10)
    old_temperature=models.DecimalField('Temperature', null=True, blank=True, max_digits=5, decimal_places=1)
    old_minutes=models.DecimalField('Minutes', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)
    old_effi_rate=models.DecimalField('EffiRate', null=True, blank=True, max_digits=6, decimal_places=4)
    old_speed_rate=models.DecimalField('SpeedRate', null=True, blank=True, max_digits=3, decimal_places=1)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_dyeprogramdetail'
        indexes=[models.Index(fields=['source_batch', 'old_program_id', 'old_step_no'],name='src_3cd036f3f78cdb90')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（p_DyeProgramDetail，待确认）'
        ordering=["-id"]

class SourceDyePFabric(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Fabric'
    SOURCE_FIELDS={'FabricID': 'old_fabric_id', 'NameC': 'old_name_c', 'NameE': 'old_name_e', 'Spec': 'old_spec', 'Structure': 'old_structure', 'FabricKindID': 'old_fabric_kind_id', 'FabricStyleID': 'old_fabric_style_id', 'GrayWeight': 'old_gray_weight', 'StockUnit': 'old_stock_unit', 'PriceUnit': 'old_price_unit', 'GrayPrice': 'old_gray_price', 'ProdPrice': 'old_prod_price', 'ProdWeight': 'old_prod_weight', 'Mnemonic': 'old_mnemonic', 'Graphic': 'old_graphic', 'IsSample': 'old_is_sample', 'IsStop': 'old_is_stop', 'StopDate': 'old_stop_date', 'WidthDn': 'old_width_dn', 'WidthUp': 'old_width_up', 'Description': 'old_description', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Density': 'old_density', 'ColorID': 'old_color_id', 'Place': 'old_place'}
    SOURCE_KEY=('FabricID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_fabric_id=models.CharField('客户规格', null=False, blank=True, max_length=20)
    old_name_c=models.CharField('中文名称', null=True, blank=True, max_length=60)
    old_name_e=models.CharField('英文名称', null=True, blank=True, max_length=60)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=50)
    old_structure=models.CharField('组织', null=True, blank=True, max_length=50)
    old_fabric_kind_id=models.CharField('纱种类别', null=True, blank=True, max_length=10)
    old_fabric_style_id=models.CharField('纱种风格编码', null=True, blank=True, max_length=10)
    old_gray_weight=models.DecimalField('胚纱克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_stock_unit=models.IntegerField('库存单位', null=True, blank=True)
    old_price_unit=models.IntegerField('计价单位编码', null=True, blank=True)
    old_gray_price=models.DecimalField('胚纱价格', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prod_price=models.DecimalField('成品价格', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prod_weight=models.DecimalField('成品克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_mnemonic=models.CharField('助记符', null=True, blank=True, max_length=10)
    old_graphic=models.BinaryField('图案', null=True, blank=True, editable=True)
    old_is_sample=models.BooleanField('是否样品', null=True, blank=True)
    old_is_stop=models.BooleanField('是否停用', null=True, blank=True)
    old_stop_date=models.DateTimeField('停用时间', null=True, blank=True)
    old_width_dn=models.DecimalField('门幅下限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_width_up=models.DecimalField('门幅上限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_density=models.CharField('密度', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=20)
    old_place=models.CharField('存放位置', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_fabric'
        indexes=[models.Index(fields=['source_batch', 'old_fabric_id'],name='src_f957d7efcc0565af')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（p_Fabric，待确认）'
        ordering=["-id"]

class SourceDyePFabricCust(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Fabric_Cust'
    SOURCE_FIELDS={'FabricID': 'old_fabric_id', 'CustomerID': 'old_customer_id', 'Kind': 'old_kind', 'CustFabricName': 'old_cust_fabric_name', 'PriceTime': 'old_price_time', 'Price': 'old_price', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('FabricID', 'CustomerID', 'Kind')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Gray', 'target': 'erp_base.SourceDyePGray', 'source_fields': ['FabricID'], 'target_fields': ['GrayID'], 'evidence': ['原界面主从 p_Gray_Cust → p_Gray']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_fabric_id=models.CharField('客户规格', null=False, blank=True, max_length=20)
    old_customer_id=models.CharField('客户编码', null=False, blank=True, max_length=10)
    old_kind=models.CharField('胚纱/成品', null=False, blank=True, max_length=10)
    old_cust_fabric_name=models.CharField('客户规格', null=True, blank=True, max_length=50)
    old_price_time=models.DateTimeField('价格时间', null=True, blank=True)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePGray', verbose_name='原关系：p_Gray', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_fabric_cust'
        indexes=[models.Index(fields=['source_batch', 'old_fabric_id', 'old_customer_id', 'old_kind'],name='src_5f92e2a93d98551e')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（p_Fabric_Cust，待确认）'
        ordering=["-id"]

class SourceDyePFabricFact(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Fabric_Fact'
    SOURCE_FIELDS={'FabricID': 'old_fabric_id', 'CustCategoryCode': 'old_cust_category_code', 'FactID': 'old_fact_id', 'Kind': 'old_kind', 'Qty': 'old_qty', 'Price': 'old_price', 'PriceTime': 'old_price_time', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('FabricID', 'CustCategoryCode', 'FactID', 'Kind')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Gray', 'target': 'erp_base.SourceDyePGray', 'source_fields': ['FabricID'], 'target_fields': ['GrayID'], 'evidence': ['原界面主从 p_Gray_Fact → p_Gray']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_fabric_id=models.CharField('客户规格', null=False, blank=True, max_length=20)
    old_cust_category_code=models.IntegerField('供应商分类', null=False, blank=False)
    old_fact_id=models.CharField('供应商编号', null=False, blank=True, max_length=10)
    old_kind=models.CharField('胚纱/成品', null=False, blank=True, max_length=10)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_price_time=models.DateTimeField('时间', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePGray', verbose_name='原关系：p_Gray', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_fabric_fact'
        indexes=[models.Index(fields=['source_batch', 'old_fabric_id', 'old_cust_category_code', 'old_fact_id', 'old_kind'],name='src_f9e76a722b98ae34')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（p_Fabric_Fact，待确认）'
        ordering=["-id"]

class SourceDyePFabricOther(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Fabric_Other'
    SOURCE_FIELDS={'FabricID': 'old_fabric_id', 'FabricInfoKindID': 'old_fabric_info_kind_id', 'Code': 'old_code', 'Kind': 'old_kind', 'NumValue': 'old_num_value', 'StringValue': 'old_string_value'}
    SOURCE_KEY=('FabricID', 'FabricInfoKindID', 'Code', 'Kind')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Gray', 'target': 'erp_base.SourceDyePGray', 'source_fields': ['FabricID'], 'target_fields': ['GrayID'], 'evidence': ['原界面主从 p_Gray_Other → p_Gray']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_fabric_id=models.CharField('客户规格', null=False, blank=True, max_length=10)
    old_fabric_info_kind_id=models.CharField('胚纱信息分类代码', null=False, blank=True, max_length=10)
    old_code=models.CharField('信息代码', null=False, blank=True, max_length=10)
    old_kind=models.CharField('胚纱/成品', null=False, blank=True, max_length=10)
    old_num_value=models.DecimalField('数值信息', null=True, blank=True, max_digits=18, decimal_places=6)
    old_string_value=models.CharField('文字信息', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePGray', verbose_name='原关系：p_Gray', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_fabric_other'
        indexes=[models.Index(fields=['source_batch', 'old_fabric_id', 'old_fabric_info_kind_id', 'old_code', 'old_kind'],name='src_b3348eaa1a28b3e8')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（p_Fabric_Other，待确认）'
        ordering=["-id"]

class SourceDyePFeelCode(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_FeelCode'
    SOURCE_FIELDS={'FeelCode': 'old_feel_code', 'FeelName': 'old_feel_name', 'SerialNumber': 'old_serial_number', 'ProdID': 'old_prod_id'}
    SOURCE_KEY=('ProdID', 'FeelCode')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Product', 'target': 'erp_base.SourceDyePProduct', 'source_fields': ['ProdID'], 'target_fields': ['ProdID'], 'evidence': ['原界面主从 p_FeelCode → p_Product']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_feel_code=models.CharField('手感编号', null=False, blank=True, max_length=50)
    old_feel_name=models.CharField('手感名称', null=True, blank=True, max_length=100)
    old_serial_number=models.IntegerField('序号', null=True, blank=True)
    old_prod_id=models.CharField('本厂规格', null=False, blank=True, max_length=50)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePProduct', verbose_name='原关系：p_Product', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_feelcode'
        indexes=[models.Index(fields=['source_batch', 'old_prod_id', 'old_feel_code'],name='src_01b7b77504d3dc76')]
        verbose_name=verbose_name_plural='基础主数据相关表（p_FeelCode，待确认）'
        ordering=["-id"]

class SourceDyePFieldMemo(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_FieldMemo'
    SOURCE_FIELDS={'FieldType': 'old_field_type', 'Name': 'old_name', 'IsStop': 'old_is_stop', 'StopDate': 'old_stop_date', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer'}
    SOURCE_KEY=('FieldType', 'Name')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_field_type=models.CharField('类型', null=False, blank=True, max_length=20)
    old_name=models.CharField('Name', null=False, blank=True, max_length=500)
    old_is_stop=models.BooleanField('IsStop', null=True, blank=True)
    old_stop_date=models.DateTimeField('停用日期', null=True, blank=True)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_fieldmemo'
        indexes=[models.Index(fields=['source_batch', 'old_field_type', 'old_name'],name='src_0639e3bb61e96b3e')]
        verbose_name=verbose_name_plural='基础主数据相关表（p_FieldMemo，待确认）'
        ordering=["-id"]

class SourceDyePFieldValid(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_FieldValid'
    SOURCE_FIELDS={'FieldType': 'old_field_type', 'Code': 'old_code', 'Name': 'old_name', 'Mnemonic': 'old_mnemonic', 'NumValue': 'old_num_value', 'SortValue': 'old_sort_value', 'Description': 'old_description', 'Reserved1': 'old_reserved1', 'Reserved2': 'old_reserved2', 'Reserved3': 'old_reserved3', 'Reserved4': 'old_reserved4', 'Reserved5': 'old_reserved5', 'StopDate': 'old_stop_date', 'ParentCode': 'old_parent_code', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'IsStop': 'old_is_stop', 'BusinessUnitID': 'old_business_unit_id', 'NumValueNo': 'old_num_value_no', 'CustomerID': 'old_customer_id', 'Long_CM': 'old_long_cm', 'Wide_CM': 'old_wide_cm', 'High_CM': 'old_high_cm'}
    SOURCE_KEY=('FieldType', 'Code')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_sort_value': ('literal', 0), 'old_reserved2': ('literal', '0'), 'old_reserved3': ('literal', '0'), 'old_reserved4': ('literal', '0'), 'old_reserved5': ('literal', '0')}
    SOURCE_IDENTITIES=()
    old_field_type=models.CharField('数据类型', null=False, blank=True, max_length=20)
    old_code=models.CharField('编号', null=False, blank=True, max_length=20)
    old_name=models.CharField('名称', null=False, blank=True, max_length=100)
    old_mnemonic=models.CharField('助记符', null=True, blank=True, max_length=100)
    old_num_value=models.DecimalField('数值值', null=True, blank=True, max_digits=18, decimal_places=6)
    old_sort_value=models.IntegerField('排序值', null=True, blank=True)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    old_reserved1=models.CharField('单位', null=True, blank=True, max_length=1000)
    old_reserved2=models.CharField('是否打印', null=True, blank=True, max_length=100)
    old_reserved3=models.CharField('扣分值', null=True, blank=True, max_length=100)
    old_reserved4=models.CharField('保留值4', null=True, blank=True, max_length=100)
    old_reserved5=models.CharField('保留值5', null=True, blank=True, max_length=100)
    old_stop_date=models.DateTimeField('停用日期', null=True, blank=True)
    old_parent_code=models.CharField('父级代码', null=True, blank=True, max_length=10)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_is_stop=models.BooleanField('是否停用', null=True, blank=True)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=20)
    old_num_value_no=models.IntegerField('NumValueNo', null=True, blank=True)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=20)
    old_long_cm=models.DecimalField('长(CM)', null=True, blank=True, max_digits=6, decimal_places=1)
    old_wide_cm=models.DecimalField('宽(CM)', null=True, blank=True, max_digits=6, decimal_places=1)
    old_high_cm=models.DecimalField('高(CM)', null=True, blank=True, max_digits=6, decimal_places=1)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_fieldvalid'
        indexes=[models.Index(fields=['source_batch', 'old_field_type', 'old_code'],name='src_4878bf7ccd75f693')]
        verbose_name=verbose_name_plural='通用代码字典'
        ordering=["-id"]

class SourceDyePFieldValidSub(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_FieldValidSub'
    SOURCE_FIELDS={'FieldType': 'old_field_type', 'Code': 'old_code', 'SubCode': 'old_sub_code', 'SortValue': 'old_sort_value', 'Name': 'old_name', 'NumValue': 'old_num_value', 'NumValue2': 'old_num_value2', 'PriceUnit': 'old_price_unit', 'Description': 'old_description', 'IsDefault': 'old_is_default', 'NumValue3': 'old_num_value3', 'CodeName': 'old_code_name'}
    SOURCE_KEY=('FieldType', 'Code', 'SubCode', 'SortValue')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_FieldValid', 'target': 'erp_base.SourceDyePFieldValid', 'source_fields': ['FieldType', 'Code'], 'target_fields': ['FieldType', 'Code'], 'evidence': ['原界面主从 p_ProductionDetail → p_Production', '原界面主从 DefectGroupDetail → DefectGroup', '原界面主从 PrintStarchWasteDetail → PrintStarchWaste', '原界面主从 p_FieldValidSub → p_FieldValid', '原界面主从 DefectKindDetail → DefectKind', '原界面主从 RequireValue → RequireClass']}]
    SOURCE_DEFAULTS={'old_sort_value': ('literal', 0), 'old_name': ('literal', ''), 'old_num_value': ('literal', 0), 'old_description': ('literal', '')}
    SOURCE_IDENTITIES=()
    old_field_type=models.CharField('数据类型', null=False, blank=True, max_length=20)
    old_code=models.CharField('疵点编号', null=False, blank=True, max_length=20)
    old_sub_code=models.CharField('疵点代码', null=False, blank=True, max_length=10)
    old_sort_value=models.IntegerField('排序值', null=False, blank=False)
    old_name=models.CharField('疵点名', null=False, blank=True, max_length=60)
    old_num_value=models.DecimalField('数值值', null=True, blank=True, max_digits=18, decimal_places=6)
    old_num_value2=models.DecimalField('收费价格', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price_unit=models.IntegerField('收费单位', null=True, blank=True)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    old_is_default=models.IntegerField('默认选择', null=True, blank=True)
    old_num_value3=models.IntegerField('是否收费', null=True, blank=True)
    old_code_name=models.CharField('代码', null=True, blank=True, max_length=30)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePFieldValid', verbose_name='原关系：p_FieldValid', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_fieldvalidsub'
        indexes=[models.Index(fields=['source_batch', 'old_field_type', 'old_code', 'old_sub_code'],name='src_5e1047db3770667f'),models.Index(fields=['source_batch', 'old_field_type', 'old_code', 'old_sub_code', 'old_sort_value'],name='src_c33ea712b1f5f4dd')]
        verbose_name=verbose_name_plural='基础主数据相关表（p_FieldValidSub，待确认）'
        ordering=["-id"]

class SourceDyePFieldValidSubCust(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_FieldValidSubCust'
    SOURCE_FIELDS={'FieldType': 'old_field_type', 'Code': 'old_code', 'SubCode': 'old_sub_code', 'CustomerID': 'old_customer_id', 'Value01': 'old_value01', 'Value02': 'old_value02', 'NumValue': 'old_num_value', 'NumValue2': 'old_num_value2', 'PriceUnit': 'old_price_unit', 'Description': 'old_description'}
    SOURCE_KEY=('FieldType', 'Code', 'SubCode', 'CustomerID', 'Value01')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_FieldValidSub', 'target': 'erp_base.SourceDyePFieldValidSub', 'source_fields': ['FieldType', 'Code', 'SubCode'], 'target_fields': ['FieldType', 'Code', 'SubCode'], 'evidence': ['原界面主从 RequireValueCust → RequireValue', '原界面主从 p_FieldValidSubCust → p_FieldValidSub']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_field_type=models.CharField('数据类型', null=False, blank=True, max_length=20)
    old_code=models.CharField('主分类编码', null=False, blank=True, max_length=20)
    old_sub_code=models.CharField('子分类编码', null=False, blank=True, max_length=10)
    old_customer_id=models.CharField('客户', null=False, blank=True, max_length=10)
    old_value01=models.CharField('Value01', null=False, blank=True, max_length=20)
    old_value02=models.CharField('Value02', null=True, blank=True, max_length=20)
    old_num_value=models.DecimalField('数值值', null=True, blank=True, max_digits=18, decimal_places=6)
    old_num_value2=models.DecimalField('收费价格', null=True, blank=True, max_digits=10, decimal_places=2)
    old_price_unit=models.IntegerField('收费单位', null=True, blank=True)
    old_description=models.CharField('描述', null=True, blank=True, max_length=500)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePFieldValidSub', verbose_name='原关系：p_FieldValidSub', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_fieldvalidsubcust'
        indexes=[models.Index(fields=['source_batch', 'old_field_type', 'old_code', 'old_sub_code', 'old_customer_id', 'old_value01'],name='src_aa885cabc09fac83')]
        verbose_name=verbose_name_plural='客户订单与销售相关表（p_FieldValidSubCust，待确认）'
        ordering=["-id"]

class SourceDyePGray(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Gray'
    SOURCE_FIELDS={'GrayID': 'old_gray_id', 'NameC': 'old_name_c', 'NameE': 'old_name_e', 'Spec': 'old_spec', 'Structure': 'old_structure', 'FabricKindID': 'old_fabric_kind_id', 'FabricStyleID': 'old_fabric_style_id', 'GrayWeight': 'old_gray_weight', 'Density': 'old_density', 'ColorID': 'old_color_id', 'StockUnit': 'old_stock_unit', 'PriceUnit': 'old_price_unit', 'Place': 'old_place', 'GrayPrice': 'old_gray_price', 'ProdPrice': 'old_prod_price', 'ProdWeight': 'old_prod_weight', 'Mnemonic': 'old_mnemonic', 'Graphic': 'old_graphic', 'IsSample': 'old_is_sample', 'IsStop': 'old_is_stop', 'StopDate': 'old_stop_date', 'WidthDn': 'old_width_dn', 'WidthUp': 'old_width_up', 'Description': 'old_description', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ProductionID': 'old_production_id', 'RealLoss': 'old_real_loss', 'AddLoss': 'old_add_loss', 'CustSelfProduct': 'old_cust_self_product', 'CustomerID': 'old_customer_id', 'OldGrayID': 'old_old_gray_id', 'PCS': 'old_pcs', 'FatherGrayID': 'old_father_gray_id', 'JNKind': 'old_jnkind', 'STKind': 'old_stkind', 'ZTKind': 'old_ztkind', 'RSKind': 'old_rskind', 'JTKind': 'old_jtkind', 'ChengBen0': 'old_cheng_ben0', 'ChengBen1': 'old_cheng_ben1', 'ChengBen2': 'old_cheng_ben2', 'ChengBen3': 'old_cheng_ben3', 'ChengBen4': 'old_cheng_ben4', 'ChengBen5': 'old_cheng_ben5', 'JiJianPiece0': 'old_ji_jian_piece0', 'JiJianPiece1': 'old_ji_jian_piece1', 'JiJianPiece2': 'old_ji_jian_piece2', 'JiJianPiece3': 'old_ji_jian_piece3', 'JiJianPiece4': 'old_ji_jian_piece4', 'JiJianPiece5': 'old_ji_jian_piece5'}
    SOURCE_KEY=('GrayID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_gray_id=models.CharField('规格编码', null=False, blank=True, max_length=20)
    old_name_c=models.CharField('规格名称', null=True, blank=True, max_length=150)
    old_name_e=models.CharField('客户名称', null=True, blank=True, max_length=150)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=50)
    old_structure=models.CharField('组织', null=True, blank=True, max_length=50)
    old_fabric_kind_id=models.CharField('胚纱类别', null=True, blank=True, max_length=30)
    old_fabric_style_id=models.CharField('风格编码', null=True, blank=True, max_length=10)
    old_gray_weight=models.DecimalField('胚纱克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_density=models.CharField('密度', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=20)
    old_stock_unit=models.IntegerField('库存单位', null=True, blank=True)
    old_price_unit=models.IntegerField('计价单位编码', null=True, blank=True)
    old_place=models.CharField('存放位置', null=True, blank=True, max_length=100)
    old_gray_price=models.DecimalField('胚纱价格', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prod_price=models.DecimalField('成品价格', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prod_weight=models.DecimalField('成品克重', null=True, blank=True, max_digits=6, decimal_places=2)
    old_mnemonic=models.CharField('助记符', null=True, blank=True, max_length=10)
    old_graphic=models.BinaryField('图案', null=True, blank=True, editable=True)
    old_is_sample=models.BooleanField('样品否', null=True, blank=True)
    old_is_stop=models.BooleanField('停用否', null=True, blank=True)
    old_stop_date=models.DateTimeField('停用时间', null=True, blank=True)
    old_width_dn=models.DecimalField('门幅下限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_width_up=models.DecimalField('门幅上限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_production_id=models.CharField('工序路私', null=True, blank=True, max_length=20)
    old_real_loss=models.DecimalField('RealLoss', null=True, blank=True, max_digits=6, decimal_places=2)
    old_add_loss=models.DecimalField('AddLoss', null=True, blank=True, max_digits=10, decimal_places=2)
    old_cust_self_product=models.CharField('客户规格', null=True, blank=True, max_length=150)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=50)
    old_old_gray_id=models.CharField('旧编号', null=True, blank=True, max_length=120)
    old_pcs=models.IntegerField('粒/件', null=True, blank=True)
    old_father_gray_id=models.CharField('父系规格', null=True, blank=True, max_length=50)
    old_jnkind=models.CharField('加捻分类', null=True, blank=True, max_length=50)
    old_stkind=models.CharField('松筒分类', null=True, blank=True, max_length=50)
    old_ztkind=models.CharField('装缸脱水分类', null=True, blank=True, max_length=50)
    old_rskind=models.CharField('染色分类', null=True, blank=True, max_length=50)
    old_jtkind=models.CharField('紧筒分类', null=True, blank=True, max_length=50)
    old_cheng_ben0=models.DecimalField('染色成本', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben1=models.DecimalField('前纺成本', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben2=models.DecimalField('后纺成本', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben3=models.DecimalField('加捻成本', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben4=models.DecimalField('包装成本', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cheng_ben5=models.DecimalField('合股夹纱成本', null=True, blank=True, max_digits=6, decimal_places=2)
    old_ji_jian_piece0=models.DecimalField('JiJianPiece0', null=True, blank=True, max_digits=6, decimal_places=2)
    old_ji_jian_piece1=models.DecimalField('JiJianPiece1', null=True, blank=True, max_digits=6, decimal_places=2)
    old_ji_jian_piece2=models.DecimalField('JiJianPiece2', null=True, blank=True, max_digits=6, decimal_places=2)
    old_ji_jian_piece3=models.DecimalField('JiJianPiece3', null=True, blank=True, max_digits=6, decimal_places=2)
    old_ji_jian_piece4=models.DecimalField('JiJianPiece4', null=True, blank=True, max_digits=6, decimal_places=2)
    old_ji_jian_piece5=models.DecimalField('JiJianPiece5', null=True, blank=True, max_digits=6, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_gray'
        indexes=[models.Index(fields=['source_batch', 'old_gray_id'],name='src_33caf3851bedd32d')]
        verbose_name=verbose_name_plural='坯布'
        ordering=["-id"]

class SourceDyePGrayBak(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_GrayBak'
    SOURCE_FIELDS={'GrayID': 'old_gray_id', 'NameC': 'old_name_c', 'NameE': 'old_name_e', 'Spec': 'old_spec', 'Structure': 'old_structure', 'FabricKindID': 'old_fabric_kind_id', 'FabricStyleID': 'old_fabric_style_id', 'GrayWeight': 'old_gray_weight', 'Density': 'old_density', 'ColorID': 'old_color_id', 'StockUnit': 'old_stock_unit', 'PriceUnit': 'old_price_unit', 'Place': 'old_place', 'GrayPrice': 'old_gray_price', 'ProdPrice': 'old_prod_price', 'ProdWeight': 'old_prod_weight', 'Mnemonic': 'old_mnemonic', 'Graphic': 'old_graphic', 'IsSample': 'old_is_sample', 'IsStop': 'old_is_stop', 'StopDate': 'old_stop_date', 'WidthDn': 'old_width_dn', 'WidthUp': 'old_width_up', 'Description': 'old_description', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ProductionID': 'old_production_id', 'RealLoss': 'old_real_loss', 'AddLoss': 'old_add_loss', 'CustSelfProduct': 'old_cust_self_product', 'Width': 'old_width', 'Weight': 'old_weight', 'ZhiTong': 'old_zhi_tong', 'KongJi': 'old_kong_ji', 'ProportionOfComponents': 'old_proportion_of_components', 'shaguan': 'old_shaguan', 'jianju': 'old_jianju', 'CustomerID': 'old_customer_id', 'FabricID': 'old_fabric_id'}
    SOURCE_KEY=('GrayID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_gray_id=models.CharField('GrayID', null=False, blank=True, max_length=20)
    old_name_c=models.CharField('NameC', null=True, blank=True, max_length=200)
    old_name_e=models.CharField('NameE', null=True, blank=True, max_length=60)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=50)
    old_structure=models.CharField('Structure', null=True, blank=True, max_length=50)
    old_fabric_kind_id=models.CharField('FabricKindID', null=True, blank=True, max_length=10)
    old_fabric_style_id=models.CharField('FabricStyleID', null=True, blank=True, max_length=10)
    old_gray_weight=models.DecimalField('GrayWeight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_density=models.CharField('Density', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=20)
    old_stock_unit=models.IntegerField('StockUnit', null=True, blank=True)
    old_price_unit=models.IntegerField('PriceUnit', null=True, blank=True)
    old_place=models.CharField('Place', null=True, blank=True, max_length=100)
    old_gray_price=models.DecimalField('GrayPrice', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prod_price=models.DecimalField('ProdPrice', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prod_weight=models.DecimalField('ProdWeight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_mnemonic=models.CharField('Mnemonic', null=True, blank=True, max_length=10)
    old_graphic=models.BinaryField('Graphic', null=True, blank=True, editable=True)
    old_is_sample=models.BooleanField('IsSample', null=True, blank=True)
    old_is_stop=models.BooleanField('IsStop', null=True, blank=True)
    old_stop_date=models.DateTimeField('StopDate', null=True, blank=True)
    old_width_dn=models.DecimalField('WidthDn', null=True, blank=True, max_digits=6, decimal_places=2)
    old_width_up=models.DecimalField('WidthUp', null=True, blank=True, max_digits=6, decimal_places=2)
    old_description=models.CharField('Description', null=True, blank=True, max_length=100)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_production_id=models.CharField('ProductionID', null=True, blank=True, max_length=20)
    old_real_loss=models.DecimalField('RealLoss', null=True, blank=True, max_digits=6, decimal_places=2)
    old_add_loss=models.DecimalField('AddLoss', null=True, blank=True, max_digits=10, decimal_places=2)
    old_cust_self_product=models.CharField('CustSelfProduct', null=True, blank=True, max_length=200)
    old_width=models.CharField('Width', null=True, blank=True, max_length=50)
    old_weight=models.CharField('Weight', null=True, blank=True, max_length=50)
    old_zhi_tong=models.FloatField('ZhiTong', null=True, blank=True)
    old_kong_ji=models.FloatField('KongJi', null=True, blank=True)
    old_proportion_of_components=models.CharField('ProportionOfComponents', null=True, blank=True, max_length=50)
    old_shaguan=models.CharField('shaguan', null=True, blank=True, max_length=20)
    old_jianju=models.CharField('jianju', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=50)
    old_fabric_id=models.CharField('FabricID', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_graybak'
        indexes=[models.Index(fields=['source_batch', 'old_gray_id'],name='src_75e428103fc0fd8f')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（p_GrayBak，待确认）'
        ordering=["-id"]

class SourceDyePITOnRest(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_ITOnRest'
    SOURCE_FIELDS={'EmpID': 'old_emp_id', 'RowNo': 'old_row_no', 'Kind': 'old_kind', 'DayNum': 'old_day_num', 'BeginTime': 'old_begin_time', 'EndTime': 'old_end_time'}
    SOURCE_KEY=('EmpID', 'RowNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_emp_id=models.CharField('EmpID', null=False, blank=True, max_length=50)
    old_row_no=models.IntegerField('RowNo', null=False, blank=False)
    old_kind=models.IntegerField('类型：临时；每周', null=True, blank=True)
    old_day_num=models.IntegerField('DayNum', null=True, blank=True)
    old_begin_time=models.DateTimeField('BeginTime', null=True, blank=True)
    old_end_time=models.DateTimeField('EndTime', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_itonrest'
        indexes=[models.Index(fields=['source_batch', 'old_emp_id', 'old_row_no'],name='src_f487382f1936829f')]
        verbose_name=verbose_name_plural='基础主数据相关表（p_ITOnRest，待确认）'
        ordering=["-id"]

class SourceDyePITWatch(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_ITWatch'
    SOURCE_FIELDS={'EmpID': 'old_emp_id', 'WorkBegin': 'old_work_begin', 'WorkEnd': 'old_work_end', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('EmpID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_emp_id=models.CharField('EmpID', null=False, blank=True, max_length=50)
    old_work_begin=models.TimeField('WorkBegin', null=True, blank=True)
    old_work_end=models.TimeField('WorkEnd', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=200)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_itwatch'
        indexes=[models.Index(fields=['source_batch', 'old_emp_id'],name='src_83181d664792ecab')]
        verbose_name=verbose_name_plural='基础主数据相关表（p_ITWatch，待确认）'
        ordering=["-id"]

class SourceDyePLable(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Lable'
    SOURCE_FIELDS={'LableID': 'old_lable_id', 'CustomerID': 'old_customer_id', 'LableName': 'old_lable_name', 'LableKind': 'old_lable_kind', 'SpecData': 'old_spec_data', 'FabricID': 'old_fabric_id', 'FabricNameC': 'old_fabric_name_c', 'FabricNameE': 'old_fabric_name_e', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'Grade': 'old_grade', 'Color': 'old_color', 'ShortName': 'old_short_name', 'FullName': 'old_full_name', 'BarCode': 'old_bar_code', 'JobMainNo': 'old_job_main_no', 'Meter': 'old_meter', 'JobDetailNo': 'old_job_detail_no', 'Kg': 'old_kg', 'Pound': 'old_pound', 'Yard': 'old_yard', 'Width': 'old_width', 'Thick': 'old_thick', 'StopDate': 'old_stop_date', 'Description': 'old_description', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer'}
    SOURCE_KEY=('LableID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_lable_id=models.CharField('LableID', null=False, blank=True, max_length=10)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_lable_name=models.CharField('LableName', null=True, blank=True, max_length=50)
    old_lable_kind=models.IntegerField('LableKind', null=True, blank=True)
    old_spec_data=models.BinaryField('SpecData', null=True, blank=True, editable=True)
    old_fabric_id=models.CharField('FabricID', null=True, blank=True, max_length=128)
    old_fabric_name_c=models.CharField('FabricNameC', null=True, blank=True, max_length=50)
    old_fabric_name_e=models.CharField('FabricNameE', null=True, blank=True, max_length=50)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=50)
    old_grade=models.CharField('Grade', null=True, blank=True, max_length=10)
    old_color=models.CharField('Color', null=True, blank=True, max_length=20)
    old_short_name=models.CharField('ShortName', null=True, blank=True, max_length=50)
    old_full_name=models.CharField('FullName', null=True, blank=True, max_length=60)
    old_bar_code=models.CharField('BarCode', null=True, blank=True, max_length=50)
    old_job_main_no=models.CharField('JobMainNo', null=True, blank=True, max_length=20)
    old_meter=models.DecimalField('Meter', null=True, blank=True, max_digits=10, decimal_places=2)
    old_job_detail_no=models.CharField('JobDetailNo', null=True, blank=True, max_length=20)
    old_kg=models.DecimalField('Kg', null=True, blank=True, max_digits=10, decimal_places=2)
    old_pound=models.DecimalField('Pound', null=True, blank=True, max_digits=10, decimal_places=2)
    old_yard=models.DecimalField('Yard', null=True, blank=True, max_digits=10, decimal_places=2)
    old_width=models.DecimalField('Width', null=True, blank=True, max_digits=6, decimal_places=2)
    old_thick=models.DecimalField('Thick', null=True, blank=True, max_digits=6, decimal_places=2)
    old_stop_date=models.DateTimeField('StopDate', null=True, blank=True)
    old_description=models.CharField('Description', null=True, blank=True, max_length=100)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_lable'
        indexes=[models.Index(fields=['source_batch', 'old_lable_id'],name='src_852e24b0c2b5c10c')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（p_Lable，待确认）'
        ordering=["-id"]

class SourceDyePMachine(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Machine'
    SOURCE_FIELDS={'MachineID': 'old_machine_id', 'Name': 'old_name', 'MachineKindID': 'old_machine_kind_id', 'WorkShopID': 'old_work_shop_id', 'StationID': 'old_station_id', 'Description': 'old_description', 'KindName': 'old_kind_name', 'MaxRolls': 'old_max_rolls', 'MAxSpindles': 'old_max_spindles', 'Rate': 'old_rate', 'bit1': 'old_bit1', 'bit2': 'old_bit2', 'bit3': 'old_bit3', 'bit4': 'old_bit4', 'bit5': 'old_bit5', 'bit6': 'old_bit6', 'bit7': 'old_bit7', 'bit8': 'old_bit8', 'IPAddress': 'old_ipaddress', 'IsStop': 'old_is_stop', 'StopDate': 'old_stop_date', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'MachineNo': 'old_machine_no', 'Speed': 'old_speed', 'MachineType': 'old_machine_type', 'NameE': 'old_name_e', 'PreMinutes': 'old_pre_minutes', 'Ports': 'old_ports', 'OPCs': 'old_opcs', 'IsMain': 'old_is_main', 'Model': 'old_model', 'Spec': 'old_spec', 'Power': 'old_power', 'Purpose': 'old_purpose', 'Manufacturer': 'old_manufacturer', 'ProduceDate': 'old_produce_date', 'ManufactureNo': 'old_manufacture_no', 'Supplier': 'old_supplier', 'Capacity': 'old_capacity', 'UnitStr': 'old_unit_str', 'AcceptDate': 'old_accept_date', 'InDate': 'old_in_date', 'DeptID': 'old_dept_id', 'Place': 'old_place', 'MinVatQty': 'old_min_vat_qty', 'MaxWaitVats': 'old_max_wait_vats', 'SequenceNo': 'old_sequence_no', 'IsProcess': 'old_is_process', 'MachineIndex': 'old_machine_index', 'BusinessUnitID': 'old_business_unit_id', 'MachineStatus': 'old_machine_status', 'MachineClass': 'old_machine_class'}
    SOURCE_KEY=('MachineID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_machine_id=models.CharField('机台编码', null=False, blank=True, max_length=20)
    old_name=models.CharField('机台名称', null=True, blank=True, max_length=60)
    old_machine_kind_id=models.CharField('机型代码', null=True, blank=True, max_length=10)
    old_work_shop_id=models.CharField('生产车间代码', null=True, blank=True, max_length=10)
    old_station_id=models.CharField('站别代码', null=True, blank=True, max_length=10)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    old_kind_name=models.CharField('机台类别', null=True, blank=True, max_length=100)
    old_max_rolls=models.IntegerField('最大粒数', null=True, blank=True)
    old_max_spindles=models.IntegerField('最大锭数', null=True, blank=True)
    old_rate=models.DecimalField('水比', null=True, blank=True, max_digits=7, decimal_places=1)
    old_bit1=models.BooleanField('设备巡检', null=True, blank=True)
    old_bit2=models.BooleanField('配件更换', null=True, blank=True)
    old_bit3=models.BooleanField('器具巡检', null=True, blank=True)
    old_bit4=models.BooleanField('暂空', null=True, blank=True)
    old_bit5=models.BooleanField('部位润滑', null=True, blank=True)
    old_bit6=models.BooleanField('清洁卫生', null=True, blank=True)
    old_bit7=models.BooleanField('安全检查', null=True, blank=True)
    old_bit8=models.BooleanField('暂空', null=True, blank=True)
    old_ipaddress=models.CharField('IP地址', null=True, blank=True, max_length=25)
    old_is_stop=models.BooleanField('是否停用', null=True, blank=True)
    old_stop_date=models.DateTimeField('停用时间', null=True, blank=True)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_machine_no=models.IntegerField('机台编号', null=True, blank=True)
    old_speed=models.DecimalField('转速', null=True, blank=True, max_digits=8, decimal_places=2)
    old_machine_type=models.IntegerField('机型', null=True, blank=True)
    old_name_e=models.CharField('NameE', null=True, blank=True, max_length=128)
    old_pre_minutes=models.IntegerField('PreMinutes', null=True, blank=True)
    old_ports=models.IntegerField('Ports', null=True, blank=True)
    old_opcs=models.IntegerField('OPCs', null=True, blank=True)
    old_is_main=models.BooleanField('IsMain', null=True, blank=True)
    old_model=models.CharField('电视分组显示', null=True, blank=True, max_length=20)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=200)
    old_power=models.CharField('Power', null=True, blank=True, max_length=20)
    old_purpose=models.CharField('Purpose', null=True, blank=True, max_length=100)
    old_manufacturer=models.CharField('制造商', null=True, blank=True, max_length=64)
    old_produce_date=models.DateTimeField('ProduceDate', null=True, blank=True)
    old_manufacture_no=models.CharField('ManufactureNo', null=True, blank=True, max_length=50)
    old_supplier=models.CharField('Supplier', null=True, blank=True, max_length=100)
    old_capacity=models.DecimalField('Capacity', null=True, blank=True, max_digits=10, decimal_places=2)
    old_unit_str=models.CharField('UnitStr', null=True, blank=True, max_length=6)
    old_accept_date=models.DateTimeField('AcceptDate', null=True, blank=True)
    old_in_date=models.DateTimeField('InDate', null=True, blank=True)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=10)
    old_place=models.CharField('Place', null=True, blank=True, max_length=100)
    old_min_vat_qty=models.DecimalField('MinVatQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_max_wait_vats=models.DecimalField('MaxWaitVats', null=True, blank=True, max_digits=6, decimal_places=1)
    old_sequence_no=models.CharField('SequenceNo', null=True, blank=True, max_length=50)
    old_is_process=models.BooleanField('IsProcess', null=True, blank=True)
    old_machine_index=models.IntegerField('MachineIndex', null=True, blank=True)
    old_business_unit_id=models.CharField('分厂', null=True, blank=True, max_length=20)
    old_machine_status=models.CharField('MachineStatus', null=True, blank=True, max_length=10)
    old_machine_class=models.CharField('MachineClass', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_machine'
        indexes=[models.Index(fields=['source_batch', 'old_machine_id'],name='src_2251675a260d9080')]
        verbose_name=verbose_name_plural='机台设备'
        ordering=["-id"]

class SourceDyePMachineColor(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_MachineColor'
    SOURCE_FIELDS={'MachineID': 'old_machine_id', 'ColorDepthID': 'old_color_depth_id', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('MachineID', 'ColorDepthID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Machine', 'target': 'erp_base.SourceDyePMachine', 'source_fields': ['MachineID'], 'target_fields': ['MachineID'], 'evidence': ['原界面主从 p_MachineColor → p_Machine']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_machine_id=models.CharField('机台编码', null=False, blank=True, max_length=10)
    old_color_depth_id=models.CharField('颜色深浅', null=False, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=300)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePMachine', verbose_name='原关系：p_Machine', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_machinecolor'
        indexes=[models.Index(fields=['source_batch', 'old_machine_id', 'old_color_depth_id'],name='src_c6075b78f3d08783')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（p_MachineColor，待确认）'
        ordering=["-id"]

class SourceDyePMachineFaultClass(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_MachineFaultClass'
    SOURCE_FIELDS={'RecordID': 'old_record_id', 'SortNo': 'old_sort_no', 'Class1': 'old_class1', 'Class2': 'old_class2', 'Class3': 'old_class3', 'EmpGroup': 'old_emp_group'}
    SOURCE_KEY=('Class1', 'Class2', 'Class3')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_record_id': ('uuid', None), 'old_sort_no': ('literal', ''), 'old_class1': ('literal', ''), 'old_class2': ('literal', ''), 'old_class3': ('literal', ''), 'old_emp_group': ('literal', '')}
    SOURCE_IDENTITIES=()
    old_record_id=models.UUIDField('唯一ID', null=False, blank=False)
    old_sort_no=models.CharField('序号', null=False, blank=True, max_length=10)
    old_class1=models.CharField('一级分类', null=False, blank=True, max_length=50)
    old_class2=models.CharField('二级分类', null=False, blank=True, max_length=50)
    old_class3=models.CharField('三级分类', null=False, blank=True, max_length=50)
    old_emp_group=models.CharField('维修分组', null=False, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_machinefaultclass'
        indexes=[models.Index(fields=['source_batch', 'old_class1', 'old_class2', 'old_class3'],name='src_b75cf3ceaf731e75')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（p_MachineFaultClass，待确认）'
        ordering=["-id"]

class SourceDyePMachineFaultStatus(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_MachineFaultStatus'
    SOURCE_FIELDS={'StatusID': 'old_status_id', 'StatusName': 'old_status_name', 'StatusType': 'old_status_type', 'FontColor': 'old_font_color', 'BackColor': 'old_back_color', 'TypeFontColor': 'old_type_font_color', 'TypeBackColor': 'old_type_back_color', 'CompleteStatus': 'old_complete_status'}
    SOURCE_KEY=('StatusID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_status_id': ('literal', 0), 'old_status_name': ('literal', ''), 'old_status_type': ('literal', ''), 'old_complete_status': ('literal', '')}
    SOURCE_IDENTITIES=()
    old_status_id=models.IntegerField('StatusID', null=False, blank=False)
    old_status_name=models.CharField('StatusName', null=False, blank=True, max_length=20)
    old_status_type=models.CharField('StatusType', null=False, blank=True, max_length=20)
    old_font_color=models.CharField('FontColor', null=True, blank=True, max_length=10)
    old_back_color=models.CharField('BackColor', null=True, blank=True, max_length=10)
    old_type_font_color=models.CharField('TypeFontColor', null=True, blank=True, max_length=10)
    old_type_back_color=models.CharField('TypeBackColor', null=True, blank=True, max_length=10)
    old_complete_status=models.CharField('CompleteStatus', null=False, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_machinefaultstatus'
        indexes=[models.Index(fields=['source_batch', 'old_status_id'],name='src_dbd8e72bc16b9090')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（p_MachineFaultStatus，待确认）'
        ordering=["-id"]

class SourceDyePMachinePart(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_MachinePart'
    SOURCE_FIELDS={'MachineID': 'old_machine_id', 'PartID': 'old_part_id', 'PartName': 'old_part_name', 'ArticleID': 'old_article_id', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('MachineID', 'PartID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Machine', 'target': 'erp_base.SourceDyePMachine', 'source_fields': ['MachineID'], 'target_fields': ['MachineID'], 'evidence': ['原界面主从 p_MachinePart → p_Machine']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_machine_id=models.CharField('机台编码', null=False, blank=True, max_length=10)
    old_part_id=models.CharField('部位编码', null=False, blank=True, max_length=10)
    old_part_name=models.CharField('部位名称', null=True, blank=True, max_length=50)
    old_article_id=models.CharField('物料代码', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePMachine', verbose_name='原关系：p_Machine', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_machinepart'
        indexes=[models.Index(fields=['source_batch', 'old_machine_id', 'old_part_id'],name='src_3ee98e8c38b37c40')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（p_MachinePart，待确认）'
        ordering=["-id"]

class SourceDyePMachinePoint(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_MachinePoint'
    SOURCE_FIELDS={'MachineID': 'old_machine_id', 'PointNo': 'old_point_no', 'PortID': 'old_port_id', 'ModuleID': 'old_module_id', 'ChannelNo': 'old_channel_no', 'ParamID': 'old_param_id', 'PPName': 'old_ppname', 'Remarks': 'old_remarks', 'PointType': 'old_point_type', 'PointPlace': 'old_point_place', 'Precision': 'old_precision', 'MethodID': 'old_method_id', 'Express': 'old_express', 'MeterID': 'old_meter_id', 'AlarmDelta': 'old_alarm_delta', 'CommunicatWay': 'old_communicat_way', 'IsNotShow': 'old_is_not_show', 'AddrNo': 'old_addr_no', 'GatherWay': 'old_gather_way', 'BelongPart': 'old_belong_part', 'EnergyCutRatio': 'old_energy_cut_ratio', 'IsCompare': 'old_is_compare'}
    SOURCE_KEY=('MachineID', 'PointNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Machine', 'target': 'erp_base.SourceDyePMachine', 'source_fields': ['MachineID'], 'target_fields': ['MachineID'], 'evidence': ['原界面主从 p_MachinePoint → p_Machine']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_machine_id=models.CharField('机台号', null=False, blank=True, max_length=10)
    old_point_no=models.IntegerField('采控点编号', null=False, blank=False)
    old_port_id=models.CharField('串口编号', null=True, blank=True, max_length=10)
    old_module_id=models.CharField('模块编号', null=True, blank=True, max_length=10)
    old_channel_no=models.IntegerField('通道号', null=True, blank=True)
    old_param_id=models.CharField('参数编码', null=True, blank=True, max_length=10)
    old_ppname=models.CharField('参数名称', null=True, blank=True, max_length=20)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_point_type=models.IntegerField('采控点类别', null=True, blank=True)
    old_point_place=models.IntegerField('采控点位置', null=True, blank=True)
    old_precision=models.IntegerField('存储精度', null=True, blank=True)
    old_method_id=models.CharField('通讯方法编码', null=True, blank=True, max_length=10)
    old_express=models.CharField('表达式', null=True, blank=True, max_length=500)
    old_meter_id=models.CharField('仪表编号', null=True, blank=True, max_length=10)
    old_alarm_delta=models.DecimalField('AlarmDelta', null=True, blank=True, max_digits=10, decimal_places=2)
    old_communicat_way=models.IntegerField('CommunicatWay', null=True, blank=True)
    old_is_not_show=models.BooleanField('IsNotShow', null=True, blank=True)
    old_addr_no=models.CharField('AddrNo', null=True, blank=True, max_length=12)
    old_gather_way=models.CharField('GatherWay', null=True, blank=True, max_length=1)
    old_belong_part=models.IntegerField('BelongPart', null=True, blank=True)
    old_energy_cut_ratio=models.DecimalField('EnergyCutRatio', null=True, blank=True, max_digits=3, decimal_places=2)
    old_is_compare=models.BooleanField('是否执行对比', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePMachine', verbose_name='原关系：p_Machine', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_machinepoint'
        indexes=[models.Index(fields=['source_batch', 'old_machine_id', 'old_point_no'],name='src_7309469eb4a46afe')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（p_MachinePoint，待确认）'
        ordering=["-id"]

class SourceDyePMachinePort(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_MachinePort'
    SOURCE_FIELDS={'MachineID': 'old_machine_id', 'PortNum': 'old_port_num', 'BaudRate': 'old_baud_rate', 'StopBits': 'old_stop_bits', 'DataBits': 'old_data_bits', 'Parity': 'old_parity', 'WriteInterval': 'old_write_interval', 'Points': 'old_points', 'IPAddress': 'old_ipaddress'}
    SOURCE_KEY=('MachineID', 'PortNum')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_machine_id=models.CharField('MachineID', null=False, blank=True, max_length=10)
    old_port_num=models.IntegerField('PortNum', null=False, blank=False)
    old_baud_rate=models.CharField('BaudRate', null=True, blank=True, max_length=10)
    old_stop_bits=models.IntegerField('StopBits', null=True, blank=True)
    old_data_bits=models.IntegerField('DataBits', null=True, blank=True)
    old_parity=models.CharField('Parity', null=True, blank=True, max_length=15)
    old_write_interval=models.IntegerField('WriteInterval', null=True, blank=True)
    old_points=models.IntegerField('Points', null=True, blank=True)
    old_ipaddress=models.CharField('IPAddress', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_machineport'
        indexes=[models.Index(fields=['source_batch', 'old_machine_id', 'old_port_num'],name='src_f7eaaf6bd70b7963')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（p_MachinePort，待确认）'
        ordering=["-id"]

class SourceDyePMachineProcess(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_MachineProcess'
    SOURCE_FIELDS={'MachineID': 'old_machine_id', 'ProcessID': 'old_process_id', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('MachineID', 'ProcessID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Machine', 'target': 'erp_base.SourceDyePMachine', 'source_fields': ['MachineID'], 'target_fields': ['MachineID'], 'evidence': ['原界面主从 p_MachineProcess → p_Machine']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_machine_id=models.CharField('机台编号', null=False, blank=True, max_length=10)
    old_process_id=models.CharField('工序代码', null=False, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=300)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePMachine', verbose_name='原关系：p_Machine', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_machineprocess'
        indexes=[models.Index(fields=['source_batch', 'old_machine_id', 'old_process_id'],name='src_f5c5cd684093076c')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（p_MachineProcess，待确认）'
        ordering=["-id"]

class SourceDyePMachineProd(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_MachineProd'
    SOURCE_FIELDS={'MachineID': 'old_machine_id', 'ProdKindID': 'old_prod_kind_id', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('MachineID', 'ProdKindID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Machine', 'target': 'erp_base.SourceDyePMachine', 'source_fields': ['MachineID'], 'target_fields': ['MachineID'], 'evidence': ['原界面主从 p_MachineProd → p_Machine']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_machine_id=models.CharField('机台编码', null=False, blank=True, max_length=10)
    old_prod_kind_id=models.CharField('纱种分类编码', null=False, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=300)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePMachine', verbose_name='原关系：p_Machine', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_machineprod'
        indexes=[models.Index(fields=['source_batch', 'old_machine_id', 'old_prod_kind_id'],name='src_e371f534c7d6fef3')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（p_MachineProd，待确认）'
        ordering=["-id"]

class SourceDyePMachineShift(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_MachineShift'
    SOURCE_FIELDS={'MachineID': 'old_machine_id', 'ShiftID': 'old_shift_id'}
    SOURCE_KEY=('MachineID', 'ShiftID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_machine_id=models.CharField('MachineID', null=False, blank=True, max_length=20)
    old_shift_id=models.CharField('ShiftID', null=False, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_machineshift'
        indexes=[models.Index(fields=['source_batch', 'old_machine_id', 'old_shift_id'],name='src_7eefecaa60bfa8e8')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（p_MachineShift，待确认）'
        ordering=["-id"]

class SourceDyePMeter(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Meter'
    SOURCE_FIELDS={'MeterID': 'old_meter_id', 'Name': 'old_name', 'Spec': 'old_spec', 'DeptID': 'old_dept_id', 'ClassID': 'old_class_id', 'ParentMeterID': 'old_parent_meter_id', 'AddrNo': 'old_addr_no', 'Manufacturer': 'old_manufacturer', 'Place': 'old_place', 'EnergyKind': 'old_energy_kind', 'GatherWay': 'old_gather_way', 'LastAdjustTime': 'old_last_adjust_time', 'LastCommTime': 'old_last_comm_time', 'LimitDays': 'old_limit_days', 'Ratio': 'old_ratio', 'Status': 'old_status', 'Remarks': 'old_remarks', 'IPAddress': 'old_ipaddress', 'RegisterAddress': 'old_register_address', 'RegisterNumber': 'old_register_number', 'MeasureGrade': 'old_measure_grade', 'ReadQty': 'old_read_qty', 'GroupNo': 'old_group_no', 'MaxValue': 'old_max_value', 'PortID': 'old_port_id', 'Multiple': 'old_multiple', 'DayStartReadQty': 'old_day_start_read_qty', 'IsContrast': 'old_is_contrast', 'FuncCode': 'old_func_code', 'CommunicatWay': 'old_communicat_way', 'CommStr': 'old_comm_str', 'Error_Check': 'old_error_check', 'ParseWay': 'old_parse_way', 'GatherKind': 'old_gather_kind', 'IsStop': 'old_is_stop', 'Mnemonic': 'old_mnemonic', 'Model': 'old_model'}
    SOURCE_KEY=('MeterID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_meter_id=models.CharField('仪表编号', null=False, blank=True, max_length=10)
    old_name=models.CharField('名称', null=True, blank=True, max_length=500)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=200)
    old_dept_id=models.CharField('部门编码', null=True, blank=True, max_length=10)
    old_class_id=models.CharField('班别代码', null=True, blank=True, max_length=10)
    old_parent_meter_id=models.CharField('父表代码', null=True, blank=True, max_length=10)
    old_addr_no=models.CharField('地址号', null=True, blank=True, max_length=12)
    old_manufacturer=models.CharField('生产厂家', null=True, blank=True, max_length=100)
    old_place=models.CharField('存放位置', null=True, blank=True, max_length=100)
    old_energy_kind=models.IntegerField('能耗类型', null=True, blank=True)
    old_gather_way=models.CharField('采集方式', null=True, blank=True, max_length=1)
    old_last_adjust_time=models.DateTimeField('最后校准时间', null=True, blank=True)
    old_last_comm_time=models.DateTimeField('最后通讯时间', null=True, blank=True)
    old_limit_days=models.IntegerField('收款期限', null=True, blank=True)
    old_ratio=models.DecimalField('比例', null=True, blank=True, max_digits=12, decimal_places=5)
    old_status=models.CharField('状态', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_ipaddress=models.CharField('IP地址', null=True, blank=True, max_length=50)
    old_register_address=models.CharField('寄存器地址', null=True, blank=True, max_length=10)
    old_register_number=models.CharField('寄存器数量', null=True, blank=True, max_length=10)
    old_measure_grade=models.IntegerField('能源计量级别', null=True, blank=True)
    old_read_qty=models.DecimalField('读数', null=True, blank=True, max_digits=18, decimal_places=6)
    old_group_no=models.CharField('分组号', null=True, blank=True, max_length=20)
    old_max_value=models.DecimalField('最大值', null=True, blank=True, max_digits=10, decimal_places=2)
    old_port_id=models.CharField('串口编号', null=True, blank=True, max_length=10)
    old_multiple=models.DecimalField('Multiple', null=True, blank=True, max_digits=12, decimal_places=6)
    old_day_start_read_qty=models.DecimalField('DayStartReadQty', null=True, blank=True, max_digits=10, decimal_places=2)
    old_is_contrast=models.BooleanField('IsContrast', null=True, blank=True)
    old_func_code=models.CharField('FuncCode', null=True, blank=True, max_length=20)
    old_communicat_way=models.IntegerField('CommunicatWay', null=True, blank=True)
    old_comm_str=models.CharField('CommStr', null=True, blank=True, max_length=200)
    old_error_check=models.CharField('Error_Check', null=True, blank=True, max_length=5)
    old_parse_way=models.IntegerField('ParseWay', null=True, blank=True)
    old_gather_kind=models.IntegerField('GatherKind', null=True, blank=True)
    old_is_stop=models.BooleanField('是否停用', null=True, blank=True)
    old_mnemonic=models.CharField('Mnemonic', null=True, blank=True, max_length=200)
    old_model=models.CharField('分组统计', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_meter'
        indexes=[models.Index(fields=['source_batch', 'old_meter_id'],name='src_89c4ce56e843783d')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（p_Meter，待确认）'
        ordering=["-id"]

class SourceDyePMeterAlarm(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_MeterAlarm'
    SOURCE_FIELDS={'MeterID': 'old_meter_id', 'PortNum': 'old_port_num', 'AddrNo': 'old_addr_no', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('MeterID', 'PortNum', 'AddrNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_meter_id=models.CharField('MeterID', null=False, blank=True, max_length=10)
    old_port_num=models.IntegerField('PortNum', null=False, blank=False)
    old_addr_no=models.CharField('AddrNo', null=False, blank=True, max_length=12)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_meteralarm'
        indexes=[models.Index(fields=['source_batch', 'old_meter_id', 'old_port_num', 'old_addr_no'],name='src_4ad1098718eb022f')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（p_MeterAlarm，待确认）'
        ordering=["-id"]

class SourceDyePMeterMachine(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_MeterMachine'
    SOURCE_FIELDS={'MeterID': 'old_meter_id', 'MachineID': 'old_machine_id', 'Ratio': 'old_ratio', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('MeterID', 'MachineID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Meter', 'target': 'erp_base.SourceDyePMeter', 'source_fields': ['MeterID'], 'target_fields': ['MeterID'], 'evidence': ['原界面主从 p_MeterMachine → p_Meter']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_meter_id=models.CharField('仪表编号', null=False, blank=True, max_length=10)
    old_machine_id=models.CharField('机台编号', null=False, blank=True, max_length=10)
    old_ratio=models.DecimalField('比例', null=True, blank=True, max_digits=12, decimal_places=5)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePMeter', verbose_name='原关系：p_Meter', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_metermachine'
        indexes=[models.Index(fields=['source_batch', 'old_meter_id', 'old_machine_id'],name='src_4f71f13aec08d465')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（p_MeterMachine，待确认）'
        ordering=["-id"]

class SourceDyePPDesign(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_PDesign'
    SOURCE_FIELDS={'DesignNo': 'old_design_no', 'Name': 'old_name', 'CustomerID': 'old_customer_id', 'CustDesignNo': 'old_cust_design_no', 'LabSheetNo': 'old_lab_sheet_no', 'ProdID': 'old_prod_id', 'Spec': 'old_spec', 'Weight': 'old_weight', 'Width': 'old_width', 'PrintKind': 'old_print_kind', 'Colors': 'old_colors', 'Sets': 'old_sets', 'DifficultyID': 'old_difficulty_id', 'GetSampleDate': 'old_get_sample_date', 'ScreenRepeat': 'old_screen_repeat', 'FinishRepeat': 'old_finish_repeat', 'StrikedTime': 'old_striked_time', 'StrikeOffFee': 'old_strike_off_fee', 'ProgramID': 'old_program_id', 'Status': 'old_status', 'IsStop': 'old_is_stop', 'StopDate': 'old_stop_date', 'Description': 'old_description', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'SamplerID': 'old_sampler_id', 'DrawerID': 'old_drawer_id'}
    SOURCE_KEY=('DesignNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_design_no=models.CharField('DesignNo', null=False, blank=True, max_length=50)
    old_name=models.CharField('Name', null=True, blank=True, max_length=60)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_cust_design_no=models.CharField('CustDesignNo', null=True, blank=True, max_length=20)
    old_lab_sheet_no=models.CharField('LabSheetNo', null=True, blank=True, max_length=20)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=20)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=128)
    old_weight=models.DecimalField('Weight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_width=models.DecimalField('Width', null=True, blank=True, max_digits=6, decimal_places=2)
    old_print_kind=models.CharField('PrintKind', null=True, blank=True, max_length=2)
    old_colors=models.IntegerField('Colors', null=True, blank=True)
    old_sets=models.IntegerField('Sets', null=True, blank=True)
    old_difficulty_id=models.CharField('DifficultyID', null=True, blank=True, max_length=10)
    old_get_sample_date=models.DateTimeField('GetSampleDate', null=True, blank=True)
    old_screen_repeat=models.DecimalField('ScreenRepeat', null=True, blank=True, max_digits=7, decimal_places=2)
    old_finish_repeat=models.DecimalField('FinishRepeat', null=True, blank=True, max_digits=7, decimal_places=2)
    old_striked_time=models.DateTimeField('StrikedTime', null=True, blank=True)
    old_strike_off_fee=models.DecimalField('StrikeOffFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_program_id=models.CharField('ProgramID', null=True, blank=True, max_length=10)
    old_status=models.IntegerField('Status', null=True, blank=True)
    old_is_stop=models.BooleanField('IsStop', null=True, blank=True)
    old_stop_date=models.DateTimeField('StopDate', null=True, blank=True)
    old_description=models.CharField('Description', null=True, blank=True, max_length=100)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_sampler_id=models.CharField('SamplerID', null=True, blank=True, max_length=10)
    old_drawer_id=models.CharField('DrawerID', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_pdesign'
        indexes=[models.Index(fields=['source_batch', 'old_design_no'],name='src_3efd66732f89ee12')]
        verbose_name=verbose_name_plural='基础主数据相关表（p_PDesign，待确认）'
        ordering=["-id"]

class SourceDyePPDesignDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_PDesignDetail'
    SOURCE_FIELDS={'DesignNo': 'old_design_no', 'SequenceNo': 'old_sequence_no', 'DetailNo': 'old_detail_no', 'Percent': 'old_percent'}
    SOURCE_KEY=('DesignNo', 'SequenceNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_design_no=models.CharField('DesignNo', null=False, blank=True, max_length=50)
    old_sequence_no=models.BigIntegerField('SequenceNo', null=False, blank=False)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=36)
    old_percent=models.DecimalField('Percent', null=True, blank=True, max_digits=4, decimal_places=3)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_pdesigndetail'
        indexes=[models.Index(fields=['source_batch', 'old_design_no', 'old_sequence_no'],name='src_4c2da12f7e39eb9c')]
        verbose_name=verbose_name_plural='基础主数据相关表（p_PDesignDetail，待确认）'
        ordering=["-id"]

class SourceDyePPDesignSet(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_PDesignSet'
    SOURCE_FIELDS={'DesignNo': 'old_design_no', 'ColorSeries': 'old_color_series', 'ColorID': 'old_color_id', 'ColorNo01': 'old_color_no01', 'ColorRGB01': 'old_color_rgb01', 'ColorNo02': 'old_color_no02', 'ColorRGB02': 'old_color_rgb02', 'ColorNo03': 'old_color_no03', 'ColorRGB03': 'old_color_rgb03', 'ColorNo04': 'old_color_no04', 'ColorRGB04': 'old_color_rgb04', 'ColorNo05': 'old_color_no05', 'ColorRGB05': 'old_color_rgb05', 'ColorNo06': 'old_color_no06', 'ColorRGB06': 'old_color_rgb06', 'ColorNo07': 'old_color_no07', 'ColorRGB07': 'old_color_rgb07', 'ColorNo08': 'old_color_no08', 'ColorRGB08': 'old_color_rgb08', 'ColorNo09': 'old_color_no09', 'ColorRGB09': 'old_color_rgb09', 'ColorNo10': 'old_color_no10', 'ColorRGB10': 'old_color_rgb10', 'ColorNo11': 'old_color_no11', 'ColorRGB11': 'old_color_rgb11', 'ColorNo12': 'old_color_no12', 'ColorRGB12': 'old_color_rgb12', 'ColorNo13': 'old_color_no13', 'ColorRGB13': 'old_color_rgb13', 'ColorNo14': 'old_color_no14', 'ColorRGB14': 'old_color_rgb14', 'ColorNo15': 'old_color_no15', 'ColorRGB15': 'old_color_rgb15', 'ColorNo16': 'old_color_no16', 'ColorRGB16': 'old_color_rgb16', 'ColorNo17': 'old_color_no17', 'ColorRGB17': 'old_color_rgb17', 'ColorNo18': 'old_color_no18', 'ColorRGB18': 'old_color_rgb18', 'ColorNo19': 'old_color_no19', 'ColorRGB19': 'old_color_rgb19', 'ColorNo20': 'old_color_no20', 'ColorRGB20': 'old_color_rgb20', 'SampleFileName': 'old_sample_file_name', 'Description': 'old_description', 'ColorNum': 'old_color_num'}
    SOURCE_KEY=('DesignNo', 'ColorSeries')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_design_no=models.CharField('DesignNo', null=False, blank=True, max_length=50)
    old_color_series=models.CharField('ColorSeries', null=False, blank=True, max_length=20)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=20)
    old_color_no01=models.CharField('ColorNo01', null=True, blank=True, max_length=20)
    old_color_rgb01=models.IntegerField('ColorRGB01', null=True, blank=True)
    old_color_no02=models.CharField('ColorNo02', null=True, blank=True, max_length=20)
    old_color_rgb02=models.IntegerField('ColorRGB02', null=True, blank=True)
    old_color_no03=models.CharField('ColorNo03', null=True, blank=True, max_length=20)
    old_color_rgb03=models.IntegerField('ColorRGB03', null=True, blank=True)
    old_color_no04=models.CharField('ColorNo04', null=True, blank=True, max_length=20)
    old_color_rgb04=models.IntegerField('ColorRGB04', null=True, blank=True)
    old_color_no05=models.CharField('ColorNo05', null=True, blank=True, max_length=20)
    old_color_rgb05=models.IntegerField('ColorRGB05', null=True, blank=True)
    old_color_no06=models.CharField('ColorNo06', null=True, blank=True, max_length=20)
    old_color_rgb06=models.IntegerField('ColorRGB06', null=True, blank=True)
    old_color_no07=models.CharField('ColorNo07', null=True, blank=True, max_length=20)
    old_color_rgb07=models.IntegerField('ColorRGB07', null=True, blank=True)
    old_color_no08=models.CharField('ColorNo08', null=True, blank=True, max_length=20)
    old_color_rgb08=models.IntegerField('ColorRGB08', null=True, blank=True)
    old_color_no09=models.CharField('ColorNo09', null=True, blank=True, max_length=20)
    old_color_rgb09=models.IntegerField('ColorRGB09', null=True, blank=True)
    old_color_no10=models.CharField('ColorNo10', null=True, blank=True, max_length=20)
    old_color_rgb10=models.IntegerField('ColorRGB10', null=True, blank=True)
    old_color_no11=models.CharField('ColorNo11', null=True, blank=True, max_length=20)
    old_color_rgb11=models.IntegerField('ColorRGB11', null=True, blank=True)
    old_color_no12=models.CharField('ColorNo12', null=True, blank=True, max_length=20)
    old_color_rgb12=models.IntegerField('ColorRGB12', null=True, blank=True)
    old_color_no13=models.CharField('ColorNo13', null=True, blank=True, max_length=20)
    old_color_rgb13=models.IntegerField('ColorRGB13', null=True, blank=True)
    old_color_no14=models.CharField('ColorNo14', null=True, blank=True, max_length=20)
    old_color_rgb14=models.IntegerField('ColorRGB14', null=True, blank=True)
    old_color_no15=models.CharField('ColorNo15', null=True, blank=True, max_length=20)
    old_color_rgb15=models.IntegerField('ColorRGB15', null=True, blank=True)
    old_color_no16=models.CharField('ColorNo16', null=True, blank=True, max_length=20)
    old_color_rgb16=models.IntegerField('ColorRGB16', null=True, blank=True)
    old_color_no17=models.CharField('ColorNo17', null=True, blank=True, max_length=20)
    old_color_rgb17=models.IntegerField('ColorRGB17', null=True, blank=True)
    old_color_no18=models.CharField('ColorNo18', null=True, blank=True, max_length=20)
    old_color_rgb18=models.IntegerField('ColorRGB18', null=True, blank=True)
    old_color_no19=models.CharField('ColorNo19', null=True, blank=True, max_length=20)
    old_color_rgb19=models.IntegerField('ColorRGB19', null=True, blank=True)
    old_color_no20=models.CharField('ColorNo20', null=True, blank=True, max_length=20)
    old_color_rgb20=models.IntegerField('ColorRGB20', null=True, blank=True)
    old_sample_file_name=models.CharField('SampleFileName', null=True, blank=True, max_length=200)
    old_description=models.CharField('Description', null=True, blank=True, max_length=100)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_pdesignset'
        indexes=[models.Index(fields=['source_batch', 'old_design_no', 'old_color_series'],name='src_ca7b10e0d4dd609b')]
        verbose_name=verbose_name_plural='基础主数据相关表（p_PDesignSet，待确认）'
        ordering=["-id"]

class SourceDyePPriceList(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_PriceList'
    SOURCE_FIELDS={'ID': 'old_id', 'ProdKindID': 'old_prod_kind_id', 'WeightDn': 'old_weight_dn', 'WeightUp': 'old_weight_up', 'Price': 'old_price', 'Remarks': 'old_remarks', 'StuffKindID': 'old_stuff_kind_id', 'PriceUnit': 'old_price_unit'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.CharField('编码', null=False, blank=True, max_length=50)
    old_prod_kind_id=models.CharField('成品类别', null=True, blank=True, max_length=10)
    old_weight_dn=models.DecimalField('克重下限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight_up=models.DecimalField('克重上限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=300)
    old_stuff_kind_id=models.CharField('染化料类别', null=True, blank=True, max_length=10)
    old_price_unit=models.IntegerField('计价单位', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_pricelist'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_823886776b3cee33')]
        verbose_name=verbose_name_plural='价格表'
        ordering=["-id"]

class SourceDyePPriceListAtte(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_PriceListAtte'
    SOURCE_FIELDS={'ID': 'old_id', 'AtteCode': 'old_atte_code', 'Price': 'old_price'}
    SOURCE_KEY=('ID', 'AtteCode')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.CharField('ID', null=False, blank=True, max_length=20)
    old_atte_code=models.CharField('AtteCode', null=False, blank=True, max_length=10)
    old_price=models.DecimalField('Price', null=True, blank=True, max_digits=8, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_pricelistatte'
        indexes=[models.Index(fields=['source_batch', 'old_id', 'old_atte_code'],name='src_fcd98aa330342269')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（p_PriceListAtte，待确认）'
        ordering=["-id"]

class SourceDyePPriceListColor(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_PriceListColor'
    SOURCE_FIELDS={'ID': 'old_id', 'ColorDepthID': 'old_color_depth_id', 'Price': 'old_price', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('ID', 'ColorDepthID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_PriceList', 'target': 'erp_base.SourceDyePPriceList', 'source_fields': ['ID'], 'target_fields': ['ID'], 'evidence': ['原界面主从 p_PriceListColor → p_PriceList']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.CharField('编码', null=False, blank=True, max_length=50)
    old_color_depth_id=models.CharField('颜色深浅', null=False, blank=True, max_length=10)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=300)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePPriceList', verbose_name='原关系：p_PriceList', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_pricelistcolor'
        indexes=[models.Index(fields=['source_batch', 'old_id', 'old_color_depth_id'],name='src_3e63317a3202bc26')]
        verbose_name=verbose_name_plural='色号价格表'
        ordering=["-id"]

class SourceDyePPriceListProcess(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_PriceListProcess'
    SOURCE_FIELDS={'ID': 'old_id', 'ProcessID': 'old_process_id', 'Price': 'old_price', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('ID', 'ProcessID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_PriceList', 'target': 'erp_base.SourceDyePPriceList', 'source_fields': ['ID'], 'target_fields': ['ID'], 'evidence': ['原界面主从 p_PriceListProcess → p_PriceList']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.CharField('编码', null=False, blank=True, max_length=50)
    old_process_id=models.CharField('另收费工序', null=False, blank=True, max_length=10)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=300)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePPriceList', verbose_name='原关系：p_PriceList', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_pricelistprocess'
        indexes=[models.Index(fields=['source_batch', 'old_id', 'old_process_id'],name='src_ce48c9c0a7b26ee3')]
        verbose_name=verbose_name_plural='工序价格表'
        ordering=["-id"]

class SourceDyePPriceListVat(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_PriceListVat'
    SOURCE_FIELDS={'ID': 'old_id', 'LengthDn': 'old_length_dn', 'LengthUp': 'old_length_up', 'Unit': 'old_unit', 'Price': 'old_price', 'PhaseID': 'old_phase_id'}
    SOURCE_KEY=('ID', 'LengthDn', 'LengthUp')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_PriceList', 'target': 'erp_base.SourceDyePPriceList', 'source_fields': ['ID'], 'target_fields': ['ID'], 'evidence': ['原界面主从 p_PriceListVat → p_PriceList']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.CharField('编码', null=False, blank=True, max_length=50)
    old_length_dn=models.DecimalField('最小长度', null=False, blank=False, max_digits=7, decimal_places=2)
    old_length_up=models.DecimalField('最大长度', null=False, blank=False, max_digits=7, decimal_places=2)
    old_unit=models.IntegerField('收费单位', null=True, blank=True)
    old_price=models.DecimalField('价格', null=True, blank=True, max_digits=8, decimal_places=2)
    old_phase_id=models.CharField('染色流程', null=True, blank=True, max_length=10)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePPriceList', verbose_name='原关系：p_PriceList', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_pricelistvat'
        indexes=[models.Index(fields=['source_batch', 'old_id', 'old_length_dn', 'old_length_up'],name='src_e851c25700d19394')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（p_PriceListVat，待确认）'
        ordering=["-id"]

class SourceDyePProcess(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Process'
    SOURCE_FIELDS={'ProcessID': 'old_process_id', 'Name': 'old_name', 'StationID': 'old_station_id', 'Price': 'old_price', 'EffiRate': 'old_effi_rate', 'CurrLimitHours': 'old_curr_limit_hours', 'SampleLimitHours': 'old_sample_limit_hours', 'ToArrange': 'old_to_arrange', 'ToMainPlan': 'old_to_main_plan', 'ToPopFshBox': 'old_to_pop_fsh_box', 'ToInputMachine': 'old_to_input_machine', 'ToInputQty': 'old_to_input_qty', 'ToWeight': 'old_to_weight', 'IsNeedRecipe': 'old_is_need_recipe', 'IsOverShift': 'old_is_over_shift', 'CanModify': 'old_can_modify', 'CanSkip': 'old_can_skip', 'CalcWay': 'old_calc_way', 'TimeWay': 'old_time_way', 'LinesInCard': 'old_lines_in_card', 'FixCost': 'old_fix_cost', 'StopDate': 'old_stop_date', 'Description': 'old_description', 'Unit': 'old_unit', 'SumLimitHours': 'old_sum_limit_hours', 'ToInputVehicle': 'old_to_input_vehicle', 'IsCanAddWorkQty': 'old_is_can_add_work_qty', 'IsUseWeight': 'old_is_use_weight', 'ReplaceProcessID': 'old_replace_process_id', 'IsPriority': 'old_is_priority', 'DelayHours': 'old_delay_hours', 'IsExtraCharge': 'old_is_extra_charge', 'IsMain': 'old_is_main', 'SortNo': 'old_sort_no', 'ProcessPrice': 'old_process_price', 'BusinessUnitID': 'old_business_unit_id', 'IsODM': 'old_is_odm', 'OverShiftWay': 'old_over_shift_way', 'MaxWorkVats': 'old_max_work_vats', 'MinWorkVats': 'old_min_work_vats', 'InputQtyCheckWay': 'old_input_qty_check_way', 'MaxWorkRolls': 'old_max_work_rolls', 'MaxWorkWeight': 'old_max_work_weight', 'MaxWorkLength': 'old_max_work_length', 'MinWorkLength': 'old_min_work_length', 'MinWorkRolls': 'old_min_work_rolls', 'MinWorkWeight': 'old_min_work_weight', 'WorkDonePercent': 'old_work_done_percent', 'IsCheckPlan': 'old_is_check_plan', 'SortNumber': 'old_sort_number', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'IsAllowedToBack': 'old_is_allowed_to_back', 'ToInputColor': 'old_to_input_color', 'Stereotypes': 'old_stereotypes'}
    SOURCE_KEY=('ProcessID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_process_id=models.CharField('工序代码', null=False, blank=True, max_length=10)
    old_name=models.CharField('名称', null=True, blank=True, max_length=60)
    old_station_id=models.CharField('站别代码', null=True, blank=True, max_length=10)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_effi_rate=models.DecimalField('效率比例', null=True, blank=True, max_digits=6, decimal_places=4)
    old_curr_limit_hours=models.IntegerField('当前工序限时', null=True, blank=True)
    old_sample_limit_hours=models.IntegerField('试样限时', null=True, blank=True)
    old_to_arrange=models.IntegerField('排产', null=True, blank=True)
    old_to_main_plan=models.BooleanField('排主计划', null=True, blank=True)
    old_to_pop_fsh_box=models.BooleanField('结束检查框', null=True, blank=True)
    old_to_input_machine=models.BooleanField('输入机台', null=True, blank=True)
    old_to_input_qty=models.BooleanField('输入数量', null=True, blank=True)
    old_to_weight=models.BooleanField('称重', null=True, blank=True)
    old_is_need_recipe=models.BooleanField('工序配方', null=True, blank=True)
    old_is_over_shift=models.BooleanField('交接班', null=True, blank=True)
    old_can_modify=models.IntegerField('修改重刷', null=True, blank=True)
    old_can_skip=models.BooleanField('跳过', null=True, blank=True)
    old_calc_way=models.IntegerField('统计方法', null=True, blank=True)
    old_time_way=models.IntegerField('刷卡时间', null=True, blank=True)
    old_lines_in_card=models.IntegerField('工卡占行数', null=True, blank=True)
    old_fix_cost=models.DecimalField('固定成本', null=True, blank=True, max_digits=10, decimal_places=6)
    old_stop_date=models.DateTimeField('停用时间', null=True, blank=True)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    old_unit=models.IntegerField('单位(计量，计价)', null=True, blank=True)
    old_sum_limit_hours=models.IntegerField('累计工序限时', null=True, blank=True)
    old_to_input_vehicle=models.BooleanField('输入车桶号', null=True, blank=True)
    old_is_can_add_work_qty=models.BooleanField('允许超出标准产量', null=True, blank=True)
    old_is_use_weight=models.BooleanField('按克重算成本', null=True, blank=True)
    old_replace_process_id=models.CharField('替代工序', null=True, blank=True, max_length=100)
    old_is_priority=models.BooleanField('是否优先', null=True, blank=True)
    old_delay_hours=models.IntegerField('延迟时间', null=True, blank=True)
    old_is_extra_charge=models.BooleanField('是否另收费', null=True, blank=True)
    old_is_main=models.BooleanField('IsMain', null=True, blank=True)
    old_sort_no=models.IntegerField('SortNo', null=True, blank=True)
    old_process_price=models.DecimalField('ProcessPrice', null=True, blank=True, max_digits=8, decimal_places=2)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=20)
    old_is_odm=models.BooleanField('是否委外', null=True, blank=True)
    old_over_shift_way=models.IntegerField('交接班数量检查单位', null=True, blank=True)
    old_max_work_vats=models.DecimalField('最大上卡缸数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_min_work_vats=models.DecimalField('MinWorkVats', null=True, blank=True, max_digits=10, decimal_places=2)
    old_input_qty_check_way=models.IntegerField('工序刷卡产量检查方式', null=True, blank=True)
    old_max_work_rolls=models.DecimalField('MaxWorkRolls', null=True, blank=True, max_digits=10, decimal_places=2)
    old_max_work_weight=models.DecimalField('MaxWorkWeight', null=True, blank=True, max_digits=10, decimal_places=2)
    old_max_work_length=models.DecimalField('MaxWorkLength', null=True, blank=True, max_digits=10, decimal_places=2)
    old_min_work_length=models.DecimalField('MinWorkLength', null=True, blank=True, max_digits=10, decimal_places=2)
    old_min_work_rolls=models.DecimalField('MinWorkRolls', null=True, blank=True, max_digits=10, decimal_places=2)
    old_min_work_weight=models.DecimalField('MinWorkWeight', null=True, blank=True, max_digits=10, decimal_places=2)
    old_work_done_percent=models.DecimalField('完成比例', null=True, blank=True, max_digits=5, decimal_places=2)
    old_is_check_plan=models.BooleanField('IsCheckPlan', null=True, blank=True)
    old_sort_number=models.CharField('SortNumber', null=True, blank=True, max_length=10)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_is_allowed_to_back=models.BooleanField('IsAllowedToBack', null=True, blank=True)
    old_to_input_color=models.BooleanField('ToInputColor', null=True, blank=True)
    old_stereotypes=models.IntegerField('是否定型', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_process'
        indexes=[models.Index(fields=['source_batch', 'old_process_id'],name='src_d7c389d99b623d6d')]
        verbose_name=verbose_name_plural='工序'
        ordering=["-id"]

class SourceDyePProcessArea(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_ProcessArea'
    SOURCE_FIELDS={'ProcessID': 'old_process_id', 'AreaID': 'old_area_id', 'AreaIndex': 'old_area_index', 'Name': 'old_name', 'Description': 'old_description', 'IsStop': 'old_is_stop', 'StopDate': 'old_stop_date'}
    SOURCE_KEY=('ProcessID', 'AreaID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Process', 'target': 'erp_base.SourceDyePProcess', 'source_fields': ['ProcessID'], 'target_fields': ['ProcessID'], 'evidence': ['原界面主从 p_ProcessArea → p_Process']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_process_id=models.CharField('工序', null=False, blank=True, max_length=50)
    old_area_id=models.CharField('区域编码', null=False, blank=True, max_length=10)
    old_area_index=models.IntegerField('助记序号', null=True, blank=True)
    old_name=models.CharField('区域名称', null=True, blank=True, max_length=60)
    old_description=models.CharField('描述', null=True, blank=True, max_length=500)
    old_is_stop=models.BooleanField('停用', null=True, blank=True)
    old_stop_date=models.DateTimeField('停用日期', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePProcess', verbose_name='原关系：p_Process', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_processarea'
        indexes=[models.Index(fields=['source_batch', 'old_process_id', 'old_area_id'],name='src_a1300091ee947e49')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（p_ProcessArea，待确认）'
        ordering=["-id"]

class SourceDyePProcessChemical(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_ProcessChemical'
    SOURCE_FIELDS={'ProcessID': 'old_process_id', 'ParamNo': 'old_param_no', 'ParamID': 'old_param_id', 'PPName': 'old_ppname', 'Rate': 'old_rate', 'GatherWay': 'old_gather_way', 'AlarmDelta': 'old_alarm_delta', 'Description': 'old_description'}
    SOURCE_KEY=('ProcessID', 'ParamNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Process', 'target': 'erp_base.SourceDyePProcess', 'source_fields': ['ProcessID'], 'target_fields': ['ProcessID'], 'evidence': ['原界面主从 p_ProcessChemical → p_Process']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_process_id=models.CharField('工序', null=False, blank=True, max_length=10)
    old_param_no=models.IntegerField('编号', null=False, blank=False)
    old_param_id=models.CharField('编码', null=True, blank=True, max_length=10)
    old_ppname=models.CharField('名称', null=True, blank=True, max_length=20)
    old_rate=models.DecimalField('比例', null=True, blank=True, max_digits=10, decimal_places=2)
    old_gather_way=models.CharField('采集方式', null=True, blank=True, max_length=1)
    old_alarm_delta=models.DecimalField('报警范围', null=True, blank=True, max_digits=10, decimal_places=2)
    old_description=models.CharField('描述', null=True, blank=True, max_length=500)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePProcess', verbose_name='原关系：p_Process', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_processchemical'
        indexes=[models.Index(fields=['source_batch', 'old_process_id', 'old_param_no'],name='src_6e23701d96ead44d')]
        verbose_name=verbose_name_plural='染化料与称料库存相关表（p_ProcessChemical，待确认）'
        ordering=["-id"]

class SourceDyePProcessCraft(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_ProcessCraft'
    SOURCE_FIELDS={'ProcessID': 'old_process_id', 'ParamNo': 'old_param_no', 'ParamID': 'old_param_id', 'PPName': 'old_ppname', 'MinValue': 'old_min_value', 'MaxValue': 'old_max_value', 'GatherWay': 'old_gather_way', 'AlarmDelta': 'old_alarm_delta', 'Description': 'old_description'}
    SOURCE_KEY=('ProcessID', 'ParamNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Process', 'target': 'erp_base.SourceDyePProcess', 'source_fields': ['ProcessID'], 'target_fields': ['ProcessID'], 'evidence': ['原界面主从 p_ProcessCraft → p_Process']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_process_id=models.CharField('工序代码', null=False, blank=True, max_length=10)
    old_param_no=models.IntegerField('参数编号', null=False, blank=False)
    old_param_id=models.CharField('参数编码', null=True, blank=True, max_length=10)
    old_ppname=models.CharField('参数名称', null=True, blank=True, max_length=20)
    old_min_value=models.DecimalField('最小值', null=True, blank=True, max_digits=10, decimal_places=2)
    old_max_value=models.DecimalField('最大值', null=True, blank=True, max_digits=10, decimal_places=2)
    old_gather_way=models.CharField('收集方式', null=True, blank=True, max_length=1)
    old_alarm_delta=models.DecimalField('报警范围', null=True, blank=True, max_digits=10, decimal_places=2)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePProcess', verbose_name='原关系：p_Process', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_processcraft'
        indexes=[models.Index(fields=['source_batch', 'old_process_id', 'old_param_no'],name='src_37c31811cedc76a5')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（p_ProcessCraft，待确认）'
        ordering=["-id"]

class SourceDyePProcessCraft1(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_ProcessCraft1'
    SOURCE_FIELDS={'ProcessID': 'old_process_id', 'ParamNo': 'old_param_no', 'ParamID': 'old_param_id', 'PPName': 'old_ppname', 'Description': 'old_description', 'MinValue': 'old_min_value', 'MaxValue': 'old_max_value', 'AlarmDelta': 'old_alarm_delta', 'GatherWay': 'old_gather_way'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_process_id=models.CharField('ProcessID', null=False, blank=True, max_length=5)
    old_param_no=models.IntegerField('ParamNo', null=False, blank=False)
    old_param_id=models.CharField('ParamID', null=True, blank=True, max_length=10)
    old_ppname=models.CharField('PPName', null=True, blank=True, max_length=50)
    old_description=models.CharField('Description', null=True, blank=True, max_length=100)
    old_min_value=models.DecimalField('MinValue', null=True, blank=True, max_digits=10, decimal_places=2)
    old_max_value=models.DecimalField('MaxValue', null=True, blank=True, max_digits=10, decimal_places=2)
    old_alarm_delta=models.DecimalField('AlarmDelta', null=True, blank=True, max_digits=10, decimal_places=2)
    old_gather_way=models.CharField('GatherWay', null=True, blank=True, max_length=1)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_processcraft1'
        indexes=[]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（p_ProcessCraft1，待确认）'
        ordering=["-id"]

class SourceDyePProcessDefect(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_ProcessDefect'
    SOURCE_FIELDS={'ProcessID': 'old_process_id', 'DefectID': 'old_defect_id', 'IsStop': 'old_is_stop', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('ProcessID', 'DefectID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Process', 'target': 'erp_base.SourceDyePProcess', 'source_fields': ['ProcessID'], 'target_fields': ['ProcessID'], 'evidence': ['原界面主从 p_ProcessDefect → p_Process']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_process_id=models.CharField('工序代码', null=False, blank=True, max_length=10)
    old_defect_id=models.CharField('疵点代码', null=False, blank=True, max_length=10)
    old_is_stop=models.BooleanField('是否停用', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePProcess', verbose_name='原关系：p_Process', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_processdefect'
        indexes=[models.Index(fields=['source_batch', 'old_process_id', 'old_defect_id'],name='src_2a5243d80403c8d9')]
        verbose_name=verbose_name_plural='质量检验与异常相关表（p_ProcessDefect，待确认）'
        ordering=["-id"]

class SourceDyePProcessPCraft(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_ProcessPCraft'
    SOURCE_FIELDS={'ProcessID': 'old_process_id', 'ParamNo': 'old_param_no', 'ParamID': 'old_param_id', 'PPName': 'old_ppname', 'MinValue': 'old_min_value', 'MaxValue': 'old_max_value', 'Description': 'old_description'}
    SOURCE_KEY=('ProcessID', 'ParamNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Process', 'target': 'erp_base.SourceDyePProcess', 'source_fields': ['ProcessID'], 'target_fields': ['ProcessID'], 'evidence': ['原界面主从 p_ProcessPCraft → p_Process']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_process_id=models.CharField('工序', null=False, blank=True, max_length=10)
    old_param_no=models.IntegerField('参数编号', null=False, blank=False)
    old_param_id=models.CharField('参数编码', null=True, blank=True, max_length=10)
    old_ppname=models.CharField('参数名称', null=True, blank=True, max_length=20)
    old_min_value=models.DecimalField('最小值', null=True, blank=True, max_digits=10, decimal_places=2)
    old_max_value=models.DecimalField('最大值', null=True, blank=True, max_digits=10, decimal_places=2)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePProcess', verbose_name='原关系：p_Process', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_processpcraft'
        indexes=[models.Index(fields=['source_batch', 'old_process_id', 'old_param_no'],name='src_024650b8502169a2')]
        verbose_name=verbose_name_plural='染色工艺与配方相关表（p_ProcessPCraft，待确认）'
        ordering=["-id"]

class SourceDyePProcessPrice(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_ProcessPrice'
    SOURCE_FIELDS={'ProcessID': 'old_process_id', 'ProdKindID': 'old_prod_kind_id', 'Row': 'old_row', 'WeightDn': 'old_weight_dn', 'WeightUp': 'old_weight_up', 'QtyDn': 'old_qty_dn', 'QtyUP': 'old_qty_up', 'LengthDn': 'old_length_dn', 'LengthUp': 'old_length_up', 'Price': 'old_price', 'FixCost': 'old_fix_cost', 'EffiRate': 'old_effi_rate', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('ProcessID', 'ProdKindID', 'Row')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Process', 'target': 'erp_base.SourceDyePProcess', 'source_fields': ['ProcessID'], 'target_fields': ['ProcessID'], 'evidence': ['原界面主从 p_ProcessPrice → p_Process']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_process_id=models.CharField('工序代码', null=False, blank=True, max_length=10)
    old_prod_kind_id=models.CharField('纱种代码', null=False, blank=True, max_length=10)
    old_row=models.CharField('编号', null=False, blank=True, max_length=10)
    old_weight_dn=models.DecimalField('克重下限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_weight_up=models.DecimalField('克重上限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_qty_dn=models.DecimalField('重量下限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_qty_up=models.DecimalField('重量上限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_length_dn=models.DecimalField('长度下限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_length_up=models.DecimalField('长度上限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_price=models.DecimalField('工价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_fix_cost=models.DecimalField('固定成本', null=True, blank=True, max_digits=10, decimal_places=6)
    old_effi_rate=models.DecimalField('折合系数', null=True, blank=True, max_digits=6, decimal_places=4)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePProcess', verbose_name='原关系：p_Process', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_processprice'
        indexes=[models.Index(fields=['source_batch', 'old_process_id', 'old_prod_kind_id', 'old_row'],name='src_c6879bf76b9e0ce3')]
        verbose_name=verbose_name_plural='财务结算与成本相关表（p_ProcessPrice，待确认）'
        ordering=["-id"]

class SourceDyePProduct(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Product'
    SOURCE_FIELDS={'ProdID': 'old_prod_id', 'CustomerID': 'old_customer_id', 'NameC': 'old_name_c', 'NameE': 'old_name_e', 'Spec': 'old_spec', 'Structure': 'old_structure', 'FabricKindID': 'old_fabric_kind_id', 'FabricStyleID': 'old_fabric_style_id', 'GrayWeight': 'old_gray_weight', 'StockUnit': 'old_stock_unit', 'PriceUnit': 'old_price_unit', 'GrayPrice': 'old_gray_price', 'ProdPrice': 'old_prod_price', 'ProdWeight': 'old_prod_weight', 'Mnemonic': 'old_mnemonic', 'Graphic': 'old_graphic', 'IsSample': 'old_is_sample', 'IsStop': 'old_is_stop', 'StopDate': 'old_stop_date', 'WidthDn': 'old_width_dn', 'WidthUp': 'old_width_up', 'Description': 'old_description', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Density': 'old_density', 'ColorID': 'old_color_id', 'Place': 'old_place', 'ProdCode': 'old_prod_code', 'ProductionID': 'old_production_id', 'ProdWidth': 'old_prod_width', 'WeightKindID': 'old_weight_kind_id', 'WidthKindID': 'old_width_kind_id', 'RGLX': 'old_rglx'}
    SOURCE_KEY=('ProdID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_prod_id=models.CharField('本厂规格', null=False, blank=True, max_length=20)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=20)
    old_name_c=models.CharField('中文名称', null=True, blank=True, max_length=200)
    old_name_e=models.CharField('英文名称', null=True, blank=True, max_length=160)
    old_spec=models.CharField('纱种成分', null=True, blank=True, max_length=500)
    old_structure=models.CharField('组织', null=True, blank=True, max_length=50)
    old_fabric_kind_id=models.CharField('纱种类别', null=True, blank=True, max_length=10)
    old_fabric_style_id=models.CharField('纱种分格编码', null=True, blank=True, max_length=10)
    old_gray_weight=models.IntegerField('胚纱克重', null=True, blank=True)
    old_stock_unit=models.IntegerField('库存单位', null=True, blank=True)
    old_price_unit=models.IntegerField('计价单位编码', null=True, blank=True)
    old_gray_price=models.DecimalField('胚纱价格', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prod_price=models.DecimalField('成品价格', null=True, blank=True, max_digits=10, decimal_places=2)
    old_prod_weight=models.IntegerField('克重', null=True, blank=True)
    old_mnemonic=models.CharField('助记符', null=True, blank=True, max_length=10)
    old_graphic=models.BinaryField('图案', null=True, blank=True, editable=True)
    old_is_sample=models.BooleanField('是否样品', null=True, blank=True)
    old_is_stop=models.BooleanField('是否停用', null=True, blank=True)
    old_stop_date=models.DateTimeField('停用日期', null=True, blank=True)
    old_width_dn=models.DecimalField('门幅上限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_width_up=models.DecimalField('门幅下限', null=True, blank=True, max_digits=6, decimal_places=2)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_density=models.CharField('密度', null=True, blank=True, max_length=20)
    old_color_id=models.CharField('颜色编码', null=True, blank=True, max_length=20)
    old_place=models.CharField('存放位置', null=True, blank=True, max_length=100)
    old_prod_code=models.CharField('ProdCode', null=True, blank=True, max_length=50)
    old_production_id=models.CharField('工艺路线', null=True, blank=True, max_length=50)
    old_prod_width=models.IntegerField('幅宽', null=True, blank=True)
    old_weight_kind_id=models.CharField('克重单位', null=True, blank=True, max_length=20)
    old_width_kind_id=models.CharField('幅宽单位', null=True, blank=True, max_length=50)
    old_rglx=models.CharField('染缸类型', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_product'
        indexes=[models.Index(fields=['source_batch', 'old_prod_id'],name='src_d3e89779a03246b3')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（p_Product，待确认）'
        ordering=["-id"]

class SourceDyePShift(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Shift'
    SOURCE_FIELDS={'ShiftID': 'old_shift_id', 'ClassID': 'old_class_id', 'StationID': 'old_station_id', 'ChargerID': 'old_charger_id', 'Password': 'old_password', 'Remarks': 'old_remarks', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'Name': 'old_name', 'WorkShopID': 'old_work_shop_id', 'DeptID': 'old_dept_id', 'WorkTimeSet': 'old_work_time_set', 'MachineID': 'old_machine_id', 'SortNo': 'old_sort_no', 'WorkTimeUp': 'old_work_time_up', 'WorkTimeDn': 'old_work_time_dn', 'StratDate': 'old_strat_date', 'EndDate': 'old_end_date', 'RightStatus': 'old_right_status', 'SheetStatus': 'old_sheet_status'}
    SOURCE_KEY=('ShiftID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_shift_id=models.CharField('班组代码', null=False, blank=True, max_length=10)
    old_class_id=models.CharField('班别代码', null=True, blank=True, max_length=10)
    old_station_id=models.CharField('站别代码', null=True, blank=True, max_length=10)
    old_charger_id=models.CharField('部门负责人代码', null=True, blank=True, max_length=10)
    old_password=models.CharField('查询口令', null=True, blank=True, max_length=50)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_name=models.CharField('名称', null=True, blank=True, max_length=60)
    old_work_shop_id=models.CharField('生产车间代码', null=True, blank=True, max_length=10)
    old_dept_id=models.CharField('部门', null=True, blank=True, max_length=10)
    old_work_time_set=models.DecimalField('WorkTimeSet', null=True, blank=True, max_digits=5, decimal_places=1)
    old_machine_id=models.CharField('机台', null=True, blank=True, max_length=10)
    old_sort_no=models.IntegerField('SortNo', null=True, blank=True)
    old_work_time_up=models.DecimalField('WorkTimeUp', null=True, blank=True, max_digits=5, decimal_places=1)
    old_work_time_dn=models.DecimalField('WorkTimeDn', null=True, blank=True, max_digits=5, decimal_places=1)
    old_strat_date=models.DateTimeField('开始时间', null=True, blank=True)
    old_end_date=models.DateTimeField('结束日期', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_shift'
        indexes=[models.Index(fields=['source_batch', 'old_shift_id'],name='src_7489ac2c6aba149e')]
        verbose_name=verbose_name_plural='班组班次'
        ordering=["-id"]

class SourceDyePShiftArrange(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_ShiftArrange'
    SOURCE_FIELDS={'ID': 'old_id', 'Mode': 'old_mode', 'BeginDate': 'old_begin_date', 'CycleDays': 'old_cycle_days', 'ShiftID01': 'old_shift_id01', 'ShiftID02': 'old_shift_id02', 'ShiftID03': 'old_shift_id03', 'DateBetween01': 'old_date_between01', 'DateBetween02': 'old_date_between02', 'DateBetween03': 'old_date_between03', 'ClassID01': 'old_class_id01', 'ClassID02': 'old_class_id02', 'ClassID03': 'old_class_id03'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.IntegerField('ID', null=False, blank=False)
    old_mode=models.CharField('Mode', null=True, blank=True, max_length=10)
    old_begin_date=models.DateTimeField('BeginDate', null=True, blank=True)
    old_cycle_days=models.CharField('CycleDays', null=True, blank=True, max_length=10)
    old_shift_id01=models.CharField('ShiftID01', null=True, blank=True, max_length=10)
    old_shift_id02=models.CharField('ShiftID02', null=True, blank=True, max_length=10)
    old_shift_id03=models.CharField('ShiftID03', null=True, blank=True, max_length=10)
    old_date_between01=models.CharField('DateBetween01', null=True, blank=True, max_length=100)
    old_date_between02=models.CharField('DateBetween02', null=True, blank=True, max_length=100)
    old_date_between03=models.CharField('DateBetween03', null=True, blank=True, max_length=100)
    old_class_id01=models.CharField('ClassID01', null=True, blank=True, max_length=10)
    old_class_id02=models.CharField('ClassID02', null=True, blank=True, max_length=10)
    old_class_id03=models.CharField('ClassID03', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_shiftarrange'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_89edf1a6d6e1d697')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（p_ShiftArrange，待确认）'
        ordering=["-id"]

class SourceDyePShiftArrangeDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_ShiftArrangeDetail'
    SOURCE_FIELDS={'ID': 'old_id', 'CurrDate': 'old_curr_date', 'BeginDate': 'old_begin_date', 'ShiftID01': 'old_shift_id01', 'ShiftID02': 'old_shift_id02', 'ShiftID03': 'old_shift_id03', 'DateBetween01': 'old_date_between01', 'DateBetween02': 'old_date_between02', 'DateBetween03': 'old_date_between03', 'ClassID01': 'old_class_id01', 'ClassID02': 'old_class_id02', 'ClassID03': 'old_class_id03', 'DateBetween04': 'old_date_between04', 'ClassID04': 'old_class_id04', 'ShiftID04': 'old_shift_id04'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.BigIntegerField('ID', null=False, blank=False)
    old_curr_date=models.DateTimeField('CurrDate', null=False, blank=False)
    old_begin_date=models.DateTimeField('BeginDate', null=True, blank=True)
    old_shift_id01=models.CharField('ShiftID01', null=True, blank=True, max_length=10)
    old_shift_id02=models.CharField('ShiftID02', null=True, blank=True, max_length=10)
    old_shift_id03=models.CharField('ShiftID03', null=True, blank=True, max_length=10)
    old_date_between01=models.CharField('DateBetween01', null=True, blank=True, max_length=100)
    old_date_between02=models.CharField('DateBetween02', null=True, blank=True, max_length=100)
    old_date_between03=models.CharField('DateBetween03', null=True, blank=True, max_length=100)
    old_class_id01=models.CharField('ClassID01', null=True, blank=True, max_length=10)
    old_class_id02=models.CharField('ClassID02', null=True, blank=True, max_length=10)
    old_class_id03=models.CharField('ClassID03', null=True, blank=True, max_length=10)
    old_date_between04=models.CharField('DateBetween04', null=True, blank=True, max_length=100)
    old_class_id04=models.CharField('ClassID04', null=True, blank=True, max_length=10)
    old_shift_id04=models.CharField('ShiftID04', null=True, blank=True, max_length=10)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_shiftarrangedetail'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_9e501c300f40e7ec')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（p_ShiftArrangeDetail，待确认）'
        ordering=["-id"]

class SourceDyePShiftEmp(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_ShiftEmp'
    SOURCE_FIELDS={'ShiftID': 'old_shift_id', 'SerialNumber': 'old_serial_number', 'EmpID': 'old_emp_id', 'EffiRate': 'old_effi_rate', 'Remarks': 'old_remarks', 'Post': 'old_post', 'MachineID': 'old_machine_id', 'WorkTime': 'old_work_time', 'WorkLongTime': 'old_work_long_time'}
    SOURCE_KEY=('ShiftID', 'SerialNumber')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：p_Shift', 'target': 'erp_base.SourceDyePShift', 'source_fields': ['ShiftID'], 'target_fields': ['ShiftID'], 'evidence': ['原界面主从 p_ShiftEmpZM → p_ShiftZM', '原界面主从 p_ShiftEmpKF → p_ShiftKF', '原界面主从 p_ShiftEmpZJ → p_ShiftZJ', '原界面主从 p_ShiftEmp → p_Shift', '原界面主从 p_ShiftEmpTS → p_ShiftTS', '原界面主从 p_ShiftEmpBY → p_ShiftBY', '原界面主从 p_ShiftEmpHZ → p_ShiftHZ', '原界面主从 p_ShiftEmpPB → p_ShiftPB']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_shift_id=models.CharField('班组代码', null=False, blank=True, max_length=10)
    old_serial_number=models.CharField('流水号', null=False, blank=True, max_length=30)
    old_emp_id=models.CharField('员工编号', null=False, blank=True, max_length=10)
    old_effi_rate=models.DecimalField('效率比例', null=True, blank=True, max_digits=6, decimal_places=4)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=100)
    old_post=models.CharField('岗位', null=True, blank=True, max_length=50)
    old_machine_id=models.CharField('机台', null=True, blank=True, max_length=1000)
    old_work_time=models.CharField('上班时间', null=True, blank=True, max_length=10)
    old_work_long_time=models.DecimalField('上班时长(小时)', null=True, blank=True, max_digits=6, decimal_places=1)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePShift', verbose_name='原关系：p_Shift', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_shiftemp'
        indexes=[models.Index(fields=['source_batch', 'old_shift_id', 'old_serial_number'],name='src_1430d09e62d3c390')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（p_ShiftEmp，待确认）'
        ordering=["-id"]

class SourceDyePShiftMachine(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_ShiftMachine'
    SOURCE_FIELDS={'ShiftID': 'old_shift_id', 'MachineID': 'old_machine_id', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('ShiftID', 'MachineID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_shift_id=models.CharField('ShiftID', null=False, blank=True, max_length=10)
    old_machine_id=models.CharField('MachineID', null=False, blank=True, max_length=10)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_shiftmachine'
        indexes=[models.Index(fields=['source_batch', 'old_shift_id', 'old_machine_id'],name='src_dc5de3ec8a375a90')]
        verbose_name=verbose_name_plural='设备维护与能耗相关表（p_ShiftMachine，待确认）'
        ordering=["-id"]

class SourceDyePStorageUnitID(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_StorageUnitID'
    SOURCE_FIELDS={'FieldType': 'old_field_type', 'Code': 'old_code', 'Kind': 'old_kind', 'Name': 'old_name'}
    SOURCE_KEY=('FieldType', 'Code')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_field_type=models.CharField('FieldType', null=False, blank=True, max_length=20)
    old_code=models.CharField('编码', null=False, blank=True, max_length=20)
    old_kind=models.CharField('区域类型', null=True, blank=True, max_length=20)
    old_name=models.CharField('Name', null=False, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_storageunitid'
        indexes=[models.Index(fields=['source_batch', 'old_field_type', 'old_code'],name='src_ffd0d0a9c846620d')]
        verbose_name=verbose_name_plural='仓储编码（库区/库位）'
        ordering=["-id"]

class SourceDyePStuff(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Stuff'
    SOURCE_FIELDS={'StuffID': 'old_stuff_id', 'Name': 'old_name', 'Spec': 'old_spec', 'NameE': 'old_name_e', 'StuffType': 'old_stuff_type', 'Mnemonic': 'old_mnemonic', 'StorageUnitID': 'old_storage_unit_id', 'FactID': 'old_fact_id', 'RecipeUnit': 'old_recipe_unit', 'Price': 'old_price', 'Brand': 'old_brand', 'SupplierID': 'old_supplier_id', 'WOF': 'old_wof', 'WeightMode': 'old_weight_mode', 'PackUnit': 'old_pack_unit', 'RemainQty': 'old_remain_qty', 'CupNo': 'old_cup_no', 'WeightNo': 'old_weight_no', 'StuffKindID': 'old_stuff_kind_id', 'StockUnit': 'old_stock_unit', 'IsBatch': 'old_is_batch', 'NewStuffID': 'old_new_stuff_id', 'AccSubjectID': 'old_acc_subject_id', 'SafeQty': 'old_safe_qty', 'LimitDays': 'old_limit_days', 'LeadDays': 'old_lead_days', 'Status': 'old_status', 'StopDate': 'old_stop_date', 'Remarks': 'old_remarks', 'CreateDate': 'old_create_date', 'Creater': 'old_creater', 'ModifyDate': 'old_modify_date', 'Modifyer': 'old_modifyer', 'WeightUnit': 'old_weight_unit', 'LastPrice': 'old_last_price', 'Kind': 'old_kind', 'AutoSysID': 'old_auto_sys_id', 'GaoLaodu': 'old_gao_laodu', 'TankNo': 'old_tank_no', 'Multiple': 'old_multiple'}
    SOURCE_KEY=('StuffID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_stuff_id=models.CharField('染化料代码', null=False, blank=True, max_length=20)
    old_name=models.CharField('名称', null=True, blank=True, max_length=200)
    old_spec=models.CharField('规格', null=True, blank=True, max_length=128)
    old_name_e=models.CharField('英文名称', null=True, blank=True, max_length=128)
    old_stuff_type=models.CharField('染化料类型', null=True, blank=True, max_length=10)
    old_mnemonic=models.CharField('助记符', null=True, blank=True, max_length=10)
    old_storage_unit_id=models.CharField('仓位代码', null=True, blank=True, max_length=10)
    old_fact_id=models.CharField('工厂代码', null=True, blank=True, max_length=10)
    old_recipe_unit=models.IntegerField('配方单位', null=True, blank=True)
    old_price=models.DecimalField('单价', null=True, blank=True, max_digits=16, decimal_places=6)
    old_brand=models.CharField('牌号', null=True, blank=True, max_length=20)
    old_supplier_id=models.CharField('供应商代码', null=True, blank=True, max_length=10)
    old_wof=models.DecimalField('力份', null=True, blank=True, max_digits=6, decimal_places=3)
    old_weight_mode=models.IntegerField('称料方式', null=True, blank=True)
    old_pack_unit=models.CharField('包装单位', null=True, blank=True, max_length=10)
    old_remain_qty=models.DecimalField('剩余数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_cup_no=models.CharField('滴液系统编号', null=True, blank=True, max_length=20)
    old_weight_no=models.CharField('称料系统编号', null=True, blank=True, max_length=20)
    old_stuff_kind_id=models.CharField('染化料类别', null=True, blank=True, max_length=50)
    old_stock_unit=models.CharField('库存单位', null=True, blank=True, max_length=1)
    old_is_batch=models.BooleanField('批次管理', null=True, blank=True)
    old_new_stuff_id=models.CharField('染化料新代码', null=True, blank=True, max_length=10)
    old_acc_subject_id=models.CharField('AccSubjectID', null=True, blank=True, max_length=10)
    old_safe_qty=models.DecimalField('安全库存', null=True, blank=True, max_digits=10, decimal_places=2)
    old_limit_days=models.IntegerField('收款期限', null=True, blank=True)
    old_lead_days=models.IntegerField('前置天数', null=True, blank=True)
    old_status=models.IntegerField('状态', null=True, blank=True)
    old_stop_date=models.DateTimeField('停用时间', null=True, blank=True)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_weight_unit=models.CharField('称料单位', null=True, blank=True, max_length=1)
    old_last_price=models.DecimalField('LastPrice', null=True, blank=True, max_digits=16, decimal_places=6)
    old_kind=models.CharField('属性', null=True, blank=True, max_length=10)
    old_auto_sys_id=models.CharField('配送方式', null=True, blank=True, max_length=10)
    old_gao_laodu=models.BooleanField('高牢度', null=True, blank=True)
    old_tank_no=models.IntegerField('落料桶号', null=True, blank=True)
    old_multiple=models.FloatField('配送倍数', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_stuff'
        indexes=[models.Index(fields=['source_batch', 'old_stuff_id'],name='src_2e9e5e4d77076f6a')]
        verbose_name=verbose_name_plural='染化料'
        ordering=["-id"]

class SourceDyePStuffStorageUnitID(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_StuffStorageUnitID'
    SOURCE_FIELDS={'FieldType': 'old_field_type', 'Code': 'old_code', 'Name': 'old_name'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_field_type=models.CharField('FieldType', null=True, blank=True, max_length=50)
    old_code=models.CharField('Code', null=True, blank=True, max_length=50)
    old_name=models.CharField('Name', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_stuffstorageunitid'
        indexes=[]
        verbose_name=verbose_name_plural='染化料仓位对照'
        ordering=["-id"]

class SourceDyePVehicle(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_Vehicle'
    SOURCE_FIELDS={'VehicleNo': 'old_vehicle_no', 'Weight': 'old_weight', 'Remarks': 'old_remarks', 'Status': 'old_status'}
    SOURCE_KEY=('VehicleNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_vehicle_no=models.CharField('VehicleNo', null=False, blank=True, max_length=10)
    old_weight=models.DecimalField('Weight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)
    old_status=models.CharField('Status', null=True, blank=True, max_length=1)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_vehicle'
        indexes=[models.Index(fields=['source_batch', 'old_vehicle_no'],name='src_eb2aa4a05f329b15')]
        verbose_name=verbose_name_plural='基础主数据相关表（p_Vehicle，待确认）'
        ordering=["-id"]

class SourceDyePWareHouse(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='p_WareHouse'
    SOURCE_FIELDS={'WareHouseID': 'old_ware_house_id', 'Name': 'old_name', 'Length': 'old_length', 'Width': 'old_width', 'Graphic': 'old_graphic', 'Remarks': 'old_remarks', 'StockUnit': 'old_stock_unit'}
    SOURCE_KEY=('WareHouseID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_ware_house_id=models.CharField('WareHouseID', null=False, blank=True, max_length=10)
    old_name=models.CharField('Name', null=True, blank=True, max_length=60)
    old_length=models.DecimalField('Length', null=True, blank=True, max_digits=10, decimal_places=2)
    old_width=models.DecimalField('Width', null=True, blank=True, max_digits=6, decimal_places=2)
    old_graphic=models.BinaryField('Graphic', null=True, blank=True, editable=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_stock_unit=models.IntegerField('StockUnit', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_p_warehouse'
        indexes=[models.Index(fields=['source_batch', 'old_ware_house_id'],name='src_1fd389bf67043c24')]
        verbose_name=verbose_name_plural='坯布半成品成品与仓储相关表（p_WareHouse，待确认）'
        ordering=["-id"]

class SourceDyePPasteDosage(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PPasteDosage'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'OrderNo': 'old_order_no', 'PrintCode': 'old_print_code', 'CustomerID': 'old_customer_id', 'DetailCustName': 'old_detail_cust_name', 'ProdID': 'old_prod_id', 'ColorCount': 'old_color_count', 'MachineID': 'old_machine_id', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver', 'RightStatus': 'old_right_status'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('单号', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_sheet_kind=models.IntegerField('单据类型', null=True, blank=True)
    old_order_no=models.CharField('订单号', null=True, blank=True, max_length=50)
    old_print_code=models.CharField('花号', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=10)
    old_detail_cust_name=models.CharField('明细客户', null=True, blank=True, max_length=150)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=20)
    old_color_count=models.IntegerField('(最大)颜色个数', null=True, blank=True)
    old_machine_id=models.CharField('机台号', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建日期', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_approve_date=models.DateTimeField('审核日期', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=20)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_ppastedosage'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_dcb500f57f5721f2')]
        verbose_name=verbose_name_plural='其他或待确认相关表（PPasteDosage，待确认）'
        ordering=["-id"]

class SourceDyePPasteDosageDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PPasteDosageDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'DetailNo': 'old_detail_no', 'ColorPlateID': 'old_color_plate_id', 'OrderDosage': 'old_order_dosage', 'OrderUnit': 'old_order_unit', 'Kind': 'old_kind', 'FilmRate1': 'old_film_rate1', 'Value1': 'old_value1', 'FilmRate2': 'old_film_rate2', 'Value2': 'old_value2', 'FilmRate3': 'old_film_rate3', 'Value3': 'old_value3', 'FilmRate4': 'old_film_rate4', 'Value4': 'old_value4', 'FilmRate5': 'old_film_rate5', 'Value5': 'old_value5', 'FilmRate6': 'old_film_rate6', 'Value6': 'old_value6', 'FilmRate7': 'old_film_rate7', 'Value7': 'old_value7', 'FilmRate8': 'old_film_rate8', 'Value8': 'old_value8', 'FilmRate9': 'old_film_rate9', 'Value9': 'old_value9', 'FilmRate10': 'old_film_rate10', 'Value10': 'old_value10', 'FilmRate11': 'old_film_rate11', 'Value11': 'old_value11', 'FilmRate12': 'old_film_rate12', 'Value12': 'old_value12', 'FilmRate13': 'old_film_rate13', 'Value13': 'old_value13', 'FilmRate14': 'old_film_rate14', 'Value14': 'old_value14', 'FilmRate15': 'old_film_rate15', 'Value15': 'old_value15', 'FilmRate16': 'old_film_rate16', 'Value16': 'old_value16'}
    SOURCE_KEY=('SheetSeries', 'DetailNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：PPasteDosage', 'target': 'erp_base.SourceDyePPasteDosage', 'source_fields': ['SheetSeries'], 'target_fields': ['SheetSeries'], 'evidence': ['原界面主从 PPasteDosageDetail → PPasteDosage']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=20)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=20)
    old_color_plate_id=models.CharField('花号色位', null=True, blank=True, max_length=10)
    old_order_dosage=models.DecimalField('订单量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_order_unit=models.CharField('订单单位', null=True, blank=True, max_length=10)
    old_kind=models.CharField('类型', null=True, blank=True, max_length=20)
    old_film_rate1=models.DecimalField('菲林比1', null=True, blank=True, max_digits=8, decimal_places=2)
    old_value1=models.CharField('值1', null=True, blank=True, max_length=20)
    old_film_rate2=models.DecimalField('菲林比2', null=True, blank=True, max_digits=8, decimal_places=2)
    old_value2=models.CharField('值2', null=True, blank=True, max_length=20)
    old_film_rate3=models.DecimalField('菲林比3', null=True, blank=True, max_digits=8, decimal_places=2)
    old_value3=models.CharField('值3', null=True, blank=True, max_length=20)
    old_film_rate4=models.DecimalField('菲林比4', null=True, blank=True, max_digits=8, decimal_places=2)
    old_value4=models.CharField('值4', null=True, blank=True, max_length=20)
    old_film_rate5=models.DecimalField('菲林比5', null=True, blank=True, max_digits=8, decimal_places=2)
    old_value5=models.CharField('值5', null=True, blank=True, max_length=20)
    old_film_rate6=models.DecimalField('菲林比6', null=True, blank=True, max_digits=8, decimal_places=2)
    old_value6=models.CharField('值6', null=True, blank=True, max_length=20)
    old_film_rate7=models.DecimalField('菲林比7', null=True, blank=True, max_digits=8, decimal_places=2)
    old_value7=models.CharField('值7', null=True, blank=True, max_length=20)
    old_film_rate8=models.DecimalField('菲林比8', null=True, blank=True, max_digits=8, decimal_places=2)
    old_value8=models.CharField('值8', null=True, blank=True, max_length=20)
    old_film_rate9=models.DecimalField('菲林比9', null=True, blank=True, max_digits=8, decimal_places=2)
    old_value9=models.CharField('值9', null=True, blank=True, max_length=20)
    old_film_rate10=models.DecimalField('菲林比10', null=True, blank=True, max_digits=8, decimal_places=2)
    old_value10=models.CharField('值10', null=True, blank=True, max_length=20)
    old_film_rate11=models.DecimalField('菲林比11', null=True, blank=True, max_digits=8, decimal_places=2)
    old_value11=models.CharField('值11', null=True, blank=True, max_length=20)
    old_film_rate12=models.DecimalField('菲林比12', null=True, blank=True, max_digits=8, decimal_places=2)
    old_value12=models.CharField('值12', null=True, blank=True, max_length=20)
    old_film_rate13=models.DecimalField('菲林比13', null=True, blank=True, max_digits=8, decimal_places=2)
    old_value13=models.CharField('值13', null=True, blank=True, max_length=20)
    old_film_rate14=models.DecimalField('菲林比14', null=True, blank=True, max_digits=8, decimal_places=2)
    old_value14=models.CharField('值14', null=True, blank=True, max_length=20)
    old_film_rate15=models.DecimalField('菲林比15', null=True, blank=True, max_digits=8, decimal_places=2)
    old_value15=models.CharField('值15', null=True, blank=True, max_length=20)
    old_film_rate16=models.DecimalField('菲林比16', null=True, blank=True, max_digits=8, decimal_places=2)
    old_value16=models.CharField('值16', null=True, blank=True, max_length=20)
    source_parent_1=models.ForeignKey('erp_base.SourceDyePPasteDosage', verbose_name='原关系：PPasteDosage', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_ppastedosagedetail'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series', 'old_detail_no'],name='src_673baae4b688945d')]
        verbose_name=verbose_name_plural='其他或待确认相关表（PPasteDosageDetail，待确认）'
        ordering=["-id"]

class SourceDyePrintDipsRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintDipsRecord'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetKind': 'old_sheet_kind', 'SheetDate': 'old_sheet_date', 'SheetStatus': 'old_sheet_status', 'BusinessUnitID': 'old_business_unit_id', 'CustomerID': 'old_customer_id', 'SalerGroupID': 'old_saler_group_id', 'SalerID': 'old_saler_id', 'ColorNo': 'old_color_no', 'ColorVersion': 'old_color_version', 'ConfirmVersion': 'old_confirm_version', 'DeptID': 'old_dept_id', 'CheckNo': 'old_check_no', 'MainStuffKindID': 'old_main_stuff_kind_id', 'ProdID': 'old_prod_id', 'Spec': 'old_spec', 'LotNo': 'old_lot_no', 'Structure': 'old_structure', 'ColorID': 'old_color_id', 'ColorDepthID': 'old_color_depth_id', 'ColorNum': 'old_color_num', 'CustColorNum': 'old_cust_color_num', 'ColorE': 'old_color_e', 'ColorRGB': 'old_color_rgb', 'RecipePriceSource': 'old_recipe_price_source', 'FabricSource': 'old_fabric_source', 'Weight': 'old_weight', 'CostEffirate': 'old_cost_effirate', 'Cost': 'old_cost', 'CostUnit': 'old_cost_unit', 'VerLight1ID': 'old_ver_light1_id', 'VerLight2ID': 'old_ver_light2_id', 'EmpID': 'old_emp_id', 'ShiftID': 'old_shift_id', 'CheckerID': 'old_checker_id', 'DlvSampleDate': 'old_dlv_sample_date', 'RightStatus': 'old_right_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ApproveDate': 'old_approve_date', 'Approver': 'old_approver'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_saler_group_id=models.CharField('SalerGroupID', null=True, blank=True, max_length=10)
    old_saler_id=models.CharField('SalerID', null=True, blank=True, max_length=10)
    old_color_no=models.CharField('ColorNo', null=True, blank=True, max_length=20)
    old_color_version=models.CharField('ColorVersion', null=True, blank=True, max_length=20)
    old_confirm_version=models.CharField('ConfirmVersion', null=True, blank=True, max_length=20)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=10)
    old_check_no=models.CharField('CheckNo', null=True, blank=True, max_length=20)
    old_main_stuff_kind_id=models.CharField('MainStuffKindID', null=True, blank=True, max_length=10)
    old_prod_id=models.CharField('ProdID', null=True, blank=True, max_length=20)
    old_spec=models.CharField('Spec', null=True, blank=True, max_length=128)
    old_lot_no=models.CharField('LotNo', null=True, blank=True, max_length=50)
    old_structure=models.CharField('Structure', null=True, blank=True, max_length=50)
    old_color_id=models.CharField('ColorID', null=True, blank=True, max_length=20)
    old_color_depth_id=models.CharField('ColorDepthID', null=True, blank=True, max_length=10)
    old_color_num=models.CharField('ColorNum', null=True, blank=True, max_length=20)
    old_cust_color_num=models.CharField('CustColorNum', null=True, blank=True, max_length=20)
    old_color_e=models.CharField('ColorE', null=True, blank=True, max_length=20)
    old_color_rgb=models.IntegerField('ColorRGB', null=True, blank=True)
    old_recipe_price_source=models.IntegerField('RecipePriceSource', null=True, blank=True)
    old_fabric_source=models.CharField('FabricSource', null=True, blank=True, max_length=1)
    old_weight=models.DecimalField('Weight', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cost_effirate=models.DecimalField('CostEffirate', null=True, blank=True, max_digits=6, decimal_places=2)
    old_cost=models.DecimalField('Cost', null=True, blank=True, max_digits=10, decimal_places=2)
    old_cost_unit=models.CharField('CostUnit', null=True, blank=True, max_length=1)
    old_ver_light1_id=models.CharField('VerLight1ID', null=True, blank=True, max_length=10)
    old_ver_light2_id=models.CharField('VerLight2ID', null=True, blank=True, max_length=10)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=10)
    old_shift_id=models.CharField('ShiftID', null=True, blank=True, max_length=10)
    old_checker_id=models.CharField('CheckerID', null=True, blank=True, max_length=10)
    old_dlv_sample_date=models.DateTimeField('DlvSampleDate', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printdipsrecord'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_b53d057f72e3cd64')]
        verbose_name=verbose_name_plural='其他或待确认相关表（PrintDipsRecord，待确认）'
        ordering=["-id"]

class SourceDyePrintScreen(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintScreen'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'SheetKind': 'old_sheet_kind', 'DesignNo': 'old_design_no', 'CustomerID': 'old_customer_id', 'PrintKind': 'old_print_kind', 'SheetStatus': 'old_sheet_status', 'StepNo': 'old_step_no', 'PrintTimes': 'old_print_times', 'Revisions': 'old_revisions', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'ScreenerID': 'old_screener_id', 'Sets': 'old_sets', 'ScreenFee': 'old_screen_fee', 'StorageUnitIDs': 'old_storage_unit_ids', 'FileName': 'old_file_name', 'DrawerID': 'old_drawer_id', 'ScreenFinishTime': 'old_screen_finish_time'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_sheet_kind=models.IntegerField('SheetKind', null=True, blank=True)
    old_design_no=models.CharField('DesignNo', null=True, blank=True, max_length=50)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=10)
    old_print_kind=models.CharField('PrintKind', null=True, blank=True, max_length=2)
    old_sheet_status=models.IntegerField('SheetStatus', null=True, blank=True)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_print_times=models.IntegerField('PrintTimes', null=True, blank=True)
    old_revisions=models.IntegerField('Revisions', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=512)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_screener_id=models.CharField('ScreenerID', null=True, blank=True, max_length=10)
    old_sets=models.IntegerField('Sets', null=True, blank=True)
    old_screen_fee=models.DecimalField('ScreenFee', null=True, blank=True, max_digits=10, decimal_places=2)
    old_storage_unit_ids=models.CharField('StorageUnitIDs', null=True, blank=True, max_length=100)
    old_file_name=models.CharField('FileName', null=True, blank=True, max_length=100)
    old_drawer_id=models.CharField('DrawerID', null=True, blank=True, max_length=10)
    old_screen_finish_time=models.DateTimeField('ScreenFinishTime', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printscreen'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_5789804166b31818')]
        verbose_name=verbose_name_plural='其他或待确认相关表（PrintScreen，待确认）'
        ordering=["-id"]

class SourceDyePrintScreenDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintScreenDetail'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'ScreenNo': 'old_screen_no', 'DesignDetailNo': 'old_design_detail_no', 'Status': 'old_status', 'SequenceNo': 'old_sequence_no', 'Percent': 'old_percent', 'Mesh': 'old_mesh', 'ScreenRepeat': 'old_screen_repeat', 'Width': 'old_width', 'SortNo': 'old_sort_no', 'Description': 'old_description'}
    SOURCE_KEY=('ScreenNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=20)
    old_screen_no=models.CharField('ScreenNo', null=False, blank=True, max_length=20)
    old_design_detail_no=models.CharField('DesignDetailNo', null=True, blank=True, max_length=20)
    old_status=models.IntegerField('Status', null=True, blank=True)
    old_sequence_no=models.BigIntegerField('SequenceNo', null=True, blank=True)
    old_percent=models.DecimalField('Percent', null=True, blank=True, max_digits=4, decimal_places=3)
    old_mesh=models.IntegerField('Mesh', null=True, blank=True)
    old_screen_repeat=models.DecimalField('ScreenRepeat', null=True, blank=True, max_digits=7, decimal_places=2)
    old_width=models.DecimalField('Width', null=True, blank=True, max_digits=6, decimal_places=2)
    old_sort_no=models.IntegerField('SortNo', null=True, blank=True)
    old_description=models.CharField('Description', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printscreendetail'
        indexes=[models.Index(fields=['source_batch', 'old_screen_no'],name='src_84007c8f36980ec7')]
        verbose_name=verbose_name_plural='其他或待确认相关表（PrintScreenDetail，待确认）'
        ordering=["-id"]

class SourceDyePrintScreenRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='PrintScreenRecord'
    SOURCE_FIELDS={'BookNo': 'old_book_no', 'ScreenNo': 'old_screen_no', 'DesignNo': 'old_design_no', 'DesignDetailNo': 'old_design_detail_no', 'BookKind': 'old_book_kind', 'CurrDate': 'old_curr_date', 'EmpID': 'old_emp_id', 'JobSheetNo': 'old_job_sheet_no', 'StorageUnitID': 'old_storage_unit_id', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('BookNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_book_no=models.BigIntegerField('BookNo', null=False, blank=False)
    old_screen_no=models.CharField('ScreenNo', null=True, blank=True, max_length=20)
    old_design_no=models.CharField('DesignNo', null=True, blank=True, max_length=50)
    old_design_detail_no=models.CharField('DesignDetailNo', null=True, blank=True, max_length=20)
    old_book_kind=models.IntegerField('BookKind', null=True, blank=True)
    old_curr_date=models.DateTimeField('CurrDate', null=True, blank=True)
    old_emp_id=models.CharField('EmpID', null=True, blank=True, max_length=10)
    old_job_sheet_no=models.CharField('JobSheetNo', null=True, blank=True, max_length=50)
    old_storage_unit_id=models.CharField('StorageUnitID', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_printscreenrecord'
        indexes=[models.Index(fields=['source_batch', 'old_book_no'],name='src_c14f3081d2cf978f')]
        verbose_name=verbose_name_plural='其他或待确认相关表（PrintScreenRecord，待确认）'
        ordering=["-id"]

class SourceDyeReportItem(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='ReportItem'
    SOURCE_FIELDS={'RIID': 'old_riid', 'RIIndex': 'old_riindex', 'ShowIt': 'old_show_it', 'RIName': 'old_riname', 'UnitName': 'old_unit_name', 'Formula': 'old_formula', 'CalcBySchClass': 'old_calc_by_sch_class', 'StatisticMethod': 'old_statistic_method', 'CalcLast': 'old_calc_last', 'Notes': 'old_notes'}
    SOURCE_KEY=('RIID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=('old_riid',)
    old_riid=models.IntegerField('RIID', null=False, blank=False)
    old_riindex=models.IntegerField('RIIndex', null=True, blank=True)
    old_show_it=models.IntegerField('ShowIt', null=True, blank=True)
    old_riname=models.CharField('RIName', null=True, blank=True, max_length=12)
    old_unit_name=models.CharField('UnitName', null=True, blank=True, max_length=6)
    old_formula=models.BinaryField('Formula', null=False, blank=True, editable=True)
    old_calc_by_sch_class=models.IntegerField('CalcBySchClass', null=True, blank=True)
    old_statistic_method=models.IntegerField('StatisticMethod', null=True, blank=True)
    old_calc_last=models.IntegerField('CalcLast', null=True, blank=True)
    old_notes=models.BinaryField('Notes', null=True, blank=True, editable=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_reportitem'
        indexes=[models.Index(fields=['source_batch', 'old_riid'],name='src_0a0f19af456ca54b')]
        verbose_name=verbose_name_plural='其他或待确认相关表（ReportItem，待确认）'
        ordering=["-id"]

class SourceDyeRequestLimit(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='RequestLimit'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'CustomerID': 'old_customer_id', 'ApplicantID': 'old_applicant_id', 'DesigneeID': 'old_designee_id', 'DeliveryDay': 'old_delivery_day', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'RightStatus': 'old_right_status', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'OverdueAmount': 'old_overdue_amount'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('SheetSeries', null=False, blank=True, max_length=30)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=30)
    old_sheet_date=models.DateTimeField('SheetDate', null=True, blank=True)
    old_customer_id=models.CharField('CustomerID', null=True, blank=True, max_length=30)
    old_applicant_id=models.CharField('ApplicantID', null=True, blank=True, max_length=30)
    old_designee_id=models.CharField('DesigneeID', null=True, blank=True, max_length=30)
    old_delivery_day=models.IntegerField('DeliveryDay', null=True, blank=True)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=200)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=30)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=30)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)
    old_right_status=models.IntegerField('RightStatus', null=True, blank=True)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=30)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_overdue_amount=models.DecimalField('OverdueAmount', null=True, blank=True, max_digits=12, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_requestlimit'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_39c5ff7272c31987')]
        verbose_name=verbose_name_plural='其他或待确认相关表（RequestLimit，待确认）'
        ordering=["-id"]

class SourceDyeSAutoID(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='s_AutoID'
    SOURCE_FIELDS={'IDObject': 'old_idobject', 'IDCounter': 'old_idcounter', 'IDValue': 'old_idvalue', 'CreateDate': 'old_create_date'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_idobject=models.CharField('IDObject', null=False, blank=True, max_length=50)
    old_idcounter=models.BigIntegerField('IDCounter', null=True, blank=True)
    old_idvalue=models.CharField('IDValue', null=True, blank=True, max_length=50)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_s_autoid'
        indexes=[]
        verbose_name=verbose_name_plural='旧业务编号计数'
        ordering=["-id"]

class SourceDyeSCorpTitle(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='s_CorpTitle'
    SOURCE_FIELDS={'Code': 'old_code', 'Title': 'old_title', 'SpecData': 'old_spec_data', 'StopDate': 'old_stop_date'}
    SOURCE_KEY=('Code',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_code=models.CharField('代码', null=False, blank=True, max_length=20)
    old_title=models.CharField('标题', null=True, blank=True, max_length=200)
    old_spec_data=models.BinaryField('二进制存储的内容', null=True, blank=True, editable=True)
    old_stop_date=models.DateTimeField('停用时间', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_s_corptitle'
        indexes=[models.Index(fields=['source_batch', 'old_code'],name='src_8bf1b72ba35b7cc1')]
        verbose_name=verbose_name_plural='公司抬头资料'
        ordering=["-id"]

class SourceDyeSFlow(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='s_Flow'
    SOURCE_FIELDS={'FlowID': 'old_flow_id', 'FlowName': 'old_flow_name', 'BusinessUnitID': 'old_business_unit_id', 'DataTableName': 'old_data_table_name', 'FormName': 'old_form_name', 'Description': 'old_description', 'FlowKindID': 'old_flow_kind_id', 'SheetName': 'old_sheet_name', 'IsCanUnSubmit': 'old_is_can_un_submit', 'IsToNotify': 'old_is_to_notify', 'IsCanUpdate': 'old_is_can_update', 'RptIDForEmail': 'old_rpt_idfor_email', 'SubmiterFieldName': 'old_submiter_field_name', 'IsStop': 'old_is_stop', 'StopDate': 'old_stop_date', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'IsUnEndApprovedOnlyBySelf': 'old_is_un_end_approved_only_by_self', 'FuncNo': 'old_func_no', 'PhyTableName': 'old_phy_table_name', 'RptID': 'old_rpt_id', 'IsUseWeXin': 'old_is_use_we_xin', 'RelaFuncNo': 'old_rela_func_no', 'IsDirectCancel': 'old_is_direct_cancel', 'IsCreatImage': 'old_is_creat_image', 'SubmiterCancelOnly': 'old_submiter_cancel_only'}
    SOURCE_KEY=('FlowID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_flow_id=models.CharField('流程编号', null=False, blank=True, max_length=10)
    old_flow_name=models.CharField('流程名称', null=True, blank=True, max_length=50)
    old_business_unit_id=models.CharField('经营单位代码', null=True, blank=True, max_length=10)
    old_data_table_name=models.CharField('数据集名', null=True, blank=True, max_length=50)
    old_form_name=models.CharField('审核窗口名称', null=True, blank=True, max_length=50)
    old_description=models.CharField('描述', null=True, blank=True, max_length=500)
    old_flow_kind_id=models.CharField('流程类别', null=True, blank=True, max_length=10)
    old_sheet_name=models.CharField('单据名称', null=True, blank=True, max_length=20)
    old_is_can_un_submit=models.BooleanField('终审前能否撤消', null=True, blank=True)
    old_is_to_notify=models.BooleanField('提交或撤消发通知', null=True, blank=True)
    old_is_can_update=models.BooleanField('终审前能否修改', null=True, blank=True)
    old_rpt_idfor_email=models.CharField('邮件审批模板', null=True, blank=True, max_length=10)
    old_submiter_field_name=models.CharField('提交人字段名', null=True, blank=True, max_length=20)
    old_is_stop=models.BooleanField('停用', null=True, blank=True)
    old_stop_date=models.DateTimeField('停用时间', null=True, blank=True)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改日期', null=True, blank=True)
    old_is_un_end_approved_only_by_self=models.BooleanField('只有本人才能反审核', null=True, blank=True)
    old_func_no=models.CharField('功能号', null=True, blank=True, max_length=6)
    old_phy_table_name=models.CharField('PhyTableName', null=True, blank=True, max_length=50)
    old_rpt_id=models.CharField('报表ID', null=True, blank=True, max_length=50)
    old_is_use_we_xin=models.BooleanField('发送微信消息', null=True, blank=True)
    old_rela_func_no=models.CharField('RelaFuncNo', null=True, blank=True, max_length=200)
    old_is_direct_cancel=models.BooleanField('IsDirectCancel', null=True, blank=True)
    old_is_creat_image=models.BooleanField('IsCreatImage', null=True, blank=True)
    old_submiter_cancel_only=models.BooleanField('SubmiterCancelOnly', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_s_flow'
        indexes=[models.Index(fields=['source_batch', 'old_flow_id'],name='src_c2a98a8e3f623865')]
        verbose_name=verbose_name_plural='旧审批流程配置'
        ordering=["-id"]

class SourceDyeSFlowRecord(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='s_FlowRecord'
    SOURCE_FIELDS={'FlowRecordNo': 'old_flow_record_no', 'BusinessUnitID': 'old_business_unit_id', 'FlowID': 'old_flow_id', 'StepNo': 'old_step_no', 'SheetNo': 'old_sheet_no', 'ApproveDate': 'old_approve_date', 'ApproverID': 'old_approver_id', 'Approver': 'old_approver', 'Idea': 'old_idea', 'Status': 'old_status', 'Remarks': 'old_remarks'}
    SOURCE_KEY=('FlowRecordNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=('old_flow_record_no',)
    old_flow_record_no=models.BigIntegerField('FlowRecordNo', null=False, blank=False)
    old_business_unit_id=models.CharField('BusinessUnitID', null=True, blank=True, max_length=10)
    old_flow_id=models.CharField('FlowID', null=True, blank=True, max_length=10)
    old_step_no=models.IntegerField('StepNo', null=True, blank=True)
    old_sheet_no=models.CharField('SheetNo', null=True, blank=True, max_length=20)
    old_approve_date=models.DateTimeField('ApproveDate', null=True, blank=True)
    old_approver_id=models.CharField('ApproverID', null=True, blank=True, max_length=10)
    old_approver=models.CharField('Approver', null=True, blank=True, max_length=10)
    old_idea=models.TextField('Idea', null=True, blank=True)
    old_status=models.CharField('Status', null=True, blank=True, max_length=1)
    old_remarks=models.CharField('Remarks', null=True, blank=True, max_length=100)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_s_flowrecord'
        indexes=[models.Index(fields=['source_batch', 'old_flow_record_no'],name='src_ea4a3dcffbd9b2f7')]
        verbose_name=verbose_name_plural='旧审批事实记录'
        ordering=["-id"]

class SourceDyeSFlowStep(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='s_FlowStep'
    SOURCE_FIELDS={'FlowID': 'old_flow_id', 'StepNo': 'old_step_no', 'StepName': 'old_step_name', 'Description': 'old_description', 'TimeOverHours': 'old_time_over_hours', 'IsDisagreeToBack': 'old_is_disagree_to_back', 'IsDisagreeToContinue': 'old_is_disagree_to_continue', 'IsDisagreeToSubmiter': 'old_is_disagree_to_submiter', 'IsOverAutoNotify': 'old_is_over_auto_notify', 'IsOverAutoContinue': 'old_is_over_auto_continue', 'IsCanChangeSign': 'old_is_can_change_sign', 'IsToNotifyNext': 'old_is_to_notify_next', 'IsToNotifyPrev': 'old_is_to_notify_prev', 'IsEnd': 'old_is_end', 'SignerCanModifyFieldNames': 'old_signer_can_modify_field_names', 'OverNotifyInterval': 'old_over_notify_interval', 'TaskTitleFormat': 'old_task_title_format', 'OverTitleFormat': 'old_over_title_format', 'BackedTaskTitleFormat': 'old_backed_task_title_format', 'ChangeTitleFormat': 'old_change_title_format', 'AndOr': 'old_and_or', 'NoSignProcedure': 'old_no_sign_procedure', 'GetSignerProcedure': 'old_get_signer_procedure', 'AfterSignProcedure': 'old_after_sign_procedure', 'GetNoticerProcedure': 'old_get_noticer_procedure', 'IsAndJudge': 'old_is_and_judge'}
    SOURCE_KEY=('FlowID', 'StepNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：s_Flow', 'target': 'erp_base.SourceDyeSFlow', 'source_fields': ['FlowID'], 'target_fields': ['FlowID'], 'evidence': ['原界面主从 s_FlowStep → s_Flow', '数据库声明 FK_s_FlowStep_s_Flow']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_flow_id=models.CharField('流程编号', null=False, blank=True, max_length=10)
    old_step_no=models.IntegerField('节点号', null=False, blank=False)
    old_step_name=models.CharField('节点名称', null=True, blank=True, max_length=50)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    old_time_over_hours=models.IntegerField('超时时限', null=True, blank=True)
    old_is_disagree_to_back=models.BooleanField('不同意则退回', null=True, blank=True)
    old_is_disagree_to_continue=models.BooleanField('不同意继续流转', null=True, blank=True)
    old_is_disagree_to_submiter=models.BooleanField('不同意退到提交人', null=True, blank=True)
    old_is_over_auto_notify=models.BooleanField('超时自动通知', null=True, blank=True)
    old_is_over_auto_continue=models.BooleanField('超时自动流转', null=True, blank=True)
    old_is_can_change_sign=models.BooleanField('可转签', null=True, blank=True)
    old_is_to_notify_next=models.BooleanField('通知后面节点人', null=True, blank=True)
    old_is_to_notify_prev=models.BooleanField('通知前面节点人', null=True, blank=True)
    old_is_end=models.BooleanField('终审节点', null=True, blank=True)
    old_signer_can_modify_field_names=models.CharField('签核人可修改字段', null=True, blank=True, max_length=400)
    old_over_notify_interval=models.IntegerField('超时通知间隔', null=True, blank=True)
    old_task_title_format=models.CharField('任务标题格式', null=True, blank=True, max_length=100)
    old_over_title_format=models.CharField('超时通知格式', null=True, blank=True, max_length=100)
    old_backed_task_title_format=models.CharField('退回通知格式', null=True, blank=True, max_length=100)
    old_change_title_format=models.CharField('转签通知格式', null=True, blank=True, max_length=100)
    old_and_or=models.CharField('与或签核', null=True, blank=True, max_length=10)
    old_no_sign_procedure=models.CharField('免审核存储过程名', null=True, blank=True, max_length=100)
    old_get_signer_procedure=models.CharField('获得节点签核人过程名', null=True, blank=True, max_length=100)
    old_after_sign_procedure=models.CharField('AfterSignProcedure', null=True, blank=True, max_length=50)
    old_get_noticer_procedure=models.CharField('GetNoticerProcedure', null=True, blank=True, max_length=100)
    old_is_and_judge=models.BooleanField('IsAndJudge', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_base.SourceDyeSFlow', verbose_name='原关系：s_Flow', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_s_flowstep'
        indexes=[models.Index(fields=['source_batch', 'old_flow_id', 'old_step_no'],name='src_22be92bb7699f95e')]
        verbose_name=verbose_name_plural='旧审批步骤配置'
        ordering=["-id"]

class SourceDyeSFlowStepEmp(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='s_FlowStepEmp'
    SOURCE_FIELDS={'FlowID': 'old_flow_id', 'StepNo': 'old_step_no', 'EmpID': 'old_emp_id', 'IsMustSign': 'old_is_must_sign', 'Description': 'old_description', 'TaskKind': 'old_task_kind', 'IsEnable': 'old_is_enable', 'IsSendByEmail': 'old_is_send_by_email', 'IsSendByQQ': 'old_is_send_by_qq', 'IsSendBySMS': 'old_is_send_by_sms', 'IsSendByWebservice': 'old_is_send_by_webservice', 'IsSendByWeXin': 'old_is_send_by_we_xin', 'IsSendByDingDing': 'old_is_send_by_ding_ding', 'IsSendByApp': 'old_is_send_by_app'}
    SOURCE_KEY=('FlowID', 'StepNo', 'EmpID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：s_FlowStep', 'target': 'erp_base.SourceDyeSFlowStep', 'source_fields': ['FlowID', 'StepNo'], 'target_fields': ['FlowID', 'StepNo'], 'evidence': ['原界面主从 s_FlowStepEmp → s_FlowStep', '数据库声明 FK_s_FlowStepEmp_s_FlowStep']}, {'field': 'source_parent_2', 'title': '原关系：s_FlowStepEmp', 'target': 'erp_base.SourceDyeSFlowStepEmp', 'source_fields': ['FlowID', 'StepNo', 'EmpID'], 'target_fields': ['FlowID', 'StepNo', 'EmpID'], 'evidence': ['数据库声明 FK_s_FlowStepEmp_s_FlowStepEmp']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_flow_id=models.CharField('流程编号', null=False, blank=True, max_length=10)
    old_step_no=models.IntegerField('节点号', null=False, blank=False)
    old_emp_id=models.CharField('员工编码', null=False, blank=True, max_length=10)
    old_is_must_sign=models.BooleanField('必签', null=True, blank=True)
    old_description=models.CharField('描述', null=True, blank=True, max_length=100)
    old_task_kind=models.IntegerField('工作类别', null=True, blank=True)
    old_is_enable=models.BooleanField('是否启用', null=True, blank=True)
    old_is_send_by_email=models.BooleanField('发Email', null=True, blank=True)
    old_is_send_by_qq=models.BooleanField('发QQ', null=True, blank=True)
    old_is_send_by_sms=models.BooleanField('发ＳＭＳ', null=True, blank=True)
    old_is_send_by_webservice=models.BooleanField('发ＷＥＢ', null=True, blank=True)
    old_is_send_by_we_xin=models.BooleanField('发微信', null=True, blank=True)
    old_is_send_by_ding_ding=models.BooleanField('发钉钉', null=True, blank=True)
    old_is_send_by_app=models.BooleanField('IsSendByApp', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_base.SourceDyeSFlowStep', verbose_name='原关系：s_FlowStep', null=True, blank=True, on_delete=models.PROTECT, related_name='+')
    source_parent_2=models.ForeignKey('erp_base.SourceDyeSFlowStepEmp', verbose_name='原关系：s_FlowStepEmp', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_s_flowstepemp'
        indexes=[models.Index(fields=['source_batch', 'old_flow_id', 'old_step_no', 'old_emp_id'],name='src_f5ec1b8b2a2eadda')]
        verbose_name=verbose_name_plural='旧审批人员配置'
        ordering=["-id"]

class SourceDyeSFlowTask(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='s_FlowTask'
    SOURCE_FIELDS={'FlowTaskNo': 'old_flow_task_no', 'BusinessUnitID': 'old_business_unit_id', 'FlowID': 'old_flow_id', 'StepNo': 'old_step_no', 'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'RightStatus': 'old_right_status', 'TaskTitle': 'old_task_title', 'SignedManner': 'old_signed_manner', 'SignedDate': 'old_signed_date', 'SignerID': 'old_signer_id', 'Signer': 'old_signer', 'Idea': 'old_idea', 'Status': 'old_status', 'Remarks': 'old_remarks', 'TaskKind': 'old_task_kind', 'TaskDate': 'old_task_date', 'Sender': 'old_sender', 'SenderID': 'old_sender_id', 'FlowBeginTime': 'old_flow_begin_time', 'DataTableName': 'old_data_table_name', 'SubmiterID': 'old_submiter_id', 'Submiter': 'old_submiter', 'SendDate': 'old_send_date', 'SubmitDate': 'old_submit_date', 'PhotoAddress': 'old_photo_address', 'SQLUser': 'old_sqluser', 'IsAutoSign': 'old_is_auto_sign'}
    SOURCE_KEY=('FlowTaskNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_flow_task_no=models.CharField('任务号', null=False, blank=True, max_length=38)
    old_business_unit_id=models.CharField('经营单位', null=True, blank=True, max_length=10)
    old_flow_id=models.CharField('流程编号', null=True, blank=True, max_length=10)
    old_step_no=models.IntegerField('节点编号', null=True, blank=True)
    old_sheet_series=models.CharField('表单流水号', null=True, blank=True, max_length=50)
    old_sheet_no=models.CharField('表单编号', null=True, blank=True, max_length=36)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)
    old_task_title=models.CharField('任务标题', null=True, blank=True, max_length=100)
    old_signed_manner=models.IntegerField('签核的方式', null=True, blank=True)
    old_signed_date=models.DateTimeField('签核的日期', null=True, blank=True)
    old_signer_id=models.CharField('签核人编码', null=True, blank=True, max_length=10)
    old_signer=models.CharField('签核人名', null=True, blank=True, max_length=10)
    old_idea=models.TextField('签核意见', null=True, blank=True)
    old_status=models.CharField('任务状态', null=True, blank=True, max_length=10)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=512)
    old_task_kind=models.IntegerField('任务类别', null=True, blank=True)
    old_task_date=models.DateTimeField('任务开始时间', null=True, blank=True)
    old_sender=models.CharField('发送人姓名', null=True, blank=True, max_length=10)
    old_sender_id=models.CharField('发送人编码', null=True, blank=True, max_length=10)
    old_flow_begin_time=models.DateTimeField('流程开始时间', null=True, blank=True)
    old_data_table_name=models.CharField('DataTableName', null=True, blank=True, max_length=50)
    old_submiter_id=models.CharField('SubmiterID', null=True, blank=True, max_length=10)
    old_submiter=models.CharField('Submiter', null=True, blank=True, max_length=10)
    old_send_date=models.DateTimeField('SendDate', null=True, blank=True)
    old_submit_date=models.DateTimeField('SubmitDate', null=True, blank=True)
    old_photo_address=models.CharField('PhotoAddress', null=True, blank=True, max_length=512)
    old_sqluser=models.CharField('SQLUser', null=True, blank=True, max_length=50)
    old_is_auto_sign=models.BooleanField('IsAutoSign', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_s_flowtask'
        indexes=[models.Index(fields=['source_batch', 'old_flow_task_no'],name='src_1e047cd1db5085d8')]
        verbose_name=verbose_name_plural='旧审批待办及签署事实'
        ordering=["-id"]

class SourceDyeSRevision(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='s_Revision'
    SOURCE_FIELDS={'ReviNo': 'old_revi_no', 'SheetNo': 'old_sheet_no', 'ReviDate': 'old_revi_date', 'RevierID': 'old_revier_id', 'ReviDesc': 'old_revi_desc', 'CheckerID': 'old_checker_id', 'CheckDate': 'old_check_date', 'CheckDesc': 'old_check_desc', 'FuncNo': 'old_func_no', 'IsChecked': 'old_is_checked', 'IsUpdated': 'old_is_updated', 'Content': 'old_content', 'RevierIP': 'old_revier_ip', 'ComputerName': 'old_computer_name', 'ReviMode': 'old_revi_mode', 'TableName': 'old_table_name'}
    SOURCE_KEY=('ReviNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=('old_revi_no',)
    old_revi_no=models.IntegerField('ReviNo', null=False, blank=False)
    old_sheet_no=models.CharField('SheetNo', null=False, blank=True, max_length=30)
    old_revi_date=models.DateTimeField('ReviDate', null=True, blank=True)
    old_revier_id=models.CharField('RevierID', null=True, blank=True, max_length=20)
    old_revi_desc=models.CharField('ReviDesc', null=True, blank=True, max_length=80)
    old_checker_id=models.CharField('CheckerID', null=True, blank=True, max_length=20)
    old_check_date=models.DateTimeField('CheckDate', null=True, blank=True)
    old_check_desc=models.CharField('CheckDesc', null=True, blank=True, max_length=80)
    old_func_no=models.CharField('FuncNo', null=True, blank=True, max_length=6)
    old_is_checked=models.CharField('IsChecked', null=True, blank=True, max_length=1)
    old_is_updated=models.CharField('IsUpdated', null=True, blank=True, max_length=1)
    old_content=models.BinaryField('Content', null=True, blank=True, editable=True)
    old_revier_ip=models.CharField('RevierIP', null=True, blank=True, max_length=20)
    old_computer_name=models.CharField('ComputerName', null=True, blank=True, max_length=50)
    old_revi_mode=models.CharField('ReviMode', null=True, blank=True, max_length=8)
    old_table_name=models.CharField('TableName', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_s_revision'
        indexes=[models.Index(fields=['source_batch', 'old_revi_no'],name='src_8e80fe590faf5511')]
        verbose_name=verbose_name_plural='旧业务字段变更单'
        ordering=["-id"]

class SourceDyeSRevisionDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='s_RevisionDetail'
    SOURCE_FIELDS={'ReviNo': 'old_revi_no', 'RowNo': 'old_row_no', 'OriValue': 'old_ori_value', 'CurrValue': 'old_curr_value', 'TableName': 'old_table_name', 'FieldName': 'old_field_name', 'DisplayName': 'old_display_name', 'ReviMode': 'old_revi_mode'}
    SOURCE_KEY=('ReviNo', 'RowNo')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_revi_no=models.IntegerField('ReviNo', null=False, blank=False)
    old_row_no=models.DecimalField('RowNo', null=False, blank=False, max_digits=3, decimal_places=0)
    old_ori_value=models.CharField('OriValue', null=True, blank=True, max_length=50)
    old_curr_value=models.CharField('CurrValue', null=True, blank=True, max_length=50)
    old_table_name=models.CharField('TableName', null=True, blank=True, max_length=20)
    old_field_name=models.CharField('FieldName', null=True, blank=True, max_length=20)
    old_display_name=models.CharField('DisplayName', null=True, blank=True, max_length=20)
    old_revi_mode=models.CharField('ReviMode', null=True, blank=True, max_length=8)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_s_revisiondetail'
        indexes=[models.Index(fields=['source_batch', 'old_revi_no', 'old_row_no'],name='src_a5cda4384d744b49')]
        verbose_name=verbose_name_plural='旧业务字段变更明细'
        ordering=["-id"]

class SourceDyeSSaveMessRule(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='s_SaveMessRule'
    SOURCE_FIELDS={'FuncNo': 'old_func_no', 'TimeWay': 'old_time_way', 'ProcName': 'old_proc_name', 'ProcParamFields': 'old_proc_param_fields', 'IsEnable': 'old_is_enable', 'StopDate': 'old_stop_date', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date'}
    SOURCE_KEY=('FuncNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_func_no=models.CharField('FuncNo', null=False, blank=True, max_length=6)
    old_time_way=models.IntegerField('TimeWay', null=True, blank=True)
    old_proc_name=models.CharField('ProcName', null=True, blank=True, max_length=20)
    old_proc_param_fields=models.CharField('ProcParamFields', null=True, blank=True, max_length=50)
    old_is_enable=models.BooleanField('IsEnable', null=True, blank=True)
    old_stop_date=models.DateTimeField('StopDate', null=True, blank=True)
    old_creater=models.CharField('Creater', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('CreateDate', null=True, blank=True)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_s_savemessrule'
        indexes=[models.Index(fields=['source_batch', 'old_func_no'],name='src_4a52b9729448653b')]
        verbose_name=verbose_name_plural='旧业务提交通知规则'
        ordering=["-id"]

class SourceDyeSSaveMessRuleDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='s_SaveMessRuleDetail'
    SOURCE_FIELDS={'FuncNo': 'old_func_no', 'DetailNo': 'old_detail_no', 'DataTableName': 'old_data_table_name', 'SourceFilter': 'old_source_filter', 'ReceiverIDs': 'old_receiver_ids', 'Subject': 'old_subject', 'Content': 'old_content', 'ParamFields': 'old_param_fields', 'IsEnable': 'old_is_enable', 'StopDate': 'old_stop_date', 'TimeWay': 'old_time_way'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_func_no=models.CharField('FuncNo', null=True, blank=True, max_length=6)
    old_detail_no=models.CharField('DetailNo', null=False, blank=True, max_length=36)
    old_data_table_name=models.CharField('DataTableName', null=True, blank=True, max_length=50)
    old_source_filter=models.TextField('SourceFilter', null=True, blank=True)
    old_receiver_ids=models.CharField('ReceiverIDs', null=True, blank=True, max_length=50)
    old_subject=models.CharField('Subject', null=True, blank=True, max_length=200)
    old_content=models.TextField('Content', null=True, blank=True)
    old_param_fields=models.CharField('ParamFields', null=True, blank=True, max_length=50)
    old_is_enable=models.BooleanField('IsEnable', null=True, blank=True)
    old_stop_date=models.DateTimeField('StopDate', null=True, blank=True)
    old_time_way=models.IntegerField('TimeWay', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_s_savemessruledetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_73cbe0ac4a445bd1')]
        verbose_name=verbose_name_plural='旧业务提交通知规则明细'
        ordering=["-id"]

class SourceDyeSSheetNo(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='s_SheetNo'
    SOURCE_FIELDS={'SheetTypeID': 'old_sheet_type_id', 'PrevDate': 'old_prev_date', 'Prefix': 'old_prefix', 'PrevNo': 'old_prev_no', 'SheetName': 'old_sheet_name', 'YearCode': 'old_year_code', 'MonthCode': 'old_month_code', 'IsUseDayCode': 'old_is_use_day_code', 'EndCode': 'old_end_code'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_type_id=models.DecimalField('SheetTypeID', null=False, blank=False, max_digits=3, decimal_places=0)
    old_prev_date=models.CharField('PrevDate', null=False, blank=True, max_length=8)
    old_prefix=models.CharField('Prefix', null=False, blank=True, max_length=2)
    old_prev_no=models.DecimalField('PrevNo', null=True, blank=True, max_digits=9, decimal_places=0)
    old_sheet_name=models.CharField('SheetName', null=True, blank=True, max_length=20)
    old_year_code=models.IntegerField('YearCode', null=True, blank=True)
    old_month_code=models.IntegerField('MonthCode', null=True, blank=True)
    old_is_use_day_code=models.IntegerField('IsUseDayCode', null=True, blank=True)
    old_end_code=models.IntegerField('EndCode', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_s_sheetno'
        indexes=[]
        verbose_name=verbose_name_plural='旧单据编号规则'
        ordering=["-id"]

class SourceDyeSchClass(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SchClass'
    SOURCE_FIELDS={'schClassid': 'old_sch_classid', 'schName': 'old_sch_name', 'StartTime': 'old_start_time', 'EndTime': 'old_end_time', 'LateMinutes': 'old_late_minutes', 'EarlyMinutes': 'old_early_minutes', 'CheckIn': 'old_check_in', 'CheckOut': 'old_check_out', 'CheckInTime1': 'old_check_in_time1', 'CheckInTime2': 'old_check_in_time2', 'CheckOutTime1': 'old_check_out_time1', 'CheckOutTime2': 'old_check_out_time2', 'Color': 'old_color', 'AutoBind': 'old_auto_bind', 'WorkDay': 'old_work_day', 'SensorID': 'old_sensor_id', 'WorkMins': 'old_work_mins'}
    SOURCE_KEY=('schClassid',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_check_in': ('literal', 1), 'old_check_out': ('literal', 1), 'old_color': ('literal', 16715535), 'old_auto_bind': ('literal', 1), 'old_work_day': ('literal', 1), 'old_work_mins': ('literal', 0)}
    SOURCE_IDENTITIES=('old_sch_classid',)
    old_sch_classid=models.IntegerField('schClassid', null=False, blank=False)
    old_sch_name=models.CharField('schName', null=False, blank=True, max_length=20)
    old_start_time=models.DateTimeField('StartTime', null=False, blank=False)
    old_end_time=models.DateTimeField('EndTime', null=False, blank=False)
    old_late_minutes=models.IntegerField('LateMinutes', null=True, blank=True)
    old_early_minutes=models.IntegerField('EarlyMinutes', null=True, blank=True)
    old_check_in=models.IntegerField('CheckIn', null=True, blank=True)
    old_check_out=models.IntegerField('CheckOut', null=True, blank=True)
    old_check_in_time1=models.DateTimeField('CheckInTime1', null=True, blank=True)
    old_check_in_time2=models.DateTimeField('CheckInTime2', null=True, blank=True)
    old_check_out_time1=models.DateTimeField('CheckOutTime1', null=True, blank=True)
    old_check_out_time2=models.DateTimeField('CheckOutTime2', null=True, blank=True)
    old_color=models.IntegerField('Color', null=True, blank=True)
    old_auto_bind=models.IntegerField('AutoBind', null=True, blank=True)
    old_work_day=models.FloatField('WorkDay', null=True, blank=True)
    old_sensor_id=models.CharField('SensorID', null=True, blank=True, max_length=5)
    old_work_mins=models.FloatField('WorkMins', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_schclass'
        indexes=[models.Index(fields=['source_batch', 'old_sch_classid'],name='src_7fbcbfe98d995cd1')]
        verbose_name=verbose_name_plural='其他或待确认相关表（SchClass，待确认）'
        ordering=["-id"]

class SourceDyeSHIFT(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SHIFT'
    SOURCE_FIELDS={'SHIFTID': 'old_shiftid', 'NAME': 'old_name', 'USHIFTID': 'old_ushiftid', 'STARTDATE': 'old_startdate', 'ENDDATE': 'old_enddate', 'RUNNUM': 'old_runnum', 'SCH1': 'old_sch1', 'SCH2': 'old_sch2', 'SCH3': 'old_sch3', 'SCH4': 'old_sch4', 'SCH5': 'old_sch5', 'SCH6': 'old_sch6', 'SCH7': 'old_sch7', 'SCH8': 'old_sch8', 'SCH9': 'old_sch9', 'SCH10': 'old_sch10', 'SCH11': 'old_sch11', 'SCH12': 'old_sch12', 'CYCLE': 'old_cycle', 'UNITS': 'old_units'}
    SOURCE_KEY=('SHIFTID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_ushiftid': ('literal', -1), 'old_startdate': ('literal', '1900-1-1'), 'old_enddate': ('literal', '1900-12-31'), 'old_runnum': ('literal', 0), 'old_sch1': ('literal', 0), 'old_sch2': ('literal', 0), 'old_sch3': ('literal', 0), 'old_sch4': ('literal', 0), 'old_sch5': ('literal', 0), 'old_sch6': ('literal', 0), 'old_sch7': ('literal', 0), 'old_sch8': ('literal', 0), 'old_sch9': ('literal', 0), 'old_sch10': ('literal', 0), 'old_sch11': ('literal', 0), 'old_sch12': ('literal', 0), 'old_cycle': ('literal', 0), 'old_units': ('literal', 0)}
    SOURCE_IDENTITIES=('old_shiftid',)
    old_shiftid=models.IntegerField('SHIFTID', null=False, blank=False)
    old_name=models.CharField('NAME', null=True, blank=True, max_length=20)
    old_ushiftid=models.IntegerField('USHIFTID', null=True, blank=True)
    old_startdate=models.DateTimeField('STARTDATE', null=False, blank=False)
    old_enddate=models.DateTimeField('ENDDATE', null=True, blank=True)
    old_runnum=models.IntegerField('RUNNUM', null=True, blank=True)
    old_sch1=models.IntegerField('SCH1', null=True, blank=True)
    old_sch2=models.IntegerField('SCH2', null=True, blank=True)
    old_sch3=models.IntegerField('SCH3', null=True, blank=True)
    old_sch4=models.IntegerField('SCH4', null=True, blank=True)
    old_sch5=models.IntegerField('SCH5', null=True, blank=True)
    old_sch6=models.IntegerField('SCH6', null=True, blank=True)
    old_sch7=models.IntegerField('SCH7', null=True, blank=True)
    old_sch8=models.IntegerField('SCH8', null=True, blank=True)
    old_sch9=models.IntegerField('SCH9', null=True, blank=True)
    old_sch10=models.IntegerField('SCH10', null=True, blank=True)
    old_sch11=models.IntegerField('SCH11', null=True, blank=True)
    old_sch12=models.IntegerField('SCH12', null=True, blank=True)
    old_cycle=models.IntegerField('CYCLE', null=True, blank=True)
    old_units=models.IntegerField('UNITS', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_shift'
        indexes=[models.Index(fields=['source_batch', 'old_shiftid'],name='src_a7c2cd17bd720eac')]
        verbose_name=verbose_name_plural='生产工单与排程相关表（SHIFT，待确认）'
        ordering=["-id"]

class SourceDyeSHOUPITONGZHIDAN(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SHOUPITONGZHIDAN'
    SOURCE_FIELDS={'ID': 'old_id', 'CustomerID': 'old_customer_id', 'DIZHI': 'old_dizhi', 'LXR': 'old_lxr', 'DHHM': 'old_dhhm', 'RQ': 'old_rq', 'PISHU': 'old_pishu', 'BZ': 'old_bz', 'JIANCHEN': 'old_jianchen'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.CharField('单号', null=False, blank=True, max_length=20)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    old_dizhi=models.CharField('地址', null=True, blank=True, max_length=200)
    old_lxr=models.CharField('联系人', null=True, blank=True, max_length=50)
    old_dhhm=models.CharField('电话号码', null=True, blank=True, max_length=500)
    old_rq=models.DateTimeField('日期', null=True, blank=True)
    old_pishu=models.DecimalField('粒数', null=True, blank=True, max_digits=9, decimal_places=1)
    old_bz=models.CharField('备注', null=True, blank=True, max_length=500)
    old_jianchen=models.CharField('客户简称', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_shoupitongzhidan'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_f4f9c36245b871d0')]
        verbose_name=verbose_name_plural='其他或待确认相关表（SHOUPITONGZHIDAN，待确认）'
        ordering=["-id"]

class SourceDyeStaffEstablishing(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='StaffEstablishing'
    SOURCE_FIELDS={'id': 'old_id', 'DeptID': 'old_dept_id', 'Empkind': 'old_empkind', 'OrgNum': 'old_org_num'}
    SOURCE_KEY=('id',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_id=models.CharField('id', null=False, blank=True, max_length=10)
    old_dept_id=models.CharField('DeptID', null=True, blank=True, max_length=20)
    old_empkind=models.CharField('Empkind', null=True, blank=True, max_length=20)
    old_org_num=models.IntegerField('OrgNum', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_staffestablishing'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_2978a93674d1530b')]
        verbose_name=verbose_name_plural='其他或待确认相关表（StaffEstablishing，待确认）'
        ordering=["-id"]

class SourceDyeSwipeEmpEdit(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SwipeEmpEdit'
    SOURCE_FIELDS={'SheetSeries': 'old_sheet_series', 'SheetNo': 'old_sheet_no', 'SheetDate': 'old_sheet_date', 'CustomerID': 'old_customer_id', 'ProdID': 'old_prod_id', 'Remarks': 'old_remarks', 'Creater': 'old_creater', 'CreateDate': 'old_create_date', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'Approver': 'old_approver', 'ApproveDate': 'old_approve_date', 'RightStatus': 'old_right_status'}
    SOURCE_KEY=('SheetSeries',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheet_series=models.CharField('表单流水号', null=False, blank=True, max_length=50)
    old_sheet_no=models.CharField('制单单号', null=True, blank=True, max_length=50)
    old_sheet_date=models.DateTimeField('单据日期', null=True, blank=True)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=50)
    old_prod_id=models.CharField('品名', null=True, blank=True, max_length=50)
    old_remarks=models.CharField('备注', null=True, blank=True, max_length=500)
    old_creater=models.CharField('创建人', null=True, blank=True, max_length=10)
    old_create_date=models.DateTimeField('创建时间', null=True, blank=True)
    old_modifyer=models.CharField('修改人', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('修改时间', null=True, blank=True)
    old_approver=models.CharField('审核人', null=True, blank=True, max_length=10)
    old_approve_date=models.DateTimeField('审核时间', null=True, blank=True)
    old_right_status=models.IntegerField('审核状态', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_swipeempedit'
        indexes=[models.Index(fields=['source_batch', 'old_sheet_series'],name='src_deea2c4ecf2e9bc9')]
        verbose_name=verbose_name_plural='基础主数据相关表（SwipeEmpEdit，待确认）'
        ordering=["-id"]

class SourceDyeSwipeEmpEditDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='SwipeEmpEditDetail'
    SOURCE_FIELDS={'Sheetseries': 'old_sheetseries', 'DetailNo': 'old_detail_no', 'CustomerID': 'old_customer_id', 'JobSheetNo': 'old_job_sheet_no', 'ProdID': 'old_prod_id', 'ColorNum': 'old_color_num', 'ColorID': 'old_color_id', 'LotNo': 'old_lot_no', 'OrderQty': 'old_order_qty', 'Qty': 'old_qty', 'Rolls': 'old_rolls', 'Area': 'old_area', 'CustSelfNo': 'old_cust_self_no', 'ContractNo': 'old_contract_no', 'SumAssignedRolls': 'old_sum_assigned_rolls', 'SumAssignedWeightQty': 'old_sum_assigned_weight_qty', 'ColorRemarks': 'old_color_remarks', 'CheckNo': 'old_check_no', 'LabelWareHouse': 'old_label_ware_house', 'LabelRemarks': 'old_label_remarks', 'WindingID': 'old_winding_id', 'TubeWeight': 'old_tube_weight', 'PackBag': 'old_pack_bag', 'MachineID': 'old_machine_id', 'GY': 'old_gy', 'CustFabricName': 'old_cust_fabric_name', 'LTSheetNo': 'old_ltsheet_no', 'FenTou': 'old_fen_tou'}
    SOURCE_KEY=('DetailNo',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_sheetseries=models.CharField('表单号', null=False, blank=True, max_length=50)
    old_detail_no=models.CharField('明细单号', null=False, blank=True, max_length=50)
    old_customer_id=models.CharField('客户', null=True, blank=True, max_length=30)
    old_job_sheet_no=models.CharField('缸号', null=True, blank=True, max_length=30)
    old_prod_id=models.CharField('本厂规格', null=True, blank=True, max_length=30)
    old_color_num=models.CharField('色号', null=True, blank=True, max_length=30)
    old_color_id=models.CharField('颜色', null=True, blank=True, max_length=30)
    old_lot_no=models.CharField('批号', null=True, blank=True, max_length=50)
    old_order_qty=models.DecimalField('订单数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_qty=models.DecimalField('数量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_rolls=models.DecimalField('粒数', null=True, blank=True, max_digits=10, decimal_places=2)
    old_area=models.CharField('区域', null=True, blank=True, max_length=100)
    old_cust_self_no=models.CharField('制单号', null=True, blank=True, max_length=100)
    old_contract_no=models.CharField('客户单号', null=True, blank=True, max_length=500)
    old_sum_assigned_rolls=models.DecimalField('生产个数', null=True, blank=True, max_digits=7, decimal_places=2)
    old_sum_assigned_weight_qty=models.DecimalField('生产重量', null=True, blank=True, max_digits=10, decimal_places=2)
    old_color_remarks=models.CharField('用途', null=True, blank=True, max_length=500)
    old_check_no=models.CharField('订单明细号', null=True, blank=True, max_length=50)
    old_label_ware_house=models.CharField('标签仓库', null=True, blank=True, max_length=100)
    old_label_remarks=models.CharField('标签用途', null=True, blank=True, max_length=500)
    old_winding_id=models.CharField('登记员工', null=True, blank=True, max_length=30)
    old_tube_weight=models.DecimalField('纸筒', null=True, blank=True, max_digits=7, decimal_places=3)
    old_pack_bag=models.DecimalField('包装', null=True, blank=True, max_digits=7, decimal_places=3)
    old_machine_id=models.CharField('机台', null=True, blank=True, max_length=100)
    old_gy=models.CharField('工艺', null=True, blank=True, max_length=200)
    old_cust_fabric_name=models.CharField('客户规格', null=True, blank=True, max_length=200)
    old_ltsheet_no=models.CharField('排产号', null=True, blank=True, max_length=30)
    old_fen_tou=models.CharField('分头', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_swipeempeditdetail'
        indexes=[models.Index(fields=['source_batch', 'old_detail_no'],name='src_f6e510be60545b06')]
        verbose_name=verbose_name_plural='基础主数据相关表（SwipeEmpEditDetail，待确认）'
        ordering=["-id"]

class SourceDyeTBKEY(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='TBKEY'
    SOURCE_FIELDS={'PreName': 'old_pre_name', 'ONEKEY': 'old_onekey'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_pre_name=models.CharField('PreName', null=True, blank=True, max_length=12)
    old_onekey=models.IntegerField('ONEKEY', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_tbkey'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（TBKEY，待确认）'
        ordering=["-id"]

class SourceDyeTBSMSALLOT(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='TBSMSALLOT'
    SOURCE_FIELDS={'REFERENCE': 'old_reference', 'SMSREF': 'old_smsref', 'USERREF': 'old_userref', 'GENTM': 'old_gentm'}
    SOURCE_KEY=('REFERENCE',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_reference=models.IntegerField('REFERENCE', null=False, blank=False)
    old_smsref=models.IntegerField('SMSREF', null=False, blank=False)
    old_userref=models.IntegerField('USERREF', null=False, blank=False)
    old_gentm=models.CharField('GENTM', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_tbsmsallot'
        indexes=[models.Index(fields=['source_batch', 'old_reference'],name='src_60e94604ce677bd4')]
        verbose_name=verbose_name_plural='其他或待确认相关表（TBSMSALLOT，待确认）'
        ordering=["-id"]

class SourceDyeTBSMSINFO(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='TBSMSINFO'
    SOURCE_FIELDS={'REFERENCE': 'old_reference', 'SMSID': 'old_smsid', 'SMSINDEX': 'old_smsindex', 'SMSTYPE': 'old_smstype', 'SMSCONTENT': 'old_smscontent', 'SMSSTARTTM': 'old_smsstarttm', 'SMSTMLENG': 'old_smstmleng', 'GENTM': 'old_gentm'}
    SOURCE_KEY=('REFERENCE',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_reference=models.IntegerField('REFERENCE', null=False, blank=False)
    old_smsid=models.CharField('SMSID', null=False, blank=True, max_length=16)
    old_smsindex=models.IntegerField('SMSINDEX', null=False, blank=False)
    old_smstype=models.IntegerField('SMSTYPE', null=True, blank=True)
    old_smscontent=models.TextField('SMSCONTENT', null=True, blank=True)
    old_smsstarttm=models.CharField('SMSSTARTTM', null=True, blank=True, max_length=32)
    old_smstmleng=models.IntegerField('SMSTMLENG', null=True, blank=True)
    old_gentm=models.CharField('GENTM', null=True, blank=True, max_length=20)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_tbsmsinfo'
        indexes=[models.Index(fields=['source_batch', 'old_reference'],name='src_d1c5231e29bf9d8e')]
        verbose_name=verbose_name_plural='其他或待确认相关表（TBSMSINFO，待确认）'
        ordering=["-id"]

class SourceDyeTEMPLATE(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='TEMPLATE'
    SOURCE_FIELDS={'TEMPLATEID': 'old_templateid', 'USERID': 'old_userid', 'FINGERID': 'old_fingerid', 'TEMPLATE': 'old_template', 'TEMPLATE2': 'old_template2', 'TEMPLATE3': 'old_template3', 'BITMAPPICTURE': 'old_bitmappicture', 'BITMAPPICTURE2': 'old_bitmappicture2', 'BITMAPPICTURE3': 'old_bitmappicture3', 'BITMAPPICTURE4': 'old_bitmappicture4', 'USETYPE': 'old_usetype', 'EMACHINENUM': 'old_emachinenum', 'TEMPLATE1': 'old_template1', 'Flag': 'old_flag', 'DivisionFP': 'old_division_fp', 'TEMPLATE4': 'old_template4'}
    SOURCE_KEY=('TEMPLATEID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_flag': ('literal', 1), 'old_division_fp': ('literal', 0)}
    SOURCE_IDENTITIES=('old_templateid',)
    old_templateid=models.IntegerField('TEMPLATEID', null=False, blank=False)
    old_userid=models.IntegerField('USERID', null=False, blank=False)
    old_fingerid=models.IntegerField('FINGERID', null=False, blank=False)
    old_template=models.BinaryField('TEMPLATE', null=False, blank=True, editable=True)
    old_template2=models.BinaryField('TEMPLATE2', null=True, blank=True, editable=True)
    old_template3=models.BinaryField('TEMPLATE3', null=True, blank=True, editable=True)
    old_bitmappicture=models.BinaryField('BITMAPPICTURE', null=True, blank=True, editable=True)
    old_bitmappicture2=models.BinaryField('BITMAPPICTURE2', null=True, blank=True, editable=True)
    old_bitmappicture3=models.BinaryField('BITMAPPICTURE3', null=True, blank=True, editable=True)
    old_bitmappicture4=models.BinaryField('BITMAPPICTURE4', null=True, blank=True, editable=True)
    old_usetype=models.IntegerField('USETYPE', null=True, blank=True)
    old_emachinenum=models.CharField('EMACHINENUM', null=True, blank=True, max_length=3)
    old_template1=models.BinaryField('TEMPLATE1', null=True, blank=True, editable=True)
    old_flag=models.IntegerField('Flag', null=True, blank=True)
    old_division_fp=models.IntegerField('DivisionFP', null=True, blank=True)
    old_template4=models.BinaryField('TEMPLATE4', null=True, blank=True, editable=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_template'
        indexes=[models.Index(fields=['source_batch', 'old_templateid'],name='src_f313da368843726b')]
        verbose_name=verbose_name_plural='基础主数据相关表（TEMPLATE，待确认）'
        ordering=["-id"]

class SourceDyeUSEROFRUN(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='USER_OF_RUN'
    SOURCE_FIELDS={'USERID': 'old_userid', 'NUM_OF_RUN_ID': 'old_num_of_run_id', 'STARTDATE': 'old_startdate', 'ENDDATE': 'old_enddate', 'ISNOTOF_RUN': 'old_isnotof_run', 'ORDER_RUN': 'old_order_run'}
    SOURCE_KEY=('USERID', 'NUM_OF_RUN_ID', 'STARTDATE', 'ENDDATE')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_startdate': ('literal', '1900-1-1'), 'old_enddate': ('literal', '2099-12-31'), 'old_isnotof_run': ('literal', 0)}
    SOURCE_IDENTITIES=()
    old_userid=models.IntegerField('USERID', null=False, blank=False)
    old_num_of_run_id=models.IntegerField('NUM_OF_RUN_ID', null=False, blank=False)
    old_startdate=models.DateTimeField('STARTDATE', null=False, blank=False)
    old_enddate=models.DateTimeField('ENDDATE', null=False, blank=False)
    old_isnotof_run=models.IntegerField('ISNOTOF_RUN', null=True, blank=True)
    old_order_run=models.IntegerField('ORDER_RUN', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_user_of_run'
        indexes=[models.Index(fields=['source_batch', 'old_userid', 'old_num_of_run_id', 'old_startdate', 'old_enddate'],name='src_a489c79e36182a0d')]
        verbose_name=verbose_name_plural='其他或待确认相关表（USER_OF_RUN，待确认）'
        ordering=["-id"]

class SourceDyeUSERSPEDAY(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='USER_SPEDAY'
    SOURCE_FIELDS={'USERID': 'old_userid', 'STARTSPECDAY': 'old_startspecday', 'ENDSPECDAY': 'old_endspecday', 'DATEID': 'old_dateid', 'YUANYING': 'old_yuanying', 'DATE': 'old_date'}
    SOURCE_KEY=('USERID', 'STARTSPECDAY', 'DATEID')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_startspecday': ('literal', '1900-1-1'), 'old_endspecday': ('literal', '2099-12-31'), 'old_dateid': ('literal', -1)}
    SOURCE_IDENTITIES=()
    old_userid=models.IntegerField('USERID', null=False, blank=False)
    old_startspecday=models.DateTimeField('STARTSPECDAY', null=False, blank=False)
    old_endspecday=models.DateTimeField('ENDSPECDAY', null=True, blank=True)
    old_dateid=models.IntegerField('DATEID', null=False, blank=False)
    old_yuanying=models.CharField('YUANYING', null=True, blank=True, max_length=200)
    old_date=models.DateTimeField('DATE', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_user_speday'
        indexes=[models.Index(fields=['source_batch', 'old_userid', 'old_startspecday', 'old_dateid'],name='src_d66f34c9c4866065')]
        verbose_name=verbose_name_plural='其他或待确认相关表（USER_SPEDAY，待确认）'
        ordering=["-id"]

class SourceDyeUSERTEMPSCH(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='USER_TEMP_SCH'
    SOURCE_FIELDS={'USERID': 'old_userid', 'COMETIME': 'old_cometime', 'LEAVETIME': 'old_leavetime', 'OVERTIME': 'old_overtime', 'TYPE': 'old_type', 'FLAG': 'old_flag', 'SCHCLASSID': 'old_schclassid'}
    SOURCE_KEY=('USERID', 'COMETIME', 'LEAVETIME')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_overtime': ('literal', 0), 'old_type': ('literal', 0), 'old_flag': ('literal', 1), 'old_schclassid': ('literal', -1)}
    SOURCE_IDENTITIES=()
    old_userid=models.IntegerField('USERID', null=False, blank=False)
    old_cometime=models.DateTimeField('COMETIME', null=False, blank=False)
    old_leavetime=models.DateTimeField('LEAVETIME', null=False, blank=False)
    old_overtime=models.IntegerField('OVERTIME', null=False, blank=False)
    old_type=models.IntegerField('TYPE', null=True, blank=True)
    old_flag=models.IntegerField('FLAG', null=True, blank=True)
    old_schclassid=models.IntegerField('SCHCLASSID', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_user_temp_sch'
        indexes=[models.Index(fields=['source_batch', 'old_userid', 'old_cometime', 'old_leavetime'],name='src_8d43ba9b6bab8412')]
        verbose_name=verbose_name_plural='基础主数据相关表（USER_TEMP_SCH，待确认）'
        ordering=["-id"]

class SourceDyeUSERINFO(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='USERINFO'
    SOURCE_FIELDS={'USERID': 'old_userid', 'BADGENUMBER': 'old_badgenumber', 'SSN': 'old_ssn', 'NAME': 'old_name', 'GENDER': 'old_gender', 'TITLE': 'old_title', 'PAGER': 'old_pager', 'BIRTHDAY': 'old_birthday', 'HIREDDAY': 'old_hiredday', 'STREET': 'old_street', 'CITY': 'old_city', 'STATE': 'old_state', 'ZIP': 'old_zip', 'OPHONE': 'old_ophone', 'FPHONE': 'old_fphone', 'VERIFICATIONMETHOD': 'old_verificationmethod', 'DEFAULTDEPTID': 'old_defaultdeptid', 'SECURITYFLAGS': 'old_securityflags', 'ATT': 'old_att', 'INLATE': 'old_inlate', 'OUTEARLY': 'old_outearly', 'OVERTIME': 'old_overtime', 'SEP': 'old_sep', 'HOLIDAY': 'old_holiday', 'MINZU': 'old_minzu', 'PASSWORD': 'old_password', 'LUNCHDURATION': 'old_lunchduration', 'MVerifyPass': 'old_mverify_pass', 'PHOTO': 'old_photo', 'Notes': 'old_notes', 'privilege': 'old_privilege', 'InheritDeptSch': 'old_inherit_dept_sch', 'InheritDeptSchClass': 'old_inherit_dept_sch_class', 'AutoSchPlan': 'old_auto_sch_plan', 'MinAutoSchInterval': 'old_min_auto_sch_interval', 'RegisterOT': 'old_register_ot', 'InheritDeptRule': 'old_inherit_dept_rule', 'EMPRIVILEGE': 'old_emprivilege', 'CardNo': 'old_card_no', 'FaceGroup': 'old_face_group', 'AccGroup': 'old_acc_group', 'UseAccGroupTZ': 'old_use_acc_group_tz', 'VerifyCode': 'old_verify_code', 'Expires': 'old_expires', 'ValidCount': 'old_valid_count', 'ValidTimeBegin': 'old_valid_time_begin', 'ValidTimeEnd': 'old_valid_time_end', 'TimeZone1': 'old_time_zone1', 'TimeZone2': 'old_time_zone2', 'TimeZone3': 'old_time_zone3', 'IDCardNo': 'old_idcard_no', 'IDCardValidTime': 'old_idcard_valid_time', 'EMail': 'old_email', 'IDCardName': 'old_idcard_name', 'IDCardBirth': 'old_idcard_birth', 'IDCardSN': 'old_idcard_sn', 'IDCardDN': 'old_idcard_dn', 'IDCardAddr': 'old_idcard_addr', 'IDCardNewAddr': 'old_idcard_new_addr', 'IDCardISSUER': 'old_idcard_issuer', 'IDCardGender': 'old_idcard_gender', 'IDCardNation': 'old_idcard_nation', 'IDCardReserve': 'old_idcard_reserve', 'IDCardNotice': 'old_idcard_notice', 'IDCard_MainCard': 'old_idcard_main_card', 'IDCard_ViceCard': 'old_idcard_vice_card', 'FSelected': 'old_fselected', 'Pin1': 'old_pin1'}
    SOURCE_KEY=('USERID',)
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_defaultdeptid': ('literal', 1), 'old_att': ('literal', 1), 'old_inlate': ('literal', 1), 'old_outearly': ('literal', 1), 'old_overtime': ('literal', 1), 'old_sep': ('literal', 1), 'old_holiday': ('literal', 1), 'old_lunchduration': ('literal', 1), 'old_privilege': ('literal', 0), 'old_inherit_dept_sch': ('literal', 1), 'old_inherit_dept_sch_class': ('literal', 1), 'old_auto_sch_plan': ('literal', 1), 'old_min_auto_sch_interval': ('literal', 24), 'old_register_ot': ('literal', 1), 'old_inherit_dept_rule': ('literal', 1), 'old_emprivilege': ('literal', 0), 'old_face_group': ('literal', 0), 'old_acc_group': ('literal', 1), 'old_use_acc_group_tz': ('literal', 1), 'old_verify_code': ('literal', 0), 'old_expires': ('literal', 0), 'old_valid_count': ('literal', 0), 'old_time_zone1': ('literal', 1), 'old_time_zone2': ('literal', 0), 'old_time_zone3': ('literal', 0), 'old_fselected': ('literal', 0)}
    SOURCE_IDENTITIES=('old_userid',)
    old_userid=models.IntegerField('USERID', null=False, blank=False)
    old_badgenumber=models.CharField('BADGENUMBER', null=False, blank=True, max_length=24)
    old_ssn=models.CharField('SSN', null=True, blank=True, max_length=20)
    old_name=models.CharField('NAME', null=True, blank=True, max_length=40)
    old_gender=models.CharField('GENDER', null=True, blank=True, max_length=8)
    old_title=models.CharField('TITLE', null=True, blank=True, max_length=20)
    old_pager=models.CharField('PAGER', null=True, blank=True, max_length=20)
    old_birthday=models.DateTimeField('BIRTHDAY', null=True, blank=True)
    old_hiredday=models.DateTimeField('HIREDDAY', null=True, blank=True)
    old_street=models.CharField('STREET', null=True, blank=True, max_length=80)
    old_city=models.CharField('CITY', null=True, blank=True, max_length=2)
    old_state=models.CharField('STATE', null=True, blank=True, max_length=2)
    old_zip=models.CharField('ZIP', null=True, blank=True, max_length=12)
    old_ophone=models.CharField('OPHONE', null=True, blank=True, max_length=20)
    old_fphone=models.CharField('FPHONE', null=True, blank=True, max_length=20)
    old_verificationmethod=models.IntegerField('VERIFICATIONMETHOD', null=True, blank=True)
    old_defaultdeptid=models.IntegerField('DEFAULTDEPTID', null=True, blank=True)
    old_securityflags=models.IntegerField('SECURITYFLAGS', null=True, blank=True)
    old_att=models.IntegerField('ATT', null=False, blank=False)
    old_inlate=models.IntegerField('INLATE', null=False, blank=False)
    old_outearly=models.IntegerField('OUTEARLY', null=False, blank=False)
    old_overtime=models.IntegerField('OVERTIME', null=False, blank=False)
    old_sep=models.IntegerField('SEP', null=False, blank=False)
    old_holiday=models.IntegerField('HOLIDAY', null=False, blank=False)
    old_minzu=models.CharField('MINZU', null=True, blank=True, max_length=8)
    old_password=models.CharField('PASSWORD', null=True, blank=True, max_length=50)
    old_lunchduration=models.IntegerField('LUNCHDURATION', null=False, blank=False)
    old_mverify_pass=models.CharField('MVerifyPass', null=True, blank=True, max_length=10)
    old_photo=models.BinaryField('PHOTO', null=True, blank=True, editable=True)
    old_notes=models.BinaryField('Notes', null=True, blank=True, editable=True)
    old_privilege=models.IntegerField('privilege', null=True, blank=True)
    old_inherit_dept_sch=models.IntegerField('InheritDeptSch', null=True, blank=True)
    old_inherit_dept_sch_class=models.IntegerField('InheritDeptSchClass', null=True, blank=True)
    old_auto_sch_plan=models.IntegerField('AutoSchPlan', null=True, blank=True)
    old_min_auto_sch_interval=models.IntegerField('MinAutoSchInterval', null=True, blank=True)
    old_register_ot=models.IntegerField('RegisterOT', null=True, blank=True)
    old_inherit_dept_rule=models.IntegerField('InheritDeptRule', null=True, blank=True)
    old_emprivilege=models.IntegerField('EMPRIVILEGE', null=True, blank=True)
    old_card_no=models.CharField('CardNo', null=True, blank=True, max_length=20)
    old_face_group=models.IntegerField('FaceGroup', null=True, blank=True)
    old_acc_group=models.IntegerField('AccGroup', null=True, blank=True)
    old_use_acc_group_tz=models.IntegerField('UseAccGroupTZ', null=True, blank=True)
    old_verify_code=models.IntegerField('VerifyCode', null=True, blank=True)
    old_expires=models.IntegerField('Expires', null=True, blank=True)
    old_valid_count=models.IntegerField('ValidCount', null=True, blank=True)
    old_valid_time_begin=models.DateTimeField('ValidTimeBegin', null=True, blank=True)
    old_valid_time_end=models.DateTimeField('ValidTimeEnd', null=True, blank=True)
    old_time_zone1=models.IntegerField('TimeZone1', null=True, blank=True)
    old_time_zone2=models.IntegerField('TimeZone2', null=True, blank=True)
    old_time_zone3=models.IntegerField('TimeZone3', null=True, blank=True)
    old_idcard_no=models.CharField('IDCardNo', null=True, blank=True, max_length=50)
    old_idcard_valid_time=models.CharField('IDCardValidTime', null=True, blank=True, max_length=32)
    old_email=models.CharField('EMail', null=True, blank=True, max_length=100)
    old_idcard_name=models.CharField('IDCardName', null=True, blank=True, max_length=30)
    old_idcard_birth=models.CharField('IDCardBirth', null=True, blank=True, max_length=16)
    old_idcard_sn=models.CharField('IDCardSN', null=True, blank=True, max_length=24)
    old_idcard_dn=models.CharField('IDCardDN', null=True, blank=True, max_length=24)
    old_idcard_addr=models.CharField('IDCardAddr', null=True, blank=True, max_length=70)
    old_idcard_new_addr=models.CharField('IDCardNewAddr', null=True, blank=True, max_length=255)
    old_idcard_issuer=models.CharField('IDCardISSUER', null=True, blank=True, max_length=32)
    old_idcard_gender=models.IntegerField('IDCardGender', null=True, blank=True)
    old_idcard_nation=models.IntegerField('IDCardNation', null=True, blank=True)
    old_idcard_reserve=models.CharField('IDCardReserve', null=True, blank=True, max_length=36)
    old_idcard_notice=models.CharField('IDCardNotice', null=True, blank=True, max_length=255)
    old_idcard_main_card=models.CharField('IDCard_MainCard', null=True, blank=True, max_length=24)
    old_idcard_vice_card=models.CharField('IDCard_ViceCard', null=True, blank=True, max_length=24)
    old_fselected=models.BooleanField('FSelected', null=True, blank=True)
    old_pin1=models.IntegerField('Pin1', null=True, blank=True)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_userinfo'
        indexes=[models.Index(fields=['source_batch', 'old_userid'],name='src_d624393937051656')]
        verbose_name=verbose_name_plural='其他或待确认相关表（USERINFO，待确认）'
        ordering=["-id"]

class SourceDyeUserUsedSClasses(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='UserUsedSClasses'
    SOURCE_FIELDS={'UserId': 'old_user_id', 'SchId': 'old_sch_id'}
    SOURCE_KEY=('UserId', 'SchId')
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_user_id=models.IntegerField('UserId', null=False, blank=False)
    old_sch_id=models.IntegerField('SchId', null=False, blank=False)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_userusedsclasses'
        indexes=[models.Index(fields=['source_batch', 'old_user_id', 'old_sch_id'],name='src_1a109f8d23af4863')]
        verbose_name=verbose_name_plural='其他或待确认相关表（UserUsedSClasses，待确认）'
        ordering=["-id"]

class SourceDyeYunfeibiaozhun(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='yunfeibiaozhun'
    SOURCE_FIELDS={'CODE': 'old_code', 'Address': 'old_address', 'LeiXing': 'old_lei_xing', 'outPrice': 'old_out_price', 'inprice': 'old_inprice'}
    SOURCE_KEY=()
    SOURCE_DOCUMENT=True
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_code=models.CharField('CODE', null=True, blank=True, max_length=5)
    old_address=models.CharField('Address', null=True, blank=True, max_length=50)
    old_lei_xing=models.CharField('LeiXing', null=True, blank=True, max_length=5)
    old_out_price=models.DecimalField('outPrice', null=True, blank=True, max_digits=18, decimal_places=2)
    old_inprice=models.DecimalField('inprice', null=True, blank=True, max_digits=18, decimal_places=2)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_yunfeibiaozhun'
        indexes=[]
        verbose_name=verbose_name_plural='其他或待确认相关表（yunfeibiaozhun，待确认）'
        ordering=["-id"]

class SourceDyeZRevisionDetail(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='z_RevisionDetail'
    SOURCE_FIELDS={'RecordID': 'old_record_id', 'ID': 'old_id', 'FieldName': 'old_field_name', 'OriValue': 'old_ori_value', 'CurrValue': 'old_curr_value'}
    SOURCE_KEY=('RecordID', 'ID')
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[{'field': 'source_parent_1', 'title': '原关系：z_RevisionKey', 'target': 'erp_base.SourceDyeZRevisionKey', 'source_fields': ['ID'], 'target_fields': ['ID'], 'evidence': ['数据库声明 FK_z_RevisionDetail_z_RevisionKey', '原界面主从 z_RevisionDetail → z_RevisionKey']}]
    SOURCE_DEFAULTS={}
    SOURCE_IDENTITIES=()
    old_record_id=models.CharField('RecordID', null=False, blank=True, max_length=38)
    old_id=models.CharField('ID', null=False, blank=True, max_length=50)
    old_field_name=models.CharField('FieldName', null=True, blank=True, max_length=50)
    old_ori_value=models.TextField('OriValue', null=True, blank=True)
    old_curr_value=models.TextField('CurrValue', null=True, blank=True)
    source_parent_1=models.ForeignKey('erp_base.SourceDyeZRevisionKey', verbose_name='原关系：z_RevisionKey', null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    class Meta(SourceRecord.Meta):
        db_table='src_dye_z_revisiondetail'
        indexes=[models.Index(fields=['source_batch', 'old_record_id', 'old_id'],name='src_81a21eb8ea57b4c3')]
        verbose_name=verbose_name_plural='旧业务字段修改值'
        ordering=["-id"]

class SourceDyeZRevisionKey(SourceRecord):
    SOURCE_SCHEMA='dye'
    SOURCE_TABLE='z_RevisionKey'
    SOURCE_FIELDS={'ID': 'old_id', 'DataTableName': 'old_data_table_name', 'KeyField': 'old_key_field', 'KeyValue': 'old_key_value', 'Modifyer': 'old_modifyer', 'ModifyDate': 'old_modify_date', 'IPAddress': 'old_ipaddress', 'ComputerName': 'old_computer_name'}
    SOURCE_KEY=('ID',)
    SOURCE_DOCUMENT=False
    SOURCE_RELATIONS=[]
    SOURCE_DEFAULTS={'old_modify_date': ('now', None)}
    SOURCE_IDENTITIES=()
    old_id=models.CharField('ID', null=False, blank=True, max_length=50)
    old_data_table_name=models.CharField('DataTableName', null=True, blank=True, max_length=50)
    old_key_field=models.CharField('KeyField', null=True, blank=True, max_length=512)
    old_key_value=models.CharField('KeyValue', null=True, blank=True, max_length=512)
    old_modifyer=models.CharField('Modifyer', null=True, blank=True, max_length=10)
    old_modify_date=models.DateTimeField('ModifyDate', null=False, blank=False)
    old_ipaddress=models.CharField('IPAddress', null=True, blank=True, max_length=50)
    old_computer_name=models.CharField('ComputerName', null=True, blank=True, max_length=50)

    class Meta(SourceRecord.Meta):
        db_table='src_dye_z_revisionkey'
        indexes=[models.Index(fields=['source_batch', 'old_id'],name='src_6ce6431046ff82ba')]
        verbose_name=verbose_name_plural='旧业务字段修改来源键'
        ordering=["-id"]
