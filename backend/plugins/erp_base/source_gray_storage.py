"""坯料库位调整：拆分实际收料明细、移动指定细码和对应库存，反审逐项还原。"""
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db.models.functions import Upper, RTrim
from django.utils import timezone
from .business import locked, persist, record, snapshot
from .source_context import SourceDocumentContext
from .source_numbers import reserve
from .source_calculations import decimal
from .source_stock_services import raw, detail_rows, copy_fields


def model(table):
    return apps.get_model('erp_warehouse.SourceDye' + table)


def matching(query, field, value):
    return query.none() if value is None else query.alias(match=Upper(RTrim(field))).filter(match=value.rstrip(' ').upper())


def change(item, values, effects, actor):
    before = snapshot(item)
    for key, value in values.items():
        setattr(item, key, value)
    persist(item, actor)
    after = snapshot(item)
    effects.append({'entity': item._meta.label, 'id': item.pk,
                    'before': {key: before[key] for key in values},
                    'after': {key: after[key] for key in values}})
    record(item, 'gray_storage_move', before, actor, '坯料库位调整的实际来源回写')


def undo(context, actor):
    for effect in reversed(context.effects.get('gray_storage_changes', [])):
        item = locked(apps.get_model(effect['entity']).objects.get(pk=effect['id']))
        matches = []
        for key, value in effect['after'].items():
            field = item._meta.get_field(key)
            expected = value if field.is_relation else field.to_python(value)
            matches.append(field.value_from_object(item) == expected)
        if not all(matches):
            raise ValidationError({'source': '转仓影响已被后续业务改变，请先撤销后续办理，再反审此转仓单。'})
        before = snapshot(item)
        for key, value in effect['before'].items():
            field = item._meta.get_field(key)
            setattr(item, field.attname, value if field.is_relation else field.to_python(value))
        persist(item, actor)
        record(item, 'reverse_gray_storage', before, actor, '还原本次库位调整实际改变的字段')
    context.effects = {**context.effects, 'gray_storage_changes': []}


def derive(item, context, actor):
    incoming = model('GrayInDetail')
    records = model('GrayInRecord')
    books = model('GrayStockBook')
    changes = []
    derived = {}
    stock_rows = []
    for line in detail_rows(item, 'GrayStorageAdjustDetail'):
        receipt = raw(line, 'ReceSheetNo')
        sources = matching(incoming.objects.select_for_update(), 'old_rece_sheet_no', receipt)
        # 当前明细LotNo保存原入库单的SheetSeries，旧过程也以此定位库存和撤销来源。
        sources = matching(sources, 'old_sheet_series', raw(line, 'LotNo')).order_by('pk')
        source_list = list(sources)
        if not source_list:
            raise ValidationError({'source': '库位调整明细必须对应实际收料单号及收料批次；原明细可保存，办理时请补明实际来源。'})
        for source in source_list:
            prefix = receipt[:6].replace('Z', '') if receipt.startswith('Z') else 'Z' + receipt[:6]
            def initial():
                values = incoming.objects.filter(old_rece_sheet_no__startswith=prefix).values_list('old_rece_sheet_no', flat=True)
                return max((int(value[len(prefix):]) for value in values if value[len(prefix):].isdigit()), default=0)
            number = prefix + str(reserve(source, 'old_rece_sheet_no', {'kind': 'gray_storage', 'prefix': prefix}, initial, actor)).zfill(4)
            values = {new: getattr(source, new) for new in source.SOURCE_FIELDS.values()}
            values.update(old_rece_sheet_no=number, old_area=raw(line, 'ToArea'),
                          old_storage_unit_ids=raw(line, 'ToStorageUnitIDs'), old_rolls=raw(line, 'Rolls'),
                          old_weight_qty=raw(line, 'WeightQty'), old_length_qty=raw(line, 'LengthQty'),
                          old_ori_rece_sheet_no=receipt,
                          old_remarks=None if raw(line, 'Remarks') is None else '▲原单号：' + receipt + raw(line, 'Remarks'))
            split = persist(incoming(**values, source_parent_1=source.source_parent_1), actor)
            derived.setdefault(split._meta.label, []).append(split.pk)
            SourceDocumentContext.objects.create(entity=split._meta.label, object_id=split.pk,
                entry_name='GrayInDetail', creator=actor, modifier=actor,
                effects={'derived_from': {'entity': item._meta.label, 'id': item.pk}})
            record(split, 'derive_gray_storage', {'exists': False}, actor, '转仓拆分实际收料明细')
            quantities = {}
            for old in ['Rolls', 'WeightQty', 'LengthQty']:
                original, moved = raw(source, old), raw(line, old)
                result = None if original is None or moved is None else decimal(original) - decimal(moved)
                quantities[source.SOURCE_FIELDS[old]] = 0 if result is None and old != 'Rolls' else result
            change(source, quantities, changes, actor)
            barcode_rows = model('GrayStorageAdjustRecord').objects.filter(source_parent_1=line)
            codes = list(barcode_rows.values_list('old_rece_sheet_no', flat=True))
            for code in codes:
                selected = matching(records.objects.select_for_update().filter(source_parent_1=source), 'old_bar_code', code)
                for tag in selected:
                    change(tag, {'old_rece_sheet_no': number, 'source_parent_1': split}, changes, actor)
            source_books = matching(books.objects.select_for_update(), 'old_sheet_series', raw(source, 'SheetSeries'))
            source_books = matching(matching(source_books, 'old_rece_sheet_no', receipt), 'old_detail_no', receipt)
            for book in source_books:
                values = {}
                for old, quantity in [('InRolls', 'Rolls'), ('InWeightQty', 'WeightQty'), ('InLengthQty', 'LengthQty')]:
                    actual, moved = raw(book, old), raw(line, quantity)
                    values[book.SOURCE_FIELDS[old]] = None if actual is None or moved is None else decimal(actual) - decimal(moved)
                change(book, values, changes, actor)
            parent = source.source_parent_1
            if parent is None:
                raise ValidationError({'source': '所选收料明细的实际收料表头关系尚未明确，请补齐后办理。'})
            stock_rows.append(('GrayStockBook', {**copy_fields(parent, ['SheetDate', 'SheetKind', 'BusinessUnitID', 'CustomerID', 'FactID', 'WareHouseID', 'SalerGroupID', 'SheetNo', 'SheetSeries']),
                'BookDate': raw(parent, 'SheetDate'), 'BookKind': raw(parent, 'SheetKind'), 'CurrDate': timezone.now(),
                **copy_fields(source, ['GrayID', 'Spec', 'LotNo']), 'StorageUnitIDs': raw(line, 'ToStorageUnitIDs'),
                'ReceSheetNo': number, 'DetailNo': number, 'JobSheetNo': None,
                'InRolls': raw(line, 'Rolls'), 'InLengthQty': raw(line, 'LengthQty'), 'InWeightQty': raw(line, 'WeightQty'),
                'OutRolls': 0, 'OutLengthQty': 0, 'OutWeightQty': 0, 'Price': 0}))
            change(line, {'old_spec': number}, changes, actor)
    # 库存表没有SheetDate/SheetKind列，原SELECT只是它们的值来源。
    for table, values in stock_rows:
        del values['SheetDate'], values['SheetKind']
    context.effects = {**context.effects, 'gray_storage_changes': changes, 'derived_records': derived}
    persist(context, actor)
    return stock_rows
