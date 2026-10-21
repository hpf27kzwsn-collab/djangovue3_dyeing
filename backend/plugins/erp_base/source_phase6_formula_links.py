"""未建额外外键的原主从码；重复原行均保留，父行有多候选时不任选。"""
RAW_LINKS={
    'PStuffWeightDetail':('PStuffWeightPhase',{'SheetSeries':'SheetSeries','PhaseNo':'PhaseNo'}),
    'DefectiveInRecord':('DefectiveInDetail',{'SheetSeries':'SheetSeries','DetailNo':'DetailNo'}),
    'ProdOutPriceProcess':('ProdOutDetail',{'SheetSeries':'SheetSeries','DetailNo':'DetailNo'}),
    'ShiftArrangeDetail':('ShiftArrange',{'Sheetseries':'SheetSeries'}),
}


def match(query,values):
    from .source_business_updates import matching
    for field,value in values.items():
        if value is None:return query.none()
        if isinstance(value,str):query=matching(query,**{field:value})
        else:query=query.filter(**{query.model.SOURCE_FIELDS[field]:value})
    return query


def parent_rows(item):
    from .source_phase3_operations import model
    from .source_stock_services import raw
    from .source_execution_state import active
    if item.SOURCE_TABLE not in RAW_LINKS:return []
    table,keys=RAW_LINKS[item.SOURCE_TABLE]
    return list(match(active(model(table).objects.all()),{target:raw(item,source) for source,target in keys.items()}).order_by('pk'))


def child_rows(item):
    from .source_phase3_operations import model
    from .source_stock_services import raw
    from .source_execution_state import active
    for table,(parent,keys) in RAW_LINKS.items():
        if parent==item.SOURCE_TABLE:
            yield from match(active(model(table).objects.all()),{source:raw(item,target) for source,target in keys.items()}).order_by('pk')
