"""原表字段决定原键；批次和提取行定位一次抽取中的记录。"""
import json


def is_historical(item):
    if item.source_batch_id is not None:
        return True
    if item.SOURCE_TABLE not in {'WProcessBak','WProcessStepBak','JobShiftEmpBak'} or item.pk is None:
        return False
    from .source_context import SourceDocumentContext
    batch=SourceDocumentContext.objects.filter(entity=item._meta.label,object_id=item.pk).values_list(
        'effects__work_archive_copy__source__source__source_batch',flat=True).first()
    return batch is not None


def reference(item):
    from .business import FactsEncoder
    value={
        'schema': item.SOURCE_SCHEMA,
        'table': item.SOURCE_TABLE,
        'key': {name: getattr(item, item.SOURCE_FIELDS[name]) for name in item.SOURCE_KEY},
        'batch_id': item.source_batch_id,
        'row': item.source_row,
    }
    return json.loads(json.dumps(value,cls=FactsEncoder))
