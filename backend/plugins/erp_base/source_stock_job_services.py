"""坯料/半成品工卡领用及配纱审核的明确上游回写。"""
from decimal import Decimal, ROUND_HALF_UP
from django.apps import apps
from django.db.models import Sum
from django.db.models.functions import Upper, RTrim
from .business import locked
from .source_entry_services import entry_for
from .source_stock_services import raw, detail_rows
from .source_workflow_services import apply_changes


def removing(item, context, actor):
    if item.SOURCE_TABLE != 'GrayOut':
        return
    book_model = apps.get_model('erp_warehouse.SourceDyeGrayStockBook')
    keys = context.effects.get('stock_rows', {}).get(book_model._meta.label, [])
    numbers = book_model.objects.filter(pk__in=keys, old_book_kind=29).values_list('old_job_sheet_no', flat=True)
    jobs = apps.get_model('erp_production.SourceDyeJobSheet')
    for number in sorted({number for number in numbers if number not in [None, '']}):
        selected = jobs.objects.alias(code=Upper(RTrim('old_sheet_no'))).filter(code=number.rstrip(' ').upper())
        for job in selected.order_by('pk'):
            apply_changes(locked(job), {'CurrProcessID': '退仓待处理', 'SheetStatus': 9}, actor, 'gray_return_removed')


def refresh(item, actor):
    entry = entry_for(item)
    if entry not in ['GrayOut', 'GrayOutJob', 'SemiOutJob']:
        return
    line_name = 'GrayOutDetail' if item.SOURCE_TABLE == 'GrayOut' else 'SemiOutDetail'
    lines = detail_rows(item, line_name)
    numbers = sorted({raw(line, 'JobSheetNo') for line in lines if raw(line, 'JobSheetNo') not in [None, '']})
    jobs = apps.get_model('erp_production.SourceDyeJobSheet')
    for number in numbers:
        selected = lines.filter(old_job_sheet_no__iexact=number)
        totals = selected.aggregate(weight=Sum('old_weight_qty'), rolls=Sum('old_rolls'), packs=Sum('old_packs'))
        values = {}
        if entry in ['GrayOutJob', 'SemiOutJob']:
            # 原过程的中间变量为decimal(10,2)，原SUM未填时仍为NULL。
            values = {old: None if totals[key] is None else Decimal(str(totals[key])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                for old, key in [('SumAssignedWeightQty', 'weight'), ('SumAssignedRolls', 'rolls'), ('SumAssignedPacks', 'packs')]}
        if raw(item, 'SheetKind') == 21:
            # 当前AfterSaveSQL与库存过程的工序名称交叉，本轮采用当前明确界面钩子。
            values.update(CurrProcessID='发纱出库' if entry == 'SemiOutJob' else '胚纱出库', StockUnit=raw(item, 'StockUnit'))
        for job in jobs.objects.filter(old_sheet_no__iexact=number).order_by('pk'):
            job = locked(job)
            apply_changes(job, values, actor, 'stock_job_allocation')
            if entry in ['GrayOut', 'GrayOutJob']:
                receipts = [raw(line, 'ReceSheetNo').rstrip(' ').upper() for line in selected if raw(line, 'ReceSheetNo') is not None]
                assignments = apps.get_model('erp_production.SourceDyeJobAssign').objects.alias(receipt=Upper(RTrim('old_rece_sheet_no'))).filter(source_parent_1=job, receipt__in=receipts).order_by('pk')
                for assignment in assignments:
                    apply_changes(locked(assignment), {'Status': 1 if raw(item, 'RightStatus') == 10 else 0}, actor, 'gray_assignment_approval')
