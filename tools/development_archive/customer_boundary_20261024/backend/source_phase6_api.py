"""旧入口读取接口；业务查询逐来源检查数据与字段权限。"""
import base64
import csv
import gzip
import io
import json
from decimal import Decimal
from functools import lru_cache
from pathlib import Path
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from rest_framework import serializers
from core.responses import success
from plugins.erp_base.business_api import parameters
from . import source_phase6_entries as entries


def web_values(value):
    """浏览器数字不能准确表示原decimal和大整数，按原十进制文本传输。"""
    if isinstance(value,Decimal) or isinstance(value,int) and abs(value)>9007199254740991:return str(value)
    if isinstance(value,list):return [web_values(item) for item in value]
    if isinstance(value,dict):return {key:web_values(item) for key,item in value.items()}
    return value


def catalog_view(view):
    if view.request.query_params.get('reports')=='1':
        from plugins.erp_base.source_phase6_layouts import manifest
        catalog=entries.catalog()
        layouts=manifest()['reports']
        reports=[{**r,'layout_state':layouts[r['index']]['geometry_state'],
            'data_member':layouts[r['index']].get('data_member'),'layout_issue_count':len(layouts[r['index']].get('issues',[]))} for r in catalog['reports']]
        return success({'reports':reports,'menus':catalog['report_menus'],'functions':catalog['functions']})
    name=view.request.query_params.get('entry')
    return success(entries.detail(name) if name is not None else entries.summaries())


def query_view(view,export=False):
    p=parameters(view,{'entry':serializers.ChoiceField(choices=list(entries.entries())),
        'parameters':serializers.DictField(default=dict),
        'editor_field':serializers.CharField(required=False),
        'editor_context':serializers.DictField(required=False),
        'filter_text':serializers.CharField(default='',allow_blank=True),
        'load_records':serializers.BooleanField(default=False),
        'include_retained':serializers.BooleanField(default=True),
        'calculate_formulas':serializers.BooleanField(default=False)})
    if 'editor_field' in p:
        from plugins.erp_base.source_phase6_editors import options
        return success(web_values(options(p['entry'],p['editor_field'],p['filter_text'],entries.reader(view.request),p.get('editor_context'))))
    p.pop('editor_context',None)
    p.pop('filter_text')
    support=entries.query_support()[p['entry']]
    if support['query_state']=='unresolved':
        raise ValidationError({'entry':'此入口查询仍有待解决差异，原配置、全部字段和对应原表保留。','difference':support['error']})
    calculate=p.pop('calculate_formulas',False)
    query_name=p.pop('entry');query_parameters=p.pop('parameters');reader=entries.reader(view.request)
    from plugins.erp_base.source_phase6_projection_overrides import projections as formula_projections
    result=entries.run(query_name,query_parameters,reader,additional_projection=formula_projections(query_name) if calculate else (),**p)
    if calculate:
        from plugins.erp_base.source_phase6_projection_formulas import calculate as project_formulas
        from plugins.erp_base.source_phase6_projection_context import ProjectionContext
        result=project_formulas(result,entries.definition(result['entry'])['fields'],ProjectionContext(result,reader,query_parameters,p['include_retained']))
    if not export:return success(web_values(result))
    output=io.StringIO(newline='');writer=csv.writer(output)
    writer.writerow([c['name'] for c in result['columns']])
    # \N是SQL NULL；空字符串原样为空。重复行及同名列全部写出。
    writer.writerows(['\\N' if cell is None else cell.replace('\\','\\\\') if isinstance(cell,str) else cell for cell in row] for row in result['rows'])
    response=HttpResponse('\ufeff'+output.getvalue(),content_type='text/csv; charset=utf-8')
    response['Content-Disposition']='attachment; filename="original-entry.csv"'
    return response


@lru_cache(maxsize=1)
def templates():
    return json.loads(gzip.decompress((Path(__file__).resolve().parent.parent/'data').joinpath('source_phase6_templates.json.gz').read_bytes()))


def template_view(view):
    from plugins.erp_base.source_foundation_api import require_original_admin
    require_original_admin(view.request)
    p=parameters(view,{'index':serializers.IntegerField(min_value=0,max_value=len(templates())-1),
        'format':serializers.ChoiceField(choices=['Template','TemplateXml','Layout','Proof']),
        'print_key':serializers.CharField(default=None,allow_null=True,allow_blank=True,trim_whitespace=False),
        'print_null_key':serializers.BooleanField(default=False),
        'parameters':serializers.DictField(default=dict),
        'load_records':serializers.BooleanField(default=False),
        'include_retained':serializers.BooleanField(default=True)})
    row=templates()[p['index']]
    if p['format']=='Layout':
        from plugins.erp_base.source_phase6_layouts import describe
        from plugins.erp_base.source_phase6_rendering import requirements
        layout=describe(row);layout['proof_issues']=requirements(row)
        return success(layout)
    if p['format']=='Proof':
        from plugins.erp_base.source_phase6_rendering import render, requirements, reference_columns
        from plugins.erp_base.source_phase6_layouts import describe
        issues=requirements(row)
        if issues:raise ValidationError({'layout':issues})
        name=describe(row)['data_member']
        from plugins.erp_base.source_phase6_print_sources import projections
        result=entries.run(name,p['parameters'],entries.reader(view.request),
                           load_records=p['load_records'],include_retained=p['include_retained'],additional_projection=projections(name))
        from plugins.erp_base.source_phase6_print_sources import attach,select_parent
        from plugins.erp_base.source_phase6_layouts import parse_xml
        root,_=parse_xml(base64.b64decode(row['TemplateXml']))
        result=select_parent(row['RptID'],result,p['print_key'],p['print_null_key'])
        result=attach(root,result,entries.reader(view.request),p['parameters'],p['include_retained'])
        return success(web_values(render(row,reference_columns(row,result,entries.reader(view.request)))))
    value=row[p['format']]
    if value is None:raise ValidationError({'format':'此条原配置没有该格式，其他模板原文仍保留。'})
    response=HttpResponse(base64.b64decode(value),content_type='application/octet-stream')
    response['Content-Disposition']='attachment; filename="original-template.'+('xml' if p['format']=='TemplateXml' else 'cs')+'"'
    return response
