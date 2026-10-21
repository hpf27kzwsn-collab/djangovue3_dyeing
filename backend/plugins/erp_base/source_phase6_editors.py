"""旧字段绑定的资料选择与组合框；重复代码按返回行位置展示。"""
import json
from pathlib import Path
from django.core.exceptions import ValidationError
from .source_phase6_entries import definition
from .source_foundation_queries import lookup, combo, LOOKUPS
from .source_trial_steps import equal

CONFIG = json.loads(Path(__file__).with_name('source_phase6_field_links.json').read_text(encoding='utf8'))

# 原关系缺一端；这里只列已核实两边原字段及查询投影的明确实现，原配置原样保留。
RECONSTRUCTED_FILTERS = {
    'A026': ('JobSheetNo', 'JobSheetNo'),
    'A031': ('JobSheetNo', 'JobSheetNo'),
    'B080': ('StationID', 'StationID'),
    'B128': ('CustomerID', 'CustomerID'),
    'B133': ('CustomerID', 'CustomerID'),
    'B145': ('SheetNo', 'SheetNo'),
    'B146': ('SheetNo', 'JobSheetNo'),
    'B176': ('CurveID', 'CurveID'),
    'B186': ('JobSheetNo', 'JobSheetNo'),
    'B210': ('ProdID', 'ProdID'),
    'B305': ('CustomerID', 'CustomerID'),
}


def filter_mapping(relation):
    master, target = relation['MasterFilterField'], relation['LookupFilterField']
    original = {'MasterFilterField':master, 'LookupFilterField':target}
    reconstructed = (not master or not target) and relation['LookupID'] in RECONSTRUCTED_FILTERS
    if reconstructed:master, target = RECONSTRUCTED_FILTERS[relation['LookupID']]
    return {'MasterFilterField':master, 'LookupFilterField':target,
            'original':original, 'mapping_source':'explicit_reconstruction' if reconstructed else 'original'}


def options(entry, field, filter_text, reader, context=None):
    spec = definition(entry)
    if spec['finance']:
        raise ValidationError({'entry': '独立财务入口暂缓。'})
    rules = [f for f in spec['fields'] if f['FieldName'] == field]
    if len(rules) != 1:
        raise ValidationError({'editor_field': '此字段没有唯一的原编辑器配置。'})
    rule = rules[0];kind = rule['EditorKind'];code = rule['EditorID']
    if kind in ['Lookup','Lookup_NoCheck']:
        if code not in LOOKUPS:
            raise ValidationError({'editor_field': '原资料选择编号没有对应定义：'+str(code)})
        columns = [c for c in CONFIG['lookup_columns'] if c['LookUpID'] == code]
        relations = [r for r in CONFIG['lookups'] if r['LookupID'] == code]
        filters = []
        for relation in relations:
            mapping = filter_mapping(relation)
            master, target = mapping['MasterFilterField'], mapping['LookupFilterField']
            if not master and not target:continue
            state = 'incomplete_configuration' if not master or not target else 'missing_context' if context is None or master not in context else 'applied'
            filters.append({**mapping,'state':state,
                            **({'value':context[master]} if state=='applied' else {})})
        fields = [c['FieldName'] for c in columns]+[f['LookupFilterField'] for f in filters if f['state']=='applied']
        extra = list(dict.fromkeys(name for name in fields
                                 if name not in [LOOKUPS[code]['KeyField'], LOOKUPS[code]['DisplayField']]))
        result = lookup(code,filter_text,extra,reader)
        for item in filters:
            if item['state']!='applied':continue
            field_name = item['LookupFilterField']
            column = 'id' if field_name==LOOKUPS[code]['KeyField'] else 'text' if field_name==LOOKUPS[code]['DisplayField'] else field_name
            result['rows'] = [row for row in result['rows'] if equal(row[column],item['value'])]
        result['original_filters'] = filters
        result['columns'] = columns
    elif kind in ['DBCombo','DBCombo_Edit']:
        result = combo(code,filter_text,reader)
        result['implemented'] = True;result['columns'] = []
    else:
        raise ValidationError({'editor_field': '此原编辑器不是Lookup或DBCombo：'+str(kind)})
    result.update(entry=entry,field=field,editor_id=code,editor_kind=kind)
    result['notes'] = [*result.get('notes',[]), '选择行只回填当前字段的原代码。完整上下文配置按等值筛选，NULL不匹配；缺字段或未提供上下文的关系单独标明，原候选不删除。此比较方式为明确替代，见E171。']
    return result
