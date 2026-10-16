"""已登记资料选择SQL的只读翻译；输入只能选择登记编号与原字段名。"""
import re
import json
from pathlib import Path
import unicodedata
from functools import lru_cache
import sqlglot
from sqlglot import exp
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.annotate_types import annotate_types
from sqlglot.optimizer.pushdown_projections import pushdown_projections
from django.apps import apps
from django.conf import settings
from django.db import connection
from .source_execution_state import active
from .source_trial_steps import sql_like
from .source_package_labels import varchar
VIEWS=json.loads(Path(__file__).with_name('source_foundation_view_definitions.json').read_text(encoding='utf8'))
INLINE_FUNCTIONS={
    'fn_getphaseno': "(SELECT TOP 1 NULLIF(CONVERT(VARCHAR(10),_phase.PhaseNo),'') FROM dye.StuffWeightPhase _phase WHERE _phase.SheetSeries=@p0 AND _phase.ProgramID=@p1)",
    'fn_getfeelcode': "(SELECT TOP 1 NULLIF(CONVERT(VARCHAR(50),_feel.FeelCode),'') FROM dye.p_Product _product JOIN dye.p_FeelCode _feel ON _feel.ProdID=_product.ProdID WHERE _product.ProdID=@p0)",
    'fn_getdyevat': 'CASE WHEN ISNULL(@p0,0)>0 THEN CASE WHEN @p0<300 THEN 1.7 ELSE ROUND(CAST(@p0/300 AS FLOAT),6) END ELSE 0 END',
}
_GROUP="FROM dye.JobShiftEmp _j JOIN dye.h_Employee _h ON _h.EmpID=_j.EmpID WHERE _j.JobSheetNo=@p0 AND _j.ProcessID=@p1 AND _j.ProcessNo=@p2 AND _j.ShiftID=@p7"
INLINE_FUNCTIONS['fn_getprocessworkmoney']="""CAST(ROUND((@p6/1000)*@p5 /
 ((SELECT COUNT(_j.ShiftID) {group} AND ISNULL(_h.Ratio,1)=ISNULL(@p3,1))*ISNULL(@p3,1)
 + CASE WHEN (SELECT COUNT(DISTINCT ISNULL(_h.Ratio,1)) {group})>1 THEN
 (SELECT TOP 1 COUNT(_j.ShiftID)*ISNULL(_h.Ratio,1) {group} AND ISNULL(_h.Ratio,0)<>ISNULL(@p3,0)
  GROUP BY ISNULL(_h.Ratio,1) ORDER BY ISNULL(_h.Ratio,1) DESC) ELSE 0 END)*ISNULL(@p3,1),2) AS FLOAT)""".format(group=_GROUP)


def inline_functions(tree):
    for node in list(tree.find_all(exp.Dot)):
        function=node.expression
        if isinstance(function,exp.Anonymous) and str(node.this).lower()=='dye' and function.name.lower() in INLINE_FUNCTIONS:
            replacement=sqlglot.parse_one(INLINE_FUNCTIONS[function.name.lower()],read='tsql')
            for parameter in list(replacement.find_all(exp.Parameter)):
                parameter.replace(function.expressions[int(parameter.name.removeprefix('p'))].copy())
            node.replace(replacement)
    return tree


def expand_views(tree, trail=()):
    for table in list(tree.find_all(exp.Table)):
        name=table.name.lower()
        if not table.catalog and table.db.lower() in ['', 'dye'] and name in VIEWS:
            if name in trail:
                raise ValueError('原视图循环引用：'+name)
            definition=sqlglot.parse_one(VIEWS[name],read='tsql').expression
            expand_views(definition,(*trail,name))
            table.replace(exp.Subquery(this=definition,alias=exp.TableAlias(this=exp.to_identifier(table.alias or table.name))))
    return tree


def original_query(spec):
    if spec.get('execution_query') is not None:
        return spec['execution_query']
    sql=spec['query']
    offset=sql.find('1=1')
    if offset>=0:
        sql=sql[:offset]
    elif re.search('where',sql,re.I):
        sql+=' AND '
    else:
        sql+=' WHERE '
    return sql+(spec['LookupDataFilter'] or '1=1')


