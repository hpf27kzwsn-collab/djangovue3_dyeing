"""完整登记每份原模板的几何解析、脚本和控件差异，不以解析成功替代打印完成。"""
import base64
from collections import Counter
import gzip
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TARGET=ROOT/'backend/plugins/erp_base'


def build():
    spec=importlib.util.spec_from_file_location('original_layouts',TARGET/'source_phase6_layouts.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    templates=json.loads(gzip.decompress((TARGET/'source_phase6_templates.json.gz').read_bytes()))
    entries=json.loads(gzip.decompress((TARGET/'source_phase6_catalog.json.gz').read_bytes()))['entries']
    entry_fields={e['table']['DataTableName']:{f['FieldName'] for f in e['fields']} for e in entries}
    result=[]
    for index,row in enumerate(templates):
        item={'index':index,'RptID':row['RptID'],'title':row['RptTitle'],'has_template':bool(row['Template']),
            'has_xml':bool(row['TemplateXml']),'development':'原运行版式尚未全部复刻','historical_reconciliation':'未对账','field_acceptance':'未验收'}
        if row['TemplateXml']:
            root,refs=module.parse_xml(base64.b64decode(row['TemplateXml']))
            layout=module.describe(row)
            bindings=[dict(n.attrib) for n in root.iter() if 'DataMember' in n.attrib]
            scripts=[{'element':n.tag,'name':n.get('Name'),'attribute':k,'value':v} for n in root.iter() for k,v in n.attrib.items() if 'Script' in k and k!='Ref' or n.tag=='Scripts' and k!='Ref']
            controls=dict(Counter(module.kind(n) for n in root.iter() if n.get('ControlType')))
            missing=[]
            for binding in bindings:
                name=binding['DataMember'];parts=name.rsplit('.',1)
                if len(parts)==2 and parts[0] in entry_fields and parts[1] not in entry_fields[parts[0]]:missing.append(name)
            item.update(geometry_state='parsed',data_member=root.get('DataMember'),page=layout['page'],
                bands=len(layout['bands']),controls=controls,issues=layout['issues'],bindings=bindings,
                numeric_control_references=refs,script_bindings=scripts,fields_missing_from_same_named_entry=missing,
                data_member_is_registered_entry=root.get('DataMember') in entry_fields,sha256=layout['sha256'])
        else:item.update(geometry_state='no_xml',reason='只有原客户端模板' if row['Template'] else '原配置没有模板内容')
        result.append(item)
    report={'reports':result,'counts':{'reports':len(result),'parsed_xml':sum(r['geometry_state']=='parsed' for r in result),
        'no_xml':sum(r['geometry_state']=='no_xml' for r in result),'control_entity_templates':sum(bool(r.get('numeric_control_references')) for r in result),
        'script_templates':sum(bool(r.get('script_bindings')) for r in result),'fully_replicated_print_layouts':0}}
    for target in [TARGET/'source_phase6_layout_manifest.json',ROOT/'docs/erp-phase6-layout-review-20261017.json']:
        target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(report['counts'])


if __name__=='__main__':build()
