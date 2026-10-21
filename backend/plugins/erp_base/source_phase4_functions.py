"""第四阶段原工卡函数；候选重复、负数和原NULL传播均保留。"""
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from .source_quality_reports import rows
from .source_business_updates import matching
from .source_stock_services import raw
from .source_package_labels import varchar
from .source_foundation_functions import first_number, extract, extract_number
from .source_trial_steps import equal, sql_like
from .source_static_lookup import execute
from .source_phase3_sql import bind

NAMES=['fn_ArticlePriceWeightedAverage','fn_StuffPriceWeightedAverage','fn_ConcatJobAtte',
    'fn_ConcatWeightKg','fn_Get_JiaoDai','Fn_Get_Machine','fn_GetJObSheetNoAttePrice',
    'fn_GetJObSheetNoAttePriceUnit','fn_GetPaperTubeByJobNo','fn_GetPhaseNo','fn_GetProcessWorkMoney',
    'fn_GetTubeWeightByJobNo','fn_JobAssign','fn_JobAttelect','fn_ProcessIDPire','fn_ProcessIDPrice','GetPropOfJobShiftEmp','F_JobProcessTable']


def weighted_price(family,code,warehouse,query=rows):
    # 原函数没有截止时间参数；结存取最大CarryDate全部并列行，流水只取其后指定入库种类。
    sql=f"""SELECT SUM(ISNULL(TotalMoney,0)) AS money,SUM(ISNULL(TotalQty,0)) AS qty FROM (
      SELECT InQty AS TotalQty,InMoney AS TotalMoney FROM dye.{family}StockBook
      WHERE WareHouseID=@warehouse AND {family}ID=@code AND BookKind IN (11,13,14,16,19)
      AND BookDate>(SELECT MAX(d) FROM (SELECT CAST('1900-01-01' AS DATETIME) AS d UNION ALL
        SELECT MAX(ISNULL(CarryDate,CAST('1900-01-01' AS DATETIME))) FROM dye.{family}Stock
        WHERE WareHouseID=@warehouse AND {family}ID=@code) dates)
      UNION ALL
      SELECT a.PreMonthQty,a.PreMonthMoney FROM dye.{family}Stock a
      JOIN (SELECT MAX(CarryDate) AS CarryDate,WareHouseID,{family}ID FROM dye.{family}Stock
        GROUP BY WareHouseID,{family}ID) b ON a.CarryDate=b.CarryDate
        AND a.WareHouseID=b.WareHouseID AND a.{family}ID=b.{family}ID
      WHERE a.WareHouseID=@warehouse AND a.{family}ID=@code) amounts"""
    result=execute(bind(sql,{'warehouse':varchar(warehouse,10),'code':varchar(code,16)}),query)[0]
    money=Decimal(str(result['money'] or 0)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
    qty=Decimal(str(result['qty'] or 0)).quantize(Decimal('.000001' if family=='Stuff' else '.01'),rounding=ROUND_HALF_UP)
    value=(Decimal(0) if qty==0 else money/qty).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
    return {'result':value,'money':money,'qty':qty}


def calculate(name,p,query=rows):
    if name=='F_JobProcessTable':
        output=[]
        for job in query('JobSheet','erp_production').order_by('pk'):
            value=''
            for step in matching(query('JobProcess','erp_production'),SheetSeries=raw(job,'SheetSeries')).order_by('pk'):
                process=raw(step,'ProcessID');value=None if process is None or value is None else varchar(value+process+'-',500)
            parts=[] if value is None else [varchar(v,10) for v in value.split('-')[:-1] if v.rstrip(' ')]
            output.append({'SheetSeries':raw(job,'SheetSeries'),**{'ProcessID'+str(i):parts[i] if i<len(parts) else '' for i in range(27)}})
        return {'report':name,'rows':output,'notes':['原函数不使用JobSheetSeries入参，遍历全部工卡；27列、500字节原中间串限制不改变，完整工序原行仍保留。']}
    if name in ['fn_ArticlePriceWeightedAverage','fn_StuffPriceWeightedAverage']:
        family='Article' if name.startswith('fn_Article') else 'Stuff'
        return {'report':name,'rows':[weighted_price(family,p[family.lower()+'code'],p['warehouseid'],query)]}
    if name=='Fn_Get_Machine':
        from .source_machine_choice import entered_machine
        return entered_machine(p['jobsheetno'],query)
    if name=='GetPropOfJobShiftEmp':
        from .source_shift_work import proportion
        return proportion(p['empid'],p['wprocessno'],query)
    if name in ['fn_GetJObSheetNoAttePrice','fn_GetJObSheetNoAttePriceUnit']:
        from .source_quote_functions import calculate as quote
        return quote(name,{'job_number':p['jobsheetno'],'customer':p['customerid'],'service':p['attevalue']},query)
    def select(table,app='erp_production',**filters):
        return list(matching(query(table,app),**filters).order_by('pk'))
    def sql(text,params=p):return execute(bind(text,params),query)
    job=varchar(p.get('jobsheetno'),30)
    jobs=select('JobSheet',SheetNo=job)
    series=varchar(raw(jobs[-1],'SheetSeries'),50) if jobs else None
    evidence=[];value=None
    if name=='fn_GetPhaseNo':
        selected=select('StuffWeightPhase',SheetSeries=varchar(p['sheetseries'],100),ProgramID=varchar(p['programid'],50))
        evidence=[{'PhaseNo':raw(r,'PhaseNo'),'record_id':r.pk} for r in selected]
        value=None if not selected else varchar(str(raw(selected[0],'PhaseNo')),10) if raw(selected[0],'PhaseNo') is not None else None
    elif name in ['fn_JobAssign','fn_JobAttelect']:
        table,field=('JobAssign','MachineID') if name=='fn_JobAssign' else ('JobAtte','AtteValue')
        for r in select(table,SheetSeries=varchar(p['jobseries'],30)):
            part=raw(r,field);evidence.append({'record_id':r.pk,field:part})
            value=None if part is None else varchar((value or '')+';'+part,8000)
        value=value[1:] if value else None
    elif name=='fn_ConcatJobAtte':
        kind=p['ischarge'];value=''
        for r in select('JobAtte',SheetSeries=series):
            atte=raw(r,'AtteValue');description=raw(r,'Description');field=raw(r,'FieldType')
            include={0:equal(field,'00'),1:raw(r,'PriceUnit')==2,2:sql_like(atte,'%封度%'),3:sql_like(atte,'%克重%'),
                4:equal(field,'05') and atte is not None and not sql_like(atte,'%胶袋%'),5:sql_like(atte,'%纸筒%'),
                6:sql_like(atte,'%胶袋%'),7:sql_like(atte,'%加重%'),8:equal(field,'01'),9:equal(field,'02'),10:equal(field,'00')}.get(kind,False)
            if not include:continue
            evidence.append({'record_id':r.pk,'AtteValue':atte,'Description':description})
            if kind==0:part=None if atte is None else atte+' '+(description or '')
            elif kind==1:part=atte
            elif kind==4:part=atte if description is None or equal(description,'') else description
            elif kind in [5,6,7]:part=None if description is None else description.replace({5:'kg纸筒',6:'胶袋',7:'成品加重'}[kind],'')
            elif kind==10:part=atte if any(sql_like(atte,'%'+s+'%') for s in ['胶袋','纸筒','纸管']) else description
            else:part=description
            separator='-' if kind==1 else ',' if kind in [2,3,5,6,7,10] else '+'
            value=None if part is None else varchar(('' if kind in [5,6,7] else value or '')+separator+part,8000)
        value=value[1:] if value else ''
    elif name in ['fn_ConcatWeightKg','fn_Get_JiaoDai','fn_GetPaperTubeByJobNo','fn_GetTubeWeightByJobNo']:
        selected=select('JobAtte',SheetSeries=series);value=0
        if name in ['fn_ConcatWeightKg','fn_Get_JiaoDai']:
            text=None
            for r in selected:
                atte=raw(r,'AtteValue')
                if not (equal(atte,'成品加重') if name=='fn_ConcatWeightKg' else sql_like(atte,'%胶袋%')):continue
                for valid in select('PFieldValidSub','erp_base',Name=atte,FieldType='AtteKind'):
                    if name=='fn_Get_JiaoDai' and not equal(raw(valid,'Code'),'00'):continue
                    text=raw(r,'Description') if name=='fn_ConcatWeightKg' else raw(valid,'Description')
                    evidence.append({'record_id':r.pk,'dictionary_id':valid.pk,'Description':text})
            if name=='fn_ConcatWeightKg':
                # ISNUMERIC单字符包含正负号、小数点、货币符号；不能替换为纯数字提取。
                value= varchar(''.join(c for c in (text or '').rstrip(' ') if c in '0123456789+-.,$£¥\\'),20) or '0'
            else:
                number=extract(text,'Fn_Get_NumNo');value=0.0 if number is None or number=='' else float(number)
        else:
            for r in selected:
                atte=raw(r,'AtteValue');text=raw(r,'Description') or ''
                if not (sql_like(atte,'%纸筒%') or name=='fn_GetTubeWeightByJobNo' and sql_like(atte,'%成品加重%')):continue
                evidence.append({'record_id':r.pk,'Description':text})
                if name=='fn_GetPaperTubeByJobNo':value+=first_number(text)
                else:
                    # 原式误把PATINDEX位置当重量。暂按Unicode范围定位；排序规则差异列入异常文档。
                    value+=next((i for i,c in enumerate(text.upper(),1) if '吖'<=c<='座'),0)
    elif name=='fn_GetProcessWorkMoney':
        from .source_static_lookup import INLINE_FUNCTIONS
        expression=INLINE_FUNCTIONS['fn_getprocessworkmoney']
        parameters=dict(zip(['p'+str(i) for i in range(8)],[job,p['processid'],p['processno'],p['ratio'],p['empid'],p['price'],p['currkg'],p['shiftid']]))
        value=sql('SELECT '+expression+' AS result',parameters)[0]['result']
    elif name=='fn_ProcessIDPire':
        candidates=sql('SELECT g.FabricKindID,j.Weight FROM dye.JobSheet j LEFT JOIN dye.p_Gray g ON g.GrayID=j.ProdID WHERE j.SheetNo=@jobsheetno')
        selected=candidates[-1] if candidates else None
        weight=0 if selected is None else Decimal(extract_number(str(selected['weight'] or 0),20)[:3] or '0').quantize(Decimal('.1'),rounding=ROUND_HALF_UP)
        params={**p,'fabric':None if selected is None else selected['fabrickindid'],'weight':weight,'num':None if p['num'] is None else Decimal(str(p['num'])).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)}
        condition='AND ISNULL(WeightDn,0)<@weight AND ISNULL(WeightUP,999)>=@weight' if p['processid'] in ['GX09','GX10','GX11'] else 'AND ISNULL(QtyDn,0)<@num AND ISNULL(QtyUP,999)>=@num' if p['processid'] in ['GX06','GX07'] else ''
        evidence=sql('SELECT ISNULL(Price,0) AS price FROM dye.p_ProcessPrice WHERE ProcessID=@processid AND ProdKindID=@fabric '+condition,params)
        value=evidence[0]['price'] if evidence else None
    elif name=='fn_ProcessIDPrice':
        if p['kind']==0:
            text="""SELECT a.Price FROM dye.CusBasicsPriceDetail a LEFT JOIN dye.CusBasicsPrice b ON a.SheetSeries=b.SheetSeries
            WHERE a.RSKind=(SELECT TOP 1 g.RSKind FROM dye.JobSheet j LEFT JOIN dye.p_Gray g ON g.GrayID=j.ProdID WHERE j.SheetNo=@jobsheetno)
            AND a.KindName=(SELECT TOP 1 m.KindName FROM (SELECT TOP 1 MachineID FROM dye.WProcess WHERE JobSheetNo=@jobsheetno
            AND ProcessID=@processid AND ISNULL(MachineID,'')<>'') w LEFT JOIN dye.p_Machine m ON m.MachineID=w.MachineID)"""
        elif p['kind']==1:
            text='SELECT a.Price FROM dye.FeelOfferDetail a LEFT JOIN dye.FeelOfferMain b ON a.SheetSeries=b.SheetSeries WHERE a.ProcessID=@processid AND a.ProdID=(SELECT TOP 1 ProdID FROM dye.JobSheet WHERE SheetNo=@jobsheetno)'
        else:return {'report':name,'rows':[{'result':None}]}
        evidence=sql(text);value=0 if not evidence else evidence[0]['price'] or 0
    return {'report':name,'rows':[{'result':value}],'candidate_rows':evidence}
