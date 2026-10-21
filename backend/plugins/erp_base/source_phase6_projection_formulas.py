"""查询公式另列试算列；原投影、重名列、重复行和异常行均保留。"""
from sqlglot import exp
from sqlglot.errors import ParseError
from .source_phase6_formula_runtime import tree,scalar
from .source_phase6_projection_context import CHILD
from .source_phase6_projection_overrides import expression


def calculate(result,fields,context=None):
    original=[c['name'].lower() for c in result['columns']]
    formulas=[f for f in fields if f['Express']]
    plans=[];resolutions=[]
    for field in formulas:
        text,resolution=expression(result.get('entry',''),field)
        if resolution:resolutions.append({'field':field['FieldName'],'original_expression':field['Express'],'implemented_expression':text,'basis':resolution})
        reason=None;parsed=None;aggregates={}
        def aggregate(match):
            key='_projection_child_'+str(len(aggregates));aggregates[key]=match.groups();return '['+key+']'
        text=CHILD.sub(aggregate,text)
        try:
            parsed=tree(text)
            if (aggregates or any(n.table for n in parsed.find_all(exp.Column))) and context is None:reason='此公式需要父子行上下文，当前查询结果不提供明确关系'
            elif any(n.table and n.table.lower()!='parent' for n in parsed.find_all(exp.Column)):reason='未对应此跨入口字段前缀'
            elif any(isinstance(n,exp.Anonymous) for n in parsed.walk()):reason='未登记查询计算函数'
        except ParseError as error:reason='原表达式不能解析：'+str(error)
        plans.append((field,parsed,reason,aggregates))
    rows=[list(r) for r in result['rows']];columns=list(result['columns']);issues=[];counts={}
    computed=[{} for _ in rows];failed=[set() for _ in rows];remaining=list(plans)
    while remaining:
        names={f['FieldName'].lower() for f,_,_,_ in remaining}
        ready=[v for v in remaining if v[2] or not ({n.name.lower() for n in v[1].find_all(exp.Column) if not n.table}-{v[0]['FieldName'].lower()}).intersection(names)]
        if not ready:
            ready=[(f,p,'公式互相引用，查询试算不猜测输入方向',a) for f,p,_,a in remaining];remaining=[]
        for field,parsed,reason,aggregates in ready:
            remaining=[v for v in remaining if v[0] is not field]
            target=field['FieldName'];position=len(columns)
            columns.append({'key':'c'+str(position),'name':target+'__formula','title':(field['FieldCaption'] or target)+'（试算）','encoding':None})
            passed=0
            for index,row in enumerate(rows):
                def read(table,name):
                    if name in aggregates:return context.aggregate(row,*aggregates[name])
                    if table.lower()=='parent':return context.parent(row,name)
                    key=name.lower()
                    if key in failed[index] and key!=target.lower():raise ValueError('依赖公式'+name+'未能计算，不能改用原列冒充本次结果')
                    if key in computed[index] and key!=target.lower():return computed[index][key]
                    positions=[i for i,n in enumerate(original) if n==key]
                    if len(positions)!=1:raise ValueError('来源字段'+name+'对应投影位置'+str(positions))
                    return row[positions[0]]
                issue=reason
                if issue is None:
                    try:value=scalar(parsed,read)
                    except (ArithmeticError,TypeError,ValueError,KeyError,AttributeError) as error:issue=str(error)
                if issue is not None:
                    failed[index].add(target.lower())
                    row.append(None);issues.append({'row':index+1,'field':target,'reason':issue})
                else:
                    row.append(value);computed[index][target.lower()]=value;passed+=1
            counts[target]={'calculated_rows':passed,'unresolved_rows':len(rows)-passed,'expression':field['Express'],'configuration_issue':reason}
    return {**result,'columns':columns,'rows':rows,'formula_calculations':counts,'formula_issues':issues,'formula_source_resolutions':resolutions,
        'formula_note':'试算列单独追加，不覆盖原列或写回数据；缺来源、重名来源及除零逐行列明。'}
