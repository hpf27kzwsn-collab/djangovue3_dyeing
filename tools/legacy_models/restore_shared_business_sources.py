"""恢复盘点确认的非财务业务来源；只更新本地模型目录，不连接旧库。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    'ClothGetMoney': ('erp_sales', '提货记录原表（ClothGetMoney）', True),
    'ClothGetMoneyDetail': ('erp_sales', '提货数量明细原表（ClothGetMoneyDetail）', False),
    'SalaryChanges': ('erp_production', '工卡及人员调整原表（SalaryChanges）', True),
    'SalaryChangesDetail': ('erp_production', '工卡及人员调整明细原表（SalaryChangesDetail）', False),
    'h_SalaryAttend': ('erp_base', '人员出勤原始汇总（h_SalaryAttend）', False),
    'h_SalaryWorkQty': ('erp_production', '员工工序产量原始汇总（h_SalaryWorkQty）', False),
    'h_SalaryWorkShift': ('erp_production', '班组工序产量原始汇总（h_SalaryWorkShift）', False),
    'ZKAttendanceMonthStatistics': ('erp_base', '考勤月统计原表（ZKAttendanceMonthStatistics）', False),
    'FARMain': ('erp_quality', '质量数量来源头（原FARMain）', False),
    'FARDetail': ('erp_quality', '质量数量来源明细（原FARDetail）', False),
    'FARRecord': ('erp_quality', '质量数量来源细码（原FARRecord）', False),
}
PARENTS = {
    'ClothGetMoneyDetail': ('ClothGetMoney', ['SheetSeries']),
    'SalaryChangesDetail': ('SalaryChanges', ['SheetSeries']),
    'FARDetail': ('FARMain', ['SheetSeries']),
    'FARRecord': ('FARDetail', ['SheetSeries', 'DetailNo']),
}


def restore():
    path = ROOT / 'tools/legacy_models/source_catalog.json'
    catalog = json.loads(path.read_text(encoding='utf-8'))
    tables = {row['table']: row for row in catalog['tables'] if row['schema'] == 'dye'}
    for name, (module, title, document) in SOURCES.items():
        table = tables[name]
        table.update(module=module, title=title, document=document, handling='business_model',
                     reason='P1盘点确认的提货、工卡调整、出勤产量或质量数量来源；原字段完整保留，独立财务办理暂缓',
                     classification_basis='2026-10-16最新结构、入口主从及原程序引用；见P1实施记录')
        if name in ['FARMain', 'FARDetail', 'FARRecord']:
            table['entry_scope'] = 'business_source_only'
    for name, (parent_name, fields) in PARENTS.items():
        parent = tables[parent_name]
        tables[name]['relations'] = [{
            'field': 'source_parent_1', 'title': '原关系：'+parent_name,
            'target': parent['module']+'.'+parent['model'],
            'source_fields': fields, 'target_fields': fields,
            'evidence': ['原界面主从 '+name+' → '+parent_name+'；SalaryChanges各变体均按SheetSeries'],
        }]
    path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('恢复11个原表模型、180个原字段、4组明确主从；FAR仅业务来源，不启用应收入口。')


if __name__ == '__main__':
    restore()
