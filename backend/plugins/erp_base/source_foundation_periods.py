"""原业务期间边界；只计算日期，不进行财务处理。"""
from datetime import datetime, timedelta, time
from .source_quality_reports import rows, key
from .source_stock_services import raw


def boundary(value, year, reference):
    if value is None:
        return None
    parts=value.strip().split(maxsplit=1)
    day=datetime.strptime(f'{year}-{parts[0]}','%Y-%m-%d')
    clock=time.fromisoformat(parts[1]) if len(parts)==2 else time()
    return datetime.combine(day.date(),clock).replace(tzinfo=reference.tzinfo)


def periods(value, sources=None, begin=None, end=None):
    """Sp_GetAccDate输出参数未命中保持原值；两个函数默认NULL。"""
    if value is None:
        return begin, end
    sources = rows('SAccMonth', 'erp_base').order_by('pk') if sources is None else sources
    for item in sources:
        month = raw(item, 'AccMonth')
        start = boundary(raw(item,'StartTime'), value.year-(month==1), value)
        stop = boundary(raw(item,'EndTime'), value.year+(month==1 and value.month==12), value)
        if start is not None and stop is not None and start <= value < stop:
            begin = boundary(raw(item,'StartTime'), value.year-(month==1 and value.month==1), value)
            end = stop
    if value.month == 2 and end is not None and end.day == 28 and (end+timedelta(days=1)).month == 2:
        end += timedelta(days=1)
    return begin, end


def parameter_first_date(value, sources=None):
    if value is None:
        return None
    sources = list(rows('SSysParams','erp_base')) if sources is None else sources
    result = None
    for month, abbreviation in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(), 1):
        parts = []
        for prefix in ['Beg','End']:
            values = [raw(p,'Description') for p in sources if key(raw(p,'ParamName')) == key(prefix+abbreviation)
                      and raw(p,'Description') is not None]
            parts.append(max(values, key=key) if values else None)
        start = boundary(parts[0], value.year-(month==1), value)
        # 原参数版12月上界使用BegJan，不能改成EndJan。
        stop = boundary(parts[0] if month==1 and value.month==12 else parts[1],
                        value.year+(month==1 and value.month==12), value)
        if start is not None and stop is not None and start <= value < stop:
            result = boundary(parts[0], value.year-(month==1 and value.month==1), value)
    return result
