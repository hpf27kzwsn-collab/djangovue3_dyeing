"""参数、组合框和逐定义翻译的Lookup；不执行原动态SQL文本。"""
import json
from pathlib import Path
from .source_quality_reports import rows
from .source_business_updates import matching
from .source_stock_services import raw
from .source_trial_steps import equal, sql_like
from .source_package_labels import varchar

LOOKUPS = json.loads(Path(__file__).with_name('source_foundation_lookups.json').read_text(encoding='utf8'))['lookups']
SYSTEM_FIELDS = {name: name for name in ['MachineFault_UseFaultClass', 'MachineFault_UseSendTo',
    'MachineFault_MachineSourceType', 'MachineFault_EditControl', 'MF_HideMachineID', 'MF_HideMachinePlace']}
SYSTEM_FIELDS.update(MF_UseMachineCareDetail='IsUseMachineCase', MF_UseMachineInspectionDetail='IsUseMachineInspectionCase')


def parameter_value(name, query=rows):
    """GetSysParamValue的20字节输入和局部变量；原返回声明100不扩大局部值。"""
    matches = list(matching(query('SSysParams', 'erp_base'), ParamName=varchar(name, 20)).order_by('pk'))
    return None if not matches else varchar(raw(matches[-1], 'ParamValue'), 20)


def system_parameters(query=rows):
    """sp_App_sysGetSystemParams直接查原名，不能改为调用20字节名字函数。"""
    result = {}
    for output, name in SYSTEM_FIELDS.items():
        matches = list(matching(query('SSysParams', 'erp_base'), ParamName=name).order_by('pk'))
        result[output] = None if not matches else varchar(raw(matches[-1], 'ParamValue'), 10)
    return {'report': '原现场系统参数', 'rows': [result]}


def combo(combo_id, filter_text, query=rows):
    """sp_App_S_GetDBComboListByID；NULL过滤条件返回空集，原LIKE通配符仍有效。"""
    combo_id, filter_text = varchar(combo_id, 50), varchar(filter_text, 1000)
    result = []
    for item in matching(query('SDBComboValue', 'erp_base'), ComboID=combo_id).order_by('pk'):
        code, label = raw(item, 'KeyValue'), raw(item, 'DisplayValue')
        if equal(filter_text, '') or filter_text is not None and (sql_like(code, '%'+filter_text+'%') or sql_like(label, '%'+filter_text+'%')):
            result.append({'index': raw(item, 'DisplayIndex'), 'id': code, 'text': label})
    return {'report': '原组合框选项', 'rows': result,
            'notes': ['原过程不按DisplayIndex排序、不去重；同值及NULL原样保留。']}


def values(item):
    return {old: raw(item, old) for old in item.SOURCE_FIELDS}


def lookup(lookup_id, filter_text='', other_fields=(), query=rows):
    """原资料选择项；静态登记的查询使用当前项目及当前用户的数据范围。"""
    spec = LOOKUPS[lookup_id]
    adapter = spec['adapter']
    if adapter and adapter.get('engine')=='static_sql':
        from .source_static_lookup import lookup as static_lookup
        return {'report':'原资料选项 '+lookup_id,'implemented':True,
                'rows':static_lookup(spec,filter_text,other_fields,query),
                'notes':[spec.get('adaptation','原静态查询按当前项目数据执行；连接倍增保留。')]}
    if adapter and adapter.get('engine')=='external':
        return {'report':'原资料选项 '+lookup_id,'implemented':False,'status':'external_source_required','rows':[],
                'supplemental_rows':[{'lookup':lookup_id,'dataset':spec['DataTableName'],'query':spec['query'],
                    'issue':'原来源为192.168.23.254.ccs_erp中控库，当前快照不含该库的数据和字段；未以空数据替代。'}]}
    if adapter is None:
        return {'report': '原资料选项', 'rows': [], 'implemented': False,
                'supplemental_rows': [{'lookup': lookup_id, 'dataset': spec['DataTableName'],
                    'query': spec['query'], 'filter': spec['LookupDataFilter'], 'issue': '原联查/表达式尚未翻译，保留待办；不是原查询无数据。'}]}
    source = query(adapter['table'], 'erp_base')
    if adapter['table'] == 'PFieldValid':
        source = matching(source, FieldType=adapter['field_type'])
    output = []
    for item in source.order_by('pk'):
        value = values(item)
        if lookup_id == 'B062' and (value['DeptID'] is None or equal(value['DeptID'], '00')):
            continue
        if lookup_id in ['B001', 'A002'] and not equal(value['CustKindID'], '0'):
            continue
        if lookup_id == 'B001' and value['IsStop']:
            continue
        if lookup_id == 'A002' and (value['RightStatus'] != 10 or not equal(value['MasterCustomer'] or '', '')):
            continue
        if lookup_id == 'B006' and value['IsOut']:
            continue
        joins = [value]
        if lookup_id == 'B001':
            contacts = list(matching(query('PCustLinker', 'erp_base'), CustomerID=value['CustomerID']).filter(old_row_no=1).order_by('pk'))
            joins = [{**value, 'EbOd': str(value['EnableOrders'] or 0),
                      'Linker': None if contact is None else raw(contact, 'Name'),
                      'LinkerTel': None if contact is None else raw(contact, 'Mobile')} for contact in contacts or [None]]
        if lookup_id in ['B006', 'B154']:
            departments = list(matching(query('PDept', 'erp_base'), DeptID=value['DeptID']).order_by('pk'))
            joins = [{**{name: value[name] for name in ['EmpID', 'Name', 'IsOut', 'DeptID', 'EmpKind']},
                      'DeptIDName': None if department is None else raw(department, 'Name')} for department in departments or [None]]
        if lookup_id == 'A002':
            joins = [{name: value[name] for name in ['CustKindID', 'CustomerID', 'ShortName']}]
        if lookup_id == 'B405':
            joins = [{**value, 'unit': value['StockUnit']}]
        for row in joins:
            code, label = row[spec['KeyField']], row[spec['DisplayField']]
            text = varchar(filter_text, 1000)
            # 原动态SQL拼接NULL时无可执行SQL，本接口明确列为差异，不当作空字符串。
            if text is None:
                continue
            if equal(text, '') or sql_like(None if code is None else str(code), '%'+text+'%') or sql_like(None if label is None else str(label), '%'+text+'%'):
                output.append({'id': code, 'text': label, **{name: row[name] for name in other_fields}})
    return {'report': '原资料选项 '+lookup_id, 'implemented': True, 'rows': output,
            'notes': ['保留原过滤和连接倍增；附加列按原字段名显式选择，不解释用户提供的SQL表达式。',
                      '旧无序返回按项目ID顺序；完整旧动态SQL协议、全排序规则及NULL参数行为见E104。']}
