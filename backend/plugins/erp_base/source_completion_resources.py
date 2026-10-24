"""剩余链的具体业务动作及两组原主从；不更换原模型或原码。"""
def field(key,title,kind='text',**extra):return {'key':key,'title':title,'kind':kind,'required':False,'options':[],**extra}


def remote(table,label):
    entity={'p_FieldValid':'erp_base_sourcedyepfieldvalid','OrderMain':'erp_sales_sourcedyeordermain',
        'JobSheet':'erp_production_sourcedyejobsheet','JobProcess':'erp_production_sourcedyejobprocess',
        'ProdOutDetail':'erp_warehouse_sourcedyeprodoutdetail','DyeLabColor':'erp_sampling_sourcedyedyelabcolor','DyeRecipe':'erp_sampling_sourcedyedyerecipe'}[table]
    key={'Name':'old_name','SheetNo':'old_sheet_no','ProcessID':'old_process_id','DetailNo':'old_detail_no','ColorNo':'old_color_no'}[label]
    extra={'p_FieldValid':[('old_code','路线编码')],'OrderMain':[('old_sheet_series','原流水'),('old_customer_id','客户编码')],
        'JobSheet':[('old_sheet_series','原流水'),('old_prod_id','物料编码')],
        'JobProcess':[('old_sheet_series','工卡原流水'),('old_process_no','工序序号')],
        'ProdOutDetail':[('old_job_sheet_no','工卡号'),('old_weight_qty','重量数量'),('old_rolls','粒数')],
        'DyeLabColor':[('old_sheet_series','来样原流水'),('old_color_num','色号')],
        'DyeRecipe':[('old_sheet_series','配方原流水'),('old_color_num','色号'),('old_sheet_kind','原配方类别')]}[table]
    return {'entity':entity,'pk':'id','label':key,'columns':[{'field':'id','title':'记录ID'},{'field':key,'title':'名称/原编号'},
        *[{'field':f,'title':t} for f,t in extra]]}


def extend(resources):
    if 'SourceDyeCustomerTS' in resources:
        for child in resources['SourceDyeCustomerTS']['workflow']['children']:
            if child['entity']=='erp_sales_sourcedyecustomertsdetail':child['title']='客户投诉明细'
    for parent,child,module in [('SourceDyeDyeRecipe','SourceDyeDyeRecipeDetail','erp_sampling'),('SourceDyeStuffWeight','SourceDyeStuffWeightDetail','erp_production')]:
        if parent in resources:
            resources[parent]['workflow']['children'].append({'entity':module+'_'+child.lower(),'title':'全部材料明细（含所有染程）',
                'key':'old_sheet_series','parent_field':'old_sheet_series','atomic':False})
    for parent,child,title in [('SourceDyeCarryMaterial','SourceDyeCarryMaterialDetail','提料单明细'),('SourceDyeTightTube','SourceDyeTightTubeDetail','紧筒业务明细')]:
        if parent not in resources:continue
        module='erp_warehouse' if 'Carry' in parent else 'erp_production'
        resources[parent]['workflow']['children'].append({'entity':module+'_'+child.lower(),'title':title,'key':'source_parent_1','atomic':True})
        resources[child]['crud_fields'].append('source_parent_1')
    event=[field('at','办理时间','datetime',required=True),field('reason','办理说明',required=True)]
    if 'SourceDyeDyeRecipe' in resources:
        resources['SourceDyeDyeRecipe']['workflow']['actions'].append({'key':'adopt_recipe_references','title':'选择来样及配方来源','states':[None, 'unreviewed'],'inputs':[
            field('color','采用来样颜色记录','select',remote=remote('DyeLabColor','ColorNo')),
            field('original','采用原配方记录','select',remote=remote('DyeRecipe','SheetNo')),
            field('standard','采用标准配方记录','select',remote=remote('DyeRecipe','SheetNo')),*event]})
    if 'SourceDyeProdLoading' in resources:
        resources['SourceDyeProdLoading']['viewset']='plugins.erp_base.source_api.SourceLoadingViewSet'
        resources['SourceDyeProdLoading']['workflow']['actions'].append({'key':'add_outgoing_lines','title':'选择成品出库明细装车','states':[None, 'unreviewed'],'inputs':[
            field('lines','采用的成品出库原行','multi',required=True,remote=remote('ProdOutDetail','DetailNo')),*event]})
    if 'SourceDyeJobInWareEdit' in resources:
        resources['SourceDyeJobInWareEdit']['viewset']='plugins.erp_base.source_api.SourceJobWarehouseViewSet'
        resources['SourceDyeJobInWareEdit']['workflow']['actions'].append({'key':'register_outgoing','title':'根据进仓记录登记出仓','states':[None, 'unreviewed', 'approved'],'inputs':[
            field('rolls','本次登记粒数','decimal'),field('weight','本次登记重量','decimal'),*event]})
    if 'SourceDyeWDefect' in resources:
        resources['SourceDyeWDefect']['viewset']='plugins.erp_base.source_api.SourceReviewViewSet'
        resources['SourceDyeWDefect']['workflow']['actions'].append({'key':'open_rework_card','title':'按评审开回修工卡','states':[None, 'unreviewed', 'approved'],'inputs':[
            field('job','明确来源工卡','select',required=True,remote=remote('JobSheet','SheetNo')),
            field('quantity','回修计划数量','decimal'),field('rolls','回修计划粒数','decimal'),field('unit','分配单位编码','number'),
            field('sheet_kind','回修单据类型编码','number',required=True),field('job_kind','回修业务类型编码'),
            field('processes','采用来源卡的计划工序','multi',remote=remote('JobProcess','ProcessID')),*event]})
    if 'SourceDyeOrderColor' in resources:
        route=field('route','采用工艺路线','select',remote=remote('p_FieldValid','Name'))
        route['remote']['params']={'old_field_type':'Production'}
        resources['SourceDyeOrderColor']['workflow']['actions'].append({'key':'open_first_card','title':'订单首次开卡','states':[None, 'unreviewed'],'inputs':[
            field('head','所属染整订单','select',required=True,remote=remote('OrderMain','SheetNo'),source_field='source_parent_1'),
            field('number_prefix','工卡编号前缀（如J01，可留空）'),
            field('quantity','本订单行分配数量','decimal',source_field='old_order_qty'),field('rolls','本次计划总粒数','decimal',source_field='old_order_rolls'),
            field('unit','分配单位编码','number'),field('yarn','供纱方式','select',required=True,options=[{'value':'本厂采购','label':'包工包料（本厂采购）'},{'value':'客户来纱','label':'来料加工（客户来纱）'}]),route,
            field('members','共同开卡的其他订单行','editable_rows',default=[],columns=[field('line_id','订单颜色行记录ID','number',required=True),field('quantity','本行分配数量','decimal')]),
            field('assignments','明确实料来源的预配计划','editable_rows',default=[],columns=[field(k,t) for k,t in [('ReceSheetNo','原收料明细号'),('GrayID','坯料编码'),('LotNo','批号'),('WareHouseID','仓库'),('StorageUnitID','库位')]]+
                [field(k,t,'decimal') for k,t in [('Rolls','计划粒数'),('WeightQty','计划重量'),('LengthQty','计划长度')]]),*event]})
    if 'SourceDyeJobSheet' in resources:
        route=field('route','明确采用工艺路线','select',required=True,remote=remote('p_FieldValid','Name'))
        route['remote']['params']={'old_field_type':'Production'}
        resources['SourceDyeJobSheet']['workflow']['actions'].append({'key':'adopt_route','title':'采用路线生成计划工序','states':['unreviewed', None],'inputs':[route,*event]})
