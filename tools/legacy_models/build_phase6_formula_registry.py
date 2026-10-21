"""将固定清单内能确定物理字段及明确主从路径的公式编译成保存登记。"""
import os,sys,json,re
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','application.settings')
import django
django.setup()
from django.apps import apps
from sqlglot import exp,parse_one
from sqlglot.errors import ParseError
from plugins.erp_base.source_ownership import OWNERS
from plugins.erp_base.source_entry_registry import ENTRY_RULES
from plugins.erp_base.source_phase6_formula_links import RAW_LINKS


def paths(label,target,trail=()):
    if label==target:return [[]]
    if label in trail:return []
    owner_rules=OWNERS.get(label,[])
    if apps.get_model(label).SOURCE_TABLE=='RecordDefect':owner_rules=apps.get_model(label).SOURCE_RELATIONS
    return [[r['field'],*path] for r in owner_rules for path in paths(r['target'],target,(*trail,label))]


def input_source(label,name,parent):
    result=[]
    for model in apps.get_models():
        if not hasattr(model,'SOURCE_FIELDS'):continue
        names={n.lower():n for n in model.SOURCE_FIELDS}
        if name.lower() not in names:continue
        for path in paths(label,model._meta.label):
            if parent and not path:continue
            result.append({'model':model._meta.label,'path':path,'field':names[name.lower()]})
    if not result:
        source=apps.get_model(label)
        if source.SOURCE_TABLE in RAW_LINKS:
            table,keys=RAW_LINKS[source.SOURCE_TABLE]
            target=next(m for m in apps.get_models() if getattr(m,'SOURCE_TABLE',None)==table)
            names={n.lower():n for n in target.SOURCE_FIELDS}
            if name.lower() in names:return {'model':target._meta.label,'path':['raw_parent'],'field':names[name.lower()]}
        raise ValueError('缺物理来源：'+('parent.' if parent else '')+name)
    shortest=min(len(v['path']) for v in result)
    result=[r for r in result if len(r['path'])==shortest]
    if len(result)!=1:raise ValueError('来源路径不唯一：'+name)
    return result[0]


def compile_rule(row,target):
    model=apps.get_model(target['model']);field=row['field'];original=row['expression']
    if model.SOURCE_FIELDS[field] in model.SOURCE_IDENTITIES:
        raise ValueError('原业务身份由编号/来源服务维护；原公式仅试算，不在普通修改中改号')
    if original=='yyyy-MM-dd':raise ValueError('原Express是日期格式串；保留日期录入，不将格式串当日期算式')
    # 已证实的原缺字来源，采用实际原表同义字段；原文不改。
    aliases={('JobSheetQuery','OriSourceJobNoTemp'):'OriSourceJobNo2',('PrintJobSheet','OriSourceJobNoTemp'):'OriSourceJobNo',
        ('SaleJobSheet','OriSourceJobNoTemp'):'OriSourceJobNo',('TwiJobSheet','OriSourceJobNoTemp'):'OriSourceJobNo'}
    aggregates={}
    def aggregate(match):
        operation,relation,column=match.groups()
        names={r:label for label,entries in ENTRY_RULES.items() for r in entries if r.lower()==relation.lower()}
        candidates=[]
        for label,entries in ENTRY_RULES.items():
            for entry in entries:
                if relation.lower()!=entry.lower() and not relation.lower().endswith('_'+entry.lower()):continue
                child=apps.get_model(label)
                lookup={n.lower():n for n in child.SOURCE_FIELDS}
                if column.lower() in lookup:
                    for path in paths(label,model._meta.label):
                        if path:candidates.append({'model':label,'path':path,'field':lookup[column.lower()],'operation':operation.lower()})
        if not candidates:
            for table,(parent,keys) in RAW_LINKS.items():
                if parent!=model.SOURCE_TABLE:continue
                child=next(m for m in apps.get_models() if getattr(m,'SOURCE_TABLE',None)==table)
                if relation.lower().endswith('_'+table.lower()) and column in child.SOURCE_FIELDS:
                    candidates.append({'model':child._meta.label,'path':[],'keys':keys,'field':column,'operation':operation.lower()})
        if not candidates and relation=='PrintColorSeparateDetail_PrintColorSeparateRecord' and column=='RollNo':
            child=apps.get_model('erp_sampling.SourceDyePrintColorSeparateRecord')
            candidates.append({'model':child._meta.label,'path':['source_parent_1'],'field':None,'operation':'count'}) # 原查询明确投影1 AS RollNo。
        if len(candidates)!=1:raise ValueError('子来源无法唯一对应：'+relation+'.'+column+'，路径数'+str(len(candidates)))
        key='_child'+str(len(aggregates));aggregates[key]=candidates[0];return '['+key+']'
    text=re.sub(r'(sum|count)\s*\(\s*Child\(([^)]+)\)\.\[([^]]+)\]\s*\)',aggregate,original,flags=re.I)
    parsed=parse_one(text,read='tsql');inputs={}
    for node in parsed.find_all(exp.Column):
        name=node.name
        if name in aggregates:continue
        if node.table and node.table.lower()!='parent':raise ValueError('未确定连接投影：'+node.sql())
        actual=aliases.get((row['entry'],name),name)
        if actual==row['entry']+'.'+field:raise ValueError('原入口自引用占位，保留录入值')
        inputs[(node.table+'.' if node.table else '')+name]=input_source(model._meta.label,actual,node.table.lower()=='parent')
    allowed=(exp.Column,exp.Identifier,exp.Literal,exp.Null,exp.Boolean,exp.Paren,exp.Neg,exp.If,exp.Coalesce,exp.Substring,
             exp.Not,exp.In,exp.And,exp.Or,exp.Add,exp.Sub,exp.Mul,exp.Div,exp.EQ,exp.NEQ,exp.GT,exp.GTE,exp.LT,exp.LTE)
    unsupported={type(n).__name__ for n in parsed.walk() if not isinstance(n,allowed)}
    if unsupported:raise ValueError('尚未编译节点：'+','.join(sorted(unsupported)))
    if any(v['field']==field and not v['path'] and key!='OriSourceJobNoTemp' for key,v in inputs.items()):raise ValueError('原公式自引用，保留明确输入')
    return {'original_expression':original,'compiled_expression':text,'inputs':inputs,'aggregates':aggregates,
        'generate_time':row['generate_time'],'create_only':field in model.SOURCE_KEY or field=='Password' or field=='NeedQty' and not inputs,
        'ancestor_models':sorted({v['model'] for v in inputs.values() if v['path']}),
        'basis':'原字段/原表达式；保存时机与明确外键路径为本项目实现，旧客户端完整时序单列差异'}


