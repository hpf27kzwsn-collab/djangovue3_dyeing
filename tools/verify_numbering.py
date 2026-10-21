"""在已承接基础资料的独立PostgreSQL库核验编号；业务测试逐案回滚。"""
import os
import sys
import json
import traceback
from pathlib import Path
from datetime import date, datetime
from decimal import Decimal

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
import django
django.setup()
from django.apps import apps
from django.db import connection, transaction
from django.test.utils import setup_test_environment
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from plugins.erp_base.numbering_registry import SUGGESTIONS
from plugins.erp_base.numbering_models import NumberingRule
from plugins.erp_base import numbering
from plugins.erp_base.source_entry_registry import ENTRY_RULES
from plugins.erp_base.foundation_catalog import DEFINITIONS

assert str(connection.settings_dict['PORT']) == '5440', '此验证仅在5440独立库运行'
setup_test_environment()
actor = get_user_model().objects.get(username='xlsx-update-20261021')
client = APIClient(HTTP_HOST='localhost')
client.force_authenticate(actor)
output = ROOT / '.runtime-temp/numbering-implementation-20261021'
output.mkdir(exist_ok=True)
results = []
models = {r['target_model']: apps.get_model(r['target_model']) for r in SUGGESTIONS}
before = {key: model.objects.count() for key, model in models.items()}


def body_for(rule):
    model = apps.get_model(rule.target_model)
    query = model.objects.all()
    for key, value in rule.scope_filters.items():
        query = query.filter(**{key + '__in': value}) if isinstance(value, list) else query.filter(**{key: value})
    item = query.order_by('id').first()
    body = {} if item is None else {key: getattr(item, key) for key in model.SOURCE_FIELDS.values() if key not in model.SOURCE_IDENTITIES}
    for key in list(body):
        if isinstance(body[key], (datetime, date, Decimal)):
            body[key] = str(body[key])
        if isinstance(body[key], (bytes, memoryview)):
            body.pop(key)
    for key, value in rule.scope_filters.items():
        body[key] = value[0] if isinstance(value, list) else value
    profiles = [d for d in DEFINITIONS.values() if d['model'] == model._meta.label and not d.get('readonly')
                and all(body.get(k) == v for k, v in d['filters'].items()) and d['entry'] is not None]
    profile = next((d for d in profiles if d['filters']), profiles[0] if profiles else None)
    entry = profile['entry'] if profile else next(iter(ENTRY_RULES[model._meta.label]))
    body['_entry'] = entry
    body.pop(rule.target_field, None)
    if model.SOURCE_TABLE == 'p_Customer':
        body.pop('old_num', None)
    for old in ['Name', 'NameC', 'ShortName']:
        if old in model.SOURCE_FIELDS:
            body[model.SOURCE_FIELDS[old]] = '编号验证' + str(rule.pk)
    return model, body


def post(model, body):
    response = client.post('/api/system/' + model._meta.label_lower.replace('.', '_') + '/', body, format='json')
    assert response.status_code in [200, 201], str(response.data)
    return model.objects.get(pk=response.data['data']['id'])


def case(name, operation):
    try:
        with transaction.atomic():
            detail = operation()
            transaction.set_rollback(True)
        results.append({'name': name, 'passed': True, 'detail': detail})
        print('PASS', name, flush=True)
    except Exception as error:
        results.append({'name': name, 'passed': False, 'error': str(error), 'traceback': traceback.format_exc()})
        print('FAIL', name, str(error)[:450], flush=True)


for rule in NumberingRule.objects.order_by('id'):
    def automatic(rule=rule):
        model, body = body_for(rule)
        expected = numbering.preview(rule)['code']
        item = post(model, body)
        assert getattr(item, rule.target_field) == expected, (getattr(item, rule.target_field), expected)
        if body['_entry'] == 'p_Supplier':
            assert item.old_num == item.old_customer_id
        if body['_entry'] == 'p_Customer':
            assert item.old_num == 'K' + item.old_customer_id
        rule.refresh_from_db()
        assert rule.last_number == numbering.suffix(rule, expected)
        return {'code': expected, 'entry': body['_entry']}
    case(rule.name + ' 自动保存', automatic)