def dtype(field):
    kind=field.get_internal_type()
    if kind in ['BooleanField','IntegerField','SmallIntegerField','PositiveIntegerField']:
        return 'INT'
    if kind=='BigIntegerField':
        return 'BIGINT'
    if kind=='FloatField':
        return 'FLOAT'
    if kind=='DecimalField':
        return f'DECIMAL({field.max_digits},{field.decimal_places})'
    if kind=='DateTimeField':
        return 'DATETIME'
    if kind=='DateField':
        return 'DATE'
    if kind=='BinaryField':
        return 'VARBINARY'
    return 'VARCHAR'


@lru_cache(maxsize=300)
def compile_query(sql, selected=()):
    tree=sqlglot.parse_one(sql,read='tsql')
    if not isinstance(tree,(exp.Select,exp.Union)):
        raise ValueError('资料定义必须是SELECT查询。')
    if selected:
        tree=exp.select(*(exp.column(name.lower()) for name in dict.fromkeys(selected))).from_(tree.subquery('_requested'))
    tree=inline_functions(expand_views(tree))
    for node in list(tree.find_all(exp.Convert)):
        if node.args.get('style') is None and node.this.this!=exp.DType.IMAGE:
            node.replace(exp.Cast(this=node.expression.copy(),to=node.this.copy()))
    models={m.SOURCE_TABLE.lower():m for m in apps.get_models() if getattr(m,'SOURCE_SCHEMA',None)=='dye'}
    schema={};used={}
    for identifier in tree.find_all(exp.Identifier):
        identifier.set('this',identifier.this.lower())
    for column in tree.find_all(exp.Column):
        column.set('db',None);column.set('catalog',None)
    for table in tree.find_all(exp.Table):
        # 外部数据库不映射成本地同名表。
        if table.catalog or table.db not in ['', 'dye']:
            raise ValueError('原资料包含外部数据库来源：'+table.sql())
        model=models[table.name]
        used[table.name]=model
        schema[table.name]={old.lower():dtype(model._meta.get_field(field)) for old,field in model.SOURCE_FIELDS.items()}
        table.set('db',None)
    tree=qualify(tree,schema=schema,dialect='tsql')
    if selected:
        requested=tree.args['from_'].this.this
        if isinstance(requested,exp.Select) and not requested.args.get('distinct'):
            requested.set('expressions',[e for e in requested.expressions if e.alias_or_name.lower() in {s.lower() for s in selected}])
    tree=pushdown_projections(tree)
    tree=annotate_types(tree,schema=schema,dialect='tsql')
    def text_type(node):
        if isinstance(node,exp.Literal) and node.is_string:return True
        if isinstance(node,exp.Convert):return node.this.this in [exp.DType.VARCHAR,exp.DType.NVARCHAR,exp.DType.CHAR,exp.DType.NCHAR]
        if isinstance(node,exp.DPipe):return True
        return node.type is not None and node.type.this in [exp.DType.VARCHAR,exp.DType.NVARCHAR,exp.DType.CHAR,exp.DType.NCHAR,exp.DType.TEXT]
    def normalize(node):
        normalized=exp.Anonymous(this='NORMALIZE',expressions=[node.copy(),exp.Var(this='NFKC')])
        return exp.Upper(this=exp.Trim(this=normalized,position='TRAILING'))
    def numeric_type(node):
        return node.type is not None and node.type.this in [exp.DType.INT,exp.DType.BIGINT,exp.DType.SMALLINT,
            exp.DType.TINYINT,exp.DType.FLOAT,exp.DType.DOUBLE,exp.DType.DECIMAL]
    def to_numeric(node,target):
        text=exp.Case(ifs=[exp.If(this=exp.EQ(this=exp.Trim(this=node.copy()),expression=exp.Literal.string('')),
                                   true=exp.Literal.string('0'))],default=node.copy())
        return exp.Cast(this=text,to=target.type.copy())
    # TSQL的字符串+不是PostgreSQL数值+；空值继续通过||传播。
    for node in reversed(list(tree.walk(bfs=False))):
        if isinstance(node,exp.Add) and (text_type(node) or text_type(node.this) and text_type(node.expression)):
            node.replace(exp.DPipe(this=node.this.copy(),expression=node.expression.copy()))
        elif isinstance(node, (exp.EQ,exp.NEQ,exp.GT,exp.GTE,exp.LT,exp.LTE)) and text_type(node.this) and text_type(node.expression):
            node.set('this',normalize(node.this));node.set('expression',normalize(node.expression))
        elif isinstance(node,(exp.EQ,exp.NEQ,exp.GT,exp.GTE,exp.LT,exp.LTE)):
            if text_type(node.this) and numeric_type(node.expression):node.set('this',to_numeric(node.this,node.expression))
            elif numeric_type(node.this) and text_type(node.expression):node.set('expression',to_numeric(node.expression,node.this))
        elif isinstance(node,exp.In) and node.expressions and text_type(node.this):
            number=next((v for v in node.expressions if numeric_type(v)),None)
            if number is not None:node.set('this',to_numeric(node.this,number))
            else:
                node.set('this',normalize(node.this));node.set('expressions',[normalize(v) if text_type(v) else v for v in node.expressions])
        elif isinstance(node,exp.Like) and text_type(node.this):
            node.set('this',exp.Upper(this=node.this.copy()));node.set('expression',exp.Upper(this=node.expression.copy()))
        elif isinstance(node,exp.Coalesce) and node.args.get('is_null'):
            first=node.this
            others=[]
            for value in node.expressions:
                if text_type(first) and not text_type(value) and not isinstance(value,exp.Null):
                    value=exp.Cast(this=value.copy(),to=exp.DataType.build('VARCHAR'))
                elif not text_type(first) and isinstance(value,exp.Literal) and value.is_string and not value.this.strip():
                    value=exp.Literal.number(0)
                others.append(value)
            node.set('expressions',others)
        elif isinstance(node,exp.Convert) and node.this.this==exp.DType.IMAGE and isinstance(node.expression,exp.Null):
            node.replace(exp.Cast(this=exp.Null(),to=exp.DataType.build('BYTEA',dialect='postgres')))
        elif isinstance(node,exp.Union):
            for left,right in zip(node.this.selects,node.expression.selects):
                a=left.this if isinstance(left,exp.Alias) else left
                b=right.this if isinstance(right,exp.Alias) else right
                if numeric_type(a) and text_type(b):b.replace(to_numeric(b,a))
                elif numeric_type(b) and text_type(a):a.replace(to_numeric(a,b))
        elif isinstance(node,exp.Case):
            values=[branch.args['true'] for branch in node.args.get('ifs',[])]+[node.args.get('default')]
            target=next((v for v in values if v is not None and numeric_type(v)),None)
            if target is not None:
                for branch in node.args.get('ifs',[]):
                    if text_type(branch.args['true']):branch.set('true',to_numeric(branch.args['true'],target))
                default=node.args.get('default')
                if default is not None and text_type(default):node.set('default',to_numeric(default,target))
        elif isinstance(node,exp.Round) and node.args.get('decimals') is not None and node.this.type is not None and node.this.type.this in [exp.DType.FLOAT,exp.DType.DOUBLE]:
            node.set('this',exp.Cast(this=node.this.copy(),to=exp.DataType.build('DECIMAL')))
        elif isinstance(node,exp.CurrentTimestamp):
            node.replace(exp.AtTimeZone(this=node.copy(),zone=exp.Literal.string(settings.TIME_ZONE)))
        elif isinstance(node,(exp.DateAdd,exp.DateDiff)):
            for argument in (['this'] if isinstance(node,exp.DateAdd) else ['this','expression']):
                value=node.args.get(argument)
                if isinstance(value,exp.Literal) and not value.is_string and value.this=='0':
                    node.set(argument,exp.Cast(this=exp.Literal.string('1900-01-01'),to=exp.DataType.build('TIMESTAMP')))
    for select in tree.find_all(exp.Select):
        group=select.args.get('group')
        if group is not None:
            for original in list(group.expressions):
                if not text_type(original):continue
                for projection in select.expressions:
                    for node in list(projection.walk()):
                        if node==original and node.find_ancestor(exp.AggFunc) is None:
                            node.replace(exp.Min(this=node.copy()))
                original.replace(normalize(original))
        limit=select.args.get('limit')
        if limit is not None and limit.expression.name=='100' and limit.args.get('limit_options') is not None and limit.args['limit_options'].args.get('percent'):
            select.set('limit',None)
        if select.args.get('distinct'):
            expressions=[e.this if isinstance(e,exp.Alias) else e for e in select.expressions]
            if any(text_type(e) for e in expressions):
                select.set('distinct',exp.Distinct(on=exp.Tuple(expressions=[normalize(e) if text_type(e) else e.copy() for e in expressions])))
    columns=tree.named_selects
    return tree.sql(dialect='postgres'),used,columns


