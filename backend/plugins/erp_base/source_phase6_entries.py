"""旧入口的原配置、查询投影及打印取数。原行和重名投影按位置保存。"""
import gzip
import base64
import json
from functools import lru_cache
from pathlib import Path
from sqlglot import exp,parse,parse_one
from django.core.exceptions import ValidationError
from .source_entry_registry import ENTRY_RULES
from .source_phase3_sql import bind
from .source_phase6_reconstructions import differences


@lru_cache(maxsize=1)
def catalog():
    return json.loads(gzip.decompress(Path(__file__).with_name('source_phase6_catalog.json.gz').read_bytes()))


@lru_cache(maxsize=1)
def query_support():
    return json.loads(Path(__file__).with_name('source_phase6_query_support.json').read_text(encoding='utf8'))


@lru_cache(maxsize=1)
def hook_support():
    return json.loads(Path(__file__).with_name('source_phase6_hook_manifest.json').read_text(encoding='utf8'))


@lru_cache(maxsize=1)
def entries():
    return {row['table']['DataTableName']:row for row in catalog()['entries']}


@lru_cache(maxsize=1)
def bindings():
    result={name:[] for name in entries()}
    for model,rules in ENTRY_RULES.items():
        for name in rules:result[name].append(model)
    return result


def definition(name):
    if name not in entries():raise ValidationError({'entry':'没有此旧入口。'})
    return entries()[name]


def summaries():
    return [{'name':name,'title':r['table']['Alias'],'kind':r['table']['Kind'],
        'module':r['table']['ModuleName'],'finance':r['finance'],'models':bindings()[name],
        'query_state':query_support()[name]['query_state'],'field_count':len(r['fields'])} for name,r in entries().items()]


def tree_for(name):
    from .source_phase6_query_overrides import replacement
    row=definition(name)
    if row['finance']:raise ValidationError({'entry':'此入口为独立财务，本期暂缓。原配置保留。'})
    sql=replacement(name) or row['table']['SQL']
    # 此原入口把AND与数字粘连，原文保留在目录；明确修正这一处语法。
    if name=='JobSheetCombine':sql=sql.replace('and1=2','and 1=2')
    if name=='JobSheetPrintList1':sql=sql.replace("'-'+ ProcessID","'-'+ CAST(ProcessID AS VARCHAR(MAX))")
    # 原装箱汇总在内层把所属单据写成空串；按目录SheetSeries父子键改为明确必填参数。
    if name=='ProdLoadingDetail2':sql=sql.replace("WHERE SheetSeries=''","WHERE SheetSeries=@SheetSeries")
    # 此日期标签明确要求数字月份；英文月份名不能再转整数。原目录 SQL 保留。
    if name=='ProdOut':sql=sql.replace('CONVERT(INT,DATENAME(MONTH,po.SheetDate))','DATEPART(MONTH,po.SheetDate)')
    trees=[tree for tree in parse(sql,read='tsql') if tree is not None and not isinstance(tree,exp.Semicolon)]
    if len(trees)!=1 or not isinstance(trees[0],(exp.Select,exp.Union)):
        raise ValidationError({'entry':'此旧入口使用多语句/临时表，尚未作为单SELECT入口移植；原配置及原表仍可查阅。'})
    tree=trees[0]
    # 最新表增加同名字段后原未限定投影歧义；按本入口明细/汇总来源明确取数。
    aliases={'ArrivalNotice':{'prodid':'OrderColor'},'dyeWorkQty':{'customerid':'h','empid':'h_Employee'},
        'QCJobList':{'kg':'cnt','payard':'cnt'},'qry_CraftPreCheckOrder':{'checkno':'oc','prodid':'oc'}}
    for column in tree.find_all(exp.Column):
        if column.find_ancestor(exp.Select) is tree and not column.table and column.name.lower() in aliases.get(name,{}):
            column.set('table',exp.to_identifier(aliases[name][column.name.lower()]))
        if name=='qry_CraftCheckedJobSheet' and column.table.lower()=='standcraftjobno' and column.name.lower()=='ordersheetno':
            column.set('table',exp.to_identifier('JobSheet'))
    if row['table'].get('OrderBy'):
        # 旧平台把尾部GROUP BY也存入OrderBy；它是完整原查询的一部分。
        suffix=parse_one('SELECT 1 '+row['table']['OrderBy'],read='tsql')
        for key in ['group','order']:
            if suffix.args.get(key) is not None:tree.set(key,suffix.args[key].copy())
    from .source_phase6_reconstructions import adapt
    from .source_phase6_periods import adapt as adapt_period
    return adapt_period(name,adapt(name, tree))


