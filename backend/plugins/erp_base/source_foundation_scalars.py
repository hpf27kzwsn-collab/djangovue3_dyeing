"""原基础计算的剩余标量规则；无效原输入保留错误，不代填零值。"""
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP, localcontext
from django.utils import timezone
import json
from pathlib import Path
from .source_package_labels import varchar

PINYIN = json.loads(Path(__file__).with_name('source_pinyin_map.json').read_text(encoding='utf8'))


def pinyin(value, variant='first'):
    """两版原阈值排序表逐BMP字符核对；不使用现代拼音库替代。"""
    if value is None:
        return ''
    text = value[:400 if variant == 'first' else 4000]
    mapping = PINYIN[variant]
    if variant == 'first':
        return ''.join(mapping.get(str(ord(c)), c) for c in text.rstrip(' '))
    result = ''
    while text.rstrip(' '):
        part = mapping.get(str(ord(text[0])), text[0])
        result = None if result is None or part is None else result+part
        size = len(text.rstrip(' '))-1
        text = text[-size:] if size else ''
    return result


def station_split(value, delimiter):
    value, delimiter = varchar(value,8000), varchar(delimiter,10)
    if delimiter is not None and not delimiter.rstrip(' '):
        raise ValueError('原get_fsplit_StationID的空分隔符循环不推进，不能生成有限结果；原输入可原样留档。')
    result=[]
    if value is None:
        return result
    while delimiter is not None:
        index=value.upper().find(delimiter.upper())
        if index < 0:
            break
        result.append({'StationID':value[:index]})
        value=value[index+len(delimiter.rstrip(' ')):]
    if value.rstrip(' '):
        result.append({'StationID':value})
    return result


def employee_names(value, delimiter, query=None):
    from .source_quality_reports import rows
    from .source_trial_steps import sql_like
    from .source_stock_services import raw
    query = rows if query is None else query
    delimiter=varchar(delimiter,10)
    wrapped=None if value is None or delimiter is None else delimiter+value+delimiter
    result=None
    for employee in query('HEmployee','erp_base').order_by('pk'):
        code=raw(employee,'EmpID')
        pattern=None if code is None or delimiter is None else '%'+delimiter+code+delimiter+'%'
        if wrapped is not None and pattern is not None and sql_like(wrapped,pattern):
            name=raw(employee,'Name')
            result=None if name is None else ('' if result is None else result+delimiter)+name
    return result or ''


def feel_code(product, query=None):
    from .source_quality_reports import rows
    from .source_business_updates import matching
    from .source_stock_services import raw
    query=rows if query is None else query
    for item in matching(query('PProduct','erp_base'),ProdID=varchar(product,100)).order_by('pk'):
        for feel in matching(query('PFeelCode','erp_base'),ProdID=raw(item,'ProdID')).order_by('pk'):
            value=varchar(raw(feel,'FeelCode'),50)
            return None if value is None or value=='' else value
    return None


def sql_int(value):
    number = int(value.strip() or '0')
    if not -2147483648 <= number <= 2147483647:
        raise OverflowError('原INT转换溢出。')
    return number


def expand_range(value):
    value = None if value is None else value[:20]
    if value is None or '-' not in value:
        return value
    position = value.index('-')
    start = sql_int(value[:position])
    size = len(value.rstrip(' '))-position-1
    end = sql_int(value[-size:] if size else '')
    if start > end:
        raise ValueError('原fn_ExpandRange最终LEFT长度为负数。')
    if end == 2147483647:
        raise OverflowError('原fn_ExpandRange循环计数INT溢出。')
    return ','.join(str(n) for n in range(start, end+1))


def dye_vat(value):
    value = 0 if value is None else float(value)
    if value <= 0:
        return 0.0
    if value < 300:
        return 1.7
    return float(Decimal(str(value/300)).quantize(Decimal('.000001'), rounding=ROUND_HALF_UP))


