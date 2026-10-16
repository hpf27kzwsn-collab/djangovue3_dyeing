"""RecordYield_Add替换新增及Sp_RecordYieldQuery排序配对；原行留档，差异见E56/E57。"""
from collections import defaultdict
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from .business import locked, snapshot
from .source_business_updates import matching
from .source_context import SourceDocumentContext
from .source_continuation import origin, save_effect
from .source_execution_state import active, require_available
from .source_gray_split_merge import active as gray_active
from .source_operation_effects import change, restore
from .source_stock_services import raw


ADD_FIELDS = ['JobSheetNo', 'MainNo', 'DetailNo', 'RollNo', 'Kg', 'ColorNum', 'CustomerID',
    'SumAssignedWeightQty', 'SumAssignedRolls', 'Scroll', 'PackBag', 'AddWeigth',
    'CustomerGrayName', 'ColorID', 'Spec', 'WidthSpec', 'WeightSpec', 'ProdID', 'Qty', 'CountUnit']


def reader(name, module):
    return apps.get_model(module + '.SourceDye' + name).objects.all()


def rows(name, query=reader, module='erp_warehouse'):
    return active(query(name, module))


def effect(item, name):
    context = SourceDocumentContext.objects.filter(entity=item._meta.label, object_id=item.pk).first()
    return None if context is None else context.effects.get(name)


def scoped(item, query):
    return locked(get_object_or_404(query(item.SOURCE_TABLE, item._meta.app_label), pk=item.pk))


def check_scope(items, query):
    groups = defaultdict(set)
    for item in items:
        groups[(type(item).__name__.removeprefix('SourceDye'), item._meta.app_label)].add(item.pk)
    for (name, module), ids in groups.items():
        if query(name, module).filter(pk__in=ids).count() != len(ids):
            raise ValidationError({'scope': '当前权限没有覆盖本次包装操作的全部关联记录，不能只处理其中一部分。'})


def lock_jobs(number, query):
    jobs = list(matching(rows('JobSheet', module='erp_production'), SheetNo=number).order_by('pk'))
    check_scope(jobs, query)
    for job in jobs:
        require_available(locked(job))
    return jobs


def replacement_rows(item, query=reader):
    return matching(rows('RecordYield', query), JobSheetNo=raw(item, 'JobSheetNo'), RollNo=raw(item, 'RollNo'))


def preview_replace(item, query=reader):
    selected = list(replacement_rows(item, query).order_by('pk'))
    return {'report': '同工卡同卷号包装替换预览', 'rows': [
        {'record_id': row.pk, 'legacy_id': row.legacy_id, 'JobSheetNo': raw(row, 'JobSheetNo'),
         'RollNo': raw(row, 'RollNo'), 'BarCode': raw(row, 'BarCode'), 'Kg': raw(row, 'Kg')}
        for row in selected], 'notes': [
        '按原JobSheetNo与RollNo匹配全部活动原行；NULL不与NULL相等。',
        '替换仅改变包装活动记录，原收发、库存、打印及签收事实保留；实际收发纠错另行办理。',
        '新行采用原过程20个参数列，未传修改值沿用所选行参数；最新表必填CheckNo沿用所选行，其余旧列不复制。']}


