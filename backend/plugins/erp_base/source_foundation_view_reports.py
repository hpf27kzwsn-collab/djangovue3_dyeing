"""第一阶段原视图只读服务；查询在当前项目数据及权限范围内执行。"""
from sqlglot import exp, parse_one
from .source_static_lookup import execute, compile_query
from .source_quality_reports import rows
from .source_package_labels import varchar

NAMES=['A_GrayID','CureDyeByBill','CureDyeByBill_LX','MaxSavePlease','s_vwColorDepth','s_vwCustomer',
       'v_App_Customer','v_APP_EmployeeDevice','v_Customer','v_DyePhase','v_DyeWorkQty_Day','V_GrayToProduct',
       'v_KQ_CType','v_KQ_InRecord','v_KQ_OutRecord','v_PatQuery','V_Stuff','vw_DyeWorkQtyQuer','vw_ZHENZHIYUNFEITJ1','sp_app_QueryEmployees']
QUERIES={'sp_app_QueryEmployees':"SELECT EmpID,Name,Mobile,MFLevel,MFGiveOut,DeptID,IsOut,BusinessUnitID,Password,NameE,LoginName,CustomerID,IsCustomer,ISNULL(EmpGroup,'') AS EmpGroup FROM dye.h_Employee"}


def statement(name,filters):
    sql=QUERIES.get(name,'SELECT * FROM dye.'+name)
    _,_,fields=compile_query(sql)
    tree=exp.select('*').from_(parse_one(sql,read='tsql').subquery('_original'))
    for condition in filters:
        name=condition['field'].lower()
        if name not in fields:raise KeyError(condition['field'])
        column=exp.column(name);operator=condition['operator'];value=condition['value']
        if operator=='isnull':
            predicate=exp.Is(this=column,expression=exp.Null())
            if not value:predicate=exp.Not(this=predicate)
        elif operator=='in':
            predicate=exp.In(this=column,expressions=[exp.convert(v) for v in value])
        else:
            types={'eq':exp.EQ,'gt':exp.GT,'gte':exp.GTE,'lt':exp.LT,'lte':exp.LTE,'ne':exp.NEQ}
            predicate=types[operator](this=column,expression=exp.convert(value))
        tree=tree.where(predicate)
    return tree.sql(dialect='tsql')


def report(name,filters=(),query=rows):
    if name not in NAMES:raise KeyError(name)
    result=execute(statement(name,filters),query)
    return {'report':name,'rows':result,'notes':['使用原视图当前定义的字段与连接；原文、移植差异和核验范围见第一阶段实施记录。']}


def work_quantity_count(years,employee,query=rows):
    years,employee=varchar(years,7),varchar(employee,10)
    if employee is None or years is None:return {'report':'fn_GetWorkQtyCount','rows':[{'result':None}],'candidate_rows':[]}
    candidates=execute(statement('v_DPWorkQtyCount',[{'field':'YEARS','operator':'eq','value':years}]),query)
    # 原@EmpID=@EmpID没有过滤员工，不能擅自改为EmpID=@EmpID。
    chosen=candidates[-1] if candidates else None
    result=None if chosen is None else float(chosen['summoney'] or 0)
    return {'report':'fn_GetWorkQtyCount','rows':[{'result':result}],'candidate_rows':candidates,
        'notes':['按原函数保留员工参数自比较；非NULL员工查询整月全部员工/班组来源，最后返回行覆盖前值。原查询无排序，单值存在顺序差异。']}
