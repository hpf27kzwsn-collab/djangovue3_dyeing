"""剩余返修报告；财务依赖仅接收有来源的数量，不启用财务业务。"""
from calendar import monthrange
from collections import defaultdict
from datetime import datetime,timedelta
from decimal import Decimal
from django.utils import timezone
from django.db.models.functions import Upper,RTrim
from .source_rework_reports import statistics,repair_sources,by_code
from .source_quality_reports import rows,key,total,rounded
from .source_stock_services import raw


def ratio(numerator,denominator):
    return None if numerator is None or denominator in [None,0] else rounded(Decimal(numerator)/Decimal(denominator)*100)


def months(start,end):
    current=timezone.localtime(start).date().replace(day=1);last=timezone.localtime(end).date().replace(day=1)
    while current<=last:
        yield current.strftime('%Y-%m')
        current=current.replace(year=current.year+1,month=1) if current.month==12 else current.replace(month=current.month+1)


def daily(as_of,query=rows):
    start=timezone.make_aware(datetime.combine(as_of.replace(day=1),datetime.min.time()))
    day=timezone.make_aware(datetime.combine(as_of,datetime.min.time()));end=day+timedelta(days=1,milliseconds=-3)
    works=list(query('WProcess','erp_production').filter(old_create_date__gte=start,old_create_date__lte=end))
    _,sources,supplement=repair_sources(works,query)
    denominators={}
    for station in ['05','06']:
        selected=[work for work in works if key(raw(work,'StationID'))==station]
        # 本过程分母先SUM未逐条舍入的公斤，区别于2/3的两阶段舍入。
        values=[None if raw(work,'CurrDosage') is None or raw(work,'CurrKg') is None else
            raw(work,'CurrDosage')*raw(work,'CurrKg')/100 for work in selected]
        kg=total(values)
        denominators[station]=(sum(raw(work,'CurrDosage') is not None and raw(work,'CurrDosage')>0 for work in selected),
            None if kg is None else rounded(kg/1000))
    grouped=defaultdict(list)
    for source in sources:
        station=key(source['StationID'])
        if station not in ['05','06']:continue
        local=key(source['DefectDept']) in (['07'] if station=='05' else ['02','03','04'])
        grouped[(station,key(source['FabricName']),'本车间' if local else '外车间')].append(source)
    result=[]
    for (station,fabric,workshop),items in grouped.items():
        row={'Num':'A','StationID':station,'StationIDName':'定型' if station=='05' else '溢流',
            'FabricName':items[0]['FabricName'],'Workshop':workshop}
        for period,selected in [('Day',[item for item in items if item['CreateDate']>=day]),('Month',items)]:
            for kind in ['N','K']:
                row[f'{kind}_Num{period}']=sum(item[kind+'_Num'] for item in selected)
                row[f'{kind}_RKg{period}']=rounded(sum((item[kind+'_RKg'] for item in selected),Decimal(0))/1000)
        row['AllMonthNum']=row['N_NumMonth']+row['K_NumMonth']
        # 旧过程先汇总两类未除1000的公斤，再统一舍入，不将已舍入分类重量相加。
        row['ALLMonthKg']=rounded(sum((item['N_RKg']+item['K_RKg'] for item in items),Decimal(0))/1000)
        row['ZNum'],row['ZKg']=denominators[station]
        row['Rate']=ratio(row['ALLMonthKg'],row['ZKg']) if station=='05' else ratio(row['AllMonthNum'],row['ZNum'])
        if row['Rate'] is None:supplement.append({'StationID':station,'FabricName':row['FabricName'],'Workshop':workshop,
            'issue':'原比例分母为零或NULL，比例保留NULL；原SQL零分母会终止报告，当前保留该组全部数量。'})
        result.append(row)
    subtotal=defaultdict(list)
    for row in result:subtotal[(row['StationID'],key(row['FabricName']))].append(row)
    for items in subtotal.values():
        row={name:items[0][name] for name in ['StationID','StationIDName','FabricName']}
        row.update(Num='B',Workshop='小计')
        row.update({name:total([item[name] for item in items]) for name in items[0] if name not in row})
        result.append(row)
    result.sort(key=lambda row:(row['StationID'],row['Num'],key(row['FabricName']) or '',row['Workshop']))
    return {'report':'Sp_ReworkCloth1','rows':result,'result_rows':sources,'supplemental_rows':supplement,
        'notes':['日及月累计截至当日23:59:59.997；05按吨、06按次数计算比例。',
            '布种和车间连接全部保留；原小计SUM每组分母和比例，重复分母不去重。零分母差异见异常说明。']}


