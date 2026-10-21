"""补齐全部非财务平台原表；配置文本只保存，原行为另行移植。"""
import argparse
import hashlib
import json
from pathlib import Path
from generate_models import identifier,declaration,original_default
from build_entry_rules import build as build_rules

ROOT=Path(__file__).resolve().parents[2]
TABLES={'s_AlertFormat','s_AlertItem','s_AlertLog','s_AlertParams','s_AlertUser',
    's_App','s_AppFuncs','s_AppQuerys','s_AppTables','s_DataTableCopy','s_DataTableFieldRely',
    's_FormButton','s_GridCondition','s_GridParamChart','s_GridUser','s_Language','s_LookupColumn',
    's_ManagerSQL','s_Message','s_Notice','s_PanelFieldParam','s_QueryParam','s_RecordRight',
    's_RptInfoDetail','s_RptInfoSub','s_RptParam','s_SubscribePage','s_TimerJobField',
    's_TimerJobParams','s_UIModule','s_UpgradeFile',
    'AlarmLog','EmOpLog','rp_Permission','s_AccessLog','s_AlertEmp','s_AlertSender','s_App_ApiLog',
    's_ClientMacAddress','s_DataRelation','s_DataTableRelation','s_Exception','s_FieldCopy','s_FormFormat',
    's_FunDesktop','s_Language1','s_LocalAdmins','s_ManagerSetting','s_ManagerSQL-','s_ModuleDesktop',
    's_MonthEnd','s_PersonalDataRight','s_SecurityInfo','s_SysAdmins','s_TVScreenReport',
    's_TVScreenReportDetail','s_WeiXinAgent','s_WeiXinMenu','SECURITYDETAILS','ServerLog','SystemLog',
    'UserACPrivilege','UserUpdates'}


def restore(snapshot):
    schema=json.loads(snapshot.read_text(encoding='utf-8-sig'))
    catalog_path=ROOT/'tools/legacy_models/source_catalog.json'
    catalog=json.loads(catalog_path.read_text(encoding='utf8'))
    tables=[t for t in catalog['tables'] if t['schema']=='dye' and t['table'] in TABLES]
    assert len(tables)==len(TABLES)==63
    for table in tables:
        if table['table']=='s_ManagerSQL-':table['model']='SourceDyeSManagerSQLDash'
        table.update(handling='business_model',title='旧入口平台来源（'+table['table']+'）',
            reason='P6原入口的明确取数/字段配置来源，按最新字段及原键承接；保存原SQL/脚本/通知文本，不自动执行或对外发送。',
            classification_basis='P6完整入口及全部非财务原表核查确认原表已存在而模型缺失')
    assert len({t['model'] for t in tables})==len(tables)
    catalog_path.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    build_rules(snapshot)
    rules=json.loads((ROOT/'backend/plugins/erp_base/source_entry_rules.json').read_text(encoding='utf8'))['models']
    models_path=ROOT/'backend/plugins/erp_base/source_models.py';models=models_path.read_text(encoding='utf8')
    imports_path=ROOT/'backend/plugins/erp_base/models.py';imports=imports_path.read_text(encoding='utf8')
    resources_path=ROOT/'backend/plugins/erp_base/source_resources.py';resources=resources_path.read_text(encoding='utf8')
    identity_rules={(r['schema_name'],r['table_name'],r['field_name']):(int(r['seed']),int(r['increment'])) for r in schema['identities']}
    rows=[]
    for table in tables:
        name=table['model'];label='erp_base.'+name
        fields=[c for c in schema['fields'] if c['schema_name']=='dye' and c['table_name']==table['table']]
        assert {c['field_name'] for c in fields}==set(table['fields'])
        raw={c['field_name']:identifier(c['field_name']) for c in fields}
        collations={raw[c['field_name']]:c['collation_name'] for c in fields if c['collation_name']}
        code=['','class '+name+'(SourceRecord):',"    SOURCE_SCHEMA='dye'",'    SOURCE_TABLE='+repr(table['table']),
            '    SOURCE_FIELDS='+repr(raw),'    SOURCE_KEY='+repr(tuple(table['primary_key'])),
            '    SOURCE_DOCUMENT=False','    SOURCE_COLLATIONS='+repr(collations),'    SOURCE_RELATIONS=[]',
            '    SOURCE_DEFAULTS='+repr({raw[c['field_name']]:original_default(c['default_definition']) for c in fields if c['default_definition']}),
            '    SOURCE_IDENTITIES='+repr(tuple(raw[c['field_name']] for c in fields if c['is_identity'])),
            '    SOURCE_IDENTITY_RULES='+repr({raw[c['field_name']]:identity_rules['dye',table['table'],c['field_name']] for c in fields if c['is_identity']})]
        code.extend('    '+raw[c['field_name']]+'='+declaration(c,table['captions'][c['field_name']]) for c in fields)
        indexes=[]
        if table['primary_key']:
            key=table['primary_key'];suffix=hashlib.sha256((label+','.join(key)).encode()).hexdigest()[:16]
            indexes.append('models.Index(fields='+repr(['source_batch',*[raw[k] for k in key]])+',name='+repr('src_'+suffix)+')')
            if any(raw[k] in collations for k in key):
                expressions=["models.F('source_batch')"]
                for field in key:
                    expression='models.F('+repr(raw[field])+')'
                    if raw[field] in collations:
                        expression='RTrim('+expression+')'
                        if '_CI_' in collations[raw[field]]:expression='Upper('+expression+')'
                    expressions.append(expression)
                indexes.append('models.Index('+','.join(expressions)+',name='+repr('src_ci_'+suffix)+')')
        code+=['','    class Meta(SourceRecord.Meta):','        db_table='+repr(table['db_table']),
            '        indexes=['+','.join(indexes)+']','        verbose_name=verbose_name_plural='+repr(table['title']),
            '        ordering=["-id"]','']
        if '\nclass '+name+'(' not in models:models+='\n'.join(code)
        statement='from .source_models import '+name
        if statement+'\n' not in imports:imports+='\n'+statement+'\n'
        entries=rules.get(label,{})
        options={'viewset':'plugins.erp_base.source_api.SourceRecordViewSet','serializer':'plugins.erp_base.source_api.SourceRecordSerializer',
            'crud_fields':['id','entry_name',*raw.values(),'approval_stage','confirmed_at','confirmed_by','approved_at','approved_by','source_batch','source_row','remarks'],
            'fields':{'entry_name':{'title':'业务类型','column':{'show':False}},'source_batch':{'column':{'show':False}},'source_row':{'column':{'show':False}}},
            'workflow':{'source_model':True,'state_field':'approval_stage','actions':[],'entries':[
                {'value':entry,'label':rule['title'],'generated_fields':[raw[old] for old in [*rule['number_fields'],*rule['default_fields']]]} for entry,rule in entries.items()],
                'children':[]}}
        if repr(name)+':' not in resources:
            resources=resources.replace('\n}\nfrom plugins.erp_base.source_phase2_actions', '\n    '+repr(name)+': '+repr(options)+',\n}\nfrom plugins.erp_base.source_phase2_actions',1)
        rows.append({'model':label,'table':table['table'],'fields':len(fields),'original_key':table['primary_key']})
    models_path.write_text(models,encoding='utf8');imports_path.write_text(imports,encoding='utf8');resources_path.write_text(resources,encoding='utf8')
    result={'models':len(rows),'fields':sum(r['fields'] for r in rows),'extra_legacy_id_fields':0,'tables':rows}
    (ROOT/'docs/erp-phase6-added-source-models-20261016.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--snapshot',type=Path,required=True)
    restore(parser.parse_args().snapshot)