def manual_policy():
    rule = NumberingRule.objects.get(name='供应商')
    model, body = body_for(rule)
    body['old_num'] = 'G900'
    item = post(model, body)
    assert item.old_customer_id == item.old_num == 'G900'
    rule.refresh_from_db()
    assert rule.last_number == 900
    assert numbering.preview(rule)['code'] == 'G901'
    NumberingRule.objects.filter(pk=rule.pk).update(allow_manual_input=False)
    response = client.post('/api/system/erp_base_sourcedyepcustomer/', body, format='json')
    assert response.status_code == 400
    body.pop('old_num')
    assert post(model, body).old_customer_id == 'G901'
    return '供应商别名不绕过禁止手工输入，自动号仅消耗一次'
case('手工别名及上限', manual_policy)


def change_policy():
    rule = NumberingRule.objects.get(name='幅宽克重单位共用号码池')
    NumberingRule.objects.filter(pk=rule.pk).update(allow_code_change=False)
    model, body = body_for(rule)
    item = post(model, body)
    url = '/api/system/' + model._meta.label_lower.replace('.', '_') + '/' + str(item.pk) + '/'
    response = client.patch(url, {rule.target_field: item.old_code}, format='json')
    assert response.status_code == 200, str(response.data)
    response = client.patch(url, {rule.target_field: 'VEDIT'}, format='json')
    assert response.status_code == 400
    NumberingRule.objects.filter(pk=rule.pk).update(allow_code_change=True)
    response = client.patch(url, {rule.target_field: 'VEDIT'}, format='json')
    assert response.status_code == 200, str(response.data)
    item.refresh_from_db()
    assert item.old_code == 'VEDIT'
    return '相同值可提交；禁止更改生效；未引用编号可明确更改'
case('修改编号', change_policy)


def shared_pool():
    rule = NumberingRule.objects.get(name='幅宽克重单位共用号码池')
    model, body = body_for(rule)
    expected = numbering.preview(rule)['next_number']
    a = post(model, {**body, 'old_kind': 0})
    b = post(model, {**body, 'old_kind': 1})
    assert int(a.old_code) == int(expected) and int(b.old_code) == int(expected) + 1
    return [a.old_code, b.old_code]
case('幅宽克重共用流水', shared_pool)


def preview_rollback():
    rule = NumberingRule.objects.get(name='部门')
    high = rule.last_number
    assert numbering.preview(rule) == numbering.preview(rule)
    rule.refresh_from_db()
    assert rule.last_number == high
    model, body = body_for(rule)
    bad = {**body, 'old_name': 'X' * 1000}
    response = client.post('/api/system/erp_base_sourcedyepdept/', bad, format='json')
    assert response.status_code == 400
    rule.refresh_from_db()
    assert rule.last_number == high
    NumberingRule.objects.filter(pk=rule.pk).update(last_number=99)
    response = client.post('/api/system/erp_base_sourcedyepdept/', body, format='json')
    assert response.status_code == 400 and '流水' in str(response.data)
    return '预览不占号；失败保存回滚；溢出不截断'
case('预览、失败与溢出', preview_rollback)


def manual_only():
    rule = NumberingRule.objects.get(name='部门')
    NumberingRule.objects.filter(pk=rule.pk).update(auto_enabled=False)
    model, body = body_for(rule)
    response = client.post('/api/system/erp_base_sourcedyepdept/', body, format='json')
    assert response.status_code == 400
    item = post(model, {**body, rule.target_field: 'M1'})
    assert item.old_dept_id == 'M1'
    return '关闭自动编号后不调用旧DateCode规则'
case('手工专用规则', manual_only)


def config():
    rule = NumberingRule.objects.get(name='客户')
    data = {key: getattr(rule, key) for key in ['name', 'target_model', 'target_field', 'scope_key', 'prefix', 'digits', 'start_number', 'auto_enabled', 'allow_manual_input', 'allow_code_change']}
    endpoint = '/api/system/erp_base_numberingrule/'
    response = client.post(endpoint + 'preview/', {**data, '_id': rule.pk}, format='json')
    assert response.status_code == 200, str(response.data)
    high = rule.last_number
    assert client.patch(endpoint + str(rule.pk) + '/', {'last_number': 0}, format='json').status_code == 400
    assert client.patch(endpoint + str(rule.pk) + '/', {'auto_enabled': False, 'allow_manual_input': False}, format='json').status_code == 400
    supplier = NumberingRule.objects.get(name='供应商')
    assert client.patch(endpoint + str(supplier.pk) + '/', {'prefix': ''}, format='json').status_code == 400
    assert client.patch(endpoint + str(supplier.pk) + '/', {'prefix': '', 'digits': 4}, format='json').status_code == 400
    rule.refresh_from_db()
    assert rule.last_number == high
    return '配置预览、只读上限、规则互斥、共池格式冲突检查通过'
