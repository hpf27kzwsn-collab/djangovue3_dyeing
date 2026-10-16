"""原APP手感报价、产量及费用查询；断开的旧调用按已说明的业务来源接续。"""
from collections import defaultdict
from calendar import monthrange
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
from math import ceil
from uuid import uuid4
from django.utils import timezone
from .source_quality_reports import rows, key, total
from .source_business_updates import matching
from .source_stock_services import raw
from .source_trial_steps import sql_like
from .source_package_labels import varchar
from .source_static_lookup import execute
from .source_foundation_view_reports import statement
from .source_station_yield import code_index


def shift_month(value,offset):
    year,month=divmod(value.year*12+value.month-1+offset,12)
    return value.replace(year=year,month=month+1,day=min(value.day,monthrange(year,month+1)[1]))


def sql_sum(values,precision=16):
    value=total(values)
    if value is None:return None
    result=Decimal(str(value)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
    if abs(result)>=Decimal(10)**(precision-2):raise OverflowError(f'原decimal({precision},2)汇总溢出。')
    return result


def feel_offers(filter_text='',current=1,size=10,employee='',start=None,end=None,query=rows,now=None):
    """Sp_AppQueryFeelOfferMain：主表分页，原第三结果集仍返回全明细。"""
    now=timezone.localtime() if now is None else now
    end=now+timedelta(days=1) if end is None else end
    start=shift_month(end,-12) if start is None else start
    current=1 if current is None or current<1 else current
    size=10 if size is None or size<1 else size
    text=varchar(filter_text,36)
    text=text.rstrip(' ') if text is not None else text
    customers=code_index(query('PCustomer','erp_base'),['CustomerID'])
    products=code_index(query('PProduct','erp_base'),['ProdID'])
    lines=list(query('FeelOfferDetail','erp_base').order_by('pk'))
    line_index=code_index(lines,['SheetSeries']);heads=[]
    for head in query('FeelOfferMain','erp_base').filter(old_sheet_date__gte=start,old_sheet_date__lt=end).order_by('-old_sheet_date','pk'):
        details=line_index[(key(raw(head,'SheetSeries')),)]
        product_match=any(sql_like(raw(p,'NameC'),'%'+text+'%') for d in details for p in products[(key(raw(d,'ProdID')),)] ) if text else False
        feel_match=any(sql_like(raw(d,'FeelCode'),'%'+text+'%') for d in details) if text else False
        for customer in customers[(key(raw(head,'CustomerID')),)] or [None]:
            short=None if customer is None else raw(customer,'ShortName')
            if text and not (product_match or feel_match or sql_like(short,'%'+text+'%')):continue
            heads.append({'RowIndex':len(heads)+1,'SheetSeries':raw(head,'SheetSeries'),'CustomerID':raw(head,'CustomerID'),
                'ShortName':short,'SheetDate':timezone.localtime(raw(head,'SheetDate')).strftime('%Y-%m-%d'),
                'Creater':raw(head,'Creater'),'CreateDate':None if raw(head,'CreateDate') is None else timezone.localtime(raw(head,'CreateDate')).strftime('%Y-%m-%d %H:%M:%S')})
    details=[]
    for line in lines:
        for product in products[(key(raw(line,'ProdID')),)] or [None]:
            details.append({**{f:raw(line,f) for f in ['SheetSeries','ProdID','FeelCode','CusPrice','Price','Remarks']},
                            'FabricName':None if product is None else raw(product,'NameC')})
    return {'report':'Sp_AppQueryFeelOfferMain','rows':heads[(current-1)*size:current*size],
        'pagination':{'current':current,'size':size,'pages':ceil(len(heads)/size),'total':len(heads)},
        'detail_rows':details,'notes':['原@empID未参与过滤；原明细结果集未按分页表头筛选，保持返回全部授权明细。']}


def output_sum(filter_text='',date_mode=1,start=None,end=None,query=rows,now=None):
    """SP_APP_QueryOutputSum的当前调用已失配；以当前工序及包装来源补回岗位/工序汇总。"""
    now=timezone.localtime() if now is None else now
    end=now.replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=1) if end is None else end
    start=end-timedelta(days=1) if date_mode==1 else shift_month(end,-1) if date_mode==2 else end-timedelta(days=1) if start is None else start
    text=varchar(filter_text,36)
    text=text.rstrip(' ') if text is not None else text
    jobs=code_index(query('JobSheet','erp_production'),['SheetNo'])
    stations=code_index(matching(query('PFieldValid','erp_base'),FieldType='Station'),['Code'])
    processes=code_index(query('PProcess','erp_base'),['ProcessID'])
    source_rows=[]
    for name,module,date_field in [('WProcess','erp_production','old_create_date'),('RecordYield','erp_warehouse','old_pack_time')]:
        for item in query(name,module).filter(**{date_field+'__gte':start,date_field+'__lt':end}).order_by('pk'):
            packaging=name=='RecordYield';job=raw(item,'JobSheetNo')
            process='GX98' if packaging else raw(item,'ProcessID');station='07' if packaging else raw(item,'StationID')
            dosage=100 if packaging or key(process) in ['GX00','GX01'] and key(raw(item,'Creater'))=='翻布刷卡' else raw(item,'CurrDosage') or 0
            kilograms=raw(item,'Kg' if packaging else 'CurrKg');metres=raw(item,'Meter' if packaging else 'CurrMeter')
            roll_count=raw(item,'Rolls' if packaging else 'CurrRolls')
            parents=jobs[(key(job),)] or [None]
            # 当前Sp_WorkQtySum阶段内和阶段后各连接一次工卡，原重号倍增照留。
            for first in parents:
                for second in parents:
                    unit=None if second is None else raw(second,'AssignUnit')
                    kg=None if unit==1 and kilograms is None else kilograms*dosage/100 if unit==1 else 0
                    meter=None if unit==0 and metres is None else metres*dosage/100 if unit==0 else 0
                    for post in stations[(key(station),)] or [None]:
                        for process_row in processes[(key(process),)] or [None]:
                            post_name=None if post is None else raw(post,'Name');process_name=None if process_row is None else raw(process_row,'Name')
                            if text and not (sql_like(post_name,'%'+text+'%') or sql_like(process_name,'%'+text+'%')):continue
                            source_rows.append({'entity':item._meta.label,'record_id':item.pk,'legacy_id':item.legacy_id,'JobSheetNo':job,
                                'ProcessID':process,'StationID':station,'PostName':post_name,'ProcessName':process_name,
                                'CurrKg':kg,'CurrMeter':meter,'CurrRolls':roll_count,'raw_kg':kilograms,'raw_meter':metres,
                                'AssignUnit':unit,'CurrDosage':dosage,'first_job_id':None if first is None else first.pk,
                                'second_job_id':None if second is None else second.pk})
    posts=defaultdict(list);groups=defaultdict(list)
    for row in source_rows:
        posts[key(row['PostName'])].append(row);groups[(key(row['PostName']),key(row['ProcessName']))].append(row)
    summaries=[{'PostName':group[0]['PostName'],'SumOutput':sql_sum([r['CurrKg'] for r in group])} for group in posts.values()]
    details=[{'PostName':group[0]['PostName'],'ProcessName':group[0]['ProcessName'],'fRolls':total([r['CurrRolls'] for r in group]),
              'fWeight':sql_sum([r['CurrKg'] for r in group]),'fMeter':sql_sum([r['CurrMeter'] for r in group])} for group in groups.values()]
    return {'report':'SP_APP_QueryOutputSum','rows':summaries,'detail_rows':details,'source_rows':source_rows,
        'notes':['旧APP仍传StartDate/EndDate并接收五列，而当前Sp_WorkQtySum要求NewSTime/NewETime/StationID/ShiftID且返回十列，不能直接执行。',
                 '新实现按当前CreateDate/PackTime、CurrDosage和AssignUnit计算公斤与米，工序保留以便按工序汇总；卷数采用原CurrRolls/Rolls，原无值保持NULL。不把包装行数当卷数。']}


