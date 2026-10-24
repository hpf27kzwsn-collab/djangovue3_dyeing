"""明确的本地业务查询来源；原行、空值及重复来源分别展示。"""
from functools import partial
from decimal import Decimal
from django.apps import apps

# 查询直接展示已保存的业务字段，不借用备用模型推造状态、数量或计价单位。
SOURCES = {
    'orders': ('订单明细与交付累计', 'erp_sales.SourceDyeOrderColor',
        'CheckNo SheetSeries ProdID ColorNum OrderQty Unit Price Amount SumDlvQty SumDlvRolls DlvDate', 'DlvDate', None),
    'production': ('工卡实际报工', 'erp_production.SourceDyeWProcess',
        'WProcessNo JobSheetNo ProcessNo ProcessID MachineID EmpID StartTime EndTime CurrKg CurrRolls CurrMeter Status', 'StartTime', 'Status'),
    'materials': ('称料计划与实称明细', 'erp_production.SourceDyeStuffWeightDetail',
        'SheetSeries PhaseNo StuffNo StuffID WeightUnit NeedQty RealQty OutTime Status', 'OutTime', 'Status'),
    'quality': ('质量检验与处置', 'erp_quality.SourceDyeWDefect',
        'SheetNo SheetDate JobSheetNo WProcessNo ProcessID DefectQty DefectLengthQty Result Status Remarks', 'SheetDate', 'Status'),
    'packages': ('包装细码与实称', 'erp_warehouse.SourceDyeRecordYield',
        'Guid BarCode JobSheetNo CheckNo ProdID Unit Kg NetKg Meter Rolls GradeID Status PackTime', 'PackTime', 'Status'),
    'prices': ('染整报价与客户确认价', 'erp_sales.SourceDyeFixedPriceDetail',
        'DetailNo SheetSeries ProdID YarnCategory CusPrice Price Pricesum PriceUnit ProcessPrice FenTouPrice MinAmount IsConfirmed', None, None),
    'sampling': ('打样记录与确认版本', 'erp_sampling.SourceDyeDyeDipsRecord',
        'SheetNo SheetDate ColorNo ColorVersion ConfirmVersion CustomerID ProdID EmpID CheckerID ApproveDate RightStatus', 'SheetDate', 'RightStatus'),
    'purchases': ('采购明细与交期', 'erp_purchase.SourceDyePurDetail',
        'DetailNo SheetSeries ApplySheetNo GrayID ArticleID StuffID Qty Rolls Price Amount DlvDate', 'DlvDate', None),
    'schedules': ('机台排程与进度', 'erp_production.SourceDyeProcessSchedule',
        'ID JobSheetNo ProcessNo ProcessID MachineID PlanDate StartTime FinishTime PlanWeightQty PlanRolls Status', 'PlanDate', 'Status'),
    'rework': ('返修及质量责任来源', 'erp_quality.SourceDyeWDefect',
        'WDefectNo SheetNo JobSheetNo WProcessNo Kind DefectDept DefectProcessID DefectEmpID DefectQty DefectLengthQty Result Status Remarks', 'SheetDate', 'Status'),
    'lineage': ('工卡投坯与批次来源', 'erp_production.SourceDyeJobGrayRecord',
        'SheetSeries ReceSheetNo RollNo GrayBarCode BarCode AssignedNo GUnit Rolls WeightQty LengthQty Kg Status', None, 'Status'),
}


def records(reader, filters, key):
    from .reports import page
    title, label, original_fields, date, status = SOURCES[key]
    model = apps.get_model(label)
    names = original_fields.split()
    columns = [model.SOURCE_FIELDS[name] for name in names]
    needed = [*columns, *[model.SOURCE_FIELDS[name] for name in [date,status] if name is not None]]
    query = reader.source(model, needed)
    if key == 'packages' and 'barcode' in filters:
        query = query.filter(old_bar_code=filters['barcode'])
    count, items = page(query, filters, model.SOURCE_FIELDS[date] if date else None,
                        model.SOURCE_FIELDS[status] if status else None)
    return count, [{'id':item.pk, **{old:str(getattr(item, model.SOURCE_FIELDS[old])) if isinstance(getattr(item, model.SOURCE_FIELDS[old]),Decimal) else getattr(item, model.SOURCE_FIELDS[old]) for old in names}} for item in items]


def stock(reader, filters):
    from .source_inventory_queries import FAMILIES, balances
    offset = (filters['page']-1)*filters['page_size']
    total = 0; result = []
    for family in FAMILIES:
        count, _ = balances(reader, {**filters,'page':1,'page_size':0}, family)
        if offset < total+count and len(result) < filters['page_size']:
            _, rows = balances(reader, {**filters,'_offset':max(offset-total,0),
                'page_size':filters['page_size']-len(result)}, family)
            table, title, material, quantities = FAMILIES[family]
            for row in rows:
                result.append({'family':title,'material':row[material], **row})
        total += count
    return total, result


def definitions():
    reports = {}; functions = {}
    for key, (title,label,fields,date,status) in SOURCES.items():
        model = apps.get_model(label)
        reports[key] = {'title':title,'uses_units':False,'columns':[
            ('id','记录ID'), *[(old,str(model._meta.get_field(model.SOURCE_FIELDS[old]).verbose_name)) for old in fields.split()]]}
        if key == 'production':
            reports[key]['columns'] = [(old,{'WProcessNo':'报工流水号','JobSheetNo':'工卡号'}.get(old,label))
                                       for old,label in reports[key]['columns']]
        functions[key] = partial(records, key=key)
    reports['stock'] = {'title':'各仓类实际库存收发汇总','uses_units':False,
        'columns':[('family','仓类'),('material','物料编码'),('WareHouseID','仓库编码'),
                   ('LotNo','批号'),('StorageUnitIDs','库位编码'),('StockUnit','库存单位编码'),('row_count','流水条数'),
                   ('Qty_net','净数量'),('WeightQty_net','净重量'),('LengthQty_net','净长度'),('Rolls_net','净粒数')]}
    functions['stock'] = stock
    return reports, functions
