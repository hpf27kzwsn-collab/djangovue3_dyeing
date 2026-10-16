"""sp_GetNewCode_HasOutput/New：同对象同日计数、短/长日期分别保留。"""
import hashlib
import json
from django.db import transaction
from django.utils import timezone
from .business import locked, persist, record, snapshot
from .source_business_updates import matching
from .source_quality_reports import rows, key
from .source_sequences import SourceIdentitySequence
from .source_package_labels import varchar


@transaction.atomic
def allocate(object_name, digits, long_date, actor, at=None):
    at = timezone.localtime() if at is None else at
    name = varchar(object_name, 50)
    day = at.strftime('%Y%m%d' if long_date else '%y%m%d')
    scope = json.dumps([key(name), day], ensure_ascii=False)
    mutex, _ = SourceIdentitySequence.objects.get_or_create(
        namespace='original_daily:'+hashlib.sha256(scope.encode()).hexdigest(),
        defaults={'last_number': 0, 'creator': actor, 'modifier': actor})
    locked(mutex)
    source = matching(rows('SAutoID', 'erp_base'), IDObject=name, IDValue=day)
    active = list(source.filter(source_batch__isnull=True, legacy_id__isnull=True).order_by('pk').select_for_update())
    seeded = []
    if not active:
        originals = list(source.exclude(source_batch__isnull=True).order_by('pk'))
        for original in originals:
            current = source.model(old_idobject=original.old_idobject, old_idvalue=original.old_idvalue,
                                   old_idcounter=original.old_idcounter, old_create_date=original.old_create_date)
            persist(current, actor)
            record(current, 'adopt_daily_counter', {'exists': False}, actor, '保留历史原行；复制计数来源ID='+str(original.pk))
            active.append(current);seeded.append(original.pk)
        if not originals:
            current = source.model(old_idobject=name, old_idvalue=day, old_idcounter=1, old_create_date=at)
            persist(current, actor);record(current, 'create_daily_counter', {'exists': False}, actor)
            active.append(current)
    # 原表IDCounter为bigint，过程逐行赋给int变量；先转换后更新。
    for item in active:
        if item.old_idcounter is not None and not -2147483648 <= item.old_idcounter <= 2147483647:
            raise OverflowError('原编号过程的int计数变量转换溢出。')
    counter = active[-1].old_idcounter
    if counter is None or digits is None:
        code = None
    else:
        width = max(digits, len(str(counter)))
        suffix = '0000000000000'+str(counter)
        code = varchar(day+suffix[-width:], 50)
    for item in active:
        before = snapshot(item)
        if item.old_idcounter is not None:
            item.old_idcounter += 1
        persist(item, actor);record(item, 'allocate_daily_number', before, actor)
    return {'report': '原统一编号', 'rows': [{'object': name, 'date': day, 'counter': counter, 'code': code}],
            'source_ids': seeded, 'active_ids': [item.pk for item in active],
            'notes': ['生成会消耗本项目计数；不修改历史来源行。重复计数按项目ID最后一条取值、全部递增。',
                      '原计数快照批次范围及无序差异见E103；本动作不等于全部单据调用点已替换。']}
