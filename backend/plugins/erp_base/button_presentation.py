"""逐项核查的操作归属；业务身份和接口权限保持独立。"""
import json
from pathlib import Path

POLICIES = json.loads(Path(__file__).with_suffix('.json').read_text(encoding='utf-8'))
DEFERRED = json.loads(Path(__file__).with_name('button_deferred.json').read_text(encoding='utf-8'))
DEFERRED_OPTIONS = set(DEFERRED['queries'] + DEFERRED['finance'] + DEFERRED['printing'])
TITLES = {
    'app_order_save': '现场订单录入', 'app_order_modify': '订单变更并保留原版',
    'open_first_card': '首次开卡', 'adopt_route': '选择路线并生成工序',
    'adopt_recipe_references': '选择配方来源', 'calculate': '本单公式补算',
    'phase6_formula': '公式核验与采用', 'confirm': '确认', 'reopen': '反审核／恢复编辑',
    'create_fault': '新增报修', 'save_fault': '编辑报修与附件',
    'create_equipment_document': '新增设备记录', 'save_equipment_document': '编辑设备记录及项目',
    'phase6_quote_to_order': '报价生成订单', 'phase6_quote_to_price_adjustment': '报价生成调价单',
    'phase6_purchase_to_arrival': '采购生成到货通知', 'phase6_purchase_to_product': '采购生成成品入库',
    'phase6_department_apply_to_purchase': '部门申请生成采购',
    'phase6_reverse_head_transfer': '撤销本次整单转入', 'phase6_reverse_line_transfer': '撤销本次明细转入',
    'phase6_reverse_quote_adjustment': '撤销报价转调价', 'phase6_care_plan_to_article_out': '保养配件领料',
    'original_quote_adjustment': '执行／撤销调价', 'refresh_order_prices': '补算订单收费',
    'refresh_recipe_costs': '全部配方成本重算', 'close_expired': '按180天规则结单',
    'site_records': '现场报工与补录', 'create_site_record': '新增报工／补录',
    'formal_dye_steps': '正式染程步骤', 'trial_steps': '试验染程步骤',
    'process_machines': '可选机台', 'entered_machine': '进缸机台',
    'charge_quote': '另收费明细', 'split_card': '拆卡', 'merge_cards': '合卡',
    'reverse_card': '撤销拆合计划', 'reverse_execution_chain': '撤销执行整链',
    'undo_execution_reverse': '撤回本次整链撤销', 'preview_execution_reverse': '预览整链撤销范围',
    'preview_package_pairing': '预览包装投坯配对', 'apply_package_pairing': '采用包装投坯配对',
    'preview_package_replace': '预览包装替换', 'replace_package': '同卡同卷替换包装',
    'preview_progress': '预览全库工序维护范围', 'maintain_progress': '全库工序进度维护',
    'material_receipts': '采购收货与退货记录', 'purchase_movements': '坯料及半成品采购收退',
    'outwork_closure': '结案与损耗明细', 'close_outwork': '确认损耗并结案',
    'reopen_outwork': '撤销外协结案', 'review_followup': '结案后收退变化',
    'trace_outwork': '外协收发退及质量来源', 'receive_package': '包装实际入库',
    'link_execution_source': '修复执行来源对应', 'continuation': '办理记录与接续来源',
    'phase2_report': '订单、报价及打样查询', 'phase3_report': '采购、外协及库存查询',
    'phase4_report': '生产、称料及设备查询', 'phase5_report': '质量、包装及交付查询',
    'phase3_operation': '收发及库存过程工具', 'phase4_operation': '工卡及包装过程工具',
    'phase5_operation': '收坯、交付及逆向过程工具', 'phase4_equipment': '设备表单保存工具',
    'phase3_carry': '库存结转／反结转', 'phase4_attendance': '考勤及包装计件计算',
    'phase4_function': '工卡工序函数核验', 'phase5_function': '包装交付函数核验',
    'synchronize_package_labels': '补同步包装及二维码数据', 'automatic_combine': '手工发起合卡同步',
    'sync_combined_process': '补同步合卡工序进度', 'update_result': '补回写打样结果',
    'quote_trigger_check': '报价触发规则核验', 'refresh_sample_book': '补同步小样收发',
    'preview_package_labels': '查看包装及二维码同步范围', 'undo_package_labels': '撤销包装及二维码数据同步',
    'undo_package_pairing': '撤销包装投坯配对', 'undo_package_replace': '撤销包装替换',
    'preview_auto_combine': '预览合卡选路', 'combine_members': '合卡成员及来源',
    'combine_group': '同流水合卡关系', 'preview_sample_variant': '预览打样变体',
    'apply_sample_variant': '采用打样变体', 'undo_sample_variant': '撤销打样变体采用',
    'preview_trial_work': '预览试验加色报工', 'apply_trial_work': '生成试验加色报工',
    'undo_trial_work': '撤销试验报工', 'rebuild_dye_quality': '重建选定范围的质量统计',
}
PROCESS_TOOLS = {'phase3_operation', 'phase4_operation', 'phase5_operation', 'phase4_equipment'}
REVERSALS = {
    'undo_package_labels':'package_label_sync', 'undo_package_pairing':'package_pairing',
    'undo_package_replace':'package_replacement', 'undo_execution_reverse':'execution_chain',
    'undo_sample_variant':'sample_variant', 'undo_trial_work':'trial_work',
    'undo_shift_work':'shift_work', 'undo_calendar':'calendar_generation',
}
TOPICS = {
    '执行整链撤销': {'preview_execution_reverse','reverse_execution_chain','undo_execution_reverse'},
    '包装投坯配对': {'preview_package_pairing','apply_package_pairing','undo_package_pairing'},
    '包装替换': {'preview_package_replace','replace_package','undo_package_replace'},
    '打样变体': {'preview_sample_variant','apply_sample_variant','undo_sample_variant'},
    '试验加色报工': {'preview_trial_work','apply_trial_work','undo_trial_work'},
    '报工人员调整': {'preview_shift_work','apply_shift_work','undo_shift_work'},
    '质量重建': {'preview_dye_quality','rebuild_dye_quality'},
    '工卡与路线': {'open_first_card','adopt_route','adopt_recipe','adopt_recipe_references','release','prepare','reprocess','to_production'},
    '报工与排程': {'create_site_record','site_records','schedule','reschedule','start','complete','skip','correct','resolve_shift','generate_calendar','undo_calendar','preview_calendar','preview_shift_work','apply_shift_work','undo_shift_work','delete_shift_record','perform_fault_action'},
    '拆合与细码': {'split_card','merge_cards','reverse_card','split_gray','merge_gray','undo_gray','adopt_combine_link','reverse_link','transfer_allocation','reverse_allocation','combine_members','combine_group'},
    '实际收发与交付': {'receive','receive_material','return_purchase','return_raw_purchase','dispatch_outwork','receive_outwork','receive_outwork_material','return_material','return_outwork_material','issue_to_job','transfer_to_job','issue_materials','receive_package','register_outgoing','add_outgoing_lines','confirm_delivery','dispatch_product','receive_return','deliver','undo_delivery','pack','adopt_gray_record','undo_gray_record','replace_package','undo_package_replace','apply_package_pairing','undo_package_pairing'},
    '质量与外协结案': {'judge','dispose','factory_quality','open_rework_card','close_outwork','reopen_outwork','close','rebuild_dye_quality','preview_dye_quality'},
    '撤销与更正': {'reverse_execution_chain','undo_execution_reverse','preview_execution_reverse','phase6_reverse_head_transfer','phase6_reverse_line_transfer','phase6_reverse_quote_adjustment','void','reverse','cancel','reopen'},
}


