"""普通工位和两类包装产量的原连接、分组和来源核对。"""
from collections import defaultdict
from datetime import timedelta
from django.db.models.functions import Upper,RTrim
from django.utils import timezone
from .source_stock_services import raw
from .source_quality_reports import rows,key,total
from .source_business_updates import matching
from .source_station_quality import reference


def normalized(value):
    return key(value) if isinstance(value,str) else value


def code_index(items,fields):
    result=defaultdict(list)
    for item in items:
        code=tuple(normalized(raw(item,name)) for name in fields)
        if None not in code:result[code].append(item)
    return result


def work_quantity(start,end,query=rows):
    works=list(query('WProcess','erp_production').filter(old_end_time__gte=start,old_end_time__lte=end).order_by('pk'))
    numbers={key(raw(item,'JobSheetNo')) for item in works if raw(item,'JobSheetNo') is not None}
    def relevant(name):
        return query(name,'erp_production').alias(job_code=Upper(RTrim('old_job_sheet_no' if name=='JobShiftEmp' else 'old_sheet_no'))).filter(job_code__in=numbers).order_by('pk')
    fields=['JobSheetNo','ShiftID','ProcessNo','ProcessID','WProcessNo']
    assignments=code_index(relevant('JobShiftEmp'),fields)
    jobs=code_index(relevant('JobSheet'),['SheetNo'])
    processes=code_index(query('PProcess','erp_base'),['ProcessID'])
    # 原p_Shift为左连接且无投影字段，DISTINCT后不改变结果。
    output={};supplement=[];expanded=[]
    columns=['WProcessNo','JobSheetNo','ProcessNo','ProcessID','StationID','MachineID','ShiftID','StartTime','EndTime','CurrRolls','CurrKg']
    for item in works:
        code=tuple(normalized(raw(item,name)) for name in fields)
        members=assignments[code];parents=jobs[(key(raw(item,'JobSheetNo')),)]
        process=processes[(key(raw(item,'ProcessID')),)]
        if key(raw(item,'StationID')) in [None,'02'] or not members or not parents or not process:
            supplement.append(reference(item,**{name:raw(item,name) for name in columns},
                issue='原排除02/NULL工位，或缺少班组报工人员、工卡、工序内连接',employee_matches=len(members),job_matches=len(parents),process_matches=len(process)))
            continue
        for parent in parents:
            values={name:raw(item,name) for name in columns}
            values.update({name:raw(parent,source) for name,source in [('OrderSheetNo','OrderSheetNo'),('CustomerID','CustomerID'),('ProdID','CustSelfProduct'),('ColorNum','ColorNum'),('ColorID','ColorID')]})
            values['Days']=(timezone.localtime(raw(item,'EndTime'))-timedelta(minutes=470)).strftime('%Y-%m-%d')
            group=tuple(normalized(value) for value in values.values())
            result=output.setdefault(group,{**values,'source_ids':[]})
            result['source_ids'].append(item.pk)
            expanded.append(reference(item,job_id=parent.pk,employee_ids=[row.pk for row in members],process_ids=[row.pk for row in process]))
    return {'report':'v_WProcess_WorkQty','rows':list(output.values()),'supplemental_rows':supplement,'result_rows':expanded,
        'notes':['原视图DISTINCT按输出业务字段去重，全部参与原记录ID另外保留；不按条码或流水号删原行。',
            'EndTime减470分钟后取日期，即7点50分换日；与染色质量8点换日分别计算。',
            '原内连接未匹配或02/NULL工位进入补充明细。此报表不生成工资和财务记录。']}


def distinct_values(items,field):
    result={}
    for item in items:
        value=raw(item,field)
        if value is not None:result.setdefault(normalized(value),value)
    return result


