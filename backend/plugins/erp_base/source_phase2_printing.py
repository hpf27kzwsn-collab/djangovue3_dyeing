"""保留印花旧变体：色版用浆和订单称料，原查询不写库存。"""
from collections import defaultdict
from decimal import Decimal,ROUND_HALF_UP
from django.db.models import F
from .source_quality_reports import rows,key,total
from .source_stock_services import raw
from .source_business_updates import matching
from .source_static_lookup import execute
from .source_phase2_reports import bind


def money(value):
    return None if value is None else Decimal(str(value)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)


def sql_max(values):
    return max((v for v in values if v is not None),default=None)


def same(a,b):
    return a is not None and b is not None and key(str(a))==key(str(b))


def pastedetails(series,order,query=rows):
    heads=list(matching(query('OrderMain','erp_sales'),SheetNo=order).filter(old_sheet_kind=40).order_by('pk'))
    head=heads[-1] if heads else None
    print_code=None if head is None else raw(head,'PrintCode');order_series=None if head is None else raw(head,'SheetSeries')
    machines=list(matching(query('ProcessSchedule','erp_production'),JobSheetNo=order).order_by('pk'))
    machine=None if not machines else raw(machines[-1],'MachineID')
    waste=None
    for option in matching(query('PFieldValid','erp_base'),FieldType='MachinePaste').order_by('pk'):
        if raw(option,'Reserved1') is not None and 'Y01' in raw(option,'Reserved1').upper().split(';'):waste=money(raw(option,'NumValue'))
    counts=execute(bind('SELECT MAX(b.ColorCount) AS value FROM dye.PrintColorSeparateDetail b LEFT JOIN dye.PrintColorSeparate a ON a.SheetSeries=b.SheetSeries WHERE a.PrintCode=@print_code',locals()),query)
    colors=execute(bind('''SELECT ROW_NUMBER() OVER(ORDER BY oc.ColorPlateID) AS PlateIndex,oc.CheckNo,om.ProdID,om.PrintCode,oc.ColorPlateID,oc.FilmNo,oc.OrderQty,om.Unit
      FROM dye.OrderColor oc LEFT JOIN dye.OrderMain om ON oc.SheetSeries=om.SheetSeries WHERE oc.SheetSeries=@order_series''',locals()),query)
    uses=[]
    for color in colors:
        qty=color['orderqty'];unit=color['unit']
        if unit==0:qty=None if qty is None else money(qty*Decimal('1.0936133'));unit=2
        elif unit in [3,5]:qty=None if qty is None else money(qty*(Decimal('.4535924') if unit==3 else 1000));unit=1
        # 原同一NumValue同时<=OrderQty且>OrderQty恒不成立，EatValue保持0。
        use=None if qty is None and unit in [1,2] else Decimal(0)
        matches=execute(bind('''SELECT psd.DetailNo,psd.ColorPlateName,psr.RowNo,psr.ColorName,psr.Rate
          FROM dye.PrintColorSeparate ps LEFT JOIN dye.PrintColorSeparateDetail psd ON psd.SheetSeries=ps.SheetSeries AND psd.ColorPlateID=@plate
          LEFT JOIN dye.PrintColorSeparateRecord psr ON psr.SheetSeries=psd.SheetSeries AND psr.DetailNo=psd.DetailNo WHERE ps.PrintCode=@code''',
          {'plate':color['colorplateid'],'code':color['printcode']}),query)
        for match in matches or [dict(detailno=None,colorplatename=None,rowno=None,colorname=None,rate=None)]:
            match['rowno']=None if match['rowno'] is None else int(match['rowno'] or '0')
            amount=None if use is None or match['rate'] is None else money(use*Decimal(str(match['rate']))/100)
            combined=None if amount is None else (waste or 0)+amount;other=Decimal(0)
            for option in matching(query('PFieldValid','erp_base'),FieldType='DyeingTubeWaste').order_by('pk'):
                lower,upper=raw(option,'NumValue'),raw(option,'SortValue')
                if combined is not None and lower is not None and upper is not None and lower<=combined<upper:other=money(raw(option,'Name'))
            amount_total=None if waste is None or amount is None or other is None else money(waste+amount+other)
            rounded=Decimal(0)
            for option in matching(query('PFieldValid','erp_base'),FieldType='PrintMortarCarry').order_by('pk'):
                lower,upper=raw(option,'NumValue'),raw(option,'SortValue')
                if amount_total is not None and lower is not None and upper is not None and lower<amount_total<=upper:
                    mode=raw(option,'Description')
                    rounded=money(raw(option,'Name')) if mode=='01' else money(int(amount_total+Decimal('.5'))) if mode=='02' else money(int(amount_total)) if mode=='03' else amount_total
            uses.append({**color,**match,'orderqty':qty,'unit':unit,'rowindex':None if match['detailno'] is None else int(match['detailno'][-2:]),
                'eatvalue':0,'totalusevalueround':rounded,'machinewaste':waste,'otherwaste':other})
    recipes=list(matching(query('PrintingTest','erp_sampling'),PrintCode=print_code).order_by(F('old_sheet_date').desc(nulls_last=True),'-pk'))
    recipe=None if not recipes else raw(recipes[0],'SheetSeries')
    palette=execute(bind("""SELECT pc.*,pd.ColorPlateID,pd.ColorPlateName,REPLACE(pc.Note,'同浆','') AS fromColor,
      pd.SampleSign+CONVERT(VARCHAR(10),pc.SerialNumber) AS thisColor FROM dye.PrintingTestColor pc
      LEFT JOIN dye.PrintingTestDetail pd ON pc.WPSerialNumber=pd.WPSerialNumber AND pc.SheetSeries=pd.SheetSeries WHERE pc.SheetSeries=@recipe""",locals()),query)
    linked=[]
    for use in uses:
        matches=[p for p in palette if same(p['colorplateid'],use['colorplateid']) and same(p['colorname'],use['colorname']) and same(p['serialnumber'],use['rowno'])]
        linked.extend({**use,'same':p['issamepulp'],'from':p['fromcolor'],'this':p['thiscolor']} for p in matches)
        if not matches:linked.append({**use,'same':None,'from':None,'this':None})
    cycles=0
    while any(r['same']==1 for r in linked) and cycles<10000:
        cycles+=1
        referenced={key(r['from']) for r in linked if r['from'] is not None and key(r['from'])!=''}
        leaves=[r for r in linked if r['same']==1 and r['this'] is not None and key(r['this']) not in referenced]
        grouped=defaultdict(list)
        for leaf in leaves:grouped[key(leaf['from'])].append(leaf['totalusevalueround'])
        for row in linked:
            if row['this'] is not None and key(row['this']) in grouped:
                addition=total(grouped[key(row['this'])]);value=row['totalusevalueround']
                row['totalusevalueround']=None if value is None or addition is None else money(value+addition)
        for leaf in leaves:leaf.update(totalusevalueround=Decimal(0),same=0,**{'from':''})
    for use in uses:
        for row in linked:
            if same(use['plateindex'],row['plateindex']) and same(use['colorplateid'],row['colorplateid']) and same(use['rowno'],row['rowno']):use['totalusevalueround']=row['totalusevalueround']
    groups=defaultdict(list)
    for use in uses:groups[(key(use['colorplateid']),use['orderqty'],use['unit'],use['rowindex'])].append(use)
    output=[]
    for (_,qty,unit,index),group in groups.items():
        for offset,kind in [(1,'色名'),(0,'用量')]:
            row={'SheetSeries':series,'DetailNo':None if series is None or index is None else series+'-'+('000'+str(index*2-offset))[-2:],
                 'ColorPlateID':group[0]['colorplateid'],'OrderDosage':qty,'OrderUnit':unit,'Kind':kind,'MachineID':machine,'ColorCount':counts[0]['value']}
            for number in range(1,17):
                row['FilmRate'+str(number)]=sql_max([r['rate'] if r['rowno']==number else 0 for r in group])
                values=[r['colorname'] if r['rowno']==number else '' for r in group] if kind=='色名' else [r['totalusevalueround'] if r['rowno']==number else Decimal(0) for r in group]
                row['Value'+str(number)]=sql_max(values)
            output.append(row)
    output.sort(key=lambda r:(r['DetailNo'] is not None,r['DetailNo'] or ''))
    return {'report':'sp_PrintOrderToPasteDosageDetail','rows':output,'supplemental_rows':uses,
            'summary':{'same_pulp_iterations':cycles,'remaining_same_pulp':sum(r['same']==1 for r in linked)},
            'notes':['保留原PrintStarchWaste互斥条件、16色槽和两位流水截断；原行保留在来源表。']}


