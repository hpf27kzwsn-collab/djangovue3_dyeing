"""原报价函数：独立保留取价、日期、数量区间、单位和无序候选。"""
from plugins.erp_base.source_provenance import reference as source_reference
from decimal import Decimal, ROUND_HALF_UP
from .source_quality_reports import rows, key
from .source_stock_services import raw
from .source_business_updates import matching
from .source_sales_services import numeric_color
from .source_package_labels import varchar
from .source_foundation_functions import extract_number, same_number

FUNCTIONS = ['fn_GetColorNumPrice', 'fn_GetPriceListVat', 'fn_GetPriceUnit', 'fn_ColorNum_BasicsPrice',
    'fn_GetPackPrice', 'fn_GetPackQtyPrice', 'fn_GetDyePrice', 'fn_GetPriceRemark',
    'fn_GetJObSheetNoAttePrice', 'fn_GetJObSheetNoAttePriceUnit','fn_NewGetDyePrice','fn_GetTechPrice']


def money(value):
    return None if value is None else Decimal(str(value)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)


def calculate(function, params, query=rows):
    if function in ['fn_NewGetDyePrice','fn_GetTechPrice']:
        from .source_quote_components import calculate as components
        return components(function,params,query)
    params = {**params, **{name: money(params.get(name)) for name in ['weight','gray_quantity']}}
    evidence = []
    def select(name, module='erp_sales', **filters):
        return list(matching(query(name, module), **filters).order_by('pk'))
    def candidates(stage, items, field):
        for item in items:
            evidence.append({'stage': stage, 'entity': item._meta.label, 'record_id': item.pk,
                'source': source_reference(item), 'field': field, 'value': raw(item, field)})
    def last(stage, items, field, default=None):
        candidates(stage, items, field)
        return raw(items[-1], field) if items else default
    def joined(head, detail, color_digits=None, customer=None, filter_customer=False, width=10):
        pairs = []
        for line in select(detail):
            color = raw(line, 'ColorNum')
            number = extract_number(color,width)
            if not same_number(number,color_digits):
                continue
            filters = {'SheetSeries': raw(line, 'SheetSeries')}
            if filter_customer: filters['CustomerID'] = customer
            for parent in select(head, **filters):
                pairs.append((parent, line))
        return pairs

    color = varchar(params.get('color'), 20)
    customer = varchar(params.get('customer'), 20)
    if function in ['fn_GetPackPrice', 'fn_GetPackQtyPrice']:
        value = last('工序价格', select('PProcess', 'erp_base', ProcessID=varchar(params.get('process'), 30)), 'Price')
    elif function == 'fn_GetDyePrice':
        items = [item for item in select('PDyeCurve', 'erp_base', PhaseID=varchar(params.get('phase'), 10)) if raw(item, 'DyePhase') == 1]
        value = last('染色曲线MaxValue（原函数实际返回）', items, 'MaxValue')
    elif function == 'fn_GetPriceRemark':
        items = [item for item in select('QuoteDetail') if same_number(numeric_color(raw(item, 'ColorNum')),color)]
        value = ''
        for item in items:
            remark = raw(item, 'Remarks')
            value = None if remark is None else varchar((value or '') + remark, 100)
        candidates('F_Get_No(原色号)等于原传入文本；逐次varchar(100)', items, 'Remarks')
    elif function in ['fn_GetJObSheetNoAttePrice', 'fn_GetJObSheetNoAttePriceUnit']:
        customer = varchar(params.get('customer'), 50)
        service = varchar(params.get('service'), 100)
        items = [line for parent in select('CusBasicsPrice', CustomerID=customer)
            for line in select('CusExtraCharge', SheetSeries=raw(parent, 'SheetSeries'), PayService=service)]
        field = 'Price' if function.endswith('Price') else 'PriceUnit'
        if not items:
            # 原@ProdID没有赋值，第一条物料专属分支不能命中。
            items = [item for item in select('QuoteItemPrice', CustomerID=customer, Item=service) if key(raw(item, 'ProdID') or '') == '']
            if not items:
                items = [item for item in select('QuoteItemPrice', Item=service)
                    if key(raw(item, 'ProdID') or '') == '' and key(raw(item, 'CustomerID') or '') == '']
            field = 'Price' if function.endswith('Price') else 'Unit'
        value = last('客户基础另收费→客户空物料→通用空物料', items, field)
        if function.endswith('Unit'): value = None if value is None else str(value)
    elif function == 'fn_ColorNum_BasicsPrice':
        items = [line for parent in select('CusBasicsPrice', CustomerID=customer)
            for line in select('CusBasicsPriceDetail', SheetSeries=raw(parent, 'SheetSeries'), GradeID=varchar(params.get('grade'), 30))]
        cost, dosage = (None if params.get(name) is None else float(params[name]) for name in ['cost','dosage'])
        first = [item for item in items if dosage is not None and cost is not None
            and raw(item,'StuffRatio1') is not None and raw(item,'StuffRatio2') is not None and raw(item,'FormulaCost2') is not None
            and float(raw(item,'StuffRatio1')) < dosage <= float(raw(item,'StuffRatio2')) and float(raw(item,'FormulaCost2')) >= cost]
        candidates('用量下限开/上限闭、成本上限闭', first, 'Price')
        prices = [raw(item,'Price') for item in first if raw(item,'Price') is not None]
        value = money(min(prices)) if prices else None
        if value in [None, 0]:
            second = [item for item in items if cost is not None and raw(item,'FormulaCost1') is not None and raw(item,'FormulaCost2') is not None
                and float(raw(item,'FormulaCost1')) <= cost < float(raw(item,'FormulaCost2'))]
            candidates('零/NULL价时成本下限闭/上限开', second, 'Price')
            prices = [raw(item,'Price') for item in second if raw(item,'Price') is not None]
            value = money(min(prices)) if prices else None
        value = (value or Decimal(0)) / Decimal(1000)
    elif function == 'fn_GetPriceUnit':
        weight = params.get('gray_quantity') if key(params.get('charging')) == '01' else params.get('weight')
        value = 2
        if weight is not None and 0 < weight <= 80:
            special = key(params.get('phase')) == 'RC07'
            items = [item for item in select('PPriceListVat','erp_base') if raw(item,'LengthDn') is not None and raw(item,'LengthUp') is not None
                and raw(item,'LengthDn') < weight <= raw(item,'LengthUp') and (key(raw(item,'PhaseID') or '') == 'RC07') == special]
            value = last('80公斤小缸计价单位', items, 'Unit', 2)
        else:
            number = extract_number(color,20)
            pairs = joined('Quote','QuoteDetail',number,customer,True,20)
            value = last('客户/20位数字色号计价单位', [line for _,line in pairs], 'PriceUnit', 2)
    else:
        value = Decimal(0)
        if key(params.get('charging')) == '02':
            pairs = joined('Quote','QuoteDetail',numeric_color(color))
            prices = [line for _,line in pairs]
            base = money(last('色号原价；原函数不按客户/物料筛选', prices, 'Price'))
            adjusts = joined('PriceAdjust','PriceAdjustDetail',numeric_color(color))
            adjusts.sort(key=lambda pair: (raw(pair[0],'StartDate') is not None, raw(pair[0],'StartDate'), pair[0].pk, pair[1].pk), reverse=True)
            candidates('调价候选按日期降序，仅原前两行', [line for _,line in adjusts], 'AdjustPrice')
            if not adjusts: value = base if prices else Decimal(0)
            elif function == 'fn_GetColorNumPrice': value = money(raw(adjusts[0][1],'AdjustPrice'))
            else:
                def decision(pair):
                    parent, line = pair
                    kind = key(raw(parent,'DateType'))
                    date = params.get('sheet_date') if kind == '1' else params.get('order_date') if kind == '0' else None
                    start = raw(parent,'StartDate')
                    return None if date is None or start is None else date >= start
                decision1 = decision(adjusts[0])
                if decision1 is True: value = money(raw(adjusts[0][1],'AdjustPrice'))
                elif decision1 is False:
                    if len(adjusts) < 2 or key(raw(adjusts[1][0],'SheetSeries') or '') == '': value = base
                    else:
                        decision2 = decision(adjusts[1])
                        if decision2 is True: value = money(raw(adjusts[1][1],'AdjustPrice'))
                        elif decision2 is False: value = base
            if function == 'fn_GetPriceListVat' and params.get('weight') is not None and 0 < params['weight'] <= 20:
                items = [item for item in select('PPriceListVat','erp_base') if raw(item,'LengthDn') is not None and raw(item,'LengthUp') is not None
                    and raw(item,'LengthDn') < params['weight'] <= raw(item,'LengthUp') and key(raw(item,'PhaseID') or '') != 'RC07']
                candidates('20公斤小缸逐行累加（重复区间保留）', items, 'Price')
                for item in items:
                    price = raw(item,'Price')
                    value = None if price is None else money((value or Decimal(0)) + price)
    issues=[]
    if function=='fn_GetPriceUnit' and value is not None and not 0<=value<=255:
        issues.append({'value':value,'issue':'原函数tinyint返回值溢出；原单位保留并展示，不改成默认单位，见E78'})
    return {'report': function, 'rows': [{'function': function, 'value': value}], 'candidate_rows': evidence,'supplemental_rows':issues,
        'notes': ['保留原函数的NULL、零值、负数及未使用参数；此查询不生成财务记录。',
            '原无序标量按项目ID最后一行，日期并列按表头/明细ID明确先后；全部候选展示，差异见E78。']}
