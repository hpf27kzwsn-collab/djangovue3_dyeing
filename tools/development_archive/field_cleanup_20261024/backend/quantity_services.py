"""质量原数量文件映射及报告自动取数；每个抽取版本完整保留。"""
import hashlib
import json
from datetime import datetime
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from plugins.erp_base.business import persist,record
from .quantity_models import QualityQuantityBatch,QualityQuantitySource


def source_date(value):
    if value is None:return None
    parsed=datetime.fromisoformat(value)
    return timezone.make_aware(parsed) if timezone.is_naive(parsed) else parsed


@transaction.atomic
def import_quantities(path,actor):
    content=path.read_bytes();digest=hashlib.sha256(content).hexdigest()
    existing=QualityQuantityBatch.objects.filter(sha256=digest).first()
    if existing is not None:return existing
    data=json.loads(content.decode('utf-8-sig'))
    if data['format']!='erp-quality-quantity-v1' or data['row_count']!=len(data['rows']):
        raise ValidationError('质量数量文件格式或行数不符。')
    batch=persist(QualityQuantityBatch(sha256=digest,database_name=data['database'],captured_at=source_date(data['captured_at']),
        row_count=data['row_count'],length_available=data['length_available'],evidence={key:value for key,value in data.items() if key!='rows'}),actor)
    for index,row in enumerate(data['rows'],1):
        values={name:row[name] for name in ['detail_sheet_series','sheet_kind','business_unit','job_number','out_detail_no','stock_unit','zero_amount']}
        values.update({name:None if row[name] is None else Decimal(row[name]) for name in ['quantity','metres']})
        persist(QualityQuantitySource(batch=batch,source_row=index,detail_no=row['detail_key'],
            header_sheet_series=row['header_key'],
            sheet_date=source_date(row['sheet_date']),**values),actor)
    record(batch,'quality_quantities_imported',{'exists':False},actor,'完整质量数量投影；只读原来源，不生成财务或库存单据')
    return batch


def automatic(start,end,batches,sources,batch=None,previous_start=None,previous_end=None):
    batch=batch if batch is not None else batches.order_by('-captured_at','-pk').first()
    if batch is None:
        return [],'尚无已映射质量数量批次',{'state':'unavailable','batch_id':None,'visible_rows':0}
    period=Q(sheet_date__gte=start,sheet_date__lte=end)|Q(sheet_date__isnull=True)
    if previous_start is not None:period |= Q(sheet_date__gte=previous_start,sheet_date__lte=previous_end)
    selected=sources.filter(batch=batch).filter(period).order_by('source_row')
    result=[{name:getattr(row,name) for name in ['detail_no','header_sheet_series','sheet_date','sheet_kind','job_number','quantity','metres','zero_amount']}
        | {'source_id':row.pk,'source_row':row.source_row,'batch_id':batch.pk,'out_detail_no':row.out_detail_no,
            'stock_unit':row.stock_unit,'business_unit':row.business_unit} for row in selected]
    return result,f'{batch.database_name} / 批次{batch.pk} / {batch.captured_at.isoformat()} / SHA256 {batch.sha256}',{
        'state':'mapped','batch_id':batch.pk,'captured_at':batch.captured_at,'batch_rows':batch.row_count,
        'visible_rows':len(result),'length_available':batch.length_available}


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
