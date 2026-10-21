"""原DevExpress版式的可核对几何模型；原模板、脚本和不支持控件均保留。"""
import base64
import hashlib
import re
import xml.etree.ElementTree as ET
import json
from functools import lru_cache
from pathlib import Path
from django.core.exceptions import ValidationError


@lru_cache(maxsize=1)
def manifest():
    return json.loads(Path(__file__).with_name('source_phase6_layout_manifest.json').read_text(encoding='utf8'))


def parse_xml(data):
    text=data.decode('utf-8-sig')
    references=[]
    # 七份原模板把XML 1.0禁用的控制字符写成数字实体；只在解析副本转义并还原属性值。
    marker='ERP_XML_CONTROL_'+hashlib.sha256(data).hexdigest()+'_'
    def entity(match):
        literal=match[0];number=int(match[1][1:],16) if match[1].startswith(('x','X')) else int(match[1])
        if number in [9,10,13] or 32<=number<=0xD7FF or 0xE000<=number<=0xFFFD or 0x10000<=number<=0x10FFFF:return literal
        if not 0<=number<=0x10FFFF:raise ValueError('原数字实体不属于Unicode码位：'+literal)
        token=marker+str(len(references))+'__';references.append({'token':token,'literal':literal,'codepoint':number})
        return token
    root=ET.fromstring(re.sub(r'&#(x[0-9a-fA-F]+|[0-9]+);',entity,text))
    for node in root.iter():
        for key,value in node.attrib.items():
            for item in references:value=value.replace(item['token'],chr(item['codepoint']))
            node.set(key,value)
    return root,references


def kind(node):return node.get('ControlType','').split(',')[0].split('.')[-1]


def pair(value):return [float(n.strip()) for n in value.split(',')]


def describe(row):
    if row['TemplateXml'] is None:
        raise ValidationError({'layout':'此原报表只有旧客户端模板，没有XML版式；原模板继续保留。'})
    data=base64.b64decode(row['TemplateXml']);root,references=parse_xml(data)
    bands=[];issues=[]
    def node_tree(node):return {'tag':node.tag,'attributes':dict(node.attrib),'children':[node_tree(c) for c in node]}
    def flatten(node,offset=(0,0),box=None,inherited=None):
        inherited=inherited or {}
        style={**inherited,**{k:v for k,v in node.attrib.items() if k in ['Font','ForeColor','BackColor','Borders','BorderWidth','TextAlignment','Padding']}}
        x,y=pair(node.get('LocationFloat','0,0'));w,h=pair(node.get('SizeF','0,0'))
        if box is not None:x,y,w,h=box
        x+=offset[0];y+=offset[1]
        control=kind(node)
        binding=[dict(n.attrib) for n in node.findall('./DataBindings/*')]
        result={'kind':control,'name':node.get('Name'),'x':x,'y':y,'width':w,'height':h,
            'style':style,'text':node.get('Text',''),'bindings':binding,'attributes':dict(node.attrib),'children':[],
            'summary':dict(node.find('Summary').attrib) if node.find('Summary') is not None else None}
        result['symbology']=dict(node.find('Symbology').attrib) if node.find('Symbology') is not None else None
        if control=='XRTable':
            rows=list(node.findall('./Rows/*'));weights=[float(r.get('Weight','1')) for r in rows];top=0
            for r,rw in zip(rows,weights):
                height=h*rw/sum(weights);cells=list(r.findall('./Cells/*'));cw=[float(c.get('Weight','1')) for c in cells];left=0
                row_style={**style,**{k:v for k,v in r.attrib.items() if k in style or k in ['Font','Borders','TextAlignment']}}
                for cell,weight in zip(cells,cw):
                    width=w*weight/sum(cw)
                    result['children'].append(flatten(cell,(x,y),(left,top,width,height),row_style));left+=width
                top+=height
        else:
            result['children']=[flatten(c,(x,y),inherited=style) for c in node.findall('./Controls/*')]
        from . import source_phase6_qr_print as qr_print
        qr_supported=control=='XRBarCode' and not qr_print.issues(node,root)
        if control not in ['XRTable','XRTableCell','XRLabel','XRLine','XRPageInfo'] and not qr_supported:
            issues.append({'control':node.get('Name'),'kind':control,'reason':'保留原位置与属性；此控件的旧运行行为尚未实现'})
        if node.find('Scripts') is not None and not qr_print.script_event(node.find('Scripts'),root):issues.append({'control':node.get('Name'),'kind':control,'reason':'原控件有事件脚本，几何预览不执行脚本'})
        return result
    def band_nodes(parent,trail):
        for band in parent.findall('./Bands/*'):
            name=band.get('Name','');path=[*trail,name]
            if kind(band)!='DetailReportBand':
                style={**{k:v for k,v in root.attrib.items() if k in ['Font','Borders','TextAlignment']},**dict(band.attrib)}
                bands.append({'name':name,'path':path,'kind':kind(band),'height':float(band.get('HeightF','0')),
                    'attributes':dict(band.attrib),'controls':[flatten(c,inherited=style) for c in band.findall('./Controls/*')]})
            band_nodes(band,path)
    band_nodes(root,[])
    return {'report_id':row['RptID'],'title':row['RptTitle'],'sha256':hashlib.sha256(data).hexdigest(),
        'page':dict(root.attrib),'data_member':root.get('DataMember'),'bands':bands,
        'source_tree':node_tree(root),'control_references':references,'issues':issues,
        'mode':'original_geometry_review','development':'原几何、绑定和属性已解析；脚本、分组分页及设备输出待逐项复刻',
        'historical_reconciliation':'未进行业务结果对账','field_acceptance':'待纸张、打印机及标签现场验收'}
