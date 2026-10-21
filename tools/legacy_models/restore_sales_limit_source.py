"""销售限制需要的只读共享来源；不启用收款/核销办理。"""
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent))
from generate_models import identifier,declaration,original_default


def restore(schema_path):
    schema=json.loads(Path(schema_path).read_text(encoding='utf-8-sig'))
    path=ROOT/'tools/legacy_models/source_catalog.json'
    catalog=json.loads(path.read_text(encoding='utf8'))
    table=next(t for t in catalog['tables'] if t['schema']=='dye' and t['table']=='FMoneyInDetail')
    table.update(handling='business_model',entry_scope='business_source_only',title='销售限制共享核销来源（原FMoneyInDetail，只读）',
        reason='fn_RKL/RKLimit只读计算所需原行；不启用收款、核销、凭证及财务办理',classification_basis='P2原函数及视图当前依赖')
    fields=[c for c in schema['fields'] if c['schema_name']=='dye' and c['table_name']==table['table']]
    raw={c['field_name']:identifier(c['field_name']) for c in fields}
    code=['','class '+table['model']+'(SourceRecord):',"    SOURCE_SCHEMA='dye'","    SOURCE_TABLE='FMoneyInDetail'",
        '    SOURCE_FIELDS='+repr(raw),'    SOURCE_KEY='+repr(tuple(table['primary_key'])),
        '    SOURCE_DOCUMENT=False','    SOURCE_COLLATIONS='+repr({raw[c['field_name']]:c['collation_name'] for c in fields if c['collation_name']}),
        '    SOURCE_RELATIONS=[]','    SOURCE_DEFAULTS='+repr({raw[c['field_name']]:original_default(c['default_definition']) for c in fields if c['default_definition'] is not None}),
        '    SOURCE_IDENTITIES=()','    SOURCE_IDENTITY_RULES={}']
    code.extend('    '+raw[c['field_name']]+'='+declaration(c,table['captions'][c['field_name']]) for c in fields)
    scope='erp_base.'+table['model']+','.join(table['primary_key']);suffix=hashlib.sha256(scope.encode()).hexdigest()[:16]
    code+=['','    class Meta(SourceRecord.Meta):',"        db_table='src_dye_fmoneyindetail'",
        "        indexes=[models.Index(fields=['source_batch','old_sheet_series','old_detail_no'],name='src_"+suffix+"'),models.Index(models.F('source_batch'),Upper(RTrim(models.F('old_sheet_series'))),Upper(RTrim(models.F('old_detail_no'))),name='src_ci_"+suffix+"')]",
        '        verbose_name=verbose_name_plural='+repr(table['title']),'        ordering=["-id"]','']
    target=ROOT/'backend/plugins/erp_base/source_models.py';text=target.read_text(encoding='utf8')
    if '\nclass '+table['model']+'(' not in text:target.write_text(text+'\n'.join(code),encoding='utf8')
    target=ROOT/'backend/plugins/erp_base/models.py';text=target.read_text(encoding='utf8')
    statement='from .source_models import SourceDyeFMoneyInDetail'
    if statement not in text:target.write_text(text+'\n'+statement+'\n',encoding='utf8')
    path.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


if __name__=='__main__':restore(sys.argv[1])
