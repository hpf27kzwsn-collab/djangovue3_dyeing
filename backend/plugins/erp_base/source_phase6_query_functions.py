"""旧界面投影复用已核验的Python标量服务，不建立SQL Server兼容存储函数。"""
import json
from sqlglot import exp,parse_one
from .business import FactsEncoder
from .source_static_lookup import execute_table,expand_views

FUNCTIONS={
    'fn_concatjobatte':('fn_ConcatJobAtte',['jobsheetno','ischarge'],'VARCHAR'),
    'fn_jobattelect':('fn_JobAttelect',['jobseries'],'VARCHAR'),
    'fn_jobassign':('fn_JobAssign',['jobseries'],'VARCHAR'),
    'fn_getpapertubebyjobno':('fn_GetPaperTubeByJobNo',['jobsheetno'],'DOUBLE'),
    'fn_gettubeweightbyjobno':('fn_GetTubeWeightByJobNo',['jobsheetno'],'DOUBLE'),
    'fn_get_jiaodai':('fn_Get_JiaoDai',['jobsheetno'],'DOUBLE'),
    'fn_concatweightkg':('fn_ConcatWeightKg',['jobsheetno'],'VARCHAR'),
    'fn_getdyestuffdosage':('dosage',['color','kind'],'DOUBLE'),
    'fn_a_getremarks':('label_remarks',['kind','check'],'VARCHAR'),
    'getrecorddefect':('GetRecordDefect',['barcode'],'VARCHAR'),
    'fn_concatbusinessunitid':('unit_ids',['employee'],'VARCHAR'),
    'fn_concatbusinessunitname':('unit_names',['employee'],'VARCHAR'),
    'get_number':('GET_NUMBER',['value'],'VARCHAR'),
    'fn_rkl':('limit',['customer','at'],'DOUBLE'),
    'fn_expandrange':('fn_ExpandRange',['value'],'VARCHAR'),
}


def calculate(name,values,reader):
    function,keys,_=FUNCTIONS[name];p=dict(zip(keys,values))
    if function in ['dosage','label_remarks']:
        from . import source_phase2_functions
        return getattr(source_phase2_functions,function)(*values,query=reader)
    if function in ['unit_ids','unit_names']:
        from .source_foundation import business_units
        return business_units(values[0],reader)[function]
    if function=='GET_NUMBER':
        from .source_foundation_functions import extract
        return extract(values[0],'GET_NUMBER')
    if function=='fn_ExpandRange':
        from .source_foundation_scalars import expand_range
        return expand_range(values[0])
    if function=='limit':
        from .source_phase2_limits import limit
        return limit(*values,query=reader)
    if function=='GetRecordDefect':
        from .source_phase5_functions import calculate as service
    else:
        from .source_phase4_functions import calculate as service
    return service(function,p,reader)['rows'][0]['result']


def prepare(sql,reader,include_retained):
    tree=expand_views(parse_one(sql,read='tsql'));evaluated=[]
    # 每个原调用按本查询实际参数组合计算；只缓存相同调用，不去重查询结果。
    for node in list(tree.find_all(exp.Dot)):
        call=node.expression
        if not isinstance(call,exp.Anonymous) or node.this.name.lower()!='dye' or call.name.lower() not in FUNCTIONS:continue
        name=call.name.lower();args=call.expressions;select=node.find_ancestor(exp.Select)
        arguments=select.copy()
        arguments.set('expressions',[exp.alias_(arg.copy(),'_arg'+str(i),quoted=True) for i,arg in enumerate(args)])
        for key in ['group','having','order','limit']:arguments.set(key,None)
        arguments.set('distinct',None)
        if node.find_ancestor(exp.Where) is not None:
            # WHERE中的函数先从同一FROM/JOIN取参数，再保留原WHERE作最终筛选。
            # 这样相关子查询的父别名不会泄入独立参数查询，也不会调用尚未替换的自身。
            arguments.set('where',None)
        rows=execute_table(arguments.sql(dialect='tsql'),reader,include_retained=include_retained)['rows']
        seen=set();branches=[]
        for values in rows:
            key=json.dumps(values,cls=FactsEncoder,ensure_ascii=False)
            if key in seen:continue
            seen.add(key);value=calculate(name,values,reader)
            comparisons=[exp.NullSafeEQ(this=arg.copy(),expression=exp.convert(v)) for arg,v in zip(args,values)]
            branches.append(exp.If(this=exp.and_(*comparisons),true=exp.convert(value)))
            evaluated.append({'function':FUNCTIONS[name][0],'arguments':values,'result':value})
        expression=exp.Case(ifs=branches,default=exp.Null()) if branches else exp.Null()
        node.replace(exp.Cast(this=expression,to=exp.DataType.build(FUNCTIONS[name][2])))
    return tree.sql(dialect='tsql'),evaluated
