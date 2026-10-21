"""从明确的结构快照和逐表去向生成静态Django字段，不读取或修改旧数据库。"""
import argparse,ast,json,re,hashlib,runpy
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
extend_continuation_actions=runpy.run_path(str(ROOT/'tools/legacy_models/continuation_actions.py'))['extend']
extend_foundation_actions=runpy.run_path(str(ROOT/'tools/legacy_models/foundation_actions.py'))['extend']
MODULES=['erp_base','erp_sales','erp_purchase','erp_sampling','erp_production','erp_warehouse','erp_quality']

def identifier(name):
    words=re.sub(r'([a-z0-9])([A-Z])',r'\1_\2',name)
    return 'old_'+re.sub(r'\W','_',words.lower()).strip('_')

def model_name(schema,table):
    if (schema,table)==('dye','s_ManagerSQL-'):return 'SourceDyeSManagerSQLDash'
    return 'Source'+schema.title()+''.join(word[:1].upper()+word[1:] for word in re.split(r'[^\w]|_',table) if word)

def original_default(definition):
    value=definition
    while value.startswith('(') and value.endswith(')'):value=value[1:-1]
    if value.lower()=='getdate()':return ('now',None)
    if value.lower()=='newid()':return ('uuid',None)
    if value.startswith("'") and value.endswith("'"):return ('literal',value[1:-1].replace("''","'"))
    if re.fullmatch(r'-?\d+',value):return ('literal',int(value))
    raise ValueError('尚未明确翻译的原默认定义：'+definition)

def declaration(column,title):
    kind=column['data_type'];null=column['is_nullable']
    blank=null or kind in ['varchar','nvarchar','char','nchar','text','ntext','image','binary','varbinary']
    arguments=[repr(title),'null='+repr(null),'blank='+repr(blank)]
    if kind in ['varchar','nvarchar','char','nchar']:
        size=column['max_length']//2 if kind in ['nvarchar','nchar'] else column['max_length']
        if size==-1:field='TextField'
        else:field='CharField';arguments.append('max_length='+str(size))
    elif kind in ['text','ntext']:field='TextField'
    elif kind in ['decimal','numeric','money']:
        field='DecimalField';arguments.extend(['max_digits='+str(column['precision']),'decimal_places='+str(column['scale'])])
    elif kind in ['float','real']:field='FloatField'
    elif kind in ['tinyint','smallint','int']:field='IntegerField'
    elif kind=='bigint':field='BigIntegerField'
    elif kind=='bit':field='BooleanField'
    elif kind in ['datetime','datetime2','smalldatetime']:field='DateTimeField'
    elif kind=='date':field='DateField'
    elif kind=='time':field='TimeField'
    elif kind in ['image','binary','varbinary']:field='BinaryField';arguments.append('editable=True')
    elif kind=='uniqueidentifier':field='UUIDField'
    else:raise ValueError('未声明的源类型：'+kind)
    return 'models.'+field+'('+', '.join(arguments)+')'

