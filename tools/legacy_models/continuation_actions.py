"""来源单据接续动作元数据，与生成器一起生成页面和权限。"""
STATES=['draft','confirmed','approved',None]


def field(key,title,kind='text',required=False,**values):
    return {'key':key,'title':title,'kind':kind,'required':required,'options':[],**values}


def choice(key,title,options):
    return field(key,title,'select',True,options=[{'value':key,'label':label} for key,label in options])


def relation(key,title,entity,label,many=True):
    columns=[{'field':'id','title':'记录ID'},{'field':'legacy_id','title':'旧erpID'}, {'field':label,'title':title}]
    extras={'erp_warehouse_sourcedyeprodinrecord':[('old_sheet_series','入库流水'),('old_roll_no','卷号'),('old_weight_qty','重量'),('old_length_qty','长度')],
        'erp_production_sourcedyejobprocess':[('old_sheet_series','工卡流水'),('old_process_no','工序序号'),('old_status','原状态')],
        'erp_production_sourcedyejobsheet':[('old_sheet_series','工卡流水'),('old_pre_vat_qty','计划量'),('old_assign_unit','原单位')]}
    columns.extend({'field':field,'title':title} for field,title in extras.get(entity,[]))
    return field(key,title,'multi' if many else 'select',not many,
        remote={'entity':entity,'pk':'id','label':label,'columns':columns})


def event():
    return [field('at','实际办理时间','datetime',True,default_now=False),field('reason','办理依据/异常说明','textarea',True)]


def movement(unit=True,customer=False):
    result=[field(key,title,'decimal',nullable=True) for key,title in [('weight','本次实际重量'),('length','本次实际长度'),('rolls','本次实际粒数')]]
    result += [field('warehouse','实际仓库原编码'),field('sheet_kind','原单据类型编码','number',True)]
    if unit:result.append(field('unit','实际StockUnit整数编码','number',nullable=True))
    if customer:result.append(field('customer','实际客户原编码（空值仍保留）'))
    return result+event()


def action(key,title,inputs):
    return {'key':key,'title':title,'states':STATES,'inputs':inputs}


def factory_quality_action():
    return action('factory_quality','登记加工厂质量处置',[
            field('factory','加工厂原编码'),
            choice('result','本次质量处置',[('released','放行'),('concession','让步放行'),('hold','待处理'),('return','退厂'),('withdrawn','撤回处置')]),
            {**relation('inspection','采用的原质量评审（可空）','erp_quality_sourcedyewdefect','old_sheet_no',False),'required':False},*event()])