@transaction.atomic
def replace_package(item, actor, at, reason, query=reader, **overrides):
    from .source_services import write
    from .source_chain_reverse import capture
    item = scoped(item, query)
    require_available(item)
    lock_jobs(raw(item, 'JobSheetNo'), query)
    selected = list(replacement_rows(item).select_for_update().order_by('pk'))
    check_scope(selected, query)
    for row in selected:
        require_available(row)
    model = type(item)
    # 只采用原过程实际接收的参数；拼接NULL条码继续由已有INSERT规则补号。
    values = {model.SOURCE_FIELDS[key]: raw(item, key) for key in ADD_FIELDS}
    # 当前CheckNo非空且无默认值，旧过程漏列；沿用明确来源而非填造订单明细号。
    values['old_check_no'] = raw(item, 'CheckNo')
    values.update(overrides)
    number, roll = values['old_job_sheet_no'], values['old_roll_no']
    values['old_bar_code'] = None if number is None or roll is None else number + roll
    prior = [{'origin': origin(row), 'previous': effect(row, 'package_retained')} for row in selected]
    # 留档在新增前生效，包装汇总不同时计入新旧两份。
    for row in selected:
        save_effect(row, 'package_retained', {'active': True, 'state': 'replaced', 'at': at, 'reason': reason}, actor, reason)
    with capture() as changes:
        result = write(model, values, actor=actor)
    raw_changes = [entry for entry in changes if 'before' in entry and not
        (entry['entity'] == result._meta.label and entry['id'] == result.pk)]
    check_scope([apps.get_model(entry['entity']).objects.get(pk=entry['id']) for entry in raw_changes], query)
    for row in selected:
        save_effect(row, 'package_retained', {'active': True, 'state': 'replaced', 'replacement_id': result.pk,
            'at': at, 'reason': reason}, actor, reason)
    result.refresh_from_db()
    save_effect(result, 'package_replacement', {'state': 'applied', 'at': at, 'reason': reason,
        'template': origin(item), 'parameters': values, 'retained': prior, 'changes': raw_changes,
        'after': origin(result), 'receipts_before': downstream(result)}, actor, reason)
    return result


def downstream(item):
    """原实称删除校验按条码；明确新入库关系同时按记录ID核对。"""
    records = matching(rows('ProdInRecord'), ProdBarCode=raw(item, 'BarCode'))
    heads = SourceDocumentContext.objects.filter(effects__package_receipt_origin__entity=item._meta.label,
        effects__package_receipt_origin__source__id=item.pk).values('object_id')
    return {'records': list(records.order_by('pk').values_list('pk', flat=True)),
        'heads': list(rows('ProdIn').filter(pk__in=heads).order_by('pk').values_list('pk', flat=True))}


def replaced_sources(item, query=reader):
    """用于追溯旧包装派生的实际收发；留档包装本身不再次计量或撤销。"""
    seen = {item.pk}
    pending = [item]
    result = []
    while pending:
        parent = pending.pop()
        value = effect(parent, 'package_replacement')
        if value is None or value['state'] != 'applied':
            continue
        ids = {entry['origin']['source']['id'] for entry in value['retained']} - seen
        for row in query('RecordYield', 'erp_warehouse').filter(pk__in=ids).order_by('pk'):
            seen.add(row.pk); result.append(row); pending.append(row)
    return result


@transaction.atomic
def undo_replace(item, actor, at, reason, query=reader):
    item = scoped(item, query)
    require_available(item)
    value = effect(item, 'package_replacement')
    if value is None or value['state'] != 'applied':
        raise ValidationError({'source': '本行没有可撤回的包装替换。'})
    lock_jobs(raw(item, 'JobSheetNo'), query)
    current_receipts = downstream(item)
    if any(set(current_receipts[key]) - set(value['receipts_before'][key]) for key in current_receipts):
        raise ValidationError({'source': '本包装条码已有活动入库细码或明确入库来源，请先处理实际入库再撤回包装替换。'})
    after = value['after']['source']
    if any(getattr(item, key) != item._meta.get_field(key).to_python(after[key]) for key in item.SOURCE_FIELDS.values()):
        raise ValidationError({'source': '新包装已有后续字段变更，请先撤回该变更再恢复替换前记录。'})
    originals = []
    for entry in value['retained']:
        row = scoped(type(item).objects.get(pk=entry['origin']['source']['id']), query)
        current = effect(row, 'package_retained')
        if current is None or not current['active'] or current.get('replacement_id') != item.pk:
            raise ValidationError({'source': '包装替换关系已有后续操作，请按办理顺序倒序撤回。'})
        # retained自身在正常办理中不可修改，整链等其他办理仍需显式核对。
        context = effect(row, 'chain_cancelled')
        if context is not None and context['active']:
            raise ValidationError({'source': '原包装正在整链撤销中，请先撤回该整链操作。'})
        originals.append((row, entry['previous']))
    check_scope([apps.get_model(entry['entity']).objects.get(pk=entry['id']) for entry in value['changes']], query)
    restore(value['changes'], actor, reason)
    for row, previous in originals:
        save_effect(row, 'package_retained', previous or {'active': False, 'reversed_at': at}, actor, reason)
    save_effect(item, 'package_retained', {'active': True, 'state': 'replacement_undone', 'at': at, 'reason': reason}, actor, reason)
    save_effect(item, 'package_replacement', {**value, 'state': 'reversed', 'reversed_at': at, 'reverse_reason': reason}, actor, reason)
    return item


