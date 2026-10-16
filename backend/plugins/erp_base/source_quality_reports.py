"""Sp_QualityIssues1～4的日/月、旬、一级分类及染色质量奖扣统计。"""
from plugins.erp_base.source_provenance import reference as source_reference
from collections import defaultdict
import re
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from django.apps import apps
from django.db.models import Q
from django.utils import timezone

KINDS = {'内部评审': 'N', '客退评审': 'K', '赔付评审': 'P'}
COLUMNS = [f'{period}_{kind}_{measure}' for period in ['Day', 'Month'] for kind in 'NKP' for measure in ['Qty', 'LengthQty']]


def rows(name, module):
    from .source_execution_state import active as execution_active
    source=execution_active(apps.get_model(module + '.SourceDye' + name).objects.all())
    if name=='DyeCheckout':
        from .source_dye_rebuild import active
        return active(source)
    return source


def key(value):
    return None if value is None else value.rstrip(' ').upper()


def total(values):
    present = [value for value in values if value is not None]
    return sum(present) if present else None


def rounded(value, places='0.01'):
    return None if value is None else Decimal(value).quantize(Decimal(places), rounding=ROUND_HALF_UP)


def period_dates(as_of, report):
    start = datetime.combine(as_of, datetime.min.time())
    month = start.replace(day=1)
    if report == 2:
        start = month.replace(day=1 if as_of.day <= 10 else 11 if as_of.day <= 20 else 21)
        end = month.replace(day=11 if as_of.day <= 10 else 21) if as_of.day <= 20 else (month.replace(day=28) + timedelta(days=4)).replace(day=1)
    else:
        end = start + timedelta(days=1)
    return [timezone.make_aware(value) for value in [start, end - timedelta(milliseconds=3), month]]


def class_key(value):
    normalized = key(value)
    if normalized is None:
        return None
    if normalized.strip() == '' or re.fullmatch(r'[+-]?[0-9]+', normalized.strip()):
        return ('number', int(normalized) if normalized.strip() else 0)
    return ('original_text', normalized)


def indexed(query, code, columns, normalize=key):
    result = defaultdict(list)
    for value in query.order_by('pk').values(code, *columns):
        normalized = normalize(value[code])
        if normalized is not None:
            result[normalized].append(value)
    return result


def accumulate(groups, grouping, values):
    bucket = groups.setdefault(grouping, {column: [] for column in COLUMNS})
    for column in COLUMNS:
        bucket[column].append(values.get(column))


def sums(bucket):
    return {column: total(values) for column, values in bucket.items()}


def base_report(report, as_of, query=rows):
    start, end, month = period_dates(as_of, report)
    jobs = indexed(query('JobSheet', 'erp_production'), 'old_sheet_no', ['old_assign_unit'])
    dictionary = query('PFieldValid', 'erp_base')
    classes = indexed(dictionary.filter(old_field_type='Class'), 'old_code', ['old_name'], class_key)
    departments = indexed(dictionary.filter(old_field_type='Defects'), 'old_code', ['old_name', 'old_description', 'old_mnemonic'])
    groups, first_grade = {}, {}
    source_ids = []
    defects = query('WDefect', 'erp_quality').filter(old_sheet_date__gte=month, old_sheet_date__lte=end)
    for defect in defects.order_by('pk'):
        kind = KINDS.get(defect.old_kind.rstrip(' ') if defect.old_kind is not None else None)
        if kind is None:
            continue  # 原三个评审范围；原表其他Kind仍保留在原查询。
        source_ids.append(defect.pk)
        dept = key(defect.old_defect_dept)
        for job in jobs.get(key(defect.old_job_sheet_no), [None]):
            for unit in ['数量', '卡数']:
                cls = class_key(defect.old_defect_class_id)
                if unit == '数量' and cls == ('number', 5):
                    cls = ('number', 3)
                values = {}
                for period, begin in [('Day', start), ('Month', month)]:
                    strict = (unit == '数量' and period == 'Day' and report in [1, 2]) or (
                        unit == '卡数' and ((report == 1 and period == 'Month') or report == 3 or (report == 2 and period == 'Day')))
                    included = begin <= defect.old_sheet_date and (defect.old_sheet_date < end if strict else defect.old_sheet_date <= end)
                    if included:
                        values[f'{period}_{kind}_Qty'] = defect.old_defect_qty if unit == '数量' else (
                            1 if job is not None and job['old_assign_unit'] == 1 else None)
                        values[f'{period}_{kind}_LengthQty'] = defect.old_defect_length_qty if unit == '数量' else (
                            1 if job is not None and job['old_assign_unit'] == 0 else None)
                if not values:  # 两个原时间分支都未命中时，UNION中没有该行。
                    continue
                for class_row in classes.get(cls, [None]):
                    for dept_row in departments.get(dept, [None]):
                        class_name = None if class_row is None else class_row['old_name']
                        dept_name = None if dept_row is None else dept_row['old_name']
                        grade = None if dept_row is None else dept_row['old_description']
                        accumulate(groups, (dept, dept_name, class_name, unit), values)
                        accumulate(first_grade, (grade, unit), values)
    expanded = [{'DefectDept': group[0], 'DefectDeptName': group[1], 'ClassName': group[2], 'UnitName': group[3],
                 **sums(bucket)} for group, bucket in groups.items()]
    return expanded, first_grade, departments, source_ids, {'start': start.isoformat(), 'end': end.isoformat(), 'month_start': month.isoformat()}