def extend(table,options):
    actions=options['workflow']['actions']
    if table in ['MachineCase','p_Machine']:
        if table=='MachineCase':options['viewset']='plugins.erp_base.source_api.SourceMachineCaseViewSet'
        actions.append(action('machine_case_projects','查看原机台方案项目',[]))
    if table in ['MachineCareRecords','InspectionLog']:
        options['viewset']='plugins.erp_base.source_api.SourceEquipmentProjectsViewSet'
        project=[field('case','原方案流水（不是机台号）',nullable=True),
            field('changed_ids','变更项目原DetailNo（用反引号分隔）','textarea',nullable=True),
            field('changed_values','对应实际值（用反引号分隔）','textarea',nullable=True),
            field('changed_results','对应Result整数（用反引号分隔）','textarea',nullable=True)]
        common=[field(k,t,nullable=True) for k,t in [('employee','办理员工原编码'),('machine','机台原编码'),('machine_name','设备名称'),('location','位置'),('people','巡检/保养人员原编码列表')]]
        common += [field('performed_at','实际巡检/保养时间（原修改过程不回写本列）','datetime',nullable=True),field('remarks','原备注','textarea',nullable=True)]
        if table=='InspectionLog':common += [field('sheet_date','单据日期','datetime',nullable=True),field('survey','巡检概况','textarea',nullable=True)]
        else:common += [field('idea','相关意见','textarea',nullable=True),field('result','保养结果原编码',nullable=True)]
        actions.extend([action('equipment_projects','查询原记录项目或方案带出',[]),
            {**action('preview_equipment_projects','预览方案项目与变更值',project),'detail':False},
            {**action('create_equipment_document','按原APP过程新增记录及项目',project+common+event()),'detail':False},
            action('save_equipment_document','按原APP过程修改记录并替换项目',project+common+event()),
            action('undo_equipment','撤回本次设备办理',event()),action('continuation','查看设备办理事实',[])])
    if table=='MachineFault':
        options['viewset']='plugins.erp_base.source_api.SourceMachineFaultViewSet'
        fields=[field(k,t,nullable=True) for k,t in [('employee','报修员工原编码'),('machine','机台原编码'),('machine_name','设备名称'),('location','设备位置'),('shift','班组原编码'),
            ('fault','故障描述（原APP的FaultID参数）'),('business_unit','经营单位原编码'),('fault_class','故障分类'),('group','维修分组'),('machine_class','设备分类'),('sheet_kind','原单据类型'),('uploads','已上传文件Guid（分号分隔）')]]
        fields += [field('urgent','是否紧急原整数','number',nullable=True),field('remarks','备注','textarea')]
        flow=choice('action','原办理动作',[(n,n) for n in ['受理','指派','签到','取消签到','提交','退回','确认','拒绝','评价','评论','关闭','恢复','重新提交']])
        actions.extend([{**action('create_fault','按原APP过程新增报修',fields+event()),'detail':False},
            action('save_fault','按原APP过程修改报修及附件绑定',fields+event()),action('fault_save_check','核对原APP保存检查',[]),
            action('fault_actions','查询原员工可操作列表',[field('employee','登录员工原编码',nullable=True),choice('version','原权限列表版本',[(2,'含签到新版'),(1,'普通版')])]),
            action('check_fault_action','核对原动作检查',[flow,field('fixers','指定维修工原编码列表',nullable=True)]),
            action('perform_fault_action','办理维修流转或签到',[flow,field('employee','操作员工原编码',nullable=True),field('fixers','维修工原编码列表（分号分隔）',nullable=True),
                field('remarks','流转备注','textarea'),field('score','评价分数（原无0～5限制）','number',nullable=True),*event()]),
            action('fault_history','查看逐条维修流转和评论',[]),action('undo_equipment','撤回本次设备办理',event()),action('continuation','查看设备办理事实',[])])
    if table=='JobSheet':
        values=[choice('entry','现场记录类型',[('DPWProcess','染色刷卡'),('AddWProcessEdit','刷卡产量补录'),('WProcessEdit','普通产量登记'),('AddDyeWProcessStep','独立染色产量补录')]),
            field('process_no','原工序序号','number',True,nullable=True)]
        values += [field(k,t,nullable=True) for k,t in [('process','工序原编码'),('employee','实际员工原编码'),('machine','实际机台原编码'),('shift','班组原编码'),('class_id','班别原编码'),('station','工位原编码'),('dye_state','染色状态原值'),('program','独立补录计件项目'),('dye_process','独立补录染程工步')]]
        values += [field(k,t,'decimal',nullable=True) for k,t in [('rolls','实际粒数'),('weight','实际重量'),('length','实际长度'),('real_value','独立补录比例')]]
        values += [field('start','开始/独立补录时间','datetime',nullable=True),field('end','结束时间（普通刷卡补录不填则沿用开始）','datetime',nullable=True),field('remarks','原备注','textarea',nullable=True)]
        actions.extend([action('site_records','查询本卡现场报工和独立补录',[]),action('create_site_record','录入现场报工或补录',values)])
    if table in ['p_ShiftArrange','p_ShiftArrangeDetail','p_Machine']:
        options['viewset']='plugins.erp_base.source_api.SourceShiftCalendarViewSet'
        inputs=[field('curr_time','查询班次的时间','datetime',True,nullable=True),field('machine','原机台编码',required=True,nullable=True)]
        actions.append({**action('lookup_shift','按原日历查询机台班组（只读）',inputs),'detail':False})
        if table in ['p_ShiftArrange','p_Machine']:
            actions.extend([action('resolve_shift','按原逻辑补日历并查询机台班组',inputs+event()),
                action('undo_calendar','撤回本条发起的日历生成',event()),action('continuation','查看本条日历办理事实',[])])
        if table=='p_ShiftArrange':
            days=[field('create_days','原生成天数（零/负数仍按换版范围处理）','number',True,nullable=True)]
            actions.extend([{**action('preview_calendar','预览班次循环与替换范围',days),'detail':False},
                action('generate_calendar','生成循环日历并留存被替换行',days+event())])
    if table=='JobSheet':
        actions.extend([action('entered_machine','查询原进缸机台及全部候选',[]),
            action('process_machines','按原工序与人员查询可选机台',[
                field('shift','原班组编码',required=True,nullable=True),field('employee','原员工编码',required=True,nullable=True),
                field('process','原工序编码',required=True,nullable=True),field('as_of','原GETDATE核对时刻','datetime',True)])])
        actions.extend([{**action('scan_dye_job','染色主副卡扫码选卡',[
            field('barcode','原主/副工卡号',required=True,nullable=True)]),'detail':False},
            action('formal_dye_steps','查询正式染程剩余步骤',[
                field('process','原工序编码',required=True,nullable=True),field('process_no','原工序序号','number',True,nullable=True),
                field('employee','原EmpID参数（实际比较班组ShiftID）',required=True,nullable=True)])])
    if table=='StuffWeight':
        options['viewset']='plugins.erp_base.source_api.SourceWeightViewSet'
        actions.append(action('material_steps','备料步骤与立信准备数据',[
            choice('mode','原查询口径',[('standard','普通备料次序'),('lx','立信准备次序'),('to_lx','立信料单/缸号/槽号投影')])]))
    if table=='ShiftArrange':
        options['viewset']='plugins.erp_base.source_api.SourceShiftArrangeViewSet'
        actions.extend([action('preview_shift_work','预览排班调整报工人员',[]),
            action('apply_shift_work','按排班调整报工人员',event()),action('undo_shift_work','撤回本次报工人员调整',event())])
    if table=='WProcess':
        actions.append(action('site_work_details','按现场入口查询人员与步骤',[
            choice('entry','原现场入口',[(key,title) for key,title in [('DPWProcess','染色刷卡'),('DPWProcessEdit','刷卡产量查询登记'),('AddWProcessEdit','刷卡补录'),('WProcessEdit','普通产量登记')]])]))
        actions.append(action('employee_proportion','核对班组人员原比例',[
            field('employee','原员工编码',required=True,nullable=True)]))
    if table=='QuoteDetail':
        actions.append(action('quote_trigger_check','核对原新增/修改/删除触发规则',[
            choice('operation','核对的原操作',[('insert','新增后检查'),('update','修改后检查'),('delete','删除检查')]),
            field('right_status_in_statement','修改语句包含RightStatus列（即使值不变）','boolean',default=False)]))
    if table in ['DyeDipsRecord','DyeReprint']:
        if table=='DyeReprint':options['viewset']='plugins.erp_base.source_api.SourceSampleReportsViewSet'
        actions.extend([{**action('sample_work_report','打样计件、工作日及日报',[
            choice('mode','原统计口径',[('summary','主工号计件汇总'),('details','主工号原产量明细'),('daily','7:30工作日报'),('days','原工作日数'),('emp1','EmpID1/SheetKind原计件变体')]),
            field('start','开始时间（包含；空为全历史）','datetime',nullable=True),field('end','结束时间（不含；空为全历史）','datetime',nullable=True),
            field('employee','原工号（空值NULL为全部）',nullable=True)]),'detail':False},
            {**action('sample_checker_report','打样人员/对色员返打统计',[
                field('start','开始时间（包含）','datetime',True),field('end','结束时间（包含）','datetime',True)]),'detail':False}])
    if table in ['Quote','QuoteDetail']:
        options['viewset']='plugins.erp_base.source_api.SourceQuoteFunctionsViewSet'
        names=['fn_GetColorNumPrice','fn_GetPriceListVat','fn_GetPriceUnit','fn_ColorNum_BasicsPrice',
            'fn_GetPackPrice','fn_GetPackQtyPrice','fn_GetDyePrice','fn_GetPriceRemark','fn_GetJObSheetNoAttePrice','fn_GetJObSheetNoAttePriceUnit','fn_NewGetDyePrice','fn_GetTechPrice']
        actions.append({**action('quote_function','核对原报价函数及候选来源',[
            choice('function','原取价函数',[(name,name) for name in names]),
            *[field(key,title,nullable=True) for key,title in [('color','原色号'),('customer','客户原编码'),('charging','收费口径01坯布/02成品'),
                ('process','工序原编码'),('phase','染程原编码'),('grade','等级原编码'),('service','另收费项目原编码'),('job','原工卡号'),('detail','原出库明细号')]],
            field('kind','套价分量Kind（0总价，1～6分量，7基础，8其他）','number',nullable=True),
            *[field(key,title,'decimal',nullable=True) for key,title in [('weight','成品重量'),('gray_quantity','坯布重量'),('cost','配方成本'),('dosage','染料用量')]],
            field('sheet_date','实际出库日期','datetime',nullable=True),field('order_date','原订单日期','datetime',nullable=True)]),'detail':False})
    if table=='QuoteDetail':options['viewset']='plugins.erp_base.source_api.SourceQuoteDetailViewSet'
    if table=='DyeDipsRecord':
        variants=['Sp_DyeDipsRecord','Sp_DyeDipsRecord1','Sp_DyeDipsRecord2','Sp_DyeDipsRecord10','Sp_DyeDipsRecord22','Sp_DyeDipsRecord_EmpID']
        inputs=[choice('variant','采用的原过程',[(name,name) for name in variants]),
            {**choice('scope','办理范围',[('selected','明确所选流水'),('original','原过程范围（全库变体将处理全库）')]),'default':'selected'}]
        actions.extend([action('preview_sample_variant','预览打样变体回写',inputs),
            action('apply_sample_variant','采用原打样变体规则',inputs+event()),action('undo_sample_variant','撤回本次打样规则办理',event())])
    if table=='DyeLabColor':
        options['viewset']='plugins.erp_base.source_api.SourceLabColorViewSet'
        actions.extend([action('sample_schedule_options','核对客样打样排单来源',[]),action('schedule_sample','客样颜色生成普通或复版打样',[
            choice('entry','原打样入口',[('DyeDipsRecord','普通打样'),('DyeDipsRecordBulk','复版打样')]),
            field('version','本次打样版本',required=True,nullable=True),field('employee','安排人员原编码',nullable=True),
            field('shift','安排班组原编码',nullable=True),*event()])])
    if table=='ProdTest':
        options['viewset']='plugins.erp_base.source_api.SourceTrialViewSet'
        actions.extend([action('preview_trial_work','核对试验物料及加色报工来源',[]),
            action('apply_trial_work','采用试验登记生成加色报工',event()),action('undo_trial_work','撤回本次试验报工',event())])
    if table in ['GrayOutDetail','SemiOutDetail']:
        actions.append(action('material_receipt_options','查看外协21/25/26类原收回余额',[]))
        actions.append(action('receive_outwork_material','按实际量办理外协回料',[
            choice('destination','实际收回仓类',[('gray','坯料21类'),('semi','半成品25类')] if table=='GrayOutDetail' else [('semi','半成品26类')]),
            *[item for item in movement(customer=True) if item['key']!='sheet_kind'],
            field('packs','实际件数Packs','decimal',nullable=True),field('supplier','实际供应商原编码'),
            field('receipt_number','新收料号（原号非数字时明确填写）')]))
        actions.append(action('return_material','外协原料退回入库',movement(customer=True)))
        actions.append(action('transfer_to_job','原卡实际退料并转领至另一工卡',[
            relation('source_job','本次退料所属原卡','erp_production_sourcedyejobsheet','old_sheet_no',False),
            relation('target','实际领用目标工卡','erp_production_sourcedyejobsheet','old_sheet_no',False),
            *[item for item in movement(customer=True) if item['key']!='sheet_kind'],
            field('return_kind','退回入库原类型编码','number',True),field('issue_kind','目标领用原类型编码','number',True),
            field('issue_number','新领用明细号（不填按原规则递增；原号非数字时明确填写）')]))
    elif table in ['GrayInDetail','SemiInDetail']:
        options['viewset']='plugins.erp_base.source_api.SourceReceiptMaterialViewSet'
        actions.append(factory_quality_action())
        actions.append(action('return_outwork_material','实际退回加工厂（独立出库）',[
            *movement(customer=True),field('packs','实际件数Packs','decimal',nullable=True),field('factory','实际加工厂原编码'),
            field('issue_number','新出库明细号（原号非数字时明确填写）')]))
        actions.append(action('issue_to_job','按实际量领用至工卡',[
            relation('target','实际领用工卡','erp_production_sourcedyejobsheet','old_sheet_no',False),
            field('issue_number','新领用明细号（不填按原规则递增；原号非数字时明确填写）'),*movement()]))
        actions.append(action('return_raw_purchase','采用本条收货办理16类采购退货',[
            *[item for item in movement() if item['key']!='sheet_kind'],field('supplier','实际供应商原编码'),
            field('receipt_number','新退货收料号（不填按原规则递增；原号非数字时明确填写）')]))
    elif table=='PurDetail':
        actions.append(action('purchase_movements','查看坯料半成品采购全部收退',[]))
        for item in actions:
            if item['key']=='receive':item['inputs'] += [field('length','实际长度','decimal',nullable=True),
                field('supplier','指定供应商原编码（不填采用唯一原采购表头）'),field('receipt_number','新收料号（原号非数字时明确填写）')]
    elif table in ['StuffInDetail','ArticleInDetail']:
        options['viewset']='plugins.erp_base.source_api.SourcePurchaseReceiptLineViewSet'
        actions.append(action('return_purchase','采用本条收货办理16类采购退货',[
            field('quantity','本次原退货数量（保留正负）','decimal',nullable=True),field('warehouse','实际仓库原编码'),
            field('supplier','实际供应商原编码'),*event()]))
    elif table in ['OutWorkApply','SemiOutWorkApply']:
        actions.append(action('trace_outwork','查看外协发回退及质量来源链',[]))
        actions.append(action('review_followup','核对结案后收退及结案变化',[]))
        for item in actions:
            if item['key']=='close_outwork':
                item['inputs'] += [relation('received_gray','本次累计加工回坯入库明细','erp_warehouse_sourcedyegrayindetail','old_rece_sheet_no'),
                    relation('received_semi','本次累计加工回半成品入库明细','erp_warehouse_sourcedyesemiindetail','old_rece_sheet_no'),
                    relation('returned_material','本次累计原料退回入库明细（独立列示原量）',
                    'erp_warehouse_sourcedye'+('grayindetail' if table=='OutWorkApply' else 'semiindetail'),'old_rece_sheet_no'),
                    relation('returned_product','本次累计退厂成品出库明细','erp_warehouse_sourcedyeprodoutdetail','old_detail_no')]
    elif table=='WDefect':
        actions.extend([{**action('rework_daily','日/月布种车间返修统计',[
            field('as_of','统计日期','date',True)]),'detail':False},
            {**action('rework_extended','综合返修、同比及责任数量统计',[
                choice('report','原报告',[(name,name) for name in ['Sp_ReworkCloth4','Rework_Comparison1','Rework_Comparison2','Rework_Comparison3']]),
                field('start','起始时间（含）','datetime',True,default_now=False),field('end','结束时间（含）','datetime',True,default_now=False),
                {**choice('mode','同比来源口径',[('legacy','原过程：上年仍关联本期返修来源'),('same_period','明确修正：各自同期来源')]),'default':'legacy'},
                {**choice('quantity_source','数量来源',[('automatic','自动采用已映射原数量'),('manual','手动指定独立数量')]),'default':'automatic'},
                field('quantity_batch','数量批次（空为最新可读批次）','select',remote={'entity':'erp_quality_qualityquantitybatch','pk':'id','label':'captured_at'}),
                field('far_rows','手动来源明细（仅手动模式使用）','rework_sources'),
                field('far_reference','数量来源、抽取范围及长度依据','textarea')]),'detail':False}])
        actions.append({**action('rework_statistics','原05/06站点月度返修统计',[
            choice('station','原统计站点',[('05','05 / Sp_ReworkCloth2'),('06','06 / Sp_ReworkCloth3')]),
            field('start','起始时间（含）','datetime',True,default_now=False),
            field('end','结束时间（含）','datetime',True,default_now=False)]),'detail':False})
    elif table=='RecordYield':
        options['viewset']='plugins.erp_base.source_api.SourcePackageViewSet'
        actions.append({**action('package_people','最新包装人员及多人产量分摊',[
            choice('report','查询内容',[('latest','原最新包装人员'),('shared','多人分摊产量')]),
            field('number','工卡号（不填为全部）',nullable=True),
            {**choice('mode','分摊连接口径',[('legacy_barcode','原视图按包装BarCode'),('entry_guid','按原录入主从Guid对应')]),'default':'legacy_barcode'}]),'detail':False})
        inputs=[]
        for key,title,kind in [('old_kg','重量Kg','decimal'),('old_main_no','MainNo','text'),('old_detail_no','DetailNo','text'),
            ('old_color_num','客户色号','text'),('old_customer_id','客户原编码','text'),
            ('old_sum_assigned_weight_qty','原实配重量','decimal'),('old_sum_assigned_rolls','原实配粒数','decimal'),
            ('old_scroll','卷序号Scroll','text'),('old_pack_bag','包装重PackBag','decimal'),('old_add_weigth','附加重量原文AddWeigth','text'),
            ('old_customer_gray_name','客户坯料品名','text'),('old_color_id','颜色原编码','text'),('old_spec','规格','text'),
            ('old_width_spec','幅宽规格','text'),('old_weight_spec','克重规格','text'),('old_prod_id','品名原编码','text'),
            ('old_qty','数量Qty','decimal'),('old_count_unit','计数单位原文','text')]:
            inputs.append(field(key,title,kind,nullable=True,source_field=key))
        actions.extend([action('preview_package_replace','预览同卡同卷包装替换',[]),
            action('replace_package','同卡同卷替换新增包装',inputs+event()),
            action('undo_package_replace','撤回本次包装替换',event()),
            action('undo_gray_record','撤回明确投坯采用',event())])
        actions.append(action('receive_package','采用本条包装生成实际入库',movement()))
        actions.append(action('adopt_gray_record','明确采用原投坯细码',[
            relation('source','采用的投坯原记录','erp_production_sourcedyejobgrayrecord','old_gray_bar_code',False),*event()]))
    elif table=='ProdIn':
        options['viewset']='plugins.erp_base.source_api.SourceProductReceiptViewSet'
        actions.append(factory_quality_action())
        actions.append(action('dispatch_product','实际交付或退厂出库',[
            choice('purpose','本次业务',[('customer_delivery','客户交付'),('factory_return','退回加工厂')]),
            field('receiver','实际接收方原编码'),field('price','本次采用单价','decimal',nullable=True),
            relation('records','本次采用的入库细码（按记录选择）','erp_warehouse_sourcedyeprodinrecord','old_bar_code'),*movement(unit=False)]))
    elif table=='ProdOut':
        options['viewset']='plugins.erp_base.source_api.SourceProductDispatchViewSet'
        actions.append(action('confirm_delivery','交付签收/拒收/撤回登记',[
            choice('result','交付结果',[('delivered','签收'),('refused','拒收'),('withdrawn','撤回签收')]),field('receiver','实际签收方'),*event()]))
    elif table=='ProdOutDetail':
        options['viewset']='plugins.erp_base.source_api.SourceProductDispatchDetailViewSet'
        actions.append(action('receive_return','实际交付退货入库',movement(customer=True)))
    elif table=='JobSheet':
        actions.append(action('trial_steps','核对原DPJobStep_Test剩余染程步骤',[
            field('process','原工序编码',required=True,nullable=True),field('process_no','原工序序号','number',True,nullable=True),
            field('employee','原EmpID参数（实际用于比较班组ShiftID）',required=True,nullable=True)]))
        label_series=[field('series','目标原流水（未指定用当前工卡；可填写缺失表头的原流水）',nullable=True)]
        actions.extend([action('preview_package_labels','预览自动包装标签同步',label_series),
            action('synchronize_package_labels','同步已包装资料与二维码',label_series+event()),
            action('undo_package_labels','撤回本次包装标签同步',event())])
        actions.extend([action('preview_package_pairing','预览包装与投坯排序配对',[]),
            action('apply_package_pairing','按原排序采用投坯细码',event()),
            action('undo_package_pairing','撤回本次包装排序配对',event())])
        actions.append(action('link_execution_source','明确关联缺失对应的执行原记录',[
            choice('source_table','原业务表',[(name,name) for name in ['WProcess','StuffWeight','RecordYield','ProdIn','GrayOutDetail','SemiOutDetail',
                'StuffOut','ProdOutDetail','JobGrayRecord','ColoringCheck','DyeCheckout','CarryMaterialDetail','StuffIn','GrayOut','GrayIn','SemiOut','SemiIn','ProdOut',
                'StuffStockBook','GrayStockBook','SemiStockBook','ProdStockBook','ProdInRecord','ProdOutRecord','GrayOutRecord','SemiOutRecord',
                'StuffWeightPhase','StuffWeightDetail','WProcessStep','JobShiftEmp','ColorShiftEmp']]),
            field('record_id','本项目原记录ID（请按列表ID选择）','number',True),*event()]))
        actions.extend([action('preview_execution_reverse','预览报工称料包装收发整链撤销',[]),
            action('reverse_execution_chain','撤销工卡执行整链',[
                choice('mode','撤销范围',[('execution_only','撤销执行，原计划保留'),('execution_and_plan','撤销执行及本次拆合计划')]),
                choice('work_mode','刷卡回写范围',[('trigger_then_maintenance','原删除触发及独立进度维护'),('trigger_only','仅原删除触发回写')]),*event()]),
            action('undo_execution_reverse','撤回本次执行整链撤销',event())])
        actions.extend([{**action('preview_progress','预览全库空工序进度维护',[]),'detail':False},
            {**action('maintain_progress','执行全库空工序进度维护',event()),'detail':False}])
        actions.append(action('reverse_card','撤回本次拆合计划',[
            choice('mode','撤回范围',[('unstarted','撤回未执行计划'),('plan_only','仅撤回计划，保留已执行单据与未转移分配')]),*event()]))
        inputs=[field('quantity','新卡计划数量','decimal',nullable=True),field('rolls','新卡计划粒数','decimal',nullable=True),
            field('unit','明确采用AssignUnit整数编码','number',nullable=True),
            relation('processes','采用的原工序计划（可多选，含参数理论值）','erp_production_sourcedyejobprocess','old_process_id'),*event()]
        actions.extend([action('split_card','按明确计划量拆卡',inputs),action('merge_cards','建立新合卡及原卡关系',[
            relation('members','另选参与合卡的工卡（当前卡自动包含）','erp_production_sourcedyejobsheet','old_sheet_no'),*inputs]),
            action('combine_members','查看逐条原合卡关系',[])])
        actions.append(action('reprocess','采用本卡及质量评审建立再加工计划',[
            {**relation('review','采用的质量评审（可空）','erp_quality_sourcedyewdefect','old_sheet_no',False),'required':False},
            field('sheet_kind','再加工原单据类型编码','number',True),field('job_kind','再加工原工卡类型编码'),*inputs]))
    elif table=='JobCombineOrder':
        actions.append(action('reverse_allocation','撤回本次分配转移',event()))
        options['viewset']='plugins.erp_base.source_api.SourceJobAllocationViewSet'
        actions.append(action('transfer_allocation','转移明确的订单分配量',[
            relation('target','采用的目标工卡','erp_production_sourcedyejobsheet','old_sheet_no',False),
            field('quantity','本次转移CombineQty','decimal',nullable=True),*event()]))
    elif table=='JobProcess':
        completion=field('completion_status','本次传入完成状态（原Status；1触发质量重建）','number',nullable=True)
        actions.extend([action('preview_dye_quality','预览原染色产量与质量重建',[{**completion,'required':True}]),
            action('rebuild_dye_quality','执行原染色质量重建',[{**completion,'required':True},*event()])])
        route=[field('plan_have_time','按原工序延迟小时筛选排程','boolean',True,default=False),field('as_of','排程选路基准时间','datetime',True,default_now=False)]
        actions.extend([action('preview_auto_combine','预览原自动合卡选路',route),
            action('automatic_combine','按原称料/排程自动同步合卡',[*route,
                completion,
                choice('time_way','原时间回写方式',[(0,'开始和结束'),(1,'仅开始'),(2,'仅结束')]),
                field('machine','本次实际机台原编码'),*event()])])
        options['viewset']='plugins.erp_base.source_api.SourceJobProcessViewSet'
        actions.append(action('sync_combined_process','向明确的合卡工序同步进度',[
            relation('targets','本次同步的目标原工序','erp_production_sourcedyejobprocess','old_process_id'),
            choice('time_way','原时间回写方式',[(0,'开始和结束'),(1,'仅开始'),(2,'仅结束')]),
            field('machine','本次实际机台原编码'),*event()]))
    elif table=='JobCombine':
        actions.append(action('reverse_link','撤回本次原合卡关系采用',event()))
        options['viewset']='plugins.erp_base.source_api.SourceJobLinkViewSet'
        actions.extend([action('combine_group','查看同原流水全部合卡关系',[]),
            action('adopt_combine_link','将本条原关系采用到明确工卡',[
                relation('target','采用的目标工卡','erp_production_sourcedyejobsheet','old_sheet_no',False),*event()])])
    elif table in ['GrayInRecord','JobGrayRecord']:
        options['viewset']='plugins.erp_base.source_api.SourceGrayRecordViewSet'
        entity='erp_warehouse_sourcedyegrayinrecord' if table=='GrayInRecord' else 'erp_production_sourcedyejobgrayrecord'
        job={**relation('job','同步的工卡（出库前可选）','erp_production_sourcedyejobsheet','old_sheet_no',False),'required':False}
        actions.extend([action('split_gray','拆分本条坯料细码',[
            *[field(key,title,'decimal',nullable=True) for key,title in [('weight','拆出重量'),('length','拆出长度'),('rolls','拆出粒数')]],job,*event()]),
            action('merge_gray','合并选定坯料细码并保留参与行',[
                relation('members','另选参与细码（当前行自动包含）',entity,'old_roll_no'),job,*event()])])
    elif table=='GrayRecordCutLogs':
        options['viewset']='plugins.erp_base.source_api.SourceGrayOperationViewSet'
        actions.extend([action('operation_report','查看拆合结果或原日志',[]),action('undo_gray','撤回本次细码拆合',event())])
        measure=choice('measure','无标签旧数量的含义',[('unknown','尚未确定，仅保留原数量'),('WeightQty','重量'),('LengthQty','长度'),('Rolls','粒数')])
        actions.extend([action('history_recovery_preview','核对历史拆合恢复依据',[measure]),
            action('recover_history','恢复历史细码资料或办理逆向',[
                choice('stage','本次恢复阶段',[('before','出库前收料细码'),('after','出库后工卡投坯细码')]),
                choice('mode','办理范围',[('archive','恢复已知字段留档，不计入当前库存'),('reverse','按日志与选定当前结果办理逆向')]),measure,
                {**relation('job','恢复所属工卡（出库后必选）','erp_production_sourcedyejobsheet','old_sheet_no',False),'required':False},
                relation('receipt_records','出库前当前结果（逆向时完整选择）','erp_warehouse_sourcedyegrayinrecord','old_roll_no'),
                relation('job_records','出库后当前结果（逆向时完整选择）','erp_production_sourcedyejobgrayrecord','old_roll_no'),*event()]),
            action('undo_history_recovery','撤回本次历史恢复',event())])
    if table in ['JobSheet','JobCombineOrder','JobProcess','JobCombine','GrayIn','SemiIn','ProdIn','ProdOut','StuffIn','ArticleIn','RecordYield','GrayInRecord','JobGrayRecord','GrayRecordCutLogs']:
        actions.append(action('continuation','查看本单接续办理事实',[]))
    if table in ['PurApplyDetail','PurDetail','ArticlePurDetail','StuffPurDetail']:
        if table!='PurDetail':options['viewset']='plugins.erp_base.source_api.SourceMaterialPurchaseViewSet'
        entries={'ArticlePurDetail':['ArticleIn','FabricArticleIn'],'StuffPurDetail':['StuffIn','SmallStuffIn']}
        choices=entries[table] if table in entries else ['StuffIn','SmallStuffIn','ArticleIn','FabricArticleIn']
        actions.extend([action('material_receipts','查看逐条采购收货与退货',[]),
            action('receive_material','采用采购明细办理实际收货',[
                choice('entry','原收货入口',[(name,name) for name in choices]),
                field('quantity','本次实际Qty/InQty','decimal',nullable=True),field('warehouse','实际仓库原编码'),
                field('supplier','实际供应商原编码'),field('sheet_kind','原入库类型编码','number',True),*event()])])

    period=[field('start','开始时间（含）','datetime',True,default_now=False),field('end','结束时间（含）','datetime',True,default_now=False)]
    if table=='dyeCheckout':
        actions.extend([{**action('dye_rate','班组与对色员直通率',[
            choice('by','原统计口径',[('shift','班组 / Sp_DyeRateNew'),('matching','对色员 / Sp_DyeRateNew_ColorMatching')]),*period]),'detail':False},
            {**action('station_dashboard','对色员质量与色级产量看板',[
                choice('report','原报表',[('matching','对色员质量与加色次数'),('depth','色级出缸产量')]),
                field('as_of','核对时刻（原8点换日）','datetime',True),
                {**choice('mode','色级上月连接口径',[('legacy','原栏目连接'),('matched_month','明确修正上月栏目连接')]),'default':'legacy'}]),'detail':False}])
    if table=='WProcess':
        actions.extend([{**action('preview_work_archive','预览半年工位归档范围',[
            field('as_of','归档核对时刻','datetime',True)]),'detail':False},
            action('archive_work','办理半年工位归档',event()),action('undo_work_archive','撤回本次工位归档',event())])
        actions.extend([{**action('work_quantity','普通工位报工产量与原未匹配来源',period),'detail':False},
            {**action('process_status','核对原工位顺序与间隔',[
                field('number','工卡原编码','text',True),field('process','原工序编码','text',True),field('state','原染色状态','text',True,nullable=True),
                field('as_of','核对时刻','datetime',True)]),'detail':False}])
    if table=='RecordYield':
        actions.append({**action('package_yield','员工或络筒包装产量',[
            choice('by','分组口径',[('employee','员工、品名、色号'),('winding','络筒、品名、色号')]),
            *[dict(item,required=False) for item in period],field('employee','筛选员工原编码'),field('winding','筛选络筒原编码'),
            field('product','筛选品名原编码'),field('color','筛选色号原文')]),'detail':False})
    if table=='ProcessSchedule':
        options['viewset']='plugins.erp_base.source_api.SourceScheduleViewSet'
        actions.append({**action('existing_schedules','核对工卡已有排程',[
            field('numbers','工卡原编码（英文逗号分隔）','textarea',True)]),'detail':False})

    if table=='WDefect':
        for item in actions:
            if item['key']=='quality_statistics':
                item['inputs'] += [{**choice('quantity_source','旬报分母来源',[('automatic','自动采用质量数量批次'),('manual','明确手动分母')]),'default':'automatic'},
                    {**relation('quantity_batch','指定数量批次（不填采用最新可读批次）','erp_quality_qualityquantitybatch','captured_at',False),'required':False}]
