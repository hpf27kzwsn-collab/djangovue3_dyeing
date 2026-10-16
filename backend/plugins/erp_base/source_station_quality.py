"""原出缸直通率、对色员看板与色级产量；聚合口径和来源分别保留。"""
from plugins.erp_base.source_provenance import reference as source_reference
from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_DOWN
from django.db.models import Q
from django.utils import timezone
from .source_quality_reports import rows, key, total, rounded
from .source_stock_services import raw
from .source_business_updates import matching


MEASURES = {'TotalKg':'ClothQtyKg','ZKg':'ZKg','JKg':'JKg','RTKg':'RTKg',
            'ZNum':'ZNum','JNum':'JNum','RNum':'RNum','TNum':'TNum','JTimes':'JTimes'}


def reference(item, **values):
    return {'entity':item._meta.label,'record_id':item.pk,'source': source_reference(item),**values}


def ratio(numerator, denominator, display=False):
    # 原零分母会中止整张报表；新报告保留该组与全部来源，比例未知。
    if numerator is None or denominator in [None,0]:return None
    value=(rounded(numerator)/Decimal(denominator)).quantize(Decimal('0.0000000000001'),rounding=ROUND_DOWN)*100
    return rounded(value) if display else value


def measures(items, display=False):
    result={name:total([raw(item,column) for item in items]) for name,column in MEASURES.items()}
    for name in ['TotalKg','ZKg','JKg','RTKg']:result[name]=rounded(result[name])
    result.update(Rate=ratio(result['ZNum'],result['TNum'],display),RTRate=ratio(result['RNum'],result['TNum'],display))
    result['ratio_issue']='原TNum为零，比例未定义' if result['TNum']==0 else None
    return result


def dye_rate(start,end,by='shift',query=rows):
    source=list(query('DyeCheckout','erp_quality').filter(old_end_time__gte=start,old_end_time__lte=end).order_by('pk'))
    field='ShiftID' if by=='shift' else 'ColorMatching'
    groups=defaultdict(list)
    for item in source:groups[(key(raw(item,field)),key(raw(item,'ClassID')))].append(item)
    result=[]
    for (code,cls),items in groups.items():
        result.append({field:raw(items[0],field),'ClassID':raw(items[0],'ClassID'),**measures(items),'source_ids':[item.pk for item in items]})
    result.append({field:'合计汇总','ClassID':'合计汇总',**measures(source),'source_ids':[item.pk for item in source]})
    if by=='shift':
        for item in result:item.pop('JTimes')
    return {'report':'Sp_DyeRateNew' if by=='shift' else 'Sp_DyeRateNew_ColorMatching','rows':result,
        'result_rows':[reference(item,**{name:raw(item,name) for name in ['EndTime',field,'ClassID',*MEASURES.values()]}) for item in source],
        'notes':['按原EndTime含起止分组；负数、空班组与空对色员仍计入原组和总合计。',
            '原直通/返修比例按ZNum/RNum除TNum；零分母保留NULL并标明，空结果仍返回原总合计行。']}


def periods(as_of):
    shifted=timezone.localtime(as_of)-timedelta(hours=8)
    today=shifted.date();month=today.replace(day=1)
    last=(month-timedelta(days=1)).replace(day=1)
    next_month=(month.replace(day=28)+timedelta(days=4)).replace(day=1)
    return {'today':str(today),'yesterday':str(today-timedelta(days=1)),
        'month':str(month)[:7],'last':str(last)[:7],
        'start':timezone.make_aware(datetime.combine(last,datetime.min.time()))+timedelta(hours=8),
        'end':timezone.make_aware(datetime.combine(next_month,datetime.min.time()))+timedelta(hours=8)}


def dashboard_source(as_of,query):
    period=periods(as_of)
    selected=Q(old_days__in=[period['today'],period['yesterday']])|Q(old_tmonth__in=[period['month'],period['last']])
    # 原存储的DAYS/TMonth与实际结束时间可能不同；差异来源仍供核对。
    selected |= Q(old_end_time__gte=period['start'],old_end_time__lt=period['end'])
    return period,list(query('DyeCheckout','erp_quality').filter(selected).order_by('pk'))


