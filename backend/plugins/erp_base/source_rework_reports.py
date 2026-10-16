"""Sp_ReworkCloth2/3月度返修统计；完整保留旧连接倍增及未归类刷卡。"""
from plugins.erp_base.source_provenance import reference as source_reference
from collections import defaultdict
from decimal import Decimal
from itertools import product
from django.utils import timezone
from .source_business_updates import matching
from .source_quality_reports import rows, key, total, rounded
from .source_stock_services import raw


def by_code(source, field):
    groups=defaultdict(list)
    for row in source:
        value=key(raw(row,field))
        if value is not None:groups[value].append(row)
    return groups


def weighted(dosage, weight, coalesce=False):
    if coalesce:dosage,weight=0 if dosage is None else dosage,0 if weight is None else weight
    return None if dosage is None or weight is None else rounded(Decimal(str(dosage))*Decimal(str(weight))/100)


def repair_sources(works, query):
    numbers={raw(row,'JobSheetNo') for row in works if raw(row,'JobSheetNo') is not None}
    # 大小写/尾空格按原业务码匹配，避免直接IN把已证明的对应遗漏。
    from django.db.models.functions import Upper,RTrim
    jobs=list(query('JobSheet','erp_production').alias(code=Upper(RTrim('old_sheet_no'))).filter(code__in={key(value) for value in numbers}))
    job_index=by_code(jobs,'SheetNo')
    review_numbers={key(raw(job,'LossStr')) for job in jobs if raw(job,'LossStr') is not None}
    reviews=query('WDefect','erp_quality').alias(code=Upper(RTrim('old_sheet_no'))).filter(code__in=review_numbers)
    review_index=by_code(reviews,'SheetNo')
    gray_index=by_code(query('PGray','erp_base'),'GrayID')
    dictionary=query('PFieldValid','erp_base')
    fabric=by_code(matching(dictionary,FieldType='FabricKind'),'Code')
    departments=by_code(matching(dictionary,FieldType='Defects'),'Code')
    repair=defaultdict(list);supplement=[];expanded=[]
    for work in works:
        sources=[]
        dosage=raw(work,'CurrDosage')
        for job in job_index[key(raw(work,'JobSheetNo'))]:
            for review in review_index[key(raw(job,'LossStr'))]:
                department,kind=key(raw(review,'DefectDept')),raw(review,'Kind')
                if department in [None,''] or key(kind) in [None,''] or dosage is None or dosage<=0:continue
                for gray in gray_index[key(raw(job,'ProdID'))] or [None]:
                    fabric_key=None if gray is None else key(raw(gray,'FabricKindID'))
                    for cloth,dept in product(fabric[fabric_key] or [None],departments[department] or [None]):
                        kg=weighted(dosage,raw(work,'CurrKg'),True)
                        sources.append({'work_id':work.pk,'source': source_reference(work),'job_id':job.pk,'review_id':review.pk,
                            'fabric_id':None if cloth is None else cloth.pk,'department_id':None if dept is None else dept.pk,
                            'FabricName':None if cloth is None else raw(cloth,'Description'),
                            'StationID':raw(work,'StationID'),'CreateDate':raw(work,'CreateDate'),
                            'Kind':kind,'DefectDept':raw(review,'DefectDept'),'RKg':kg,
                            'N_Num':1 if key(kind)=='内部评审' else 0,'K_Num':1 if key(kind)=='客退评审' else 0,
                            'N_RKg':kg if key(kind)=='内部评审' else Decimal(0),'K_RKg':kg if key(kind)=='客退评审' else Decimal(0)})
        expanded.extend(sources)
        if key(raw(work,'StationID')) in ['05','06']:
            code=key(raw(work,'WProcessNo'))
            if code is not None:repair[code].extend(sources)
        if not sources or key(raw(work,'StationID')) not in ['05','06'] or any(key(row['Kind']) not in ['内部评审','客退评审'] for row in sources):
            supplement.append({'record_id':work.pk,'source': source_reference(work),'StationID':raw(work,'StationID'),
                'CurrDosage':dosage,'CurrKg':raw(work,'CurrKg'),'issue':'未进入原返修分类，原刷卡及数量保留。'})
    return repair,expanded,supplement


def statistics(start, end, station, query=rows, repair_works=None):
    works=list(query('WProcess','erp_production').filter(old_create_date__gte=start,old_create_date__lte=end).order_by('pk'))
    repair,expanded,supplement=repair_sources(works if repair_works is None else repair_works,query)
    if repair_works is not None:
        # 同比原程序借用本期返修来源，但补充明细仍列本次统计期间的真实刷卡。
        supplement=[{'record_id':work.pk,'source': source_reference(work),'StationID':raw(work,'StationID'),
            'CurrDosage':raw(work,'CurrDosage'),'CurrKg':raw(work,'CurrKg'),
            'issue':'原同期刷卡未进入所采用的返修分类，原刷卡及数量保留。'} for work in works
            if key(raw(work,'StationID')) not in ['05','06'] or not repair[key(raw(work,'WProcessNo'))]
            or any(key(row['Kind']) not in ['内部评审','客退评审'] for row in repair[key(raw(work,'WProcessNo'))])]
    grouped=defaultdict(list);details=[]
    for work in works:
        if key(raw(work,'StationID'))!=station:continue
        month=timezone.localtime(raw(work,'CreateDate')).strftime('%Y-%m')
        for source in repair[key(raw(work,'WProcessNo'))] or [None]:
            data={'month':month,'record_id':work.pk,'source': source_reference(work),'WProcessNo':raw(work,'WProcessNo'),
                'AllNum':1,'AllKg':weighted(raw(work,'CurrDosage'),raw(work,'CurrKg')),
                **{name:None if source is None else source[name] for name in ['N_Num','K_Num','N_RKg','K_RKg']},
                'repair_source':source}
            grouped[month].append(data);details.append(data)
    # 原SPT_VALUES日序列缺少同日/结束月及长区间；新报告按实际请求月份完整列出。
    current=timezone.localtime(start).date().replace(day=1);last=timezone.localtime(end).date().replace(day=1)
    results=[]
    while current<=last:
        month=current.strftime('%Y-%m');items=grouped[month]
        sums={name:total([entry[name] for entry in items]) for name in ['AllNum','AllKg','N_Num','K_Num','N_RKg','K_RKg']}
        for name in ['AllKg','N_RKg','K_RKg']:
            sums[name]=None if sums[name] is None else rounded(sums[name]/1000)
        results.append({'month':month,**sums})
        current=current.replace(year=current.year+1,month=1) if current.month==12 else current.replace(month=current.month+1)
    return {'report':'Sp_ReworkCloth'+('2' if station=='05' else '3'),'rows':results,
        'result_rows':details,'supplemental_rows':supplement,
        'notes':['按CreateDate含起止时间；AllKg先逐条按CurrDosage×CurrKg/100保留两位，再汇总除1000；返修数量按原ISNULL规则。',
            '同刷卡流水多行、同号工卡/评审和重复字典连接均展开；原重复连接会增加AllNum，不按记录总数替代。',
            '月份按完整请求区间列出；与原SPT_VALUES日序列边界差异单独登记。未归类及负数原记录另列。']}
