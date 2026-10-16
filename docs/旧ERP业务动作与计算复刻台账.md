# 旧ERP业务动作与计算复刻台账

生成依据：保存的有效入口配置及原完整配置快照。日期：2026-10-14。

台账中的“待逐项对照”表示证据已登记，不表示代码已复刻。空值、注释SQL和原公式均保留证据；旧SQL不执行。连接阶段和物料明细的入口同时列实际连接模型，公式证据另标记物理目标，查询别名不会冒充阶段字段。

2026-10-15第十七批增量：正式DPJobStep与DPJobSheet、三套备料视图及fn_GetPhaseNo、班组人员比例、排班审核/报工人员重建及撤回已接入；四类现场入口的不同主从关系与缺省字段继承分别实现。两个实际排班1,404组、30组比例和称料投影/扫码实际结果对照通过。非空设备步骤与客户端补录仍需实际证据，中控七表未伪造接入。见本批实施记录及异常E85～E89。

2026-10-15第十六批增量：报价明细三个触发检查、打样对色责任、主工号计件/工作日/日报、EmpID1计件变体和DPJobStep_Test已接入服务与页面。重复报价按要求照存、原审核状态限制保留；SQL只读证明跨曲线引用和浮点边界。当前未匹配称料阶段仍保留，不能把0步骤结果当作真实设备验收。详见本批实施记录及异常E82～E84。

2026-10-15第十五批增量：12个报价函数及完整候选、Sp_DyeDipsRecord/1/2/10/22/EmpID六规则、普通/复版打样排单、ProdTest七入口及加色AfterSave生成/替换留档/撤回已接入。99组实际SQL函数结果一致。当前报价明细和试验表为空，功能非空分支经隔离测试；不把空历史结果称为现场验收。sp_AuTo_Quote缺失P_ColorNum3及其他差异见E78～E81，剩余触发器/计件日报/DPJobStep_Test仍单列待办。详见《2026-10-15报价打样排单试验变体实施记录》。

2026-10-15第六批增量：JobProcess自动合卡预览/同步、原称料正反向成员/排程延迟选路、所涉工卡空进度及剩余染程步骤；JobSheet/JobCombine/JobCombineOrder本次计划采用逆向；GrayInRecord/JobGrayRecord四套细码拆合及GrayRecordCutLogs撤回已接入。已消耗行留档并退出活动汇总，异常量继续办理。详见本批实施记录和异常E46～E49。原合卡质量重建尾段、全库维护和实际单据整链逆向仍单列待办，未批量标记全部入口完成。

2026-10-15增量：OrderMain/OrderColor变更回写、PriceAdjust明细触发及审核逆向、TrialDyeRecipe确板版本和配方染程/用料/金额规则已接入service。具体触发范围、合理差异与验证见《2026-10-15销售调价与打样业务链实施记录》、程序覆盖台账及异常E24～E26。下表仍登记完整入口，不能把局部分支已接入批量改成整个入口已对照通过。

2026-10-15第二批增量：订单另收费取价及整单汇总、工卡另收费查询、ShowDyeLabMain色号同步、打样结果/回复、A～F列采用及试产转生产、样品入出库已接入。对应按钮、字段和测试见《2026-10-15另收费与打样接续实施记录》；多候选取价、原删除重建、客户端缺项和样品生效时点分别见异常E27～E30。全部原入口继续登记，未覆盖的试验变体及其他报价过程仍为待办。

2026-10-15第三批增量：PurMain/机物料及染化料采购申请的实际收货引用、采购进度和分批收货；两类发外申请、实际发出与分批回货；对色累计/班组、疵布处理及余额、评审回修引用、刷卡机台继承和指定产量规则已接入。原保存即更新库存的时点保留。详细边界和例外见异常E31～E35及《2026-10-15采购外协生产质量接续实施记录》。未关闭程序继续逐项登记。