def daily_layout(expanded, departments):
    grouped = {}
    for row in expanded:
        dept, cls, unit = row['DefectDept'], row['ClassName'], row['UnitName']
        # 原'01''07'是一个含单引号字符串，不偷偷改为两个部门。
        if (dept in ["01'07", '09'] and cls in ['甲班', '乙班'] and unit == '数量') or (dept in ['02', '03'] and cls in ['甲班', '乙班']):
            accumulate(grouped, (dept, row['DefectDeptName'], cls, unit), row)
        elif dept in ['04', '05', '06', '10', '11'] or dept in ['08', '12', '13', '14', '15'] and unit == '数量':
            accumulate(grouped, (dept, row['DefectDeptName'], '', unit), row)
        if unit == '数量':
            accumulate(grouped, ('合计', '合计', '', unit), row)
    template = []
    for dept in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '合计']:
        classes = ['甲班', '乙班'] if dept in ['01', '02', '03', '07', '09'] else ['']
        units = ['数量', '卡数'] if dept in ['02', '03', '04', '05', '06', '10', '11'] else ['数量']
        for cls in classes:
            for unit in units:
                matches = [sums(value) for group, value in grouped.items() if group[0] == dept and group[2:] == (cls, unit)]
                for values in matches or [{column: None for column in COLUMNS}]:
                    for dictionary in departments.get(dept, [None]):
                        template.append({'DefectDept': dept, 'DefectDeptName': '合计' if dictionary is not None and dictionary['old_name'] == '合计' else dept,
                            'ClassName': cls, 'UnitName': unit, **values})
    return template


def percentage(numerator, denominator):
    if denominator == 0:  # 原IIF分母=0返回0；不是通用兜底。
        return Decimal('0.00')
    return None if denominator is None or numerator is None else rounded(Decimal(numerator) / denominator * 100)


def ten_day_layout(expanded, departments, denominator):
    groups = {}
    for row in expanded:
        dept, unit = row['DefectDept'], row['UnitName']
        if dept is None or (unit != ('卡数' if dept in ['02', '03', '04', '05', '06'] else '数量')):
            continue
        for dictionary in departments.get(dept, [None]):
            grade = None if dictionary is None else dictionary['old_mnemonic']
            accumulate(groups, (grade, unit), row)
    grades = list(dict.fromkeys(row['old_mnemonic'] for group in departments.values() for row in group))
    result = []
    for grade in grades:
        matches = [(group[1], sums(bucket)) for group, bucket in groups.items() if grade is not None and group[0] == grade]
        for unit, values in matches or [(None, {column: None for column in COLUMNS})]:
            row = {'TowGrade': grade, 'UnitName': unit, **values}
            for column, period, kind in [('N1', 'Day', 'N'), ('N2', 'Month', 'N'), ('K1', 'Day', 'K'), ('K2', 'Month', 'K')]:
                divisor = denominator[period + ('AllNum' if unit == '卡数' else 'AllKg')]
                row[column] = percentage(values[f'{period}_{kind}_Qty'], divisor)
            result.append(row)
    return result


