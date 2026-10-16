"""当前主档触发器：原检查留事实，部门/员工/考勤联动逐行办理。"""
from django.core.exceptions import ValidationError
from .business import persist, record, snapshot
from .source_business_updates import matching
from .source_calculations import store_value
from .source_context import SourceDocumentContext
from .source_quality_reports import rows
from .source_sequences import allocate
from .source_stock_services import raw
from .source_trial_steps import equal
from .source_package_labels import varchar
from decimal import Decimal, ROUND_HALF_UP

TABLES = {'p_Customer', 'p_Gray', 'p_Dept', 'h_Employee', 'USERINFO', 'KindLimit', 'NoLimit', 'Limit', 'FeelOfferDetail'}


def retain(item, actor, reason):
    """原DELETE的业务效果；原行和删除前值留档，活动查询不再返回。"""
    context, _ = SourceDocumentContext.objects.get_or_create(entity=item._meta.label, object_id=item.pk,
        defaults={'entry_name': 'foundation_trigger', 'creator': actor, 'modifier': actor})
    context.effects['foundation_retained'] = {'active': True, 'reason': reason}
    persist(context, actor)
    record(item, 'foundation_delete_retained', snapshot(item), actor, reason)


def update(item, values, actor, reason):
    before = snapshot(item)
    for old, value in values.items():
        field, converted = store_value(item, old, value)
        setattr(item, field, converted)
    persist(item, actor)
    record(item, 'foundation_trigger_update', before, actor, reason)
    if item.SOURCE_TABLE == 'USERINFO':
        userinfo_saved(item, actor)


def userinfo_saved(item, actor):
    # USERINFO_Add以插入/修改后的USERID删除空SSN，保留同USERID多行效果。
    if equal(raw(item, 'SSN') or '', ''):
        for candidate in rows('USERINFO', 'erp_base').filter(old_userid=raw(item, 'USERID')).order_by('pk'):
            if equal(raw(candidate, 'SSN') or '', ''):
                retain(candidate, actor, 'USERINFO_Add：空SSN按原规则退出活动考勤档案，原行留档')


def check(item, data, created, actor):
    name = item.SOURCE_TABLE
    if name == 'p_Customer':
        if not created and 'old_customer_id' in data and equal(raw(item, 'CustKindID'), '0'):
            raise ValidationError({'old_customer_id': '原p_Customer_UPDATE：客户编码不能修改（原UPDATE列判断包含同值赋值）。'})
        if created:
            counts = {kind: matching(rows('PCustomer', 'erp_base'), ShortName=raw(item, 'ShortName'), CustKindID=kind).count() for kind in ['0', '1']}
            if any(count > 1 for count in counts.values()):
                record(item, 'original_master_duplicate', snapshot(item), actor,
                       'p_CustomerInsert原重名检查：'+str(counts)+'；按完整保留异常原行的要求保存，不去重')
    elif name == 'p_Gray' and not created:
        if matching(rows('PGray', 'erp_base'), NameC=raw(item, 'NameC')).count() > 1:
            record(item, 'original_master_duplicate', snapshot(item), actor,
                   'p_GrayModify原规格重名检查命中；按完整保留异常原行的要求保存，不去重')
        if 'old_gray_id' in data:
            raise ValidationError({'old_gray_id': '原p_GrayModify：规格编码不能修改（含同值赋值）。'})


def department_saved(item, actor):
    departments = rows('DEPARTMENTS', 'erp_base')
    matches = list(matching(departments, Code=raw(item, 'DeptID')).order_by('pk'))
    # COUNT(Name)忽略NULL；原分支随后按全表Name查找，不按DeptID插入。
    if matches and raw(item, 'Name') is not None:
        for department in matches:
            update(department, {'DEPTNAME': raw(item, 'Name')}, actor, 'p_Dept_Add：原部门名更新')
    else:
        name = varchar(raw(item, 'Name'), 50)
        for department in matching(rows('PDept', 'erp_base'), Name=name).order_by('pk'):
            values = {'Code': raw(department, 'DeptID'), 'DEPTNAME': raw(department, 'Name'),
                      **{key: 1 for key in ['SUPDEPTID', 'InheritDeptSch', 'InheritDeptSchClass', 'AutoSchPlan',
                          'InLate', 'OutEarly', 'ATT', 'Holiday', 'OverTime', 'DefaultSchId', 'RegisterOT']},
                      'MinAutoSchInterval': 24}
            child = departments.model(**{departments.model.SOURCE_FIELDS[key]: value for key, value in values.items()})
            allocate(child, actor); persist(child, actor)
            record(child, 'foundation_department_create', {'exists': False}, actor, 'p_Dept_Add：原同名部门全部生成')