| 原入口 | 原表/模型（含明确连接明细） | 主入口 | 公式数 | 钩子SQL数 | 状态 |
|---|---|---|---:|---:|---|
| AddJobShiftEmpEdit | JobShiftEmp / erp_production.SourceDyeJobShiftEmp | AddWProcessEdit | 0 | 0 | 待逐项对照 |
| AddStuffWeight | StuffWeight / erp_production.SourceDyeStuffWeight | None | 4 | 7 | 待逐项对照 |
| AddStuffWeightPhaseDetail | StuffWeightPhase / erp_production.SourceDyeStuffWeightPhase；连接：erp_production.SourceDyeStuffWeightDetail | AddStuffWeight | 6 | 0 | 待逐项对照 |
| AddWProcessEdit | WProcess / erp_production.SourceDyeWProcess | None | 1 | 0 | 待逐项对照 |
| AfterNormalStuffWeight | StuffWeight / erp_production.SourceDyeStuffWeight | None | 2 | 8 | 待逐项对照 |
| AfterNormalStuffWeightPhaseDetail | StuffWeightPhase / erp_production.SourceDyeStuffWeightPhase；连接：erp_production.SourceDyeStuffWeightDetail | AfterNormalStuffWeight | 6 | 0 | 待逐项对照 |
| ArticleIn | ArticleIn / erp_warehouse.SourceDyeArticleIn | None | 0 | 3 | 待逐项对照 |
| ArticleInDetail | ArticleInDetail / erp_warehouse.SourceDyeArticleInDetail | ArticleIn | 2 | 0 | 待逐项对照 |
| ArticleOut | ArticleOut / erp_warehouse.SourceDyeArticleOut | None | 0 | 0 | 待逐项对照 |
| ArticleOutDetail | ArticleOutDetail / erp_warehouse.SourceDyeArticleOutDetail | ArticleOut | 1 | 0 | 待逐项对照 |
| ArticlePurApplyDetail | PurApplyDetail / erp_purchase.SourceDyePurApplyDetail | ArticlePurApplyMain | 1 | 0 | 待逐项对照 |
| ArticlePurApplyMain | PurApplyMain / erp_purchase.SourceDyePurApplyMain | None | 0 | 3 | 待逐项对照 |
| ArticlePurDetail | PurDetail / erp_purchase.SourceDyePurDetail | ArticlePurMain | 1 | 0 | 待逐项对照 |
| BulkDyeRecipe | DyeRecipe / erp_sampling.SourceDyeDyeRecipe | None | 1 | 0 | 待逐项对照 |
| BulkDyeRecipePhaseDetail | DyeRecipePhase / erp_sampling.SourceDyeDyeRecipePhase；连接：erp_sampling.SourceDyeDyeRecipeDetail | BulkDyeRecipe | 1 | 0 | 待逐项对照 |
| ChengBen_Gray | p_Gray / erp_base.SourceDyePGray | None | 0 | 1 | 待逐项对照 |
| ChengBen_Kind | p_Gray / erp_base.SourceDyePGray | None | 0 | 1 | 待逐项对照 |
| CusReturnSemiIn | SemiIn / erp_warehouse.SourceDyeSemiIn | None | 0 | 1 | 待逐项对照 |
| CusReturnSemiInDetail | SemiInDetail / erp_warehouse.SourceDyeSemiInDetail | CusReturnSemiIn | 1 | 0 | 待逐项对照 |
| CustomerTS | CustomerTS / erp_sales.SourceDyeCustomerTS | None | 0 | 0 | 待逐项对照 |
| CustomerTSDetail | CustomerTSDetail / erp_sales.SourceDyeCustomerTSDetail | CustomerTS | 0 | 0 | 待逐项对照 |
| CustomerTSSumInfo | CustomerTSDetail / erp_sales.SourceDyeCustomerTSDetail |  | 0 | 0 | 待逐项对照 |
| DefectGroup | p_FieldValid / erp_base.SourceDyePFieldValid | None | 0 | 0 | 待逐项对照 |
| DefectKind | p_FieldValid / erp_base.SourceDyePFieldValid | None | 0 | 0 | 待逐项对照 |
| DPJobAssign | JobAssign / erp_production.SourceDyeJobAssign | DPJobSheet | 0 | 0 | 待逐项对照 |
| DPJobProcess | JobProcess / erp_production.SourceDyeJobProcess | DPJobSheet | 0 | 0 | 待逐项对照 |
| DPJobSheet | JobSheet / erp_production.SourceDyeJobSheet |  | 0 | 0 | 待逐项对照 |
| DPJobShiftEmpEdit | JobShiftEmp / erp_production.SourceDyeJobShiftEmp | DPWProcessEdit | 4 | 0 | 待逐项对照 |
| DPJudgeStatus | JobProcess / erp_production.SourceDyeJobProcess | None | 0 | 0 | 待逐项对照 |
| DPProcess | JobProcess / erp_production.SourceDyeJobProcess | None | 0 | 0 | 待逐项对照 |
| DPWDefect | WDefect / erp_quality.SourceDyeWDefect | None | 0 | 0 | 待逐项对照 |
| DPWProcess | WProcess / erp_production.SourceDyeWProcess | None | 0 | 0 | 待逐项对照 |
| DPWProcessEdit | WProcess / erp_production.SourceDyeWProcess | None | 0 | 0 | 待逐项对照 |
| DStuffOut | StuffOut / erp_warehouse.SourceDyeStuffOut | None | 0 | 0 | 待逐项对照 |
| DStuffOutDetail | StuffOutDetail / erp_warehouse.SourceDyeStuffOutDetail | DStuffOut | 1 | 0 | 待逐项对照 |
| DyeDipsRecord | DyeDipsRecord / erp_sampling.SourceDyeDyeDipsRecord |  | 0 | 1 | 待逐项对照 |
| DyeDipsRecordBulk | DyeDipsRecord / erp_sampling.SourceDyeDyeDipsRecord | None | 0 | 0 | 待逐项对照 |
| DyeingTubeWaste | p_FieldValid / erp_base.SourceDyePFieldValid | None | 0 | 0 | 待逐项对照 |
| DyeLabColor | DyeLabColor / erp_sampling.SourceDyeDyeLabColor | DyeLabMain | 4 | 1 | 待逐项对照 |
| DyeLabColorBulk | DyeLabColor / erp_sampling.SourceDyeDyeLabColor | DyeLabMainBulk | 0 | 0 | 待逐项对照 |
| DyeLabMain | DyeLabMain / erp_sampling.SourceDyeDyeLabMain | None | 0 | 1 | 待逐项对照 |
| DyeLabMainBulk | DyeLabMain / erp_sampling.SourceDyeDyeLabMain | None | 0 | 0 | 待逐项对照 |
| DyeRecipe | DyeRecipe / erp_sampling.SourceDyeDyeRecipe | None | 0 | 0 | 待逐项对照 |
| DyeRecipeDetail | DyeRecipeDetail / erp_sampling.SourceDyeDyeRecipeDetail | DyeRecipePhase | 0 | 0 | 待逐项对照 |
| DyeRecipePhase | DyeRecipePhase / erp_sampling.SourceDyeDyeRecipePhase | DyeRecipe | 0 | 0 | 待逐项对照 |
| DyeRecipePhaseDetail | DyeRecipePhase / erp_sampling.SourceDyeDyeRecipePhase；连接：erp_sampling.SourceDyeDyeRecipeDetail | DyeRecipe | 1 | 0 | 待逐项对照 |
| FabricArticleIn | ArticleIn / erp_warehouse.SourceDyeArticleIn | None | 0 | 4 | 待逐项对照 |
| FabricArticleInDetail | ArticleInDetail / erp_warehouse.SourceDyeArticleInDetail | FabricArticleIn | 2 | 0 | 待逐项对照 |
| FabricArticleOut | ArticleOut / erp_warehouse.SourceDyeArticleOut | None | 0 | 0 | 待逐项对照 |
| FabricArticleOutDetail | ArticleOutDetail / erp_warehouse.SourceDyeArticleOutDetail | FabricArticleOut | 1 | 0 | 待逐项对照 |
| FinishDyeRecipe | DyeRecipe / erp_sampling.SourceDyeDyeRecipe | None | 1 | 0 | 待逐项对照 |
| FinishDyeRecipePhaseDetail | DyeRecipePhase / erp_sampling.SourceDyeDyeRecipePhase；连接：erp_sampling.SourceDyeDyeRecipeDetail | FinishDyeRecipe | 1 | 0 | 待逐项对照 |
| FixedPrice | Quote / erp_sales.SourceDyeQuote | None | 1 | 1 | 待逐项对照 |
| FixedPriceDetail | QuoteDetail / erp_sales.SourceDyeQuoteDetail | FixedPrice | 1 | 0 | 待逐项对照 |
| GrayAllotIn | GrayIn / erp_warehouse.SourceDyeGrayIn | None | 0 | 0 | 待逐项对照 |
| GrayAllotInDetail | GrayInDetail / erp_warehouse.SourceDyeGrayInDetail | GrayAllotIn | 3 | 0 | 待逐项对照 |
| GrayAllotOut | GrayOut / erp_warehouse.SourceDyeGrayOut | None | 0 | 0 | 待逐项对照 |
| GrayAllotOutDetail | GrayOutDetail / erp_warehouse.SourceDyeGrayOutDetail | GrayAllotOut | 0 | 0 | 待逐项对照 |
| GrayIn | GrayIn / erp_warehouse.SourceDyeGrayIn | None | 4 | 2 | 待逐项对照 |
| GrayInDetail | GrayInDetail / erp_warehouse.SourceDyeGrayInDetail | GrayIn | 3 | 0 | 待逐项对照 |
| GrayInDetailUpdate | GrayInDetail / erp_warehouse.SourceDyeGrayInDetail |  | 0 | 1 | 待逐项对照 |
| GrayInEdit | GrayIn / erp_warehouse.SourceDyeGrayIn | None | 0 | 0 | 待逐项对照 |
| GrayInToAPList | GrayInDetail / erp_warehouse.SourceDyeGrayInDetail | None | 0 | 0 | 待逐项对照 |
| GrayInWork | GrayIn / erp_warehouse.SourceDyeGrayIn | None | 4 | 2 | 待逐项对照 |
| GrayInWorkDetail | GrayInDetail / erp_warehouse.SourceDyeGrayInDetail | GrayInWork | 3 | 0 | 待逐项对照 |
| GrayMaterial | GrayMaterial / erp_warehouse.SourceDyeGrayMaterial | None | 0 | 0 | 待逐项对照 |
| GrayMaterialDetail | GrayMaterialDetail / erp_warehouse.SourceDyeGrayMaterialDetail | GrayMaterial | 0 | 0 | 待逐项对照 |
| GrayOut | GrayOut / erp_warehouse.SourceDyeGrayOut | None | 1 | 5 | 待逐项对照 |
| GrayOutDetail | GrayOutDetail / erp_warehouse.SourceDyeGrayOutDetail | GrayOut | 1 | 0 | 待逐项对照 |
| GrayOutDetailJob | GrayOutDetail / erp_warehouse.SourceDyeGrayOutDetail | GrayOutJob | 1 | 0 | 待逐项对照 |
| GrayOutDetailShenHe | GrayOutDetail / erp_warehouse.SourceDyeGrayOutDetail | GrayOutShenHe | 0 | 0 | 待逐项对照 |
| GrayOutDetailTurn | GrayOutDetail / erp_warehouse.SourceDyeGrayOutDetail | GrayOutTurn | 2 | 0 | 待逐项对照 |
| GrayOutEdit | GrayOut / erp_warehouse.SourceDyeGrayOut | None | 0 | 0 | 待逐项对照 |
| GrayOutJob | GrayOut / erp_warehouse.SourceDyeGrayOut | None | 0 | 5 | 待逐项对照 |
| GrayOutSale | GrayOut / erp_warehouse.SourceDyeGrayOut | None | 1 | 5 | 待逐项对照 |
| GrayOutSaleDetail | GrayOutDetail / erp_warehouse.SourceDyeGrayOutDetail | GrayOutSale | 2 | 0 | 待逐项对照 |
| GrayOutShenHe | GrayOut / erp_warehouse.SourceDyeGrayOut | None | 0 | 2 | 待逐项对照 |
| GrayOutToSemiIn | SemiIn / erp_warehouse.SourceDyeSemiIn | None | 0 | 1 | 待逐项对照 |
| GrayOutToSemiInDetail | SemiInDetail / erp_warehouse.SourceDyeSemiInDetail | GrayOutToSemiIn | 1 | 0 | 待逐项对照 |
| GrayOutTurn | GrayOut / erp_warehouse.SourceDyeGrayOut | None | 1 | 5 | 待逐项对照 |
| GrayOutWork | GrayOut / erp_warehouse.SourceDyeGrayOut | None | 0 | 5 | 待逐项对照 |
| GrayOutWorkDetail | GrayOutDetail / erp_warehouse.SourceDyeGrayOutDetail | GrayOutWork | 0 | 0 | 待逐项对照 |
| GrayStockAdjust | GrayStockAdjust / erp_warehouse.SourceDyeGrayStockAdjust | None | 0 | 4 | 待逐项对照 |
| GrayStockAllot | GrayStockAllot / erp_warehouse.SourceDyeGrayStockAllot | None | 0 | 0 | 待逐项对照 |
| GrayStockCheck | GrayStockCheck / erp_warehouse.SourceDyeGrayStockCheck | None | 0 | 0 | 待逐项对照 |
| h_Employee | h_Employee / erp_base.SourceDyeHEmployee |  | 2 | 0 | 待逐项对照 |
| h_EmployeeEdit | h_Employee / erp_base.SourceDyeHEmployee |  | 2 | 0 | 待逐项对照 |
| h_EmployeeEditALL | h_Employee / erp_base.SourceDyeHEmployee |  | 1 | 0 | 待逐项对照 |
| h_Employeelit | h_Employee / erp_base.SourceDyeHEmployee | None | 0 | 0 | 待逐项对照 |
| HUOCHEZL | p_FieldValid / erp_base.SourceDyePFieldValid | None | 0 | 0 | 待逐项对照 |
| JiaNianGrayIn | GrayIn / erp_warehouse.SourceDyeGrayIn | None | 4 | 1 | 待逐项对照 |
| JiaNianGrayInDetail | GrayInDetail / erp_warehouse.SourceDyeGrayInDetail | JiaNianGrayIn | 3 | 0 | 待逐项对照 |
| JobAssign | JobAssign / erp_production.SourceDyeJobAssign | JobSheet | 0 | 0 | 待逐项对照 |
| JobAssignCombined | JobAssign / erp_production.SourceDyeJobAssign | JobSheetCombined | 0 | 0 | 待逐项对照 |
| JobAtte | JobAtte / erp_production.SourceDyeJobAtte | JobSheet | 0 | 0 | 待逐项对照 |
| JobAtteForDeal | JobAtte / erp_production.SourceDyeJobAtte | JobSheetForDeal | 0 | 0 | 待逐项对照 |
| JobCardCombined | JobCombine / erp_production.SourceDyeJobCombine | JobSheetCombined | 0 | 0 | 待逐项对照 |
| JobCombine | JobCombine / erp_production.SourceDyeJobCombine | JobSheet | 0 | 0 | 待逐项对照 |
| JobCombineForDeal | JobCombine / erp_production.SourceDyeJobCombine | JobSheetForDeal | 0 | 0 | 待逐项对照 |
| JobCombineOrder | JobCombineOrder / erp_production.SourceDyeJobCombineOrder | JobSheet | 0 | 0 | 待逐项对照 |
| JobCraft | JobProcess / erp_production.SourceDyeJobProcess | None | 0 | 0 | 待逐项对照 |
| JobCraftListForSelect | JobSheet / erp_production.SourceDyeJobSheet | None | 0 | 0 | 待逐项对照 |
| JobCraftProcessI | JobProcess / erp_production.SourceDyeJobProcess | JobCraftList | 0 | 0 | 待逐项对照 |
| JobCraftProcessII | JobProcess / erp_production.SourceDyeJobProcess | JobCraftList | 0 | 0 | 待逐项对照 |
| JobProcess | JobProcess / erp_production.SourceDyeJobProcess | JobSheet | 0 | 0 | 待逐项对照 |
| JobProcess2 | JobProcess / erp_production.SourceDyeJobProcess | None | 0 | 0 | 待逐项对照 |
| JobProcessForDeal | JobProcess / erp_production.SourceDyeJobProcess | JobSheetForDeal | 0 | 0 | 待逐项对照 |
| JobSheet | JobSheet / erp_production.SourceDyeJobSheet | None | 10 | 4 | 待逐项对照 |
| JobSheetColorNum | JobSheet / erp_production.SourceDyeJobSheet | None | 0 | 0 | 待逐项对照 |
| JobSheetCombine | JobCombine / erp_production.SourceDyeJobCombine | JobSheet | 0 | 0 | 待逐项对照 |
| JobSheetCombined | JobSheet / erp_production.SourceDyeJobSheet | None | 0 | 0 | 待逐项对照 |
| JobSheetCombinedOrder | JobCombineOrder / erp_production.SourceDyeJobCombineOrder | JobSheetCombined | 0 | 0 | 待逐项对照 |
| JobSheetForDeal | JobSheet / erp_production.SourceDyeJobSheet | None | 0 | 0 | 待逐项对照 |
| JobSheetQuery | JobSheet / erp_production.SourceDyeJobSheet | None | 2 | 5 | 待逐项对照 |
| JobShiftEmp | JobShiftEmp / erp_production.SourceDyeJobShiftEmp | DPWProcess | 0 | 0 | 待逐项对照 |
| JobShiftEmpEdit | JobShiftEmp / erp_production.SourceDyeJobShiftEmp | WProcessEdit | 4 | 0 | 待逐项对照 |
| KeTuiGrayIn | GrayIn / erp_warehouse.SourceDyeGrayIn | None | 4 | 1 | 待逐项对照 |
| KeTuiGrayInDetail | GrayInDetail / erp_warehouse.SourceDyeGrayInDetail | KeTuiGrayIn | 3 | 0 | 待逐项对照 |
| MachinePaste | p_FieldValid / erp_base.SourceDyePFieldValid | None | 0 | 0 | 待逐项对照 |
| MaterialSemiIn | SemiIn / erp_warehouse.SourceDyeSemiIn | None | 0 | 1 | 待逐项对照 |
| MaterialSemiInDetail | SemiInDetail / erp_warehouse.SourceDyeSemiInDetail | MaterialSemiIn | 1 | 0 | 待逐项对照 |
| NoexistsRecipeJobSheet | JobSheet / erp_production.SourceDyeJobSheet |  | 0 | 0 | 待逐项对照 |
| NormalStuffWeight | StuffWeight / erp_production.SourceDyeStuffWeight | None | 2 | 8 | 待逐项对照 |
| NormalStuffWeight_Wash | StuffWeight / erp_production.SourceDyeStuffWeight | None | 2 | 3 | 待逐项对照 |
| NormalStuffWeightPhaseDetail | StuffWeightPhase / erp_production.SourceDyeStuffWeightPhase；连接：erp_production.SourceDyeStuffWeightDetail | NormalStuffWeight | 6 | 0 | 待逐项对照 |
| NormalStuffWeightPhaseDetail_Wash | StuffWeightPhase / erp_production.SourceDyeStuffWeightPhase；连接：erp_production.SourceDyeStuffWeightDetail | NormalStuffWeight_Wash | 4 | 0 | 待逐项对照 |
| OrderAtte | OrderAtte / erp_sales.SourceDyeOrderAtte | OrderColor | 0 | 0 | 待逐项对照 |
| OrderAtte1 | OrderAtte / erp_sales.SourceDyeOrderAtte |  | 0 | 0 | 待逐项对照 |
| OrderAtteChange | OrderAtte / erp_sales.SourceDyeOrderAtte | OrderMainChange | 0 | 0 | 待逐项对照 |
| OrderAtteSup | OrderAtte / erp_sales.SourceDyeOrderAtte | OrderMainSup | 0 | 0 | 待逐项对照 |
| OrderColor | OrderColor / erp_sales.SourceDyeOrderColor | OrderMain | 5 | 0 | 待逐项对照 |
| OrderColorChange | OrderColor / erp_sales.SourceDyeOrderColor | OrderMainChange | 5 | 0 | 待逐项对照 |
| OrderColorJobCards | JobSheet / erp_production.SourceDyeJobSheet |  | 0 | 0 | 待逐项对照 |
| OrderColorSup | OrderColor / erp_sales.SourceDyeOrderColor | OrderMainSup | 5 | 0 | 待逐项对照 |
| OrderMain | OrderMain / erp_sales.SourceDyeOrderMain |  | 0 | 5 | 待逐项对照 |
| OrderMainChange | OrderMain / erp_sales.SourceDyeOrderMain |  | 0 | 4 | 待逐项对照 |
| OrderMainSup | OrderMain / erp_sales.SourceDyeOrderMain |  | 0 | 4 | 待逐项对照 |
| OtherDyeRecipe | DyeRecipe / erp_sampling.SourceDyeDyeRecipe | None | 0 | 0 | 待逐项对照 |
| OtherDyeRecipePhaseDetail | DyeRecipePhase / erp_sampling.SourceDyeDyeRecipePhase；连接：erp_sampling.SourceDyeDyeRecipeDetail | OtherDyeRecipe | 1 | 0 | 待逐项对照 |
| p_Article | p_Article / erp_base.SourceDyePArticle | None | 0 | 2 | 待逐项对照 |
| p_Customer | p_Customer / erp_base.SourceDyePCustomer | None | 1 | 3 | 待逐项对照 |
| p_Defect | p_FieldValid / erp_base.SourceDyePFieldValid | None | 0 | 0 | 待逐项对照 |
| p_DyeCurve | p_DyeCurve / erp_base.SourceDyePDyeCurve |  | 0 | 0 | 待逐项对照 |
| p_DyeCurveDetail | p_DyeCurveDetail / erp_base.SourceDyePDyeCurveDetail | p_DyeCurve | 1 | 0 | 待逐项对照 |
| p_DyeCurveDetailJJ | p_DyeCurveDetail / erp_base.SourceDyePDyeCurveDetail | p_DyeCurveJJ | 1 | 0 | 待逐项对照 |
| p_DyeCurveJJ | p_DyeCurve / erp_base.SourceDyePDyeCurve |  | 0 | 0 | 待逐项对照 |
| p_FieldValid | p_FieldValid / erp_base.SourceDyePFieldValid | None | 0 | 0 | 待逐项对照 |
| p_FieldValidDye | p_FieldValid / erp_base.SourceDyePFieldValid | None | 0 | 0 | 待逐项对照 |
| p_Gray | p_Gray / erp_base.SourceDyePGray | None | 0 | 2 | 待逐项对照 |
| p_Gray_Cust | p_Fabric_Cust / erp_base.SourceDyePFabricCust | p_Gray | 0 | 0 | 待逐项对照 |
| p_Machine | p_Machine / erp_base.SourceDyePMachine | None | 0 | 0 | 待逐项对照 |
| p_Process | p_Process / erp_base.SourceDyePProcess | None | 0 | 0 | 待逐项对照 |
| p_Product_Cust | p_Fabric_Cust / erp_base.SourceDyePFabricCust |  | 0 | 0 | 待逐项对照 |
| p_Proofing | p_FieldValid / erp_base.SourceDyePFieldValid | None | 0 | 0 | 待逐项对照 |
| p_Shift | p_Shift / erp_base.SourceDyePShift |  | 0 | 0 | 待逐项对照 |
| p_ShiftBY | p_Shift / erp_base.SourceDyePShift | None | 0 | 0 | 待逐项对照 |
| p_ShiftHZ | p_Shift / erp_base.SourceDyePShift |  | 0 | 1 | 待逐项对照 |
| p_ShiftKF | p_Shift / erp_base.SourceDyePShift | None | 0 | 1 | 待逐项对照 |
| p_ShiftPB | p_Shift / erp_base.SourceDyePShift | None | 0 | 1 | 待逐项对照 |
| p_ShiftRB | p_Shift / erp_base.SourceDyePShift | None | 0 | 1 | 待逐项对照 |
| p_ShiftSC | p_Shift / erp_base.SourceDyePShift | None | 0 | 1 | 待逐项对照 |
| p_ShiftTS | p_Shift / erp_base.SourceDyePShift | None | 0 | 0 | 待逐项对照 |
| p_ShiftZJ | p_Shift / erp_base.SourceDyePShift | None | 0 | 1 | 待逐项对照 |
| p_ShiftZM | p_Shift / erp_base.SourceDyePShift |  | 0 | 0 | 待逐项对照 |
| p_StorageUnitID | p_StorageUnitID / erp_base.SourceDyePStorageUnitID | None | 1 | 0 | 待逐项对照 |
| p_StorageUnitID_Area | p_StorageUnitID / erp_base.SourceDyePStorageUnitID | None | 0 | 0 | 待逐项对照 |
| p_StorageUnitID_Prod | p_StorageUnitID / erp_base.SourceDyePStorageUnitID | None | 1 | 0 | 待逐项对照 |
| p_Stuff | p_Stuff / erp_base.SourceDyePStuff |  | 3 | 0 | 待逐项对照 |
| p_Supplier | p_Customer / erp_base.SourceDyePCustomer | None | 1 | 0 | 待逐项对照 |
| PackBag | p_FieldValid / erp_base.SourceDyePFieldValid | None | 0 | 0 | 待逐项对照 |
| PackBag_QF | p_FieldValid / erp_base.SourceDyePFieldValid | None | 0 | 0 | 待逐项对照 |
| PrepareDyeRecipe | DyeRecipe / erp_sampling.SourceDyeDyeRecipe | None | 0 | 0 | 待逐项对照 |
| PrepareDyeRecipePhaseDetail | DyeRecipePhase / erp_sampling.SourceDyeDyeRecipePhase；连接：erp_sampling.SourceDyeDyeRecipeDetail | PrepareDyeRecipe | 1 | 0 | 待逐项对照 |
| PrintJobAssign | JobAssign / erp_production.SourceDyeJobAssign | PrintJobSheet | 0 | 0 | 待逐项对照 |
| PrintJobAtte | JobAtte / erp_production.SourceDyeJobAtte | PrintJobSheet | 0 | 0 | 待逐项对照 |
| PrintJobCombine | JobCombine / erp_production.SourceDyeJobCombine | PrintJobSheet | 0 | 0 | 待逐项对照 |
| PrintJobProcess | JobProcess / erp_production.SourceDyeJobProcess | PrintJobSheet | 0 | 0 | 待逐项对照 |
| PrintJobSheet | JobSheet / erp_production.SourceDyeJobSheet | None | 5 | 5 | 待逐项对照 |
| PrintMortarCarry | p_FieldValid / erp_base.SourceDyePFieldValid | None | 0 | 0 | 待逐项对照 |
| PrintOrderAtte | OrderAtte / erp_sales.SourceDyeOrderAtte | PrintOrderMain | 0 | 0 | 待逐项对照 |
| PrintOrderColor | OrderColor / erp_sales.SourceDyeOrderColor | PrintOrderMain | 7 | 0 | 待逐项对照 |
| PrintOrderMain | OrderMain / erp_sales.SourceDyeOrderMain |  | 0 | 1 | 待逐项对照 |
| PrintStarchWaste | p_FieldValid / erp_base.SourceDyePFieldValid | None | 0 | 0 | 待逐项对照 |
| ProcessPlanView | ProcessSchedule / erp_production.SourceDyeProcessSchedule | None | 0 | 0 | 待逐项对照 |
| ProcessSchedule | ProcessSchedule / erp_production.SourceDyeProcessSchedule | None | 0 | 0 | 待逐项对照 |
| ProcessScheduleDX | ProcessSchedule / erp_production.SourceDyeProcessSchedule | None | 0 | 0 | 待逐项对照 |
| ProcessScheduleFB | ProcessSchedule / erp_production.SourceDyeProcessSchedule | None | 0 | 0 | 待逐项对照 |
| ProcessScheduleGX | ProcessSchedule / erp_production.SourceDyeProcessSchedule | None | 0 | 0 | 待逐项对照 |
| ProcessScheduleRS | ProcessSchedule / erp_production.SourceDyeProcessSchedule | None | 0 | 1 | 待逐项对照 |
| ProcessStuffWeight | StuffWeight / erp_production.SourceDyeStuffWeight | None | 1 | 5 | 待逐项对照 |
| ProcessStuffWeightPhaseDetail | StuffWeightPhase / erp_production.SourceDyeStuffWeightPhase；连接：erp_production.SourceDyeStuffWeightDetail | ProcessStuffWeight | 3 | 0 | 待逐项对照 |
| ProdIn | ProdIn / erp_warehouse.SourceDyeProdIn | None | 4 | 4 | 待逐项对照 |
| ProdIn_ht | ProdIn / erp_warehouse.SourceDyeProdIn | None | 5 | 2 | 待逐项对照 |
| ProdInEdit | ProdIn / erp_warehouse.SourceDyeProdIn | None | 5 | 0 | 待逐项对照 |
| ProdInRecord | ProdInRecord / erp_warehouse.SourceDyeProdInRecord | ProdIn | 1 | 0 | 待逐项对照 |
| ProdInRecord_ht | ProdInRecord / erp_warehouse.SourceDyeProdInRecord | ProdIn_ht | 1 | 0 | 待逐项对照 |
| ProdInRecordWork | ProdInRecord / erp_warehouse.SourceDyeProdInRecord | ProdInWork | 1 | 0 | 待逐项对照 |
| ProdInWork | ProdIn / erp_warehouse.SourceDyeProdIn | None | 4 | 4 | 待逐项对照 |
| ProdOut | ProdOut / erp_warehouse.SourceDyeProdOut | None | 3 | 5 | 待逐项对照 |
| ProdOutDetail | ProdOutDetail / erp_warehouse.SourceDyeProdOutDetail | ProdOut | 3 | 0 | 待逐项对照 |
| ProdOutDetailUpdate | ProdOutDetail / erp_warehouse.SourceDyeProdOutDetail | ProdOutUpdate | 2 | 0 | 待逐项对照 |
| ProdOutUpdate | ProdOut / erp_warehouse.SourceDyeProdOut | None | 3 | 5 | 待逐项对照 |
| ProdStockAllot | ProdStockAllot / erp_warehouse.SourceDyeProdStockAllot | None | 0 | 0 | 待逐项对照 |
| ProdStockCheck | ProdStockCheck / erp_warehouse.SourceDyeProdStockCheck | None | 0 | 0 | 待逐项对照 |
| PurApplyDetail | PurApplyDetail / erp_purchase.SourceDyePurApplyDetail | PurApplyMain | 0 | 0 | 待逐项对照 |
| PurApplyMain | PurApplyMain / erp_purchase.SourceDyePurApplyMain | None | 0 | 0 | 待逐项对照 |
| PurDetail | PurDetail / erp_purchase.SourceDyePurDetail | PurMain | 1 | 0 | 待逐项对照 |
| PurGrayIn | GrayIn / erp_warehouse.SourceDyeGrayIn | None | 4 | 2 | 待逐项对照 |
| PurGrayInDetail | GrayInDetail / erp_warehouse.SourceDyeGrayInDetail | PurGrayIn | 3 | 0 | 待逐项对照 |
| PurMain | PurMain / erp_purchase.SourceDyePurMain | None | 0 | 2 | 待逐项对照 |
| PurSemiIn | SemiIn / erp_warehouse.SourceDyeSemiIn | None | 0 | 1 | 待逐项对照 |
| PurSemiInDetail | SemiInDetail / erp_warehouse.SourceDyeSemiInDetail | PurSemiIn | 1 | 0 | 待逐项对照 |
| QC_Record | RecordYield / erp_warehouse.SourceDyeRecordYield | qry_QcWorkList | 5 | 1 | 待逐项对照 |
| QFQC_Record | RecordYield / erp_warehouse.SourceDyeRecordYield | qry_QFQcWorkList | 4 | 1 | 待逐项对照 |
| qry_ArticlePurApplyDetail | PurApplyDetail / erp_purchase.SourceDyePurApplyDetail | None | 0 | 0 | 待逐项对照 |
| qry_ArticlePurApplyQuery | PurDetail / erp_purchase.SourceDyePurDetail | None | 0 | 0 | 待逐项对照 |
| qry_CraftPreCheckJobSheet | JobProcess / erp_production.SourceDyeJobProcess | qry_CraftPreCheckOrder | 0 | 0 | 待逐项对照 |
| qry_DPMachine | p_Machine / erp_base.SourceDyePMachine | None | 0 | 0 | 待逐项对照 |
| qry_DyeRecipeDetail | DyeRecipeDetail / erp_sampling.SourceDyeDyeRecipeDetail |  | 0 | 0 | 待逐项对照 |
| qry_GetOrderAtteToJob | OrderAtte / erp_sales.SourceDyeOrderAtte | qry_GetOrderInfoToJob | 0 | 0 | 待逐项对照 |
| qry_GetOrderColorToJob | OrderColor / erp_sales.SourceDyeOrderColor | qry_GetOrderInfoToJob | 0 | 0 | 待逐项对照 |
| qry_GetOrderInfoToJob | OrderColor / erp_sales.SourceDyeOrderColor |  | 0 | 0 | 待逐项对照 |
| qry_GrayOutTurnToSemiIn | GrayOutDetail / erp_warehouse.SourceDyeGrayOutDetail | None | 0 | 0 | 待逐项对照 |
| qry_JobAssignWaitGrayOut | JobAssign / erp_production.SourceDyeJobAssign | None | 0 | 0 | 待逐项对照 |
| qry_JobAssignWaitSemiOut | JobAssign / erp_production.SourceDyeJobAssign | None | 0 | 0 | 待逐项对照 |
| qry_OriJobAssign | JobAssign / erp_production.SourceDyeJobAssign | qry_OriJobSheet | 0 | 0 | 待逐项对照 |
| qry_OriJobCombineOrder | JobCombineOrder / erp_production.SourceDyeJobCombineOrder | qry_OriJobSheet | 0 | 0 | 待逐项对照 |
| qry_OriJobSheet | JobSheet / erp_production.SourceDyeJobSheet | None | 1 | 0 | 待逐项对照 |
| qry_OriPrintJobAssign | JobAssign / erp_production.SourceDyeJobAssign | qry_OriPrintJobSheet | 0 | 0 | 待逐项对照 |
| qry_OriPrintJobSheet | JobSheet / erp_production.SourceDyeJobSheet | None | 0 | 0 | 待逐项对照 |
| qry_PrintOrder | OrderMain / erp_sales.SourceDyeOrderMain |  | 0 | 1 | 待逐项对照 |
| qry_PrintOrderToPasteDosage | OrderMain / erp_sales.SourceDyeOrderMain |  | 0 | 0 | 待逐项对照 |
| qry_StuffPurApplyDetail | PurApplyDetail / erp_purchase.SourceDyePurApplyDetail | None | 0 | 0 | 待逐项对照 |
| qry_StuffPurApplyQuery | PurDetail / erp_purchase.SourceDyePurDetail | None | 0 | 0 | 待逐项对照 |
| qry_TwiToGrayIn | JobSheet / erp_production.SourceDyeJobSheet | None | 0 | 0 | 待逐项对照 |
| qry_WorkQtyRS | WProcess / erp_production.SourceDyeWProcess | None | 0 | 0 | 待逐项对照 |
| QueryRecord | RecordYield / erp_warehouse.SourceDyeRecordYield | QueryWorkList | 6 | 0 | 待逐项对照 |
| Quote | FixedPrice / erp_sales.SourceDyeFixedPrice | None | 2 | 0 | 待逐项对照 |
| QuoteDetail | FixedPriceDetail / erp_sales.SourceDyeFixedPriceDetail | Quote | 3 | 0 | 待逐项对照 |
| RecordYield | RecordYield / erp_warehouse.SourceDyeRecordYield | None | 0 | 0 | 待逐项对照 |
| RequireClass | p_FieldValid / erp_base.SourceDyePFieldValid | None | 1 | 1 | 待逐项对照 |
| ReworkDyeRecipe | DyeRecipe / erp_sampling.SourceDyeDyeRecipe | None | 0 | 0 | 待逐项对照 |
| ReworkDyeRecipePhaseDetail | DyeRecipePhase / erp_sampling.SourceDyeDyeRecipePhase；连接：erp_sampling.SourceDyeDyeRecipeDetail | ReworkDyeRecipe | 1 | 0 | 待逐项对照 |
| ReworkStuffWeight | StuffWeight / erp_production.SourceDyeStuffWeight | None | 3 | 7 | 待逐项对照 |
| ReworkStuffWeightPhaseDetail | StuffWeightPhase / erp_production.SourceDyeStuffWeightPhase；连接：erp_production.SourceDyeStuffWeightDetail | ReworkStuffWeight | 5 | 0 | 待逐项对照 |
| SaleJobAssign | JobAssign / erp_production.SourceDyeJobAssign | SaleJobSheet | 0 | 0 | 待逐项对照 |
| SaleJobAtte | JobAtte / erp_production.SourceDyeJobAtte | SaleJobSheet | 0 | 0 | 待逐项对照 |
| SaleJobCombine | JobCombine / erp_production.SourceDyeJobCombine | SaleJobSheet | 0 | 0 | 待逐项对照 |
| SaleJobCombineOrder | JobCombineOrder / erp_production.SourceDyeJobCombineOrder | SaleJobSheet | 0 | 0 | 待逐项对照 |
| SaleJobProcess | JobProcess / erp_production.SourceDyeJobProcess | SaleJobSheet | 0 | 0 | 待逐项对照 |
| SaleJobSheet | JobSheet / erp_production.SourceDyeJobSheet | None | 5 | 5 | 待逐项对照 |
| SelfStuffWeight | StuffWeight / erp_production.SourceDyeStuffWeight | None | 2 | 4 | 待逐项对照 |
| SelfStuffWeightPhaseDetail | StuffWeightPhase / erp_production.SourceDyeStuffWeightPhase；连接：erp_production.SourceDyeStuffWeightDetail | SelfStuffWeight | 4 | 0 | 待逐项对照 |
| SemiIn | SemiIn / erp_warehouse.SourceDyeSemiIn | None | 0 | 1 | 待逐项对照 |
| SemiInBack | SemiIn / erp_warehouse.SourceDyeSemiIn | None | 0 | 1 | 待逐项对照 |
| SemiInDetail | SemiInDetail / erp_warehouse.SourceDyeSemiInDetail | SemiIn | 1 | 0 | 待逐项对照 |
| SemiInDetailBack | SemiInDetail / erp_warehouse.SourceDyeSemiInDetail | SemiInBack | 1 | 0 | 待逐项对照 |
| SemiOut | SemiOut / erp_warehouse.SourceDyeSemiOut | None | 0 | 1 | 待逐项对照 |
| SemiOutDetail | SemiOutDetail / erp_warehouse.SourceDyeSemiOutDetail | SemiOut | 1 | 0 | 待逐项对照 |
| SemiOutDetailJob | SemiOutDetail / erp_warehouse.SourceDyeSemiOutDetail | SemiOutJob | 2 | 0 | 待逐项对照 |
| SemiOutDetailTurn | SemiOutDetail / erp_warehouse.SourceDyeSemiOutDetail | SemiOutTurn | 2 | 0 | 待逐项对照 |
| SemiOutJob | SemiOut / erp_warehouse.SourceDyeSemiOut | None | 0 | 1 | 待逐项对照 |
| SemiOutSale | SemiOut / erp_warehouse.SourceDyeSemiOut | None | 0 | 1 | 待逐项对照 |
| SemiOutSaleDetail | SemiOutDetail / erp_warehouse.SourceDyeSemiOutDetail | SemiOutSale | 3 | 0 | 待逐项对照 |
| SemiOutTurn | SemiOut / erp_warehouse.SourceDyeSemiOut | None | 0 | 3 | 待逐项对照 |
| SemiOutWork | SemiOut / erp_warehouse.SourceDyeSemiOut | None | 0 | 1 | 待逐项对照 |
| SemiOutWorkDetail | SemiOutDetail / erp_warehouse.SourceDyeSemiOutDetail | SemiOutWork | 0 | 0 | 待逐项对照 |
| SemiStockAdjust | SemiStockAdjust / erp_warehouse.SourceDyeSemiStockAdjust | None | 0 | 4 | 待逐项对照 |
| SemiStockAdjustDetail | SemiStockAdjustDetail / erp_warehouse.SourceDyeSemiStockAdjustDetail | SemiStockAdjust | 3 | 0 | 待逐项对照 |
| SemiToGrayIn | GrayIn / erp_warehouse.SourceDyeGrayIn | None | 2 | 2 | 待逐项对照 |
| SemiToGrayInDetail | GrayInDetail / erp_warehouse.SourceDyeGrayInDetail | SemiToGrayIn | 2 | 0 | 待逐项对照 |
| ShowDyeLabColor | DyeLabColor / erp_sampling.SourceDyeDyeLabColor | ShowDyeLabMain | 4 | 1 | 待逐项对照 |
| ShowDyeLabMain | DyeLabMain / erp_sampling.SourceDyeDyeLabMain | None | 0 | 1 | 待逐项对照 |
| SmallStuffIn | StuffIn / erp_warehouse.SourceDyeStuffIn | None | 0 | 1 | 待逐项对照 |
| SmallStuffInDetail | StuffInDetail / erp_warehouse.SourceDyeStuffInDetail | SmallStuffIn | 2 | 0 | 待逐项对照 |
| SmallStuffOut | StuffOut / erp_warehouse.SourceDyeStuffOut | None | 0 | 0 | 待逐项对照 |
| SmallStuffOutDetail | StuffOutDetail / erp_warehouse.SourceDyeStuffOutDetail | SmallStuffOut | 1 | 0 | 待逐项对照 |
| StandardDyeRecipe | DyeRecipe / erp_sampling.SourceDyeDyeRecipe | None | 0 | 0 | 待逐项对照 |
| StandardDyeRecipePhaseDetail | DyeRecipePhase / erp_sampling.SourceDyeDyeRecipePhase；连接：erp_sampling.SourceDyeDyeRecipeDetail | StandardDyeRecipe | 1 | 0 | 待逐项对照 |
| StuffAllot | StuffAllot / erp_warehouse.SourceDyeStuffAllot | None | 0 | 0 | 待逐项对照 |
| StuffAllotDetail | StuffAllotDetail / erp_warehouse.SourceDyeStuffAllotDetail | StuffAllot | 1 | 0 | 待逐项对照 |
| StuffIn | StuffIn / erp_warehouse.SourceDyeStuffIn | None | 1 | 4 | 待逐项对照 |
| StuffInDetail | StuffInDetail / erp_warehouse.SourceDyeStuffInDetail | StuffIn | 2 | 0 | 待逐项对照 |
| StuffOut | StuffOut / erp_warehouse.SourceDyeStuffOut | None | 0 | 5 | 待逐项对照 |
| StuffOutDetail | StuffOutDetail / erp_warehouse.SourceDyeStuffOutDetail | StuffOut | 1 | 0 | 待逐项对照 |
| StuffPurApplyDetail | PurApplyDetail / erp_purchase.SourceDyePurApplyDetail | StuffPurApplyMain | 1 | 0 | 待逐项对照 |
| StuffPurApplyMain | PurApplyMain / erp_purchase.SourceDyePurApplyMain | None | 0 | 3 | 待逐项对照 |
| StuffPurDetail | PurDetail / erp_purchase.SourceDyePurDetail | StuffPurMain | 1 | 0 | 待逐项对照 |
| StuffStockAdjust | StuffStockAdjust / erp_warehouse.SourceDyeStuffStockAdjust | None | 0 | 0 | 待逐项对照 |
| StuffStockAdjustDetail | StuffStockAdjustDetail / erp_warehouse.SourceDyeStuffStockAdjustDetail | StuffStockAdjust | 3 | 0 | 待逐项对照 |
| StuffWeight | StuffWeight / erp_production.SourceDyeStuffWeight | None | 1 | 0 | 待逐项对照 |
| StuffWeightDetail | StuffWeightDetail / erp_production.SourceDyeStuffWeightDetail | None | 0 | 0 | 待逐项对照 |
| StuffWeightPhase | StuffWeightPhase / erp_production.SourceDyeStuffWeightPhase | None | 0 | 0 | 待逐项对照 |
| StuffWeightPhaseDetail | StuffWeightPhase / erp_production.SourceDyeStuffWeightPhase；连接：erp_production.SourceDyeStuffWeightDetail | StuffWeight | 2 | 0 | 待逐项对照 |
| SwipeLabelPrint | SwipeLabelPrint / erp_warehouse.SourceDyeSwipeLabelPrint | None | 0 | 0 | 待逐项对照 |
| TrialDyeRecipe | DyeRecipe / erp_sampling.SourceDyeDyeRecipe | None | 1 | 1 | 待逐项对照 |
| TrialDyeRecipePhaseDetail | DyeRecipePhase / erp_sampling.SourceDyeDyeRecipePhase | TrialDyeRecipe | 0 | 0 | 待逐项对照 |
| TrialToBulkRecipe | DyeRecipe / erp_sampling.SourceDyeDyeRecipe | None | 0 | 0 | 待逐项对照 |
| TSGrayOut | GrayOut / erp_warehouse.SourceDyeGrayOut | None | 1 | 3 | 待逐项对照 |
| TSGrayOutDetail | GrayOutDetail / erp_warehouse.SourceDyeGrayOutDetail | TSGrayOut | 3 | 0 | 待逐项对照 |
| TubeWeight | p_FieldValid / erp_base.SourceDyePFieldValid | None | 0 | 0 | 待逐项对照 |
| TubeWeight_QF | p_FieldValid / erp_base.SourceDyePFieldValid | None | 0 | 0 | 待逐项对照 |
| TuiHuoGrayIn | GrayIn / erp_warehouse.SourceDyeGrayIn | None | 4 | 0 | 待逐项对照 |
| TuiHuoGrayInDetail | GrayInDetail / erp_warehouse.SourceDyeGrayInDetail | TuiHuoGrayIn | 2 | 0 | 待逐项对照 |
| TurnSemiIn | SemiIn / erp_warehouse.SourceDyeSemiIn | None | 0 | 0 | 待逐项对照 |
| TurnSemiInDetail | SemiInDetail / erp_warehouse.SourceDyeSemiInDetail | TurnSemiIn | 1 | 0 | 待逐项对照 |
| TwiJobAssign | JobAssign / erp_production.SourceDyeJobAssign | TwiJobSheet | 0 | 0 | 待逐项对照 |
| TwiJobAtte | JobAtte / erp_production.SourceDyeJobAtte | TwiJobSheet | 0 | 0 | 待逐项对照 |
| TwiJobCombine | JobCombine / erp_production.SourceDyeJobCombine | TwiJobSheet | 0 | 0 | 待逐项对照 |
| TwiJobProcess | JobProcess / erp_production.SourceDyeJobProcess | TwiJobSheet | 0 | 0 | 待逐项对照 |
| TwiJobSheet | JobSheet / erp_production.SourceDyeJobSheet | None | 5 | 5 | 待逐项对照 |
| vwProdStockCheck | ProdStockCheck / erp_warehouse.SourceDyeProdStockCheck | None | 0 | 0 | 待逐项对照 |
| WashDyeRecipe | DyeRecipe / erp_sampling.SourceDyeDyeRecipe | None | 0 | 0 | 待逐项对照 |
| WashDyeRecipePhaseDetail | DyeRecipePhase / erp_sampling.SourceDyeDyeRecipePhase；连接：erp_sampling.SourceDyeDyeRecipeDetail | WashDyeRecipe | 1 | 0 | 待逐项对照 |
| WashProcessStuffWeight | StuffWeight / erp_production.SourceDyeStuffWeight | None | 1 | 4 | 待逐项对照 |
| WashProcessStuffWeightPhaseDetail | StuffWeightPhase / erp_production.SourceDyeStuffWeightPhase；连接：erp_production.SourceDyeStuffWeightDetail | WashProcessStuffWeight | 3 | 0 | 待逐项对照 |
| WDefect | WDefect / erp_quality.SourceDyeWDefect | None | 0 | 0 | 待逐项对照 |
| WDefectJudgeBack | WDefect / erp_quality.SourceDyeWDefect | None | 0 | 1 | 待逐项对照 |
| WDefectJudgeInterior | WDefect / erp_quality.SourceDyeWDefect | None | 0 | 1 | 待逐项对照 |
| WDefectJudgeOther | WDefect / erp_quality.SourceDyeWDefect | None | 0 | 0 | 待逐项对照 |
| WDefectOther | WDefect / erp_quality.SourceDyeWDefect | None | 0 | 0 | 待逐项对照 |
| WDefectPayouts | WDefect / erp_quality.SourceDyeWDefect | None | 0 | 0 | 待逐项对照 |
| WDefectRecord | WDefect / erp_quality.SourceDyeWDefect | None | 0 | 0 | 待逐项对照 |
| WeighRecordYield | RecordYield / erp_warehouse.SourceDyeRecordYield | None | 1 | 1 | 待逐项对照 |
| WProcessEdit | WProcess / erp_production.SourceDyeWProcess | None | 0 | 0 | 待逐项对照 |
| YHSys_Type | p_FieldValid / erp_base.SourceDyePFieldValid | None | 0 | 0 | 待逐项对照 |

