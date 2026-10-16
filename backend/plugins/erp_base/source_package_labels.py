"""sp_AuTo_RecordYield：投坯条码回写、全包装条码标签同步和逐字段撤回。"""
import re
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from .source_stock_services import raw
from .source_business_updates import matching
from .source_package_operations import reader, rows, scoped, check_scope, effect
from .source_station_yield import normalized
from .source_continuation import origin, save_effect
from .source_execution_state import require_available
from .source_operation_effects import change, restore


JOB_FIELDS = ['ColorNum', 'ColorID', 'CustColorNum', 'ContractNo', 'FabricNO2', 'CustSelfNo']
LABEL_FIELDS = ['CustomerID', 'CustomerGrayName', 'BarCode', 'CustColorNum', 'ShipMentType',
                'CustQty', 'NetKg', 'JobSheetNo', 'RollNo', 'DB2Code']


def varchar(value, size):
    # Chinese_PRC_CI_AS 的 varchar 按 CP936 字节计长，变量赋值保留原截断。
    return None if value is None else value.encode('gbk', errors='replace')[:size].decode('gbk', errors='ignore')


def label_code(values, product_code):
    color, job, roll = (values[name] for name in ['CustColorNum', 'JobSheetNo', 'RollNo'])
    quantity = values['CustQty'] if normalized(values['ShipMentType']) in [None, '', '1'] else values['NetKg']
    if color is None or job is None or roll is None or quantity is None:
        return None
    digits = format(quantity, '.1f').replace('.', '')[:10]
    return (product_code + '000000')[:6] + ('0000' + color[:4].strip(' '))[-4:] + ('000' + digits)[-3:] + job + ('000' + roll)[-3:]


def plan(job, query=reader, lock=False, series=None):
    def selected(name, module, **values):
        result = matching(rows(name, reader, module), **values).order_by('pk')
        return list(result.select_for_update() if lock else result)

    series = varchar(raw(job, 'SheetSeries') if series is None else series, 50)
    jobs = selected('JobSheet', 'erp_production', SheetSeries=series)
    gray = selected('JobGrayRecord', 'erp_production', SheetSeries=series)
    products = []
    product_candidates = []
    for parent in jobs:
        for product in selected('PProduct', 'erp_base', ProdID=raw(parent, 'CustSelfProduct')):
            products.append(product)
            product_candidates.append({'job_id': parent.pk, 'product_id': product.pk, 'NameC': raw(product, 'NameC')})
    product_name = varchar(product_candidates[-1]['NameC'], 200) if product_candidates else None
    packages = {}
    gray_candidates = {}
    for source in gray:
        for item in selected('RecordYield', 'erp_warehouse', GrayBarCode=raw(source, 'GrayBarCode')):
            packages[item.pk] = item
            gray_candidates.setdefault(item.pk, []).append(source.pk)
    updates = {}
    state = {}
    for pk, item in packages.items():
        values = {name: raw(item, name) for name in LABEL_FIELDS}
        updates[pk] = {}
        if jobs:
            parent = jobs[-1]
            updates[pk] = {name: raw(parent, name) for name in JOB_FIELDS}
            updates[pk].update(JobSheetNo=raw(parent, 'SheetNo'), JobDetailNo=raw(parent, 'SheetNo'), CustomerGrayName=product_name)
            values.update(updates[pk])
        state[pk] = values
    # #t 在第一轮 UPDATE 后取得快照；游标仍保留重复投坯连接，不按条码去重。
    cursor = []
    targets = dict(packages)
    for pk in sorted(packages):
        values = state[pk]
        name = values['CustomerGrayName']
        code = varchar(name.split('#', 1)[0].strip(' '), 50) if name is not None and '#' in name else '000000'
        barcode = varchar(values['BarCode'], 50)
        eligible = normalized(varchar(values['CustomerID'], 50)) == ''
        matched = selected('RecordYield', 'erp_warehouse', BarCode=barcode) if eligible else []
        for gray_id in gray_candidates[pk]:
            cursor.append({'source_id': pk, 'gray_id': gray_id, 'CustomerID': values['CustomerID'],
                'BarCode': barcode, 'ProdCode': code, 'eligible': eligible, 'target_ids': [row.pk for row in matched]})
            for target in matched:
                targets[target.pk] = target
                target_values = state.get(target.pk, {name: raw(target, name) for name in LABEL_FIELDS})
                updates.setdefault(target.pk, {})['DB2Code'] = label_code(target_values, code)
    check_scope([job, *jobs, *gray, *products, *targets.values()], query)
    progress_sources = {}
    for pk, item in targets.items():
        if not updates[pk]:
            continue
        # 沿用E44：只维护本次实际命中包装，不重放全库清空/负数归零。
        roll = raw(item, 'RollNo')
        if roll is not None and re.fullmatch(r'\s*[+-]?[0-9]+\s*', roll) and -2147483648 <= int(roll) <= 2147483647:
            updates[pk]['Scroll'] = str(int(roll))
        number = updates[pk].get('JobSheetNo', raw(item, 'JobSheetNo'))
        if normalized(number or '') != normalized(updates[pk].get('JobDetailNo', raw(item, 'JobDetailNo')) or ''):
            updates[pk]['JobDetailNo'] = number
        for parent in selected('JobSheet', 'erp_production', SheetNo=number):
            progress_sources[(parent._meta.label, parent.pk)] = parent
            for process in selected('JobProcess', 'erp_production', SheetSeries=raw(parent, 'SheetSeries')):
                progress_sources[(process._meta.label, process.pk)] = process
        for employee in selected('HEmployee', 'erp_base', EmpID=raw(item, 'EmpID')):
            progress_sources[(employee._meta.label, employee.pk)] = employee
    check_scope(progress_sources.values(), query)
    output = [{'record_id': pk, 'legacy_id': item.legacy_id, 'gray_ids': gray_candidates.get(pk, []),
        'outside_gray_scope': pk not in packages, 'before': {name: raw(item, name) for name in updates[pk]},
        'after': updates[pk]} for pk, item in sorted(targets.items())]
    report = {'report': '自动包装标签同步范围', 'target_series': series, 'rows': output, 'result_rows': cursor,
        'candidate_rows': [{'job_id': item.pk, 'SheetNo': raw(item, 'SheetNo'), 'selected': item.pk == jobs[-1].pk} for item in jobs],
        'supplemental_rows': product_candidates + [{'source_entity': item._meta.label, 'record_id': item.pk,
            'issue': '本次包装开工和当前工序回写的关联来源'} for item in progress_sources.values()],
        'notes': ['先按投坯GrayBarCode回写，再按BarCode更新全部命中包装；NULL不相等，空条码及重复条码保留原范围。',
            '原无序变量和游标改为项目记录ID升序，最后候选生效；全部候选保留，差异见E75。',
            '同步维护实际命中包装的Scroll/JobDetailNo及GX98开工；不清空品名、不把负净重归零，沿用E44。',
            '这里只更新包装字段和DB2Code，不代表标签已打印或设备已确认。']}
    return report, targets, [*jobs, *gray, *products, *progress_sources.values()]