def far_summary(evidence,start,end):
    grouped=defaultdict(list)
    for row in evidence:
        if row['sheet_date'] is not None and start<=row['sheet_date']<=end and row['sheet_kind'] in [30,40]:
            grouped[timezone.localtime(row['sheet_date']).strftime('%Y-%m')].append(row)
    result={}
    for month,items in grouped.items():
        quantity=total([item['quantity'] for item in items])
        result[month]={'FARNum':len(items),'FARKg':None if quantity is None else rounded(quantity/1000)}
    return result


def combined(start,end,far_rows,far_reference,query=rows):
    a,b=statistics(start,end,'06',query),statistics(start,end,'05',query)
    far=far_summary(far_rows,start,end);result=[]
    for left,right in zip(a['rows'],b['rows']):
        month=left['month'];row={'month':month,**far.get(month,{'FARNum':None,'FARKg':None})}
        row.update({name:(left[name] or 0)+(right[name] or 0) for name in ['AllNum','AllKg']})
        row.update({name+station:part[name] for station,part in [('06',left),('05',right)] for name in ['N_Num','K_Num','N_RKg','K_RKg']})
        result.append(row)
    return {'report':'Sp_ReworkCloth4','rows':result,'result_rows':[
        {'StationID':station,**row} for station,part in [('06',a),('05',b)] for row in part['result_rows']],
        'supplemental_rows':a['supplemental_rows'],'quantity_sources':far_rows,'quantity_reference':far_reference,
        'notes':['05/06总量按原ISNULL相加；两站返修仍各自保留NULL。',
            'FAR采用已映射的原数量或明确手动输入；重复原连接行保留，未取得来源时保持未知，不代表零业务。']}


def previous_year(value):
    return value.replace(year=value.year-1,day=min(value.day,monthrange(value.year-1,value.month)[1]))


def comparison(start,end,station,mode,far_rows,far_reference,query=rows):
    current=statistics(start,end,station,query)
    last_start,last_end=previous_year(start),previous_year(end)
    repair_works=list(query('WProcess','erp_production').filter(old_create_date__gte=start,old_create_date__lte=end)) if mode=='legacy' else None
    previous=statistics(last_start,last_end,station,query,repair_works=repair_works)
    last={row['month']:row for row in previous['rows']}
    far=far_summary(far_rows,start,end)
    far_last=far if mode=='legacy' else far_summary(far_rows,last_start,last_end)
    result=[];supplement=[{'period':period,**row} for period,part in [('current',current),('previous',previous)] for row in part['supplemental_rows']]
    for row in current['rows']:
        month=row['month'];old_month=str(int(month[:4])-1)+month[4:]
        if row['AllNum'] is None:
            supplement.append({'month':month,'issue':'原INNER JOIN排除此无本期刷卡月份，月份仍在此列示。'});continue
        old=last[old_month]
        far1=far_last.get(old_month,{}).get('FARKg');far2=far.get(month,{}).get('FARKg')
        if mode=='legacy' and month not in far:far1=None
        result_row={'YF':str(int(month[-2:]))+'月','RQ1':old_month,'RQ2':month,'FARKg1':far1,'FARKg2':far2}
        for suffix,source in [('1',old),('2',row)]:
            result_row.update({name+suffix:source[name] for name in ['AllKg','N_RKg','K_RKg']})
            for kind in ['N','K']:result_row[kind+'Rate'+suffix]=ratio(source[kind+'_RKg'],source['AllKg'])
        result.append(result_row)
    return {'report':'Rework_Comparison'+('1' if station=='05' else '2'),'rows':result,
        'result_rows':[{'period':period,**row} for period,part in [('current',current),('previous',previous)] for row in part['result_rows']],
        'supplemental_rows':supplement,'mode':mode,'quantity_sources':far_rows,'quantity_reference':far_reference,
        'notes':['legacy保留旧上年刷卡连接本年返修临时表、上年FAR仍取本期的行为；same_period为明确的同期修正版，不静默替代旧规则。',
            '原YF把缺失FAR显示为0，当前分列FARKg1/2保持NULL和来源；完整月份及原INNER JOIN排除项分别显示。']}