def package_yield(start=None,end=None,by='employee',filters=None,query=rows):
    grouping=['EmpID' if by=='employee' else 'WindingID','ProdID','ColorNum']
    queryset=query('RecordYield','erp_warehouse')
    if start is not None:queryset=queryset.filter(old_sheet_date__gte=start)
    if end is not None:queryset=queryset.filter(old_sheet_date__lte=end)
    for field,value in ({} if filters is None else filters).items():queryset=matching(queryset,**{field:value})
    selected=list(queryset.order_by('pk'))
    groups=defaultdict(list)
    for item in selected:groups[tuple(normalized(raw(item,name)) for name in grouping)].append(item)
    gray=code_index(query('PGray','erp_base'),['GrayID']) if by=='employee' else {}
    combo=code_index(matching(query('SDBComboValue','erp_base'),ComboID='Z017'),['KeyValue']) if by=='employee' else {}
    employees=code_index(query('HEmployee','erp_base'),['EmpID']) if by=='winding' else {}
    result=[];expanded=[];supplement=[]
    for group,original in groups.items():
        joined=[];kinds=[]
        for item in original:
            if by=='employee':
                for material in gray[(key(raw(item,'ProdID')),)] or [None]:
                    for dictionary in ([] if material is None else combo[(key(raw(material,'RSKind')),)]) or [None]:
                        joined.append(item)
                        if dictionary is not None and raw(dictionary,'DisplayValue') is not None:kinds.append(raw(dictionary,'DisplayValue'))
                        expanded.append(reference(item,material_id=None if material is None else material.pk,dictionary_id=None if dictionary is None else dictionary.pk))
            else:joined.append(item);expanded.append(reference(item))
        dates=[raw(item,'SheetDate') for item in joined if raw(item,'SheetDate') is not None]
        row={name:'0' if raw(original[0],name) is None else raw(original[0],name) for name in grouping}
        row.update(SheetDate=max(dates) if dates else None,Rolls=total([raw(item,'Rolls') for item in joined]),
            NetKg=total([raw(item,'NetKg') for item in joined]),source_ids=[item.pk for item in joined],
            original_group={name:raw(original[0],name) for name in grouping})
        if by=='employee':row.update(Packs=len(joined),CustQty=sum(raw(item,'CustQty') or 0 for item in joined),pinzhong=max(kinds,key=key) if kinds else None)
        # 原多值字符串子查询未带日期条件；保持同组全历史来源，同时单列越界行。
        text_fields=['ColorID','JobSheetNo','PackBag','TubeWeight'] if by=='employee' else ['ColorID','JobSheetNo','CustSelfNo','EmpID']
        multi=any(len(distinct_values(joined,field))>1 for field in text_fields)
        historical=list(matching(query('RecordYield','erp_warehouse'),**dict(zip(grouping,group))).order_by('pk')) if multi else []
        for field in text_fields:
            values=distinct_values(joined,field)
            if len(values)==1:row[field]=str(next(iter(values.values())))
            elif not values:row[field]='' if field in ['PackBag','TubeWeight'] else None
            else:
                candidates=distinct_values(historical,field)
                if by=='winding' and field=='EmpID':
                    names={}
                    for code in candidates:
                        matches=employees[(code,)]
                        for person in matches:
                            if raw(person,'Name') is not None:names.setdefault(key(raw(person,'Name')),raw(person,'Name'))
                        if len(matches)>1:supplement.append({'employee_code':code,'employee_ids':[person.pk for person in matches],
                            'issue':'旧员工标量子查询多行会失败；新结果列出全部姓名，不任选一人'})
                    candidates=names
                width=10 if field=='ColorID' else 50
                text=';'.join(str(value)[:width] for _,value in sorted(candidates.items(),key=lambda pair:str(pair[0])))
                row[field]=text or None
        included={item.pk for item in original}
        supplement.extend(reference(item,issue='参与原多值字符串拼接，但不在本次数量过滤范围',**{name:raw(item,name) for name in grouping+text_fields}) for item in historical if item.pk not in included)
        result.append(row)
    return {'report':'sp_SimpleRecordYieldQuery' if by=='employee' else 'sp_RecordYieldByWinding',
        'rows':result,'result_rows':expanded,'supplemental_rows':supplement,
        'notes':['实称包装按原SheetDate过滤；原NULL分组显示0但original_group保留真实NULL，不与实际0组混并。',
            '员工产量的物料/品种字典重复连接会放大Packs、Rolls、NetKg，按原式保留；原记录ID可追溯。',
            '多值字段按原同组全历史拼接，数量仍仅统计过滤范围；无序字符串改按稳定编码顺序，原截断长度保留。',
            '原工号/品名参数声明INT但实际列为文本，新参数接受原编码原文；非数字编码不被跳过。']}