def text_key(value):
    return None if value is None else value.rstrip(' ').upper()


def sort_key(value):
    return (value is not None, text_key(value) or '')


def pairing(job, query=reader):
    """保留原排序连接所有候选；并列按内部ID排序，多匹配采用最后候选。"""
    number = raw(job, 'SheetNo')
    jobs = list(matching(rows('JobSheet', query, 'erp_production'), SheetNo=number).order_by('pk'))
    packages = sorted(matching(rows('RecordYield', query), JobSheetNo=number),
        key=lambda row: (sort_key(raw(row, 'RollNo')), row.pk))
    partitions = defaultdict(list)
    for head in jobs:
        gray = gray_active(matching(query('JobGrayRecord', 'erp_production'), SheetSeries=raw(head, 'SheetSeries')))
        for row in gray:
            partitions[text_key(raw(head, 'SheetSeries'))].append((row, head))
    indexed = defaultdict(list)
    ordered_gray = []
    for series in sorted(partitions, key=sort_key):
        source = sorted(partitions[series], key=lambda pair: (sort_key(raw(pair[0], 'ReceSheetNo')),
            sort_key(raw(pair[0], 'RollNo')), pair[0].pk, pair[1].pk))
        for rank, (row, head) in enumerate(source, 1):
            candidate = {'record_id': row.pk, 'job_id': head.pk, 'legacy_id': row.legacy_id,
                'SheetSeries': raw(row, 'SheetSeries'), 'ReceSheetNo': raw(row, 'ReceSheetNo'),
                'RollNo': raw(row, 'RollNo'), 'GrayBarCode': raw(row, 'GrayBarCode'),
                'WeightQty': raw(row, 'WeightQty'), 'rank': rank}
            indexed[rank].append(candidate)
            ordered_gray.append(candidate)
    by_barcode = defaultdict(list)
    for rank, package in enumerate(packages, 1):
        code = text_key(raw(package, 'BarCode'))
        if code is not None:
            by_barcode[code].extend({**candidate, 'rank_package_id': package.pk} for candidate in indexed[rank])
    results = []
    for rank, package in enumerate(packages, 1):
        candidates = by_barcode[text_key(raw(package, 'BarCode'))]
        selected = candidates[-1] if candidates else None
        results.append({'record_id': package.pk, 'legacy_id': package.legacy_id, 'RollNo': raw(package, 'RollNo'),
            'BarCode': raw(package, 'BarCode'), 'rank': rank, 'candidate_count': len(candidates),
            'source_id': None if selected is None else selected['record_id'],
            'GrayWeight': None if selected is None else selected['WeightQty'],
            'GrayBarCode': None if selected is None else selected['GrayBarCode'],
            'candidates': candidates, 'matched': selected is not None})
    used = {candidate['record_id'] for result in results for candidate in result['candidates']}
    return {'jobs': jobs, 'packages': packages, 'gray': ordered_gray, 'rows': results,
        'supplemental_rows': [dict(row, issue='没有包装排序连接') for row in ordered_gray if row['record_id'] not in used]}


