"""最新原库存过程的固定投影、审核门槛及历史流水留档。"""
import json
from pathlib import Path
from django.db import transaction
from django.utils import timezone
from .source_phase3_operations import source,model,query,create,change,retire,result
from .source_business_updates import matching
from .source_stock_services import raw
from .source_entry_registry import ENTRY_RULES

SPECS=json.loads(Path(__file__).with_name('source_phase3_posting.json').read_text(encoding='utf8'))
KINDS={'GrayBalance':('SheetKind',[55]),'GrayIn':('BookKind',list(range(10,22))),
 'GrayOut':('BookKind',list(range(20,31))+[34]),'DiscardGrayOut':('BookKind',list(range(20,30))),
 'GrayStockAdjust':('BookKind',[33,34]),'GrayStockSpecUp':('BookKind',[27]),'GrayStockAllot':('BookKind',[41,42]),
 'SemiIn':('SheetKind',list(range(11,22))+[24,25,26,30,104]),'SemiOut':('SheetKind',list(range(21,33))+[36,204]),
 'SemiStockAdjust':('BookKind',[33,34]),'SemiStockSpecUp':('BookKind',[22]),
 'ProdIn':('BookKind',list(range(10,21))),'ProdOut':('BookKind',list(range(20,30))),'ProdOutUpdate':('BookKind',[30]),
 'ArticleIn':('BookKind',[11,13,18,14,16,19]),'ArticleOut':('BookKind',[21,22,23,24,25,29]),
 'ArticleStockAdjust':('BookKind',[33]),'StuffIn':('BookKind',[11,13,14,16,18,19]),
 'StuffOut':('BookKind',[21,22,23,24,25,29]),'StuffStockAdjust':('BookKind',[33]),'ProdStockAdjust':('BookKind',[33,34])}