case('编号配置API', config)


def excel_paths():
    from io import BytesIO
    from openpyxl import load_workbook
    from django.core.files.uploadedfile import SimpleUploadedFile
    from plugins.erp_base.source_excel_history import columns
    from system.excel import write_workbook
    rule = NumberingRule.objects.get(name='幅宽克重单位共用号码池')
    model, body = body_for(rule)
    base = '/api/system/' + model._meta.label_lower.replace('.', '_') + '/'
    response = client.get(base + 'import_template/', {'_entry': body['_entry']})
    assert response.status_code == 200
    book = load_workbook(BytesIO(b''.join(response.streaming_content)))
    assert any('编号管理' in str(row) for row in book['填写说明'].values)
    titles = {str(model._meta.get_field(key).verbose_name): key for key in model.SOURCE_FIELDS.values()}
    sheet = book['数据']
    headers = [c.value for c in sheet[1]]
    for ordinal, code in enumerate([None, '899', '899'], 1):
        row = dict(body)
        row[rule.target_field] = code
        sheet.append([ordinal if title == '序号' else row['_entry'] if title == '业务入口' else row.get(titles.get(title)) for title in headers])
    stream = BytesIO()
    book.save(stream)
    response = client.post(base + 'import/', {'file': SimpleUploadedFile('编号测试.xlsx', stream.getvalue())}, format='multipart')
    assert response.status_code == 200, str(response.data)
    assert response.data['data']['created'] == 3
    assert model.objects.filter(old_code='899', source_batch__isnull=True).count() == 2
    rule.refresh_from_db()
    assert rule.last_number == 899
    NumberingRule.objects.filter(pk=rule.pk).update(allow_manual_input=False)
    count = model.objects.count()
    response = client.post(base + 'import/', {'file': SimpleUploadedFile('禁止手工整批.xlsx', stream.getvalue())}, format='multipart')
    assert response.status_code == 400, str(response.data)
    assert model.objects.count() == count
    rule.refresh_from_db()
    assert rule.last_number == 899, '首行已取900也应随整批失败回滚'
    original = {key: body.get(key) for key in model.SOURCE_FIELDS.values()}
    original.update(old_code='950', old_name_c=None)
    history = BytesIO()
    write_workbook([original, original], columns(model), history, 'create', {'导入方式': '历史基础资料原值承接'})
    response = client.post(base + 'import/', {'file': SimpleUploadedFile('历史重复.xlsx', history.getvalue())}, format='multipart')
    assert response.status_code == 200, str(response.data)
    imported = model.objects.filter(old_code='950')
    assert imported.count() == 2 and imported.filter(old_name_c__isnull=True).count() == 2
    assert list(imported.order_by('source_row').values_list('source_row', flat=True)) == [1, 2]
    rule.refresh_from_db()
    assert rule.last_number == 950
    # 留出一个明确空字符串与NULL并存的历史事实。
    original.update(old_code='', old_name_c='')
    history = BytesIO()
    write_workbook([original], columns(model), history, 'create', {'导入方式': '历史基础资料原值承接'})
    response = client.post(base + 'import/', {'file': SimpleUploadedFile('历史空文本.xlsx', history.getvalue())}, format='multipart')
    assert response.status_code == 200, str(response.data)
    return '普通Excel自动号/重复手填，禁止手工整批回滚，历史重复/NULL/空串保留并同步上限'
case('真实Excel新增与历史承接', excel_paths)


def referenced_change():
    rule = NumberingRule.objects.get(name='客户')
    model, body = body_for(rule)
    item = post(model, body)
    NumberingRule.objects.filter(pk=rule.pk).update(allow_code_change=True)
    child = apps.get_model('erp_base.SourceDyePFabricCust')
    child.objects.create(old_customer_id=item.old_customer_id, old_kind=0)
    response = client.patch('/api/system/erp_base_sourcedyepcustomer/' + str(item.pk) + '/', {'old_customer_id': 'VCNEW'}, format='json')
    assert response.status_code == 400, str(response.data)
    item.refresh_from_db()
    assert item.old_customer_id != 'VCNEW'
    return '原关联码存在、尚未建立FK时仍识别引用，不批量改写旧码'
case('未对应FK的原码引用', referenced_change)