def employee_saved(item, actor):
    employee = varchar(raw(item, 'EmpID'), 50)
    department = varchar(raw(item, 'DeptID'), 10)
    candidates = list(matching(rows('DEPARTMENTS', 'erp_base'), Code=department).order_by('pk'))
    target = None if not candidates else raw(candidates[-1], 'DEPTID')
    departed = bool(raw(item, 'IsOut'))
    for account in matching(rows('USERINFO', 'erp_base'), SSN=employee).order_by('pk'):
        update(account, {'DEFAULTDEPTID': target}, actor, 'UpdateEmployee：原第一次部门回写')
    for account in matching(rows('USERINFO', 'erp_base'), SSN=raw(item, 'EmpID')).order_by('pk'):
        values = {'DEFAULTDEPTID': 1, 'CardNo': ''} if departed else {
            'SSN': raw(item, 'EmpID'), 'NAME': raw(item, 'Name'),
            'GENDER': 'M' if equal(raw(item, 'Sex'), '男') else 'F' if equal(raw(item, 'Sex'), '女') else '',
            'HIREDDAY': raw(item, 'InDate'), 'CardNo': raw(item, 'RFID'), 'BADGENUMBER': raw(item, 'EmpID')}
        update(account, values, actor, 'UpdateEmployee：离职/在职考勤字段回写')
    if departed:
        for member in matching(rows('PShiftEmp', 'erp_base'), EmpID=raw(item, 'EmpID')).order_by('pk'):
            retain(member, actor, 'UpdateEmployee：离职员工退出原班组，原成员行留档')
    # 原最后一次部门覆盖仍执行，不能把离职部门永久改成1。
    for account in matching(rows('USERINFO', 'erp_base'), SSN=employee).order_by('pk'):
        update(account, {'DEFAULTDEPTID': target}, actor, 'UpdateEmployee：原最后一次部门覆盖')
    if departed:
        for person in matching(rows('HEmployee', 'erp_base'), EmpID=employee).filter(old_is_out=True).order_by('pk'):
            if not equal(raw(person, 'RFID') or '', ''):
                update(person, {'RFID': ''}, actor, 'UpdateEmployee：原离职清卡，不重放递归触发器')
                if person.pk == item.pk:
                    item.old_rfid = ''


def saved(item, data, created, actor):
    if item.SOURCE_TABLE not in TABLES or item.source_batch_id is not None or item.legacy_id is not None:
        return
    check(item, data, created, actor)
    if item.SOURCE_TABLE == 'p_Dept':
        department_saved(item, actor)
    elif item.SOURCE_TABLE == 'h_Employee' and not created:
        employee_saved(item, actor)
    elif item.SOURCE_TABLE == 'USERINFO':
        userinfo_saved(item, actor)
    elif item.SOURCE_TABLE in ['KindLimit', 'NoLimit', 'Limit']:
        column = 'EmpID' if item.SOURCE_TABLE == 'Limit' else 'Kind'
        value = raw(item, column)
        source = rows(item.SOURCE_TABLE, 'erp_base')
        count = (matching(source, EmpID=varchar(value, 30)).count() if column == 'EmpID' else
                 source.filter(**{item.SOURCE_FIELDS[column]: value}).count()) if value is not None else 0
        if count > 1:
            record(item, 'original_master_duplicate', snapshot(item), actor,
                   f'{item.SOURCE_TABLE}Insert：原{column}重复检查{count}行；异常行照存')
    elif item.SOURCE_TABLE == 'FeelOfferDetail':
        feel_saved(item, data, created, actor)


def feel_saved(item, data, created, actor):
    heads = list(matching(rows('FeelOfferMain', 'erp_base'), SheetSeries=raw(item, 'SheetSeries')).order_by('pk'))
    product = varchar(raw(item, 'ProdID'), 20) if heads else ''
    feel = varchar(raw(item, 'FeelCode'), 50) if heads else None
    count = matching(rows('FeelOfferDetail', 'erp_base'), ProdID=product, FeelCode=feel).count()
    if count > 1:
        record(item, 'original_master_duplicate', snapshot(item), actor,
               f'FeelOfferDetail_Modify：跨客户同产品/手感{count}行；原重名检查留档，不去重')
    if heads and not created and 'old_right_status' not in data and raw(item, 'RightStatus') == 10:
        raise ValidationError({'old_right_status': '原手感报价已审核，不能修改。'})
    for line in matching(rows('FeelOfferDetail', 'erp_base'), DetailNo=raw(item, 'DetailNo')).order_by('pk'):
        price = raw(line, 'Price')
        value = None
        if price is not None:
            text = str(int((Decimal(str(price))*10).quantize(Decimal('1'), rounding=ROUND_HALF_UP)))
            text = text if len(text) <= 10 else '*'*10
            value = ('0' if price < 1 else '')+text
        update(line, {'SGDH': value}, actor, 'FeelOfferDetail_Modify：按原STR及价格分支回写手感代号')
        if line.pk == item.pk:
            setattr(item, item.SOURCE_FIELDS['SGDH'], value)


def removing(item, actor):
    if item.SOURCE_TABLE == 'FeelOfferDetail' and raw(item, 'RightStatus') == 10:
        raise ValidationError({'old_right_status': '原FeelOfferDetail_Del：已审核手感报价不能删除。'})
    if item.SOURCE_TABLE == 'h_Employee':
        for account in matching(rows('USERINFO', 'erp_base'), SSN=raw(item, 'EmpID')).order_by('pk'):
            retain(account, actor, 'DelEmployee：删除员工后考勤档案退出活动范围，原行留档')