def cook_query(start,end,query=rows):
    """Sp_CookQuery：采购/入库费用来源的四层汇总，不进行财务记账。"""
    data=[] if start is None or end is None else execute(statement('v_CookQuery',[
        {'field':'SheetDate','operator':'gte','value':start.strftime('%Y-%m-%d')},
        {'field':'SheetDate','operator':'lte','value':end.strftime('%Y-%m-%d')}]),query)
    output=[]
    for level,fields in enumerate([['idno','buyerid','kind','articlekindid','name'],['idno','buyerid','kind'],['buyerid']]):
        groups=defaultdict(list)
        for row in data:groups[tuple(key(row[f]) if isinstance(row[f],str) else row[f] for f in fields)].append(row)
        for group in groups.values():
            row=group[0];amount=sql_sum([r['total'] for r in group],10)
            output.append({'ID':str(uuid4()),'IDNO':int(row['idno']) if level<2 else 100,'Kind':row['kind'] if level<2 else '合计',
                'uindex':level,'BuyerID':row['buyerid'],'ArticleKindID':row['articlekindid'] if level==0 else '汇总' if level==1 else '合计',
                'Name':row['name'] if level==0 else None if level==1 and row['kind'] is None else row['kind']+'汇总' if level==1 else '合计',
                'SumARMoney':amount if level==0 else None,'Total':None if level==0 else amount})
    output.append({'ID':str(uuid4()),'IDNO':100,'Kind':'本期总合计','uindex':3,'BuyerID':'本期总合计','ArticleKindID':'本期总合计',
                   'Name':'本期总合计','SumARMoney':None,'Total':total([r['total'] for r in data])})
    output.sort(key=lambda r:(r['BuyerID'] is not None,key(r['BuyerID']) or '',r['IDNO'],key(r['Kind']) or '',r['uindex']))
    return {'report':'Sp_CookQuery','rows':output}
