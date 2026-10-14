"""登记当前数据库程序和入口覆盖；登记不能代替业务对照通过。"""
import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
import sqlparse

ROOT = Path(__file__).resolve().parents[2]
IMPLEMENTED_PARTS = {
    'Sp_UpdateProdStockBook': '成品入/出库、盘点、30类修正流水及入库工卡回写；待真实单据对照',
    'Sp_UpdateJobSheetByProdIn': '按实际 JobReProdIn 参数回写新办理工卡；待真实单据对照',
    'Sp_JobProcessUpdate': '新办理工卡的实际工序进度；无序TOP1和子串范围采用明确排序及归属，见异常说明',
    'Sp_UpdateStuffStockBook': '染化料入/出库、调整、TO/SR调拨派生单及M计价主档价回写已接入；待真实单据对照',
    'Sp_UpdateArticleStockBook': '机物料入/出库及调整流水已接入；现行主档价回写段已注释，不新增生效动作；待真实单据对照',
    'Sp_UpdateGrayStockBook': '坯料入/出库、盘点、规格变更、调拨、收料细码单位、工卡细码领用及库位调整/反审已接入；对应差异见异常说明，待真实单据对照',
    'Sp_UpdateSemiStockBook': '半成品入/出库、盘点、规格变更、实际细码合理分配及工卡领用回写已接入；待实际单据对照',
    'sp_StuffWeightAutoStuffOut': '本库计划/实称采用、单位/WOF换算及一次领料已接入明确软件动作；外库与真实设备回传仍待接入',
    'Sp_InSertSemiOutRecord': '按收料单/条码/细码合理分配已接入，保留人工细码及历史；原重量符号/重复连接差异见异常文档',
    'Sp_UpdateJobOutAC': '各明确工卡分别回写当前出库单实配总量；多分组与名称冲突的合理处理见异常文档',
    'FD_GetFieldSeries': '日期、时间、表内/行内等编号已接入；原客户端模式和溢出采用说明见异常文档',
}


def build(path):
    evidence = json.loads(path.read_text(encoding='utf-8-sig'))
    catalog = json.loads((ROOT / 'tools/legacy_models/source_catalog.json').read_text(encoding='utf8'))
    tables = {(row['schema'], row['table']): row for row in catalog['tables'] if row['handling'] == 'business_model'}
    dependencies = defaultdict(list)
    for row in evidence['dependencies']:
        dependencies[(row['source_schema'], row['source_name'])].append(row)
    objects = {(row['schema_name'].lower(), row['table_name'].lower()) for row in evidence['tables']}
    objects |= {(row['schema_name'].lower(), row['object_name'].lower()) for row in evidence['modules']}
    modules = []
    for row in evidence['modules']:
        definition = row['definition']
        active = '' if definition is None else sqlparse.format(definition, strip_comments=True)
        refs = sorted(set(re.findall(r'\b(dye|dbo)\.\[?([A-Za-z_][A-Za-z_0-9]*)\]?', active, re.I)))
        missing = ['.'.join(ref) for ref in refs if tuple(part.lower() for part in ref) not in objects]
        source_refs = [dependency for dependency in dependencies[(row['schema_name'], row['object_name'])]
            if (dependency['referenced_schema_name'] or 'dye', dependency['referenced_entity_name']) in tables
            and dependency['referenced_database_name'] in [None, evidence['database']]]
        modules.append({'schema': row['schema_name'], 'name': row['object_name'], 'type': row['type'],
            'encrypted': bool(row['is_encrypted']), 'definition_available': definition is not None,
            'definition_sha256': None if definition is None else hashlib.sha256(definition.encode('utf8')).hexdigest(),
            'business_dependencies': source_refs, 'declared_dependencies': dependencies[(row['schema_name'], row['object_name'])],
            'qualified_references_missing_in_current_objects': missing,
            'status': IMPLEMENTED_PARTS.get(row['object_name'], '已取得原定义，待逐项翻译/对照' if definition is not None else '定义不可读取，需合理替代并登记'),
        })
    registry = json.loads((ROOT / 'backend/plugins/erp_base/source_entry_rules.json').read_text(encoding='utf8'))
    output = {'captured_at': evidence['captured_at'], 'database': evidence['database'],
        'scope': '全部现存程序、视图、触发器、函数；基础/业务依赖与外库依赖分别登记，财务独立范围仍忽略',
        'modules': modules, 'entry_binding_count': sum(map(len, registry['models'].values()))}
    (ROOT / 'tools/legacy_models/logic_coverage.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    lines = ['# 旧ERP当前程序与入口覆盖核对', '', '核对时间：' + evidence['captured_at'], '',
        '本表登记所有现存程序，保留空表、少用及停用业务的证据。状态写“已接入”的具体分支才有对应代码；源码可读取、存在模型或历史字段一致均不等于整个业务链对照通过。', '',
        f"当前732个数据库模块，731个定义可读取；新办理规则覆盖{output['entry_binding_count']}组模型/入口对应。", '',
        '数据库已声明依赖保存在 logic_coverage.json。动态SQL依赖不一定登记完整；以下“缺失引用”是去除注释后发现的限定名称，需结合语句上下文核实，不据此停用整项业务。', '',
        '| 原对象 | 类型 | 当前代码覆盖/待办 | 当前对象集缺失的限定引用 |', '|---|---|---|---|']
    for row in modules:
        missing = '、'.join(row['qualified_references_missing_in_current_objects']) or '—'
        lines.append(f"| {row['schema']}.{row['name']} | {row['type']} | {row['status']} | {missing} |")
    lines += ['', '## 当前可证明的特殊项', '',
        '- dye.f_num_chn 为加密函数，无法读取其实现；不能宣称已按原代码复刻。',
        '- GrayStockAllot 的原库存过程引用 GrayStockAllotDetail；当前物理表及现存视图中没有该对象。新代码使用当前调拨表头实际持有的转出/转入字段，原表头及原流水仍完整保留。',
        '- 染化料自动出库含 WeighingSystem、Textile_GXHFZD 及旧计量链路依赖；仅凭当前 Textile_GXHFRS 不能证明外部实际回传。历史出库与称料数据仍完整承接。',
        '- 当前库存流水服务的生成结果按新单据办理对应保存；历史加载不调用这些服务，不重演原出库或覆盖原库存流水。', '']
    (ROOT / 'docs/旧ERP当前程序与入口覆盖核对.md').write_text('\n'.join(lines), encoding='utf8')
    print(json.dumps({'modules': len(modules), 'definitions': sum(row['definition_available'] for row in modules), 'entry_bindings': output['entry_binding_count']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--evidence', type=Path, required=True)
    build(parser.parse_args().evidence)