def print_weight(order,query=rows):
    heads=list(matching(query('OrderMain','erp_sales'),SheetNo=order).order_by('pk'))
    code=None if not heads else raw(heads[-1],'PrintCode')
    plans=list(matching(query('PPasteDosage','erp_base'),OrderNo=order).filter(old_right_status=10).order_by(F('old_sheet_date').desc(nulls_last=True),'-pk'))
    series=None if not plans else raw(plans[0],'SheetSeries')
    lines=list(matching(query('PPasteDosageDetail','erp_base'),SheetSeries=series).order_by('pk'))
    colors=[]
    for line in lines:
        if raw(line,'Kind')!='色名':continue
        for n in range(1,17):
            name=raw(line,'Value'+str(n))
            if name is None or name in ['','0.00']:continue
            quantity=Decimal(0)
            for dosage in lines:
                if raw(dosage,'Kind')=='用量' and same(raw(dosage,'ColorPlateID'),raw(line,'ColorPlateID')):
                    value=raw(dosage,'Value'+str(n))
                    if value is not None and value!='0.00':quantity=money(value)
            if quantity!=0:colors.append({'ColorPlateID':raw(line,'ColorPlateID'),'ColorName':name,'ColorDosage':quantity})
    ingredients=execute(bind("""SELECT ps.*,pd.ColorPlateID,pd.ColorPlateName,pc.IsSamePulp,pd.SampleSign,
      REPLACE(pc.Note,'同浆','') AS fromColor,pd.SampleSign+CONVERT(VARCHAR(10),pc.SerialNumber) AS thisColor,
      pd.SampleSign+CONVERT(VARCHAR(10),pc.SerialNumber) AS ColorCode,CAST(0 AS decimal(10,2)) AS PasteDosage
      FROM dye.PrintingTestStuff ps LEFT JOIN dye.PrintingTestColor pc ON ps.SheetSeries=pc.SheetSeries AND ps.WPSerialNumber=pc.WPSerialNumber AND ps.SerialNumber=pc.SerialNumber
      LEFT JOIN dye.PrintingTestDetail pd ON pc.SheetSeries=pd.SheetSeries AND pc.WPSerialNumber=pd.WPSerialNumber
      LEFT JOIN dye.PrintingTest p ON pd.SheetSeries=p.SheetSeries WHERE p.PrintCode=@code AND ISNULL(ps.DyeStuffCode,'')<>''""",locals()),query)
    for _ in range(10000 if any(r['issamepulp']==1 for r in ingredients) else 0):
        referenced={key(r['fromcolor']) for r in ingredients if r['issamepulp']==1 and r['fromcolor'] is not None and key(r['fromcolor'])!=''}
        leaves=[dict(r) for r in ingredients if r['issamepulp']==1 and r['thiscolor'] is not None and key(r['thiscolor']) not in referenced]
        for row in ingredients:
            for leaf in leaves:
                if same(row['thiscolor'],leaf['fromcolor']):row['colorcode']=None if row['colorcode'] is None or leaf['colorcode'] is None else row['colorcode']+','+leaf['colorcode']
        for row in ingredients:
            if any(same(row['thiscolor'],leaf['thiscolor']) for leaf in leaves):row.update(colorcode='',issamepulp=0,fromcolor='')
    output=[r for r in ingredients if r['note'] is None or not str(r['note']).startswith('同浆')]
    for row in output:
        for color in colors:
            if same(row['printcode'],code) and same(row['colorname'],color['ColorName']):
                row['pastedosage']=color['ColorDosage'];row['dosage']=float(row['ratio'] or 0)*float(color['ColorDosage'] or 0)*10
    pairs=sorted({(r['wpserialnumber'],r['serialnumber']) for r in output},key=lambda p:tuple((v is not None,v or 0) for v in p))
    for row in output:row['PhaseNo']=pairs.index((row['wpserialnumber'],row['serialnumber']))+1
    return {'report':'sp_GetPrintWeightByOrderNo','rows':output,'supplemental_rows':colors}
