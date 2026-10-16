"""第一阶段逐对象实现位置；有代码不等于已逐入口验收。"""
GROUPS={
 'source_foundation_functions.py':('F_Get_No Fn_Get_No','两种原数字提取按100字节输入及10/20字节返回接入，16组只读SQL一致，报价/调价/打样失效调用补齐全角及字节截断；完整排序边界继续见E106'),
 'source_foundation_scalars.py':('f_GetPy fun_getPY fn_ExpandRange fn_GetDyeVat L2U GetStrTimeFormat ChangeIDListToEmpName fn_APP_ChangeIDListToEmpName fn_GetFeelCode fn_GetPackQtyPrice get_fsplit_StationID New_StringSplit f_splitWithRowNo',
    '已接入基础函数service和查询动作；保留原截断、NULL、错误和拆串规则，63,488个BMP字符及56组原标量证据；字符排序/无序/非BMP差异见E106'),
 'source_foundation_periods.py':('GetAccBeginDate GetAccEndDate ufn_GetAccFirstDate Sp_GetAccDate',
    '已接入原期间字段、两套期间算法、跨年/闰日及时间查询；独立财务记账未启用，日期及原输出参数差异见E107'),
 'source_field_numbers.py':('FD_GetFieldSeries',
    '六路原编号算法已提供不占号预览，含AutoAdd原SUBSTRING问题及DateCode回绕；新单据事务编号保持独立，原SQLFilter协议及自动调用映射差异见E107'),
 'source_foundation_platform.py':('GetPrintRight s_FuncUser_Add s_FuncUser_UpdateSerialNum sp_FuncNoPrint sp_FuncStop sp_s_FieldRight sp_UINav_To_Functions Sp_UpdateFuncNo',
    '原收藏、顺序、导航、字段/打印权限记录操作已接入管理员动作和事务审计；旧角色记录不自动授予新Django权限；固定角色、无序和原批量差异见E108'),
 'source_master_data.py':('DelEmployee FeelOfferDetail_Del FeelOfferDetail_Modify KindLimitInsert LimitInsert NoLimitInsert p_Customer_UPDATE p_CustomerInsert p_Dept_Add p_GrayModify UpdateEmployee USERINFO_Add',
    '已接入原主档保存/删除及批量字段更新服务；重复保留并记原检查，删除影响退出活动范围而原行留档，UPDATE字段时点和逐行处理差异见E105'),
 'source_foundation_led.py':('Led',
    '02站排程看板已接入，保留空机台、NULL文字、重名机台及重复连接；动态列改记录ID并保留原列名，原无序行号差异见E111'),
 'source_foundation_utilities.py':('Pro_GetPageData spSqlPageByRowNumber RowToColumn Sp_DyeRowDenormaliser Sp_WagesRowDenormaliser sp_GenInsertSQL',
    '分页、原临时表展列及完整原字段导出已接入服务/动作；空员工、超99组、原SQL文本协议与二进制处理差异见E111'),
 'source_foundation_views.py':('sp_App_GetAppChildFunctions sp_App_GetEmployeePhone sp_App_O_GetPostList sp_App_sysGetMFEmpGroup',
    '原现场子导航、电话、岗位和人员组查询已接入；完整候选和原角色关联保留，不复用为当前授权，原无序和客户端界面待逐入口验收，见E108/E109'),
 'source_foundation_view_reports.py':('A_GrayID CureDyeByBill CureDyeByBill_LX MaxSavePlease s_vwColorDepth s_vwCustomer v_App_Customer v_APP_EmployeeDevice v_Customer v_DyePhase v_DyeWorkQty_Day V_GrayToProduct v_KQ_CType v_KQ_InRecord v_KQ_OutRecord v_PatQuery V_Stuff vw_DyeWorkQtyQuer vw_ZHENZHIYUNFEITJ1 sp_app_QueryEmployees fn_GetWorkQtyCount',
    '原19视图、完整员工查询及月计件返回已接入；当前库22个查询含依赖结构执行通过，非全历史逐行等价证明；分组排序、月计件自比较及多费率分组差异见E109'),
 'source_foundation_app_reports.py':('SP_APP_QueryOutputSum Sp_AppQueryFeelOfferMain Sp_CookQuery',
    '报价表头分页/全部明细、岗位工序产量和采购入库费用四层汇总已接入；旧产量调用参数/列数失配按原实际数量来源接续，见E110'),
 'source_static_lookup.py':('sp_App_S_GetLookUpListByID',
    '266项定义保留：262项本地可查、4项中控外库明确缺资料；新增161项中159项对照逐值一致、2项分组/数量一致但原文代表值不同；旧拼接缺陷修正及附加列范围见E112'),
}


def registrations():
    return {name:description for names,description in GROUPS.values() for name in names.split()}