@transaction.atomic
def post(entry,series,actor):
    label=next(label for label,entries in ENTRY_RULES.items() if entry in entries and entries[entry]['master_entry'] is None)
    from django.apps import apps
    headmodel=apps.get_model(label);table=headmodel.SOURCE_TABLE
    if table=='StuffAllot':return allot(series,actor)
    if table=='GrayStorageAdjust':return storage(series,actor)
    branch='ProdOutUpdate' if entry=='ProdOutUpdate' else 'DiscardGrayOut' if entry=='DiscardGrayOut' else table
    specs=SPECS[branch];book=specs[0]['table'];field,kinds=KINDS[branch]
    heads=list(matching(source(table),SheetSeries=series).order_by('pk'))
    current=matching(source(book),SheetSeries=series).filter(**{model(book).SOURCE_FIELDS[field]+'__in':kinds})
    ready=bool(heads) and (ENTRY_RULES[label][entry]['save_updates_stock'] is True or raw(heads[-1],'RightStatus')==10)
    if entry=='ProdOutUpdate':
        if heads and ENTRY_RULES[label][entry]['save_updates_stock'] is True and raw(heads[-1],'RightStatus')==10:
            return result('Sp_UpdateProdStockBook',[])
        ready=bool(heads) and ENTRY_RULES[label][entry]['save_updates_stock'] is True and raw(heads[-1],'RightStatus')!=10
    # 原ArticleOut分支没有给RightStatus赋值，只有“保存更新库存”可进入写入分支。
    if table=='ArticleOut':
        ready=bool(heads) and ENTRY_RULES[label][entry]['save_updates_stock'] is True
        if heads and not ready:return result('Sp_UpdateArticleStockBook',[])
    if table=='ProdIn':
        prior_jobs=list(matching(source(book),SheetSeries=series).order_by('pk').values_list('old_job_sheet_no',flat=True))
        if ready or not heads:current=matching(source(book),SheetSeries=series).filter(old_book_kind__in=[10,11,12,14,15,16,17,19,20])
        if heads and not ready and raw(heads[-1],'RightStatus') is None:return result('Sp_UpdateProdStockBook',[])
    if table=='ProdOut' and not heads:current=matching(source(book),SheetSeries=series)
    if table=='GrayIn' and heads and not ready:current=matching(source(book),SheetSeries=series).filter(old_book_kind__in=[10,11,12,13,14,15,16,17,18,19,21])
    if table=='SemiIn':
        selected=KINDS['SemiIn'][1] if ready else [11,12,13,14,15,16,17,18,19,20,21,24,30,104] if heads else [11,12,13,14,15,24,16,17,18,19,21,20,25,26,104]
        current=matching(source(book),SheetSeries=series).filter(old_sheet_kind__in=selected)
    if table=='GrayOut' and not heads and current.filter(old_book_kind=29).exists():
        prior=matching(source(book),SheetSeries=series).order_by('pk').last()
        change(matching(source('JobSheet'),SheetNo=raw(prior,'JobSheetNo') or ''),{'CurrProcessID':'退仓待处理','SheetStatus':9},actor)
    incoming=table in ['ArticleIn','StuffIn']
    retained=[] if ready and incoming else retire(current,actor,entry+'更新/反审核库存，原流水留档')
    created=[]
    if ready:
        if table=='GrayStockAllot':
            from .source_gray_stock import rows as allot_rows
            for head in heads:
                for name,data in allot_rows(head,entry):created.append(create(name,data,actor))
            return result('Sp_UpdateGrayStockBook',created,retained)
        p={'sheetseries':series,'currdate':timezone.now()}
        if table=='SemiOut':
            from .source_phase3_operations import records
            records('304',{'semioutsheetseries':series},actor)
        for spec in specs:
            values=query(spec['sql'],p);fields={f.lower():f for f in model(book).SOURCE_FIELDS}
            detailkeys=[]
            for value in values:
                data={fields[f]:v for f,v in value.items()}
                targets=current.none()
                if incoming:
                    detailkeys.append(data['DetailNo']);targets=matching(current,DetailNo=data['DetailNo'])
                    if table=='StuffIn':targets=matching(source(book),SheetNo=data['SheetNo'],DetailNo=data['DetailNo']).filter(old_book_kind__in=kinds)
                if targets.exists():
                    if table=='StuffIn':data.pop('InDetailNo') # 原更新分支没有更新该字段。
                    change(targets,data,actor);created.extend(targets)
                    if table=='StuffIn':
                        from .source_phase3_triggers import saved
                        for target in targets:saved(target,{},False,actor)
                else:created.append(create(book,data,actor))
            if incoming and None not in detailkeys:
                retained.extend(retire(current.exclude(old_detail_no__in=detailkeys).exclude(old_detail_no__isnull=True),actor,'原入库已移除明细，旧流水留档'))
        if table=='GrayIn':
            for head in heads:change(matching(source('GrayInDetail'),SheetSeries=series),{'GUnit':raw(head,'StockUnit')},actor)
        if table=='GrayOut':gray_links(series,actor)
        if entry in ['GrayOutJob','SemiOutJob']:job_totals(table,series,actor)
    if table=='ProdIn':
        from .source_phase3_dispatch import perform
        job=raw(heads[-1],'JobSheetNo') if heads else prior_jobs[-1] if prior_jobs else None
        perform('Sp_UpdateJobSheetByProdIn',{'jobsheetno':job},actor)
    return result('Sp_Update'+book,created,retained)


def gray_links(series,actor):
    jobs=query('SELECT JobSheetNo FROM dye.GrayOutDetail WHERE SheetSeries=@s GROUP BY JobSheetNo',{'s':series})
    if not jobs:return
    selected=list(matching(source('JobSheet'),SheetNo=jobs[-1]['jobsheetno']).order_by('pk'))
    if not selected:return
    jobseries=raw(selected[-1],'SheetSeries')
    for line in matching(source('JobGrayRecord'),SheetSeries=jobseries).order_by('pk'):
        outgoing=list(matching(source('GrayOutRecord'),BarCode=raw(line,'GrayBarCode')).order_by('pk'))
        if outgoing:
            value={'AssignedNo':raw(outgoing[-1],'AssignedNo')}
            change(matching(source('JobGrayRecord'),SheetSeries=jobseries,GrayBarCode=raw(line,'GrayBarCode')),value,actor)
            change(matching(source('GrayInRecord'),ReceSheetNo=raw(line,'ReceSheetNo'),BarCode=raw(line,'GrayBarCode')),
                {**value,'JobSheetNo':jobseries},actor)