def responsibility(start,end,far_rows,far_reference,query=rows):
    numbers={key(row['job_number']) for row in far_rows if row['job_number'] is not None}
    jobs=list(query('JobSheet','erp_production').alias(code=Upper(RTrim('old_sheet_no'))).filter(code__in=numbers))
    job_index=by_code(jobs,'SheetNo')
    reviews=by_code(query('WDefect','erp_quality').alias(code=Upper(RTrim('old_sheet_no'))).filter(
        code__in={key(raw(job,'LossStr')) for job in jobs if raw(job,'LossStr') is not None}),'SheetNo')
    quantities=['JQty1','JMeter1','YQty1','YMeter1','JQty2','JMeter2','YQty2','YMeter2','Qty3','Meter3','Qty4','Meter4','Qty5','Meter5','AllQty','AllMeter']
    grouped=defaultdict(list);details=[];supplement=[]
    for position,source in enumerate(far_rows):
        joined=[]
        for job in job_index[key(source['job_number'])]:
            for review in reviews[key(raw(job,'LossStr'))]:
                dept,shift=key(raw(review,'DefectDept')),key(raw(review,'DefectClassID'))
                if dept in [None,''] or shift in [None,'']:continue
                joined.append((job,review,dept,shift))
        selected=source['sheet_date'] is not None and start<=source['sheet_date']<=end and source['sheet_kind']==30 and source['zero_amount'] is True
        if not selected or not joined:
            supplement.append({'position':position,**source,'issue':'未满足原30类、零应收、日期及责任部门/班次连接；原数量保留。'});continue
        for job,review,dept,shift in joined:
            month=timezone.localtime(source['sheet_date']).strftime('%Y-%m')
            row=dict.fromkeys(quantities,Decimal(0))
            if dept in ['07','02','03','04']:
                prefix='J' if shift in ['03','05'] else 'Y';suffix='1' if dept=='07' else '2'
                qty,meter=prefix+'Qty'+suffix,prefix+'Meter'+suffix
            else:
                suffix={'12':'3','14':'4'}.get(dept,'5');qty,meter='Qty'+suffix,'Meter'+suffix
            row[qty],row[meter]=source['quantity'],source['metres']
            row['AllQty'],row['AllMeter']=source['quantity'],source['metres']
            row.update(month=month,position=position,legacy_id=source['legacy_id'],header_legacy_id=source['header_legacy_id'],
                job_id=job.pk,review_id=review.pk,DefectDept=raw(review,'DefectDept'),DefectClassID=raw(review,'DefectClassID'))
            grouped[month].append(row);details.append(row)
    result=[]
    for month in months(start,end):
        row={'month':month}
        for name in quantities:
            value=total([item[name] for item in grouped[month]])
            row[name]=None if value is None else rounded(value/(10000 if 'Meter' in name else 1000))
        result.append(row)
    return {'report':'Rework_Comparison3','rows':result,'result_rows':details,'supplemental_rows':supplement,
        'quantity_sources':far_rows,'quantity_reference':far_reference,
        'notes':['原Qty汇总除1000，PreMeter汇总除10000；重复工卡/评审全部展开，03/05与其他班次分别分类。',
            '最新FARDetail无PreMeter；有独立长度依据才输入metres，未提供保持NULL，不用重量推算。财务模块仍不启用。']}