## 主从办理范围

已登记主从关系集中到source_ownership.py。PurDetail明确允许三种采购表头之一；记录包装到工卡、质量/人员到包装、订单交付申请到订单等独立事实引用不作编辑归属。原外键与归属关系含义不同，不能只因有外键就冻结所有来源单据。

## 仍需补查的入口

未在有效入口快照中登记的业务原表继续在全源表目录中跟踪，不能因没有匹配当前配置而排除。

- dbo.AA：其他或待确认相关表（AA，待确认）；已建模型，入口动作仍需查证。
- dbo.AAA：其他或待确认相关表（AAA，待确认）；已建模型，入口动作仍需查证。
- dbo.AAKC1：其他或待确认相关表（AAKC1，待确认）；已建模型，入口动作仍需查证。
- dbo.ABC：其他或待确认相关表（ABC，待确认）；已建模型，入口动作仍需查证。
- dbo.ADD：其他或待确认相关表（ADD，待确认）；已建模型，入口动作仍需查证。
- dbo.AEE：其他或待确认相关表（AEE，待确认）；已建模型，入口动作仍需查证。
- dbo.BackDyeRecipePhase：染色工艺与配方相关表（BackDyeRecipePhase，待确认）；已建模型，入口动作仍需查证。
- dbo.C：其他或待确认相关表（C，待确认）；已建模型，入口动作仍需查证。
- dbo.cbbz1109：其他或待确认相关表（cbbz1109，待确认）；已建模型，入口动作仍需查证。
- dbo.ckpd20221024：其他或待确认相关表（ckpd20221024，待确认）；已建模型，入口动作仍需查证。
- dbo.ckpd20221024bak：其他或待确认相关表（ckpd20221024bak，待确认）；已建模型，入口动作仍需查证。
- dbo.ckpd20221027：其他或待确认相关表（ckpd20221027，待确认）；已建模型，入口动作仍需查证。
- dbo.cksgz20221024：其他或待确认相关表（cksgz20221024，待确认）；已建模型，入口动作仍需查证。
- dbo.cpdqkc20221024：其他或待确认相关表（cpdqkc20221024，待确认）；已建模型，入口动作仍需查证。
- dbo.DXCHANLIANG：其他或待确认相关表（DXCHANLIANG，待确认）；已建模型，入口动作仍需查证。
- dbo.hypf：其他或待确认相关表（hypf，待确认）；已建模型，入口动作仍需查证。
- dbo.itbak20221120：其他或待确认相关表（itbak20221120，待确认）；已建模型，入口动作仍需查证。
- dbo.itbak20221121：其他或待确认相关表（itbak20221121，待确认）；已建模型，入口动作仍需查证。
- dbo.jxtbzyq：其他或待确认相关表（jxtbzyq，待确认）；已建模型，入口动作仍需查证。
- dbo.jxtkckh：其他或待确认相关表（jxtkckh，待确认）；已建模型，入口动作仍需查证。
- dbo.NHTJ：其他或待确认相关表（NHTJ，待确认）；已建模型，入口动作仍需查证。
- dbo.pbpd20230422：其他或待确认相关表（pbpd20230422，待确认）；已建模型，入口动作仍需查证。
- dbo.prodin1029：坯布半成品成品与仓储相关表（prodin1029，待确认）；已建模型，入口动作仍需查证。
- dbo.PS20221218：其他或待确认相关表（PS20221218，待确认）；已建模型，入口动作仍需查证。
- dbo.ransechugangtongji：其他或待确认相关表（ransechugangtongji，待确认）；已建模型，入口动作仍需查证。
- dbo.ransetongji：其他或待确认相关表（ransetongji，待确认）；已建模型，入口动作仍需查证。
- dbo.RCDDZJB：其他或待确认相关表（RCDDZJB，待确认）；已建模型，入口动作仍需查证。
- dbo.shda：其他或待确认相关表（shda，待确认）；已建模型，入口动作仍需查证。
- dbo.SHIFT：生产工单与排程相关表（SHIFT，待确认）；已建模型，入口动作仍需查证。
- dbo.SHLEIXING：其他或待确认相关表（SHLEIXING，待确认）；已建模型，入口动作仍需查证。
- dbo.tmp20221104：其他或待确认相关表（tmp20221104，待确认）；已建模型，入口动作仍需查证。
- dbo.xxtcbkc20221023：其他或待确认相关表（xxtcbkc20221023，待确认）；已建模型，入口动作仍需查证。
- dbo.xxtzzp20221024：其他或待确认相关表（xxtzzp20221024，待确认）；已建模型，入口动作仍需查证。
- dbo.zhenzhibaobiao：其他或待确认相关表（zhenzhibaobiao，待确认）；已建模型，入口动作仍需查证。
- dbo.ZJHXMXBB：其他或待确认相关表（ZJHXMXBB，待确认）；已建模型，入口动作仍需查证。
- dye.A_ProdRecord：坯布半成品成品与仓储相关表（A_ProdRecord，待确认）；已建模型，入口动作仍需查证。
- dye.ACGroup：其他或待确认相关表（ACGroup，待确认）；已建模型，入口动作仍需查证。
- dye.acholiday：其他或待确认相关表（acholiday，待确认）；已建模型，入口动作仍需查证。
- dye.ACUnlockComb：其他或待确认相关表（ACUnlockComb，待确认）；已建模型，入口动作仍需查证。
- dye.AddDyeWProcessStep：染色工艺与配方相关表（AddDyeWProcessStep，待确认）；已建模型，入口动作仍需查证。
- dye.APPUploadFilesInfo：其他或待确认相关表（APPUploadFilesInfo，待确认）；已建模型，入口动作仍需查证。
- dye.APPUploadFilesInfoDel：其他或待确认相关表（APPUploadFilesInfoDel，待确认）；已建模型，入口动作仍需查证。
- dye.ArrivalNotice：其他或待确认相关表（ArrivalNotice，待确认）；已建模型，入口动作仍需查证。
- dye.ArrivalNoticeDetail：其他或待确认相关表（ArrivalNoticeDetail，待确认）；已建模型，入口动作仍需查证。
- dye.ArticleDeptApply：其他或待确认相关表（ArticleDeptApply，待确认）；已建模型，入口动作仍需查证。
- dye.ArticleDeptApplyDetail：其他或待确认相关表（ArticleDeptApplyDetail，待确认）；已建模型，入口动作仍需查证。
- dye.ArticleOutApply：其他或待确认相关表（ArticleOutApply，待确认）；已建模型，入口动作仍需查证。
- dye.ArticleOutApplyDetail：其他或待确认相关表（ArticleOutApplyDetail，待确认）；已建模型，入口动作仍需查证。
- dye.ArticlePurDetail：其他或待确认相关表（ArticlePurDetail，待确认）；已建模型，入口动作仍需查证。
- dye.ArticlePurMain：其他或待确认相关表（ArticlePurMain，待确认）；已建模型，入口动作仍需查证。
- dye.ArticleStock：坯布半成品成品与仓储相关表（ArticleStock，待确认）；已建模型，入口动作仍需查证。
- dye.ArticleStockAdjust：坯布半成品成品与仓储相关表（ArticleStockAdjust，待确认）；已建模型，入口动作仍需查证。
- dye.ArticleStockAdjustDetail：坯布半成品成品与仓储相关表（ArticleStockAdjustDetail，待确认）；已建模型，入口动作仍需查证。
- dye.ArticleStockBook：辅料库存流水；已建模型，入口动作仍需查证。
- dye.Attachment：其他或待确认相关表（Attachment，待确认）；已建模型，入口动作仍需查证。
- dye.AttParam：系统平台与配置相关表（AttParam，待确认）；已建模型，入口动作仍需查证。
- dye.AuditedExc：其他或待确认相关表（AuditedExc，待确认）；已建模型，入口动作仍需查证。
- dye.AUTHDEVICE：设备维护与能耗相关表（AUTHDEVICE，待确认）；已建模型，入口动作仍需查证。
- dye.BalancingConditions：其他或待确认相关表（BalancingConditions，待确认）；已建模型，入口动作仍需查证。
- dye.BaseCase：其他或待确认相关表（BaseCase，待确认）；已建模型，入口动作仍需查证。
- dye.BaseCaseDetail：其他或待确认相关表（BaseCaseDetail，待确认）；已建模型，入口动作仍需查证。
- dye.Biotemplate：基础主数据相关表（Biotemplate，待确认）；已建模型，入口动作仍需查证。
- dye.CarryMaterial：染化料与称料库存相关表（CarryMaterial，待确认）；已建模型，入口动作仍需查证。
- dye.CarryMaterialDetail：染化料与称料库存相关表（CarryMaterialDetail，待确认）；已建模型，入口动作仍需查证。
- dye.CHECKEXACT：质量检验与异常相关表（CHECKEXACT，待确认）；已建模型，入口动作仍需查证。
- dye.CHECKINOUT：质量检验与异常相关表（CHECKINOUT，待确认）；已建模型，入口动作仍需查证。
- dye.ClockShift：生产工单与排程相关表（ClockShift，待确认）；已建模型，入口动作仍需查证。
- dye.ColorCard：染色工艺与配方相关表（ColorCard，待确认）；已建模型，入口动作仍需查证。
- dye.ColorCardDetail：染色工艺与配方相关表（ColorCardDetail，待确认）；已建模型，入口动作仍需查证。
- dye.ColorCardFlow：系统平台与配置相关表（ColorCardFlow，待确认）；已建模型，入口动作仍需查证。
- dye.ColorChangeRisk：染色工艺与配方相关表（ColorChangeRisk，待确认）；已建模型，入口动作仍需查证。
- dye.ColoringCheck：质量检验与异常相关表（ColoringCheck，待确认）；已建模型，入口动作仍需查证。
- dye.ColorShiftEmp：染色工艺与配方相关表（ColorShiftEmp，待确认）；已建模型，入口动作仍需查证。
- dye.compensatedetail：其他或待确认相关表（compensatedetail，待确认）；已建模型，入口动作仍需查证。
- dye.compensatemain：其他或待确认相关表（compensatemain，待确认）；已建模型，入口动作仍需查证。
- dye.CookIn：其他或待确认相关表（CookIn，待确认）；已建模型，入口动作仍需查证。
- dye.CookInDetail：坯布半成品成品与仓储相关表（CookInDetail，待确认）；已建模型，入口动作仍需查证。
- dye.CptLabRecipe：染色工艺与配方相关表（CptLabRecipe，待确认）；已建模型，入口动作仍需查证。
- dye.CptLabRecipeDetail：染色工艺与配方相关表（CptLabRecipeDetail，待确认）；已建模型，入口动作仍需查证。
- dye.Cur_Smp_PrescriptEntry：其他或待确认相关表（Cur_Smp_PrescriptEntry，待确认）；已建模型，入口动作仍需查证。
- dye.CusAddPrice：财务结算与成本相关表（CusAddPrice，待确认）；已建模型，入口动作仍需查证。
- dye.CusAddPriceDetail：财务结算与成本相关表（CusAddPriceDetail，待确认）；已建模型，入口动作仍需查证。
- dye.CusBasicsPrice：财务结算与成本相关表（CusBasicsPrice，待确认）；已建模型，入口动作仍需查证。
- dye.CusBasicsPriceDetail：财务结算与成本相关表（CusBasicsPriceDetail，待确认）；已建模型，入口动作仍需查证。
- dye.CusExtraCharge：其他或待确认相关表（CusExtraCharge，待确认）；已建模型，入口动作仍需查证。
- dye.CustomerNoLimit：客户订单与销售相关表（CustomerNoLimit，待确认）；已建模型，入口动作仍需查证。
- dye.DefectiveIn：质量检验与异常相关表（DefectiveIn，待确认）；已建模型，入口动作仍需查证。
- dye.DefectiveInDetail：质量检验与异常相关表（DefectiveInDetail，待确认）；已建模型，入口动作仍需查证。
- dye.DefectiveInRecord：质量检验与异常相关表（DefectiveInRecord，待确认）；已建模型，入口动作仍需查证。
- dye.DefectiveOut：质量检验与异常相关表（DefectiveOut，待确认）；已建模型，入口动作仍需查证。
- dye.DefectiveOutDetail：质量检验与异常相关表（DefectiveOutDetail，待确认）；已建模型，入口动作仍需查证。
- dye.DefectiveOutRecord：质量检验与异常相关表（DefectiveOutRecord，待确认）；已建模型，入口动作仍需查证。
- dye.DEPARTMENTS：其他或待确认相关表（DEPARTMENTS，待确认）；已建模型，入口动作仍需查证。
- dye.DeptUsedSchs：其他或待确认相关表（DeptUsedSchs，待确认）；已建模型，入口动作仍需查证。
- dye.DP_WorkQty：生产工单与排程相关表（DP_WorkQty，待确认）；已建模型，入口动作仍需查证。
- dye.DyeCheck：质量检验与异常相关表（DyeCheck，待确认）；已建模型，入口动作仍需查证。
- dye.dyeCheckout：财务结算与成本相关表（dyeCheckout，待确认）；已建模型，入口动作仍需查证。
- dye.DyeColor：染色工艺与配方相关表（DyeColor，待确认）；已建模型，入口动作仍需查证。
- dye.DyeDipsRecordDetail：染色工艺与配方相关表（DyeDipsRecordDetail，待确认）；已建模型，入口动作仍需查证。
- dye.DyeDipsRecordEmp：染色工艺与配方相关表（DyeDipsRecordEmp，待确认）；已建模型，入口动作仍需查证。
- dye.DyeDipsRecordNote：染色工艺与配方相关表（DyeDipsRecordNote，待确认）；已建模型，入口动作仍需查证。
- dye.DyeDipsRecordPhase：染色工艺与配方相关表（DyeDipsRecordPhase，待确认）；已建模型，入口动作仍需查证。
- dye.DyeLabAtte：染色工艺与配方相关表（DyeLabAtte，待确认）；已建模型，入口动作仍需查证。
- dye.DyeLabColorRecord：染色工艺与配方相关表（DyeLabColorRecord，待确认）；已建模型，入口动作仍需查证。
- dye.DyeProcessPrice：财务结算与成本相关表（DyeProcessPrice，待确认）；已建模型，入口动作仍需查证。
- dye.DyeProduceItem：染色工艺与配方相关表（DyeProduceItem，待确认）；已建模型，入口动作仍需查证。
- dye.DyeRecipeJob：染色工艺与配方相关表（DyeRecipeJob，待确认）；已建模型，入口动作仍需查证。
- dye.DyeReprint：染色工艺与配方相关表（DyeReprint，待确认）；已建模型，入口动作仍需查证。
- dye.DyeStartDateTime：染色工艺与配方相关表（DyeStartDateTime，待确认）；已建模型，入口动作仍需查证。
- dye.DyeStuffOut：染化料与称料库存相关表（DyeStuffOut，待确认）；已建模型，入口动作仍需查证。
- dye.DyeStuffOutDetail：染化料与称料库存相关表（DyeStuffOutDetail，待确认）；已建模型，入口动作仍需查证。
- dye.e_Energy_day：设备维护与能耗相关表（e_Energy_day，待确认）；已建模型，入口动作仍需查证。
- dye.e_YardMeterGether：设备维护与能耗相关表（e_YardMeterGether，待确认）；已建模型，入口动作仍需查证。
- dye.Emp_Room：基础主数据相关表（Emp_Room，待确认）；已建模型，入口动作仍需查证。
- dye.EmpShiftClock：生产工单与排程相关表（EmpShiftClock，待确认）；已建模型，入口动作仍需查证。
- dye.EnableCard：其他或待确认相关表（EnableCard，待确认）；已建模型，入口动作仍需查证。
- dye.EnergyConsumption：设备维护与能耗相关表（EnergyConsumption，待确认）；已建模型，入口动作仍需查证。
- dye.EnergyConsumptionDetail：设备维护与能耗相关表（EnergyConsumptionDetail，待确认）；已建模型，入口动作仍需查证。
- dye.EnergyRecords：设备维护与能耗相关表（EnergyRecords，待确认）；已建模型，入口动作仍需查证。
- dye.EXCNOTES：其他或待确认相关表（EXCNOTES，待确认）；已建模型，入口动作仍需查证。
- dye.FabricPurDetail：坯布半成品成品与仓储相关表（FabricPurDetail，待确认）；已建模型，入口动作仍需查证。
- dye.FabricPurMain：坯布半成品成品与仓储相关表（FabricPurMain，待确认）；已建模型，入口动作仍需查证。
- dye.FaceTemp：基础主数据相关表（FaceTemp，待确认）；已建模型，入口动作仍需查证。
- dye.FeelOfferDetail：其他或待确认相关表（FeelOfferDetail，待确认）；已建模型，入口动作仍需查证。
- dye.FeelOfferMain：其他或待确认相关表（FeelOfferMain，待确认）；已建模型，入口动作仍需查证。
- dye.FixedCanDetail：其他或待确认相关表（FixedCanDetail，待确认）；已建模型，入口动作仍需查证。
- dye.FixedCanRecord：其他或待确认相关表（FixedCanRecord，待确认）；已建模型，入口动作仍需查证。
- dye.FixedPriceAtte：财务结算与成本相关表（FixedPriceAtte，待确认）；已建模型，入口动作仍需查证。
- dye.FixedPriceProcess：财务结算与成本相关表（FixedPriceProcess，待确认）；已建模型，入口动作仍需查证。
- dye.GetClothNotice：坯布半成品成品与仓储相关表（GetClothNotice，待确认）；已建模型，入口动作仍需查证。
- dye.GetClothNoticeDetail：坯布半成品成品与仓储相关表（GetClothNoticeDetail，待确认）；已建模型，入口动作仍需查证。
- dye.GetJobSheetReceive：财务结算与成本相关表（GetJobSheetReceive，待确认）；已建模型，入口动作仍需查证。
- dye.GrayBalance：财务结算与成本相关表（GrayBalance，待确认）；已建模型，入口动作仍需查证。
- dye.GrayBalanceDetail：财务结算与成本相关表（GrayBalanceDetail，待确认）；已建模型，入口动作仍需查证。
- dye.GrayInDefect：质量检验与异常相关表（GrayInDefect，待确认）；已建模型，入口动作仍需查证。
- dye.GrayInRecord：坯布半成品成品与仓储相关表（GrayInRecord，待确认）；已建模型，入口动作仍需查证。
- dye.GrayOutRecord：坯布半成品成品与仓储相关表（GrayOutRecord，待确认）；已建模型，入口动作仍需查证。
- dye.GrayPostionUp：坯布半成品成品与仓储相关表（GrayPostionUp，待确认）；已建模型，入口动作仍需查证。
- dye.GrayRecord：坯布半成品成品与仓储相关表（GrayRecord，待确认）；已建模型，入口动作仍需查证。
- dye.GrayRecordCutLogs：坯布半成品成品与仓储相关表（GrayRecordCutLogs，待确认）；已建模型，入口动作仍需查证。
- dye.GrayReturnApply：坯布半成品成品与仓储相关表（GrayReturnApply，待确认）；已建模型，入口动作仍需查证。
- dye.GrayReturnApplyDetail：坯布半成品成品与仓储相关表（GrayReturnApplyDetail，待确认）；已建模型，入口动作仍需查证。
- dye.GrayStock：坯布半成品成品与仓储相关表（GrayStock，待确认）；已建模型，入口动作仍需查证。
- dye.GrayStockAdjustDetail：坯布半成品成品与仓储相关表（GrayStockAdjustDetail，待确认）；已建模型，入口动作仍需查证。
- dye.GrayStockBook：坯布库存流水；已建模型，入口动作仍需查证。
- dye.GrayStockSpecUp：坯布半成品成品与仓储相关表（GrayStockSpecUp，待确认）；已建模型，入口动作仍需查证。
- dye.GrayStockSpecUpDetail：坯布半成品成品与仓储相关表（GrayStockSpecUpDetail，待确认）；已建模型，入口动作仍需查证。
- dye.GrayStorageAdjust：坯布半成品成品与仓储相关表（GrayStorageAdjust，待确认）；已建模型，入口动作仍需查证。
- dye.GrayStorageAdjustDetail：坯布半成品成品与仓储相关表（GrayStorageAdjustDetail，待确认）；已建模型，入口动作仍需查证。
- dye.GrayStorageAdjustRecord：坯布半成品成品与仓储相关表（GrayStorageAdjustRecord，待确认）；已建模型，入口动作仍需查证。
- dye.GWName：其他或待确认相关表（GWName，待确认）；已建模型，入口动作仍需查证。
- dye.h_Contract：客户订单与销售相关表（h_Contract，待确认）；已建模型，入口动作仍需查证。
- dye.h_EmpAppNotice：基础主数据相关表（h_EmpAppNotice，待确认）；已建模型，入口动作仍需查证。
- dye.h_EmpDeptPerm：基础主数据相关表（h_EmpDeptPerm，待确认）；已建模型，入口动作仍需查证。
- dye.h_Employee2：基础主数据相关表（h_Employee2，待确认）；已建模型，入口动作仍需查证。
- dye.h_EmployeeIORecord：基础主数据相关表（h_EmployeeIORecord，待确认）；已建模型，入口动作仍需查证。
- dye.h_EmpRole：员工角色；已建模型，入口动作仍需查证。
- dye.h_Leave：基础主数据相关表（h_Leave，待确认）；已建模型，入口动作仍需查证。
- dye.h_PositionChange：基础主数据相关表（h_PositionChange，待确认）；已建模型，入口动作仍需查证。
- dye.h_RewardPunish：基础主数据相关表（h_RewardPunish，待确认）；已建模型，入口动作仍需查证。
- dye.HOLIDAYS：其他或待确认相关表（HOLIDAYS，待确认）；已建模型，入口动作仍需查证。
- dye.HS_JobsheetNo：生产工单与排程相关表（HS_JobsheetNo，待确认）；已建模型，入口动作仍需查证。
- dye.Human：其他或待确认相关表（Human，待确认）；已建模型，入口动作仍需查证。
- dye.InspectionLog：质量检验与异常相关表（InspectionLog，待确认）；已建模型，入口动作仍需查证。
- dye.InspectionLogDetail：质量检验与异常相关表（InspectionLogDetail，待确认）；已建模型，入口动作仍需查证。
- dye.InspectionProject：质量检验与异常相关表（InspectionProject，待确认）；已建模型，入口动作仍需查证。
- dye.ITMANAGE：其他或待确认相关表（ITMANAGE，待确认）；已建模型，入口动作仍需查证。
- dye.JingShaRegister：其他或待确认相关表（JingShaRegister，待确认）；已建模型，入口动作仍需查证。
- dye.JingShaRegisterDetail：其他或待确认相关表（JingShaRegisterDetail，待确认）；已建模型，入口动作仍需查证。
- dye.JobColor：染色工艺与配方相关表（JobColor，待确认）；已建模型，入口动作仍需查证。
- dye.JobExceptions：生产工单与排程相关表（JobExceptions，待确认）；已建模型，入口动作仍需查证。
- dye.JobGrayRecord：坯布半成品成品与仓储相关表（JobGrayRecord，待确认）；已建模型，入口动作仍需查证。
- dye.JobInWareEdit：生产工单与排程相关表（JobInWareEdit，待确认）；已建模型，入口动作仍需查证。
- dye.JobMain：生产工单与排程相关表（JobMain，待确认）；已建模型，入口动作仍需查证。
- dye.JobOutWareEdit：生产工单与排程相关表（JobOutWareEdit，待确认）；已建模型，入口动作仍需查证。
- dye.JobPreRegist：生产工单与排程相关表（JobPreRegist，待确认）；已建模型，入口动作仍需查证。
- dye.JobProcessPre：染色工艺与配方相关表（JobProcessPre，待确认）；已建模型，入口动作仍需查证。
- dye.JobSheetMasrkCar：生产工单与排程相关表（JobSheetMasrkCar，待确认）；已建模型，入口动作仍需查证。
- dye.JobSheetNoRushOrder：生产工单与排程相关表（JobSheetNoRushOrder，待确认）；已建模型，入口动作仍需查证。
- dye.JobSheetOther：生产工单与排程相关表（JobSheetOther，待确认）；已建模型，入口动作仍需查证。
- dye.JobSheetReceive：工卡接收/结算记录；已建模型，入口动作仍需查证。
- dye.JobSheetRegister：生产工单与排程相关表（JobSheetRegister，待确认）；已建模型，入口动作仍需查证。
- dye.JobSheetSchedule：生产工单与排程相关表（JobSheetSchedule，待确认）；已建模型，入口动作仍需查证。
- dye.JobShiftEmpBak：生产工单与排程相关表（JobShiftEmpBak，待确认）；已建模型，入口动作仍需查证。
- dye.JobStartRollNo：生产工单与排程相关表（JobStartRollNo，待确认）；已建模型，入口动作仍需查证。
- dye.KindLimit：其他或待确认相关表（KindLimit，待确认）；已建模型，入口动作仍需查证。
- dye.KQ：其他或待确认相关表（KQ，待确认）；已建模型，入口动作仍需查证。
- dye.KQ_Query：其他或待确认相关表（KQ_Query，待确认）；已建模型，入口动作仍需查证。
- dye.LabDips：染色工艺与配方相关表（LabDips，待确认）；已建模型，入口动作仍需查证。
- dye.LeaveClass：其他或待确认相关表（LeaveClass，待确认）；已建模型，入口动作仍需查证。
- dye.LeaveClass1：其他或待确认相关表（LeaveClass1，待确认）；已建模型，入口动作仍需查证。
- dye.Limit：其他或待确认相关表（Limit，待确认）；已建模型，入口动作仍需查证。
- dye.LossBill：其他或待确认相关表（LossBill，待确认）；已建模型，入口动作仍需查证。
- dye.MachineCarePlan：设备维护与能耗相关表（MachineCarePlan，待确认）；已建模型，入口动作仍需查证。
- dye.MachineCarePlanDetail：设备维护与能耗相关表（MachineCarePlanDetail，待确认）；已建模型，入口动作仍需查证。
- dye.MachineCareProject：设备维护与能耗相关表（MachineCareProject，待确认）；已建模型，入口动作仍需查证。
- dye.MachineCareRecords：设备维护与能耗相关表（MachineCareRecords，待确认）；已建模型，入口动作仍需查证。
- dye.MachineCase：设备维护与能耗相关表（MachineCase，待确认）；已建模型，入口动作仍需查证。
- dye.MachineCaseDetail：设备维护与能耗相关表（MachineCaseDetail，待确认）；已建模型，入口动作仍需查证。
- dye.MachineCaseProject：设备维护与能耗相关表（MachineCaseProject，待确认）；已建模型，入口动作仍需查证。
- dye.MachineFault：设备维护与能耗相关表（MachineFault，待确认）；已建模型，入口动作仍需查证。
- dye.MachineFaultArticleInfo：设备维护与能耗相关表（MachineFaultArticleInfo，待确认）；已建模型，入口动作仍需查证。
- dye.MachineFaultComment：设备维护与能耗相关表（MachineFaultComment，待确认）；已建模型，入口动作仍需查证。
- dye.MachineFaultFilter：设备维护与能耗相关表（MachineFaultFilter，待确认）；已建模型，入口动作仍需查证。
- dye.MachineFaultRecord：设备维护与能耗相关表（MachineFaultRecord，待确认）；已建模型，入口动作仍需查证。
- dye.Machines：设备维护与能耗相关表（Machines，待确认）；已建模型，入口动作仍需查证。
- dye.MaterialPriceAdjust：财务结算与成本相关表（MaterialPriceAdjust，待确认）；已建模型，入口动作仍需查证。
- dye.MaterialPriceAdjustDetail：财务结算与成本相关表（MaterialPriceAdjustDetail，待确认）；已建模型，入口动作仍需查证。
- dye.MoveShiftBill：生产工单与排程相关表（MoveShiftBill，待确认）；已建模型，入口动作仍需查证。
- dye.NoLimit：其他或待确认相关表（NoLimit，待确认）；已建模型，入口动作仍需查证。
- dye.NUM_RUN：其他或待确认相关表（NUM_RUN，待确认）；已建模型，入口动作仍需查证。
- dye.NUM_RUN_DEIL：其他或待确认相关表（NUM_RUN_DEIL，待确认）；已建模型，入口动作仍需查证。
- dye.ODMIn：其他或待确认相关表（ODMIn，待确认）；已建模型，入口动作仍需查证。
- dye.ODMInDetail：坯布半成品成品与仓储相关表（ODMInDetail，待确认）；已建模型，入口动作仍需查证。
- dye.ODMInRecord：其他或待确认相关表（ODMInRecord，待确认）；已建模型，入口动作仍需查证。
- dye.ODMOut：其他或待确认相关表（ODMOut，待确认）；已建模型，入口动作仍需查证。
- dye.ODMOutDetail：坯布半成品成品与仓储相关表（ODMOutDetail，待确认）；已建模型，入口动作仍需查证。
- dye.ODMOutRecord：其他或待确认相关表（ODMOutRecord，待确认）；已建模型，入口动作仍需查证。
- dye.OrderAssign：客户订单与销售相关表（OrderAssign，待确认）；已建模型，入口动作仍需查证。
- dye.OrderAssign2：客户订单与销售相关表（OrderAssign2，待确认）；已建模型，入口动作仍需查证。
- dye.OrderCombine：客户订单与销售相关表（OrderCombine，待确认）；已建模型，入口动作仍需查证。
- dye.OrderDlvApply：客户订单与销售相关表（OrderDlvApply，待确认）；已建模型，入口动作仍需查证。
- dye.OrderDlvApplyLock：客户订单与销售相关表（OrderDlvApplyLock，待确认）；已建模型，入口动作仍需查证。
- dye.OrderDlvApplySheet：客户订单与销售相关表（OrderDlvApplySheet，待确认）；已建模型，入口动作仍需查证。
- dye.OrderFee：客户订单与销售相关表（OrderFee，待确认）；已建模型，入口动作仍需查证。
- dye.OrderInfo：客户订单与销售相关表（OrderInfo，待确认）；已建模型，入口动作仍需查证。
- dye.OrderInfoProcess：染色工艺与配方相关表（OrderInfoProcess，待确认）；已建模型，入口动作仍需查证。
- dye.OrderPriceProcess：财务结算与成本相关表（OrderPriceProcess，待确认）；已建模型，入口动作仍需查证。
- dye.OrderProcess：染色工艺与配方相关表（OrderProcess，待确认）；已建模型，入口动作仍需查证。
- dye.OrderProcessPre：染色工艺与配方相关表（OrderProcessPre，待确认）；已建模型，入口动作仍需查证。
- dye.OtherIn：其他或待确认相关表（OtherIn，待确认）；已建模型，入口动作仍需查证。
- dye.OtherInDetail：坯布半成品成品与仓储相关表（OtherInDetail，待确认）；已建模型，入口动作仍需查证。
- dye.OutGoingBill：其他或待确认相关表（OutGoingBill，待确认）；已建模型，入口动作仍需查证。
- dye.OutGoingBillDetail：其他或待确认相关表（OutGoingBillDetail，待确认）；已建模型，入口动作仍需查证。
- dye.OutPlan：生产工单与排程相关表（OutPlan，待确认）；已建模型，入口动作仍需查证。
- dye.OutPlanDetail：生产工单与排程相关表（OutPlanDetail，待确认）；已建模型，入口动作仍需查证。
- dye.OutWorkApply：生产工单与排程相关表（OutWorkApply，待确认）；已建模型，入口动作仍需查证。
- dye.OutWorkApplyDetail：生产工单与排程相关表（OutWorkApplyDetail，待确认）；已建模型，入口动作仍需查证。
- dye.p_ArticleStorageUnitID：辅料仓位对照；已建模型，入口动作仍需查证。
- dye.p_AtteSub：生产工单与排程相关表（p_AtteSub，待确认）；已建模型，入口动作仍需查证。
- dye.p_AtteType：生产工单与排程相关表（p_AtteType，待确认）；已建模型，入口动作仍需查证。
- dye.p_AuxRule：基础主数据相关表（p_AuxRule，待确认）；已建模型，入口动作仍需查证。
- dye.p_AuxRuleDetail：基础主数据相关表（p_AuxRuleDetail，待确认）；已建模型，入口动作仍需查证。
- dye.p_BalanceType：财务结算与成本相关表（p_BalanceType，待确认）；已建模型，入口动作仍需查证。
- dye.P_ColorNum：色号与样品；已建模型，入口动作仍需查证。
- dye.p_CommissionRatio：基础主数据相关表（p_CommissionRatio，待确认）；已建模型，入口动作仍需查证。
- dye.p_CommMethod：基础主数据相关表（p_CommMethod，待确认）；已建模型，入口动作仍需查证。
- dye.p_CommModule：基础主数据相关表（p_CommModule，待确认）；已建模型，入口动作仍需查证。
- dye.p_CommPort：基础主数据相关表（p_CommPort，待确认）；已建模型，入口动作仍需查证。
- dye.p_Cook：基础主数据相关表（p_Cook，待确认）；已建模型，入口动作仍需查证。
- dye.p_CraftParam：系统平台与配置相关表（p_CraftParam，待确认）；已建模型，入口动作仍需查证。
- dye.p_CraftPParam：系统平台与配置相关表（p_CraftPParam，待确认）；已建模型，入口动作仍需查证。
- dye.p_CustAddress：客户订单与销售相关表（p_CustAddress，待确认）；已建模型，入口动作仍需查证。
- dye.p_CustCategory：客户订单与销售相关表（p_CustCategory，待确认）；已建模型，入口动作仍需查证。
- dye.p_CustLinker：客户订单与销售相关表（p_CustLinker，待确认）；已建模型，入口动作仍需查证。
- dye.p_CustRelation：客户订单与销售相关表（p_CustRelation，待确认）；已建模型，入口动作仍需查证。
- dye.p_Dept：部门；已建模型，入口动作仍需查证。
- dye.p_DyeProgram：染色工艺与配方相关表（p_DyeProgram，待确认）；已建模型，入口动作仍需查证。
- dye.p_DyeProgramDetail：染色工艺与配方相关表（p_DyeProgramDetail，待确认）；已建模型，入口动作仍需查证。
- dye.p_Fabric：坯布半成品成品与仓储相关表（p_Fabric，待确认）；已建模型，入口动作仍需查证。
- dye.p_Fabric_Fact：坯布半成品成品与仓储相关表（p_Fabric_Fact，待确认）；已建模型，入口动作仍需查证。
- dye.p_Fabric_Other：坯布半成品成品与仓储相关表（p_Fabric_Other，待确认）；已建模型，入口动作仍需查证。
- dye.p_FeelCode：基础主数据相关表（p_FeelCode，待确认）；已建模型，入口动作仍需查证。
- dye.p_FieldMemo：基础主数据相关表（p_FieldMemo，待确认）；已建模型，入口动作仍需查证。
- dye.p_FieldValidSub：基础主数据相关表（p_FieldValidSub，待确认）；已建模型，入口动作仍需查证。
- dye.p_FieldValidSubCust：客户订单与销售相关表（p_FieldValidSubCust，待确认）；已建模型，入口动作仍需查证。
- dye.p_GrayBak：坯布半成品成品与仓储相关表（p_GrayBak，待确认）；已建模型，入口动作仍需查证。
- dye.p_ITOnRest：基础主数据相关表（p_ITOnRest，待确认）；已建模型，入口动作仍需查证。
- dye.p_ITWatch：基础主数据相关表（p_ITWatch，待确认）；已建模型，入口动作仍需查证。
- dye.p_Lable：染色工艺与配方相关表（p_Lable，待确认）；已建模型，入口动作仍需查证。
- dye.p_MachineColor：设备维护与能耗相关表（p_MachineColor，待确认）；已建模型，入口动作仍需查证。
- dye.p_MachineFaultClass：设备维护与能耗相关表（p_MachineFaultClass，待确认）；已建模型，入口动作仍需查证。
- dye.p_MachineFaultStatus：设备维护与能耗相关表（p_MachineFaultStatus，待确认）；已建模型，入口动作仍需查证。
- dye.p_MachinePart：设备维护与能耗相关表（p_MachinePart，待确认）；已建模型，入口动作仍需查证。
- dye.p_MachinePoint：设备维护与能耗相关表（p_MachinePoint，待确认）；已建模型，入口动作仍需查证。
- dye.p_MachinePort：设备维护与能耗相关表（p_MachinePort，待确认）；已建模型，入口动作仍需查证。
- dye.p_MachineProcess：设备维护与能耗相关表（p_MachineProcess，待确认）；已建模型，入口动作仍需查证。
- dye.p_MachineProd：设备维护与能耗相关表（p_MachineProd，待确认）；已建模型，入口动作仍需查证。
- dye.p_MachineShift：设备维护与能耗相关表（p_MachineShift，待确认）；已建模型，入口动作仍需查证。
- dye.p_Meter：设备维护与能耗相关表（p_Meter，待确认）；已建模型，入口动作仍需查证。
- dye.p_MeterAlarm：设备维护与能耗相关表（p_MeterAlarm，待确认）；已建模型，入口动作仍需查证。
- dye.p_MeterMachine：设备维护与能耗相关表（p_MeterMachine，待确认）；已建模型，入口动作仍需查证。
- dye.p_PDesign：基础主数据相关表（p_PDesign，待确认）；已建模型，入口动作仍需查证。
- dye.p_PDesignDetail：基础主数据相关表（p_PDesignDetail，待确认）；已建模型，入口动作仍需查证。
- dye.p_PDesignSet：基础主数据相关表（p_PDesignSet，待确认）；已建模型，入口动作仍需查证。
- dye.p_PriceList：价格表；已建模型，入口动作仍需查证。
- dye.p_PriceListAtte：财务结算与成本相关表（p_PriceListAtte，待确认）；已建模型，入口动作仍需查证。
- dye.p_PriceListColor：色号价格表；已建模型，入口动作仍需查证。
- dye.p_PriceListProcess：工序价格表；已建模型，入口动作仍需查证。
- dye.p_PriceListVat：财务结算与成本相关表（p_PriceListVat，待确认）；已建模型，入口动作仍需查证。
- dye.p_ProcessArea：染色工艺与配方相关表（p_ProcessArea，待确认）；已建模型，入口动作仍需查证。
- dye.p_ProcessChemical：染化料与称料库存相关表（p_ProcessChemical，待确认）；已建模型，入口动作仍需查证。
- dye.p_ProcessCraft：染色工艺与配方相关表（p_ProcessCraft，待确认）；已建模型，入口动作仍需查证。
- dye.p_ProcessCraft1：染色工艺与配方相关表（p_ProcessCraft1，待确认）；已建模型，入口动作仍需查证。
- dye.p_ProcessDefect：质量检验与异常相关表（p_ProcessDefect，待确认）；已建模型，入口动作仍需查证。
- dye.p_ProcessPCraft：染色工艺与配方相关表（p_ProcessPCraft，待确认）；已建模型，入口动作仍需查证。
- dye.p_ProcessPrice：财务结算与成本相关表（p_ProcessPrice，待确认）；已建模型，入口动作仍需查证。
- dye.p_Product：坯布半成品成品与仓储相关表（p_Product，待确认）；已建模型，入口动作仍需查证。
- dye.p_ShiftArrange：生产工单与排程相关表（p_ShiftArrange，待确认）；已建模型，入口动作仍需查证。
- dye.p_ShiftArrangeDetail：生产工单与排程相关表（p_ShiftArrangeDetail，待确认）；已建模型，入口动作仍需查证。
- dye.p_ShiftEmp：生产工单与排程相关表（p_ShiftEmp，待确认）；已建模型，入口动作仍需查证。
- dye.p_ShiftMachine：设备维护与能耗相关表（p_ShiftMachine，待确认）；已建模型，入口动作仍需查证。
- dye.p_StuffStorageUnitID：染化料仓位对照；已建模型，入口动作仍需查证。
- dye.p_TestItem：质量检验与异常相关表（p_TestItem，待确认）；已建模型，入口动作仍需查证。
- dye.p_Vehicle：基础主数据相关表（p_Vehicle，待确认）；已建模型，入口动作仍需查证。
- dye.p_WareHouse：坯布半成品成品与仓储相关表（p_WareHouse，待确认）；已建模型，入口动作仍需查证。
- dye.PackQty：其他或待确认相关表（PackQty，待确认）；已建模型，入口动作仍需查证。
- dye.PackQty1：其他或待确认相关表（PackQty1，待确认）；已建模型，入口动作仍需查证。
- dye.PackWorkQty：生产工单与排程相关表（PackWorkQty，待确认）；已建模型，入口动作仍需查证。
- dye.PackWorkQty1：生产工单与排程相关表（PackWorkQty1，待确认）；已建模型，入口动作仍需查证。
- dye.PackWorkQtyDetail：生产工单与排程相关表（PackWorkQtyDetail，待确认）；已建模型，入口动作仍需查证。
- dye.PackWorkSumQty：生产工单与排程相关表（PackWorkSumQty，待确认）；已建模型，入口动作仍需查证。
- dye.PlanDetail：生产工单与排程相关表（PlanDetail，待确认）；已建模型，入口动作仍需查证。
- dye.PlanMain：生产工单与排程相关表（PlanMain，待确认）；已建模型，入口动作仍需查证。
- dye.PPasteDosage：其他或待确认相关表（PPasteDosage，待确认）；已建模型，入口动作仍需查证。
- dye.PPasteDosageDetail：其他或待确认相关表（PPasteDosageDetail，待确认）；已建模型，入口动作仍需查证。
- dye.PrePlanOrder：生产工单与排程相关表（PrePlanOrder，待确认）；已建模型，入口动作仍需查证。
- dye.PriceAdjust：财务结算与成本相关表（PriceAdjust，待确认）；已建模型，入口动作仍需查证。
- dye.PriceAdjustDetail：财务结算与成本相关表（PriceAdjustDetail，待确认）；已建模型，入口动作仍需查证。
- dye.PrintColorSeparate：染色工艺与配方相关表（PrintColorSeparate，待确认）；已建模型，入口动作仍需查证。
- dye.PrintColorSeparateDetail：染色工艺与配方相关表（PrintColorSeparateDetail，待确认）；已建模型，入口动作仍需查证。
- dye.PrintColorSeparateRecord：染色工艺与配方相关表（PrintColorSeparateRecord，待确认）；已建模型，入口动作仍需查证。
- dye.PrintDipsRecord：其他或待确认相关表（PrintDipsRecord，待确认）；已建模型，入口动作仍需查证。
- dye.PrintingTest：质量检验与异常相关表（PrintingTest，待确认）；已建模型，入口动作仍需查证。
- dye.PrintingTestColor：质量检验与异常相关表（PrintingTestColor，待确认）；已建模型，入口动作仍需查证。
- dye.PrintingTestDetail：质量检验与异常相关表（PrintingTestDetail，待确认）；已建模型，入口动作仍需查证。
- dye.PrintingTestStuff：质量检验与异常相关表（PrintingTestStuff，待确认）；已建模型，入口动作仍需查证。
- dye.PrintLabAttach：染色工艺与配方相关表（PrintLabAttach，待确认）；已建模型，入口动作仍需查证。
- dye.PrintLabAtte：染色工艺与配方相关表（PrintLabAtte，待确认）；已建模型，入口动作仍需查证。
- dye.PrintLabMain：染色工艺与配方相关表（PrintLabMain，待确认）；已建模型，入口动作仍需查证。
- dye.PrintRecipe：染色工艺与配方相关表（PrintRecipe，待确认）；已建模型，入口动作仍需查证。
- dye.PrintRecipeColor：染色工艺与配方相关表（PrintRecipeColor，待确认）；已建模型，入口动作仍需查证。
- dye.PrintRecipeDetail：染色工艺与配方相关表（PrintRecipeDetail，待确认）；已建模型，入口动作仍需查证。
- dye.PrintScreen：其他或待确认相关表（PrintScreen，待确认）；已建模型，入口动作仍需查证。
- dye.PrintScreenDetail：其他或待确认相关表（PrintScreenDetail，待确认）；已建模型，入口动作仍需查证。
- dye.PrintScreenRecord：其他或待确认相关表（PrintScreenRecord，待确认）；已建模型，入口动作仍需查证。
- dye.ProcessCraft：染色工艺与配方相关表（ProcessCraft，待确认）；已建模型，入口动作仍需查证。
- dye.ProcessCraftJobNo：染色工艺与配方相关表（ProcessCraftJobNo，待确认）；已建模型，入口动作仍需查证。
- dye.ProcessCraftOrderNo：染色工艺与配方相关表（ProcessCraftOrderNo，待确认）；已建模型，入口动作仍需查证。
- dye.ProcessSchedulebak：染色工艺与配方相关表（ProcessSchedulebak，待确认）；已建模型，入口动作仍需查证。
- dye.ProdIn_to：坯布半成品成品与仓储相关表（ProdIn_to，待确认）；已建模型，入口动作仍需查证。
- dye.ProdInPDARecord：坯布半成品成品与仓储相关表（ProdInPDARecord，待确认）；已建模型，入口动作仍需查证。
- dye.ProdInPriceAtte：财务结算与成本相关表（ProdInPriceAtte，待确认）；已建模型，入口动作仍需查证。
- dye.ProdInPriceProcess：财务结算与成本相关表（ProdInPriceProcess，待确认）；已建模型，入口动作仍需查证。
- dye.ProdLoading：坯布半成品成品与仓储相关表（ProdLoading，待确认）；已建模型，入口动作仍需查证。
- dye.ProdLoadingDetail：坯布半成品成品与仓储相关表（ProdLoadingDetail，待确认）；已建模型，入口动作仍需查证。
- dye.ProdOutPDARecord：坯布半成品成品与仓储相关表（ProdOutPDARecord，待确认）；已建模型，入口动作仍需查证。
- dye.ProdOutPriceAtte：财务结算与成本相关表（ProdOutPriceAtte，待确认）；已建模型，入口动作仍需查证。
- dye.ProdOutPriceProcess：财务结算与成本相关表（ProdOutPriceProcess，待确认）；已建模型，入口动作仍需查证。
- dye.ProdOutRecord：坯布半成品成品与仓储相关表（ProdOutRecord，待确认）；已建模型，入口动作仍需查证。
- dye.ProdStock：坯布半成品成品与仓储相关表（ProdStock，待确认）；已建模型，入口动作仍需查证。
- dye.ProdStockAdjust：坯布半成品成品与仓储相关表（ProdStockAdjust，待确认）；已建模型，入口动作仍需查证。
- dye.ProdStockAdjustDetail：坯布半成品成品与仓储相关表（ProdStockAdjustDetail，待确认）；已建模型，入口动作仍需查证。
- dye.ProdStockBook：成品库存流水；已建模型，入口动作仍需查证。
- dye.ProdStockCheckDetail：质量检验与异常相关表（ProdStockCheckDetail，待确认）；已建模型，入口动作仍需查证。
- dye.ProdStorageAdjust：坯布半成品成品与仓储相关表（ProdStorageAdjust，待确认）；已建模型，入口动作仍需查证。
- dye.ProdStorageAdjustDetail：坯布半成品成品与仓储相关表（ProdStorageAdjustDetail，待确认）；已建模型，入口动作仍需查证。
- dye.ProdStorageAdjustRecord：坯布半成品成品与仓储相关表（ProdStorageAdjustRecord，待确认）；已建模型，入口动作仍需查证。
- dye.ProdTest：质量检验与异常相关表（ProdTest，待确认）；已建模型，入口动作仍需查证。
- dye.PStuffWeight：染化料与称料库存相关表（PStuffWeight，待确认）；已建模型，入口动作仍需查证。
- dye.PStuffWeightDetail：染化料与称料库存相关表（PStuffWeightDetail，待确认）；已建模型，入口动作仍需查证。
- dye.PStuffWeightPhase：染化料与称料库存相关表（PStuffWeightPhase，待确认）；已建模型，入口动作仍需查证。
- dye.PTSampleRegist：质量检验与异常相关表（PTSampleRegist，待确认）；已建模型，入口动作仍需查证。
- dye.PTSampleRegistAtte：质量检验与异常相关表（PTSampleRegistAtte，待确认）；已建模型，入口动作仍需查证。
- dye.PTSampleRegistDetail：质量检验与异常相关表（PTSampleRegistDetail，待确认）；已建模型，入口动作仍需查证。
- dye.QualityAccident：质量检验与异常相关表（QualityAccident，待确认）；已建模型，入口动作仍需查证。
- dye.QualityDeduction：质量检验与异常相关表（QualityDeduction，待确认）；已建模型，入口动作仍需查证。
- dye.QualityRegister：质量检验与异常相关表（QualityRegister，待确认）；已建模型，入口动作仍需查证。
- dye.QuoteAtte：生产工单与排程相关表（QuoteAtte，待确认）；已建模型，入口动作仍需查证。
- dye.QuoteItemPrice：财务结算与成本相关表（QuoteItemPrice，待确认）；已建模型，入口动作仍需查证。
- dye.QuotePriceAtte：财务结算与成本相关表（QuotePriceAtte，待确认）；已建模型，入口动作仍需查证。
- dye.QuotePriceProcess：财务结算与成本相关表（QuotePriceProcess，待确认）；已建模型，入口动作仍需查证。
- dye.RCORDERCOLOR：染色工艺与配方相关表（RCORDERCOLOR，待确认）；已建模型，入口动作仍需查证。
- dye.RCORDERMAIN：客户订单与销售相关表（RCORDERMAIN，待确认）；已建模型，入口动作仍需查证。
- dye.RecordDefect：质量检验与异常相关表（RecordDefect，待确认）；已建模型，入口动作仍需查证。
- dye.RecordEmp：基础主数据相关表（RecordEmp，待确认）；已建模型，入口动作仍需查证。
- dye.ReportItem：其他或待确认相关表（ReportItem，待确认）；已建模型，入口动作仍需查证。
- dye.RequestLimit：其他或待确认相关表（RequestLimit，待确认）；已建模型，入口动作仍需查证。
- dye.s_AutoID：旧业务编号计数；已建模型，入口动作仍需查证。
- dye.s_CorpTitle：公司抬头资料；已建模型，入口动作仍需查证。
- dye.s_Flow：旧审批流程配置；已建模型，入口动作仍需查证。
- dye.s_FlowRecord：旧审批事实记录；已建模型，入口动作仍需查证。
- dye.s_FlowStep：旧审批步骤配置；已建模型，入口动作仍需查证。
- dye.s_FlowStepEmp：旧审批人员配置；已建模型，入口动作仍需查证。
- dye.s_FlowTask：旧审批待办及签署事实；已建模型，入口动作仍需查证。
- dye.s_Revision：旧业务字段变更单；已建模型，入口动作仍需查证。
- dye.s_RevisionDetail：旧业务字段变更明细；已建模型，入口动作仍需查证。
- dye.s_SaveMessRule：旧业务提交通知规则；已建模型，入口动作仍需查证。
- dye.s_SaveMessRuleDetail：旧业务提交通知规则明细；已建模型，入口动作仍需查证。
- dye.s_SheetNo：旧单据编号规则；已建模型，入口动作仍需查证。
- dye.SampleChoice：质量检验与异常相关表（SampleChoice，待确认）；已建模型，入口动作仍需查证。
- dye.SampleIn：质量检验与异常相关表（SampleIn，待确认）；已建模型，入口动作仍需查证。
- dye.SampleInDetail：质量检验与异常相关表（SampleInDetail，待确认）；已建模型，入口动作仍需查证。
- dye.SampleOut：质量检验与异常相关表（SampleOut，待确认）；已建模型，入口动作仍需查证。
- dye.SampleOutDetail：质量检验与异常相关表（SampleOutDetail，待确认）；已建模型，入口动作仍需查证。
- dye.SampleStockBook：质量检验与异常相关表（SampleStockBook，待确认）；已建模型，入口动作仍需查证。
- dye.SchClass：其他或待确认相关表（SchClass，待确认）；已建模型，入口动作仍需查证。
- dye.SemiAxisBook：坯布半成品成品与仓储相关表（SemiAxisBook，待确认）；已建模型，入口动作仍需查证。
- dye.SemiAxisRemain：坯布半成品成品与仓储相关表（SemiAxisRemain，待确认）；已建模型，入口动作仍需查证。
- dye.SemiInRecord：坯布半成品成品与仓储相关表（SemiInRecord，待确认）；已建模型，入口动作仍需查证。
- dye.SemiOutRecord：坯布半成品成品与仓储相关表（SemiOutRecord，待确认）；已建模型，入口动作仍需查证。
- dye.SemiOutWorkApply：坯布半成品成品与仓储相关表（SemiOutWorkApply，待确认）；已建模型，入口动作仍需查证。
- dye.SemiOutWorkApplyDetail：坯布半成品成品与仓储相关表（SemiOutWorkApplyDetail，待确认）；已建模型，入口动作仍需查证。
- dye.SemiPostionUp：坯布半成品成品与仓储相关表（SemiPostionUp，待确认）；已建模型，入口动作仍需查证。
- dye.SemiStock：坯布半成品成品与仓储相关表（SemiStock，待确认）；已建模型，入口动作仍需查证。
- dye.SemiStockBook：半成品库存流水；已建模型，入口动作仍需查证。
- dye.SemiStockSpecUp：坯布半成品成品与仓储相关表（SemiStockSpecUp，待确认）；已建模型，入口动作仍需查证。
- dye.SemiStockSpecUpDetail：坯布半成品成品与仓储相关表（SemiStockSpecUpDetail，待确认）；已建模型，入口动作仍需查证。
- dye.SHIFT：生产工单与排程相关表（SHIFT，待确认）；已建模型，入口动作仍需查证。
- dye.ShiftArrange：生产工单与排程相关表（ShiftArrange，待确认）；已建模型，入口动作仍需查证。
- dye.ShiftArrangeDetail：生产工单与排程相关表（ShiftArrangeDetail，待确认）；已建模型，入口动作仍需查证。
- dye.ShiftPlan：生产工单与排程相关表（ShiftPlan，待确认）；已建模型，入口动作仍需查证。
- dye.ShiftPlanDetail：生产工单与排程相关表（ShiftPlanDetail，待确认）；已建模型，入口动作仍需查证。
- dye.SHOUPITONGZHIDAN：其他或待确认相关表（SHOUPITONGZHIDAN，待确认）；已建模型，入口动作仍需查证。
- dye.Smp_PrescriptEntry：其他或待确认相关表（Smp_PrescriptEntry，待确认）；已建模型，入口动作仍需查证。
- dye.StaffEstablishing：其他或待确认相关表（StaffEstablishing，待确认）；已建模型，入口动作仍需查证。
- dye.StandCraft：染色工艺与配方相关表（StandCraft，待确认）；已建模型，入口动作仍需查证。
- dye.StandCraftBeforeDetail：染色工艺与配方相关表（StandCraftBeforeDetail，待确认）；已建模型，入口动作仍需查证。
- dye.StandCraftDetail：染色工艺与配方相关表（StandCraftDetail，待确认）；已建模型，入口动作仍需查证。
- dye.StandCraftJobNo：染色工艺与配方相关表（StandCraftJobNo，待确认）；已建模型，入口动作仍需查证。
- dye.SterotypeTech：其他或待确认相关表（SterotypeTech，待确认）；已建模型，入口动作仍需查证。
- dye.Stuff_Step：染化料与称料库存相关表（Stuff_Step，待确认）；已建模型，入口动作仍需查证。
- dye.StuffChange：染化料与称料库存相关表（StuffChange，待确认）；已建模型，入口动作仍需查证。
- dye.StuffCombineSheets：染化料与称料库存相关表（StuffCombineSheets，待确认）；已建模型，入口动作仍需查证。
- dye.StuffDeptApply：染化料与称料库存相关表（StuffDeptApply，待确认）；已建模型，入口动作仍需查证。
- dye.StuffDeptApplyDetail：染化料与称料库存相关表（StuffDeptApplyDetail，待确认）；已建模型，入口动作仍需查证。
- dye.StuffOutApply：染化料与称料库存相关表（StuffOutApply，待确认）；已建模型，入口动作仍需查证。
- dye.StuffOutApplyDetail：染化料与称料库存相关表（StuffOutApplyDetail，待确认）；已建模型，入口动作仍需查证。
- dye.StuffPurDetail：染化料与称料库存相关表（StuffPurDetail，待确认）；已建模型，入口动作仍需查证。
- dye.StuffPurMain：染化料与称料库存相关表（StuffPurMain，待确认）；已建模型，入口动作仍需查证。
- dye.StuffStock：染化料与称料库存相关表（StuffStock，待确认）；已建模型，入口动作仍需查证。
- dye.StuffStockBook：染化料库存流水；已建模型，入口动作仍需查证。
- dye.StuffWeightJobSheetNo：染化料与称料库存相关表（StuffWeightJobSheetNo，待确认）；已建模型，入口动作仍需查证。
- dye.StuffWeightPrint：染化料与称料库存相关表（StuffWeightPrint，待确认）；已建模型，入口动作仍需查证。
- dye.SwipeEmpEdit：基础主数据相关表（SwipeEmpEdit，待确认）；已建模型，入口动作仍需查证。
- dye.SwipeEmpEditDetail：基础主数据相关表（SwipeEmpEditDetail，待确认）；已建模型，入口动作仍需查证。
- dye.TBKEY：其他或待确认相关表（TBKEY，待确认）；已建模型，入口动作仍需查证。
- dye.TBSMSALLOT：其他或待确认相关表（TBSMSALLOT，待确认）；已建模型，入口动作仍需查证。
- dye.TBSMSINFO：其他或待确认相关表（TBSMSINFO，待确认）；已建模型，入口动作仍需查证。
- dye.TEMPLATE：基础主数据相关表（TEMPLATE，待确认）；已建模型，入口动作仍需查证。
- dye.Test_Detail：质量检验与异常相关表（Test_Detail，待确认）；已建模型，入口动作仍需查证。
- dye.Test_Main：质量检验与异常相关表（Test_Main，待确认）；已建模型，入口动作仍需查证。
- dye.TightTube：其他或待确认相关表（TightTube，待确认）；已建模型，入口动作仍需查证。
- dye.TightTubeDetail：其他或待确认相关表（TightTubeDetail，待确认）；已建模型，入口动作仍需查证。
- dye.TightTubePlan：生产工单与排程相关表（TightTubePlan，待确认）；已建模型，入口动作仍需查证。
- dye.TightTubePlanDetail：生产工单与排程相关表（TightTubePlanDetail，待确认）；已建模型，入口动作仍需查证。
- dye.UrgentInStruct：其他或待确认相关表（UrgentInStruct，待确认）；已建模型，入口动作仍需查证。
- dye.UrgentInStructDetail：其他或待确认相关表（UrgentInStructDetail，待确认）；已建模型，入口动作仍需查证。
- dye.USER_OF_RUN：其他或待确认相关表（USER_OF_RUN，待确认）；已建模型，入口动作仍需查证。
- dye.USER_SPEDAY：其他或待确认相关表（USER_SPEDAY，待确认）；已建模型，入口动作仍需查证。
- dye.USER_TEMP_SCH：基础主数据相关表（USER_TEMP_SCH，待确认）；已建模型，入口动作仍需查证。
- dye.UserACMachines：设备维护与能耗相关表（UserACMachines，待确认）；已建模型，入口动作仍需查证。
- dye.USERINFO：其他或待确认相关表（USERINFO，待确认）；已建模型，入口动作仍需查证。
- dye.UsersMachines：设备维护与能耗相关表（UsersMachines，待确认）；已建模型，入口动作仍需查证。
- dye.UserUsedSClasses：其他或待确认相关表（UserUsedSClasses，待确认）；已建模型，入口动作仍需查证。
- dye.WareHouseProdCount：坯布半成品成品与仓储相关表（WareHouseProdCount，待确认）；已建模型，入口动作仍需查证。
- dye.WashTheTankDye：染色工艺与配方相关表（WashTheTankDye，待确认）；已建模型，入口动作仍需查证。
- dye.WDefectPenalty：旧质量责任及扣奖明细；已建模型，入口动作仍需查证。
- dye.WeightTechInfo：染化料与称料库存相关表（WeightTechInfo，待确认）；已建模型，入口动作仍需查证。
- dye.WidthGramWeight：染化料与称料库存相关表（WidthGramWeight，待确认）；已建模型，入口动作仍需查证。
- dye.WProcessBak：染色工艺与配方相关表（WProcessBak，待确认）；已建模型，入口动作仍需查证。
- dye.WProcessStep：染色工艺与配方相关表（WProcessStep，待确认）；已建模型，入口动作仍需查证。
- dye.WProcessStepBak：染色工艺与配方相关表（WProcessStepBak，待确认）；已建模型，入口动作仍需查证。
- dye.WVehicle：其他或待确认相关表（WVehicle，待确认）；已建模型，入口动作仍需查证。
- dye.WWorkRecord：生产工单与排程相关表（WWorkRecord，待确认）；已建模型，入口动作仍需查证。
- dye.WWorkTime：生产工单与排程相关表（WWorkTime，待确认）；已建模型，入口动作仍需查证。
- dye.ye.dye：染色工艺与配方相关表（ye.dye，待确认）；已建模型，入口动作仍需查证。
- dye.yunfeibiaozhun：其他或待确认相关表（yunfeibiaozhun，待确认）；已建模型，入口动作仍需查证。
- dye.z_RevisionDetail：旧业务字段修改值；已建模型，入口动作仍需查证。
- dye.z_RevisionKey：旧业务字段修改来源键；已建模型，入口动作仍需查证。
- dye.ZDAddPrice：财务结算与成本相关表（ZDAddPrice，待确认）；已建模型，入口动作仍需查证。
- dye.ZDAddPriceDetail：财务结算与成本相关表（ZDAddPriceDetail，待确认）；已建模型，入口动作仍需查证。
- dye.zhijianwenti：其他或待确认相关表（zhijianwenti，待确认）；已建模型，入口动作仍需查证。


