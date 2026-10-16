"""删列前核对既有来源；这是一次性迁移代码，不参与当前业务识别。"""
import json


def preserve_sources(apps, schema_editor):
    alias=schema_editor.connection.alias
    maps=apps.get_model('erp_base','LegacyObjectMap').objects.using(alias)
    contexts=apps.get_model('erp_base','SourceDocumentContext').objects.using(alias)
    for model in apps.get_models():
        names={f.name for f in model._meta.fields}
        if not model._meta.app_label.startswith('erp_') or 'legacy_id' not in names:
            continue
        records=model.objects.using(alias).exclude(legacy_id=None)
        if 'source_batch' in names:
            # 有批次的原行已经以原字段和提取行号定位，不重写数千万条记录。
            records=records.filter(source_batch=None)
        for item in records.iterator(chunk_size=2000):
            key=json.loads(item.legacy_id)
            if model._meta.model_name=='qualityquantitysource':
                if item.detail_no!=key['key']['DetailNo']:
                    raise ValueError(f'质量明细原键不一致：{item.pk}')
                continue
            if model._meta.model_name=='sourcebusinessparameter':
                if item.name!=key['key']['ParamName']:
                    raise ValueError(f'业务参数原键不一致：{item.pk}')
                context,_=contexts.get_or_create(entity=model._meta.label,object_id=item.pk,
                    defaults={'entry_name':'parameter_adoption','effects':{}})
                context.effects['parameter_source']={'schema':key['schema'],'table':key['table'],'field':'ParamName'}
                context.save(using=alias,update_fields=['effects'])
                continue
            matches=maps.filter(target_model=model._meta.label,target_id=item.pk,
                source_table__schema_name=key['schema'],source_table__table_name=key['table'],source_key=key['key'])
            if not matches.exists():
                raise ValueError(f'删列前需补齐来源映射：{model._meta.label}#{item.pk}')
            if 'source_batch' in names:
                origins=list(matches.values_list('source_table__batch_id','row_number').distinct())
                if len(origins)!=1:
                    raise ValueError(f'原行来源批次存在多项：{model._meta.label}#{item.pk}')
                item.source_batch_id,item.source_row=origins[0]
                item.save(using=alias,update_fields=['source_batch','source_row'])


def remove_menu_columns(apps,schema_editor):
    fields=apps.get_model('system','MenuField').objects.using(schema_editor.connection.alias)
    fields.filter(model__startswith='erp_',field_name='legacy_id').delete()
    fields.filter(model='erp_quality.QualityQuantitySource',field_name='header_legacy_id').update(
        field_name='header_sheet_series',title='原匹配表头流水')
