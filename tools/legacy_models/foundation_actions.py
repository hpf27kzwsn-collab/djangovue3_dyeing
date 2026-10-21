"""P1基础查询页面动作；每个处理函数都有明确的原来源。"""
def extend(table, options):
    actions = options['workflow']['actions']
    views = {'p_FieldValid': 'SourceFoundationViewSet', 'p_Machine': 'SourceMachineFoundationViewSet',
             'h_Employee': 'SourceEmployeeFoundationViewSet', 'p_Article': 'SourceArticleFoundationViewSet',
             'p_Customer': 'SourceArticleFoundationViewSet', 'p_Gray': 'SourceArticleFoundationViewSet',
             's_SysParams': 'SourceParameterFoundationViewSet', 's_AutoID': 'SourceDailyNumberViewSet',
             's_DBComboValue': 'SourceFoundationViewSet'}
    views.update({name:'SourcePlatformFoundationViewSet' for name in ['s_Functions','s_FuncUser','s_Roles','s_Permission','s_RptMenu','s_RptInfo','s_RptRight','s_FieldRight','s_UINav']})
    views['s_AccMonth']='SourceFoundationViewSet'
    if table not in views:
        return
    options['viewset'] = 'plugins.erp_base.source_foundation_api.'+views[table]
    if table in ['p_Machine', 'h_Employee', 'p_Article', 'p_Customer', 'p_Gray']:
        actions.append({'key': 'correspondence', 'title': '核对原资料对应',
                        'states': ['draft', 'confirmed', 'approved', None], 'inputs': []})
    if table == 'h_Employee':
        actions.append({'key': 'business_units', 'title': '查询原员工主体名单',
                        'states': ['draft', 'confirmed', 'approved', None], 'inputs': []})
    if table == 'p_FieldValid':
        def field(key, title, kind='text'):
            return {'key': key, 'title': title, 'kind': kind, 'required': True, 'nullable': True, 'options': []}
        actions.extend([
            {'key': 'convert_unit', 'title': '按旧函数换算单位', 'detail': False, 'inputs': [
                field('source_unit', '原单位（0米/1公斤/2码/3磅/4卷）', 'number'),
                field('destination_unit', '目标单位（其他原值仍可录入）', 'number'), field('quantity', '原数量')]},
            {'key': 'calendar_days', 'title': '按原日期函数展开', 'detail': False, 'inputs': [
                field('start', '开始日期（含）', 'date'), field('end', '结束日期（含）', 'date')]},
            {'key': 'foundation_lookup', 'title': '查询原基础资料选项', 'detail': False, 'inputs': [
                {'key': 'lookup_id', 'title': '原资料项', 'kind': 'select', 'required': True, 'options': [
                    {'value': value, 'label': label} for value, label in [
                        ('B049', '机物料单位（名称）'), ('B062', '部门/机台分厂'), ('B084', '加工站别'), ('B085', '生产车间')]]}]},
        ])
    def input_field(key, title, kind='text', nullable=True):
        return {'key': key, 'title': title, 'kind': kind, 'required': True, 'nullable': nullable, 'options': []}
    if table in ['p_FieldValid', 's_DBComboValue']:
        actions.append({'key': 'original_combo', 'title': '查询原组合框选项', 'detail': False, 'inputs': [
            input_field('combo_id', '组合框编号'), input_field('filter_text', '筛选内容（空串查全部）')]})
    if table == 'p_FieldValid':
        import json
        from pathlib import Path
        lookups = json.loads((Path(__file__).resolve().parents[2]/'backend/plugins/erp_base/source_foundation_lookups.json').read_text(encoding='utf8'))['lookups']
        actions.extend([
            {'key':'machine_board','title':'查看原染色机台排程看板','detail':False,'inputs':[]},
            {'key':'original_view','title':'完整原基础及产量查询','detail':False,'inputs':[
                dict(input_field('name','原报表','select',False),options=[{'value':name,'label':label} for name,label in [
                    ('A_GrayID','坯料和客户坯料'),('CureDyeByBill','按单染化料'),('CureDyeByBill_LX','按单染化料另一版'),
                    ('MaxSavePlease','客户保留期限'),('s_vwColorDepth','颜色深度'),('s_vwCustomer','客户汇总'),
                    ('v_App_Customer','现场客户'),('v_APP_EmployeeDevice','员工设备'),('v_Customer','客户联系人'),
                    ('v_DyePhase','染程阶段'),('v_DyeWorkQty_Day','每日染色产量'),('V_GrayToProduct','坯料产品对应'),
                    ('v_KQ_CType','考勤刷卡类型'),('v_KQ_InRecord','上班记录'),('v_KQ_OutRecord','下班记录'),
                    ('v_PatQuery','薪酬原计算来源'),('V_Stuff','染化料'),('vw_DyeWorkQtyQuer','染色计件产量'),
                    ('vw_ZHENZHIYUNFEITJ1','针织运费业务数量'),('sp_app_QueryEmployees','完整员工资料')]])]},
            {'key':'original_app_report','title':'现场报价、产量及采购费用查询','detail':False,'inputs':[
                dict(input_field('name','查询','select',False),options=[{'value':v,'label':n} for v,n in [('Sp_AppQueryFeelOfferMain','手感报价'),('SP_APP_QueryOutputSum','岗位工序产量'),('Sp_CookQuery','采购入库费用来源')]]),
                input_field('filter_text','筛选内容'),input_field('current','页码','number'),input_field('size','每页条数','number'),
                input_field('employee','员工编号'),input_field('date_mode','日期模式：0指定范围/1日/2月','number'),
                input_field('start','开始时间','datetime'),input_field('end','结束时间','datetime')]},
            {'key':'original_table_export','title':'导出完整原字段及留档记录','detail':False,'inputs':[input_field('model','原模型标识',nullable=False)]},
            {'key':'original_field_number','title':'预览原字段编号规则','detail':False,'inputs':[
                input_field('model','原模型标识',nullable=False),input_field('field','原字段名',nullable=False),
                input_field('rule','原字段编号参数','json',False),input_field('series','单据内部编号'),input_field('at','编号时间','datetime',False)]},
            {'key':'original_table_transform','title':'原临时表分页及员工展列','detail':False,'inputs':[
                dict(input_field('name','处理规则','select',False),options=[{'value':v,'label':n} for v,n in [('RowToColumn','员工金额展列'),('Sp_DyeRowDenormaliser','染色员工展列'),('Sp_WagesRowDenormaliser','工资来源员工展列'),('Pro_GetPageData','原通用分页'),('spSqlPageByRowNumber','按行号分页')]]),
                input_field('records','来源明细','json',False),input_field('order_fields','排序字段','array',False),
                input_field('size','每页条数','number'),input_field('index','页码','number')]},
        ])
        actions.extend([
            {'key': 'original_function', 'title': '原文本及数字处理', 'detail': False, 'inputs': [
                dict(input_field('function', '处理规则', 'select', False), options=[{'value': name, 'label': title} for name,title in [
                    ('Fn_Get_AZ','取字母'),('Fn_Get_NumNo','取数字及点号'),('GET_NUMBER','取全部数字'),
                    ('F_Get_No','色号数字（10字节）'),('Fn_Get_No','打样色号数字（20字节）'),
                    ('GetNumberFromString3','取首段数字'),('NormalizeTextFast','原标点与换行转换'),
                    ('SafeVarToFloat','原四位小数转换'),('SafeVarToInt','原整数转换'),('f_GetPy','基础拼音首字母'),
                    ('fun_getPY','另一版原拼音首字母'),('fn_ExpandRange','展开数字范围'),('fn_GetDyeVat','按原重量计算缸数')]]), input_field('value','原内容')]},
            {'key': 'continuous_dates', 'title': '展开连续年月日期', 'detail': False, 'inputs': [input_field('value','基准日期','date'),
                input_field('kind','年year/月month/日day/年中月ym/月中日md'),input_field('previous','往前数量或指定月起日','number'),input_field('following','后续数量或指定月止日','number')]},
            {'key': 'original_lookup', 'title': '查询原资料选择项', 'detail': False, 'inputs': [
                dict(input_field('lookup_id','资料选择项','select',False),options=[{'value': key,'label': key+' '+str(row['LookupName'])+('（待接入）' if row['adapter'] is None else '')} for key,row in lookups.items()]),
                input_field('filter_text','筛选内容（空串查全部）')]},
        ])
        actions.append({'key':'original_shared_function','title':'原名单、手感和打印格式','detail':False,'inputs':[
            dict(input_field('function','规则','select',False),options=[{'value':name,'label':title} for name,title in [
                ('L2U','数字大写打印格式'),('ChangeIDListToEmpName','员工名单转姓名'),('fn_APP_ChangeIDListToEmpName','APP员工名单转姓名'),
                ('get_fsplit_StationID','工位字符串拆分'),('fn_GetFeelCode','原产品手感代码'),
                ('fn_GetWorkQtyCount','原月份计件金额返回'),('fn_GetPackQtyPrice','包装工序单价'),
                ('New_StringSplit','原员工名单拆分'),('f_splitWithRowNo','带行号拆分')]]),
            input_field('value','原内容'),input_field('extra','分隔符或打印格式（L2U为0时合并零）')]})
        reports=['A_GrayID','s_vwCustomer','v_App_Customer','v_APP_EmployeeDevice','v_Customer','v_DyePhase',
                 'V_GrayToProduct','V_Stuff','v_KQ_CType','MaxSavePlease','sp_App_GetEmployeePhone',
                 'sp_App_O_GetPostList','sp_App_sysGetMFEmpGroup','sp_App_GetAppChildFunctions']
        actions.append({'key':'original_foundation_report','title':'查询原基础资料视图','detail':False,'inputs':[
            dict(input_field('name','原查询','select',False),options=[{'value':name,'label':name} for name in reports]),
            input_field('value','名单或功能号（其余查询可空）'),input_field('employee','员工编码（导航查询使用）')]})
    if table in ['p_FieldValid','s_AccMonth']:
        actions.append({'key':'original_period','title':'查询原业务期间及历时','detail':False,'inputs':[input_field('value','原时间','datetime'),dict(input_field('begin','原过程传入的开始日期','datetime'),required=False),dict(input_field('end','原过程传入的结束日期','datetime'),required=False)]})
    if views[table]=='SourcePlatformFoundationViewSet':
        operations=['s_FuncUser_Add','s_FuncUser_UpdateSerialNum','GetPrintRight','sp_FuncStop','Sp_UpdateFuncNo','sp_UINav_To_Functions','sp_s_FieldRight','sp_FuncNoPrint']
        actions.append({'key':'original_config','title':'办理原导航及报表配置','detail':False,'inputs':[
            dict(input_field('operation','原办理规则','select',False),options=[{'value':name,'label':name} for name in operations]),
            input_field('value','员工/功能/角色编号（改号填原号）'),input_field('extra','菜单功能号/报表员工号/新功能号'),input_field('index','菜单新序号（-1移到最后）','number')]})
    if table == 's_SysParams':
        actions.extend([{'key':'original_value','title':'查询原函数参数值','states':[None,'draft','confirmed','approved'],'inputs':[]},
                        {'key':'system_parameters','title':'查询原现场参数','detail':False,'inputs':[]}])
    if table == 's_AutoID':
        actions.append({'key':'allocate_number','title':'领取原统一编号','detail':False,'inputs':[
            input_field('object_name','编号对象',nullable=False),input_field('digits','流水位数','number'),
            dict(input_field('long_date','日期格式','select',False),options=[{'value':False,'label':'短日期 yyMMdd'},{'value':True,'label':'完整日期 yyyyMMdd'}])]})