## 2026-10-15第五批接续

外协原料退回、成品退厂、加工厂质量处置、包装入库/投坯原行采用、实际交付/退货/签收、工卡拆合/订单分配转移、明确工序同步及缺表头合卡关系采用已接入；新增22项测试，完整167项通过。代码与实际历史核查见《2026-10-15外协退回工卡拆合包装交付实施记录》。旧等价规则与合理差异、待接续程序严格按异常E41～E45区分，不以页面存在或原字段齐全代表整链完成。

## 2026-10-15第六、七批接续

第六批增加自动合卡选路/同步/步骤判断、工卡计划及关系撤回、出库前后四套细码拆合和撤回。第七批接上全库空进度、GX06/GX07染色质量重建及历史细码恢复。当前223项回归测试通过。

| 原程序/入口 | 当前实现 | 保留差异与待办 |
|---|---|---|
| Sp_DPSyncToCombineSheets尾段 | 自动合卡执行全库维护、Curr1、DP步骤、质量重建；可独立预览质量 | 无序选择、NULL删除、多行标量与原单对照见E46/E50 |
| vwDyeWorkQty、vw_DyeWorkQtyQuer | 最小工序组、最后时间并列、原数量汇总、班别、质量类别与加料统计 | 全部原刷卡保留，视图筛选只影响统计；合理展开差异E50 |
| Sp_JobProcessUpdate_Curr | 全库空进度预览及维护，逐卡审计 | 旧游标变量残值不跨卡复制，见E51 |
| GrayRecordCutLogs历史恢复 | 全部173条日志解析，资料留档、明确当前结果的逆向、撤回恢复 | 159条数量种类未标；缺失旧细码完整前值及33条失败日志见E52 |

