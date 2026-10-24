"""客户运行资源；保留本地业务模型，开发档案不注册为产品接口。"""

# 这些s_表承载实际业务枚举、审批事实、变更和通知，不是窗体设计器。
BUSINESS_CONFIG_TABLES = {
    's_CorpTitle', 's_DBComboValue', 's_Flow', 's_FlowRecord', 's_FlowStep',
    's_FlowStepEmp', 's_FlowTask', 's_Revision', 's_RevisionDetail',
    's_SaveMessRule', 's_SaveMessRuleDetail',
}
SUPPORT_MODELS = {
    'BusinessAction', 'LegacyImportBatch', 'LegacyImportIssue', 'NumberingRule',
    'SourceBusinessParameter', 'QualityQuantityBatch', 'QualityQuantitySource',
}
DEVELOPMENT_ACTIONS = {
    'phase6_catalog', 'phase6_formula', 'phase6_template',
    'phase6_prepare_print', 'phase6_finish_print', 'phase6_print_history',
    'original_config',
    'foundation_lookup', 'original_combo', 'original_view', 'original_app_report',
    'original_table_export', 'original_field_number', 'original_table_transform',
    'original_function', 'original_lookup', 'original_shared_function',
    'original_foundation_report', 'original_period',
    'phase4_function', 'phase5_function', 'quote_function', 'quote_trigger_check',
    'app_order_check', 'fault_save_check', 'check_fault_action',
    'convert_unit', 'calendar_days', 'continuous_dates',
    'correspondence', 'business_units',
}

BUSINESS_QUERIES = {
    'SourceDyeFixedPrice': ('手感报价查询', [('filter_text','客户或报价','text'),
        ('employee','业务员编码','text'),('start','开始时间','datetime'),('end','结束时间','datetime')]),
    'SourceDyeWProcess': ('实际产量查询', [('filter_text','工卡或客户','text'),
        ('date_mode','日期口径','number'),('start','开始时间','datetime'),('end','结束时间','datetime')]),
    'SourceDyePurMain': ('采购费用查询', [('start','开始时间','datetime'),('end','结束时间','datetime')]),
}
BUSINESS_TITLES = {'SourceDyePurMain':'采购订单','SourceDyeWDefect':'质量评审单',
                   'SourceDyeRecordYield':'包装细码与实称'}


def exposed_model(model):
    if not model._meta.app_label.startswith('erp_'):
        return True
    table = getattr(model, 'SOURCE_TABLE', None)
    if table is None:
        return model.__name__ in SUPPORT_MODELS
    if table.startswith('s_'):
        return table in BUSINESS_CONFIG_TABLES
    return table not in {'h_EmpDeptPerm', 'h_EmpRole', 'TBKEY', 'z_AccessLog', 'rp_Permission'}


def configure(options):
    for name, config in options.items():
        if name in BUSINESS_TITLES:
            config['title'] = BUSINESS_TITLES[name]
        workflow = config.get('workflow', {})
        if not workflow.get('source_model'):
            continue
        # 通用确认不是客户录单步骤；有明确原审核字段的单据保留审核及反审。
        reviewed = 'old_right_status' in config['crud_fields']
        excluded = DEVELOPMENT_ACTIONS | {'confirm'}
        if name=='SourceDyePFieldValid':
            excluded |= {'machine_board'}
        if not reviewed:
            excluded |= {'approve', 'reopen'}
            workflow.pop('editable_states', None)
        workflow['actions'] = [a for a in workflow.get('actions', []) if a['key'] not in excluded]
        if not reviewed:
            for action in workflow['actions']:
                action.pop('states', None)
        if name in BUSINESS_QUERIES:
            title, fields = BUSINESS_QUERIES[name]
            inputs = [{'key':key,'title':label,'kind':kind,
                       'required':name=='SourceDyePurMain','options':[]} for key,label,kind in fields]
            for field in inputs:
                if field['key']=='date_mode':
                    field.update(kind='select',default=1,options=[
                        {'value':1,'label':'结束时间前一天'}, {'value':2,'label':'结束时间前一个月'},
                        {'value':3,'label':'指定起止时间'}])
            workflow['actions'].append({'key':'business_query','title':title,'detail':False,'inputs':inputs})
        if name=='SourceDyePMachine':
            workflow['actions'].append({'key':'machine_board','title':'染色机台排程看板','detail':False,'inputs':[]})
        hidden = {'approval_stage', 'confirmed_at', 'confirmed_by', 'approved_at', 'approved_by'}
        config['crud_fields'] = [field for field in config['crud_fields'] if field not in hidden]
        if name=='SourceDyePCustomer':
            # 旧门户/客户端配置原值可导入留存，新系统登录不使用这些字段。
            for field in ['old_password','old_login_name','old_xmlfolder','old_port_no']:
                if field in config['crud_fields']:
                    config.setdefault('fields', {})[field] = {'column':{'show':False},'form':{'show':False}}
        if name=='SourceDyeHEmployee':
            config.setdefault('fields', {})['old_password'] = {'column':{'show':False},'form':{'show':False}}
