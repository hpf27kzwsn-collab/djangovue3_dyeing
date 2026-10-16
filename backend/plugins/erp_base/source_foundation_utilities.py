"""原分页与临时表展列的service实现；参数为已授权的数据，不接收可执行SQL。"""
from collections import defaultdict
from decimal import Decimal
from .source_quality_reports import key, total


def sort_value(value):
    return (value is not None,key(value) if isinstance(value,str) else value)


def page(values, order_fields, size, index, variant='Pro_GetPageData', descending=True):
    result=list(values)
    for field in reversed(order_fields):
        result.sort(key=lambda row:sort_value(row[field]),reverse=descending)
    count=len(result)
    if variant=='Pro_GetPageData':
        pages=int((count-1)/size)+1  # 原零页尺寸是除零错误，不代填10。
        if index>pages:index=pages
        upper=index*size;lower=(index-1)*size
        if upper<0:raise ValueError('原TOP行数不能为负数。')
        result=[{**row,'ROWNUM':n} for n,row in enumerate(result[:upper],1) if n>lower]
    elif variant=='spSqlPageByRowNumber':
        if index is None or size is None:return {'rows':[],'total':count}
        if index<=0:index=1
        lower=(index-1)*size;upper=index*size
        result=[{**row,'rowId':n} for n,row in enumerate(result,1) if lower<n<=upper]
    else:
        raise KeyError(variant)
    return {'rows':result,'total':count}


PIVOT_GROUP=['RQ','Years','RQDay','ShiftID','ShifAmount','ShifSCAmount','Supplements','Subtotal','SumNum']


def row_to_column(records):
    """RowToColumn：九列分组、员工列SUM；未分配员工也保留。"""
    groups={};employees={}
    for row in records:
        identity=tuple(key(row[f]) if isinstance(row[f],str) else row[f] for f in PIVOT_GROUP)
        employee=key(row['EmpID']);employees.setdefault(employee,row['EmpID'])
        if identity not in groups:groups[identity]={'head':{f:row[f] for f in PIVOT_GROUP},'values':defaultdict(list)}
        groups[identity]['values'][employee].append(row['EmpIDSubtotal'])
    columns={employee:'employee_'+str(index) for index,employee in enumerate(employees,1)}
    output=[{**group['head'],**{column:total(group['values'][employee]) for employee,column in columns.items()}} for group in groups.values()]
    output.sort(key=lambda row:tuple(sort_value(row[f]) for f in PIVOT_GROUP))
    return {'report':'RowToColumn','rows':output,'columns':list(columns.values()),
        'column_mapping':[{'column':columns[employee],'EmpID':original} for employee,original in employees.items()],
        'notes':['员工名称按原编号作列；无员工编号的数据单列保留，不通过动态SQL丢弃。']}


def employee_columns(records, variant):
    """Sp_DyeRowDenormaliser/Sp_WagesRowDenormaliser；保留旧两位列号和扩展列的对应。"""
    fields=['Kind','EmpID','Years','ShiftID'] if variant=='Sp_DyeRowDenormaliser' else ['EmpID','Years','ShiftID']
    unique={tuple(key(row[f]) if isinstance(row[f],str) else row[f] for f in fields):{f:row[f] for f in fields} for row in records}
    ordered=sorted(unique.values(),key=lambda row:tuple(sort_value(row[f]) for f in fields))
    employees={key(row['EmpID']) for row in records};groups={};columns=[]
    for n,row in enumerate(ordered,1):
        column='Emp'+str(n).zfill(2)
        columns.append({'column':column,'original_column':'Emp'+('000'+str(n))[-2:],
                        'original_column_selected':n<=len(employees),'EmpID':row['EmpID']})
        identity=(key(row['Years']),key(row['ShiftID']))
        group=groups.setdefault(identity,{'Years':row['Years'],'ShiftID':row['ShiftID']})
        group[column]=row['EmpID']
    output=[{**{'Years':row['Years'],'ShiftID':row['ShiftID']},**{c['column']:row.get(c['column']) for c in columns}} for row in groups.values()]
    return {'report':variant,'rows':output,'column_mapping':columns,
        'notes':['原列清单仅按员工数生成、明细却按员工/月份/班组生成；新表保留全部组，超99列不重复覆盖，原列号及原是否选中同时列出。']}


def export_original(query):
    """sp_GenInsertSQL的迁移替代：完整原字段与旧erpID，二进制不再写成NULL。"""
    import base64
    from datetime import date,datetime
    def value(raw):
        if isinstance(raw,(bytes,memoryview)):return {'encoding':'base64','value':base64.b64encode(raw).decode('ascii')}
        if isinstance(raw,Decimal):return str(raw)
        if isinstance(raw,(date,datetime)):return raw.isoformat()
        return raw
    return [{'record_id':item.pk,'legacy_id':item.legacy_id,
             'values':{old:value(getattr(item,new)) for old,new in item.SOURCE_FIELDS.items()}} for item in query.order_by('pk')]
