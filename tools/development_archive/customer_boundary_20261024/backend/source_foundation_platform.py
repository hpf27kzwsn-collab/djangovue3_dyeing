"""原导航、个人菜单、报表权限配置办理；不赋予新系统用户权限。"""
from django.db import transaction
from plugins.erp_base.business import persist, record
from plugins.erp_base.source_sequences import allocate
from plugins.erp_base.source_master_data import update, retain
from plugins.erp_base.source_business_updates import matching
from plugins.erp_base.source_quality_reports import rows, key
from plugins.erp_base.source_stock_services import raw
from plugins.erp_base.source_package_labels import varchar


def source(name):
    return rows(name, 'erp_base').order_by('pk')


def create(name, values, actor, reason):
    from plugins.erp_base.source_services import apply_defaults
    model = source(name).model
    data = {model.SOURCE_FIELDS[k]:v for k,v in values.items()}
    item = model(**data)
    apply_defaults(item, data)
    allocate(item, actor)
    persist(item, actor)
    record(item, 'foundation_config_create', {'exists':False}, actor, reason)
    return item


@transaction.atomic
def add_favorite(employee, function, actor):
    employee, function = varchar(employee,50), varchar(function,50)
    current = matching(source('SFuncUser'), EmpID=employee, FuncNo=function)
    if current.exists():
        return list(current)
    numbers = [raw(r,'uiSerialNumber') for r in matching(source('SFuncUser'), EmpID=employee)
               if raw(r,'uiSerialNumber') is not None]
    number = max(numbers)+1 if numbers else 1
    number = 1 if number==0 else number
    return [create('SFuncUser', {'EmpID':employee,'FuncNo':function,'uiSerialNumber':number}, actor, 's_FuncUser_Add')]


@transaction.atomic
def move_favorite(employee, function, new_index, actor):
    employee, function = varchar(employee,50), varchar(function,50)
    selected = list(matching(source('SFuncUser'), EmpID=employee, FuncNo=function))
    old_index = raw(selected[-1],'uiSerialNumber') if selected else None
    group = list(matching(source('SFuncUser'), EmpID=employee))
    if new_index == -1:
        for item in selected:
            update(item, {'uiSerialNumber':999}, actor, 's_FuncUser_UpdateSerialNum：移至末位')
        group = list(matching(source('SFuncUser'), EmpID=employee))
        ordered = sorted(group, key=lambda r:(raw(r,'uiSerialNumber') is not None, raw(r,'uiSerialNumber') or 0, r.pk))
        indexes = {}
        for number, item in enumerate(ordered, 1):
            indexes.setdefault(key(raw(item,'FuncNo')), number)
        for item in group:
            if raw(item,'FuncNo') is not None:
                update(item, {'uiSerialNumber':indexes[key(raw(item,'FuncNo'))]}, actor, '原按功能号连接行号；同号多行保留')
    else:
        for item in group:
            number = raw(item,'uiSerialNumber')
            if number is not None and old_index is not None and new_index is not None:
                if old_index < number <= new_index:
                    update(item, {'uiSerialNumber':number-1}, actor, '原个人菜单前移')
                elif new_index <= number < old_index:
                    update(item, {'uiSerialNumber':number+1}, actor, '原个人菜单后移')
        for item in selected:
            update(item, {'uiSerialNumber':new_index}, actor, '原个人菜单指定序号')
    return list(matching(source('SFuncUser'), EmpID=employee))


def distinct(values):
    result, seen = [], set()
    for row in values:
        identity = tuple(key(v) if isinstance(v,str) else v for v in row.values())
        if identity not in seen:
            result.append(row); seen.add(identity)
    return result