def query_parameters(name):
    return sorted({node.name for node in tree_for(name).find_all(exp.Parameter)},key=str.lower)


def prepare(name,parameters,load_records=False):
    tree=tree_for(name)
    expected={node.name.lower() for node in tree.find_all(exp.Parameter)}
    provided={k.lower():v for k,v in parameters.items()}
    from .source_phase6_periods import parameters as period_parameters
    provided=period_parameters(name,provided)
    from .source_phase6_reconstructions import validate_parameters
    validate_parameters(name, provided)
    if set(provided)!=expected:
        raise ValidationError({'parameters':'缺少参数：'+str(sorted(expected-set(provided)))+'；多余参数：'+str(sorted(set(provided)-expected))})
    if load_records:
        # 客户端用于取得列结构的外层1=2只在明确加载记录时移除；业务筛选及子查询保持原样。
        def roots(node):
            return [node] if isinstance(node,exp.Select) else roots(node.left)+roots(node.right)
        branches=roots(tree)
        if name in ['jm_Specifications','sm_Specifications','qry_Static_EmpDetail','qry_CraftCheckedJobSheet']:
            branches=list(tree.find_all(exp.Select))
        for branch in branches:
            where=branch.args.get('where')
            if where is not None:
                for node in list(where.find_all(exp.EQ,exp.GT)):
                    if node.find_ancestor(exp.Select) is branch and node.this==exp.Literal.number(1) and node.expression==exp.Literal.number(2):
                        node.replace(exp.true())
    return bind(tree.sql(dialect='tsql'),provided)


def run(name,parameters,reader,load_records=False,include_retained=True,additional_projection=()):
    from .source_phase6_periods import description as period_description
    from .source_static_lookup import execute_table
    from .source_phase6_query_functions import prepare as prepare_functions
    if not include_retained:
        from .source_execution_state import active
        original_reader=reader
        reader=lambda name,module:active(original_reader(name,module))
    sql=prepare(name,parameters,load_records)
    if additional_projection:
        tree=parse_one(sql,read='tsql')
        tree=tree.select(*(parse_one(value,read='tsql') for value in additional_projection))
        sql=tree.sql(dialect='tsql')
    sql,evaluated=prepare_functions(sql,reader,include_retained)
    table=execute_table(sql,reader,include_retained=include_retained)
    fields=definition(name)['fields']
    labels={r['FieldName'].lower():r['FieldCaption'] or r['FieldName'] for r in fields}
    binary={i for row in table['rows'] for i,value in enumerate(row) if isinstance(value,(bytes,bytearray,memoryview))}
    rows=[['base64:'+base64.b64encode(bytes(value)).decode('ascii') if isinstance(value,(bytes,bytearray,memoryview)) else value for value in row] for row in table['rows']]
    return {'entry':name,'title':definition(name)['table']['Alias'],
        'columns':[{'key':'c'+str(i),'name':col,'title':labels.get(col.lower(),col),'encoding':'base64' if i in binary else None} for i,col in enumerate(table['columns'])],
        'rows':rows,'count':len(rows),'include_retained':include_retained,'load_records':load_records,
        'function_values':evaluated,'period':period_description(name,parameters),
        'additional_projection':list(additional_projection),
        'reconstruction':differences(name)}


def reader(request):
    from .reports import Reader
    from django.apps import apps
    scoped=Reader(request)
    def source(name,module):
        model=apps.get_model(module+'.SourceDye'+name)
        return scoped.source(model,list(model.SOURCE_FIELDS.values()))
    return source


def detail(name):
    row=definition(name)
    return {**row,'models':bindings()[name],
        'write_bindings':[{'model':label,**ENTRY_RULES[label][name]['write_binding']} for label in bindings()[name]],
        'query_support':query_support()[name],'hook_support':hook_support().get(name,[]),
        'reports':[r for r in catalog()['reports'] if any(m['RptID']==r['RptID'] and m['FuncNo']==row['table']['ModuleNo'] for m in catalog()['report_menus'])]}