def quality_statistics(report, as_of, denominator=None, query=rows):
    expanded, grades, departments, ids, dates = base_report(report, as_of, query)
    notes = ['原班次表达式按整数比较（05归03仅作用于数量）；非数字班次按原文本保留，并列为E38合理差异。']
    if report == 1:
        result = daily_layout(expanded, departments)
        notes.append("原部门条件'01''07'保持原结果；01/07和未列部门的实际统计见补充明细，不丢弃。")
    elif report == 2:
        if denominator is None:
            denominator = dict.fromkeys(['DayAllNum', 'DayAllKg', 'MonthAllNum', 'MonthAllKg'])
        result = ten_day_layout(expanded, departments, denominator)
        notes.append('原分母来自FARMain/FARDetail，本期不建设财务表；使用质量数量投影自动映射或明确手动分母，未知保持NULL。')
    else:
        valid = {value['old_description'] for group in departments.values() for value in group if value['old_description'] is not None}
        result = [{'OneGrade': group[0], 'UnitName': group[1], **sums(bucket)} for group, bucket in grades.items()
                  if group[0] in valid and group[1] == '数量']
    source = query('WDefect', 'erp_quality').filter(Q(old_sheet_date__isnull=True) | Q(old_sheet_date__gte=dates['month_start'], old_sheet_date__lte=dates['end'])).exclude(pk__in=ids)
    unclassified = [{'id': row.pk, 'source': source_reference(row), 'SheetNo': row.old_sheet_no,
        'SheetDate': row.old_sheet_date, 'Kind': row.old_kind, 'DefectDept': row.old_defect_dept,
        'DefectQty': row.old_defect_qty, 'DefectLengthQty': row.old_defect_length_qty,
        'reason': '日期为空，不能归入所选月份' if row.old_sheet_date is None else '不属于旧报表三种评审类型'} for row in source.order_by('pk')]
    return {'report': f'Sp_QualityIssues{report}', 'rows': result, 'supplemental_rows': expanded, 'unclassified_rows': unclassified,
            'source_ids': ids, 'period': dates, 'denominator': denominator, 'notes': notes}


def dye_quality_award(start, end, query=rows):
    jobs = indexed(query('JobSheet', 'erp_production'), 'old_sheet_no', ['old_loss_str'])
    defects = indexed(query('WDefect', 'erp_quality').filter(old_defect_dept='03'), 'old_sheet_no', [])
    groups = defaultdict(lambda: {'A': [], 'B': []})
    ids, unclassified = [], []
    for row in query('DyeCheckout', 'erp_quality').filter(old_end_time__gte=start, old_end_time__lte=end).order_by('pk'):
        ids.append(row.pk)
        groups[key(row.old_class_id)]['A'].append(Decimal(1))
        cls = key(row.old_defect_class_id)
        if cls is None or cls == '':
            continue
        matches = 0
        for job in jobs.get(key(row.old_job_sheet_no), []):
            for defect in defects.get(key(job['old_loss_str']), []):
                groups[cls]['B'].append(row.old_wdnum)
                matches += 1
        if not matches:
            unclassified.append({'id': row.pk, 'source': source_reference(row), 'WProcessNo': row.old_wprocess_no,
                'JobSheetNo': row.old_job_sheet_no, 'DefectClassID': row.old_defect_class_id, 'WDNum': row.old_wdnum,
                'reason': '有责任班次，但未匹配原03部门返修评审；保留A产量，原B分支无对应行'})
    for row in query('DyeCheckout', 'erp_quality').filter(old_end_time__isnull=True).order_by('pk'):
        unclassified.append({'id': row.pk, 'source': source_reference(row), 'WProcessNo': row.old_wprocess_no,
            'JobSheetNo': row.old_job_sheet_no, 'DefectClassID': row.old_defect_class_id, 'WDNum': row.old_wdnum,
            'reason': '结束时间为空，不能归入本次统计区间'})
    values = []
    for cls, bucket in groups.items():
        a, b = total(bucket['A']), total(bucket['B'])
        values.append({'ClassID': cls, 'AClassIDNum': rounded(a, '0.1'), 'BClassIDNum': rounded(b, '0.1'),
            'Rate': None if a in [None, 0] or b is None else rounded(Decimal(str(b)) / a * 100)})
    all_a = total([row['AClassIDNum'] for row in values])
    for row in values:
        a, b = row['AClassIDNum'], row['BClassIDNum']
        rate = row['Rate']
        share = None if a is None or all_a in [None, 0] else rounded(a / all_a * 2000)
        penalty = Decimal(0) if b is None or b <= 5 else (b - 5) * 50
        row.update(Rate=rate, ClassIDMoeny=share, KFMoeny=penalty,
                   Moeny=Decimal(0) if rate is not None and rate > Decimal('2.3') else None if share is None else share - penalty)
    return {'report': 'Sp_QualityIssues4', 'rows': values, 'source_ids': ids, 'supplemental_rows': [],
            'unclassified_rows': unclassified, 'period': {'start': start.isoformat(), 'end': end.isoformat()},
            'notes': ['质量责任奖扣计算，保留原Moeny拼写及2000/5/50/2.3参数；不生成财务凭证。']}
