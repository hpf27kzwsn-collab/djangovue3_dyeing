"""FD_GetFieldSeries六路原算法的明确复刻；预览不占号。"""
from datetime import timedelta
from .source_foundation_scalars import sql_int
from .source_package_labels import varchar
from .source_trial_steps import sql_like, equal
from .source_stock_services import raw
from .source_business_updates import matching


def right(value,width):
    if width<0:
        raise ValueError('原RIGHT长度为负数。')
    return value[-width:] if width else ''


def next_number(rule, candidates, series, at):
    kind=rule['FieldKind'];prefix=rule['Prefix'] or ''
    width=2 if rule['FixedLength'] is None or rule['FixedLength']<=0 else rule['FixedLength']
    values=[value for value in candidates if value is not None]
    def maximum(length):
        value=max(values,key=lambda v:v.rstrip(' ').upper()) if values and isinstance(values[0],str) else max(values) if values else ''
        return varchar(str(value),length)
    def formatted(number,length):
        number=sql_int(str(number))
        return right('0000000000'+varchar(str(number),10),length)
    if kind=='DateCode':
        year_width=max(2,min(4,4 if rule['YearCode'] is None else rule['YearCode']))
        prefix=prefix+at.strftime('%Y')[-year_width:]+(rule['YearMonthSplit'] or '')+at.strftime('%m')+(rule['MonthDaySplit'] or '')+at.strftime('%d')+(rule['DayQueueSplit'] or '')
        suffix_width=3 if rule['EndCode'] is None else 2 if not str(rule['EndCode']).rstrip(' ') else sql_int(str(rule['EndCode']))
        if suffix_width<0:
            raise ValueError('原SUBSTRING长度为负数。')
        numbers=[]
        for value in values:
            value=str(value)
            if sql_like(value,prefix+'%'):
                position=value.upper().find(prefix.upper())
                numbers.append(sql_int(value[position+len(prefix.rstrip(' ')):position+len(prefix.rstrip(' '))+suffix_width]))
        return varchar(prefix+formatted((max(numbers) if numbers else 0)+1,suffix_width),100)
    if kind=='AutoAdd_Time':
        # SQL datetime以1/300秒存储；DATEPART(ms)输出0/3/7等整数，不补三位。
        midnight=at.replace(hour=0,minute=0,second=0,microsecond=0)
        ticks=int((at-midnight).total_seconds()*300+0.5)
        milliseconds=(ticks*1000+150)//300
        rounded=midnight+timedelta(milliseconds=milliseconds)
        return rounded.strftime('%Y%m%d%H%M%S')+str(rounded.microsecond//1000)
    if kind in ['RowNo','SheetRowNo','SeriesAndRowNo']:
        value=maximum(100 if kind=='SeriesAndRowNo' else 10)
        if kind=='SeriesAndRowNo' and value.rstrip(' '):
            value=varchar(value[value.find('-')+1:],10)
        number=sql_int(value)+1 if value.rstrip(' ') else 1
        suffix=formatted(number,width)
        return None if kind=='SeriesAndRowNo' and series is None else varchar(series+'-'+suffix,100) if kind=='SeriesAndRowNo' else suffix
    if kind=='AutoAdd':
        values=[v for v in values if not prefix.rstrip(' ') or sql_like(str(v),prefix+'%')]
        value=maximum(10)
        if value.rstrip(' '):
            sql_int(prefix)  # 原@Prefix+1的隐式转换；原SUBSTRING长度恒为0。
        return varchar(prefix+formatted(1,max(6,width)),100)
    return ''  # 原过程没有其他FieldKind分支。


def preview(model, old, rule, series, at, query):
    source=query(model.__name__.removeprefix('SourceDye'),model._meta.app_label)
    if rule['FieldKind'] in ['SeriesAndRowNo','SheetRowNo']:
        source=matching(source,SheetSeries=series)
    values=list(source.values_list(model.SOURCE_FIELDS[old],flat=True))
    return next_number(rule,values,series,at)