def color_matching_dashboard(as_of,query=rows):
    period,source=dashboard_source(as_of,query)
    employees=defaultdict(list)
    for item in query('HEmployee','erp_base').order_by('pk'):
        if raw(item,'EmpID') is not None:employees[key(raw(item,'EmpID'))].append(item)
    additions=[]
    weights=query('StuffWeight','erp_production').filter(old_sheet_kind=2,old_recipe_type=1,
        old_sheet_date__gte=period['start'],old_sheet_date__lt=period['end']).order_by('pk')
    for item in weights:
        code=key(raw(item,'ColorMatching'))
        if code in [None,'']:continue
        date=timezone.localtime(raw(item,'SheetDate'))-timedelta(hours=8)
        additions.append((item,code,date.strftime('%Y-%m-%d'),date.strftime('%Y-%m')))
    specs=[(0,'上月合计','TMonth','last',False),(1,'上月总合计','TMonth','last',True),
        (2,'昨日','DAYS','yesterday',False),(3,'今日','DAYS','today',False),
        (4,'本月合计','TMonth','month',False),(4,'本月总合计','TMonth','month',True)]
    result=[];included=set();expanded=[]
    for group,title,date_field,date_key,summary in specs:
        selected=[item for item in source if key(raw(item,date_field))==period[date_key]]
        groups=defaultdict(list);names={}
        for item in selected:
            if summary:groups[(None,'')].append(item);included.add(item.pk)
            else:
                for employee in employees[key(raw(item,'ColorMatching'))]:
                    group_key=(key(raw(item,'ColorMatching')),key(raw(employee,'Name')))
                    groups[group_key].append(item);names.setdefault(group_key,raw(employee,'Name'))
                    expanded.append(reference(item,employee_id=employee.pk,period=title));included.add(item.pk)
        for (code,name),items in groups.items():
            add=[item.pk for item,emp,day,month in additions if (month if date_field=='TMonth' else day)==period[date_key] and (summary or emp==code)]
            result.append({'original_group':group,'DayType':title,'Name':'' if summary else names[(code,name)],
                'ColorMatching':None if summary else raw(items[0],'ColorMatching'),
                **measures(items,True),'DyeAdd':len(add) if add else None,'source_ids':[item.pk for item in items],'addition_ids':add})
    result.sort(key=lambda row:(row['original_group'],row['DayType'],row['Name'] or ''))
    for index,item in enumerate(result,1):item.update(rowindex=index,GroupIndex=index);item.pop('JTimes')
    return {'report':'Sp_DyeRate_ColorMatching_Query','rows':result,'result_rows':expanded,
        'supplemental_rows':[reference(item,ColorMatching=raw(item,'ColorMatching'),DAYS=raw(item,'DAYS'),TMonth=raw(item,'TMonth'),
            issue='未匹配原员工内连接或不在原存储日期范围；原月总量仍按自身规则计算') for item in source
            if item.pk not in included or not employees[key(raw(item,'ColorMatching'))]],
        'notes':['原8点换日，DAYS/TMonth沿用原存储字段；加色次数来自2类、RecipeType=1且对色员非空的称料单。',
            '员工重复连接按原式展开，月总量直接按出缸表；两者可能不相等。原10页上限取消，全部结果返回。',
            '原GroupIndex输出实际是行序号，另保留original_group；同名并列按稳定顺序展示。零分母比例为NULL。']}


def color_depth_dashboard(as_of,mode='legacy',query=rows):
    period,source=dashboard_source(as_of,query)
    classes=list(matching(query('PFieldValid','erp_base'),FieldType='Class').order_by('pk'))
    class_index=defaultdict(list)
    for item in classes:
        if raw(item,'Code') is not None:class_index[key(raw(item,'Code'))].append(item)
    depths=[(key(raw(item,'Code')),raw(item,'Name')) for item in matching(query('PFieldValid','erp_base'),FieldType='ColorDepth').order_by('pk')]+[('10','汇总')]
    specs=[('ZuoRi','DAYS','yesterday',False),('JinRi','DAYS','today',False),('BenYue','TMonth','month',False),
        ('BenYueZongHeJi','TMonth','month',True),('上月ZongHeJi' if mode=='legacy' else 'ShangYueZongHeJi','TMonth','last',True)]
    aggregates=[];used=set()
    for title,date_field,date_key,summary in specs:
        groups=defaultdict(list)
        for item in source:
            if key(raw(item,date_field))!=period[date_key]:continue
            used.add(item.pk)
            for cls in class_index[key(raw(item,'ClassID'))] or [None]:
                name=None if cls is None else key(raw(cls,'Name'))
                typ=title if summary else None if name is None else title+name
                for bucket,depth in [('depth',key(raw(item,'ColorDepthID'))),('total','10')]:
                    grouping=(typ,None if summary else key(raw(item,'ClassID')),depth,bucket)
                    groups[grouping].append(item)
        for (typ,cls,depth,bucket),items in groups.items():
            aggregates.append({'Type':typ,'ClassID':cls,'ColorDepthID':depth,'bucket':bucket,
                'TotalKg':rounded(total([raw(item,'ClothQtyKg') for item in items])),'source_ids':[item.pk for item in items]})
    frame=[prefix+key(raw(cls,'Name')) for prefix in ['ZuoRi','JinRi','BenYue'] for cls in classes if key(raw(cls,'Name')) in ['甲班','乙班']]
    frame+=['BenYueZongHeJi','ShangYueZongHeJi']
    output={};matched=set()
    for code,name in depths:
        target=output.setdefault((code,key(name)),{'original_depth_code':code,'ColorDepthName':name})
        for typ in frame:
            label=typ.replace('甲班','JiaBan').replace('乙班','YiBan')
            values=target.setdefault(label,[])
            for index,row in enumerate(aggregates):
                if code is not None and row['ColorDepthID']==code and row['Type']==typ:
                    values.append(row['TotalKg']);matched.add(index)
    result=[]
    for index,((code,_),row) in enumerate(sorted(output.items(),key=lambda pair:(pair[0][0] or '',pair[0][1] or '')),1):
        result.append({name:total(value) if isinstance(value,list) else value for name,value in row.items()}|{'ColorDepthCode':index})
    return {'report':'Sp_DyeRate_dyeCheckout_Query','rows':result,'result_rows':aggregates,'calculation_mode':mode,
        'supplemental_rows':[dict(row,issue='原框架未匹配的分类汇总，完整保留') for i,row in enumerate(aggregates) if i not in matched]+
            [reference(item,issue='实际时间在核对范围，但原DAYS/TMonth不在统计窗口') for item in source if item.pk not in used],
        'notes':['原班次字典左连接和色级字典框架均保留重复；原色级10与总计10冲突会按原UNION ALL叠加。',
            '默认legacy保留上月ZongHeJi与ShangYueZongHeJi不匹配；matched_month仅明确修正此连接。',
            'ColorDepthCode沿原结果输出行号，original_depth_code另存真实色级码；未知分类列为补充明细。']}