新增恢复行不伪造旧细码主键；完整旧日志旧erpID记录在来源事实。实际报工、称料、包装和收发的拆合整链撤销尚未全部闭合，继续按后续开发方案办理。

## 2026-10-15第八批接续

报工、称料及其实际染化料出库、包装成品收发/退回、坯料半成品领用、投坯细码与相关质量记录已接入工卡整链预览和撤销；可同时撤回新拆合计划，并可撤回本次整链撤销。新增明确来源关联入口，承接缺工卡号和孤立原记录。原行留档、实际库存反记、逐条刷卡回写、包装/领用/入库进度、签收及质量处置事实恢复均由服务层办理。

本批不声称存在一个完全等价的旧整链过程：原过程、原入口限制和新组合语义分别记录，见E53～E55及《2026-10-15工卡执行整链撤销实施记录》。此前“未闭合”是第七批时点；当前剩余为未证明的动态链、跨卡依赖、现场回执以及真实原单逐项对照，不能据此遗漏模型、历史事实或少用入口。

## 2026-10-15第九批接续

| 原程序/入口 | 本批实现 | 差异及验收边界 |
|---|---|---|
| RecordYield_Add | 同工卡同卷号全部活动包装替换新增、预览及撤回；原行留档，新Guid与原参数，新包装CheckNo沿用选定来源 | 最新非空字段与旧过程漏列、旧长度、原DELETE留档语义见E56 |
| Sp_RecordYieldQuery | 包装文本排序、投坯流水分组排序、同序号及重复条码全候选配对；批量回写和撤回 | 并列确定顺序、多候选选最后、三位溢出扩展及重复Guid按明确行回写见E57 |
| 明确单条投坯采用 | 增加逐字段前值及撤回，可恢复此前批量配对事实 | 老办理缺前值不能凭空补出；新办理完整留档 |
| 工卡执行整链 | 继续追溯每层包装替换前来源所生成的实际入库，包含缺失工卡号的明确来源 | 原包装留档不重复计量；真实库存仍按实际流水反记，见E58 |

