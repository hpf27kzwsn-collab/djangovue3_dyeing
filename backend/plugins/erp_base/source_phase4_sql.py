"""固定原查询的临时表按依赖生成CTE，避免多次内嵌相同统计。"""
from sqlglot import exp,parse_one
from .source_phase3_sql import bind
from .source_static_lookup import execute
from .source_quality_reports import rows


def query(sql,parameters,definitions=None,reader=rows):
    definitions=definitions or {};built={}
    def visit(tree):
        for table in list(tree.find_all(exp.Table)):
            key=table.name.lower().lstrip('#')
            if key not in definitions:continue
            if key not in built:
                value=parse_one(definitions[key],read='tsql');visit(value);built[key]=value
            table.set('this',exp.to_identifier('_p4_'+key));table.set('db',None);table.set('catalog',None)
            if not table.args.get('alias'):table.set('alias',exp.TableAlias(this=exp.to_identifier(key)))
        for column in tree.find_all(exp.Column):
            if column.table.lower().lstrip('#') in definitions:column.set('table',exp.to_identifier(column.table.lower().lstrip('#')));column.set('db',None)
    tree=parse_one(sql,read='tsql');visit(tree)
    original=tree.args.get('with_');ctes=[exp.CTE(this=value,alias=exp.TableAlias(this=exp.to_identifier('_p4_'+key))) for key,value in built.items()]
    if original:ctes.extend(original.expressions)
    if ctes:tree.set('with_',exp.With(expressions=ctes))
    return execute(bind(tree.sql(dialect='tsql'),parameters),reader)
