"""原日期格式的数字部分及引号字面量；区域月份/星期名称尚不猜测。"""
import re
from datetime import datetime
from django.core.exceptions import ValidationError


def format_date(value,pattern):
    if len(pattern)==1:
        raise ValidationError({'format':'单字符日期标准格式需要旧客户端区域定义：'+pattern})
    if not isinstance(value,datetime):value=datetime.combine(value,datetime.min.time())
    pieces=[];index=0
    while index<len(pattern):
        char=pattern[index]
        if char in ['"',"'"]:
            quote=char;index+=1;literal=[]
            while index<len(pattern) and pattern[index]!=quote:
                if pattern[index]=='\\':index+=1
                if index==len(pattern):raise ValidationError({'format':'日期字面量转义未结束：'+pattern})
                literal.append(pattern[index]);index+=1
            if index==len(pattern):raise ValidationError({'format':'日期字面量引号未结束：'+pattern})
            pieces.append(''.join(literal));index+=1;continue
        if char=='\\':
            index+=1
            if index==len(pattern):raise ValidationError({'format':'日期转义未结束：'+pattern})
            pieces.append(pattern[index]);index+=1;continue
        if char=='%':raise ValidationError({'format':'未实现百分号日期格式标记：'+pattern})
        if char.isascii() and char.isalpha():
            token=re.match(r'([A-Za-z])\1*',pattern[index:])[0]
            if token in ['yyyy','yy']:text=str(value.year).zfill(4) if token=='yyyy' else str(value.year%100).zfill(2)
            elif token in ['M','MM','d','dd','H','HH','h','hh','m','mm','s','ss']:
                name={'M':'month','d':'day','H':'hour','h':'hour','m':'minute','s':'second'}[token[0]]
                number=getattr(value,name)
                if token[0]=='h':number=number%12 or 12
                text=str(number).zfill(len(token))
            else:raise ValidationError({'format':'未实现此原日期格式标记：'+token+'；'+pattern})
            pieces.append(text);index+=len(token);continue
        pieces.append(char);index+=1
    return ''.join(pieces)