def execute(sql_text,query,selected=()):
    sql,models,columns=compile_query(sql_text,tuple(selected))
    ctes=[];parameters=[]
    quote=connection.ops.quote_name
    for name,model in models.items():
        scoped=active(query(model.__name__.removeprefix('SourceDye'),model._meta.app_label)).order_by()
        source_sql,source_params=scoped.values(*model.SOURCE_FIELDS.values()).query.sql_with_params()
        fields=[]
        field_parameters=[]
        for old,field in model.SOURCE_FIELDS.items():
            expression='_source.'+quote(field)
            if model._meta.get_field(field).get_internal_type()=='BooleanField':
                expression='CAST('+expression+' AS INTEGER)'
            elif model._meta.get_field(field).get_internal_type()=='DateTimeField':
                expression='timezone(%s,'+expression+')'
                field_parameters.append(settings.TIME_ZONE)
            fields.append(expression+' AS '+quote(old.lower()))
        ctes.append(quote(name)+' AS (SELECT '+','.join(fields)+' FROM ('+source_sql+') _source)')
        parameters.extend(field_parameters);parameters.extend(source_params)
    statement=('WITH '+','.join(ctes)+' ' if ctes else '')+sql.replace('%','%%')
    with connection.cursor() as cursor:
        cursor.execute(statement,parameters)
        names=[column[0] for column in cursor.description]
        result=[dict(zip(names,row)) for row in cursor.fetchall()]
    return result