实际开发历史库只读核验：包装RecordYield 377,215条、投坯JobGrayRecord 0条。工卡S260814003有34条包装，配对预览34条均明确未匹配，未清空原投坯字段，也未补造投坯。代码测试和运行服务核验详见《2026-10-15包装替换排序配对实施记录》及验证JSON；真实非空历史配对仍待原单对照。

## 2026-10-15第十批接续

| 原字段/入口/程序 | 本批实现 | 差异及验收边界 |
|---|---|---|
| JobSheet.LossStr、WDefect及工序计划 | 原卡与明确评审生成再加工卡，保留原计划及实际记录，采用选定工序理论值 | 通过明确类型参数生成，不宣称JobSheetInsert全流程等价；E59 |
| GrayInDetail/SemiInDetail、GrayOutJob/SemiOutJob | 实际领用到所选卡；跨卡生成原卡退回和目标卡转领，两单事务及各自原库存规则 | 明确所属记录ID、异常编号可填写新号、所有原行保留；E59 |
| 拆/合/再加工及整链逆向 | 合卡全部成员、再加工来源、跨卡实际退领依赖；下游先撤销，上游先恢复 | 历史没有前值或明确来源仍单列，不猜接；E59 |
| PurApplyDetail到StuffIn/SmallStuffIn/ArticleIn/FabricArticleIn | 四入口实际收货、16类退货、逐条采购来源报告 | 分别Qty/InQty及-ABS/取负；空表也实现并测试，E60 |
| OutWorkApply/SemiOutWorkApply来源 | 发出、回货、退回、交付及加工厂质量处置逐条追溯；含留档原单 | 无明确来源的历史明细单列，结案仍按实际选定收发核对，E60 |
| Sp_ReworkCloth2、Sp_ReworkCloth3 | 05/06月度总量及内审/客退返修，两阶段舍入、全部重复连接和NULL | 完整月份修正，1/4及Comparison系列继续待办，E61 |