def generate(schema_path,registry_path):
    source=json.loads(schema_path.read_text(encoding='utf-8-sig'));registry=json.loads(registry_path.read_text(encoding='utf-8'))
    targets={table['module']+'.'+table['model']:table for table in registry['tables'] if table['handling']=='business_model'}
    for table in targets.values():
        for relation in table['relations']:
            assert len(relation['source_fields'])==len(relation['target_fields']),relation
            assert set(relation['source_fields'])<=set(table['fields']),(table['table'],relation)
            assert set(relation['target_fields'])<=set(targets[relation['target']]['fields']),(table['table'],relation)
    columns=defaultdict(list)
    identity_rules={(row['schema_name'],row['table_name'],row['field_name']):(int(row['seed']),int(row['increment']))
                    for row in source['identities']}
    owners=runpy.run_path(str(ROOT/'backend/plugins/erp_base/source_ownership.py'))['OWNERS']
    formulas=runpy.run_path(str(ROOT/'backend/plugins/erp_base/source_calculations.py'))
    entry_formulas=runpy.run_path(str(ROOT/'backend/plugins/erp_base/source_calculation_entries.py'))['ENTRY_METHODS']
    entry_rules=json.loads((ROOT/'backend/plugins/erp_base/source_entry_rules.json').read_text(encoding='utf8'))['models']
    for column in source['fields']:columns[(column['schema_name'],column['table_name'])].append(column)
    grouping=defaultdict(list)
    for table in registry['tables']:
        if table['handling']=='business_model':grouping[table['module']].append(table)
    for module in MODULES:
        code=['"""静态旧业务字段；由tools/legacy_models生成，逐表来源见source_catalog.json。"""',
              'from django.db import models','from django.db.models.functions import Upper,RTrim',
              'from plugins.erp_base.source_documents import SourceRecord','']
        resources=['"""原业务模型的完整字段与主从入口。"""','RESOURCE_OPTIONS = {']
        for table in grouping[module]:
            name=table['model'];fields=columns[(table['schema'],table['table'])]
            raw={column['field_name']:identifier(column['field_name']) for column in fields}
            assert len(set(raw.values()))==len(raw),name
            code += ['', 'class '+name+'(SourceRecord):','    SOURCE_SCHEMA='+repr(table['schema']),
                     '    SOURCE_TABLE='+repr(table['table']),'    SOURCE_FIELDS='+repr(raw),'    SOURCE_KEY='+repr(tuple(table['primary_key'])),
                     '    SOURCE_DOCUMENT='+repr(table['document']),
                     '    SOURCE_COLLATIONS='+repr({raw[column['field_name']]:column['collation_name'] for column in fields if column['collation_name'] is not None}),
                     '    SOURCE_RELATIONS='+repr(table['relations']),
                     '    SOURCE_DEFAULTS='+repr({raw[column['field_name']]:original_default(column['default_definition'])
                                                for column in fields if column['default_definition'] is not None}),
                     '    SOURCE_IDENTITIES='+repr(tuple(raw[column['field_name']] for column in fields if column['is_identity'])),
                     '    SOURCE_IDENTITY_RULES='+repr({raw[column['field_name']]:identity_rules[(table['schema'],table['table'],column['field_name'])]
                                                       for column in fields if column['is_identity']})]
            for column in fields:
                title=table['captions'][column['field_name']]
                code.append('    '+raw[column['field_name']]+'='+declaration(column,title))
            for relation in table['relations']:
                code.append('    '+relation['field']+'=models.ForeignKey('+repr(relation['target'])+", verbose_name="+repr(relation['title'])+", null=True, blank=True, on_delete=models.PROTECT, related_name='+')")
            indexed={tuple(table['primary_key'])} if table['primary_key'] else set()
            indexed.update(tuple(r['target_fields']) for t in registry['tables'] for r in t['relations'] if r['target']==module+'.'+name)
            index_code=[]
            for key in sorted(indexed):
                fields=['source_batch',*[raw[column] for column in key]]
                index_name='src_'+hashlib.sha256((module+'.'+name+','.join(key)).encode()).hexdigest()[:16]
                index_code.append('models.Index(fields='+repr(fields)+',name='+repr(index_name)+')')
                collations={raw[column['field_name']]:column['collation_name'] for column in columns[(table['schema'],table['table'])] if column['collation_name'] is not None}
                if any(raw[column] in collations for column in key):
                    expressions=["models.F('source_batch')"]
                    for column in key:
                        field_key=raw[column];expression='models.F('+repr(field_key)+')'
                        if field_key in collations:
                            expression='RTrim('+expression+')'
                            if '_CI_' in collations[field_key]:expression='Upper('+expression+')'
                        expressions.append(expression)
                    ci_name='src_ci_'+hashlib.sha256((module+'.'+table['model']+','.join(key)).encode()).hexdigest()[:16]
                    index_code.append('models.Index('+','.join(expressions)+',name='+repr(ci_name)+')')
            code+=['','    class Meta(SourceRecord.Meta):','        db_table='+repr(table['db_table']),
                   '        indexes=['+','.join(index_code)+']',
                   '        verbose_name=verbose_name_plural='+repr(table['title']),'        ordering=["-id"]']
            options={'viewset':'plugins.erp_base.source_api.SourceRecordViewSet','serializer':'plugins.erp_base.source_api.SourceRecordSerializer',
                     'crud_fields':['id','entry_name',*raw.values(),*[r['field'] for r in table['relations']],'approval_stage','confirmed_at','confirmed_by','approved_at','approved_by','source_batch','source_row','remarks'],
                     'fields':{'source_batch':{'column':{'show':False}},'source_row':{'column':{'show':False}}},
                     'workflow':{'source_model':True,'state_field':'approval_stage','actions':[]}}
            if table['document']:
                options['workflow'].update({'editable_states':['draft'],'actions':[
                    {'key':'confirm','title':'确认','states':['draft'],'inputs':[]},
                    {'key':'approve','title':'审核','states':['confirmed'],'inputs':[]},
                    {'key':'reopen','title':'重新办理','states':['confirmed','approved'],'inputs':[{'key':'reason','title':'原因','kind':'textarea','required':True,'options':[]}]}]})
            rules=entry_rules.get(module+'.'+name,{})
            options['fields']['entry_name']={'title':'业务类型','column':{'show':False}}
            options['workflow']['entries']=[{'value':entry,'label':rule['title'],
                'generated_fields':[raw[old] for old in [*rule['number_fields'],*rule['default_fields']]]}
                for entry,rule in rules.items()]
            if table['table']=='OrderMain':
                options['viewset']='plugins.erp_base.source_api.SourceOrderViewSet'
                options['workflow']['actions'].append({'key':'close_expired','title':'按原180天规则结单',
                    'states':['draft','confirmed','approved',None],'inputs':[
                        {'key':'as_of','title':'核对日期（YYYY-MM-DD）','kind':'text','required':True,'options':[]}]})
            if table['table']=='DyeDipsRecord':
                options['viewset']='plugins.erp_base.source_api.SourceDipsViewSet'
                options['workflow']['actions'].extend([
                    {'key':'update_result','title':'按原规则回写本单打样结果','states':['draft','confirmed','approved',None],'inputs':[]},
                    {'key':'record_reply','title':'登记打样回复/确版号','states':['draft','confirmed','approved',None],'inputs':[
                        {'key':'note','title':'回复说明（原Note）','kind':'textarea','required':False,'options':[]},
                        {'key':'status','title':'原回复状态值','kind':'select','required':True,'options':[{'value':True,'label':'1'},{'value':False,'label':'0'}]},
                        {'key':'confirm_version','title':'确版号（原值）','kind':'text','required':False,'options':[]},
                        {'key':'reply_at','title':'实际回复时间','kind':'datetime','required':True,'default_now':False,'options':[]}]},
                    {'key':'adopt_recipe','title':'采用试验列生成配方','states':['draft','confirmed','approved',None],'inputs':[
                        {'key':'entry','title':'目标配方类型','kind':'select','required':True,'options':[{'value':'TrialDyeRecipe','label':'试产配方'},{'value':'BulkDyeRecipe','label':'生产配方'}]},
                        {'key':'slot','title':'实际采用试验列','kind':'select','required':True,'options':[{'value':key,'label':key} for key in 'ABCDEF']},
                        {'key':'version','title':'新配方版本','kind':'text','required':True,'options':[]},
                        {'key':'adopted_at','title':'实际采用时间','kind':'datetime','required':True,'default_now':False,'options':[]}]}])
            if table['table']=='DyeRecipe':
                options['viewset']='plugins.erp_base.source_api.SourceRecipeViewSet'
                options['workflow']['actions'].append({'key':'to_production','title':'复制采用为生产配方',
                    'states':['draft','confirmed','approved',None],'inputs':[
                        {'key':'version','title':'新生产配方版本','kind':'text','required':True,'options':[]},
                        {'key':'adopted_at','title':'实际采用时间','kind':'datetime','required':True,'default_now':False,'options':[]}]})
            if table['table']=='JobSheet':
                options['viewset']='plugins.erp_base.source_api.SourceJobViewSet'
                options['workflow']['actions'].append({'key':'charge_quote','title':'查询原另收费合计',
                    'states':['draft','confirmed','approved',None],'inputs':[]})
            if table['table']=='PurDetail':
                options['viewset']='plugins.erp_base.source_api.SourcePurchaseDetailViewSet'
                options['workflow']['actions'].extend([
                    {'key':'receipt_progress','title':'查询原采购收货进度','states':['draft','confirmed','approved',None],'inputs':[]},
                    {'key':'receive','title':'按实际分批量生成收货单','states':['draft','confirmed','approved',None],'inputs':[
                        {'key':'entry','title':'收货入口','kind':'select','required':True,'options':[{'value':'PurGrayIn','label':'采购坯料入库'},{'value':'PurSemiIn','label':'采购半成品入库'}]},
                        {'key':'received_at','title':'实际收货时间','kind':'datetime','required':True,'default_now':False,'options':[]},
                        {'key':'quantity','title':'本次实际重量（可负数）','kind':'decimal','nullable':True,'required':False,'options':[]},
                        {'key':'rolls','title':'本次实际粒数（可小数/负数）','kind':'decimal','nullable':True,'required':False,'options':[]},
                        {'key':'warehouse','title':'实际仓库原编码','kind':'text','required':False,'options':[]},
                        {'key':'unit','title':'实际库存单位原编码','kind':'text','required':False,'options':[]}]}])
            if table['table']=='OrderColor':
                options['viewset']='plugins.erp_base.source_api.SourceOutworkOrderViewSet'
                options['workflow']['actions'].extend([
                    {'key':'outwork_remaining','title':'查询原外协待申请量','states':['draft','confirmed','approved',None],'inputs':[]},
                    {'key':'apply_outwork','title':'按明确数量生成外协申请','states':['draft','confirmed','approved',None],'inputs':[
                        {'key':'quantity','title':'本次申请量（可负数）','kind':'decimal','nullable':True,'required':False,'options':[]},
                        {'key':'rolls','title':'本次申请粒数','kind':'decimal','nullable':True,'required':False,'options':[]},
                        {'key':'factory','title':'外协厂原编码','kind':'text','required':False,'options':[]},
                        {'key':'process','title':'加工工序原编码','kind':'text','required':False,'options':[]},
                        {'key':'entry','title':'申请类型','kind':'select','required':True,'options':[{'value':'OutWorkApply','label':'坯料发外'},{'value':'SemiOutWorkApply','label':'半成品发外'}]},
                        {'key':'applied_at','title':'实际申请时间','kind':'datetime','required':True,'default_now':False,'options':[]}]}])
            if table['table'] in ['OutWorkApplyDetail','SemiOutWorkApplyDetail','GrayOutDetail','SemiOutDetail']:
                is_apply=table['table'] in ['OutWorkApplyDetail','SemiOutWorkApplyDetail']
                options['viewset']='plugins.erp_base.source_api.'+('SourceOutworkApplyDetailViewSet' if is_apply else 'SourceOutworkDispatchDetailViewSet')
                options['workflow']['actions'].append({'key':'dispatch_outwork' if is_apply else 'receive_outwork',
                    'title':'按实际量生成外协发出单' if is_apply else '按实际量生成外协回货成品单',
                    'states':['draft','confirmed','approved',None],'inputs':[
                        {'key':'quantity','title':'本次实际重量','kind':'decimal','nullable':True,'required':False,'options':[]},
                        {'key':'rolls','title':'本次实际粒数','kind':'decimal','nullable':True,'required':False,'options':[]},
                        {'key':'warehouse','title':'实际仓库原编码','kind':'text','required':False,'options':[]},
                        {'key':'unit','title':'实际库存单位原编码','kind':'text','required':False,'options':[]},
                        {'key':'job_number','title':'实际工卡号（原值）','kind':'text','required':False,'options':[]},
                        {'key':'sheet_kind','title':'本次原单据类型编码','kind':'number','required':True,'options':[]},
                        {'key':'happened_at','title':'实际收发时间','kind':'datetime','required':True,'default_now':False,'options':[]}]})
            if table['table']=='DefectiveInDetail':
                options['viewset']='plugins.erp_base.source_api.SourceDefectiveDetailViewSet'
                options['workflow']['actions'].append({'key':'defective_balance','title':'查询原疵布收发余额',
                    'states':['draft','confirmed','approved',None],'inputs':[]})
            if table['table'] in ['OutWorkApply','SemiOutWorkApply']:
                options['viewset']='plugins.erp_base.source_api.SourceOutworkApplyViewSet'
                movement='grayoutdetail' if table['table']=='OutWorkApply' else 'semioutdetail'
                options['workflow']['actions'].extend([
                    {'key':'close_outwork','title':'核对收发并确认损耗结案','states':['draft','confirmed','approved',None],'inputs':[
                        {'key':'dispatched','title':'实际发外明细（可多选）','kind':'multi','required':False,'options':[],
                         'remote':{'entity':'erp_warehouse_sourcedye'+movement,'pk':'id','label':'old_assigned_no' if table['table']=='OutWorkApply' else 'old_detail_no'}},
                        {'key':'received','title':'实际回货单（可多选）','kind':'multi','required':False,'options':[],
                         'remote':{'entity':'erp_warehouse_sourcedyeprodin','pk':'id','label':'old_sheet_no'}},
                        {'key':'losses','title':'确认损耗明细','kind':'losses','required':False,'default':[], 'options':[]},
                        {'key':'closed_at','title':'实际结案时间','kind':'datetime','required':True,'default_now':False,'options':[]},
                        {'key':'reason','title':'结案依据/差异说明','kind':'textarea','required':True,'options':[]}]},
                    {'key':'outwork_closure','title':'查看结案与损耗核对','states':['draft','confirmed','approved',None],'inputs':[]},
                    {'key':'reopen_outwork','title':'撤回外协结案','states':['draft','confirmed','approved',None],'inputs':[
                        {'key':'reason','title':'撤回原因','kind':'textarea','required':True,'options':[]}]}])
            if table['table']=='WProcess':
                options['viewset']='plugins.erp_base.source_api.SourceWorkViewSet'
                options['workflow']['actions'].append({'key':'delete_shift_record','title':'按旧班次规则删除刷卡',
                    'states':['draft','confirmed','approved',None],'hide_when':['source_batch'],'inputs':[
                        {'key':'mode','title':'实际删除链','kind':'select','required':True,'options':[
                            {'value':'trigger','label':'原删除触发器'},
                            {'value':'trigger_then_maintenance','label':'删除触发器后执行删除维护过程'}]},
                        {'key':'reason','title':'删除原因','kind':'textarea','required':True,'options':[]}]})
            if table['table']=='WDefect':
                options['viewset']='plugins.erp_base.source_api.SourceQualityViewSet'
                inputs=[{'key':'report','title':'统计口径','kind':'select','required':True,'options':[
                    {'value':1,'label':'日/月部门及班次统计'}, {'value':2,'label':'旬/月二级分类统计'}, {'value':3,'label':'日/月一级分类统计'}]},
                    {'key':'as_of','title':'统计日期','kind':'date','required':True,'options':[]}]
                inputs.extend({'key':key,'title':title,'kind':'decimal','nullable':True,'required':False,'options':[]} for key,title in [
                    ('DayAllNum','原本旬分母卡数'),('DayAllKg','原本旬分母重量'),('MonthAllNum','原月累计分母卡数'),('MonthAllKg','原月累计分母重量')])
                inputs.append({'key':'denominator_reference','title':'原分母来源（旬报）','kind':'textarea','required':False,'options':[]})
                options['workflow']['actions'].append({'key':'quality_statistics','title':'质量日/月/旬统计','detail':False,'inputs':inputs})
            if table['table']=='dyeCheckout':
                options['viewset']='plugins.erp_base.source_api.SourceDyeCheckoutViewSet'
                options['workflow']['actions'].append({'key':'quality_award','title':'染色质量责任奖扣统计','detail':False,'inputs':[
                    {'key':'start','title':'开始时间（含）','kind':'datetime','required':True,'default_now':False,'options':[]},
                    {'key':'end','title':'结束时间（含）','kind':'datetime','required':True,'default_now':False,'options':[]}]})
            if table['table']=='StuffWeight':
                options['workflow']['actions'].append({'key':'issue_materials','title':'按原称料规则生成领料',
                    'states':['draft','confirmed','approved'],'inputs':[
                        {'key':'finished_at','title':'实际事件时间','kind':'datetime','required':True,'default_now':False,'options':[]},
                        {'key':'evidence_kind','title':'实际事件类型','kind':'select','required':True,'options':[
                            {'value':'weighing_finished','label':'称量完成记录'},{'value':'process_started','label':'染色工序开工记录'}]},
                        {'key':'evidence_reference','title':'实际事件记录号或证明','kind':'text','required':True,'options':[]}]})
            extend_continuation_actions(table['table'],options)
            extend_foundation_actions(table['table'],options)
            for relation in table['relations']:
                target=targets[relation['target']]
                label='SheetNo' if 'SheetNo' in target['fields'] else target['primary_key'][0] if target['primary_key'] else target['fields'][0]
                options['fields'][relation['field']]={'remote':{'entity':target['module']+'_'+target['model'].lower(),
                    'pk':'id','label':identifier(label),'columns':[{'field':identifier(old),'title':target['captions'][old]}
                    for old in list(dict.fromkeys([label,*relation['target_fields']]))]}}
            if module+'.'+name in owners:
                options['workflow']['editable_states']=['draft',None]
            methods=[]
            if table['table'] in formulas['PRODUCTS'] or table['table'] in formulas['SPECIAL_TABLES']:
                methods=[{'value':'fields','label':'原字段公式'}]
            elif table['table']=='RecordYield':
                methods=[{'value':key,'label':value} for key,value in formulas['PACK_METHODS'].items()]
            if table['table']=='StuffInDetail':
                methods.append({'value':'amount_to_price','label':'原金额反算单价'})
            methods.extend({'value':'entry:'+entry,'label':'原入口：'+title}
                           for entry,title in entry_formulas.get(table['table'],{}).items())
            if methods:
                options['workflow']['actions'].append({'key':'calculate','title':'按原公式计算','states':['draft',None],
                    'inputs':[{'key':'method','title':'计算方法','kind':'select','required':True,'options':methods}]})
            children=[{'entity':child['module']+'_'+child['model'].lower(),'title':child['title'],'key':relation['field'],
                       'atomic':any(rule['field']==relation['field'] and rule['target']==module+'.'+name for rule in owners.get(child['module']+'.'+child['model'],[]))}
                      for child in registry['tables'] if child['handling']=='business_model' for relation in child['relations'] if relation['target']==module+'.'+name]
            options['workflow']['children']=children
            for child in children:
                child['parent_states']=['draft',None] if child['atomic'] else ['draft','confirmed','approved',None]
            if table['table']=='FMoneyInDetail':
                options['viewset']='plugins.erp_base.source_api.SourceSalesLimitReadOnlyViewSet'
                options['workflow'].update(actions=[],entries=[],children=[],readonly=True)
            resources.append('    '+repr(name)+': '+repr(options)+',')
        resources.append('}')
        resources.append('from plugins.erp_base.source_phase2_actions import extend as extend_phase2_actions')
        resources.append('extend_phase2_actions(RESOURCE_OPTIONS)')
        resources.append('from plugins.erp_base.source_phase3_actions import extend as extend_phase3_actions')
        resources.append('extend_phase3_actions(RESOURCE_OPTIONS)')
        resources.append('from plugins.erp_base.source_phase4_actions import extend as extend_phase4_actions')
        resources.append('extend_phase4_actions(RESOURCE_OPTIONS)')
        resources.append('from plugins.erp_base.source_phase5_actions import extend as extend_phase5_actions')
        resources.append('extend_phase5_actions(RESOURCE_OPTIONS)')
        resources.append('from plugins.erp_base.source_phase6_forms import extend as extend_phase6_forms')
        resources.append('extend_phase6_forms(RESOURCE_OPTIONS)')
        code_text='\n'.join(code)+'\n';ast.parse(code_text)
        (ROOT/'backend/plugins'/module/'source_models.py').write_text(code_text,encoding='utf-8',newline='\n')
        (ROOT/'backend/plugins'/module/'source_resources.py').write_text('\n'.join(resources)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'business_models':sum(map(len,grouping.values())),'by_module':{key:len(value) for key,value in grouping.items()},'fields':sum(len(columns[(t['schema'],t['table'])]) for t in registry['tables'] if t['handling']=='business_model')},ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--schema',type=Path,required=True);parser.add_argument('--catalog',type=Path,required=True)
    args=parser.parse_args();generate(args.schema,args.catalog)
