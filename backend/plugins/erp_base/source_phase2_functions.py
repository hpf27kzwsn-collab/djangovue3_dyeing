"""销售打样补充函数：原价格方向、空值、重复连接和取值顺序。"""
from decimal import Decimal, ROUND_HALF_UP
from .source_quality_reports import rows
from .source_stock_services import raw
from .source_business_updates import matching
from .source_foundation_functions import number_matches
from .source_static_lookup import execute
from .source_phase2_reports import bind


def label_remarks(kind,check,query=rows):
    from .source_static_lookup import label_remarks as original_label_remarks
    return original_label_remarks(kind,check,query)


def produce_color(color,color_input):
    from .source_package_labels import varchar
    from .source_trial_steps import equal
    color,color_input=varchar(color,50),varchar(color_input,50)
    return {'Code':0,'Msg':'产生成功！','ColorNum':color if equal(color_input or '','') else color_input}


def dosage(color,kind,query=rows):
    if kind not in [0,1]:return None
    values=[]
    for master in number_matches(query('PColorNum','erp_base'),color,20):
        samples=query('DyeDipsRecord','erp_sampling')
        samples=number_matches(samples,raw(master,'ColorNum'),20) if kind==0 else matching(samples,ColorNum=raw(master,'ColorNum'))
        values.extend(v for v in samples.values_list('old_cost' if kind==0 else 'old_stuff_dosage',flat=True) if v is not None)
    return float(max(values)) if values else None


def flow_info(flow,series,step,query=rows):
    from .source_package_labels import varchar
    series=varchar(series,30)
    result=None
    for head in matching(query('OrderMain','erp_sales'),SheetSeries=series).order_by('pk'):
        customer,salesperson=raw(head,'CustomerID'),raw(head,'SalerID')
        result=None if customer is None or salesperson is None else "{'客户':'"+customer+"','业务员':'"+salesperson+"'}"
    return result


def previous_material_price(series,at,supplier,material,kind,query=rows):
    if kind not in [0,1]:return None
    table,field=('StuffIn','StuffID') if kind==0 else ('ArticleIn','ArticleID')
    sql=f'''SELECT TOP 1 CAST(a.Price AS decimal(12,4)) AS Price FROM dye.{table}Detail a
      JOIN dye.{table} b ON a.SheetSeries=b.SheetSeries
      WHERE b.SheetKind=13 AND b.RightStatus=10 AND b.SupplierID=@supplier AND b.SheetDate<@at
      AND b.SheetSeries<>@series AND a.{field}=@material
      AND NOT EXISTS(SELECT 1 FROM dye.MaterialPriceAdjust c WHERE c.InSheetNo=b.SheetNo AND ISNULL(c.RightStatus,0)<>10)
      ORDER BY b.SheetDate DESC'''
    selected=execute(bind(sql,locals()),query)
    return float(selected[0]['price'] or 0) if selected else 0.0


def confirmed_price(check,job,customer,product,category,kind,query=rows):
    if kind not in [0,1,2]:return 0.0
    field=['CusPrice','FenTouPrice','MinAmount'][kind]
    selected=execute(bind(f'''SELECT TOP 1 a.{field} AS Price FROM dye.FixedPriceDetail a
      LEFT JOIN dye.FixedPrice b ON a.SheetSeries=b.SheetSeries
      WHERE b.CustomerID=@customer AND a.ProdID=@product AND a.YarnCategory=@category ORDER BY b.SheetDate DESC''',locals()),query)
    value=float(selected[0]['price'] or 0) if selected else 0.0
    if kind==0:
        fees=execute(bind("""SELECT SUM(b.NumValue2) AS Price FROM dye.OrderAtte a LEFT JOIN dye.p_FieldValidSub b
          ON b.FieldType='AtteKind' AND a.AtteCode=b.Code WHERE a.CheckNo=@check AND ISNULL(b.NumValue3,0)=1""",locals()),query)
        value+=float(fees[0]['price'] or 0)
    return value


def color_price(customer,color,grade,variant,level=None,query=rows):
    pairs=[]
    for master in number_matches(query('PColorNum','erp_base'),color,20):
        pairs.extend(matching(query('DyeDipsRecord','erp_sampling'),ColorNum=raw(master,'ColorNum')))
    if variant=='Sp_QueryColorNum_BasicsPrice':
        costs=[raw(s,'Cost') for s in pairs if raw(s,'Cost') is not None]
        doses=[raw(s,'StuffDosage') for s in pairs if raw(s,'StuffDosage') is not None]
        cost=max(costs) if costs else None;dose=max(doses) if doses else None
    else:
        pairs.sort(key=lambda r:(raw(r,'ApproveDate') is not None,raw(r,'ApproveDate'),r.pk))
        cost=raw(pairs[0],'Cost') if pairs else None;dose=None
        if cost in [None,0]:return {'report':variant,'rows':[]}  # 原SELECT返回位于IF内部。
    cost=None if cost is None else Decimal(str(cost)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
    def choose(grade,use_dosage):
        extra='a.StuffRatio1<@dose AND a.StuffRatio2>=@dose AND a.FormulaCost2>=@cost' if use_dosage else 'a.FormulaCost1<=@cost AND a.FormulaCost2>=@cost'
        found=execute(bind('SELECT a.Price FROM dye.CusBasicsPriceDetail a LEFT JOIN dye.CusBasicsPrice b ON a.SheetSeries=b.SheetSeries WHERE b.CustomerID=@customer AND a.GradeID=@grade AND '+extra+' ORDER BY b.SheetDate DESC',{'customer':customer,'grade':grade,'dose':dose,'cost':cost}),query)
        # SELECT @Price=Price ORDER BY DESC最终采用最后一行（并非TOP 1）。
        return None if not found or found[-1]['price'] is None else Decimal(str(found[-1]['price'])).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
    value=choose(grade,variant=='Sp_QueryColorNum_BasicsPrice')
    if value in [None,0]:
        if variant=='Sp_QueryColorNum_BasicsPrice':value=choose(grade,False)
        elif grade=='一等品':value=choose('合格品',False)
    result=None if value is None else value/1000 if variant=='Sp_QueryColorNum_BasicsPrice' else value
    return {'report':variant,'rows':[{'CmdOK':1 if value in [None,0] else 0,'Price':result}]}
