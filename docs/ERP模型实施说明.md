# 染色 ERP 模型实施说明

> 2026-10-16 来源设计更新：当前及后续开发取消额外【旧erpID】，保留旧表原键字段，使用来源批次/提取行及既有来源映射追溯。本文早期实施和验证记录中的旧字段描述属于当时状态，不再作为当前模型要求。以[原键字段与来源追溯规范](原键字段与来源追溯规范.md)为准。

当前补充（2026-10-14）：本文件下文保留对应阶段记录。最新结构、662个ERP模型、553表完整来源、原服务分支及承接/采用结果见[2026-10-14完整原表承接与业务服务实施记录](2026-10-14完整原表承接与业务服务实施记录.md)。旧SQL停止、91表覆盖及旧模型数量不再代表当前起点。

实施日期：2026-10-11，实施状态更新于 2026-10-12。依据：[六模块模型与字段设计](H:/Project_python/django-vue3-admin/dyeing/染色ERP六模块模型与字段设计.md)。当前项目：`djangovue3_dyeing`，Django 5.2.18。

七个ERP业务应用已注册。当前700个ERP模型，其中589个原表复刻模型，保留12,016个旧表原字段。公共基类保留业务备注及平台审计字段，取消额外旧ID列；原表按批次/提取行、转换主档按既有来源映射追溯。以下早期分批计数保留为实施历史；当前来源设计见《原键字段与来源追溯规范》。

本次按当前旧系统字段设置复核，修订字段含义、标题、长度、精度及空值；具体已复刻和合理调整见 [旧系统字段复刻与差异处理说明](H:/Project_python/django-vue3-admin/djangovue3_dyeing/docs/旧系统字段复刻与差异处理说明.md) 和 [逐项对照](H:/Project_python/django-vue3-admin/djangovue3_dyeing/docs/旧系统字段逐项对照.md)。

## 应用与源码入口

| 模块 | 应用标签 | 模型数 | 模型文件 | 初始迁移数 | 当前迁移总数 |
|---|---|---:|---|---:|---:|
| 基础信息 | erp_base | 31 | [models.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_base/models.py) | 2 | 10 |
| 销售管理 | erp_sales | 13 | [models.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_sales/models.py) | 2 | 7 |
| 采购管理 | erp_purchase | 6 | [models.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_purchase/models.py) | 3 | 6 |
| 打样管理 | erp_sampling | 10 | [models.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_sampling/models.py) | 1 | 3 |
| 生产管理 | erp_production | 27 | [models.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_production/models.py) | 3 | 11 |
| 仓储管理 | erp_warehouse | 19 | [models.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_warehouse/models.py) | 1 | 8 |

应用配置位于 [application/plugins.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/application/plugins.py)。跨应用外键使用明确的 `app_label.Model` 字符串；Django 将跨模块依赖拆成多份初始迁移。所有实体继承 `ErpModel(CoreModel)`，增加长业务备注 `remarks`，复用现有账号、部门和附件资源；取消额外旧 ID 字段，保留原表真实键列。

已有框架把登记的模型转换为资源接口。六个应用的 106 个模型均已登记，普通基础资料、明确业务动作和只读结果分别使用对应服务与权限；库存流水和余额由收发、盘点、调拨及冲销动作维护。A 批的历史实施范围见 [基础信息A批实施记录](H:/Project_python/django-vue3-admin/djangovue3_dyeing/docs/基础信息A批实施记录.md)，后续各批见 [业务功能逐批实施记录](业务功能逐批实施记录.md)。

## 已实现的字段与关系规则

- 字段中文名称、声明长度、小数精度、空值、枚举默认和关系目标按设计逐项核对。所有外键均需明确关联对象，没有隐含的默认外键 ID。
- 数量、粒数、剂量、重量和价格采用 Decimal；缺失数值保留 NULL，明确零值保留 0。旧粒数包含小数，新模型保留相应精度。
- 45 类固定状态或类别集中在 [choices.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_base/choices.py)。基础业务字典通过 BusinessChoice 维护，旧状态码迁移仍需逐项对照。
- 从属明细使用 CASCADE；主数据及历史引用使用 PROTECT；路线/工卡前置节点、地址到联系人使用 RESTRICT，以支持整份未采用草稿的从属删除。
- 232 条命名的 UniqueConstraint/CheckConstraint 已进入数据库，包括复合身份、默认联系人/地址、可空包装库存维度、有效排程、采用配方轮次、库存来源和冲销等约束；单字段唯一、外键、一对一约束另由字段定义建立。
- `clean()` 定义跨表业务一致性：同仓库库位、同工卡参数和分配、同来源配方阶段、同物料包装批次、库存基本单位，以及冲销的原维度和等量反向规则。

