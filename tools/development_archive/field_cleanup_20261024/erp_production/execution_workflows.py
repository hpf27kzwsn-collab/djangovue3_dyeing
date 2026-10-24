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
'WorkCardOperation': {**PLAN['WorkCardOperation'],'children':[*PLAN['WorkCardOperation']['children'],
        child('OperationExecution','本节点实际执行','operation')], 'actions':[*PLAN['WorkCardOperation']['actions'],
        action('start','实际开工',['released','running'],start),action('skip','明确跳过可选工序',['released','running'],[reason])]},
'DyeBatch': {**PLAN['DyeBatch'],'children':[*PLAN['DyeBatch']['children'],
        child('PhysicalBatchExecution','同缸物理执行','batch'),child('WeighingOrder','阶段料单','batch',parent_states=['planned','scheduled','running'])],
        'actions':[*PLAN['DyeBatch']['actions'],action('start','同缸统一开工',['scheduled','running'],[
            related('process','实际工序','erp_base_process','name'),*start])]},
'OperationExecution': {'readonly':True,'children':[child('ExecutionWorker','参与人员','execution',parent_states=['running']),
        child('ExecutionMeasurement','实际工艺参数','execution',parent_states=['running']),child('ExecutionCorrection','更正历史','execution')],
        'actions':[action('complete','实际完工',['running'],[at,*outputs]),action('correct','产量与时间更正',['completed'],[
            at,employee,reason,field('changes','本次更正项','changes',columns=[
                field('output_quantity','产出量','decimal',False,nullable=True),field('output_mass_kg','产出kg','decimal',False,nullable=True),
                field('started_at','实际开工','datetime',False,nullable=True),field('ended_at','实际完工','datetime',False,nullable=True)])])]},
'PhysicalBatchExecution': {'readonly':True,'children':[child('OperationExecution','成员实际分配','physical_execution')],
        'actions':[action('complete','整缸完工及实绩分配',['running'],[at,field('output_mass_kg','整缸实际kg','decimal'),
            field('members','逐工卡实际量','rows',entity='erp_production_operationexecution',parent_key='physical_execution',
                source_key='id',source_from_row=True,identity_key='execution',label_key='work_card_number',columns=outputs,
                defaults={'input_quantity':None,'input_unit':None,'output_quantity':None,'output_unit':None,'output_mass_kg':None,
                    'output_length_m':None,'output_pieces':None,'defect_quantity':None,'quality_note':None})])]},
'ExecutionWorker': {},
'ExecutionMeasurement': {},
'ExecutionCorrection': {'readonly':True},
'ProductionRecipe': {**PLAN['ProductionRecipe'],'actions':[action('create_order','建立计划料单',['active'],[
        field('number','料单号'),at,field('kind','料单类型','select',options=[{'value':key,'label':label} for key,label in
            [('normal','常规'),('addition','加料'),('after_treatment','后处理'),('wash','洗缸')]]),field('reason','特殊料单依据','textarea',False)])]},
'WeighingOrder': {'editable_states':['draft'],'children':[child('WeighingStage','料单阶段','order',True)],'actions':[
        action('confirm','确认计划',['draft'],[]),action('close','结束料单',['confirmed','partial_issued','issued'],[reason]),
        action('cancel','取消未采用料单',['draft','confirmed'],[reason])]},
'WeighingStage': {'children':[child('WeighingLine','料单物料','stage',True)]},
'WeighingLine': {'children':[child('WeighingRecord','实际称量','line')],'actions':[action('weigh','记录实际称量',['planned','weighed','issued'],[
        at,employee,field('quantity','实称数量','decimal'),related('unit','实称单位','erp_base_unit','name'),
        field('source','实称来源','select',options=[{'value':'manual','label':'人工实测'},{'value':'scale','label':'秤采集'}])])]},
'WeighingRecord': {'readonly':True,'state_field':'is_void','actions':[action('void','作废原实称',[False],[at,reason])]},
'ReworkOrder': {'editable_states':['draft'],'actions':[action('release','下达独立返修路线',['draft'],[
        field('number','新返修工卡号'),related('route_version','返修路线版本','erp_base_routeversion','version'),at]),
        action('close','合格复检后结案',['reinspected'],[related('inspection','合格复检单','erp_quality_qualityinspection','number'),reason])]}
}
