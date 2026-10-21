"""可办理的编号字段及类别；不能把外键、流水身份或语义枚举当作编码。"""
import json
from functools import lru_cache
from pathlib import Path
from django.apps import apps
from django.db import models


SUGGESTIONS = json.loads(Path(__file__).with_name('numbering_suggestions.json').read_text(encoding='utf8'))


@lru_cache(maxsize=1)
def registry():
    result = {}
    for rule in SUGGESTIONS:
        model = apps.get_model(rule['target_model'])
        key = (model._meta.label, rule['target_field'])
        spec = result.setdefault(key, {'model': model, 'scopes': []})
        filters = {model.SOURCE_FIELDS[old]: value for old, value in rule['source_filters'].items()}
        spec['scopes'].append({'key': rule['scope_key'], 'title': rule['name'], 'filters': filters, 'entry_name': ''})
    for label, old, title in [('erp_base.SourceDyePProduct', 'ProdID', '成品规格'),
                            ('erp_quality.SourceDyePTestItem', 'ItemID', '质量试验项目'),
                            ('erp_base.SourceDyePDyeProgram', 'ProgramID', '染色程序'),
                            ('erp_base.SourceDyeSCorpTitle', 'Code', '公司抬头'),
                            ('erp_base.SourceDyePMachine', 'MachineID', '机台编码')]:
        model = apps.get_model(label)
        key = model.SOURCE_FIELDS[old]
        result[(label, key)] = {'model': model, 'scopes': [{'key': 'all', 'title': title, 'filters': {}, 'entry_name': ''}]}
    # 业务单号可明确选择简单规则；不预装规则，日期、续号等原规则继续使用。
    from .source_entry_registry import ENTRY_RULES
    import gzip
    entries_catalog = json.loads(gzip.decompress(Path(__file__).with_name('source_phase6_catalog.json.gz').read_bytes()))['entries']
    entries_catalog = {entry['table']['DataTableName']: entry for entry in entries_catalog}
    for label, entries in ENTRY_RULES.items():
        model = apps.get_model(label)
        if model._meta.app_label not in {'erp_sales', 'erp_purchase', 'erp_sampling', 'erp_production', 'erp_warehouse', 'erp_quality'}:
            continue
        key = getattr(model, 'SOURCE_FIELDS', {}).get('SheetNo')
        if key is None or key in model.SOURCE_IDENTITIES or not isinstance(model._meta.get_field(key), models.CharField):
            continue
        if model.SOURCE_TABLE in {'HS_JobsheetNo', 'OtherIn', 'SalaryChanges'}:
            continue
        scopes = [{'key': 'entry:' + entry, 'title': definition['title'], 'filters': {}, 'entry_name': entry}
                  for entry, definition in entries.items() if 'SheetNo' in definition['number_fields']
                  and not entries_catalog[entry]['finance']]
        if scopes:
            result.setdefault((model._meta.label, key), {'model': model, 'scopes': scopes})
    return result


def specification(model_label, field):
    key = (model_label, field)
    if key not in registry():
        from django.core.exceptions import ValidationError
        raise ValidationError({'target_field': '请选择已登记的业务编号字段；主键、关联码和明细流水不参与简单编号。'})
    return registry()[key]


def scope_definition(model_label, field, key):
    from django.core.exceptions import ValidationError
    for scope in specification(model_label, field)['scopes']:
        if scope['key'] == key:
            return scope
    raise ValidationError({'scope_key': '请选择该编号字段的适用类别。'})


def catalog():
    groups = {}
    titles = {'p_Dept': '部门', 'h_Employee': '员工', 'p_Gray': '坯纱规格', 'p_Shift': '生产班组',
              'p_DyeCurve': '染色曲线', 'WidthGramWeight': '幅宽克重单位', 'p_Customer': '客户与供应商',
              'p_FieldValid': '分类基础资料', 'p_StorageUnitID': '仓储位置资料', 'p_Stuff': '染化料', 'p_Article': '机物料'}
    titles.update(p_Product='成品规格', p_TestItem='质量试验项目', p_DyeProgram='染色程序', s_CorpTitle='公司抬头', p_Machine='机台')
    titles.update(StuffWeight='染料称料单', DyeRecipe='染色配方', JobSheet='生产工卡',
                  GrayIn='胚纱入库单', GrayOut='胚纱出库单', SemiIn='半成品入库单', SemiOut='半成品出库单',
                  ProdIn='成品入库单', ProdOut='成品出库单', WDefect='质量评审与检验',
                  ProdTest='生产质量检测', DyeLabColor='打样任务单', DyeLab='打样记录',
                  ArticleIn='机物料入库单', ArticleOut='机物料出库单', StuffIn='染化料入库单', StuffOut='染化料出库单')
    for (label, field), spec in registry().items():
        model = spec['model']
        business_titles = list(dict.fromkeys(scope['title'] for scope in spec['scopes']))
        title = titles.get(model.SOURCE_TABLE, '销售订单' if model.SOURCE_TABLE == 'OrderMain' else ' / '.join(business_titles))
        group = groups.setdefault(label, {'value': label, 'title': title, 'fields': []})
        group['fields'].append({'value': field, 'title': '单据编号' if field == 'old_sheet_no' else '编码' if field == 'old_code' else '客户/供应商编码' if model.SOURCE_TABLE == 'p_Customer' else str(model._meta.get_field(field).verbose_name),
            'max_length': model._meta.get_field(field).max_length, 'scopes': spec['scopes'],
            'can_change': not any(s['entry_name'] for s in spec['scopes']),
            'change_capability': '单据编号更改服务暂未完整对应，当前不开放更改单号。' if any(s['entry_name'] for s in spec['scopes'])
                else '仅未被引用的记录可更改；已被引用的编号须有完整专用变更服务后才能办理。'})
    return list(groups.values())
