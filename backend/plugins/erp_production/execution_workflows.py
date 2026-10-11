from .workflows import WORKFLOWS as PLAN,field,related,child,action,at,reason
employee=related('employee','操作员工','erp_base_employee','name')
unit=lambda key,title:related(key,title,'erp_base_unit','name',False)
outputs=[field('input_quantity','实际投入量','decimal',False,nullable=True),unit('input_unit','投入单位'),
    field('output_quantity','实际产出量','decimal',False,nullable=True),unit('output_unit','产出单位'),
    field('output_mass_kg','实际产出kg','decimal',False,nullable=True),
    field('output_length_m','实际长度m','decimal',False,nullable=True),field('output_pieces','实际粒数','decimal',False,nullable=True),
    field('defect_quantity','实际疵品量','decimal',False,nullable=True),field('quality_note','质量说明','textarea',False)]
start=[at,employee,related('machine','实际机台','erp_base_machine','name',False),related('shift','班次','erp_base_shift','name',False)]
WORKFLOWS={
    'WorkCardOperation':{**PLAN['WorkCardOperation'],'children':[*PLAN['WorkCardOperation']['children'],
        child('OperationExecution','本节点实际执行','operation')], 'actions':[*PLAN['WorkCardOperation']['actions'],
        action('start','实际开工',['released','running'],start),action('skip','明确跳过可选工序',['released','running'],[reason])]},
    'DyeBatch':{**PLAN['DyeBatch'],'children':[*PLAN['DyeBatch']['children'],
        child('PhysicalBatchExecution','同缸物理执行','batch'),child('WeighingOrder','阶段料单','batch',parent_states=['planned','scheduled','running'])],
        'actions':[*PLAN['DyeBatch']['actions'],action('start','同缸统一开工',['scheduled','running'],[
            related('process','实际工序','erp_base_process','name'),*start])]},
    'OperationExecution':{'readonly':True,'children':[child('ExecutionWorker','参与人员','execution',parent_states=['running']),
        child('ExecutionMeasurement','实际工艺参数','execution',parent_states=['running']),child('ExecutionCorrection','更正历史','execution')],
        'actions':[action('complete','实际完工',['running'],[at,*outputs]),action('correct','产量与时间更正',['completed'],[
            at,employee,reason,field('changes','本次更正项','changes',columns=[
                field('output_quantity','产出量','decimal',False,nullable=True),field('output_mass_kg','产出kg','decimal',False,nullable=True),
                field('started_at','实际开工','datetime',False,nullable=True),field('ended_at','实际完工','datetime',False,nullable=True)])])]},
    'PhysicalBatchExecution':{'readonly':True,'children':[child('OperationExecution','成员实际分配','physical_execution')],
        'actions':[action('complete','整缸完工及实绩分配',['running'],[at,field('output_mass_kg','整缸实际kg','decimal'),
            field('members','逐工卡实际量','rows',entity='erp_production_operationexecution',parent_key='physical_execution',
                source_key='id',source_from_row=True,identity_key='execution',label_key='work_card_number',columns=outputs,
                defaults={'input_quantity':None,'input_unit':None,'output_quantity':None,'output_unit':None,'output_mass_kg':None,
                    'output_length_m':None,'output_pieces':None,'defect_quantity':None,'quality_note':None})])]},
    'ExecutionWorker':{},'ExecutionMeasurement':{},'ExecutionCorrection':{'readonly':True},
    'ProductionRecipe':{**PLAN['ProductionRecipe'],'actions':[action('create_order','建立计划料单',['active'],[
        field('number','料单号'),at,field('kind','料单类型','select',options=[{'value':key,'label':label} for key,label in
            [('normal','常规'),('addition','加料'),('after_treatment','后处理'),('wash','洗缸')]]),field('reason','特殊料单依据','textarea',False)])]},
    'WeighingOrder':{'editable_states':['draft'],'children':[child('WeighingStage','料单阶段','order',True)],'actions':[
        action('confirm','确认计划',['draft'],[]),action('close','结束料单',['confirmed','partial_issued','issued'],[reason]),
        action('cancel','取消未采用料单',['draft','confirmed'],[reason])]},
    'WeighingStage':{'children':[child('WeighingLine','料单物料','stage',True)]},
    'WeighingLine':{'children':[child('WeighingRecord','实际称量','line')],'actions':[action('weigh','记录实际称量',['planned','weighed','issued'],[
        at,employee,field('quantity','实称数量','decimal'),related('unit','实称单位','erp_base_unit','name'),
        field('source','实称来源','select',options=[{'value':'manual','label':'人工实测'},{'value':'scale','label':'秤采集'}])])]},
    'WeighingRecord':{'readonly':True,'state_field':'is_void','actions':[action('void','作废原实称',[False],[at,reason])]},
    'QualityInspection':{'state_field':'result','editable_states':['pending'],'freeze_when':['is_void'],'children':[
        child('InspectionResultLine','实际检验项目','inspection',True),child('QualityDisposition','处置历史','inspection')],
        'actions':[dict(action('void','取消检验采用',['pending','pass','fail'],[at,reason]),hide_when=['is_void']),action('judge','检验判定',['pending'],[employee,field('result','实际判定','select',options=[
            {'value':'pass','label':'合格'},{'value':'fail','label':'不合格'}])]),action('dispose','明确数量处置',['pass','fail'],[
            at,employee,field('kind','实际处置','select',options=[{'value':key,'label':label} for key,label in [
                ('release','放行'),('concession','让步'),('rework','返修'),('downgrade','降级'),('scrap','报废'),('hold','隔离')]]),
            field('quantity','覆盖数量','decimal'),related('unit','覆盖单位','erp_base_unit','name'),reason,
            related('supersedes','被替换原处置','erp_production_qualitydisposition','id',False)])]},
    'InspectionResultLine':{},'QualityDisposition':{'readonly':True},
    'QualityDefect':{'editable_states':['open','handling'],'actions':[action('close','关闭异常',['open','handling'],[field('handling','处理说明','textarea')])]},
    'ReworkOrder':{'editable_states':['draft'],'actions':[action('release','下达独立返修路线',['draft'],[
        field('number','新返修工卡号'),related('route_version','返修路线版本','erp_base_routeversion','version'),at]),
        action('close','合格复检后结案',['reinspected'],[related('inspection','合格复检单','erp_production_qualityinspection','number'),reason])]},
}
for action_config in WORKFLOWS['QualityInspection']['actions']:
    action_config['hide_when']=['is_void']