运行中42次HTTP检查通过，新增12个动作定义，662模型全部具有旧erpID。2026年8月返修报告和独立只读SQL结果一致：05没有该站点刷卡；06有5,464条原刷卡；全月11,916条刷卡CurrDosage均为空，原公式AllKg和返修分类结果因此为NULL。原CurrKg均有值，不能擅自把未知投入比例当100来凑结果。全部未归类原行在补充明细展示，不代表刷卡或产量被删除。

本批代码与验证见[跨卡再加工采购外协返修实施记录](2026-10-15跨卡再加工采购外协返修实施记录.md)及[验证JSON](erp-cross-card-verification-20261015.json)。历史库只读核对，新实际收发和逆向写入在独立测试库验证，不对已承接历史批量办理。

## 2026-10-15第十一批接续

| 原模型/程序 | 本批实现 | 差异及验收边界 |
|---|---|---|
| PurGrayIn/PurSemiIn、GrayInDetail/SemiInDetail | 采用原行生成16类采购退货、保留原收料号及采购来源；全部类型收退查询 | 实际量和原入库符号不改；非数字收料号提供明确新号，E62 |
| OutWorkApply/SemiOutWorkApply | 结案后继续收退登记、待复核、累计原料退回/成品退厂核对及再次结案版本 | 不自动算损耗，不猜接历史关系；单据/表头变化和退出活动范围可查，E63 |
| Sp_ReworkCloth1 | 日/月、布种/车间返修，05重量/06次数比例，原小计公式 | 原分母重复与异常比例保留；零分母为NULL并说明，E64 |
| Sp_ReworkCloth4 | 05/06综合原总量、各站返修及FAR数量输入 | 财务来源未自动抽取，缺失FAR为NULL，E64/E65 |
| Rework_Comparison1/2 | 默认原年份连接，明确同期修正版，两期真实来源分列 | 原错误年份及FAR连接保留；YF拆列/月份边界说明，E65 |
| Rework_Comparison3 | 原部门/班次数量与长度分类、重复连接及未匹配来源 | 最新PreMeter缺列，采用独立输入且未知为NULL；不宣称自动全量复刻，E65 |

