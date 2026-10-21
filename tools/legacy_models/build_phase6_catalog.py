"""将核实过的旧界面、字段及打印原配置完整打包；不凭名称丢弃配置。"""
import argparse
import base64
import gzip
import hashlib
import json
import xml.etree.ElementTree as ET
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TARGET=ROOT/'backend/plugins/erp_base'


def build(snapshot,printing):
    evidence=json.loads(snapshot.read_text(encoding='utf-8-sig'))
    inventory=json.loads((ROOT/'docs/erp-remaining-inventory-20261016.json').read_text(encoding='utf8'))
    financial={r['name'] for r in inventory['axes']['旧界面配置入口'] if r['status']=='财务暂缓'}
    fields=defaultdict(list)
    for row in evidence['ui_fields']:fields[row['DataTableName']].append(row)
    entries=[{'table':row,'fields':fields[row['DataTableName']], 'finance':row['DataTableName'] in financial} for row in evidence['ui_tables']]
    assert len({r['table']['DataTableName'] for r in entries})==len(entries)
    reports=[json.loads(line)['values'] for line in (printing/'dye.s_RptInfo.jsonl').open(encoding='utf8')]
    menus=[json.loads(line)['values'] for line in (printing/'dye.s_RptMenu.jsonl').open(encoding='utf8')]
    functions=[json.loads(line)['values'] for line in (printing/'dye.s_Functions.jsonl').open(encoding='utf8')]
    manifest=[]
    for index,row in enumerate(reports):
        info={k:v for k,v in row.items() if k not in ['Template','TemplateXml']}
        info.update(index=index,has_template=bool(row['Template']),has_xml=bool(row['TemplateXml']))
        info['sha256']={k:hashlib.sha256(base64.b64decode(row[k])).hexdigest() for k in ['Template','TemplateXml'] if row[k]}
        if row['TemplateXml']:
            try:tree=ET.fromstring(base64.b64decode(row['TemplateXml']).decode('utf-8-sig'))
            except ET.ParseError as error:info['xml_error']=str(error)
            else:
                info['data_member']=tree.get('DataMember')
                info['bindings']=[dict(n.attrib) for n in tree.iter() if 'DataMember' in n.attrib]
                info['controls']=dict(Counter(n.get('ControlType').split(',')[0] for n in tree.iter() if n.get('ControlType')))
                info['script_attributes']=[{'tag':n.tag,'name':n.get('Name'),'attribute':k,'value':v} for n in tree.iter() for k,v in n.attrib.items() if 'Script' in k or n.tag=='Scripts']
        manifest.append(info)
    catalog={'captured_at':evidence['captured_at'],'snapshot_sha256':hashlib.sha256(snapshot.read_bytes()).hexdigest(),
        'entries':entries,'reports':manifest,'report_menus':menus,'functions':functions}
    for name,value in [('source_phase6_catalog',catalog),('source_phase6_templates',reports)]:
        payload=json.dumps(value,ensure_ascii=False,separators=(',',':')).encode('utf8')
        (TARGET/(name+'.json.gz')).write_bytes(gzip.compress(payload,mtime=0))
    summary={'entries':len(entries),'fields':len(evidence['ui_fields']),'finance':len(financial),'reports':len(reports),'report_menus':len(menus),'functions':len(functions),
        'xml_templates':sum(r['has_xml'] for r in manifest),'xml_errors':[{'index':r['index'],'RptID':r['RptID'],'error':r['xml_error']} for r in manifest if 'xml_error' in r],
        'script_templates':sum(bool(r.get('script_attributes')) for r in manifest),'snapshot_sha256':catalog['snapshot_sha256']}
    (TARGET/'source_phase6_catalog_manifest.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--snapshot',type=Path,required=True);parser.add_argument('--printing',type=Path,required=True)
    args=parser.parse_args();build(args.snapshot,args.printing)