def preview_pairing(job, query=reader):
    data = pairing(job, query)
    return {'report': '包装与投坯细码排序配对', 'rows': data['rows'], 'supplemental_rows': data['supplemental_rows'],
        'notes': ['包装按RollNo文本顺序，投坯按工卡流水分组、ReceSheetNo及RollNo文本顺序；NULL排前。',
            '重复条码保留全部排序候选；并列按内部ID稳定排序，多候选取最后一条，完整候选留档。',
            '序号超过999继续使用完整序号，原三位转换的溢出行为不用于混配；Unicode排序与旧库排序规则差异见E57。',
            '未配对行保留原GrayWeight和GrayBarCode；不以NULL覆盖，也不补造投坯记录。']}


@transaction.atomic
def apply_pairing(job, actor, at, reason, query=reader):
    job = scoped(job, query)
    require_available(job)
    previous = effect(job, 'package_pairing')
    if previous is not None and previous['state'] == 'applied':
        raise ValidationError({'source': '本工卡已有一次排序配对，请先撤回后再重新配对。'})
    jobs = lock_jobs(raw(job, 'SheetNo'), query)
    data = pairing(job)
    check_scope(data['packages'], query)
    gray_model = apps.get_model('erp_production.SourceDyeJobGrayRecord')
    gray = list(gray_model.objects.filter(pk__in={row['record_id'] for row in data['gray']}).select_for_update().order_by('pk'))
    check_scope(gray, query)
    packages = {row.pk: scoped(row, query) for row in data['packages']}
    changes, states = [], []
    for result in data['rows']:
        if not result['matched']:
            continue
        item = packages[result['record_id']]
        require_available(item)
        states.append({'id': item.pk, 'previous': effect(item, 'package_gray_origin')})
        change(item, {key: result[key] for key in ['GrayWeight', 'GrayBarCode']}, changes, actor, reason)
        save_effect(item, 'package_gray_origin', {'state': 'applied', 'mode': 'sorted_pairing', 'job_id': job.pk,
            'source_id': result['source_id'], 'candidates': result['candidates'], 'at': at, 'reason': reason}, actor, reason)
    save_effect(job, 'package_pairing', {'state': 'applied', 'at': at, 'reason': reason, 'rows': data['rows'],
        'supplemental_rows': data['supplemental_rows'], 'changes': changes, 'states': states,
        'jobs': [origin(row) for row in jobs], 'gray_sources': [origin(row) for row in gray]}, actor, reason)
    return {'report': '包装排序配对结果', 'rows': data['rows'], 'supplemental_rows': data['supplemental_rows'],
        'notes': [f'实际回写{len(changes)}条包装记录；未匹配原记录保留。']}


@transaction.atomic
def undo_pairing(job, actor, at, reason, query=reader):
    job = scoped(job, query)
    require_available(job)
    lock_jobs(raw(job, 'SheetNo'), query)
    value = effect(job, 'package_pairing')
    if value is None or value['state'] != 'applied':
        raise ValidationError({'source': '本工卡没有可撤回的排序配对。'})
    for entry in value['states']:
        row = locked(get_object_or_404(query('RecordYield', 'erp_warehouse'), pk=entry['id']))
        require_available(row)
        current = effect(row, 'package_gray_origin')
        if current is None or current.get('mode') != 'sorted_pairing' or current.get('job_id') != job.pk:
            raise ValidationError({'source': '包装投坯对应已有后续采用，请先处理该采用再撤回排序配对。'})
    restore(value['changes'], actor, reason)
    for entry in value['states']:
        row = reader('RecordYield', 'erp_warehouse').get(pk=entry['id'])
        save_effect(row, 'package_gray_origin', entry['previous'] or {'state': 'reversed', 'reversed_at': at}, actor, reason)
    save_effect(job, 'package_pairing', {**value, 'state': 'reversed', 'reversed_at': at, 'reverse_reason': reason}, actor, reason)
    return job