def lookup(spec,filter_text,other_fields,query):
    code=spec.get('effective_key_field') or spec['KeyField']
    label=spec.get('effective_display_field') or spec['DisplayField']
    _,_,available=compile_query(original_query(spec))
    for field in [code,label,*other_fields]:
        if field.lower() not in available:raise KeyError(field)
    filter_text=varchar(filter_text,1000)
    if filter_text is None:
        return []  # 与已有接口一致：NULL动态命令无结果，见E104。
    remark_fields={'labelwarehouse':0,'labelremarks':1} if spec['LookupID'] in ['A026','B214'] else {}
    requested=[code,label,*[f for f in other_fields if f.lower() not in remark_fields]]
    if any(f.lower() in remark_fields for f in other_fields):requested.append('CheckNo')
    values=execute(original_query(spec),query,requested)
    result=[{'id':row[code.lower()],'text':row[label.lower()],**{f:label_remarks(remark_fields[f.lower()],row['checkno'],query)
             if f.lower() in remark_fields else row[f.lower()] for f in other_fields}} for row in values]
    if filter_text.rstrip(' '):
        pattern='%'+unicodedata.normalize('NFKC',filter_text)+'%'
        result=[row for row in result if any(sql_like(None if row[field] is None else unicodedata.normalize('NFKC',str(row[field])),pattern) for field in ['id','text'])]
    return result


def label_remarks(kind,check_no,query):
    """fn_A_GetRemarks：标签字典在订单备注中匹配，仓库无匹配时保留原客户分支。"""
    from .source_business_updates import matching
    from .source_stock_services import raw
    from .source_trial_steps import equal
    customer=remarks=None
    for color in matching(query('OrderColor','erp_sales'),CheckNo=varchar(check_no,50)).order_by('pk'):
        for main in list(matching(query('OrderMain','erp_sales'),SheetSeries=raw(color,'SheetSeries')).order_by('pk')) or [None]:
            customer=None if main is None else varchar(raw(main,'CustomerID'),20)
            remarks=varchar(raw(color,'ColorRemarks'),500)
    values=[]
    for item in matching(query('PFieldValid','erp_base'),FieldType='LabelWareHouse' if kind==0 else 'LabelRemarks').order_by('pk'):
        name=raw(item,'Name')
        if name is not None and remarks is not None and name.upper() in remarks.upper():values.append(name)
    result=varchar(''.join(values),500) if values else None
    return ('东莞' if equal(customer,'000') else '高州' if equal(customer,'004') else '') if kind==0 and (result is None or equal(result,'')) else result
