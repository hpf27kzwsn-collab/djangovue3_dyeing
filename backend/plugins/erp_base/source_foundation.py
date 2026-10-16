"""已核实的基础资料查询、主体名单、原单位和日期函数。"""
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from .source_business_updates import matching
from .source_package_labels import varchar
from .source_quality_reports import rows
from .source_stock_services import raw
from .source_trial_steps import equal


def decimal10_2(value):
    if value is None:
        return None
    result = Decimal(str(value)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    if abs(result) >= Decimal('100000000'):
        raise OverflowError('原decimal(10,2)字段溢出。')
    return result


def convert_unit(source_unit, destination_unit, quantity):
    """dye.convertUnit；其他组合原函数直接返回数量，包括NULL单位。"""
    value = decimal10_2(quantity)
    if value is None:
        return None
    pair = source_unit, destination_unit
    if pair == (0, 2):
        value /= Decimal('.9144')
    elif pair == (2, 0):
        value *= Decimal('.9144')
    elif pair == (1, 3):
        value *= Decimal('2.2046')
    elif pair == (3, 1):
        value /= Decimal('2.2046')
    return decimal10_2(value)


def get_days(start, end):
    """dbo.fn_GetDays和dye.fn_GetDays：实库master..spt_values的P为0～2047。"""
    if start is None or end is None:
        return []
    return [{'days': start+timedelta(days=n)} for n in range(min(2048, (end-start).days+1))]


def source_row(item, fields):
    return {'entity': item._meta.label, 'record_id': item.pk, 'legacy_id': item.legacy_id,
            **{field: raw(item, field) for field in fields}}


def business_units(employee, query=rows):
    """fn_ConcatBusinessUnitID、fn_ConcatBusinessUnitName；无员工或空主体遍历原字典。"""
    employees = list(matching(query('HEmployee', 'erp_base'), EmpID=varchar(employee, 30)).order_by('pk'))
    dictionary = list(matching(query('PFieldValid', 'erp_base'), FieldType='BusinessUnit').order_by('old_code', 'pk'))
    value = ''
    for person in employees:
        value = varchar(raw(person, 'BusinessUnitID') or '', 100)
    if equal(value, ''):
        for item in dictionary:
            code = raw(item, 'Code')
            value = None if code is None else varchar((value or '')+';'+code, 100)
        value = value[1:] if value else None  # SQL STUFF('',1,1,'')返回NULL。
    names = ''
    selected = []
    if value is not None and not equal(value, ''):
        for item in dictionary:
            code = raw(item, 'Code')
            # 原CHARINDEX只检查尾部分隔符；不能改成split后的精确集合判断。
            if code is not None and (code+';').upper() in (value+';').upper():
                selected.append(item)
                name = raw(item, 'Name')
                names = None if name is None else varchar((names or '')+';'+name, 200)
        names = names[1:] if names else None
    return {'report': '原员工主体名单', 'unit_ids': value, 'unit_names': varchar(names, 100),
            'rows': [source_row(item, ['Code', 'Name', 'IsStop']) for item in selected],
            'employee_candidates': [source_row(item, ['EmpID', 'BusinessUnitID']) for item in employees],
            'notes': ['主体代码来自p_FieldValid.BusinessUnit；不据此替代机台分厂的p_Dept关系。',
                      '重复员工按项目ID最后一条，无序字典统一按Code和项目ID；全部候选留明，见E101。']}


LOOKUPS = {
    'B049': ('PFieldValid', 'Name', 'Name', 'ArticleUnit'),
    'B062': ('PDept', 'DeptID', 'Name', None),
    'B084': ('PFieldValid', 'Code', 'Name', 'Station'),
    'B085': ('PFieldValid', 'Code', 'Name', 'WorkShop'),
}


def lookup(lookup_id, query=rows):
    if lookup_id not in ['B049', 'B062', 'B084', 'B085']:
        from .source_foundation_queries import lookup as original_lookup
        result = original_lookup(lookup_id, query=query)
        result['rows'] = [dict(row, value=row['id'], label=row['text']) for row in result['rows']]
        return result
    table, code, name, kind = LOOKUPS[lookup_id]
    source = query(table, 'erp_base')
    if kind is not None:
        source = matching(source, FieldType=kind)
    items = list(source.order_by('pk'))
    if lookup_id == 'B062':
        items = [item for item in items if raw(item, 'DeptID') is not None and not equal(raw(item, 'DeptID'), '00')]
    return {'report': '原基础资料选项 '+lookup_id,
            'rows': [dict(source_row(item, [code, name]), value=raw(item, code), label=raw(item, name)) for item in items],
            'notes': ['沿用原Lookup筛选，不额外排除停用资料，不去重，不将原编码替换成新系统ID。']}


CORRESPONDENCE = {
    'p_Machine': {'BusinessUnitID': 'B062', 'DeptID': 'B062', 'StationID': 'B084', 'WorkShopID': 'B085'},
    'h_Employee': {'DeptID': 'B062'},
    'p_Article': {'Unit': 'B049'},
    'p_Customer': {'AreaID': 'B024', 'CorpKindID': 'B047', 'CountryID': 'B046',
                   'CreditGrade': 'B013', 'CustKindID': 'B007', 'AddrDlv': 'B048', 'MasterCustomer': 'A002'},
    'p_Gray': {'CustomerID': 'B001', 'FabricKindID': 'B003', 'FatherGrayID': 'B405', 'ProductionID': 'B005',
               'RSKind': 'S021', 'JNKind': 'S022', 'STKind': 'S023', 'ZTKind': 'S024', 'JTKind': 'S025'},
}


def correspondence(item, query=rows):
    result = []
    for field, lookup_id in CORRESPONDENCE[item.SOURCE_TABLE].items():
        value = raw(item, field)
        candidates = [row for row in lookup(lookup_id, query)['rows'] if equal(row['value'], value)]
        result.append({'field': field, 'original_value': value, 'lookup': lookup_id, 'matches': candidates,
                       'matched_count': len(candidates)})
    return {'report': '原基础资料对应核对', 'rows': result,
            'notes': ['无匹配、多匹配和空编码原样展示；本查询不自动建立新组织/工厂对应，也不改写旧值。',
                      '机台BusinessUnitID原编辑器B062指向部门，不是员工主体字典；机物料Unit按名称选取，见E101。']}


def salary_changes_saved(item):
    """SalaryChanges_InUp；原行导入独立保存，业务保存执行当前有效规则。"""
    if item.source_batch_id is not None or item.legacy_id is not None:
        return
    if raw(item, 'Kind') in (3, 4) and not matching(rows('JobSheet', 'erp_production'), SheetNo=raw(item, 'JobSheetNo')).exists():
        raise ValidationError({'old_job_sheet_no': '原工卡调整规则：Kind为3或4时，生产编号必须存在。'})