def main():
    baseline=json.loads((ROOT/'docs/erp-phase6-six-groups-baseline-20261017.json').read_text(encoding='utf8'))
    registry={};outcomes=[]
    for row in baseline['groups']['1']+baseline['groups']['2']:
        results=[]
        for target in row['targets']:
            if not target['physical_field']:continue
            manual={('AddStuffWeight','ClothQtyKg'):'原自引用占位；保存明确录入的胚重，不生成另一份值。',
                    ('MoveShiftBill','BeginTime'):'日期格式不是计算式；保留录入日期及时间，不截去时分秒。',
                    ('MoveShiftBill','DayEnd'):'日期格式不是计算式；保留录入日期及时间，不截去时分秒。'}
            if (row['entry'],row['field']) in manual:
                results.append({'model':target['model'],'state':'explicit_manual_input','reason':manual[row['entry'],row['field']]});continue
            if (row['entry'],row['field'])==('qry_QuoteRelaRecipe','Remarks'):
                results.append({'model':target['model'],'state':'query_projection_only','reason':'原Kind=Query，UpdateSQL及TableName均为空；按原父工卡备注查询投影，不向配方原表写回。'});continue
            if target['dedicated_save_path']:
                results.append({'model':target['model'],'state':'existing_auto_service','reason':target['dedicated_save_path']});continue
            try:spec=compile_rule(row,target)
            except (ValueError,ParseError) as error:
                results.append({'model':target['model'],'state':'explicit_difference','reason':str(error)});continue
            registry.setdefault(target['model'],{}).setdefault(row['entry'],{})[row['field']]=spec
            results.append({'model':target['model'],'state':'compiled_save_formula','reason':spec['basis']})
        outcomes.append({'id':row['id'],'entry':row['entry'],'field':row['field'],'results':results})
    data={'rules':registry,'outcomes':outcomes,'counts':dict(Counter(r['state'] for v in outcomes for r in v['results']))}
    (ROOT/'backend/plugins/erp_base/source_phase6_formula_registry.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(data['counts'])
    for v in outcomes:
        for r in v['results']:
            if r['state']=='explicit_difference':print(v['entry'],v['field'],r['reason'])

if __name__=='__main__':main()
