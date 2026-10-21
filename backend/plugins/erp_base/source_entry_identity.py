"""原登录员工字段的明确对应；账号名不充当员工、部门或班组编号。"""
from django.core.exceptions import ValidationError
from .source_business_updates import matching
from .source_phase3_operations import source
from .source_stock_services import raw

EMPLOYEE_FIELDS = {
    'LoginPeople_EmpID': 'EmpID', 'LoginPeople.EmpID': 'EmpID',
    'LoginPeople_EmpName': 'Name', 'LoginPeople_EmpDeptID': 'DeptID',
    'LoginPeople_EmpBusinessUnitID': 'BusinessUnitID', 'LoginPeople_EmpShiftID': 'ShiftID',
    'LoginPeople_EmpPositionID': 'PosID',
}
LOGIN_KINDS = {*EMPLOYEE_FIELDS, 'LoginPeople_LoginName', 'LoginPeople_EmpShift', 'LoginPeople_EmpDept'}


def unique_value(values, kind):
    distinct = set(values)
    if len(distinct) > 1:
        raise ValidationError({'employee': '登录资料的'+kind+'有不同候选值，请明确填写该业务字段；原重复资料保留。'})
    return next(iter(distinct)) if distinct else None


def login_value(kind, actor):
    if kind == 'LoginPeople_LoginName':
        return actor.username
    employees = list(matching(source('h_Employee'), LoginName=actor.username).order_by('pk'))
    if kind in EMPLOYEE_FIELDS:
        return unique_value([raw(employee, EMPLOYEE_FIELDS[kind]) for employee in employees], kind)
    table, field = {'LoginPeople_EmpShift': ('p_Shift', 'ShiftID'),
                    'LoginPeople_EmpDept': ('p_Dept', 'DeptID')}[kind]
    return unique_value([raw(row, 'Name') for employee in employees
                         for row in matching(source(table), **{field: raw(employee, field)})], kind)
