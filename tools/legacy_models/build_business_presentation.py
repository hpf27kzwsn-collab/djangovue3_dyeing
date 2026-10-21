"""从已核查的入口标题生成业务展示名称；不改表、字段、路由或权限。"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
catalog=read('tools/legacy_models/source_catalog.json')
entries=read('backend/plugins/erp_base/source_entry_rules.json')['models']
foundation=read('backend/plugins/erp_base/foundation_catalog.json')['definitions']
names={}
for table in catalog['tables']:
    entity=table['module']+'_'+table['model'].lower()
    rules=entries.get(table['module']+'.'+table['model'],{})
    exact=[v['title'] for k,v in rules.items() if k.lower()==table['table'].lower()]
    titles={v['title'] for v in rules.values()}
    if exact:names[entity]=exact[0]
    elif len(titles)==1:names[entity]=next(iter(titles))
    elif '待确认' not in table['title']:names[entity]=table['title']
    else:names[entity]='资料（'+table['table']+'）'
for key,item in foundation.items():
    names[key]=item['title']
names.update({'erp':'染色ERP','erp_base_original':'业务资料与单据','erp_sales_original':'业务单据与明细',
 'erp_purchase_original':'业务单据与明细','erp_sampling_original':'业务单据与明细',
 'erp_production_original':'业务单据与明细','erp_warehouse_original':'业务单据与明细','erp_quality_original':'业务单据与明细',
 'erp_base_sourcedyepfieldvalid':'分类资料汇总','erp_base_sourcedyepfieldvalidsub':'分类明细汇总',
 'erp_base_sourcedyepcustomer':'往来单位汇总','erp_sales_sourcedyeordermain':'销售订单',
 'erp_production_sourcedyejobsheet':'生产工卡','erp_purchase_sourcedyepurmain':'采购订单',
 'erp_warehouse_sourcedyegrayin':'坯料入库单','erp_warehouse_sourcedyegrayout':'坯料出库单',
 'erp_base_sourcedyearrivalnotice':'到货通知','erp_base_businessaction':'操作记录',
 'erp_sampling_sourcedyelabdips':'打样记录','erp_sampling_sourcedyedyelabmain':'打样任务单',
 'erp_sampling_sourcedyedyerecipe':'染色配方','erp_warehouse_sourcedyeprodout':'成品出库单',
 'erp_sales_sourcedyequote':'客户报价','erp_base_legacyimportbatch':'资料导入批次',
 'erp_base_legacysourcetable':'资料来源登记','erp_base_legacyobjectmap':'记录对应关系',
 'erp_base_legacyimportissue':'资料核对事项','erp_base_sourcedyepwarehouse':'仓库资料（独立登记）',
 'foundation_short_warehouse_p_warehouse':'仓库资料（独立登记）',
 'erp_sampling_sourcedyedyeproduceitem':'工卡染色投料项目','erp_warehouse_sourcedyeweighttechinfo':'称料工艺参数',
 'erp_base_sourcedyesautoid':'业务编号计数','erp_base_sourcedyesflowrecord':'审批记录',
 'erp_base_sourcedyesrevision':'字段变更单','erp_base_sourcedyesrevisiondetail':'字段变更明细',
 'erp_base_sourcedyessavemessrule':'提交通知规则','erp_base_sourcedyessavemessruledetail':'提交通知规则明细',
 'erp_base_sourcedyessheetno':'单据编号规则','task_result':'任务运行记录','periodic_task':'定时任务'})
table_entities={t['table']:t['module']+'_'+t['model'].lower() for t in catalog['tables'] if t['schema']=='dye'}
preferred={module:[table_entities[t] for t in tables if t in table_entities] for module,tables in {
 'erp_sales':['OrderMain','Quote','OrderChange'], 'erp_purchase':['PurMain','ArrivalNotice','ApplyPur'],
 'erp_sampling':['LabDips','DyeLabMain','DyeRecipe'], 'erp_production':['JobSheet','WProcess','StuffWeight'],
 'erp_warehouse':['GrayIn','GrayOut','ProdOut'], 'erp_quality':['QualityRegister','Rework','QualityAccident']}.items()}
common=['erp_base_sourcedyepdept','erp_base_sourcedyehemployee','foundation_party_0','foundation_party_1',
 next(k for k,v in foundation.items() if v['filters']=={'old_field_type':'WareHouseID'}),
 'foundation_unit_width','foundation_unit_weight','erp_base_sourcedyepprocess']
preferred['erp_base']=common[:3]
result={'names':names,'common_keys':common,'preferred':preferred}
(ROOT/'web/src/erp-business-presentation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(len(names),'展示名称；菜单归属使用已授权的实际目录。')
