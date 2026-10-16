"""工卡六项套价与出库附加工艺取价，保留连接倍数和原NULL语义。"""
from .source_quality_reports import rows,key
from .source_business_updates import matching
from .source_stock_services import raw
from .source_package_labels import varchar


def calculate(function,params,query=rows):
    from .source_quote_functions import money
    evidence=[]
    def select(name,module='erp_sales',**filters):
        return list(matching(query(name,module),**filters).order_by('pk'))
    def value(item,field):return None if item is None else raw(item,field)
    def same(a,b):return a is not None and b is not None and key(a)==key(b)
    def add(stage,item,field,amount=None):
        amount=value(item,field) if amount is None else amount
        if item is not None:evidence.append({'stage':stage,'entity':item._meta.label,'record_id':item.pk,'legacy_id':item.legacy_id,'field':field,'value':amount})
        return amount
    job= varchar(params.get('job'),30)
    if function=='fn_GetTechPrice':
        amounts=[]
        for detail in select('ProdOutDetail','erp_warehouse',DetailNo=varchar(params.get('detail'),32),JobSheetNo=job):
            for head in select('ProdOut','erp_warehouse',SheetSeries=raw(detail,'SheetSeries')):
                for atte in select('ProdOutPriceAtte','erp_warehouse',SheetSeries=raw(detail,'SheetSeries'),DetailNo=raw(detail,'DetailNo'),FieldType='05'):
                    if raw(atte,'PriceUnit')!=4:continue
                    customer=varchar(raw(head,'CustomerID'),20);service=varchar(raw(atte,'AtteValue'),50)
                    prices=select('QuoteItemPrice',CustomerID=customer,Item=service)
                    if not prices:prices=[row for row in select('QuoteItemPrice',Item=service) if key(raw(row,'CustomerID') or '')=='']
                    amounts.extend(add('出库附加工艺：客户优先；所有候选累加',row,'Price') for row in prices)
        present=[float(v) for v in amounts if v is not None]
        result=sum(present) if present else None;components=[]
    else:
        contexts=[]
        for sheet in select('JobSheet','erp_production',SheetNo=job):
            for gray in select('PGray','erp_base',GrayID=raw(sheet,'ProdID')) or [None]:
                for recipe in select('DyeRecipe','erp_sampling',ColorNum=raw(sheet,'ColorNum')) or [None]:
                    contexts.append((sheet,gray,recipe))
                    evidence.append({'stage':'工卡/坯料/配方左连接候选','record_id':sheet.pk,
                        'gray_id':None if gray is None else gray.pk,'recipe_id':None if recipe is None else recipe.pk})
        sheet,gray,recipe=contexts[-1] if contexts else (None,None,None)
        customer=varchar(value(sheet,'CustomerID'),20);fabric=varchar(value(gray,'FabricKindID'),20)
        depth=varchar(value(recipe,'ColorDepthID'),20);weight=money(value(sheet,'Weight'))
        fixed=[]
        for line in select('FixedPriceDetail'):
            for head in select('FixedPrice',SheetSeries=raw(line,'SheetSeries')):
                fixed.append((head,line))
        matched=[(head,line) for head,line in fixed if same(raw(head,'CustomerID'),customer)
            and same(raw(line,'FabricKind'),fabric) and same(raw(line,'ColorDepthID'),depth)]
        base=[add('1基础套价',line,'CusPrice') for head,line in matched]
        job_extras=[]
        for sheet1,gray1,recipe1 in contexts:
            for atte in select('JobAtte','erp_production',SheetSeries=raw(sheet1,'SheetSeries'),FieldType='05'):
                job_extras.append((sheet1,gray1,recipe1,atte))
        included=[]
        for head,line in fixed:
            for atte in select('FixedPriceAtte',DetailNo=raw(line,'DetailNo')):
                included.append((head,line,atte))
        added=[]
        for sh,gr,re,atte in job_extras:
            if any(same(raw(a,'AtteCode'),raw(atte,'AtteCode')) and same(raw(h,'CustomerID'),raw(sh,'CustomerID'))
                   and same(raw(l,'FabricKind'),value(gr,'FabricKindID')) and same(raw(l,'ColorDepthID'),value(re,'ColorDepthID')) for h,l,a in included):continue
            for price in select('QuoteItemPrice',Item=raw(atte,'AtteCode')):
                for parent in select('FixedPrice',SheetSeries=raw(price,'SheetSeries'),CustomerID=raw(sh,'CustomerID')):
                    amount=0 if same(fabric,'ZN') and same(raw(price,'Item'),'23053104') else raw(price,'Price')
                    added.append(add('2工卡额外工艺',price,'Price',amount))
        deducted=[]
        for head,line,atte in included:
            if not (same(raw(head,'CustomerID'),customer) and same(raw(line,'FabricKind'),fabric) and same(raw(line,'ColorDepthID'),depth)):continue
            if any(same(raw(a,'AtteCode'),raw(atte,'AtteCode')) and same(raw(sh,'CustomerID'),customer)
                and same(value(gr,'FabricKindID'),fabric) and same(value(re,'ColorDepthID'),depth) for sh,gr,re,a in job_extras):continue
            for price in select('QuoteItemPrice',SheetSeries=raw(head,'SheetSeries'),Item=raw(atte,'AtteCode')):
                amount=0 if same(fabric,'ZN') and same(raw(price,'Item'),'23053104') else raw(price,'Price')
                deducted.append(add('3套价包含但工卡未用的工艺扣价',price,'Price',amount))
        fluorescence=[add('4荧光附价',row,'NumValue') for row in select('PFieldValid','erp_base',FieldType='fluorescence',Code=varchar(value(recipe,'Fluorescence'),20))]
        grades=[add('5等级附价',row,'NumValue') for row in select('PFieldValid','erp_base',FieldType='ColorNumGradeID',Code=varchar(value(recipe,'GradeID'),20))]
        vats=[]
        for head in select('FixedPrice',CustomerID=customer):
            for line in select('FixedCanDetail','erp_base',SheetSeries=raw(head,'SheetSeries'),FabricKindID=fabric):
                lower,upper=raw(line,'Weight1'),raw(line,'Weight2')
                if weight is not None and lower is not None and upper is not None and lower<weight<=upper:
                    vats.append(add('6小缸附价TOP1候选',line,'Price'))
        def last(items):return float(items[-1] or 0) if items else 0.
        parts=[last(base),sum(float(v) for v in added if v is not None),sum(float(v) for v in deducted if v is not None),
            last(fluorescence),last(grades),float(vats[0] or 0) if vats else 0.]
        components=[{'component':i+1,'value':v} for i,v in enumerate(parts)]
        results={0:parts[0]+parts[1]-parts[2]+sum(parts[3:]),**{i+1:v for i,v in enumerate(parts)},
            7:parts[0]+parts[1]-parts[2],8:sum(parts[3:])}
        result=results.get(params.get('kind'))
    return {'report':function,'rows':[{'function':function,'value':result}],'result_rows':components,'candidate_rows':evidence,
        'notes':['原重复连接全部参与计算，NULL金额不虚构；fn_NewGetDyePrice保留ZN指定项目免价及全部Kind分量。',
            '无ORDER BY的单值赋值按项目ID最后候选；TOP1小缸按项目ID第一候选，差异见E78。']}
