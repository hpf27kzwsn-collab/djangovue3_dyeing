# 染色 ERP 模型实施说明

实施日期：2026-10-11。依据：[六模块模型与字段设计](H:/Project_python/django-vue3-admin/dyeing/染色ERP六模块模型与字段设计.md)。当前项目：`djangovue3_dyeing`，Django 5.2.18。

六个业务应用已经注册，98 个实体模型、851 个专属字段全部落地；每个模型另有 9 个公共字段，含“旧系统id” `legacy_id`。12 个初始迁移及13个字段修订迁移已经在本项目的 `backend/db.sqlite3` 执行，ERP 表共98张。当前 ERP 业务表为空，准备承接后续基础资料与业务单据开发。

本次按当前旧系统字段设置复核，修订字段含义、标题、长度、精度及空值；具体已复刻和合理调整见 [旧系统字段复刻与差异处理说明](H:/Project_python/django-vue3-admin/djangovue3_dyeing/docs/旧系统字段复刻与差异处理说明.md) 和 [逐项对照](H:/Project_python/django-vue3-admin/djangovue3_dyeing/docs/旧系统字段逐项对照.md)。

## 应用与源码入口

| 模块 | 应用标签 | 模型数 | 模型文件 | 初始迁移数 | 当前迁移总数 |
|---|---|---:|---|---:|---:|
| 基础信息 | erp_base | 26 | [models.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_base/models.py) | 2 | 4 |
| 销售管理 | erp_sales | 13 | [models.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_sales/models.py) | 2 | 5 |
| 采购管理 | erp_purchase | 6 | [models.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_purchase/models.py) | 3 | 5 |
| 打样管理 | erp_sampling | 10 | [models.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_sampling/models.py) | 1 | 3 |
| 生产管理 | erp_production | 25 | [models.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_production/models.py) | 3 | 5 |
| 仓储管理 | erp_warehouse | 18 | [models.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_warehouse/models.py) | 1 | 3 |

应用配置位于 [application/plugins.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/application/plugins.py)。跨应用外键使用明确的 `app_label.Model` 字符串；Django 将跨模块依赖拆成多份初始迁移。所有实体继承 `ErpModel(CoreModel)`，增加长业务备注 `remarks` 和旧系统id `legacy_id`，复用现有账号、部门和附件资源。

已有框架会把登记的模型自动转换为通用增删改接口。本阶段 ERP 应用同时列入 `MODEL_EXCLUDE_APPS`，先完成模型与表结构；ORM 和迁移仍正常使用。基础资料接口、单据确认及库存生效服务接入时再登记相应资源，库存流水和余额由专门业务动作维护。

## 已实现的字段与关系规则

- 字段中文名称、声明长度、小数精度、空值、枚举默认和关系目标按设计逐项核对。所有外键均需明确关联对象，没有隐含的默认外键 ID。
- 数量、粒数、剂量、重量和价格采用 Decimal；缺失数值保留 NULL，明确零值保留 0。旧粒数包含小数，新模型保留相应精度。
- 44 类固定状态或类别集中在 [choices.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_base/choices.py)。基础业务字典通过 BusinessChoice 维护，旧状态码迁移仍需逐项对照。
- 从属明细使用 CASCADE；主数据及历史引用使用 PROTECT；路线/工卡前置节点、地址到联系人使用 RESTRICT，以支持整份未采用草稿的从属删除。
- 223 条命名的 UniqueConstraint/CheckConstraint 已进入数据库，包括复合身份、默认联系人/地址、可空包装库存维度、有效排程、采用配方轮次、库存来源和冲销等约束；单字段唯一、外键、一对一约束另由字段定义建立。
- `clean()` 定义跨表业务一致性：同仓库库位、同工卡参数和分配、同来源配方阶段、同物料包装批次、库存基本单位，以及冲销的原维度和等量反向规则。

跨表校验由后续业务动作明确调用 `full_clean()`；普通 `save()` 不会自动运行该方法。本次没有在每次保存时加入通用异常捕获或备用字段选择。[Django 模型校验说明](https://docs.djangoproject.com/en/5.2/ref/models/instances/#validating-objects)。数据库内约束使用 Django 5.2 的 `condition=` 定义。[约束说明](https://docs.djangoproject.com/en/5.2/ref/models/constraints/)。

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

包装公式位于 [warehouse/calculations.py](H:/Project_python/django-vue3-admin/djangovue3_dyeing/backend/plugins/erp_warehouse/calculations.py)。已保存的采用剂量、计划数量、净重与合同价格是业务快照，后续由采用/确认动作明确填写，主资料修改不会自动重算历史快照。

## 数据库验证

字段修订后再次核对：98张ERP表全部含可空TEXT列 `legacy_id`，累计25个ERP迁移；现有ERP业务记录仍为0。与本次迁移前备份比较，除迁移记录外原有43张平台表的结构及5,556条记录完全一致；SQLite完整性和外键检查通过。

本次字段修订前备份：[db_before_legacy_field_alignment_20261011_204728.sqlite3](H:/Project_python/django-vue3-admin/djangovue3_dyeing/data-backups/db_before_legacy_field_alignment_20261011_204728.sqlite3)。以下是首次建立ERP模型时的历史核对结果。

迁移前快照：[db_before_erp_models_20261011.sqlite3](H:/Project_python/django-vue3-admin/djangovue3_dyeing/data-backups/db_before_erp_models_20261011.sqlite3)。

已经与快照逐表逐条核对：

- 新增 98 张 ERP 表，应用 12 个 ERP 初始迁移。
- 原有 44 张表的结构保持一致，原有 5,137 条记录全部保留。
- 新 ERP 业务表总记录数为 0；没有生成示例客户、物料、工卡或库存记录。
- SQLite 完整性检查通过，外键违规数为 0。
- 当前模型与迁移一致，`makemigrations --check --dry-run` 无变化。

旧 SQL Server 及旧 ERP 业务数据未写入。财务系统不在这批模型范围内，商业合同价格作为销售/采购业务信息保留。

## 测试结果

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

具体批次、页面、业务动作和验收条件见 [染色ERP后续开发方案](H:/Project_python/django-vue3-admin/djangovue3_dyeing/docs/染色ERP后续开发方案.md)。下一步先接入基础资料；库存基础服务在生产实际领料和销售交付前完成，供各模块共同使用。单据确认、版本冻结、订单分配上限、实际称量更正、库存生效/冲销、余额更新与并发控制属于后续业务动作，模型建表不代表这些流程已经实现。

旧单位全空、旧合卡孤儿记录、报价确认表达式冲突、检验项目槽位、浴比和百分数基准等，继续按照设计第 12、15 章处理；这些内容没有被编造成迁移默认值。本次没有导入旧业务数据。

正式业务数据库切换到 PostgreSQL 后，应执行同一套迁移，并补充库存并发服务验收；本次数据库运行验证是在当前 SQLite 环境完成的。
