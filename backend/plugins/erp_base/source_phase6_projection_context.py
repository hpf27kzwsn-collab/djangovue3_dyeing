"""查询试算沿原入口的 Master/RelaFieldNames 取父子行，使用本次请求的授权 reader。"""
import re
from . import source_phase6_entries as entries
from .source_trial_steps import equal
from .source_phase6_projection_overrides import PRINT_PARENTS

CHILD=re.compile(r'(sum|count)\s*\(\s*Child\(([^)]+)\)\.\[([^]]+)\]\s*\)',re.I)

def cell(result,row,name):
    positions=[i for i,c in enumerate(result['columns']) if c['name'].lower()==name.lower()]
    if len(positions)!=1:raise ValueError('来源字段'+name+'对应投影位置'+str(positions))
    return row[positions[0]]

class ProjectionContext:
    def __init__(self,result,reader,parameters,include_retained):
        self.result=result;self.reader=reader;self.parameters=parameters;self.include_retained=include_retained;self.cache={}

    def query(self,name):
        if name not in self.cache:
            support=entries.query_support()[name]
            if support['query_state'] not in ['executed_empty_fixture','reconstructed_missing_projection']:
                raise ValueError('父子来源查询仍有差异或暂缓：'+name)
            if entries.definition(name)['finance'] or name.startswith(('ImpairmentPayouts','FAR','FAP','FMoney')):
                raise ValueError('财务来源暂缓：'+name)
            required=entries.query_parameters(name)
            if any(key not in self.parameters for key in required):raise ValueError('父子来源查询缺参数：'+name)
            self.cache[name]=entries.run(name,{k:self.parameters[k] for k in required},self.reader,load_records=True,include_retained=self.include_retained)
        return self.cache[name]

    def relation(self,child,parent):
        if PRINT_PARENTS.get(child)==parent:return [('SheetSeries','SheetSeries')]
        table=entries.definition(child)['table']
        if table['MasterDataTableName']!=parent:raise ValueError('原配置没有此明确父子关系：'+parent+'/'+child)
        left=(table['RelaFieldNames'] or '').split(';');right=(table['MasterRelaFieldNames'] or '').split(';')
        if not all(left+right) or len(left)!=len(right):raise ValueError('原父子连接字段不完整：'+child)
        return list(zip(left,right))

    def parent(self,row,name):
        child=self.result['entry'];parent=PRINT_PARENTS.get(child,entries.definition(child)['table']['MasterDataTableName'])
        if not parent:raise ValueError('原入口未声明父入口：'+child)
        keys=self.relation(child,parent);data=self.query(parent)
        matches=[r for r in data['rows'] if all(cell(self.result,row,a) is not None and equal(cell(self.result,row,a),cell(data,r,b)) for a,b in keys)]
        if len(matches)!=1:raise ValueError('父查询匹配行数'+str(len(matches))+'；保留全部候选，不选第一行')
        return cell(data,matches[0],name)

    def aggregate(self,row,operation,relation,name):
        parent=self.result['entry'];prefix=parent+'_'
        if not relation.startswith(prefix):raise ValueError('子关系前缀与当前入口不同：'+relation)
        child=relation[len(prefix):]
        if child not in entries.entries():raise ValueError('缺子入口：'+child)
        keys=self.relation(child,parent);data=self.query(child)
        matches=[r for r in data['rows'] if all(cell(self.result,row,b) is not None and equal(cell(self.result,row,b),cell(data,r,a)) for a,b in keys)]
        values=[cell(data,r,name) for r in matches if cell(data,r,name) is not None]
        return len(values) if operation.lower()=='count' else sum(values) if values else None
