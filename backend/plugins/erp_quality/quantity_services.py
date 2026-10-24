"""质量统计读取客户本地数量集，保留空值和重复行。"""
from django.db.models import Q


def automatic(start,end,batches,sources,batch=None,previous_start=None,previous_end=None):
    batch=batch if batch is not None else batches.order_by('-create_datetime','-pk').first()
    if batch is None:
        return [],'尚未录入质量统计数量集',{'state':'unavailable','batch_id':None,'visible_rows':0}
    period=Q(sheet_date__gte=start,sheet_date__lte=end)|Q(sheet_date__isnull=True)
    if previous_start is not None:period |= Q(sheet_date__gte=previous_start,sheet_date__lte=previous_end)
    selected=sources.filter(batch=batch).filter(period).order_by('pk')
    names=['detail_no','header_sheet_series','sheet_date','sheet_kind','job_number','quantity','metres','zero_amount','out_detail_no','stock_unit','business_unit']
    result=[{name:getattr(row,name) for name in names}|{'source_id':row.pk,'batch_id':batch.pk} for row in selected]
    return result,(batch.name or '数量集 #'+str(batch.pk)),{
        'state':'mapped','batch_id':batch.pk,'visible_rows':len(result),'batch_rows':sources.filter(batch=batch).count()}


def ten_day_denominators(as_of,batches,sources,batch=None):
    from plugins.erp_base.source_quality_reports import period_dates,key,total
    start,end,month=period_dates(as_of,2)
    data,reference,status=automatic(month,end,batches,sources,batch)
    result=dict.fromkeys(['DayAllNum','DayAllKg','MonthAllNum','MonthAllKg'])
    if status['state']=='mapped':
        for period,begin in [('Day',start),('Month',month)]:
            selected=[row for row in data if row['sheet_date'] is not None and begin<=row['sheet_date']<=end]
            result[period+'AllNum']=len({key(row['job_number']) for row in selected if row['job_number'] is not None})
            result[period+'AllKg']=total([row['quantity'] for row in selected])
    return result,data,reference,status
