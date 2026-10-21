"""固定第三阶段查询参数：日期在SQL中保留日期类型。"""
from datetime import datetime
from django.utils import timezone
from sqlglot import exp,parse_one


def bind(sql,parameters):
    tree=parse_one(sql,read='tsql');values={k.lower():v for k,v in parameters.items()}
    for parameter in list(tree.find_all(exp.Parameter)):
        value=values[parameter.name.lower()]
        if isinstance(value,datetime):
            if timezone.is_aware(value):value=timezone.localtime(value)
            replacement=exp.Cast(this=exp.Literal.string(value.replace(tzinfo=None).isoformat(' ')),to=exp.DataType.build('DATETIME'))
        else:replacement=exp.convert(int(value) if isinstance(value,bool) else value)
        parameter.replace(replacement)
    return tree.sql(dialect='tsql')
