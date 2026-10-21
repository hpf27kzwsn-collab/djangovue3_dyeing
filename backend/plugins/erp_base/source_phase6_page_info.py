"""原页信息的已出现格式；默认区域格式明确采用本项目格式，保留旧文字和占位编号。"""
import re
from django.core.exceptions import ValidationError


def date_text(value, spec):
    tokens={'yyyy':f'{value.year:04}', 'yy':f'{value.year%100:02}',
        'MM':f'{value.month:02}', 'M':str(value.month), 'dd':f'{value.day:02}', 'd':str(value.day),
        'HH':f'{value.hour:02}', 'H':str(value.hour), 'mm':f'{value.minute:02}', 'm':str(value.minute),
        'ss':f'{value.second:02}', 's':str(value.second)}
    parts=re.findall(r"'[^']*'|yyyy|yy|MM|M|dd|d|HH|H|mm|m|ss|s|.",spec)
    result=[]
    for part in parts:
        if part.startswith("'"):result.append(part[1:-1])
        elif part in tokens:result.append(tokens[part])
        elif re.search('[A-Za-z]',part):raise ValidationError({'format':'未实现页日期格式：'+spec})
        else:result.append(part)
    return ''.join(result)


def page_info(attributes, number, total, generated_at):
    mode=attributes.get('PageInfo','NumberOfTotal')
    pattern=attributes.get('Format',attributes.get('TextFormatString',''))
    if mode=='None':return pattern
    if not pattern:pattern={'Number':'{0}','NumberOfTotal':'{0} / {1}','DateTime':'{0:yyyy-MM-dd HH:mm:ss}'}[mode]
    def replace(match):
        index=int(match[1]);spec=match[2] or ''
        if mode=='DateTime':
            if index!=0:raise ValidationError({'format':'日期页信息只有占位0。'})
            return date_text(generated_at,spec or 'yyyy-MM-dd HH:mm:ss')
        value=[number,total][index]
        if spec and not re.fullmatch('0+',spec):raise ValidationError({'format':'未实现页码格式：'+spec})
        return str(value).zfill(len(spec))
    return re.sub(r'\{([01])(?::([^{}]+))?\}',replace,pattern)
