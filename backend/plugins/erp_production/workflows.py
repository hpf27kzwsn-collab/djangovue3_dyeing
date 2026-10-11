"""页面只开放对应业务动作，不直接编辑状态和采用事实。"""
def field(key, title, kind='text', required=True, **extra):
    return {'key': key, 'title': title, 'kind': kind, 'required': required, 'options': [], **extra}


def related(key, title, entity, label, required=True, **extra):
    return field(key, title, 'select', required, remote={'entity': entity, 'pk': 'id', 'label': label}, **extra)


def child(name, title, key, atomic=False, **extra):
    return {'entity': 'erp_production_'+name.lower(), 'title': title, 'key': key, 'atomic': atomic, **extra}


def action(key, title, states, inputs):
    return {'key': key, 'title': title, 'states': states, 'inputs': inputs}


reason = field('reason', '原因', 'textarea')
at = field('at', '实际时间', 'datetime')
slot = [related('machine', '机台', 'erp_base_machine', 'name'), field('planned_start', '计划开始', 'datetime'),
        field('planned_end', '计划结束', 'datetime')]
WORKFLOWS = {
    'WorkCard': {'editable_states': ['draft'], 'children': [
        child('WorkCardOrderAllocation', '订单分配', 'work_card', True),
        child('WorkCardOperation', '计划工序', 'work_card', parent_states=['draft','released','running']),
        child('WorkCardRequirement', '采用要求', 'work_card', True)], 'actions': [
        action('prepare', '展开路线与订单要求', ['draft'], [field('steps', '采用节点', 'multi',
            remote={'entity':'erp_base_routestep','pk':'id','label':'sequence'}, params_from_row={'route_version':'route_version'})]),
        action('release', '下达工卡', ['draft'], [at]), action('cancel', '取消工卡', ['draft','released'], [reason])]},
    'WorkCardOrderAllocation': {},
    'WorkCardRequirement': {},
    'DyeBatch': {'editable_states':['planned'], 'children': [
        child('DyeBatchWorkCard','缸批成员','batch',True),
        child('ProductionRecipe','采用配方','batch')], 'actions': [
        action('cancel','取消缸批',['planned','scheduled'],[reason]),
        action('adopt_recipe','采用生产配方',['planned','scheduled'],[
            related('recipe_version','配方版本','erp_sampling_recipeversion','version'), at,
            field('dry_mass_kg','计算干料kg','decimal'), field('stages','阶段采用','rows',
                entity='erp_sampling_recipestage', parent_key='version', source_key='recipe_version', identity_key='stage',
                label_key='sequence', columns=[field('water_amount','实际采用浴液量','decimal',False,nullable=True),
                    related('water_unit','浴液单位','erp_base_unit','name',False),
                    field('density','质量浴液密度kg/L','decimal',False,nullable=True),
                    field('adjustment_percent','剂量调整%','decimal',True)],
                defaults={'water_amount':None,'water_unit':None,'density':None,'adjustment_percent':'0'})])]},
    'DyeBatchWorkCard': {'children':[child('DyeBatchAllocation','本缸订单分配','batch_work_card',True)]},
    'DyeBatchAllocation': {},
    'WorkCardOperation': {'readonly':True, 'state_from_parent':True, 'children':[
        child('OperationParameter','参数快照','operation',parent_states=['draft']),
        child('ScheduleAssignment','排程历史','operation')], 'actions':[
        action('schedule','人工排程',['released','running'],[*slot,related('batch','共用缸批','erp_production_dyebatch','number',False)])]},
    'OperationParameter': {},
    'ScheduleAssignment': {'readonly':True, 'actions':[
        action('publish','发布安排',['planned'],[]),action('reschedule','改排',['planned','released'],[*slot,reason]),
        action('cancel','取消安排',['planned','released'],[reason])]},
    'ProductionRecipe': {'readonly':True,'children':[child('MaterialPlanStage','采用阶段','production_recipe')]},
    'MaterialPlanStage': {'readonly':True,'children':[child('MaterialPlanLine','用料计划','stage')]},
    'MaterialPlanLine': {'readonly':True},
}
