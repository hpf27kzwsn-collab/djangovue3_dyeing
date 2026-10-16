"""包装最新人员及原按条码人数分摊产量的两个视图。"""
from collections import defaultdict
from decimal import Decimal, ROUND_DOWN, localcontext
from .source_quality_reports import rows, key, total
from .source_station_yield import code_index
from .source_stock_services import raw
from .source_business_updates import matching


def projected(query, fields):
    columns = ['pk', 'legacy_id', *[query.model.SOURCE_FIELDS[name] for name in fields]]
    for values in query.order_by('pk').values_list(*columns).iterator(chunk_size=4000):
        yield dict(zip(['record_id', 'legacy_id', *fields], values))


def latest_packers(number=None, query=rows):
    source = query('RecordYield', 'erp_warehouse')
    # 先全历史按DetailNo求MAX，工卡筛选仅限定视图输出，不能改变最大时间。
    latest = {}
    for item in projected(source, ['DetailNo', 'PackTime']):
        code, time = key(item['DetailNo']), item['PackTime']
        if code is not None and time is not None and (code not in latest or time > latest[code]):
            latest[code] = time
    if number is not None:
        source = matching(source, JobSheetNo=number)
    employees = code_index(query('HEmployee', 'erp_base'), ['EmpID'])
    output = []; excluded = []
    for item in projected(source, ['DetailNo', 'PackTime', 'EmpID', 'JobSheetNo']):
        code = key(item['DetailNo'])
        if code not in latest or item['PackTime'] != latest[code]:
            excluded.append(item['record_id'])
            continue
        for employee in employees[(key(item['EmpID']),)] or [None]:
            output.append({**item, 'employee_id': None if employee is None else employee.pk,
                'Packer': None if employee is None else raw(employee, 'Name')})
    return {'report': 'RecordYield_EmpID 最新包装人员', 'rows': output,
        'supplemental_rows': [{'issue': '不是DetailNo全历史最大包装时间，或关联字段为NULL',
            'source_entity': 'erp_warehouse_sourcedyerecordyield', 'source_ids': excluded, 'count': len(excluded)}],
        'notes': ['同DetailNo最新时间并列及重复员工连接均保留；原视图无DISTINCT。未命中原行仍可在包装原表查询。']}


def shared_yield(number=None, mode='legacy_barcode', query=rows):
    source = query('RecordYield', 'erp_warehouse')
    if number is not None:
        source = matching(source, JobSheetNo=number)
    assignments = defaultdict(list)
    for item in projected(query('RecordEmp', 'erp_production'), ['BarCode', 'EmpID']):
        assignments[key(item['BarCode'])].append(item)
    groups = {}; unmatched = []; used = set()
    join_field = 'BarCode' if mode == 'legacy_barcode' else 'Guid'
    for item in projected(source, [join_field, 'JobSheetNo', 'ShiftID', 'CustQty']):
        barcode = key(item[join_field])
        members = assignments[barcode] if barcode is not None else []
        if not members:
            unmatched.append(item['record_id']); continue
        for member in members:
            used.add(member['record_id'])
            code = (key(item['JobSheetNo']), key(item['ShiftID']), key(member['EmpID']))
            group = groups.setdefault(code, {'JobSheetNo': item['JobSheetNo'], 'ShiftID': item['ShiftID'],
                'EmpID': member['EmpID'], 'values': [], 'sources': []})
            with localcontext() as context:
                context.prec = 40
                amount = None if item['CustQty'] is None else (item['CustQty'] / len(members)).quantize(Decimal('0.000000000001'), rounding=ROUND_DOWN)
            group['values'].append(amount)
            group['sources'].append({'record_id': item['record_id'], 'employee_record_id': member['record_id'], 'people': len(members), 'Qty': amount})
    output = []
    for group in groups.values():
        amount = total(group.pop('values'))
        output.append({**group, 'Qty': amount})
    # 补充区列出全部未参与ID和数量；不把无法相连的原记录伪造为零产量。
    employee_ids = [item['record_id'] for members in assignments.values() for item in members if item['record_id'] not in used]
    return {'report': 'V_RecordYield 包装多人分摊产量', 'mode': mode, 'rows': output, 'supplemental_rows': [
        {'issue': '包装条码没有对应人员行', 'source_entity': 'erp_warehouse_sourcedyerecordyield', 'source_ids': unmatched, 'count': len(unmatched)},
        {'issue': '人员条码未参与本次范围的包装连接', 'source_entity': 'erp_production_sourcedyerecordemp', 'source_ids': employee_ids, 'count': len(employee_ids)}],
        'notes': ['人数是同条码人员原行COUNT，不是员工去重数；重复条码会连接多条包装。',
            'CustQty按原decimal(10,1)/int结果截断至12位小数再SUM；NULL不补零，负数照算。',
            'legacy_barcode按原视图BarCode连接；entry_guid按原QueryRecordEmp主从元数据Guid连接，属于明确选择的修正版，不能混称原视图。']}
