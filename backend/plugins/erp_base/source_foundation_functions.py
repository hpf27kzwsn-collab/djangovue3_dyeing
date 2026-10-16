"""当前旧基础函数；原函数的零值、错误、截断分别保留。"""
import re
import unicodedata
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP, localcontext
from .source_package_labels import varchar


def compatible(char):
    return unicodedata.normalize('NFKC', char)


def extract(value, kind):
    """Fn_Get_AZ、Fn_Get_NumNo、GET_NUMBER；保留原字符，不把全角改写为半角。"""
    value = varchar(value, 100)
    if value is None:
        return None
    def accepted(char):
        normalized = compatible(char)
        if kind == 'Fn_Get_AZ':
            return bool(re.fullmatch('[A-Za-z]', unicodedata.normalize('NFD', normalized)[0]))
        return normalized in '0123456789' or kind == 'Fn_Get_NumNo' and normalized == '.'
    return varchar(''.join(c for c in value if accepted(c)), 100 if kind == 'GET_NUMBER' else 20)


def extract_number(value,width=10):
    """F_Get_No/Fn_Get_No：输入100字节，分别返回10/20字节，不改写全角原字符。"""
    return varchar(extract(value,'GET_NUMBER'),width)


def same_number(left,right):
    return left is not None and right is not None and compatible(left).rstrip(' ').upper()==compatible(right).rstrip(' ').upper()


def number_matches(query,value,width=10):
    expected=extract_number(value,width)
    ids=[pk for pk,color in query.values_list('pk','old_color_num') if same_number(extract_number(color,width),expected)]
    return query.filter(pk__in=ids)


def first_number(value):
    """GetNumberFromString3：取首段，孤立负号为0，'-.'仍是转换错误。"""
    value = varchar(value, 100)
    text = ''
    for char in (value or '').rstrip(' '):
        n = compatible(char)
        if n in '0123456789' or n == '.' and text and '.' not in text or n == '-' and not text:
            text = (text+char).replace(' ', '')[:50]
        elif text:
            break
    if unicodedata.normalize('NFKC', text) in ['', '-', '.']:
        return 0.0
    if not re.fullmatch(r'-?[0-9]+(?:\.[0-9]*)?|-?\.[0-9]+', text):
        raise ValueError('原GetNumberFromString3无法将提取结果转换为float。')
    return float(text)


def safe_decimal(value, integer=False):
    """SafeVarToFloat/Int的原规则；不是给其他新逻辑增加兜底转换。"""
    value = varchar(value, 1000)
    text = '0' if value is None else value.strip(' ')
    # 原循环先赋值varchar(1)，双字节全角数字不能作为有效数字通过。
    if not text or any(len(c.encode('gbk')) != 1 or c not in '0123456789.' for c in text):
        return Decimal('0.0000')
    if not re.fullmatch(r'[0-9]+(?:\.[0-9]*)?|\.[0-9]+', text):
        raise ValueError('原数字函数的numeric转换错误。')
    with localcontext() as context:
        context.prec = max(32, len(text)+5)
        number = Decimal(text).quantize(Decimal('1' if integer else '.0001'), rounding=ROUND_HALF_UP)
        if abs(number) >= Decimal(10)**(18 if integer else 14) or integer and number > 2147483647:
            raise OverflowError('原数字函数numeric/int溢出。')
        return number.quantize(Decimal('.0001'))


SYMBOLS = dict(zip('。，；：！？、（）【】｛｝《》「」『』～＠＃￥％＆＊＋－＝／｜＼',
                   '.,;:!?,()[]{}<>""""~@#$%&*+-=/|\\'))


def normalize_text(value):
    """NormalizeTextFast：仅替换原32个标点及6类换行，制表符不清理。"""
    if value is None or not value.rstrip(' '):
        return value
    text = value.replace('\r\n', ' ')
    for char in '\r\n\x85\u2028\u2029':
        text = text.replace(char, ' ')
    # FOR XML PATH(TYPE)不接受XML 1.0禁止的控制字符。
    if any(ord(c) < 32 and c != '\t' for c in text):
        raise ValueError('原NormalizeTextFast的XML字符转换错误。')
    return re.sub(' +', ' ', ''.join(SYMBOLS.get(c, c) for c in text)).strip(' ')


FUNCTIONS = {'Fn_Get_AZ': lambda v: extract(v, 'Fn_Get_AZ'),
             'F_Get_No':extract_number,'Fn_Get_No':lambda v:extract_number(v,20),
             'Fn_Get_NumNo': lambda v: extract(v, 'Fn_Get_NumNo'),
             'GET_NUMBER': lambda v: extract(v, 'GET_NUMBER'),
             'GetNumberFromString3': first_number, 'NormalizeTextFast': normalize_text,
             'SafeVarToFloat': safe_decimal, 'SafeVarToInt': lambda v: safe_decimal(v, True)}
from .source_foundation_scalars import expand_range, dye_vat, pinyin
FUNCTIONS.update(fn_ExpandRange=expand_range, fn_GetDyeVat=dye_vat, f_GetPy=pinyin,
                 fun_getPY=lambda value: pinyin(value, 'second'))


def continuous_dates(value, kind, previous, following):
    """dbo.fn_GetContinuousDate；md指定月为上月previous日到本月following日。"""
    kind = None if kind is None else kind[:10].lower().rstrip(' ')
    base = value
    def month_shift(day, count):
        if day is None:
            return None
        year, month = divmod(day.year*12+day.month-1+count, 12)
        return date(year, month+1, 1)
    def day_shift(day, count):
        return None if day is None else day+timedelta(days=count)
    if kind in ['year', 'y', 'month', 'mon', 'm', 'day', 'd']:
        unit = 'year' if kind in ['year', 'y'] else 'month' if kind in ['month', 'mon', 'm'] else 'day'
        if base is not None:
            base = date(base.year, 1 if unit=='year' else base.month, 1 if unit!='day' else base.day)
        offsets = list(range(-max(previous or 0, 0), 0))+[0]+list(range(1, (following or 0)+1))
        dates = [day_shift(base, n) if unit=='day' else month_shift(base, n*(12 if unit=='year' else 1)) for n in offsets]
    elif kind in ['yearmonth', 'ym']:
        unit = 'yearmonth'
        base = None if base is None else date(base.year, 1, 1)
        dates = [month_shift(base, n) for n in range(12)]
    elif kind in ['monthday', 'md']:
        unit = 'monthday'
        if base is None:
            return []
        first = date(base.year, base.month, 1)
        if previous is not None and following is not None and previous>0 and following>0:
            start = month_shift(first, -1)+timedelta(days=previous-1)
            end = first+timedelta(days=following)
        else:
            start, end = first, month_shift(first, 1)
        dates = [start+timedelta(days=n) for n in range((end-start).days)]
    else:
        return []
    result = []
    for day in dates:
        alias = common = None
        if day is not None:
            alias = f'{day.year}年'
            common = str(day.year)
            if unit != 'year':
                alias += f'{day.month}月'; common += f'/{day.month}'
            if unit in ['day', 'monthday']:
                alias += f'{day.day}日'; common += f'/{day.day}'
            if unit == 'yearmonth':
                alias = f'{day.month}月'
            if unit == 'monthday':
                common = day.isoformat()
        result.append({'DataDate': day, 'DateAlis': alias, 'DateCommon': common})
    return result