def present(entity, model, action):
    policy = POLICIES[entity + ':' + action['key']]
    key = action['key']
    item = {**action, **policy, 'display_title': TITLES.get(key, action['title'])}
    if key in REVERSALS:
        item['effect_required'] = REVERSALS[key]
    if entity == 'erp_sampling_sampleconfirmation' and key == 'send':
        item['hide_when'] = [*item.get('hide_when', []), 'sent_at']
    item['inputs'] = [{**field, 'options': [
        {**option, 'disabled': True, 'label': option['label'] + '（暂缓）'}
        if field['key'] in ['name', 'entry', 'function', 'operation'] and option['value'] in DEFERRED_OPTIONS
        else option for option in field.get('options', [])]}
        for field in action['inputs']]
    if key == 'create_site_record':
        item['inputs'].append({'key':'auto_shift','title':'按机台时间确定班组（不采用时可手填或留空）',
                               'kind':'boolean','default':True,'required':False,'options':[]})
    if key in PROCESS_TOOLS:
        item['placement'] = 'maintenance'
    if key == 'confirm' and item['title'] == '确认' and hasattr(model, 'SOURCE_TABLE'):
        item['placement'] = 'maintenance'
        item['display_title'] = '原确认阶段处理'
    if key == 'approve' and hasattr(model, 'SOURCE_TABLE'):
        if 'RightStatus' not in model.SOURCE_FIELDS:
            item['placement'] = 'maintenance'
        else:
            item['states'] = ['draft', 'confirmed']
    if item['placement'] == 'maintenance' or item['placement'] == 'automatic':
        item['topic'] = '业务维护'
    else:
        item['topic'] = next((title for title, keys in TOPICS.items() if key in keys),
                             '查询与统计' if any(word in item['title'] for word in ['查询','查看','统计','看板','核对','预览']) else '单据办理')
    return item


def effect_states(instance):
    """仅返回逆向按钮需要的办理状态，不暴露来源及业务明细。"""
    from core.resources import resource_options
    required = {REVERSALS[a['key']] for a in resource_options(type(instance)).get('workflow', {}).get('actions', [])
                if a['key'] in REVERSALS}
    if not required:
        return {}
    from .source_context import SourceDocumentContext
    context = SourceDocumentContext.objects.filter(entity=instance._meta.label, object_id=instance.pk).first()
    effects = context.effects if context is not None else {}
    return {name: effects[name]['state'] for name in required if name in effects}
