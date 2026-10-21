"""打样统计按原生产日SDate筛选；起日含、止日不含，未选范围即全期。"""
from datetime import date
from django.core.exceptions import ValidationError
from sqlglot import parse_one, exp

ENTRY='qryDyeDipsRecord'
PARAMETERS=['FromProductionDate','UntilProductionDate']


def adapt(name,tree):
    if name==ENTRY:
        condition=parse_one('''SELECT 1 WHERE
            (@FromProductionDate IS NULL OR a.SDate >= @FromProductionDate)
            AND (@UntilProductionDate IS NULL OR a.SDate < @UntilProductionDate)''',read='tsql').args['where'].this
        tree.set('where',exp.Where(this=exp.and_(tree.args['where'].this,condition)))
    return tree


def parameters(name,values):
    if name!=ENTRY:return values
    values={**{key.lower():None for key in PARAMETERS},**values}
    start,end=[values[key.lower()] for key in PARAMETERS]
    if start is None and end is None:return values
    if not isinstance(start,str) or not isinstance(end,str):
        raise ValidationError({'parameters':'生产日起止日期须同时指定，或同时留空查询全期。'})
    try:
        first,last=date.fromisoformat(start),date.fromisoformat(end)
    except ValueError as error:
        raise ValidationError({'parameters':'生产日使用YYYY-MM-DD日期。'}) from error
    if first>=last:raise ValidationError({'parameters':'生产日止日不包含在范围内，须晚于起日。'})
    return {**values,'fromproductiondate':first.isoformat(),'untilproductiondate':last.isoformat()}


def description(name,values):
    from .source_phase6_inventory_queries import PERIOD_ENTRIES
    if name in PERIOD_ENTRIES:
        selected={k.lower():v for k,v in values.items()}
        return {'label':'库存期间','opening_date':selected['stockdate'],
                'from_inclusive':selected.get('fromdate',selected['stockdate']),
                'until_exclusive':selected['untildate'],'mode':'explicit_stock_period',
                'source':'期初日按开始时点取选定快照；前期与本期台账分开，旧结转时点待核对。',
                'old_client_filter_verified':False}
    if name!=ENTRY:return None
    selected=parameters(name,{k.lower():v for k,v in values.items()})
    return {'label':'生产日','from_inclusive':selected['fromproductiondate'],'until_exclusive':selected['untilproductiondate'],
            'source':'原vw_DyeDipsRecord_EmpID.SDate = SheetDate减450分钟后的日期；不改原记录时间。',
            'mode':'explicit_production_date_filter','old_client_filter_verified':False}
