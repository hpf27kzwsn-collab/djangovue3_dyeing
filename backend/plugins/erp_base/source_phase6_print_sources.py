"""原打印跨单头字段沿目录声明取数；不通过字段同名猜测关联。"""
from django.core.exceptions import ValidationError
from . import source_phase6_entries as entries
from .source_phase6_projection_context import ProjectionContext, cell
from .source_trial_steps import equal

PROJECTIONS={'GrayInWaste':('pc.NameC AS NameC',),'GrayOutWaste':('a.GrayKindID AS GrayKind',)}
PROJECTION_NOTES={'GrayInWaste':'原查询已关联pc客户表，补取pc.NameC供原客户全称标签使用；不改原连接与行数。',
                 'GrayOutWaste':'原GrayKind展示列缺失；明确按出库单头GrayKindID原胚纱类别代码分组，不猜测旧客户端类别显示名。',
                 'TwiJobSheet':'H006日期误绑定PrintJobSheet.SheetDate；两入口原表均为JobSheet，校样采用本行TwiJobSheet.SheetDate，不跨工卡借值。',
                 'h_Employeelit':'R154编号误绑定h_Employee.EmpID；两入口查询原员工表，校样采用本行h_Employeelit.EmpID，不另查同号员工。'}
LOCAL_BINDINGS={('TwiJobSheet','PrintJobSheet.SheetDate'):'SheetDate',
                ('h_Employeelit','h_Employee.EmpID'):'EmpID',
                ('GrayOutWaste','GrayInWaste.NameC'):'NameC'}
PROJECTION_NOTES['GrayOutWaste']+=' R015客户全称误绑GrayInWaste.NameC，采用当前出库查询已提供的pc.NameC，不跨入库借值。'
PROJECTION_NOTES['ProdLoadingDetail2']='R66-2按明确SheetSeries参数读取本装车单；原内层空串条件改为必填参数，未改分组和重复行计数。原DlvAddress选择器A009实为付款类型，仍按原配置取候选，未匹配的地址保留原文；尚未证明旧客户端的地址显示来源。'


def projections(entry):return PROJECTIONS.get(entry,())


def select_parent(report,result,key,null_key=False):
    """单头/客户页眉版式按明确范围打印，查询结果及其他单据不改写。"""
    scopes={'H004':('SheetSeries','父单流水号'),'K008':('SheetSeries','父单流水号'),'R015':('CustomerID','客户编码')}
    scopes.update({code:('SheetSeries','父单流水号') for code in ['R121','H008','H024','H015','H017','H018','H025','H029']})
    if report not in scopes:return result
    field,label=scopes[report]
    if key is None and not null_key:raise ValidationError({'print_key':'本原版式页眉属于同一'+label+'，请明确选择本次打印范围；NULL和空字符串可分别选用。'})
    rows=[r for r in result['rows'] if (cell(result,r,field) is None if null_key else equal(cell(result,r,field),key))]
    if null_key:key=None
    return {**result,'rows':rows,'count':len(rows),'print_selection':{'field':field,'label':label,'value':key,'input_rows':len(result['rows']),'selected_rows':len(rows)}}


def parent_path(entry, target):
    path=[];visited=set()
    while entry != target:
        if entry in visited:raise ValueError('原打印父关系循环：'+entry)
        visited.add(entry)
        parent=entries.definition(entry)['table']['MasterDataTableName']
        if not parent:raise ValueError('缺原打印父关系：'+entry+'/'+target)
        context=ProjectionContext({'entry':entry},None,{},True)
        keys=context.relation(entry,parent)
        path.append((entry,parent,keys));entry=parent
    return path


def binding_field(entry,member):
    return LOCAL_BINDINGS.get((entry,member),member[len(entry)+1:] if member.startswith(entry+'.') else member)


def source_issue(entry,member):
    from .source_phase6_rendering import projection_names,reference_available
    if (entry,member) in LOCAL_BINDINGS:
        return None if binding_field(entry,member).lower() in projection_names(entries.tree_for(entry)) else '缺本行打印字段：'+member
    target,field=member.rsplit('.',1)
    try:
        parent_path(entry,target)
        if entries.definition(target)['finance']:return '财务打印来源暂缓：'+member
        if entries.query_support()[target]['query_state']=='unresolved':return '原打印父查询暂缓：'+target
        projected=projection_names(entries.tree_for(target))
        if field.lower() not in projected and not reference_available(target,field,projected):return '原打印父投影缺字段：'+member
    except ValueError:return '缺跨表关联：'+member
    except (KeyError,ValidationError) as error:return str(error)
    return None


def attach(root,result,reader,parameters,include_retained):
    entry=result['entry']
    members=sorted({b.get('DataMember') for b in root.findall('.//DataBindings/*')
                    if not b.get('DataMember','').startswith(entry+'.') and (entry,b.get('DataMember')) not in LOCAL_BINDINGS})
    output={**result,'columns':list(result['columns']),'rows':[list(r) for r in result['rows']]}
    context=ProjectionContext(result,reader,parameters,include_retained)
    evidence=[]
    for member in members:
        target,field=member.rsplit('.',1);path=parent_path(entry,target)
        reference_resolutions=[]
        output['columns'].append({'name':member})
        for index,row in enumerate(result['rows']):
            data=result;values=row
            for child,parent,keys in path:
                parents=context.query(parent)
                if parent==target and field.lower() not in {c['name'].lower() for c in parents['columns']}:
                    from .source_phase6_rendering import resolve_reference_columns
                    parents=resolve_reference_columns(parents,[field],reader)
                    context.cache[parent]=parents
                if parent==target:reference_resolutions=parents.get('reference_resolutions',[])
                matches=[p for p in parents['rows'] if all(cell(data,values,a) is not None and equal(cell(data,values,a),cell(parents,p,b)) for a,b in keys)]
                if len(matches)!=1:
                    raise ValidationError({'print_source':f'第{index+1}行 {member}，父入口{parent} matched_rows={len(matches)}；原父单必须明确对应，全部候选保留，不取第一条，也不跳过该明细'})
                data=parents;values=matches[0]
            output['rows'][index].append(cell(data,values,field))
        evidence.append({'binding':member,'path':[p for _,p,_ in path],'rows':len(result['rows']),
                         'reference_resolutions':reference_resolutions})
    output['parent_source_resolutions']=evidence
    return output