def preview(job, query=reader, series=None):
    job = query(job.SOURCE_TABLE, job._meta.app_label).get(pk=job.pk)
    return plan(job, query, series=series)[0]


@transaction.atomic
def synchronize(job, actor, at, reason, query=reader, series=None):
    job = scoped(job, query)
    require_available(job)
    previous = effect(job, 'package_label_sync')
    if previous is not None and previous['state'] == 'applied':
        raise ValidationError({'source': '请先撤回本工卡上次标签同步，再重新同步。'})
    report, targets, sources = plan(job, query, lock=True, series=series)
    changes = []
    for row in report['rows']:
        item = targets[row['record_id']]
        require_available(item)
        if row['after']:
            change(item, row['after'], changes, actor, reason)
    from .source_chain_reverse import capture
    from .source_packaging_flow import start_packing
    with capture() as progress_changes:
        for row in report['rows']:
            if not row['after']:
                continue
            item = targets[row['record_id']]
            item.refresh_from_db()
            start_packing(item, actor)
    check_scope([apps.get_model(row['entity']).objects.get(pk=row['id']) for row in progress_changes], query)
    changes.extend(progress_changes)
    save_effect(job, 'package_label_sync', {'state': 'applied', 'at': at, 'reason': reason,
        'changes': changes, 'report': report, 'sources': [origin(item) for item in sources]}, actor, reason)
    return report


@transaction.atomic
def undo(job, actor, at, reason, query=reader):
    job = scoped(job, query)
    require_available(job)
    value = effect(job, 'package_label_sync')
    if value is None or value['state'] != 'applied':
        raise ValidationError({'source': '本工卡没有可撤回的标签同步。'})
    targets = [apps.get_model(row['entity']).objects.select_for_update().get(pk=row['id']) for row in value['changes']]
    check_scope(targets, query)
    for item in targets:
        require_available(item)
    restore(value['changes'], actor, reason)
    save_effect(job, 'package_label_sync', {**value, 'state': 'reversed', 'reversed_at': at, 'reverse_reason': reason}, actor, reason)
    return job


def related_operations(nodes):
    """按实际办理审计顺序撤回涉及执行链的标签同步，包括跨卡同条码目标。"""
    from .source_context import SourceDocumentContext
    from .models import BusinessAction
    ids = {item.pk for item in nodes if item.SOURCE_TABLE == 'RecordYield'}
    operations = []
    for context in SourceDocumentContext.objects.filter(effects__package_label_sync__state='applied'):
        value = context.effects['package_label_sync']
        if any(row['entity'] == 'erp_warehouse.SourceDyeRecordYield' and row['id'] in ids for row in value['changes']):
            last = BusinessAction.objects.filter(entity=context._meta.label, object_id=context.pk, action='package_label_sync').latest('pk')
            operations.append((last.pk, context.object_id))
    return [job_id for _, job_id in sorted(operations, reverse=True)]