跨表校验由业务动作明确调用 `full_clean()`；普通 `save()` 不会自动运行该方法。本次没有在每次保存时加入通用异常捕获或备用字段选择。[Django 模型校验说明](https://docs.djangoproject.com/en/5.2/ref/models/instances/#validating-objects)。数据库内约束使用 Django 5.2 的 `condition=` 定义。[约束说明](https://docs.djangoproject.com/en/5.2/ref/models/constraints/)。

## 已实现的计算

| 计算 | 源码入口/调用 | 行为 |
|---|---|---|
| 固定单位换算 | `Unit.convert_quantity(quantity, target_unit)` | 同维度、同基准单位按倍率换算；kg 与米不能混算 |
| 合同总单价 | `CommercialPriceLine.calculated_unit_price` | 客确基础价 + 另计价；任一未知则结果未知 |
| 剂量调整 | `MaterialPlanLine.calculated_adopted_dosage` | 原剂量 × (1 + 调整百分比 / 100) |
| 计划染化料质量 | [production/calculations.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_production/calculations.py) 的 `planned_chemical_mass_kg` | 干料质量百分比或浴液 g/L，分别使用明确计算基准；结果为 kg |
| 执行经过分钟 | `OperationExecution.elapsed_minutes` | 根据明确开始/结束时间计算，支持跨日；不推算扣停机工时 |
| 包装计算净重 | `Package.calculated_net_mass_kg` | 明确选择毛重扣皮重或固定单粒质量方法；结果不自动覆盖已采用快照 |
| 盘点差异 | `StockCountLine.difference` | 实盘量 − 冻结账面量；未盘为 NULL，实盘零产生完整盘亏差额 |

包装公式位于 [warehouse/calculations.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_warehouse/calculations.py)。已保存的采用剂量、计划数量、净重与合同价格是业务快照，由采用/确认动作明确填写，主资料修改不会自动重算历史快照。

## 数据库验证

2026-10-12 最终核对：106 张 ERP 表全部含可空 TEXT 列 `legacy_id`，累计 45 个 ERP 迁移。已登记 91 张完整旧来源表，并明确导入 1,343 条基础主档；另外五个业务应用的单据表记录仍为零。完整回归及实际 157 项运行检查通过，详情见《业务功能逐批实施记录》。

以下为字段修订阶段和初始建模阶段的历史验证，不代表当前模型数或导入数量。

字段修订阶段核对：98张ERP表全部含可空TEXT列 `legacy_id`，累计25个ERP迁移；当时ERP业务记录为0。与当时迁移前备份比较，除迁移记录外原有43张平台表的结构及5,556条记录完全一致；SQLite完整性和外键检查通过。

本次字段修订前备份：[db_before_legacy_field_alignment_20261011_204728.sqlite3](H:/Project_python/django-vue3-admin/djangovue3_dyeing/data-backups/db_before_legacy_field_alignment_20261011_204728.sqlite3)。以下是首次建立ERP模型时的历史核对结果。

迁移前快照：[db_before_erp_models_20261011.sqlite3](H:/Project_python/django-vue3-admin/djangovue3_dyeing/data-backups/db_before_erp_models_20261011.sqlite3)。

已经与快照逐表逐条核对：

- 新增 98 张 ERP 表，应用 12 个 ERP 初始迁移。
- 原有 44 张表的结构保持一致，原有 5,137 条记录全部保留。
- 新 ERP 业务表总记录数为 0；没有生成示例客户、物料、工卡或库存记录。
- SQLite 完整性检查通过，外键违规数为 0。
- 当前模型与迁移一致，`makemigrations --check --dry-run` 无变化。

旧 SQL Server 及旧 ERP 业务数据未写入。财务系统不在这批模型范围内，商业合同价格作为销售/采购业务信息保留。

## 字段修订阶段测试结果

64 项测试通过：ERP 测试 52 项，现有模型身份与业务合同回归测试 12 项。测试数据库从空库实际执行了完整迁移；覆盖固定单位换算、NULL 与零值、小数粒数、默认联系人、草稿从属删除、主数据保护、可空库存维度唯一、来源重复、冲销、更正、排程与现有附件/Excel行为；新增旧身份文本与复合键、未知标志、NULL/空串、完整进厂时间、品牌/用途/特殊事项，以及生产完成与结案时间分离的验证。

从项目根目录可运行：

```powershell
Push-Location backend
..\.venv\Scripts\python.exe manage.py check --database default
..\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
..\.venv\Scripts\python.exe manage.py test plugins.erp_base.tests system.tests.test_model_identity system.tests.test_business_contracts --settings=system.tests.extension_settings --verbosity 1
Pop-Location
```

## 后续开发入口

本轮已实现报价、打样、订单、采购、库存、生产计划、实际执行、质量、返修、包装、交付、查询及归档对照的软件能力。具体业务顺序见 [染色ERP后续开发方案](H:/Project_python/django-vue3-admin/djangovue3_dyeing/docs/染色ERP后续开发方案.md)，实际完成范围及现场待核实项见 [染色ERP本轮实施及验收说明](染色ERP本轮实施及验收说明.md)。

旧单位全空、旧合卡孤儿记录、报价确认表达式冲突、检验项目槽位、浴比和百分数基准等，继续按照设计第 12、15 章处理；这些内容没有被编造成迁移默认值。完整历史业务归档与明确主档导入分别办理，尚未证明的业务对应保留核对事项。

当前项目运行 SQLite；完整迁移及五项实际并发已在独立 PostgreSQL 验证。正式业务数据库切换时仍须执行同一套迁移、迁移实际项目数据并核对，不把独立测试数据库当作已完成正式切换。