def job_totals(table,series,actor):
    values=query('SELECT JobSheetNo,SUM(WeightQty) AS WeightQty,SUM(Rolls) AS Rolls,SUM(Packs) AS Packs FROM dye.'+table+'Detail WHERE SheetSeries=@s GROUP BY JobSheetNo',{'s':series})
    if not values:return
    from decimal import Decimal,ROUND_HALF_UP
    from .business import record,snapshot
    value=values[-1];targets=matching(source('JobSheet'),SheetNo=value['jobsheetno'])
    updates={'SumAssigned'+f:None if value[f.lower()] is None else Decimal(str(value[f.lower()])).quantize(Decimal('.01'),rounding=ROUND_HALF_UP) for f in ['WeightQty','Rolls','Packs']}
    change(targets,{**updates,'CurrProcessID':'发纱出库' if table=='GrayOut' else '胚纱出库'},actor)
    if len(values)>1:
        for job in targets:record(job,'phase3_actual_assignment_groups',snapshot(job),actor,'Sp_UpdateJobOutAC原标量分组候选：'+str(values))


def allot(series,actor):
    from .source_stuff_allot import derive
    from .source_entry_services import save_context
    from django.apps import apps
    heads=list(matching(source('StuffAllot'),SheetSeries=series).order_by('pk'))
    created=[];retained=[]
    suffix=series[-8:]
    for table,number in [('StuffOut','TO'+suffix),('StuffIn','SR'+suffix)]:
        for name in [table+'Detail',table]:retained.extend(retire(matching(source(name),SheetSeries=number),actor,'原调拨派生单据重办/撤回留档'))
    retained.extend(retire(source('StuffStockBook').filter(old_sheet_series__in=['TO'+suffix,'SR'+suffix]),actor,'调拨双侧旧流水留档'))
    for head in heads:
        context=save_context(head,actor,'StuffAllot')
        for label,ids in context.effects.get('derived_records',{}).items():
            retained.extend(retire(apps.get_model(label).objects.filter(pk__in=ids),actor,'调拨重办原派生单据留档'))
        suffix=series[-8:]
        retained.extend(retire(source('StuffStockBook').filter(old_sheet_series__in=['TO'+suffix,'SR'+suffix]),actor,'调拨双侧旧流水留档'))
        if not (raw(head,'RightStatus')==10 or ENTRY_RULES[head._meta.label]['StuffAllot']['save_updates_stock']):continue
        for name,data in derive(head,context,actor,matching(source('StuffAllotDetail'),SheetSeries=series).order_by('pk')):
            created.append(create(name,data,actor))
    return result('Sp_UpdateStuffStockBook',created,retained)


def storage(series,actor):
    from .source_gray_storage import derive,undo
    from .source_entry_services import save_context
    from django.apps import apps
    created=[];retained=[]
    for head in matching(source('GrayStorageAdjust'),SheetSeries=series).order_by('pk'):
        context=save_context(head,actor,'GrayStorageAdjust')
        if context.effects.get('gray_storage_changes'):undo(context,actor)
        for label,ids in context.effects.get('derived_records',{}).items():
            retained.extend(retire(apps.get_model(label).objects.filter(pk__in=ids),actor,'库位调整重办原派生行留档'))
        if raw(head,'RightStatus')==10 or ENTRY_RULES[head._meta.label]['GrayStorageAdjust']['save_updates_stock']:
            for name,data in derive(head,context,actor,matching(source('GrayStorageAdjustDetail'),SheetSeries=series).order_by('pk')):
                row=create(name,data,actor);created.append(row)
                context.effects['derived_records'].setdefault(row._meta.label,[]).append(row.pk)
            from .business import persist
            persist(context,actor)
    return result('Sp_UpdateGrayStockBook',created,retained)