for action_config in WORKFLOWS['OperationExecution']['actions']:
    action_config['hide_when']=['physical_execution']
WORKFLOWS['PhysicalExecutionCorrection']={'readonly':True}
WORKFLOWS['PhysicalBatchExecution']['children'].append(child('PhysicalExecutionCorrection','整缸更正历史','physical_execution'))
WORKFLOWS['PhysicalBatchExecution']['actions'].append(action('correct','整缸实绩更正',['completed'],[
    at,employee,reason,field('started_at','更正后实际开工','datetime'),field('ended_at','更正后实际完工','datetime'),
    field('output_mass_kg','更正后整缸kg','decimal'),field('members','更正后成员实绩','rows',
        entity='erp_production_operationexecution',parent_key='physical_execution',source_key='id',source_from_row=True,
        identity_key='execution',label_key='work_card_number',columns=[field('output_mass_kg','更正后成员kg','decimal')],defaults={'output_mass_kg':None})]))
WORKFLOWS['WorkCard']={**PLAN['WorkCard'],'actions':[*PLAN['WorkCard']['actions'],
    dict(action('pause','暂停工卡',['released','running'],[reason]),hide_when=['is_paused']),
    action('resume','恢复工卡',['released','running'],[reason]),action('complete','确认生产完成',['running'],[at,reason]),
    action('close','生产结案',['completed'],[at,reason]),action('reopen','按依据重新处理生产',['completed','closed'],[reason])]}
WORKFLOWS['DyeBatch']['actions'] += [action('complete','缸批生产完成',['running'],[reason]),action('close','缸批结案',['completed'],[reason])]
WORKFLOWS['WorkCardOrderAllocation']={**PLAN['WorkCardOrderAllocation'],'actions':[action('release_demand','按实际释放未完成需求',['completed','closed'],[at,field('quantity','本次明确释放量（分配单位）','decimal'),reason])],
    'state_from_parent':True}
WORKFLOWS['ReworkOrder']['actions'][0]['inputs'].append(field('allocations','承接原订单分配','rows',
    entity='erp_production_workcardorderallocation',parent_key='work_card',source_key='original_work_card',source_from_row=True,
    identity_key='original',label_key='order_number',selectable=True,required=False,columns=[
        field('quantity','实际承接数量','decimal'),related('unit','数量单位','erp_base_unit','name')],defaults={'quantity':None,'unit':None}))

WORKFLOWS['OperationExecution']['actions'].append(dict(action('abort','中止本轮实际执行',['running'],[at,reason]),hide_when=['physical_execution']))
WORKFLOWS['PhysicalBatchExecution']['actions'].append(action('abort','整缸中止本轮执行',['running'],[at,reason]))
member_inputs=WORKFLOWS['PhysicalBatchExecution']['actions'][0]['inputs'][2]
member_inputs['columns']=[{**column,**({'required':True,'nullable':False} if column['key']=='output_mass_kg' else {})} for column in outputs]