def print_rights(function, employee):
    function, employee = varchar(function,10), varchar(employee,10)
    menus = list(matching(source('SRptMenu'), FuncNo=function))
    pairs = [(menu,info) for menu in menus for info in matching(source('SRptInfo'), RptID=raw(menu,'RptID'))]
    has_rights = any(matching(source('SRptRight'), RptID=raw(menu,'RptID')).exists() for menu,info in pairs)
    def projection(menu, info, person):
        return {'FuncNo':raw(menu,'FuncNo'),'RptID':raw(menu,'RptID'),'EmpID':person,
                'RptTitle':raw(info,'RptTitle'),'RptUse':raw(menu,'RptNo')}
    if not has_rights:
        return distinct(projection(m,i,'Admin') for m,i in pairs)
    result = distinct(projection(m,i,raw(right,'EmpID')) for m,i in pairs
                      for right in matching(source('SRptRight'),RptID=raw(m,'RptID'),EmpID=employee))
    if key(employee) == 'ADMIN':
        result += distinct(projection(m,i,'Admin') for m,i in pairs)
    return result  # UNION ALL保留Admin两路重复；原IsEnable不参与过滤。


@transaction.atomic
def stop_function(function, actor):
    items = list(matching(source('SFunctions'), FuncNo=None if function is None else function[:20]))
    for item in items:
        update(item, {'IsEnable':False}, actor, 'sp_FuncStop')
    return items


@transaction.atomic
def rename_function(old, new, actor):
    old, new = varchar(old,20), varchar(new,20)
    items = []
    for name in ['SFormParam','SFunctions','SGridColumnParam','SGridParam','SPanelParam',
                 'SPermission','SPivotGridColumnParam','SPivotGridParam']:
        for item in matching(source(name), FuncNo=old):
            update(item, {'FuncNo':new}, actor, 'Sp_UpdateFuncNo：原八表改号')
            items.append(item)
    return items


@transaction.atomic
def navigation_permissions(function, actor):
    function = varchar(function,20)
    created = []
    for role in source('SRoles'):
        number = raw(role,'RoleNo')
        if number is None or key(number)=='028':
            continue
        if matching(source('SPermission'), RoleNo=number,FuncNo=function).exists():
            continue
        for nav in matching(source('SUINav'), FuncNo=function):
            for definition in matching(source('SFunctions'), FuncNo=raw(nav,'FuncNo')):
                if raw(definition,'IsEnable') and raw(definition,'ModuleNo') not in [None,49,60,48]:
                    created.append(create('SPermission', {'RoleNo':number,'FuncNo':raw(nav,'FuncNo')},actor,'sp_UINav_To_Functions'))
    return created


@transaction.atomic
def field_rights(role_number, actor):
    # 原@RoleNo未被使用，始终取002；原删除只限定表名，不能只删SheetNo字段。
    created = []
    for role in matching(source('SRoles'),RoleNo='002'):
        for member in matching(source('HEmpRole'),RoleNo=raw(role,'RoleNo')):
            employee = varchar(raw(member,'EmpID'),50)
            for right in matching(source('SFieldRight'),EmpID=employee,DataTableName='JobSheet'):
                retain(right,actor,'sp_s_FieldRight：原删除配置留档')
            created.append(create('SFieldRight',{'EmpID':employee,'DataTableName':'JobSheet','FieldName':'SheetNo','FieldRight':0},actor,'sp_s_FieldRight'))
    return created


@transaction.atomic
def allocate_print_rights(role_number, actor):
    created=[]
    for role in matching(source('SRoles'),RoleNo=varchar(role_number,20)):
        if key(raw(role,'RoleNo')) not in ['002','017']:
            continue
        permissions=list(matching(source('SPermission'),RoleNo=raw(role,'RoleNo')))
        for member in matching(source('HEmpRole'),RoleNo=raw(role,'RoleNo')):
            employee= varchar(raw(member,'EmpID'),50)
            for permission in permissions:
                function= varchar(raw(permission,'FuncNo'),20)
                if key(function) not in ['030207','030200']:
                    continue
                allowed=any(raw(p,'IsCanPrint')==1 for er in matching(source('HEmpRole'),EmpID=employee)
                            for p in matching(source('SPermission'),RoleNo=raw(er,'RoleNo'),FuncNo=function))
                if allowed:
                    menus=list(matching(source('SRptMenu'),FuncNo=function))
                    for menu in menus:
                        for right in matching(source('SRptRight'),RptID=raw(menu,'RptID'),EmpID=employee):
                            retain(right,actor,'sp_FuncNoPrint：原权限替换留档')
                    for menu in menus:
                        created.append(create('SRptRight',{'RptID':raw(menu,'RptID'),'EmpID':employee,'IsEnable':1},actor,'sp_FuncNoPrint'))
    return created