def elapsed(value, now=None):
    if value is None:
        return ''
    now = timezone.localtime() if now is None else now
    # DATEDIFF计算跨越的分钟/小时边界，并非先除总秒数。
    total = int((now.replace(second=0, microsecond=0)-value.replace(second=0, microsecond=0)).total_seconds()/60)
    if not -2147483648 <= total <= 2147483647:
        raise OverflowError('原DATEDIFF分钟溢出。')
    if total > 1440:
        hours = int((now.replace(minute=0, second=0, microsecond=0)-value.replace(minute=0, second=0, microsecond=0)).total_seconds()/3600)
        return f'{int(hours/24)}天{hours-int(hours/24)*24}时'
    hours = int(total/60)
    return f'{hours}时{total-hours*60}分'


def uppercase_number(value, transform_type):
    """L2U共享打印格式；不办理应收、应付或记账。"""
    if value is None:
        return ''
    with localcontext() as context:
        context.prec = 40
        number = Decimal(str(value)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        if abs(number) >= Decimal('10000000000000'):
            raise OverflowError('原numeric(15,2)溢出。')
    if number < 0:
        return None  # 原CASE没有负号分支，字符串连接传播NULL。
    text = format(abs(number), '.2f')
    digits = dict(zip('0123456789.', '零壹贰叁肆伍陆柒捌玖元'))
    units = ['分', '角', '', '', '拾', '佰', '仟', '万', '拾', '佰', '仟', '亿', '拾', '佰', '仟', '万']
    result = ''.join(digits[c]+units[i] for i, c in reversed(list(enumerate(text[::-1]))))
    if transform_type == 0:
        pairs = [('零拾','零'),('零佰','零'),('零仟','零'),('零零零','零'),('零零','零'),
                 ('零角零分','整'),('零分','整'),('零角','零'),('零亿零万零元','亿元'),
                 ('亿零万零元','亿元'),('零亿零万','亿'),('零万零元','万元'),('万零元','万元'),
                 ('零亿','亿'),('零万','万'),('零元','元'),('零零','零')]
        for old, new in pairs:
            result = result.replace(old, new)
    for prefix in ['元', '零', '角', '分']:
        if result.startswith(prefix):
            result = result[1:]
    return '零元整' if result.startswith('整') else result
def new_string_split(value, delimiter):
    """New_StringSplit：原多字符分隔符仍只前移一字符，空分隔符逐字输出空项。"""
    if value is None:return []
    delimiter=None if delimiter is None else delimiter[:20]
    end=len(value.rstrip(' '));position=0;result=[]
    while position<end:
        found=-1 if delimiter is None else value.upper().find(delimiter.upper(),position)
        stop=end if found<0 else found
        part=value[position:stop].strip(' ')
        if len(part)>200:raise ValueError('原New_StringSplit单项超过nvarchar(200)。')
        result.append({'EmpID':part});position=stop+1
    return result


def split_with_row_number(value, delimiter):
    """f_splitWithRowNo：保留尾空项、仅排除末尾反斜杠、每次只消耗一个分隔字符。"""
    if value is None:return []
    value=value.replace('\t','').replace('\n','').replace('\r','').strip(' ')
    delimiter=varchar(delimiter,10);result=[]
    if delimiter=='':raise ValueError('原空分隔符会在空串上无限循环，必须提供非空分隔符。')
    def append(part):
        if len(part.encode('gbk',errors='replace'))>100:raise ValueError('原f_splitWithRowNo单项超过varchar(100)。')
        result.append({'RowNo':len(result)+1,'Name':part})
    while delimiter is not None:
        index=value.upper().find(delimiter.upper())
        if index<0:break
        append(value[:index]);value=value[index+1:len(value.rstrip(' '))]
    if value.rstrip(' ')!='\\':append(value)
    return result


def pack_quantity_price(process, query):
    from .source_business_updates import matching
    from .source_stock_services import raw
    matches=list(matching(query('PProcess','erp_base'),ProcessID=varchar(process,30)).order_by('pk'))
    return None if not matches else raw(matches[-1],'Price')

