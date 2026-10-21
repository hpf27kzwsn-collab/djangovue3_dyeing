"""销售限制的共享原表查询；不办理收款或核销。"""
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from .source_quality_reports import rows
from .source_static_lookup import execute
from .source_phase2_reports import bind, shift_month


SQL = '''SELECT c.CustomerID,p.ShortName,SUM(b.Balance) AS Balance FROM
 (SELECT a.ARDetailNo,SUM(a.Money) AS Balance FROM
   (SELECT ARDetailNo,-WriteOffMoney AS Money FROM dye.FMoneyInDetail
    UNION ALL SELECT SheetSeries,ARMoney FROM dye.FARMain) a GROUP BY a.ARDetailNo) b
 LEFT JOIN dye.FARMain c ON b.ARDetailNo=c.SheetSeries
 LEFT JOIN dye.p_Customer p ON p.CustomerID=c.CustomerID
 WHERE c.SheetDate<=CASE WHEN p.SettleID='02' THEN CAST(@two AS DATETIME) ELSE CAST(@one AS DATETIME) END
 GROUP BY c.CustomerID,p.ShortName'''


def balances(at, query=rows, customer=None):
    if at is not None and timezone.is_aware(at):at=timezone.localtime(at)
    start=None if at is None else at.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
    sql=SQL if customer is None else SQL.replace('GROUP BY c.CustomerID,p.ShortName',
        'AND c.CustomerID=@customer GROUP BY c.CustomerID,p.ShortName')
    return execute(bind(sql,{'one':None if start is None else shift_month(start,-1),'two':None if start is None else shift_month(start,-2),'customer':customer}),query)


def limit(customer,at,query=rows):
    values=balances(at,query,customer)
    value=values[-1]['balance'] if values else None
    return None if value is None else Decimal(value).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)


def report(query=rows,now=None):
    now=timezone.localtime() if now is None else now
    from .source_quality_reports import key
    output={}
    for at,column in [(now,'CurrentNotWriteOffMoney'),(shift_month(now,1),'NextMonthNotWriteOffMoney')]:
        for row in balances(at,query):
            group=(key(row['customerid']),key(row['shortname']))
            output.setdefault(group,{'CustomerID':row['customerid'],'ShortName':row['shortname'],
                'CurrentNotWriteOffMoney':None,'NextMonthNotWriteOffMoney':None})[column]=row['balance']
    return {'report':'RKLimit','rows':list(output.values())}