def legacy_sequence():
    import hashlib
    from plugins.erp_base.source_sequences import SourceIdentitySequence
    rule = NumberingRule.objects.get(name='员工')
    definition = next(r['number_fields']['EmpID'] for r in ENTRY_RULES[rule.target_model].values()
                      if 'EmpID' in r['number_fields'] and r['number_fields']['EmpID']['Prefix'] == 'HF')
    kind = definition['FieldKind']
    scope = {'kind': kind, 'prefix': 'HF'} if kind == 'AutoAdd' else {'kind': kind, 'scope': {}, 'series': '', 'prefix': 'HF'}
    encoded = json.dumps(scope, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    namespace = rule.target_model + '.' + rule.target_field + ':' + hashlib.sha256(encoded.encode()).hexdigest()[:32]
    SourceIdentitySequence.objects.update_or_create(namespace=namespace, defaults={'last_number': 8888})
    assert numbering.preview(rule)['code'] == 'HF8889'
    return '可明确对应的旧计数器高水位被继承，不回退取已删除旧号'
case('既有计数器高水位', legacy_sequence)


def supplier_scope_bypass():
    rule = NumberingRule.objects.get(name='供应商')
    model, body = body_for(rule)
    item = post(model, body)
    response = client.patch('/api/system/erp_base_sourcedyepcustomer/' + str(item.pk) + '/', {'old_customer_id': 'BYPASS', 'old_cust_kind_id': '9'}, format='json')
    assert response.status_code == 400, str(response.data)
    return '更换为未配置类别不能绕过原类别禁止改码'
case('分类切换不能绕过改码策略', supplier_scope_bypass)


def true_save_failure():
    # 让错误发生在已经取号之后，验证数据库事务，而非只验证序列化输入错误。
    from unittest.mock import patch
    from django.core.exceptions import ValidationError
    from plugins.erp_base.source_services import write
    rule = NumberingRule.objects.get(name='幅宽克重单位共用号码池')
    model, body = body_for(rule)
    high = rule.last_number
    with transaction.atomic():
        with patch.object(model, 'full_clean', side_effect=ValidationError({'old_name': '取号后模拟业务保存失败'})):
            try:
                write(model, body, actor=actor)
            except ValidationError:
                pass
            else:
                raise AssertionError('预期保存失败')
    rule.refresh_from_db()
    assert rule.last_number == high
    return '已取号后业务校验失败，规则行与单据一并回滚'
case('取号后真实事务回滚', true_save_failure)


def legacy_documents():
    from django.utils import timezone
    from plugins.erp_base.source_phase3_operations import model
    from plugins.erp_base.source_numbers import generate
    evidence = {}
    for table, entry, old in [('OrderMain', 'OrderMain', 'SheetNo'), ('OrderMain', 'OrderMain', 'SheetSeries')]:
        target = model(table)
        definition = ENTRY_RULES[target._meta.label][entry]['number_fields'][old]
        value = generate(target(), old, definition, actor, timezone.localtime())
        assert value
        evidence[old] = {'mode': definition['FieldKind'], 'value': str(value)}
    from plugins.erp_base.source_services import write
    customer = NumberingRule.objects.get(name='客户')
    customer_model, body = body_for(customer)
    source = post(customer_model, body)
    order = write(model('OrderMain'), {'_entry': 'OrderMain', 'old_customer_id': source.old_customer_id}, actor=actor)
    assert order.old_sheet_no and order.old_sheet_series
    configured = numbering.save_rule({'name': '验证订单简单规则', 'target_model': order._meta.label,
        'target_field': 'old_sheet_no', 'scope_key': 'entry:OrderMain', 'prefix': 'NV', 'digits': 5,
        'start_number': 1, 'allow_manual_input': False}, actor)
    generated = generate(model('OrderMain')(), 'SheetNo', ENTRY_RULES[order._meta.label]['OrderMain']['number_fields']['SheetNo'], actor, timezone.localtime())
    new = write(model('OrderMain'), {'_entry': 'OrderMain', 'old_customer_id': source.old_customer_id, 'old_sheet_no': generated}, actor=actor)
    assert new.old_sheet_no == 'NV00001'
    configured.refresh_from_db()
    assert configured.last_number == 1
    return {'legacy': evidence, 'explicit_override': new.old_sheet_no}
case('原单号及自动建单服务接入', legacy_documents)


def global_material_pool():
    from plugins.erp_base.business import persist
    rule = NumberingRule.objects.get(name='A系列染化料')
    model, body = body_for(rule)
    item = model(old_stuff_id='a998 ', old_stuff_kind_id='ZZ')
    persist(item, actor)
    rule.refresh_from_db()
    assert rule.last_number == 998
    expected = numbering.preview(rule)['code']
    assert expected == 'A999'
    return '其他类别的同前缀原码也计入全表号码池，按原不区分大小写与尾空格比较'
case('物料全表号码池与原排序规则', global_material_pool)


def historical_edit():
    rule = NumberingRule.objects.get(name='幅宽克重单位共用号码池')
    model = apps.get_model(rule.target_model)
    item = model.objects.filter(source_batch__isnull=False).first()
    NumberingRule.objects.filter(pk=rule.pk).update(allow_code_change=False)
    url = '/api/system/' + model._meta.label_lower.replace('.', '_') + '/' + str(item.pk) + '/'
    response = client.patch(url, {'old_code': 'HISTNEW'}, format='json')
    assert response.status_code == 400, str(response.data)
    item.refresh_from_db()
    response = client.patch(url, {'old_code': item.old_code, 'remarks': '原值同值提交'}, format='json')
    assert response.status_code == 200, str(response.data)
    return '历史新增不发号；历史行编辑受更改权限控制，相同值不视为改号'
case('历史记录编号编辑边界', historical_edit)


def optional_candidate():
    configured = numbering.save_rule({'name': '验证空表选配', 'target_model': 'erp_quality.SourceDyePTestItem',
        'target_field': 'old_item_id', 'scope_key': 'all', 'prefix': 'QT', 'digits': 3, 'start_number': 1}, actor)
    target = apps.get_model(configured.target_model)
    item = post(target, {'old_item_name': '独立验证质量项目'})
    assert item.old_item_id == 'QT001'
    return '无旧数据的登记资料可自行配规则，不伪装为29条有证据的预置规则'
case('空表候选模型接入', optional_candidate)


def concurrent_saves():
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    from django.db import connections
    rule = NumberingRule.objects.get(name='幅宽克重单位共用号码池')
    model, body = body_for(rule)
    initial = int(numbering.preview(rule)['next_number'])
    barrier = Barrier(8)
    ids = []
    def worker(index):
        local = APIClient(HTTP_HOST='localhost')
        local.force_authenticate(actor)
        barrier.wait(timeout=30)
        try:
            response = local.post('/api/system/' + model._meta.label_lower.replace('.', '_') + '/',
                {**body, 'old_name_c': '并发测试' + str(index)}, format='json')
            assert response.status_code in [200, 201], str(response.data)
            pk = response.data['data']['id']
            ids.append(pk)
            return model.objects.get(pk=pk).old_code
        finally:
            connections.close_all()
    try:
        with ThreadPoolExecutor(max_workers=8) as executor:
            codes = list(executor.map(worker, range(8)))
        assert sorted(int(code) for code in codes) == list(range(initial, initial + 8)), codes
        # 成功保存再删除，不回收已发号码。
        response = client.delete('/api/system/' + model._meta.label_lower.replace('.', '_') + '/' + str(ids[-1]) + '/')
        assert response.status_code == 200, str(response.data)
        rule.refresh_from_db()
        assert int(numbering.preview(rule)['next_number']) == initial + 8
        return {'workers': 8, 'codes': sorted(codes), 'deleted_code_not_reused': True}
    finally:
        model.objects.filter(pk__in=ids).delete()


try:
    detail = concurrent_saves()
    results.append({'name': '8连接并发保存及删除不回收', 'passed': True, 'detail': detail})
    print('PASS 8连接并发保存及删除不回收', flush=True)
except Exception as error:
    results.append({'name': '8连接并发保存及删除不回收', 'passed': False, 'error': str(error), 'traceback': traceback.format_exc()})
    print('FAIL 并发', str(error), flush=True)

assert {key: model.objects.count() for key, model in models.items()} == before
report = {'database': connection.settings_dict['NAME'], 'port': '5440', 'cases': len(results),
          'passed': sum(r['passed'] for r in results), 'all_business_cases_rolled_back': True, 'business_counts_unchanged': before,
          'results': results}
(output / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf8')
print(json.dumps({'cases': report['cases'], 'passed': report['passed']}, ensure_ascii=False))
sys.exit(0 if report['cases'] == report['passed'] else 1)
