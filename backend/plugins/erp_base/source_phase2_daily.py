"""Sp_QueryDyeingOrder各原分支汇总和未络筒累计；不把计划代替实产。"""
from collections import defaultdict
from datetime import timedelta
from decimal import Decimal
from uuid import uuid4
from .source_phase2_reports import QUERIES,bind,date
from .source_static_lookup import execute
from .source_quality_reports import total

FIELDS=['orderqty','outorderqty','twistingqty','barrelqty','yarnweightqty','repairqty','netkg','orderweightqty','outorderweightqty','schedulingqty']


def report(parameters,query):
    p={k.lower():v for k,v in parameters.items()}
    start,end=date(p['startdate']),date(p['enddate'])
    sources={name:execute(bind(sql,p),query) for name,sql in QUERIES['Sp_QueryDyeingOrder']['temps'].items()}
    days=defaultdict(lambda:defaultdict(list))
    for i,field in enumerate(FIELDS,1):
        for row in sources['t'+str(i)]:
            for column in FIELDS:days[str(row['sheetdate'])[:10]][column].append(row[field] if column==field else Decimal(0))
    schedule={str(r['sheetdate'])[:10]:r['schedulingqty'] for r in sources['t10']}
    yield_qty={str(r['sheetdate'])[:10]:r['netkg'] for r in sources['t12']}
    current=start;previous=0;scheduling=net=None;loop=[]
    while current<end:
        key=current.strftime('%Y-%m-%d')
        # 原日期变量有时分秒时不等于日汇总日期；SELECT无行则沿用上一轮变量。
        if current.hour==current.minute==current.second==current.microsecond==0 and (key in schedule or key in yield_qty):
            scheduling=total([schedule[key] if key in schedule else None,Decimal(0) if key in yield_qty else None])
            net=total([yield_qty[key] if key in yield_qty else None,Decimal(0) if key in schedule else None])
        value=None if scheduling is None or net is None or current!=start and previous is None else scheduling-net+(0 if current==start else previous)
        loop.append({'SheetDate':current,'SchedulingQty':scheduling,'NetKg':net,'UnWindingQty':value})
        previous=None if value is None else int(value)
        for column in FIELDS:days[key][column].append(Decimal(0))
        current+=timedelta(days=1)
    output=[];running=None
    for day,columns in sorted(days.items()):
        record={column:total(values) for column,values in columns.items()}
        amount=None if record['schedulingqty'] is None or record['netkg'] is None else record['schedulingqty']-record['netkg']
        running=total([running,amount])
        output.append({'id':str(uuid4()),'sheetdate':day,**record,'unwindingqty':running})
    return {'report':'Sp_QueryDyeingOrder','rows':output,'supplemental_rows':loop,
        'notes':['最终UnWindingQty按原SUM(排单数量－络筒产量)窗口累计；原临时游标结果单独保留，不替换最终口径。']}