代码在source_purchase_flow、source_outwork_followup、source_outwork_close、source_rework_reports和source_rework_extended服务中；接口负责参数和权限，页面元数据注册7个新增动作定义。没有新增模型迁移，662个ERP模型均保留旧erpID。

详见[第十一批实施记录](2026-10-15采购退货外协结案返修报告实施记录.md)和[历史及运行核验JSON](erp-rework-followup-verification-20261015.json)。真实开发历史库仅调用只读报告和预览，新收退和结案在隔离测试库验证。

## 2026-10-15第十二批：质量自动数量及采购、外协回料

| 原来源/入口 | 本批服务与动作 | 原异常及边界 |
|---|---|---|
| FARMain/FARDetail质量投影 | 固定SELECT抽取、不可变版本导入、报告自动选批次；401条逐字段及五个月独立聚合核对 | 不建财务流程；PreMeter缺列为NULL；责任缺项完整返回，E66 |
| Sp_ReworkCloth4、Rework_Comparison1/2/3 | 自动采用本期/同期原数量；可指定批次或明确手动来源 | 不叠加版本；不伪造零；原错误年份与修正版分开 |
| PurDetail/PurApplyDetail/ArticlePurDetail/StuffPurDetail | 四类采购明细采用实际数量生成染化料/机物料收货；保留原采购数量和全部候选表头 | 原界面共用表与独立空表均实现；价格单位不当数量单位，E68 |
| GrayIn/SemiIn采购收退 | 两种引用列均查询；实际长度、供应商与非数字新号可明确填写 | 旧18/20进度仍沿原PurDetailNo |
| GrayOut30、SemiOut32 → GrayIn21/SemiIn25/26 | 原余额及来源报告、实际收回、库存、质量处置、实际退厂 | 原混量粒数公式照列，实际量独立，E67 |
| 外协结案与工卡执行逆向 | 收回/退厂/质量处置登记结案复核；混合收回模型核对；执行撤销与恢复 | 同ID不同模型不去重、无工卡号沿明确来源追溯 |

计算与办理在source_purchase_flow、source_outwork_material、source_outwork_close、source_outwork_followup、source_chain_reverse及quantity_services中；接口负责参数/权限，页面显示自动来源批次。新增2模型并迁移，664个ERP模型均有旧erpID。本批取代上一批“财务数量未自动抽取”的状态；缺失原长度仍未解决。

详见[实施记录](2026-10-15质量数量自动映射采购外协收回实施记录.md)和[运行核验](erp-quantity-mapping-verification-20261015.json)。

## 2026-10-15第十三批：工位质量、产量及排程核对

| 原程序/来源 | 本批实现 | 边界与异常 |
|---|---|---|
| Sp_DyeRateNew / ColorMatching | 原班组/对色员分组、总计、直通率/返修率、JTimes | SQL比例精度、零分母和原NULL保留，E69 |
| Sp_DyeRate_ColorMatching_Query / v_ColorMatching_DyeAdd | 原8点换日、存储日期、称料加色次数及员工连接看板 | 员工未匹配、重复连接、原100行上限取消，E69 |
| Sp_DyeRate_dyeCheckout_Query / s_vwColorDepth | 原色级框架、班组及总量列；明确上月修正版 | 上月错连、10号碰撞、字典倍增原样保留，E70 |
| v_WProcess_WorkQty | 原人员/工卡/工序连接、DISTINCT、7点50分换日 | 02/NULL及缺关联来源补充显示，E71 |
| sp_SimpleRecordYieldQuery / sp_RecordYieldByWinding | 原员工/络筒包装产量、跨日期字符串和字典依赖 | NULL分组、文本编码、无序拼接及员工标量多行，E72 |
| s_DBComboValue | 新基础原形模型，全表403行承接、4字段逐值对照 | 完整复合旧erpID，全部枚举保留 |
| Sp_CheckProcessRS / CheckProcessStatus | 重复排程、GX03/GX07顺序和间隔核对 | 不确定变量/最新时间候选全部列示；调用时机待补证，E73 |
| T_PSD / vw_ProcessDyMachine | 原最近06刷卡、称料、计划日期和优先级排名 | 81条真实旧SQL序位一致，E73 |
| Sp_QualityIssues2 | 自动旬/月原数量与去重工卡分母 | 全类型、不额外过滤；未知/空区间区分，E74 |

新增3个service模块和6个页面动作定义，原质量旬报动作扩展自动分母。新增基础字典迁移及出缸质量名称迁移；665模型全部有旧erpID。详见[实施记录](2026-10-15工位质量产量排程核对实施记录.md)与[旧SQL对照结果](erp-station-reports-verification-20261015.json)。


## 2026-10-15 第十四批：自动标签、包装人员和工位归档

| 原对象 | service及页面动作 | 当前核验与差异 |
|---|---|---|
| sp_AuTo_RecordYield | source_package_labels；工卡预览/同步/撤回，接入整链逆向 | 保留投坯条码与全包装条码范围；真实连接为空，隔离数据验证；E75 |
| RecordYield_EmpID | source_package_people.latest_packers；包装人员查询 | 70,751条真实旧新结果一致；306,464条未参与来源保留；E76 |
| V_RecordYield | source_package_people.shared_yield；原条码/明确Guid口径 | 377,215条包装、577,705条人员均保留；两种连接当前均0条，非空分支隔离验证；E76 |
| Sp_WprocessBackUp | source_work_archive；预览/归档/撤回 | 原范围、明细复制、触发回写及恢复已接入；缺ProcessNo和无序触发采用明确实现；三张空备份表仍有功能；E77 |

本批无模型迁移、无重复历史导入；实际开发历史库仅查询及预览，操作回归在隔离库。新代码接入不等于全部旧客户端和设备验收完成。


## 2026-10-15第十八批：循环日历、班次与机台选择

| 原对象 | service与页面动作 | 保留差异与边界 |
|---|---|---|
| Sp_CreateShiftAndClassDetail | source_shift_calendar；配置预览、生成、换版留档、撤回 | 无序末组、零/负/NULL生成天数、原ID复用、跨午夜第四段覆盖；E90 |
| Sp_GetShiftAndClass3 | 同日四段查询、机台部门匹配、缺日仅一次365天续排 | RIGHT(5)、原ClassName含义、NULL及重复连接保留；E91 |
| qry_ProcessMachine | source_machine_choice；工卡查询可选机台 | 06占机与复版审核两路、非06的AA/NULL、原无序变量和排除原因；E92 |
| Fn_Get_Machine / New_StringSplit | 工卡进缸机台查询、员工分号名单解释 | TOP1无序明确首条；前三字符备选；名单空段及原长度限制；E92 |

入口位于基础信息的p_ShiftArrange/p_ShiftArrangeDetail/p_Machine和生产工卡JobSheet。未添加模型字段，所有模型原有旧erpID继续保留。真实核对、隔离办理与尚未证明的旧客户端调用分开记载，详见[本批实施记录](2026-10-15班次循环机台选择实施记录.md)。

## 2026-10-16第十九批：现场补录、巡检保养和维修

| 原对象 | service与页面动作 | 边界与差异 |
|---|---|---|
| DPWProcess/AddWProcessEdit/WProcessEdit/AddDyeWProcessStep | source_site_work；生产工卡查询及四类录入 | 独立补录不擅自转正式工步；负数/NULL保留；E93 |
| SaveInspectionLog/SaveMachineCareRecords | source_equipment_projects；新增、修改、项目预览、替换留档和撤回 | 修改日期差异、无序后缀、三串左连接倍增、空值规则；E94/E95 |
| GetMachineCaseProject/两个BySheetSeries项目部分 | 机台/方案项目、记录项目查询 | 直接方案与机台回退分别处理；字面Y、不虚构旧双结果集协议；E94/E95 |
| SaveMachineFaultBill/CheckMachineFaultBill | source_equipment_faults；报修、附件绑定和创建/修改流转 | 原FaultID输入实际为描述，注释检查不恢复；E96 |
| GetFaultActions1/2/FalutAction_Check | 两版动作列表与原有效检查 | 104组实际结果一致；原重复关闭/签到文字差异保留；E96 |
| FalutAction八过程 | 13类维修动作、配件轮次、双评论、签到、恢复/重新提交和撤回 | 精简拒绝也确认、签到故障码覆盖、原不清时间等保留；E96/E97 |
| MachineFault_Update/ChangeIDListToEmpName | 普通写入和动作中的结果触发、分号姓名解析 | 包含已修均触发、无序标量/拼接明确来源ID顺序；E97 |
| 外库机台参数与s_Notice | 原定义/待办及通知意图留存 | 外链与实际投递尚未接入，未伪造成功结果；E98 |

25项动作绑定、45项运行HTTP检查，历史字段和旧erpID不变。10项原设备参数在本批采用，历史业务单据没有重复导入。非空真实报工4条60字段一致；当前为空的项目/配件/评论/补录表也已编码和隔离测试。详见[实施记录](2026-10-16现场报工补录设备维修实施记录.md)及[核对结果](erp-equipment-verification-20261015.json)。
