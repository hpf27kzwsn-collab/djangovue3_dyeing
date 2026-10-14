# 染色ERP七模块原表模型字段与关系清单

结构证据：`Textile_GXHFRS`，采集于 `2026-10-12T03:02:50.2608400+08:00`。

本清单与静态 Django 声明由同一份结构证据和逐表登记生成。源字段的列名、类型、长度、精度、空值性均保留；最新界面配置提供中文字段名，没有中文标题的保留原列名。字段语义、计算公式、归属仍需要结合原界面 SQL 和后续真实操作逐项核实，不能把字段建成等同于旧业务联动已完成。

所有 ERP 模型都有 `legacy_id`，界面名称为【旧erpID】。来源有主键时记录 schema、table、完整原主键 JSON；无主键时保持为空，以来源批次及提取行号追溯，不伪造旧ID。

新增原表模型还含来源批次、提取行号、办理阶段、确认时间/人、审核时间/人。新增单据草稿→确认→审核；导入历史单据不编造办理阶段，旧状态原字段原样保留。原表中的计算结果作为原事实字段保存，尚未证明的公式不重新计算或覆盖旧值。

原码和可选关联字段并存。关联只按已声明数据库外键或原界面明确主从配置建立；原码缺父项或匹配多项时仍可承接原行，等待对照。重复条码、原负数、小数件数、空值及倒序时间不设额外拒收规则。

## 2026-10-14关系增补

下方保留原11,412个物理字段清单；本轮增加以下三项明确关系，未改原列。当前原表关系总数161组。

| 明细模型 | 新关联 | 目标模型 | 原列对应 | 依据 |
|---|---|---|---|---|
| `erp_sales.SourceDyeCustomerTSDetail` | `source_parent_1` | `erp_sales.SourceDyeCustomerTS` | `Sheetseries → SheetSeries` | 有效入口主从声明 |
| `erp_warehouse.SourceDyeGrayMaterialDetail` | `source_parent_1` | `erp_warehouse.SourceDyeGrayMaterial` | `Sheetseries → SheetSeries` | 有效入口主从声明 |
| `erp_production.SourceDyeStuffWeightDetail` | `source_parent_1` | `erp_production.SourceDyeStuffWeightPhase` | `SheetSeries＋PhaseNo → SheetSeries＋PhaseNo` | 有效称料阶段明细SQL连接 |

阶段/物料的公式归属及各入口差异见《旧ERP复刻异常与合理实现说明》E12～E14；界面查询别名仍与物理列分别记录。

## 基础信息

新增原表模型 207 个，原字段 2955 个。

### SourceDboAA — 其他或待确认相关表（AA，待确认）

源表：`dbo.AA`；新表：`src_dbo_aa`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| 库存位置 | old_库存位置 | 库存位置 | nvarchar；字节长度 510 | 是 | CharField |
| 重量 | old_重量 | 重量 | float | 是 | FloatField |
| 类别 | old_类别 | 类别 | nvarchar；字节长度 510 | 是 | CharField |
| 规格 | old_规格 | 规格 | nvarchar；字节长度 510 | 是 | CharField |
| 供应商 | old_供应商 | 供应商 | nvarchar；字节长度 510 | 是 | CharField |
| 批号/等级 | old_批号_等级 | 批号/等级 | nvarchar；字节长度 510 | 是 | CharField |
| 剩余库存 | old_剩余库存 | 剩余库存 | float | 是 | FloatField |
| 类别1 | old_类别1 | 类别1 | nvarchar；字节长度 510 | 是 | CharField |

### SourceDboAAA — 其他或待确认相关表（AAA，待确认）

源表：`dbo.AAA`；新表：`src_dbo_aaa`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| 编号 | old_编号 | 编号 | nvarchar；字节长度 510 | 是 | CharField |
| 名称 | old_名称 | 名称 | nvarchar；字节长度 510 | 是 | CharField |
| 供应商 | old_供应商 | 供应商 | nvarchar；字节长度 510 | 是 | CharField |
| 单价 | old_单价 | 单价 | float | 是 | FloatField |
| 数量 | old_数量 | 数量 | float | 是 | FloatField |
| 金额 | old_金额 | 金额 | float | 是 | FloatField |

### SourceDboAAKC1 — 其他或待确认相关表（AAKC1，待确认）

源表：`dbo.AAKC1`；新表：`src_dbo_aakc1`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| 入库类別 | old_入库类別 | 入库类別 | nvarchar；字节长度 510 | 是 | CharField |
| 客户 | old_客户 | 客户 | nvarchar；字节长度 510 | 是 | CharField |
| 本厂规格 | old_本厂规格 | 本厂规格 | nvarchar；字节长度 510 | 是 | CharField |
| 供应商 | old_供应商 | 供应商 | nvarchar；字节长度 510 | 是 | CharField |
| 批号 | old_批号 | 批号 | nvarchar；字节长度 510 | 是 | CharField |
| 锭重 | old_锭重 | 锭重 | float | 是 | FloatField |
| 粒数 | old_粒数 | 粒数 | nvarchar；字节长度 510 | 是 | CharField |
| 重量 | old_重量 | 重量 | float | 是 | FloatField |
| 实际重量 | old_实际重量 | 实际重量 | float | 是 | FloatField |
| 实际区域 | old_实际区域 | 实际区域 | float | 是 | FloatField |
| 半成品颜色 | old_半成品颜色 | 半成品颜色 | nvarchar；字节长度 510 | 是 | CharField |
| 区域 | old_区域 | 区域 | nvarchar；字节长度 510 | 是 | CharField |
| 半成品缸号 | old_半成品缸号 | 半成品缸号 | nvarchar；字节长度 510 | 是 | CharField |
| 采购单号 | old_采购单号 | 采购单号 | nvarchar；字节长度 510 | 是 | CharField |
| A_B | old_a_b | A_B | nvarchar；字节长度 510 | 是 | CharField |
| 件数 | old_件数 | 件数 | nvarchar；字节长度 510 | 是 | CharField |

### SourceDboABC — 其他或待确认相关表（ABC，待确认）

源表：`dbo.ABC`；新表：`src_dbo_abc`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| 库存位置 | old_库存位置 | 库存位置 | nvarchar；字节长度 510 | 是 | CharField |
| 重量 | old_重量 | 重量 | float | 是 | FloatField |
| 类别 | old_类别 | 类别 | nvarchar；字节长度 510 | 是 | CharField |
| 规格 | old_规格 | 规格 | nvarchar；字节长度 510 | 是 | CharField |
| 供应商 | old_供应商 | 供应商 | nvarchar；字节长度 510 | 是 | CharField |
| 批号/等级 | old_批号_等级 | 批号/等级 | nvarchar；字节长度 510 | 是 | CharField |
| 8月结存 | old_8月结存 | 8月结存 | float | 是 | FloatField |
| 本月松筒进仓 | old_本月松筒进仓 | 本月松筒进仓 | float | 是 | FloatField |
| 剩余库存 | old_剩余库存 | 剩余库存 | float | 是 | FloatField |

### SourceDboADD — 其他或待确认相关表（ADD，待确认）

源表：`dbo.ADD`；新表：`src_dbo_add`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| 入库类別 | old_入库类別 | 入库类別 | nvarchar；字节长度 510 | 是 | CharField |
| 客户 | old_客户 | 客户 | nvarchar；字节长度 510 | 是 | CharField |
| 本厂规格 | old_本厂规格 | 本厂规格 | nvarchar；字节长度 510 | 是 | CharField |
| 供应商 | old_供应商 | 供应商 | nvarchar；字节长度 510 | 是 | CharField |
| 批号 | old_批号 | 批号 | nvarchar；字节长度 510 | 是 | CharField |
| 锭重 | old_锭重 | 锭重 | float | 是 | FloatField |
| 粒数 | old_粒数 | 粒数 | nvarchar；字节长度 510 | 是 | CharField |
| 重量 | old_重量 | 重量 | float | 是 | FloatField |
| 实际重量 | old_实际重量 | 实际重量 | float | 是 | FloatField |
| 实际区域 | old_实际区域 | 实际区域 | float | 是 | FloatField |
| 半成品颜色 | old_半成品颜色 | 半成品颜色 | nvarchar；字节长度 510 | 是 | CharField |
| 区域 | old_区域 | 区域 | nvarchar；字节长度 510 | 是 | CharField |
| 半成品缸号 | old_半成品缸号 | 半成品缸号 | nvarchar；字节长度 510 | 是 | CharField |
| 采购单号 | old_采购单号 | 采购单号 | nvarchar；字节长度 510 | 是 | CharField |
| A_B | old_a_b | A_B | nvarchar；字节长度 510 | 是 | CharField |
| 件数 | old_件数 | 件数 | nvarchar；字节长度 510 | 是 | CharField |

### SourceDboAEE — 其他或待确认相关表（AEE，待确认）

源表：`dbo.AEE`；新表：`src_dbo_aee`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| 编码 | old_编码 | 编码 | nvarchar；字节长度 510 | 是 | CharField |
| 名称 | old_名称 | 名称 | nvarchar；字节长度 510 | 是 | CharField |
| 产地 | old_产地 | 产地 | nvarchar；字节长度 510 | 是 | CharField |
| 单价 | old_单价 | 单价 | money(19,4) | 是 | DecimalField |
| 数量 | old_数量 | 数量 | float | 是 | FloatField |
| 金额 | old_金额 | 金额 | money(19,4) | 是 | DecimalField |
| F7 | old_f7 | F7 | nvarchar；字节长度 510 | 是 | CharField |
| F8 | old_f8 | F8 | nvarchar；字节长度 510 | 是 | CharField |
| F9 | old_f9 | F9 | nvarchar；字节长度 510 | 是 | CharField |
| F10 | old_f10 | F10 | nvarchar；字节长度 510 | 是 | CharField |
| F11 | old_f11 | F11 | nvarchar；字节长度 510 | 是 | CharField |
| F12 | old_f12 | F12 | nvarchar；字节长度 510 | 是 | CharField |
| F13 | old_f13 | F13 | nvarchar；字节长度 510 | 是 | CharField |
| F14 | old_f14 | F14 | nvarchar；字节长度 510 | 是 | CharField |
| F15 | old_f15 | F15 | nvarchar；字节长度 510 | 是 | CharField |
| F16 | old_f16 | F16 | nvarchar；字节长度 510 | 是 | CharField |
| F17 | old_f17 | F17 | nvarchar；字节长度 510 | 是 | CharField |
| F18 | old_f18 | F18 | nvarchar；字节长度 510 | 是 | CharField |
| F19 | old_f19 | F19 | nvarchar；字节长度 510 | 是 | CharField |
| F20 | old_f20 | F20 | nvarchar；字节长度 510 | 是 | CharField |

### SourceDboC — 其他或待确认相关表（C，待确认）

源表：`dbo.C`；新表：`src_dbo_c`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| CODE | old_code | CODE | varchar；字节长度 50 | 是 | CharField |
| NAME | old_name | NAME | varchar；字节长度 50 | 是 | CharField |

### SourceDboCbbz1109 — 其他或待确认相关表（cbbz1109，待确认）

源表：`dbo.cbbz1109`；新表：`src_dbo_cbbz1109`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| kh | old_kh | kh | varchar；字节长度 50 | 是 | CharField |
| bz | old_bz | bz | varchar；字节长度 250 | 是 | CharField |

### SourceDboCkpd20221024 — 其他或待确认相关表（ckpd20221024，待确认）

源表：`dbo.ckpd20221024`；新表：`src_dbo_ckpd20221024`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| kh | old_kh | kh | varchar；字节长度 50 | 是 | CharField |
| qy | old_qy | qy | varchar；字节长度 50 | 是 | CharField |
| kw | old_kw | kw | varchar；字节长度 50 | 是 | CharField |
| card | old_card | card | varchar；字节长度 50 | 是 | CharField |
| ys | old_ys | ys | varchar；字节长度 50 | 是 | CharField |
| rolls | old_rolls | rolls | decimal(18,2) | 是 | DecimalField |
| bz | old_bz | bz | varchar；字节长度 150 | 是 | CharField |
| bz1 | old_bz1 | bz1 | varchar；字节长度 150 | 是 | CharField |
| bz2 | old_bz2 | bz2 | varchar；字节长度 150 | 是 | CharField |
| bz3 | old_bz3 | bz3 | varchar；字节长度 150 | 是 | CharField |
| bz4 | old_bz4 | bz4 | varchar；字节长度 150 | 是 | CharField |
| sumrolls | old_sumrolls | sumrolls | decimal(18,2) | 是 | DecimalField |

### SourceDboCkpd20221024bak — 其他或待确认相关表（ckpd20221024bak，待确认）

源表：`dbo.ckpd20221024bak`；新表：`src_dbo_ckpd20221024bak`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| kh | old_kh | kh | varchar；字节长度 50 | 是 | CharField |
| qy | old_qy | qy | varchar；字节长度 50 | 是 | CharField |
| kw | old_kw | kw | varchar；字节长度 50 | 是 | CharField |
| card | old_card | card | varchar；字节长度 50 | 是 | CharField |
| ys | old_ys | ys | varchar；字节长度 50 | 是 | CharField |
| rolls | old_rolls | rolls | decimal(18,2) | 是 | DecimalField |
| bz | old_bz | bz | varchar；字节长度 150 | 是 | CharField |
| bz1 | old_bz1 | bz1 | varchar；字节长度 150 | 是 | CharField |
| bz2 | old_bz2 | bz2 | varchar；字节长度 150 | 是 | CharField |
| bz3 | old_bz3 | bz3 | varchar；字节长度 150 | 是 | CharField |
| bz4 | old_bz4 | bz4 | varchar；字节长度 150 | 是 | CharField |
| sumrolls | old_sumrolls | sumrolls | decimal(18,2) | 是 | DecimalField |

### SourceDboCkpd20221027 — 其他或待确认相关表（ckpd20221027，待确认）

源表：`dbo.ckpd20221027`；新表：`src_dbo_ckpd20221027`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| kh | old_kh | kh | varchar；字节长度 50 | 是 | CharField |
| qy | old_qy | qy | varchar；字节长度 50 | 是 | CharField |
| kw | old_kw | kw | varchar；字节长度 50 | 是 | CharField |
| card | old_card | card | varchar；字节长度 50 | 是 | CharField |
| ys | old_ys | ys | varchar；字节长度 50 | 是 | CharField |
| rolls | old_rolls | rolls | decimal(18,2) | 是 | DecimalField |
| bz | old_bz | bz | varchar；字节长度 150 | 是 | CharField |
| bz1 | old_bz1 | bz1 | varchar；字节长度 150 | 是 | CharField |
| 类型 | old_类型 | 类型 | varchar；字节长度 150 | 是 | CharField |

### SourceDboCksgz20221024 — 其他或待确认相关表（cksgz20221024，待确认）

源表：`dbo.cksgz20221024`；新表：`src_dbo_cksgz20221024`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| xh | old_xh | xh | varchar；字节长度 50 | 是 | CharField |
| rkrq | old_rkrq | rkrq | date | 是 | DateField |
| kh | old_kh | kh | varchar；字节长度 50 | 是 | CharField |
| card | old_card | card | varchar；字节长度 50 | 是 | CharField |
| cp | old_cp | cp | varchar；字节长度 150 | 是 | CharField |
| ys | old_ys | ys | varchar；字节长度 50 | 是 | CharField |
| sh | old_sh | sh | varchar；字节长度 50 | 是 | CharField |
| qy | old_qy | qy | varchar；字节长度 50 | 是 | CharField |
| kw | old_kw | kw | varchar；字节长度 50 | 是 | CharField |
| rolls | old_rolls | rolls | decimal(18,2) | 是 | DecimalField |
| pz | old_pz | pz | decimal(18,2) | 是 | DecimalField |
| cz | old_cz | cz | decimal(18,2) | 是 | DecimalField |
| pdrolls | old_pdrolls | pdrolls | decimal(18,2) | 是 | DecimalField |
| bz | old_bz | bz | varchar；字节长度 250 | 是 | CharField |
| bz1 | old_bz1 | bz1 | varchar；字节长度 250 | 是 | CharField |
| bz2 | old_bz2 | bz2 | varchar；字节长度 250 | 是 | CharField |
| bz33 | old_bz33 | bz33 | varchar；字节长度 250 | 是 | CharField |

### SourceDboCpdqkc20221024 — 其他或待确认相关表（cpdqkc20221024，待确认）

源表：`dbo.cpdqkc20221024`；新表：`src_dbo_cpdqkc20221024`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| xh | old_xh | xh | varchar；字节长度 50 | 是 | CharField |
| rkrq | old_rkrq | rkrq | date | 是 | DateField |
| kh | old_kh | kh | varchar；字节长度 50 | 是 | CharField |
| card | old_card | card | varchar；字节长度 50 | 是 | CharField |
| pb | old_pb | pb | varchar；字节长度 150 | 是 | CharField |
| cp | old_cp | cp | varchar；字节长度 150 | 是 | CharField |
| sh | old_sh | sh | varchar；字节长度 50 | 是 | CharField |
| ksh | old_ksh | ksh | varchar；字节长度 50 | 是 | CharField |
| ys | old_ys | ys | varchar；字节长度 50 | 是 | CharField |
| rolls | old_rolls | rolls | decimal(18,2) | 是 | DecimalField |
| pz | old_pz | pz | decimal(18,2) | 是 | DecimalField |
| cz | old_cz | cz | decimal(18,2) | 是 | DecimalField |
| bz | old_bz | bz | varchar；字节长度 150 | 是 | CharField |
| bz1 | old_bz1 | bz1 | varchar；字节长度 150 | 是 | CharField |
| bz2 | old_bz2 | bz2 | varchar；字节长度 150 | 是 | CharField |

### SourceDboDXCHANLIANG — 其他或待确认相关表（DXCHANLIANG，待确认）

源表：`dbo.DXCHANLIANG`；新表：`src_dbo_dxchanliang`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| 日期 | old_日期 | 日期 | varchar；字节长度 50 | 是 | CharField |
| 机台 | old_机台 | 机台 | varchar；字节长度 50 | 是 | CharField |
| 数量 | old_数量 | 数量 | decimal(9,2) | 是 | DecimalField |
| 工序 | old_工序 | 工序 | varchar；字节长度 50 | 是 | CharField |

### SourceDboHypf — 其他或待确认相关表（hypf，待确认）

源表：`dbo.hypf`；新表：`src_dbo_hypf`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| RQ | old_rq | RQ | datetime | 是 | DateTimeField |
| G_SH | old_g_sh | G_SH | nvarchar；字节长度 510 | 是 | CharField |
| D_YS | old_d_ys | D_YS | nvarchar；字节长度 510 | 是 | CharField |
| G_PFH | old_g_pfh | G_PFH | nvarchar；字节长度 510 | 是 | CharField |
| G_GXH | old_g_gxh | G_GXH | nvarchar；字节长度 510 | 是 | CharField |
| G_PH | old_g_ph | G_PH | nvarchar；字节长度 510 | 是 | CharField |
| YL | old_yl | YL | float | 是 | FloatField |
| CZY | old_czy | CZY | nvarchar；字节长度 510 | 是 | CharField |
| BZ | old_bz | BZ | nvarchar；字节长度 510 | 是 | CharField |
| G_ID | old_g_id | G_ID | nvarchar；字节长度 510 | 是 | CharField |
| G_UP | old_g_up | G_UP | bit | 否 | BooleanField |
| G_UPID | old_g_upid | G_UPID | float | 是 | FloatField |
| G_ROW | old_g_row | G_ROW | float | 是 | FloatField |

### SourceDboItbak20221120 — 其他或待确认相关表（itbak20221120，待确认）

源表：`dbo.itbak20221120`；新表：`src_dbo_itbak20221120`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | int | 否 | IntegerField |
| FENCHANG | old_fenchang | FENCHANG | varchar；字节长度 50 | 是 | CharField |
| BUMEN | old_bumen | BUMEN | varchar；字节长度 50 | 是 | CharField |
| NAME | old_name | NAME | varchar；字节长度 250 | 是 | CharField |
| LEIXING | old_leixing | LEIXING | varchar；字节长度 250 | 是 | CharField |
| CPU | old_cpu | CPU | varchar；字节长度 250 | 是 | CharField |
| NEICUN | old_neicun | NEICUN | varchar；字节长度 250 | 是 | CharField |
| YINGPAN | old_yingpan | YINGPAN | varchar；字节长度 250 | 是 | CharField |
| MACADDRESS | old_macaddress | MACADDRESS | varchar；字节长度 250 | 是 | CharField |
| USER | old_user | USER | varchar；字节长度 250 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 50 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 50 | 是 | CharField |
| IsStop | old_is_stop | IsStop | bit | 是 | BooleanField |
| StopDate | old_stop_date | StopDate | datetime | 是 | DateTimeField |
| BZ | old_bz | BZ | varchar；字节长度 500 | 是 | CharField |
| sjbm | old_sjbm | sjbm | varchar；字节长度 20 | 是 | CharField |

### SourceDboItbak20221121 — 其他或待确认相关表（itbak20221121，待确认）

源表：`dbo.itbak20221121`；新表：`src_dbo_itbak20221121`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | int | 否 | IntegerField |
| FENCHANG | old_fenchang | FENCHANG | varchar；字节长度 50 | 是 | CharField |
| BUMEN | old_bumen | BUMEN | varchar；字节长度 50 | 是 | CharField |
| NAME | old_name | NAME | varchar；字节长度 250 | 是 | CharField |
| LEIXING | old_leixing | LEIXING | varchar；字节长度 250 | 是 | CharField |
| CPU | old_cpu | CPU | varchar；字节长度 250 | 是 | CharField |
| NEICUN | old_neicun | NEICUN | varchar；字节长度 250 | 是 | CharField |
| YINGPAN | old_yingpan | YINGPAN | varchar；字节长度 250 | 是 | CharField |
| MACADDRESS | old_macaddress | MACADDRESS | varchar；字节长度 250 | 是 | CharField |
| USER | old_user | USER | varchar；字节长度 250 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 50 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 50 | 是 | CharField |
| IsStop | old_is_stop | IsStop | bit | 是 | BooleanField |
| StopDate | old_stop_date | StopDate | datetime | 是 | DateTimeField |
| BZ | old_bz | BZ | varchar；字节长度 500 | 是 | CharField |
| sjbm | old_sjbm | sjbm | varchar；字节长度 20 | 是 | CharField |

### SourceDboJxtbzyq — 其他或待确认相关表（jxtbzyq，待确认）

源表：`dbo.jxtbzyq`；新表：`src_dbo_jxtbzyq`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| kh | old_kh | kh | varchar；字节长度 255 | 是 | CharField |
| ddh | old_ddh | ddh | varchar；字节长度 255 | 是 | CharField |
| bzyq | old_bzyq | bzyq | varchar；字节长度 255 | 是 | CharField |

### SourceDboJxtkckh — 其他或待确认相关表（jxtkckh，待确认）

源表：`dbo.jxtkckh`；新表：`src_dbo_jxtkckh`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| kh | old_kh | kh | varchar；字节长度 50 | 是 | CharField |

### SourceDboNHTJ — 其他或待确认相关表（NHTJ，待确认）

源表：`dbo.NHTJ`；新表：`src_dbo_nhtj`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| 日期 | old_日期 | 日期 | varchar；字节长度 50 | 是 | CharField |
| 序号 | old_序号 | 序号 | varchar；字节长度 10 | 是 | CharField |
| 类别 | old_类别 | 类别 | varchar；字节长度 50 | 是 | CharField |
| 机台编号 | old_机台编号 | 机台编号 | varchar；字节长度 50 | 是 | CharField |
| 编号 | old_编号 | 编号 | nchar；字节长度 20 | 是 | CharField |
| 部门 | old_部门 | 部门 | varchar；字节长度 50 | 是 | CharField |
| 区域位置 | old_区域位置 | 区域位置 | varchar；字节长度 50 | 是 | CharField |
| 使用说明 | old_使用说明 | 使用说明 | varchar；字节长度 250 | 是 | CharField |
| 开始 | old_开始 | 开始 | decimal(18,0) | 是 | DecimalField |
| 中间 | old_中间 | 中间 | decimal(18,0) | 是 | DecimalField |
| 结束 | old_结束 | 结束 | decimal(18,0) | 是 | DecimalField |
| 早班能耗 | old_早班能耗 | 早班能耗 | decimal(18,0) | 是 | DecimalField |
| 晚班能耗 | old_晚班能耗 | 晚班能耗 | decimal(18,0) | 是 | DecimalField |
| 当天能耗 | old_当天能耗 | 当天能耗 | decimal(18,0) | 是 | DecimalField |
| 系统开始 | old_系统开始 | 系统开始 | decimal(18,0) | 是 | DecimalField |
| 系统中间 | old_系统中间 | 系统中间 | decimal(18,0) | 是 | DecimalField |
| 系统结束 | old_系统结束 | 系统结束 | decimal(18,0) | 是 | DecimalField |
| 系统早班能耗 | old_系统早班能耗 | 系统早班能耗 | decimal(18,0) | 是 | DecimalField |
| 系统晚班能耗 | old_系统晚班能耗 | 系统晚班能耗 | decimal(18,0) | 是 | DecimalField |
| 系统当天能耗 | old_系统当天能耗 | 系统当天能耗 | decimal(18,0) | 是 | DecimalField |
| 早班差异 | old_早班差异 | 早班差异 | decimal(18,0) | 是 | DecimalField |
| 晚班差异 | old_晚班差异 | 晚班差异 | decimal(18,0) | 是 | DecimalField |
| 当天能耗差异 | old_当天能耗差异 | 当天能耗差异 | decimal(18,0) | 是 | DecimalField |
| 当天读数差异 | old_当天读数差异 | 当天读数差异 | decimal(18,0) | 是 | DecimalField |

### SourceDboPbpd20230422 — 其他或待确认相关表（pbpd20230422，待确认）

源表：`dbo.pbpd20230422`；新表：`src_dbo_pbpd20230422`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| 客户 | old_客户 | 客户 | varchar；字节长度 50 | 是 | CharField |
| 针厂 | old_针厂 | 针厂 | varchar；字节长度 50 | 是 | CharField |
| 布种 | old_布种 | 布种 | varchar；字节长度 50 | 是 | CharField |
| 条数 | old_条数 | 条数 | decimal(18,2) | 是 | DecimalField |
| 备注 | old_备注 | 备注 | varchar；字节长度 50 | 是 | CharField |

### SourceDboPS20221218 — 其他或待确认相关表（PS20221218，待确认）

源表：`dbo.PS20221218`；新表：`src_dbo_ps20221218`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| STUFFID | old_stuffid | STUFFID | varchar；字节长度 50 | 是 | CharField |
| AUTOSYSID | old_autosysid | AUTOSYSID | varchar；字节长度 50 | 是 | CharField |

### SourceDboRansechugangtongji — 其他或待确认相关表（ransechugangtongji，待确认）

源表：`dbo.ransechugangtongji`；新表：`src_dbo_ransechugangtongji`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| MachName | old_mach_name | MachName | varchar；字节长度 50 | 是 | CharField |
| bb | old_bb | bb | varchar；字节长度 50 | 是 | CharField |
| NameC | old_name_c | NameC | varchar；字节长度 50 | 是 | CharField |
| PM | old_pm | PM | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 50 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 50 | 是 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 150 | 是 | CharField |
| MachineID | old_machine_id | MachineID | varchar；字节长度 50 | 是 | CharField |
| Rolls | old_rolls | Rolls | decimal(18,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | WeightQty | decimal(18,2) | 是 | DecimalField |
| Note1 | old_note1 | Note1 | varchar；字节长度 50 | 是 | CharField |
| StartTime | old_start_time | StartTime | datetime | 是 | DateTimeField |
| EndTime | old_end_time | EndTime | datetime | 是 | DateTimeField |
| timecost | old_timecost | timecost | varchar；字节长度 50 | 是 | CharField |
| TLSJ | old_tlsj | TLSJ | varchar；字节长度 50 | 是 | CharField |

### SourceDboRansetongji — 其他或待确认相关表（ransetongji，待确认）

源表：`dbo.ransetongji`；新表：`src_dbo_ransetongji`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| 客户 | old_客户 | 客户 | varchar；字节长度 50 | 是 | CharField |
| 布种 | old_布种 | 布种 | varchar；字节长度 250 | 是 | CharField |
| 机型 | old_机型 | 机型 | varchar；字节长度 50 | 是 | CharField |
| 直通 | old_直通 | 直通 | varchar；字节长度 50 | 是 | CharField |
| 缸号 | old_缸号 | 缸号 | varchar；字节长度 150 | 是 | CharField |
| 匹数 | old_匹数 | 匹数 | decimal(18,2) | 是 | DecimalField |
| 重量 | old_重量 | 重量 | decimal(18,2) | 是 | DecimalField |
| 色号 | old_色号 | 色号 | varchar；字节长度 50 | 是 | CharField |
| 颜色 | old_颜色 | 颜色 | varchar；字节长度 150 | 是 | CharField |
| 进缸时间 | old_进缸时间 | 进缸时间 | datetime | 是 | DateTimeField |
| 出缸时间 | old_出缸时间 | 出缸时间 | datetime | 是 | DateTimeField |
| 耗时 | old_耗时 | 耗时 | varchar；字节长度 150 | 是 | CharField |
| 停留时间 | old_停留时间 | 停留时间 | varchar；字节长度 150 | 是 | CharField |

### SourceDboRCDDZJB — 其他或待确认相关表（RCDDZJB，待确认）

源表：`dbo.RCDDZJB`；新表：`src_dbo_rcddzjb`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| CustSelfNo | old_cust_self_no | CustSelfNo | varchar；字节长度 500 | 是 | CharField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 20 | 是 | CharField |
| CustFabricName | old_cust_fabric_name | CustFabricName | varchar；字节长度 250 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 150 | 是 | CharField |
| CustColorNum | old_cust_color_num | CustColorNum | varchar；字节长度 20 | 是 | CharField |
| Width | old_width | Width | varchar；字节长度 200 | 是 | CharField |
| WidthUnit | old_width_unit | WidthUnit | nvarchar；字节长度 40 | 是 | CharField |
| Weight | old_weight | Weight | varchar；字节长度 200 | 是 | CharField |
| WeightKindID | old_weight_kind_id | WeightKindID | nvarchar；字节长度 40 | 是 | CharField |
| OrderRolls | old_order_rolls | OrderRolls | decimal(10,2) | 是 | DecimalField |
| TubeWeight | old_tube_weight | TubeWeight | float | 是 | FloatField |
| AddWeigth | old_add_weigth | AddWeigth | float | 是 | FloatField |
| DlvDate | old_dlv_date | DlvDate | datetime | 是 | DateTimeField |

### SourceDboShda — 其他或待确认相关表（shda，待确认）

源表：`dbo.shda`；新表：`src_dbo_shda`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| RQ | old_rq | RQ | datetime | 是 | DateTimeField |
| SJ | old_sj | SJ | nvarchar；字节长度 510 | 是 | CharField |
| G_SH | old_g_sh | G_SH | nvarchar；字节长度 510 | 是 | CharField |
| D_YS | old_d_ys | D_YS | nvarchar；字节长度 510 | 是 | CharField |
| G_PFH | old_g_pfh | G_PFH | nvarchar；字节长度 510 | 是 | CharField |
| G_LBH | old_g_lbh | G_LBH | nvarchar；字节长度 510 | 是 | CharField |
| D_YSLB | old_d_yslb | D_YSLB | nvarchar；字节长度 510 | 是 | CharField |
| G_KHSH | old_g_khsh | G_KHSH | nvarchar；字节长度 510 | 是 | CharField |
| G_KH | old_g_kh | G_KH | nvarchar；字节长度 510 | 是 | CharField |
| G_PH | old_g_ph | G_PH | nvarchar；字节长度 510 | 是 | CharField |
| D_PM | old_d_pm | D_PM | nvarchar；字节长度 510 | 是 | CharField |
| D_PBLB | old_d_pblb | D_PBLB | nvarchar；字节长度 510 | 是 | CharField |
| PBKZ | old_pbkz | PBKZ | nvarchar；字节长度 510 | 是 | CharField |
| TSLJJ | old_tsljj | TSLJJ | nvarchar；字节长度 510 | 是 | CharField |
| D_RLLB | old_d_rllb | D_RLLB | nvarchar；字节长度 510 | 是 | CharField |
| LD | old_ld | LD | nvarchar；字节长度 510 | 是 | CharField |
| SC | old_sc | SC | nvarchar；字节长度 510 | 是 | CharField |
| HB | old_hb | HB | nvarchar；字节长度 510 | 是 | CharField |
| DSGY | old_dsgy | DSGY | nvarchar；字节长度 510 | 是 | CharField |
| G_JY | old_g_jy | G_JY | float | 是 | FloatField |
| F_YB | old_f_yb | F_YB | float | 是 | FloatField |
| G_GYH | old_g_gyh | G_GYH | nvarchar；字节长度 510 | 是 | CharField |
| F_GY | old_f_gy | F_GY | nvarchar；字节长度 510 | 是 | CharField |
| F_LCMC | old_f_lcmc | F_LCMC | nvarchar；字节长度 510 | 是 | CharField |
| F_DY | old_f_dy | F_DY | nvarchar；字节长度 510 | 是 | CharField |
| F_KLD | old_f_kld | F_KLD | nvarchar；字节长度 510 | 是 | CharField |
| F_DABH | old_f_dabh | F_DABH | nvarchar；字节长度 510 | 是 | CharField |
| DYY | old_dyy | DYY | nvarchar；字节长度 510 | 是 | CharField |
| CZY | old_czy | CZY | nvarchar；字节长度 510 | 是 | CharField |
| BZ | old_bz | BZ | nvarchar；字节长度 510 | 是 | CharField |
| G_ID | old_g_id | G_ID | nvarchar；字节长度 510 | 是 | CharField |
| G_UP | old_g_up | G_UP | bit | 否 | BooleanField |
| G_UPID | old_g_upid | G_UPID | nvarchar；字节长度 510 | 是 | CharField |
| G_ROW | old_g_row | G_ROW | float | 是 | FloatField |

### SourceDboSHIFT — 生产工单与排程相关表（SHIFT，待确认）

源表：`dbo.SHIFT`；新表：`src_dbo_shift`；原主键：SHIFTID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SHIFTID | old_shiftid | SHIFTID | int | 否 | IntegerField |
| NAME | old_name | NAME | varchar；字节长度 20 | 是 | CharField |
| USHIFTID | old_ushiftid | USHIFTID | int | 是 | IntegerField |
| STARTDATE | old_startdate | STARTDATE | datetime | 否 | DateTimeField |
| ENDDATE | old_enddate | ENDDATE | datetime | 是 | DateTimeField |
| RUNNUM | old_runnum | RUNNUM | smallint | 是 | IntegerField |
| SCH1 | old_sch1 | SCH1 | int | 是 | IntegerField |
| SCH2 | old_sch2 | SCH2 | int | 是 | IntegerField |
| SCH3 | old_sch3 | SCH3 | int | 是 | IntegerField |
| SCH4 | old_sch4 | SCH4 | int | 是 | IntegerField |
| SCH5 | old_sch5 | SCH5 | int | 是 | IntegerField |
| SCH6 | old_sch6 | SCH6 | int | 是 | IntegerField |
| SCH7 | old_sch7 | SCH7 | int | 是 | IntegerField |
| SCH8 | old_sch8 | SCH8 | int | 是 | IntegerField |
| SCH9 | old_sch9 | SCH9 | int | 是 | IntegerField |
| SCH10 | old_sch10 | SCH10 | int | 是 | IntegerField |
| SCH11 | old_sch11 | SCH11 | int | 是 | IntegerField |
| SCH12 | old_sch12 | SCH12 | int | 是 | IntegerField |
| CYCLE | old_cycle | CYCLE | smallint | 是 | IntegerField |
| UNITS | old_units | UNITS | smallint | 是 | IntegerField |

### SourceDboSHLEIXING — 其他或待确认相关表（SHLEIXING，待确认）

源表：`dbo.SHLEIXING`；新表：`src_dbo_shleixing`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| CODE | old_code | CODE | varchar；字节长度 20 | 是 | CharField |
| lx | old_lx | lx | varchar；字节长度 20 | 是 | CharField |
| LXNAME | old_lxname | LXNAME | varchar；字节长度 50 | 是 | CharField |

### SourceDboTmp20221104 — 其他或待确认相关表（tmp20221104，待确认）

源表：`dbo.tmp20221104`；新表：`src_dbo_tmp20221104`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |

### SourceDboXxtcbkc20221023 — 其他或待确认相关表（xxtcbkc20221023，待确认）

源表：`dbo.xxtcbkc20221023`；新表：`src_dbo_xxtcbkc20221023`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| kh | old_kh | kh | varchar；字节长度 50 | 是 | CharField |
| qy | old_qy | qy | varchar；字节长度 50 | 是 | CharField |
| kw | old_kw | kw | varchar；字节长度 50 | 是 | CharField |
| card | old_card | card | varchar；字节长度 50 | 是 | CharField |
| ys | old_ys | ys | varchar；字节长度 50 | 是 | CharField |
| ps | old_ps | ps | decimal(18,2) | 是 | DecimalField |
| bz1 | old_bz1 | bz1 | varchar；字节长度 250 | 是 | CharField |
| bz2 | old_bz2 | bz2 | varchar；字节长度 250 | 是 | CharField |
| bj | old_bj | bj | varchar；字节长度 250 | 是 | CharField |

### SourceDboXxtzzp20221024 — 其他或待确认相关表（xxtzzp20221024，待确认）

源表：`dbo.xxtzzp20221024`；新表：`src_dbo_xxtzzp20221024`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| KH | old_kh | KH | varchar；字节长度 50 | 是 | CharField |
| CARD | old_card | CARD | varchar；字节长度 50 | 是 | CharField |
| OLDCARD | old_oldcard | OLDCARD | varchar；字节长度 50 | 是 | CharField |
| PB | old_pb | PB | varchar；字节长度 150 | 是 | CharField |
| CP | old_cp | CP | varchar；字节长度 150 | 是 | CharField |
| SH | old_sh | SH | varchar；字节长度 50 | 是 | CharField |
| YS | old_ys | YS | varchar；字节长度 50 | 是 | CharField |
| PS | old_ps | PS | decimal(18,2) | 是 | DecimalField |
| PBSL | old_pbsl | PBSL | decimal(18,2) | 是 | DecimalField |
| JINDU | old_jindu | JINDU | varchar；字节长度 150 | 是 | CharField |
| PT | old_pt | PT | datetime | 是 | DateTimeField |
| BZ1 | old_bz1 | BZ1 | varchar；字节长度 150 | 是 | CharField |
| BZ2 | old_bz2 | BZ2 | varchar；字节长度 150 | 是 | CharField |
| BZ3 | old_bz3 | BZ3 | varchar；字节长度 150 | 是 | CharField |

### SourceDboZhenzhibaobiao — 其他或待确认相关表（zhenzhibaobiao，待确认）

源表：`dbo.zhenzhibaobiao`；新表：`src_dbo_zhenzhibaobiao`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| 日期 | old_日期 | 日期 | date | 是 | DateField |
| 下单 | old_下单 | 下单 | int | 是 | IntegerField |
| 下单匹数 | old_下单匹数 | 下单匹数 | decimal(38,2) | 是 | DecimalField |
| 下单数量 | old_下单数量 | 下单数量 | decimal(38,2) | 是 | DecimalField |
| 正常开卡 | old_正常开卡 | 正常开卡 | int | 是 | IntegerField |
| 预配匹数 | old_预配匹数 | 预配匹数 | decimal(38,2) | 是 | DecimalField |
| 预配数量 | old_预配数量 | 预配数量 | decimal(38,2) | 是 | DecimalField |
| 回修开卡 | old_回修开卡 | 回修开卡 | int | 是 | IntegerField |
| 回修预配匹数 | old_回修预配匹数 | 回修预配匹数 | decimal(38,2) | 是 | DecimalField |
| 回修预配数量 | old_回修预配数量 | 回修预配数量 | decimal(38,2) | 是 | DecimalField |
| 在制品缸数 | old_在制品缸数 | 在制品缸数 | int | 是 | IntegerField |
| 在制品匹数 | old_在制品匹数 | 在制品匹数 | decimal(38,2) | 是 | DecimalField |
| 在制品数量 | old_在制品数量 | 在制品数量 | decimal(38,2) | 是 | DecimalField |
| 出缸数 | old_出缸数 | 出缸数 | int | 是 | IntegerField |
| 出缸匹数 | old_出缸匹数 | 出缸匹数 | decimal(38,2) | 是 | DecimalField |
| 出缸数量 | old_出缸数量 | 出缸数量 | decimal(38,2) | 是 | DecimalField |
| 成定缸数 | old_成定缸数 | 成定缸数 | int | 是 | IntegerField |
| 成定匹数 | old_成定匹数 | 成定匹数 | decimal(38,3) | 是 | DecimalField |
| 成定数量 | old_成定数量 | 成定数量 | decimal(38,3) | 是 | DecimalField |
| 打卷缸数 | old_打卷缸数 | 打卷缸数 | int | 是 | IntegerField |
| 打卷坯重 | old_打卷坯重 | 打卷坯重 | decimal(38,2) | 是 | DecimalField |
| 打卷成品重 | old_打卷成品重 | 打卷成品重 | decimal(38,2) | 是 | DecimalField |
| 入库单数 | old_入库单数 | 入库单数 | int | 是 | IntegerField |
| 入库匹数 | old_入库匹数 | 入库匹数 | decimal(38,2) | 是 | DecimalField |
| 入库坯重 | old_入库坯重 | 入库坯重 | decimal(38,2) | 是 | DecimalField |
| 入库成品重 | old_入库成品重 | 入库成品重 | decimal(38,2) | 是 | DecimalField |
| 库存成品匹数 | old_库存成品匹数 | 库存成品匹数 | decimal(38,2) | 是 | DecimalField |
| 库存成品坯重 | old_库存成品坯重 | 库存成品坯重 | decimal(38,2) | 是 | DecimalField |
| 库存成品重量 | old_库存成品重量 | 库存成品重量 | decimal(38,2) | 是 | DecimalField |
| 库存坯布匹数 | old_库存坯布匹数 | 库存坯布匹数 | decimal(38,2) | 是 | DecimalField |
| 库存坯重 | old_库存坯重 | 库存坯重 | decimal(38,2) | 是 | DecimalField |

### SourceDboZJHXMXBB — 其他或待确认相关表（ZJHXMXBB，待确认）

源表：`dbo.ZJHXMXBB`；新表：`src_dbo_zjhxmxbb`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| 序号 | old_序号 | 序号 | varchar；字节长度 10 | 是 | CharField |
| 日期 | old_日期 | 日期 | date | 是 | DateField |
| 客户 | old_客户 | 客户 | varchar；字节长度 50 | 是 | CharField |
| 缸号 | old_缸号 | 缸号 | varchar；字节长度 50 | 是 | CharField |
| 布种 | old_布种 | 布种 | varchar；字节长度 50 | 是 | CharField |
| 颜色 | old_颜色 | 颜色 | varchar；字节长度 50 | 是 | CharField |
| 原缸条数 | old_原缸条数 | 原缸条数 | decimal(9,1) | 是 | DecimalField |
| 抽疋条数 | old_抽疋条数 | 抽疋条数 | decimal(9,1) | 是 | DecimalField |
| 异常原因 | old_异常原因 | 异常原因 | varchar；字节长度 500 | 是 | CharField |
| 责任部门 | old_责任部门 | 责任部门 | varchar；字节长度 50 | 是 | CharField |
| 责任人 | old_责任人 | 责任人 | varchar；字节长度 50 | 是 | CharField |
| 处理方案 | old_处理方案 | 处理方案 | varchar；字节长度 500 | 是 | CharField |
| 完成时间 | old_完成时间 | 完成时间 | varchar；字节长度 50 | 是 | CharField |
| 备注 | old_备注 | 备注 | varchar；字节长度 500 | 是 | CharField |
| 处罚金额 | old_处罚金额 | 处罚金额 | varchar；字节长度 500 | 是 | CharField |

### SourceDyeACGroup — 其他或待确认相关表（ACGroup，待确认）

源表：`dye.ACGroup`；新表：`src_dye_acgroup`；原主键：GroupID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| GroupID | old_group_id | GroupID | smallint | 否 | IntegerField |
| Name | old_name | Name | varchar；字节长度 30 | 是 | CharField |
| TimeZone1 | old_time_zone1 | TimeZone1 | smallint | 是 | IntegerField |
| TimeZone2 | old_time_zone2 | TimeZone2 | smallint | 是 | IntegerField |
| TimeZone3 | old_time_zone3 | TimeZone3 | smallint | 是 | IntegerField |
| holidayvaild | old_holidayvaild | holidayvaild | bit | 是 | BooleanField |
| verifystyle | old_verifystyle | verifystyle | int | 是 | IntegerField |

### SourceDyeAcholiday — 其他或待确认相关表（acholiday，待确认）

源表：`dye.acholiday`；新表：`src_dye_acholiday`；原主键：primaryid。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| begindate | old_begindate | begindate | datetime | 是 | DateTimeField |
| enddate | old_enddate | enddate | datetime | 是 | DateTimeField |
| holidayid | old_holidayid | holidayid | int | 是 | IntegerField |
| primaryid | old_primaryid | primaryid | int | 否 | IntegerField |
| timezone | old_timezone | timezone | int | 是 | IntegerField |

### SourceDyeACUnlockComb — 其他或待确认相关表（ACUnlockComb，待确认）

源表：`dye.ACUnlockComb`；新表：`src_dye_acunlockcomb`；原主键：UnlockCombID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| UnlockCombID | old_unlock_comb_id | UnlockCombID | smallint | 否 | IntegerField |
| Name | old_name | Name | varchar；字节长度 30 | 是 | CharField |
| Group01 | old_group01 | Group01 | smallint | 是 | IntegerField |
| Group02 | old_group02 | Group02 | smallint | 是 | IntegerField |
| Group03 | old_group03 | Group03 | smallint | 是 | IntegerField |
| Group04 | old_group04 | Group04 | smallint | 是 | IntegerField |
| Group05 | old_group05 | Group05 | smallint | 是 | IntegerField |

### SourceDyeAPPUploadFilesInfo — 其他或待确认相关表（APPUploadFilesInfo，待确认）

源表：`dye.APPUploadFilesInfo`；新表：`src_dye_appuploadfilesinfo`；原主键：Guid。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 是 | CharField |
| Kind | old_kind | Kind | int | 是 | IntegerField |
| uiIndex | old_ui_index | uiIndex | int | 是 | IntegerField |
| Guid | old_guid | Guid | varchar；字节长度 50 | 否 | CharField |
| OriFileName | old_ori_file_name | OriFileName | nvarchar；字节长度 200 | 是 | CharField |
| SaveFileName | old_save_file_name | SaveFileName | nvarchar；字节长度 400 | 是 | CharField |
| FileNameUrl | old_file_name_url | FileNameUrl | nvarchar；字节长度 400 | 是 | CharField |
| SaveDate | old_save_date | SaveDate | datetime | 是 | DateTimeField |
| UserID | old_user_id | UserID | varchar；字节长度 20 | 是 | CharField |
| fileType | old_file_type | fileType | varchar；字节长度 20 | 是 | CharField |

### SourceDyeAPPUploadFilesInfoDel — 其他或待确认相关表（APPUploadFilesInfoDel，待确认）

源表：`dye.APPUploadFilesInfoDel`；新表：`src_dye_appuploadfilesinfodel`；原主键：Guid。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 是 | CharField |
| Kind | old_kind | Kind | int | 是 | IntegerField |
| uiIndex | old_ui_index | uiIndex | int | 是 | IntegerField |
| Guid | old_guid | Guid | varchar；字节长度 50 | 否 | CharField |
| OriFileName | old_ori_file_name | OriFileName | nvarchar；字节长度 200 | 是 | CharField |
| SaveFileName | old_save_file_name | SaveFileName | nvarchar；字节长度 400 | 是 | CharField |
| FileNameUrl | old_file_name_url | FileNameUrl | nvarchar；字节长度 400 | 是 | CharField |
| SaveDate | old_save_date | SaveDate | datetime | 是 | DateTimeField |
| UserID | old_user_id | UserID | varchar；字节长度 20 | 是 | CharField |
| DeletePerson | old_delete_person | DeletePerson | varchar；字节长度 20 | 是 | CharField |
| DeleteDate | old_delete_date | DeleteDate | datetime | 是 | DateTimeField |
| fileType | old_file_type | fileType | varchar；字节长度 20 | 是 | CharField |

### SourceDyeArrivalNotice — 其他或待确认相关表（ArrivalNotice，待确认）

源表：`dye.ArrivalNotice`；新表：`src_dye_arrivalnotice`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商代码 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |

### SourceDyeArrivalNoticeDetail — 其他或待确认相关表（ArrivalNoticeDetail，待确认）

源表：`dye.ArrivalNoticeDetail`；新表：`src_dye_arrivalnoticedetail`；原主键：DetailNo。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 表单明细号（子表） | varchar；字节长度 20 | 否 | CharField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 10 | 否 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 10 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| ColorE | old_color_e | 颜色英文名 | varchar；字节长度 20 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| StockUnit | old_stock_unit | 库存单位 | tinyint | 是 | IntegerField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| JobDetailNo | old_job_detail_no | 加工作业号 | varchar；字节长度 20 | 是 | CharField |
| PurDetailNo | old_pur_detail_no | 采购单明细号 | varchar；字节长度 20 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyeArrivalNotice`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ArivalNoticeDetail → ArrivalNotice。

### SourceDyeAttachment — 其他或待确认相关表（Attachment，待确认）

源表：`dye.Attachment`；新表：`src_dye_attachment`；原主键：ID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | varchar；字节长度 50 | 否 | CharField |
| RowNo | old_row_no | RowNo | smallint | 是 | IntegerField |
| DataTableName | old_data_table_name | DataTableName | varchar；字节长度 50 | 是 | CharField |
| FieldValues | old_field_values | FieldValues | varchar；字节长度 1000 | 是 | CharField |
| FilePath | old_file_path | FilePath | varchar；字节长度 500 | 是 | CharField |
| FileName | old_file_name | FileName | varchar；字节长度 100 | 是 | CharField |
| FileType | old_file_type | FileType | varchar；字节长度 10 | 是 | CharField |
| FileSize | old_file_size | FileSize | int | 是 | IntegerField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| Description | old_description | Description | varchar；字节长度 500 | 是 | CharField |

### SourceDyeAttParam — 系统平台与配置相关表（AttParam，待确认）

源表：`dye.AttParam`；新表：`src_dye_attparam`；原主键：PARANAME。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| PARANAME | old_paraname | PARANAME | varchar；字节长度 20 | 否 | CharField |
| PARATYPE | old_paratype | PARATYPE | varchar；字节长度 2 | 是 | CharField |
| PARAVALUE | old_paravalue | PARAVALUE | varchar；字节长度 100 | 否 | CharField |

### SourceDyeAuditedExc — 其他或待确认相关表（AuditedExc，待确认）

源表：`dye.AuditedExc`；新表：`src_dye_auditedexc`；原主键：AEID。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| AEID | old_aeid | AEID | int | 否 | IntegerField |
| UserId | old_user_id | UserId | int | 是 | IntegerField |
| CheckTime | old_check_time | CheckTime | datetime | 否 | DateTimeField |
| NewExcID | old_new_exc_id | NewExcID | int | 是 | IntegerField |
| IsLeave | old_is_leave | IsLeave | smallint | 是 | IntegerField |
| UName | old_uname | UName | varchar；字节长度 20 | 是 | CharField |
| UTime | old_utime | UTime | datetime | 否 | DateTimeField |

### SourceDyeAUTHDEVICE — 设备维护与能耗相关表（AUTHDEVICE，待确认）

源表：`dye.AUTHDEVICE`；新表：`src_dye_authdevice`；原主键：USERID, MachineID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | int | 否 | IntegerField |
| USERID | old_userid | USERID | int | 否 | IntegerField |
| MachineID | old_machine_id | MachineID | int | 否 | IntegerField |

### SourceDyeBalancingConditions — 其他或待确认相关表（BalancingConditions，待确认）

源表：`dye.BalancingConditions`；新表：`src_dye_balancingconditions`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 30 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 30 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| Rolls | old_rolls | Rolls | decimal(7,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | WeightQty | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | LengthQty | decimal(10,2) | 是 | DecimalField |
| Creater | old_creater | Creater | nchar；字节长度 40 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | nchar；字节长度 40 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |

### SourceDyeBaseCase — 其他或待确认相关表（BaseCase，待确认）

源表：`dye.BaseCase`；新表：`src_dye_basecase`；原主键：SheetSeries。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 类型 | smallint | 是 | IntegerField |
| CaseName | old_case_name | 方案名称 | nvarchar；字节长度 100 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 制单人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 制单日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |

### SourceDyeBaseCaseDetail — 其他或待确认相关表（BaseCaseDetail，待确认）

源表：`dye.BaseCaseDetail`；新表：`src_dye_basecasedetail`；原主键：SheetSeries, DetailNo。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 36 | 否 | CharField |
| SortNo | old_sort_no | 排序序号 | int | 是 | IntegerField |
| SerialNum | old_serial_num | 序号 | nvarchar；字节长度 20 | 是 | CharField |
| ProjectInfo | old_project_info | 项目内容 | nvarchar；字节长度 400 | 是 | CharField |
| DefaultValue | old_default_value | 常规值 | nvarchar；字节长度 200 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| IsInputText | old_is_input_text | 是否输入文本 | bit | 是 | BooleanField |

关联 `source_parent_1` → `erp_base.SourceDyeBaseCase`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 BaseCaseDetail → BaseCase。

### SourceDyeBiotemplate — 基础主数据相关表（Biotemplate，待确认）

源表：`dye.Biotemplate`；新表：`src_dye_biotemplate`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | int | 否 | IntegerField |
| USER_ID | old_user_id | USER_ID | int | 是 | IntegerField |
| user_pin | old_user_pin | user_pin | varchar；字节长度 50 | 是 | CharField |
| create_operator | old_create_operator | create_operator | varchar；字节长度 50 | 是 | CharField |
| create_time | old_create_time | create_time | datetime | 是 | DateTimeField |
| valid_flag | old_valid_flag | valid_flag | int | 是 | IntegerField |
| is_duress | old_is_duress | is_duress | int | 是 | IntegerField |
| bio_type | old_bio_type | bio_type | int | 是 | IntegerField |
| version | old_version | version | varchar；字节长度 50 | 是 | CharField |
| data_format | old_data_format | data_format | int | 是 | IntegerField |
| template_no | old_template_no | template_no | int | 是 | IntegerField |
| template_no_index | old_template_no_index | template_no_index | int | 是 | IntegerField |
| Template_Data | old_template_data | Template_Data | varchar；字节长度 -1 | 是 | TextField |
| nOldType | old_n_old_type | nOldType | int | 是 | IntegerField |

### SourceDyeClockShift — 生产工单与排程相关表（ClockShift，待确认）

源表：`dye.ClockShift`；新表：`src_dye_clockshift`；原主键：EmpID, ShiftCode。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| EmpID | old_emp_id | EmpID | varchar；字节长度 20 | 否 | CharField |
| ShiftCode | old_shift_code | ShiftCode | varchar；字节长度 20 | 否 | CharField |
| CreateTime | old_create_time | CreateTime | datetime | 否 | DateTimeField |

### SourceDyeCompensatedetail — 其他或待确认相关表（compensatedetail，待确认）

源表：`dye.compensatedetail`；新表：`src_dye_compensatedetail`；原主键：SheetSeries, DetailNo。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 20 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 20 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 20 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 200 | 是 | CharField |
| CustomerProdName | old_customer_prod_name | CustomerProdName | varchar；字节长度 200 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 20 | 是 | CharField |
| CustColorNum | old_cust_color_num | CustColorNum | varchar；字节长度 150 | 是 | CharField |
| Weight | old_weight | Weight | varchar；字节长度 256 | 是 | CharField |
| Width | old_width | Width | varchar；字节长度 256 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | WeightQty | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | LengthQty | decimal(10,2) | 是 | DecimalField |
| Description | old_description | Description | varchar；字节长度 512 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| QualityDeductionSheetNo | old_quality_deduction_sheet_no | QualityDeductionSheetNo | varchar；字节长度 32 | 是 | CharField |
| GrayQty | old_gray_qty | GrayQty | decimal(10,2) | 是 | DecimalField |
| qy | old_qy | qy | varchar；字节长度 150 | 是 | CharField |
| kw | old_kw | kw | varchar；字节长度 150 | 是 | CharField |
| PayMoney | old_pay_money | PayMoney | decimal(7,2) | 是 | DecimalField |
| PayQTY | old_pay_qty | PayQTY | decimal(7,2) | 是 | DecimalField |

关联 `source_parent_1` → `erp_base.SourceDyeCompensatemain`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 compensatedetail → compensatemain。

### SourceDyeCompensatemain — 其他或待确认相关表（compensatemain，待确认）

源表：`dye.compensatemain`；新表：`src_dye_compensatemain`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| PendOutSheetSeries | old_pend_out_sheet_series | PendOutSheetSeries | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 20 | 是 | CharField |

### SourceDyeCookIn — 其他或待确认相关表（CookIn，待确认）

源表：`dye.CookIn`；新表：`src_dye_cookin`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| InKindID | old_in_kind_id | 入库类别 | varchar；字节长度 10 | 是 | CharField |
| BuyerID | old_buyer_id | 采购员 | varchar；字节长度 50 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库代码 | varchar；字节长度 10 | 是 | CharField |
| SupplierID | old_supplier_id | 结算方式 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| Keeper | old_keeper | 仓管员 | varchar；字节长度 10 | 是 | CharField |
| Reason | old_reason | Reason | nvarchar；字节长度 512 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| Settle | old_settle | Settle | varchar；字节长度 50 | 是 | CharField |
| deliverynum | old_deliverynum | deliverynum | varchar；字节长度 50 | 是 | CharField |
| APMoney | old_apmoney | APMoney | decimal(10,2) | 是 | DecimalField |
| APQty | old_apqty | APQty | decimal(10,2) | 是 | DecimalField |
| UnClearQty | old_un_clear_qty | UnClearQty | decimal(10,2) | 是 | DecimalField |
| UnClearMoney | old_un_clear_money | UnClearMoney | decimal(10,2) | 是 | DecimalField |
| UnClearInvoiceQty | old_un_clear_invoice_qty | UnClearInvoiceQty | decimal(10,2) | 是 | DecimalField |
| UnClearInvoiceMoney | old_un_clear_invoice_money | UnClearInvoiceMoney | decimal(10,2) | 是 | DecimalField |
| DiscountMoney | old_discount_money | DiscountMoney | decimal(10,2) | 是 | DecimalField |
| SumAmount | old_sum_amount | SumAmount | decimal(10,2) | 是 | DecimalField |
| InvoiceClearStatus | old_invoice_clear_status | InvoiceClearStatus | tinyint | 是 | IntegerField |
| MoneyClearStatus | old_money_clear_status | MoneyClearStatus | tinyint | 是 | IntegerField |

### SourceDyeDEPARTMENTS — 其他或待确认相关表（DEPARTMENTS，待确认）

源表：`dye.DEPARTMENTS`；新表：`src_dye_departments`；原主键：DEPTID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| DEPTID | old_deptid | DEPTID | int | 否 | IntegerField |
| DEPTNAME | old_deptname | DEPTNAME | varchar；字节长度 30 | 是 | CharField |
| SUPDEPTID | old_supdeptid | SUPDEPTID | int | 否 | IntegerField |
| InheritParentSch | old_inherit_parent_sch | InheritParentSch | smallint | 是 | IntegerField |
| InheritDeptSch | old_inherit_dept_sch | InheritDeptSch | smallint | 是 | IntegerField |
| InheritDeptSchClass | old_inherit_dept_sch_class | InheritDeptSchClass | smallint | 是 | IntegerField |
| AutoSchPlan | old_auto_sch_plan | AutoSchPlan | smallint | 是 | IntegerField |
| InLate | old_in_late | InLate | smallint | 是 | IntegerField |
| OutEarly | old_out_early | OutEarly | smallint | 是 | IntegerField |
| InheritDeptRule | old_inherit_dept_rule | InheritDeptRule | smallint | 是 | IntegerField |
| MinAutoSchInterval | old_min_auto_sch_interval | MinAutoSchInterval | int | 是 | IntegerField |
| RegisterOT | old_register_ot | RegisterOT | smallint | 是 | IntegerField |
| DefaultSchId | old_default_sch_id | DefaultSchId | int | 否 | IntegerField |
| ATT | old_att | ATT | smallint | 是 | IntegerField |
| Holiday | old_holiday | Holiday | smallint | 是 | IntegerField |
| OverTime | old_over_time | OverTime | smallint | 是 | IntegerField |
| Code | old_code | Code | varchar；字节长度 10 | 是 | CharField |

### SourceDyeDeptUsedSchs — 其他或待确认相关表（DeptUsedSchs，待确认）

源表：`dye.DeptUsedSchs`；新表：`src_dye_deptusedschs`；原主键：DeptId, SchId。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| DeptId | old_dept_id | DeptId | int | 否 | IntegerField |
| SchId | old_sch_id | SchId | int | 否 | IntegerField |

### SourceDyeDyeProcessPrice — 财务结算与成本相关表（DyeProcessPrice，待确认）

源表：`dye.DyeProcessPrice`；新表：`src_dye_dyeprocessprice`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 编号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 时间 | datetime | 是 | DateTimeField |
| GrayKindID | old_gray_kind_id | 纱类 | varchar；字节长度 10 | 是 | CharField |
| PhaseID | old_phase_id | 染程 | varchar；字节长度 10 | 是 | CharField |
| MachineKindID | old_machine_kind_id | 机台管数 | varchar；字节长度 10 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | nvarchar；字节长度 100 | 是 | CharField |
| Price | old_price | 单价 | decimal(16,6) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyeEmpRoom — 基础主数据相关表（Emp_Room，待确认）

源表：`dye.Emp_Room`；新表：`src_dye_emp_room`；原主键：RoomNo。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| RoomNo | old_room_no | 房间号 | varchar；字节长度 10 | 否 | CharField |
| EmpID1 | old_emp_id1 | 员工1 | varchar；字节长度 10 | 是 | CharField |
| EmpID2 | old_emp_id2 | 员工2 | varchar；字节长度 10 | 是 | CharField |
| EmpID3 | old_emp_id3 | 员工3 | varchar；字节长度 10 | 是 | CharField |
| EmpID4 | old_emp_id4 | 员工4 | varchar；字节长度 10 | 是 | CharField |
| EmpID5 | old_emp_id5 | 员工5 | varchar；字节长度 10 | 是 | CharField |
| EmpID6 | old_emp_id6 | 员工6 | varchar；字节长度 10 | 是 | CharField |
| EmpID7 | old_emp_id7 | 员工7 | varchar；字节长度 10 | 是 | CharField |
| EmpID8 | old_emp_id8 | 员工8 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 50 | 是 | CharField |
| EmpID9 | old_emp_id9 | 员工9 | varchar；字节长度 10 | 是 | CharField |
| EmpID10 | old_emp_id10 | 员工10 | varchar；字节长度 10 | 是 | CharField |

### SourceDyeEnableCard — 其他或待确认相关表（EnableCard，待确认）

源表：`dye.EnableCard`；新表：`src_dye_enablecard`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 30 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 30 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| FirstCard | old_first_card | FirstCard | bit | 是 | BooleanField |
| SecondCard | old_second_card | SecondCard | bit | 是 | BooleanField |
| Creater | old_creater | Creater | nchar；字节长度 40 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | nchar；字节长度 40 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |

### SourceDyeEXCNOTES — 其他或待确认相关表（EXCNOTES，待确认）

源表：`dye.EXCNOTES`；新表：`src_dye_excnotes`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| USERID | old_userid | USERID | int | 是 | IntegerField |
| ATTDATE | old_attdate | ATTDATE | datetime | 是 | DateTimeField |
| NOTES | old_notes | NOTES | varchar；字节长度 200 | 是 | CharField |

### SourceDyeFaceTemp — 基础主数据相关表（FaceTemp，待确认）

源表：`dye.FaceTemp`；新表：`src_dye_facetemp`；原主键：TEMPLATEID。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| TEMPLATEID | old_templateid | TEMPLATEID | int | 否 | IntegerField |
| USERNO | old_userno | USERNO | varchar；字节长度 24 | 是 | CharField |
| SIZE | old_size | SIZE | int | 是 | IntegerField |
| pin | old_pin | pin | int | 是 | IntegerField |
| FACEID | old_faceid | FACEID | int | 是 | IntegerField |
| VALID | old_valid | VALID | int | 是 | IntegerField |
| RESERVE | old_reserve | RESERVE | int | 是 | IntegerField |
| ACTIVETIME | old_activetime | ACTIVETIME | int | 是 | IntegerField |
| VFCOUNT | old_vfcount | VFCOUNT | int | 是 | IntegerField |
| TEMPLATE | old_template | TEMPLATE | image | 是 | BinaryField |
| UserID | old_user_id | UserID | int | 是 | IntegerField |

### SourceDyeFeelOfferDetail — 其他或待确认相关表（FeelOfferDetail，待确认）

源表：`dye.FeelOfferDetail`；新表：`src_dye_feelofferdetail`；原主键：DetailNo。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 40 | 是 | CharField |
| Price | old_price | 确价 | decimal(9,2) | 是 | DecimalField |
| Unit | old_unit | 单位 | varchar；字节长度 40 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1024 | 是 | CharField |
| FeelCode | old_feel_code | 手感编号 | varchar；字节长度 40 | 是 | CharField |
| CusPrice | old_cus_price | 报价 | decimal(10,2) | 是 | DecimalField |
| RightStatus | old_right_status | 状态 | smallint | 是 | IntegerField |
| Approver | old_approver | 审核人 | varchar；字节长度 50 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| SGDH | old_sgdh | SGDH | varchar；字节长度 50 | 是 | CharField |
| ProcessID | old_process_id | 工序 | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyeFeelOfferMain`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 FeelOfferDetail → FeelOfferMain。

### SourceDyeFeelOfferMain — 其他或待确认相关表（FeelOfferMain，待确认）

源表：`dye.FeelOfferMain`；新表：`src_dye_feeloffermain`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单号 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 单据时间 | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1024 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| LastTime | old_last_time | LastTime | datetime | 是 | DateTimeField |

### SourceDyeFixedCanDetail — 其他或待确认相关表（FixedCanDetail，待确认）

源表：`dye.FixedCanDetail`；新表：`src_dye_fixedcandetail`；原主键：DetailNo。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 50 | 否 | CharField |
| GradeID | old_grade_id | GradeID | varchar；字节长度 30 | 是 | CharField |
| FabricKindID | old_fabric_kind_id | FabricKindID | varchar；字节长度 30 | 是 | CharField |
| ColorLevel | old_color_level | ColorLevel | varchar；字节长度 30 | 是 | CharField |
| TaxPrice | old_tax_price | TaxPrice | decimal(10,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(10,2) | 是 | DecimalField |
| StuffRatio1 | old_stuff_ratio1 | StuffRatio1 | decimal(10,2) | 是 | DecimalField |
| StuffRatio2 | old_stuff_ratio2 | StuffRatio2 | decimal(10,2) | 是 | DecimalField |
| FormulaCost1 | old_formula_cost1 | FormulaCost1 | decimal(10,2) | 是 | DecimalField |
| FormulaCost2 | old_formula_cost2 | FormulaCost2 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Weight1 | old_weight1 | Weight1 | decimal(10,2) | 是 | DecimalField |
| Weight2 | old_weight2 | Weight2 | decimal(10,2) | 是 | DecimalField |

### SourceDyeFixedCanRecord — 其他或待确认相关表（FixedCanRecord，待确认）

源表：`dye.FixedCanRecord`；新表：`src_dye_fixedcanrecord`；原主键：DetailNo, RollNo。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 50 | 否 | CharField |
| RollNo | old_roll_no | RollNo | int | 否 | IntegerField |
| GradeID | old_grade_id | GradeID | varchar；字节长度 30 | 是 | CharField |
| FabricKindID | old_fabric_kind_id | FabricKindID | varchar；字节长度 30 | 是 | CharField |
| ColorLevel | old_color_level | ColorLevel | varchar；字节长度 30 | 是 | CharField |
| TaxPrice | old_tax_price | TaxPrice | decimal(10,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(10,2) | 是 | DecimalField |
| StuffRatio1 | old_stuff_ratio1 | StuffRatio1 | decimal(10,2) | 是 | DecimalField |
| StuffRatio2 | old_stuff_ratio2 | StuffRatio2 | decimal(10,2) | 是 | DecimalField |
| FormulaCost1 | old_formula_cost1 | FormulaCost1 | decimal(10,2) | 是 | DecimalField |
| FormulaCost2 | old_formula_cost2 | FormulaCost2 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Weight1 | old_weight1 | Weight1 | decimal(10,2) | 是 | DecimalField |
| Weight2 | old_weight2 | Weight2 | decimal(10,2) | 是 | DecimalField |

### SourceDyeGetJobSheetReceive — 财务结算与成本相关表（GetJobSheetReceive，待确认）

源表：`dye.GetJobSheetReceive`；新表：`src_dye_getjobsheetreceive`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 36 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | 客户编码 | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 200 | 是 | CharField |
| ColorE | old_color_e | 颜色英文名 | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 200 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 100 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 200 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 500 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 200 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 10 | 是 | CharField |
| Creater | old_creater | 登记人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 登记时间 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| Width | old_width | 幅宽 | varchar；字节长度 200 | 是 | CharField |
| Weight | old_weight | 克重 | varchar；字节长度 200 | 是 | CharField |
| ProgramItem | old_program_item | 单双染 | varchar；字节长度 500 | 是 | CharField |
| dyeDescription | old_dye_description | 是否首缸 | varchar；字节长度 200 | 是 | CharField |
| SheetType | old_sheet_type | SheetType | varchar；字节长度 20 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 50 | 是 | CharField |
| CombineSheetNos | old_combine_sheet_nos | 合缸缸号 | varchar；字节长度 -1 | 是 | TextField |
| MachineNo | old_machine_no | 机台 | varchar；字节长度 50 | 是 | CharField |
| ColorMatching | old_color_matching | 对色员 | varchar；字节长度 50 | 是 | CharField |
| Days | old_days | 日期 | varchar；字节长度 10 | 是 | CharField |
| ShiftID | old_shift_id | 班别 | varchar；字节长度 50 | 是 | CharField |
| Bigs | old_bigs | Bigs | float | 是 | FloatField |
| AddVat | old_add_vat | AddVat | int | 是 | IntegerField |
| RTVat | old_rtvat | RTVat | float | 是 | FloatField |
| PassVat | old_pass_vat | PassVat | float | 是 | FloatField |

### SourceDyeGWName — 其他或待确认相关表（GWName，待确认）

源表：`dye.GWName`；新表：`src_dye_gwname`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Keeper | old_keeper | Keeper | varchar；字节长度 10 | 是 | CharField |
| Reason | old_reason | Reason | nvarchar；字节长度 512 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| FabricKindID | old_fabric_kind_id | FabricKindID | varchar；字节长度 20 | 是 | CharField |
| GWName | old_gwname | GWName | varchar；字节长度 20 | 是 | CharField |
| MinQty | old_min_qty | MinQty | decimal(10,2) | 是 | DecimalField |
| MaxQty | old_max_qty | MaxQty | decimal(10,2) | 是 | DecimalField |

### SourceDyeHContract — 客户订单与销售相关表（h_Contract，待确认）

源表：`dye.h_Contract`；新表：`src_dye_h_contract`；原主键：SheetSeries。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| Type | old_type | 合同类别 | varchar；字节长度 50 | 是 | CharField |
| PartyA | old_party_a | 甲方 | varchar；字节长度 100 | 是 | CharField |
| PartyB | old_party_b | 乙方 | varchar；字节长度 100 | 是 | CharField |
| EmpID | old_emp_id | 员工编号 | varchar；字节长度 10 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 20 | 是 | CharField |
| MainMemo | old_main_memo | 主要说明 | varchar；字节长度 300 | 是 | CharField |
| SignedDate | old_signed_date | 签订日期 | datetime | 是 | DateTimeField |
| StartDate | old_start_date | 生效日期 | datetime | 是 | DateTimeField |
| EndDate | old_end_date | 到期日期 | datetime | 是 | DateTimeField |
| IsCanAbort | old_is_can_abort | 能否中止 | bit | 是 | BooleanField |
| StopDate | old_stop_date | 中止日期 | datetime | 是 | DateTimeField |
| CycleType | old_cycle_type | 合同中止类别 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |

### SourceDyeHEmpAppNotice — 基础主数据相关表（h_EmpAppNotice，待确认）

源表：`dye.h_EmpAppNotice`；新表：`src_dye_h_empappnotice`；原主键：无主键。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| EmpId | old_emp_id | 员工id | varchar；字节长度 20 | 否 | CharField |
| ClientId | old_client_id | 绑定app推送的clientid | varchar；字节长度 50 | 否 | CharField |
| CreateTime | old_create_time | 创建时间 | datetime | 否 | DateTimeField |
| UpdateTime | old_update_time | 更新时间 | datetime | 是 | DateTimeField |
| UpdateEmpId | old_update_emp_id | 更新员工id | varchar；字节长度 20 | 是 | CharField |
| IsDeleted | old_is_deleted | 是否删除 | bit | 是 | BooleanField |

### SourceDyeHEmpDeptPerm — 基础主数据相关表（h_EmpDeptPerm，待确认）

源表：`dye.h_EmpDeptPerm`；新表：`src_dye_h_empdeptperm`；原主键：EmpID, DeptKindID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| EmpID | old_emp_id | EmpID | varchar；字节长度 50 | 否 | CharField |
| DeptKindID | old_dept_kind_id | DeptKindID | varchar；字节长度 10 | 否 | CharField |
| PermValue | old_perm_value | PermValue | varchar；字节长度 100 | 是 | CharField |
| Description | old_description | Description | varchar；字节长度 100 | 是 | CharField |

### SourceDyeHEmployee — 员工

源表：`dye.h_Employee`；新表：`src_dye_h_employee`；原主键：EmpID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| EmpID | old_emp_id | 员工编码 | varchar；字节长度 50 | 否 | CharField |
| Password | old_password | 密码 | varchar；字节长度 50 | 是 | CharField |
| Name | old_name | 名称 | varchar；字节长度 60 | 是 | CharField |
| NameE | old_name_e | 英文名 | varchar；字节长度 128 | 是 | CharField |
| LoginName | old_login_name | 登录名 | varchar；字节长度 20 | 是 | CharField |
| InDate | old_in_date | 进厂日期 | datetime | 是 | DateTimeField |
| ProbationDate | old_probation_date | 试用结束日期 | datetime | 是 | DateTimeField |
| OutDate | old_out_date | 离职日期 | datetime | 是 | DateTimeField |
| OutReason | old_out_reason | 离职原因 | varchar；字节长度 50 | 是 | CharField |
| Sex | old_sex | 性别 | varchar；字节长度 6 | 是 | CharField |
| IdentityNo | old_identity_no | 身份证号 | varchar；字节长度 20 | 是 | CharField |
| HomeAddr | old_home_addr | 家庭地址 | varchar；字节长度 100 | 是 | CharField |
| HomeTel | old_home_tel | 家庭电话 | varchar；字节长度 15 | 是 | CharField |
| MaritalStatus | old_marital_status | 婚姻状况 | varchar；字节长度 16 | 是 | CharField |
| OfficeTel | old_office_tel | 办公电话 | varchar；字节长度 16 | 是 | CharField |
| Extension | old_extension | 分机号码 | varchar；字节长度 15 | 是 | CharField |
| Mobile | old_mobile | 移动电话 | varchar；字节长度 15 | 是 | CharField |
| QQ | old_qq | QQ号 | varchar；字节长度 20 | 是 | CharField |
| EducationID | old_education_id | 教育程度 | varchar；字节长度 10 | 是 | CharField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 10 | 是 | CharField |
| Photo | old_photo | 照片 | image | 是 | BinaryField |
| IsOut | old_is_out | 是否离职 | bit | 是 | BooleanField |
| Email | old_email | EMAIL | varchar；字节长度 60 | 是 | CharField |
| Birthday | old_birthday | 出生日期 | datetime | 是 | DateTimeField |
| PosDate | old_pos_date | 入职日期 | datetime | 是 | DateTimeField |
| PosID | old_pos_id | 职位代码 | varchar；字节长度 10 | 是 | CharField |
| NativeID | old_native_id | 籍贯 | varchar；字节长度 10 | 是 | CharField |
| HumanID | old_human_id | 户籍 | varchar；字节长度 10 | 是 | CharField |
| InsuranceID | old_insurance_id | 保险种类 | varchar；字节长度 10 | 是 | CharField |
| InsuranceNo | old_insurance_no | 保险编号 | varchar；字节长度 30 | 是 | CharField |
| StopDate | old_stop_date | 停用时间 | datetime | 是 | DateTimeField |
| EmpKind | old_emp_kind | 员工类别 | varchar；字节长度 50 | 是 | CharField |
| JobKindID | old_job_kind_id | 工种类别 | varchar；字节长度 10 | 是 | CharField |
| LoginStatus | old_login_status | 登陆状态 | bit | 是 | BooleanField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| NumValue1 | old_num_value1 | 数值1 | decimal(10,2) | 是 | DecimalField |
| NumValue2 | old_num_value2 | 数值2 | decimal(10,2) | 是 | DecimalField |
| LoginIPAddress | old_login_ipaddress | 登陆IP | varchar；字节长度 25 | 是 | CharField |
| LoginNetPort | old_login_net_port | LoginNetPort | varchar；字节长度 50 | 是 | CharField |
| SecuritySNID | old_security_snid | 安全序列号 | varchar；字节长度 50 | 是 | CharField |
| IsReceiveMessage | old_is_receive_message | IsReceiveMessage | bit | 是 | BooleanField |
| ChargStationID | old_charg_station_id | ChargStationID | varchar；字节长度 50 | 是 | CharField |
| IsCanSendSMS | old_is_can_send_sms | 是否能发消息 | bit | 是 | BooleanField |
| FuncNo | old_func_no | 常规操作功能号 | varchar；字节长度 6 | 是 | CharField |
| IntroducerDept | old_introducer_dept | IntroducerDept | varchar；字节长度 20 | 是 | CharField |
| IntroducerPos | old_introducer_pos | IntroducerPos | varchar；字节长度 20 | 是 | CharField |
| Introducer | old_introducer | 介绍人 | varchar；字节长度 20 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 50 | 是 | CharField |
| ShiftNameID | old_shift_name_id | 班别 | varchar；字节长度 16 | 是 | CharField |
| IntroducerRelation | old_introducer_relation | IntroducerRelation | varchar；字节长度 50 | 是 | CharField |
| TransferDate | old_transfer_date | TransferDate | datetime | 是 | DateTimeField |
| TransferOutDept | old_transfer_out_dept | TransferOutDept | varchar；字节长度 20 | 是 | CharField |
| TransferInDept | old_transfer_in_dept | TransferInDept | varchar；字节长度 20 | 是 | CharField |
| BeforeTransferPos | old_before_transfer_pos | BeforeTransferPos | varchar；字节长度 20 | 是 | CharField |
| IsSign | old_is_sign | IsSign | bit | 是 | BooleanField |
| SignDate | old_sign_date | SignDate | datetime | 是 | DateTimeField |
| SignNo | old_sign_no | SignNo | varchar；字节长度 50 | 是 | CharField |
| IsInsurance | old_is_insurance | IsInsurance | bit | 是 | BooleanField |
| InsuranceDate | old_insurance_date | InsuranceDate | datetime | 是 | DateTimeField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 50 | 是 | CharField |
| RFID | old_rfid | IC卡号 | varchar；字节长度 64 | 是 | CharField |
| BankAccount | old_bank_account | BankAccount | varchar；字节长度 50 | 是 | CharField |
| BankName | old_bank_name | BankName | varchar；字节长度 20 | 是 | CharField |
| fBasicSalary | old_f_basic_salary | fBasicSalary | decimal(8,2) | 是 | DecimalField |
| BasicSalary | old_basic_salary | BasicSalary | varchar；字节长度 30 | 是 | CharField |
| shiyongqi | old_shiyongqi | shiyongqi | int | 是 | IntegerField |
| shiyonggongzi | old_shiyonggongzi | shiyonggongzi | int | 是 | IntegerField |
| jibingshi | old_jibingshi | jibingshi | varchar；字节长度 20 | 是 | CharField |
| sushe | old_sushe | sushe | varchar；字节长度 20 | 是 | CharField |
| zhengshu | old_zhengshu | zhengshu | varchar；字节长度 20 | 是 | CharField |
| CurrAddr | old_curr_addr | 主前住址 | varchar；字节长度 100 | 是 | CharField |
| sEmpID | old_s_emp_id | sEmpID | varchar；字节长度 10 | 是 | CharField |
| hetongnum | old_hetongnum | hetongnum | varchar；字节长度 30 | 是 | CharField |
| tijiannum | old_tijiannum | tijiannum | varchar；字节长度 30 | 是 | CharField |
| Emergencycontact | old_emergencycontact | Emergencycontact | varchar；字节长度 20 | 是 | CharField |
| EmergencycontactPhone | old_emergencycontact_phone | EmergencycontactPhone | varchar；字节长度 30 | 是 | CharField |
| sNational | old_s_national | sNational | varchar；字节长度 20 | 是 | CharField |
| ExpiryDate | old_expiry_date | ExpiryDate | datetime | 是 | DateTimeField |
| GinsengProtectDate | old_ginseng_protect_date | GinsengProtectDate | datetime | 是 | DateTimeField |
| GinsengProtectType | old_ginseng_protect_type | GinsengProtectType | nvarchar；字节长度 100 | 是 | CharField |
| GinsengProtectSum | old_ginseng_protect_sum | GinsengProtectSum | decimal(10,2) | 是 | DecimalField |
| DDEmpId | old_ddemp_id | DDEmpId | varchar；字节长度 50 | 是 | CharField |
| WeXinId | old_we_xin_id | WeXinId | varchar；字节长度 50 | 是 | CharField |
| RoomNo | old_room_no | 宿舍号 | varchar；字节长度 50 | 是 | CharField |
| Ratio | old_ratio | 工资系数 | float | 是 | FloatField |
| IsNotKQ | old_is_not_kq | IsNotKQ | bit | 是 | BooleanField |
| PwdUsefulLife | old_pwd_useful_life | PwdUsefulLife | smallint | 是 | IntegerField |
| PwdExDate | old_pwd_ex_date | PwdExDate | date | 是 | DateField |
| IsCustomer | old_is_customer | IsCustomer | bit | 是 | BooleanField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 32 | 是 | CharField |
| MFLevel | old_mflevel | 报修权限 | int | 是 | IntegerField |
| MFGiveOut | old_mfgive_out | 报修指派 | bit | 是 | BooleanField |
| EmpGroup | old_emp_group | 维修分组 | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyeHEmployee2 — 基础主数据相关表（h_Employee2，待确认）

源表：`dye.h_Employee2`；新表：`src_dye_h_employee2`；原主键：EmpID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| EmpID | old_emp_id | EmpID | varchar；字节长度 56 | 否 | CharField |
| Password | old_password | Password | char；字节长度 15 | 是 | CharField |
| Name | old_name | Name | varchar；字节长度 56 | 是 | CharField |
| NameE | old_name_e | NameE | varchar；字节长度 56 | 是 | CharField |
| LoginName | old_login_name | LoginName | varchar；字节长度 20 | 是 | CharField |
| InDate | old_in_date | InDate | datetime | 是 | DateTimeField |
| OutDate | old_out_date | OutDate | datetime | 是 | DateTimeField |
| Sex | old_sex | Sex | varchar；字节长度 1 | 是 | CharField |
| IdentityNo | old_identity_no | IdentityNo | varchar；字节长度 20 | 是 | CharField |
| HomeAddr | old_home_addr | HomeAddr | varchar；字节长度 128 | 是 | CharField |
| CurrAddr | old_curr_addr | CurrAddr | char；字节长度 40 | 是 | CharField |
| OfficeTel | old_office_tel | OfficeTel | varchar；字节长度 30 | 是 | CharField |
| Extension | old_extension | Extension | varchar；字节长度 15 | 是 | CharField |
| Mobile | old_mobile | Mobile | varchar；字节长度 15 | 是 | CharField |
| HomeTel | old_home_tel | HomeTel | varchar；字节长度 15 | 是 | CharField |
| EducationID | old_education_id | EducationID | varchar；字节长度 4 | 是 | CharField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 4 | 是 | CharField |
| Remarks | old_remarks | Remarks | image | 是 | BinaryField |
| IsOut | old_is_out | IsOut | varchar；字节长度 1 | 是 | CharField |
| Email | old_email | Email | varchar；字节长度 60 | 是 | CharField |
| ReviseTimes | old_revise_times | ReviseTimes | numeric(2,0) | 是 | DecimalField |
| Birthday | old_birthday | Birthday | datetime | 是 | DateTimeField |
| FromDate | old_from_date | FromDate | datetime | 是 | DateTimeField |
| PosID | old_pos_id | PosID | varchar；字节长度 10 | 是 | CharField |
| NativeID | old_native_id | NativeID | varchar；字节长度 16 | 是 | CharField |
| HumanID | old_human_id | HumanID | char；字节长度 2 | 是 | CharField |
| InsuranceID | old_insurance_id | InsuranceID | char；字节长度 4 | 是 | CharField |
| InsuranceNo | old_insurance_no | InsuranceNo | char；字节长度 30 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 20 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 20 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| EmpKind | old_emp_kind | EmpKind | varchar；字节长度 10 | 是 | CharField |

### SourceDyeHEmployeeIORecord — 基础主数据相关表（h_EmployeeIORecord，待确认）

源表：`dye.h_EmployeeIORecord`；新表：`src_dye_h_employeeiorecord`；原主键：ID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | 序号 | varchar；字节长度 50 | 否 | CharField |
| EmpID | old_emp_id | 员工编号 | varchar；字节长度 10 | 是 | CharField |
| Name | old_name | 名称 | varchar；字节长度 60 | 是 | CharField |
| InDate | old_in_date | 进厂日期 | datetime | 是 | DateTimeField |
| OutDate | old_out_date | 出库日期 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |

关联 `source_parent_1` → `erp_base.SourceDyeHEmployee`；原码 `EmpID` → 父表原码 `EmpID`；依据：原界面主从 h_EmployeeIORecord → h_EmployeeEdit。

### SourceDyeHEmpRole — 员工角色

源表：`dye.h_EmpRole`；新表：`src_dye_h_emprole`；原主键：EmpID, RoleNo。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| EmpID | old_emp_id | 员工编号 | varchar；字节长度 50 | 否 | CharField |
| RoleNo | old_role_no | 角色编号 | varchar；字节长度 10 | 否 | CharField |
| IsSuper | old_is_super | 是否超级用户 | bit | 是 | BooleanField |

### SourceDyeHLeave — 基础主数据相关表（h_Leave，待确认）

源表：`dye.h_Leave`；新表：`src_dye_h_leave`；原主键：SheetSeries。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetKind | old_sheet_kind | 请假类型 | smallint | 是 | IntegerField |
| EmpID | old_emp_id | 员工编号 | varchar；字节长度 10 | 是 | CharField |
| PostID | old_post_id | 岗位编码 | varchar；字节长度 10 | 是 | CharField |
| DeptID | old_dept_id | 部门编码 | varchar；字节长度 10 | 是 | CharField |
| MachineID | old_machine_id | 机台号 | varchar；字节长度 10 | 是 | CharField |
| BeginDate | old_begin_date | 开始时间 | datetime | 是 | DateTimeField |
| EndDate | old_end_date | 结束时间 | datetime | 是 | DateTimeField |
| DaysOffSet | old_days_off_set | 请假天数 | decimal(6,2) | 是 | DecimalField |
| Atte | old_atte | 请假原因 | varchar；字节长度 100 | 是 | CharField |
| AtteValue | old_atte_value | 其他说明 | varchar；字节长度 50 | 是 | CharField |
| Adjuster | old_adjuster | 顶班人 | varchar；字节长度 20 | 是 | CharField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyeHPositionChange — 基础主数据相关表（h_PositionChange，待确认）

源表：`dye.h_PositionChange`；新表：`src_dye_h_positionchange`；原主键：SheetSeries。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| EmpID | old_emp_id | 员工编号 | varchar；字节长度 10 | 是 | CharField |
| Type | old_type | 异动类别 | varchar；字节长度 50 | 是 | CharField |
| OriDeptID | old_ori_dept_id | 原部门编码 | varchar；字节长度 10 | 是 | CharField |
| DeptID | old_dept_id | 部门编码 | varchar；字节长度 10 | 是 | CharField |
| OriPosID | old_ori_pos_id | 原职务编码 | varchar；字节长度 10 | 是 | CharField |
| PosID | old_pos_id | 职务编码 | varchar；字节长度 10 | 是 | CharField |
| OriPost | old_ori_post | 原岗位 | varchar；字节长度 60 | 是 | CharField |
| Post | old_post | 岗位 | varchar；字节长度 60 | 是 | CharField |
| AdjustTime | old_adjust_time | 调整时间 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |

### SourceDyeHRewardPunish — 基础主数据相关表（h_RewardPunish，待确认）

源表：`dye.h_RewardPunish`；新表：`src_dye_h_rewardpunish`；原主键：SheetSeries。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| EmpID | old_emp_id | 员工编号 | varchar；字节长度 10 | 是 | CharField |
| Kind | old_kind | 类别 | varchar；字节长度 1 | 是 | CharField |
| Atte | old_atte | 奖惩原因 | varchar；字节长度 100 | 是 | CharField |
| AtteValue | old_atte_value | 奖惩内容 | varchar；字节长度 50 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |

### SourceDyeHOLIDAYS — 其他或待确认相关表（HOLIDAYS，待确认）

源表：`dye.HOLIDAYS`；新表：`src_dye_holidays`；原主键：HOLIDAYID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| HOLIDAYID | old_holidayid | HOLIDAYID | int | 否 | IntegerField |
| HOLIDAYNAME | old_holidayname | HOLIDAYNAME | varchar；字节长度 20 | 是 | CharField |
| HOLIDAYYEAR | old_holidayyear | HOLIDAYYEAR | smallint | 是 | IntegerField |
| HOLIDAYMONTH | old_holidaymonth | HOLIDAYMONTH | smallint | 是 | IntegerField |
| HOLIDAYDAY | old_holidayday | HOLIDAYDAY | smallint | 是 | IntegerField |
| STARTTIME | old_starttime | STARTTIME | datetime | 是 | DateTimeField |
| DURATION | old_duration | DURATION | smallint | 是 | IntegerField |
| HOLIDAYTYPE | old_holidaytype | HOLIDAYTYPE | smallint | 是 | IntegerField |
| XINBIE | old_xinbie | XINBIE | varchar；字节长度 4 | 是 | CharField |
| MINZU | old_minzu | MINZU | varchar；字节长度 50 | 是 | CharField |
| DeptID | old_dept_id | DeptID | smallint | 是 | IntegerField |
| timezone | old_timezone | timezone | int | 是 | IntegerField |

### SourceDyeHuman — 其他或待确认相关表（Human，待确认）

源表：`dye.Human`；新表：`src_dye_human`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | varchar；字节长度 50 | 是 | CharField |
| Name | old_name | Name | varchar；字节长度 100 | 是 | CharField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 50 | 是 | CharField |
| DeptName | old_dept_name | DeptName | varchar；字节长度 50 | 是 | CharField |
| FactID | old_fact_id | FactID | varchar；字节长度 50 | 是 | CharField |
| FactName | old_fact_name | FactName | varchar；字节长度 100 | 是 | CharField |
| FieldType | old_field_type | FieldType | varchar；字节长度 50 | 是 | CharField |

### SourceDyeITMANAGE — 其他或待确认相关表（ITMANAGE，待确认）

源表：`dye.ITMANAGE`；新表：`src_dye_itmanage`；原主键：ID。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | int | 否 | IntegerField |
| FENCHANG | old_fenchang | 所属分厂 | varchar；字节长度 50 | 是 | CharField |
| BUMEN | old_bumen | 部门 | varchar；字节长度 50 | 是 | CharField |
| NAME | old_name | 名称 | varchar；字节长度 250 | 是 | CharField |
| LEIXING | old_leixing | 设备类型 | varchar；字节长度 250 | 是 | CharField |
| CPU | old_cpu | CPU | varchar；字节长度 250 | 是 | CharField |
| NEICUN | old_neicun | 内存规格 | varchar；字节长度 250 | 是 | CharField |
| YINGPAN | old_yingpan | 硬盘规格 | varchar；字节长度 250 | 是 | CharField |
| MACADDRESS | old_macaddress | MAC地址 | varchar；字节长度 250 | 是 | CharField |
| SYR | old_syr | 使用人 | varchar；字节长度 250 | 是 | CharField |
| CreateDate | old_create_date | 领用日期 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 50 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 50 | 是 | CharField |
| IsStop | old_is_stop | 是否注销 | bit | 是 | BooleanField |
| StopDate | old_stop_date | 注销日期 | datetime | 是 | DateTimeField |
| BZ | old_bz | 备注 | varchar；字节长度 500 | 是 | CharField |
| sjbm | old_sjbm | 上级部门 | varchar；字节长度 20 | 是 | CharField |

### SourceDyeKindLimit — 其他或待确认相关表（KindLimit，待确认）

源表：`dye.KindLimit`；新表：`src_dye_kindlimit`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 30 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 30 | 是 | CharField |
| Kind | old_kind | Kind | smallint | 是 | IntegerField |
| MinLimit | old_min_limit | MinLimit | decimal(12,2) | 是 | DecimalField |
| MaxLimit | old_max_limit | MaxLimit | decimal(12,2) | 是 | DecimalField |
| DeliveryDay | old_delivery_day | DeliveryDay | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 200 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 30 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 30 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| Approver | old_approver | Approver | varchar；字节长度 30 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |

### SourceDyeKQ — 其他或待确认相关表（KQ，待确认）

源表：`dye.KQ`；新表：`src_dye_kq`；原主键：ID。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | varchar；字节长度 50 | 否 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 20 | 是 | CharField |
| EmpCode | old_emp_code | EmpCode | varchar；字节长度 20 | 是 | CharField |
| dtDate | old_dt_date | dtDate | varchar；字节长度 10 | 是 | CharField |
| ShiftID | old_shift_id | ShiftID | nvarchar；字节长度 64 | 是 | CharField |
| ShiftName | old_shift_name | ShiftName | varchar；字节长度 7 | 是 | CharField |
| InTime | old_in_time | InTime | datetime | 是 | DateTimeField |
| OutTime | old_out_time | OutTime | datetime | 是 | DateTimeField |
| BeginTime | old_begin_time | BeginTime | datetime | 是 | DateTimeField |
| EndTime | old_end_time | EndTime | datetime | 是 | DateTimeField |
| LateTime | old_late_time | LateTime | int | 是 | IntegerField |
| BeforCount | old_befor_count | BeforCount | int | 是 | IntegerField |
| BeforTime | old_befor_time | BeforTime | float | 是 | FloatField |
| WorkCount | old_work_count | WorkCount | float | 是 | FloatField |
| WorkTime | old_work_time | WorkTime | float | 是 | FloatField |
| NoWork | old_no_work | NoWork | float | 是 | FloatField |
| IsHoliday | old_is_holiday | IsHoliday | int | 是 | IntegerField |
| LeaveTime | old_leave_time | LeaveTime | float | 是 | FloatField |
| IsLeave | old_is_leave | IsLeave | float | 是 | FloatField |
| LateCount | old_late_count | LateCount | float | 是 | FloatField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 50 | 是 | CharField |

### SourceDyeKQQuery — 其他或待确认相关表（KQ_Query，待确认）

源表：`dye.KQ_Query`；新表：`src_dye_kq_query`；原主键：ID。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | varchar；字节长度 50 | 否 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 20 | 是 | CharField |
| EmpCode | old_emp_code | EmpCode | varchar；字节长度 20 | 是 | CharField |
| dtDate | old_dt_date | dtDate | varchar；字节长度 10 | 是 | CharField |
| DAYS | old_days | DAYS | varchar；字节长度 10 | 是 | CharField |
| ShiftID | old_shift_id | ShiftID | nvarchar；字节长度 64 | 是 | CharField |
| ShiftName | old_shift_name | ShiftName | varchar；字节长度 7 | 是 | CharField |
| InTime | old_in_time | InTime | datetime | 是 | DateTimeField |
| OutTime | old_out_time | OutTime | datetime | 是 | DateTimeField |
| BeginTime | old_begin_time | BeginTime | datetime | 是 | DateTimeField |
| EndTime | old_end_time | EndTime | datetime | 是 | DateTimeField |
| LateTime | old_late_time | LateTime | int | 是 | IntegerField |
| BeforCount | old_befor_count | BeforCount | int | 是 | IntegerField |
| BeforTime | old_befor_time | BeforTime | float | 是 | FloatField |
| WorkCount | old_work_count | WorkCount | float | 是 | FloatField |
| WorkTime | old_work_time | WorkTime | float | 是 | FloatField |
| NoWork | old_no_work | NoWork | float | 是 | FloatField |
| IsHoliday | old_is_holiday | IsHoliday | int | 是 | IntegerField |
| LeaveTime | old_leave_time | LeaveTime | float | 是 | FloatField |
| IsLeave | old_is_leave | IsLeave | float | 是 | FloatField |
| LateCount | old_late_count | LateCount | float | 是 | FloatField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 50 | 是 | CharField |
| STATUS | old_status | STATUS | varchar；字节长度 10 | 是 | CharField |

### SourceDyeLeaveClass — 其他或待确认相关表（LeaveClass，待确认）

源表：`dye.LeaveClass`；新表：`src_dye_leaveclass`；原主键：LeaveId。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| LeaveId | old_leave_id | LeaveId | int | 否 | IntegerField |
| LeaveName | old_leave_name | LeaveName | varchar；字节长度 20 | 否 | CharField |
| MinUnit | old_min_unit | MinUnit | float | 否 | FloatField |
| Unit | old_unit | Unit | smallint | 否 | IntegerField |
| RemaindProc | old_remaind_proc | RemaindProc | smallint | 否 | IntegerField |
| RemaindCount | old_remaind_count | RemaindCount | smallint | 否 | IntegerField |
| ReportSymbol | old_report_symbol | ReportSymbol | varchar；字节长度 4 | 否 | CharField |
| Deduct | old_deduct | Deduct | float | 否 | FloatField |
| Color | old_color | Color | int | 否 | IntegerField |
| Classify | old_classify | Classify | smallint | 否 | IntegerField |

### SourceDyeLeaveClass1 — 其他或待确认相关表（LeaveClass1，待确认）

源表：`dye.LeaveClass1`；新表：`src_dye_leaveclass1`；原主键：LeaveId。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| LeaveId | old_leave_id | LeaveId | int | 否 | IntegerField |
| LeaveName | old_leave_name | LeaveName | varchar；字节长度 20 | 否 | CharField |
| MinUnit | old_min_unit | MinUnit | float | 否 | FloatField |
| Unit | old_unit | Unit | smallint | 否 | IntegerField |
| RemaindProc | old_remaind_proc | RemaindProc | smallint | 否 | IntegerField |
| RemaindCount | old_remaind_count | RemaindCount | smallint | 否 | IntegerField |
| ReportSymbol | old_report_symbol | ReportSymbol | varchar；字节长度 4 | 否 | CharField |
| Deduct | old_deduct | Deduct | float | 否 | FloatField |
| LeaveType | old_leave_type | LeaveType | smallint | 否 | IntegerField |
| Color | old_color | Color | int | 否 | IntegerField |
| Classify | old_classify | Classify | smallint | 否 | IntegerField |
| Calc | old_calc | Calc | text | 是 | TextField |

### SourceDyeLimit — 其他或待确认相关表（Limit，待确认）

源表：`dye.Limit`；新表：`src_dye_limit`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 30 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 30 | 否 | CharField |
| Kind | old_kind | Kind | smallint | 是 | IntegerField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 30 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 200 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 30 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 30 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| Approver | old_approver | Approver | varchar；字节长度 30 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |

### SourceDyeLossBill — 其他或待确认相关表（LossBill，待确认）

源表：`dye.LossBill`；新表：`src_dye_lossbill`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 单据流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 报损单号 | varchar；字节长度 20 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 10 | 是 | CharField |
| SheetDate | old_sheet_date | 报损日期 | datetime | 是 | DateTimeField |
| OrderNo | old_order_no | 订单号 | varchar；字节长度 20 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 20 | 是 | CharField |
| LossKindIDs | old_loss_kind_ids | 报损事由 | varchar；字节长度 100 | 是 | CharField |
| PreProfit | old_pre_profit | 预计毛利 | decimal(10,2) | 是 | DecimalField |
| LossMoney | old_loss_money | 损失金额 | decimal(10,2) | 是 | DecimalField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员代码 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| GrayFactID | old_gray_fact_id | 纱厂代码 | varchar；字节长度 10 | 是 | CharField |
| JobFactID | old_job_fact_id | 染厂代码 | varchar；字节长度 10 | 是 | CharField |
| OtherID | old_other_id | 其他方代码 | varchar；字节长度 10 | 是 | CharField |
| CustIDea | old_cust_idea | 客户意见 | varchar；字节长度 1000 | 是 | CharField |
| DeptIdea | old_dept_idea | 部门意见 | varchar；字节长度 1000 | 是 | CharField |
| JobIdea | old_job_idea | 染厂意见 | varchar；字节长度 1000 | 是 | CharField |
| GrayIdea | old_gray_idea | 纱厂意见 | varchar；字节长度 1000 | 是 | CharField |
| OtherIdea | old_other_idea | 其他方意见 | varchar；字节长度 1000 | 是 | CharField |
| Description | old_description | 总结意见 | varchar；字节长度 100 | 是 | CharField |
| PreGrayMoney | old_pre_gray_money | 纱厂应承担金额 | decimal(10,2) | 是 | DecimalField |
| PreJobMoney | old_pre_job_money | 染厂应承担金额 | decimal(10,2) | 是 | DecimalField |
| PreCustMoney | old_pre_cust_money | 客户应承担额 | decimal(10,2) | 是 | DecimalField |
| PreDeptMoney | old_pre_dept_money | 部门应承担额 | decimal(10,2) | 是 | DecimalField |
| PreOtherMoney | old_pre_other_money | 其他方应承担额 | decimal(10,2) | 是 | DecimalField |
| RealGrayMoney | old_real_gray_money | 纱厂实际承担金额 | decimal(10,2) | 是 | DecimalField |
| RealJobMoney | old_real_job_money | 染厂实际承担金额 | decimal(10,2) | 是 | DecimalField |
| RealCustMoney | old_real_cust_money | 客户实际承担金额 | decimal(10,2) | 是 | DecimalField |
| RealDeptMoney | old_real_dept_money | 部门实际承担金额 | decimal(10,2) | 是 | DecimalField |
| RealOtherMoney | old_real_other_money | 其他方实际承担金额 | decimal(10,2) | 是 | DecimalField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |

### SourceDyeMaterialPriceAdjust — 财务结算与成本相关表（MaterialPriceAdjust，待确认）

源表：`dye.MaterialPriceAdjust`；新表：`src_dye_materialpriceadjust`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| WareHouseID | old_ware_house_id | WareHouseID | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| InSheetSeries | old_in_sheet_series | InSheetSeries | varchar；字节长度 20 | 是 | CharField |
| InSheetNo | old_in_sheet_no | InSheetNo | varchar；字节长度 20 | 是 | CharField |

### SourceDyeMaterialPriceAdjustDetail — 财务结算与成本相关表（MaterialPriceAdjustDetail，待确认）

源表：`dye.MaterialPriceAdjustDetail`；新表：`src_dye_materialpriceadjustdetail`；原主键：DetailNo。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 否 | CharField |
| SupplierID | old_supplier_id | SupplierID | varchar；字节长度 36 | 是 | CharField |
| ArticleID | old_article_id | ArticleID | varchar；字节长度 100 | 是 | CharField |
| StuffID | old_stuff_id | StuffID | varchar；字节长度 100 | 是 | CharField |
| LastUnitPrice | old_last_unit_price | LastUnitPrice | decimal(10,4) | 是 | DecimalField |
| CurrentUnitPrice | old_current_unit_price | CurrentUnitPrice | decimal(10,4) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| InDetailNo | old_in_detail_no | InDetailNo | varchar；字节长度 36 | 是 | CharField |
| InSheetSeries | old_in_sheet_series | InSheetSeries | varchar；字节长度 20 | 是 | CharField |
| ExecutionDate | old_execution_date | ExecutionDate | datetime | 是 | DateTimeField |

### SourceDyeNoLimit — 其他或待确认相关表（NoLimit，待确认）

源表：`dye.NoLimit`；新表：`src_dye_nolimit`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 30 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 30 | 是 | CharField |
| Kind | old_kind | Kind | smallint | 是 | IntegerField |
| NoLimitAmount | old_no_limit_amount | NoLimitAmount | decimal(12,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 200 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 30 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 30 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| Approver | old_approver | Approver | varchar；字节长度 30 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |

### SourceDyeNUMRUN — 其他或待确认相关表（NUM_RUN，待确认）

源表：`dye.NUM_RUN`；新表：`src_dye_num_run`；原主键：NUM_RUNID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| NUM_RUNID | old_num_runid | NUM_RUNID | int | 否 | IntegerField |
| OLDID | old_oldid | OLDID | int | 是 | IntegerField |
| NAME | old_name | NAME | varchar；字节长度 30 | 否 | CharField |
| STARTDATE | old_startdate | STARTDATE | datetime | 是 | DateTimeField |
| ENDDATE | old_enddate | ENDDATE | datetime | 是 | DateTimeField |
| CYLE | old_cyle | CYLE | smallint | 是 | IntegerField |
| UNITS | old_units | UNITS | smallint | 是 | IntegerField |

### SourceDyeNUMRUNDEIL — 其他或待确认相关表（NUM_RUN_DEIL，待确认）

源表：`dye.NUM_RUN_DEIL`；新表：`src_dye_num_run_deil`；原主键：NUM_RUNID, SDAYS, STARTTIME。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| NUM_RUNID | old_num_runid | NUM_RUNID | smallint | 否 | IntegerField |
| STARTTIME | old_starttime | STARTTIME | datetime | 否 | DateTimeField |
| ENDTIME | old_endtime | ENDTIME | datetime | 是 | DateTimeField |
| SDAYS | old_sdays | SDAYS | smallint | 否 | IntegerField |
| EDAYS | old_edays | EDAYS | smallint | 是 | IntegerField |
| SCHCLASSID | old_schclassid | SCHCLASSID | int | 是 | IntegerField |
| OverTime | old_over_time | OverTime | int | 是 | IntegerField |

### SourceDyePArticle — 基础主数据相关表（p_Article，待确认）

源表：`dye.p_Article`；新表：`src_dye_p_article`；原主键：ArticleID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ArticleID | old_article_id | 机物料代码 | varchar；字节长度 20 | 否 | CharField |
| Name | old_name | 名称 | varchar；字节长度 60 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| NameE | old_name_e | 英文名称 | varchar；字节长度 128 | 是 | CharField |
| Mnemonic | old_mnemonic | 助记符 | varchar；字节长度 10 | 是 | CharField |
| ArticleKindID | old_article_kind_id | 物料种类代码 | varchar；字节长度 20 | 是 | CharField |
| StorageUnitID | old_storage_unit_id | 仓位代码 | varchar；字节长度 10 | 是 | CharField |
| FactID | old_fact_id | 包装单位 | varchar；字节长度 10 | 是 | CharField |
| Brand | old_brand | 牌号 | varchar；字节长度 20 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商代码 | varchar；字节长度 10 | 是 | CharField |
| Unit | old_unit | 单位（计量、计价） | varchar；字节长度 20 | 是 | CharField |
| Price | old_price | 单价 | decimal(18,6) | 是 | DecimalField |
| RemainQty | old_remain_qty | 剩余数量 | decimal(10,2) | 是 | DecimalField |
| SafeQty | old_safe_qty | 安全库存 | decimal(10,2) | 是 | DecimalField |
| LimitDays | old_limit_days | 收款期限 | int | 是 | IntegerField |
| LeadDays | old_lead_days | 前置天数 | smallint | 是 | IntegerField |
| IsBatch | old_is_batch | 批次管理 | bit | 是 | BooleanField |
| AccSubjectID | old_acc_subject_id | 财务科目代码 | varchar；字节长度 10 | 是 | CharField |
| Status | old_status | 状态 | tinyint | 是 | IntegerField |
| StopDate | old_stop_date | 停用时间 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| LastPrice | old_last_price | 最新采购价 | decimal(18,6) | 是 | DecimalField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| Approver | old_approver | 审核人 | nchar；字节长度 40 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |

### SourceDyePArticleStorageUnitID — 辅料仓位对照

源表：`dye.p_ArticleStorageUnitID`；新表：`src_dye_p_articlestorageunitid`；原主键：无主键。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FieldType | old_field_type | FieldType | varchar；字节长度 50 | 是 | CharField |
| Code | old_code | Code | varchar；字节长度 50 | 是 | CharField |
| Name | old_name | Name | varchar；字节长度 50 | 是 | CharField |

### SourceDyePAtteSub — 生产工单与排程相关表（p_AtteSub，待确认）

源表：`dye.p_AtteSub`；新表：`src_dye_p_attesub`；原主键：Code, SubCode。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| Code | old_code | Code | varchar；字节长度 20 | 否 | CharField |
| SubCode | old_sub_code | 加工要求选项 | varchar；字节长度 20 | 否 | CharField |
| SortValue | old_sort_value | 排序值 | int | 否 | IntegerField |
| Name | old_name | 选项名称 | varchar；字节长度 50 | 是 | CharField |
| NumValue | old_num_value | 默认值 | decimal(18,2) | 是 | DecimalField |
| IsDefault | old_is_default | 默认加载选项 | bit | 是 | BooleanField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |
| Price | old_price | Price | decimal(18,2) | 是 | DecimalField |
| PriceUnit | old_price_unit | PriceUnit | tinyint | 是 | IntegerField |
| GoWith | old_go_with | 关联选项，自动带出 | varchar；字节长度 50 | 是 | CharField |
| RequireFields | old_require_fields | 必填检查字段 | varchar；字节长度 50 | 是 | CharField |
| RequireTypes | old_require_types | 关联必选的组 | varchar；字节长度 50 | 是 | CharField |
| MutexTypes | old_mutex_types | 与之互斥的选项组 | varchar；字节长度 50 | 是 | CharField |

### SourceDyePAtteType — 生产工单与排程相关表（p_AtteType，待确认）

源表：`dye.p_AtteType`；新表：`src_dye_p_attetype`；原主键：Code。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| Code | old_code | 加工要求分组编码 | varchar；字节长度 20 | 否 | CharField |
| Name | old_name | 加工要求组名 | varchar；字节长度 50 | 是 | CharField |
| SortValue | old_sort_value | 排序值 | int | 是 | IntegerField |
| AtteKind | old_atte_kind | AtteKind | tinyint | 是 | IntegerField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |
| IsStop | old_is_stop | 是否停用 | bit | 是 | BooleanField |
| StopDate | old_stop_date | 停用时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 20 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 20 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 10 | 是 | CharField |
| IsMutex | old_is_mutex | 组内互斥 | bit | 是 | BooleanField |
| RequireNum | old_require_num | 必选项数 | smallint | 是 | IntegerField |

### SourceDyePAuxRule — 基础主数据相关表（p_AuxRule，待确认）

源表：`dye.p_AuxRule`；新表：`src_dye_p_auxrule`；原主键：ID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | varchar；字节长度 50 | 否 | CharField |
| ProdKindID | old_prod_kind_id | ProdKindID | varchar；字节长度 10 | 是 | CharField |
| StuffKindID | old_stuff_kind_id | StuffKindID | varchar；字节长度 10 | 是 | CharField |
| NumValue1 | old_num_value1 | NumValue1 | decimal(10,2) | 是 | DecimalField |
| NumValue2 | old_num_value2 | NumValue2 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 300 | 是 | CharField |

### SourceDyePAuxRuleDetail — 基础主数据相关表（p_AuxRuleDetail，待确认）

源表：`dye.p_AuxRuleDetail`；新表：`src_dye_p_auxruledetail`；原主键：ID, StuffID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | varchar；字节长度 50 | 否 | CharField |
| StuffID | old_stuff_id | StuffID | varchar；字节长度 10 | 否 | CharField |
| Dosage | old_dosage | Dosage | decimal(15,6) | 是 | DecimalField |
| RecipeUnit | old_recipe_unit | RecipeUnit | tinyint | 是 | IntegerField |
| CalcWay | old_calc_way | CalcWay | varchar；字节长度 1 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 300 | 是 | CharField |

### SourceDyePBalanceType — 财务结算与成本相关表（p_BalanceType，待确认）

源表：`dye.p_BalanceType`；新表：`src_dye_p_balancetype`；原主键：F_ID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| F_ID | old_f_id | F_ID | varchar；字节长度 30 | 否 | CharField |
| F_Name | old_f_name | F_Name | varchar；字节长度 60 | 是 | CharField |
| F_PayMonth | old_f_pay_month | F_PayMonth | int | 是 | IntegerField |
| F_PayDay | old_f_pay_day | F_PayDay | int | 是 | IntegerField |
| F_Remark | old_f_remark | F_Remark | varchar；字节长度 80 | 是 | CharField |
| F_Type | old_f_type | F_Type | int | 是 | IntegerField |
| F_Date | old_f_date | F_Date | int | 是 | IntegerField |

### SourceDyePColorNum — 色号与样品

源表：`dye.P_ColorNum`；新表：`src_dye_p_colornum`；原主键：ColorNo。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 是 | CharField |
| ColorNo | old_color_no | ColorNo | varchar；字节长度 50 | 否 | CharField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 50 | 是 | CharField |
| LabDipsSource | old_lab_dips_source | LabDipsSource | tinyint | 是 | IntegerField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 500 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 1000 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 528 | 是 | CharField |
| ColorDepthID | old_color_depth_id | ColorDepthID | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 100 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 50 | 是 | CharField |
| ColorE | old_color_e | ColorE | varchar；字节长度 50 | 是 | CharField |
| CustColorNum | old_cust_color_num | CustColorNum | varchar；字节长度 100 | 是 | CharField |
| ColorRGB | old_color_rgb | ColorRGB | int | 是 | IntegerField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| MainStuffKindID | old_main_stuff_kind_id | MainStuffKindID | varchar；字节长度 10 | 是 | CharField |
| IsToDoSample | old_is_to_do_sample | IsToDoSample | bit | 是 | BooleanField |
| ColorCards | old_color_cards | ColorCards | tinyint | 是 | IntegerField |
| Status | old_status | Status | varchar；字节长度 2 | 是 | CharField |
| StartTime | old_start_time | StartTime | char；字节长度 14 | 是 | CharField |
| LimitHours | old_limit_hours | LimitHours | decimal(5,2) | 是 | DecimalField |
| OverTimeReason | old_over_time_reason | OverTimeReason | varchar；字节长度 20 | 是 | CharField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 10 | 是 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 50 | 是 | CharField |
| WorkQty | old_work_qty | WorkQty | decimal(10,2) | 是 | DecimalField |
| RedoTimes | old_redo_times | RedoTimes | tinyint | 是 | IntegerField |
| OriColorNo | old_ori_color_no | OriColorNo | varchar；字节长度 20 | 是 | CharField |
| OriEmpID | old_ori_emp_id | OriEmpID | varchar；字节长度 10 | 是 | CharField |
| OriShifID | old_ori_shif_id | OriShifID | varchar；字节长度 10 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |
| Width | old_width | Width | decimal(6,2) | 是 | DecimalField |
| Weight | old_weight | Weight | decimal(6,2) | 是 | DecimalField |
| CustSelfProduct | old_cust_self_product | CustSelfProduct | varchar；字节长度 200 | 是 | CharField |
| ColorMark | old_color_mark | ColorMark | varchar；字节长度 10 | 是 | CharField |
| ColorNumMark | old_color_num_mark | ColorNumMark | varchar；字节长度 10 | 是 | CharField |
| R | old_r | R | int | 是 | IntegerField |
| G | old_g | G | int | 是 | IntegerField |
| B | old_b | B | int | 是 | IntegerField |
| RGB | old_rgb | RGB | int | 是 | IntegerField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 100 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 20 | 是 | CharField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 20 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| OKTime | old_oktime | OKTime | datetime | 是 | DateTimeField |
| EndTime | old_end_time | EndTime | datetime | 是 | DateTimeField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 50 | 是 | CharField |
| ColorNumNO | old_color_num_no | ColorNumNO | varchar；字节长度 50 | 是 | CharField |
| IsOrder | old_is_order | IsOrder | varchar；字节长度 10 | 是 | CharField |
| IsOrderTime | old_is_order_time | IsOrderTime | datetime | 是 | DateTimeField |
| CusRemark | old_cus_remark | CusRemark | varchar；字节长度 1000 | 是 | CharField |
| IsToSampleDaTe | old_is_to_sample_da_te | IsToSampleDaTe | datetime | 是 | DateTimeField |
| VerLight1ID | old_ver_light1_id | VerLight1ID | varchar；字节长度 50 | 是 | CharField |
| VerLight2ID | old_ver_light2_id | VerLight2ID | varchar；字节长度 50 | 是 | CharField |
| StuffDosage | old_stuff_dosage | StuffDosage | decimal(10,6) | 是 | DecimalField |
| DyePhaseName | old_dye_phase_name | DyePhaseName | varchar；字节长度 100 | 是 | CharField |
| GaoLaodu | old_gao_laodu | GaoLaodu | varchar；字节长度 100 | 是 | CharField |
| Note | old_note | Note | varchar；字节长度 1000 | 是 | CharField |
| Daipaidaban | old_daipaidaban | Daipaidaban | varchar；字节长度 10 | 是 | CharField |
| Duiseluogang | old_duiseluogang | Duiseluogang | varchar；字节长度 10 | 是 | CharField |
| Dabanpise | old_dabanpise | Dabanpise | varchar；字节长度 10 | 是 | CharField |
| KindType | old_kind_type | KindType | varchar；字节长度 10 | 是 | CharField |
| IsDoubleDye | old_is_double_dye | IsDoubleDye | tinyint | 是 | IntegerField |
| GradeID | old_grade_id | GradeID | varchar；字节长度 50 | 是 | CharField |
| CostQuote | old_cost_quote | CostQuote | float | 是 | FloatField |

### SourceDyePCommissionRatio — 基础主数据相关表（p_CommissionRatio，待确认）

源表：`dye.p_CommissionRatio`；新表：`src_dye_p_commissionratio`；原主键：无主键。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| BeginOutD | old_begin_out_d | BeginOutD | int | 是 | IntegerField |
| EndOutD | old_end_out_d | EndOutD | int | 是 | IntegerField |
| BeginMoneyD | old_begin_money_d | BeginMoneyD | int | 是 | IntegerField |
| EndMoneyD | old_end_money_d | EndMoneyD | int | 是 | IntegerField |

### SourceDyePCommMethod — 基础主数据相关表（p_CommMethod，待确认）

源表：`dye.p_CommMethod`；新表：`src_dye_p_commmethod`；原主键：MethodID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| MethodID | old_method_id | 通讯方法编码 | varchar；字节长度 10 | 否 | CharField |
| Interval | old_interval | 发送间隔 | int | 是 | IntegerField |
| SendFormat | old_send_format | 发送格式 | varchar；字节长度 100 | 是 | CharField |
| ReceFormat | old_rece_format | 接收格式 | varchar；字节长度 200 | 是 | CharField |
| Error_Check | old_error_check | 校验方法 | varchar；字节长度 5 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| RespondFormat | old_respond_format | 响应处理格式 | varchar；字节长度 100 | 是 | CharField |
| Name | old_name | 名称 | varchar；字节长度 60 | 是 | CharField |

### SourceDyePCommModule — 基础主数据相关表（p_CommModule，待确认）

源表：`dye.p_CommModule`；新表：`src_dye_p_commmodule`；原主键：ModuleID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ModuleID | old_module_id | 模块编号 | varchar；字节长度 10 | 否 | CharField |
| Name | old_name | 名称 | varchar；字节长度 60 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| Channels | old_channels | 通道数 | tinyint | 是 | IntegerField |
| RS485s | old_rs485s | RS485s | tinyint | 是 | IntegerField |

### SourceDyePCommPort — 基础主数据相关表（p_CommPort，待确认）

源表：`dye.p_CommPort`；新表：`src_dye_p_commport`；原主键：PortID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| PortID | old_port_id | PortID | varchar；字节长度 10 | 否 | CharField |
| IPAddress | old_ipaddress | IP地址 | varchar；字节长度 50 | 否 | CharField |
| PortNum | old_port_num | 端(串)口号 | tinyint | 否 | IntegerField |
| StopBits | old_stop_bits | 停止位 | tinyint | 是 | IntegerField |
| DataBits | old_data_bits | 数据位 | tinyint | 是 | IntegerField |
| Parity | old_parity | 奇偶校验位 | varchar；字节长度 15 | 是 | CharField |
| ReadInterval | old_read_interval | 读时间间隔 | int | 是 | IntegerField |
| WriteInterval | old_write_interval | 写时间间隔 | int | 是 | IntegerField |
| Kind | old_kind | Kind | tinyint | 是 | IntegerField |
| ModuleType | old_module_type | ModuleType | tinyint | 是 | IntegerField |
| BaudRate | old_baud_rate | BaudRate | varchar；字节长度 10 | 是 | CharField |
| TimeOutSecond | old_time_out_second | TimeOutSecond | smallint | 是 | IntegerField |
| IsStop | old_is_stop | IsStop | bit | 是 | BooleanField |

### SourceDyePCook — 基础主数据相关表（p_Cook，待确认）

源表：`dye.p_Cook`；新表：`src_dye_p_cook`；原主键：无主键。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| CookID | old_cook_id | 编码 | varchar；字节长度 20 | 否 | CharField |
| Name | old_name | 名称 | varchar；字节长度 60 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| NameE | old_name_e | 英文名称 | varchar；字节长度 128 | 是 | CharField |
| Mnemonic | old_mnemonic | 助记符 | varchar；字节长度 10 | 是 | CharField |
| ArticleKindID | old_article_kind_id | ArticleKindID | varchar；字节长度 20 | 是 | CharField |
| StorageUnitID | old_storage_unit_id | 仓位代码 | varchar；字节长度 10 | 是 | CharField |
| FactID | old_fact_id | 包装单位 | varchar；字节长度 10 | 是 | CharField |
| Brand | old_brand | 牌号 | varchar；字节长度 20 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商代码 | varchar；字节长度 10 | 是 | CharField |
| Unit | old_unit | 单位（计量、计价） | varchar；字节长度 20 | 是 | CharField |
| Price | old_price | 单价 | decimal(18,6) | 是 | DecimalField |
| RemainQty | old_remain_qty | 剩余数量 | decimal(10,2) | 是 | DecimalField |
| SafeQty | old_safe_qty | 安全库存 | decimal(10,2) | 是 | DecimalField |
| LimitDays | old_limit_days | 收款期限 | int | 是 | IntegerField |
| LeadDays | old_lead_days | 前置天数 | smallint | 是 | IntegerField |
| IsBatch | old_is_batch | 批次管理 | bit | 是 | BooleanField |
| AccSubjectID | old_acc_subject_id | 财务科目代码 | varchar；字节长度 10 | 是 | CharField |
| Status | old_status | 状态 | tinyint | 是 | IntegerField |
| StopDate | old_stop_date | 停用时间 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| LastPrice | old_last_price | 最新采购价 | decimal(18,6) | 是 | DecimalField |

### SourceDyePCraftParam — 系统平台与配置相关表（p_CraftParam，待确认）

源表：`dye.p_CraftParam`；新表：`src_dye_p_craftparam`；原主键：ParamID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ParamID | old_param_id | 参数编码 | varchar；字节长度 10 | 否 | CharField |
| ParamName | old_param_name | 参数名 | varchar；字节长度 50 | 是 | CharField |
| ParamType | old_param_type | 参数类型 | varchar；字节长度 10 | 是 | CharField |
| UnitStr | old_unit_str | 计量单位名称 | varchar；字节长度 6 | 是 | CharField |
| Description | old_description | 增减率 | varchar；字节长度 100 | 是 | CharField |
| CommStr | old_comm_str | 串口设置字串 | varchar；字节长度 200 | 是 | CharField |
| Rate | old_rate | 描述 | decimal(10,2) | 是 | DecimalField |

### SourceDyePCraftPParam — 系统平台与配置相关表（p_CraftPParam，待确认）

源表：`dye.p_CraftPParam`；新表：`src_dye_p_craftpparam`；原主键：ParamID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ParamID | old_param_id | ParamID | varchar；字节长度 10 | 否 | CharField |
| ParamName | old_param_name | ParamName | varchar；字节长度 50 | 是 | CharField |
| ParamType | old_param_type | ParamType | varchar；字节长度 10 | 是 | CharField |
| UnitStr | old_unit_str | UnitStr | varchar；字节长度 6 | 是 | CharField |
| Description | old_description | Description | varchar；字节长度 100 | 是 | CharField |

### SourceDyePCustAddress — 客户订单与销售相关表（p_CustAddress，待确认）

源表：`dye.p_CustAddress`；新表：`src_dye_p_custaddress`；原主键：CustomerID, address。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| CustomerID | old_customer_id | 客户编码 | varchar；字节长度 10 | 否 | CharField |
| address | old_address | 收发地址 | varchar；字节长度 500 | 否 | CharField |
| zhichang | old_zhichang | 织厂 | varchar；字节长度 200 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePCustomer`；原码 `CustomerID` → 父表原码 `CustomerID`；依据：原界面主从 p_CustAddress → p_Customer。

### SourceDyePCustCategory — 客户订单与销售相关表（p_CustCategory，待确认）

源表：`dye.p_CustCategory`；新表：`src_dye_p_custcategory`；原主键：CustomerID, CustCategoryCode。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 否 | CharField |
| CustCategoryCode | old_cust_category_code | 客户分类码 | tinyint | 否 | IntegerField |

关联 `source_parent_1` → `erp_base.SourceDyePCustomer`；原码 `CustomerID` → 父表原码 `CustomerID`；依据：原界面主从 p_CustCategory → p_Customer；原界面主从 p_CustCategory_Supplier → p_Supplier。

### SourceDyePCustLinker — 客户订单与销售相关表（p_CustLinker，待确认）

源表：`dye.p_CustLinker`；新表：`src_dye_p_custlinker`；原主键：CustomerID, RowNo。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 否 | CharField |
| RowNo | old_row_no | 行号 | numeric(3,0) | 否 | DecimalField |
| Name | old_name | 名称 | varchar；字节长度 60 | 是 | CharField |
| Dept | old_dept | 部门 | varchar；字节长度 20 | 是 | CharField |
| Title | old_title | 职位 | varchar；字节长度 20 | 是 | CharField |
| Mobile | old_mobile | 手机 | varchar；字节长度 15 | 是 | CharField |
| OfficeTel | old_office_tel | 办公室电话 | varchar；字节长度 16 | 是 | CharField |
| Fax | old_fax | 传真 | varchar；字节长度 20 | 是 | CharField |
| Email | old_email | Email | varchar；字节长度 60 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| Addr | old_addr | Addr | varchar；字节长度 160 | 是 | CharField |
| Tel | old_tel | Tel | varchar；字节长度 16 | 是 | CharField |
| QQ | old_qq | QQ | varchar；字节长度 20 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePCustomer`；原码 `CustomerID` → 父表原码 `CustomerID`；依据：原界面主从 p_CustLinker_Supplier → p_Supplier；原界面主从 p_CustLinker → p_Customer。

### SourceDyePCustomer — 往来单位（客户/供应商）

源表：`dye.p_Customer`；新表：`src_dye_p_customer`；原主键：CustomerID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| CustomerID | old_customer_id | 客户编码 | varchar；字节长度 10 | 否 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 50 | 是 | CharField |
| ShortName | old_short_name | 客户简称 | varchar；字节长度 50 | 是 | CharField |
| Mnemonic | old_mnemonic | 助记符 | varchar；字节长度 30 | 是 | CharField |
| NameC | old_name_c | 中文名称 | varchar；字节长度 128 | 是 | CharField |
| NameE | old_name_e | 英文名称 | varchar；字节长度 128 | 是 | CharField |
| SalerID | old_saler_id | 业务员代码 | varchar；字节长度 10 | 是 | CharField |
| CustKindID | old_cust_kind_id | 类别 | varchar；字节长度 10 | 是 | CharField |
| CorpKindID | old_corp_kind_id | 企业类型 | varchar；字节长度 10 | 是 | CharField |
| Tel | old_tel | 电话 | varchar；字节长度 50 | 是 | CharField |
| Fax | old_fax | 传真 | varchar；字节长度 20 | 是 | CharField |
| Zip | old_zip | 邮编 | varchar；字节长度 10 | 是 | CharField |
| CountryID | old_country_id | 国家代码 | varchar；字节长度 10 | 是 | CharField |
| Addr | old_addr | 地址 | varchar；字节长度 160 | 是 | CharField |
| AddrE | old_addr_e | 英文地址名 | varchar；字节长度 160 | 是 | CharField |
| AddrDlv | old_addr_dlv | 交货地址 | varchar；字节长度 160 | 是 | CharField |
| AddrInv | old_addr_inv | 发票地址 | varchar；字节长度 160 | 是 | CharField |
| Charger | old_charger | 负责人 | varchar；字节长度 128 | 是 | CharField |
| CorpCode | old_corp_code | 公司代码 | varchar；字节长度 30 | 是 | CharField |
| Email | old_email | Email | varchar；字节长度 60 | 是 | CharField |
| WebSite | old_web_site | 网站 | varchar；字节长度 60 | 是 | CharField |
| CreditLimit | old_credit_limit | 信用额度 | bigint | 是 | BigIntegerField |
| Deposit | old_deposit | 折扣 | decimal(8,2) | 是 | DecimalField |
| AreaID | old_area_id | 区域 | varchar；字节长度 10 | 是 | CharField |
| CreditGrade | old_credit_grade | 信用等级 | varchar；字节长度 10 | 是 | CharField |
| IsAbroad | old_is_abroad | 自动包装 | bit | 是 | BooleanField |
| BeginDate | old_begin_date | 初始日期 | datetime | 是 | DateTimeField |
| Market | old_market | 市场区域 | varchar；字节长度 100 | 是 | CharField |
| SettleID | old_settle_id | 结算方式 | varchar；字节长度 10 | 是 | CharField |
| LimitDays | old_limit_days | 收款期限 | int | 是 | IntegerField |
| PaymentID | old_payment_id | 付款方式 | varchar；字节长度 10 | 是 | CharField |
| BillDays | old_bill_days | 票据天数 | smallint | 是 | IntegerField |
| BankName | old_bank_name | 户名 | varchar；字节长度 100 | 是 | CharField |
| BankNo | old_bank_no | 银行卡号 | varchar；字节长度 100 | 是 | CharField |
| Bank | old_bank | 开户行 | varchar；字节长度 100 | 是 | CharField |
| BankName1 | old_bank_name1 | BankName1 | varchar；字节长度 200 | 是 | CharField |
| BankNo1 | old_bank_no1 | BankNo1 | varchar；字节长度 200 | 是 | CharField |
| Bank1 | old_bank1 | Bank1 | varchar；字节长度 200 | 是 | CharField |
| BankName2 | old_bank_name2 | BankName2 | varchar；字节长度 200 | 是 | CharField |
| BankNo2 | old_bank_no2 | BankNo2 | varchar；字节长度 200 | 是 | CharField |
| Bank2 | old_bank2 | Bank2 | varchar；字节长度 200 | 是 | CharField |
| IsStop | old_is_stop | 是否停用 | bit | 是 | BooleanField |
| StopDate | old_stop_date | 停用时间 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| ParentCustID | old_parent_cust_id | ParentCustID | varchar；字节长度 10 | 是 | CharField |
| Discount | old_discount | Discount | decimal(3,2) | 是 | DecimalField |
| APMoney | old_apmoney | APMoney | decimal(10,2) | 是 | DecimalField |
| ARMoney | old_armoney | ARMoney | decimal(10,2) | 是 | DecimalField |
| ProdCode | old_prod_code | ProdCode | varchar；字节长度 32 | 是 | CharField |
| PrintTimes | old_print_times | PrintTimes | int | 是 | IntegerField |
| PASSWORD | old_password | PASSWORD | varchar；字节长度 50 | 是 | CharField |
| LoginName | old_login_name | LoginName | varchar；字节长度 50 | 是 | CharField |
| GaryPrice | old_gary_price | 计价类别 | varchar；字节长度 20 | 是 | CharField |
| LabelID | old_label_id | 标签 | varchar；字节长度 20 | 是 | CharField |
| CorpType | old_corp_type | 供应商类别 | varchar；字节长度 10 | 是 | CharField |
| AddQty | old_add_qty | 包装加重 | float | 是 | FloatField |
| XMLFolder | old_xmlfolder | XMLFolder | nvarchar；字节长度 2000 | 是 | CharField |
| EnableOrders | old_enable_orders | 是否启用订单 | bit | 是 | BooleanField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| Contact | old_contact | 联系人 | varchar；字节长度 50 | 是 | CharField |
| MasterCustomer | old_master_customer | 主客户名 | varchar；字节长度 30 | 是 | CharField |
| Merchandiser | old_merchandiser | 跟单员 | varchar；字节长度 30 | 是 | CharField |
| PortNO | old_port_no | PortNO | varchar；字节长度 10 | 是 | CharField |
| Num | old_num | Num | varchar；字节长度 20 | 是 | CharField |

### SourceDyePCustRelation — 客户订单与销售相关表（p_CustRelation，待确认）

源表：`dye.p_CustRelation`；新表：`src_dye_p_custrelation`；原主键：CustomerID, RowNo。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| CustomerID | old_customer_id | 客户编码 | varchar；字节长度 10 | 否 | CharField |
| RowNo | old_row_no | 行号 | numeric(2,0) | 否 | DecimalField |
| Code | old_code | 编码 | varchar；字节长度 10 | 是 | CharField |
| RelaCustomerID | old_rela_customer_id | 关系客户代码 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePCustomer`；原码 `CustomerID` → 父表原码 `CustomerID`；依据：原界面主从 p_CustRelation → p_Customer；数据库声明 FK_p_CustAddr_p_Customer；原界面主从 p_CustRelation_Supplier → p_Supplier。

### SourceDyePDept — 部门

源表：`dye.p_Dept`；新表：`src_dye_p_dept`；原主键：DeptID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| DeptID | old_dept_id | 部门编码 | varchar；字节长度 10 | 否 | CharField |
| Name | old_name | 名称 | varchar；字节长度 60 | 是 | CharField |
| ParentCode | old_parent_code | 父级代码 | varchar；字节长度 10 | 是 | CharField |
| ChargerID | old_charger_id | 部门负责人 | varchar；字节长度 10 | 是 | CharField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |
| StopDate | old_stop_date | 停用时间 | datetime | 是 | DateTimeField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| DeptKindID | old_dept_kind_id | 部门类型 | varchar；字节长度 10 | 是 | CharField |
| IsStop | old_is_stop | 是否停用 | bit | 是 | BooleanField |
| IsCostUnit | old_is_cost_unit | 成本部门 | bit | 是 | BooleanField |

### SourceDyePDyeCurve — 染色工艺与配方相关表（p_DyeCurve，待确认）

源表：`dye.p_DyeCurve`；新表：`src_dye_p_dyecurve`；原主键：CurveID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| CurveID | old_curve_id | 编号 | varchar；字节长度 10 | 否 | CharField |
| Name | old_name | 曲线名称 | varchar；字节长度 60 | 是 | CharField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |
| ProgramKindID | old_program_kind_id | 分类 | varchar；字节长度 10 | 是 | CharField |
| DyePhase | old_dye_phase | 阶段 | tinyint | 是 | IntegerField |
| PreMinutes | old_pre_minutes | 准备时间 | smallint | 是 | IntegerField |
| ProgramMinutes | old_program_minutes | 工艺时间 | smallint | 是 | IntegerField |
| TotalMinutes | old_total_minutes | 合计时间 | smallint | 是 | IntegerField |
| SelfDefineImage | old_self_define_image | 自定义曲线图 | image | 是 | BinaryField |
| AutoImage | old_auto_image | 计算产生曲线图 | image | 是 | BinaryField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| IsStop | old_is_stop | 停用 | bit | 是 | BooleanField |
| StopDate | old_stop_date | 停用时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| EffiRate | old_effi_rate | EffiRate | decimal(6,4) | 是 | DecimalField |
| MaxValue | old_max_value | MaxValue | decimal(10,2) | 是 | DecimalField |
| PhaseID | old_phase_id | 染色流程 | varchar；字节长度 10 | 是 | CharField |

### SourceDyePDyeCurveDetail — 染色工艺与配方相关表（p_DyeCurveDetail，待确认）

源表：`dye.p_DyeCurveDetail`；新表：`src_dye_p_dyecurvedetail`；原主键：CurveID, StepNo。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| CurveID | old_curve_id | 曲线编码 | varchar；字节长度 10 | 否 | CharField |
| StepNo | old_step_no | 步号 | tinyint | 否 | IntegerField |
| DyeProcessID | old_dye_process_id | 染色工序 | nvarchar；字节长度 100 | 是 | CharField |
| Temperature | old_temperature | 温度 | decimal(5,1) | 是 | DecimalField |
| SpeedRate | old_speed_rate | 速率 | decimal(3,1) | 是 | DecimalField |
| Minutes | old_minutes | 分钟 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| DefaultValue | old_default_value | DefaultValue | decimal(10,2) | 是 | DecimalField |
| Memo | old_memo | Memo | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePDyeCurve`；原码 `CurveID` → 父表原码 `CurveID`；依据：原界面主从 p_DyeCurveDetailJJ → p_DyeCurveJJ；原界面主从 p_DyeCurveDetail → p_DyeCurve。

### SourceDyePDyeProgram — 染色工艺与配方相关表（p_DyeProgram，待确认）

源表：`dye.p_DyeProgram`；新表：`src_dye_p_dyeprogram`；原主键：ProgramID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ProgramID | old_program_id | ProgramID | varchar；字节长度 10 | 否 | CharField |
| Name | old_name | Name | varchar；字节长度 60 | 是 | CharField |
| Description | old_description | Description | varchar；字节长度 100 | 是 | CharField |
| ProgramKindID | old_program_kind_id | ProgramKindID | varchar；字节长度 10 | 是 | CharField |
| PreMinutes | old_pre_minutes | PreMinutes | smallint | 是 | IntegerField |
| ProgramMinutes | old_program_minutes | ProgramMinutes | smallint | 是 | IntegerField |
| TotalMinutes | old_total_minutes | TotalMinutes | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| IsStop | old_is_stop | IsStop | bit | 是 | BooleanField |
| StopDate | old_stop_date | StopDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| DyePhase | old_dye_phase | DyePhase | tinyint | 是 | IntegerField |
| SelfDefineImage | old_self_define_image | SelfDefineImage | image | 是 | BinaryField |
| AutoImage | old_auto_image | AutoImage | image | 是 | BinaryField |

### SourceDyePDyeProgramDetail — 染色工艺与配方相关表（p_DyeProgramDetail，待确认）

源表：`dye.p_DyeProgramDetail`；新表：`src_dye_p_dyeprogramdetail`；原主键：ProgramID, StepNo。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ProgramID | old_program_id | ProgramID | varchar；字节长度 10 | 否 | CharField |
| StepNo | old_step_no | StepNo | tinyint | 否 | IntegerField |
| DyeProcessID | old_dye_process_id | DyeProcessID | varchar；字节长度 10 | 是 | CharField |
| Temperature | old_temperature | Temperature | decimal(5,1) | 是 | DecimalField |
| Minutes | old_minutes | Minutes | decimal(10,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| EffiRate | old_effi_rate | EffiRate | decimal(6,4) | 是 | DecimalField |
| SpeedRate | old_speed_rate | SpeedRate | decimal(3,1) | 是 | DecimalField |

### SourceDyePFabric — 坯布半成品成品与仓储相关表（p_Fabric，待确认）

源表：`dye.p_Fabric`；新表：`src_dye_p_fabric`；原主键：FabricID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 20 | 否 | CharField |
| NameC | old_name_c | 中文名称 | varchar；字节长度 60 | 是 | CharField |
| NameE | old_name_e | 英文名称 | varchar；字节长度 60 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 50 | 是 | CharField |
| Structure | old_structure | 组织 | varchar；字节长度 50 | 是 | CharField |
| FabricKindID | old_fabric_kind_id | 纱种类别 | varchar；字节长度 10 | 是 | CharField |
| FabricStyleID | old_fabric_style_id | 纱种风格编码 | varchar；字节长度 10 | 是 | CharField |
| GrayWeight | old_gray_weight | 胚纱克重 | decimal(6,2) | 是 | DecimalField |
| StockUnit | old_stock_unit | 库存单位 | tinyint | 是 | IntegerField |
| PriceUnit | old_price_unit | 计价单位编码 | tinyint | 是 | IntegerField |
| GrayPrice | old_gray_price | 胚纱价格 | decimal(10,2) | 是 | DecimalField |
| ProdPrice | old_prod_price | 成品价格 | decimal(10,2) | 是 | DecimalField |
| ProdWeight | old_prod_weight | 成品克重 | decimal(6,2) | 是 | DecimalField |
| Mnemonic | old_mnemonic | 助记符 | varchar；字节长度 10 | 是 | CharField |
| Graphic | old_graphic | 图案 | image | 是 | BinaryField |
| IsSample | old_is_sample | 是否样品 | bit | 是 | BooleanField |
| IsStop | old_is_stop | 是否停用 | bit | 是 | BooleanField |
| StopDate | old_stop_date | 停用时间 | datetime | 是 | DateTimeField |
| WidthDn | old_width_dn | 门幅下限 | decimal(6,2) | 是 | DecimalField |
| WidthUp | old_width_up | 门幅上限 | decimal(6,2) | 是 | DecimalField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Density | old_density | 密度 | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 20 | 是 | CharField |
| Place | old_place | 存放位置 | varchar；字节长度 100 | 是 | CharField |

### SourceDyePFabricCust — 坯布半成品成品与仓储相关表（p_Fabric_Cust，待确认）

源表：`dye.p_Fabric_Cust`；新表：`src_dye_p_fabric_cust`；原主键：FabricID, CustomerID, Kind。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 20 | 否 | CharField |
| CustomerID | old_customer_id | 客户编码 | varchar；字节长度 10 | 否 | CharField |
| Kind | old_kind | 胚纱/成品 | varchar；字节长度 10 | 否 | CharField |
| CustFabricName | old_cust_fabric_name | 客户规格 | varchar；字节长度 50 | 是 | CharField |
| PriceTime | old_price_time | 价格时间 | datetime | 是 | DateTimeField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePGray`；原码 `FabricID` → 父表原码 `GrayID`；依据：原界面主从 p_Gray_Cust → p_Gray。

### SourceDyePFabricFact — 坯布半成品成品与仓储相关表（p_Fabric_Fact，待确认）

源表：`dye.p_Fabric_Fact`；新表：`src_dye_p_fabric_fact`；原主键：FabricID, CustCategoryCode, FactID, Kind。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 20 | 否 | CharField |
| CustCategoryCode | old_cust_category_code | 供应商分类 | tinyint | 否 | IntegerField |
| FactID | old_fact_id | 供应商编号 | varchar；字节长度 10 | 否 | CharField |
| Kind | old_kind | 胚纱/成品 | varchar；字节长度 10 | 否 | CharField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| PriceTime | old_price_time | 时间 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePGray`；原码 `FabricID` → 父表原码 `GrayID`；依据：原界面主从 p_Gray_Fact → p_Gray。

### SourceDyePFabricOther — 坯布半成品成品与仓储相关表（p_Fabric_Other，待确认）

源表：`dye.p_Fabric_Other`；新表：`src_dye_p_fabric_other`；原主键：FabricID, FabricInfoKindID, Code, Kind。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 10 | 否 | CharField |
| FabricInfoKindID | old_fabric_info_kind_id | 胚纱信息分类代码 | varchar；字节长度 10 | 否 | CharField |
| Code | old_code | 信息代码 | varchar；字节长度 10 | 否 | CharField |
| Kind | old_kind | 胚纱/成品 | varchar；字节长度 10 | 否 | CharField |
| NumValue | old_num_value | 数值信息 | numeric(18,6) | 是 | DecimalField |
| StringValue | old_string_value | 文字信息 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePGray`；原码 `FabricID` → 父表原码 `GrayID`；依据：原界面主从 p_Gray_Other → p_Gray。

### SourceDyePFeelCode — 基础主数据相关表（p_FeelCode，待确认）

源表：`dye.p_FeelCode`；新表：`src_dye_p_feelcode`；原主键：ProdID, FeelCode。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FeelCode | old_feel_code | 手感编号 | varchar；字节长度 50 | 否 | CharField |
| FeelName | old_feel_name | 手感名称 | varchar；字节长度 100 | 是 | CharField |
| SerialNumber | old_serial_number | 序号 | int | 是 | IntegerField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 50 | 否 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePProduct`；原码 `ProdID` → 父表原码 `ProdID`；依据：原界面主从 p_FeelCode → p_Product。

### SourceDyePFieldMemo — 基础主数据相关表（p_FieldMemo，待确认）

源表：`dye.p_FieldMemo`；新表：`src_dye_p_fieldmemo`；原主键：FieldType, Name。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FieldType | old_field_type | 类型 | varchar；字节长度 20 | 否 | CharField |
| Name | old_name | Name | varchar；字节长度 500 | 否 | CharField |
| IsStop | old_is_stop | IsStop | bit | 是 | BooleanField |
| StopDate | old_stop_date | 停用日期 | datetime | 是 | DateTimeField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |

### SourceDyePFieldValid — 通用代码字典

源表：`dye.p_FieldValid`；新表：`src_dye_p_fieldvalid`；原主键：FieldType, Code。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FieldType | old_field_type | 数据类型 | varchar；字节长度 20 | 否 | CharField |
| Code | old_code | 编号 | varchar；字节长度 20 | 否 | CharField |
| Name | old_name | 名称 | varchar；字节长度 100 | 否 | CharField |
| Mnemonic | old_mnemonic | 助记符 | varchar；字节长度 100 | 是 | CharField |
| NumValue | old_num_value | 数值值 | numeric(18,6) | 是 | DecimalField |
| SortValue | old_sort_value | 排序值 | smallint | 是 | IntegerField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |
| Reserved1 | old_reserved1 | 单位 | varchar；字节长度 1000 | 是 | CharField |
| Reserved2 | old_reserved2 | 是否打印 | varchar；字节长度 100 | 是 | CharField |
| Reserved3 | old_reserved3 | 扣分值 | varchar；字节长度 100 | 是 | CharField |
| Reserved4 | old_reserved4 | 保留值4 | varchar；字节长度 100 | 是 | CharField |
| Reserved5 | old_reserved5 | 保留值5 | varchar；字节长度 100 | 是 | CharField |
| StopDate | old_stop_date | 停用日期 | datetime | 是 | DateTimeField |
| ParentCode | old_parent_code | 父级代码 | varchar；字节长度 10 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| IsStop | old_is_stop | 是否停用 | bit | 是 | BooleanField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 20 | 是 | CharField |
| NumValueNo | old_num_value_no | NumValueNo | int | 是 | IntegerField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 20 | 是 | CharField |
| Long_CM | old_long_cm | 长(CM) | decimal(6,1) | 是 | DecimalField |
| Wide_CM | old_wide_cm | 宽(CM) | decimal(6,1) | 是 | DecimalField |
| High_CM | old_high_cm | 高(CM) | decimal(6,1) | 是 | DecimalField |

### SourceDyePFieldValidSub — 基础主数据相关表（p_FieldValidSub，待确认）

源表：`dye.p_FieldValidSub`；新表：`src_dye_p_fieldvalidsub`；原主键：FieldType, Code, SubCode, SortValue。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FieldType | old_field_type | 数据类型 | varchar；字节长度 20 | 否 | CharField |
| Code | old_code | 疵点编号 | varchar；字节长度 20 | 否 | CharField |
| SubCode | old_sub_code | 疵点代码 | varchar；字节长度 10 | 否 | CharField |
| SortValue | old_sort_value | 排序值 | smallint | 否 | IntegerField |
| Name | old_name | 疵点名 | varchar；字节长度 60 | 否 | CharField |
| NumValue | old_num_value | 数值值 | numeric(18,6) | 是 | DecimalField |
| NumValue2 | old_num_value2 | 收费价格 | decimal(10,2) | 是 | DecimalField |
| PriceUnit | old_price_unit | 收费单位 | tinyint | 是 | IntegerField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |
| IsDefault | old_is_default | 默认选择 | int | 是 | IntegerField |
| NumValue3 | old_num_value3 | 是否收费 | int | 是 | IntegerField |
| CodeName | old_code_name | 代码 | nchar；字节长度 60 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePFieldValid`；原码 `FieldType, Code` → 父表原码 `FieldType, Code`；依据：原界面主从 p_ProductionDetail → p_Production；原界面主从 DefectGroupDetail → DefectGroup；原界面主从 PrintStarchWasteDetail → PrintStarchWaste；原界面主从 p_FieldValidSub → p_FieldValid；原界面主从 DefectKindDetail → DefectKind；原界面主从 RequireValue → RequireClass。

### SourceDyePFieldValidSubCust — 客户订单与销售相关表（p_FieldValidSubCust，待确认）

源表：`dye.p_FieldValidSubCust`；新表：`src_dye_p_fieldvalidsubcust`；原主键：FieldType, Code, SubCode, CustomerID, Value01。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FieldType | old_field_type | 数据类型 | varchar；字节长度 20 | 否 | CharField |
| Code | old_code | 主分类编码 | varchar；字节长度 20 | 否 | CharField |
| SubCode | old_sub_code | 子分类编码 | varchar；字节长度 10 | 否 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 否 | CharField |
| Value01 | old_value01 | Value01 | varchar；字节长度 20 | 否 | CharField |
| Value02 | old_value02 | Value02 | varchar；字节长度 20 | 是 | CharField |
| NumValue | old_num_value | 数值值 | numeric(18,6) | 是 | DecimalField |
| NumValue2 | old_num_value2 | 收费价格 | decimal(10,2) | 是 | DecimalField |
| PriceUnit | old_price_unit | 收费单位 | tinyint | 是 | IntegerField |
| Description | old_description | 描述 | varchar；字节长度 500 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePFieldValidSub`；原码 `FieldType, Code, SubCode` → 父表原码 `FieldType, Code, SubCode`；依据：原界面主从 RequireValueCust → RequireValue；原界面主从 p_FieldValidSubCust → p_FieldValidSub。

### SourceDyePGray — 坯布

源表：`dye.p_Gray`；新表：`src_dye_p_gray`；原主键：GrayID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| GrayID | old_gray_id | 规格编码 | varchar；字节长度 20 | 否 | CharField |
| NameC | old_name_c | 规格名称 | varchar；字节长度 150 | 是 | CharField |
| NameE | old_name_e | 客户名称 | varchar；字节长度 150 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 50 | 是 | CharField |
| Structure | old_structure | 组织 | varchar；字节长度 50 | 是 | CharField |
| FabricKindID | old_fabric_kind_id | 胚纱类别 | varchar；字节长度 30 | 是 | CharField |
| FabricStyleID | old_fabric_style_id | 风格编码 | varchar；字节长度 10 | 是 | CharField |
| GrayWeight | old_gray_weight | 胚纱克重 | decimal(6,2) | 是 | DecimalField |
| Density | old_density | 密度 | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 20 | 是 | CharField |
| StockUnit | old_stock_unit | 库存单位 | tinyint | 是 | IntegerField |
| PriceUnit | old_price_unit | 计价单位编码 | tinyint | 是 | IntegerField |
| Place | old_place | 存放位置 | varchar；字节长度 100 | 是 | CharField |
| GrayPrice | old_gray_price | 胚纱价格 | decimal(10,2) | 是 | DecimalField |
| ProdPrice | old_prod_price | 成品价格 | decimal(10,2) | 是 | DecimalField |
| ProdWeight | old_prod_weight | 成品克重 | decimal(6,2) | 是 | DecimalField |
| Mnemonic | old_mnemonic | 助记符 | varchar；字节长度 10 | 是 | CharField |
| Graphic | old_graphic | 图案 | image | 是 | BinaryField |
| IsSample | old_is_sample | 样品否 | bit | 是 | BooleanField |
| IsStop | old_is_stop | 停用否 | bit | 是 | BooleanField |
| StopDate | old_stop_date | 停用时间 | datetime | 是 | DateTimeField |
| WidthDn | old_width_dn | 门幅下限 | decimal(6,2) | 是 | DecimalField |
| WidthUp | old_width_up | 门幅上限 | decimal(6,2) | 是 | DecimalField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| ProductionID | old_production_id | 工序路私 | varchar；字节长度 20 | 是 | CharField |
| RealLoss | old_real_loss | RealLoss | decimal(6,2) | 是 | DecimalField |
| AddLoss | old_add_loss | AddLoss | decimal(10,2) | 是 | DecimalField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 150 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 50 | 是 | CharField |
| OldGrayID | old_old_gray_id | 旧编号 | varchar；字节长度 120 | 是 | CharField |
| PCS | old_pcs | 粒/件 | int | 是 | IntegerField |
| FatherGrayID | old_father_gray_id | 父系规格 | varchar；字节长度 50 | 是 | CharField |
| JNKind | old_jnkind | 加捻分类 | varchar；字节长度 50 | 是 | CharField |
| STKind | old_stkind | 松筒分类 | varchar；字节长度 50 | 是 | CharField |
| ZTKind | old_ztkind | 装缸脱水分类 | varchar；字节长度 50 | 是 | CharField |
| RSKind | old_rskind | 染色分类 | varchar；字节长度 50 | 是 | CharField |
| JTKind | old_jtkind | 紧筒分类 | varchar；字节长度 50 | 是 | CharField |
| ChengBen0 | old_cheng_ben0 | 染色成本 | decimal(6,2) | 是 | DecimalField |
| ChengBen1 | old_cheng_ben1 | 前纺成本 | decimal(6,2) | 是 | DecimalField |
| ChengBen2 | old_cheng_ben2 | 后纺成本 | decimal(6,2) | 是 | DecimalField |
| ChengBen3 | old_cheng_ben3 | 加捻成本 | decimal(6,2) | 是 | DecimalField |
| ChengBen4 | old_cheng_ben4 | 包装成本 | decimal(6,2) | 是 | DecimalField |
| ChengBen5 | old_cheng_ben5 | 合股夹纱成本 | decimal(6,2) | 是 | DecimalField |
| JiJianPiece0 | old_ji_jian_piece0 | JiJianPiece0 | decimal(6,2) | 是 | DecimalField |
| JiJianPiece1 | old_ji_jian_piece1 | JiJianPiece1 | decimal(6,2) | 是 | DecimalField |
| JiJianPiece2 | old_ji_jian_piece2 | JiJianPiece2 | decimal(6,2) | 是 | DecimalField |
| JiJianPiece3 | old_ji_jian_piece3 | JiJianPiece3 | decimal(6,2) | 是 | DecimalField |
| JiJianPiece4 | old_ji_jian_piece4 | JiJianPiece4 | decimal(6,2) | 是 | DecimalField |
| JiJianPiece5 | old_ji_jian_piece5 | JiJianPiece5 | decimal(6,2) | 是 | DecimalField |

### SourceDyePGrayBak — 坯布半成品成品与仓储相关表（p_GrayBak，待确认）

源表：`dye.p_GrayBak`；新表：`src_dye_p_graybak`；原主键：GrayID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| GrayID | old_gray_id | GrayID | varchar；字节长度 20 | 否 | CharField |
| NameC | old_name_c | NameC | varchar；字节长度 200 | 是 | CharField |
| NameE | old_name_e | NameE | varchar；字节长度 60 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 50 | 是 | CharField |
| Structure | old_structure | Structure | varchar；字节长度 50 | 是 | CharField |
| FabricKindID | old_fabric_kind_id | FabricKindID | varchar；字节长度 10 | 是 | CharField |
| FabricStyleID | old_fabric_style_id | FabricStyleID | varchar；字节长度 10 | 是 | CharField |
| GrayWeight | old_gray_weight | GrayWeight | decimal(6,2) | 是 | DecimalField |
| Density | old_density | Density | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 20 | 是 | CharField |
| StockUnit | old_stock_unit | StockUnit | tinyint | 是 | IntegerField |
| PriceUnit | old_price_unit | PriceUnit | tinyint | 是 | IntegerField |
| Place | old_place | Place | varchar；字节长度 100 | 是 | CharField |
| GrayPrice | old_gray_price | GrayPrice | decimal(10,2) | 是 | DecimalField |
| ProdPrice | old_prod_price | ProdPrice | decimal(10,2) | 是 | DecimalField |
| ProdWeight | old_prod_weight | ProdWeight | decimal(6,2) | 是 | DecimalField |
| Mnemonic | old_mnemonic | Mnemonic | varchar；字节长度 10 | 是 | CharField |
| Graphic | old_graphic | Graphic | image | 是 | BinaryField |
| IsSample | old_is_sample | IsSample | bit | 是 | BooleanField |
| IsStop | old_is_stop | IsStop | bit | 是 | BooleanField |
| StopDate | old_stop_date | StopDate | datetime | 是 | DateTimeField |
| WidthDn | old_width_dn | WidthDn | decimal(6,2) | 是 | DecimalField |
| WidthUp | old_width_up | WidthUp | decimal(6,2) | 是 | DecimalField |
| Description | old_description | Description | varchar；字节长度 100 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| ProductionID | old_production_id | ProductionID | varchar；字节长度 20 | 是 | CharField |
| RealLoss | old_real_loss | RealLoss | decimal(6,2) | 是 | DecimalField |
| AddLoss | old_add_loss | AddLoss | decimal(10,2) | 是 | DecimalField |
| CustSelfProduct | old_cust_self_product | CustSelfProduct | varchar；字节长度 200 | 是 | CharField |
| Width | old_width | Width | varchar；字节长度 50 | 是 | CharField |
| Weight | old_weight | Weight | varchar；字节长度 50 | 是 | CharField |
| ZhiTong | old_zhi_tong | ZhiTong | float | 是 | FloatField |
| KongJi | old_kong_ji | KongJi | float | 是 | FloatField |
| ProportionOfComponents | old_proportion_of_components | ProportionOfComponents | varchar；字节长度 50 | 是 | CharField |
| shaguan | old_shaguan | shaguan | varchar；字节长度 20 | 是 | CharField |
| jianju | old_jianju | jianju | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 50 | 是 | CharField |
| FabricID | old_fabric_id | FabricID | varchar；字节长度 50 | 是 | CharField |

### SourceDyePITOnRest — 基础主数据相关表（p_ITOnRest，待确认）

源表：`dye.p_ITOnRest`；新表：`src_dye_p_itonrest`；原主键：EmpID, RowNo。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| EmpID | old_emp_id | EmpID | varchar；字节长度 50 | 否 | CharField |
| RowNo | old_row_no | RowNo | tinyint | 否 | IntegerField |
| Kind | old_kind | 类型：临时；每周 | tinyint | 是 | IntegerField |
| DayNum | old_day_num | DayNum | smallint | 是 | IntegerField |
| BeginTime | old_begin_time | BeginTime | datetime | 是 | DateTimeField |
| EndTime | old_end_time | EndTime | datetime | 是 | DateTimeField |

### SourceDyePITWatch — 基础主数据相关表（p_ITWatch，待确认）

源表：`dye.p_ITWatch`；新表：`src_dye_p_itwatch`；原主键：EmpID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| EmpID | old_emp_id | EmpID | varchar；字节长度 50 | 否 | CharField |
| WorkBegin | old_work_begin | WorkBegin | time | 是 | TimeField |
| WorkEnd | old_work_end | WorkEnd | time | 是 | TimeField |
| Remarks | old_remarks | Remarks | varchar；字节长度 200 | 是 | CharField |

### SourceDyePLable — 染色工艺与配方相关表（p_Lable，待确认）

源表：`dye.p_Lable`；新表：`src_dye_p_lable`；原主键：LableID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| LableID | old_lable_id | LableID | varchar；字节长度 10 | 否 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| LableName | old_lable_name | LableName | varchar；字节长度 50 | 是 | CharField |
| LableKind | old_lable_kind | LableKind | tinyint | 是 | IntegerField |
| SpecData | old_spec_data | SpecData | image | 是 | BinaryField |
| FabricID | old_fabric_id | FabricID | varchar；字节长度 128 | 是 | CharField |
| FabricNameC | old_fabric_name_c | FabricNameC | varchar；字节长度 50 | 是 | CharField |
| FabricNameE | old_fabric_name_e | FabricNameE | varchar；字节长度 50 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 是 | CharField |
| Grade | old_grade | Grade | nvarchar；字节长度 20 | 是 | CharField |
| Color | old_color | Color | varchar；字节长度 20 | 是 | CharField |
| ShortName | old_short_name | ShortName | varchar；字节长度 50 | 是 | CharField |
| FullName | old_full_name | FullName | nvarchar；字节长度 120 | 是 | CharField |
| BarCode | old_bar_code | BarCode | varchar；字节长度 50 | 是 | CharField |
| JobMainNo | old_job_main_no | JobMainNo | varchar；字节长度 20 | 是 | CharField |
| Meter | old_meter | Meter | decimal(10,2) | 是 | DecimalField |
| JobDetailNo | old_job_detail_no | JobDetailNo | varchar；字节长度 20 | 是 | CharField |
| Kg | old_kg | Kg | decimal(10,2) | 是 | DecimalField |
| Pound | old_pound | Pound | decimal(10,2) | 是 | DecimalField |
| Yard | old_yard | Yard | decimal(10,2) | 是 | DecimalField |
| Width | old_width | Width | decimal(6,2) | 是 | DecimalField |
| Thick | old_thick | Thick | decimal(6,2) | 是 | DecimalField |
| StopDate | old_stop_date | StopDate | datetime | 是 | DateTimeField |
| Description | old_description | Description | varchar；字节长度 100 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |

### SourceDyePMachine — 机台设备

源表：`dye.p_Machine`；新表：`src_dye_p_machine`；原主键：MachineID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| MachineID | old_machine_id | 机台编码 | varchar；字节长度 20 | 否 | CharField |
| Name | old_name | 机台名称 | varchar；字节长度 60 | 是 | CharField |
| MachineKindID | old_machine_kind_id | 机型代码 | varchar；字节长度 10 | 是 | CharField |
| WorkShopID | old_work_shop_id | 生产车间代码 | varchar；字节长度 10 | 是 | CharField |
| StationID | old_station_id | 站别代码 | varchar；字节长度 10 | 是 | CharField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |
| KindName | old_kind_name | 机台类别 | varchar；字节长度 100 | 是 | CharField |
| MaxRolls | old_max_rolls | 最大粒数 | int | 是 | IntegerField |
| MAxSpindles | old_max_spindles | 最大锭数 | int | 是 | IntegerField |
| Rate | old_rate | 水比 | decimal(7,1) | 是 | DecimalField |
| bit1 | old_bit1 | 设备巡检 | bit | 是 | BooleanField |
| bit2 | old_bit2 | 配件更换 | bit | 是 | BooleanField |
| bit3 | old_bit3 | 器具巡检 | bit | 是 | BooleanField |
| bit4 | old_bit4 | 暂空 | bit | 是 | BooleanField |
| bit5 | old_bit5 | 部位润滑 | bit | 是 | BooleanField |
| bit6 | old_bit6 | 清洁卫生 | bit | 是 | BooleanField |
| bit7 | old_bit7 | 安全检查 | bit | 是 | BooleanField |
| bit8 | old_bit8 | 暂空 | bit | 是 | BooleanField |
| IPAddress | old_ipaddress | IP地址 | varchar；字节长度 25 | 是 | CharField |
| IsStop | old_is_stop | 是否停用 | bit | 是 | BooleanField |
| StopDate | old_stop_date | 停用时间 | datetime | 是 | DateTimeField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| MachineNo | old_machine_no | 机台编号 | smallint | 是 | IntegerField |
| Speed | old_speed | 转速 | decimal(8,2) | 是 | DecimalField |
| MachineType | old_machine_type | 机型 | tinyint | 是 | IntegerField |
| NameE | old_name_e | NameE | varchar；字节长度 128 | 是 | CharField |
| PreMinutes | old_pre_minutes | PreMinutes | smallint | 是 | IntegerField |
| Ports | old_ports | Ports | tinyint | 是 | IntegerField |
| OPCs | old_opcs | OPCs | tinyint | 是 | IntegerField |
| IsMain | old_is_main | IsMain | bit | 是 | BooleanField |
| Model | old_model | 电视分组显示 | nvarchar；字节长度 40 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 200 | 是 | CharField |
| Power | old_power | Power | nvarchar；字节长度 40 | 是 | CharField |
| Purpose | old_purpose | Purpose | varchar；字节长度 100 | 是 | CharField |
| Manufacturer | old_manufacturer | 制造商 | nvarchar；字节长度 128 | 是 | CharField |
| ProduceDate | old_produce_date | ProduceDate | datetime | 是 | DateTimeField |
| ManufactureNo | old_manufacture_no | ManufactureNo | varchar；字节长度 50 | 是 | CharField |
| Supplier | old_supplier | Supplier | varchar；字节长度 100 | 是 | CharField |
| Capacity | old_capacity | Capacity | decimal(10,2) | 是 | DecimalField |
| UnitStr | old_unit_str | UnitStr | varchar；字节长度 6 | 是 | CharField |
| AcceptDate | old_accept_date | AcceptDate | datetime | 是 | DateTimeField |
| InDate | old_in_date | InDate | datetime | 是 | DateTimeField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 10 | 是 | CharField |
| Place | old_place | Place | varchar；字节长度 100 | 是 | CharField |
| MinVatQty | old_min_vat_qty | MinVatQty | decimal(10,2) | 是 | DecimalField |
| MaxWaitVats | old_max_wait_vats | MaxWaitVats | decimal(6,1) | 是 | DecimalField |
| SequenceNo | old_sequence_no | SequenceNo | varchar；字节长度 50 | 是 | CharField |
| IsProcess | old_is_process | IsProcess | bit | 是 | BooleanField |
| MachineIndex | old_machine_index | MachineIndex | int | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | 分厂 | varchar；字节长度 20 | 是 | CharField |
| MachineStatus | old_machine_status | MachineStatus | varchar；字节长度 10 | 是 | CharField |
| MachineClass | old_machine_class | MachineClass | nvarchar；字节长度 200 | 是 | CharField |

### SourceDyePMachineColor — 设备维护与能耗相关表（p_MachineColor，待确认）

源表：`dye.p_MachineColor`；新表：`src_dye_p_machinecolor`；原主键：MachineID, ColorDepthID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| MachineID | old_machine_id | 机台编码 | varchar；字节长度 10 | 否 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 10 | 否 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 300 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePMachine`；原码 `MachineID` → 父表原码 `MachineID`；依据：原界面主从 p_MachineColor → p_Machine。

### SourceDyePMachineFaultClass — 设备维护与能耗相关表（p_MachineFaultClass，待确认）

源表：`dye.p_MachineFaultClass`；新表：`src_dye_p_machinefaultclass`；原主键：Class1, Class2, Class3。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| RecordID | old_record_id | 唯一ID | uniqueidentifier | 否 | UUIDField |
| SortNo | old_sort_no | 序号 | varchar；字节长度 10 | 否 | CharField |
| Class1 | old_class1 | 一级分类 | nvarchar；字节长度 100 | 否 | CharField |
| Class2 | old_class2 | 二级分类 | nvarchar；字节长度 100 | 否 | CharField |
| Class3 | old_class3 | 三级分类 | nvarchar；字节长度 100 | 否 | CharField |
| EmpGroup | old_emp_group | 维修分组 | nvarchar；字节长度 40 | 否 | CharField |

### SourceDyePMachineFaultStatus — 设备维护与能耗相关表（p_MachineFaultStatus，待确认）

源表：`dye.p_MachineFaultStatus`；新表：`src_dye_p_machinefaultstatus`；原主键：StatusID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| StatusID | old_status_id | StatusID | int | 否 | IntegerField |
| StatusName | old_status_name | StatusName | nvarchar；字节长度 40 | 否 | CharField |
| StatusType | old_status_type | StatusType | nvarchar；字节长度 40 | 否 | CharField |
| FontColor | old_font_color | FontColor | varchar；字节长度 10 | 是 | CharField |
| BackColor | old_back_color | BackColor | varchar；字节长度 10 | 是 | CharField |
| TypeFontColor | old_type_font_color | TypeFontColor | varchar；字节长度 10 | 是 | CharField |
| TypeBackColor | old_type_back_color | TypeBackColor | varchar；字节长度 10 | 是 | CharField |
| CompleteStatus | old_complete_status | CompleteStatus | varchar；字节长度 10 | 否 | CharField |

### SourceDyePMachinePart — 设备维护与能耗相关表（p_MachinePart，待确认）

源表：`dye.p_MachinePart`；新表：`src_dye_p_machinepart`；原主键：MachineID, PartID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| MachineID | old_machine_id | 机台编码 | varchar；字节长度 10 | 否 | CharField |
| PartID | old_part_id | 部位编码 | varchar；字节长度 10 | 否 | CharField |
| PartName | old_part_name | 部位名称 | varchar；字节长度 50 | 是 | CharField |
| ArticleID | old_article_id | 物料代码 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePMachine`；原码 `MachineID` → 父表原码 `MachineID`；依据：原界面主从 p_MachinePart → p_Machine。

### SourceDyePMachinePoint — 设备维护与能耗相关表（p_MachinePoint，待确认）

源表：`dye.p_MachinePoint`；新表：`src_dye_p_machinepoint`；原主键：MachineID, PointNo。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| MachineID | old_machine_id | 机台号 | varchar；字节长度 10 | 否 | CharField |
| PointNo | old_point_no | 采控点编号 | tinyint | 否 | IntegerField |
| PortID | old_port_id | 串口编号 | varchar；字节长度 10 | 是 | CharField |
| ModuleID | old_module_id | 模块编号 | varchar；字节长度 10 | 是 | CharField |
| ChannelNo | old_channel_no | 通道号 | tinyint | 是 | IntegerField |
| ParamID | old_param_id | 参数编码 | varchar；字节长度 10 | 是 | CharField |
| PPName | old_ppname | 参数名称 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| PointType | old_point_type | 采控点类别 | tinyint | 是 | IntegerField |
| PointPlace | old_point_place | 采控点位置 | tinyint | 是 | IntegerField |
| Precision | old_precision | 存储精度 | tinyint | 是 | IntegerField |
| MethodID | old_method_id | 通讯方法编码 | varchar；字节长度 10 | 是 | CharField |
| Express | old_express | 表达式 | varchar；字节长度 500 | 是 | CharField |
| MeterID | old_meter_id | 仪表编号 | varchar；字节长度 10 | 是 | CharField |
| AlarmDelta | old_alarm_delta | AlarmDelta | decimal(10,2) | 是 | DecimalField |
| CommunicatWay | old_communicat_way | CommunicatWay | tinyint | 是 | IntegerField |
| IsNotShow | old_is_not_show | IsNotShow | bit | 是 | BooleanField |
| AddrNo | old_addr_no | AddrNo | varchar；字节长度 12 | 是 | CharField |
| GatherWay | old_gather_way | GatherWay | varchar；字节长度 1 | 是 | CharField |
| BelongPart | old_belong_part | BelongPart | tinyint | 是 | IntegerField |
| EnergyCutRatio | old_energy_cut_ratio | EnergyCutRatio | decimal(3,2) | 是 | DecimalField |
| IsCompare | old_is_compare | 是否执行对比 | bit | 是 | BooleanField |

关联 `source_parent_1` → `erp_base.SourceDyePMachine`；原码 `MachineID` → 父表原码 `MachineID`；依据：原界面主从 p_MachinePoint → p_Machine。

### SourceDyePMachinePort — 设备维护与能耗相关表（p_MachinePort，待确认）

源表：`dye.p_MachinePort`；新表：`src_dye_p_machineport`；原主键：MachineID, PortNum。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| MachineID | old_machine_id | MachineID | varchar；字节长度 10 | 否 | CharField |
| PortNum | old_port_num | PortNum | tinyint | 否 | IntegerField |
| BaudRate | old_baud_rate | BaudRate | varchar；字节长度 10 | 是 | CharField |
| StopBits | old_stop_bits | StopBits | tinyint | 是 | IntegerField |
| DataBits | old_data_bits | DataBits | tinyint | 是 | IntegerField |
| Parity | old_parity | Parity | varchar；字节长度 15 | 是 | CharField |
| WriteInterval | old_write_interval | WriteInterval | int | 是 | IntegerField |
| Points | old_points | Points | tinyint | 是 | IntegerField |
| IPAddress | old_ipaddress | IPAddress | varchar；字节长度 50 | 是 | CharField |

### SourceDyePMachineProcess — 设备维护与能耗相关表（p_MachineProcess，待确认）

源表：`dye.p_MachineProcess`；新表：`src_dye_p_machineprocess`；原主键：MachineID, ProcessID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| MachineID | old_machine_id | 机台编号 | varchar；字节长度 10 | 否 | CharField |
| ProcessID | old_process_id | 工序代码 | varchar；字节长度 10 | 否 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 300 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePMachine`；原码 `MachineID` → 父表原码 `MachineID`；依据：原界面主从 p_MachineProcess → p_Machine。

### SourceDyePMachineProd — 设备维护与能耗相关表（p_MachineProd，待确认）

源表：`dye.p_MachineProd`；新表：`src_dye_p_machineprod`；原主键：MachineID, ProdKindID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| MachineID | old_machine_id | 机台编码 | varchar；字节长度 10 | 否 | CharField |
| ProdKindID | old_prod_kind_id | 纱种分类编码 | varchar；字节长度 10 | 否 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 300 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePMachine`；原码 `MachineID` → 父表原码 `MachineID`；依据：原界面主从 p_MachineProd → p_Machine。

### SourceDyePMachineShift — 设备维护与能耗相关表（p_MachineShift，待确认）

源表：`dye.p_MachineShift`；新表：`src_dye_p_machineshift`；原主键：MachineID, ShiftID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| MachineID | old_machine_id | MachineID | varchar；字节长度 20 | 否 | CharField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 10 | 否 | CharField |

### SourceDyePMeter — 设备维护与能耗相关表（p_Meter，待确认）

源表：`dye.p_Meter`；新表：`src_dye_p_meter`；原主键：MeterID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| MeterID | old_meter_id | 仪表编号 | varchar；字节长度 10 | 否 | CharField |
| Name | old_name | 名称 | varchar；字节长度 500 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 200 | 是 | CharField |
| DeptID | old_dept_id | 部门编码 | varchar；字节长度 10 | 是 | CharField |
| ClassID | old_class_id | 班别代码 | varchar；字节长度 10 | 是 | CharField |
| ParentMeterID | old_parent_meter_id | 父表代码 | varchar；字节长度 10 | 是 | CharField |
| AddrNo | old_addr_no | 地址号 | varchar；字节长度 12 | 是 | CharField |
| Manufacturer | old_manufacturer | 生产厂家 | varchar；字节长度 100 | 是 | CharField |
| Place | old_place | 存放位置 | varchar；字节长度 100 | 是 | CharField |
| EnergyKind | old_energy_kind | 能耗类型 | tinyint | 是 | IntegerField |
| GatherWay | old_gather_way | 采集方式 | varchar；字节长度 1 | 是 | CharField |
| LastAdjustTime | old_last_adjust_time | 最后校准时间 | datetime | 是 | DateTimeField |
| LastCommTime | old_last_comm_time | 最后通讯时间 | datetime | 是 | DateTimeField |
| LimitDays | old_limit_days | 收款期限 | int | 是 | IntegerField |
| Ratio | old_ratio | 比例 | decimal(12,5) | 是 | DecimalField |
| Status | old_status | 状态 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| IPAddress | old_ipaddress | IP地址 | varchar；字节长度 50 | 是 | CharField |
| RegisterAddress | old_register_address | 寄存器地址 | varchar；字节长度 10 | 是 | CharField |
| RegisterNumber | old_register_number | 寄存器数量 | varchar；字节长度 10 | 是 | CharField |
| MeasureGrade | old_measure_grade | 能源计量级别 | tinyint | 是 | IntegerField |
| ReadQty | old_read_qty | 读数 | decimal(18,6) | 是 | DecimalField |
| GroupNo | old_group_no | 分组号 | varchar；字节长度 20 | 是 | CharField |
| MaxValue | old_max_value | 最大值 | decimal(10,2) | 是 | DecimalField |
| PortID | old_port_id | 串口编号 | varchar；字节长度 10 | 是 | CharField |
| Multiple | old_multiple | Multiple | decimal(12,6) | 是 | DecimalField |
| DayStartReadQty | old_day_start_read_qty | DayStartReadQty | decimal(10,2) | 是 | DecimalField |
| IsContrast | old_is_contrast | IsContrast | bit | 是 | BooleanField |
| FuncCode | old_func_code | FuncCode | varchar；字节长度 20 | 是 | CharField |
| CommunicatWay | old_communicat_way | CommunicatWay | tinyint | 是 | IntegerField |
| CommStr | old_comm_str | CommStr | varchar；字节长度 200 | 是 | CharField |
| Error_Check | old_error_check | Error_Check | varchar；字节长度 5 | 是 | CharField |
| ParseWay | old_parse_way | ParseWay | tinyint | 是 | IntegerField |
| GatherKind | old_gather_kind | GatherKind | tinyint | 是 | IntegerField |
| IsStop | old_is_stop | 是否停用 | bit | 是 | BooleanField |
| Mnemonic | old_mnemonic | Mnemonic | varchar；字节长度 200 | 是 | CharField |
| Model | old_model | 分组统计 | varchar；字节长度 50 | 是 | CharField |

### SourceDyePMeterAlarm — 设备维护与能耗相关表（p_MeterAlarm，待确认）

源表：`dye.p_MeterAlarm`；新表：`src_dye_p_meteralarm`；原主键：MeterID, PortNum, AddrNo。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| MeterID | old_meter_id | MeterID | varchar；字节长度 10 | 否 | CharField |
| PortNum | old_port_num | PortNum | tinyint | 否 | IntegerField |
| AddrNo | old_addr_no | AddrNo | varchar；字节长度 12 | 否 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |

### SourceDyePMeterMachine — 设备维护与能耗相关表（p_MeterMachine，待确认）

源表：`dye.p_MeterMachine`；新表：`src_dye_p_metermachine`；原主键：MeterID, MachineID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| MeterID | old_meter_id | 仪表编号 | varchar；字节长度 10 | 否 | CharField |
| MachineID | old_machine_id | 机台编号 | varchar；字节长度 10 | 否 | CharField |
| Ratio | old_ratio | 比例 | decimal(12,5) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePMeter`；原码 `MeterID` → 父表原码 `MeterID`；依据：原界面主从 p_MeterMachine → p_Meter。

### SourceDyePPDesign — 基础主数据相关表（p_PDesign，待确认）

源表：`dye.p_PDesign`；新表：`src_dye_p_pdesign`；原主键：DesignNo。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| DesignNo | old_design_no | DesignNo | varchar；字节长度 50 | 否 | CharField |
| Name | old_name | Name | varchar；字节长度 60 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| CustDesignNo | old_cust_design_no | CustDesignNo | varchar；字节长度 20 | 是 | CharField |
| LabSheetNo | old_lab_sheet_no | LabSheetNo | varchar；字节长度 20 | 是 | CharField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 是 | CharField |
| Weight | old_weight | Weight | decimal(6,2) | 是 | DecimalField |
| Width | old_width | Width | decimal(6,2) | 是 | DecimalField |
| PrintKind | old_print_kind | PrintKind | varchar；字节长度 2 | 是 | CharField |
| Colors | old_colors | Colors | smallint | 是 | IntegerField |
| Sets | old_sets | Sets | tinyint | 是 | IntegerField |
| DifficultyID | old_difficulty_id | DifficultyID | varchar；字节长度 10 | 是 | CharField |
| GetSampleDate | old_get_sample_date | GetSampleDate | datetime | 是 | DateTimeField |
| ScreenRepeat | old_screen_repeat | ScreenRepeat | decimal(7,2) | 是 | DecimalField |
| FinishRepeat | old_finish_repeat | FinishRepeat | decimal(7,2) | 是 | DecimalField |
| StrikedTime | old_striked_time | StrikedTime | datetime | 是 | DateTimeField |
| StrikeOffFee | old_strike_off_fee | StrikeOffFee | decimal(10,2) | 是 | DecimalField |
| ProgramID | old_program_id | ProgramID | varchar；字节长度 10 | 是 | CharField |
| Status | old_status | Status | tinyint | 是 | IntegerField |
| IsStop | old_is_stop | IsStop | bit | 是 | BooleanField |
| StopDate | old_stop_date | StopDate | datetime | 是 | DateTimeField |
| Description | old_description | Description | varchar；字节长度 100 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| SamplerID | old_sampler_id | SamplerID | varchar；字节长度 10 | 是 | CharField |
| DrawerID | old_drawer_id | DrawerID | varchar；字节长度 10 | 是 | CharField |

### SourceDyePPDesignDetail — 基础主数据相关表（p_PDesignDetail，待确认）

源表：`dye.p_PDesignDetail`；新表：`src_dye_p_pdesigndetail`；原主键：DesignNo, SequenceNo。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| DesignNo | old_design_no | DesignNo | varchar；字节长度 50 | 否 | CharField |
| SequenceNo | old_sequence_no | SequenceNo | bigint | 否 | BigIntegerField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 否 | CharField |
| Percent | old_percent | Percent | decimal(4,3) | 是 | DecimalField |

### SourceDyePPDesignSet — 基础主数据相关表（p_PDesignSet，待确认）

源表：`dye.p_PDesignSet`；新表：`src_dye_p_pdesignset`；原主键：DesignNo, ColorSeries。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| DesignNo | old_design_no | DesignNo | varchar；字节长度 50 | 否 | CharField |
| ColorSeries | old_color_series | ColorSeries | varchar；字节长度 20 | 否 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 20 | 是 | CharField |
| ColorNo01 | old_color_no01 | ColorNo01 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB01 | old_color_rgb01 | ColorRGB01 | int | 是 | IntegerField |
| ColorNo02 | old_color_no02 | ColorNo02 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB02 | old_color_rgb02 | ColorRGB02 | int | 是 | IntegerField |
| ColorNo03 | old_color_no03 | ColorNo03 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB03 | old_color_rgb03 | ColorRGB03 | int | 是 | IntegerField |
| ColorNo04 | old_color_no04 | ColorNo04 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB04 | old_color_rgb04 | ColorRGB04 | int | 是 | IntegerField |
| ColorNo05 | old_color_no05 | ColorNo05 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB05 | old_color_rgb05 | ColorRGB05 | int | 是 | IntegerField |
| ColorNo06 | old_color_no06 | ColorNo06 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB06 | old_color_rgb06 | ColorRGB06 | int | 是 | IntegerField |
| ColorNo07 | old_color_no07 | ColorNo07 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB07 | old_color_rgb07 | ColorRGB07 | int | 是 | IntegerField |
| ColorNo08 | old_color_no08 | ColorNo08 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB08 | old_color_rgb08 | ColorRGB08 | int | 是 | IntegerField |
| ColorNo09 | old_color_no09 | ColorNo09 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB09 | old_color_rgb09 | ColorRGB09 | int | 是 | IntegerField |
| ColorNo10 | old_color_no10 | ColorNo10 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB10 | old_color_rgb10 | ColorRGB10 | int | 是 | IntegerField |
| ColorNo11 | old_color_no11 | ColorNo11 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB11 | old_color_rgb11 | ColorRGB11 | int | 是 | IntegerField |
| ColorNo12 | old_color_no12 | ColorNo12 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB12 | old_color_rgb12 | ColorRGB12 | int | 是 | IntegerField |
| ColorNo13 | old_color_no13 | ColorNo13 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB13 | old_color_rgb13 | ColorRGB13 | int | 是 | IntegerField |
| ColorNo14 | old_color_no14 | ColorNo14 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB14 | old_color_rgb14 | ColorRGB14 | int | 是 | IntegerField |
| ColorNo15 | old_color_no15 | ColorNo15 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB15 | old_color_rgb15 | ColorRGB15 | int | 是 | IntegerField |
| ColorNo16 | old_color_no16 | ColorNo16 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB16 | old_color_rgb16 | ColorRGB16 | int | 是 | IntegerField |
| ColorNo17 | old_color_no17 | ColorNo17 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB17 | old_color_rgb17 | ColorRGB17 | int | 是 | IntegerField |
| ColorNo18 | old_color_no18 | ColorNo18 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB18 | old_color_rgb18 | ColorRGB18 | int | 是 | IntegerField |
| ColorNo19 | old_color_no19 | ColorNo19 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB19 | old_color_rgb19 | ColorRGB19 | int | 是 | IntegerField |
| ColorNo20 | old_color_no20 | ColorNo20 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB20 | old_color_rgb20 | ColorRGB20 | int | 是 | IntegerField |
| SampleFileName | old_sample_file_name | SampleFileName | varchar；字节长度 200 | 是 | CharField |
| Description | old_description | Description | varchar；字节长度 100 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 20 | 是 | CharField |

### SourceDyePPriceList — 价格表

源表：`dye.p_PriceList`；新表：`src_dye_p_pricelist`；原主键：ID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | 编码 | varchar；字节长度 50 | 否 | CharField |
| ProdKindID | old_prod_kind_id | 成品类别 | varchar；字节长度 10 | 是 | CharField |
| WeightDn | old_weight_dn | 克重下限 | decimal(6,2) | 是 | DecimalField |
| WeightUp | old_weight_up | 克重上限 | decimal(6,2) | 是 | DecimalField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 300 | 是 | CharField |
| StuffKindID | old_stuff_kind_id | 染化料类别 | varchar；字节长度 10 | 是 | CharField |
| PriceUnit | old_price_unit | 计价单位 | tinyint | 是 | IntegerField |

### SourceDyePPriceListAtte — 财务结算与成本相关表（p_PriceListAtte，待确认）

源表：`dye.p_PriceListAtte`；新表：`src_dye_p_pricelistatte`；原主键：ID, AtteCode。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | varchar；字节长度 20 | 否 | CharField |
| AtteCode | old_atte_code | AtteCode | varchar；字节长度 10 | 否 | CharField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |

### SourceDyePPriceListColor — 色号价格表

源表：`dye.p_PriceListColor`；新表：`src_dye_p_pricelistcolor`；原主键：ID, ColorDepthID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | 编码 | varchar；字节长度 50 | 否 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 10 | 否 | CharField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 300 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePPriceList`；原码 `ID` → 父表原码 `ID`；依据：原界面主从 p_PriceListColor → p_PriceList。

### SourceDyePPriceListProcess — 工序价格表

源表：`dye.p_PriceListProcess`；新表：`src_dye_p_pricelistprocess`；原主键：ID, ProcessID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | 编码 | varchar；字节长度 50 | 否 | CharField |
| ProcessID | old_process_id | 另收费工序 | varchar；字节长度 10 | 否 | CharField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 300 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePPriceList`；原码 `ID` → 父表原码 `ID`；依据：原界面主从 p_PriceListProcess → p_PriceList。

### SourceDyePPriceListVat — 财务结算与成本相关表（p_PriceListVat，待确认）

源表：`dye.p_PriceListVat`；新表：`src_dye_p_pricelistvat`；原主键：ID, LengthDn, LengthUp。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | 编码 | varchar；字节长度 50 | 否 | CharField |
| LengthDn | old_length_dn | 最小长度 | decimal(7,2) | 否 | DecimalField |
| LengthUp | old_length_up | 最大长度 | decimal(7,2) | 否 | DecimalField |
| Unit | old_unit | 收费单位 | tinyint | 是 | IntegerField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| PhaseID | old_phase_id | 染色流程 | varchar；字节长度 10 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePPriceList`；原码 `ID` → 父表原码 `ID`；依据：原界面主从 p_PriceListVat → p_PriceList。

### SourceDyePProcess — 工序

源表：`dye.p_Process`；新表：`src_dye_p_process`；原主键：ProcessID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ProcessID | old_process_id | 工序代码 | varchar；字节长度 10 | 否 | CharField |
| Name | old_name | 名称 | varchar；字节长度 60 | 是 | CharField |
| StationID | old_station_id | 站别代码 | varchar；字节长度 10 | 是 | CharField |
| Price | old_price | 单价 | decimal(16,6) | 是 | DecimalField |
| EffiRate | old_effi_rate | 效率比例 | decimal(6,4) | 是 | DecimalField |
| CurrLimitHours | old_curr_limit_hours | 当前工序限时 | tinyint | 是 | IntegerField |
| SampleLimitHours | old_sample_limit_hours | 试样限时 | tinyint | 是 | IntegerField |
| ToArrange | old_to_arrange | 排产 | tinyint | 是 | IntegerField |
| ToMainPlan | old_to_main_plan | 排主计划 | bit | 是 | BooleanField |
| ToPopFshBox | old_to_pop_fsh_box | 结束检查框 | bit | 是 | BooleanField |
| ToInputMachine | old_to_input_machine | 输入机台 | bit | 是 | BooleanField |
| ToInputQty | old_to_input_qty | 输入数量 | bit | 是 | BooleanField |
| ToWeight | old_to_weight | 称重 | bit | 是 | BooleanField |
| IsNeedRecipe | old_is_need_recipe | 工序配方 | bit | 是 | BooleanField |
| IsOverShift | old_is_over_shift | 交接班 | bit | 是 | BooleanField |
| CanModify | old_can_modify | 修改重刷 | tinyint | 是 | IntegerField |
| CanSkip | old_can_skip | 跳过 | bit | 是 | BooleanField |
| CalcWay | old_calc_way | 统计方法 | tinyint | 是 | IntegerField |
| TimeWay | old_time_way | 刷卡时间 | tinyint | 是 | IntegerField |
| LinesInCard | old_lines_in_card | 工卡占行数 | tinyint | 是 | IntegerField |
| FixCost | old_fix_cost | 固定成本 | decimal(10,6) | 是 | DecimalField |
| StopDate | old_stop_date | 停用时间 | datetime | 是 | DateTimeField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |
| Unit | old_unit | 单位(计量，计价) | tinyint | 是 | IntegerField |
| SumLimitHours | old_sum_limit_hours | 累计工序限时 | tinyint | 是 | IntegerField |
| ToInputVehicle | old_to_input_vehicle | 输入车桶号 | bit | 是 | BooleanField |
| IsCanAddWorkQty | old_is_can_add_work_qty | 允许超出标准产量 | bit | 是 | BooleanField |
| IsUseWeight | old_is_use_weight | 按克重算成本 | bit | 是 | BooleanField |
| ReplaceProcessID | old_replace_process_id | 替代工序 | varchar；字节长度 100 | 是 | CharField |
| IsPriority | old_is_priority | 是否优先 | bit | 是 | BooleanField |
| DelayHours | old_delay_hours | 延迟时间 | int | 是 | IntegerField |
| IsExtraCharge | old_is_extra_charge | 是否另收费 | bit | 是 | BooleanField |
| IsMain | old_is_main | IsMain | bit | 是 | BooleanField |
| SortNo | old_sort_no | SortNo | smallint | 是 | IntegerField |
| ProcessPrice | old_process_price | ProcessPrice | decimal(8,2) | 是 | DecimalField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 20 | 是 | CharField |
| IsODM | old_is_odm | 是否委外 | bit | 是 | BooleanField |
| OverShiftWay | old_over_shift_way | 交接班数量检查单位 | tinyint | 是 | IntegerField |
| MaxWorkVats | old_max_work_vats | 最大上卡缸数 | decimal(10,2) | 是 | DecimalField |
| MinWorkVats | old_min_work_vats | MinWorkVats | decimal(10,2) | 是 | DecimalField |
| InputQtyCheckWay | old_input_qty_check_way | 工序刷卡产量检查方式 | tinyint | 是 | IntegerField |
| MaxWorkRolls | old_max_work_rolls | MaxWorkRolls | decimal(10,2) | 是 | DecimalField |
| MaxWorkWeight | old_max_work_weight | MaxWorkWeight | decimal(10,2) | 是 | DecimalField |
| MaxWorkLength | old_max_work_length | MaxWorkLength | decimal(10,2) | 是 | DecimalField |
| MinWorkLength | old_min_work_length | MinWorkLength | decimal(10,2) | 是 | DecimalField |
| MinWorkRolls | old_min_work_rolls | MinWorkRolls | decimal(10,2) | 是 | DecimalField |
| MinWorkWeight | old_min_work_weight | MinWorkWeight | decimal(10,2) | 是 | DecimalField |
| WorkDonePercent | old_work_done_percent | 完成比例 | decimal(5,2) | 是 | DecimalField |
| IsCheckPlan | old_is_check_plan | IsCheckPlan | bit | 是 | BooleanField |
| SortNumber | old_sort_number | SortNumber | varchar；字节长度 10 | 是 | CharField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| IsAllowedToBack | old_is_allowed_to_back | IsAllowedToBack | bit | 是 | BooleanField |
| ToInputColor | old_to_input_color | ToInputColor | bit | 是 | BooleanField |
| Stereotypes | old_stereotypes | 是否定型 | int | 是 | IntegerField |

### SourceDyePProcessArea — 染色工艺与配方相关表（p_ProcessArea，待确认）

源表：`dye.p_ProcessArea`；新表：`src_dye_p_processarea`；原主键：ProcessID, AreaID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ProcessID | old_process_id | 工序 | varchar；字节长度 50 | 否 | CharField |
| AreaID | old_area_id | 区域编码 | varchar；字节长度 10 | 否 | CharField |
| AreaIndex | old_area_index | 助记序号 | tinyint | 是 | IntegerField |
| Name | old_name | 区域名称 | varchar；字节长度 60 | 是 | CharField |
| Description | old_description | 描述 | varchar；字节长度 500 | 是 | CharField |
| IsStop | old_is_stop | 停用 | bit | 是 | BooleanField |
| StopDate | old_stop_date | 停用日期 | datetime | 是 | DateTimeField |

关联 `source_parent_1` → `erp_base.SourceDyePProcess`；原码 `ProcessID` → 父表原码 `ProcessID`；依据：原界面主从 p_ProcessArea → p_Process。

### SourceDyePProcessChemical — 染化料与称料库存相关表（p_ProcessChemical，待确认）

源表：`dye.p_ProcessChemical`；新表：`src_dye_p_processchemical`；原主键：ProcessID, ParamNo。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ProcessID | old_process_id | 工序 | varchar；字节长度 10 | 否 | CharField |
| ParamNo | old_param_no | 编号 | smallint | 否 | IntegerField |
| ParamID | old_param_id | 编码 | varchar；字节长度 10 | 是 | CharField |
| PPName | old_ppname | 名称 | varchar；字节长度 20 | 是 | CharField |
| Rate | old_rate | 比例 | decimal(10,2) | 是 | DecimalField |
| GatherWay | old_gather_way | 采集方式 | varchar；字节长度 1 | 是 | CharField |
| AlarmDelta | old_alarm_delta | 报警范围 | decimal(10,2) | 是 | DecimalField |
| Description | old_description | 描述 | varchar；字节长度 500 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePProcess`；原码 `ProcessID` → 父表原码 `ProcessID`；依据：原界面主从 p_ProcessChemical → p_Process。

### SourceDyePProcessCraft — 染色工艺与配方相关表（p_ProcessCraft，待确认）

源表：`dye.p_ProcessCraft`；新表：`src_dye_p_processcraft`；原主键：ProcessID, ParamNo。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ProcessID | old_process_id | 工序代码 | varchar；字节长度 10 | 否 | CharField |
| ParamNo | old_param_no | 参数编号 | smallint | 否 | IntegerField |
| ParamID | old_param_id | 参数编码 | varchar；字节长度 10 | 是 | CharField |
| PPName | old_ppname | 参数名称 | varchar；字节长度 20 | 是 | CharField |
| MinValue | old_min_value | 最小值 | decimal(10,2) | 是 | DecimalField |
| MaxValue | old_max_value | 最大值 | decimal(10,2) | 是 | DecimalField |
| GatherWay | old_gather_way | 收集方式 | varchar；字节长度 1 | 是 | CharField |
| AlarmDelta | old_alarm_delta | 报警范围 | decimal(10,2) | 是 | DecimalField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePProcess`；原码 `ProcessID` → 父表原码 `ProcessID`；依据：原界面主从 p_ProcessCraft → p_Process。

### SourceDyePProcessCraft1 — 染色工艺与配方相关表（p_ProcessCraft1，待确认）

源表：`dye.p_ProcessCraft1`；新表：`src_dye_p_processcraft1`；原主键：无主键。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ProcessID | old_process_id | ProcessID | varchar；字节长度 5 | 否 | CharField |
| ParamNo | old_param_no | ParamNo | smallint | 否 | IntegerField |
| ParamID | old_param_id | ParamID | varchar；字节长度 10 | 是 | CharField |
| PPName | old_ppname | PPName | varchar；字节长度 50 | 是 | CharField |
| Description | old_description | Description | varchar；字节长度 100 | 是 | CharField |
| MinValue | old_min_value | MinValue | decimal(10,2) | 是 | DecimalField |
| MaxValue | old_max_value | MaxValue | decimal(10,2) | 是 | DecimalField |
| AlarmDelta | old_alarm_delta | AlarmDelta | decimal(10,2) | 是 | DecimalField |
| GatherWay | old_gather_way | GatherWay | varchar；字节长度 1 | 是 | CharField |

### SourceDyePProcessDefect — 质量检验与异常相关表（p_ProcessDefect，待确认）

源表：`dye.p_ProcessDefect`；新表：`src_dye_p_processdefect`；原主键：ProcessID, DefectID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ProcessID | old_process_id | 工序代码 | varchar；字节长度 10 | 否 | CharField |
| DefectID | old_defect_id | 疵点代码 | varchar；字节长度 10 | 否 | CharField |
| IsStop | old_is_stop | 是否停用 | bit | 是 | BooleanField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePProcess`；原码 `ProcessID` → 父表原码 `ProcessID`；依据：原界面主从 p_ProcessDefect → p_Process。

### SourceDyePProcessPCraft — 染色工艺与配方相关表（p_ProcessPCraft，待确认）

源表：`dye.p_ProcessPCraft`；新表：`src_dye_p_processpcraft`；原主键：ProcessID, ParamNo。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ProcessID | old_process_id | 工序 | varchar；字节长度 10 | 否 | CharField |
| ParamNo | old_param_no | 参数编号 | smallint | 否 | IntegerField |
| ParamID | old_param_id | 参数编码 | varchar；字节长度 10 | 是 | CharField |
| PPName | old_ppname | 参数名称 | varchar；字节长度 20 | 是 | CharField |
| MinValue | old_min_value | 最小值 | decimal(10,2) | 是 | DecimalField |
| MaxValue | old_max_value | 最大值 | decimal(10,2) | 是 | DecimalField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePProcess`；原码 `ProcessID` → 父表原码 `ProcessID`；依据：原界面主从 p_ProcessPCraft → p_Process。

### SourceDyePProcessPrice — 财务结算与成本相关表（p_ProcessPrice，待确认）

源表：`dye.p_ProcessPrice`；新表：`src_dye_p_processprice`；原主键：ProcessID, ProdKindID, Row。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ProcessID | old_process_id | 工序代码 | varchar；字节长度 10 | 否 | CharField |
| ProdKindID | old_prod_kind_id | 纱种代码 | varchar；字节长度 10 | 否 | CharField |
| Row | old_row | 编号 | varchar；字节长度 10 | 否 | CharField |
| WeightDn | old_weight_dn | 克重下限 | decimal(6,2) | 是 | DecimalField |
| WeightUp | old_weight_up | 克重上限 | decimal(6,2) | 是 | DecimalField |
| QtyDn | old_qty_dn | 重量下限 | decimal(6,2) | 是 | DecimalField |
| QtyUP | old_qty_up | 重量上限 | decimal(6,2) | 是 | DecimalField |
| LengthDn | old_length_dn | 长度下限 | decimal(6,2) | 是 | DecimalField |
| LengthUp | old_length_up | 长度上限 | decimal(6,2) | 是 | DecimalField |
| Price | old_price | 工价 | decimal(16,6) | 是 | DecimalField |
| FixCost | old_fix_cost | 固定成本 | decimal(10,6) | 是 | DecimalField |
| EffiRate | old_effi_rate | 折合系数 | decimal(6,4) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePProcess`；原码 `ProcessID` → 父表原码 `ProcessID`；依据：原界面主从 p_ProcessPrice → p_Process。

### SourceDyePProduct — 坯布半成品成品与仓储相关表（p_Product，待确认）

源表：`dye.p_Product`；新表：`src_dye_p_product`；原主键：ProdID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 否 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 20 | 是 | CharField |
| NameC | old_name_c | 中文名称 | varchar；字节长度 200 | 是 | CharField |
| NameE | old_name_e | 英文名称 | varchar；字节长度 160 | 是 | CharField |
| Spec | old_spec | 纱种成分 | varchar；字节长度 500 | 是 | CharField |
| Structure | old_structure | 组织 | varchar；字节长度 50 | 是 | CharField |
| FabricKindID | old_fabric_kind_id | 纱种类别 | varchar；字节长度 10 | 是 | CharField |
| FabricStyleID | old_fabric_style_id | 纱种分格编码 | varchar；字节长度 10 | 是 | CharField |
| GrayWeight | old_gray_weight | 胚纱克重 | int | 是 | IntegerField |
| StockUnit | old_stock_unit | 库存单位 | tinyint | 是 | IntegerField |
| PriceUnit | old_price_unit | 计价单位编码 | tinyint | 是 | IntegerField |
| GrayPrice | old_gray_price | 胚纱价格 | decimal(10,2) | 是 | DecimalField |
| ProdPrice | old_prod_price | 成品价格 | decimal(10,2) | 是 | DecimalField |
| ProdWeight | old_prod_weight | 克重 | int | 是 | IntegerField |
| Mnemonic | old_mnemonic | 助记符 | varchar；字节长度 10 | 是 | CharField |
| Graphic | old_graphic | 图案 | image | 是 | BinaryField |
| IsSample | old_is_sample | 是否样品 | bit | 是 | BooleanField |
| IsStop | old_is_stop | 是否停用 | bit | 是 | BooleanField |
| StopDate | old_stop_date | 停用日期 | datetime | 是 | DateTimeField |
| WidthDn | old_width_dn | 门幅上限 | decimal(6,2) | 是 | DecimalField |
| WidthUp | old_width_up | 门幅下限 | decimal(6,2) | 是 | DecimalField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Density | old_density | 密度 | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 20 | 是 | CharField |
| Place | old_place | 存放位置 | varchar；字节长度 100 | 是 | CharField |
| ProdCode | old_prod_code | ProdCode | varchar；字节长度 50 | 是 | CharField |
| ProductionID | old_production_id | 工艺路线 | varchar；字节长度 50 | 是 | CharField |
| ProdWidth | old_prod_width | 幅宽 | int | 是 | IntegerField |
| WeightKindID | old_weight_kind_id | 克重单位 | nvarchar；字节长度 40 | 是 | CharField |
| WidthKindID | old_width_kind_id | 幅宽单位 | varchar；字节长度 50 | 是 | CharField |
| RGLX | old_rglx | 染缸类型 | varchar；字节长度 50 | 是 | CharField |

### SourceDyePShift — 班组班次

源表：`dye.p_Shift`；新表：`src_dye_p_shift`；原主键：ShiftID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ShiftID | old_shift_id | 班组代码 | varchar；字节长度 10 | 否 | CharField |
| ClassID | old_class_id | 班别代码 | varchar；字节长度 10 | 是 | CharField |
| StationID | old_station_id | 站别代码 | varchar；字节长度 10 | 是 | CharField |
| ChargerID | old_charger_id | 部门负责人代码 | varchar；字节长度 10 | 是 | CharField |
| Password | old_password | 查询口令 | varchar；字节长度 50 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| Name | old_name | 名称 | varchar；字节长度 60 | 是 | CharField |
| WorkShopID | old_work_shop_id | 生产车间代码 | varchar；字节长度 10 | 是 | CharField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 10 | 是 | CharField |
| WorkTimeSet | old_work_time_set | WorkTimeSet | decimal(5,1) | 是 | DecimalField |
| MachineID | old_machine_id | 机台 | varchar；字节长度 10 | 是 | CharField |
| SortNo | old_sort_no | SortNo | smallint | 是 | IntegerField |
| WorkTimeUp | old_work_time_up | WorkTimeUp | decimal(5,1) | 是 | DecimalField |
| WorkTimeDn | old_work_time_dn | WorkTimeDn | decimal(5,1) | 是 | DecimalField |
| StratDate | old_strat_date | 开始时间 | datetime | 是 | DateTimeField |
| EndDate | old_end_date | 结束日期 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |

### SourceDyePShiftArrange — 生产工单与排程相关表（p_ShiftArrange，待确认）

源表：`dye.p_ShiftArrange`；新表：`src_dye_p_shiftarrange`；原主键：ID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | tinyint | 否 | IntegerField |
| Mode | old_mode | Mode | varchar；字节长度 10 | 是 | CharField |
| BeginDate | old_begin_date | BeginDate | datetime | 是 | DateTimeField |
| CycleDays | old_cycle_days | CycleDays | varchar；字节长度 10 | 是 | CharField |
| ShiftID01 | old_shift_id01 | ShiftID01 | varchar；字节长度 10 | 是 | CharField |
| ShiftID02 | old_shift_id02 | ShiftID02 | varchar；字节长度 10 | 是 | CharField |
| ShiftID03 | old_shift_id03 | ShiftID03 | varchar；字节长度 10 | 是 | CharField |
| DateBetween01 | old_date_between01 | DateBetween01 | varchar；字节长度 100 | 是 | CharField |
| DateBetween02 | old_date_between02 | DateBetween02 | varchar；字节长度 100 | 是 | CharField |
| DateBetween03 | old_date_between03 | DateBetween03 | varchar；字节长度 100 | 是 | CharField |
| ClassID01 | old_class_id01 | ClassID01 | varchar；字节长度 10 | 是 | CharField |
| ClassID02 | old_class_id02 | ClassID02 | varchar；字节长度 10 | 是 | CharField |
| ClassID03 | old_class_id03 | ClassID03 | varchar；字节长度 10 | 是 | CharField |

### SourceDyePShiftArrangeDetail — 生产工单与排程相关表（p_ShiftArrangeDetail，待确认）

源表：`dye.p_ShiftArrangeDetail`；新表：`src_dye_p_shiftarrangedetail`；原主键：ID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | bigint | 否 | BigIntegerField |
| CurrDate | old_curr_date | CurrDate | datetime | 否 | DateTimeField |
| BeginDate | old_begin_date | BeginDate | datetime | 是 | DateTimeField |
| ShiftID01 | old_shift_id01 | ShiftID01 | varchar；字节长度 10 | 是 | CharField |
| ShiftID02 | old_shift_id02 | ShiftID02 | varchar；字节长度 10 | 是 | CharField |
| ShiftID03 | old_shift_id03 | ShiftID03 | varchar；字节长度 10 | 是 | CharField |
| DateBetween01 | old_date_between01 | DateBetween01 | varchar；字节长度 100 | 是 | CharField |
| DateBetween02 | old_date_between02 | DateBetween02 | varchar；字节长度 100 | 是 | CharField |
| DateBetween03 | old_date_between03 | DateBetween03 | varchar；字节长度 100 | 是 | CharField |
| ClassID01 | old_class_id01 | ClassID01 | varchar；字节长度 10 | 是 | CharField |
| ClassID02 | old_class_id02 | ClassID02 | varchar；字节长度 10 | 是 | CharField |
| ClassID03 | old_class_id03 | ClassID03 | varchar；字节长度 10 | 是 | CharField |
| DateBetween04 | old_date_between04 | DateBetween04 | varchar；字节长度 100 | 是 | CharField |
| ClassID04 | old_class_id04 | ClassID04 | varchar；字节长度 10 | 是 | CharField |
| ShiftID04 | old_shift_id04 | ShiftID04 | varchar；字节长度 10 | 是 | CharField |

### SourceDyePShiftEmp — 生产工单与排程相关表（p_ShiftEmp，待确认）

源表：`dye.p_ShiftEmp`；新表：`src_dye_p_shiftemp`；原主键：ShiftID, SerialNumber。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ShiftID | old_shift_id | 班组代码 | varchar；字节长度 10 | 否 | CharField |
| SerialNumber | old_serial_number | 流水号 | varchar；字节长度 30 | 否 | CharField |
| EmpID | old_emp_id | 员工编号 | varchar；字节长度 10 | 否 | CharField |
| EffiRate | old_effi_rate | 效率比例 | decimal(6,4) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| Post | old_post | 岗位 | varchar；字节长度 50 | 是 | CharField |
| MachineID | old_machine_id | 机台 | varchar；字节长度 1000 | 是 | CharField |
| WorkTime | old_work_time | 上班时间 | varchar；字节长度 10 | 是 | CharField |
| WorkLongTime | old_work_long_time | 上班时长(小时) | decimal(6,1) | 是 | DecimalField |

关联 `source_parent_1` → `erp_base.SourceDyePShift`；原码 `ShiftID` → 父表原码 `ShiftID`；依据：原界面主从 p_ShiftEmpZM → p_ShiftZM；原界面主从 p_ShiftEmpKF → p_ShiftKF；原界面主从 p_ShiftEmpZJ → p_ShiftZJ；原界面主从 p_ShiftEmp → p_Shift；原界面主从 p_ShiftEmpTS → p_ShiftTS；原界面主从 p_ShiftEmpBY → p_ShiftBY；原界面主从 p_ShiftEmpHZ → p_ShiftHZ；原界面主从 p_ShiftEmpPB → p_ShiftPB。

### SourceDyePShiftMachine — 设备维护与能耗相关表（p_ShiftMachine，待确认）

源表：`dye.p_ShiftMachine`；新表：`src_dye_p_shiftmachine`；原主键：ShiftID, MachineID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 10 | 否 | CharField |
| MachineID | old_machine_id | MachineID | varchar；字节长度 10 | 否 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |

### SourceDyePStorageUnitID — 仓储编码（库区/库位）

源表：`dye.p_StorageUnitID`；新表：`src_dye_p_storageunitid`；原主键：FieldType, Code。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FieldType | old_field_type | FieldType | varchar；字节长度 20 | 否 | CharField |
| Code | old_code | 编码 | varchar；字节长度 20 | 否 | CharField |
| Kind | old_kind | 区域类型 | varchar；字节长度 20 | 是 | CharField |
| Name | old_name | Name | varchar；字节长度 100 | 否 | CharField |

### SourceDyePStuff — 染化料

源表：`dye.p_Stuff`；新表：`src_dye_p_stuff`；原主键：StuffID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| StuffID | old_stuff_id | 染化料代码 | varchar；字节长度 20 | 否 | CharField |
| Name | old_name | 名称 | varchar；字节长度 200 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| NameE | old_name_e | 英文名称 | varchar；字节长度 128 | 是 | CharField |
| StuffType | old_stuff_type | 染化料类型 | varchar；字节长度 10 | 是 | CharField |
| Mnemonic | old_mnemonic | 助记符 | varchar；字节长度 10 | 是 | CharField |
| StorageUnitID | old_storage_unit_id | 仓位代码 | varchar；字节长度 10 | 是 | CharField |
| FactID | old_fact_id | 工厂代码 | varchar；字节长度 10 | 是 | CharField |
| RecipeUnit | old_recipe_unit | 配方单位 | tinyint | 是 | IntegerField |
| Price | old_price | 单价 | decimal(16,6) | 是 | DecimalField |
| Brand | old_brand | 牌号 | varchar；字节长度 20 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商代码 | varchar；字节长度 10 | 是 | CharField |
| WOF | old_wof | 力份 | decimal(6,3) | 是 | DecimalField |
| WeightMode | old_weight_mode | 称料方式 | tinyint | 是 | IntegerField |
| PackUnit | old_pack_unit | 包装单位 | varchar；字节长度 10 | 是 | CharField |
| RemainQty | old_remain_qty | 剩余数量 | decimal(10,2) | 是 | DecimalField |
| CupNo | old_cup_no | 滴液系统编号 | varchar；字节长度 20 | 是 | CharField |
| WeightNo | old_weight_no | 称料系统编号 | varchar；字节长度 20 | 是 | CharField |
| StuffKindID | old_stuff_kind_id | 染化料类别 | varchar；字节长度 50 | 是 | CharField |
| StockUnit | old_stock_unit | 库存单位 | varchar；字节长度 1 | 是 | CharField |
| IsBatch | old_is_batch | 批次管理 | bit | 是 | BooleanField |
| NewStuffID | old_new_stuff_id | 染化料新代码 | varchar；字节长度 10 | 是 | CharField |
| AccSubjectID | old_acc_subject_id | AccSubjectID | varchar；字节长度 10 | 是 | CharField |
| SafeQty | old_safe_qty | 安全库存 | decimal(10,2) | 是 | DecimalField |
| LimitDays | old_limit_days | 收款期限 | int | 是 | IntegerField |
| LeadDays | old_lead_days | 前置天数 | smallint | 是 | IntegerField |
| Status | old_status | 状态 | tinyint | 是 | IntegerField |
| StopDate | old_stop_date | 停用时间 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| WeightUnit | old_weight_unit | 称料单位 | varchar；字节长度 1 | 是 | CharField |
| LastPrice | old_last_price | LastPrice | decimal(16,6) | 是 | DecimalField |
| Kind | old_kind | 属性 | varchar；字节长度 10 | 是 | CharField |
| AutoSysID | old_auto_sys_id | 配送方式 | varchar；字节长度 10 | 是 | CharField |
| GaoLaodu | old_gao_laodu | 高牢度 | bit | 是 | BooleanField |
| TankNo | old_tank_no | 落料桶号 | int | 是 | IntegerField |
| Multiple | old_multiple | 配送倍数 | float | 是 | FloatField |

### SourceDyePStuffStorageUnitID — 染化料仓位对照

源表：`dye.p_StuffStorageUnitID`；新表：`src_dye_p_stuffstorageunitid`；原主键：无主键。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FieldType | old_field_type | FieldType | varchar；字节长度 50 | 是 | CharField |
| Code | old_code | Code | varchar；字节长度 50 | 是 | CharField |
| Name | old_name | Name | varchar；字节长度 50 | 是 | CharField |

### SourceDyePVehicle — 基础主数据相关表（p_Vehicle，待确认）

源表：`dye.p_Vehicle`；新表：`src_dye_p_vehicle`；原主键：VehicleNo。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| VehicleNo | old_vehicle_no | VehicleNo | varchar；字节长度 10 | 否 | CharField |
| Weight | old_weight | Weight | decimal(6,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |
| Status | old_status | Status | varchar；字节长度 1 | 是 | CharField |

### SourceDyePWareHouse — 坯布半成品成品与仓储相关表（p_WareHouse，待确认）

源表：`dye.p_WareHouse`；新表：`src_dye_p_warehouse`；原主键：WareHouseID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| WareHouseID | old_ware_house_id | WareHouseID | varchar；字节长度 10 | 否 | CharField |
| Name | old_name | Name | varchar；字节长度 60 | 是 | CharField |
| Length | old_length | Length | decimal(10,2) | 是 | DecimalField |
| Width | old_width | Width | decimal(6,2) | 是 | DecimalField |
| Graphic | old_graphic | Graphic | image | 是 | BinaryField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| StockUnit | old_stock_unit | StockUnit | tinyint | 是 | IntegerField |

### SourceDyePPasteDosage — 其他或待确认相关表（PPasteDosage，待确认）

源表：`dye.PPasteDosage`；新表：`src_dye_ppastedosage`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| OrderNo | old_order_no | 订单号 | varchar；字节长度 50 | 是 | CharField |
| PrintCode | old_print_code | 花号 | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 150 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| ColorCount | old_color_count | (最大)颜色个数 | int | 是 | IntegerField |
| MachineID | old_machine_id | 机台号 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |

### SourceDyePPasteDosageDetail — 其他或待确认相关表（PPasteDosageDetail，待确认）

源表：`dye.PPasteDosageDetail`；新表：`src_dye_ppastedosagedetail`；原主键：SheetSeries, DetailNo。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 20 | 否 | CharField |
| ColorPlateID | old_color_plate_id | 花号色位 | varchar；字节长度 10 | 是 | CharField |
| OrderDosage | old_order_dosage | 订单量 | decimal(10,2) | 是 | DecimalField |
| OrderUnit | old_order_unit | 订单单位 | varchar；字节长度 10 | 是 | CharField |
| Kind | old_kind | 类型 | varchar；字节长度 20 | 是 | CharField |
| FilmRate1 | old_film_rate1 | 菲林比1 | decimal(8,2) | 是 | DecimalField |
| Value1 | old_value1 | 值1 | varchar；字节长度 20 | 是 | CharField |
| FilmRate2 | old_film_rate2 | 菲林比2 | decimal(8,2) | 是 | DecimalField |
| Value2 | old_value2 | 值2 | varchar；字节长度 20 | 是 | CharField |
| FilmRate3 | old_film_rate3 | 菲林比3 | decimal(8,2) | 是 | DecimalField |
| Value3 | old_value3 | 值3 | varchar；字节长度 20 | 是 | CharField |
| FilmRate4 | old_film_rate4 | 菲林比4 | decimal(8,2) | 是 | DecimalField |
| Value4 | old_value4 | 值4 | varchar；字节长度 20 | 是 | CharField |
| FilmRate5 | old_film_rate5 | 菲林比5 | decimal(8,2) | 是 | DecimalField |
| Value5 | old_value5 | 值5 | varchar；字节长度 20 | 是 | CharField |
| FilmRate6 | old_film_rate6 | 菲林比6 | decimal(8,2) | 是 | DecimalField |
| Value6 | old_value6 | 值6 | varchar；字节长度 20 | 是 | CharField |
| FilmRate7 | old_film_rate7 | 菲林比7 | decimal(8,2) | 是 | DecimalField |
| Value7 | old_value7 | 值7 | varchar；字节长度 20 | 是 | CharField |
| FilmRate8 | old_film_rate8 | 菲林比8 | decimal(8,2) | 是 | DecimalField |
| Value8 | old_value8 | 值8 | varchar；字节长度 20 | 是 | CharField |
| FilmRate9 | old_film_rate9 | 菲林比9 | decimal(8,2) | 是 | DecimalField |
| Value9 | old_value9 | 值9 | varchar；字节长度 20 | 是 | CharField |
| FilmRate10 | old_film_rate10 | 菲林比10 | decimal(8,2) | 是 | DecimalField |
| Value10 | old_value10 | 值10 | varchar；字节长度 20 | 是 | CharField |
| FilmRate11 | old_film_rate11 | 菲林比11 | decimal(8,2) | 是 | DecimalField |
| Value11 | old_value11 | 值11 | varchar；字节长度 20 | 是 | CharField |
| FilmRate12 | old_film_rate12 | 菲林比12 | decimal(8,2) | 是 | DecimalField |
| Value12 | old_value12 | 值12 | varchar；字节长度 20 | 是 | CharField |
| FilmRate13 | old_film_rate13 | 菲林比13 | decimal(8,2) | 是 | DecimalField |
| Value13 | old_value13 | 值13 | varchar；字节长度 20 | 是 | CharField |
| FilmRate14 | old_film_rate14 | 菲林比14 | decimal(8,2) | 是 | DecimalField |
| Value14 | old_value14 | 值14 | varchar；字节长度 20 | 是 | CharField |
| FilmRate15 | old_film_rate15 | 菲林比15 | decimal(8,2) | 是 | DecimalField |
| Value15 | old_value15 | 值15 | varchar；字节长度 20 | 是 | CharField |
| FilmRate16 | old_film_rate16 | 菲林比16 | decimal(8,2) | 是 | DecimalField |
| Value16 | old_value16 | 值16 | varchar；字节长度 20 | 是 | CharField |

关联 `source_parent_1` → `erp_base.SourceDyePPasteDosage`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 PPasteDosageDetail → PPasteDosage。

### SourceDyePrintDipsRecord — 其他或待确认相关表（PrintDipsRecord，待确认）

源表：`dye.PrintDipsRecord`；新表：`src_dye_printdipsrecord`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | SalerGroupID | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 10 | 是 | CharField |
| ColorNo | old_color_no | ColorNo | varchar；字节长度 20 | 是 | CharField |
| ColorVersion | old_color_version | ColorVersion | varchar；字节长度 20 | 是 | CharField |
| ConfirmVersion | old_confirm_version | ConfirmVersion | varchar；字节长度 20 | 是 | CharField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 10 | 是 | CharField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 是 | CharField |
| MainStuffKindID | old_main_stuff_kind_id | MainStuffKindID | varchar；字节长度 10 | 是 | CharField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 是 | CharField |
| Structure | old_structure | Structure | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 20 | 是 | CharField |
| ColorDepthID | old_color_depth_id | ColorDepthID | varchar；字节长度 10 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 20 | 是 | CharField |
| CustColorNum | old_cust_color_num | CustColorNum | varchar；字节长度 20 | 是 | CharField |
| ColorE | old_color_e | ColorE | varchar；字节长度 20 | 是 | CharField |
| ColorRGB | old_color_rgb | ColorRGB | int | 是 | IntegerField |
| RecipePriceSource | old_recipe_price_source | RecipePriceSource | tinyint | 是 | IntegerField |
| FabricSource | old_fabric_source | FabricSource | varchar；字节长度 1 | 是 | CharField |
| Weight | old_weight | Weight | decimal(6,2) | 是 | DecimalField |
| CostEffirate | old_cost_effirate | CostEffirate | decimal(6,2) | 是 | DecimalField |
| Cost | old_cost | Cost | decimal(10,2) | 是 | DecimalField |
| CostUnit | old_cost_unit | CostUnit | varchar；字节长度 1 | 是 | CharField |
| VerLight1ID | old_ver_light1_id | VerLight1ID | varchar；字节长度 10 | 是 | CharField |
| VerLight2ID | old_ver_light2_id | VerLight2ID | varchar；字节长度 10 | 是 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 10 | 是 | CharField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 10 | 是 | CharField |
| CheckerID | old_checker_id | CheckerID | varchar；字节长度 10 | 是 | CharField |
| DlvSampleDate | old_dlv_sample_date | DlvSampleDate | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyePrintScreen — 其他或待确认相关表（PrintScreen，待确认）

源表：`dye.PrintScreen`；新表：`src_dye_printscreen`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| DesignNo | old_design_no | DesignNo | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| PrintKind | old_print_kind | PrintKind | varchar；字节长度 2 | 是 | CharField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| ScreenerID | old_screener_id | ScreenerID | varchar；字节长度 10 | 是 | CharField |
| Sets | old_sets | Sets | tinyint | 是 | IntegerField |
| ScreenFee | old_screen_fee | ScreenFee | decimal(10,2) | 是 | DecimalField |
| StorageUnitIDs | old_storage_unit_ids | StorageUnitIDs | varchar；字节长度 100 | 是 | CharField |
| FileName | old_file_name | FileName | varchar；字节长度 100 | 是 | CharField |
| DrawerID | old_drawer_id | DrawerID | varchar；字节长度 10 | 是 | CharField |
| ScreenFinishTime | old_screen_finish_time | ScreenFinishTime | datetime | 是 | DateTimeField |

### SourceDyePrintScreenDetail — 其他或待确认相关表（PrintScreenDetail，待确认）

源表：`dye.PrintScreenDetail`；新表：`src_dye_printscreendetail`；原主键：ScreenNo。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| ScreenNo | old_screen_no | ScreenNo | varchar；字节长度 20 | 否 | CharField |
| DesignDetailNo | old_design_detail_no | DesignDetailNo | varchar；字节长度 20 | 是 | CharField |
| Status | old_status | Status | tinyint | 是 | IntegerField |
| SequenceNo | old_sequence_no | SequenceNo | bigint | 是 | BigIntegerField |
| Percent | old_percent | Percent | decimal(4,3) | 是 | DecimalField |
| Mesh | old_mesh | Mesh | smallint | 是 | IntegerField |
| ScreenRepeat | old_screen_repeat | ScreenRepeat | decimal(7,2) | 是 | DecimalField |
| Width | old_width | Width | decimal(6,2) | 是 | DecimalField |
| SortNo | old_sort_no | SortNo | smallint | 是 | IntegerField |
| Description | old_description | Description | varchar；字节长度 100 | 是 | CharField |

### SourceDyePrintScreenRecord — 其他或待确认相关表（PrintScreenRecord，待确认）

源表：`dye.PrintScreenRecord`；新表：`src_dye_printscreenrecord`；原主键：BookNo。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| BookNo | old_book_no | BookNo | bigint | 否 | BigIntegerField |
| ScreenNo | old_screen_no | ScreenNo | varchar；字节长度 20 | 是 | CharField |
| DesignNo | old_design_no | DesignNo | varchar；字节长度 50 | 是 | CharField |
| DesignDetailNo | old_design_detail_no | DesignDetailNo | varchar；字节长度 20 | 是 | CharField |
| BookKind | old_book_kind | BookKind | tinyint | 是 | IntegerField |
| CurrDate | old_curr_date | CurrDate | datetime | 是 | DateTimeField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 10 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| StorageUnitID | old_storage_unit_id | StorageUnitID | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |

### SourceDyeReportItem — 其他或待确认相关表（ReportItem，待确认）

源表：`dye.ReportItem`；新表：`src_dye_reportitem`；原主键：RIID。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| RIID | old_riid | RIID | int | 否 | IntegerField |
| RIIndex | old_riindex | RIIndex | int | 是 | IntegerField |
| ShowIt | old_show_it | ShowIt | smallint | 是 | IntegerField |
| RIName | old_riname | RIName | varchar；字节长度 12 | 是 | CharField |
| UnitName | old_unit_name | UnitName | varchar；字节长度 6 | 是 | CharField |
| Formula | old_formula | Formula | image | 否 | BinaryField |
| CalcBySchClass | old_calc_by_sch_class | CalcBySchClass | smallint | 是 | IntegerField |
| StatisticMethod | old_statistic_method | StatisticMethod | smallint | 是 | IntegerField |
| CalcLast | old_calc_last | CalcLast | smallint | 是 | IntegerField |
| Notes | old_notes | Notes | image | 是 | BinaryField |

### SourceDyeRequestLimit — 其他或待确认相关表（RequestLimit，待确认）

源表：`dye.RequestLimit`；新表：`src_dye_requestlimit`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 30 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 30 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 30 | 是 | CharField |
| ApplicantID | old_applicant_id | ApplicantID | varchar；字节长度 30 | 是 | CharField |
| DesigneeID | old_designee_id | DesigneeID | varchar；字节长度 30 | 是 | CharField |
| DeliveryDay | old_delivery_day | DeliveryDay | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 200 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 30 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 30 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| Approver | old_approver | Approver | varchar；字节长度 30 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| OverdueAmount | old_overdue_amount | OverdueAmount | decimal(12,2) | 是 | DecimalField |

### SourceDyeSAutoID — 旧业务编号计数

源表：`dye.s_AutoID`；新表：`src_dye_s_autoid`；原主键：无主键。

归属依据：按原字段核实的公司资料、业务编号、审批或字段变更历史；不因平台前缀而仅留证据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| IDObject | old_idobject | IDObject | nvarchar；字节长度 100 | 否 | CharField |
| IDCounter | old_idcounter | IDCounter | bigint | 是 | BigIntegerField |
| IDValue | old_idvalue | IDValue | nvarchar；字节长度 100 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |

### SourceDyeSCorpTitle — 公司抬头资料

源表：`dye.s_CorpTitle`；新表：`src_dye_s_corptitle`；原主键：Code。

归属依据：按原字段核实的公司资料、业务编号、审批或字段变更历史；不因平台前缀而仅留证据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| Code | old_code | 代码 | varchar；字节长度 20 | 否 | CharField |
| Title | old_title | 标题 | varchar；字节长度 200 | 是 | CharField |
| SpecData | old_spec_data | 二进制存储的内容 | image | 是 | BinaryField |
| StopDate | old_stop_date | 停用时间 | datetime | 是 | DateTimeField |

### SourceDyeSFlow — 旧审批流程配置

源表：`dye.s_Flow`；新表：`src_dye_s_flow`；原主键：FlowID。

归属依据：按原字段核实的公司资料、业务编号、审批或字段变更历史；不因平台前缀而仅留证据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FlowID | old_flow_id | 流程编号 | varchar；字节长度 10 | 否 | CharField |
| FlowName | old_flow_name | 流程名称 | varchar；字节长度 50 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| DataTableName | old_data_table_name | 数据集名 | varchar；字节长度 50 | 是 | CharField |
| FormName | old_form_name | 审核窗口名称 | varchar；字节长度 50 | 是 | CharField |
| Description | old_description | 描述 | varchar；字节长度 500 | 是 | CharField |
| FlowKindID | old_flow_kind_id | 流程类别 | varchar；字节长度 10 | 是 | CharField |
| SheetName | old_sheet_name | 单据名称 | varchar；字节长度 20 | 是 | CharField |
| IsCanUnSubmit | old_is_can_un_submit | 终审前能否撤消 | bit | 是 | BooleanField |
| IsToNotify | old_is_to_notify | 提交或撤消发通知 | bit | 是 | BooleanField |
| IsCanUpdate | old_is_can_update | 终审前能否修改 | bit | 是 | BooleanField |
| RptIDForEmail | old_rpt_idfor_email | 邮件审批模板 | varchar；字节长度 10 | 是 | CharField |
| SubmiterFieldName | old_submiter_field_name | 提交人字段名 | varchar；字节长度 20 | 是 | CharField |
| IsStop | old_is_stop | 停用 | bit | 是 | BooleanField |
| StopDate | old_stop_date | 停用时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| IsUnEndApprovedOnlyBySelf | old_is_un_end_approved_only_by_self | 只有本人才能反审核 | bit | 是 | BooleanField |
| FuncNo | old_func_no | 功能号 | varchar；字节长度 6 | 是 | CharField |
| PhyTableName | old_phy_table_name | PhyTableName | varchar；字节长度 50 | 是 | CharField |
| RptID | old_rpt_id | 报表ID | varchar；字节长度 50 | 是 | CharField |
| IsUseWeXin | old_is_use_we_xin | 发送微信消息 | bit | 是 | BooleanField |
| RelaFuncNo | old_rela_func_no | RelaFuncNo | varchar；字节长度 200 | 是 | CharField |
| IsDirectCancel | old_is_direct_cancel | IsDirectCancel | bit | 是 | BooleanField |
| IsCreatImage | old_is_creat_image | IsCreatImage | bit | 是 | BooleanField |
| SubmiterCancelOnly | old_submiter_cancel_only | SubmiterCancelOnly | bit | 是 | BooleanField |

### SourceDyeSFlowRecord — 旧审批事实记录

源表：`dye.s_FlowRecord`；新表：`src_dye_s_flowrecord`；原主键：FlowRecordNo。

归属依据：按原字段核实的公司资料、业务编号、审批或字段变更历史；不因平台前缀而仅留证据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FlowRecordNo | old_flow_record_no | FlowRecordNo | bigint | 否 | BigIntegerField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| FlowID | old_flow_id | FlowID | varchar；字节长度 10 | 是 | CharField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| ApproverID | old_approver_id | ApproverID | varchar；字节长度 10 | 是 | CharField |
| Approver | old_approver | Approver | varchar；字节长度 10 | 是 | CharField |
| Idea | old_idea | Idea | varchar；字节长度 -1 | 是 | TextField |
| Status | old_status | Status | varchar；字节长度 1 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |

### SourceDyeSFlowStep — 旧审批步骤配置

源表：`dye.s_FlowStep`；新表：`src_dye_s_flowstep`；原主键：FlowID, StepNo。

归属依据：按原字段核实的公司资料、业务编号、审批或字段变更历史；不因平台前缀而仅留证据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FlowID | old_flow_id | 流程编号 | varchar；字节长度 10 | 否 | CharField |
| StepNo | old_step_no | 节点号 | tinyint | 否 | IntegerField |
| StepName | old_step_name | 节点名称 | varchar；字节长度 50 | 是 | CharField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |
| TimeOverHours | old_time_over_hours | 超时时限 | smallint | 是 | IntegerField |
| IsDisagreeToBack | old_is_disagree_to_back | 不同意则退回 | bit | 是 | BooleanField |
| IsDisagreeToContinue | old_is_disagree_to_continue | 不同意继续流转 | bit | 是 | BooleanField |
| IsDisagreeToSubmiter | old_is_disagree_to_submiter | 不同意退到提交人 | bit | 是 | BooleanField |
| IsOverAutoNotify | old_is_over_auto_notify | 超时自动通知 | bit | 是 | BooleanField |
| IsOverAutoContinue | old_is_over_auto_continue | 超时自动流转 | bit | 是 | BooleanField |
| IsCanChangeSign | old_is_can_change_sign | 可转签 | bit | 是 | BooleanField |
| IsToNotifyNext | old_is_to_notify_next | 通知后面节点人 | bit | 是 | BooleanField |
| IsToNotifyPrev | old_is_to_notify_prev | 通知前面节点人 | bit | 是 | BooleanField |
| IsEnd | old_is_end | 终审节点 | bit | 是 | BooleanField |
| SignerCanModifyFieldNames | old_signer_can_modify_field_names | 签核人可修改字段 | varchar；字节长度 400 | 是 | CharField |
| OverNotifyInterval | old_over_notify_interval | 超时通知间隔 | smallint | 是 | IntegerField |
| TaskTitleFormat | old_task_title_format | 任务标题格式 | varchar；字节长度 100 | 是 | CharField |
| OverTitleFormat | old_over_title_format | 超时通知格式 | varchar；字节长度 100 | 是 | CharField |
| BackedTaskTitleFormat | old_backed_task_title_format | 退回通知格式 | varchar；字节长度 100 | 是 | CharField |
| ChangeTitleFormat | old_change_title_format | 转签通知格式 | varchar；字节长度 100 | 是 | CharField |
| AndOr | old_and_or | 与或签核 | varchar；字节长度 10 | 是 | CharField |
| NoSignProcedure | old_no_sign_procedure | 免审核存储过程名 | varchar；字节长度 100 | 是 | CharField |
| GetSignerProcedure | old_get_signer_procedure | 获得节点签核人过程名 | varchar；字节长度 100 | 是 | CharField |
| AfterSignProcedure | old_after_sign_procedure | AfterSignProcedure | varchar；字节长度 50 | 是 | CharField |
| GetNoticerProcedure | old_get_noticer_procedure | GetNoticerProcedure | varchar；字节长度 100 | 是 | CharField |
| IsAndJudge | old_is_and_judge | IsAndJudge | bit | 是 | BooleanField |

关联 `source_parent_1` → `erp_base.SourceDyeSFlow`；原码 `FlowID` → 父表原码 `FlowID`；依据：原界面主从 s_FlowStep → s_Flow；数据库声明 FK_s_FlowStep_s_Flow。

### SourceDyeSFlowStepEmp — 旧审批人员配置

源表：`dye.s_FlowStepEmp`；新表：`src_dye_s_flowstepemp`；原主键：FlowID, StepNo, EmpID。

归属依据：按原字段核实的公司资料、业务编号、审批或字段变更历史；不因平台前缀而仅留证据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FlowID | old_flow_id | 流程编号 | varchar；字节长度 10 | 否 | CharField |
| StepNo | old_step_no | 节点号 | tinyint | 否 | IntegerField |
| EmpID | old_emp_id | 员工编码 | varchar；字节长度 10 | 否 | CharField |
| IsMustSign | old_is_must_sign | 必签 | bit | 是 | BooleanField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |
| TaskKind | old_task_kind | 工作类别 | tinyint | 是 | IntegerField |
| IsEnable | old_is_enable | 是否启用 | bit | 是 | BooleanField |
| IsSendByEmail | old_is_send_by_email | 发Email | bit | 是 | BooleanField |
| IsSendByQQ | old_is_send_by_qq | 发QQ | bit | 是 | BooleanField |
| IsSendBySMS | old_is_send_by_sms | 发ＳＭＳ | bit | 是 | BooleanField |
| IsSendByWebservice | old_is_send_by_webservice | 发ＷＥＢ | bit | 是 | BooleanField |
| IsSendByWeXin | old_is_send_by_we_xin | 发微信 | bit | 是 | BooleanField |
| IsSendByDingDing | old_is_send_by_ding_ding | 发钉钉 | bit | 是 | BooleanField |
| IsSendByApp | old_is_send_by_app | IsSendByApp | bit | 是 | BooleanField |

关联 `source_parent_1` → `erp_base.SourceDyeSFlowStep`；原码 `FlowID, StepNo` → 父表原码 `FlowID, StepNo`；依据：原界面主从 s_FlowStepEmp → s_FlowStep；数据库声明 FK_s_FlowStepEmp_s_FlowStep。

关联 `source_parent_2` → `erp_base.SourceDyeSFlowStepEmp`；原码 `FlowID, StepNo, EmpID` → 父表原码 `FlowID, StepNo, EmpID`；依据：数据库声明 FK_s_FlowStepEmp_s_FlowStepEmp。

### SourceDyeSFlowTask — 旧审批待办及签署事实

源表：`dye.s_FlowTask`；新表：`src_dye_s_flowtask`；原主键：FlowTaskNo。

归属依据：按原字段核实的公司资料、业务编号、审批或字段变更历史；不因平台前缀而仅留证据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FlowTaskNo | old_flow_task_no | 任务号 | varchar；字节长度 38 | 否 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 10 | 是 | CharField |
| FlowID | old_flow_id | 流程编号 | varchar；字节长度 10 | 是 | CharField |
| StepNo | old_step_no | 节点编号 | tinyint | 是 | IntegerField |
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 是 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 36 | 是 | CharField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| TaskTitle | old_task_title | 任务标题 | varchar；字节长度 100 | 是 | CharField |
| SignedManner | old_signed_manner | 签核的方式 | tinyint | 是 | IntegerField |
| SignedDate | old_signed_date | 签核的日期 | datetime | 是 | DateTimeField |
| SignerID | old_signer_id | 签核人编码 | varchar；字节长度 10 | 是 | CharField |
| Signer | old_signer | 签核人名 | varchar；字节长度 10 | 是 | CharField |
| Idea | old_idea | 签核意见 | varchar；字节长度 -1 | 是 | TextField |
| Status | old_status | 任务状态 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| TaskKind | old_task_kind | 任务类别 | tinyint | 是 | IntegerField |
| TaskDate | old_task_date | 任务开始时间 | datetime | 是 | DateTimeField |
| Sender | old_sender | 发送人姓名 | varchar；字节长度 10 | 是 | CharField |
| SenderID | old_sender_id | 发送人编码 | varchar；字节长度 10 | 是 | CharField |
| FlowBeginTime | old_flow_begin_time | 流程开始时间 | datetime | 是 | DateTimeField |
| DataTableName | old_data_table_name | DataTableName | varchar；字节长度 50 | 是 | CharField |
| SubmiterID | old_submiter_id | SubmiterID | varchar；字节长度 10 | 是 | CharField |
| Submiter | old_submiter | Submiter | varchar；字节长度 10 | 是 | CharField |
| SendDate | old_send_date | SendDate | datetime | 是 | DateTimeField |
| SubmitDate | old_submit_date | SubmitDate | datetime | 是 | DateTimeField |
| PhotoAddress | old_photo_address | PhotoAddress | varchar；字节长度 512 | 是 | CharField |
| SQLUser | old_sqluser | SQLUser | varchar；字节长度 50 | 是 | CharField |
| IsAutoSign | old_is_auto_sign | IsAutoSign | bit | 是 | BooleanField |

### SourceDyeSRevision — 旧业务字段变更单

源表：`dye.s_Revision`；新表：`src_dye_s_revision`；原主键：ReviNo。

归属依据：按原字段核实的公司资料、业务编号、审批或字段变更历史；不因平台前缀而仅留证据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ReviNo | old_revi_no | ReviNo | int | 否 | IntegerField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 30 | 否 | CharField |
| ReviDate | old_revi_date | ReviDate | datetime | 是 | DateTimeField |
| RevierID | old_revier_id | RevierID | varchar；字节长度 20 | 是 | CharField |
| ReviDesc | old_revi_desc | ReviDesc | varchar；字节长度 80 | 是 | CharField |
| CheckerID | old_checker_id | CheckerID | varchar；字节长度 20 | 是 | CharField |
| CheckDate | old_check_date | CheckDate | datetime | 是 | DateTimeField |
| CheckDesc | old_check_desc | CheckDesc | varchar；字节长度 80 | 是 | CharField |
| FuncNo | old_func_no | FuncNo | varchar；字节长度 6 | 是 | CharField |
| IsChecked | old_is_checked | IsChecked | varchar；字节长度 1 | 是 | CharField |
| IsUpdated | old_is_updated | IsUpdated | varchar；字节长度 1 | 是 | CharField |
| Content | old_content | Content | image | 是 | BinaryField |
| RevierIP | old_revier_ip | RevierIP | varchar；字节长度 20 | 是 | CharField |
| ComputerName | old_computer_name | ComputerName | varchar；字节长度 50 | 是 | CharField |
| ReviMode | old_revi_mode | ReviMode | varchar；字节长度 8 | 是 | CharField |
| TableName | old_table_name | TableName | varchar；字节长度 50 | 是 | CharField |

### SourceDyeSRevisionDetail — 旧业务字段变更明细

源表：`dye.s_RevisionDetail`；新表：`src_dye_s_revisiondetail`；原主键：ReviNo, RowNo。

归属依据：按原字段核实的公司资料、业务编号、审批或字段变更历史；不因平台前缀而仅留证据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ReviNo | old_revi_no | ReviNo | int | 否 | IntegerField |
| RowNo | old_row_no | RowNo | decimal(3,0) | 否 | DecimalField |
| OriValue | old_ori_value | OriValue | varchar；字节长度 50 | 是 | CharField |
| CurrValue | old_curr_value | CurrValue | varchar；字节长度 50 | 是 | CharField |
| TableName | old_table_name | TableName | varchar；字节长度 20 | 是 | CharField |
| FieldName | old_field_name | FieldName | varchar；字节长度 20 | 是 | CharField |
| DisplayName | old_display_name | DisplayName | varchar；字节长度 20 | 是 | CharField |
| ReviMode | old_revi_mode | ReviMode | varchar；字节长度 8 | 是 | CharField |

### SourceDyeSSaveMessRule — 旧业务提交通知规则

源表：`dye.s_SaveMessRule`；新表：`src_dye_s_savemessrule`；原主键：FuncNo。

归属依据：按原字段核实的公司资料、业务编号、审批或字段变更历史；不因平台前缀而仅留证据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FuncNo | old_func_no | FuncNo | varchar；字节长度 6 | 否 | CharField |
| TimeWay | old_time_way | TimeWay | tinyint | 是 | IntegerField |
| ProcName | old_proc_name | ProcName | varchar；字节长度 20 | 是 | CharField |
| ProcParamFields | old_proc_param_fields | ProcParamFields | varchar；字节长度 50 | 是 | CharField |
| IsEnable | old_is_enable | IsEnable | bit | 是 | BooleanField |
| StopDate | old_stop_date | StopDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |

### SourceDyeSSaveMessRuleDetail — 旧业务提交通知规则明细

源表：`dye.s_SaveMessRuleDetail`；新表：`src_dye_s_savemessruledetail`；原主键：DetailNo。

归属依据：按原字段核实的公司资料、业务编号、审批或字段变更历史；不因平台前缀而仅留证据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FuncNo | old_func_no | FuncNo | varchar；字节长度 6 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 否 | CharField |
| DataTableName | old_data_table_name | DataTableName | varchar；字节长度 50 | 是 | CharField |
| SourceFilter | old_source_filter | SourceFilter | varchar；字节长度 -1 | 是 | TextField |
| ReceiverIDs | old_receiver_ids | ReceiverIDs | varchar；字节长度 50 | 是 | CharField |
| Subject | old_subject | Subject | varchar；字节长度 200 | 是 | CharField |
| Content | old_content | Content | text | 是 | TextField |
| ParamFields | old_param_fields | ParamFields | varchar；字节长度 50 | 是 | CharField |
| IsEnable | old_is_enable | IsEnable | bit | 是 | BooleanField |
| StopDate | old_stop_date | StopDate | datetime | 是 | DateTimeField |
| TimeWay | old_time_way | TimeWay | tinyint | 是 | IntegerField |

### SourceDyeSSheetNo — 旧单据编号规则

源表：`dye.s_SheetNo`；新表：`src_dye_s_sheetno`；原主键：无主键。

归属依据：按原字段核实的公司资料、业务编号、审批或字段变更历史；不因平台前缀而仅留证据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetTypeID | old_sheet_type_id | SheetTypeID | numeric(3,0) | 否 | DecimalField |
| PrevDate | old_prev_date | PrevDate | varchar；字节长度 8 | 否 | CharField |
| Prefix | old_prefix | Prefix | varchar；字节长度 2 | 否 | CharField |
| PrevNo | old_prev_no | PrevNo | numeric(9,0) | 是 | DecimalField |
| SheetName | old_sheet_name | SheetName | varchar；字节长度 20 | 是 | CharField |
| YearCode | old_year_code | YearCode | smallint | 是 | IntegerField |
| MonthCode | old_month_code | MonthCode | smallint | 是 | IntegerField |
| IsUseDayCode | old_is_use_day_code | IsUseDayCode | smallint | 是 | IntegerField |
| EndCode | old_end_code | EndCode | smallint | 是 | IntegerField |

### SourceDyeSchClass — 其他或待确认相关表（SchClass，待确认）

源表：`dye.SchClass`；新表：`src_dye_schclass`；原主键：schClassid。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| schClassid | old_sch_classid | schClassid | int | 否 | IntegerField |
| schName | old_sch_name | schName | varchar；字节长度 20 | 否 | CharField |
| StartTime | old_start_time | StartTime | datetime | 否 | DateTimeField |
| EndTime | old_end_time | EndTime | datetime | 否 | DateTimeField |
| LateMinutes | old_late_minutes | LateMinutes | int | 是 | IntegerField |
| EarlyMinutes | old_early_minutes | EarlyMinutes | int | 是 | IntegerField |
| CheckIn | old_check_in | CheckIn | int | 是 | IntegerField |
| CheckOut | old_check_out | CheckOut | int | 是 | IntegerField |
| CheckInTime1 | old_check_in_time1 | CheckInTime1 | datetime | 是 | DateTimeField |
| CheckInTime2 | old_check_in_time2 | CheckInTime2 | datetime | 是 | DateTimeField |
| CheckOutTime1 | old_check_out_time1 | CheckOutTime1 | datetime | 是 | DateTimeField |
| CheckOutTime2 | old_check_out_time2 | CheckOutTime2 | datetime | 是 | DateTimeField |
| Color | old_color | Color | int | 是 | IntegerField |
| AutoBind | old_auto_bind | AutoBind | smallint | 是 | IntegerField |
| WorkDay | old_work_day | WorkDay | float | 是 | FloatField |
| SensorID | old_sensor_id | SensorID | varchar；字节长度 5 | 是 | CharField |
| WorkMins | old_work_mins | WorkMins | float | 是 | FloatField |

### SourceDyeSHIFT — 生产工单与排程相关表（SHIFT，待确认）

源表：`dye.SHIFT`；新表：`src_dye_shift`；原主键：SHIFTID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SHIFTID | old_shiftid | SHIFTID | int | 否 | IntegerField |
| NAME | old_name | NAME | varchar；字节长度 20 | 是 | CharField |
| USHIFTID | old_ushiftid | USHIFTID | int | 是 | IntegerField |
| STARTDATE | old_startdate | STARTDATE | datetime | 否 | DateTimeField |
| ENDDATE | old_enddate | ENDDATE | datetime | 是 | DateTimeField |
| RUNNUM | old_runnum | RUNNUM | smallint | 是 | IntegerField |
| SCH1 | old_sch1 | SCH1 | int | 是 | IntegerField |
| SCH2 | old_sch2 | SCH2 | int | 是 | IntegerField |
| SCH3 | old_sch3 | SCH3 | int | 是 | IntegerField |
| SCH4 | old_sch4 | SCH4 | int | 是 | IntegerField |
| SCH5 | old_sch5 | SCH5 | int | 是 | IntegerField |
| SCH6 | old_sch6 | SCH6 | int | 是 | IntegerField |
| SCH7 | old_sch7 | SCH7 | int | 是 | IntegerField |
| SCH8 | old_sch8 | SCH8 | int | 是 | IntegerField |
| SCH9 | old_sch9 | SCH9 | int | 是 | IntegerField |
| SCH10 | old_sch10 | SCH10 | int | 是 | IntegerField |
| SCH11 | old_sch11 | SCH11 | int | 是 | IntegerField |
| SCH12 | old_sch12 | SCH12 | int | 是 | IntegerField |
| CYCLE | old_cycle | CYCLE | smallint | 是 | IntegerField |
| UNITS | old_units | UNITS | smallint | 是 | IntegerField |

### SourceDyeSHOUPITONGZHIDAN — 其他或待确认相关表（SHOUPITONGZHIDAN，待确认）

源表：`dye.SHOUPITONGZHIDAN`；新表：`src_dye_shoupitongzhidan`；原主键：ID。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | 单号 | varchar；字节长度 20 | 否 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| DIZHI | old_dizhi | 地址 | varchar；字节长度 200 | 是 | CharField |
| LXR | old_lxr | 联系人 | varchar；字节长度 50 | 是 | CharField |
| DHHM | old_dhhm | 电话号码 | varchar；字节长度 500 | 是 | CharField |
| RQ | old_rq | 日期 | datetime | 是 | DateTimeField |
| PISHU | old_pishu | 粒数 | decimal(9,1) | 是 | DecimalField |
| BZ | old_bz | 备注 | varchar；字节长度 500 | 是 | CharField |
| JIANCHEN | old_jianchen | 客户简称 | varchar；字节长度 50 | 是 | CharField |

### SourceDyeStaffEstablishing — 其他或待确认相关表（StaffEstablishing，待确认）

源表：`dye.StaffEstablishing`；新表：`src_dye_staffestablishing`；原主键：id。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| id | old_id | id | nchar；字节长度 20 | 否 | CharField |
| DeptID | old_dept_id | DeptID | nchar；字节长度 40 | 是 | CharField |
| Empkind | old_empkind | Empkind | nchar；字节长度 40 | 是 | CharField |
| OrgNum | old_org_num | OrgNum | int | 是 | IntegerField |

### SourceDyeSwipeEmpEdit — 基础主数据相关表（SwipeEmpEdit，待确认）

源表：`dye.SwipeEmpEdit`；新表：`src_dye_swipeempedit`；原主键：SheetSeries。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 制单单号 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 品名 | varchar；字节长度 50 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1000 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |

### SourceDyeSwipeEmpEditDetail — 基础主数据相关表（SwipeEmpEditDetail，待确认）

源表：`dye.SwipeEmpEditDetail`；新表：`src_dye_swipeempeditdetail`；原主键：DetailNo。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| Sheetseries | old_sheetseries | 表单号 | varchar；字节长度 50 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 30 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 30 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 30 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 30 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 30 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| OrderQty | old_order_qty | 订单数量 | decimal(10,2) | 是 | DecimalField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| Area | old_area | 区域 | varchar；字节长度 100 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 100 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 500 | 是 | CharField |
| SumAssignedRolls | old_sum_assigned_rolls | 生产个数 | decimal(7,2) | 是 | DecimalField |
| SumAssignedWeightQty | old_sum_assigned_weight_qty | 生产重量 | decimal(10,2) | 是 | DecimalField |
| ColorRemarks | old_color_remarks | 用途 | varchar；字节长度 500 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 50 | 是 | CharField |
| LabelWareHouse | old_label_ware_house | 标签仓库 | varchar；字节长度 100 | 是 | CharField |
| LabelRemarks | old_label_remarks | 标签用途 | varchar；字节长度 500 | 是 | CharField |
| WindingID | old_winding_id | 登记员工 | varchar；字节长度 30 | 是 | CharField |
| TubeWeight | old_tube_weight | 纸筒 | decimal(7,3) | 是 | DecimalField |
| PackBag | old_pack_bag | 包装 | decimal(7,3) | 是 | DecimalField |
| MachineID | old_machine_id | 机台 | varchar；字节长度 100 | 是 | CharField |
| GY | old_gy | 工艺 | varchar；字节长度 200 | 是 | CharField |
| CustFabricName | old_cust_fabric_name | 客户规格 | varchar；字节长度 200 | 是 | CharField |
| LTSheetNo | old_ltsheet_no | 排产号 | varchar；字节长度 30 | 是 | CharField |
| FenTou | old_fen_tou | 分头 | varchar；字节长度 50 | 是 | CharField |

### SourceDyeTBKEY — 其他或待确认相关表（TBKEY，待确认）

源表：`dye.TBKEY`；新表：`src_dye_tbkey`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| PreName | old_pre_name | PreName | varchar；字节长度 12 | 是 | CharField |
| ONEKEY | old_onekey | ONEKEY | int | 是 | IntegerField |

### SourceDyeTBSMSALLOT — 其他或待确认相关表（TBSMSALLOT，待确认）

源表：`dye.TBSMSALLOT`；新表：`src_dye_tbsmsallot`；原主键：REFERENCE。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| REFERENCE | old_reference | REFERENCE | int | 否 | IntegerField |
| SMSREF | old_smsref | SMSREF | int | 否 | IntegerField |
| USERREF | old_userref | USERREF | int | 否 | IntegerField |
| GENTM | old_gentm | GENTM | varchar；字节长度 20 | 是 | CharField |

### SourceDyeTBSMSINFO — 其他或待确认相关表（TBSMSINFO，待确认）

源表：`dye.TBSMSINFO`；新表：`src_dye_tbsmsinfo`；原主键：REFERENCE。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| REFERENCE | old_reference | REFERENCE | int | 否 | IntegerField |
| SMSID | old_smsid | SMSID | varchar；字节长度 16 | 否 | CharField |
| SMSINDEX | old_smsindex | SMSINDEX | int | 否 | IntegerField |
| SMSTYPE | old_smstype | SMSTYPE | int | 是 | IntegerField |
| SMSCONTENT | old_smscontent | SMSCONTENT | text | 是 | TextField |
| SMSSTARTTM | old_smsstarttm | SMSSTARTTM | varchar；字节长度 32 | 是 | CharField |
| SMSTMLENG | old_smstmleng | SMSTMLENG | int | 是 | IntegerField |
| GENTM | old_gentm | GENTM | varchar；字节长度 20 | 是 | CharField |

### SourceDyeTEMPLATE — 基础主数据相关表（TEMPLATE，待确认）

源表：`dye.TEMPLATE`；新表：`src_dye_template`；原主键：TEMPLATEID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| TEMPLATEID | old_templateid | TEMPLATEID | int | 否 | IntegerField |
| USERID | old_userid | USERID | int | 否 | IntegerField |
| FINGERID | old_fingerid | FINGERID | int | 否 | IntegerField |
| TEMPLATE | old_template | TEMPLATE | image | 否 | BinaryField |
| TEMPLATE2 | old_template2 | TEMPLATE2 | image | 是 | BinaryField |
| TEMPLATE3 | old_template3 | TEMPLATE3 | image | 是 | BinaryField |
| BITMAPPICTURE | old_bitmappicture | BITMAPPICTURE | image | 是 | BinaryField |
| BITMAPPICTURE2 | old_bitmappicture2 | BITMAPPICTURE2 | image | 是 | BinaryField |
| BITMAPPICTURE3 | old_bitmappicture3 | BITMAPPICTURE3 | image | 是 | BinaryField |
| BITMAPPICTURE4 | old_bitmappicture4 | BITMAPPICTURE4 | image | 是 | BinaryField |
| USETYPE | old_usetype | USETYPE | smallint | 是 | IntegerField |
| EMACHINENUM | old_emachinenum | EMACHINENUM | varchar；字节长度 3 | 是 | CharField |
| TEMPLATE1 | old_template1 | TEMPLATE1 | image | 是 | BinaryField |
| Flag | old_flag | Flag | smallint | 是 | IntegerField |
| DivisionFP | old_division_fp | DivisionFP | smallint | 是 | IntegerField |
| TEMPLATE4 | old_template4 | TEMPLATE4 | image | 是 | BinaryField |

### SourceDyeUSEROFRUN — 其他或待确认相关表（USER_OF_RUN，待确认）

源表：`dye.USER_OF_RUN`；新表：`src_dye_user_of_run`；原主键：USERID, NUM_OF_RUN_ID, STARTDATE, ENDDATE。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| USERID | old_userid | USERID | int | 否 | IntegerField |
| NUM_OF_RUN_ID | old_num_of_run_id | NUM_OF_RUN_ID | int | 否 | IntegerField |
| STARTDATE | old_startdate | STARTDATE | datetime | 否 | DateTimeField |
| ENDDATE | old_enddate | ENDDATE | datetime | 否 | DateTimeField |
| ISNOTOF_RUN | old_isnotof_run | ISNOTOF_RUN | int | 是 | IntegerField |
| ORDER_RUN | old_order_run | ORDER_RUN | int | 是 | IntegerField |

### SourceDyeUSERSPEDAY — 其他或待确认相关表（USER_SPEDAY，待确认）

源表：`dye.USER_SPEDAY`；新表：`src_dye_user_speday`；原主键：USERID, STARTSPECDAY, DATEID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| USERID | old_userid | USERID | int | 否 | IntegerField |
| STARTSPECDAY | old_startspecday | STARTSPECDAY | datetime | 否 | DateTimeField |
| ENDSPECDAY | old_endspecday | ENDSPECDAY | datetime | 是 | DateTimeField |
| DATEID | old_dateid | DATEID | smallint | 否 | IntegerField |
| YUANYING | old_yuanying | YUANYING | varchar；字节长度 200 | 是 | CharField |
| DATE | old_date | DATE | datetime | 是 | DateTimeField |

### SourceDyeUSERTEMPSCH — 基础主数据相关表（USER_TEMP_SCH，待确认）

源表：`dye.USER_TEMP_SCH`；新表：`src_dye_user_temp_sch`；原主键：USERID, COMETIME, LEAVETIME。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| USERID | old_userid | USERID | int | 否 | IntegerField |
| COMETIME | old_cometime | COMETIME | datetime | 否 | DateTimeField |
| LEAVETIME | old_leavetime | LEAVETIME | datetime | 否 | DateTimeField |
| OVERTIME | old_overtime | OVERTIME | int | 否 | IntegerField |
| TYPE | old_type | TYPE | smallint | 是 | IntegerField |
| FLAG | old_flag | FLAG | smallint | 是 | IntegerField |
| SCHCLASSID | old_schclassid | SCHCLASSID | int | 是 | IntegerField |

### SourceDyeUSERINFO — 其他或待确认相关表（USERINFO，待确认）

源表：`dye.USERINFO`；新表：`src_dye_userinfo`；原主键：USERID。

归属依据：基础/人员/设备/共用配置来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| USERID | old_userid | USERID | int | 否 | IntegerField |
| BADGENUMBER | old_badgenumber | BADGENUMBER | varchar；字节长度 24 | 否 | CharField |
| SSN | old_ssn | SSN | varchar；字节长度 20 | 是 | CharField |
| NAME | old_name | NAME | varchar；字节长度 40 | 是 | CharField |
| GENDER | old_gender | GENDER | varchar；字节长度 8 | 是 | CharField |
| TITLE | old_title | TITLE | varchar；字节长度 20 | 是 | CharField |
| PAGER | old_pager | PAGER | varchar；字节长度 20 | 是 | CharField |
| BIRTHDAY | old_birthday | BIRTHDAY | datetime | 是 | DateTimeField |
| HIREDDAY | old_hiredday | HIREDDAY | datetime | 是 | DateTimeField |
| STREET | old_street | STREET | varchar；字节长度 80 | 是 | CharField |
| CITY | old_city | CITY | varchar；字节长度 2 | 是 | CharField |
| STATE | old_state | STATE | varchar；字节长度 2 | 是 | CharField |
| ZIP | old_zip | ZIP | varchar；字节长度 12 | 是 | CharField |
| OPHONE | old_ophone | OPHONE | varchar；字节长度 20 | 是 | CharField |
| FPHONE | old_fphone | FPHONE | varchar；字节长度 20 | 是 | CharField |
| VERIFICATIONMETHOD | old_verificationmethod | VERIFICATIONMETHOD | smallint | 是 | IntegerField |
| DEFAULTDEPTID | old_defaultdeptid | DEFAULTDEPTID | smallint | 是 | IntegerField |
| SECURITYFLAGS | old_securityflags | SECURITYFLAGS | smallint | 是 | IntegerField |
| ATT | old_att | ATT | smallint | 否 | IntegerField |
| INLATE | old_inlate | INLATE | smallint | 否 | IntegerField |
| OUTEARLY | old_outearly | OUTEARLY | smallint | 否 | IntegerField |
| OVERTIME | old_overtime | OVERTIME | smallint | 否 | IntegerField |
| SEP | old_sep | SEP | smallint | 否 | IntegerField |
| HOLIDAY | old_holiday | HOLIDAY | smallint | 否 | IntegerField |
| MINZU | old_minzu | MINZU | varchar；字节长度 8 | 是 | CharField |
| PASSWORD | old_password | PASSWORD | varchar；字节长度 50 | 是 | CharField |
| LUNCHDURATION | old_lunchduration | LUNCHDURATION | smallint | 否 | IntegerField |
| MVerifyPass | old_mverify_pass | MVerifyPass | varchar；字节长度 10 | 是 | CharField |
| PHOTO | old_photo | PHOTO | image | 是 | BinaryField |
| Notes | old_notes | Notes | image | 是 | BinaryField |
| privilege | old_privilege | privilege | int | 是 | IntegerField |
| InheritDeptSch | old_inherit_dept_sch | InheritDeptSch | smallint | 是 | IntegerField |
| InheritDeptSchClass | old_inherit_dept_sch_class | InheritDeptSchClass | smallint | 是 | IntegerField |
| AutoSchPlan | old_auto_sch_plan | AutoSchPlan | smallint | 是 | IntegerField |
| MinAutoSchInterval | old_min_auto_sch_interval | MinAutoSchInterval | int | 是 | IntegerField |
| RegisterOT | old_register_ot | RegisterOT | smallint | 是 | IntegerField |
| InheritDeptRule | old_inherit_dept_rule | InheritDeptRule | smallint | 是 | IntegerField |
| EMPRIVILEGE | old_emprivilege | EMPRIVILEGE | smallint | 是 | IntegerField |
| CardNo | old_card_no | CardNo | varchar；字节长度 20 | 是 | CharField |
| FaceGroup | old_face_group | FaceGroup | int | 是 | IntegerField |
| AccGroup | old_acc_group | AccGroup | int | 是 | IntegerField |
| UseAccGroupTZ | old_use_acc_group_tz | UseAccGroupTZ | int | 是 | IntegerField |
| VerifyCode | old_verify_code | VerifyCode | int | 是 | IntegerField |
| Expires | old_expires | Expires | int | 是 | IntegerField |
| ValidCount | old_valid_count | ValidCount | int | 是 | IntegerField |
| ValidTimeBegin | old_valid_time_begin | ValidTimeBegin | datetime | 是 | DateTimeField |
| ValidTimeEnd | old_valid_time_end | ValidTimeEnd | datetime | 是 | DateTimeField |
| TimeZone1 | old_time_zone1 | TimeZone1 | int | 是 | IntegerField |
| TimeZone2 | old_time_zone2 | TimeZone2 | int | 是 | IntegerField |
| TimeZone3 | old_time_zone3 | TimeZone3 | int | 是 | IntegerField |
| IDCardNo | old_idcard_no | IDCardNo | varchar；字节长度 50 | 是 | CharField |
| IDCardValidTime | old_idcard_valid_time | IDCardValidTime | varchar；字节长度 32 | 是 | CharField |
| EMail | old_email | EMail | varchar；字节长度 100 | 是 | CharField |
| IDCardName | old_idcard_name | IDCardName | varchar；字节长度 30 | 是 | CharField |
| IDCardBirth | old_idcard_birth | IDCardBirth | varchar；字节长度 16 | 是 | CharField |
| IDCardSN | old_idcard_sn | IDCardSN | varchar；字节长度 24 | 是 | CharField |
| IDCardDN | old_idcard_dn | IDCardDN | varchar；字节长度 24 | 是 | CharField |
| IDCardAddr | old_idcard_addr | IDCardAddr | varchar；字节长度 70 | 是 | CharField |
| IDCardNewAddr | old_idcard_new_addr | IDCardNewAddr | varchar；字节长度 255 | 是 | CharField |
| IDCardISSUER | old_idcard_issuer | IDCardISSUER | varchar；字节长度 32 | 是 | CharField |
| IDCardGender | old_idcard_gender | IDCardGender | int | 是 | IntegerField |
| IDCardNation | old_idcard_nation | IDCardNation | int | 是 | IntegerField |
| IDCardReserve | old_idcard_reserve | IDCardReserve | varchar；字节长度 36 | 是 | CharField |
| IDCardNotice | old_idcard_notice | IDCardNotice | varchar；字节长度 255 | 是 | CharField |
| IDCard_MainCard | old_idcard_main_card | IDCard_MainCard | varchar；字节长度 24 | 是 | CharField |
| IDCard_ViceCard | old_idcard_vice_card | IDCard_ViceCard | varchar；字节长度 24 | 是 | CharField |
| FSelected | old_fselected | FSelected | bit | 是 | BooleanField |
| Pin1 | old_pin1 | Pin1 | int | 是 | IntegerField |

### SourceDyeUserUsedSClasses — 其他或待确认相关表（UserUsedSClasses，待确认）

源表：`dye.UserUsedSClasses`；新表：`src_dye_userusedsclasses`；原主键：UserId, SchId。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| UserId | old_user_id | UserId | int | 否 | IntegerField |
| SchId | old_sch_id | SchId | int | 否 | IntegerField |

### SourceDyeYunfeibiaozhun — 其他或待确认相关表（yunfeibiaozhun，待确认）

源表：`dye.yunfeibiaozhun`；新表：`src_dye_yunfeibiaozhun`；原主键：无主键。

归属依据：用途未完全解释，先在基础信息原形承接；不丢字段/数据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| CODE | old_code | CODE | varchar；字节长度 5 | 是 | CharField |
| Address | old_address | Address | varchar；字节长度 50 | 是 | CharField |
| LeiXing | old_lei_xing | LeiXing | varchar；字节长度 5 | 是 | CharField |
| outPrice | old_out_price | outPrice | decimal(18,2) | 是 | DecimalField |
| inprice | old_inprice | inprice | decimal(18,2) | 是 | DecimalField |

### SourceDyeZRevisionDetail — 旧业务字段修改值

源表：`dye.z_RevisionDetail`；新表：`src_dye_z_revisiondetail`；原主键：RecordID, ID。

归属依据：按原字段核实的公司资料、业务编号、审批或字段变更历史；不因平台前缀而仅留证据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| RecordID | old_record_id | RecordID | nvarchar；字节长度 76 | 否 | CharField |
| ID | old_id | ID | varchar；字节长度 50 | 否 | CharField |
| FieldName | old_field_name | FieldName | varchar；字节长度 50 | 是 | CharField |
| OriValue | old_ori_value | OriValue | nvarchar；字节长度 -1 | 是 | TextField |
| CurrValue | old_curr_value | CurrValue | nvarchar；字节长度 -1 | 是 | TextField |

关联 `source_parent_1` → `erp_base.SourceDyeZRevisionKey`；原码 `ID` → 父表原码 `ID`；依据：数据库声明 FK_z_RevisionDetail_z_RevisionKey；原界面主从 z_RevisionDetail → z_RevisionKey。

### SourceDyeZRevisionKey — 旧业务字段修改来源键

源表：`dye.z_RevisionKey`；新表：`src_dye_z_revisionkey`；原主键：ID。

归属依据：按原字段核实的公司资料、业务编号、审批或字段变更历史；不因平台前缀而仅留证据。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | varchar；字节长度 50 | 否 | CharField |
| DataTableName | old_data_table_name | DataTableName | varchar；字节长度 50 | 是 | CharField |
| KeyField | old_key_field | KeyField | nvarchar；字节长度 1024 | 是 | CharField |
| KeyValue | old_key_value | KeyValue | nvarchar；字节长度 1024 | 是 | CharField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 否 | DateTimeField |
| IPAddress | old_ipaddress | IPAddress | varchar；字节长度 50 | 是 | CharField |
| ComputerName | old_computer_name | ComputerName | varchar；字节长度 50 | 是 | CharField |

## 销售管理

新增原表模型 39 个，原字段 892 个。

### SourceDyeCusAddPrice — 财务结算与成本相关表（CusAddPrice，待确认）

源表：`dye.CusAddPrice`；新表：`src_dye_cusaddprice`；原主键：SheetSeries。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 30 | 否 | CharField |
| SheetNo | old_sheet_no | 表单号 | varchar；字节长度 30 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyeCusAddPriceDetail — 财务结算与成本相关表（CusAddPriceDetail，待确认）

源表：`dye.CusAddPriceDetail`；新表：`src_dye_cusaddpricedetail`；原主键：DetailNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单号 | varchar；字节长度 30 | 是 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 30 | 否 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 30 | 是 | CharField |
| Remarks1 | old_remarks1 | 备注1 | varchar；字节长度 512 | 是 | CharField |
| Remarks2 | old_remarks2 | 备注2 | varchar；字节长度 512 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 30 | 是 | CharField |
| MinTwist | old_min_twist | 捻度> | decimal(10,2) | 是 | DecimalField |
| MaxTwist | old_max_twist | 捻度<= | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(10,2) | 是 | DecimalField |
| PriceUnit | old_price_unit | 报价单位 | int | 是 | IntegerField |

关联 `source_parent_1` → `erp_sales.SourceDyeCusAddPrice`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 CusAddPriceDetail → CusAddPrice。

### SourceDyeCusBasicsPrice — 财务结算与成本相关表（CusBasicsPrice，待确认）

源表：`dye.CusBasicsPrice`；新表：`src_dye_cusbasicsprice`；原主键：SheetSeries。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 单据时间 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 30 | 是 | CharField |
| CurrencyID | old_currency_id | 币别 | varchar；字节长度 50 | 是 | CharField |
| IsTax | old_is_tax | 是否含税 | bit | 是 | BooleanField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| TaxRate | old_tax_rate | 税率 | decimal(10,2) | 是 | DecimalField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| ApproverDate | old_approver_date | 审核时间 | datetime | 是 | DateTimeField |

### SourceDyeCusBasicsPriceDetail — 财务结算与成本相关表（CusBasicsPriceDetail，待确认）

源表：`dye.CusBasicsPriceDetail`；新表：`src_dye_cusbasicspricedetail`；原主键：DetailNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |
| GradeID | old_grade_id | 色号等级 | varchar；字节长度 30 | 是 | CharField |
| FabricKindID | old_fabric_kind_id | 纱种类别 | varchar；字节长度 30 | 是 | CharField |
| ColorLevel | old_color_level | 色级 | varchar；字节长度 30 | 是 | CharField |
| TaxPrice | old_tax_price | 含税单价 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 不含税单价 | decimal(10,2) | 是 | DecimalField |
| StuffRatio1 | old_stuff_ratio1 | 染料溶度> | decimal(10,2) | 是 | DecimalField |
| StuffRatio2 | old_stuff_ratio2 | 染料溶度<= | decimal(10,2) | 是 | DecimalField |
| FormulaCost1 | old_formula_cost1 | 配方成本> | decimal(10,2) | 是 | DecimalField |
| FormulaCost2 | old_formula_cost2 | 配方成本<= | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Weight1 | old_weight1 | 克重> | decimal(10,2) | 是 | DecimalField |
| Weight2 | old_weight2 | 克重<= | decimal(10,2) | 是 | DecimalField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| RSKind | old_rskind | 染色分类 | varchar；字节长度 50 | 是 | CharField |
| KindName | old_kind_name | 机台分类 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_sales.SourceDyeCusBasicsPrice`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 CusBasicsPriceDetail → CusBasicsPrice。

### SourceDyeCusExtraCharge — 其他或待确认相关表（CusExtraCharge，待确认）

源表：`dye.CusExtraCharge`；新表：`src_dye_cusextracharge`；原主键：DetailNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |
| Price | old_price | 单价 | decimal(10,2) | 是 | DecimalField |
| PriceUnit | old_price_unit | 单价单位 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| PayService | old_pay_service | 收费项目 | nvarchar；字节长度 80 | 是 | CharField |
| TaxPrice | old_tax_price | 含税单价 | float | 是 | FloatField |
| GradeID | old_grade_id | 色号等级 | varchar；字节长度 10 | 是 | CharField |

关联 `source_parent_1` → `erp_sales.SourceDyeCusBasicsPrice`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 CusExtraCharge → CusBasicsPrice。

### SourceDyeCustomerNoLimit — 客户订单与销售相关表（CustomerNoLimit，待确认）

源表：`dye.CustomerNoLimit`；新表：`src_dye_customernolimit`；原主键：SheetSeries。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 30 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 30 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 30 | 是 | CharField |
| Kind | old_kind | Kind | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 200 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 30 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 30 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| Approver | old_approver | Approver | varchar；字节长度 30 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| NoLimitAmount | old_no_limit_amount | NoLimitAmount | decimal(10,2) | 是 | DecimalField |

### SourceDyeCustomerTS — 客户订单与销售相关表（CustomerTS，待确认）

源表：`dye.CustomerTS`；新表：`src_dye_customerts`；原主键：SheetSeries。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 表单号 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 品名 | varchar；字节长度 50 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1000 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |

### SourceDyeCustomerTSDetail — 客户订单与销售相关表（CustomerTSDetail，待确认）

源表：`dye.CustomerTSDetail`；新表：`src_dye_customertsdetail`；原主键：DetailNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| Sheetseries | old_sheetseries | 表单号 | varchar；字节长度 50 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 30 | 是 | CharField |
| BarCode | old_bar_code | 条码 | varchar；字节长度 30 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 30 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 30 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 30 | 是 | CharField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| Result | old_result | 处理意见 | nvarchar；字节长度 1052 | 是 | CharField |
| Remarks | old_remarks | 投诉问题 | nvarchar；字节长度 1052 | 是 | CharField |
| SheetDate | old_sheet_date | 日期 | datetime | 是 | DateTimeField |

### SourceDyeFixedPrice — 财务结算与成本相关表（FixedPrice，待确认）

源表：`dye.FixedPrice`；新表：`src_dye_fixedprice`；原主键：SheetSeries。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 否 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| QuoteKindID | old_quote_kind_id | 报价类别 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员代码 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| Linker | old_linker | 联系人 | varchar；字节长度 10 | 是 | CharField |
| CurrencyID | old_currency_id | 币别 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 -1 | 是 | TextField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| SettleID | old_settle_id | 结算方式 | varchar；字节长度 10 | 是 | CharField |
| ExchangeRate | old_exchange_rate | 汇率 | decimal(10,2) | 是 | DecimalField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| IsConfirmed | old_is_confirmed | 确价 | smallint | 是 | IntegerField |
| BeiZhu | old_bei_zhu | BeiZhu | varchar；字节长度 150 | 是 | CharField |
| IsTax | old_is_tax | 单价类别 | varchar；字节长度 10 | 是 | CharField |
| TaxRate | old_tax_rate | 税率% | decimal(10,2) | 是 | DecimalField |
| Tel | old_tel | Tel | varchar；字节长度 100 | 是 | CharField |
| CustomerCode | old_customer_code | 客户全称 | varchar；字节长度 50 | 是 | CharField |
| LastTime | old_last_time | LastTime | datetime | 是 | DateTimeField |

### SourceDyeFixedPriceAtte — 财务结算与成本相关表（FixedPriceAtte，待确认）

源表：`dye.FixedPriceAtte`；新表：`src_dye_fixedpriceatte`；原主键：SheetSeries, FieldType, AtteCode, DetailNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| FieldType | old_field_type | 基础数据类别 | varchar；字节长度 20 | 否 | CharField |
| AtteCode | old_atte_code | 事项代码 | varchar；字节长度 10 | 否 | CharField |
| AtteValue | old_atte_value | 事项内容 | varchar；字节长度 500 | 是 | CharField |
| PriceUnit | old_price_unit | 计价单位 | tinyint | 是 | IntegerField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| Description | old_description | 描述 | varchar；字节长度 500 | 是 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 30 | 否 | CharField |

关联 `source_parent_1` → `erp_sales.SourceDyeFixedPriceDetail`；原码 `DetailNo` → 父表原码 `DetailNo`；依据：原界面主从 c → QuoteDetail；原界面主从 QuoteAtte → QuoteDetail。

关联 `source_parent_2` → `erp_sales.SourceDyeQuoteItemPrice`；原码 `DetailNo` → 父表原码 `DetailNo`；依据：原界面主从 QuotePriceAtte → QuoteItemPrice。

### SourceDyeFixedPriceDetail — 财务结算与成本相关表（FixedPriceDetail，待确认）

源表：`dye.FixedPriceDetail`；新表：`src_dye_fixedpricedetail`；原主键：DetailNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 表单明细号（子表） | varchar；字节长度 36 | 否 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| Structure | old_structure | 组织 | varchar；字节长度 50 | 是 | CharField |
| Width | old_width | 幅宽 | decimal(6,2) | 否 | DecimalField |
| Weight | old_weight | 克重 | decimal(6,2) | 否 | DecimalField |
| Price | old_price | 客确价格 | decimal(8,2) | 是 | DecimalField |
| PriceUnit | old_price_unit | 单位 | tinyint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Loss | old_loss | 数值缩率 | decimal(4,1) | 是 | DecimalField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 50 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| MainStuffKindID | old_main_stuff_kind_id | 主染料类别 | varchar；字节长度 10 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 10 | 是 | CharField |
| RecipePrice | old_recipe_price | 配方成本 | decimal(8,2) | 是 | DecimalField |
| ProcessMemo | old_process_memo | 套价项目 | varchar；字节长度 300 | 是 | CharField |
| ProcessPrice | old_process_price | 另计价 | decimal(8,2) | 是 | DecimalField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 100 | 是 | CharField |
| Pricesum | old_pricesum | 总单价 | decimal(8,2) | 是 | DecimalField |
| CusPrice | old_cus_price | 对客报价 | decimal(8,2) | 是 | DecimalField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 20 | 是 | CharField |
| AdjustPrice | old_adjust_price | AdjustPrice | decimal(12,2) | 是 | DecimalField |
| StartDate | old_start_date | StartDate | datetime | 是 | DateTimeField |
| DateType | old_date_type | DateType | tinyint | 是 | IntegerField |
| IsConfirmed | old_is_confirmed | 是否确价 | smallint | 是 | IntegerField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 32 | 是 | CharField |
| ColorNumNO | old_color_num_no | 确版号 | varchar；字节长度 10 | 是 | CharField |
| StuffDosage | old_stuff_dosage | 染料用量 | float | 是 | FloatField |
| DyePhaseName | old_dye_phase_name | 染色工艺 | varchar；字节长度 100 | 是 | CharField |
| GaoLaodu | old_gao_laodu | 高牢度 | varchar；字节长度 100 | 是 | CharField |
| Note | old_note | 配方 | varchar；字节长度 1000 | 是 | CharField |
| Customer | old_customer | 客户 | varchar；字节长度 50 | 是 | CharField |
| Photo | old_photo | Photo | image | 是 | BinaryField |
| StanPrice | old_stan_price | 标准单价 | decimal(9,2) | 是 | DecimalField |
| ConPrice | old_con_price | 参考单价 | decimal(9,2) | 是 | DecimalField |
| GradeID | old_grade_id | 色号等级 | varchar；字节长度 20 | 是 | CharField |
| RightStatus | old_right_status | 审核 | smallint | 是 | IntegerField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 50 | 是 | CharField |
| FabricKind | old_fabric_kind | 纱种类别 | varchar；字节长度 50 | 是 | CharField |
| YarnCategory | old_yarn_category | 服务方式 | varchar；字节长度 50 | 是 | CharField |
| SumPrice | old_sum_price | SumPrice | decimal(10,2) | 是 | DecimalField |
| SumChengBen | old_sum_cheng_ben | 总成本 | decimal(6,2) | 是 | DecimalField |
| ChengBen0 | old_cheng_ben0 | 染色成本 | decimal(6,2) | 是 | DecimalField |
| ChengBen1 | old_cheng_ben1 | 前纺成本 | decimal(6,2) | 是 | DecimalField |
| ChengBen2 | old_cheng_ben2 | 后纺成本 | decimal(6,2) | 是 | DecimalField |
| ChengBen3 | old_cheng_ben3 | 加捻成本 | decimal(6,2) | 是 | DecimalField |
| ChengBen4 | old_cheng_ben4 | 包装成本 | decimal(6,2) | 是 | DecimalField |
| ChengBen5 | old_cheng_ben5 | 合股夹纱成本 | decimal(6,2) | 是 | DecimalField |
| FenTouPrice | old_fen_tou_price | 分头报价 | decimal(6,2) | 是 | DecimalField |
| MinAmount | old_min_amount | 最低消费 | decimal(8,2) | 是 | DecimalField |

关联 `source_parent_1` → `erp_sales.SourceDyeFixedPrice`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 QuoteDetail → Quote。

### SourceDyeFixedPriceProcess — 财务结算与成本相关表（FixedPriceProcess，待确认）

源表：`dye.FixedPriceProcess`；新表：`src_dye_fixedpriceprocess`；原主键：SheetSeries, DetailNo, ProcessID。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号(子表) | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 表单明细号 | varchar；字节长度 36 | 否 | CharField |
| ProcessID | old_process_id | 工序 | varchar；字节长度 50 | 否 | CharField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 300 | 是 | CharField |

关联 `source_parent_1` → `erp_sales.SourceDyeFixedPrice`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 QuotePriceProcess → Quote。

### SourceDyeOrderAssign — 客户订单与销售相关表（OrderAssign，待确认）

源表：`dye.OrderAssign`；新表：`src_dye_orderassign`；原主键：SheetSeries, CheckNo, AssignNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 否 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 是 | CharField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| Packs | old_packs | 件数 | decimal(7,2) | 是 | DecimalField |
| GWeight | old_gweight | 胚纱克重 | decimal(6,2) | 是 | DecimalField |
| GWidth | old_gwidth | 坏纱门幅 | decimal(6,2) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 仓位代码 | varchar；字节长度 10 | 是 | CharField |
| RollAvgQty | old_roll_avg_qty | 平均粒长\粒重 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| AssignNo | old_assign_no | 预配单号 | tinyint | 否 | IntegerField |
| LengthQty | old_length_qty | 长度数量 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量数量 | decimal(10,2) | 是 | DecimalField |
| MachineID | old_machine_id | 机号 | varchar；字节长度 10 | 是 | CharField |
| DetailsCustomer | old_details_customer | 织厂 | nchar；字节长度 20 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |
| PreField2 | old_pre_field2 | 氨纶 | varchar；字节长度 50 | 是 | CharField |
| PreField3 | old_pre_field3 | 针数 | varchar；字节长度 50 | 是 | CharField |
| PreField4 | old_pre_field4 | 寸数 | varchar；字节长度 50 | 是 | CharField |
| PreField5 | old_pre_field5 | 车架 | varchar；字节长度 50 | 是 | CharField |
| AssignFabKind | old_assign_fab_kind | AssignFabKind | tinyint | 是 | IntegerField |

关联 `source_parent_1` → `erp_sales.SourceDyeOrderColor`；原码 `SheetSeries, CheckNo` → 父表原码 `SheetSeries, CheckNo`；依据：原界面主从 OrderAssign → OrderColor；原界面主从 PrintOrderAssign → PrintOrderColor；原界面主从 OrderAssignSup → OrderColorSup；原界面主从 OrderAssignChange → OrderColorChange。

### SourceDyeOrderAssign2 — 客户订单与销售相关表（OrderAssign2，待确认）

源表：`dye.OrderAssign2`；新表：`src_dye_orderassign2`；原主键：SheetSeries, AssignNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| AssignNo | old_assign_no | 预配单号 | tinyint | 否 | IntegerField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 是 | CharField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 200 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 200 | 是 | CharField |
| Packs | old_packs | 件数 | decimal(7,2) | 是 | DecimalField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度数量 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量数量 | decimal(10,2) | 是 | DecimalField |
| GWeight | old_gweight | 胚纱克重 | decimal(6,2) | 是 | DecimalField |
| GWidth | old_gwidth | 坏纱门幅 | decimal(6,2) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 仓位代码 | varchar；字节长度 10 | 是 | CharField |
| RollAvgQty | old_roll_avg_qty | 平均粒长\粒重 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| AssignFabKind | old_assign_fab_kind | 纱来源类型 | tinyint | 是 | IntegerField |
| LastPacks | old_last_packs | 剩余包数 | decimal(10,2) | 是 | DecimalField |
| LastRolls | old_last_rolls | 剩余粒数 | decimal(10,2) | 是 | DecimalField |
| LastLengthQty | old_last_length_qty | 剩余长度 | decimal(10,2) | 是 | DecimalField |
| LastWeightQty | old_last_weight_qty | 剩余重量 | decimal(10,2) | 是 | DecimalField |

关联 `source_parent_1` → `erp_sales.SourceDyeOrderMain`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 PrintOrderAssign2 → PrintOrderMain；原界面主从 OrderAssign2 → OrderMain；原界面主从 OrderAssign2Sup → OrderMainSup。

### SourceDyeOrderAtte — 生产工单与排程相关表（OrderAtte，待确认）

源表：`dye.OrderAtte`；新表：`src_dye_orderatte`；原主键：SheetSeries, FieldType, AtteCode, CheckNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| FieldType | old_field_type | 基础数据类别 | varchar；字节长度 20 | 否 | CharField |
| AtteCode | old_atte_code | 事项代码 | varchar；字节长度 10 | 否 | CharField |
| AtteValue | old_atte_value | 事项内容 | varchar；字节长度 500 | 是 | CharField |
| Description | old_description | 描述 | nvarchar；字节长度 1000 | 是 | CharField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| PriceUnit | old_price_unit | 计价单位 | tinyint | 是 | IntegerField |
| CheckNo | old_check_no | 订单号 | varchar；字节长度 30 | 否 | CharField |

关联 `source_parent_1` → `erp_sales.SourceDyeOrderColor`；原码 `SheetSeries, CheckNo` → 父表原码 `SheetSeries, CheckNo`；依据：原界面主从 OrderAtte → OrderColor；原界面主从 qry_GetOrderAtteToJob → qry_GetOrderInfoToJob。

关联 `source_parent_2` → `erp_sales.SourceDyeOrderMain`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 OrderAtteChange → OrderMainChange；原界面主从 OrderAtteSup → OrderMainSup；原界面主从 PrintOrderAtte → PrintOrderMain。

### SourceDyeOrderColor — 订单颜色/规格明细

源表：`dye.OrderColor`；新表：`src_dye_ordercolor`；原主键：CheckNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 否 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 200 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 200 | 是 | CharField |
| RelaLotNo | old_rela_lot_no | 参考批号 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 150 | 是 | CharField |
| ColorE | old_color_e | 颜色英文名 | varchar；字节长度 20 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 50 | 是 | CharField |
| DesignNo | old_design_no | 花号 | varchar；字节长度 20 | 是 | CharField |
| WidthDn | old_width_dn | 门幅下限 | varchar；字节长度 150 | 是 | CharField |
| WidthUp | old_width_up | 门幅上限 | decimal(6,2) | 是 | DecimalField |
| WidthKindID | old_width_kind_id | 幅宽种类 | nvarchar；字节长度 40 | 是 | CharField |
| WeightDn | old_weight_dn | 克重下限 | varchar；字节长度 150 | 是 | CharField |
| WeightUp | old_weight_up | 克重上限 | decimal(6,2) | 是 | DecimalField |
| OrderQty | old_order_qty | 成品数量 | decimal(10,2) | 是 | DecimalField |
| OrderRolls | old_order_rolls | 订单粒数 | decimal(10,2) | 是 | DecimalField |
| GrayQty | old_gray_qty | 投坏数量 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 染整价格 | decimal(8,2) | 是 | DecimalField |
| Fee | old_fee | 费用 | decimal(10,2) | 是 | DecimalField |
| Amount | old_amount | 金额 | decimal(10,2) | 是 | DecimalField |
| DlvDate | old_dlv_date | 染色日期 | datetime | 是 | DateTimeField |
| SumDlvRolls | old_sum_dlv_rolls | 合计交货粒数 | decimal(7,2) | 是 | DecimalField |
| SumDlvQty | old_sum_dlv_qty | 合计交货数量 | decimal(10,2) | 是 | DecimalField |
| ToPlace | old_to_place | 交货地点 | varchar；字节长度 500 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 250 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 10 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 100 | 是 | CharField |
| ProductionID | old_production_id | 工艺线路 | varchar；字节长度 10 | 是 | CharField |
| CardQty | old_card_qty | 缸数 | smallint | 是 | IntegerField |
| StandCraftNo | old_stand_craft_no | 标准工艺号 | varchar；字节长度 20 | 是 | CharField |
| CraftCheck | old_craft_check | 工艺审核状态 | bit | 是 | BooleanField |
| TechCheck | old_tech_check | 技术审核状态 | bit | 是 | BooleanField |
| PlanCheck | old_plan_check | 计划审核状态 | bit | 是 | BooleanField |
| CustFabricName | old_cust_fabric_name | 客户规格 | varchar；字节长度 250 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 150 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 -1 | 是 | TextField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 150 | 是 | CharField |
| CustSelfNoDetail | old_cust_self_no_detail | 客户单号明细 | varchar；字节长度 150 | 是 | CharField |
| MainStuffKindID | old_main_stuff_kind_id | 主染料类别 | varchar；字节长度 10 | 是 | CharField |
| FinalDlvDate | old_final_dlv_date | 协议交货日期 | datetime | 是 | DateTimeField |
| IsToDoSample | old_is_to_do_sample | 打样安排 | varchar；字节长度 10 | 是 | CharField |
| IsSampleCharge | old_is_sample_charge | 打样是否收费 | bit | 是 | BooleanField |
| CraftCheckIdea | old_craft_check_idea | 工艺审核意见 | varchar；字节长度 300 | 是 | CharField |
| CraftCheckTime | old_craft_check_time | 工艺审核时间 | datetime | 是 | DateTimeField |
| PlanCheckIdea | old_plan_check_idea | 计划审核意见 | varchar；字节长度 300 | 是 | CharField |
| PlanCheckTime | old_plan_check_time | 计划审核时间 | datetime | 是 | DateTimeField |
| TechCheckIdea | old_tech_check_idea | 技术审核意见 | varchar；字节长度 300 | 是 | CharField |
| TechCheckTime | old_tech_check_time | 技术审核时间 | datetime | 是 | DateTimeField |
| ColorRGB | old_color_rgb | 颜色RGB | int | 是 | IntegerField |
| SumProdRolls | old_sum_prod_rolls | 合计成品粒数 | decimal(7,2) | 是 | DecimalField |
| SumProdQty | old_sum_prod_qty | 合计成品数量 | decimal(10,2) | 是 | DecimalField |
| IsContinue | old_is_continue | 连缸 | bit | 是 | BooleanField |
| IsToConfirmed | old_is_to_confirmed | 是否要确认 | bit | 是 | BooleanField |
| IsSpecColor | old_is_spec_color | 特殊颜色 | bit | 是 | BooleanField |
| IsSpecVat | old_is_spec_vat | 小缸 | bit | 是 | BooleanField |
| ColorCards | old_color_cards | 色卡份数 | tinyint | 是 | IntegerField |
| Atte | old_atte | 特殊事项 | varchar；字节长度 100 | 是 | CharField |
| ProgramKindID | old_program_kind_id | 染色工艺分类 | varchar；字节长度 10 | 是 | CharField |
| IsHaveFirstVat | old_is_have_first_vat | 有头缸 | bit | 是 | BooleanField |
| ConfirmSideID | old_confirm_side_id | 对色面 | varchar；字节长度 10 | 是 | CharField |
| ProcessPrice | old_process_price | 另收费项目单价 | decimal(8,2) | 是 | DecimalField |
| PriceCheck | old_price_check | 价格审核状态 | bit | 是 | BooleanField |
| PriceCheckIdea | old_price_check_idea | 价格审核意见 | varchar；字节长度 300 | 是 | CharField |
| PriceCheckTime | old_price_check_time | 价格审核时间 | datetime | 是 | DateTimeField |
| CraftChecker | old_craft_checker | 工艺审核人 | varchar；字节长度 10 | 是 | CharField |
| TechChecker | old_tech_checker | 技术审核人 | varchar；字节长度 10 | 是 | CharField |
| PriceChecker | old_price_checker | 价格审核人 | varchar；字节长度 10 | 是 | CharField |
| PlanChecker | old_plan_checker | 计划审核人 | varchar；字节长度 10 | 是 | CharField |
| PrepareVats | old_prepare_vats | 前处理缸数 | decimal(5,1) | 是 | DecimalField |
| WeightUnit | old_weight_unit | 克重单位 | nvarchar；字节长度 40 | 是 | CharField |
| Model1 | old_model1 | 款号 | varchar；字节长度 200 | 是 | CharField |
| ColorKind | old_color_kind | ColorKind | varchar；字节长度 20 | 是 | CharField |
| Code | old_code | 颜色备用 | varchar；字节长度 20 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | StorageUnitIDs | varchar；字节长度 100 | 是 | CharField |
| RollAvgQtyStr | old_roll_avg_qty_str | RollAvgQtyStr | varchar；字节长度 50 | 是 | CharField |
| Unit | old_unit | 单位 | varchar；字节长度 50 | 是 | CharField |
| IsFinished | old_is_finished | IsFinished | bit | 是 | BooleanField |
| PreProductionID | old_pre_production_id | PreProductionID | varchar；字节长度 50 | 是 | CharField |
| FabricKindID | old_fabric_kind_id | FabricKindID | varchar；字节长度 10 | 是 | CharField |
| LOT | old_lot | LOT | varchar；字节长度 50 | 是 | CharField |
| ColorMatch | old_color_match | ColorMatch | varchar；字节长度 500 | 是 | CharField |
| NeedleCountUp | old_needle_count_up | NeedleCountUp | smallint | 是 | IntegerField |
| NeedleCountDn | old_needle_count_dn | NeedleCountDn | smallint | 是 | IntegerField |
| Twist | old_twist | Twist | int | 是 | IntegerField |
| Tenters | old_tenters | Tenters | int | 是 | IntegerField |
| Plaiting | old_plaiting | Plaiting | varchar；字节长度 50 | 是 | CharField |
| Edge | old_edge | 手感 | varchar；字节长度 50 | 是 | CharField |
| CodeFront | old_code_front | CodeFront | varchar；字节长度 50 | 是 | CharField |
| ProviderCode | old_provider_code | ProviderCode | varchar；字节长度 16 | 是 | CharField |
| DlvAddress | old_dlv_address | DlvAddress | varchar；字节长度 200 | 是 | CharField |
| PlanDate | old_plan_date | PlanDate | datetime | 是 | DateTimeField |
| RequireWeight | old_require_weight | RequireWeight | decimal(10,2) | 是 | DecimalField |
| RequireKG | old_require_kg | RequireKG | decimal(10,2) | 是 | DecimalField |
| MachinePin | old_machine_pin | 织厂 | varchar；字节长度 200 | 是 | CharField |
| MachineDozen | old_machine_dozen | MachineDozen | float | 是 | FloatField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 50 | 是 | CharField |
| OutQty | old_out_qty | OutQty | decimal(10,2) | 是 | DecimalField |
| OutYard | old_out_yard | OutYard | decimal(10,2) | 是 | DecimalField |
| DryFub | old_dry_fub | DryFub | varchar；字节长度 20 | 是 | CharField |
| WetFub | old_wet_fub | WetFub | varchar；字节长度 20 | 是 | CharField |
| WashFastness | old_wash_fastness | WashFastness | varchar；字节长度 20 | 是 | CharField |
| SolarFastness | old_solar_fastness | SolarFastness | varchar；字节长度 20 | 是 | CharField |
| ShrinV | old_shrin_v | ShrinV | varchar；字节长度 30 | 是 | CharField |
| ShrinL | old_shrin_l | ShrinL | varchar；字节长度 30 | 是 | CharField |
| CutYard | old_cut_yard | CutYard | decimal(10,2) | 是 | DecimalField |
| Remarks01 | old_remarks01 | 备注01 | varchar；字节长度 512 | 是 | CharField |
| Remarks02 | old_remarks02 | 明细状态 | varchar；字节长度 512 | 是 | CharField |
| Remarks03 | old_remarks03 | 参考缸号 | varchar；字节长度 512 | 是 | CharField |
| Remarks04 | old_remarks04 | Remarks04 | varchar；字节长度 512 | 是 | CharField |
| PrintCode | old_print_code | 花号 | varchar；字节长度 50 | 是 | CharField |
| ColorPlateID | old_color_plate_id | 色位号 | varchar；字节长度 10 | 是 | CharField |
| FilmNo | old_film_no | 菲林号 | varchar；字节长度 50 | 是 | CharField |
| Width | old_width | 幅宽 | varchar；字节长度 200 | 是 | CharField |
| Weight | old_weight | 克重 | varchar；字节长度 200 | 是 | CharField |
| AddWeigth | old_add_weigth | 空计 | float | 是 | FloatField |
| TubeWeight | old_tube_weight | 纸筒 | float | 是 | FloatField |
| CustGrayID | old_cust_gray_id | 客纱种编码 | varchar；字节长度 50 | 是 | CharField |
| Rate | old_rate | 浮动百分比 | float | 是 | FloatField |
| ColorRemarks | old_color_remarks | 用途 | varchar；字节长度 500 | 是 | CharField |
| WidthUnit | old_width_unit | WidthUnit | nvarchar；字节长度 40 | 是 | CharField |
| WeightKindID | old_weight_kind_id | 克重单位 | nvarchar；字节长度 40 | 是 | CharField |
| IsSupplement | old_is_supplement | 补单 | bit | 是 | BooleanField |
| bhd | old_bhd | 备货单 | bit | 是 | BooleanField |
| GradeID | old_grade_id | 色号等级 | varchar；字节长度 50 | 是 | CharField |
| GWName | old_gwname | 缸位字母 | varchar；字节长度 20 | 是 | CharField |
| DyeDate | old_dye_date | 交货日期 | varchar；字节长度 150 | 是 | CharField |
| Postpone_Advance | old_postpone_advance | Postpone_Advance | varchar；字节长度 150 | 是 | CharField |
| BatchColorCase | old_batch_color_case | BatchColorCase | varchar；字节长度 150 | 是 | CharField |
| IsPurAplNo | old_is_pur_apl_no | 是否采购申请单(旧ERP申请单) | bit | 是 | BooleanField |
| CustJobNo | old_cust_job_no | 客户缸号 | varchar；字节长度 100 | 是 | CharField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| ApproveDate | old_approve_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 30 | 是 | CharField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 30 | 是 | CharField |
| ModifyDate | old_modify_date | 审核时间 | datetime | 是 | DateTimeField |
| SheetStatus | old_sheet_status | 中止状态 | smallint | 是 | IntegerField |

关联 `source_parent_1` → `erp_sales.SourceDyeOrderMain`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 OrderColorSup → OrderMainSup；原界面主从 OrderColor → OrderMain；原界面主从 PrintOrderColor → PrintOrderMain；原界面主从 OrderColorChange → OrderMainChange。

### SourceDyeOrderCombine — 客户订单与销售相关表（OrderCombine，待确认）

源表：`dye.OrderCombine`；新表：`src_dye_ordercombine`；原主键：SheetSeries, CheckNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 否 | CharField |
| Rolls | old_rolls | Rolls | decimal(7,2) | 是 | DecimalField |
| Qty | old_qty | Qty | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 300 | 是 | CharField |

### SourceDyeOrderDlvApply — 客户订单与销售相关表（OrderDlvApply，待确认）

源表：`dye.OrderDlvApply`；新表：`src_dye_orderdlvapply`；原主键：SheetSeries。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 编号 | varchar；字节长度 36 | 是 | CharField |
| BusinessKind | old_business_kind | BusinessKind | smallint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| SalerID | old_saler_id | 业务员 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度数量 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量数量 | decimal(10,2) | 是 | DecimalField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 20 | 是 | CharField |
| ApproveIdea | old_approve_idea | ApproveIdea | varchar；字节长度 200 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| ApplyDlvDate | old_apply_dlv_date | 交货日期 | date | 是 | DateField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| SheetType | old_sheet_type | SheetType | smallint | 是 | IntegerField |
| ApplyKindID | old_apply_kind_id | 申请种类 | varchar；字节长度 50 | 是 | CharField |
| Status | old_status | 状态 | tinyint | 是 | IntegerField |
| OrderSheetSeries | old_order_sheet_series | 订单流水号 | varchar；字节长度 20 | 是 | CharField |
| Reason | old_reason | 原因 | varchar；字节长度 256 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |
| PreField2 | old_pre_field2 | 打回原因 | varchar；字节长度 50 | 是 | CharField |
| PreField3 | old_pre_field3 | PreField3 | varchar；字节长度 50 | 是 | CharField |
| PreField4 | old_pre_field4 | PreField4 | varchar；字节长度 50 | 是 | CharField |
| PreField5 | old_pre_field5 | PreField5 | varchar；字节长度 50 | 是 | CharField |
| IsVIP | old_is_vip | 是否VIP | bit | 是 | BooleanField |
| VipReason | old_vip_reason | VIP原因 | varchar；字节长度 500 | 是 | CharField |

### SourceDyeOrderDlvApplyLock — 客户订单与销售相关表（OrderDlvApplyLock，待确认）

源表：`dye.OrderDlvApplyLock`；新表：`src_dye_orderdlvapplylock`；原主键：ApplyKindID, ApplyDlvDate。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ApplyDlvDate | old_apply_dlv_date | 申请日期 | date | 否 | DateField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度数量 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量数量 | decimal(10,2) | 是 | DecimalField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| Status | old_status | 状态 | tinyint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| ApplyKindID | old_apply_kind_id | 申请种类 | varchar；字节长度 50 | 否 | CharField |

### SourceDyeOrderDlvApplySheet — 客户订单与销售相关表（OrderDlvApplySheet，待确认）

源表：`dye.OrderDlvApplySheet`；新表：`src_dye_orderdlvapplysheet`；原主键：SheetSeries, OrderSheetSeries。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 50 | 否 | CharField |
| OrderSheetSeries | old_order_sheet_series | 订单流水号 | varchar；字节长度 20 | 否 | CharField |
| OrderSheetNo | old_order_sheet_no | 订单号 | varchar；字节长度 20 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 下单日期 | datetime | 是 | DateTimeField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度数量 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量数量 | decimal(10,2) | 是 | DecimalField |
| Status | old_status | 状态 | tinyint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |

关联 `source_parent_1` → `erp_sales.SourceDyeOrderMain`；原码 `OrderSheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 OrderDlvApplySheet → OrderMain；原界面主从 PrintOrderDlvApplySheet → PrintOrderMain；原界面主从 OrderDlvApplySheetSup → OrderMainSup。

### SourceDyeOrderFee — 客户订单与销售相关表（OrderFee，待确认）

源表：`dye.OrderFee`；新表：`src_dye_orderfee`；原主键：SheetSeries, FeeKindID。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| FeeKindID | old_fee_kind_id | FeeKindID | varchar；字节长度 10 | 否 | CharField |
| PreValue | old_pre_value | PreValue | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |
| RealValue | old_real_value | RealValue | decimal(10,2) | 是 | DecimalField |
| Description | old_description | Description | varchar；字节长度 100 | 是 | CharField |
| CurrDate | old_curr_date | CurrDate | datetime | 是 | DateTimeField |
| Maker | old_maker | Maker | varchar；字节长度 10 | 是 | CharField |

### SourceDyeOrderInfo — 客户订单与销售相关表（OrderInfo，待确认）

源表：`dye.OrderInfo`；新表：`src_dye_orderinfo`；原主键：SheetSeries。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| SheetType | old_sheet_type | 订单分型 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 否 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 200 | 是 | CharField |
| FabricKindID | old_fabric_kind_id | 纱编类别 | varchar；字节长度 10 | 是 | CharField |
| ColorKind | old_color_kind | 颜色类别 | varchar；字节长度 20 | 是 | CharField |
| LOT | old_lot | LOT号 | varchar；字节长度 50 | 是 | CharField |
| ColorMatch | old_color_match | 对色资料 | varchar；字节长度 500 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| NeedleCountUp | old_needle_count_up | 针数/寸数 | smallint | 是 | IntegerField |
| NeedleCountDn | old_needle_count_dn | 针数/寸数 | smallint | 是 | IntegerField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 150 | 是 | CharField |
| Twist | old_twist | 扭度 | int | 是 | IntegerField |
| Tenters | old_tenters | 定型 | int | 是 | IntegerField |
| WeightDn | old_weight_dn | (折纱)克重 | decimal(6,2) | 是 | DecimalField |
| Plaiting | old_plaiting | 折纱 | varchar；字节长度 50 | 是 | CharField |
| WeightUp | old_weight_up | (定型)克重 | decimal(6,2) | 是 | DecimalField |
| Edge | old_edge | 连边 | varchar；字节长度 50 | 是 | CharField |
| CodeFront | old_code_front | 编号头 | varchar；字节长度 50 | 是 | CharField |
| ProviderCode | old_provider_code | 供应商 | varchar；字节长度 16 | 是 | CharField |
| DlvAddress | old_dlv_address | 送交 | varchar；字节长度 200 | 是 | CharField |
| DlvDate | old_dlv_date | 交货日期 | datetime | 是 | DateTimeField |
| PlanDate | old_plan_date | 排交日期 | datetime | 是 | DateTimeField |
| RequireWeight | old_require_weight | 要求重量 | decimal(10,2) | 是 | DecimalField |
| RequireKG | old_require_kg | (要求)公斤 | decimal(10,2) | 是 | DecimalField |
| MachinePin | old_machine_pin | 扁机尺寸 | nvarchar；字节长度 100 | 是 | CharField |
| MachineDozen | old_machine_dozen | 扁机打数 | float | 是 | FloatField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 50 | 是 | CharField |
| OutQty | old_out_qty | 客户要求出货数量 | decimal(10,2) | 是 | DecimalField |
| OutYard | old_out_yard | 客户要求出货码数 | decimal(10,2) | 是 | DecimalField |
| DryFub | old_dry_fub | 干擦级数 | varchar；字节长度 20 | 是 | CharField |
| WetFub | old_wet_fub | 湿擦级数 | varchar；字节长度 20 | 是 | CharField |
| WashFastness | old_wash_fastness | 洗水级数 | varchar；字节长度 20 | 是 | CharField |
| SolarFastness | old_solar_fastness | 日晒级数 | varchar；字节长度 20 | 是 | CharField |
| ShrinV | old_shrin_v | 横缩 | varchar；字节长度 30 | 是 | CharField |
| ShrinL | old_shrin_l | 直缩 | varchar；字节长度 30 | 是 | CharField |
| CutYard | old_cut_yard | 成品剪码数 | decimal(10,2) | 是 | DecimalField |
| Remarks01 | old_remarks01 | 工场备注1 | varchar；字节长度 512 | 是 | CharField |
| Remarks02 | old_remarks02 | 工场备注2 | varchar；字节长度 512 | 是 | CharField |
| Remarks03 | old_remarks03 | 仓库备注 | varchar；字节长度 512 | 是 | CharField |
| Remarks04 | old_remarks04 | 执胚单 | varchar；字节长度 512 | 是 | CharField |

### SourceDyeOrderInfoProcess — 染色工艺与配方相关表（OrderInfoProcess，待确认）

源表：`dye.OrderInfoProcess`；新表：`src_dye_orderinfoprocess`；原主键：SheetSeries, ProcessNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| ProcessNo | old_process_no | 顺序 | tinyint | 否 | IntegerField |
| ProcessID | old_process_id | 工序编号 | varchar；字节长度 10 | 是 | CharField |
| ProcessName | old_process_name | 工序名称 | varchar；字节长度 100 | 是 | CharField |
| ProcessClass | old_process_class | 类别 | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_sales.SourceDyeOrderInfo`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 OrderInfoProcess → OrderInfo。

### SourceDyeOrderMain — 订单主表

源表：`dye.OrderMain`；新表：`src_dye_ordermain`；原主键：SheetSeries。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| SheetType | old_sheet_type | 订单分型 | smallint | 是 | IntegerField |
| OrderKindID | old_order_kind_id | 订单类别代码 | varchar；字节长度 10 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 150 | 是 | CharField |
| SalerID | old_saler_id | 业务员 | varchar；字节长度 10 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 500 | 是 | CharField |
| Linker | old_linker | 品牌 | varchar；字节长度 250 | 是 | CharField |
| ExchangeRate | old_exchange_rate | 汇率 | decimal(10,2) | 是 | DecimalField |
| PriceUnit | old_price_unit | 计价单位编码 | tinyint | 是 | IntegerField |
| CurrencyID | old_currency_id | 币别 | varchar；字节长度 10 | 是 | CharField |
| PaymentID | old_payment_id | 付款方式 | varchar；字节长度 10 | 是 | CharField |
| SettleID | old_settle_id | 结算方式 | varchar；字节长度 10 | 是 | CharField |
| DlvMannerID | old_dlv_manner_id | 交货方式编码 | varchar；字节长度 10 | 是 | CharField |
| HandFeelID | old_hand_feel_id | 手感编码 | varchar；字节长度 10 | 是 | CharField |
| VerLight1ID | old_ver_light1_id | 主对色光源 | varchar；字节长度 10 | 是 | CharField |
| FirstDlvDate | old_first_dlv_date | 头缸交期 | datetime | 是 | DateTimeField |
| OrderUp | old_order_up | 订量上限 | tinyint | 是 | IntegerField |
| OrderDn | old_order_dn | 订量下限 | tinyint | 是 | IntegerField |
| RealGrayQty | old_real_gray_qty | 实际投坏数 | decimal(10,2) | 是 | DecimalField |
| RealGrayPrice | old_real_gray_price | 实际坏纱价格 | decimal(10,2) | 是 | DecimalField |
| RealGrayMoney | old_real_gray_money | 实际坏纱成本 | decimal(10,2) | 是 | DecimalField |
| RealProdQty | old_real_prod_qty | 实际成品数量 | decimal(10,2) | 是 | DecimalField |
| RealProdPrice | old_real_prod_price | 实际成品价格 | decimal(10,2) | 是 | DecimalField |
| RealProdMoney | old_real_prod_money | 实际成品金额 | decimal(10,2) | 是 | DecimalField |
| RealLoss | old_real_loss | 实际缩率 | decimal(4,1) | 是 | DecimalField |
| RealProfit | old_real_profit | 实际毛利 | decimal(10,2) | 是 | DecimalField |
| RealUnitProfit | old_real_unit_profit | 实际毛利率 | decimal(10,2) | 是 | DecimalField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 -1 | 是 | TextField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| BusinessKind | old_business_kind | 业务类别 | smallint | 是 | IntegerField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 500 | 是 | CharField |
| VerLight2ID | old_ver_light2_id | 副光源 | varchar；字节长度 10 | 是 | CharField |
| IsHurry | old_is_hurry | 加急 | bit | 是 | BooleanField |
| FinishDate | old_finish_date | 结案日期 | datetime | 是 | DateTimeField |
| AssignUnit | old_assign_unit | 配纱单位 | tinyint | 是 | IntegerField |
| RollCodeManner | old_roll_code_manner | 箱号编码规则 | tinyint | 是 | IntegerField |
| VatCodeManner | old_vat_code_manner | 缸号编码规则 | tinyint | 是 | IntegerField |
| LabelID | old_label_id | 标签 | varchar；字节长度 10 | 是 | CharField |
| ShippingMarkID | old_shipping_mark_id | 唛头 | varchar；字节长度 10 | 是 | CharField |
| Unit | old_unit | 单位 | tinyint | 是 | IntegerField |
| AddQty | old_add_qty | 加码数量 | decimal(6,2) | 是 | DecimalField |
| Discount | old_discount | 折扣 | decimal(3,2) | 是 | DecimalField |
| ClothInspection | old_cloth_inspection | 检验方法 | tinyint | 是 | IntegerField |
| FactID | old_fact_id | 工厂 | varchar；字节长度 10 | 是 | CharField |
| ToPlace | old_to_place | 交货地点 | varchar；字节长度 500 | 是 | CharField |
| WeftDensity | old_weft_density | 纬密 | decimal(6,2) | 是 | DecimalField |
| WarpDensity | old_warp_density | 经密 | decimal(6,2) | 是 | DecimalField |
| TakeFabStatus | old_take_fab_status | 带纱状态 | varchar；字节长度 1 | 是 | CharField |
| LinkerInfo | old_linker_info | 联系人信息 | varchar；字节长度 100 | 是 | CharField |
| Loss | old_loss | 数值缩率 | decimal(4,1) | 是 | DecimalField |
| LossStr | old_loss_str | 文字缩率 | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| InvoiceKind | old_invoice_kind | InvoiceKind | tinyint | 是 | IntegerField |
| AddrDlv | old_addr_dlv | 交货地址 | nvarchar；字节长度 1000 | 是 | CharField |
| RedoReasonID | old_redo_reason_id | RedoReasonID | varchar；字节长度 500 | 是 | CharField |
| IsFinished | old_is_finished | IsFinished | bit | 是 | BooleanField |
| PrepareSheetNo | old_prepare_sheet_no | 计划单号 | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| PrintCode | old_print_code | 印花 | varchar；字节长度 50 | 是 | CharField |
| BHD | old_bhd | 备货单 | bit | 是 | BooleanField |
| JiaGong | old_jia_gong | 加工要求 | varchar；字节长度 20 | 是 | CharField |

### SourceDyeOrderPriceProcess — 财务结算与成本相关表（OrderPriceProcess，待确认）

源表：`dye.OrderPriceProcess`；新表：`src_dye_orderpriceprocess`；原主键：SheetSeries, CheckNo, ProcessID。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 否 | CharField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 50 | 否 | CharField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 300 | 是 | CharField |

### SourceDyeOrderProcess — 染色工艺与配方相关表（OrderProcess，待确认）

源表：`dye.OrderProcess`；新表：`src_dye_orderprocess`；原主键：SheetSeries, CheckNo, ProcessNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 否 | CharField |
| ProcessNo | old_process_no | 工序号 | tinyint | 否 | IntegerField |
| ProcessID | old_process_id | 工序代码 | varchar；字节长度 10 | 否 | CharField |
| StationID | old_station_id | 站别代码 | varchar；字节长度 10 | 是 | CharField |
| MachineID | old_machine_id | 机台号 | varchar；字节长度 10 | 是 | CharField |
| PPName01 | old_ppname01 | 参数名1 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue01 | old_theory_value01 | 设定值1 | varchar；字节长度 20 | 是 | CharField |
| PPName02 | old_ppname02 | 参数名2 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue02 | old_theory_value02 | 设定值2 | varchar；字节长度 20 | 是 | CharField |
| PPName03 | old_ppname03 | 参数名3 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue03 | old_theory_value03 | 设定值3 | varchar；字节长度 20 | 是 | CharField |
| PPName04 | old_ppname04 | PPName04 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue04 | old_theory_value04 | TheoryValue04 | varchar；字节长度 20 | 是 | CharField |
| PPName05 | old_ppname05 | PPName05 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue05 | old_theory_value05 | TheoryValue05 | varchar；字节长度 20 | 是 | CharField |
| PPName06 | old_ppname06 | PPName06 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue06 | old_theory_value06 | TheoryValue06 | varchar；字节长度 20 | 是 | CharField |
| PPName07 | old_ppname07 | PPName07 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue07 | old_theory_value07 | TheoryValue07 | varchar；字节长度 20 | 是 | CharField |
| PPName08 | old_ppname08 | PPName08 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue08 | old_theory_value08 | TheoryValue08 | varchar；字节长度 20 | 是 | CharField |
| PPName09 | old_ppname09 | PPName09 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue09 | old_theory_value09 | TheoryValue09 | varchar；字节长度 20 | 是 | CharField |
| PPName10 | old_ppname10 | PPName10 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue10 | old_theory_value10 | TheoryValue10 | varchar；字节长度 20 | 是 | CharField |
| PPName11 | old_ppname11 | PPName11 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue11 | old_theory_value11 | TheoryValue11 | varchar；字节长度 20 | 是 | CharField |
| PPName12 | old_ppname12 | PPName12 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue12 | old_theory_value12 | TheoryValue12 | varchar；字节长度 20 | 是 | CharField |
| PPName13 | old_ppname13 | PPName13 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue13 | old_theory_value13 | TheoryValue13 | varchar；字节长度 20 | 是 | CharField |
| PPName14 | old_ppname14 | PPName14 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue14 | old_theory_value14 | TheoryValue14 | varchar；字节长度 20 | 是 | CharField |
| PPName15 | old_ppname15 | PPName15 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue15 | old_theory_value15 | TheoryValue15 | varchar；字节长度 20 | 是 | CharField |
| PPName16 | old_ppname16 | PPName16 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue16 | old_theory_value16 | TheoryValue16 | varchar；字节长度 20 | 是 | CharField |
| PPName17 | old_ppname17 | PPName17 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue17 | old_theory_value17 | TheoryValue17 | varchar；字节长度 20 | 是 | CharField |
| PPName18 | old_ppname18 | PPName18 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue18 | old_theory_value18 | TheoryValue18 | varchar；字节长度 20 | 是 | CharField |
| PPName19 | old_ppname19 | PPName19 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue19 | old_theory_value19 | TheoryValue19 | varchar；字节长度 20 | 是 | CharField |
| PPName20 | old_ppname20 | PPName20 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue20 | old_theory_value20 | TheoryValue20 | varchar；字节长度 20 | 是 | CharField |
| Price | old_price | 另收费价格 | decimal(8,2) | 是 | DecimalField |
| RecipeCheck | old_recipe_check | 工序配方审核 | bit | 是 | BooleanField |
| RecipeSeries | old_recipe_series | 工序配方流水号 | varchar；字节长度 20 | 是 | CharField |

关联 `source_parent_1` → `erp_sales.SourceDyeOrderColor`；原码 `SheetSeries, CheckNo` → 父表原码 `SheetSeries, CheckNo`；依据：原界面主从 OrderProcessChange → OrderColorChange；原界面主从 PrintOrderProcess → PrintOrderColor；原界面主从 OrderProcess → OrderColor；原界面主从 qry_GetOrderProcessToJob → qry_GetOrderColorToJob；原界面主从 OrderProcessSup → OrderColorSup；原界面主从 OrderProcessExtraChange → OrderColorChange；原界面主从 OrderProcessExtra → OrderColor；原界面主从 OrderProcessExtraSup → OrderColorSup。

### SourceDyeOrderProcessPre — 染色工艺与配方相关表（OrderProcessPre，待确认）

源表：`dye.OrderProcessPre`；新表：`src_dye_orderprocesspre`；原主键：SheetSeries, CheckNo, ProcessNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水 | varchar；字节长度 50 | 否 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 否 | CharField |
| ProcessNo | old_process_no | 工序号 | tinyint | 否 | IntegerField |
| ProcessID | old_process_id | 工序 | varchar；字节长度 10 | 是 | CharField |
| StationID | old_station_id | 站别 | varchar；字节长度 10 | 是 | CharField |
| Price | old_price | 价格 | decimal(10,4) | 是 | DecimalField |
| PPName01 | old_ppname01 | 参数名1 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue01 | old_theory_value01 | 设定值1 | varchar；字节长度 20 | 是 | CharField |
| PPName02 | old_ppname02 | 参数名2 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue02 | old_theory_value02 | 设定值2 | varchar；字节长度 20 | 是 | CharField |
| PPName03 | old_ppname03 | 参数名3 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue03 | old_theory_value03 | 设定值3 | varchar；字节长度 20 | 是 | CharField |
| PPName04 | old_ppname04 | 参数名4 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue04 | old_theory_value04 | 设定值4 | varchar；字节长度 20 | 是 | CharField |
| PPName05 | old_ppname05 | 参数名5 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue05 | old_theory_value05 | 设定值5 | varchar；字节长度 20 | 是 | CharField |
| PPName06 | old_ppname06 | 参数名6 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue06 | old_theory_value06 | 设定值6 | varchar；字节长度 20 | 是 | CharField |
| PPName07 | old_ppname07 | 参数名7 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue07 | old_theory_value07 | 设定值7 | varchar；字节长度 20 | 是 | CharField |
| PPName08 | old_ppname08 | 参数名8 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue08 | old_theory_value08 | 设定值8 | varchar；字节长度 20 | 是 | CharField |
| PPName09 | old_ppname09 | 参数名9 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue09 | old_theory_value09 | 设定值9 | varchar；字节长度 20 | 是 | CharField |
| PPName10 | old_ppname10 | 参数名10 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue10 | old_theory_value10 | 设定值10 | varchar；字节长度 20 | 是 | CharField |
| PPName11 | old_ppname11 | 参数名11 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue11 | old_theory_value11 | 设定值11 | varchar；字节长度 20 | 是 | CharField |
| PPName12 | old_ppname12 | 参数名12 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue12 | old_theory_value12 | 设定值12 | varchar；字节长度 20 | 是 | CharField |
| PPName13 | old_ppname13 | 参数名13 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue13 | old_theory_value13 | 设定值13 | varchar；字节长度 20 | 是 | CharField |
| PPName14 | old_ppname14 | 参数名14 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue14 | old_theory_value14 | 设定值14 | varchar；字节长度 20 | 是 | CharField |
| PPName15 | old_ppname15 | 参数名15 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue15 | old_theory_value15 | 设定值15 | varchar；字节长度 20 | 是 | CharField |
| PPName16 | old_ppname16 | 参数名16 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue16 | old_theory_value16 | 设定值16 | varchar；字节长度 20 | 是 | CharField |
| PPName17 | old_ppname17 | 参数名17 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue17 | old_theory_value17 | 设定值17 | varchar；字节长度 20 | 是 | CharField |
| PPName18 | old_ppname18 | 参数名18 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue18 | old_theory_value18 | 设定值18 | varchar；字节长度 20 | 是 | CharField |
| PPName19 | old_ppname19 | 参数名19 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue19 | old_theory_value19 | 设定值19 | varchar；字节长度 20 | 是 | CharField |
| PPName20 | old_ppname20 | 参数名20 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue20 | old_theory_value20 | 设定值20 | varchar；字节长度 20 | 是 | CharField |
| MachineID | old_machine_id | 机台号 | varchar；字节长度 10 | 是 | CharField |
| RecipeCheck | old_recipe_check | 工序配方审核 | bit | 是 | BooleanField |
| RecipeSeries | old_recipe_series | 配方流水号 | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 是 | CharField |

关联 `source_parent_1` → `erp_sales.SourceDyeOrderColor`；原码 `SheetSeries, CheckNo` → 父表原码 `SheetSeries, CheckNo`；依据：原界面主从 PrintOrderProcessPre → PrintOrderColor；原界面主从 OrderProcessPreSup → OrderColorSup。

### SourceDyePriceAdjust — 财务结算与成本相关表（PriceAdjust，待确认）

源表：`dye.PriceAdjust`；新表：`src_dye_priceadjust`；原主键：SheetSeries。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 单据流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 单据编号 | varchar；字节长度 36 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| DateType | old_date_type | 日期类型 | nvarchar；字节长度 20 | 是 | CharField |
| StartDate | old_start_date | 实行日期 | datetime | 是 | DateTimeField |
| AdjustMoney | old_adjust_money | 调整金额 | decimal(14,6) | 是 | DecimalField |
| AdjustRatio | old_adjust_ratio | 调整比例 | decimal(8,4) | 是 | DecimalField |
| Creater | old_creater | 调价人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 调价日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |

### SourceDyePriceAdjustDetail — 财务结算与成本相关表（PriceAdjustDetail，待确认）

源表：`dye.PriceAdjustDetail`；新表：`src_dye_priceadjustdetail`；原主键：SheetSeries, DetailNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 单据编号 | varchar；字节长度 50 | 否 | CharField |
| DetailNo | old_detail_no | 明细编号 | varchar；字节长度 36 | 否 | CharField |
| QuoteDetailNo | old_quote_detail_no | 报价单明细号 | varchar；字节长度 50 | 是 | CharField |
| AdjustPrice | old_adjust_price | 调整后价格 | decimal(16,4) | 是 | DecimalField |
| OldPrice | old_old_price | 调价前价格 | decimal(16,4) | 是 | DecimalField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 50 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 20 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 20 | 是 | CharField |
| FlowMain | old_flow_main | 加工主流程 | varchar；字节长度 50 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 100 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 报价日期 | datetime | 是 | DateTimeField |
| SheetNo | old_sheet_no | 报价单号 | varchar；字节长度 50 | 是 | CharField |
| CustSelfProdCode | old_cust_self_prod_code | 客纱类编码 | varchar；字节长度 100 | 是 | CharField |
| ProcessMemo | old_process_memo | 备注 | varchar；字节长度 50 | 是 | CharField |
| FabricKindID | old_fabric_kind_id | 类别 | varchar；字节长度 10 | 是 | CharField |

关联 `source_parent_1` → `erp_sales.SourceDyePriceAdjust`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 PriceAdjustDetail → PriceAdjust。

### SourceDyeQuote — 其他或待确认相关表（Quote，待确认）

源表：`dye.Quote`；新表：`src_dye_quote`；原主键：SheetSeries。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 否 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| QuoteKindID | old_quote_kind_id | 报价类别 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员代码 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| Linker | old_linker | 联系人 | varchar；字节长度 10 | 是 | CharField |
| CurrencyID | old_currency_id | 币别 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| SettleID | old_settle_id | 结算方式 | varchar；字节长度 10 | 是 | CharField |
| ExchangeRate | old_exchange_rate | 汇率 | decimal(10,2) | 是 | DecimalField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| IsConfirmed | old_is_confirmed | 确价 | smallint | 是 | IntegerField |
| BeiZhu | old_bei_zhu | BeiZhu | varchar；字节长度 150 | 是 | CharField |
| IsTax | old_is_tax | 单价类别 | varchar；字节长度 10 | 是 | CharField |
| TaxRate | old_tax_rate | 税率% | decimal(10,2) | 是 | DecimalField |
| Tel | old_tel | Tel | varchar；字节长度 100 | 是 | CharField |
| CustomerCode | old_customer_code | 客户全称 | varchar；字节长度 50 | 是 | CharField |
| LastTime | old_last_time | LastTime | datetime | 是 | DateTimeField |

### SourceDyeQuoteAtte — 生产工单与排程相关表（QuoteAtte，待确认）

源表：`dye.QuoteAtte`；新表：`src_dye_quoteatte`；原主键：SheetSeries, FieldType, AtteCode。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| FieldType | old_field_type | 基础数据类别 | varchar；字节长度 20 | 否 | CharField |
| AtteCode | old_atte_code | 事项代码 | varchar；字节长度 10 | 否 | CharField |
| AtteValue | old_atte_value | 事项内容 | varchar；字节长度 50 | 是 | CharField |
| PriceUnit | old_price_unit | 计价单位 | tinyint | 是 | IntegerField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_sales.SourceDyeQuote`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 FixedPriceAtte → FixedPrice。

### SourceDyeQuoteDetail — 其他或待确认相关表（QuoteDetail，待确认）

源表：`dye.QuoteDetail`；新表：`src_dye_quotedetail`；原主键：DetailNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 表单明细号（子表） | varchar；字节长度 36 | 否 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| Structure | old_structure | 组织 | varchar；字节长度 50 | 是 | CharField |
| Width | old_width | 幅宽 | decimal(6,2) | 否 | DecimalField |
| Weight | old_weight | 克重 | decimal(6,2) | 否 | DecimalField |
| Price | old_price | 客确价格 | decimal(8,2) | 是 | DecimalField |
| PriceUnit | old_price_unit | 单位 | tinyint | 否 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Loss | old_loss | 数值缩率 | decimal(4,1) | 是 | DecimalField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 50 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| MainStuffKindID | old_main_stuff_kind_id | 主染料类别 | varchar；字节长度 10 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 10 | 是 | CharField |
| RecipePrice | old_recipe_price | 配方成本 | decimal(8,2) | 是 | DecimalField |
| ProcessMemo | old_process_memo | 套价项目 | varchar；字节长度 300 | 是 | CharField |
| ProcessPrice | old_process_price | 另计价 | decimal(8,2) | 是 | DecimalField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 100 | 是 | CharField |
| Pricesum | old_pricesum | 总单价 | decimal(8,2) | 是 | DecimalField |
| CusPrice | old_cus_price | 对客报价 | decimal(8,2) | 是 | DecimalField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 20 | 是 | CharField |
| AdjustPrice | old_adjust_price | AdjustPrice | decimal(12,2) | 是 | DecimalField |
| StartDate | old_start_date | 调价实行日期 | datetime | 是 | DateTimeField |
| DateType | old_date_type | 调价日期类型 | tinyint | 是 | IntegerField |
| IsConfirmed | old_is_confirmed | 是否确价 | smallint | 是 | IntegerField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 32 | 是 | CharField |
| ColorNumNO | old_color_num_no | 确版号 | varchar；字节长度 10 | 是 | CharField |
| StuffDosage | old_stuff_dosage | 染料用量 | float | 是 | FloatField |
| DyePhaseName | old_dye_phase_name | 染色工艺 | varchar；字节长度 100 | 是 | CharField |
| GaoLaodu | old_gao_laodu | 高牢度 | varchar；字节长度 100 | 是 | CharField |
| Note | old_note | 配方 | varchar；字节长度 1000 | 是 | CharField |
| Customer | old_customer | 客户 | varchar；字节长度 50 | 是 | CharField |
| Photo | old_photo | Photo | image | 是 | BinaryField |
| StanPrice | old_stan_price | 标准单价 | decimal(9,2) | 是 | DecimalField |
| ConPrice | old_con_price | 参考单价 | decimal(9,2) | 是 | DecimalField |
| GradeID | old_grade_id | 色号等级 | varchar；字节长度 20 | 是 | CharField |
| RightStatus | old_right_status | 审核 | smallint | 是 | IntegerField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | varchar；字节长度 50 | 是 | CharField |
| FixedSheetNo | old_fixed_sheet_no | 报价单号 | varchar；字节长度 50 | 是 | CharField |
| YarnCategory | old_yarn_category | YarnCategory | varchar；字节长度 50 | 是 | CharField |
| SumPrice | old_sum_price | SumPrice | decimal(10,2) | 是 | DecimalField |
| SumChengBen | old_sum_cheng_ben | SumChengBen | decimal(6,2) | 是 | DecimalField |
| ChengBen0 | old_cheng_ben0 | ChengBen0 | decimal(6,2) | 是 | DecimalField |
| ChengBen1 | old_cheng_ben1 | ChengBen1 | decimal(6,2) | 是 | DecimalField |
| ChengBen2 | old_cheng_ben2 | ChengBen2 | decimal(6,2) | 是 | DecimalField |
| ChengBen3 | old_cheng_ben3 | ChengBen3 | decimal(6,2) | 是 | DecimalField |
| ChengBen4 | old_cheng_ben4 | ChengBen4 | decimal(6,2) | 是 | DecimalField |
| ChengBen5 | old_cheng_ben5 | ChengBen5 | decimal(6,2) | 是 | DecimalField |

关联 `source_parent_1` → `erp_sales.SourceDyeQuote`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 FixedPriceDetail → FixedPrice。

### SourceDyeQuoteItemPrice — 财务结算与成本相关表（QuoteItemPrice，待确认）

源表：`dye.QuoteItemPrice`；新表：`src_dye_quoteitemprice`；原主键：DetailNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 30 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 20 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 100 | 是 | CharField |
| Price | old_price | Price | decimal(6,1) | 是 | DecimalField |
| Unit | old_unit | Unit | varchar；字节长度 20 | 是 | CharField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |
| Item | old_item | Item | varchar；字节长度 50 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 50 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 50 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | varchar；字节长度 50 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| IsConfirmed | old_is_confirmed | IsConfirmed | smallint | 是 | IntegerField |
| FabricKindID | old_fabric_kind_id | 胚纱类别 | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_sales.SourceDyeFixedPrice`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 QuoteItemPrice → Quote。

### SourceDyeQuotePriceAtte — 财务结算与成本相关表（QuotePriceAtte，待确认）

源表：`dye.QuotePriceAtte`；新表：`src_dye_quotepriceatte`；原主键：SheetSeries, FieldType, AtteCode, DetailNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| FieldType | old_field_type | FieldType | varchar；字节长度 20 | 否 | CharField |
| AtteCode | old_atte_code | AtteCode | varchar；字节长度 10 | 否 | CharField |
| AtteValue | old_atte_value | AtteValue | varchar；字节长度 500 | 是 | CharField |
| PriceUnit | old_price_unit | PriceUnit | tinyint | 是 | IntegerField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| Description | old_description | Description | varchar；字节长度 500 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 30 | 否 | CharField |

### SourceDyeQuotePriceProcess — 财务结算与成本相关表（QuotePriceProcess，待确认）

源表：`dye.QuotePriceProcess`；新表：`src_dye_quotepriceprocess`；原主键：SheetSeries, DetailNo, ProcessID。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号(子表) | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 表单明细号 | varchar；字节长度 36 | 否 | CharField |
| ProcessID | old_process_id | 工序 | varchar；字节长度 50 | 否 | CharField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 300 | 是 | CharField |

关联 `source_parent_1` → `erp_sales.SourceDyeQuote`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 FixedPriceProcess → FixedPrice。

### SourceDyeRCORDERCOLOR — 染色工艺与配方相关表（RCORDERCOLOR，待确认）

源表：`dye.RCORDERCOLOR`；新表：`src_dye_rcordercolor`；原主键：无主键。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 是 | CharField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 20 | 是 | CharField |
| CustFabricName | old_cust_fabric_name | CustFabricName | varchar；字节长度 250 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 150 | 是 | CharField |
| CustColorNum | old_cust_color_num | CustColorNum | varchar；字节长度 20 | 是 | CharField |
| Width | old_width | Width | varchar；字节长度 200 | 是 | CharField |
| WidthUnit | old_width_unit | WidthUnit | nvarchar；字节长度 40 | 是 | CharField |
| Weight | old_weight | Weight | varchar；字节长度 200 | 是 | CharField |
| WeightKindID | old_weight_kind_id | WeightKindID | nvarchar；字节长度 40 | 是 | CharField |
| OrderRolls | old_order_rolls | OrderRolls | decimal(10,2) | 是 | DecimalField |
| TubeWeight | old_tube_weight | TubeWeight | float | 是 | FloatField |
| AddWeigth | old_add_weigth | AddWeigth | float | 是 | FloatField |
| DlvDate | old_dlv_date | DlvDate | datetime | 是 | DateTimeField |
| CustSelfNo | old_cust_self_no | CustSelfNo | varchar；字节长度 500 | 是 | CharField |

### SourceDyeRCORDERMAIN — 客户订单与销售相关表（RCORDERMAIN，待确认）

源表：`dye.RCORDERMAIN`；新表：`src_dye_rcordermain`；原主键：无主键。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 是 | CharField |
| CustSelfNo | old_cust_self_no | CustSelfNo | varchar；字节长度 500 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 -1 | 是 | TextField |

### SourceDyeZDAddPrice — 财务结算与成本相关表（ZDAddPrice，待确认）

源表：`dye.ZDAddPrice`；新表：`src_dye_zdaddprice`；原主键：SheetSeries。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 30 | 否 | CharField |
| SheetNo | old_sheet_no | 表单号 | varchar；字节长度 30 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyeZDAddPriceDetail — 财务结算与成本相关表（ZDAddPriceDetail，待确认）

源表：`dye.ZDAddPriceDetail`；新表：`src_dye_zdaddpricedetail`；原主键：DetailNo。

归属依据：报价/订单/客户业务来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单号 | varchar；字节长度 30 | 是 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 30 | 否 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 30 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 30 | 是 | CharField |
| Price | old_price | 单价 | decimal(10,2) | 是 | DecimalField |
| PriceUnit | old_price_unit | 报价单位 | int | 是 | IntegerField |
| Remarks1 | old_remarks1 | 备注1 | varchar；字节长度 512 | 是 | CharField |
| Remarks2 | old_remarks2 | 备注2 | varchar；字节长度 512 | 是 | CharField |

关联 `source_parent_1` → `erp_sales.SourceDyeZDAddPrice`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ZDAddPriceDetail → ZDAddPrice。

## 采购管理

新增原表模型 10 个，原字段 253 个。

### SourceDyeArticlePurDetail — 其他或待确认相关表（ArticlePurDetail，待确认）

源表：`dye.ArticlePurDetail`；新表：`src_dye_articlepurdetail`；原主键：DetailNo。

归属依据：采购来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 否 | CharField |
| ApplySheetNo | old_apply_sheet_no | ApplySheetNo | varchar；字节长度 20 | 是 | CharField |
| SupplierID | old_supplier_id | SupplierID | varchar；字节长度 10 | 是 | CharField |
| ArticleKindID | old_article_kind_id | ArticleKindID | varchar；字节长度 20 | 是 | CharField |
| ArticleID | old_article_id | ArticleID | varchar；字节长度 20 | 是 | CharField |
| Unit | old_unit | Unit | varchar；字节长度 20 | 是 | CharField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| NeedQty | old_need_qty | NeedQty | decimal(10,2) | 是 | DecimalField |
| Qty | old_qty | Qty | decimal(10,2) | 是 | DecimalField |
| Amount | old_amount | Amount | decimal(10,2) | 是 | DecimalField |
| UseID | old_use_id | UseID | varchar；字节长度 10 | 是 | CharField |
| DlvDate | old_dlv_date | DlvDate | datetime | 是 | DateTimeField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| PackQty | old_pack_qty | PackQty | decimal(10,2) | 是 | DecimalField |
| PackUnit | old_pack_unit | PackUnit | varchar；字节长度 10 | 是 | CharField |
| FinishDate | old_finish_date | FinishDate | datetime | 是 | DateTimeField |

### SourceDyeArticlePurMain — 其他或待确认相关表（ArticlePurMain，待确认）

源表：`dye.ArticlePurMain`；新表：`src_dye_articlepurmain`；原主键：SheetSeries。

归属依据：采购来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| DeptID | old_dept_id | 部门编码 | varchar；字节长度 10 | 是 | CharField |
| PurKindID | old_pur_kind_id | 采购类别代码 | varchar；字节长度 10 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| CurrencyID | old_currency_id | 币别 | varchar；字节长度 10 | 是 | CharField |
| ExchangeRate | old_exchange_rate | 汇率 | decimal(10,2) | 是 | DecimalField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| BuyerID | old_buyer_id | 采购员 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyeFabricPurDetail — 坯布半成品成品与仓储相关表（FabricPurDetail，待确认）

源表：`dye.FabricPurDetail`；新表：`src_dye_fabricpurdetail`；原主键：DetailNo。

归属依据：采购来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 否 | CharField |
| ApplySheetNo | old_apply_sheet_no | ApplySheetNo | varchar；字节长度 20 | 是 | CharField |
| FabricID | old_fabric_id | FabricID | varchar；字节长度 128 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 是 | CharField |
| Structure | old_structure | Structure | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 20 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 20 | 是 | CharField |
| DesignNo | old_design_no | DesignNo | varchar；字节长度 20 | 是 | CharField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| PriceUnit | old_price_unit | PriceUnit | tinyint | 是 | IntegerField |
| Rolls | old_rolls | Rolls | decimal(7,2) | 是 | DecimalField |
| Qty | old_qty | Qty | decimal(10,2) | 是 | DecimalField |
| Fee | old_fee | Fee | decimal(10,2) | 是 | DecimalField |
| Amount | old_amount | Amount | decimal(10,2) | 是 | DecimalField |
| DlvDate | old_dlv_date | DlvDate | datetime | 是 | DateTimeField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 是 | CharField |
| OrderDn | old_order_dn | OrderDn | tinyint | 是 | IntegerField |
| OrderUp | old_order_up | OrderUp | tinyint | 是 | IntegerField |
| ToPlace | old_to_place | ToPlace | varchar；字节长度 500 | 是 | CharField |
| WeightDn | old_weight_dn | WeightDn | decimal(6,2) | 是 | DecimalField |
| WeightUp | old_weight_up | WeightUp | decimal(6,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |

### SourceDyeFabricPurMain — 坯布半成品成品与仓储相关表（FabricPurMain，待确认）

源表：`dye.FabricPurMain`；新表：`src_dye_fabricpurmain`；原主键：SheetSeries。

归属依据：采购来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| PurKindID | old_pur_kind_id | PurKindID | varchar；字节长度 10 | 是 | CharField |
| SupplierID | old_supplier_id | SupplierID | varchar；字节长度 10 | 是 | CharField |
| BuyerID | old_buyer_id | BuyerID | varchar；字节长度 10 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | SalerGroupID | varchar；字节长度 10 | 是 | CharField |
| ContractNo | old_contract_no | ContractNo | varchar；字节长度 20 | 是 | CharField |
| DlvMannerID | old_dlv_manner_id | DlvMannerID | varchar；字节长度 10 | 是 | CharField |
| SumAmount | old_sum_amount | SumAmount | decimal(10,2) | 是 | DecimalField |
| SumFee | old_sum_fee | SumFee | decimal(10,2) | 是 | DecimalField |
| SettleID | old_settle_id | SettleID | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyePurApplyDetail — 其他或待确认相关表（PurApplyDetail，待确认）

源表：`dye.PurApplyDetail`；新表：`src_dye_purapplydetail`；原主键：DetailNo。

归属依据：采购来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | 表单明细号（子表） | varchar；字节长度 20 | 否 | CharField |
| OrderNo | old_order_no | 订单号 | varchar；字节长度 20 | 是 | CharField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 10 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 50 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 20 | 是 | CharField |
| Structure | old_structure | 组织 | varchar；字节长度 50 | 是 | CharField |
| FabricID2 | old_fabric_id2 | 供应商胚纱编号 | varchar；字节长度 10 | 是 | CharField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 10 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| DesignNo | old_design_no | 花号 | varchar；字节长度 20 | 是 | CharField |
| FirstDlvDate | old_first_dlv_date | 头缸交期 | datetime | 是 | DateTimeField |
| GrayQty | old_gray_qty | 投胚数 | decimal(10,2) | 是 | DecimalField |
| RollAvgQty | old_roll_avg_qty | 平均粒长/粒重 | decimal(10,2) | 是 | DecimalField |
| GrayPrice | old_gray_price | 胚纱价格 | decimal(10,2) | 是 | DecimalField |
| PriceUnit | old_price_unit | 计价单位编码 | tinyint | 是 | IntegerField |
| Amount | old_amount | 金额 | decimal(10,2) | 是 | DecimalField |
| GrayMoney | old_gray_money | 胚纱金额 | decimal(10,2) | 是 | DecimalField |
| GrayWeight | old_gray_weight | 胚纱克重 | decimal(6,2) | 是 | DecimalField |
| GrayWidth | old_gray_width | 胚纱门幅 | decimal(6,2) | 是 | DecimalField |
| GrayDlvDate | old_gray_dlv_date | 胚纱交期 | datetime | 是 | DateTimeField |
| ProdQty | old_prod_qty | 成品数 | decimal(10,2) | 是 | DecimalField |
| ProdDlvDate | old_prod_dlv_date | 大货交期 | datetime | 是 | DateTimeField |
| ProdWeight | old_prod_weight | 成品克重 | decimal(6,2) | 是 | DecimalField |
| ProdWidth | old_prod_width | 成品门幅 | decimal(6,2) | 是 | DecimalField |
| Loss | old_loss | 数值缩率 | decimal(4,1) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| GrayWeightDn | old_gray_weight_dn | 胚纱克重下限 | decimal(6,2) | 是 | DecimalField |
| GrayWidthDn | old_gray_width_dn | 胚纱门幅下限 | decimal(6,2) | 是 | DecimalField |
| ProdWeightDn | old_prod_weight_dn | 成品克重下限 | decimal(6,2) | 是 | DecimalField |
| ProdWidthDn | old_prod_width_dn | 成品门幅下限 | decimal(6,2) | 是 | DecimalField |
| ArticleID | old_article_id | 物料编码 | varchar；字节长度 20 | 是 | CharField |
| ArticleName | old_article_name | 物料名称 | varchar；字节长度 20 | 是 | CharField |
| ArticleKindID | old_article_kind_id | 物料种类 | varchar；字节长度 20 | 是 | CharField |
| StuffID | old_stuff_id | 染化料编码 | varchar；字节长度 20 | 是 | CharField |
| StuffName | old_stuff_name | 染化料名称 | varchar；字节长度 20 | 是 | CharField |
| StuffKindID | old_stuff_kind_id | 染化料种类 | varchar；字节长度 20 | 是 | CharField |
| ArticleUnit | old_article_unit | 物料单位 | varchar；字节长度 20 | 是 | CharField |
| StuffUnit | old_stuff_unit | 染化料单位 | varchar；字节长度 20 | 是 | CharField |
| Price | old_price | 单价 | decimal(10,2) | 是 | DecimalField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| remarks2 | old_remarks2 | remarks2 | varchar；字节长度 255 | 是 | CharField |

关联 `source_parent_1` → `erp_purchase.SourceDyePurApplyMain`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ArticlePurApplyDetail → ArticlePurApplyMain；原界面主从 StuffPurApplyDetail → StuffPurApplyMain；原界面主从 PurApplyDetail → PurApplyMain。

### SourceDyePurApplyMain — 其他或待确认相关表（PurApplyMain，待确认）

源表：`dye.PurApplyMain`；新表：`src_dye_purapplymain`；原主键：SheetSeries。

归属依据：采购来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| PurKindID | old_pur_kind_id | 采购类别代码 | varchar；字节长度 10 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商代码 | varchar；字节长度 10 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| SalerID | old_saler_id | 业务员代码 | varchar；字节长度 10 | 是 | CharField |
| BuyerID | old_buyer_id | 采购员 | varchar；字节长度 10 | 是 | CharField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| DeptID | old_dept_id | 部门名称 | varchar；字节长度 50 | 是 | CharField |
| FactID | old_fact_id | 所属分厂 | varchar；字节长度 50 | 是 | CharField |
| DlvMannerID | old_dlv_manner_id | 交货方式 | varchar；字节长度 200 | 是 | CharField |
| Approver | old_approver | 审核人 | varchar；字节长度 50 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Applicant | old_applicant | 申请人 | nchar；字节长度 60 | 是 | CharField |

### SourceDyePurDetail — 其他或待确认相关表（PurDetail，待确认）

源表：`dye.PurDetail`；新表：`src_dye_purdetail`；原主键：DetailNo。

归属依据：采购来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 表单明细号（子表） | varchar；字节长度 20 | 否 | CharField |
| ApplySheetNo | old_apply_sheet_no | 审购单号 | varchar；字节长度 20 | 是 | CharField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 150 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 50 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 20 | 是 | CharField |
| Structure | old_structure | 组织 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 10 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| DesignNo | old_design_no | 花稿号 | varchar；字节长度 20 | 是 | CharField |
| Price | old_price | 价格 | decimal(8,4) | 是 | DecimalField |
| PriceUnit | old_price_unit | 计价单位编码 | tinyint | 是 | IntegerField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| Fee | old_fee | 费用 | decimal(10,2) | 是 | DecimalField |
| Amount | old_amount | 金额 | decimal(10,2) | 是 | DecimalField |
| DlvDate | old_dlv_date | 交货日期 | datetime | 是 | DateTimeField |
| OrderDn | old_order_dn | 订量下限 | tinyint | 是 | IntegerField |
| OrderUp | old_order_up | 订量上限 | tinyint | 是 | IntegerField |
| ToPlace | old_to_place | 交货地点 | varchar；字节长度 50 | 是 | CharField |
| WeightDn | old_weight_dn | 克重下限 | decimal(6,2) | 是 | DecimalField |
| WeightUp | old_weight_up | 克重上限 | decimal(6,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 否 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| ArticleID | old_article_id | 物料编码 | varchar；字节长度 50 | 是 | CharField |
| ArticleName | old_article_name | 物料名称 | varchar；字节长度 50 | 是 | CharField |
| ArticleKindID | old_article_kind_id | 物料种类 | varchar；字节长度 50 | 是 | CharField |
| ArticleUnit | old_article_unit | ArticleUnit | varchar；字节长度 50 | 是 | CharField |
| StuffID | old_stuff_id | 染化料编码 | varchar；字节长度 50 | 是 | CharField |
| StuffName | old_stuff_name | 染化料名称 | varchar；字节长度 50 | 是 | CharField |
| StuffKindID | old_stuff_kind_id | 染化料种类 | varchar；字节长度 50 | 是 | CharField |
| StuffUnit | old_stuff_unit | 染化料单位 | varchar；字节长度 50 | 是 | CharField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_purchase.SourceDyeArticlePurMain`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ArticlePurDetail → ArticlePurMain。

关联 `source_parent_2` → `erp_purchase.SourceDyePurMain`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 PurDetail → PurMain。

关联 `source_parent_3` → `erp_purchase.SourceDyeStuffPurMain`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 StuffPurDetail → StuffPurMain。

### SourceDyePurMain — 其他或待确认相关表（PurMain，待确认）

源表：`dye.PurMain`；新表：`src_dye_purmain`；原主键：SheetSeries。

归属依据：采购来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| PurKindID | old_pur_kind_id | 采购类别代码 | varchar；字节长度 10 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商 | varchar；字节长度 10 | 是 | CharField |
| Factory | old_factory | 加工厂 | varchar；字节长度 50 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| BuyerID | old_buyer_id | 采购员 | varchar；字节长度 10 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 20 | 是 | CharField |
| OrderNo | old_order_no | 订单号 | varchar；字节长度 20 | 是 | CharField |
| DlvDate | old_dlv_date | 交货日期 | datetime | 是 | DateTimeField |
| DlvMannerID | old_dlv_manner_id | 交货方式编码 | varchar；字节长度 10 | 是 | CharField |
| SumAmount | old_sum_amount | 总金额 | decimal(10,2) | 是 | DecimalField |
| SumFee | old_sum_fee | 总费用 | decimal(10,2) | 是 | DecimalField |
| SettleID | old_settle_id | 结算方式 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |

### SourceDyeStuffPurDetail — 染化料与称料库存相关表（StuffPurDetail，待确认）

源表：`dye.StuffPurDetail`；新表：`src_dye_stuffpurdetail`；原主键：DetailNo。

归属依据：采购来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 否 | CharField |
| ApplySheetNo | old_apply_sheet_no | ApplySheetNo | varchar；字节长度 20 | 是 | CharField |
| SupplierID | old_supplier_id | SupplierID | varchar；字节长度 10 | 是 | CharField |
| StuffID | old_stuff_id | StuffID | varchar；字节长度 10 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 是 | CharField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| NeedQty | old_need_qty | NeedQty | decimal(10,2) | 是 | DecimalField |
| Qty | old_qty | Qty | decimal(10,2) | 是 | DecimalField |
| Amount | old_amount | Amount | decimal(10,2) | 是 | DecimalField |
| PackQty | old_pack_qty | PackQty | decimal(10,2) | 是 | DecimalField |
| PackUnit | old_pack_unit | PackUnit | varchar；字节长度 10 | 是 | CharField |
| DlvDate | old_dlv_date | DlvDate | datetime | 是 | DateTimeField |
| FinishDate | old_finish_date | FinishDate | datetime | 是 | DateTimeField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| PriceUnit | old_price_unit | PriceUnit | tinyint | 是 | IntegerField |

### SourceDyeStuffPurMain — 染化料与称料库存相关表（StuffPurMain，待确认）

源表：`dye.StuffPurMain`；新表：`src_dye_stuffpurmain`；原主键：SheetSeries。

归属依据：采购来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| DeptID | old_dept_id | 部门编码 | varchar；字节长度 10 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| PurKindID | old_pur_kind_id | 采购类别代码 | varchar；字节长度 10 | 是 | CharField |
| BuyerID | old_buyer_id | 采购员 | varchar；字节长度 10 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |

## 打样管理

新增原表模型 51 个，原字段 990 个。

### SourceDboBackDyeRecipePhase — 染色工艺与配方相关表（BackDyeRecipePhase，待确认）

源表：`dbo.BackDyeRecipePhase`；新表：`src_dbo_backdyerecipephase`；原主键：无主键。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 是 | CharField |
| PhaseNo | old_phase_no | PhaseNo | varchar；字节长度 50 | 是 | CharField |
| PhaseID | old_phase_id | PhaseID | varchar；字节长度 50 | 是 | CharField |
| ProgramID | old_program_id | ProgramID | varchar；字节长度 50 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 50 | 是 | CharField |

### SourceDyeAddDyeWProcessStep — 染色工艺与配方相关表（AddDyeWProcessStep，待确认）

源表：`dye.AddDyeWProcessStep`；新表：`src_dye_adddyewprocessstep`；原主键：WPStepNo。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| WPStepNo | old_wpstep_no | WPStepNo | varchar；字节长度 20 | 否 | CharField |
| WProcessNo | old_wprocess_no | WProcessNo | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| ProcessNo | old_process_no | ProcessNo | tinyint | 是 | IntegerField |
| ProcessID | old_process_id | 工序 | varchar；字节长度 10 | 是 | CharField |
| DyeProcessID | old_dye_process_id | DyeProcessID | nvarchar；字节长度 100 | 是 | CharField |
| RealValue | old_real_value | 比例 | decimal(10,2) | 是 | DecimalField |
| RecordID | old_record_id | 染色工 | nvarchar；字节长度 76 | 是 | CharField |
| CurrTime | old_curr_time | 日期 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |
| ProgramID | old_program_id | 计件项目 | varchar；字节长度 50 | 是 | CharField |
| Rolls | old_rolls | 粒数 | int | 是 | IntegerField |
| WeightQty | old_weight_qty | 重量 | float | 是 | FloatField |
| MachineNo | old_machine_no | 机台 | varchar；字节长度 10 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 100 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 100 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 100 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 100 | 是 | CharField |

### SourceDyeColorCard — 染色工艺与配方相关表（ColorCard，待确认）

源表：`dye.ColorCard`；新表：`src_dye_colorcard`；原主键：SheetSeries。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | SalerGroupID | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 10 | 是 | CharField |
| Linker | old_linker | Linker | varchar；字节长度 10 | 是 | CharField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 10 | 是 | CharField |
| ColorNo | old_color_no | ColorNo | varchar；字节长度 20 | 是 | CharField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 20 | 是 | CharField |
| ColorE | old_color_e | ColorE | varchar；字节长度 20 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 20 | 是 | CharField |
| CustColorNum | old_cust_color_num | CustColorNum | varchar；字节长度 20 | 是 | CharField |
| ColorDepthID | old_color_depth_id | ColorDepthID | varchar；字节长度 10 | 是 | CharField |
| ColorRGB | old_color_rgb | ColorRGB | int | 是 | IntegerField |
| ColorVersion | old_color_version | ColorVersion | varchar；字节长度 20 | 是 | CharField |
| ColorCards | old_color_cards | ColorCards | tinyint | 是 | IntegerField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| LimitDays | old_limit_days | LimitDays | int | 是 | IntegerField |
| Maker | old_maker | Maker | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | WareHouseID | varchar；字节长度 10 | 是 | CharField |
| StorageUnitID | old_storage_unit_id | StorageUnitID | varchar；字节长度 10 | 是 | CharField |
| Place | old_place | Place | varchar；字节长度 100 | 是 | CharField |
| MainStuffKindID | old_main_stuff_kind_id | MainStuffKindID | varchar；字节长度 10 | 是 | CharField |
| RFID | old_rfid | RFID | varchar；字节长度 20 | 是 | CharField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyeColorCardDetail — 染色工艺与配方相关表（ColorCardDetail，待确认）

源表：`dye.ColorCardDetail`；新表：`src_dye_colorcarddetail`；原主键：SheetSeries, WorkSheetKind, DataTableName, ProcessID。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| WorkSheetKind | old_work_sheet_kind | WorkSheetKind | tinyint | 否 | IntegerField |
| DataTableName | old_data_table_name | DataTableName | varchar；字节长度 50 | 否 | CharField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 10 | 否 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| Photo | old_photo | Photo | image | 是 | BinaryField |
| Signer | old_signer | Signer | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 300 | 是 | CharField |

### SourceDyeColorCardFlow — 系统平台与配置相关表（ColorCardFlow，待确认）

源表：`dye.ColorCardFlow`；新表：`src_dye_colorcardflow`；原主键：SheetSeries, SignedDate。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SignedDate | old_signed_date | SignedDate | datetime | 否 | DateTimeField |
| Flag | old_flag | Flag | tinyint | 是 | IntegerField |
| Signer | old_signer | Signer | varchar；字节长度 10 | 是 | CharField |

### SourceDyeColorChangeRisk — 染色工艺与配方相关表（ColorChangeRisk，待确认）

源表：`dye.ColorChangeRisk`；新表：`src_dye_colorchangerisk`；原主键：SheetSeries, JobSheetNo, ColorNum。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 否 | CharField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| GrayName | old_gray_name | GrayName | varchar；字节长度 150 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| ProdName | old_prod_name | ProdName | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 50 | 否 | CharField |
| Color | old_color | Color | varchar；字节长度 50 | 是 | CharField |
| CustColorNum | old_cust_color_num | CustColorNum | varchar；字节长度 50 | 是 | CharField |
| ROLLS | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| Weight | old_weight | Weight | decimal(7,2) | 是 | DecimalField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| Remarks | old_remarks | Remarks | varchar；字节长度 500 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| CustomerShortName | old_customer_short_name | CustomerShortName | varchar；字节长度 50 | 是 | CharField |
| CustomerName | old_customer_name | CustomerName | varchar；字节长度 250 | 是 | CharField |
| ChangeColorID | old_change_color_id | ChangeColorID | varchar；字节长度 250 | 是 | CharField |
| ChangeColor | old_change_color | ChangeColor | varchar；字节长度 250 | 是 | CharField |
| ChangeCustColorNum | old_change_cust_color_num | ChangeCustColorNum | varchar；字节长度 250 | 是 | CharField |
| CustomerOrderCode | old_customer_order_code | CustomerOrderCode | varchar；字节长度 250 | 是 | CharField |

### SourceDyeCptLabRecipe — 染色工艺与配方相关表（CptLabRecipe，待确认）

源表：`dye.CptLabRecipe`；新表：`src_dye_cptlabrecipe`；原主键：ID。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | bigint | 否 | BigIntegerField |
| strCode | old_str_code | strCode | varchar；字节长度 30 | 是 | CharField |
| lVersion | old_l_version | lVersion | int | 是 | IntegerField |
| strName | old_str_name | strName | varchar；字节长度 50 | 是 | CharField |
| strSubstateCode | old_str_substate_code | strSubstateCode | varchar；字节长度 30 | 是 | CharField |
| strOperator | old_str_operator | strOperator | varchar；字节长度 20 | 是 | CharField |
| strCustomer | old_str_customer | strCustomer | varchar；字节长度 50 | 是 | CharField |
| dwSampleWt | old_dw_sample_wt | dwSampleWt | float | 是 | FloatField |
| dwLiquidRatio | old_dw_liquid_ratio | dwLiquidRatio | float | 是 | FloatField |
| dwTotalWt | old_dw_total_wt | dwTotalWt | float | 是 | FloatField |
| dtModifyDate | old_dt_modify_date | dtModifyDate | datetime | 是 | DateTimeField |
| dwCostPerKg | old_dw_cost_per_kg | dwCostPerKg | float | 是 | FloatField |
| strUser1 | old_str_user1 | strUser1 | varchar；字节长度 40 | 是 | CharField |
| strUser2 | old_str_user2 | strUser2 | varchar；字节长度 40 | 是 | CharField |
| strUser3 | old_str_user3 | strUser3 | varchar；字节长度 40 | 是 | CharField |
| bAddWater | old_b_add_water | bAddWater | bit | 否 | BooleanField |
| strPotCode | old_str_pot_code | strPotCode | varchar；字节长度 20 | 是 | CharField |
| dwStdDispWt | old_dw_std_disp_wt | dwStdDispWt | float | 是 | FloatField |
| lDispFlag | old_l_disp_flag | lDispFlag | int | 是 | IntegerField |
| IP | old_ip | IP | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |

### SourceDyeCptLabRecipeDetail — 染色工艺与配方相关表（CptLabRecipeDetail，待确认）

源表：`dye.CptLabRecipeDetail`；新表：`src_dye_cptlabrecipedetail`；原主键：ID。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | bigint | 否 | BigIntegerField |
| nSide | old_n_side | nSide | smallint | 是 | IntegerField |
| dwRate | old_dw_rate | dwRate | float | 是 | FloatField |
| bManualSel | old_b_manual_sel | bManualSel | bit | 否 | BooleanField |
| dwStrength | old_dw_strength | dwStrength | float | 是 | FloatField |
| dwCalWt | old_dw_cal_wt | dwCalWt | float | 是 | FloatField |
| strCode | old_str_code | strCode | varchar；字节长度 30 | 是 | CharField |
| lVersion | old_l_version | lVersion | int | 是 | IntegerField |
| lDetSeq | old_l_det_seq | lDetSeq | int | 是 | IntegerField |
| lBottNo | old_l_bott_no | lBottNo | int | 是 | IntegerField |
| strProdCode | old_str_prod_code | strProdCode | varchar；字节长度 30 | 是 | CharField |
| strUnit | old_str_unit | strUnit | varchar；字节长度 1 | 是 | CharField |
| dwDispWt | old_dw_disp_wt | dwDispWt | float | 是 | FloatField |
| IP | old_ip | IP | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| dtModifyDate | old_dt_modify_date | dtModifyDate | datetime | 是 | DateTimeField |

### SourceDyeCurSmpPrescriptEntry — 其他或待确认相关表（Cur_Smp_PrescriptEntry，待确认）

源表：`dye.Cur_Smp_PrescriptEntry`；新表：`src_dye_cur_smp_prescriptentry`；原主键：FInterID, FEntryID, FParentID。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FInterID | old_finter_id | FInterID | int | 否 | IntegerField |
| FEntryID | old_fentry_id | FEntryID | int | 否 | IntegerField |
| FParentID | old_fparent_id | FParentID | int | 否 | IntegerField |
| PhaseNo | old_phase_no | PhaseNo | int | 是 | IntegerField |
| StuffNo | old_stuff_no | StuffNo | int | 是 | IntegerField |
| FItemID | old_fitem_id | FItemID | int | 是 | IntegerField |
| FTechID | old_ftech_id | FTechID | int | 是 | IntegerField |
| FTechUnit | old_ftech_unit | FTechUnit | varchar；字节长度 30 | 是 | CharField |
| FRatioQty | old_fratio_qty | FRatioQty | decimal(28,10) | 是 | DecimalField |
| FRealRatioQty | old_freal_ratio_qty | FRealRatioQty | decimal(28,10) | 是 | DecimalField |
| FPrice | old_fprice | FPrice | decimal(28,10) | 是 | DecimalField |
| FAmount | old_famount | FAmount | decimal(28,10) | 是 | DecimalField |
| FCost | old_fcost | FCost | decimal(28,10) | 是 | DecimalField |
| FNote | old_fnote | FNote | varchar；字节长度 255 | 是 | CharField |
| FBomEntryID | old_fbom_entry_id | FBomEntryID | int | 是 | IntegerField |
| FCalculateID | old_fcalculate_id | FCalculateID | int | 是 | IntegerField |
| FRoutingRequest | old_frouting_request | FRoutingRequest | varchar；字节长度 200 | 是 | CharField |
| FC_SW | old_fc_sw | FC_SW | varchar；字节长度 50 | 是 | CharField |
| FC_PZYL | old_fc_pzyl | FC_PZYL | varchar；字节长度 50 | 是 | CharField |
| FC_SWater | old_fc_swater | FC_SWater | varchar；字节长度 50 | 是 | CharField |
| FC_PZYLI | old_fc_pzyli | FC_PZYLI | varchar；字节长度 50 | 是 | CharField |
| FC_PHZ | old_fc_phz | FC_PHZ | varchar；字节长度 50 | 是 | CharField |
| FC_DDL | old_fc_ddl | FC_DDL | varchar；字节长度 50 | 是 | CharField |
| FC_TIME | old_fc_time | FC_TIME | varchar；字节长度 50 | 是 | CharField |
| FC_WD | old_fc_wd | FC_WD | varchar；字节长度 50 | 是 | CharField |
| FC_SB | old_fc_sb | FC_SB | varchar；字节长度 50 | 是 | CharField |

### SourceDyeDyeColor — 染色工艺与配方相关表（DyeColor，待确认）

源表：`dye.DyeColor`；新表：`src_dye_dyecolor`；原主键：ColorNo。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单号 | varchar；字节长度 20 | 是 | CharField |
| ColorNo | old_color_no | 来样明细号 | varchar；字节长度 20 | 否 | CharField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 是 | CharField |
| LabDipsSource | old_lab_dips_source | LabDipsSource | tinyint | 是 | IntegerField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 10 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 20 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| ColorE | old_color_e | ColorE | varchar；字节长度 20 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客色号 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB | old_color_rgb | ColorRGB | int | 是 | IntegerField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| MainStuffKindID | old_main_stuff_kind_id | MainStuffKindID | varchar；字节长度 10 | 是 | CharField |
| IsToDoSample | old_is_to_do_sample | IsToDoSample | varchar；字节长度 10 | 是 | CharField |
| ColorCards | old_color_cards | ColorCards | tinyint | 是 | IntegerField |
| Status | old_status | Status | varchar；字节长度 2 | 是 | CharField |
| StartTime | old_start_time | StartTime | char；字节长度 14 | 是 | CharField |
| LimitHours | old_limit_hours | LimitHours | decimal(5,2) | 是 | DecimalField |
| OverTimeReason | old_over_time_reason | OverTimeReason | varchar；字节长度 20 | 是 | CharField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 10 | 是 | CharField |
| EmpID | old_emp_id | 打样人 | varchar；字节长度 10 | 是 | CharField |
| WorkQty | old_work_qty | WorkQty | decimal(10,2) | 是 | DecimalField |
| RedoTimes | old_redo_times | RedoTimes | tinyint | 是 | IntegerField |
| OriColorNo | old_ori_color_no | 原色号明细 | varchar；字节长度 20 | 是 | CharField |
| OriEmpID | old_ori_emp_id | OriEmpID | varchar；字节长度 10 | 是 | CharField |
| OriShifID | old_ori_shif_id | OriShifID | varchar；字节长度 10 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| Remarks | old_remarks | 返打版原因 | varchar；字节长度 100 | 是 | CharField |
| Width | old_width | Width | decimal(6,2) | 是 | DecimalField |
| Weight | old_weight | Weight | decimal(6,2) | 是 | DecimalField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 100 | 是 | CharField |
| GetSampleDate | old_get_sample_date | GetSampleDate | datetime | 是 | DateTimeField |
| DlvSampleDate | old_dlv_sample_date | 要求交样日期 | datetime | 是 | DateTimeField |
| DyeRemarks | old_dye_remarks | 打样要求描述 | varchar；字节长度 1000 | 是 | CharField |
| fSampleDate | old_f_sample_date | 任务分配日期 | datetime | 是 | DateTimeField |
| PhaseID | old_phase_id | 染色流程 | varchar；字节长度 100 | 是 | CharField |
| Dos | old_dos | 打样计分 | decimal(10,2) | 是 | DecimalField |
| fDos | old_f_dos | 扣分 | decimal(10,2) | 是 | DecimalField |
| DosAll | old_dos_all | 总分 | decimal(10,2) | 是 | DecimalField |
| WSampleDate | old_wsample_date | 打样完成日期 | datetime | 是 | DateTimeField |
| SSampleDate | old_ssample_date | 送样日期 | datetime | 是 | DateTimeField |
| DyeColorID | old_dye_color_id | 是否返打 | varchar；字节长度 50 | 是 | CharField |
| CreateDate | old_create_date | 制单日期 | datetime | 是 | DateTimeField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Creater | old_creater | 制单人 | varchar；字节长度 50 | 是 | CharField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 来样日期 | datetime | 是 | DateTimeField |

### SourceDyeDyeDipsRecord — 小样/打样记录

源表：`dye.DyeDipsRecord`；新表：`src_dye_dyedipsrecord`；原主键：SheetSeries。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 记录单号 | varchar；字节长度 20 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户名称 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员 | varchar；字节长度 10 | 是 | CharField |
| ColorNo | old_color_no | 颜色明细ID | varchar；字节长度 20 | 是 | CharField |
| ColorVersion | old_color_version | 色板号 | varchar；字节长度 20 | 是 | CharField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 10 | 是 | CharField |
| CheckNo | old_check_no | 订单明细ID | varchar；字节长度 20 | 是 | CharField |
| MainStuffKindID | old_main_stuff_kind_id | 主料类别 | varchar；字节长度 10 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| Structure | old_structure | 组织 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 50 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 30 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 50 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 100 | 是 | CharField |
| ColorE | old_color_e | 英文名 | varchar；字节长度 20 | 是 | CharField |
| ColorRGB | old_color_rgb | 颜色RGB | int | 是 | IntegerField |
| RecipePriceSource | old_recipe_price_source | 单价来源 | tinyint | 是 | IntegerField |
| FabricSource | old_fabric_source | 纱来源 | varchar；字节长度 1 | 是 | CharField |
| Weight | old_weight | 克重 | decimal(6,2) | 是 | DecimalField |
| CostEffirate | old_cost_effirate | 成本系数 | decimal(6,2) | 是 | DecimalField |
| Cost | old_cost | 成本 | decimal(10,2) | 是 | DecimalField |
| CostUnit | old_cost_unit | 成本单位 | varchar；字节长度 1 | 是 | CharField |
| VerLight1ID | old_ver_light1_id | 主光源 | varchar；字节长度 10 | 是 | CharField |
| VerLight2ID | old_ver_light2_id | 副光源 | varchar；字节长度 10 | 是 | CharField |
| ConfirmSideID | old_confirm_side_id | 对色面 | varchar；字节长度 10 | 是 | CharField |
| EmpID | old_emp_id | 员工名称 | varchar；字节长度 10 | 是 | CharField |
| ShiftID | old_shift_id | 班别 | varchar；字节长度 10 | 是 | CharField |
| CheckerID | old_checker_id | 检验人 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 确版时间 | datetime | 是 | DateTimeField |
| DlvSampleDate | old_dlv_sample_date | 交样日期 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| ConfirmVersion | old_confirm_version | 确版号 | varchar；字节长度 20 | 是 | CharField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| Times | old_times | 试样次数 | smallint | 是 | IntegerField |
| StuffDosage | old_stuff_dosage | 染料分量 | decimal(15,6) | 是 | DecimalField |
| LabSheetNo | old_lab_sheet_no | LabSheetNo | varchar；字节长度 20 | 是 | CharField |
| PreFinalized | old_pre_finalized | 预定 | varchar；字节长度 50 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 200 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 50 | 是 | CharField |
| CostQuote | old_cost_quote | CostQuote | decimal(10,2) | 是 | DecimalField |
| DyePhaseName | old_dye_phase_name | DyePhaseName | varchar；字节长度 100 | 是 | CharField |
| GaoLaodu | old_gao_laodu | 高牢度 | varchar；字节长度 100 | 是 | CharField |
| EmpID1 | old_emp_id1 | 打样员1 | varchar；字节长度 50 | 是 | CharField |
| ShiftCheckerID | old_shift_checker_id | 领班 | varchar；字节长度 50 | 是 | CharField |
| EmpID2 | old_emp_id2 | 打样员2 | varchar；字节长度 50 | 是 | CharField |
| EmpID3 | old_emp_id3 | 打样员3 | varchar；字节长度 50 | 是 | CharField |
| Num | old_num | 计件数 | float | 是 | FloatField |
| IsDoubleDye | old_is_double_dye | 单双染 | tinyint | 是 | IntegerField |
| Invalid | old_invalid | Invalid | bit | 是 | BooleanField |
| GradeID | old_grade_id | 色号等级 | varchar；字节长度 30 | 是 | CharField |
| ColorNumMark | old_color_num_mark | 色号类型 | varchar；字节长度 30 | 是 | CharField |
| DepthE | old_depth_e | 深浅E | varchar；字节长度 30 | 是 | CharField |
| Revise | old_revise | 是否修改 | bit | 是 | BooleanField |
| Fluorescence | old_fluorescence | 荧光类别 | varchar；字节长度 30 | 是 | CharField |
| OriColorNo | old_ori_color_no | 原色号明细 | varchar；字节长度 50 | 是 | CharField |

### SourceDyeDyeDipsRecordDetail — 染色工艺与配方相关表（DyeDipsRecordDetail，待确认）

源表：`dye.DyeDipsRecordDetail`；新表：`src_dye_dyedipsrecorddetail`；原主键：SheetSeries, PhaseNo, StuffNo。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| PhaseNo | old_phase_no | 染程序号 | tinyint | 否 | IntegerField |
| StuffNo | old_stuff_no | 染料序号 | tinyint | 否 | IntegerField |
| StuffType | old_stuff_type | 染料类别 | varchar；字节长度 1 | 是 | CharField |
| StuffID | old_stuff_id | 染料编码 | varchar；字节长度 10 | 是 | CharField |
| Price | old_price | 单价 | decimal(8,2) | 是 | DecimalField |
| DosageA | old_dosage_a | 用量比例（A） | decimal(15,6) | 是 | DecimalField |
| AmountA | old_amount_a | 金额A | decimal(10,2) | 是 | DecimalField |
| DosageB | old_dosage_b | 用量比例（B） | decimal(15,6) | 是 | DecimalField |
| AmountB | old_amount_b | 金额B | decimal(10,2) | 是 | DecimalField |
| DosageC | old_dosage_c | 用量比例（C） | decimal(15,6) | 是 | DecimalField |
| AmountC | old_amount_c | 金额C | decimal(10,2) | 是 | DecimalField |
| DosageD | old_dosage_d | 用量比例（D） | decimal(15,6) | 是 | DecimalField |
| AmountD | old_amount_d | 金额D | decimal(10,2) | 是 | DecimalField |
| DosageE | old_dosage_e | 用量比例（E） | decimal(15,6) | 是 | DecimalField |
| AmountE | old_amount_e | 金额E | decimal(10,2) | 是 | DecimalField |
| DosageF | old_dosage_f | DosageF | decimal(15,6) | 是 | DecimalField |
| AmountF | old_amount_f | AmountF | decimal(10,2) | 是 | DecimalField |
| RecipeUnit | old_recipe_unit | RecipeUnit | tinyint | 是 | IntegerField |
| DetailNote | old_detail_note | 备注 | nvarchar；字节长度 512 | 是 | CharField |
| NewStuffID | old_new_stuff_id | NewStuffID | varchar；字节长度 20 | 是 | CharField |

### SourceDyeDyeDipsRecordEmp — 染色工艺与配方相关表（DyeDipsRecordEmp，待确认）

源表：`dye.DyeDipsRecordEmp`；新表：`src_dye_dyedipsrecordemp`；原主键：SheetSeries, EmpID。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| EmpID | old_emp_id | 员工名称 | varchar；字节长度 10 | 否 | CharField |
| ColorVersion | old_color_version | 色板号 | varchar；字节长度 20 | 是 | CharField |
| CurrTime | old_curr_time | 当前时间 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |

关联 `source_parent_1` → `erp_sampling.SourceDyeDyeDipsRecord`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 DyeDipsRecordEmp → DyeDipsRecord。

### SourceDyeDyeDipsRecordNote — 染色工艺与配方相关表（DyeDipsRecordNote，待确认）

源表：`dye.DyeDipsRecordNote`；新表：`src_dye_dyedipsrecordnote`；原主键：SheetSeries。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| Note | old_note | Note | nvarchar；字节长度 2000 | 是 | CharField |
| Status | old_status | Status | bit | 是 | BooleanField |

### SourceDyeDyeDipsRecordPhase — 染色工艺与配方相关表（DyeDipsRecordPhase，待确认）

源表：`dye.DyeDipsRecordPhase`；新表：`src_dye_dyedipsrecordphase`；原主键：SheetSeries, PhaseNo。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| PhaseNo | old_phase_no | 染程序号 | tinyint | 否 | IntegerField |
| PhaseID | old_phase_id | 染程编码 | varchar；字节长度 10 | 是 | CharField |
| BathRatio | old_bath_ratio | 浴比 | decimal(6,2) | 是 | DecimalField |
| PH | old_ph | PH值 | varchar；字节长度 10 | 是 | CharField |
| ProgramID | old_program_id | 工艺编码 | varchar；字节长度 10 | 是 | CharField |
| WaterQty | old_water_qty | 水重 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Temperature | old_temperature | Temperature | decimal(5,1) | 是 | DecimalField |
| Minutes | old_minutes | Minutes | decimal(10,2) | 是 | DecimalField |

关联 `source_parent_1` → `erp_sampling.SourceDyeDyeDipsRecord`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 DyeDipsRecordPhaseDetail → DyeDipsRecord；原界面主从 DyeDipsRecordPhase → DyeDipsRecord。

关联 `source_parent_2` → `erp_sampling.SourceDyeDyeDipsRecordDetail`；原码 `SheetSeries, PhaseNo` → 父表原码 `SheetSeries, PhaseNo`；依据：原界面主从 DyeDipsRecordPhaseBulk → DyeDipsRecordDetailBulk。

### SourceDyeDyeLabAtte — 染色工艺与配方相关表（DyeLabAtte，待确认）

源表：`dye.DyeLabAtte`；新表：`src_dye_dyelabatte`；原主键：SheetSeries, FieldType, AtteCode。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| FieldType | old_field_type | 数据类别 | varchar；字节长度 20 | 否 | CharField |
| AtteCode | old_atte_code | 事项 | varchar；字节长度 10 | 否 | CharField |
| AtteValue | old_atte_value | 内容 | varchar；字节长度 500 | 是 | CharField |
| Description | old_description | 描述 | varchar；字节长度 500 | 是 | CharField |

关联 `source_parent_1` → `erp_sampling.SourceDyeDyeLabMain`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 DyeLabAtteBulk → DyeLabMainBulk；原界面主从 DyeLabAtte → DyeLabMain。

### SourceDyeDyeLabColor — 化验室颜色与打样

源表：`dye.DyeLabColor`；新表：`src_dye_dyelabcolor`；原主键：ColorNo。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 是 | CharField |
| ColorNo | old_color_no | 颜色明细号 | varchar；字节长度 20 | 否 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| LabDipsSource | old_lab_dips_source | 打样任务来源 | tinyint | 是 | IntegerField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 200 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 10 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 50 | 是 | CharField |
| OrderNum | old_order_num | 顺序编号 | varchar；字节长度 10 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| ColorE | old_color_e | 原色号 | varchar；字节长度 20 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 100 | 是 | CharField |
| ColorRGB | old_color_rgb | 颜色RGB | int | 是 | IntegerField |
| ColorAfter | old_color_after | 色号后缀 | varchar；字节长度 10 | 是 | CharField |
| ColorNumInput | old_color_num_input | 输入色号 | varchar；字节长度 20 | 是 | CharField |
| ColorNumMark | old_color_num_mark | 色号类型 | varchar；字节长度 10 | 是 | CharField |
| ColorMark | old_color_mark | 颜色代号 | varchar；字节长度 10 | 是 | CharField |
| ColorMarkt | old_color_markt | 色号前缀 | varchar；字节长度 10 | 是 | CharField |
| Price | old_price | 单价 | decimal(8,2) | 是 | DecimalField |
| MainStuffKindID | old_main_stuff_kind_id | 主料类别 | varchar；字节长度 10 | 是 | CharField |
| IsToDoSample | old_is_to_do_sample | 打样安排 | varchar；字节长度 10 | 是 | CharField |
| ColorCards | old_color_cards | 色卡份数 | tinyint | 是 | IntegerField |
| Status | old_status | 状态 | varchar；字节长度 2 | 是 | CharField |
| StartTime | old_start_time | 开始时间 | char；字节长度 14 | 是 | CharField |
| LimitHours | old_limit_hours | 限制时间 | decimal(5,2) | 是 | DecimalField |
| OverTimeReason | old_over_time_reason | 超时原因 | varchar；字节长度 20 | 是 | CharField |
| ShiftID | old_shift_id | 班别 | varchar；字节长度 10 | 是 | CharField |
| EmpID | old_emp_id | 员工 | varchar；字节长度 10 | 是 | CharField |
| WorkQty | old_work_qty | 产量 | decimal(10,2) | 是 | DecimalField |
| RedoTimes | old_redo_times | 返打次数 | tinyint | 是 | IntegerField |
| OriColorNo | old_ori_color_no | 原色号明细 | varchar；字节长度 20 | 是 | CharField |
| OriEmpID | old_ori_emp_id | 原工号 | varchar；字节长度 10 | 是 | CharField |
| OriShifID | old_ori_shif_id | 原班别 | varchar；字节长度 10 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 1000 | 是 | CharField |
| Width | old_width | 门幅 | decimal(6,2) | 是 | DecimalField |
| Weight | old_weight | 重量 | decimal(6,2) | 是 | DecimalField |
| Markt | old_markt | Markt | varchar；字节长度 10 | 是 | CharField |
| R | old_r | R | int | 是 | IntegerField |
| G | old_g | G | int | 是 | IntegerField |
| B | old_b | B | int | 是 | IntegerField |
| RGB | old_rgb | RGB | int | 是 | IntegerField |
| GradeID | old_grade_id | 色号等级 | varchar；字节长度 50 | 是 | CharField |
| KHSHORPTSH | old_khshorptsh | KHSHORPTSH | varchar；字节长度 255 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | nvarchar；字节长度 1024 | 是 | CharField |

关联 `source_parent_1` → `erp_sampling.SourceDyeDyeLabMain`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 DyeLabColor → DyeLabMain；原界面主从 DyeLabColorBulk → DyeLabMainBulk；原界面主从 ShowDyeLabColor → ShowDyeLabMain。

### SourceDyeDyeLabColorRecord — 染色工艺与配方相关表（DyeLabColorRecord，待确认）

源表：`dye.DyeLabColorRecord`；新表：`src_dye_dyelabcolorrecord`；原主键：SheetSeries, ColorNo, RecordID。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水 | varchar；字节长度 20 | 否 | CharField |
| ColorNo | old_color_no | 颜色明细号 | varchar；字节长度 20 | 否 | CharField |
| RecordID | old_record_id | 记录编号 | varchar；字节长度 50 | 否 | CharField |
| EmpID | old_emp_id | 员工 | varchar；字节长度 50 | 是 | CharField |
| StartTime | old_start_time | 开始时间 | datetime | 是 | DateTimeField |
| EndTime | old_end_time | 结束时间 | datetime | 是 | DateTimeField |
| Status | old_status | 状态 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |

关联 `source_parent_1` → `erp_sampling.SourceDyeDyeLabColor`；原码 `SheetSeries, ColorNo` → 父表原码 `SheetSeries, ColorNo`；依据：原界面主从 DyeLabColorRecord → DyeLabColor。

### SourceDyeDyeLabMain — 化验室打样主表

源表：`dye.DyeLabMain`；新表：`src_dye_dyelabmain`；原主键：SheetSeries。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 任务单号 | varchar；字节长度 20 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetStatus | old_sheet_status | 单据日期 | smallint | 是 | IntegerField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 10 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户名称 | varchar；字节长度 10 | 是 | CharField |
| OrderSheetNo | old_order_sheet_no | 订单号 | varchar；字节长度 20 | 是 | CharField |
| GetSampleDate | old_get_sample_date | 收样时间 | datetime | 是 | DateTimeField |
| ToBackSample | old_to_back_sample | 客样退回 | bit | 是 | BooleanField |
| DlvSampleDate | old_dlv_sample_date | 交样日期 | datetime | 是 | DateTimeField |
| TakeFabStatus | old_take_fab_status | 带纱状态 | varchar；字节长度 1 | 是 | CharField |
| IsSampleCharge | old_is_sample_charge | 是否收费 | bit | 是 | BooleanField |
| Linker | old_linker | 联系人 | varchar；字节长度 10 | 是 | CharField |
| LinkerInfo | old_linker_info | 联系信息 | varchar；字节长度 100 | 是 | CharField |
| VerLight1ID | old_ver_light1_id | 主光源 | varchar；字节长度 10 | 是 | CharField |
| VerLight2ID | old_ver_light2_id | 副光源 | varchar；字节长度 10 | 是 | CharField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| NumInfo | old_num_info | 送版份数 | varchar；字节长度 50 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 50 | 是 | CharField |
| NumNO | old_num_no | 色版数 | int | 是 | IntegerField |
| KindType | old_kind_type | 打板需求 | varchar；字节长度 10 | 是 | CharField |
| Duiseluogang | old_duiseluogang | 原办选项 | varchar；字节长度 10 | 是 | CharField |
| Daipaidaban | old_daipaidaban | 待排打板 | varchar；字节长度 10 | 是 | CharField |
| Dabanpise | old_dabanpise | 打板批色 | varchar；字节长度 10 | 是 | CharField |
| CustomerCode | old_customer_code | CustomerCode | varchar；字节长度 50 | 是 | CharField |

### SourceDyeDyeProduceItem — 染色工艺与配方相关表（DyeProduceItem，待确认）

源表：`dye.DyeProduceItem`；新表：`src_dye_dyeproduceitem`；原主键：ID。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | int | 否 | IntegerField |
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| FabricKindID | old_fabric_kind_id | FabricKindID | varchar；字节长度 50 | 是 | CharField |
| PhaseID | old_phase_id | PhaseID | varchar；字节长度 50 | 是 | CharField |
| PhaseNo | old_phase_no | PhaseNo | varchar；字节长度 50 | 是 | CharField |
| Dosage | old_dosage | Dosage | decimal(10,6) | 是 | DecimalField |
| MDosage | old_mdosage | MDosage | decimal(10,6) | 是 | DecimalField |
| ColorLevel | old_color_level | ColorLevel | varchar；字节长度 50 | 是 | CharField |

### SourceDyeDyeRecipe — 染色配方

源表：`dye.DyeRecipe`；新表：`src_dye_dyerecipe`；原主键：SheetSeries。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 配方编号 | varchar；字节长度 20 | 是 | CharField |
| SheetKind | old_sheet_kind | 配方类型 | smallint | 是 | IntegerField |
| SheetType | old_sheet_type | 配方料单类别 | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 10 | 是 | CharField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 32 | 是 | CharField |
| CustomerID | old_customer_id | 客户名称 | varchar；字节长度 32 | 是 | CharField |
| SalerID | old_saler_id | 业务员 | varchar；字节长度 32 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 56 | 是 | CharField |
| ProcessID | old_process_id | 工序名称 | varchar；字节长度 250 | 是 | CharField |
| MainStuffKindID | old_main_stuff_kind_id | 染化料主料类别 | varchar；字节长度 56 | 是 | CharField |
| ColorNo | old_color_no | 任务颜色明细号 | varchar；字节长度 56 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 50 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| ColorE | old_color_e | 英文名称 | varchar；字节长度 50 | 是 | CharField |
| ColorRGB | old_color_rgb | 颜色RGB | int | 是 | IntegerField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 32 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 100 | 是 | CharField |
| L | old_l | CIE色度L值 | decimal(7,3) | 是 | DecimalField |
| A | old_a | CIE色度A值 | decimal(7,3) | 是 | DecimalField |
| B | old_b | CIE色度B值 | decimal(7,3) | 是 | DecimalField |
| OriRecipeSheetNo | old_ori_recipe_sheet_no | 原配方编号 | varchar；字节长度 56 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 128 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| Structure | old_structure | 组织 | varchar；字节长度 50 | 是 | CharField |
| ToPlace | old_to_place | 交货地址 | varchar；字节长度 500 | 是 | CharField |
| RecipePriceSource | old_recipe_price_source | 单价源 | tinyint | 是 | IntegerField |
| Cost | old_cost | 成本 | decimal(10,2) | 是 | DecimalField |
| CostUnit | old_cost_unit | 成本单位 | varchar；字节长度 1 | 是 | CharField |
| IsHaveFirstVat | old_is_have_first_vat | 是否头缸 | bit | 是 | BooleanField |
| CheckerID | old_checker_id | 检验员 | varchar；字节长度 10 | 是 | CharField |
| MakerID | old_maker_id | 复样员 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | varchar；字节长度 1 | 是 | CharField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 1000 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| ProdKindID | old_prod_kind_id | 成品类别 | varchar；字节长度 10 | 是 | CharField |
| StandRecipeNo | old_stand_recipe_no | 标准配方号 | varchar；字节长度 128 | 是 | CharField |
| ColorVersion | old_color_version | 确板号 | varchar；字节长度 20 | 是 | CharField |
| VerLight1ID | old_ver_light1_id | VerLight1ID | varchar；字节长度 20 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 200 | 是 | CharField |
| GradeID | old_grade_id | 色号等级 | varchar；字节长度 30 | 是 | CharField |
| ColorNumMark | old_color_num_mark | 色号类型 | varchar；字节长度 30 | 是 | CharField |
| DepthE | old_depth_e | DepthE | varchar；字节长度 30 | 是 | CharField |
| Revise | old_revise | 是否修改 | bit | 是 | BooleanField |
| Fluorescence | old_fluorescence | 荧光类别 | varchar；字节长度 30 | 是 | CharField |
| OriColorNo | old_ori_color_no | 原色号明细 | varchar；字节长度 50 | 是 | CharField |
| Whether | old_whether | 是否 | bit | 是 | BooleanField |
| staff | old_staff | 打办人员 | varchar；字节长度 100 | 是 | CharField |

### SourceDyeDyeRecipeDetail — 染色配方明细

源表：`dye.DyeRecipeDetail`；新表：`src_dye_dyerecipedetail`；原主键：SheetSeries, PhaseNo, StuffNo。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| PhaseNo | old_phase_no | 染程序号 | tinyint | 否 | IntegerField |
| StuffNo | old_stuff_no | 染程明细序号 | tinyint | 否 | IntegerField |
| StuffType | old_stuff_type | 染料类别 | varchar；字节长度 1 | 是 | CharField |
| StuffID | old_stuff_id | 染料名称 | varchar；字节长度 10 | 是 | CharField |
| Dosage | old_dosage | 比例 | decimal(15,6) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(16,6) | 是 | DecimalField |
| Amount | old_amount | 金额 | decimal(10,2) | 是 | DecimalField |
| RecipeUnit | old_recipe_unit | 单位 | tinyint | 是 | IntegerField |
| DetailNote | old_detail_note | DetailNote | nvarchar；字节长度 512 | 是 | CharField |
| CarryIndex | old_carry_index | CarryIndex | varchar；字节长度 20 | 是 | CharField |
| StepName | old_step_name | StepName | varchar；字节长度 50 | 是 | CharField |
| NewStuffID | old_new_stuff_id | NewStuffID | varchar；字节长度 20 | 是 | CharField |
| Describe | old_describe | Describe | varchar；字节长度 25 | 是 | CharField |

关联 `source_parent_1` → `erp_sampling.SourceDyeDyeRecipePhase`；原码 `SheetSeries, PhaseNo` → 父表原码 `SheetSeries, PhaseNo`；依据：原界面主从 DyeRecipeDetail → DyeRecipePhase。

### SourceDyeDyeRecipeJob — 染色工艺与配方相关表（DyeRecipeJob，待确认）

源表：`dye.DyeRecipeJob`；新表：`src_dye_dyerecipejob`；原主键：SheetSeries, JobSheetNo。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 否 | CharField |
| Status | old_status | 状态 | varchar；字节长度 1 | 是 | CharField |
| CurrTime | old_curr_time | 当前时间 | datetime | 是 | DateTimeField |

关联 `source_parent_1` → `erp_sampling.SourceDyeDyeRecipe`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 FinishDyeRecipeJob → FinishDyeRecipe；原界面主从 DyeRecipeJob → DyeRecipe；原界面主从 PrepareDyeRecipeJob → PrepareDyeRecipe。

### SourceDyeDyeRecipePhase — 染色配方阶段

源表：`dye.DyeRecipePhase`；新表：`src_dye_dyerecipephase`；原主键：SheetSeries, PhaseNo。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 明细流水号 | varchar；字节长度 20 | 否 | CharField |
| PhaseNo | old_phase_no | 染程序号 | tinyint | 否 | IntegerField |
| PhaseID | old_phase_id | 染程名称 | varchar；字节长度 10 | 是 | CharField |
| BathRatio | old_bath_ratio | 浴比 | decimal(6,2) | 是 | DecimalField |
| PH | old_ph | PH值 | varchar；字节长度 10 | 是 | CharField |
| ProgramID | old_program_id | 工艺编码 | varchar；字节长度 10 | 是 | CharField |
| WaterQty | old_water_qty | 水量 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Minutes | old_minutes | 分钟 | decimal(10,2) | 是 | DecimalField |
| Temperature | old_temperature | 温度 | decimal(5,1) | 是 | DecimalField |

关联 `source_parent_1` → `erp_sampling.SourceDyeDyeRecipe`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 DyeRecipePhase → DyeRecipe；原界面主从 WashDyeRecipePhaseDetail → WashDyeRecipe；原界面主从 PrepareDyeRecipePhaseDetail → PrepareDyeRecipe；原界面主从 ReworkDyeRecipePhaseDetail → ReworkDyeRecipe；原界面主从 OtherDyeRecipePhaseDetail → OtherDyeRecipe；原界面主从 StandardDyeRecipePhaseDetail → StandardDyeRecipe；原界面主从 BulkDyeRecipePhaseDetail → BulkDyeRecipe；原界面主从 FinishDyeRecipePhaseDetail → FinishDyeRecipe；原界面主从 TrialDyeRecipePhaseDetail → TrialDyeRecipe；原界面主从 DyeRecipePhaseDetail → DyeRecipe。

### SourceDyeDyeReprint — 染色工艺与配方相关表（DyeReprint，待确认）

源表：`dye.DyeReprint`；新表：`src_dye_dyereprint`；原主键：SheetSeries。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单号 | varchar；字节长度 50 | 是 | CharField |
| SheetKind | old_sheet_kind | 类型 | smallint | 是 | IntegerField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 50 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| ShiftID | old_shift_id | 班别 | varchar；字节长度 50 | 是 | CharField |
| ShiftCheckerID | old_shift_checker_id | 领班 | varchar；字节长度 50 | 是 | CharField |
| EmpID | old_emp_id | 员工名称 | varchar；字节长度 10 | 是 | CharField |
| EmpID1 | old_emp_id1 | 打样员1 | varchar；字节长度 50 | 是 | CharField |
| EmpID2 | old_emp_id2 | 打样员2 | varchar；字节长度 50 | 是 | CharField |
| EmpID3 | old_emp_id3 | 打样员3 | varchar；字节长度 50 | 是 | CharField |
| Num | old_num | Num | float | 是 | FloatField |
| Remarks | old_remarks | Remarks | varchar；字节长度 1000 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| Kind | old_kind | 类型 | tinyint | 是 | IntegerField |

### SourceDyeDyeStartDateTime — 染色工艺与配方相关表（DyeStartDateTime，待确认）

源表：`dye.DyeStartDateTime`；新表：`src_dye_dyestartdatetime`；原主键：AutoID。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| AutoID | old_auto_id | AutoID | int | 否 | IntegerField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| ProcessNo | old_process_no | ProcessNo | varchar；字节长度 10 | 是 | CharField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 32 | 是 | CharField |
| MachineID | old_machine_id | MachineID | varchar；字节长度 50 | 是 | CharField |
| PlanDate | old_plan_date | PlanDate | datetime | 是 | DateTimeField |
| JobSheetSeries | old_job_sheet_series | JobSheetSeries | varchar；字节长度 50 | 是 | CharField |
| CombineSheetNos | old_combine_sheet_nos | CombineSheetNos | varchar；字节长度 200 | 是 | CharField |

### SourceDyeLabDips — 染色工艺与配方相关表（LabDips，待确认）

源表：`dye.LabDips`；新表：`src_dye_labdips`；原主键：SheetSeries。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| SheetType | old_sheet_type | SheetType | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 10 | 是 | CharField |
| DetailCustName | old_detail_cust_name | DetailCustName | varchar；字节长度 50 | 是 | CharField |
| OrderSheetNo | old_order_sheet_no | OrderSheetNo | varchar；字节长度 20 | 是 | CharField |
| IsHurry | old_is_hurry | IsHurry | bit | 是 | BooleanField |
| IsHaveFirstVat | old_is_have_first_vat | IsHaveFirstVat | bit | 是 | BooleanField |
| GetSampleDate | old_get_sample_date | GetSampleDate | datetime | 是 | DateTimeField |
| ToBackSample | old_to_back_sample | ToBackSample | bit | 是 | BooleanField |
| DlvSampleDate | old_dlv_sample_date | DlvSampleDate | datetime | 是 | DateTimeField |
| TakeFabStatus | old_take_fab_status | TakeFabStatus | varchar；字节长度 10 | 是 | CharField |
| Linker | old_linker | Linker | varchar；字节长度 10 | 是 | CharField |
| LinkerInfo | old_linker_info | LinkerInfo | varchar；字节长度 100 | 是 | CharField |
| VerLight1ID | old_ver_light1_id | VerLight1ID | varchar；字节长度 10 | 是 | CharField |
| VerLight2ID | old_ver_light2_id | VerLight2ID | varchar；字节长度 10 | 是 | CharField |
| Width | old_width | Width | decimal(6,2) | 是 | DecimalField |
| Weight | old_weight | Weight | decimal(6,2) | 是 | DecimalField |
| SheetStatus | old_sheet_status | SheetStatus | varchar；字节长度 1 | 是 | CharField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| TotalColors | old_total_colors | TotalColors | tinyint | 是 | IntegerField |

### SourceDyePrintColorSeparate — 染色工艺与配方相关表（PrintColorSeparate，待确认）

源表：`dye.PrintColorSeparate`；新表：`src_dye_printcolorseparate`；原主键：SheetSeries。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 分色单号 | varchar；字节长度 20 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| LYSheetNo | old_lysheet_no | 来样单号 | varchar；字节长度 50 | 是 | CharField |
| LYDetailNo | old_lydetail_no | 来样明细单号 | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| DetailCustomer | old_detail_customer | 明细客户 | nvarchar；字节长度 200 | 是 | CharField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| ScreenType | old_screen_type | 网版类型 | varchar；字节长度 20 | 是 | CharField |
| OriginalNO | old_original_no | 原稿编号 | varchar；字节长度 50 | 是 | CharField |
| PrintCode | old_print_code | 花号 | varchar；字节长度 50 | 是 | CharField |
| PrintName | old_print_name | 花名 | nvarchar；字节长度 100 | 是 | CharField |
| ColorPlateCount | old_color_plate_count | 色位个数 | int | 是 | IntegerField |
| FilmPiece | old_film_piece | 菲林张数 | int | 是 | IntegerField |
| FilmSize | old_film_size | 菲林尺寸 | nvarchar；字节长度 200 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1024 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| PrintSheetNo | old_print_sheet_no | PrintSheetNo | varchar；字节长度 20 | 是 | CharField |

### SourceDyePrintColorSeparateDetail — 染色工艺与配方相关表（PrintColorSeparateDetail，待确认）

源表：`dye.PrintColorSeparateDetail`；新表：`src_dye_printcolorseparatedetail`；原主键：SheetSeries, DetailNo。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| ColorPlateID | old_color_plate_id | 色位组号 | varchar；字节长度 10 | 否 | CharField |
| ColorPlateName | old_color_plate_name | 色位名称 | nvarchar；字节长度 40 | 是 | CharField |
| Note | old_note | 备注 | nvarchar；字节长度 1024 | 是 | CharField |
| ColorCount | old_color_count | 分色个数 | int | 是 | IntegerField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |

### SourceDyePrintColorSeparateRecord — 染色工艺与配方相关表（PrintColorSeparateRecord，待确认）

源表：`dye.PrintColorSeparateRecord`；新表：`src_dye_printcolorseparaterecord`；原主键：SheetSeries, RowNo, DetailNo。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| ColorPlateID | old_color_plate_id | 色位组号 | varchar；字节长度 10 | 否 | CharField |
| RowNo | old_row_no | 行号 | varchar；字节长度 10 | 否 | CharField |
| ColorIndex | old_color_index | 分色序号 | int | 是 | IntegerField |
| NetNo | old_net_no | 网号 | varchar；字节长度 10 | 是 | CharField |
| NetKind | old_net_kind | 网别 | varchar；字节长度 10 | 是 | CharField |
| ColorName | old_color_name | 颜色名 | nvarchar；字节长度 200 | 是 | CharField |
| Rate | old_rate | 比例 | decimal(8,4) | 是 | DecimalField |
| Density | old_density | 密度 | varchar；字节长度 100 | 是 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |

关联 `source_parent_1` → `erp_sampling.SourceDyePrintColorSeparateDetail`；原码 `SheetSeries, DetailNo, ColorPlateID` → 父表原码 `SheetSeries, DetailNo, ColorPlateID`；依据：原界面主从 PrintColorSeparateRecord → PrintColorSeparateDetail。

### SourceDyePrintingTest — 质量检验与异常相关表（PrintingTest，待确认）

源表：`dye.PrintingTest`；新表：`src_dye_printingtest`；原主键：SheetSeries。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 配方单号 | varchar；字节长度 50 | 否 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| PrintCode | old_print_code | 花号 | nvarchar；字节长度 100 | 是 | CharField |
| ColorPlateCount | old_color_plate_count | 色位个数 | int | 是 | IntegerField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 20 | 是 | CharField |
| DetailCustomer | old_detail_customer | 明细客户 | nvarchar；字节长度 200 | 是 | CharField |
| BeginDate | old_begin_date | 试样开始日期 | datetime | 是 | DateTimeField |
| EndDate | old_end_date | 试样结束日期 | datetime | 是 | DateTimeField |
| Sampler | old_sampler | 试样员 | varchar；字节长度 20 | 是 | CharField |
| SkillGrade | old_skill_grade | 难易程度 | nvarchar；字节长度 100 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 512 | 是 | CharField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 10 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |

### SourceDyePrintingTestColor — 质量检验与异常相关表（PrintingTestColor，待确认）

源表：`dye.PrintingTestColor`；新表：`src_dye_printingtestcolor`；原主键：SheetSeries, WPSerialNumber, SerialNumber。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| WPSerialNumber | old_wpserial_number | 色位序号 | int | 否 | IntegerField |
| SerialNumber | old_serial_number | 颜色序号 | int | 否 | IntegerField |
| ColorID | old_color_id | 颜色编号 | varchar；字节长度 50 | 是 | CharField |
| ColorName | old_color_name | 颜色名称 | nvarchar；字节长度 100 | 是 | CharField |
| Factor | old_factor | Factor | float | 是 | FloatField |
| WaterValue | old_water_value | WaterValue | float | 是 | FloatField |
| Note | old_note | Note | nvarchar；字节长度 512 | 是 | CharField |
| IsSamePulp | old_is_same_pulp | 是否同浆 | bit | 是 | BooleanField |
| PrintCode | old_print_code | PrintCode | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_sampling.SourceDyePrintingTestDetail`；原码 `SheetSeries, WPSerialNumber` → 父表原码 `SheetSeries, WPSerialNumber`；依据：原界面主从 PrintingTestColor → PrintingTestDetail。

### SourceDyePrintingTestDetail — 质量检验与异常相关表（PrintingTestDetail，待确认）

源表：`dye.PrintingTestDetail`；新表：`src_dye_printingtestdetail`；原主键：SheetSeries, WPSerialNumber。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| WPSerialNumber | old_wpserial_number | 色位序号 | int | 否 | IntegerField |
| SampleSign | old_sample_sign | 色位标记 | nvarchar；字节长度 64 | 是 | CharField |
| MaterialType | old_material_type | 材料类型 | nvarchar；字节长度 64 | 是 | CharField |
| MachineCode | old_machine_code | 机台号 | varchar；字节长度 32 | 是 | CharField |
| Note | old_note | 备注 | nvarchar；字节长度 512 | 是 | CharField |
| MaterialName | old_material_name | 糊料 | nvarchar；字节长度 128 | 是 | CharField |
| PrintCode | old_print_code | 印花花号 | nvarchar；字节长度 100 | 是 | CharField |
| GroundColor | old_ground_color | 底色 | nvarchar；字节长度 128 | 是 | CharField |
| ColorPlateID | old_color_plate_id | 色位ID | varchar；字节长度 20 | 是 | CharField |
| ColorPlateName | old_color_plate_name | 色位名称 | nvarchar；字节长度 40 | 是 | CharField |

关联 `source_parent_1` → `erp_sampling.SourceDyePrintingTest`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 PrintingTestDetail → PrintingTest。

### SourceDyePrintingTestStuff — 质量检验与异常相关表（PrintingTestStuff，待确认）

源表：`dye.PrintingTestStuff`；新表：`src_dye_printingteststuff`；原主键：SheetSeries, WPSerialNumber, SerialNumber, DyeStuffSerialNumber。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| WPSerialNumber | old_wpserial_number | 色位序号 | int | 否 | IntegerField |
| SerialNumber | old_serial_number | 颜色序号 | int | 否 | IntegerField |
| ColorID | old_color_id | 颜色编号 | varchar；字节长度 50 | 是 | CharField |
| ColorName | old_color_name | 颜色名称 | nvarchar；字节长度 100 | 是 | CharField |
| DyeStuffSerialNumber | old_dye_stuff_serial_number | 染化料序号 | int | 否 | IntegerField |
| DyeStuffCode | old_dye_stuff_code | 染化料编号 | varchar；字节长度 50 | 是 | CharField |
| DyeStuffName | old_dye_stuff_name | 染化料名称 | nvarchar；字节长度 200 | 是 | CharField |
| Class | old_class | 类型 | nvarchar；字节长度 128 | 是 | CharField |
| Ratio | old_ratio | 比例 | float | 是 | FloatField |
| RatioUnit | old_ratio_unit | 比例单位 | nvarchar；字节长度 16 | 是 | CharField |
| Dosage | old_dosage | 领用量 | float | 是 | FloatField |
| Unit | old_unit | 领用量单位 | nvarchar；字节长度 100 | 是 | CharField |
| IsSend | old_is_send | IsSend | bit | 是 | BooleanField |
| Send | old_send | Send | nvarchar；字节长度 16 | 是 | CharField |
| DpCode | old_dp_code | DpCode | nvarchar；字节长度 32 | 是 | CharField |
| OrderColorNumber | old_order_color_number | OrderColorNumber | nvarchar；字节长度 100 | 是 | CharField |
| Note | old_note | 备注 | nvarchar；字节长度 512 | 是 | CharField |
| detail_id | old_detail_id | detail_id | varchar；字节长度 20 | 是 | CharField |
| PrintCode | old_print_code | 花号 | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_sampling.SourceDyePrintingTestColor`；原码 `SheetSeries, WPSerialNumber, SerialNumber` → 父表原码 `SheetSeries, WPSerialNumber, SerialNumber`；依据：原界面主从 PrintingTestStuff → PrintingTestColor。

### SourceDyePrintLabAttach — 染色工艺与配方相关表（PrintLabAttach，待确认）

源表：`dye.PrintLabAttach`；新表：`src_dye_printlabattach`；原主键：SheetSeries, RowNo。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| RowNo | old_row_no | RowNo | smallint | 否 | IntegerField |
| FileName | old_file_name | FileName | varchar；字节长度 100 | 是 | CharField |
| Description | old_description | Description | varchar；字节长度 100 | 是 | CharField |

### SourceDyePrintLabAtte — 染色工艺与配方相关表（PrintLabAtte，待确认）

源表：`dye.PrintLabAtte`；新表：`src_dye_printlabatte`；原主键：SheetSeries, FieldType, AtteCode。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| FieldType | old_field_type | FieldType | varchar；字节长度 20 | 否 | CharField |
| AtteCode | old_atte_code | AtteCode | varchar；字节长度 10 | 否 | CharField |
| AtteValue | old_atte_value | AtteValue | varchar；字节长度 50 | 是 | CharField |
| Description | old_description | Description | varchar；字节长度 100 | 是 | CharField |

### SourceDyePrintLabMain — 染色工艺与配方相关表（PrintLabMain，待确认）

源表：`dye.PrintLabMain`；新表：`src_dye_printlabmain`；原主键：SheetSeries。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | SalerGroupID | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| GetSampleDate | old_get_sample_date | GetSampleDate | datetime | 是 | DateTimeField |
| ToBackSample | old_to_back_sample | ToBackSample | bit | 是 | BooleanField |
| DlvSampleDate | old_dlv_sample_date | DlvSampleDate | datetime | 是 | DateTimeField |
| IsSampleCharge | old_is_sample_charge | IsSampleCharge | bit | 是 | BooleanField |
| Linker | old_linker | Linker | varchar；字节长度 10 | 是 | CharField |
| LinkerInfo | old_linker_info | LinkerInfo | varchar；字节长度 100 | 是 | CharField |
| VerLight1ID | old_ver_light1_id | VerLight1ID | varchar；字节长度 10 | 是 | CharField |
| VerLight2ID | old_ver_light2_id | VerLight2ID | varchar；字节长度 10 | 是 | CharField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 是 | CharField |
| DesignNo | old_design_no | DesignNo | varchar；字节长度 50 | 是 | CharField |
| Sets | old_sets | Sets | tinyint | 是 | IntegerField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| StrikeOffFee | old_strike_off_fee | StrikeOffFee | decimal(10,2) | 是 | DecimalField |
| ShapeSource | old_shape_source | ShapeSource | varchar；字节长度 2 | 是 | CharField |
| Film | old_film | Film | varchar；字节长度 2 | 是 | CharField |
| PrintKind | old_print_kind | PrintKind | varchar；字节长度 2 | 是 | CharField |
| PrintSampleKind | old_print_sample_kind | PrintSampleKind | varchar；字节长度 2 | 是 | CharField |
| Width | old_width | Width | decimal(6,2) | 是 | DecimalField |
| Weight | old_weight | Weight | decimal(6,2) | 是 | DecimalField |
| DifficultyID | old_difficulty_id | DifficultyID | varchar；字节长度 10 | 是 | CharField |
| ColorCards | old_color_cards | ColorCards | tinyint | 是 | IntegerField |
| RedoReasonID | old_redo_reason_id | RedoReasonID | varchar；字节长度 10 | 是 | CharField |
| IsNeedDraw | old_is_need_draw | IsNeedDraw | bit | 是 | BooleanField |
| IsNeedStrike | old_is_need_strike | IsNeedStrike | bit | 是 | BooleanField |
| AlloterID | old_alloter_id | AlloterID | varchar；字节长度 10 | 是 | CharField |
| AllotTime | old_allot_time | AllotTime | datetime | 是 | DateTimeField |
| Idea | old_idea | Idea | varchar；字节长度 -1 | 是 | TextField |
| DrawerID | old_drawer_id | DrawerID | varchar；字节长度 10 | 是 | CharField |
| DrawedTime | old_drawed_time | DrawedTime | datetime | 是 | DateTimeField |
| CheckerID | old_checker_id | CheckerID | varchar；字节长度 10 | 是 | CharField |
| CheckedTime | old_checked_time | CheckedTime | datetime | 是 | DateTimeField |
| CheckResult | old_check_result | CheckResult | varchar；字节长度 100 | 是 | CharField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 10 | 是 | CharField |
| StrikedTime | old_striked_time | StrikedTime | datetime | 是 | DateTimeField |
| SamplerID | old_sampler_id | SamplerID | varchar；字节长度 10 | 是 | CharField |
| SampleTime | old_sample_time | SampleTime | datetime | 是 | DateTimeField |
| SampledTime | old_sampled_time | SampledTime | datetime | 是 | DateTimeField |
| SampleAlloterID | old_sample_alloter_id | SampleAlloterID | varchar；字节长度 10 | 是 | CharField |
| SampleAllotTime | old_sample_allot_time | SampleAllotTime | datetime | 是 | DateTimeField |

### SourceDyePrintRecipe — 染色工艺与配方相关表（PrintRecipe，待确认）

源表：`dye.PrintRecipe`；新表：`src_dye_printrecipe`；原主键：SheetSeries。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| SheetType | old_sheet_type | SheetType | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| SheetStatus | old_sheet_status | SheetStatus | varchar；字节长度 1 | 是 | CharField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 10 | 是 | CharField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 是 | CharField |
| Cost | old_cost | Cost | decimal(10,2) | 是 | DecimalField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 10 | 是 | CharField |
| DesignNo | old_design_no | DesignNo | varchar；字节长度 50 | 是 | CharField |
| LabSheetNo | old_lab_sheet_no | LabSheetNo | varchar；字节长度 20 | 是 | CharField |
| ColorSeries | old_color_series | ColorSeries | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 20 | 是 | CharField |
| ColorE | old_color_e | ColorE | varchar；字节长度 20 | 是 | CharField |
| OriRecipeSheetNo | old_ori_recipe_sheet_no | OriRecipeSheetNo | varchar；字节长度 20 | 是 | CharField |
| Weight | old_weight | Weight | decimal(6,2) | 是 | DecimalField |
| Width | old_width | Width | decimal(6,2) | 是 | DecimalField |
| RecipePriceSource | old_recipe_price_source | RecipePriceSource | tinyint | 是 | IntegerField |
| CostUnit | old_cost_unit | CostUnit | varchar；字节长度 1 | 是 | CharField |
| CheckerID | old_checker_id | CheckerID | varchar；字节长度 10 | 是 | CharField |
| MakerID | old_maker_id | MakerID | varchar；字节长度 10 | 是 | CharField |
| DifficultyID | old_difficulty_id | DifficultyID | varchar；字节长度 10 | 是 | CharField |
| Colors | old_colors | Colors | smallint | 是 | IntegerField |
| ColorCards | old_color_cards | ColorCards | tinyint | 是 | IntegerField |

### SourceDyePrintRecipeColor — 染色工艺与配方相关表（PrintRecipeColor，待确认）

源表：`dye.PrintRecipeColor`；新表：`src_dye_printrecipecolor`；原主键：SheetSeries, SequenceNo。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SequenceNo | old_sequence_no | SequenceNo | bigint | 否 | BigIntegerField |
| ColorNo | old_color_no | ColorNo | varchar；字节长度 20 | 是 | CharField |
| PasteID | old_paste_id | PasteID | varchar；字节长度 10 | 是 | CharField |
| Dosage | old_dosage | Dosage | decimal(15,6) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |

### SourceDyePrintRecipeDetail — 染色工艺与配方相关表（PrintRecipeDetail，待确认）

源表：`dye.PrintRecipeDetail`；新表：`src_dye_printrecipedetail`；原主键：SheetSeries, SequenceNo, StuffNo。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SequenceNo | old_sequence_no | SequenceNo | bigint | 否 | BigIntegerField |
| StuffNo | old_stuff_no | StuffNo | tinyint | 否 | IntegerField |
| StuffID | old_stuff_id | StuffID | varchar；字节长度 10 | 是 | CharField |
| Dosage | old_dosage | Dosage | decimal(15,6) | 是 | DecimalField |
| Price | old_price | Price | decimal(16,6) | 是 | DecimalField |
| Amount | old_amount | Amount | decimal(10,2) | 是 | DecimalField |
| Unit | old_unit | Unit | tinyint | 是 | IntegerField |
| DetailNote | old_detail_note | DetailNote | nvarchar；字节长度 512 | 是 | CharField |

### SourceDyePTSampleRegist — 质量检验与异常相关表（PTSampleRegist，待确认）

源表：`dye.PTSampleRegist`；新表：`src_dye_ptsampleregist`；原主键：SheetSeries。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 来样单号 | varchar；字节长度 20 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| DetailCustomer | old_detail_customer | 明细客户 | nvarchar；字节长度 200 | 是 | CharField |
| PTCount | old_ptcount | 花型个数 | int | 是 | IntegerField |
| TempletType | old_templet_type | 确版方式 | varchar；字节长度 20 | 是 | CharField |
| MainLight | old_main_light | 对色主光源 | varchar；字节长度 100 | 是 | CharField |
| SecondaryLight | old_secondary_light | 对色副光源 | varchar；字节长度 100 | 是 | CharField |
| ColorMatchMethod | old_color_match_method | 对色方法 | varchar；字节长度 50 | 是 | CharField |
| QualityStandard | old_quality_standard | 质量标准 | varchar；字节长度 50 | 是 | CharField |
| TrackerID | old_tracker_id | 跟单员 | varchar；字节长度 20 | 是 | CharField |
| GetSampleDate | old_get_sample_date | 来样日期 | datetime | 是 | DateTimeField |
| DlvSampleDate | old_dlv_sample_date | 要求交样日期 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1024 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |

### SourceDyePTSampleRegistAtte — 质量检验与异常相关表（PTSampleRegistAtte，待确认）

源表：`dye.PTSampleRegistAtte`；新表：`src_dye_ptsampleregistatte`；原主键：SheetSeries, FieldType, AtteCode。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| FieldType | old_field_type | 基础数据类别 | varchar；字节长度 20 | 否 | CharField |
| AtteCode | old_atte_code | 事项代码 | varchar；字节长度 10 | 否 | CharField |
| AtteValue | old_atte_value | 事项内容 | varchar；字节长度 50 | 是 | CharField |
| Description | old_description | 描述 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_sampling.SourceDyePTSampleRegist`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 PTSampleRegistAtte → PTSampleRegist。

### SourceDyePTSampleRegistDetail — 质量检验与异常相关表（PTSampleRegistDetail，待确认）

源表：`dye.PTSampleRegistDetail`；新表：`src_dye_ptsampleregistdetail`；原主键：SheetSeries, DetailNo。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 30 | 否 | CharField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| ColorPlateCount | old_color_plate_count | 色位个数 | int | 是 | IntegerField |
| SampleKind | old_sample_kind | 来样类别 | varchar；字节长度 10 | 是 | CharField |
| SampleSource | old_sample_source | 样纱来源 | varchar；字节长度 100 | 是 | CharField |
| ScreenType | old_screen_type | 网版类型 | varchar；字节长度 20 | 是 | CharField |
| ColorMatchCategory | old_color_match_category | 配色类别 | varchar；字节长度 20 | 是 | CharField |
| ColorMatchRequire | old_color_match_require | 配色要求 | nvarchar；字节长度 200 | 是 | CharField |
| PlateCompany | old_plate_company | 制版公司 | varchar；字节长度 100 | 是 | CharField |
| PlateCount | old_plate_count | 制版份数 | int | 是 | IntegerField |

关联 `source_parent_1` → `erp_sampling.SourceDyePTSampleRegist`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 PTSampleRegistDetail → PTSampleRegist。

### SourceDyeSampleChoice — 质量检验与异常相关表（SampleChoice，待确认）

源表：`dye.SampleChoice`；新表：`src_dye_samplechoice`；原主键：SheetSeries。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| DetailCustName | old_detail_cust_name | DetailCustName | varchar；字节长度 500 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | SalerGroupID | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 10 | 是 | CharField |
| Linker | old_linker | Linker | varchar；字节长度 10 | 是 | CharField |
| LinkerInfo | old_linker_info | LinkerInfo | varchar；字节长度 100 | 是 | CharField |
| StockUnit | old_stock_unit | StockUnit | tinyint | 是 | IntegerField |
| Description | old_description | Description | varchar；字节长度 100 | 是 | CharField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |

### SourceDyeSampleIn — 质量检验与异常相关表（SampleIn，待确认）

源表：`dye.SampleIn`；新表：`src_dye_samplein`；原主键：SheetSeries。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| FactID | old_fact_id | 工厂代码 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员代码 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| SampleInKindID | old_sample_in_kind_id | 样品入库分类 | varchar；字节长度 10 | 是 | CharField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |

### SourceDyeSampleInDetail — 质量检验与异常相关表（SampleInDetail，待确认）

源表：`dye.SampleInDetail`；新表：`src_dye_sampleindetail`；原主键：DetailNo。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 20 | 否 | CharField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 10 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 20 | 是 | CharField |
| OrderNo | old_order_no | 订单号 | varchar；字节长度 20 | 是 | CharField |
| StorageUnitID | old_storage_unit_id | 仓位代码 | varchar；字节长度 10 | 是 | CharField |
| SampleKindID | old_sample_kind_id | 样品形式 | varchar；字节长度 10 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 价格 | decimal(5,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_sampling.SourceDyeSampleIn`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 SampleInDetail → SampleIn。

### SourceDyeSampleOut — 质量检验与异常相关表（SampleOut，待确认）

源表：`dye.SampleOut`；新表：`src_dye_sampleout`；原主键：SheetSeries。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员代码 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| ExpressSettleID | old_express_settle_id | 快递费结算方式 | varchar；字节长度 10 | 是 | CharField |
| ExpressCompanyID | old_express_company_id | 快递公司代码 | varchar；字节长度 10 | 是 | CharField |
| ExpressFee | old_express_fee | 快递费用 | decimal(5,2) | 是 | DecimalField |
| ExpressNo | old_express_no | 快递单号 | varchar；字节长度 50 | 是 | CharField |
| ExpressPhoneNo | old_express_phone_no | 快递收件人电话 | varchar；字节长度 50 | 是 | CharField |
| ExpressReceiver | old_express_receiver | 快递收件人 | varchar；字节长度 10 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| SampleOutKindID | old_sample_out_kind_id | 样品出库分类 | varchar；字节长度 10 | 是 | CharField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |

### SourceDyeSampleOutDetail — 质量检验与异常相关表（SampleOutDetail，待确认）

源表：`dye.SampleOutDetail`；新表：`src_dye_sampleoutdetail`；原主键：DetailNo。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单明细号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 20 | 否 | CharField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 10 | 是 | CharField |
| SampleKindID | old_sample_kind_id | 样品形式 | varchar；字节长度 10 | 是 | CharField |
| StorageUnitID | old_storage_unit_id | 仓位代码 | varchar；字节长度 10 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 价格 | decimal(5,2) | 是 | DecimalField |
| InDetailNo | old_in_detail_no | 入库明细单号 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_sampling.SourceDyeSampleOut`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 SampleOutDetail → SampleOut。

### SourceDyeSampleStockBook — 质量检验与异常相关表（SampleStockBook，待确认）

源表：`dye.SampleStockBook`；新表：`src_dye_samplestockbook`；原主键：BookNo。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| BookNo | old_book_no | BookNo | bigint | 否 | BigIntegerField |
| BookDate | old_book_date | BookDate | datetime | 是 | DateTimeField |
| BookKind | old_book_kind | BookKind | tinyint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| SampleInOutKindID | old_sample_in_out_kind_id | SampleInOutKindID | varchar；字节长度 10 | 是 | CharField |
| SampleKindID | old_sample_kind_id | SampleKindID | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 10 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | StorageUnitIDs | varchar；字节长度 100 | 是 | CharField |
| FabricID | old_fabric_id | FabricID | varchar；字节长度 10 | 是 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 20 | 是 | CharField |
| InQty | old_in_qty | InQty | decimal(10,2) | 是 | DecimalField |
| OutQty | old_out_qty | OutQty | decimal(10,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(5,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |

### SourceDyeSmpPrescriptEntry — 其他或待确认相关表（Smp_PrescriptEntry，待确认）

源表：`dye.Smp_PrescriptEntry`；新表：`src_dye_smp_prescriptentry`；原主键：FInterID, FEntryID, FParentID。

归属依据：试验/配方及样品来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FInterID | old_finter_id | FInterID | int | 否 | IntegerField |
| FEntryID | old_fentry_id | FEntryID | int | 否 | IntegerField |
| FParentID | old_fparent_id | FParentID | int | 否 | IntegerField |
| PhaseNo | old_phase_no | PhaseNo | int | 是 | IntegerField |
| StuffNo | old_stuff_no | StuffNo | int | 是 | IntegerField |
| FItemID | old_fitem_id | FItemID | int | 是 | IntegerField |
| FTechID | old_ftech_id | FTechID | int | 是 | IntegerField |
| FTechUnit | old_ftech_unit | FTechUnit | varchar；字节长度 30 | 是 | CharField |
| FRatioQty | old_fratio_qty | FRatioQty | decimal(28,10) | 是 | DecimalField |
| FRealRatioQty | old_freal_ratio_qty | FRealRatioQty | decimal(28,10) | 是 | DecimalField |
| FPrice | old_fprice | FPrice | decimal(28,10) | 是 | DecimalField |
| FAmount | old_famount | FAmount | decimal(28,10) | 是 | DecimalField |
| FCost | old_fcost | FCost | decimal(28,10) | 是 | DecimalField |
| FNote | old_fnote | FNote | varchar；字节长度 255 | 是 | CharField |
| FBomEntryID | old_fbom_entry_id | FBomEntryID | int | 是 | IntegerField |
| FCalculateID | old_fcalculate_id | FCalculateID | int | 是 | IntegerField |
| FRoutingRequest | old_frouting_request | FRoutingRequest | varchar；字节长度 200 | 是 | CharField |
| FC_SW | old_fc_sw | FC_SW | varchar；字节长度 50 | 是 | CharField |
| FC_PZYL | old_fc_pzyl | FC_PZYL | varchar；字节长度 50 | 是 | CharField |
| FC_SWater | old_fc_swater | FC_SWater | varchar；字节长度 50 | 是 | CharField |
| FC_PZYLI | old_fc_pzyli | FC_PZYLI | varchar；字节长度 50 | 是 | CharField |
| FC_PHZ | old_fc_phz | FC_PHZ | varchar；字节长度 50 | 是 | CharField |
| FC_DDL | old_fc_ddl | FC_DDL | varchar；字节长度 50 | 是 | CharField |
| FC_TIME | old_fc_time | FC_TIME | varchar；字节长度 50 | 是 | CharField |
| FC_WD | old_fc_wd | FC_WD | varchar；字节长度 50 | 是 | CharField |
| FC_SB | old_fc_sb | FC_SB | varchar；字节长度 50 | 是 | CharField |

### SourceDyeYeDye — 染色工艺与配方相关表（ye.dye，待确认）

源表：`dye.ye.dye`；新表：`src_dye_ye_dye`；原主键：TimeZoneID。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| TimeZoneID | old_time_zone_id | TimeZoneID | smallint | 否 | IntegerField |
| Name | old_name | Name | varchar；字节长度 30 | 是 | CharField |
| SunStart | old_sun_start | SunStart | datetime | 是 | DateTimeField |
| SunEnd | old_sun_end | SunEnd | datetime | 是 | DateTimeField |
| MonStart | old_mon_start | MonStart | datetime | 是 | DateTimeField |
| MonEnd | old_mon_end | MonEnd | datetime | 是 | DateTimeField |
| TuesStart | old_tues_start | TuesStart | datetime | 是 | DateTimeField |
| TuesEnd | old_tues_end | TuesEnd | datetime | 是 | DateTimeField |
| WedStart | old_wed_start | WedStart | datetime | 是 | DateTimeField |
| WedEnd | old_wed_end | WedEnd | datetime | 是 | DateTimeField |
| ThursStart | old_thurs_start | ThursStart | datetime | 是 | DateTimeField |
| ThursEnd | old_thurs_end | ThursEnd | datetime | 是 | DateTimeField |
| FriStart | old_fri_start | FriStart | datetime | 是 | DateTimeField |
| FriEnd | old_fri_end | FriEnd | datetime | 是 | DateTimeField |
| SatStart | old_sat_start | SatStart | datetime | 是 | DateTimeField |
| SatEnd | old_sat_end | SatEnd | datetime | 是 | DateTimeField |

## 生产管理

新增原表模型 101 个，原字段 2643 个。

### SourceDyeColorShiftEmp — 染色工艺与配方相关表（ColorShiftEmp，待确认）

源表：`dye.ColorShiftEmp`；新表：`src_dye_colorshiftemp`；原主键：JobSheetNo, ShiftID, EmpID, WProcessNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 否 | CharField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 10 | 否 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 10 | 否 | CharField |
| EffiRate | old_effi_rate | EffiRate | decimal(6,4) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 10 | 是 | CharField |
| WProcessNo | old_wprocess_no | WProcessNo | varchar；字节长度 20 | 否 | CharField |

### SourceDyeDPWorkQty — 生产工单与排程相关表（DP_WorkQty，待确认）

源表：`dye.DP_WorkQty`；新表：`src_dye_dp_workqty`；原主键：ID。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | varchar；字节长度 50 | 否 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 20 | 是 | CharField |
| EmpCode | old_emp_code | EmpCode | varchar；字节长度 20 | 是 | CharField |
| dtDate | old_dt_date | dtDate | varchar；字节长度 10 | 是 | CharField |
| ShiftID | old_shift_id | ShiftID | nvarchar；字节长度 64 | 是 | CharField |
| YEARS | old_years | YEARS | varchar；字节长度 7 | 是 | CharField |
| Qty | old_qty | Qty | float | 是 | FloatField |
| WorkMoney | old_work_money | WorkMoney | float | 是 | FloatField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 10 | 是 | CharField |
| TDAY | old_tday | TDAY | varchar；字节长度 10 | 是 | CharField |
| SumMoney | old_sum_money | SumMoney | float | 是 | FloatField |
| ShiftName | old_shift_name | ShiftName | varchar；字节长度 50 | 是 | CharField |

### SourceDyeEEnergyDay — 设备维护与能耗相关表（e_Energy_day，待确认）

源表：`dye.e_Energy_day`；新表：`src_dye_e_energy_day`；原主键：ID。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | bigint | 否 | BigIntegerField |
| MeterID | old_meter_id | MeterID | varchar；字节长度 20 | 是 | CharField |
| CurrDate | old_curr_date | CurrDate | datetime | 是 | DateTimeField |
| EnergyKind | old_energy_kind | EnergyKind | tinyint | 是 | IntegerField |
| BeginReadQty | old_begin_read_qty | BeginReadQty | decimal(18,2) | 是 | DecimalField |
| BeginReadTime | old_begin_read_time | BeginReadTime | datetime | 是 | DateTimeField |
| BeginUpID | old_begin_up_id | BeginUpID | bigint | 是 | BigIntegerField |
| EndReadQty | old_end_read_qty | EndReadQty | decimal(18,2) | 是 | DecimalField |
| EndReadTime | old_end_read_time | EndReadTime | datetime | 是 | DateTimeField |
| EndUpID | old_end_up_id | EndUpID | bigint | 是 | BigIntegerField |
| RealQty | old_real_qty | RealQty | decimal(18,2) | 是 | DecimalField |
| ActualQty | old_actual_qty | ActualQty | decimal(18,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| Amount | old_amount | Amount | decimal(18,2) | 是 | DecimalField |
| Day | old_day | Day | varchar；字节长度 50 | 是 | CharField |

### SourceDyeEYardMeterGether — 设备维护与能耗相关表（e_YardMeterGether，待确认）

源表：`dye.e_YardMeterGether`；新表：`src_dye_e_yardmetergether`；原主键：ID。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | 编号 | varchar；字节长度 50 | 否 | CharField |
| MachineID | old_machine_id | 机台 | varchar；字节长度 20 | 是 | CharField |
| MeterID | old_meter_id | 码表 | varchar；字节长度 10 | 是 | CharField |
| StartTime | old_start_time | 开始时间 | datetime | 是 | DateTimeField |
| EndTime | old_end_time | 结束时间 | datetime | 是 | DateTimeField |
| ReadLength | old_read_length | 读取长度 | decimal(10,2) | 是 | DecimalField |
| DoneLength | old_done_length | 已用长度 | decimal(10,2) | 是 | DecimalField |
| LastLength | old_last_length | 剩余长度 | decimal(10,2) | 是 | DecimalField |
| Status | old_status | 状态 | tinyint | 是 | IntegerField |
| JobSheetSeries | old_job_sheet_series | 工卡流水 | varchar；字节长度 20 | 是 | CharField |
| ProcessNo | old_process_no | 工序号 | tinyint | 是 | IntegerField |

### SourceDyeEmpShiftClock — 生产工单与排程相关表（EmpShiftClock，待确认）

源表：`dye.EmpShiftClock`；新表：`src_dye_empshiftclock`；原主键：EmpID, dtDate。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| EmpID | old_emp_id | EmpID | varchar；字节长度 10 | 否 | CharField |
| dtDate | old_dt_date | dtDate | date | 否 | DateField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 10 | 是 | CharField |
| BeginTime | old_begin_time | BeginTime | datetime | 是 | DateTimeField |
| EndTime | old_end_time | EndTime | datetime | 是 | DateTimeField |
| IsHoliday | old_is_holiday | IsHoliday | varchar；字节长度 10 | 是 | CharField |
| ShiftName | old_shift_name | ShiftName | varchar；字节长度 10 | 是 | CharField |
| CopyClassID | old_copy_class_id | CopyClassID | varchar；字节长度 10 | 是 | CharField |
| BeginLeaveTime | old_begin_leave_time | BeginLeaveTime | datetime | 是 | DateTimeField |
| EndLeaveTime | old_end_leave_time | EndLeaveTime | datetime | 是 | DateTimeField |
| IsLeave | old_is_leave | IsLeave | int | 是 | IntegerField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 20 | 是 | CharField |

### SourceDyeEnergyConsumption — 设备维护与能耗相关表（EnergyConsumption，待确认）

源表：`dye.EnergyConsumption`；新表：`src_dye_energyconsumption`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 日期 | datetime | 是 | DateTimeField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| StepNo | old_step_no | 节点号 | tinyint | 是 | IntegerField |
| Creater | old_creater | 制单人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 制单时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyeEnergyConsumptionDetail — 设备维护与能耗相关表（EnergyConsumptionDetail，待确认）

源表：`dye.EnergyConsumptionDetail`；新表：`src_dye_energyconsumptiondetail`；原主键：DetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | 明细号 | varchar；字节长度 36 | 否 | CharField |
| EnergyTableID | old_energy_table_id | 能源表 | varchar；字节长度 20 | 是 | CharField |
| UseQty | old_use_qty | 用量 | decimal(10,2) | 是 | DecimalField |
| LastReadQty | old_last_read_qty | 上次读数 | decimal(10,2) | 是 | DecimalField |
| ThisReadQty | old_this_read_qty | 本次读数 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(6,2) | 是 | DecimalField |
| Amount | old_amount | 金额 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeEnergyConsumption`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 EnergyConsumptionDetail → EnergyConsumption。

### SourceDyeEnergyRecords — 设备维护与能耗相关表（EnergyRecords，待确认）

源表：`dye.EnergyRecords`；新表：`src_dye_energyrecords`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 记录单号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 记录日期 | datetime | 是 | DateTimeField |
| WaterRecords | old_water_records | 水表记录 | float | 是 | FloatField |
| ElectricRecords | old_electric_records | 电表记录 | float | 是 | FloatField |
| GasRecords | old_gas_records | 气表记录 | float | 是 | FloatField |
| Value1Records | old_value1_records | Value1Records | float | 是 | FloatField |
| Value2Records | old_value2_records | Value2Records | float | 是 | FloatField |
| Value3Records | old_value3_records | Value3Records | float | 是 | FloatField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreaterDate | old_creater_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |

### SourceDyeGetClothNotice — 坯布半成品成品与仓储相关表（GetClothNotice，待确认）

源表：`dye.GetClothNotice`；新表：`src_dye_getclothnotice`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单号 | varchar；字节长度 20 | 否 | CharField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| Driver | old_driver | 收货司机 | varchar；字节长度 20 | 是 | CharField |
| LicensePlate | old_license_plate | 车牌号 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 单据状态 | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |

### SourceDyeGetClothNoticeDetail — 坯布半成品成品与仓储相关表（GetClothNoticeDetail，待确认）

源表：`dye.GetClothNoticeDetail`；新表：`src_dye_getclothnoticedetail`；原主键：DetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 20 | 否 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 20 | 是 | CharField |
| AddrDlv | old_addr_dlv | 织纱厂/地址 | varchar；字节长度 512 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 200 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| ReceivingType | old_receiving_type | 收货状态 | varchar；字节长度 20 | 是 | CharField |
| ReceivingDate | old_receiving_date | 收货时间 | datetime | 是 | DateTimeField |
| ReceivingRolls | old_receiving_rolls | 收货条数 | decimal(10,2) | 是 | DecimalField |
| ReceivingPeople | old_receiving_people | 收货人 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| ClothGetDetailNo | old_cloth_get_detail_no | 胚纱收单明细单号 | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeGetClothNotice`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 GetClothNoticeDetail → GetClothNotice。

### SourceDyeGrayReturnApply — 坯布半成品成品与仓储相关表（GrayReturnApply，待确认）

源表：`dye.GrayReturnApply`；新表：`src_dye_grayreturnapply`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 30 | 否 | CharField |
| SheetNo | old_sheet_no | 表单号 | varchar；字节长度 30 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| StepNo | old_step_no | 节点号 | tinyint | 是 | IntegerField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyeGrayReturnApplyDetail — 坯布半成品成品与仓储相关表（GrayReturnApplyDetail，待确认）

源表：`dye.GrayReturnApplyDetail`；新表：`src_dye_grayreturnapplydetail`；原主键：DetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单号 | varchar；字节长度 30 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 30 | 否 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 30 | 是 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 30 | 是 | CharField |
| InSheetNo | old_in_sheet_no | 入库单号 | varchar；字节长度 30 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 100 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |

关联 `source_parent_1` → `erp_production.SourceDyeGrayReturnApply`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 GrayReturnApplyDetail → GrayReturnApply。

### SourceDyeHSJobsheetNo — 生产工单与排程相关表（HS_JobsheetNo，待确认）

源表：`dye.HS_JobsheetNo`；新表：`src_dye_hs_jobsheetno`；原主键：SheetSeries。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 日期 | datetime | 是 | DateTimeField |
| JobsheetNo | old_jobsheet_no | 缸号 | varchar；字节长度 200 | 是 | CharField |
| HS_Code | old_hs_code | 商品报关编码 | varchar；字节长度 200 | 是 | CharField |
| DE_Ption | old_de_ption | 货物品名 | varchar；字节长度 200 | 是 | CharField |
| HS_Price | old_hs_price | 单价 | decimal(10,4) | 是 | DecimalField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |

### SourceDyeJingShaRegister — 其他或待确认相关表（JingShaRegister，待确认）

源表：`dye.JingShaRegister`；新表：`src_dye_jingsharegister`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 表单号 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | tinyint | 是 | IntegerField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 品名 | varchar；字节长度 50 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 主卡缸号 | varchar；字节长度 50 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1000 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |

### SourceDyeJingShaRegisterDetail — 其他或待确认相关表（JingShaRegisterDetail，待确认）

源表：`dye.JingShaRegisterDetail`；新表：`src_dye_jingsharegisterdetail`；原主键：DetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| Sheetseries | old_sheetseries | 表单号 | varchar；字节长度 50 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 30 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 30 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 30 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 30 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 30 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| OrderQty | old_order_qty | 订单数量 | decimal(10,2) | 是 | DecimalField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| Area | old_area | 区域 | varchar；字节长度 100 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 100 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 500 | 是 | CharField |
| CustFabricName | old_cust_fabric_name | 客户规格 | varchar；字节长度 250 | 是 | CharField |
| SumAssignedRolls | old_sum_assigned_rolls | 实际粒数 | decimal(7,2) | 是 | DecimalField |
| SumAssignedWeightQty | old_sum_assigned_weight_qty | 实际重量 | decimal(10,2) | 是 | DecimalField |
| ColorRemarks | old_color_remarks | 用途 | varchar；字节长度 500 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 1000 | 是 | CharField |
| DyeDate | old_dye_date | 络筒期 | nchar；字节长度 200 | 是 | CharField |
| OrderSheetDate | old_order_sheet_date | 落单日期 | datetime | 是 | DateTimeField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 500 | 是 | CharField |
| FenTou | old_fen_tou | FenTou | varchar；字节长度 50 | 是 | CharField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| Approver | old_approver | 审核人 | varchar；字节长度 30 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 30 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |

### SourceDyeJobAssign — 生产工单与排程相关表（JobAssign，待确认）

源表：`dye.JobAssign`；新表：`src_dye_jobassign`；原主键：SheetSeries, AssignNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| AssignNo | old_assign_no | 预配顺序号 | tinyint | 否 | IntegerField |
| AssignDate | old_assign_date | 预配日期 | datetime | 是 | DateTimeField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商 | varchar；字节长度 30 | 是 | CharField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 -1 | 是 | TextField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| Packs | old_packs | 件数 | decimal(7,2) | 是 | DecimalField |
| PCS | old_pcs | 粒/件 | int | 是 | IntegerField |
| FixedQty | old_fixed_qty | 锭重 | decimal(5,2) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 仓位 | varchar；字节长度 100 | 是 | CharField |
| RollAvgQty | old_roll_avg_qty | 平均粒长\粒重 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| IsChecked | old_is_checked | 检测 | bit | 是 | BooleanField |
| LengthQty | old_length_qty | 长度数量 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量数量 | decimal(10,2) | 是 | DecimalField |
| MachineID | old_machine_id | 机号 | varchar；字节长度 100 | 是 | CharField |
| DetailsCustomer | old_details_customer | 织厂 | nchar；字节长度 20 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 -1 | 是 | TextField |
| PreField2 | old_pre_field2 | 氨纶 | varchar；字节长度 -1 | 是 | TextField |
| PreField3 | old_pre_field3 | 针数 | varchar；字节长度 -1 | 是 | TextField |
| PreField4 | old_pre_field4 | 寸数 | varchar；字节长度 -1 | 是 | TextField |
| PreField5 | old_pre_field5 | 车架 | varchar；字节长度 -1 | 是 | TextField |
| Status | old_status | 实配状态 | tinyint | 是 | IntegerField |
| Area | old_area | 区域 | varchar；字节长度 100 | 是 | CharField |
| InSheetDate | old_in_sheet_date | 入库日期 | datetime | 是 | DateTimeField |
| Semi_Owner | old_semi_owner | 半成品所有者 | varchar；字节长度 30 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库 | varchar；字节长度 30 | 是 | CharField |
| InSheetKind | old_in_sheet_kind | 物料分类 | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | 物料颜色 | varchar；字节长度 20 | 是 | CharField |
| PurchaseOrders | old_purchase_orders | 采购单号 | varchar；字节长度 20 | 是 | CharField |
| A_A | old_a_a | 物料区域 | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | 物料等级 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeJobSheet`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 JobAssignCombined → JobSheetCombined；原界面主从 qry_OriPrintJobAssign → qry_OriPrintJobSheet；原界面主从 SaleJobAssign → SaleJobSheet；原界面主从 TwiJobAssign → TwiJobSheet；原界面主从 DPJobAssign → DPJobSheet；原界面主从 PrintJobAssign → PrintJobSheet；原界面主从 qry_OriJobAssign → qry_OriJobSheet；原界面主从 JobAssign → JobSheet。

### SourceDyeJobAtte — 生产工单与排程相关表（JobAtte，待确认）

源表：`dye.JobAtte`；新表：`src_dye_jobatte`；原主键：SheetSeries, FieldType, AtteCode。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| FieldType | old_field_type | 基础数据类别 | varchar；字节长度 20 | 否 | CharField |
| AtteCode | old_atte_code | 事项代码 | varchar；字节长度 10 | 否 | CharField |
| AtteValue | old_atte_value | 事项内容 | varchar；字节长度 500 | 是 | CharField |
| Description | old_description | 描述 | nvarchar；字节长度 1000 | 是 | CharField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| PriceUnit | old_price_unit | 单位 | tinyint | 是 | IntegerField |

关联 `source_parent_1` → `erp_production.SourceDyeJobSheet`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 JobAtteForDeal → JobSheetForDeal；原界面主从 SaleJobAtte → SaleJobSheet；原界面主从 PrintJobAtte → PrintJobSheet；原界面主从 TwiJobAtte → TwiJobSheet；原界面主从 JobAtte → JobSheet。

### SourceDyeJobColor — 染色工艺与配方相关表（JobColor，待确认）

源表：`dye.JobColor`；新表：`src_dye_jobcolor`；原主键：JobDetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| JobDetailNo | old_job_detail_no | JobDetailNo | varchar；字节长度 20 | 否 | CharField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 是 | CharField |
| FabricID | old_fabric_id | FabricID | varchar；字节长度 10 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 50 | 是 | CharField |
| Structure | old_structure | Structure | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 10 | 是 | CharField |
| ColorE | old_color_e | ColorE | varchar；字节长度 20 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 20 | 是 | CharField |
| DesignNo | old_design_no | DesignNo | varchar；字节长度 20 | 是 | CharField |
| WidthDn | old_width_dn | WidthDn | decimal(6,2) | 是 | DecimalField |
| WidthUp | old_width_up | WidthUp | decimal(6,2) | 是 | DecimalField |
| WidthKindID | old_width_kind_id | WidthKindID | varchar；字节长度 10 | 是 | CharField |
| WeightDn | old_weight_dn | WeightDn | decimal(6,2) | 是 | DecimalField |
| WeightUp | old_weight_up | WeightUp | decimal(6,2) | 是 | DecimalField |
| WeightUnit | old_weight_unit | WeightUnit | tinyint | 是 | IntegerField |
| ProdWeight | old_prod_weight | ProdWeight | decimal(6,2) | 是 | DecimalField |
| GrayRolls | old_gray_rolls | GrayRolls | decimal(7,2) | 是 | DecimalField |
| GrayQty | old_gray_qty | GrayQty | decimal(10,2) | 是 | DecimalField |
| ProdQty | old_prod_qty | ProdQty | decimal(10,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(5,2) | 是 | DecimalField |
| IsTaxPrice | old_is_tax_price | IsTaxPrice | bit | 是 | BooleanField |
| Fee | old_fee | Fee | decimal(10,2) | 是 | DecimalField |
| Amount | old_amount | Amount | decimal(10,2) | 是 | DecimalField |
| DlvQty | old_dlv_qty | DlvQty | decimal(10,2) | 是 | DecimalField |
| DlvRolls | old_dlv_rolls | DlvRolls | decimal(7,2) | 是 | DecimalField |
| DlvDate | old_dlv_date | DlvDate | datetime | 是 | DateTimeField |
| ToPlace | old_to_place | ToPlace | varchar；字节长度 50 | 是 | CharField |
| RealGrayQty | old_real_gray_qty | RealGrayQty | decimal(10,2) | 是 | DecimalField |
| RealLoss | old_real_loss | RealLoss | decimal(4,1) | 是 | DecimalField |
| RealProdQty | old_real_prod_qty | RealProdQty | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |
| RealGrayPrice | old_real_gray_price | RealGrayPrice | decimal(10,2) | 是 | DecimalField |
| RealGrayMoney | old_real_gray_money | RealGrayMoney | decimal(10,2) | 是 | DecimalField |
| RealJobPrice | old_real_job_price | RealJobPrice | decimal(10,2) | 是 | DecimalField |
| RealJobMoney | old_real_job_money | RealJobMoney | decimal(10,2) | 是 | DecimalField |
| RealProfit | old_real_profit | RealProfit | decimal(10,2) | 是 | DecimalField |
| OrderMoney | old_order_money | OrderMoney | decimal(10,2) | 是 | DecimalField |

### SourceDyeJobCombine — 生产工单与排程相关表（JobCombine，待确认）

源表：`dye.JobCombine`；新表：`src_dye_jobcombine`；原主键：SheetSeries, JobSheetNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 工卡流水 | varchar；字节长度 20 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 否 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 300 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| CombineKind | old_combine_kind | 合缸类别 | tinyint | 是 | IntegerField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 30 | 是 | CharField |
| RowNo | old_row_no | 行号 | varchar；字节长度 20 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeJobSheet`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 SaleJobCombine → SaleJobSheet；原界面主从 TwiJobCombine → TwiJobSheet；原界面主从 JobCombineForDeal → JobSheetForDeal；原界面主从 PrintJobCombine → PrintJobSheet；原界面主从 JobCardCombined → JobSheetCombined；原界面主从 JobSheetCombine → JobSheet；原界面主从 JobCombine → JobSheet。

### SourceDyeJobCombineOrder — 生产工单与排程相关表（JobCombineOrder，待确认）

源表：`dye.JobCombineOrder`；新表：`src_dye_jobcombineorder`；原主键：SheetSeries, CheckNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 工卡流水号 | varchar；字节长度 30 | 否 | CharField |
| CheckNo | old_check_no | 订单明细 | varchar；字节长度 30 | 否 | CharField |
| OrderSheetNo | old_order_sheet_no | 订单号 | varchar；字节长度 30 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 20 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 50 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 30 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 500 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| CustFabricName | old_cust_fabric_name | 客户规格 | varchar；字节长度 250 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 50 | 是 | CharField |
| ColorRemarks | old_color_remarks | 用途 | varchar；字节长度 500 | 是 | CharField |
| CustSelfNoDetail | old_cust_self_no_detail | 客单号明细 | varchar；字节长度 50 | 是 | CharField |
| OrderQty | old_order_qty | 订单数量 | decimal(10,2) | 是 | DecimalField |
| LastQty | old_last_qty | 未开卡数量 | decimal(10,2) | 是 | DecimalField |
| CombineQty | old_combine_qty | 合染数量 | decimal(10,2) | 是 | DecimalField |
| IsMasterOrder | old_is_master_order | 是否主表订单 | bit | 是 | BooleanField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeJobSheet`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 JobCombineOrder → JobSheet；原界面主从 SaleJobCombineOrder → SaleJobSheet；原界面主从 JobSheetCombinedOrder → JobSheetCombined；原界面主从 qry_OriJobCombineOrder → qry_OriJobSheet。

### SourceDyeJobExceptions — 生产工单与排程相关表（JobExceptions，待确认）

源表：`dye.JobExceptions`；新表：`src_dye_jobexceptions`；原主键：SheetSeries, RowNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 否 | CharField |
| RowNo | old_row_no | RowNo | smallint | 否 | IntegerField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 10 | 是 | CharField |
| ProcessNo | old_process_no | ProcessNo | tinyint | 是 | IntegerField |
| DefectIDs | old_defect_ids | DefectIDs | varchar；字节长度 100 | 是 | CharField |
| ExceptionMessage | old_exception_message | ExceptionMessage | varchar；字节长度 200 | 是 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 50 | 是 | CharField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 10 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |

关联 `source_parent_1` → `erp_production.SourceDyeJobSheet`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 DPJobExceptions → DPJobSheet。

### SourceDyeJobGrayRecord — 坯布半成品成品与仓储相关表（JobGrayRecord，待确认）

源表：`dye.JobGrayRecord`；新表：`src_dye_jobgrayrecord`；原主键：SheetSeries, ReceSheetNo, RollNo, GrayBarCode。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 工卡流水号 | varchar；字节长度 20 | 否 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 否 | CharField |
| RollNo | old_roll_no | 箱号 | varchar；字节长度 20 | 否 | CharField |
| GrayBarCode | old_gray_bar_code | GrayBarCode | varchar；字节长度 50 | 否 | CharField |
| AssignedNo | old_assigned_no | 投疋流水 | varchar；字节长度 20 | 是 | CharField |
| BarCode | old_bar_code | 条码 | varchar；字节长度 50 | 否 | CharField |
| LengthQty | old_length_qty | 长度数量 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量数量 | decimal(10,2) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 仓位代码 | varchar；字节长度 10 | 是 | CharField |
| Status | old_status | 状态 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| GUnit | old_gunit | GUnit | tinyint | 是 | IntegerField |
| Rolls | old_rolls | 粒数 | float | 是 | FloatField |
| Kg | old_kg | 公斤 | decimal(6,2) | 是 | DecimalField |
| Pound | old_pound | 磅数 | decimal(6,2) | 是 | DecimalField |

关联 `source_parent_1` → `erp_production.SourceDyeJobSheet`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 JobGrayRecord → JobSheet；原界面主从 qry_OriJobGrayRecord → qry_OriJobSheet；原界面主从 TwiJobGrayRecord → TwiJobSheet；原界面主从 JOBGRAYRECORD1 → JobSheet；原界面主从 JobGrayRecordCombined → JobSheetCombined；原界面主从 qry_OriPrintJobGrayRecord → qry_OriPrintJobSheet；原界面主从 PrintJobGrayRecord → PrintJobSheet；原界面主从 SaleJobGrayRecord → SaleJobSheet。

### SourceDyeJobInWareEdit — 生产工单与排程相关表（JobInWareEdit，待确认）

源表：`dye.JobInWareEdit`；新表：`src_dye_jobinwareedit`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 表单号 | varchar；字节长度 36 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 30 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 40 | 是 | CharField |
| ProdID | old_prod_id | 规格 | varchar；字节长度 100 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 40 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 40 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |

### SourceDyeJobMain — 生产工单与排程相关表（JobMain，待确认）

源表：`dye.JobMain`；新表：`src_dye_jobmain`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| FactID | old_fact_id | FactID | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | SalerGroupID | varchar；字节长度 10 | 是 | CharField |
| Linker | old_linker | Linker | varchar；字节长度 10 | 是 | CharField |
| TrackerID | old_tracker_id | TrackerID | varchar；字节长度 10 | 是 | CharField |
| Loss | old_loss | Loss | decimal(4,1) | 是 | DecimalField |
| RealLoss | old_real_loss | RealLoss | decimal(4,1) | 是 | DecimalField |
| LossStr | old_loss_str | LossStr | varchar；字节长度 20 | 是 | CharField |
| PriceUnit | old_price_unit | PriceUnit | tinyint | 是 | IntegerField |
| SettleID | old_settle_id | SettleID | varchar；字节长度 10 | 是 | CharField |
| HandFeelID | old_hand_feel_id | HandFeelID | varchar；字节长度 10 | 是 | CharField |
| VerLight1ID | old_ver_light1_id | VerLight1ID | varchar；字节长度 10 | 是 | CharField |
| VerLight2ID | old_ver_light2_id | VerLight2ID | varchar；字节长度 100 | 是 | CharField |
| SumDlvQty | old_sum_dlv_qty | SumDlvQty | decimal(10,2) | 是 | DecimalField |
| SumDlvRolls | old_sum_dlv_rolls | SumDlvRolls | decimal(7,2) | 是 | DecimalField |
| DlvMannerID | old_dlv_manner_id | DlvMannerID | varchar；字节长度 10 | 是 | CharField |
| ProductionID | old_production_id | ProductionID | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| CloseTime | old_close_time | CloseTime | datetime | 是 | DateTimeField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| LabelID | old_label_id | LabelID | varchar；字节长度 20 | 是 | CharField |

### SourceDyeJobOutWareEdit — 生产工单与排程相关表（JobOutWareEdit，待确认）

源表：`dye.JobOutWareEdit`；新表：`src_dye_joboutwareedit`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 表单号 | varchar；字节长度 36 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| InWareSheetNo | old_in_ware_sheet_no | 进仓登记号 | varchar；字节长度 40 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 30 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 40 | 是 | CharField |
| ProdID | old_prod_id | 规格 | varchar；字节长度 100 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 40 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 40 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |

### SourceDyeJobPreRegist — 生产工单与排程相关表（JobPreRegist，待确认）

源表：`dye.JobPreRegist`；新表：`src_dye_jobpreregist`；原主键：SheetSeries, JobSheetNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 工卡流水 | varchar；字节长度 50 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 20 | 否 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeJobSheet`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 DPJobPreRegist → DPJobSheet。

### SourceDyeJobProcess — 计划工序

源表：`dye.JobProcess`；新表：`src_dye_jobprocess`；原主键：SheetSeries, ProcessNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水 | varchar；字节长度 20 | 否 | CharField |
| ProcessNo | old_process_no | 序号 | tinyint | 否 | IntegerField |
| ProcessID | old_process_id | 工序 | varchar；字节长度 10 | 是 | CharField |
| StationID | old_station_id | 站别 | varchar；字节长度 10 | 是 | CharField |
| PPName01 | old_ppname01 | 参数名1 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue01 | old_theory_value01 | 设置值1 | varchar；字节长度 20 | 是 | CharField |
| ActualValue01 | old_actual_value01 | ActualValue01 | varchar；字节长度 20 | 是 | CharField |
| PPName02 | old_ppname02 | 参数名2 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue02 | old_theory_value02 | 设置值2 | varchar；字节长度 20 | 是 | CharField |
| ActualValue02 | old_actual_value02 | ActualValue02 | varchar；字节长度 20 | 是 | CharField |
| PPName03 | old_ppname03 | 参数名3 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue03 | old_theory_value03 | 设置值3 | varchar；字节长度 20 | 是 | CharField |
| ActualValue03 | old_actual_value03 | ActualValue03 | varchar；字节长度 20 | 是 | CharField |
| PPName04 | old_ppname04 | 参数名4 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue04 | old_theory_value04 | 设置值4 | varchar；字节长度 20 | 是 | CharField |
| ActualValue04 | old_actual_value04 | ActualValue04 | varchar；字节长度 20 | 是 | CharField |
| PPName05 | old_ppname05 | 参数名5 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue05 | old_theory_value05 | 设置值5 | varchar；字节长度 20 | 是 | CharField |
| ActualValue05 | old_actual_value05 | ActualValue05 | varchar；字节长度 20 | 是 | CharField |
| PPName06 | old_ppname06 | 参数名6 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue06 | old_theory_value06 | 设置值6 | varchar；字节长度 20 | 是 | CharField |
| ActualValue06 | old_actual_value06 | ActualValue06 | varchar；字节长度 20 | 是 | CharField |
| PPName07 | old_ppname07 | 参数名7 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue07 | old_theory_value07 | 设置值7 | varchar；字节长度 20 | 是 | CharField |
| ActualValue07 | old_actual_value07 | ActualValue07 | varchar；字节长度 20 | 是 | CharField |
| PPName08 | old_ppname08 | 参数名8 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue08 | old_theory_value08 | 设置值8 | varchar；字节长度 20 | 是 | CharField |
| ActualValue08 | old_actual_value08 | ActualValue08 | varchar；字节长度 20 | 是 | CharField |
| PPName09 | old_ppname09 | 参数名9 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue09 | old_theory_value09 | 设置值9 | varchar；字节长度 20 | 是 | CharField |
| ActualValue09 | old_actual_value09 | ActualValue09 | varchar；字节长度 20 | 是 | CharField |
| PPName10 | old_ppname10 | 参数名10 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue10 | old_theory_value10 | 设置值10 | varchar；字节长度 20 | 是 | CharField |
| ActualValue10 | old_actual_value10 | ActualValue10 | varchar；字节长度 20 | 是 | CharField |
| PPName11 | old_ppname11 | 参数名11 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue11 | old_theory_value11 | 设置值11 | varchar；字节长度 20 | 是 | CharField |
| ActualValue11 | old_actual_value11 | ActualValue11 | varchar；字节长度 20 | 是 | CharField |
| PPName12 | old_ppname12 | 参数名12 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue12 | old_theory_value12 | 设置值12 | varchar；字节长度 20 | 是 | CharField |
| ActualValue12 | old_actual_value12 | ActualValue12 | varchar；字节长度 20 | 是 | CharField |
| PPName13 | old_ppname13 | 参数名13 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue13 | old_theory_value13 | 设置值13 | varchar；字节长度 100 | 是 | CharField |
| ActualValue13 | old_actual_value13 | ActualValue13 | varchar；字节长度 20 | 是 | CharField |
| PPName14 | old_ppname14 | 参数名14 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue14 | old_theory_value14 | 设置值14 | varchar；字节长度 500 | 是 | CharField |
| ActualValue14 | old_actual_value14 | ActualValue14 | varchar；字节长度 20 | 是 | CharField |
| PPName15 | old_ppname15 | 参数名15 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue15 | old_theory_value15 | 设置值15 | varchar；字节长度 20 | 是 | CharField |
| ActualValue15 | old_actual_value15 | ActualValue15 | varchar；字节长度 20 | 是 | CharField |
| PPName16 | old_ppname16 | 参数名16 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue16 | old_theory_value16 | 设置值16 | varchar；字节长度 20 | 是 | CharField |
| ActualValue16 | old_actual_value16 | ActualValue16 | varchar；字节长度 20 | 是 | CharField |
| PPName17 | old_ppname17 | 参数名17 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue17 | old_theory_value17 | 设置值17 | varchar；字节长度 20 | 是 | CharField |
| ActualValue17 | old_actual_value17 | ActualValue17 | varchar；字节长度 20 | 是 | CharField |
| PPName18 | old_ppname18 | 参数名18 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue18 | old_theory_value18 | 设置值18 | varchar；字节长度 20 | 是 | CharField |
| ActualValue18 | old_actual_value18 | ActualValue18 | varchar；字节长度 20 | 是 | CharField |
| PPName19 | old_ppname19 | 参数名19 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue19 | old_theory_value19 | 设置值19 | varchar；字节长度 20 | 是 | CharField |
| ActualValue19 | old_actual_value19 | ActualValue19 | varchar；字节长度 20 | 是 | CharField |
| PPName20 | old_ppname20 | 参数名20 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue20 | old_theory_value20 | 设置值20 | varchar；字节长度 20 | 是 | CharField |
| ActualValue20 | old_actual_value20 | ActualValue20 | varchar；字节长度 20 | 是 | CharField |
| MachineID | old_machine_id | 机台 | varchar；字节长度 10 | 是 | CharField |
| VehicleNo | old_vehicle_no | 车号 | varchar；字节长度 100 | 是 | CharField |
| StartTime | old_start_time | 开始时间 | datetime | 是 | DateTimeField |
| EndTime | old_end_time | 结束时间 | datetime | 是 | DateTimeField |
| WProcessNo | old_wprocess_no | 刷卡记录号 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Status | old_status | 状态 | varchar；字节长度 2 | 是 | CharField |
| Flag | old_flag | 标记 | tinyint | 是 | IntegerField |
| Place | old_place | 车位 | varchar；字节长度 100 | 是 | CharField |
| LastTime | old_last_time | LastTime | smallint | 是 | IntegerField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| PPPName01 | old_pppname01 | 幅宽 | varchar；字节长度 20 | 是 | CharField |
| PValue01 | old_pvalue01 | PValue01 | varchar；字节长度 20 | 是 | CharField |
| PPPName02 | old_pppname02 | PPPName02 | varchar；字节长度 20 | 是 | CharField |
| PValue02 | old_pvalue02 | PValue02 | varchar；字节长度 20 | 是 | CharField |
| PPPName03 | old_pppname03 | PPPName03 | varchar；字节长度 20 | 是 | CharField |
| PValue03 | old_pvalue03 | PValue03 | varchar；字节长度 20 | 是 | CharField |
| PPPName04 | old_pppname04 | PPPName04 | varchar；字节长度 20 | 是 | CharField |
| PValue04 | old_pvalue04 | PValue04 | varchar；字节长度 20 | 是 | CharField |
| PPPName05 | old_pppname05 | PPPName05 | varchar；字节长度 20 | 是 | CharField |
| PValue05 | old_pvalue05 | PValue05 | varchar；字节长度 20 | 是 | CharField |
| PPPName06 | old_pppname06 | PPPName06 | varchar；字节长度 20 | 是 | CharField |
| PValue06 | old_pvalue06 | PValue06 | varchar；字节长度 20 | 是 | CharField |
| PPPName07 | old_pppname07 | PPPName07 | varchar；字节长度 20 | 是 | CharField |
| PValue07 | old_pvalue07 | PValue07 | varchar；字节长度 20 | 是 | CharField |
| PPPName08 | old_pppname08 | PPPName08 | varchar；字节长度 20 | 是 | CharField |
| PValue08 | old_pvalue08 | PValue08 | varchar；字节长度 20 | 是 | CharField |
| PPPName09 | old_pppname09 | PPPName09 | varchar；字节长度 20 | 是 | CharField |
| PValue09 | old_pvalue09 | PValue09 | varchar；字节长度 20 | 是 | CharField |
| PPPName10 | old_pppname10 | PPPName10 | varchar；字节长度 20 | 是 | CharField |
| PValue10 | old_pvalue10 | PValue10 | varchar；字节长度 20 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| SignedDate | old_signed_date | SignedDate | datetime | 是 | DateTimeField |
| Signer | old_signer | Signer | varchar；字节长度 10 | 是 | CharField |
| OriJobSheetNo | old_ori_job_sheet_no | OriJobSheetNo | varchar；字节长度 20 | 是 | CharField |
| PPPName11 | old_pppname11 | PPPName11 | varchar；字节长度 20 | 是 | CharField |
| PValue11 | old_pvalue11 | PValue11 | varchar；字节长度 20 | 是 | CharField |
| PPPName12 | old_pppname12 | PPPName12 | varchar；字节长度 20 | 是 | CharField |
| PValue12 | old_pvalue12 | PValue12 | varchar；字节长度 20 | 是 | CharField |
| PPPName13 | old_pppname13 | PPPName13 | varchar；字节长度 20 | 是 | CharField |
| PValue13 | old_pvalue13 | PValue13 | varchar；字节长度 20 | 是 | CharField |
| PPPName14 | old_pppname14 | PPPName14 | varchar；字节长度 20 | 是 | CharField |
| PValue14 | old_pvalue14 | PValue14 | varchar；字节长度 20 | 是 | CharField |
| PPPName15 | old_pppname15 | PPPName15 | varchar；字节长度 20 | 是 | CharField |
| PValue15 | old_pvalue15 | PValue15 | varchar；字节长度 20 | 是 | CharField |
| PPPName16 | old_pppname16 | PPPName16 | varchar；字节长度 20 | 是 | CharField |
| PValue16 | old_pvalue16 | PValue16 | varchar；字节长度 20 | 是 | CharField |
| PPPName17 | old_pppname17 | PPPName17 | varchar；字节长度 20 | 是 | CharField |
| PValue17 | old_pvalue17 | PValue17 | varchar；字节长度 20 | 是 | CharField |
| PPPName18 | old_pppname18 | PPPName18 | varchar；字节长度 20 | 是 | CharField |
| PValue18 | old_pvalue18 | PValue18 | varchar；字节长度 20 | 是 | CharField |
| PPPName19 | old_pppname19 | PPPName19 | varchar；字节长度 20 | 是 | CharField |
| PValue19 | old_pvalue19 | PValue19 | varchar；字节长度 20 | 是 | CharField |
| PPPName20 | old_pppname20 | PPPName20 | varchar；字节长度 20 | 是 | CharField |
| PValue20 | old_pvalue20 | PValue20 | varchar；字节长度 20 | 是 | CharField |
| PPName21 | old_ppname21 | PPName21 | varchar；字节长度 20 | 是 | CharField |
| PPName22 | old_ppname22 | PPName22 | varchar；字节长度 20 | 是 | CharField |
| PPName23 | old_ppname23 | PPName23 | varchar；字节长度 20 | 是 | CharField |
| PPName24 | old_ppname24 | PPName24 | varchar；字节长度 20 | 是 | CharField |
| PPName25 | old_ppname25 | PPName25 | varchar；字节长度 20 | 是 | CharField |
| PPName26 | old_ppname26 | PPName26 | varchar；字节长度 20 | 是 | CharField |
| PPName27 | old_ppname27 | PPName27 | varchar；字节长度 20 | 是 | CharField |
| PPName28 | old_ppname28 | PPName28 | varchar；字节长度 20 | 是 | CharField |
| PPName29 | old_ppname29 | PPName29 | varchar；字节长度 20 | 是 | CharField |
| PPName30 | old_ppname30 | PPName30 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue21 | old_theory_value21 | TheoryValue21 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue22 | old_theory_value22 | TheoryValue22 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue23 | old_theory_value23 | TheoryValue23 | varchar；字节长度 100 | 是 | CharField |
| TheoryValue24 | old_theory_value24 | TheoryValue24 | varchar；字节长度 500 | 是 | CharField |
| TheoryValue25 | old_theory_value25 | TheoryValue25 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue26 | old_theory_value26 | TheoryValue26 | varchar；字节长度 26 | 是 | CharField |
| TheoryValue27 | old_theory_value27 | TheoryValue27 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue28 | old_theory_value28 | TheoryValue28 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue29 | old_theory_value29 | TheoryValue29 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue30 | old_theory_value30 | TheoryValue30 | varchar；字节长度 20 | 是 | CharField |
| ActualValue21 | old_actual_value21 | ActualValue21 | varchar；字节长度 20 | 是 | CharField |
| ActualValue22 | old_actual_value22 | ActualValue22 | varchar；字节长度 20 | 是 | CharField |
| ActualValue23 | old_actual_value23 | ActualValue23 | varchar；字节长度 20 | 是 | CharField |
| ActualValue24 | old_actual_value24 | ActualValue24 | varchar；字节长度 20 | 是 | CharField |
| ActualValue25 | old_actual_value25 | ActualValue25 | varchar；字节长度 20 | 是 | CharField |
| ActualValue26 | old_actual_value26 | ActualValue26 | varchar；字节长度 20 | 是 | CharField |
| ActualValue27 | old_actual_value27 | ActualValue27 | varchar；字节长度 20 | 是 | CharField |
| ActualValue28 | old_actual_value28 | ActualValue28 | varchar；字节长度 20 | 是 | CharField |
| ActualValue29 | old_actual_value29 | ActualValue29 | varchar；字节长度 20 | 是 | CharField |
| ActualValue30 | old_actual_value30 | ActualValue30 | varchar；字节长度 20 | 是 | CharField |
| CraftParam | old_craft_param | 工艺参数 | varchar；字节长度 100 | 是 | CharField |
| IsODM | old_is_odm | IsODM | bit | 是 | BooleanField |
| WPWorker | old_wpworker | WPWorker | varchar；字节长度 100 | 是 | CharField |
| CurveIDs | old_curve_ids | CurveIDs | varchar；字节长度 50 | 是 | CharField |
| CombineSheetNos | old_combine_sheet_nos | CombineSheetNos | varchar；字节长度 150 | 是 | CharField |
| RecipeSeries | old_recipe_series | RecipeSeries | varchar；字节长度 50 | 是 | CharField |
| CraftCheck | old_craft_check | CraftCheck | bit | 是 | BooleanField |
| CraftChecker | old_craft_checker | CraftChecker | varchar；字节长度 10 | 是 | CharField |
| CraftCheckTime | old_craft_check_time | CraftCheckTime | datetime | 是 | DateTimeField |
| DefectIDs | old_defect_ids | DefectIDs | varchar；字节长度 100 | 是 | CharField |
| DefectApproveDate | old_defect_approve_date | DefectApproveDate | datetime | 是 | DateTimeField |
| MainProcessID | old_main_process_id | MainProcessID | varchar；字节长度 50 | 是 | CharField |
| AreaID | old_area_id | AreaID | varchar；字节长度 50 | 是 | CharField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 50 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| ColorMatching | old_color_matching | ColorMatching | nvarchar；字节长度 40 | 是 | CharField |
| Reason | old_reason | 更改/添加 原因 | nvarchar；字节长度 1042 | 是 | CharField |
| Stereotypes | old_stereotypes | 定型次数 | int | 是 | IntegerField |
| TeamName | old_team_name | TeamName | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeJobSheet`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 JobProcessForDeal → JobSheetForDeal；原界面主从 DPJobProcess → DPJobSheet；原界面主从 PrintJobProcess → PrintJobSheet；原界面主从 JobProcess → JobSheet；原界面主从 SaleJobProcess → SaleJobSheet；原界面主从 TwiJobProcess → TwiJobSheet。

### SourceDyeJobProcessPre — 染色工艺与配方相关表（JobProcessPre，待确认）

源表：`dye.JobProcessPre`；新表：`src_dye_jobprocesspre`；原主键：SheetSeries, ProcessNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| ProcessNo | old_process_no | 工序号 | tinyint | 否 | IntegerField |
| ProcessID | old_process_id | 工序代码 | varchar；字节长度 10 | 是 | CharField |
| StationID | old_station_id | 站别代码 | varchar；字节长度 10 | 是 | CharField |
| Price | old_price | Price | decimal(10,4) | 是 | DecimalField |
| MachineID | old_machine_id | 机台号 | varchar；字节长度 10 | 是 | CharField |
| CurveIDs | old_curve_ids | CurveIDs | varchar；字节长度 50 | 是 | CharField |
| VehicleNo | old_vehicle_no | 纱车号 | varchar；字节长度 100 | 是 | CharField |
| Place | old_place | Place | varchar；字节长度 100 | 是 | CharField |
| OriJobSheetNo | old_ori_job_sheet_no | OriJobSheetNo | varchar；字节长度 20 | 是 | CharField |
| PPPName01 | old_pppname01 | PPPName01 | varchar；字节长度 20 | 是 | CharField |
| PValue01 | old_pvalue01 | PValue01 | varchar；字节长度 20 | 是 | CharField |
| PPPName02 | old_pppname02 | PPPName02 | varchar；字节长度 20 | 是 | CharField |
| PValue02 | old_pvalue02 | PValue02 | varchar；字节长度 20 | 是 | CharField |
| PPPName03 | old_pppname03 | PPPName03 | varchar；字节长度 20 | 是 | CharField |
| PValue03 | old_pvalue03 | PValue03 | varchar；字节长度 20 | 是 | CharField |
| PPPName04 | old_pppname04 | PPPName04 | varchar；字节长度 20 | 是 | CharField |
| PValue04 | old_pvalue04 | PValue04 | varchar；字节长度 20 | 是 | CharField |
| PPPName05 | old_pppname05 | PPPName05 | varchar；字节长度 20 | 是 | CharField |
| PValue05 | old_pvalue05 | PValue05 | varchar；字节长度 20 | 是 | CharField |
| PPPName06 | old_pppname06 | PPPName06 | varchar；字节长度 20 | 是 | CharField |
| PValue06 | old_pvalue06 | PValue06 | varchar；字节长度 20 | 是 | CharField |
| PPPName07 | old_pppname07 | PPPName07 | varchar；字节长度 20 | 是 | CharField |
| PValue07 | old_pvalue07 | PValue07 | varchar；字节长度 20 | 是 | CharField |
| PPPName08 | old_pppname08 | PPPName08 | varchar；字节长度 20 | 是 | CharField |
| PValue08 | old_pvalue08 | PValue08 | varchar；字节长度 20 | 是 | CharField |
| PPPName09 | old_pppname09 | PPPName09 | varchar；字节长度 20 | 是 | CharField |
| PValue09 | old_pvalue09 | PValue09 | varchar；字节长度 20 | 是 | CharField |
| PPPName10 | old_pppname10 | PPPName10 | varchar；字节长度 20 | 是 | CharField |
| PValue10 | old_pvalue10 | PValue10 | varchar；字节长度 20 | 是 | CharField |
| PPPName11 | old_pppname11 | PPPName11 | varchar；字节长度 20 | 是 | CharField |
| PValue11 | old_pvalue11 | PValue11 | varchar；字节长度 20 | 是 | CharField |
| PPPName12 | old_pppname12 | PPPName12 | varchar；字节长度 20 | 是 | CharField |
| PValue12 | old_pvalue12 | PValue12 | varchar；字节长度 20 | 是 | CharField |
| PPPName13 | old_pppname13 | PPPName13 | varchar；字节长度 20 | 是 | CharField |
| PValue13 | old_pvalue13 | PValue13 | varchar；字节长度 20 | 是 | CharField |
| PPPName14 | old_pppname14 | PPPName14 | varchar；字节长度 20 | 是 | CharField |
| PValue14 | old_pvalue14 | PValue14 | varchar；字节长度 20 | 是 | CharField |
| PPPName15 | old_pppname15 | PPPName15 | varchar；字节长度 20 | 是 | CharField |
| PValue15 | old_pvalue15 | PValue15 | varchar；字节长度 20 | 是 | CharField |
| PPPName16 | old_pppname16 | PPPName16 | varchar；字节长度 20 | 是 | CharField |
| PValue16 | old_pvalue16 | PValue16 | varchar；字节长度 20 | 是 | CharField |
| PPPName17 | old_pppname17 | PPPName17 | varchar；字节长度 20 | 是 | CharField |
| PValue17 | old_pvalue17 | PValue17 | varchar；字节长度 20 | 是 | CharField |
| PPPName18 | old_pppname18 | PPPName18 | varchar；字节长度 20 | 是 | CharField |
| PValue18 | old_pvalue18 | PValue18 | varchar；字节长度 20 | 是 | CharField |
| PPPName19 | old_pppname19 | PPPName19 | varchar；字节长度 20 | 是 | CharField |
| PValue19 | old_pvalue19 | PValue19 | varchar；字节长度 20 | 是 | CharField |
| PPPName20 | old_pppname20 | PPPName20 | varchar；字节长度 20 | 是 | CharField |
| PValue20 | old_pvalue20 | PValue20 | varchar；字节长度 20 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| PPName01 | old_ppname01 | 参数名1 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue01 | old_theory_value01 | 设置值1 | varchar；字节长度 20 | 是 | CharField |
| ActualValue01 | old_actual_value01 | ActualValue01 | varchar；字节长度 50 | 是 | CharField |
| PPName02 | old_ppname02 | 参数名2 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue02 | old_theory_value02 | 设置值2 | varchar；字节长度 20 | 是 | CharField |
| ActualValue02 | old_actual_value02 | ActualValue02 | varchar；字节长度 50 | 是 | CharField |
| PPName03 | old_ppname03 | 参数名3 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue03 | old_theory_value03 | 设置值3 | varchar；字节长度 20 | 是 | CharField |
| ActualValue03 | old_actual_value03 | ActualValue03 | varchar；字节长度 500 | 是 | CharField |
| PPName04 | old_ppname04 | 参数名4 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue04 | old_theory_value04 | 设置值4 | varchar；字节长度 20 | 是 | CharField |
| ActualValue04 | old_actual_value04 | ActualValue04 | varchar；字节长度 50 | 是 | CharField |
| PPName05 | old_ppname05 | 参数名5 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue05 | old_theory_value05 | 设置值5 | varchar；字节长度 20 | 是 | CharField |
| ActualValue05 | old_actual_value05 | ActualValue05 | varchar；字节长度 50 | 是 | CharField |
| PPName06 | old_ppname06 | 参数名6 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue06 | old_theory_value06 | 设置值6 | varchar；字节长度 20 | 是 | CharField |
| ActualValue06 | old_actual_value06 | ActualValue06 | varchar；字节长度 50 | 是 | CharField |
| PPName07 | old_ppname07 | 参数名7 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue07 | old_theory_value07 | 设置值7 | varchar；字节长度 20 | 是 | CharField |
| ActualValue07 | old_actual_value07 | ActualValue07 | varchar；字节长度 50 | 是 | CharField |
| PPName08 | old_ppname08 | 参数名8 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue08 | old_theory_value08 | 设置值8 | varchar；字节长度 20 | 是 | CharField |
| ActualValue08 | old_actual_value08 | ActualValue08 | varchar；字节长度 50 | 是 | CharField |
| PPName09 | old_ppname09 | 参数名9 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue09 | old_theory_value09 | 设置值9 | varchar；字节长度 20 | 是 | CharField |
| ActualValue09 | old_actual_value09 | ActualValue09 | varchar；字节长度 50 | 是 | CharField |
| PPName10 | old_ppname10 | 参数名10 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue10 | old_theory_value10 | 设置值10 | varchar；字节长度 20 | 是 | CharField |
| ActualValue10 | old_actual_value10 | ActualValue10 | varchar；字节长度 50 | 是 | CharField |
| PPName11 | old_ppname11 | 参数名11 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue11 | old_theory_value11 | 设置值11 | varchar；字节长度 20 | 是 | CharField |
| ActualValue11 | old_actual_value11 | ActualValue11 | varchar；字节长度 50 | 是 | CharField |
| PPName12 | old_ppname12 | 参数名12 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue12 | old_theory_value12 | 设置值12 | varchar；字节长度 20 | 是 | CharField |
| ActualValue12 | old_actual_value12 | ActualValue12 | varchar；字节长度 50 | 是 | CharField |
| PPName13 | old_ppname13 | 参数名13 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue13 | old_theory_value13 | 设置值13 | varchar；字节长度 20 | 是 | CharField |
| ActualValue13 | old_actual_value13 | ActualValue13 | varchar；字节长度 50 | 是 | CharField |
| PPName14 | old_ppname14 | 参数名14 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue14 | old_theory_value14 | 设置值14 | varchar；字节长度 20 | 是 | CharField |
| ActualValue14 | old_actual_value14 | ActualValue14 | varchar；字节长度 50 | 是 | CharField |
| PPName15 | old_ppname15 | 参数名15 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue15 | old_theory_value15 | 设置值15 | varchar；字节长度 20 | 是 | CharField |
| ActualValue15 | old_actual_value15 | ActualValue15 | varchar；字节长度 50 | 是 | CharField |
| PPName16 | old_ppname16 | 参数名16 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue16 | old_theory_value16 | 设置值16 | varchar；字节长度 20 | 是 | CharField |
| ActualValue16 | old_actual_value16 | ActualValue16 | varchar；字节长度 50 | 是 | CharField |
| PPName17 | old_ppname17 | 参数名17 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue17 | old_theory_value17 | 设置值17 | varchar；字节长度 20 | 是 | CharField |
| ActualValue17 | old_actual_value17 | ActualValue17 | varchar；字节长度 50 | 是 | CharField |
| PPName18 | old_ppname18 | 参数名18 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue18 | old_theory_value18 | 设置值18 | varchar；字节长度 20 | 是 | CharField |
| ActualValue18 | old_actual_value18 | ActualValue18 | varchar；字节长度 50 | 是 | CharField |
| PPName19 | old_ppname19 | 参数名19 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue19 | old_theory_value19 | 设置值19 | varchar；字节长度 20 | 是 | CharField |
| ActualValue19 | old_actual_value19 | ActualValue19 | varchar；字节长度 50 | 是 | CharField |
| PPName20 | old_ppname20 | 参数名20 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue20 | old_theory_value20 | 设置值20 | varchar；字节长度 20 | 是 | CharField |
| ActualValue20 | old_actual_value20 | ActualValue20 | varchar；字节长度 50 | 是 | CharField |
| PPName21 | old_ppname21 | PPName21 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue21 | old_theory_value21 | TheoryValue21 | varchar；字节长度 20 | 是 | CharField |
| PPName22 | old_ppname22 | PPName22 | varchar；字节长度 20 | 是 | CharField |
| ActualValue21 | old_actual_value21 | ActualValue21 | varchar；字节长度 50 | 是 | CharField |
| TheoryValue22 | old_theory_value22 | TheoryValue22 | varchar；字节长度 20 | 是 | CharField |
| ActualValue22 | old_actual_value22 | ActualValue22 | varchar；字节长度 50 | 是 | CharField |
| PPName23 | old_ppname23 | PPName23 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue23 | old_theory_value23 | TheoryValue23 | varchar；字节长度 20 | 是 | CharField |
| ActualValue23 | old_actual_value23 | ActualValue23 | varchar；字节长度 50 | 是 | CharField |
| PPName24 | old_ppname24 | PPName24 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue24 | old_theory_value24 | TheoryValue24 | varchar；字节长度 20 | 是 | CharField |
| ActualValue24 | old_actual_value24 | ActualValue24 | varchar；字节长度 50 | 是 | CharField |
| PPName25 | old_ppname25 | PPName25 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue25 | old_theory_value25 | TheoryValue25 | varchar；字节长度 20 | 是 | CharField |
| ActualValue25 | old_actual_value25 | ActualValue25 | varchar；字节长度 50 | 是 | CharField |
| PPName26 | old_ppname26 | PPName26 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue26 | old_theory_value26 | TheoryValue26 | varchar；字节长度 26 | 是 | CharField |
| ActualValue26 | old_actual_value26 | ActualValue26 | varchar；字节长度 50 | 是 | CharField |
| PPName27 | old_ppname27 | PPName27 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue27 | old_theory_value27 | TheoryValue27 | varchar；字节长度 20 | 是 | CharField |
| ActualValue27 | old_actual_value27 | ActualValue27 | varchar；字节长度 50 | 是 | CharField |
| PPName28 | old_ppname28 | PPName28 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue28 | old_theory_value28 | TheoryValue28 | varchar；字节长度 20 | 是 | CharField |
| ActualValue28 | old_actual_value28 | ActualValue28 | varchar；字节长度 50 | 是 | CharField |
| PPName29 | old_ppname29 | PPName29 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue29 | old_theory_value29 | TheoryValue29 | varchar；字节长度 20 | 是 | CharField |
| ActualValue29 | old_actual_value29 | ActualValue29 | varchar；字节长度 50 | 是 | CharField |
| PPName30 | old_ppname30 | PPName30 | varchar；字节长度 20 | 是 | CharField |
| TheoryValue30 | old_theory_value30 | TheoryValue30 | varchar；字节长度 20 | 是 | CharField |
| CombineSheetNos | old_combine_sheet_nos | CombineSheetNos | varchar；字节长度 200 | 是 | CharField |
| ActualValue30 | old_actual_value30 | ActualValue30 | varchar；字节长度 50 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | varchar；字节长度 20 | 是 | CharField |
| SignedDate | old_signed_date | SignedDate | datetime | 是 | DateTimeField |
| Signer | old_signer | Signer | varchar；字节长度 10 | 是 | CharField |
| StartTime | old_start_time | 开始时间 | datetime | 是 | DateTimeField |
| EndTime | old_end_time | 结束时间 | datetime | 是 | DateTimeField |
| WProcessNo | old_wprocess_no | 刷卡记录号 | varchar；字节长度 20 | 是 | CharField |
| Flag | old_flag | Flag | tinyint | 是 | IntegerField |
| LastTime | old_last_time | LastTime | smallint | 是 | IntegerField |
| Status | old_status | 状态 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| IsODM | old_is_odm | IsODM | bit | 是 | BooleanField |
| RecipeSeries | old_recipe_series | RecipeSeries | varchar；字节长度 20 | 是 | CharField |
| CraftCheck | old_craft_check | CraftCheck | bit | 是 | BooleanField |
| CraftChecker | old_craft_checker | CraftChecker | varchar；字节长度 10 | 是 | CharField |
| CraftCheckTime | old_craft_check_time | CraftCheckTime | datetime | 是 | DateTimeField |
| DefectIDs | old_defect_ids | DefectIDs | varchar；字节长度 100 | 是 | CharField |
| DefectApproveDate | old_defect_approve_date | DefectApproveDate | datetime | 是 | DateTimeField |
| WPWorker | old_wpworker | WPWorker | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeJobSheet`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 SaleJobProcessPre → SaleJobSheet；原界面主从 PrintJobProcessPre → PrintJobSheet；原界面主从 TwiJobProcessPre → TwiJobSheet；原界面主从 JobProcessPre → JobSheet。

### SourceDyeJobSheet — 生产工卡/缸卡

源表：`dye.JobSheet`；新表：`src_dye_jobsheet`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 工卡号 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 开卡日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| SheetType | old_sheet_type | 工卡类型 | smallint | 是 | IntegerField |
| JobKindID | old_job_kind_id | 流程卡类别 | varchar；字节长度 10 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| BusinessKind | old_business_kind | 业务类别 | smallint | 是 | IntegerField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 150 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员 | varchar；字节长度 10 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 200 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 200 | 是 | CharField |
| Structure | old_structure | 组织 | varchar；字节长度 500 | 是 | CharField |
| ProductionID | old_production_id | 生产工艺编码 | varchar；字节长度 10 | 是 | CharField |
| Linker | old_linker | 联系人 | varchar；字节长度 10 | 是 | CharField |
| StockUnit | old_stock_unit | 单位 | tinyint | 是 | IntegerField |
| WidthKindID | old_width_kind_id | 幅宽单位 | nvarchar；字节长度 40 | 是 | CharField |
| FactID | old_fact_id | 加工商 | varchar；字节长度 10 | 是 | CharField |
| OriJobsheetNo | old_ori_jobsheet_no | 原卡号 | varchar；字节长度 20 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 10 | 是 | CharField |
| ColorE | old_color_e | 颜色英文名 | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 50 | 是 | CharField |
| DesignNo | old_design_no | 花号 | varchar；字节长度 20 | 是 | CharField |
| IsContinue | old_is_continue | 连缸 | bit | 是 | BooleanField |
| IsHurry | old_is_hurry | 加急 | bit | 是 | BooleanField |
| IsSpecColor | old_is_spec_color | 特殊颜色 | bit | 是 | BooleanField |
| IsSpecVat | old_is_spec_vat | 小缸 | bit | 是 | BooleanField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 100 | 是 | CharField |
| PreVatQty | old_pre_vat_qty | 排单数量 | decimal(10,2) | 是 | DecimalField |
| PreRolls | old_pre_rolls | 排单粒数 | decimal(7,2) | 是 | DecimalField |
| PrePacks | old_pre_packs | 排单件数 | decimal(7,2) | 是 | DecimalField |
| SumAssignedWeightQty | old_sum_assigned_weight_qty | 实发数量 | decimal(10,2) | 是 | DecimalField |
| SumAssignedRolls | old_sum_assigned_rolls | 实发粒数 | decimal(7,2) | 是 | DecimalField |
| SumAssignedPacks | old_sum_assigned_packs | 实发件数 | decimal(7,2) | 是 | DecimalField |
| SumProcessQty | old_sum_process_qty | 翻纱数量 | decimal(10,2) | 是 | DecimalField |
| VatNo | old_vat_no | 缸号 | varchar；字节长度 20 | 是 | CharField |
| DlvDate | old_dlv_date | 交期 | datetime | 是 | DateTimeField |
| FinishDate | old_finish_date | 结案日期 | datetime | 是 | DateTimeField |
| CurrProcessID | old_curr_process_id | 本道工序代码 | varchar；字节长度 50 | 是 | CharField |
| CurrProcessNo | old_curr_process_no | 本道工序号 | tinyint | 是 | IntegerField |
| CurrStationID | old_curr_station_id | 本道站别代码 | varchar；字节长度 10 | 是 | CharField |
| StartDate | old_start_date | 开始日期 | datetime | 是 | DateTimeField |
| RedoEmpID | old_redo_emp_id | 重修责任人 | varchar；字节长度 10 | 是 | CharField |
| RedoProcessID | old_redo_process_id | 重修工序 | varchar；字节长度 10 | 是 | CharField |
| RedoReasonID | old_redo_reason_id | 重修原因代码 | varchar；字节长度 500 | 是 | CharField |
| RedoShiftID | old_redo_shift_id | 重修班组 | varchar；字节长度 50 | 是 | CharField |
| WorkShopID | old_work_shop_id | 生产车间代码 | varchar；字节长度 10 | 是 | CharField |
| MachineKindID | old_machine_kind_id | 机型代码 | varchar；字节长度 10 | 是 | CharField |
| AssignUnit | old_assign_unit | 配纱方式 | tinyint | 是 | IntegerField |
| OriOrderSeries | old_ori_order_series | 订单号 | varchar；字节长度 20 | 是 | CharField |
| SumProcessRolls | old_sum_process_rolls | 工序粒数 | decimal(7,2) | 是 | DecimalField |
| LabelID | old_label_id | 标签号 | varchar；字节长度 10 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 500 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 200 | 是 | CharField |
| CraftCheck | old_craft_check | 工艺审核状态 | bit | 是 | BooleanField |
| OrderSheetNo | old_order_sheet_no | 订单号 | varchar；字节长度 20 | 是 | CharField |
| NextProcessID | old_next_process_id | 下道工序代码 | varchar；字节长度 10 | 是 | CharField |
| NextStationID | old_next_station_id | 下道站别代码 | varchar；字节长度 10 | 是 | CharField |
| ProgramID | old_program_id | 前道流程 | varchar；字节长度 10 | 是 | CharField |
| Loss | old_loss | 缩率 | varchar；字节长度 50 | 是 | CharField |
| RealLoss | old_real_loss | 实际缩率 | decimal(4,1) | 是 | DecimalField |
| AssignInfo | old_assign_info | 纱牌 | varchar；字节长度 -1 | 是 | TextField |
| StandCraftNo | old_stand_craft_no | 标准工艺 | varchar；字节长度 20 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 500 | 是 | CharField |
| IsFirstVat | old_is_first_vat | 头缸 | bit | 是 | BooleanField |
| ShippingMarkID | old_shipping_mark_id | 唛头 | varchar；字节长度 10 | 是 | CharField |
| PlanDetailNo | old_plan_detail_no | 主计划明细号码 | varchar；字节长度 30 | 是 | CharField |
| WidthDn | old_width_dn | 门幅下限 | varchar；字节长度 50 | 是 | CharField |
| WidthUp | old_width_up | 门幅上限 | varchar；字节长度 50 | 是 | CharField |
| WeightDn | old_weight_dn | 克重下限 | varchar；字节长度 50 | 是 | CharField |
| WeightUp | old_weight_up | 克重上限 | varchar；字节长度 50 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 -1 | 是 | TextField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| RelaLotNo | old_rela_lot_no | RelaLotNo | varchar；字节长度 50 | 是 | CharField |
| ColorRGB | old_color_rgb | ColorRGB | int | 是 | IntegerField |
| IsPause | old_is_pause | IsPause | bit | 是 | BooleanField |
| PrintKind | old_print_kind | PrintKind | varchar；字节长度 1 | 是 | CharField |
| ProgramKindID | old_program_kind_id | ProgramKindID | varchar；字节长度 10 | 是 | CharField |
| OriColorID | old_ori_color_id | OriColorID | varchar；字节长度 10 | 是 | CharField |
| OriColorNum | old_ori_color_num | OriColorNum | varchar；字节长度 20 | 是 | CharField |
| ConfirmSideID | old_confirm_side_id | ConfirmSideID | varchar；字节长度 10 | 是 | CharField |
| PlanDate | old_plan_date | 刷卡时间 | datetime | 是 | DateTimeField |
| MainStuffKindID | old_main_stuff_kind_id | MainStuffKindID | varchar；字节长度 10 | 是 | CharField |
| IsToLabDips | old_is_to_lab_dips | IsToLabDips | bit | 是 | BooleanField |
| RedoDefectName | old_redo_defect_name | RedoDefectName | varchar；字节长度 100 | 是 | CharField |
| MachineID | old_machine_id | 机台 | varchar；字节长度 -1 | 是 | TextField |
| LossStr | old_loss_str | LossStr | varchar；字节长度 20 | 是 | CharField |
| ProdQty | old_prod_qty | ProdQty | decimal(10,2) | 是 | DecimalField |
| GWidth | old_gwidth | 胚纱幅宽 | decimal(6,2) | 是 | DecimalField |
| GWeight | old_gweight | 胚纱克重 | decimal(6,2) | 是 | DecimalField |
| WarpDensity | old_warp_density | 经密 | varchar；字节长度 50 | 是 | CharField |
| WeftDensity | old_weft_density | 纬密 | varchar；字节长度 50 | 是 | CharField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| AddrDlv | old_addr_dlv | 送货地址 | varchar；字节长度 150 | 是 | CharField |
| WeightUnit | old_weight_unit | 克重种类 | nvarchar；字节长度 40 | 是 | CharField |
| OrderSheetDate | old_order_sheet_date | 下单日期 | datetime | 是 | DateTimeField |
| Model1 | old_model1 | 款号 | varchar；字节长度 200 | 是 | CharField |
| SumProcessLengthQty | old_sum_process_length_qty | 工序长度 | decimal(10,2) | 是 | DecimalField |
| SumProcessWeightQty | old_sum_process_weight_qty | 工序重量 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(8,2) | 是 | DecimalField |
| Code | old_code | Code | varchar；字节长度 20 | 是 | CharField |
| Code1 | old_code1 | 手感编码 | varchar；字节长度 300 | 是 | CharField |
| Weight | old_weight | 克重 | varchar；字节长度 200 | 是 | CharField |
| Width | old_width | 幅宽 | varchar；字节长度 200 | 是 | CharField |
| SumAssignedLengthQty | old_sum_assigned_length_qty | 实配长度 | decimal(10,2) | 是 | DecimalField |
| Pound | old_pound | Pound | decimal(8,2) | 是 | DecimalField |
| Kg | old_kg | Kg | decimal(8,2) | 是 | DecimalField |
| CustJobNo | old_cust_job_no | 客户缸号 | varchar；字节长度 100 | 是 | CharField |
| Sender | old_sender | 交胚人 | varchar；字节长度 50 | 是 | CharField |
| Receiver | old_receiver | 收胚人 | varchar；字节长度 50 | 是 | CharField |
| IsSplited | old_is_splited | IsSplited | smallint | 是 | IntegerField |
| WeightQty | old_weight_qty | 可入库重量 | decimal(10,2) | 是 | DecimalField |
| OriSourceJobNo | old_ori_source_job_no | 原缸号 | varchar；字节长度 50 | 是 | CharField |
| SetHurryTime | old_set_hurry_time | SetHurryTime | datetime | 是 | DateTimeField |
| SetPauseBegTime | old_set_pause_beg_time | SetPauseBegTime | datetime | 是 | DateTimeField |
| SetPauseEndTime | old_set_pause_end_time | SetPauseEndTime | datetime | 是 | DateTimeField |
| HurryInfo | old_hurry_info | HurryInfo | varchar；字节长度 512 | 是 | CharField |
| PauseInfo | old_pause_info | PauseInfo | varchar；字节长度 512 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | StorageUnitIDs | varchar；字节长度 100 | 是 | CharField |
| RollAvgQtyStr | old_roll_avg_qty_str | RollAvgQtyStr | varchar；字节长度 50 | 是 | CharField |
| IsProdInFinished | old_is_prod_in_finished | IsProdInFinished | bit | 是 | BooleanField |
| BarCode | old_bar_code | 条码 | varchar；字节长度 100 | 是 | CharField |
| PhaseID | old_phase_id | PhaseID | varchar；字节长度 10 | 是 | CharField |
| Jobattes1 | old_jobattes1 | Jobattes1 | varchar；字节长度 1000 | 是 | CharField |
| Finish | old_finish | Finish | tinyint | 是 | IntegerField |
| OriSourceJobNo2 | old_ori_source_job_no2 | OriSourceJobNo2 | varchar；字节长度 50 | 是 | CharField |
| PenetrationNO | old_penetration_no | PenetrationNO | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 20 | 是 | CharField |
| OrderQty | old_order_qty | OrderQty | decimal(8,2) | 是 | DecimalField |
| OrderQtyTotal | old_order_qty_total | OrderQtyTotal | decimal(8,2) | 是 | DecimalField |
| Customer | old_customer | Customer | varchar；字节长度 200 | 是 | CharField |
| CHECKDots | old_checkdots | CHECKDots | decimal(18,0) | 是 | DecimalField |
| Checker | old_checker | Checker | varchar；字节长度 10 | 是 | CharField |
| IsOver | old_is_over | IsOver | bit | 是 | BooleanField |
| ProdWidth | old_prod_width | ProdWidth | float | 是 | FloatField |
| ProdWeight | old_prod_weight | ProdWeight | float | 是 | FloatField |
| ProdRePeatcnt | old_prod_re_peatcnt | ProdRePeatcnt | varchar；字节长度 10 | 是 | CharField |
| ProdSkeWing | old_prod_ske_wing | ProdSkeWing | float | 是 | FloatField |
| Grade | old_grade | Grade | varchar；字节长度 10 | 是 | CharField |
| YAvgdots | old_yavgdots | YAvgdots | float | 是 | FloatField |
| PDots | old_pdots | PDots | int | 是 | IntegerField |
| PlengthQyt | old_plength_qyt | PlengthQyt | float | 是 | FloatField |
| Pkg | old_pkg | Pkg | float | 是 | FloatField |
| PRolls | old_prolls | PRolls | int | 是 | IntegerField |
| Inch | old_inch | Inch | varchar；字节长度 20 | 是 | CharField |
| FabricNO1 | old_fabric_no1 | 宝誉条码 | varchar；字节长度 200 | 是 | CharField |
| FabricNO2 | old_fabric_no2 | 任务单号 | varchar；字节长度 200 | 是 | CharField |
| FabricNO3 | old_fabric_no3 | FabricNO3 | varchar；字节长度 -1 | 是 | TextField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 10 | 是 | CharField |
| RedoDeptID | old_redo_dept_id | 责任部门 | varchar；字节长度 50 | 是 | CharField |
| PrintCode | old_print_code | 花号 | varchar；字节长度 50 | 是 | CharField |
| ColorPlateID | old_color_plate_id | 色位 | varchar；字节长度 10 | 是 | CharField |
| AddWeigth | old_add_weigth | 成品空加 | float | 是 | FloatField |
| TubeWeight | old_tube_weight | 纸筒 | float | 是 | FloatField |
| CustGrayID | old_cust_gray_id | 纱种编码 | varchar；字节长度 50 | 是 | CharField |
| LotSheetNo | old_lot_sheet_no | LotSheetNo | varchar；字节长度 20 | 是 | CharField |
| ShipMentType | old_ship_ment_type | 出货方式 | varchar；字节长度 10 | 是 | CharField |
| ColorRemarks | old_color_remarks | 用途 | varchar；字节长度 -1 | 是 | TextField |
| WidthUnit | old_width_unit | 幅宽单位 | nvarchar；字节长度 40 | 是 | CharField |
| WeightKindID | old_weight_kind_id | 克重单位 | nvarchar；字节长度 40 | 是 | CharField |
| DB2BarCode | old_db2_bar_code | 二维码睿程 | varchar；字节长度 -1 | 是 | TextField |
| PackRemarks | old_pack_remarks | PackRemarks | varchar；字节长度 -1 | 是 | TextField |
| SplitCardReason | old_split_card_reason | 拆卡原因 | nvarchar；字节长度 200 | 是 | CharField |
| ProcessName | old_process_name | 订单工序 | varchar；字节长度 255 | 是 | CharField |
| GYYQ | old_gyyq | 工艺要求 | varchar；字节长度 500 | 是 | CharField |
| PBXX | old_pbxx | 配纱信息 | varchar；字节长度 500 | 是 | CharField |
| Suffix | old_suffix | Suffix | varchar；字节长度 50 | 是 | CharField |
| Stereotypes | old_stereotypes | 定型次数 | varchar；字节长度 50 | 是 | CharField |
| ProdUnit | old_prod_unit | 标签单位 | tinyint | 是 | IntegerField |
| ReleaseCardDate | old_release_card_date | 放卡时间 | datetime | 是 | DateTimeField |
| NewLotNo | old_new_lot_no | 新批号 | varchar；字节长度 200 | 是 | CharField |
| StereotypesName | old_stereotypes_name | 染缸编号 | varchar；字节长度 50 | 是 | CharField |
| ReleaseCardDateTwo | old_release_card_date_two | ReleaseCardDateTwo | datetime | 是 | DateTimeField |
| NewProdID | old_new_prod_id | 成品规格 | varchar；字节长度 20 | 是 | CharField |
| JobSheetType | old_job_sheet_type | 工卡类型 | varchar；字节长度 10 | 是 | CharField |
| YarnCategory | old_yarn_category | 纱类别 | varchar；字节长度 50 | 是 | CharField |
| NewSheetNo | old_new_sheet_no | 数字编号 | varchar；字节长度 50 | 是 | CharField |
| FixedQty | old_fixed_qty | 锭重 | decimal(5,2) | 是 | DecimalField |
| Classify | old_classify | 半成品分类 | varchar；字节长度 50 | 是 | CharField |
| Q12 | old_q12 | 纸筒_N | varchar；字节长度 100 | 是 | CharField |
| Q13 | old_q13 | 包装_N | varchar；字节长度 100 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |

### SourceDyeJobSheetMasrkCar — 生产工单与排程相关表（JobSheetMasrkCar，待确认）

源表：`dye.JobSheetMasrkCar`；新表：`src_dye_jobsheetmasrkcar`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 36 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | 客户编码 | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 200 | 是 | CharField |
| ColorE | old_color_e | 颜色英文名 | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 200 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 100 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 20 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 500 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 200 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 10 | 是 | CharField |
| Creater | old_creater | 登记人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 登记时间 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Pound | old_pound | 磅数 | decimal(10,2) | 是 | DecimalField |
| Kg | old_kg | 公斤 | decimal(10,2) | 是 | DecimalField |
| Width | old_width | 幅宽 | varchar；字节长度 200 | 是 | CharField |
| Weight | old_weight | 克重 | varchar；字节长度 200 | 是 | CharField |
| ProgramItem | old_program_item | 工艺 | varchar；字节长度 500 | 是 | CharField |
| dyeDescription | old_dye_description | dyeDescription | varchar；字节长度 200 | 是 | CharField |
| SheetType | old_sheet_type | 送版类别 | varchar；字节长度 20 | 是 | CharField |

### SourceDyeJobSheetNoRushOrder — 生产工单与排程相关表（JobSheetNoRushOrder，待确认）

源表：`dye.JobSheetNoRushOrder`；新表：`src_dye_jobsheetnorushorder`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 200 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 50 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 50 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 50 | 是 | CharField |
| CurrProcessID | old_curr_process_id | 当前进度 | varchar；字节长度 50 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 50 | 是 | CharField |
| SWidth | old_swidth | 幅宽 | varchar；字节长度 50 | 是 | CharField |
| SWeight | old_sweight | 克重 | varchar；字节长度 50 | 是 | CharField |
| SumAssignedRolls | old_sum_assigned_rolls | 实发粒数 | decimal(10,1) | 是 | DecimalField |
| SumAssignedWeightQty | old_sum_assigned_weight_qty | 实发数量 | decimal(10,2) | 是 | DecimalField |
| Creater | old_creater | 制单人 | varchar；字节长度 50 | 是 | CharField |
| CreateDate | old_create_date | 制单日期 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 状态 | smallint | 是 | IntegerField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 50 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 50 | 是 | CharField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |

### SourceDyeJobSheetOther — 生产工单与排程相关表（JobSheetOther，待确认）

源表：`dye.JobSheetOther`；新表：`src_dye_jobsheetother`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 缸号 | varchar；字节长度 100 | 是 | CharField |
| SheetDate | old_sheet_date | 开卡日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| SheetType | old_sheet_type | SheetType | smallint | 是 | IntegerField |
| JobKindID | old_job_kind_id | JobKindID | varchar；字节长度 10 | 是 | CharField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| BusinessKind | old_business_kind | BusinessKind | smallint | 是 | IntegerField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 200 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 50 | 是 | CharField |
| SalerGroupID | old_saler_group_id | SalerGroupID | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 10 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 500 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 200 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 200 | 是 | CharField |
| Structure | old_structure | Structure | varchar；字节长度 150 | 是 | CharField |
| ProductionID | old_production_id | ProductionID | varchar；字节长度 10 | 是 | CharField |
| Linker | old_linker | Linker | varchar；字节长度 10 | 是 | CharField |
| StockUnit | old_stock_unit | StockUnit | tinyint | 是 | IntegerField |
| WidthKindID | old_width_kind_id | WidthKindID | varchar；字节长度 10 | 是 | CharField |
| FactID | old_fact_id | FactID | varchar；字节长度 10 | 是 | CharField |
| OriJobsheetNo | old_ori_jobsheet_no | OriJobsheetNo | varchar；字节长度 20 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 10 | 是 | CharField |
| ColorE | old_color_e | ColorE | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 200 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 200 | 是 | CharField |
| DesignNo | old_design_no | DesignNo | varchar；字节长度 20 | 是 | CharField |
| IsContinue | old_is_continue | IsContinue | bit | 是 | BooleanField |
| IsHurry | old_is_hurry | IsHurry | bit | 是 | BooleanField |
| IsSpecColor | old_is_spec_color | IsSpecColor | bit | 是 | BooleanField |
| IsSpecVat | old_is_spec_vat | IsSpecVat | bit | 是 | BooleanField |
| CustColorNum | old_cust_color_num | CustColorNum | varchar；字节长度 20 | 是 | CharField |
| PreVatQty | old_pre_vat_qty | 排单数量 | float | 是 | FloatField |
| PreRolls | old_pre_rolls | 排单粒数 | float | 是 | FloatField |
| SumAssignedWeightQty | old_sum_assigned_weight_qty | 实发数量 | float | 是 | FloatField |
| SumAssignedRolls | old_sum_assigned_rolls | 实发粒数 | float | 是 | FloatField |
| SumProcessQty | old_sum_process_qty | SumProcessQty | decimal(10,2) | 是 | DecimalField |
| VatNo | old_vat_no | VatNo | varchar；字节长度 20 | 是 | CharField |
| DlvDate | old_dlv_date | DlvDate | datetime | 是 | DateTimeField |
| FinishDate | old_finish_date | FinishDate | datetime | 是 | DateTimeField |
| CurrProcessID | old_curr_process_id | CurrProcessID | varchar；字节长度 10 | 是 | CharField |
| CurrProcessNo | old_curr_process_no | CurrProcessNo | tinyint | 是 | IntegerField |
| CurrStationID | old_curr_station_id | CurrStationID | varchar；字节长度 10 | 是 | CharField |
| StartDate | old_start_date | StartDate | datetime | 是 | DateTimeField |
| RedoEmpID | old_redo_emp_id | RedoEmpID | varchar；字节长度 10 | 是 | CharField |
| RedoProcessID | old_redo_process_id | RedoProcessID | varchar；字节长度 10 | 是 | CharField |
| RedoReasonID | old_redo_reason_id | RedoReasonID | varchar；字节长度 500 | 是 | CharField |
| RedoShiftID | old_redo_shift_id | RedoShiftID | varchar；字节长度 50 | 是 | CharField |
| WorkShopID | old_work_shop_id | WorkShopID | varchar；字节长度 10 | 是 | CharField |
| MachineKindID | old_machine_kind_id | MachineKindID | varchar；字节长度 10 | 是 | CharField |
| AssignUnit | old_assign_unit | AssignUnit | tinyint | 是 | IntegerField |
| OriOrderSeries | old_ori_order_series | OriOrderSeries | varchar；字节长度 20 | 是 | CharField |
| SumProcessRolls | old_sum_process_rolls | SumProcessRolls | decimal(7,2) | 是 | DecimalField |
| LabelID | old_label_id | LabelID | varchar；字节长度 10 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 200 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 50 | 是 | CharField |
| CraftCheck | old_craft_check | CraftCheck | bit | 是 | BooleanField |
| OrderSheetNo | old_order_sheet_no | OrderSheetNo | varchar；字节长度 20 | 是 | CharField |
| NextProcessID | old_next_process_id | NextProcessID | varchar；字节长度 10 | 是 | CharField |
| NextStationID | old_next_station_id | NextStationID | varchar；字节长度 10 | 是 | CharField |
| ProgramID | old_program_id | ProgramID | varchar；字节长度 10 | 是 | CharField |
| Loss | old_loss | Loss | varchar；字节长度 50 | 是 | CharField |
| RealLoss | old_real_loss | RealLoss | decimal(4,1) | 是 | DecimalField |
| AssignInfo | old_assign_info | AssignInfo | varchar；字节长度 500 | 是 | CharField |
| StandCraftNo | old_stand_craft_no | StandCraftNo | varchar；字节长度 20 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 200 | 是 | CharField |
| IsFirstVat | old_is_first_vat | IsFirstVat | bit | 是 | BooleanField |
| ShippingMarkID | old_shipping_mark_id | ShippingMarkID | varchar；字节长度 10 | 是 | CharField |
| PlanDetailNo | old_plan_detail_no | PlanDetailNo | varchar；字节长度 30 | 是 | CharField |
| WidthDn | old_width_dn | WidthDn | decimal(6,2) | 是 | DecimalField |
| WidthUp | old_width_up | WidthUp | decimal(6,2) | 是 | DecimalField |
| WeightDn | old_weight_dn | WeightDn | decimal(6,2) | 是 | DecimalField |
| WeightUp | old_weight_up | WeightUp | decimal(6,2) | 是 | DecimalField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| RelaLotNo | old_rela_lot_no | RelaLotNo | varchar；字节长度 50 | 是 | CharField |
| ColorRGB | old_color_rgb | ColorRGB | int | 是 | IntegerField |
| IsPause | old_is_pause | IsPause | bit | 是 | BooleanField |
| PrintKind | old_print_kind | PrintKind | varchar；字节长度 1 | 是 | CharField |
| ProgramKindID | old_program_kind_id | ProgramKindID | varchar；字节长度 10 | 是 | CharField |
| OriColorID | old_ori_color_id | OriColorID | varchar；字节长度 10 | 是 | CharField |
| OriColorNum | old_ori_color_num | OriColorNum | varchar；字节长度 20 | 是 | CharField |
| ConfirmSideID | old_confirm_side_id | ConfirmSideID | varchar；字节长度 10 | 是 | CharField |
| PlanDate | old_plan_date | PlanDate | datetime | 是 | DateTimeField |
| MainStuffKindID | old_main_stuff_kind_id | MainStuffKindID | varchar；字节长度 10 | 是 | CharField |
| IsToLabDips | old_is_to_lab_dips | IsToLabDips | bit | 是 | BooleanField |
| RedoDefectName | old_redo_defect_name | RedoDefectName | varchar；字节长度 100 | 是 | CharField |
| MachineID | old_machine_id | MachineID | varchar；字节长度 10 | 是 | CharField |
| LossStr | old_loss_str | LossStr | varchar；字节长度 20 | 是 | CharField |
| ProdQty | old_prod_qty | ProdQty | decimal(10,2) | 是 | DecimalField |
| GWidth | old_gwidth | GWidth | decimal(6,2) | 是 | DecimalField |
| GWeight | old_gweight | GWeight | decimal(6,2) | 是 | DecimalField |
| WarpDensity | old_warp_density | WarpDensity | varchar；字节长度 50 | 是 | CharField |
| WeftDensity | old_weft_density | WeftDensity | varchar；字节长度 50 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| AddrDlv | old_addr_dlv | AddrDlv | varchar；字节长度 50 | 是 | CharField |
| WeightUnit | old_weight_unit | WeightUnit | varchar；字节长度 10 | 是 | CharField |
| OrderSheetDate | old_order_sheet_date | OrderSheetDate | datetime | 是 | DateTimeField |
| Model1 | old_model1 | Model1 | nchar；字节长度 20 | 是 | CharField |
| SumProcessLengthQty | old_sum_process_length_qty | SumProcessLengthQty | decimal(10,2) | 是 | DecimalField |
| SumProcessWeightQty | old_sum_process_weight_qty | SumProcessWeightQty | decimal(10,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| Code | old_code | Code | varchar；字节长度 20 | 是 | CharField |
| Code1 | old_code1 | Code1 | varchar；字节长度 20 | 是 | CharField |
| Weight | old_weight | Weight | varchar；字节长度 200 | 是 | CharField |
| Width | old_width | Width | varchar；字节长度 200 | 是 | CharField |
| SumAssignedLengthQty | old_sum_assigned_length_qty | SumAssignedLengthQty | decimal(10,2) | 是 | DecimalField |
| OrderQty | old_order_qty | OrderQty | decimal(8,2) | 是 | DecimalField |
| OrderQtyTotal | old_order_qty_total | OrderQtyTotal | decimal(8,2) | 是 | DecimalField |
| CustJobNo | old_cust_job_no | CustJobNo | varchar；字节长度 50 | 是 | CharField |
| Sender | old_sender | Sender | varchar；字节长度 20 | 是 | CharField |
| Receiver | old_receiver | Receiver | varchar；字节长度 20 | 是 | CharField |
| IsSplited | old_is_splited | IsSplited | smallint | 是 | IntegerField |
| WeightQty | old_weight_qty | WeightQty | decimal(10,2) | 是 | DecimalField |
| OriSourceJobNo | old_ori_source_job_no | OriSourceJobNo | varchar；字节长度 50 | 是 | CharField |
| SetHurryTime | old_set_hurry_time | SetHurryTime | datetime | 是 | DateTimeField |
| SetPauseBegTime | old_set_pause_beg_time | SetPauseBegTime | datetime | 是 | DateTimeField |
| SetPauseEndTime | old_set_pause_end_time | SetPauseEndTime | datetime | 是 | DateTimeField |
| HurryInfo | old_hurry_info | HurryInfo | varchar；字节长度 512 | 是 | CharField |
| PauseInfo | old_pause_info | PauseInfo | varchar；字节长度 512 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | StorageUnitIDs | varchar；字节长度 100 | 是 | CharField |
| RollAvgQtyStr | old_roll_avg_qty_str | RollAvgQtyStr | varchar；字节长度 50 | 是 | CharField |
| IsProdInFinished | old_is_prod_in_finished | IsProdInFinished | bit | 是 | BooleanField |
| BarCode | old_bar_code | BarCode | varchar；字节长度 100 | 是 | CharField |
| PhaseID | old_phase_id | PhaseID | varchar；字节长度 10 | 是 | CharField |
| Jobattes1 | old_jobattes1 | Jobattes1 | varchar；字节长度 1000 | 是 | CharField |
| Finish | old_finish | Finish | tinyint | 是 | IntegerField |
| OriSourceJobNo2 | old_ori_source_job_no2 | OriSourceJobNo2 | varchar；字节长度 50 | 是 | CharField |
| Customer | old_customer | Customer | varchar；字节长度 200 | 是 | CharField |
| CHECKDots | old_checkdots | 标准分值 | decimal(18,0) | 是 | DecimalField |
| Checker | old_checker | Checker | varchar；字节长度 10 | 是 | CharField |
| IsOver | old_is_over | IsOver | bit | 是 | BooleanField |
| ProdWidth | old_prod_width | ProdWidth | float | 是 | FloatField |
| ProdWeight | old_prod_weight | ProdWeight | float | 是 | FloatField |
| ProdRePeatcnt | old_prod_re_peatcnt | ProdRePeatcnt | varchar；字节长度 10 | 是 | CharField |
| ProdSkeWing | old_prod_ske_wing | ProdSkeWing | float | 是 | FloatField |
| Grade | old_grade | Grade | varchar；字节长度 10 | 是 | CharField |
| YAvgdots | old_yavgdots | YAvgdots | float | 是 | FloatField |
| PDots | old_pdots | PDots | int | 是 | IntegerField |
| PlengthQyt | old_plength_qyt | PlengthQyt | float | 是 | FloatField |
| Pkg | old_pkg | Pkg | float | 是 | FloatField |
| PRolls | old_prolls | PRolls | int | 是 | IntegerField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 20 | 是 | CharField |
| PenetrationNO | old_penetration_no | PenetrationNO | varchar；字节长度 20 | 是 | CharField |
| Inch | old_inch | Inch | varchar；字节长度 20 | 是 | CharField |
| FabricNO1 | old_fabric_no1 | FabricNO1 | varchar；字节长度 200 | 是 | CharField |
| FabricNO2 | old_fabric_no2 | FabricNO2 | varchar；字节长度 200 | 是 | CharField |
| FabricNO3 | old_fabric_no3 | FabricNO3 | varchar；字节长度 200 | 是 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 10 | 是 | CharField |

### SourceDyeJobSheetReceive — 工卡接收/结算记录

源表：`dye.JobSheetReceive`；新表：`src_dye_jobsheetreceive`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 36 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | 单据时间 | datetime | 是 | DateTimeField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | 客户编码 | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 200 | 是 | CharField |
| ColorE | old_color_e | 颜色英文名 | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 200 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 100 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 20 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 500 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 200 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 10 | 是 | CharField |
| Creater | old_creater | 登记人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 登记时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| Width | old_width | 幅宽 | varchar；字节长度 200 | 是 | CharField |
| Weight | old_weight | 克重 | varchar；字节长度 200 | 是 | CharField |
| ProgramItem | old_program_item | 单双染 | varchar；字节长度 500 | 是 | CharField |
| dyeDescription | old_dye_description | 是否首缸 | varchar；字节长度 200 | 是 | CharField |
| SheetType | old_sheet_type | SheetType | varchar；字节长度 20 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 50 | 是 | CharField |
| CombineSheetNos | old_combine_sheet_nos | 合缸缸号 | varchar；字节长度 -1 | 是 | TextField |
| MachineNo | old_machine_no | 机台 | varchar；字节长度 50 | 是 | CharField |
| ColorMatching | old_color_matching | 对色员 | varchar；字节长度 50 | 是 | CharField |
| Days | old_days | 日期 | varchar；字节长度 10 | 是 | CharField |
| ShiftID | old_shift_id | 班别 | varchar；字节长度 50 | 是 | CharField |
| Bigs | old_bigs | Bigs | float | 是 | FloatField |
| AddVat | old_add_vat | AddVat | int | 是 | IntegerField |
| RTVat | old_rtvat | RTVat | float | 是 | FloatField |
| PassVat | old_pass_vat | PassVat | float | 是 | FloatField |
| BatchColor | old_batch_color | 批复情况 | varchar；字节长度 250 | 是 | CharField |
| DyeFactoryOpinions | old_dye_factory_opinions | 染厂意见 | varchar；字节长度 250 | 是 | CharField |
| IsOK | old_is_ok | 是否OK | varchar；字节长度 30 | 是 | CharField |

### SourceDyeJobSheetRegister — 生产工单与排程相关表（JobSheetRegister，待确认）

源表：`dye.JobSheetRegister`；新表：`src_dye_jobsheetregister`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 36 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | 单据时间 | datetime | 是 | DateTimeField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | 客户编码 | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 200 | 是 | CharField |
| ColorE | old_color_e | 颜色英文名 | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 200 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 100 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 20 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 500 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 200 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 10 | 是 | CharField |
| Creater | old_creater | 登记人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 登记时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| Width | old_width | 幅宽 | varchar；字节长度 200 | 是 | CharField |
| Weight | old_weight | 克重 | varchar；字节长度 200 | 是 | CharField |
| ProgramItem | old_program_item | 单双染 | varchar；字节长度 500 | 是 | CharField |
| dyeDescription | old_dye_description | 是否首缸 | varchar；字节长度 200 | 是 | CharField |
| SheetType | old_sheet_type | SheetType | varchar；字节长度 20 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 50 | 是 | CharField |
| CombineSheetNos | old_combine_sheet_nos | 合缸缸号 | varchar；字节长度 -1 | 是 | TextField |
| MachineNo | old_machine_no | 机台 | varchar；字节长度 50 | 是 | CharField |
| ColorMatching | old_color_matching | 对色员 | varchar；字节长度 50 | 是 | CharField |
| Days | old_days | 日期 | varchar；字节长度 10 | 是 | CharField |
| ShiftID | old_shift_id | 班别 | varchar；字节长度 50 | 是 | CharField |
| Bigs | old_bigs | Bigs | float | 是 | FloatField |
| AddVat | old_add_vat | AddVat | int | 是 | IntegerField |
| RTVat | old_rtvat | RTVat | float | 是 | FloatField |
| PassVat | old_pass_vat | PassVat | float | 是 | FloatField |
| BatchColor | old_batch_color | BatchColor | varchar；字节长度 250 | 是 | CharField |
| DyeFactoryOpinions | old_dye_factory_opinions | 加色次数 | varchar；字节长度 250 | 是 | CharField |
| IsOK | old_is_ok | IsOK | varchar；字节长度 30 | 是 | CharField |

### SourceDyeJobSheetSchedule — 生产工单与排程相关表（JobSheetSchedule，待确认）

源表：`dye.JobSheetSchedule`；新表：`src_dye_jobsheetschedule`；原主键：ID。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | 编码 | varchar；字节长度 50 | 否 | CharField |
| JobSheetSeries | old_job_sheet_series | 流程卡流水号 | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| SequenceNo | old_sequence_no | 顺序号 | bigint | 是 | BigIntegerField |
| Status | old_status | 状态 | varchar；字节长度 1 | 是 | CharField |
| PlanDate | old_plan_date | 计划日期 | datetime | 是 | DateTimeField |
| StartTime | old_start_time | 开始时间 | datetime | 是 | DateTimeField |
| FinishTime | old_finish_time | 结束时间 | datetime | 是 | DateTimeField |
| TargetMin | old_target_min | 预计分钟 | smallint | 是 | IntegerField |
| ShiftID | old_shift_id | 班组 | varchar；字节长度 10 | 是 | CharField |
| ClassID | old_class_id | 班别 | varchar；字节长度 10 | 是 | CharField |
| ProgramID | old_program_id | 前道流程 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 300 | 是 | CharField |

### SourceDyeJobShiftEmp — 生产工单与排程相关表（JobShiftEmp，待确认）

源表：`dye.JobShiftEmp`；新表：`src_dye_jobshiftemp`；原主键：JobSheetNo, ShiftID, EmpID, ProcessNo, WProcessNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 否 | CharField |
| ShiftID | old_shift_id | 班组 | varchar；字节长度 10 | 否 | CharField |
| EmpID | old_emp_id | 员工 | varchar；字节长度 10 | 否 | CharField |
| EffiRate | old_effi_rate | 效率比例 | decimal(6,4) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ProcessNo | old_process_no | 工序号 | tinyint | 否 | IntegerField |
| ProcessID | old_process_id | 工序 | varchar；字节长度 10 | 是 | CharField |
| WProcessNo | old_wprocess_no | 刷卡号 | varchar；字节长度 20 | 否 | CharField |
| Post | old_post | Post | varchar；字节长度 20 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeWProcess`；原码 `WProcessNo` → 父表原码 `WProcessNo`；依据：原界面主从 JobShiftEmp → DPWProcess；原界面主从 DPJobShiftEmpEdit → DPWProcessEdit。

关联 `source_parent_2` → `erp_production.SourceDyeWProcess`；原码 `WProcessNo, JobSheetNo, ProcessNo, ProcessID, ShiftID` → 父表原码 `WProcessNo, JobSheetNo, ProcessNo, ProcessID, ShiftID`；依据：原界面主从 JobShiftEmpEdit → WProcessEdit；原界面主从 AddJobShiftEmpEdit → AddWProcessEdit。

### SourceDyeJobShiftEmpBak — 生产工单与排程相关表（JobShiftEmpBak，待确认）

源表：`dye.JobShiftEmpBak`；新表：`src_dye_jobshiftempbak`；原主键：JobSheetNo, ShiftID, EmpID, ProcessNo, WProcessNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 否 | CharField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 10 | 否 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 10 | 否 | CharField |
| EffiRate | old_effi_rate | EffiRate | decimal(6,4) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ProcessNo | old_process_no | ProcessNo | tinyint | 否 | IntegerField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 10 | 是 | CharField |
| WProcessNo | old_wprocess_no | WProcessNo | varchar；字节长度 20 | 否 | CharField |

### SourceDyeJobStartRollNo — 生产工单与排程相关表（JobStartRollNo，待确认）

源表：`dye.JobStartRollNo`；新表：`src_dye_jobstartrollno`；原主键：无主键。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 是 | CharField |
| OrderNo | old_order_no | OrderNo | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |

### SourceDyeMachineCarePlan — 设备维护与能耗相关表（MachineCarePlan，待确认）

源表：`dye.MachineCarePlan`；新表：`src_dye_machinecareplan`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单据号码 | varchar；字节长度 36 | 是 | CharField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 10 | 是 | CharField |
| StartTime | old_start_time | 开始时间 | datetime | 是 | DateTimeField |
| EndTime | old_end_time | 结束时间 | datetime | 是 | DateTimeField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Creater | old_creater | 制单人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 制单时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Kind | old_kind | 类别 | varchar；字节长度 20 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 10 | 是 | CharField |
| Approver | old_approver | 审核人 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |

### SourceDyeMachineCarePlanDetail — 设备维护与能耗相关表（MachineCarePlanDetail，待确认）

源表：`dye.MachineCarePlanDetail`；新表：`src_dye_machinecareplandetail`；原主键：SheetSeries, DetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明显号 | varchar；字节长度 36 | 否 | CharField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 10 | 是 | CharField |
| MachineID | old_machine_id | 机台 | varchar；字节长度 50 | 是 | CharField |
| ShiftID | old_shift_id | 班组 | varchar；字节长度 10 | 是 | CharField |
| HandlerIDs | old_handler_ids | 保养人员 | varchar；字节长度 100 | 是 | CharField |
| HandleDate | old_handle_date | 保养日期 | datetime | 是 | DateTimeField |
| HandleIdea | old_handle_idea | 相关意见 | varchar；字节长度 512 | 是 | CharField |
| ResultID | old_result_id | 保养结果 | varchar；字节长度 200 | 是 | CharField |
| Approver | old_approver | 审核人 | varchar；字节长度 20 | 是 | CharField |
| ApproveIdea | old_approve_idea | 审核意见 | varchar；字节长度 200 | 是 | CharField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| PartID | old_part_id | 保养部位 | nchar；字节长度 20 | 是 | CharField |
| ArticleID | old_article_id | 机配件 | nchar；字节长度 20 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeMachineCarePlan`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 MachineCarePlanDetail → MachineCarePlan。

### SourceDyeMachineCareProject — 设备维护与能耗相关表（MachineCareProject，待确认）

源表：`dye.MachineCareProject`；新表：`src_dye_machinecareproject`；原主键：SheetSeries, DetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 否 | CharField |
| SortNo | old_sort_no | SortNo | int | 是 | IntegerField |
| SerialNum | old_serial_num | SerialNum | nvarchar；字节长度 20 | 是 | CharField |
| ProjectInfo | old_project_info | ProjectInfo | nvarchar；字节长度 400 | 是 | CharField |
| Value | old_value | Value | nvarchar；字节长度 200 | 是 | CharField |
| DefaultValue | old_default_value | DefaultValue | nvarchar；字节长度 200 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| CaseDetailNo | old_case_detail_no | CaseDetailNo | varchar；字节长度 36 | 是 | CharField |
| Result | old_result | Result | int | 是 | IntegerField |
| IsInputText | old_is_input_text | IsInputText | bit | 是 | BooleanField |

### SourceDyeMachineCareRecords — 设备维护与能耗相关表（MachineCareRecords，待确认）

源表：`dye.MachineCareRecords`；新表：`src_dye_machinecarerecords`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 记录单号 | varchar；字节长度 36 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| MachineID | old_machine_id | 保养设备 | varchar；字节长度 20 | 是 | CharField |
| CarePlanDetailNo | old_care_plan_detail_no | 保养计划明细单号 | varchar；字节长度 50 | 是 | CharField |
| EmpID | old_emp_id | 保养人 | varchar；字节长度 50 | 是 | CharField |
| CareDate | old_care_date | 保养时间 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 2000 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 20 | 是 | CharField |
| HandlerIDs | old_handler_ids | 保养员 | varchar；字节长度 100 | 是 | CharField |
| HandleIdea | old_handle_idea | 相关意见 | varchar；字节长度 50 | 是 | CharField |
| ResultID | old_result_id | 处理结果 | varchar；字节长度 200 | 是 | CharField |
| MachineName | old_machine_name | MachineName | nvarchar；字节长度 128 | 是 | CharField |
| MachineLocation | old_machine_location | MachineLocation | nvarchar；字节长度 128 | 是 | CharField |

### SourceDyeMachineCase — 设备维护与能耗相关表（MachineCase，待确认）

源表：`dye.MachineCase`；新表：`src_dye_machinecase`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 类型 | smallint | 是 | IntegerField |
| ContentName | old_content_name | 内容名称 | nvarchar；字节长度 100 | 是 | CharField |
| BaseCaseID | old_base_case_id | 基础方案 | varchar；字节长度 20 | 是 | CharField |
| IsMultipleCase | old_is_multiple_case | IsMultipleCase | bit | 是 | BooleanField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 制单人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 制单日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |

### SourceDyeMachineCaseDetail — 设备维护与能耗相关表（MachineCaseDetail，待确认）

源表：`dye.MachineCaseDetail`；新表：`src_dye_machinecasedetail`；原主键：SheetSeries, DetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 36 | 否 | CharField |
| MachineID | old_machine_id | 机台 | varchar；字节长度 50 | 是 | CharField |
| Cycle | old_cycle | 周期描述 | nvarchar；字节长度 40 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeMachineCase`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 MachineCaseDetail → MachineCase。

### SourceDyeMachineCaseProject — 设备维护与能耗相关表（MachineCaseProject，待确认）

源表：`dye.MachineCaseProject`；新表：`src_dye_machinecaseproject`；原主键：SheetSeries, DetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 36 | 否 | CharField |
| SortNo | old_sort_no | 排序号 | int | 是 | IntegerField |
| SerialNum | old_serial_num | 序号 | nvarchar；字节长度 20 | 是 | CharField |
| ProjectInfo | old_project_info | 项目内容 | nvarchar；字节长度 400 | 是 | CharField |
| DefaultValue | old_default_value | 常规值 | nvarchar；字节长度 200 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| BaseCaseDetailNo | old_base_case_detail_no | 基础方案明细号 | varchar；字节长度 36 | 是 | CharField |
| IsInputText | old_is_input_text | 是否输入文本 | bit | 是 | BooleanField |

关联 `source_parent_1` → `erp_production.SourceDyeMachineCase`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 MachineCaseProject → MachineCase。

### SourceDyeMachineFault — 设备维护与能耗相关表（MachineFault，待确认）

源表：`dye.MachineFault`；新表：`src_dye_machinefault`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 报修单号 | varchar；字节长度 36 | 是 | CharField |
| SheetDate | old_sheet_date | 报修日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | varchar；字节长度 20 | 是 | CharField |
| MachineID | old_machine_id | 机台号 | varchar；字节长度 50 | 是 | CharField |
| EmpID | old_emp_id | 员工 | varchar；字节长度 50 | 是 | CharField |
| HappenTime | old_happen_time | 发生时间 | datetime | 是 | DateTimeField |
| ApplyTime | old_apply_time | 申请时间 | datetime | 是 | DateTimeField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 20 | 是 | CharField |
| ShiftID | old_shift_id | 班别 | varchar；字节长度 20 | 是 | CharField |
| FaultID | old_fault_id | 故障 | nvarchar；字节长度 1024 | 是 | CharField |
| SeverityID | old_severity_id | 严重等级 | varchar；字节长度 20 | 是 | CharField |
| HandlerIDs | old_handler_ids | HandlerIDs | varchar；字节长度 100 | 是 | CharField |
| Handlers | old_handlers | Handlers | varchar；字节长度 100 | 是 | CharField |
| StartTime | old_start_time | 开始时间 | datetime | 是 | DateTimeField |
| EndTime | old_end_time | 结束时间 | datetime | 是 | DateTimeField |
| ResultID | old_result_id | 维修结果 | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 20 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 制单人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 制单日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| HandleIdea | old_handle_idea | HandleIdea | varchar；字节长度 512 | 是 | CharField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PhotoAddress | old_photo_address | PhotoAddress | varchar；字节长度 512 | 是 | CharField |
| ApproveIdea | old_approve_idea | ApproveIdea | varchar；字节长度 200 | 是 | CharField |
| PatrolDetailNo | old_patrol_detail_no | PatrolDetailNo | varchar；字节长度 100 | 是 | CharField |
| SheetType | old_sheet_type | 报修类别 | varchar；字节长度 10 | 是 | CharField |
| StationID | old_station_id | 站别 | varchar；字节长度 30 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 30 | 是 | CharField |
| FaultRemarks | old_fault_remarks | 故障描述 | varchar；字节长度 200 | 是 | CharField |
| MachineName | old_machine_name | MachineName | nvarchar；字节长度 128 | 是 | CharField |
| MachineLocation | old_machine_location | MachineLocation | nvarchar；字节长度 128 | 是 | CharField |
| Urgent | old_urgent | Urgent | int | 是 | IntegerField |
| FlowStatus | old_flow_status | 流转状态 | nvarchar；字节长度 40 | 是 | CharField |
| ApplyMan | old_apply_man | ApplyMan | nvarchar；字节长度 20 | 是 | CharField |
| ApplyIdea | old_apply_idea | ApplyIdea | nvarchar；字节长度 1024 | 是 | CharField |
| EmpGroup | old_emp_group | 维修分组 | nvarchar；字节长度 40 | 是 | CharField |
| FaultClass | old_fault_class | 故障分类 | nvarchar；字节长度 1000 | 是 | CharField |
| MachineClass | old_machine_class | 设备分类 | nvarchar；字节长度 200 | 是 | CharField |

### SourceDyeMachineFaultArticleInfo — 设备维护与能耗相关表（MachineFaultArticleInfo，待确认）

源表：`dye.MachineFaultArticleInfo`；新表：`src_dye_machinefaultarticleinfo`；原主键：SheetSeries, Rounds, SerialNum。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| Rounds | old_rounds | Rounds | int | 否 | IntegerField |
| SerialNum | old_serial_num | SerialNum | int | 否 | IntegerField |
| ArticleID | old_article_id | ArticleID | varchar；字节长度 100 | 是 | CharField |
| ArticleName | old_article_name | ArticleName | nvarchar；字节长度 200 | 是 | CharField |
| Spec | old_spec | Spec | nvarchar；字节长度 200 | 是 | CharField |
| Qty | old_qty | Qty | decimal(10,1) | 是 | DecimalField |
| Kind | old_kind | Kind | int | 是 | IntegerField |
| Unit | old_unit | Unit | varchar；字节长度 20 | 是 | CharField |

### SourceDyeMachineFaultComment — 设备维护与能耗相关表（MachineFaultComment，待确认）

源表：`dye.MachineFaultComment`；新表：`src_dye_machinefaultcomment`；原主键：RecordID。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| RecordID | old_record_id | RecordID | varchar；字节长度 50 | 否 | CharField |
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | nvarchar；字节长度 40 | 是 | CharField |
| Remark | old_remark | Remark | nvarchar；字节长度 400 | 是 | CharField |

### SourceDyeMachineFaultFilter — 设备维护与能耗相关表（MachineFaultFilter，待确认）

源表：`dye.MachineFaultFilter`；新表：`src_dye_machinefaultfilter`；原主键：FlowType, TabID。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FlowType | old_flow_type | FlowType | int | 否 | IntegerField |
| TabID | old_tab_id | TabID | varchar；字节长度 10 | 否 | CharField |
| TabTitle | old_tab_title | TabTitle | nvarchar；字节长度 40 | 否 | CharField |
| FilterSQL | old_filter_sql | FilterSQL | nvarchar；字节长度 512 | 否 | CharField |
| SortNo | old_sort_no | SortNo | int | 否 | IntegerField |

### SourceDyeMachineFaultRecord — 设备维护与能耗相关表（MachineFaultRecord，待确认）

源表：`dye.MachineFaultRecord`；新表：`src_dye_machinefaultrecord`；原主键：RecordID。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| RecordID | old_record_id | RecordID | varchar；字节长度 50 | 否 | CharField |
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 否 | CharField |
| Operator | old_operator | Operator | nvarchar；字节长度 100 | 是 | CharField |
| Action | old_action | Action | nvarchar；字节长度 40 | 否 | CharField |
| ActionType | old_action_type | ActionType | nvarchar；字节长度 40 | 否 | CharField |
| HandlerIDs | old_handler_ids | HandlerIDs | varchar；字节长度 100 | 是 | CharField |
| Handlers | old_handlers | Handlers | nvarchar；字节长度 400 | 是 | CharField |
| Remark | old_remark | Remark | nvarchar；字节长度 400 | 否 | CharField |
| RecordDate | old_record_date | RecordDate | datetime | 否 | DateTimeField |
| Score | old_score | Score | int | 是 | IntegerField |

### SourceDyeMachines — 设备维护与能耗相关表（Machines，待确认）

源表：`dye.Machines`；新表：`src_dye_machines`；原主键：ID。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | int | 否 | IntegerField |
| MachineAlias | old_machine_alias | MachineAlias | varchar；字节长度 20 | 否 | CharField |
| ConnectType | old_connect_type | ConnectType | int | 否 | IntegerField |
| IP | old_ip | IP | varchar；字节长度 20 | 是 | CharField |
| SerialPort | old_serial_port | SerialPort | int | 是 | IntegerField |
| Port | old_port | Port | int | 是 | IntegerField |
| Baudrate | old_baudrate | Baudrate | int | 是 | IntegerField |
| MachineNumber | old_machine_number | MachineNumber | int | 否 | IntegerField |
| IsHost | old_is_host | IsHost | bit | 是 | BooleanField |
| Enabled | old_enabled | Enabled | bit | 是 | BooleanField |
| CommPassword | old_comm_password | CommPassword | varchar；字节长度 12 | 是 | CharField |
| UILanguage | old_uilanguage | UILanguage | smallint | 是 | IntegerField |
| DateFormat | old_date_format | DateFormat | smallint | 是 | IntegerField |
| InOutRecordWarn | old_in_out_record_warn | InOutRecordWarn | smallint | 是 | IntegerField |
| Idle | old_idle | Idle | smallint | 是 | IntegerField |
| Voice | old_voice | Voice | smallint | 是 | IntegerField |
| managercount | old_managercount | managercount | smallint | 是 | IntegerField |
| usercount | old_usercount | usercount | smallint | 是 | IntegerField |
| fingercount | old_fingercount | fingercount | smallint | 是 | IntegerField |
| SecretCount | old_secret_count | SecretCount | smallint | 是 | IntegerField |
| FirmwareVersion | old_firmware_version | FirmwareVersion | varchar；字节长度 20 | 是 | CharField |
| ProductType | old_product_type | ProductType | varchar；字节长度 20 | 是 | CharField |
| LockControl | old_lock_control | LockControl | smallint | 是 | IntegerField |
| Purpose | old_purpose | Purpose | smallint | 是 | IntegerField |
| ProduceKind | old_produce_kind | ProduceKind | int | 是 | IntegerField |
| sn | old_sn | sn | varchar；字节长度 20 | 是 | CharField |
| PhotoStamp | old_photo_stamp | PhotoStamp | varchar；字节长度 20 | 是 | CharField |
| IsIfChangeConfigServer2 | old_is_if_change_config_server2 | IsIfChangeConfigServer2 | int | 是 | IntegerField |
| IsAndroid | old_is_android | IsAndroid | varchar；字节长度 1 | 是 | CharField |
| pushver | old_pushver | pushver | int | 是 | IntegerField |
| P2PUid | old_p2_puid | P2PUid | varchar；字节长度 100 | 是 | CharField |

### SourceDyeMoveShiftBill — 生产工单与排程相关表（MoveShiftBill，待确认）

源表：`dye.MoveShiftBill`；新表：`src_dye_moveshiftbill`；原主键：Code。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| Code | old_code | 单据编号 | varchar；字节长度 50 | 否 | CharField |
| EmpID | old_emp_id | 员工ID | varchar；字节长度 20 | 否 | CharField |
| BeginTime | old_begin_time | 开始时间 | datetime | 是 | DateTimeField |
| DayEnd | old_day_end | 结束时间 | datetime | 是 | DateTimeField |
| Shift | old_shift | 临时考勤班别 | varchar；字节长度 60 | 是 | CharField |
| Creater | old_creater | 制单人 | nvarchar；字节长度 16 | 是 | CharField |
| Note | old_note | 备注 | varchar；字节长度 512 | 是 | CharField |

### SourceDyeOutWorkApply — 生产工单与排程相关表（OutWorkApply，待确认）

源表：`dye.OutWorkApply`；新表：`src_dye_outworkapply`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 日期 | datetime | 是 | DateTimeField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| FactID | old_fact_id | 部门 | varchar；字节长度 20 | 是 | CharField |
| ProcessID | old_process_id | 加工项目 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1000 | 是 | CharField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| Creater | old_creater | 制单人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 制单日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审批人 | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | 审批时间 | datetime | 是 | DateTimeField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |

### SourceDyeOutWorkApplyDetail — 生产工单与排程相关表（OutWorkApplyDetail，待确认）

源表：`dye.OutWorkApplyDetail`；新表：`src_dye_outworkapplydetail`；原主键：SheetSeries, DetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |
| JobTaskSheetNo | old_job_task_sheet_no | 卡号 | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 20 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 200 | 是 | CharField |
| ColorID | old_color_id | 物料颜色 | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| Packs | old_packs | 件数 | decimal(10,2) | 是 | DecimalField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| Qty | old_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1000 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| Price | old_price | 单价 | decimal(10,2) | 是 | DecimalField |
| Amount | old_amount | 金额 | decimal(12,2) | 是 | DecimalField |
| ReceSheetNo | old_rece_sheet_no | 入库明细单号 | varchar；字节长度 30 | 是 | CharField |
| InSheetKind | old_in_sheet_kind | 物料分类 | varchar；字节长度 10 | 是 | CharField |
| FixedQty | old_fixed_qty | 锭重 | decimal(5,2) | 是 | DecimalField |
| FabricID | old_fabric_id | 成品规格 | varchar；字节长度 50 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商 | varchar；字节长度 30 | 是 | CharField |
| PurchaseOrders | old_purchase_orders | 采购单号 | varchar；字节长度 20 | 是 | CharField |
| A_A | old_a_a | 物料区域 | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | 物料等级 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeOutWorkApply`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 OutWorkApplyDetail → OutWorkApply。

### SourceDyePlanDetail — 生产工单与排程相关表（PlanDetail，待确认）

源表：`dye.PlanDetail`；新表：`src_dye_plandetail`；原主键：PlanDetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| PlanDetailNo | old_plan_detail_no | 主计划明细号 | varchar；字节长度 30 | 否 | CharField |
| SequenceNo | old_sequence_no | 顺序号 | bigint | 否 | BigIntegerField |
| OrderSheetNo | old_order_sheet_no | 订单号 | varchar；字节长度 20 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| Vats | old_vats | 缸数 | decimal(7,1) | 是 | DecimalField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| StartDate | old_start_date | 开始日期 | datetime | 是 | DateTimeField |
| FinishDate | old_finish_date | 预计交货日期 | datetime | 是 | DateTimeField |
| MainMemo | old_main_memo | 主要说明 | varchar；字节长度 300 | 是 | CharField |
| AssignMemo | old_assign_memo | 配纱说明 | varchar；字节长度 300 | 是 | CharField |
| AtteMemo | old_atte_memo | 要求说明 | varchar；字节长度 300 | 是 | CharField |
| ColorMemo | old_color_memo | 颜色说明 | varchar；字节长度 300 | 是 | CharField |
| ProcessMemo | old_process_memo | 工序说明 | varchar；字节长度 300 | 是 | CharField |
| Status | old_status | 状态 | varchar；字节长度 1 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyePlanMain`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 PlanDetail → PlanMain。

### SourceDyePlanMain — 生产工单与排程相关表（PlanMain，待确认）

源表：`dye.PlanMain`；新表：`src_dye_planmain`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyePrePlanOrder — 生产工单与排程相关表（PrePlanOrder，待确认）

源表：`dye.PrePlanOrder`；新表：`src_dye_preplanorder`；原主键：ID。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | bigint | 否 | BigIntegerField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| PlanDate | old_plan_date | PlanDate | datetime | 是 | DateTimeField |
| StartDate | old_start_date | StartDate | datetime | 是 | DateTimeField |
| EndDate | old_end_date | EndDate | datetime | 是 | DateTimeField |
| FinishDate | old_finish_date | FinishDate | datetime | 是 | DateTimeField |
| ProgramKindID | old_program_kind_id | ProgramKindID | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| OrderSheetNo | old_order_sheet_no | OrderSheetNo | varchar；字节长度 20 | 是 | CharField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 是 | CharField |
| Vats | old_vats | Vats | decimal(7,1) | 是 | DecimalField |
| Rolls | old_rolls | Rolls | decimal(7,2) | 是 | DecimalField |
| Qty | old_qty | Qty | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |
| Status | old_status | Status | varchar；字节长度 1 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |

### SourceDyeProcessCraft — 染色工艺与配方相关表（ProcessCraft，待确认）

源表：`dye.ProcessCraft`；新表：`src_dye_processcraft`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| CraftKindID | old_craft_kind_id | 工艺类别 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| Structure | old_structure | 组织 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 颜色代码 | varchar；字节长度 20 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| Width | old_width | 幅宽 | decimal(6,2) | 是 | DecimalField |
| Weight | old_weight | 克重 | decimal(6,2) | 是 | DecimalField |
| WarpDensity | old_warp_density | 经密 | decimal(6,2) | 是 | DecimalField |
| WeftDensity | old_weft_density | 纬密 | decimal(6,2) | 是 | DecimalField |
| ProcessID | old_process_id | 工序 | varchar；字节长度 10 | 是 | CharField |
| OrderSheetNo | old_order_sheet_no | 订单号 | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 10 | 是 | CharField |
| PPName01 | old_ppname01 | 参数名1 | varchar；字节长度 20 | 是 | CharField |
| Value01 | old_value01 | 参数值01 | varchar；字节长度 20 | 是 | CharField |
| PPName02 | old_ppname02 | 参数名2 | varchar；字节长度 20 | 是 | CharField |
| Value02 | old_value02 | 参数值02 | varchar；字节长度 20 | 是 | CharField |
| PPName03 | old_ppname03 | 参数名3 | varchar；字节长度 20 | 是 | CharField |
| Value03 | old_value03 | 参数值03 | varchar；字节长度 20 | 是 | CharField |
| PPName04 | old_ppname04 | 参数名4 | varchar；字节长度 20 | 是 | CharField |
| Value04 | old_value04 | 参数值04 | varchar；字节长度 20 | 是 | CharField |
| PPName05 | old_ppname05 | 参数名5 | varchar；字节长度 20 | 是 | CharField |
| Value05 | old_value05 | 参数值05 | varchar；字节长度 20 | 是 | CharField |
| PPName06 | old_ppname06 | 参数名6 | varchar；字节长度 20 | 是 | CharField |
| Value06 | old_value06 | 参数值06 | varchar；字节长度 20 | 是 | CharField |
| PPName07 | old_ppname07 | 参数名7 | varchar；字节长度 20 | 是 | CharField |
| Value07 | old_value07 | 参数值07 | varchar；字节长度 20 | 是 | CharField |
| PPName08 | old_ppname08 | 参数名8 | varchar；字节长度 20 | 是 | CharField |
| Value08 | old_value08 | 参数值08 | varchar；字节长度 20 | 是 | CharField |
| PPName09 | old_ppname09 | 参数名9 | varchar；字节长度 20 | 是 | CharField |
| Value09 | old_value09 | 参数值09 | varchar；字节长度 20 | 是 | CharField |
| PPName10 | old_ppname10 | 参数名10 | varchar；字节长度 20 | 是 | CharField |
| Value10 | old_value10 | 参数值10 | varchar；字节长度 20 | 是 | CharField |
| PPName11 | old_ppname11 | 参数名11 | varchar；字节长度 20 | 是 | CharField |
| Value11 | old_value11 | 参数值11 | varchar；字节长度 20 | 是 | CharField |
| PPName12 | old_ppname12 | 参数名12 | varchar；字节长度 20 | 是 | CharField |
| Value12 | old_value12 | 参数值12 | varchar；字节长度 20 | 是 | CharField |
| PPName13 | old_ppname13 | 参数名13 | varchar；字节长度 20 | 是 | CharField |
| Value13 | old_value13 | 参数值13 | varchar；字节长度 20 | 是 | CharField |
| PPName14 | old_ppname14 | 参数名14 | varchar；字节长度 20 | 是 | CharField |
| Value14 | old_value14 | 参数值14 | varchar；字节长度 20 | 是 | CharField |
| PPName15 | old_ppname15 | 参数名15 | varchar；字节长度 20 | 是 | CharField |
| Value15 | old_value15 | 参数值15 | varchar；字节长度 20 | 是 | CharField |
| PPName16 | old_ppname16 | 参数名16 | varchar；字节长度 20 | 是 | CharField |
| Value16 | old_value16 | 参数值16 | varchar；字节长度 20 | 是 | CharField |
| PPName17 | old_ppname17 | 参数名17 | varchar；字节长度 20 | 是 | CharField |
| Value17 | old_value17 | 参数值17 | varchar；字节长度 20 | 是 | CharField |
| PPName18 | old_ppname18 | 参数名18 | varchar；字节长度 20 | 是 | CharField |
| Value18 | old_value18 | 参数值18 | varchar；字节长度 20 | 是 | CharField |
| PPName19 | old_ppname19 | 参数名19 | varchar；字节长度 20 | 是 | CharField |
| Value19 | old_value19 | 参数值19 | varchar；字节长度 20 | 是 | CharField |
| PPName20 | old_ppname20 | 参数名20 | varchar；字节长度 20 | 是 | CharField |
| Value20 | old_value20 | 参数值20 | varchar；字节长度 20 | 是 | CharField |
| PPName21 | old_ppname21 | 参数名21 | varchar；字节长度 20 | 是 | CharField |
| Value21 | old_value21 | 参数值21 | varchar；字节长度 20 | 是 | CharField |
| PPName22 | old_ppname22 | 参数名22 | varchar；字节长度 20 | 是 | CharField |
| Value22 | old_value22 | 参数值22 | varchar；字节长度 20 | 是 | CharField |
| PPName23 | old_ppname23 | 参数名23 | varchar；字节长度 20 | 是 | CharField |
| Value23 | old_value23 | 参数值23 | varchar；字节长度 20 | 是 | CharField |
| PPName24 | old_ppname24 | 参数名24 | varchar；字节长度 20 | 是 | CharField |
| Value24 | old_value24 | 参数值24 | varchar；字节长度 20 | 是 | CharField |
| PPName25 | old_ppname25 | 参数名25 | varchar；字节长度 20 | 是 | CharField |
| Value25 | old_value25 | 参数值25 | varchar；字节长度 20 | 是 | CharField |
| PPName26 | old_ppname26 | 参数名26 | varchar；字节长度 20 | 是 | CharField |
| Value26 | old_value26 | 参数值26 | varchar；字节长度 20 | 是 | CharField |
| PPName27 | old_ppname27 | 参数名27 | varchar；字节长度 20 | 是 | CharField |
| Value27 | old_value27 | 参数值27 | varchar；字节长度 20 | 是 | CharField |
| PPName28 | old_ppname28 | 参数名28 | varchar；字节长度 20 | 是 | CharField |
| Value28 | old_value28 | 参数值28 | varchar；字节长度 20 | 是 | CharField |
| PPName29 | old_ppname29 | 参数名29 | varchar；字节长度 20 | 是 | CharField |
| Value29 | old_value29 | 参数值29 | varchar；字节长度 20 | 是 | CharField |
| PPName30 | old_ppname30 | 参数名30 | varchar；字节长度 20 | 是 | CharField |
| Value30 | old_value30 | 参数值30 | varchar；字节长度 20 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| Maker | old_maker | 业务人 | varchar；字节长度 10 | 是 | CharField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| CardQty | old_card_qty | 缸数 | smallint | 是 | IntegerField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| PPName31 | old_ppname31 | PPName31 | varchar；字节长度 20 | 是 | CharField |
| Value31 | old_value31 | Value31 | varchar；字节长度 20 | 是 | CharField |
| PPName32 | old_ppname32 | PPName32 | varchar；字节长度 20 | 是 | CharField |
| Value32 | old_value32 | Value32 | varchar；字节长度 20 | 是 | CharField |
| PPName33 | old_ppname33 | PPName33 | varchar；字节长度 20 | 是 | CharField |
| Value33 | old_value33 | Value33 | varchar；字节长度 20 | 是 | CharField |
| PPName34 | old_ppname34 | PPName34 | varchar；字节长度 20 | 是 | CharField |
| Value34 | old_value34 | Value34 | varchar；字节长度 20 | 是 | CharField |
| PPName35 | old_ppname35 | PPName35 | varchar；字节长度 20 | 是 | CharField |
| Value35 | old_value35 | Value35 | varchar；字节长度 20 | 是 | CharField |
| PPName36 | old_ppname36 | PPName36 | varchar；字节长度 20 | 是 | CharField |
| Value36 | old_value36 | Value36 | varchar；字节长度 20 | 是 | CharField |
| PPName37 | old_ppname37 | PPName37 | varchar；字节长度 20 | 是 | CharField |
| Value37 | old_value37 | Value37 | varchar；字节长度 20 | 是 | CharField |
| PPName38 | old_ppname38 | PPName38 | varchar；字节长度 20 | 是 | CharField |
| Value38 | old_value38 | Value38 | varchar；字节长度 20 | 是 | CharField |
| PPName39 | old_ppname39 | PPName39 | varchar；字节长度 20 | 是 | CharField |
| Value39 | old_value39 | Value39 | varchar；字节长度 20 | 是 | CharField |
| PPName40 | old_ppname40 | PPName40 | varchar；字节长度 20 | 是 | CharField |
| Value40 | old_value40 | Value40 | varchar；字节长度 20 | 是 | CharField |
| PPName41 | old_ppname41 | PPName41 | varchar；字节长度 20 | 是 | CharField |
| Value41 | old_value41 | Value41 | varchar；字节长度 20 | 是 | CharField |
| PPName42 | old_ppname42 | PPName42 | varchar；字节长度 20 | 是 | CharField |
| Value42 | old_value42 | Value42 | varchar；字节长度 20 | 是 | CharField |
| PPName43 | old_ppname43 | PPName43 | varchar；字节长度 20 | 是 | CharField |
| Value43 | old_value43 | Value43 | varchar；字节长度 20 | 是 | CharField |
| PPName44 | old_ppname44 | PPName44 | varchar；字节长度 20 | 是 | CharField |
| Value44 | old_value44 | Value44 | varchar；字节长度 20 | 是 | CharField |
| PPName45 | old_ppname45 | PPName45 | varchar；字节长度 20 | 是 | CharField |
| Value45 | old_value45 | Value45 | varchar；字节长度 20 | 是 | CharField |
| PPName46 | old_ppname46 | PPName46 | varchar；字节长度 20 | 是 | CharField |
| Value46 | old_value46 | Value46 | varchar；字节长度 20 | 是 | CharField |
| PPName47 | old_ppname47 | PPName47 | varchar；字节长度 20 | 是 | CharField |
| Value47 | old_value47 | Value47 | varchar；字节长度 20 | 是 | CharField |
| PPName48 | old_ppname48 | PPName48 | varchar；字节长度 20 | 是 | CharField |
| Value48 | old_value48 | Value48 | varchar；字节长度 20 | 是 | CharField |
| PPName49 | old_ppname49 | PPName49 | varchar；字节长度 20 | 是 | CharField |
| Value49 | old_value49 | Value49 | varchar；字节长度 20 | 是 | CharField |
| PPName50 | old_ppname50 | PPName50 | varchar；字节长度 20 | 是 | CharField |
| Value50 | old_value50 | Value50 | varchar；字节长度 20 | 是 | CharField |
| PPName51 | old_ppname51 | PPName51 | varchar；字节长度 20 | 是 | CharField |
| Value51 | old_value51 | Value51 | varchar；字节长度 20 | 是 | CharField |
| PPName52 | old_ppname52 | PPName52 | varchar；字节长度 20 | 是 | CharField |
| Value52 | old_value52 | Value52 | varchar；字节长度 20 | 是 | CharField |
| PPName53 | old_ppname53 | PPName53 | varchar；字节长度 20 | 是 | CharField |
| Value53 | old_value53 | Value53 | varchar；字节长度 20 | 是 | CharField |
| PPName54 | old_ppname54 | PPName54 | varchar；字节长度 20 | 是 | CharField |
| Value54 | old_value54 | Value54 | varchar；字节长度 20 | 是 | CharField |
| PPName55 | old_ppname55 | PPName55 | varchar；字节长度 20 | 是 | CharField |
| Value55 | old_value55 | Value55 | varchar；字节长度 20 | 是 | CharField |
| PPName56 | old_ppname56 | PPName56 | varchar；字节长度 20 | 是 | CharField |
| Value56 | old_value56 | Value56 | varchar；字节长度 20 | 是 | CharField |
| PPName57 | old_ppname57 | PPName57 | varchar；字节长度 20 | 是 | CharField |
| Value57 | old_value57 | Value57 | varchar；字节长度 20 | 是 | CharField |
| PPName58 | old_ppname58 | PPName58 | varchar；字节长度 20 | 是 | CharField |
| Value58 | old_value58 | Value58 | varchar；字节长度 20 | 是 | CharField |
| PPName59 | old_ppname59 | PPName59 | varchar；字节长度 20 | 是 | CharField |
| Value59 | old_value59 | Value59 | varchar；字节长度 20 | 是 | CharField |
| PPName60 | old_ppname60 | PPName60 | varchar；字节长度 20 | 是 | CharField |
| Value60 | old_value60 | Value60 | varchar；字节长度 20 | 是 | CharField |
| PPName61 | old_ppname61 | PPName61 | varchar；字节长度 20 | 是 | CharField |
| Value61 | old_value61 | Value61 | varchar；字节长度 20 | 是 | CharField |
| PPName62 | old_ppname62 | PPName62 | varchar；字节长度 20 | 是 | CharField |
| Value62 | old_value62 | Value62 | varchar；字节长度 20 | 是 | CharField |
| PPName63 | old_ppname63 | PPName63 | varchar；字节长度 20 | 是 | CharField |
| Value63 | old_value63 | Value63 | varchar；字节长度 20 | 是 | CharField |
| PPName64 | old_ppname64 | PPName64 | varchar；字节长度 20 | 是 | CharField |
| Value64 | old_value64 | Value64 | varchar；字节长度 20 | 是 | CharField |
| PPName65 | old_ppname65 | PPName65 | varchar；字节长度 20 | 是 | CharField |
| Value65 | old_value65 | Value65 | varchar；字节长度 20 | 是 | CharField |
| PPName66 | old_ppname66 | PPName66 | varchar；字节长度 20 | 是 | CharField |
| Value66 | old_value66 | Value66 | varchar；字节长度 20 | 是 | CharField |
| PPName67 | old_ppname67 | PPName67 | varchar；字节长度 20 | 是 | CharField |
| Value67 | old_value67 | Value67 | varchar；字节长度 20 | 是 | CharField |
| PPName68 | old_ppname68 | PPName68 | varchar；字节长度 20 | 是 | CharField |
| Value68 | old_value68 | Value68 | varchar；字节长度 20 | 是 | CharField |
| PPName69 | old_ppname69 | PPName69 | varchar；字节长度 20 | 是 | CharField |
| Value69 | old_value69 | Value69 | varchar；字节长度 50 | 是 | CharField |
| PPName70 | old_ppname70 | PPName70 | varchar；字节长度 20 | 是 | CharField |
| Value70 | old_value70 | Value70 | varchar；字节长度 20 | 是 | CharField |
| AddrDlv | old_addr_dlv | 客户类型 | varchar；字节长度 50 | 是 | CharField |
| Model1 | old_model1 | 模板 | nchar；字节长度 20 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 50 | 是 | CharField |
| MachineID | old_machine_id | 机号 | varchar；字节长度 50 | 是 | CharField |
| DetailsCustomer | old_details_customer | 织厂 | nchar；字节长度 20 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |
| PreField2 | old_pre_field2 | 氨纶 | varchar；字节长度 50 | 是 | CharField |
| PreField3 | old_pre_field3 | 针数 | varchar；字节长度 50 | 是 | CharField |
| PreField4 | old_pre_field4 | 寸数 | varchar；字节长度 50 | 是 | CharField |
| WeightUnit | old_weight_unit | 克重单位 | varchar；字节长度 10 | 是 | CharField |
| WidthKindID | old_width_kind_id | 门幅单位 | varchar；字节长度 10 | 是 | CharField |
| OrderSheetDate | old_order_sheet_date | 下单时间 | datetime | 是 | DateTimeField |
| IsFirstVat | old_is_first_vat | 是否头缸 | bit | 是 | BooleanField |
| Atte | old_atte | Atte | varchar；字节长度 512 | 是 | CharField |
| OriSheetSeries | old_ori_sheet_series | OriSheetSeries | varchar；字节长度 20 | 是 | CharField |
| Date1 | old_date1 | 日期 | datetime | 是 | DateTimeField |
| Date2 | old_date2 | 日期 | datetime | 是 | DateTimeField |
| Class1 | old_class1 | 班次 | varchar；字节长度 20 | 是 | CharField |
| Class2 | old_class2 | 班次 | varchar；字节长度 20 | 是 | CharField |
| Person1 | old_person1 | Person1 | varchar；字节长度 20 | 是 | CharField |
| Person2 | old_person2 | Person2 | varchar；字节长度 20 | 是 | CharField |
| FProductWidth | old_fproduct_width | FProductWidth | varchar；字节长度 50 | 是 | CharField |
| FWeightOfLength | old_fweight_of_length | FWeightOfLength | varchar；字节长度 50 | 是 | CharField |
| PreRolls | old_pre_rolls | PreRolls | decimal(6,2) | 是 | DecimalField |

### SourceDyeProcessCraftJobNo — 染色工艺与配方相关表（ProcessCraftJobNo，待确认）

源表：`dye.ProcessCraftJobNo`；新表：`src_dye_processcraftjobno`；原主键：SheetSeries, JobSheetNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 否 | CharField |
| Status | old_status | 状态 | varchar；字节长度 1 | 是 | CharField |
| CurrTime | old_curr_time | 时间 | datetime | 是 | DateTimeField |
| Maker | old_maker | Maker | varchar；字节长度 10 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeProcessCraft`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ProcessCraftJobNo → ProcessCraft。

### SourceDyeProcessCraftOrderNo — 染色工艺与配方相关表（ProcessCraftOrderNo，待确认）

源表：`dye.ProcessCraftOrderNo`；新表：`src_dye_processcraftorderno`；原主键：SheetSeries, OrderSheetNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| OrderSheetNo | old_order_sheet_no | 订单号 | varchar；字节长度 20 | 否 | CharField |
| Status | old_status | 状态 | varchar；字节长度 1 | 是 | CharField |
| CurrTime | old_curr_time | 时间 | datetime | 是 | DateTimeField |
| Maker | old_maker | Maker | varchar；字节长度 10 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeProcessCraft`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ProcessCraftOrderNo → ProcessCraft。

### SourceDyeProcessSchedule — 染色工艺与配方相关表（ProcessSchedule，待确认）

源表：`dye.ProcessSchedule`；新表：`src_dye_processschedule`；原主键：ID。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | 自增ID | varchar；字节长度 50 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 20 | 是 | CharField |
| ProcessNo | old_process_no | 工序号 | tinyint | 是 | IntegerField |
| StationID | old_station_id | 站别 | varchar；字节长度 50 | 是 | CharField |
| ProcessID | old_process_id | 工序 | varchar；字节长度 10 | 是 | CharField |
| MachineID | old_machine_id | 机台 | varchar；字节长度 10 | 是 | CharField |
| SequenceNo | old_sequence_no | 顺序号 | bigint | 是 | BigIntegerField |
| Status | old_status | 状态 | varchar；字节长度 2 | 是 | CharField |
| PlanDate | old_plan_date | 时间 | datetime | 是 | DateTimeField |
| StartTime | old_start_time | 开始时间 | datetime | 是 | DateTimeField |
| FinishTime | old_finish_time | 结束时间 | datetime | 是 | DateTimeField |
| TargetMin | old_target_min | 预计分钟 | smallint | 是 | IntegerField |
| ShiftID | old_shift_id | 班组 | varchar；字节长度 10 | 是 | CharField |
| ClassID | old_class_id | 班别 | varchar；字节长度 10 | 是 | CharField |
| ProgramID | old_program_id | 前道流程 | varchar；字节长度 50 | 是 | CharField |
| EffiRate | old_effi_rate | 效率比例 | decimal(6,4) | 是 | DecimalField |
| JobSheetSeries | old_job_sheet_series | 工卡流水号 | varchar；字节长度 20 | 是 | CharField |
| RecipeSheetNo | old_recipe_sheet_no | 配方单号 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| CombineSheetNos | old_combine_sheet_nos | 合缸 | varchar；字节长度 200 | 是 | CharField |
| WorkSort | old_work_sort | WorkSort | varchar；字节长度 50 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 50 | 是 | CharField |
| ColorRGB | old_color_rgb | ColorRGB | int | 是 | IntegerField |
| PlanWeightQty | old_plan_weight_qty | 排产重量 | decimal(10,2) | 是 | DecimalField |
| PlanRolls | old_plan_rolls | 排产粒数 | decimal(7,2) | 是 | DecimalField |
| Priority | old_priority | Priority | int | 是 | IntegerField |
| SheetKind | old_sheet_kind | 排产类型 | smallint | 是 | IntegerField |
| StereotypesName | old_stereotypes_name | 缸位 | varchar；字节长度 20 | 是 | CharField |
| IsNot | old_is_not | 是否插队 | bit | 是 | BooleanField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |

### SourceDyeProcessSchedulebak — 染色工艺与配方相关表（ProcessSchedulebak，待确认）

源表：`dye.ProcessSchedulebak`；新表：`src_dye_processschedulebak`；原主键：ID。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | bigint | 否 | BigIntegerField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 20 | 是 | CharField |
| ProcessNo | old_process_no | ProcessNo | tinyint | 是 | IntegerField |
| StationID | old_station_id | StationID | varchar；字节长度 50 | 是 | CharField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 10 | 是 | CharField |
| MachineID | old_machine_id | MachineID | varchar；字节长度 10 | 是 | CharField |
| SequenceNo | old_sequence_no | SequenceNo | bigint | 是 | BigIntegerField |
| Status | old_status | Status | varchar；字节长度 2 | 是 | CharField |
| PlanDate | old_plan_date | PlanDate | datetime | 是 | DateTimeField |
| StartTime | old_start_time | StartTime | datetime | 是 | DateTimeField |
| FinishTime | old_finish_time | FinishTime | datetime | 是 | DateTimeField |
| TargetMin | old_target_min | TargetMin | smallint | 是 | IntegerField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 10 | 是 | CharField |
| ClassID | old_class_id | ClassID | varchar；字节长度 10 | 是 | CharField |
| ProgramID | old_program_id | ProgramID | varchar；字节长度 50 | 是 | CharField |
| EffiRate | old_effi_rate | EffiRate | decimal(6,4) | 是 | DecimalField |
| JobSheetSeries | old_job_sheet_series | JobSheetSeries | varchar；字节长度 20 | 是 | CharField |
| RecipeSheetNo | old_recipe_sheet_no | RecipeSheetNo | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |
| CombineSheetNos | old_combine_sheet_nos | CombineSheetNos | varchar；字节长度 200 | 是 | CharField |
| WorkSort | old_work_sort | WorkSort | varchar；字节长度 50 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 50 | 是 | CharField |
| ColorRGB | old_color_rgb | ColorRGB | int | 是 | IntegerField |

### SourceDyePStuffWeight — 染化料与称料库存相关表（PStuffWeight，待确认）

源表：`dye.PStuffWeight`；新表：`src_dye_pstuffweight`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 印花领料单号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| RecipeType | old_recipe_type | 料单类型 | tinyint | 是 | IntegerField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 10 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 10 | 是 | CharField |
| PrintSheetNo | old_print_sheet_no | 来源单号 | varchar；字节长度 50 | 是 | CharField |
| PrintCode | old_print_code | 花号 | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 150 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| PrintQty | old_print_qty | 印花数量 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |

### SourceDyePStuffWeightDetail — 染化料与称料库存相关表（PStuffWeightDetail，待确认）

源表：`dye.PStuffWeightDetail`；新表：`src_dye_pstuffweightdetail`；原主键：SheetSeries, PhaseNo, StuffNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| PhaseNo | old_phase_no | PhaseNo | tinyint | 否 | IntegerField |
| StuffNo | old_stuff_no | StuffNo | tinyint | 否 | IntegerField |
| StuffID | old_stuff_id | StuffID | varchar；字节长度 10 | 是 | CharField |
| StuffType | old_stuff_type | StuffType | varchar；字节长度 1 | 是 | CharField |
| Rate | old_rate | Rate | decimal(8,2) | 是 | DecimalField |
| UpPercent | old_up_percent | UpPercent | decimal(8,2) | 是 | DecimalField |
| DownPercent | old_down_percent | DownPercent | decimal(8,2) | 是 | DecimalField |
| WeightUnit | old_weight_unit | WeightUnit | varchar；字节长度 1 | 是 | CharField |
| Dosage | old_dosage | Dosage | decimal(15,6) | 是 | DecimalField |
| RecipeUnit | old_recipe_unit | RecipeUnit | tinyint | 是 | IntegerField |
| AddDosage | old_add_dosage | AddDosage | decimal(15,6) | 是 | DecimalField |
| DetailNote | old_detail_note | DetailNote | nvarchar；字节长度 512 | 是 | CharField |
| IsConfirmed | old_is_confirmed | IsConfirmed | bit | 是 | BooleanField |
| Status | old_status | Status | int | 是 | IntegerField |
| OriDosage | old_ori_dosage | OriDosage | decimal(15,6) | 是 | DecimalField |

### SourceDyePStuffWeightPhase — 染化料与称料库存相关表（PStuffWeightPhase，待确认）

源表：`dye.PStuffWeightPhase`；新表：`src_dye_pstuffweightphase`；原主键：SheetSeries, PhaseNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| PhaseNo | old_phase_no | 色位颜色序号 | tinyint | 否 | IntegerField |
| ColorPlateID | old_color_plate_id | 花号色位 | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | 颜色编号 | varchar；字节长度 500 | 是 | CharField |
| ColorName | old_color_name | 颜色名称 | varchar；字节长度 10 | 是 | CharField |
| Qty | old_qty | 色浆用量 | decimal(6,2) | 是 | DecimalField |
| Remarks | old_remarks | 颜色备注 | varchar；字节长度 512 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyePStuffWeight`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 PSupplementStuffWeightDetail → PSupplementStuffWeight；原界面主从 PNormalStuffWeightDetail → PNormalStuffWeight；原界面主从 PAddStuffWeightDetail → PAddStuffWeight。

### SourceDyeRecordEmp — 基础主数据相关表（RecordEmp，待确认）

源表：`dye.RecordEmp`；新表：`src_dye_recordemp`；原主键：无主键。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| BarCode | old_bar_code | 条码 | varchar；字节长度 20 | 否 | CharField |
| EmpID | old_emp_id | 业务员代码 | varchar；字节长度 10 | 否 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeRecordYield`；原码 `BarCode` → 父表原码 `Guid`；依据：原界面主从 QueryRecordEmp → QueryRecord。

### SourceDyeSemiOutWorkApply — 坯布半成品成品与仓储相关表（SemiOutWorkApply，待确认）

源表：`dye.SemiOutWorkApply`；新表：`src_dye_semioutworkapply`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 日期 | datetime | 是 | DateTimeField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| FactID | old_fact_id | 加工厂 | varchar；字节长度 20 | 是 | CharField |
| ProcessID | old_process_id | 加工项目 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1000 | 是 | CharField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| Creater | old_creater | 制单人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 制单日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审批人 | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | 审批时间 | datetime | 是 | DateTimeField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 100 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 20 | 是 | CharField |

### SourceDyeSemiOutWorkApplyDetail — 坯布半成品成品与仓储相关表（SemiOutWorkApplyDetail，待确认）

源表：`dye.SemiOutWorkApplyDetail`；新表：`src_dye_semioutworkapplydetail`；原主键：SheetSeries, DetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |
| JobTaskSheetNo | old_job_task_sheet_no | 卡号 | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 20 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 200 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| Packs | old_packs | 件数 | decimal(10,2) | 是 | DecimalField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| Qty | old_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1000 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| Price | old_price | 单价 | decimal(10,2) | 是 | DecimalField |
| Amount | old_amount | 金额 | decimal(12,2) | 是 | DecimalField |
| ReceSheetNo | old_rece_sheet_no | 入库明细单号 | varchar；字节长度 30 | 是 | CharField |
| InSheetKind | old_in_sheet_kind | 入库类别 | varchar；字节长度 10 | 是 | CharField |
| FixedQty | old_fixed_qty | 锭重 | decimal(5,2) | 是 | DecimalField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 50 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商 | varchar；字节长度 30 | 是 | CharField |
| PurchaseOrders | old_purchase_orders | 采购单号 | varchar；字节长度 20 | 是 | CharField |
| A_A | old_a_a | 物料区域 | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | A_B | varchar；字节长度 100 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 30 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 20 | 是 | CharField |
| ColorRemarks | old_color_remarks | 用途 | varchar；字节长度 200 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 200 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 200 | 是 | CharField |
| OrderSheetNo | old_order_sheet_no | 订单号 | varchar；字节长度 50 | 是 | CharField |
| OrderRemarks | old_order_remarks | 订单备注 | varchar；字节长度 200 | 是 | CharField |
| WorkMaterials | old_work_materials | 是否包工包料 | bit | 是 | BooleanField |

关联 `source_parent_1` → `erp_production.SourceDyeSemiOutWorkApply`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 SemiOutWorkApplyDetail → SemiOutWorkApply。

### SourceDyeShiftArrange — 生产工单与排程相关表（ShiftArrange，待确认）

源表：`dye.ShiftArrange`；新表：`src_dye_shiftarrange`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 单据流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 单号 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1000 | 是 | CharField |
| Creator | old_creator | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifier | old_modifier | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| ShiftID | old_shift_id | 默认班别 | varchar；字节长度 10 | 是 | CharField |
| StartTime | old_start_time | StartTime | datetime | 是 | DateTimeField |
| EndTime | old_end_time | EndTime | datetime | 是 | DateTimeField |
| SumShiftCount | old_sum_shift_count | SumShiftCount | int | 是 | IntegerField |

### SourceDyeShiftArrangeDetail — 生产工单与排程相关表（ShiftArrangeDetail，待确认）

源表：`dye.ShiftArrangeDetail`；新表：`src_dye_shiftarrangedetail`；原主键：DetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| Sheetseries | old_sheetseries | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |
| ShiftID | old_shift_id | 班组名称 | varchar；字节长度 10 | 是 | CharField |
| EmpID | old_emp_id | 员工 | varchar；字节长度 10 | 是 | CharField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 10 | 是 | CharField |
| Post | old_post | 岗位 | varchar；字节长度 30 | 是 | CharField |
| EffiRate | old_effi_rate | 比例 | decimal(6,2) | 是 | DecimalField |

### SourceDyeShiftPlan — 生产工单与排程相关表（ShiftPlan，待确认）

源表：`dye.ShiftPlan`；新表：`src_dye_shiftplan`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ClassID | old_class_id | 班组 | varchar；字节长度 10 | 是 | CharField |
| ShiftName | old_shift_name | 排班名称 | varchar；字节长度 60 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 50 | 否 | CharField |
| ShiftID | old_shift_id | 排班编码 | varchar；字节长度 20 | 否 | CharField |
| BeginDate | old_begin_date | 排班开始日期 | int | 否 | IntegerField |
| EndDate | old_end_date | 排班结束日期 | int | 否 | IntegerField |
| BeginTime | old_begin_time | 上班时间 | varchar；字节长度 20 | 是 | CharField |
| EndTime | old_end_time | 下班时间 | varchar；字节长度 20 | 是 | CharField |

### SourceDyeShiftPlanDetail — 生产工单与排程相关表（ShiftPlanDetail，待确认）

源表：`dye.ShiftPlanDetail`；新表：`src_dye_shiftplandetail`；原主键：DetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 50 | 否 | CharField |
| ShiftDay | old_shift_day | 日期 | varchar；字节长度 10 | 否 | CharField |
| BeginTime | old_begin_time | 上班时间 | varchar；字节长度 20 | 是 | CharField |
| EndTime | old_end_time | 下班时间 | varchar；字节长度 20 | 是 | CharField |
| IsHoliday | old_is_holiday | 是否假日 | bit | 是 | BooleanField |
| DetailNo | old_detail_no | 明细号 | varchar；字节长度 50 | 否 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeShiftPlan`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ShiftPlanDetail → ShiftPlan。

### SourceDyeStandCraft — 染色工艺与配方相关表（StandCraft，待确认）

源表：`dye.StandCraft`；新表：`src_dye_standcraft`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 120 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 200 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| ColorID | old_color_id | 颜色代码 | varchar；字节长度 20 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 10 | 是 | CharField |
| ProductionID | old_production_id | 生产工艺编码 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| Maker | old_maker | 业务人 | varchar；字节长度 10 | 是 | CharField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| CraftKindID | old_craft_kind_id | 工艺类别 | varchar；字节长度 10 | 是 | CharField |
| Structure | old_structure | 组织 | varchar；字节长度 50 | 是 | CharField |
| WeftDensity | old_weft_density | WeftDensity | varchar；字节长度 32 | 是 | CharField |
| WarpDensity | old_warp_density | WarpDensity | varchar；字节长度 32 | 是 | CharField |
| Weight | old_weight | Weight | decimal(6,2) | 是 | DecimalField |
| Width | old_width | Width | varchar；字节长度 32 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 16 | 是 | CharField |

### SourceDyeStandCraftBeforeDetail — 染色工艺与配方相关表（StandCraftBeforeDetail，待确认）

源表：`dye.StandCraftBeforeDetail`；新表：`src_dye_standcraftbeforedetail`；原主键：SheetSeries, ProcessNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| ProcessNo | old_process_no | ProcessNo | tinyint | 否 | IntegerField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 10 | 是 | CharField |
| StationID | old_station_id | StationID | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| MachineID | old_machine_id | MachineID | varchar；字节长度 10 | 是 | CharField |
| LastTime | old_last_time | LastTime | smallint | 是 | IntegerField |
| PPName01 | old_ppname01 | PPName01 | varchar；字节长度 20 | 是 | CharField |
| Value01 | old_value01 | Value01 | varchar；字节长度 20 | 是 | CharField |
| PPName02 | old_ppname02 | PPName02 | varchar；字节长度 20 | 是 | CharField |
| Value02 | old_value02 | Value02 | varchar；字节长度 20 | 是 | CharField |
| PPName03 | old_ppname03 | PPName03 | varchar；字节长度 20 | 是 | CharField |
| Value03 | old_value03 | Value03 | varchar；字节长度 20 | 是 | CharField |
| PPName04 | old_ppname04 | PPName04 | varchar；字节长度 20 | 是 | CharField |
| Value04 | old_value04 | Value04 | varchar；字节长度 20 | 是 | CharField |
| PPName05 | old_ppname05 | PPName05 | varchar；字节长度 20 | 是 | CharField |
| Value05 | old_value05 | Value05 | varchar；字节长度 20 | 是 | CharField |
| PPName06 | old_ppname06 | PPName06 | varchar；字节长度 20 | 是 | CharField |
| Value06 | old_value06 | Value06 | varchar；字节长度 20 | 是 | CharField |
| PPName07 | old_ppname07 | PPName07 | varchar；字节长度 20 | 是 | CharField |
| Value07 | old_value07 | Value07 | varchar；字节长度 20 | 是 | CharField |
| PPName08 | old_ppname08 | PPName08 | varchar；字节长度 20 | 是 | CharField |
| Value08 | old_value08 | Value08 | varchar；字节长度 20 | 是 | CharField |
| PPName09 | old_ppname09 | PPName09 | varchar；字节长度 20 | 是 | CharField |
| Value09 | old_value09 | Value09 | varchar；字节长度 20 | 是 | CharField |
| PPName10 | old_ppname10 | PPName10 | varchar；字节长度 20 | 是 | CharField |
| Value10 | old_value10 | Value10 | varchar；字节长度 20 | 是 | CharField |
| PPName11 | old_ppname11 | PPName11 | varchar；字节长度 20 | 是 | CharField |
| Value11 | old_value11 | Value11 | varchar；字节长度 20 | 是 | CharField |
| PPName12 | old_ppname12 | PPName12 | varchar；字节长度 20 | 是 | CharField |
| Value12 | old_value12 | Value12 | varchar；字节长度 20 | 是 | CharField |
| PPName13 | old_ppname13 | PPName13 | varchar；字节长度 20 | 是 | CharField |
| Value13 | old_value13 | Value13 | varchar；字节长度 20 | 是 | CharField |
| PPName14 | old_ppname14 | PPName14 | varchar；字节长度 20 | 是 | CharField |
| Value14 | old_value14 | Value14 | varchar；字节长度 20 | 是 | CharField |
| PPName15 | old_ppname15 | PPName15 | varchar；字节长度 20 | 是 | CharField |
| Value15 | old_value15 | Value15 | varchar；字节长度 20 | 是 | CharField |
| PPName16 | old_ppname16 | PPName16 | varchar；字节长度 20 | 是 | CharField |
| Value16 | old_value16 | Value16 | varchar；字节长度 20 | 是 | CharField |
| PPName17 | old_ppname17 | PPName17 | varchar；字节长度 20 | 是 | CharField |
| Value17 | old_value17 | Value17 | varchar；字节长度 20 | 是 | CharField |
| PPName18 | old_ppname18 | PPName18 | varchar；字节长度 20 | 是 | CharField |
| Value18 | old_value18 | Value18 | varchar；字节长度 20 | 是 | CharField |
| PPName19 | old_ppname19 | PPName19 | varchar；字节长度 20 | 是 | CharField |
| Value19 | old_value19 | Value19 | varchar；字节长度 20 | 是 | CharField |
| PPName20 | old_ppname20 | PPName20 | varchar；字节长度 20 | 是 | CharField |
| Value20 | old_value20 | Value20 | varchar；字节长度 20 | 是 | CharField |
| Status | old_status | Status | varchar；字节长度 2 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |

### SourceDyeStandCraftDetail — 染色工艺与配方相关表（StandCraftDetail，待确认）

源表：`dye.StandCraftDetail`；新表：`src_dye_standcraftdetail`；原主键：SheetSeries, ProcessNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 120 | 否 | CharField |
| ProcessNo | old_process_no | 工序号 | tinyint | 否 | IntegerField |
| ProcessID | old_process_id | 工序代码 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| MachineID | old_machine_id | 机台编码 | varchar；字节长度 10 | 是 | CharField |
| PPName01 | old_ppname01 | 参数名1 | varchar；字节长度 20 | 是 | CharField |
| Value01 | old_value01 | 标准值01 | varchar；字节长度 20 | 是 | CharField |
| PPName02 | old_ppname02 | 参数名2 | varchar；字节长度 20 | 是 | CharField |
| Value02 | old_value02 | 标准值02 | varchar；字节长度 20 | 是 | CharField |
| PPName03 | old_ppname03 | 参数名3 | varchar；字节长度 20 | 是 | CharField |
| Value03 | old_value03 | 标准值03 | varchar；字节长度 20 | 是 | CharField |
| PPName04 | old_ppname04 | 参数名4 | varchar；字节长度 20 | 是 | CharField |
| Value04 | old_value04 | 标准值04 | varchar；字节长度 20 | 是 | CharField |
| PPName05 | old_ppname05 | 参数名5 | varchar；字节长度 20 | 是 | CharField |
| Value05 | old_value05 | 标准值05 | varchar；字节长度 20 | 是 | CharField |
| PPName06 | old_ppname06 | 参数名6 | varchar；字节长度 20 | 是 | CharField |
| Value06 | old_value06 | 标准值06 | varchar；字节长度 20 | 是 | CharField |
| PPName07 | old_ppname07 | 参数名7 | varchar；字节长度 20 | 是 | CharField |
| Value07 | old_value07 | 标准值07 | varchar；字节长度 20 | 是 | CharField |
| PPName08 | old_ppname08 | 参数名8 | varchar；字节长度 20 | 是 | CharField |
| Value08 | old_value08 | 标准值08 | varchar；字节长度 20 | 是 | CharField |
| PPName09 | old_ppname09 | 参数名9 | varchar；字节长度 20 | 是 | CharField |
| Value09 | old_value09 | 标准值09 | varchar；字节长度 20 | 是 | CharField |
| PPName10 | old_ppname10 | 参数名10 | varchar；字节长度 20 | 是 | CharField |
| Value10 | old_value10 | 标准值10 | varchar；字节长度 20 | 是 | CharField |
| PPName11 | old_ppname11 | 参数名11 | varchar；字节长度 20 | 是 | CharField |
| Value11 | old_value11 | 标准值11 | varchar；字节长度 20 | 是 | CharField |
| PPName12 | old_ppname12 | 参数名12 | varchar；字节长度 20 | 是 | CharField |
| Value12 | old_value12 | 标准值12 | varchar；字节长度 20 | 是 | CharField |
| PPName13 | old_ppname13 | 参数名13 | varchar；字节长度 20 | 是 | CharField |
| Value13 | old_value13 | 标准值13 | varchar；字节长度 20 | 是 | CharField |
| PPName14 | old_ppname14 | 参数名14 | varchar；字节长度 20 | 是 | CharField |
| Value14 | old_value14 | 标准值14 | varchar；字节长度 20 | 是 | CharField |
| PPName15 | old_ppname15 | 参数名15 | varchar；字节长度 20 | 是 | CharField |
| Value15 | old_value15 | 标准值15 | varchar；字节长度 20 | 是 | CharField |
| PPName16 | old_ppname16 | 参数名16 | varchar；字节长度 20 | 是 | CharField |
| Value16 | old_value16 | 标准值16 | varchar；字节长度 20 | 是 | CharField |
| PPName17 | old_ppname17 | 参数名17 | varchar；字节长度 20 | 是 | CharField |
| Value17 | old_value17 | 标准值17 | varchar；字节长度 20 | 是 | CharField |
| PPName18 | old_ppname18 | 参数名18 | varchar；字节长度 20 | 是 | CharField |
| Value18 | old_value18 | 标准值18 | varchar；字节长度 20 | 是 | CharField |
| PPName19 | old_ppname19 | 参数名19 | varchar；字节长度 20 | 是 | CharField |
| Value19 | old_value19 | 标准值19 | varchar；字节长度 20 | 是 | CharField |
| PPName20 | old_ppname20 | 参数名20 | varchar；字节长度 20 | 是 | CharField |
| Value20 | old_value20 | 标准值20 | varchar；字节长度 20 | 是 | CharField |
| Status | old_status | 状态 | varchar；字节长度 1 | 是 | CharField |
| StationID | old_station_id | 站别代码 | varchar；字节长度 10 | 是 | CharField |
| LastTime | old_last_time | LastTime | smallint | 是 | IntegerField |

关联 `source_parent_1` → `erp_production.SourceDyeStandCraft`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 StandCraftDetail → StandCraft。

### SourceDyeStandCraftJobNo — 染色工艺与配方相关表（StandCraftJobNo，待确认）

源表：`dye.StandCraftJobNo`；新表：`src_dye_standcraftjobno`；原主键：SheetSeries, JobSheetNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 否 | CharField |
| Status | old_status | 状态 | varchar；字节长度 1 | 是 | CharField |
| CurrTime | old_curr_time | 当前时间 | datetime | 是 | DateTimeField |
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| Maker | old_maker | 制单人 | varchar；字节长度 10 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeStandCraft`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 StandCraftJobNo → StandCraft。

### SourceDyeSterotypeTech — 其他或待确认相关表（SterotypeTech，待确认）

源表：`dye.SterotypeTech`；新表：`src_dye_sterotypetech`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 30 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 20 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| WeightQtyOrRolls | old_weight_qty_or_rolls | 重量/缸数 | varchar；字节长度 20 | 是 | CharField |
| TechColorNum | old_tech_color_num | 工艺色号 | varchar；字节长度 20 | 是 | CharField |
| Width | old_width | Width | varchar；字节长度 20 | 是 | CharField |
| Weight | old_weight | Weight | varchar；字节长度 20 | 是 | CharField |
| AddrDlv | old_addr_dlv | 织纱厂名 | varchar；字节长度 100 | 是 | CharField |
| ProductionID | old_production_id | 工艺路线 | varchar；字节长度 100 | 是 | CharField |
| DQDataWidth | old_dqdata_width | 定前资料幅宽 | varchar；字节长度 20 | 是 | CharField |
| DQDataWeight | old_dqdata_weight | 定前资料克重 | varchar；字节长度 20 | 是 | CharField |
| DQDataNumber | old_dqdata_number | 定前资料线数 | varchar；字节长度 20 | 是 | CharField |
| DQDataXHWidth | old_dqdata_xhwidth | 定前资料洗后幅宽 | varchar；字节长度 20 | 是 | CharField |
| DQDataXHWeight | old_dqdata_xhweight | 定前资料洗后克重 | varchar；字节长度 20 | 是 | CharField |
| DQDataXHNumber | old_dqdata_xhnumber | 定前资料洗后线数 | varchar；字节长度 20 | 是 | CharField |
| HGTechTemperature | old_hgtech_temperature | 烘干工艺温度 | varchar；字节长度 20 | 是 | CharField |
| HGTechSpeed | old_hgtech_speed | 烘干工艺车速 | varchar；字节长度 20 | 是 | CharField |
| HGTechQty | old_hgtech_qty | 烘干工艺张力 | varchar；字节长度 20 | 是 | CharField |
| HGTechWindPower | old_hgtech_wind_power | 烘干工艺风力 | varchar；字节长度 20 | 是 | CharField |
| HGTechSmoke | old_hgtech_smoke | 烘干工艺排烟 | varchar；字节长度 20 | 是 | CharField |
| HGTechBrush | old_hgtech_brush | 烘干工艺毛刷 | varchar；字节长度 20 | 是 | CharField |
| HGTechOverfeeding | old_hgtech_overfeeding | 烘干工艺超喂 | varchar；字节长度 20 | 是 | CharField |
| QDTechTemperature | old_qdtech_temperature | 定前工艺温度 | varchar；字节长度 20 | 是 | CharField |
| QDTechSpeed | old_qdtech_speed | 定前工艺车速 | varchar；字节长度 20 | 是 | CharField |
| QDTechQty | old_qdtech_qty | 定前工艺张力 | varchar；字节长度 20 | 是 | CharField |
| QDTechWindPower | old_qdtech_wind_power | 定前工艺风力 | varchar；字节长度 20 | 是 | CharField |
| QDTechSmoke | old_qdtech_smoke | 定前工艺排烟 | varchar；字节长度 20 | 是 | CharField |
| QDTechBrush | old_qdtech_brush | 定前工艺毛刷 | varchar；字节长度 20 | 是 | CharField |
| QDTechOverfeeding | old_qdtech_overfeeding | 定前工艺超喂 | varchar；字节长度 20 | 是 | CharField |
| QDTechJJWidth | old_qdtech_jjwidth | 定前工艺机架幅宽 | varchar；字节长度 20 | 是 | CharField |
| QDTechSJNumber | old_qdtech_sjnumber | 定前工艺上级线数 | varchar；字节长度 20 | 是 | CharField |
| QDTechXJWidth | old_qdtech_xjwidth | 定前工艺下机幅宽 | varchar；字节长度 20 | 是 | CharField |
| QDTechXJNumber | old_qdtech_xjnumber | 定前工艺下机线数 | varchar；字节长度 20 | 是 | CharField |
| QDTechWeight | old_qdtech_weight | 定前工艺克重 | varchar；字节长度 20 | 是 | CharField |
| QDTechAuxiliary | old_qdtech_auxiliary | 定前工艺助剂 | varchar；字节长度 100 | 是 | CharField |
| CDTechTemperature | old_cdtech_temperature | 成定工艺温度 | varchar；字节长度 20 | 是 | CharField |
| CDTechSpeed | old_cdtech_speed | 成定工艺车速 | varchar；字节长度 20 | 是 | CharField |
| CDTechQty | old_cdtech_qty | 成定工艺张力 | varchar；字节长度 20 | 是 | CharField |
| CDTechWindPower | old_cdtech_wind_power | 成定工艺风力 | varchar；字节长度 20 | 是 | CharField |
| CDTechSmoke | old_cdtech_smoke | 成定工艺排烟 | varchar；字节长度 20 | 是 | CharField |
| CDTechBrush | old_cdtech_brush | 成定工艺毛刷 | varchar；字节长度 20 | 是 | CharField |
| CDTechOverfeeding | old_cdtech_overfeeding | 成定工艺超喂 | varchar；字节长度 20 | 是 | CharField |
| CDTechDQWidth | old_cdtech_dqwidth | 成定工艺定前幅宽 | varchar；字节长度 20 | 是 | CharField |
| CDTechJJWidth | old_cdtech_jjwidth | 成定工艺机架幅宽 | varchar；字节长度 20 | 是 | CharField |
| CDTechSJNumber | old_cdtech_sjnumber | 成定工艺上机线数 | varchar；字节长度 20 | 是 | CharField |
| CDTechXJWidth | old_cdtech_xjwidth | 成定工艺下机幅宽 | varchar；字节长度 20 | 是 | CharField |
| CDTechXJNumber | old_cdtech_xjnumber | 成定工艺下机线数 | varchar；字节长度 20 | 是 | CharField |
| CDTechWeight | old_cdtech_weight | 成定工艺克重 | varchar；字节长度 20 | 是 | CharField |
| CDTechAuxiliary | old_cdtech_auxiliary | 成定工艺助剂 | varchar；字节长度 100 | 是 | CharField |
| Demand | old_demand | 客户要求 | nvarchar；字节长度 1600 | 是 | CharField |
| Remarks | old_remarks | 备注信息 | nvarchar；字节长度 1000 | 是 | CharField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |

### SourceDyeStuffCombineSheets — 染化料与称料库存相关表（StuffCombineSheets，待确认）

源表：`dye.StuffCombineSheets`；新表：`src_dye_stuffcombinesheets`；原主键：无主键。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| StuffSheetNo | old_stuff_sheet_no | StuffSheetNo | varchar；字节长度 30 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 30 | 是 | CharField |

### SourceDyeStuffDeptApply — 染化料与称料库存相关表（StuffDeptApply，待确认）

源表：`dye.StuffDeptApply`；新表：`src_dye_stuffdeptapply`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |

### SourceDyeStuffDeptApplyDetail — 染化料与称料库存相关表（StuffDeptApplyDetail，待确认）

源表：`dye.StuffDeptApplyDetail`；新表：`src_dye_stuffdeptapplydetail`；原主键：SheetSeries, DetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 20 | 否 | CharField |
| DeptSheetNo | old_dept_sheet_no | DeptSheetNo | varchar；字节长度 30 | 是 | CharField |
| Name | old_name | Name | varchar；字节长度 50 | 是 | CharField |
| StuffID | old_stuff_id | StuffID | varchar；字节长度 30 | 是 | CharField |
| StuffKindID | old_stuff_kind_id | StuffKindID | varchar；字节长度 30 | 是 | CharField |
| Unit | old_unit | Unit | varchar；字节长度 40 | 是 | CharField |
| Qty | old_qty | Qty | decimal(10,2) | 是 | DecimalField |
| Amount | old_amount | Amount | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 30 | 是 | CharField |
| ApplySheetNo | old_apply_sheet_no | ApplySheetNo | varchar；字节长度 40 | 是 | CharField |

### SourceDyeStuffOutApply — 染化料与称料库存相关表（StuffOutApply，待确认）

源表：`dye.StuffOutApply`；新表：`src_dye_stuffoutapply`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 否 | CharField |
| Applyer | old_applyer | Applyer | varchar；字节长度 20 | 是 | CharField |
| ApplyDept | old_apply_dept | ApplyDept | varchar；字节长度 30 | 是 | CharField |
| ApplyFactory | old_apply_factory | ApplyFactory | varchar；字节长度 30 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| UseInfo | old_use_info | UseInfo | varchar；字节长度 512 | 是 | CharField |

### SourceDyeStuffOutApplyDetail — 染化料与称料库存相关表（StuffOutApplyDetail，待确认）

源表：`dye.StuffOutApplyDetail`；新表：`src_dye_stuffoutapplydetail`；原主键：SheetSeries, DetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 20 | 否 | CharField |
| Name | old_name | Name | varchar；字节长度 50 | 是 | CharField |
| StuffID | old_stuff_id | StuffID | varchar；字节长度 30 | 是 | CharField |
| StuffKindID | old_stuff_kind_id | StuffKindID | varchar；字节长度 30 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 100 | 是 | CharField |
| Unit | old_unit | Unit | varchar；字节长度 40 | 是 | CharField |
| Qty | old_qty | Qty | decimal(10,2) | 是 | DecimalField |
| Amount | old_amount | Amount | decimal(10,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| KCQty | old_kcqty | KCQty | decimal(10,2) | 是 | DecimalField |

### SourceDyeStuffWeight — 称料/配料主单

源表：`dye.StuffWeight`；新表：`src_dye_stuffweight`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 称料单号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| RecipeType | old_recipe_type | 配方类型 | tinyint | 是 | IntegerField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 10 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户名称 | varchar；字节长度 10 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 150 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 -1 | 是 | TextField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| ClothQtyKg | old_cloth_qty_kg | 胚重 | decimal(10,2) | 是 | DecimalField |
| SubRate | old_sub_rate | 减量率 | decimal(5,3) | 是 | DecimalField |
| ClothNetKg | old_cloth_net_kg | 胚纱净重 | decimal(10,2) | 是 | DecimalField |
| Cost | old_cost | 成本 | decimal(10,2) | 是 | DecimalField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(16,6) | 是 | DecimalField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| RecipeSheetNo | old_recipe_sheet_no | 配方单号 | varchar；字节长度 20 | 是 | CharField |
| ProcessID | old_process_id | 工序名称 | varchar；字节长度 50 | 是 | CharField |
| Receiver | old_receiver | 接收人 | varchar；字节长度 10 | 是 | CharField |
| FinishDate | old_finish_date | 最后领料日期 | datetime | 是 | DateTimeField |
| IsFirstVat | old_is_first_vat | 是否头缸 | bit | 是 | BooleanField |
| WareHouseID | old_ware_house_id | 仓库名称 | varchar；字节长度 10 | 是 | CharField |
| ShiftID | old_shift_id | 班别 | varchar；字节长度 10 | 是 | CharField |
| MachineNo | old_machine_no | 机台 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改人 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| WeighterID | old_weighter_id | WeighterID | varchar；字节长度 10 | 是 | CharField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| StandRecipeNo | old_stand_recipe_no | StandRecipeNo | varchar；字节长度 20 | 是 | CharField |
| Width | old_width | 幅宽 | varchar；字节长度 80 | 是 | CharField |
| StartTime | old_start_time | StartTime | datetime | 是 | DateTimeField |
| CompleteTime | old_complete_time | CompleteTime | datetime | 是 | DateTimeField |
| LastTime | old_last_time | LastTime | datetime | 是 | DateTimeField |
| Speed | old_speed | Speed | decimal(8,2) | 是 | DecimalField |
| Pressure1 | old_pressure1 | Pressure1 | decimal(10,2) | 是 | DecimalField |
| Pressure2 | old_pressure2 | Pressure2 | decimal(10,2) | 是 | DecimalField |
| Pressure3 | old_pressure3 | Pressure3 | decimal(10,2) | 是 | DecimalField |
| Weight1 | old_weight1 | Weight1 | decimal(6,2) | 是 | DecimalField |
| Weight2 | old_weight2 | Weight2 | decimal(6,2) | 是 | DecimalField |
| Weight3 | old_weight3 | Weight3 | decimal(6,2) | 是 | DecimalField |
| Moisture1 | old_moisture1 | Moisture1 | decimal(5,3) | 是 | DecimalField |
| Moisture2 | old_moisture2 | Moisture2 | decimal(5,3) | 是 | DecimalField |
| Moisture3 | old_moisture3 | Moisture3 | decimal(5,3) | 是 | DecimalField |
| TakeRate1 | old_take_rate1 | TakeRate1 | decimal(5,3) | 是 | DecimalField |
| TakeRate2 | old_take_rate2 | TakeRate2 | decimal(5,3) | 是 | DecimalField |
| TakeRate3 | old_take_rate3 | TakeRate3 | decimal(5,3) | 是 | DecimalField |
| Weight | old_weight | 克重 | varchar；字节长度 80 | 是 | CharField |
| CombineSheetNos | old_combine_sheet_nos | CombineSheetNos | varchar；字节长度 -1 | 是 | TextField |
| RecipeCreater | old_recipe_creater | RecipeCreater | varchar；字节长度 20 | 是 | CharField |
| ColorE | old_color_e | ColorE | varchar；字节长度 500 | 是 | CharField |
| LengthQty | old_length_qty | LengthQty | varchar；字节长度 50 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 500 | 是 | CharField |
| PreField3 | old_pre_field3 | 干纱工艺 | varchar；字节长度 500 | 是 | CharField |
| StationID | old_station_id | StationID | varchar；字节长度 10 | 是 | CharField |
| Rate | old_rate | Rate | decimal(10,2) | 是 | DecimalField |
| JobKindID | old_job_kind_id | JobKindID | varchar；字节长度 10 | 是 | CharField |
| CostMoney | old_cost_money | 金额 | decimal(10,2) | 是 | DecimalField |
| BathRatio | old_bath_ratio | BathRatio | decimal(6,2) | 是 | DecimalField |
| DivideQty | old_divide_qty | DivideQty | decimal(8,2) | 是 | DecimalField |
| CustColorNum | old_cust_color_num | CustColorNum | varchar；字节长度 100 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 250 | 是 | CharField |
| MachineTypeID | old_machine_type_id | MachineTypeID | tinyint | 是 | IntegerField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 50 | 是 | CharField |
| ColorMatching | old_color_matching | 对色员 | varchar；字节长度 20 | 是 | CharField |
| DyeEmpID | old_dye_emp_id | 看缸员 | varchar；字节长度 50 | 是 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 50 | 是 | CharField |
| Votl | old_votl | Votl | float | 是 | FloatField |
| MachineId | old_machine_id | 中控机台 | int | 是 | IntegerField |
| PreField2 | old_pre_field2 | 成定工艺 | varchar；字节长度 500 | 是 | CharField |
| PreField4 | old_pre_field4 | 预缩工艺 | varchar；字节长度 500 | 是 | CharField |
| GYYQ | old_gyyq | 工艺要求 | varchar；字节长度 1000 | 是 | CharField |
| AddColorNum | old_add_color_num | 加色次数 | int | 是 | IntegerField |
| WProcessNo | old_wprocess_no | 复版完成编码 | varchar；字节长度 20 | 是 | CharField |

### SourceDyeStuffWeightDetail — 称料/配料明细

源表：`dye.StuffWeightDetail`；新表：`src_dye_stuffweightdetail`；原主键：SheetSeries, PhaseNo, StuffNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| PhaseNo | old_phase_no | PhaseNo | tinyint | 否 | IntegerField |
| StuffNo | old_stuff_no | StuffNo | tinyint | 否 | IntegerField |
| StuffID | old_stuff_id | StuffID | varchar；字节长度 10 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 是 | CharField |
| StuffType | old_stuff_type | StuffType | varchar；字节长度 1 | 是 | CharField |
| Price | old_price | Price | decimal(16,6) | 是 | DecimalField |
| WeightUnit | old_weight_unit | WeightUnit | varchar；字节长度 1 | 是 | CharField |
| Dosage | old_dosage | Dosage | decimal(15,6) | 是 | DecimalField |
| RecipeUnit | old_recipe_unit | RecipeUnit | tinyint | 是 | IntegerField |
| NeedQty | old_need_qty | NeedQty | decimal(12,4) | 是 | DecimalField |
| RealQty | old_real_qty | RealQty | decimal(10,2) | 是 | DecimalField |
| NeedMoney | old_need_money | NeedMoney | decimal(10,2) | 是 | DecimalField |
| RealMoney | old_real_money | RealMoney | decimal(10,2) | 是 | DecimalField |
| OutTime | old_out_time | OutTime | datetime | 是 | DateTimeField |
| IsConfirmed | old_is_confirmed | IsConfirmed | bit | 是 | BooleanField |
| DetailNote | old_detail_note | DetailNote | nvarchar；字节长度 512 | 是 | CharField |
| AddScale | old_add_scale | AddScale | decimal(10,4) | 是 | DecimalField |
| Status | old_status | Status | int | 是 | IntegerField |
| AddQty | old_add_qty | AddQty | decimal(10,0) | 是 | DecimalField |
| OriNeedQty | old_ori_need_qty | OriNeedQty | decimal(12,4) | 是 | DecimalField |
| OutDate | old_out_date | OutDate | varchar；字节长度 20 | 是 | CharField |
| AddDosage | old_add_dosage | AddDosage | decimal(15,6) | 是 | DecimalField |
| AddNeedQty | old_add_need_qty | AddNeedQty | decimal(12,4) | 是 | DecimalField |
| Money | old_money | Money | decimal(10,2) | 是 | DecimalField |
| CarryIndex | old_carry_index | CarryIndex | varchar；字节长度 20 | 是 | CharField |
| StepName | old_step_name | StepName | varchar；字节长度 50 | 是 | CharField |
| StepNo | old_step_no | StepNo | varchar；字节长度 50 | 是 | CharField |
| IsFinished | old_is_finished | IsFinished | int | 是 | IntegerField |
| AutoSysIDs | old_auto_sys_ids | AutoSysIDs | varchar；字节长度 10 | 是 | CharField |
| OirDosage | old_oir_dosage | OirDosage | decimal(15,6) | 是 | DecimalField |
| AdjustDosage | old_adjust_dosage | AdjustDosage | decimal(15,6) | 是 | DecimalField |

### SourceDyeStuffWeightJobSheetNo — 染化料与称料库存相关表（StuffWeightJobSheetNo，待确认）

源表：`dye.StuffWeightJobSheetNo`；新表：`src_dye_stuffweightjobsheetno`；原主键：AutoID。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| AutoID | old_auto_id | AutoID | int | 否 | IntegerField |
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 是 | CharField |
| CLSheetNo | old_clsheet_no | CLSheetNo | varchar；字节长度 50 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| AllJobSheetNo | old_all_job_sheet_no | AllJobSheetNo | varchar；字节长度 200 | 是 | CharField |
| SumAssignedRolls | old_sum_assigned_rolls | SumAssignedRolls | decimal(8,2) | 是 | DecimalField |
| SumAssignedWeightQty | old_sum_assigned_weight_qty | SumAssignedWeightQty | decimal(8,2) | 是 | DecimalField |
| Rolls | old_rolls | Rolls | decimal(8,2) | 是 | DecimalField |
| ClothQtyKg | old_cloth_qty_kg | ClothQtyKg | decimal(8,2) | 是 | DecimalField |
| Rate | old_rate | Rate | decimal(6,4) | 是 | DecimalField |
| SumAssignedLengthQty | old_sum_assigned_length_qty | SumAssignedLengthQty | decimal(8,2) | 是 | DecimalField |
| LengthQty | old_length_qty | LengthQty | decimal(8,2) | 是 | DecimalField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 200 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 100 | 是 | CharField |

### SourceDyeStuffWeightPhase — 染化料与称料库存相关表（StuffWeightPhase，待确认）

源表：`dye.StuffWeightPhase`；新表：`src_dye_stuffweightphase`；原主键：SheetSeries, PhaseNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 明细流水号 | varchar；字节长度 20 | 否 | CharField |
| PhaseNo | old_phase_no | 序号 | tinyint | 否 | IntegerField |
| PhaseID | old_phase_id | 染程名称 | varchar；字节长度 10 | 是 | CharField |
| BathRatio | old_bath_ratio | 浴比 | decimal(6,2) | 是 | DecimalField |
| ProgramID | old_program_id | 工艺编码 | varchar；字节长度 10 | 是 | CharField |
| PH | old_ph | PH值 | varchar；字节长度 10 | 是 | CharField |
| WaterQty | old_water_qty | 水量 | decimal(10,2) | 是 | DecimalField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Minutes | old_minutes | 分钟 | decimal(10,2) | 是 | DecimalField |
| Temperature | old_temperature | 温度 | decimal(5,1) | 是 | DecimalField |
| MachineTypeID | old_machine_type_id | MachineTypeID | varchar；字节长度 50 | 是 | CharField |
| StepIndex | old_step_index | StepIndex | varchar；字节长度 250 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeStuffWeight`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 StuffWeightPhaseDetail → StuffWeight；原界面主从 ProcessStuffWeightPhaseDetail → ProcessStuffWeight；原界面主从 NormalStuffWeightPhaseDetail → NormalStuffWeight；原界面主从 AddStuffWeightPhaseDetail → AddStuffWeight；原界面主从 ReworkStuffWeightPhaseDetail → ReworkStuffWeight；原界面主从 WashProcessStuffWeightPhaseDetail → WashProcessStuffWeight；原界面主从 SelfStuffWeightPhaseDetail → SelfStuffWeight；原界面主从 NormalStuffWeightPhaseDetail_Wash → NormalStuffWeight_Wash；原界面主从 AfterNormalStuffWeightPhaseDetail → AfterNormalStuffWeight。

### SourceDyeStuffWeightPrint — 染化料与称料库存相关表（StuffWeightPrint，待确认）

源表：`dye.StuffWeightPrint`；新表：`src_dye_stuffweightprint`；原主键：SheetSeries, PhaseNo, StuffNo, FormatNo, PrintNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 否 | CharField |
| PhaseNo | old_phase_no | PhaseNo | tinyint | 否 | IntegerField |
| StuffNo | old_stuff_no | StuffNo | tinyint | 否 | IntegerField |
| FormatNo | old_format_no | FormatNo | int | 否 | IntegerField |
| PrintNo | old_print_no | PrintNo | varchar；字节长度 10 | 否 | CharField |
| StuffID | old_stuff_id | StuffID | varchar；字节长度 10 | 是 | CharField |
| StuffType | old_stuff_type | StuffType | varchar；字节长度 10 | 是 | CharField |
| Price | old_price | Price | decimal(10,4) | 是 | DecimalField |
| Dosage | old_dosage | Dosage | decimal(15,6) | 是 | DecimalField |
| WaterQty | old_water_qty | WaterQty | decimal(10,2) | 是 | DecimalField |
| NeedQty | old_need_qty | NeedQty | decimal(10,2) | 是 | DecimalField |
| WeightUnit | old_weight_unit | WeightUnit | varchar；字节长度 10 | 是 | CharField |
| PhaseID | old_phase_id | PhaseID | varchar；字节长度 10 | 是 | CharField |
| ProgramID | old_program_id | ProgramID | varchar；字节长度 50 | 是 | CharField |

### SourceDyeTightTube — 其他或待确认相关表（TightTube，待确认）

源表：`dye.TightTube`；新表：`src_dye_tighttube`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 表单号 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | tinyint | 是 | IntegerField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 品名 | varchar；字节长度 50 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1000 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |

### SourceDyeTightTubeDetail — 其他或待确认相关表（TightTubeDetail，待确认）

源表：`dye.TightTubeDetail`；新表：`src_dye_tighttubedetail`；原主键：DetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| Sheetseries | old_sheetseries | 表单号 | varchar；字节长度 50 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 30 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 30 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 30 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 30 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 30 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| OrderQty | old_order_qty | 订单数量 | decimal(10,2) | 是 | DecimalField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| Area | old_area | 区域 | varchar；字节长度 100 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 100 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 500 | 是 | CharField |
| CustFabricName | old_cust_fabric_name | 客户规格 | varchar；字节长度 250 | 是 | CharField |
| SumAssignedRolls | old_sum_assigned_rolls | 实际粒数 | decimal(7,2) | 是 | DecimalField |
| SumAssignedWeightQty | old_sum_assigned_weight_qty | 实际重量 | decimal(10,2) | 是 | DecimalField |
| ColorRemarks | old_color_remarks | 用途 | varchar；字节长度 500 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 1000 | 是 | CharField |
| DyeDate | old_dye_date | 络筒期 | nchar；字节长度 200 | 是 | CharField |
| OrderSheetDate | old_order_sheet_date | 落单日期 | datetime | 是 | DateTimeField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 500 | 是 | CharField |
| FenTou | old_fen_tou | FenTou | varchar；字节长度 50 | 是 | CharField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| Approver | old_approver | 审核人 | varchar；字节长度 30 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 30 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |

### SourceDyeTightTubePlan — 生产工单与排程相关表（TightTubePlan，待确认）

源表：`dye.TightTubePlan`；新表：`src_dye_tighttubeplan`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 制单单号 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 品名 | varchar；字节长度 50 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1000 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |

### SourceDyeTightTubePlanDetail — 生产工单与排程相关表（TightTubePlanDetail，待确认）

源表：`dye.TightTubePlanDetail`；新表：`src_dye_tighttubeplandetail`；原主键：DetailNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| Sheetseries | old_sheetseries | 表单号 | varchar；字节长度 50 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 30 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 30 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 30 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 30 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 30 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| OrderQty | old_order_qty | 订单数量 | decimal(10,2) | 是 | DecimalField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| Area | old_area | 区域 | varchar；字节长度 100 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 100 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 500 | 是 | CharField |
| SumAssignedRolls | old_sum_assigned_rolls | 生产个数 | decimal(7,2) | 是 | DecimalField |
| SumAssignedWeightQty | old_sum_assigned_weight_qty | 生产重量 | decimal(10,2) | 是 | DecimalField |
| ColorRemarks | old_color_remarks | 用途 | varchar；字节长度 500 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 50 | 是 | CharField |
| LabelWareHouse | old_label_ware_house | 标签仓库 | varchar；字节长度 100 | 是 | CharField |
| LabelRemarks | old_label_remarks | 标签用途 | varchar；字节长度 500 | 是 | CharField |
| WindingID | old_winding_id | 络筒员工 | varchar；字节长度 30 | 是 | CharField |
| TubeWeight | old_tube_weight | 纸筒 | decimal(7,3) | 是 | DecimalField |
| PackBag | old_pack_bag | 包装 | decimal(7,3) | 是 | DecimalField |
| MachineID | old_machine_id | 机台 | varchar；字节长度 100 | 是 | CharField |
| GY | old_gy | 工艺 | varchar；字节长度 200 | 是 | CharField |
| CustFabricName | old_cust_fabric_name | 客户规格 | varchar；字节长度 200 | 是 | CharField |
| LTSheetNo | old_ltsheet_no | 排产号 | varchar；字节长度 30 | 是 | CharField |
| FenTou | old_fen_tou | 分头 | varchar；字节长度 50 | 是 | CharField |

### SourceDyeUserACMachines — 设备维护与能耗相关表（UserACMachines，待确认）

源表：`dye.UserACMachines`；新表：`src_dye_useracmachines`；原主键：UserID, Deviceid。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| UserID | old_user_id | UserID | int | 否 | IntegerField |
| Deviceid | old_deviceid | Deviceid | int | 否 | IntegerField |

### SourceDyeUsersMachines — 设备维护与能耗相关表（UsersMachines，待确认）

源表：`dye.UsersMachines`；新表：`src_dye_usersmachines`；原主键：无主键。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | int | 否 | IntegerField |
| USERID | old_userid | USERID | int | 否 | IntegerField |
| DEVICEID | old_deviceid | DEVICEID | int | 否 | IntegerField |

### SourceDyeWashTheTankDye — 染色工艺与配方相关表（WashTheTankDye，待确认）

源表：`dye.WashTheTankDye`；新表：`src_dye_washthetankdye`；原主键：SheetSeries。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 30 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 30 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| StuffID | old_stuff_id | StuffID | varchar；字节长度 10 | 是 | CharField |
| Creater | old_creater | Creater | nchar；字节长度 40 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | nchar；字节长度 40 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |

### SourceDyeWProcess — 实际工序执行

源表：`dye.WProcess`；新表：`src_dye_wprocess`；原主键：WProcessNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| WProcessNo | old_wprocess_no | 刷卡号 | varchar；字节长度 20 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| OrderSheetNo | old_order_sheet_no | 订单号 | varchar；字节长度 20 | 是 | CharField |
| ProcessNo | old_process_no | 工序号 | tinyint | 是 | IntegerField |
| ProcessID | old_process_id | 工序 | varchar；字节长度 10 | 是 | CharField |
| EmpID | old_emp_id | 员工代码 | varchar；字节长度 10 | 是 | CharField |
| ClassID | old_class_id | 班别 | varchar；字节长度 10 | 是 | CharField |
| ShiftID | old_shift_id | 班组 | varchar；字节长度 10 | 是 | CharField |
| GroupID | old_group_id | 车间代码 | varchar；字节长度 10 | 是 | CharField |
| StationID | old_station_id | 站别 | varchar；字节长度 10 | 是 | CharField |
| MachineID | old_machine_id | 机台 | varchar；字节长度 20 | 是 | CharField |
| PrevProcessID | old_prev_process_id | 上一道工序代码 | varchar；字节长度 10 | 是 | CharField |
| NextProcessNo | old_next_process_no | 下一道工序号 | tinyint | 是 | IntegerField |
| NextProcessID | old_next_process_id | 下一道工序代码 | varchar；字节长度 10 | 是 | CharField |
| NextStationID | old_next_station_id | 下一道站别代码 | varchar；字节长度 10 | 是 | CharField |
| StartTime | old_start_time | 开始时间 | datetime | 是 | DateTimeField |
| EndTime | old_end_time | 结束时间 | datetime | 是 | DateTimeField |
| AssignedQty | old_assigned_qty | 配纱数量 | decimal(10,2) | 是 | DecimalField |
| AssingedKg | old_assinged_kg | 配纱公斤 | decimal(10,2) | 是 | DecimalField |
| AssignedMeter | old_assigned_meter | 配纱米数 | decimal(10,2) | 是 | DecimalField |
| PrevWProcessNo | old_prev_wprocess_no | 上一道刷卡流水号 | varchar；字节长度 20 | 是 | CharField |
| PrevRolls | old_prev_rolls | 上一道粒数 | decimal(7,2) | 是 | DecimalField |
| PrevQty | old_prev_qty | 上一道数量 | decimal(10,2) | 是 | DecimalField |
| PrevMeter | old_prev_meter | 上一道米数 | decimal(10,2) | 是 | DecimalField |
| PrevKg | old_prev_kg | 上一道重量 | decimal(10,2) | 是 | DecimalField |
| PrevWeight | old_prev_weight | 上一道克重 | decimal(6,2) | 是 | DecimalField |
| PrevWidth | old_prev_width | 上一道幅宽 | decimal(6,2) | 是 | DecimalField |
| PrevEndTime | old_prev_end_time | 上一道结束时间 | datetime | 是 | DateTimeField |
| CurrRolls | old_curr_rolls | 粒数 | decimal(8,3) | 是 | DecimalField |
| CurrMeter | old_curr_meter | 长度 | decimal(10,2) | 是 | DecimalField |
| CurrKg | old_curr_kg | 重量 | decimal(10,3) | 是 | DecimalField |
| CurrWeight | old_curr_weight | 克重 | decimal(6,2) | 是 | DecimalField |
| CurrWidth | old_curr_width | 幅宽 | decimal(6,2) | 是 | DecimalField |
| CurrVats | old_curr_vats | 缸数 | decimal(8,3) | 是 | DecimalField |
| CurrEffirate | old_curr_effirate | 本道系数 | decimal(6,2) | 是 | DecimalField |
| WorkQty | old_work_qty | 产量 | decimal(10,3) | 是 | DecimalField |
| WorkMoney | old_work_money | 计件工资 | decimal(10,2) | 是 | DecimalField |
| DefectRolls | old_defect_rolls | 疵品粒数 | decimal(10,2) | 是 | DecimalField |
| DefectQty | old_defect_qty | 疵品数量 | decimal(10,2) | 是 | DecimalField |
| Status | old_status | 状态 | varchar；字节长度 1 | 是 | CharField |
| Memo | old_memo | 摘要 | varchar；字节长度 100 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModuleNo | old_module_no | ModuleNo | smallint | 是 | IntegerField |
| Kind | old_kind | 类别 | tinyint | 是 | IntegerField |
| SampleQty | old_sample_qty | SampleQty | decimal(10,2) | 是 | DecimalField |
| IPAddress | old_ipaddress | IPAddress | varchar；字节长度 25 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | varchar；字节长度 50 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| ColorMatching | old_color_matching | ColorMatching | varchar；字节长度 50 | 是 | CharField |
| QualityMemo | old_quality_memo | QualityMemo | nvarchar；字节长度 40 | 是 | CharField |
| CurrDosage | old_curr_dosage | 本道百分比 | decimal(10,2) | 是 | DecimalField |
| DyeState | old_dye_state | 染色状态 | varchar；字节长度 10 | 是 | CharField |
| SheetKind | old_sheet_kind | 类别（1为录入单据） | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 500 | 是 | CharField |

### SourceDyeWProcessBak — 染色工艺与配方相关表（WProcessBak，待确认）

源表：`dye.WProcessBak`；新表：`src_dye_wprocessbak`；原主键：WProcessNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| WProcessNo | old_wprocess_no | WProcessNo | varchar；字节长度 20 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| OrderSheetNo | old_order_sheet_no | OrderSheetNo | varchar；字节长度 20 | 是 | CharField |
| ProcessNo | old_process_no | ProcessNo | tinyint | 是 | IntegerField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 10 | 是 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 10 | 是 | CharField |
| ClassID | old_class_id | ClassID | varchar；字节长度 10 | 是 | CharField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 10 | 是 | CharField |
| GroupID | old_group_id | GroupID | varchar；字节长度 10 | 是 | CharField |
| StationID | old_station_id | StationID | varchar；字节长度 10 | 是 | CharField |
| MachineID | old_machine_id | MachineID | varchar；字节长度 20 | 是 | CharField |
| PrevProcessID | old_prev_process_id | PrevProcessID | varchar；字节长度 10 | 是 | CharField |
| NextProcessNo | old_next_process_no | NextProcessNo | tinyint | 是 | IntegerField |
| NextProcessID | old_next_process_id | NextProcessID | varchar；字节长度 10 | 是 | CharField |
| NextStationID | old_next_station_id | NextStationID | varchar；字节长度 10 | 是 | CharField |
| StartTime | old_start_time | StartTime | datetime | 是 | DateTimeField |
| EndTime | old_end_time | EndTime | datetime | 是 | DateTimeField |
| AssignedQty | old_assigned_qty | AssignedQty | decimal(10,2) | 是 | DecimalField |
| AssingedKg | old_assinged_kg | AssingedKg | decimal(10,2) | 是 | DecimalField |
| AssignedMeter | old_assigned_meter | AssignedMeter | decimal(10,2) | 是 | DecimalField |
| PrevWProcessNo | old_prev_wprocess_no | PrevWProcessNo | varchar；字节长度 20 | 是 | CharField |
| PrevRolls | old_prev_rolls | PrevRolls | decimal(7,2) | 是 | DecimalField |
| PrevQty | old_prev_qty | PrevQty | decimal(10,2) | 是 | DecimalField |
| PrevMeter | old_prev_meter | PrevMeter | decimal(10,2) | 是 | DecimalField |
| PrevKg | old_prev_kg | PrevKg | decimal(10,2) | 是 | DecimalField |
| PrevWeight | old_prev_weight | PrevWeight | decimal(6,2) | 是 | DecimalField |
| PrevWidth | old_prev_width | PrevWidth | decimal(6,2) | 是 | DecimalField |
| PrevEndTime | old_prev_end_time | PrevEndTime | datetime | 是 | DateTimeField |
| CurrRolls | old_curr_rolls | CurrRolls | decimal(8,3) | 是 | DecimalField |
| CurrMeter | old_curr_meter | CurrMeter | decimal(10,2) | 是 | DecimalField |
| CurrKg | old_curr_kg | CurrKg | decimal(10,3) | 是 | DecimalField |
| CurrWeight | old_curr_weight | CurrWeight | decimal(6,2) | 是 | DecimalField |
| CurrWidth | old_curr_width | CurrWidth | decimal(6,2) | 是 | DecimalField |
| CurrVats | old_curr_vats | CurrVats | decimal(8,3) | 是 | DecimalField |
| CurrEffirate | old_curr_effirate | CurrEffirate | decimal(6,2) | 是 | DecimalField |
| WorkQty | old_work_qty | WorkQty | decimal(10,3) | 是 | DecimalField |
| WorkMoney | old_work_money | WorkMoney | decimal(10,2) | 是 | DecimalField |
| DefectRolls | old_defect_rolls | DefectRolls | decimal(10,2) | 是 | DecimalField |
| DefectQty | old_defect_qty | DefectQty | decimal(10,2) | 是 | DecimalField |
| Status | old_status | Status | varchar；字节长度 1 | 是 | CharField |
| Memo | old_memo | Memo | varchar；字节长度 100 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModuleNo | old_module_no | ModuleNo | smallint | 是 | IntegerField |
| Kind | old_kind | Kind | tinyint | 是 | IntegerField |
| SampleQty | old_sample_qty | SampleQty | decimal(10,2) | 是 | DecimalField |
| IPAddress | old_ipaddress | IPAddress | varchar；字节长度 25 | 是 | CharField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | varchar；字节长度 50 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyeWProcessStep — 染色工艺与配方相关表（WProcessStep，待确认）

源表：`dye.WProcessStep`；新表：`src_dye_wprocessstep`；原主键：WPStepNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| WPStepNo | old_wpstep_no | 刷卡步骤号 | varchar；字节长度 20 | 否 | CharField |
| WProcessNo | old_wprocess_no | 刷卡记录号 | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| ProcessNo | old_process_no | 工序号 | tinyint | 是 | IntegerField |
| ProcessID | old_process_id | 工序代码 | varchar；字节长度 10 | 是 | CharField |
| DyeProcessID | old_dye_process_id | 染色工序 | nvarchar；字节长度 100 | 是 | CharField |
| RealValue | old_real_value | 实际值 | decimal(10,2) | 是 | DecimalField |
| RecordID | old_record_id | 记录ID | nvarchar；字节长度 76 | 是 | CharField |
| CurrTime | old_curr_time | 当前时间 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| ProgramID | old_program_id | ProgramID | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeWProcess`；原码 `WProcessNo` → 父表原码 `WProcessNo`；依据：原界面主从 qry_DyeWorkQtyDetail → qry_DyeWorkQty；原界面主从 DPWProcessStep → DPWProcess。

### SourceDyeWProcessStepBak — 染色工艺与配方相关表（WProcessStepBak，待确认）

源表：`dye.WProcessStepBak`；新表：`src_dye_wprocessstepbak`；原主键：WPStepNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| WPStepNo | old_wpstep_no | WPStepNo | varchar；字节长度 20 | 否 | CharField |
| WProcessNo | old_wprocess_no | WProcessNo | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| ProcessNo | old_process_no | ProcessNo | tinyint | 是 | IntegerField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 10 | 是 | CharField |
| DyeProcessID | old_dye_process_id | DyeProcessID | nvarchar；字节长度 100 | 是 | CharField |
| RealValue | old_real_value | RealValue | decimal(10,2) | 是 | DecimalField |
| RecordID | old_record_id | RecordID | nvarchar；字节长度 76 | 是 | CharField |
| CurrTime | old_curr_time | CurrTime | datetime | 是 | DateTimeField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |
| ProgramID | old_program_id | ProgramID | varchar；字节长度 50 | 是 | CharField |

### SourceDyeWVehicle — 其他或待确认相关表（WVehicle，待确认）

源表：`dye.WVehicle`；新表：`src_dye_wvehicle`；原主键：WProcessNo, VehicleNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| WProcessNo | old_wprocess_no | WProcessNo | varchar；字节长度 20 | 否 | CharField |
| VehicleNo | old_vehicle_no | VehicleNo | varchar；字节长度 10 | 否 | CharField |
| Place | old_place | Place | varchar；字节长度 100 | 是 | CharField |

### SourceDyeWWorkRecord — 生产工单与排程相关表（WWorkRecord，待确认）

源表：`dye.WWorkRecord`；新表：`src_dye_wworkrecord`；原主键：WorkRecordNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| WorkRecordNo | old_work_record_no | 工时登记记录号 | varchar；字节长度 20 | 否 | CharField |
| EmpID | old_emp_id | 员工 | varchar；字节长度 10 | 是 | CharField |
| ShiftID | old_shift_id | 班组 | varchar；字节长度 10 | 是 | CharField |
| CurrDate | old_curr_date | 当前日期 | datetime | 是 | DateTimeField |
| StartTime | old_start_time | 开始上班时间 | datetime | 是 | DateTimeField |
| EndTime | old_end_time | 结束下班时间 | datetime | 是 | DateTimeField |
| WorkTime | old_work_time | 工时（小时） | decimal(5,2) | 是 | DecimalField |
| CurrTime | old_curr_time | 当前时间 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |

### SourceDyeWWorkTime — 生产工单与排程相关表（WWorkTime，待确认）

源表：`dye.WWorkTime`；新表：`src_dye_wworktime`；原主键：WWorkTimeNo。

归属依据：生产/作业/申请及设备事实来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| WWorkTimeNo | old_wwork_time_no | 工时记录标识符 | varchar；字节长度 40 | 否 | CharField |
| EmpID | old_emp_id | 员工 | varchar；字节长度 10 | 否 | CharField |
| CurrDate | old_curr_date | 日期 | datetime | 否 | DateTimeField |
| ShiftID | old_shift_id | 班组 | varchar；字节长度 10 | 否 | CharField |
| EffiRate | old_effi_rate | 效率比例 | decimal(6,4) | 是 | DecimalField |
| WorkTime | old_work_time | 工时 | decimal(5,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |

## 仓储管理

新增原表模型 120 个，原字段 3052 个。

### SourceDboProdin1029 — 坯布半成品成品与仓储相关表（prodin1029，待确认）

源表：`dbo.prodin1029`；新表：`src_dbo_prodin1029`；原主键：无主键。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| StockUnit | old_stock_unit | StockUnit | tinyint | 是 | IntegerField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 250 | 是 | CharField |
| FabricID | old_fabric_id | FabricID | varchar；字节长度 250 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 20 | 是 | CharField |
| CustColorNum | old_cust_color_num | CustColorNum | varchar；字节长度 100 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 是 | CharField |
| StorageUnitID | old_storage_unit_id | StorageUnitID | varchar；字节长度 10 | 是 | CharField |
| Area | old_area | Area | varchar；字节长度 100 | 是 | CharField |
| SumRolls | old_sum_rolls | SumRolls | decimal(7,2) | 是 | DecimalField |
| SumWeightQty | old_sum_weight_qty | SumWeightQty | decimal(10,1) | 是 | DecimalField |
| SumGaryWeight | old_sum_gary_weight | SumGaryWeight | decimal(10,2) | 是 | DecimalField |
| SumLengthQty | old_sum_length_qty | SumLengthQty | decimal(10,2) | 是 | DecimalField |
| AtteFee | old_atte_fee | AtteFee | decimal(10,2) | 是 | DecimalField |
| VatFee | old_vat_fee | VatFee | decimal(10,2) | 是 | DecimalField |
| Width | old_width | Width | decimal(10,2) | 是 | DecimalField |
| Weight | old_weight | Weight | decimal(10,2) | 是 | DecimalField |
| BarCode | old_bar_code | BarCode | varchar；字节长度 50 | 否 | CharField |
| RollNo | old_roll_no | RollNo | varchar；字节长度 20 | 是 | CharField |
| GrayQty | old_gray_qty | GrayQty | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | WeightQty | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | LengthQty | decimal(10,2) | 是 | DecimalField |

### SourceDyeAProdRecord — 坯布半成品成品与仓储相关表（A_ProdRecord，待确认）

源表：`dye.A_ProdRecord`；新表：`src_dye_a_prodrecord`；原主键：无主键。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 30 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 30 | 是 | CharField |
| Row1 | old_row1 | Row1 | int | 是 | IntegerField |
| Row3 | old_row3 | Row3 | bigint | 是 | BigIntegerField |
| Rolls | old_rolls | Rolls | int | 是 | IntegerField |

### SourceDyeArticleDeptApply — 其他或待确认相关表（ArticleDeptApply，待确认）

源表：`dye.ArticleDeptApply`；新表：`src_dye_articledeptapply`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |

### SourceDyeArticleDeptApplyDetail — 其他或待确认相关表（ArticleDeptApplyDetail，待确认）

源表：`dye.ArticleDeptApplyDetail`；新表：`src_dye_articledeptapplydetail`；原主键：SheetSeries, DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 20 | 否 | CharField |
| DeptSheetNo | old_dept_sheet_no | DeptSheetNo | varchar；字节长度 30 | 是 | CharField |
| Name | old_name | Name | varchar；字节长度 50 | 是 | CharField |
| ArticleID | old_article_id | ArticleID | varchar；字节长度 30 | 是 | CharField |
| ArticleKindID | old_article_kind_id | ArticleKindID | varchar；字节长度 30 | 是 | CharField |
| Unit | old_unit | Unit | varchar；字节长度 40 | 是 | CharField |
| Qty | old_qty | Qty | decimal(10,2) | 是 | DecimalField |
| Amount | old_amount | Amount | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 30 | 是 | CharField |
| ApplySheetNo | old_apply_sheet_no | ApplySheetNo | varchar；字节长度 40 | 是 | CharField |

### SourceDyeArticleIn — 辅料入库单

源表：`dye.ArticleIn`；新表：`src_dye_articlein`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| InKindID | old_in_kind_id | 入库类别 | varchar；字节长度 10 | 是 | CharField |
| BuyerID | old_buyer_id | 业务员 | varchar；字节长度 50 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库代码 | varchar；字节长度 10 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商代码 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| Keeper | old_keeper | 仓管员 | varchar；字节长度 10 | 是 | CharField |
| Reason | old_reason | Reason | nvarchar；字节长度 512 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| Settle | old_settle | Settle | varchar；字节长度 50 | 是 | CharField |
| deliverynum | old_deliverynum | deliverynum | varchar；字节长度 50 | 是 | CharField |
| APMoney | old_apmoney | APMoney | decimal(10,2) | 是 | DecimalField |
| APQty | old_apqty | APQty | decimal(10,2) | 是 | DecimalField |
| UnClearQty | old_un_clear_qty | UnClearQty | decimal(10,2) | 是 | DecimalField |
| UnClearMoney | old_un_clear_money | UnClearMoney | decimal(10,2) | 是 | DecimalField |
| UnClearInvoiceQty | old_un_clear_invoice_qty | UnClearInvoiceQty | decimal(10,2) | 是 | DecimalField |
| UnClearInvoiceMoney | old_un_clear_invoice_money | UnClearInvoiceMoney | decimal(10,2) | 是 | DecimalField |
| DiscountMoney | old_discount_money | DiscountMoney | decimal(10,2) | 是 | DecimalField |
| SumAmount | old_sum_amount | SumAmount | decimal(10,2) | 是 | DecimalField |
| InvoiceClearStatus | old_invoice_clear_status | InvoiceClearStatus | tinyint | 是 | IntegerField |
| MoneyClearStatus | old_money_clear_status | MoneyClearStatus | tinyint | 是 | IntegerField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 50 | 是 | CharField |
| FactID | old_fact_id | 所属分厂 | varchar；字节长度 50 | 是 | CharField |
| invoice | old_invoice | invoice | varchar；字节长度 50 | 是 | CharField |

### SourceDyeArticleInDetail — 辅料入库明细

源表：`dye.ArticleInDetail`；新表：`src_dye_articleindetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | 表单明细号（子表） | varchar；字节长度 36 | 否 | CharField |
| ArticleID | old_article_id | 物料编码 | varchar；字节长度 200 | 是 | CharField |
| ArticleKindID | old_article_kind_id | 物料种类 | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 100 | 是 | CharField |
| InQty | old_in_qty | 入库数量 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(16,6) | 是 | DecimalField |
| TaxRate | old_tax_rate | 税率 | decimal(4,2) | 是 | DecimalField |
| TaxPrice | old_tax_price | 含税价 | decimal(16,6) | 是 | DecimalField |
| TaxMoney | old_tax_money | 税金 | decimal(10,2) | 是 | DecimalField |
| Total | old_total | 合计 | decimal(10,2) | 是 | DecimalField |
| PurDetailNo | old_pur_detail_no | 采购单明细号 | varchar；字节长度 20 | 是 | CharField |
| APDetailNo | old_apdetail_no | 应付单细号 | varchar；字节长度 20 | 是 | CharField |
| InvoiceNo | old_invoice_no | 发票号码 | varchar；字节长度 30 | 是 | CharField |
| FactDlvNo | old_fact_dlv_no | 送货单号 | varchar；字节长度 80 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| PackQty | old_pack_qty | 包装数量 | decimal(10,2) | 是 | DecimalField |
| PackUnit | old_pack_unit | PackUnit | varchar；字节长度 10 | 是 | CharField |
| Discount | old_discount | Discount | decimal(3,2) | 是 | DecimalField |
| DiscountMoney | old_discount_money | DiscountMoney | decimal(10,2) | 是 | DecimalField |
| OriDetailNo | old_ori_detail_no | OriDetailNo | varchar；字节长度 36 | 是 | CharField |
| Amount | old_amount | 不含税金额 | decimal(10,2) | 是 | DecimalField |
| StorageUnitIDs | old_storage_unit_ids | 货区 | varchar；字节长度 50 | 是 | CharField |
| batch | old_batch | 批次 | varchar；字节长度 250 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeArticleIn`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 FabricArticleInDetail → FabricArticleIn；原界面主从 ArticleInDetail → ArticleIn。

### SourceDyeArticleOut — 辅料出库单

源表：`dye.ArticleOut`；新表：`src_dye_articleout`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| WareHouseID | old_ware_house_id | 仓库代码 | varchar；字节长度 10 | 是 | CharField |
| ProjectNo | old_project_no | 项目 | varchar；字节长度 20 | 是 | CharField |
| EmpID | old_emp_id | 员工编号 | varchar；字节长度 10 | 是 | CharField |
| OutKindID | old_out_kind_id | 出库类型 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| DeptID | old_dept_id | 部门编码 | varchar；字节长度 10 | 是 | CharField |
| UseID | old_use_id | 用途 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| SupplierID | old_supplier_id | SupplierID | varchar；字节长度 10 | 是 | CharField |
| leaders | old_leaders | 领用人 | varchar；字节长度 50 | 是 | CharField |
| purpose | old_purpose | 用途 | varchar；字节长度 500 | 是 | CharField |
| FactID | old_fact_id | 所属分厂 | varchar；字节长度 50 | 是 | CharField |

### SourceDyeArticleOutApply — 其他或待确认相关表（ArticleOutApply，待确认）

源表：`dye.ArticleOutApply`；新表：`src_dye_articleoutapply`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 否 | CharField |
| Applyer | old_applyer | Applyer | varchar；字节长度 20 | 是 | CharField |
| ApplyDept | old_apply_dept | ApplyDept | varchar；字节长度 30 | 是 | CharField |
| ApplyFactory | old_apply_factory | ApplyFactory | varchar；字节长度 30 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| UseInfo | old_use_info | UseInfo | varchar；字节长度 512 | 是 | CharField |

### SourceDyeArticleOutApplyDetail — 其他或待确认相关表（ArticleOutApplyDetail，待确认）

源表：`dye.ArticleOutApplyDetail`；新表：`src_dye_articleoutapplydetail`；原主键：SheetSeries, DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 20 | 否 | CharField |
| Name | old_name | Name | varchar；字节长度 50 | 是 | CharField |
| ArticleID | old_article_id | ArticleID | varchar；字节长度 30 | 是 | CharField |
| ArticleKindID | old_article_kind_id | ArticleKindID | varchar；字节长度 30 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 100 | 是 | CharField |
| Unit | old_unit | Unit | varchar；字节长度 40 | 是 | CharField |
| Qty | old_qty | Qty | decimal(10,2) | 是 | DecimalField |
| Amount | old_amount | Amount | decimal(10,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | StorageUnitIDs | varchar；字节长度 20 | 是 | CharField |
| KCQty | old_kcqty | KCQty | decimal(10,2) | 是 | DecimalField |

### SourceDyeArticleOutDetail — 辅料出库明细

源表：`dye.ArticleOutDetail`；新表：`src_dye_articleoutdetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | 表单明细号（子表） | varchar；字节长度 36 | 否 | CharField |
| ArticleID | old_article_id | 物料编码 | varchar；字节长度 20 | 是 | CharField |
| ArticleKindID | old_article_kind_id | 物料种类 | varchar；字节长度 20 | 是 | CharField |
| MachineID | old_machine_id | 机台号 | varchar；字节长度 10 | 是 | CharField |
| OutQty | old_out_qty | 出库数量 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(16,6) | 是 | DecimalField |
| Total | old_total | 合计 | decimal(10,2) | 是 | DecimalField |
| InDetailNo | old_in_detail_no | 入库单明细号 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 明细备注 | varchar；字节长度 512 | 是 | CharField |
| ProjectNo | old_project_no | 工程项目 | varchar；字节长度 20 | 是 | CharField |
| SupplierID | old_supplier_id | SupplierID | varchar；字节长度 20 | 是 | CharField |
| EmpID | old_emp_id | 领用人 | varchar；字节长度 10 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | 货区 | varchar；字节长度 50 | 是 | CharField |
| Spec | old_spec | 供应商来货名称 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeArticleOut`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 FabricArticleOutDetail → FabricArticleOut；原界面主从 ArticleOutDetail → ArticleOut。

### SourceDyeArticleStock — 坯布半成品成品与仓储相关表（ArticleStock，待确认）

源表：`dye.ArticleStock`；新表：`src_dye_articlestock`；原主键：StockDate, ArticleKindID, ArticleID, WareHouseID, InDetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| StockDate | old_stock_date | StockDate | datetime | 否 | DateTimeField |
| ArticleKindID | old_article_kind_id | ArticleKindID | varchar；字节长度 20 | 否 | CharField |
| ArticleID | old_article_id | ArticleID | varchar；字节长度 20 | 否 | CharField |
| WareHouseID | old_ware_house_id | WareHouseID | varchar；字节长度 10 | 否 | CharField |
| PreMonthQty | old_pre_month_qty | PreMonthQty | decimal(10,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(16,6) | 是 | DecimalField |
| PreMonthMoney | old_pre_month_money | PreMonthMoney | decimal(12,4) | 是 | DecimalField |
| CarryDate | old_carry_date | CarryDate | datetime | 是 | DateTimeField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| InDetailNo | old_in_detail_no | InDetailNo | varchar；字节长度 20 | 否 | CharField |

### SourceDyeArticleStockAdjust — 坯布半成品成品与仓储相关表（ArticleStockAdjust，待确认）

源表：`dye.ArticleStockAdjust`；新表：`src_dye_articlestockadjust`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| WareHouseID | old_ware_house_id | 仓库 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyeArticleStockAdjustDetail — 坯布半成品成品与仓储相关表（ArticleStockAdjustDetail，待确认）

源表：`dye.ArticleStockAdjustDetail`；新表：`src_dye_articlestockadjustdetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 36 | 否 | CharField |
| ArticleKindID | old_article_kind_id | 机物料种类 | varchar；字节长度 20 | 是 | CharField |
| ArticleID | old_article_id | 机物料编码 | varchar；字节长度 200 | 是 | CharField |
| PaperQty | old_paper_qty | 账面数量 | decimal(10,2) | 是 | DecimalField |
| RealQty | old_real_qty | 盘点数量 | decimal(10,2) | 是 | DecimalField |
| AdjustQty | old_adjust_qty | 调整数量 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(10,4) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| PaperMoney | old_paper_money | 账面金额 | decimal(14,2) | 是 | DecimalField |
| RealMoney | old_real_money | 盘点金额 | decimal(14,2) | 是 | DecimalField |
| AdjustMoney | old_adjust_money | 调整金额 | decimal(14,2) | 是 | DecimalField |
| InDetailNo | old_in_detail_no | 入库明细号 | varchar；字节长度 20 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeArticleStockAdjust`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ArticleStockAdjustDetail → ArticleStockAdjust。

### SourceDyeArticleStockBook — 辅料库存流水

源表：`dye.ArticleStockBook`；新表：`src_dye_articlestockbook`；原主键：BookNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| BookNo | old_book_no | BookNo | bigint | 否 | BigIntegerField |
| BookDate | old_book_date | BookDate | datetime | 是 | DateTimeField |
| AccDate | old_acc_date | AccDate | datetime | 是 | DateTimeField |
| BookKind | old_book_kind | BookKind | tinyint | 是 | IntegerField |
| ArticleKindID | old_article_kind_id | ArticleKindID | varchar；字节长度 20 | 是 | CharField |
| ArticleID | old_article_id | ArticleID | varchar；字节长度 200 | 是 | CharField |
| SupplierID | old_supplier_id | SupplierID | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | WareHouseID | varchar；字节长度 10 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | StorageUnitIDs | varchar；字节长度 100 | 是 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 是 | CharField |
| InQty | old_in_qty | InQty | decimal(10,2) | 是 | DecimalField |
| OutQty | old_out_qty | OutQty | decimal(10,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(14,4) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 10 | 是 | CharField |
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 是 | CharField |
| StockFlag | old_stock_flag | StockFlag | nchar；字节长度 20 | 是 | CharField |
| InMoney | old_in_money | InMoney | decimal(10,2) | 是 | DecimalField |
| OutMoney | old_out_money | OutMoney | decimal(10,2) | 是 | DecimalField |
| CurrDate | old_curr_date | CurrDate | datetime | 是 | DateTimeField |
| InDetailNo | old_in_detail_no | InDetailNo | varchar；字节长度 20 | 是 | CharField |
| OriDetailNo | old_ori_detail_no | OriDetailNo | varchar；字节长度 36 | 是 | CharField |

### SourceDyeCarryMaterial — 染化料与称料库存相关表（CarryMaterial，待确认）

源表：`dye.CarryMaterial`；新表：`src_dye_carrymaterial`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 表单号 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 品名 | varchar；字节长度 50 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1000 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |

### SourceDyeCarryMaterialDetail — 染化料与称料库存相关表（CarryMaterialDetail，待确认）

源表：`dye.CarryMaterialDetail`；新表：`src_dye_carrymaterialdetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| Sheetseries | old_sheetseries | 表单号 | varchar；字节长度 50 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 30 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 30 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 30 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 30 | 是 | CharField |
| ColorID | old_color_id | 物料颜色 | varchar；字节长度 30 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| OrderQty | old_order_qty | 订单数量 | decimal(10,2) | 是 | DecimalField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| Area | old_area | 区域 | varchar；字节长度 100 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 100 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 500 | 是 | CharField |
| Semi_Owner | old_semi_owner | 半成品所有者 | varchar；字节长度 30 | 是 | CharField |
| InSheetKind | old_in_sheet_kind | 物料分类 | varchar；字节长度 30 | 是 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 30 | 是 | CharField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| SupplierID | old_supplier_id | 供应商 | varchar；字节长度 20 | 是 | CharField |
| JobColorID | old_job_color_id | 工卡颜色 | varchar；字节长度 30 | 是 | CharField |
| FixedQty | old_fixed_qty | 锭重 | decimal(5,2) | 是 | DecimalField |
| PurchaseOrders | old_purchase_orders | 采购单号 | varchar；字节长度 20 | 是 | CharField |
| A_A | old_a_a | 物料区域 | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | 物料等级 | varchar；字节长度 100 | 是 | CharField |
| PDRolls | old_pdrolls | 排单粒数 | decimal(10,2) | 是 | DecimalField |
| PDQty | old_pdqty | 排单重量 | decimal(10,2) | 是 | DecimalField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |

### SourceDyeCookInDetail — 坯布半成品成品与仓储相关表（CookInDetail，待确认）

源表：`dye.CookInDetail`；新表：`src_dye_cookindetail`；原主键：DetailNo。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | 表单明细号（子表） | varchar；字节长度 36 | 否 | CharField |
| CookID | old_cook_id | 物料编码 | varchar；字节长度 200 | 是 | CharField |
| ArticleKindID | old_article_kind_id | 物料种类 | varchar；字节长度 20 | 是 | CharField |
| InQty | old_in_qty | 入库数量 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(16,6) | 是 | DecimalField |
| TaxRate | old_tax_rate | 税率 | decimal(4,2) | 是 | DecimalField |
| TaxPrice | old_tax_price | 含税价 | decimal(16,6) | 是 | DecimalField |
| TaxMoney | old_tax_money | 税金 | decimal(10,2) | 是 | DecimalField |
| Total | old_total | 合计 | decimal(10,2) | 是 | DecimalField |
| PurDetailNo | old_pur_detail_no | 采购单明细号 | varchar；字节长度 20 | 是 | CharField |
| APDetailNo | old_apdetail_no | 应付单细号 | varchar；字节长度 20 | 是 | CharField |
| InvoiceNo | old_invoice_no | 发票号码 | varchar；字节长度 30 | 是 | CharField |
| FactDlvNo | old_fact_dlv_no | 送货单号 | varchar；字节长度 80 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| PackQty | old_pack_qty | 包装数量 | decimal(10,2) | 是 | DecimalField |
| PackUnit | old_pack_unit | PackUnit | varchar；字节长度 10 | 是 | CharField |
| Discount | old_discount | Discount | decimal(3,2) | 是 | DecimalField |
| DiscountMoney | old_discount_money | DiscountMoney | decimal(10,2) | 是 | DecimalField |
| OriDetailNo | old_ori_detail_no | OriDetailNo | varchar；字节长度 36 | 是 | CharField |
| Amount | old_amount | 不含税金额 | float | 是 | FloatField |

关联 `source_parent_1` → `erp_base.SourceDyeCookIn`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 CookInDetail → CookIn。

### SourceDyeDyeStuffOut — 染化料与称料库存相关表（DyeStuffOut，待确认）

源表：`dye.DyeStuffOut`；新表：`src_dye_dyestuffout`；原主键：SheetSeries。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 50 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 20 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | WareHouseID | varchar；字节长度 20 | 是 | CharField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 20 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 50 | 是 | CharField |
| Keeper | old_keeper | Keeper | varchar；字节长度 100 | 是 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 50 | 是 | CharField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | SheetStatus | varchar；字节长度 1 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | varchar；字节长度 50 | 是 | CharField |
| WeightSheetNo | old_weight_sheet_no | WeightSheetNo | varchar；字节长度 50 | 是 | CharField |
| InDetailNo | old_in_detail_no | InDetailNo | varchar；字节长度 50 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| OutDate | old_out_date | OutDate | datetime | 是 | DateTimeField |
| MachineID | old_machine_id | MachineID | varchar；字节长度 255 | 是 | CharField |
| FactID | old_fact_id | FactID | varchar；字节长度 50 | 是 | CharField |
| SQSheetNo | old_sqsheet_no | SQSheetNo | varchar；字节长度 50 | 是 | CharField |
| Status | old_status | Status | smallint | 是 | IntegerField |

### SourceDyeDyeStuffOutDetail — 染化料与称料库存相关表（DyeStuffOutDetail，待确认）

源表：`dye.DyeStuffOutDetail`；新表：`src_dye_dyestuffoutdetail`；原主键：DetailNo。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 40 | 否 | CharField |
| PurDetailNo | old_pur_detail_no | PurDetailNo | varchar；字节长度 20 | 是 | CharField |
| StuffID | old_stuff_id | StuffID | varchar；字节长度 10 | 是 | CharField |
| Price | old_price | Price | decimal(16,6) | 是 | DecimalField |
| TaxPrice | old_tax_price | TaxPrice | decimal(16,6) | 是 | DecimalField |
| TaxRate | old_tax_rate | TaxRate | decimal(16,6) | 是 | DecimalField |
| TaxMoney | old_tax_money | TaxMoney | decimal(16,6) | 是 | DecimalField |
| Amount | old_amount | Amount | decimal(16,6) | 是 | DecimalField |
| Qty | old_qty | Qty | decimal(15,6) | 是 | DecimalField |
| APDetailNo | old_apdetail_no | APDetailNo | varchar；字节长度 20 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 200 | 是 | CharField |
| DlvQty | old_dlv_qty | DlvQty | decimal(15,6) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| InDetailNo | old_in_detail_no | InDetailNo | varchar；字节长度 50 | 是 | CharField |
| PhaseNo | old_phase_no | PhaseNo | tinyint | 是 | IntegerField |
| PhaseID | old_phase_id | PhaseID | varchar；字节长度 50 | 是 | CharField |
| StuffNo | old_stuff_no | StuffNo | tinyint | 是 | IntegerField |
| Unit | old_unit | Unit | varchar；字节长度 20 | 是 | CharField |

### SourceDyeGrayBalance — 财务结算与成本相关表（GrayBalance，待确认）

源表：`dye.GrayBalance`；新表：`src_dye_graybalance`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库 | varchar；字节长度 10 | 是 | CharField |
| SheetKind | old_sheet_kind | 调整类别 | smallint | 是 | IntegerField |
| Keeper | old_keeper | 仓管员 | varchar；字节长度 20 | 是 | CharField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 制单人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 制单日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |

### SourceDyeGrayBalanceDetail — 财务结算与成本相关表（GrayBalanceDetail，待确认）

源表：`dye.GrayBalanceDetail`；新表：`src_dye_graybalancedetail`；原主键：SheetSeries, DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 20 | 否 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 否 | CharField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库 | varchar；字节长度 10 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | 仓位 | varchar；字节长度 100 | 是 | CharField |
| Piece | old_piece | 粒数 | decimal(8,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| GrainQty | old_grain_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(8,2) | 是 | DecimalField |
| Amount | old_amount | 金额 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| LastBookDate | old_last_book_date | 最后流水日期 | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeGrayBalance`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 GrayBalanceDetail → GrayBalance。

### SourceDyeGrayIn — 坯布入库单

源表：`dye.GrayIn`；新表：`src_dye_grayin`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库代码 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| IsInputRecord | old_is_input_record | 录入码单明细否 | bit | 是 | BooleanField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| GrayKindID | old_gray_kind_id | 胚纱类别 | varchar；字节长度 10 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商代码 | varchar；字节长度 10 | 是 | CharField |
| FactDlvNo | old_fact_dlv_no | 送货单号 | varchar；字节长度 20 | 是 | CharField |
| StockUnit | old_stock_unit | 库存单位 | tinyint | 是 | IntegerField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| BusinessKind | old_business_kind | 业务类别 | smallint | 是 | IntegerField |
| CustomerID | old_customer_id | 客户名称 | varchar；字节长度 10 | 是 | CharField |
| FactID | old_fact_id | 加工商 | varchar；字节长度 10 | 是 | CharField |
| Driver | old_driver | 司机 | varchar；字节长度 20 | 是 | CharField |
| CarNo | old_car_no | 车牌号 | varchar；字节长度 20 | 是 | CharField |
| ShiftID | old_shift_id | 班组 | varchar；字节长度 10 | 是 | CharField |
| GeterID | old_geter_id | GeterID | varchar；字节长度 10 | 是 | CharField |
| GetDate | old_get_date | GetDate | datetime | 是 | DateTimeField |
| CheckerID | old_checker_id | CheckerID | varchar；字节长度 10 | 是 | CharField |
| DefectDate | old_defect_date | DefectDate | datetime | 是 | DateTimeField |
| DefectShiftID | old_defect_shift_id | DefectShiftID | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员 | varchar；字节长度 10 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 50 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| TakeOver | old_take_over | 收货员 | varchar；字节长度 10 | 是 | CharField |
| Cargador1 | old_cargador1 | 搬运工1 | nvarchar；字节长度 20 | 是 | CharField |
| Cargador2 | old_cargador2 | 搬运工2 | nvarchar；字节长度 20 | 是 | CharField |
| Cargador3 | old_cargador3 | 搬运工3 | nvarchar；字节长度 20 | 是 | CharField |
| Cargador4 | old_cargador4 | 送货地址 | nvarchar；字节长度 20 | 是 | CharField |
| Cargador5 | old_cargador5 | 搬运工5 | nvarchar；字节长度 20 | 是 | CharField |
| Driver1 | old_driver1 | 叉车1 | nvarchar；字节长度 20 | 是 | CharField |
| Driver2 | old_driver2 | 叉车2 | nvarchar；字节长度 20 | 是 | CharField |
| Driver3 | old_driver3 | 叉车3 | nvarchar；字节长度 20 | 是 | CharField |
| Sender | old_sender | 交胚人 | nvarchar；字节长度 20 | 是 | CharField |
| Discharger1 | old_discharger1 | 装卸工1 | nvarchar；字节长度 20 | 是 | CharField |
| Discharger2 | old_discharger2 | 装卸工2 | nvarchar；字节长度 20 | 是 | CharField |
| Water | old_water | 水量 | nvarchar；字节长度 20 | 是 | CharField |
| Ingredients | old_ingredients | Ingredients | varchar；字节长度 20 | 是 | CharField |
| Toosoft | old_toosoft | 过软 | varchar；字节长度 20 | 是 | CharField |
| Isdecrement | old_isdecrement | Isdecrement | varchar；字节长度 20 | 是 | CharField |
| Loss | old_loss | Loss | varchar；字节长度 50 | 是 | CharField |
| PackageHtt | old_package_htt | 包装 | varchar；字节长度 20 | 是 | CharField |
| Width | old_width | Width | varchar；字节长度 50 | 是 | CharField |
| HandFeel | old_hand_feel | 手感 | varchar；字节长度 20 | 是 | CharField |
| Receiver | old_receiver | 收货人 | varchar；字节长度 20 | 是 | CharField |
| DlvRolls | old_dlv_rolls | 收胚粒数 | decimal(10,2) | 是 | DecimalField |
| DlvWeightQty | old_dlv_weight_qty | 收胚重量 | decimal(10,2) | 是 | DecimalField |
| CustomerCode | old_customer_code | 客户全称 | varchar；字节长度 50 | 是 | CharField |
| DlvAddress | old_dlv_address | 送货地址 | varchar；字节长度 500 | 是 | CharField |
| KTYY | old_ktyy | 客退原因 | varchar；字节长度 250 | 是 | CharField |
| WLLX | old_wllx | 物流类型 | varchar；字节长度 255 | 是 | CharField |
| combo1 | old_combo1 | 收发地点 | varchar；字节长度 10 | 是 | CharField |
| SPYSPC | old_spyspc | 收胚运输编号 | varchar；字节长度 20 | 是 | CharField |
| SemiOutSheetNo | old_semi_out_sheet_no | SemiOutSheetNo | varchar；字节长度 50 | 是 | CharField |
| A_A | old_a_a | 物料屈戌 | varchar；字节长度 50 | 是 | CharField |

### SourceDyeGrayInDefect — 质量检验与异常相关表（GrayInDefect，待确认）

源表：`dye.GrayInDefect`；新表：`src_dye_grayindefect`；原主键：ReceSheetNo, DefectNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ReceSheetNo | old_rece_sheet_no | ReceSheetNo | varchar；字节长度 20 | 否 | CharField |
| DefectNo | old_defect_no | DefectNo | smallint | 否 | IntegerField |
| DefectID | old_defect_id | DefectID | varchar；字节长度 10 | 是 | CharField |
| Qty | old_qty | Qty | decimal(10,2) | 是 | DecimalField |

### SourceDyeGrayInDetail — 坯布入库明细

源表：`dye.GrayInDetail`；新表：`src_dye_grayindetail`；原主键：ReceSheetNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 是 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 否 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | 库位代码复合 | varchar；字节长度 100 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| Packs | old_packs | 件数 | decimal(7,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| Amount | old_amount | 金额 | decimal(10,2) | 是 | DecimalField |
| Weight | old_weight | 克重 | decimal(8,4) | 是 | DecimalField |
| Width | old_width | 幅宽 | decimal(6,2) | 是 | DecimalField |
| DlvRolls | old_dlv_rolls | 交货粒数 | decimal(7,2) | 是 | DecimalField |
| DlvPacks | old_dlv_packs | 交货包数 | decimal(7,2) | 是 | DecimalField |
| DlvQty | old_dlv_qty | 交货数量 | decimal(10,2) | 是 | DecimalField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| PurDetailNo | old_pur_detail_no | 采购单明细号 | varchar；字节长度 20 | 是 | CharField |
| APDetailNo | old_apdetail_no | 应付单细号 | varchar；字节长度 20 | 是 | CharField |
| OriReceSheetNo | old_ori_rece_sheet_no | 原收纱明细编号 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 60 | 是 | CharField |
| RollAvgQty | old_roll_avg_qty | 粒长 | decimal(10,2) | 是 | DecimalField |
| WeftDensity | old_weft_density | 纬密 | decimal(6,2) | 是 | DecimalField |
| WarpDensity | old_warp_density | 经密 | decimal(6,2) | 是 | DecimalField |
| CheckResult | old_check_result | 检验意见 | varchar；字节长度 100 | 是 | CharField |
| GradeID | old_grade_id | 色号等级 | varchar；字节长度 10 | 是 | CharField |
| OriJobsheetNo | old_ori_jobsheet_no | 原工卡号 | varchar；字节长度 20 | 是 | CharField |
| MachineID | old_machine_id | 机号 | varchar；字节长度 50 | 是 | CharField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 10 | 是 | CharField |
| DetailsCustomer | old_details_customer | 织厂 | nvarchar；字节长度 100 | 是 | CharField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |
| PreField2 | old_pre_field2 | 氨纶 | varchar；字节长度 50 | 是 | CharField |
| PreField3 | old_pre_field3 | 针数 | varchar；字节长度 50 | 是 | CharField |
| PreField4 | old_pre_field4 | 寸数 | varchar；字节长度 50 | 是 | CharField |
| PreField5 | old_pre_field5 | 纱批 | varchar；字节长度 200 | 是 | CharField |
| PCS | old_pcs | 粒/件 | int | 是 | IntegerField |
| FixedQty | old_fixed_qty | 锭重 | decimal(5,2) | 是 | DecimalField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| ColorLv | old_color_lv | 色级 | varchar；字节长度 20 | 是 | CharField |
| Yardage | old_yardage | 码数 | decimal(10,2) | 是 | DecimalField |
| CustJobNo | old_cust_job_no | 收料单号 | varchar；字节长度 100 | 是 | CharField |
| GUnit | old_gunit | GUnit | tinyint | 是 | IntegerField |
| InputCode | old_input_code | 打包明细 | varchar；字节长度 50 | 是 | CharField |
| Area | old_area | 区域 | varchar；字节长度 100 | 是 | CharField |
| GrayApplyNo | old_gray_apply_no | 胚纱退货申请单号 | varchar；字节长度 30 | 是 | CharField |
| YarnCategory | old_yarn_category | 纱类别 | varchar；字节长度 30 | 是 | CharField |
| TrunReceSheetNo | old_trun_rece_sheet_no | 转仓前入库明细单号 | varchar；字节长度 50 | 是 | CharField |
| PurchaseOrders | old_purchase_orders | 采购单号 | varchar；字节长度 20 | 是 | CharField |
| A_A | old_a_a | 物料区域 | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | 物料等级 | varchar；字节长度 100 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 30 | 是 | CharField |
| InSheetKind | old_in_sheet_kind | 物料分类 | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 工卡号 | varchar；字节长度 20 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeGrayIn`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 PurGrayInDetail → PurGrayIn；原界面主从 TuiHuoGrayInDetail → TuiHuoGrayIn；原界面主从 SemiToGrayInDetail → SemiToGrayIn；原界面主从 KeTuiGrayInDetail → KeTuiGrayIn；原界面主从 GrayAllotInDetail → GrayAllotIn；原界面主从 JiaNianGrayInDetail → JiaNianGrayIn；原界面主从 GrayInWorkDetail → GrayInWork；原界面主从 GrayInDetail → GrayIn。

### SourceDyeGrayInRecord — 坯布半成品成品与仓储相关表（GrayInRecord，待确认）

源表：`dye.GrayInRecord`；新表：`src_dye_grayinrecord`；原主键：ReceSheetNo, RollNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 否 | CharField |
| RollNo | old_roll_no | 箱号 | varchar；字节长度 20 | 否 | CharField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| DlvQty | old_dlv_qty | 交货数量 | decimal(10,2) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 仓位 | varchar；字节长度 10 | 是 | CharField |
| Defects | old_defects | 疵点 | varchar；字节长度 100 | 是 | CharField |
| Status | old_status | 状态 | varchar；字节长度 1 | 是 | CharField |
| BarCode | old_bar_code | 条码 | varchar；字节长度 50 | 是 | CharField |
| AssignedNo | old_assigned_no | 投胚流水号 | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| OriReceSheetNo | old_ori_rece_sheet_no | OriReceSheetNo | varchar；字节长度 20 | 是 | CharField |
| RollNo2 | old_roll_no2 | RollNo2 | varchar；字节长度 20 | 是 | CharField |
| GUnit | old_gunit | GUnit | tinyint | 是 | IntegerField |
| OriBarCode | old_ori_bar_code | OriBarCode | varchar；字节长度 50 | 是 | CharField |
| Remark | old_remark | 备注 | varchar；字节长度 300 | 是 | CharField |
| GraySpec | old_gray_spec | GraySpec | varchar；字节长度 50 | 是 | CharField |
| Num | old_num | Num | decimal(8,0) | 是 | DecimalField |
| CBz | old_cbz | CBz | varchar；字节长度 10 | 是 | CharField |
| Rolls | old_rolls | 粒数 | float | 是 | FloatField |
| Packs | old_packs | 件数 | decimal(4,1) | 是 | DecimalField |
| InputDetailCode | old_input_detail_code | 标签打印细码 | varchar；字节长度 100 | 是 | CharField |
| Kg | old_kg | 磅重 | decimal(10,2) | 是 | DecimalField |
| CustQty | old_cust_qty | 毛重 | decimal(10,1) | 是 | DecimalField |
| TubeWeight | old_tube_weight | 纸筒 | decimal(6,2) | 是 | DecimalField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeGrayInDetail`；原码 `ReceSheetNo` → 父表原码 `ReceSheetNo`；依据：原界面主从 TuiHuoGrayInRecord → TuiHuoGrayInDetail；原界面主从 GrayInRecord → GrayInDetail；原界面主从 JiaNianGrayInRecord → JiaNianGrayInDetail；原界面主从 KeTuiGrayInRecord → KeTuiGrayInDetail；原界面主从 PurGrayInRecord → PurGrayInDetail；原界面主从 GrayAllotInRecord → GrayAllotInDetail；原界面主从 GrayInWorkRecord → GrayInWorkDetail。

### SourceDyeGrayMaterial — 染化料与称料库存相关表（GrayMaterial，待确认）

源表：`dye.GrayMaterial`；新表：`src_dye_graymaterial`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 表单号 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 品名 | varchar；字节长度 50 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1000 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |

### SourceDyeGrayMaterialDetail — 染化料与称料库存相关表（GrayMaterialDetail，待确认）

源表：`dye.GrayMaterialDetail`；新表：`src_dye_graymaterialdetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| Sheetseries | old_sheetseries | 表单号 | varchar；字节长度 50 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 30 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 30 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 30 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 30 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 30 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| OrderQty | old_order_qty | 订单数量 | decimal(10,2) | 是 | DecimalField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| Area | old_area | 区域 | varchar；字节长度 100 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 100 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 500 | 是 | CharField |
| CustFabricName | old_cust_fabric_name | 客户规格 | varchar；字节长度 250 | 是 | CharField |
| SumAssignedRolls | old_sum_assigned_rolls | 实发粒数 | decimal(7,2) | 是 | DecimalField |
| SumAssignedWeightQty | old_sum_assigned_weight_qty | 实发重量 | decimal(10,2) | 是 | DecimalField |
| ColorRemarks | old_color_remarks | 用途 | varchar；字节长度 500 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 1000 | 是 | CharField |
| DyeDate | old_dye_date | 络筒期 | nchar；字节长度 200 | 是 | CharField |
| OrderSheetDate | old_order_sheet_date | 落单日期 | datetime | 是 | DateTimeField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 500 | 是 | CharField |
| FenTou | old_fen_tou | FenTou | varchar；字节长度 50 | 是 | CharField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| Approver | old_approver | 审核人 | varchar；字节长度 30 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 30 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |

### SourceDyeGrayOut — 坯布出库单

源表：`dye.GrayOut`；新表：`src_dye_grayout`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| GrayKindID | old_gray_kind_id | 胚纱类别 | varchar；字节长度 10 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库代码 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员 | varchar；字节长度 10 | 是 | CharField |
| FactID | old_fact_id | 工厂代码 | varchar；字节长度 1000 | 是 | CharField |
| StockUnit | old_stock_unit | 库存单位 | tinyint | 是 | IntegerField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| BusinessKind | old_business_kind | 业务类别 | smallint | 是 | IntegerField |
| SupplierID | old_supplier_id | 供应商 | varchar；字节长度 10 | 是 | CharField |
| CarNo | old_car_no | 配纱员 | varchar；字节长度 20 | 是 | CharField |
| Driver | old_driver | Driver | varchar；字节长度 20 | 是 | CharField |
| ToPlace | old_to_place | ToPlace | varchar；字节长度 500 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 50 | 是 | CharField |
| Cargador1 | old_cargador1 | Cargador1 | varchar；字节长度 10 | 是 | CharField |
| Cargador2 | old_cargador2 | Cargador2 | varchar；字节长度 10 | 是 | CharField |
| Cargador3 | old_cargador3 | Cargador3 | varchar；字节长度 10 | 是 | CharField |
| Cargador4 | old_cargador4 | Cargador4 | varchar；字节长度 10 | 是 | CharField |
| Cargador5 | old_cargador5 | Cargador5 | varchar；字节长度 10 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| WProcessNo | old_wprocess_no | WProcessNo | varchar；字节长度 1000 | 是 | CharField |
| CheckNo | old_check_no | 订单明细 | varchar；字节长度 20 | 是 | CharField |

### SourceDyeGrayOutDetail — 坯布出库明细

源表：`dye.GrayOutDetail`；新表：`src_dye_grayoutdetail`；原主键：AssignedNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| AssignedNo | old_assigned_no | 投胚流水号 | varchar；字节长度 20 | 否 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度数量 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量数量 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| Amount | old_amount | 金额 | decimal(10,2) | 是 | DecimalField |
| Weight | old_weight | 克重 | decimal(6,2) | 是 | DecimalField |
| Width | old_width | 幅宽 | decimal(6,2) | 是 | DecimalField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Packs | old_packs | 件数 | decimal(7,2) | 是 | DecimalField |
| PCS | old_pcs | 粒/件 | int | 是 | IntegerField |
| FixedQty | old_fixed_qty | 锭重 | decimal(5,2) | 是 | DecimalField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | 物料颜色 | varchar；字节长度 20 | 是 | CharField |
| ColorE | old_color_e | ColorE | varchar；字节长度 20 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 10 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | 库位 | varchar；字节长度 100 | 是 | CharField |
| MachineID | old_machine_id | MachineID | varchar；字节长度 10 | 是 | CharField |
| CustJobNo | old_cust_job_no | 客户缸号 | varchar；字节长度 20 | 是 | CharField |
| BasicQty | old_basic_qty | BasicQty | decimal(10,2) | 是 | DecimalField |
| LWRate | old_lwrate | LWRate | decimal(6,4) | 是 | DecimalField |
| JobSheetSeries | old_job_sheet_series | JobSheetSeries | varchar；字节长度 20 | 是 | CharField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 50 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 50 | 是 | CharField |
| Area | old_area | 区域 | varchar；字节长度 100 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |
| PreField2 | old_pre_field2 | PreField2 | varchar；字节长度 50 | 是 | CharField |
| PreField3 | old_pre_field3 | PreField3 | varchar；字节长度 50 | 是 | CharField |
| PreField4 | old_pre_field4 | PreField4 | varchar；字节长度 50 | 是 | CharField |
| PreField5 | old_pre_field5 | PreField5 | varchar；字节长度 200 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商 | varchar；字节长度 30 | 是 | CharField |
| InSheetKind | old_in_sheet_kind | 物料分类 | varchar；字节长度 20 | 是 | CharField |
| PurchaseOrders | old_purchase_orders | 采购单号 | varchar；字节长度 20 | 是 | CharField |
| A_A | old_a_a | 物料区域 | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | 物料等级 | varchar；字节长度 100 | 是 | CharField |
| InputCode | old_input_code | 打包条码 | varchar；字节长度 40 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeGrayOut`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 GrayOutDetailTurn → GrayOutTurn；原界面主从 GrayOutDetail → GrayOut；原界面主从 TSGrayOutDetail → TSGrayOut；原界面主从 GrayOutDetailJob → GrayOutJob；原界面主从 GrayAllotOutDetail → GrayAllotOut；原界面主从 GrayOutDetailShenHe → GrayOutShenHe；原界面主从 GrayOutSaleDetail → GrayOutSale；原界面主从 GrayOutWorkDetail → GrayOutWork。

### SourceDyeGrayOutRecord — 坯布半成品成品与仓储相关表（GrayOutRecord，待确认）

源表：`dye.GrayOutRecord`；新表：`src_dye_grayoutrecord`；原主键：AssignedNo, RollNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 工卡流水 | varchar；字节长度 20 | 是 | CharField |
| AssignedNo | old_assigned_no | 投胚流水号 | varchar；字节长度 20 | 否 | CharField |
| RollNo | old_roll_no | 箱号 | varchar；字节长度 20 | 否 | CharField |
| BarCode | old_bar_code | 胚纱条码 | varchar；字节长度 50 | 是 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 是 | CharField |
| LengthQty | old_length_qty | 长度数量 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量数量 | decimal(10,2) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 仓位代码 | varchar；字节长度 10 | 是 | CharField |
| Status | old_status | 状态 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| GUnit | old_gunit | GUnit | tinyint | 是 | IntegerField |
| Rolls | old_rolls | 粒数 | decimal(4,1) | 是 | DecimalField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| Packs | old_packs | 件数 | decimal(4,1) | 是 | DecimalField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeGrayOutDetail`；原码 `AssignedNo` → 父表原码 `AssignedNo`；依据：原界面主从 GrayOutRecord → GrayOutDetail；原界面主从 GrayOutSaleRecord → GrayOutSaleDetail；原界面主从 GrayOutRecordShenHe → GrayOutDetailShenHe；原界面主从 GrayOutRecordTurn → GrayOutDetailTurn；原界面主从 GrayOutRecordMatch → GrayOutDetail；原界面主从 GrayOutWorkRecord → GrayOutWorkDetail；原界面主从 GrayOutRecordJob → GrayOutDetailJob；原界面主从 TSGrayOutRecordMatch → TSGrayOutDetail。

### SourceDyeGrayPostionUp — 坯布半成品成品与仓储相关表（GrayPostionUp，待确认）

源表：`dye.GrayPostionUp`；新表：`src_dye_graypostionup`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 36 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| InSheetKind | old_in_sheet_kind | 物料分类 | varchar；字节长度 20 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 200 | 是 | CharField |
| ColorID | old_color_id | 物料颜色 | varchar；字节长度 50 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |
| FixedQty | old_fixed_qty | 锭重 | decimal(5,2) | 是 | DecimalField |
| PurchaseOrders | old_purchase_orders | 采购单号 | varchar；字节长度 20 | 是 | CharField |
| A_A | old_a_a | 物料区域 | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | 物料等级 | varchar；字节长度 100 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量数量 | decimal(8,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度数量 | decimal(8,2) | 是 | DecimalField |
| Packs | old_packs | 件数 | decimal(7,2) | 是 | DecimalField |
| PCS | old_pcs | 粒/件 | int | 是 | IntegerField |
| Area | old_area | 原区域 | varchar；字节长度 100 | 是 | CharField |
| NewArea | old_new_area | 新区域 | varchar；字节长度 100 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| InDetailNo | old_in_detail_no | InDetailNo | varchar；字节长度 50 | 是 | CharField |

### SourceDyeGrayRecord — 坯布半成品成品与仓储相关表（GrayRecord，待确认）

源表：`dye.GrayRecord`；新表：`src_dye_grayrecord`；原主键：BarCode。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| BarCode | old_bar_code | 条码 | varchar；字节长度 50 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| CurrTime | old_curr_time | CurrTime | datetime | 是 | DateTimeField |
| Geter | old_geter | 收货员 | varchar；字节长度 10 | 是 | CharField |
| StorageUnitID | old_storage_unit_id | 仓位 | varchar；字节长度 10 | 是 | CharField |
| IsInput | old_is_input | IsInput | bit | 是 | BooleanField |

### SourceDyeGrayRecordCutLogs — 坯布半成品成品与仓储相关表（GrayRecordCutLogs，待确认）

源表：`dye.GrayRecordCutLogs`；新表：`src_dye_grayrecordcutlogs`；原主键：OperateDate, ID。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | varchar；字节长度 50 | 否 | CharField |
| Kind | old_kind | Kind | int | 否 | IntegerField |
| OriReceSheetNoList | old_ori_rece_sheet_no_list | OriReceSheetNoList | varchar；字节长度 2000 | 是 | CharField |
| NewReceSheetNoList | old_new_rece_sheet_no_list | NewReceSheetNoList | varchar；字节长度 2000 | 是 | CharField |
| OriRollNoList | old_ori_roll_no_list | OriRollNoList | varchar；字节长度 200 | 是 | CharField |
| NewRollNoList | old_new_roll_no_list | NewRollNoList | varchar；字节长度 200 | 是 | CharField |
| OriBarCodeList | old_ori_bar_code_list | OriBarCodeList | varchar；字节长度 2000 | 是 | CharField |
| NewBarCodeList | old_new_bar_code_list | NewBarCodeList | varchar；字节长度 2000 | 是 | CharField |
| OriQtyList | old_ori_qty_list | OriQtyList | varchar；字节长度 1000 | 是 | CharField |
| NewQtyList | old_new_qty_list | NewQtyList | varchar；字节长度 1000 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| Operator | old_operator | Operator | varchar；字节长度 20 | 是 | CharField |
| OperateDate | old_operate_date | OperateDate | datetime | 否 | DateTimeField |
| Status | old_status | Status | int | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| DataTableName | old_data_table_name | DataTableName | varchar；字节长度 100 | 是 | CharField |

### SourceDyeGrayStock — 坯布半成品成品与仓储相关表（GrayStock，待确认）

源表：`dye.GrayStock`；新表：`src_dye_graystock`；原主键：StockDate, ColorID, CustomerID, WareHouseID, SupplierID, GrayID, SalerID, Spec, LotNo, ReceSheetNo, PreField1, PurchaseOrders, A_A, A_B, FixedQty。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| StockDate | old_stock_date | StockDate | datetime | 否 | DateTimeField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 20 | 否 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 否 | CharField |
| WareHouseID | old_ware_house_id | WareHouseID | varchar；字节长度 10 | 否 | CharField |
| GrayKindID | old_gray_kind_id | GrayKindID | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | SalerGroupID | varchar；字节长度 10 | 是 | CharField |
| SupplierID | old_supplier_id | SupplierID | varchar；字节长度 10 | 否 | CharField |
| BusinessKind | old_business_kind | BusinessKind | smallint | 是 | IntegerField |
| GrayID | old_gray_id | GrayID | varchar；字节长度 50 | 否 | CharField |
| StockKind | old_stock_kind | StockKind | tinyint | 是 | IntegerField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 10 | 否 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 否 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 否 | CharField |
| PreMonthPacks | old_pre_month_packs | PreMonthPacks | decimal(10,2) | 是 | DecimalField |
| PreMonthRolls | old_pre_month_rolls | PreMonthRolls | decimal(10,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| CarryDate | old_carry_date | CarryDate | datetime | 是 | DateTimeField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| PreMonthWeightQty | old_pre_month_weight_qty | PreMonthWeightQty | decimal(10,2) | 是 | DecimalField |
| PreMonthLengthQty | old_pre_month_length_qty | PreMonthLengthQty | decimal(10,2) | 是 | DecimalField |
| StorageUnitIDs | old_storage_unit_ids | StorageUnitIDs | varchar；字节长度 100 | 是 | CharField |
| ReceSheetNo | old_rece_sheet_no | ReceSheetNo | varchar；字节长度 20 | 否 | CharField |
| PreField1 | old_pre_field1 | PreField1 | varchar；字节长度 50 | 否 | CharField |
| PurchaseOrders | old_purchase_orders | PurchaseOrders | varchar；字节长度 20 | 否 | CharField |
| A_A | old_a_a | A_A | varchar；字节长度 50 | 否 | CharField |
| A_B | old_a_b | A_B | varchar；字节长度 100 | 否 | CharField |
| FixedQty | old_fixed_qty | FixedQty | decimal(5,1) | 否 | DecimalField |

### SourceDyeGrayStockAdjust — 坯布半成品成品与仓储相关表（GrayStockAdjust，待确认）

源表：`dye.GrayStockAdjust`；新表：`src_dye_graystockadjust`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 10 | 是 | CharField |
| BusinessKind | old_business_kind | 业务类别 | smallint | 是 | IntegerField |
| GrayKindID | old_gray_kind_id | 胚纱类别 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库代码 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyeGrayStockAdjustDetail — 坯布半成品成品与仓储相关表（GrayStockAdjustDetail，待确认）

源表：`dye.GrayStockAdjustDetail`；新表：`src_dye_graystockadjustdetail`；原主键：SheetSeries, DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 调整明细单号 | varchar；字节长度 36 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 物料颜色 | varchar；字节长度 20 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| PaperRolls | old_paper_rolls | 帐面粒数 | decimal(10,2) | 是 | DecimalField |
| RealRolls | old_real_rolls | 实际粒数 | decimal(16,2) | 是 | DecimalField |
| AdjustRolls | old_adjust_rolls | 调整粒数 | decimal(7,2) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(8,2) | 是 | DecimalField |
| StockUnit | old_stock_unit | 库存单位 | tinyint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| PaperLength | old_paper_length | 账面长度 | decimal(10,5) | 是 | DecimalField |
| PaperWeight | old_paper_weight | 账面重量 | decimal(10,5) | 是 | DecimalField |
| RealLengthQty | old_real_length_qty | 实际长度 | decimal(10,2) | 是 | DecimalField |
| RealWeightQty | old_real_weight_qty | 实际重量 | decimal(10,2) | 是 | DecimalField |
| AdjustLengthQty | old_adjust_length_qty | 调整长度 | decimal(10,2) | 是 | DecimalField |
| AdjustWeightQty | old_adjust_weight_qty | 调整重量 | decimal(10,2) | 是 | DecimalField |
| StorageUnitIDs | old_storage_unit_ids | 库位 | varchar；字节长度 100 | 是 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| AdjustPacks | old_adjust_packs | 调整件数 | decimal(10,2) | 是 | DecimalField |
| PaperPacks | old_paper_packs | 账面件数 | decimal(10,2) | 是 | DecimalField |
| RealPacks | old_real_packs | 实际件数 | decimal(10,2) | 是 | DecimalField |
| InSheetKind | old_in_sheet_kind | 物料分类 | varchar；字节长度 20 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |
| PurchaseOrders | old_purchase_orders | 采购单号 | varchar；字节长度 20 | 是 | CharField |
| A_A | old_a_a | 物料区域 | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | 物料等级 | varchar；字节长度 100 | 是 | CharField |
| FixedQty | old_fixed_qty | 锭重 | decimal(5,2) | 是 | DecimalField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeGrayStockAdjust`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 GrayStockAdjustDetail → GrayStockAdjust。

### SourceDyeGrayStockAllot — 坯布半成品成品与仓储相关表（GrayStockAllot，待确认）

源表：`dye.GrayStockAllot`；新表：`src_dye_graystockallot`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| GrayKindID | old_gray_kind_id | 胚纱类别 | varchar；字节长度 10 | 是 | CharField |
| FromSaleGroupID | old_from_sale_group_id | 来源业务组别 | varchar；字节长度 10 | 是 | CharField |
| ToSalerGroupID | old_to_saler_group_id | 目标业务组别 | varchar；字节长度 10 | 是 | CharField |
| FromWareHouseID | old_from_ware_house_id | 来源仓库 | varchar；字节长度 10 | 是 | CharField |
| FromCustomerID | old_from_customer_id | 来源客户 | varchar；字节长度 10 | 是 | CharField |
| ToCustomerID | old_to_customer_id | 目标客户 | varchar；字节长度 10 | 是 | CharField |
| FromReceSheetNo | old_from_rece_sheet_no | 来源收纱明细编号 | varchar；字节长度 20 | 是 | CharField |
| ToWareHouseID | old_to_ware_house_id | 目标仓库 | varchar；字节长度 10 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| Packs | old_packs | 件数 | decimal(7,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| FromBusinessUnitID | old_from_business_unit_id | 来源经营单位 | varchar；字节长度 10 | 是 | CharField |
| ToBusinessUnitID | old_to_business_unit_id | 目标经营单位 | varchar；字节长度 10 | 是 | CharField |
| FromSalerID | old_from_saler_id | 来源业务员 | varchar；字节长度 10 | 是 | CharField |
| ToSalerID | old_to_saler_id | 目标业务员 | varchar；字节长度 10 | 是 | CharField |
| FromLotNo | old_from_lot_no | 来源批号 | varchar；字节长度 50 | 是 | CharField |
| ToLotNo | old_to_lot_no | 目标批号 | varchar；字节长度 50 | 是 | CharField |
| FromSpec | old_from_spec | 来源规格 | varchar；字节长度 50 | 是 | CharField |
| ToSpec | old_to_spec | 目标规格 | varchar；字节长度 50 | 是 | CharField |
| FromPrice | old_from_price | 来源价格 | decimal(8,2) | 是 | DecimalField |
| ToPrice | old_to_price | 目标价格 | decimal(8,2) | 是 | DecimalField |
| FromStructure | old_from_structure | 来源组织 | varchar；字节长度 50 | 是 | CharField |
| ToStructure | old_to_structure | 目标组织 | varchar；字节长度 50 | 是 | CharField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| BusinessKind | old_business_kind | BusinessKind | smallint | 是 | IntegerField |
| FromGrayID | old_from_gray_id | 来原品名 | varchar；字节长度 10 | 是 | CharField |
| ToGrayID | old_to_gray_id | 目标品名 | varchar；字节长度 10 | 是 | CharField |
| StockUnit | old_stock_unit | StockUnit | tinyint | 是 | IntegerField |
| FromSheetKind | old_from_sheet_kind | 来源单据类型 | smallint | 是 | IntegerField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| ToReceSheetNo | old_to_rece_sheet_no | 目标收胚明细号 | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| AssignedNo | old_assigned_no | AssignedNo | varchar；字节长度 20 | 是 | CharField |

### SourceDyeGrayStockBook — 坯布库存流水

源表：`dye.GrayStockBook`；新表：`src_dye_graystockbook`；原主键：BookNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| BookNo | old_book_no | BookNo | bigint | 否 | BigIntegerField |
| BookKind | old_book_kind | BookKind | tinyint | 是 | IntegerField |
| GrayKindID | old_gray_kind_id | GrayKindID | varchar；字节长度 10 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| BusinessKind | old_business_kind | BusinessKind | smallint | 是 | IntegerField |
| GradeID | old_grade_id | GradeID | varchar；字节长度 10 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 20 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 20 | 是 | CharField |
| SupplierID | old_supplier_id | SupplierID | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| FactID | old_fact_id | FactID | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | WareHouseID | varchar；字节长度 10 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | StorageUnitIDs | varchar；字节长度 100 | 是 | CharField |
| GrayID | old_gray_id | GrayID | varchar；字节长度 50 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 是 | CharField |
| SalerGroupID | old_saler_group_id | SalerGroupID | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 10 | 是 | CharField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 是 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| InRolls | old_in_rolls | InRolls | decimal(7,2) | 是 | DecimalField |
| InPacks | old_in_packs | InPacks | decimal(7,2) | 是 | DecimalField |
| OutRolls | old_out_rolls | OutRolls | decimal(7,2) | 是 | DecimalField |
| OutPacks | old_out_packs | OutPacks | decimal(7,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| BookDate | old_book_date | BookDate | datetime | 是 | DateTimeField |
| AccDate | old_acc_date | AccDate | datetime | 是 | DateTimeField |
| ReceSheetNo | old_rece_sheet_no | ReceSheetNo | varchar；字节长度 20 | 是 | CharField |
| Memo | old_memo | Memo | varchar；字节长度 100 | 是 | CharField |
| StockFlag | old_stock_flag | StockFlag | varchar；字节长度 1 | 是 | CharField |
| StockKind | old_stock_kind | StockKind | tinyint | 是 | IntegerField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| InLengthQty | old_in_length_qty | InLengthQty | decimal(10,2) | 是 | DecimalField |
| InWeightQty | old_in_weight_qty | InWeightQty | decimal(10,2) | 是 | DecimalField |
| OutWeightQty | old_out_weight_qty | OutWeightQty | decimal(10,2) | 是 | DecimalField |
| OutLengthQty | old_out_length_qty | OutLengthQty | decimal(10,2) | 是 | DecimalField |
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 是 | CharField |
| InMoney | old_in_money | InMoney | decimal(10,2) | 是 | DecimalField |
| OutMoney | old_out_money | OutMoney | decimal(10,2) | 是 | DecimalField |
| CurrDate | old_curr_date | CurrDate | datetime | 是 | DateTimeField |
| InSheetKind | old_in_sheet_kind | InSheetKind | varchar；字节长度 20 | 是 | CharField |
| PreField1 | old_pre_field1 | PreField1 | varchar；字节长度 50 | 是 | CharField |
| PurchaseOrders | old_purchase_orders | PurchaseOrders | varchar；字节长度 20 | 是 | CharField |
| A_A | old_a_a | A_A | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | A_B | varchar；字节长度 100 | 是 | CharField |
| FixedQty | old_fixed_qty | FixedQty | decimal(5,2) | 是 | DecimalField |

### SourceDyeGrayStockCheck — 质量检验与异常相关表（GrayStockCheck，待确认）

源表：`dye.GrayStockCheck`；新表：`src_dye_graystockcheck`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| GrayKindID | old_gray_kind_id | GrayKindID | varchar；字节长度 10 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库代码 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 是 | CharField |
| FactID | old_fact_id | FactID | varchar；字节长度 10 | 是 | CharField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 是 | CharField |
| JobDetailNo | old_job_detail_no | JobDetailNo | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 50 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| PaperRolls | old_paper_rolls | 帐面粒数 | decimal(10,2) | 是 | DecimalField |
| PaperPacks | old_paper_packs | PaperPacks | decimal(10,2) | 是 | DecimalField |
| PaperQty | old_paper_qty | PaperQty | decimal(10,2) | 是 | DecimalField |
| AdjustPacks | old_adjust_packs | AdjustPacks | decimal(7,2) | 是 | DecimalField |
| AdjustQty | old_adjust_qty | AdjustQty | decimal(10,2) | 是 | DecimalField |
| AdjustRolls | old_adjust_rolls | 调整粒数 | decimal(7,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| StockUnit | old_stock_unit | StockUnit | tinyint | 是 | IntegerField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| FlowID | old_flow_id | FlowID | varchar；字节长度 10 | 是 | CharField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 是 | CharField |
| BusinessKind | old_business_kind | BusinessKind | smallint | 是 | IntegerField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 10 | 是 | CharField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |

### SourceDyeGrayStockSpecUp — 坯布半成品成品与仓储相关表（GrayStockSpecUp，待确认）

源表：`dye.GrayStockSpecUp`；新表：`src_dye_graystockspecup`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| GrayKindID | old_gray_kind_id | 胚纱类别 | varchar；字节长度 10 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库代码 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员 | varchar；字节长度 10 | 是 | CharField |
| FactID | old_fact_id | 工厂代码 | varchar；字节长度 1000 | 是 | CharField |
| StockUnit | old_stock_unit | 库存单位 | tinyint | 是 | IntegerField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| BusinessKind | old_business_kind | 业务类别 | smallint | 是 | IntegerField |
| CarNo | old_car_no | 配纱员 | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 50 | 是 | CharField |
| SalerGroupID | old_saler_group_id | SalerGroupID | varchar；字节长度 10 | 是 | CharField |

### SourceDyeGrayStockSpecUpDetail — 坯布半成品成品与仓储相关表（GrayStockSpecUpDetail，待确认）

源表：`dye.GrayStockSpecUpDetail`；新表：`src_dye_graystockspecupdetail`；原主键：AssignedNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| AssignedNo | old_assigned_no | 出库明细号 | varchar；字节长度 20 | 否 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 是 | CharField |
| PCS | old_pcs | 粒/件 | int | 是 | IntegerField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| Packs | old_packs | 件数 | decimal(7,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Area | old_area | 区域 | varchar；字节长度 100 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | 库位 | varchar；字节长度 100 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库 | varchar；字节长度 20 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 30 | 是 | CharField |
| InSheetKind | old_in_sheet_kind | 物料分类 | varchar；字节长度 20 | 是 | CharField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 物料颜色 | varchar；字节长度 20 | 是 | CharField |
| FixedQty | old_fixed_qty | 锭重 | decimal(5,2) | 是 | DecimalField |
| SupplierID | old_supplier_id | 供应商 | varchar；字节长度 30 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |
| PurchaseOrders | old_purchase_orders | 采购单号 | varchar；字节长度 20 | 是 | CharField |
| A_A | old_a_a | 物料区域 | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | 物料等级 | varchar；字节长度 100 | 是 | CharField |
| UPCustomerID | old_upcustomer_id | 调整客户 | varchar；字节长度 30 | 是 | CharField |
| UPInSheetKind | old_upin_sheet_kind | 调整物料分类 | varchar；字节长度 20 | 是 | CharField |
| UPGrayID | old_upgray_id | 调整规格 | varchar；字节长度 50 | 是 | CharField |
| UPLotNo | old_uplot_no | 调整批号 | varchar；字节长度 50 | 是 | CharField |
| UPColorID | old_upcolor_id | 调整物料颜色 | varchar；字节长度 20 | 是 | CharField |
| UPFixedQty | old_upfixed_qty | 调整锭重 | decimal(5,2) | 是 | DecimalField |
| UPPreField1 | old_uppre_field1 | 调整捻度(H/S) | varchar；字节长度 50 | 是 | CharField |
| UPPurchaseOrders | old_uppurchase_orders | 调整采购单号 | varchar；字节长度 20 | 是 | CharField |
| UPA_A | old_upa_a | 调整物料区域 | varchar；字节长度 50 | 是 | CharField |
| UPA_B | old_upa_b | 调整物料等级 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeGrayStockSpecUp`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 GrayStockSpecUpDetail → GrayStockSpecUp。

### SourceDyeGrayStorageAdjust — 坯布半成品成品与仓储相关表（GrayStorageAdjust，待确认）

源表：`dye.GrayStorageAdjust`；新表：`src_dye_graystorageadjust`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单据号 | varchar；字节长度 20 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| SalerID | old_saler_id | 业务员 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | 调出仓库 | varchar；字节长度 10 | 是 | CharField |
| ToWareHouseID | old_to_ware_house_id | 调入仓库 | varchar；字节长度 10 | 是 | CharField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| CarryerID | old_carryer_id | 搬运工 | varchar；字节长度 20 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| Approved | old_approved | Approved | bit | 是 | BooleanField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| CarryerID1 | old_carryer_id1 | CarryerID1 | varchar；字节长度 20 | 是 | CharField |
| CarryerID2 | old_carryer_id2 | CarryerID2 | varchar；字节长度 20 | 是 | CharField |
| CarryerID3 | old_carryer_id3 | CarryerID3 | varchar；字节长度 20 | 是 | CharField |
| CarryerID4 | old_carryer_id4 | CarryerID4 | varchar；字节长度 20 | 是 | CharField |

### SourceDyeGrayStorageAdjustDetail — 坯布半成品成品与仓储相关表（GrayStorageAdjustDetail，待确认）

源表：`dye.GrayStorageAdjustDetail`；新表：`src_dye_graystorageadjustdetail`；原主键：SheetSeries, DetailNo, FromReceSheetNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细号 | varchar；字节长度 36 | 否 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 100 | 是 | CharField |
| FromReceSheetNo | old_from_rece_sheet_no | 转仓明细 | varchar；字节长度 20 | 否 | CharField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 200 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 200 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | 调出库位 | varchar；字节长度 100 | 是 | CharField |
| ToStorageUnitIDs | old_to_storage_unit_ids | 调入库位 | varchar；字节长度 100 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Area | old_area | 调出区域 | varchar；字节长度 100 | 是 | CharField |
| ToArea | old_to_area | 调入区域 | varchar；字节长度 100 | 是 | CharField |
| CustJobNo | old_cust_job_no | 收料编号 | varchar；字节长度 50 | 是 | CharField |
| InSheetKind | old_in_sheet_kind | InSheetKind | varchar；字节长度 20 | 是 | CharField |
| PreField1 | old_pre_field1 | PreField1 | varchar；字节长度 50 | 是 | CharField |
| PurchaseOrders | old_purchase_orders | PurchaseOrders | varchar；字节长度 20 | 是 | CharField |
| A_A | old_a_a | A_A | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | A_B | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeGrayStorageAdjust`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 GrayStorageAdjustDetail → GrayStorageAdjust。

### SourceDyeGrayStorageAdjustRecord — 坯布半成品成品与仓储相关表（GrayStorageAdjustRecord，待确认）

源表：`dye.GrayStorageAdjustRecord`；新表：`src_dye_graystorageadjustrecord`；原主键：SheetSeries, DetailNo, RollNo, FromReceSheetNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细号 | varchar；字节长度 36 | 否 | CharField |
| RollNo | old_roll_no | 箱号 | varchar；字节长度 20 | 否 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 100 | 是 | CharField |
| FromReceSheetNo | old_from_rece_sheet_no | 转仓明细 | varchar；字节长度 20 | 否 | CharField |
| BarCode | old_bar_code | 条码 | varchar；字节长度 100 | 是 | CharField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 调出库位 | varchar；字节长度 100 | 是 | CharField |
| ToStorageUnitID | old_to_storage_unit_id | 调入库位 | varchar；字节长度 100 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| RollNo2 | old_roll_no2 | RollNo2 | varchar；字节长度 50 | 是 | CharField |
| Rolls | old_rolls | 粒数 | float | 是 | FloatField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeGrayStorageAdjustDetail`；原码 `SheetSeries, DetailNo, FromReceSheetNo` → 父表原码 `SheetSeries, DetailNo, FromReceSheetNo`；依据：原界面主从 GrayStorageAdjustRecord → GrayStorageAdjustDetail。

### SourceDyeODMIn — 其他或待确认相关表（ODMIn，待确认）

源表：`dye.ODMIn`；新表：`src_dye_odmin`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| SheetType | old_sheet_type | 单据类型 | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| Keeper | old_keeper | 仓管员 | varchar；字节长度 100 | 是 | CharField |
| Driver | old_driver | 司机 | varchar；字节长度 20 | 是 | CharField |
| CarNo | old_car_no | 车牌号 | varchar；字节长度 20 | 是 | CharField |
| CarryerID | old_carryer_id | 搬运工1 | varchar；字节长度 20 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库代码 | varchar；字节长度 10 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| StockUnit | old_stock_unit | 库存单位 | tinyint | 是 | IntegerField |
| Cargador1 | old_cargador1 | 搬运工2 | varchar；字节长度 10 | 是 | CharField |
| Cargador2 | old_cargador2 | 搬运工3 | varchar；字节长度 10 | 是 | CharField |
| Cargador3 | old_cargador3 | 搬运工4 | varchar；字节长度 10 | 是 | CharField |
| Cargador4 | old_cargador4 | Cargador4 | varchar；字节长度 10 | 是 | CharField |
| Cargador5 | old_cargador5 | Cargador5 | varchar；字节长度 10 | 是 | CharField |

### SourceDyeODMInDetail — 坯布半成品成品与仓储相关表（ODMInDetail，待确认）

源表：`dye.ODMInDetail`；新表：`src_dye_odmindetail`；原主键：SheetSeries, DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 表单明细号（子表） | varchar；字节长度 36 | 否 | CharField |
| OutDetailNo | old_out_detail_no | 出库单明细号 | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| InRolls | old_in_rolls | 入库粒数 | decimal(7,2) | 是 | DecimalField |
| InLengthQty | old_in_length_qty | 入库长度 | decimal(10,2) | 是 | DecimalField |
| InWeightQty | old_in_weight_qty | 入库重量 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 50 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 50 | 是 | CharField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| WarpDensity | old_warp_density | WarpDensity | varchar；字节长度 50 | 是 | CharField |
| WeftDensity | old_weft_density | WeftDensity | varchar；字节长度 50 | 是 | CharField |
| StockUnit | old_stock_unit | 单位 | tinyint | 是 | IntegerField |
| OutSheetNo | old_out_sheet_no | OutSheetNo | varchar；字节长度 50 | 是 | CharField |
| Weight | old_weight | Weight | decimal(6,2) | 是 | DecimalField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 200 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeODMIn`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ODMInDetail → ODMIn。

### SourceDyeODMInRecord — 其他或待确认相关表（ODMInRecord，待确认）

源表：`dye.ODMInRecord`；新表：`src_dye_odminrecord`；原主键：RollNo, DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 工卡流水 | varchar；字节长度 50 | 是 | CharField |
| RollNo | old_roll_no | 箱号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细流水号 | varchar；字节长度 36 | 否 | CharField |
| BarCode | old_bar_code | BarCode | varchar；字节长度 100 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 是 | CharField |
| LengthQty | old_length_qty | 长度数量 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 发外重量 | decimal(10,2) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 仓位代码 | varchar；字节长度 10 | 是 | CharField |
| Status | old_status | 状态 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| WProcessNo | old_wprocess_no | WProcessNo | varchar；字节长度 20 | 是 | CharField |
| MachineID | old_machine_id | MachineID | varchar；字节长度 20 | 是 | CharField |
| Kind | old_kind | Kind | tinyint | 是 | IntegerField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeODMInDetail`；原码 `SheetSeries, DetailNo` → 父表原码 `SheetSeries, DetailNo`；依据：原界面主从 ODMInRecord → ODMInDetail。

### SourceDyeODMOut — 其他或待确认相关表（ODMOut，待确认）

源表：`dye.ODMOut`；新表：`src_dye_odmout`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| SheetType | old_sheet_type | 单据类型 | smallint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 是 | CharField |
| Keeper | old_keeper | 仓管员 | varchar；字节长度 100 | 是 | CharField |
| CarNo | old_car_no | 车牌号 | varchar；字节长度 20 | 是 | CharField |
| FactID | old_fact_id | 工厂代码 | varchar；字节长度 10 | 是 | CharField |
| Driver | old_driver | 司机 | varchar；字节长度 20 | 是 | CharField |
| OutKindID | old_out_kind_id | 发货类型 | varchar；字节长度 10 | 是 | CharField |
| OutTime | old_out_time | 领料时间 | datetime | 是 | DateTimeField |
| PackID | old_pack_id | 包装形式代码 | varchar；字节长度 10 | 是 | CharField |
| ProcessID | old_process_id | 工序代码 | varchar；字节长度 50 | 是 | CharField |
| CarryerID | old_carryer_id | 搬运工1 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| DlvDate | old_dlv_date | 交货日期 | datetime | 是 | DateTimeField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| StockUnit | old_stock_unit | 库存单位 | tinyint | 是 | IntegerField |
| Cargador1 | old_cargador1 | 搬运工2 | varchar；字节长度 10 | 是 | CharField |
| Cargador2 | old_cargador2 | 搬运工3 | varchar；字节长度 10 | 是 | CharField |
| Cargador3 | old_cargador3 | 搬运工4 | varchar；字节长度 10 | 是 | CharField |
| Cargador4 | old_cargador4 | Cargador4 | varchar；字节长度 10 | 是 | CharField |
| Cargador5 | old_cargador5 | Cargador5 | varchar；字节长度 10 | 是 | CharField |

### SourceDyeODMOutDetail — 坯布半成品成品与仓储相关表（ODMOutDetail，待确认）

源表：`dye.ODMOutDetail`；新表：`src_dye_odmoutdetail`；原主键：SheetSeries, DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 表单明细号（子表） | varchar；字节长度 36 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| GrayID | old_gray_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 50 | 是 | CharField |
| WeftDensity | old_weft_density | 纬密 | varchar；字节长度 50 | 是 | CharField |
| WarpDensity | old_warp_density | 经密 | varchar；字节长度 50 | 是 | CharField |
| OutRolls | old_out_rolls | 出库粒数 | decimal(7,2) | 是 | DecimalField |
| OutLengthQty | old_out_length_qty | 出库长度 | decimal(10,2) | 是 | DecimalField |
| OutWeightQty | old_out_weight_qty | 出库重量 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 50 | 是 | CharField |
| GWidth | old_gwidth | GWidth | varchar；字节长度 50 | 是 | CharField |
| Width | old_width | Width | varchar；字节长度 50 | 是 | CharField |
| StockUnit | old_stock_unit | 单位 | tinyint | 是 | IntegerField |
| Weight | old_weight | Weight | decimal(6,2) | 是 | DecimalField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 200 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeODMOut`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ODMOutDetail → ODMOut。

### SourceDyeODMOutRecord — 其他或待确认相关表（ODMOutRecord，待确认）

源表：`dye.ODMOutRecord`；新表：`src_dye_odmoutrecord`；原主键：RollNo, DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 工卡流水 | varchar；字节长度 50 | 是 | CharField |
| RollNo | old_roll_no | 箱号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细流水号 | varchar；字节长度 36 | 否 | CharField |
| BarCode | old_bar_code | BarCode | varchar；字节长度 100 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(10,2) | 是 | DecimalField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 是 | CharField |
| LengthQty | old_length_qty | 长度数量 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 发外重量 | decimal(10,2) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 仓位代码 | varchar；字节长度 10 | 是 | CharField |
| Status | old_status | 状态 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| WProcessNo | old_wprocess_no | WProcessNo | varchar；字节长度 20 | 是 | CharField |
| MachineID | old_machine_id | MachineID | varchar；字节长度 20 | 是 | CharField |
| Kind | old_kind | Kind | tinyint | 是 | IntegerField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeODMOutDetail`；原码 `SheetSeries, DetailNo` → 父表原码 `SheetSeries, DetailNo`；依据：原界面主从 ODMOutRecord → ODMOutDetail。

### SourceDyeOtherIn — 其他或待确认相关表（OtherIn，待确认）

源表：`dye.OtherIn`；新表：`src_dye_otherin`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| InKindID | old_in_kind_id | 入库类别 | varchar；字节长度 10 | 是 | CharField |
| BuyerID | old_buyer_id | 采购员 | varchar；字节长度 50 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库代码 | varchar；字节长度 10 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商代码 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| Keeper | old_keeper | 仓管员 | varchar；字节长度 10 | 是 | CharField |
| Reason | old_reason | Reason | nvarchar；字节长度 512 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| Settle | old_settle | Settle | varchar；字节长度 50 | 是 | CharField |
| deliverynum | old_deliverynum | deliverynum | varchar；字节长度 50 | 是 | CharField |
| APMoney | old_apmoney | APMoney | decimal(10,2) | 是 | DecimalField |
| APQty | old_apqty | APQty | decimal(10,2) | 是 | DecimalField |
| UnClearQty | old_un_clear_qty | UnClearQty | decimal(10,2) | 是 | DecimalField |
| UnClearMoney | old_un_clear_money | UnClearMoney | decimal(10,2) | 是 | DecimalField |
| UnClearInvoiceQty | old_un_clear_invoice_qty | UnClearInvoiceQty | decimal(10,2) | 是 | DecimalField |
| UnClearInvoiceMoney | old_un_clear_invoice_money | UnClearInvoiceMoney | decimal(10,2) | 是 | DecimalField |
| DiscountMoney | old_discount_money | DiscountMoney | decimal(10,2) | 是 | DecimalField |
| SumAmount | old_sum_amount | SumAmount | decimal(10,2) | 是 | DecimalField |
| InvoiceClearStatus | old_invoice_clear_status | InvoiceClearStatus | tinyint | 是 | IntegerField |
| MoneyClearStatus | old_money_clear_status | MoneyClearStatus | tinyint | 是 | IntegerField |

### SourceDyeOtherInDetail — 坯布半成品成品与仓储相关表（OtherInDetail，待确认）

源表：`dye.OtherInDetail`；新表：`src_dye_otherindetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | 表单明细号（子表） | varchar；字节长度 36 | 否 | CharField |
| CookID | old_cook_id | 物料编码 | varchar；字节长度 200 | 是 | CharField |
| ArticleKindID | old_article_kind_id | 报账类别 | varchar；字节长度 20 | 是 | CharField |
| InQty | old_in_qty | 入库数量 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(16,6) | 是 | DecimalField |
| TaxRate | old_tax_rate | 税率 | decimal(4,2) | 是 | DecimalField |
| TaxPrice | old_tax_price | 含税价 | decimal(16,6) | 是 | DecimalField |
| TaxMoney | old_tax_money | 税金 | decimal(10,2) | 是 | DecimalField |
| Total | old_total | 合计 | decimal(10,2) | 是 | DecimalField |
| PurDetailNo | old_pur_detail_no | 采购单明细号 | varchar；字节长度 20 | 是 | CharField |
| APDetailNo | old_apdetail_no | 应付单细号 | varchar；字节长度 20 | 是 | CharField |
| InvoiceNo | old_invoice_no | 发票号码 | varchar；字节长度 30 | 是 | CharField |
| FactDlvNo | old_fact_dlv_no | 送货单号 | varchar；字节长度 80 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| PackQty | old_pack_qty | 包装数量 | decimal(10,2) | 是 | DecimalField |
| PackUnit | old_pack_unit | PackUnit | varchar；字节长度 10 | 是 | CharField |
| Discount | old_discount | Discount | decimal(3,2) | 是 | DecimalField |
| DiscountMoney | old_discount_money | DiscountMoney | decimal(10,2) | 是 | DecimalField |
| OriDetailNo | old_ori_detail_no | OriDetailNo | varchar；字节长度 36 | 是 | CharField |
| Amount | old_amount | 不含税金额 | float | 是 | FloatField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeOtherIn`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 OtherInDetail → OtherIn。

### SourceDyeOutGoingBill — 其他或待确认相关表（OutGoingBill，待确认）

源表：`dye.OutGoingBill`；新表：`src_dye_outgoingbill`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 单号 | varchar；字节长度 50 | 否 | CharField |
| ShiftCode | old_shift_code | 班别 | varchar；字节长度 50 | 是 | CharField |
| StartTime | old_start_time | 放行开始时间 | datetime | 是 | DateTimeField |
| EndTime | old_end_time | 放行结束时间 | datetime | 是 | DateTimeField |
| Creator | old_creator | 创建人 | nvarchar；字节长度 40 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifier | old_modifier | 修改人 | nvarchar；字节长度 40 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| Remark | old_remark | Remark | nvarchar；字节长度 400 | 是 | CharField |

### SourceDyeOutGoingBillDetail — 其他或待确认相关表（OutGoingBillDetail，待确认）

源表：`dye.OutGoingBillDetail`；新表：`src_dye_outgoingbilldetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 否 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 50 | 否 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 50 | 是 | CharField |
| Note | old_note | Note | nvarchar；字节长度 400 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeOutGoingBill`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 OutGoingBillDetail → OutGoingBill。

### SourceDyeOutPlan — 生产工单与排程相关表（OutPlan，待确认）

源表：`dye.OutPlan`；新表：`src_dye_outplan`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| PriorityID | old_priority_id | 优先级 | varchar；字节长度 10 | 是 | CharField |
| OutKindID | old_out_kind_id | 发货类型 | varchar；字节长度 10 | 是 | CharField |
| CreditNo | old_credit_no | 信用证号 | varchar；字节长度 50 | 是 | CharField |
| ShipDate | old_ship_date | 船期 | datetime | 是 | DateTimeField |
| BoxDate | old_box_date | 装箱日期 | datetime | 是 | DateTimeField |
| BoxTypeID | old_box_type_id | 箱型 | varchar；字节长度 10 | 是 | CharField |
| ForwarderID | old_forwarder_id | 货运公司 | varchar；字节长度 10 | 是 | CharField |
| Linker | old_linker | 联系人 | varchar；字节长度 10 | 是 | CharField |
| LinkerInfo | old_linker_info | 联系人信息 | varchar；字节长度 100 | 是 | CharField |
| Fee1 | old_fee1 | 费用1 | decimal(10,2) | 是 | DecimalField |
| Fee2 | old_fee2 | 费用2 | decimal(10,2) | 是 | DecimalField |
| Fee3 | old_fee3 | 费用3 | decimal(10,2) | 是 | DecimalField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员代码 | varchar；字节长度 10 | 是 | CharField |
| CustomsCheckNo | old_customs_check_no | 海关核销单号 | varchar；字节长度 20 | 是 | CharField |
| ToPlace | old_to_place | 交货地点 | varchar；字节长度 50 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 500 | 是 | CharField |
| StorageUnitID | old_storage_unit_id | 仓位代码 | varchar；字节长度 10 | 是 | CharField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |

### SourceDyeOutPlanDetail — 生产工单与排程相关表（OutPlanDetail，待确认）

源表：`dye.OutPlanDetail`；新表：`src_dye_outplandetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 表单明细号（子表） | varchar；字节长度 20 | 否 | CharField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 20 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| ColorE | old_color_e | ColorE | varchar；字节长度 20 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| OutQty | old_out_qty | 出库数量 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| Amount | old_amount | Amount | decimal(10,2) | 是 | DecimalField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| JobDetailNo | old_job_detail_no | 加工作业号 | varchar；字节长度 20 | 是 | CharField |
| Structure | old_structure | 组织 | varchar；字节长度 50 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 30 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 50 | 是 | CharField |
| toaddress | old_toaddress | 送货地址 | varchar；字节长度 500 | 是 | CharField |
| WeightQty | old_weight_qty | 数量 | decimal(9,2) | 是 | DecimalField |
| CurrStatus | old_curr_status | 当前状态 | varchar；字节长度 500 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeOutPlan`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 OutPlanDetail → OutPlan。

### SourceDyePackQty — 其他或待确认相关表（PackQty，待确认）

源表：`dye.PackQty`；新表：`src_dye_packqty`；原主键：无主键。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 50 | 是 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 50 | 是 | CharField |
| Qty | old_qty | Qty | float | 是 | FloatField |
| EndTime | old_end_time | EndTime | varchar；字节长度 10 | 是 | CharField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 50 | 是 | CharField |

### SourceDyePackQty1 — 其他或待确认相关表（PackQty1，待确认）

源表：`dye.PackQty1`；新表：`src_dye_packqty1`；原主键：无主键。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 50 | 是 | CharField |
| CurrRolls | old_curr_rolls | CurrRolls | int | 是 | IntegerField |
| CurrKg | old_curr_kg | CurrKg | float | 是 | FloatField |

### SourceDyePackWorkQty — 生产工单与排程相关表（PackWorkQty，待确认）

源表：`dye.PackWorkQty`；新表：`src_dye_packworkqty`；原主键：ID。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | varchar；字节长度 50 | 否 | CharField |
| OrderSheetNo | old_order_sheet_no | OrderSheetNo | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 150 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 150 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 150 | 是 | CharField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 150 | 是 | CharField |
| ShiftName | old_shift_name | ShiftName | varchar；字节长度 150 | 是 | CharField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 150 | 是 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 150 | 是 | CharField |
| YEARS | old_years | YEARS | varchar；字节长度 10 | 是 | CharField |
| StartTime | old_start_time | StartTime | varchar；字节长度 10 | 是 | CharField |
| DAYS | old_days | DAYS | varchar；字节长度 10 | 是 | CharField |
| CurrRolls | old_curr_rolls | CurrRolls | int | 是 | IntegerField |
| CurrKg | old_curr_kg | CurrKg | float | 是 | FloatField |
| Qty | old_qty | Qty | float | 是 | FloatField |
| Price | old_price | Price | float | 是 | FloatField |
| WorkMoney | old_work_money | WorkMoney | float | 是 | FloatField |

### SourceDyePackWorkQty1 — 生产工单与排程相关表（PackWorkQty1，待确认）

源表：`dye.PackWorkQty1`；新表：`src_dye_packworkqty1`；原主键：ID。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | varchar；字节长度 50 | 否 | CharField |
| OrderSheetNo | old_order_sheet_no | OrderSheetNo | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 150 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 150 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 150 | 是 | CharField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 150 | 是 | CharField |
| ShiftName | old_shift_name | ShiftName | varchar；字节长度 150 | 是 | CharField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 150 | 是 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 150 | 是 | CharField |
| YEARS | old_years | YEARS | varchar；字节长度 10 | 是 | CharField |
| StartTime | old_start_time | StartTime | varchar；字节长度 10 | 是 | CharField |
| DAYS | old_days | DAYS | varchar；字节长度 10 | 是 | CharField |
| CurrRolls | old_curr_rolls | CurrRolls | int | 是 | IntegerField |
| CurrKg | old_curr_kg | CurrKg | float | 是 | FloatField |
| Qty | old_qty | Qty | float | 是 | FloatField |
| Price | old_price | Price | float | 是 | FloatField |
| WorkMoney | old_work_money | WorkMoney | float | 是 | FloatField |

### SourceDyePackWorkQtyDetail — 生产工单与排程相关表（PackWorkQtyDetail，待确认）

源表：`dye.PackWorkQtyDetail`；新表：`src_dye_packworkqtydetail`；原主键：无主键。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 50 | 是 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 50 | 是 | CharField |
| Qty | old_qty | Qty | float | 是 | FloatField |
| EndTime | old_end_time | EndTime | varchar；字节长度 10 | 是 | CharField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 50 | 是 | CharField |

### SourceDyePackWorkSumQty — 生产工单与排程相关表（PackWorkSumQty，待确认）

源表：`dye.PackWorkSumQty`；新表：`src_dye_packworksumqty`；原主键：无主键。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 50 | 是 | CharField |
| CurrRolls | old_curr_rolls | CurrRolls | int | 是 | IntegerField |
| CurrKg | old_curr_kg | CurrKg | float | 是 | FloatField |

### SourceDyeProdIn — 成品入库单

源表：`dye.ProdIn`；新表：`src_dye_prodin`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| IsInputRecord | old_is_input_record | 录入码单明细否 | bit | 是 | BooleanField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| StockUnit | old_stock_unit | 单位 | tinyint | 是 | IntegerField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员代码 | varchar；字节长度 10 | 是 | CharField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| BusinessKind | old_business_kind | 业务类别 | smallint | 是 | IntegerField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 250 | 是 | CharField |
| Spec | old_spec | 捻度(H/S) | varchar；字节长度 128 | 是 | CharField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 50 | 是 | CharField |
| StorageUnitID | old_storage_unit_id | 仓位代码 | varchar；字节长度 200 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库代码 | varchar；字节长度 10 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 毛重 | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度数量 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| Amount | old_amount | 金额 | decimal(10,2) | 是 | DecimalField |
| Total | old_total | 合计 | decimal(10,2) | 是 | DecimalField |
| TubeWeight | old_tube_weight | 筒管重 | decimal(6,2) | 是 | DecimalField |
| ProcessPrice | old_process_price | 特殊工艺价格 | decimal(8,2) | 是 | DecimalField |
| ProcessMemo | old_process_memo | 另收费项目 | varchar；字节长度 300 | 是 | CharField |
| AtteMemo | old_atte_memo | AtteMemo | varchar；字节长度 300 | 是 | CharField |
| AtteFee | old_atte_fee | 特殊要求价格 | decimal(10,2) | 是 | DecimalField |
| VatFee | old_vat_fee | VatFee | decimal(10,2) | 是 | DecimalField |
| RealLoss | old_real_loss | 损耗 | decimal(6,2) | 是 | DecimalField |
| Loss | old_loss | 损耗 | varchar；字节长度 50 | 是 | CharField |
| AdjustedLoss | old_adjusted_loss | AdjustedLoss | decimal(6,2) | 是 | DecimalField |
| Weight | old_weight | 克重 | varchar；字节长度 50 | 是 | CharField |
| Width | old_width | 幅宽 | varchar；字节长度 50 | 是 | CharField |
| WidthKindID | old_width_kind_id | WidthKindID | varchar；字节长度 50 | 是 | CharField |
| WeightUnit | old_weight_unit | WeightUnit | tinyint | 是 | IntegerField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| DetailsCustomer | old_details_customer | DetailsCustomer | varchar；字节长度 150 | 是 | CharField |
| BaseBoard | old_base_board | 底板号 | varchar；字节长度 50 | 是 | CharField |
| CustJobNo | old_cust_job_no | 客户缸号 | varchar；字节长度 100 | 是 | CharField |
| SumAssignedLengthQty | old_sum_assigned_length_qty | 投胚米数 | decimal(10,2) | 是 | DecimalField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 20 | 是 | CharField |
| Keeper | old_keeper | 仓管员 | varchar；字节长度 16 | 是 | CharField |
| WarpDensity | old_warp_density | 经密 | varchar；字节长度 50 | 是 | CharField |
| WeftDensity | old_weft_density | 纬密 | varchar；字节长度 50 | 是 | CharField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 250 | 是 | CharField |
| Cargador1 | old_cargador1 | 装/配工 | varchar；字节长度 10 | 是 | CharField |
| Cargador2 | old_cargador2 | 装/配工 | varchar；字节长度 10 | 是 | CharField |
| Cargador3 | old_cargador3 | 装/配工 | varchar；字节长度 10 | 是 | CharField |
| Cargador4 | old_cargador4 | 装/配工 | varchar；字节长度 10 | 是 | CharField |
| Cargador5 | old_cargador5 | 装/配工 | varchar；字节长度 10 | 是 | CharField |
| PhaseID | old_phase_id | PhaseID | varchar；字节长度 10 | 是 | CharField |
| GaryWeight | old_gary_weight | 胚重 | decimal(10,2) | 是 | DecimalField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 100 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 50 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 500 | 是 | CharField |
| Area | old_area | 区域 | varchar；字节长度 100 | 是 | CharField |
| ShipMentType | old_ship_ment_type | 出货方式 | varchar；字节长度 50 | 是 | CharField |
| PlasticBags | old_plastic_bags | 胶袋 | decimal(4,2) | 是 | DecimalField |
| ColorE | old_color_e | ColorE | varchar；字节长度 20 | 是 | CharField |
| ColorRemarks | old_color_remarks | 用途 | varchar；字节长度 500 | 是 | CharField |
| packremarks | old_packremarks | packremarks | varchar；字节长度 255 | 是 | CharField |
| JXTDDH | old_jxtddh | JXTDDH | varchar；字节长度 255 | 是 | CharField |
| ProdInOriSheetNo | old_prod_in_ori_sheet_no | ProdInOriSheetNo | varchar；字节长度 50 | 是 | CharField |
| YarnCategory | old_yarn_category | 纱类别 | varchar；字节长度 50 | 是 | CharField |
| NetKg | old_net_kg | 净重 | decimal(10,2) | 是 | DecimalField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 500 | 是 | CharField |
| ProdOutSheetSeries | old_prod_out_sheet_series | ProdOutSheetSeries | varchar；字节长度 30 | 是 | CharField |

### SourceDyeProdInTo — 坯布半成品成品与仓储相关表（ProdIn_to，待确认）

源表：`dye.ProdIn_to`；新表：`src_dye_prodin_to`；原主键：BarCode。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| StockUnit | old_stock_unit | StockUnit | tinyint | 是 | IntegerField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 250 | 是 | CharField |
| FabricID | old_fabric_id | FabricID | varchar；字节长度 250 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 20 | 是 | CharField |
| CustColorNum | old_cust_color_num | CustColorNum | varchar；字节长度 100 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 是 | CharField |
| StorageUnitID | old_storage_unit_id | StorageUnitID | varchar；字节长度 10 | 是 | CharField |
| Area | old_area | Area | varchar；字节长度 100 | 是 | CharField |
| SumRolls | old_sum_rolls | SumRolls | decimal(7,2) | 是 | DecimalField |
| SumWeightQty | old_sum_weight_qty | SumWeightQty | decimal(10,1) | 是 | DecimalField |
| SumGaryWeight | old_sum_gary_weight | SumGaryWeight | decimal(10,2) | 是 | DecimalField |
| SumLengthQty | old_sum_length_qty | SumLengthQty | decimal(10,2) | 是 | DecimalField |
| AtteFee | old_atte_fee | AtteFee | decimal(10,2) | 是 | DecimalField |
| VatFee | old_vat_fee | VatFee | decimal(10,2) | 是 | DecimalField |
| Width | old_width | Width | decimal(10,2) | 是 | DecimalField |
| Weight | old_weight | Weight | decimal(10,2) | 是 | DecimalField |
| BarCode | old_bar_code | BarCode | varchar；字节长度 50 | 否 | CharField |
| RollNo | old_roll_no | RollNo | varchar；字节长度 20 | 是 | CharField |
| GrayQty | old_gray_qty | GrayQty | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | WeightQty | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | LengthQty | decimal(10,2) | 是 | DecimalField |

### SourceDyeProdInPDARecord — 坯布半成品成品与仓储相关表（ProdInPDARecord，待确认）

源表：`dye.ProdInPDARecord`；新表：`src_dye_prodinpdarecord`；原主键：BarCode。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| BarCode | old_bar_code | BarCode | varchar；字节长度 50 | 否 | CharField |
| CurrTime | old_curr_time | CurrTime | datetime | 是 | DateTimeField |
| Geter | old_geter | Geter | varchar；字节长度 10 | 是 | CharField |
| StorageUnitID | old_storage_unit_id | StorageUnitID | varchar；字节长度 10 | 是 | CharField |
| Status | old_status | Status | varchar；字节长度 1 | 是 | CharField |

### SourceDyeProdInPriceAtte — 财务结算与成本相关表（ProdInPriceAtte，待确认）

源表：`dye.ProdInPriceAtte`；新表：`src_dye_prodinpriceatte`；原主键：SheetSeries, FieldType, AtteCode。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| AtteCode | old_atte_code | 要求代码 | varchar；字节长度 10 | 否 | CharField |
| Price | old_price | 单价 | decimal(8,2) | 是 | DecimalField |
| PriceUnit | old_price_unit | 计价单位 | tinyint | 是 | IntegerField |
| FieldType | old_field_type | 要求类别 | varchar；字节长度 20 | 否 | CharField |
| AtteValue | old_atte_value | 事项内容 | varchar；字节长度 500 | 是 | CharField |
| Description | old_description | 描述 | varchar；字节长度 500 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeProdIn`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ProdInPriceAtte → ProdIn。

### SourceDyeProdInPriceProcess — 财务结算与成本相关表（ProdInPriceProcess，待确认）

源表：`dye.ProdInPriceProcess`；新表：`src_dye_prodinpriceprocess`；原主键：SheetSeries, ProcessID。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| ProcessID | old_process_id | 工序 | varchar；字节长度 50 | 否 | CharField |
| Price | old_price | 单价 | decimal(8,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 300 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeProdIn`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ProdInPriceProcess → ProdIn。

### SourceDyeProdInRecord — 成品入库卷记录

源表：`dye.ProdInRecord`；新表：`src_dye_prodinrecord`；原主键：SheetSeries, RollNo, BarCode。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| RollNo | old_roll_no | 箱号 | varchar；字节长度 20 | 否 | CharField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 成品重(毛重) | decimal(10,1) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 仓位代码 | varchar；字节长度 10 | 是 | CharField |
| Status | old_status | 状态 | varchar；字节长度 1 | 是 | CharField |
| OutDetailNo | old_out_detail_no | 出库单明细号 | varchar；字节长度 20 | 是 | CharField |
| BarCode | old_bar_code | 条码 | varchar；字节长度 50 | 否 | CharField |
| GradeID | old_grade_id | 等级 | varchar；字节长度 10 | 是 | CharField |
| GrayQty | old_gray_qty | GrayQty | decimal(10,2) | 是 | DecimalField |
| AdjustQty | old_adjust_qty | AdjustQty | decimal(10,2) | 是 | DecimalField |
| RealQty | old_real_qty | 磅重 | decimal(10,2) | 是 | DecimalField |
| Meter | old_meter | 成品长 | decimal(10,2) | 是 | DecimalField |
| Yard | old_yard | 码数 | decimal(10,2) | 是 | DecimalField |
| Note | old_note | 备注 | varchar；字节长度 50 | 是 | CharField |
| GrayBarCode | old_gray_bar_code | GrayBarCode | varchar；字节长度 100 | 是 | CharField |
| RollNo3 | old_roll_no3 | RollNo3 | varchar；字节长度 20 | 是 | CharField |
| GUnit | old_gunit | GUnit | tinyint | 是 | IntegerField |
| PUnit | old_punit | PUnit | tinyint | 是 | IntegerField |
| ProdBarCode | old_prod_bar_code | 包装条码 | varchar；字节长度 200 | 是 | CharField |
| InPacks | old_in_packs | 件数 | decimal(6,1) | 是 | DecimalField |
| InRolls | old_in_rolls | 粒数 | decimal(6,1) | 是 | DecimalField |
| EmptyPlus | old_empty_plus | 空加 | decimal(6,2) | 是 | DecimalField |
| LabelLength | old_label_length | LabelLength | decimal(6,2) | 是 | DecimalField |
| NetKg | old_net_kg | 净重 | decimal(6,2) | 是 | DecimalField |
| PackBag | old_pack_bag | 包装重量 | decimal(7,3) | 是 | DecimalField |
| TubeWeight | old_tube_weight | 纸筒重 | decimal(7,3) | 是 | DecimalField |
| ProdCode | old_prod_code | 二维码字段 | varchar；字节长度 50 | 是 | CharField |
| LabelWareHouse | old_label_ware_house | 标签仓库 | varchar；字节长度 100 | 是 | CharField |
| LabelRemarks | old_label_remarks | 标签用途 | varchar；字节长度 500 | 是 | CharField |
| WindingID | old_winding_id | 络筒员工 | varchar；字节长度 30 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| ColorRemarks | old_color_remarks | 用途 | varchar；字节长度 500 | 是 | CharField |
| OutDetatilNo | old_out_detatil_no | 出库明细单号 | varchar；字节长度 30 | 是 | CharField |
| FenTou | old_fen_tou | 分头 | decimal(6,2) | 是 | DecimalField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeProdIn`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ProdInRecordWork → ProdInWork；原界面主从 ProdInRecord_ht → ProdIn_ht；原界面主从 ProdInRecord → ProdIn。

### SourceDyeProdLoading — 坯布半成品成品与仓储相关表（ProdLoading，待确认）

源表：`dye.ProdLoading`；新表：`src_dye_prodloading`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| IsInputRecord | old_is_input_record | 录入码单明细否 | bit | 是 | BooleanField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员代码 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| FactID | old_fact_id | 工厂代码 | varchar；字节长度 10 | 是 | CharField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| BusinessKind | old_business_kind | BusinessKind | smallint | 是 | IntegerField |
| Discount | old_discount | 折扣 | decimal(3,2) | 是 | DecimalField |
| PriceCheck | old_price_check | 价格审核 | bit | 是 | BooleanField |
| PriceChecker | old_price_checker | 价格审核人 | varchar；字节长度 10 | 是 | CharField |
| PriceCheckIdea | old_price_check_idea | 价格审核意见 | varchar；字节长度 300 | 是 | CharField |
| PriceCheckTime | old_price_check_time | 价格审核时间 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| WareHouseID | old_ware_house_id | 存放仓库 | varchar；字节长度 10 | 是 | CharField |
| Cargador1 | old_cargador1 | 目标客户 | nvarchar；字节长度 20 | 是 | CharField |
| Cargador2 | old_cargador2 | 搬运工 | nvarchar；字节长度 20 | 是 | CharField |
| Cargador3 | old_cargador3 | 搬运工 | nvarchar；字节长度 20 | 是 | CharField |
| Cargador4 | old_cargador4 | 搬运工 | nvarchar；字节长度 20 | 是 | CharField |
| Cargador5 | old_cargador5 | 搬运工 | nvarchar；字节长度 20 | 是 | CharField |
| Driver1 | old_driver1 | 司机电话 | nvarchar；字节长度 20 | 是 | CharField |
| Driver2 | old_driver2 | 叉车 | nvarchar；字节长度 20 | 是 | CharField |
| Driver3 | old_driver3 | 叉车 | nvarchar；字节长度 20 | 是 | CharField |
| Discharger1 | old_discharger1 | 装卸工 | nvarchar；字节长度 20 | 是 | CharField |
| Discharger2 | old_discharger2 | 装卸工 | nvarchar；字节长度 20 | 是 | CharField |
| Driver | old_driver | 司机 | nvarchar；字节长度 20 | 是 | CharField |
| CarNo | old_car_no | 车牌号 | nvarchar；字节长度 20 | 是 | CharField |
| Keeper | old_keeper | 仓管员 | varchar；字节长度 16 | 是 | CharField |
| DlvRolls | old_dlv_rolls | DlvRolls | decimal(6,1) | 是 | DecimalField |
| DlvLengthQty | old_dlv_length_qty | DlvLengthQty | decimal(10,2) | 是 | DecimalField |
| DlvWeightQty | old_dlv_weight_qty | DlvWeightQty | decimal(10,2) | 是 | DecimalField |
| DlvAddress | old_dlv_address | 送货地址 | nvarchar；字节长度 600 | 是 | CharField |
| Phone | old_phone | 司机电话 | varchar；字节长度 20 | 是 | CharField |
| CustomerCode | old_customer_code | 客户全称 | varchar；字节长度 50 | 是 | CharField |
| WLLX | old_wllx | 物流类型 | varchar；字节长度 255 | 是 | CharField |
| combo1 | old_combo1 | 收发地点 | varchar；字节长度 10 | 是 | CharField |
| FHYSPC | old_fhyspc | 送货运输编号 | varchar；字节长度 20 | 是 | CharField |
| RoundTrip | old_round_trip | 往返 | varchar；字节长度 20 | 是 | CharField |
| Contacter | old_contacter | 联系人 | varchar；字节长度 50 | 是 | CharField |
| ContactNumber | old_contact_number | 联系电话 | varchar；字节长度 50 | 是 | CharField |
| ContractNumber | old_contract_number | 合同号码 | varchar；字节长度 50 | 是 | CharField |
| DHSD_FEI | old_dhsd_fei | 大货速递费 | decimal(18,4) | 是 | DecimalField |
| TY_FEI | old_ty_fei | 托运费 | decimal(18,4) | 是 | DecimalField |

### SourceDyeProdLoadingDetail — 坯布半成品成品与仓储相关表（ProdLoadingDetail，待确认）

源表：`dye.ProdLoadingDetail`；新表：`src_dye_prodloadingdetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 否 | CharField |
| LineNumber | old_line_number | 行号 | varchar；字节长度 20 | 是 | CharField |
| CustomerIDName | old_customer_idname | 客户 | varchar；字节长度 50 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 500 | 是 | CharField |
| Structure | old_structure | Structure | varchar；字节长度 500 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 350 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 50 | 是 | CharField |
| OutRolls | old_out_rolls | OutRolls | decimal(7,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | WeightQty | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | LengthQty | decimal(10,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| Amount | old_amount | Amount | decimal(10,2) | 是 | DecimalField |
| Weight | old_weight | Weight | varchar；字节长度 50 | 是 | CharField |
| Width | old_width | Width | varchar；字节长度 50 | 是 | CharField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 是 | CharField |
| ARDetailNo | old_ardetail_no | ARDetailNo | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 -1 | 是 | TextField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| StockUnit | old_stock_unit | StockUnit | tinyint | 是 | IntegerField |
| Total | old_total | Total | decimal(10,2) | 是 | DecimalField |
| ProcessPrice | old_process_price | ProcessPrice | decimal(8,2) | 是 | DecimalField |
| AtteFee | old_atte_fee | AtteFee | decimal(10,2) | 是 | DecimalField |
| VatFee | old_vat_fee | VatFee | decimal(10,2) | 是 | DecimalField |
| ProcessMemo | old_process_memo | ProcessMemo | varchar；字节长度 -1 | 是 | TextField |
| Atte | old_atte | Atte | varchar；字节长度 100 | 是 | CharField |
| InSheetNo | old_in_sheet_no | InSheetNo | varchar；字节长度 20 | 是 | CharField |
| InPrice | old_in_price | InPrice | decimal(8,2) | 是 | DecimalField |
| InProcessPrice | old_in_process_price | InProcessPrice | decimal(8,2) | 是 | DecimalField |
| InAtteFee | old_in_atte_fee | InAtteFee | decimal(10,2) | 是 | DecimalField |
| InVatFee | old_in_vat_fee | InVatFee | decimal(10,2) | 是 | DecimalField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| WidthDn | old_width_dn | WidthDn | decimal(6,2) | 是 | DecimalField |
| WidthUp | old_width_up | WidthUp | decimal(6,2) | 是 | DecimalField |
| WeightDn | old_weight_dn | WeightDn | decimal(6,2) | 是 | DecimalField |
| WeightUp | old_weight_up | WeightUp | decimal(6,2) | 是 | DecimalField |
| WeightUnit | old_weight_unit | WeightUnit | varchar；字节长度 10 | 是 | CharField |
| WidthKindID | old_width_kind_id | WidthKindID | varchar；字节长度 10 | 是 | CharField |
| PreRolls | old_pre_rolls | 排单粒数 | decimal(7,2) | 是 | DecimalField |
| DetailsCustomer | old_details_customer | DetailsCustomer | varchar；字节长度 120 | 是 | CharField |
| OrderSheetDate | old_order_sheet_date | OrderSheetDate | datetime | 是 | DateTimeField |
| AttPrice | old_att_price | AttPrice | decimal(8,2) | 是 | DecimalField |
| ColorAddPrice | old_color_add_price | ColorAddPrice | decimal(8,2) | 是 | DecimalField |
| ColorAddFee | old_color_add_fee | ColorAddFee | decimal(10,2) | 是 | DecimalField |
| SumAssignedLengthQty | old_sum_assigned_length_qty | SumAssignedLengthQty | decimal(10,2) | 是 | DecimalField |
| CustJobNo | old_cust_job_no | CustJobNo | varchar；字节长度 200 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 20 | 是 | CharField |
| WarpDensity | old_warp_density | WarpDensity | varchar；字节长度 50 | 是 | CharField |
| WeftDensity | old_weft_density | WeftDensity | varchar；字节长度 50 | 是 | CharField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 250 | 是 | CharField |
| GrayQty | old_gray_qty | GrayQty | decimal(10,2) | 是 | DecimalField |
| Jobattes1 | old_jobattes1 | Jobattes1 | decimal(10,2) | 是 | DecimalField |
| Jobattes2 | old_jobattes2 | Jobattes2 | varchar；字节长度 -1 | 是 | TextField |
| CustColorNum | old_cust_color_num | CustColorNum | varchar；字节长度 100 | 是 | CharField |
| PriceUnit | old_price_unit | PriceUnit | tinyint | 是 | IntegerField |
| PhaseID | old_phase_id | PhaseID | varchar；字节长度 10 | 是 | CharField |
| Jobattes3 | old_jobattes3 | Jobattes3 | decimal(10,1) | 是 | DecimalField |
| Jobattes4 | old_jobattes4 | Jobattes4 | decimal(10,1) | 是 | DecimalField |
| Jobattes5 | old_jobattes5 | Jobattes5 | varchar；字节长度 -1 | 是 | TextField |
| Jobattes6 | old_jobattes6 | Jobattes6 | varchar；字节长度 200 | 是 | CharField |
| Jobattes7 | old_jobattes7 | Jobattes7 | varchar；字节长度 200 | 是 | CharField |
| Jobattes8 | old_jobattes8 | Jobattes8 | varchar；字节长度 200 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 500 | 是 | CharField |
| CustGrayID | old_cust_gray_id | CustGrayID | varchar；字节长度 50 | 是 | CharField |
| GRealLoss | old_greal_loss | GRealLoss | decimal(10,2) | 是 | DecimalField |
| ColorE | old_color_e | ColorE | varchar；字节长度 20 | 是 | CharField |
| ColorRemarks | old_color_remarks | 用途 | varchar；字节长度 500 | 是 | CharField |
| OrderSheetNo | old_order_sheet_no | OrderSheetNo | varchar；字节长度 50 | 是 | CharField |
| Model1 | old_model1 | Model1 | varchar；字节长度 200 | 是 | CharField |
| PackRemarks | old_pack_remarks | PackRemarks | varchar；字节长度 -1 | 是 | TextField |
| jobattes9 | old_jobattes9 | jobattes9 | nvarchar；字节长度 200 | 是 | CharField |
| jobattes10 | old_jobattes10 | jobattes10 | decimal(10,1) | 是 | DecimalField |
| OutDetailNo | old_out_detail_no | 出库明细单号 | varchar；字节长度 40 | 是 | CharField |
| ProdBarCode | old_prod_bar_code | 条码 | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeProdLoading`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ProdLoadingDetail → ProdLoading；原界面主从 ProdLoadApproveDetail → ProdLoadApprove。

### SourceDyeProdOut — 成品出库单

源表：`dye.ProdOut`；新表：`src_dye_prodout`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| IsInputRecord | old_is_input_record | 录入码单明细否 | bit | 是 | BooleanField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员代码 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| FactID | old_fact_id | 工厂代码 | varchar；字节长度 10 | 是 | CharField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| BusinessKind | old_business_kind | BusinessKind | smallint | 是 | IntegerField |
| Discount | old_discount | 折扣 | decimal(3,2) | 是 | DecimalField |
| PriceCheck | old_price_check | 价格审核 | bit | 是 | BooleanField |
| PriceChecker | old_price_checker | 价格审核人 | varchar；字节长度 10 | 是 | CharField |
| PriceCheckIdea | old_price_check_idea | 价格审核意见 | varchar；字节长度 300 | 是 | CharField |
| PriceCheckTime | old_price_check_time | 价格审核时间 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| WareHouseID | old_ware_house_id | 存放仓库 | varchar；字节长度 10 | 是 | CharField |
| Cargador1 | old_cargador1 | 目标客户 | nvarchar；字节长度 20 | 是 | CharField |
| Cargador2 | old_cargador2 | 搬运工 | nvarchar；字节长度 20 | 是 | CharField |
| Cargador3 | old_cargador3 | 搬运工 | nvarchar；字节长度 20 | 是 | CharField |
| Cargador4 | old_cargador4 | 搬运工 | nvarchar；字节长度 20 | 是 | CharField |
| Cargador5 | old_cargador5 | 搬运工 | nvarchar；字节长度 20 | 是 | CharField |
| Driver1 | old_driver1 | 司机电话 | nvarchar；字节长度 20 | 是 | CharField |
| Driver2 | old_driver2 | 叉车 | nvarchar；字节长度 20 | 是 | CharField |
| Driver3 | old_driver3 | 叉车 | nvarchar；字节长度 20 | 是 | CharField |
| Discharger1 | old_discharger1 | 装卸工 | nvarchar；字节长度 20 | 是 | CharField |
| Discharger2 | old_discharger2 | 装卸工 | nvarchar；字节长度 20 | 是 | CharField |
| Driver | old_driver | 司机 | nvarchar；字节长度 20 | 是 | CharField |
| CarNo | old_car_no | 车牌号 | nvarchar；字节长度 20 | 是 | CharField |
| Keeper | old_keeper | 仓管员 | varchar；字节长度 16 | 是 | CharField |
| DlvRolls | old_dlv_rolls | DlvRolls | decimal(6,1) | 是 | DecimalField |
| DlvLengthQty | old_dlv_length_qty | DlvLengthQty | decimal(10,2) | 是 | DecimalField |
| DlvWeightQty | old_dlv_weight_qty | 毛重 | decimal(10,2) | 是 | DecimalField |
| DlvAddress | old_dlv_address | 送货地址 | nvarchar；字节长度 600 | 是 | CharField |
| Phone | old_phone | 司机电话 | varchar；字节长度 20 | 是 | CharField |
| CustomerCode | old_customer_code | 客户全称 | varchar；字节长度 50 | 是 | CharField |
| WLLX | old_wllx | 物流类型 | varchar；字节长度 255 | 是 | CharField |
| combo1 | old_combo1 | 收发地点 | varchar；字节长度 10 | 是 | CharField |
| FHYSPC | old_fhyspc | 送货运输编号 | varchar；字节长度 20 | 是 | CharField |
| UpCheckNo | old_up_check_no | 调整订单号 | varchar；字节长度 30 | 是 | CharField |
| UpLabelRemarks | old_up_label_remarks | UpLabelRemarks | varchar；字节长度 500 | 是 | CharField |
| UpLabelWareHouse | old_up_label_ware_house | UpLabelWareHouse | varchar；字节长度 100 | 是 | CharField |

### SourceDyeProdOutDetail — 成品出库明细

源表：`dye.ProdOutDetail`；新表：`src_dye_prodoutdetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | 表单明细号（子表） | varchar；字节长度 36 | 否 | CharField |
| Spec | old_spec | 捻度(H/S) | varchar；字节长度 500 | 是 | CharField |
| Structure | old_structure | 组织 | varchar；字节长度 500 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 350 | 是 | CharField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 50 | 是 | CharField |
| OutRolls | old_out_rolls | 出库粒数 | decimal(7,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 毛重 | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 成品长度 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 价格 | decimal(8,2) | 是 | DecimalField |
| Amount | old_amount | 金额 | decimal(10,2) | 是 | DecimalField |
| Weight | old_weight | 克重 | varchar；字节长度 50 | 是 | CharField |
| Width | old_width | 幅宽 | varchar；字节长度 50 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| ARDetailNo | old_ardetail_no | 应收单细号 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 -1 | 是 | TextField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| StockUnit | old_stock_unit | 库存单位 | tinyint | 是 | IntegerField |
| Total | old_total | 合计 | decimal(10,2) | 是 | DecimalField |
| ProcessPrice | old_process_price | 特殊工序单价 | decimal(8,2) | 是 | DecimalField |
| AtteFee | old_atte_fee | 纸筒 | decimal(10,2) | 是 | DecimalField |
| VatFee | old_vat_fee | 空加 | decimal(10,2) | 是 | DecimalField |
| ProcessMemo | old_process_memo | ProcessMemo | varchar；字节长度 -1 | 是 | TextField |
| Atte | old_atte | 事项 | varchar；字节长度 100 | 是 | CharField |
| InSheetNo | old_in_sheet_no | InSheetNo | varchar；字节长度 20 | 是 | CharField |
| InPrice | old_in_price | InPrice | decimal(8,2) | 是 | DecimalField |
| InProcessPrice | old_in_process_price | InProcessPrice | decimal(8,2) | 是 | DecimalField |
| InAtteFee | old_in_atte_fee | InAtteFee | decimal(10,2) | 是 | DecimalField |
| InVatFee | old_in_vat_fee | InVatFee | decimal(10,2) | 是 | DecimalField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| WidthDn | old_width_dn | 门幅下限 | decimal(6,2) | 是 | DecimalField |
| WidthUp | old_width_up | 门幅上限 | decimal(6,2) | 是 | DecimalField |
| WeightDn | old_weight_dn | 克重下限 | decimal(6,2) | 是 | DecimalField |
| WeightUp | old_weight_up | 克重上限 | decimal(6,2) | 是 | DecimalField |
| WeightUnit | old_weight_unit | 克重单位 | varchar；字节长度 10 | 是 | CharField |
| WidthKindID | old_width_kind_id | 门幅单位 | varchar；字节长度 10 | 是 | CharField |
| PreRolls | old_pre_rolls | 排单粒数 | decimal(7,2) | 是 | DecimalField |
| DetailsCustomer | old_details_customer | 织厂 | varchar；字节长度 120 | 是 | CharField |
| OrderSheetDate | old_order_sheet_date | 下单日期 | datetime | 是 | DateTimeField |
| AttPrice | old_att_price | 特殊要求单价 | decimal(8,2) | 是 | DecimalField |
| ColorAddPrice | old_color_add_price | 色号加价 | decimal(8,2) | 是 | DecimalField |
| ColorAddFee | old_color_add_fee | ColorAddFee | decimal(10,2) | 是 | DecimalField |
| SumAssignedLengthQty | old_sum_assigned_length_qty | 胚纱长度 | decimal(10,2) | 是 | DecimalField |
| CustJobNo | old_cust_job_no | 客户缸号 | varchar；字节长度 200 | 是 | CharField |
| ColorDepthID | old_color_depth_id | 颜色深浅 | varchar；字节长度 20 | 是 | CharField |
| WarpDensity | old_warp_density | WarpDensity | varchar；字节长度 50 | 是 | CharField |
| WeftDensity | old_weft_density | WeftDensity | varchar；字节长度 50 | 是 | CharField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 250 | 是 | CharField |
| GrayQty | old_gray_qty | 胚重 | decimal(10,2) | 是 | DecimalField |
| Jobattes1 | old_jobattes1 | 加工要求 | varchar；字节长度 -1 | 是 | TextField |
| Jobattes2 | old_jobattes2 | 收费项目 | varchar；字节长度 -1 | 是 | TextField |
| CustColorNum | old_cust_color_num | CustColorNum | varchar；字节长度 100 | 是 | CharField |
| PriceUnit | old_price_unit | 单价单位 | tinyint | 是 | IntegerField |
| PhaseID | old_phase_id | 套染 | varchar；字节长度 10 | 是 | CharField |
| Jobattes3 | old_jobattes3 | 幅宽 | nvarchar；字节长度 1000 | 是 | CharField |
| Jobattes4 | old_jobattes4 | 克重 | nvarchar；字节长度 200 | 是 | CharField |
| Jobattes5 | old_jobattes5 | Jobattes5 | varchar；字节长度 -1 | 是 | TextField |
| Jobattes6 | old_jobattes6 | Jobattes6 | varchar；字节长度 200 | 是 | CharField |
| Jobattes7 | old_jobattes7 | 胶袋 | varchar；字节长度 200 | 是 | CharField |
| Jobattes8 | old_jobattes8 | 加重 | varchar；字节长度 200 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 500 | 是 | CharField |
| CustGrayID | old_cust_gray_id | CustGrayID | varchar；字节长度 50 | 是 | CharField |
| GRealLoss | old_greal_loss | GRealLoss | decimal(10,2) | 是 | DecimalField |
| ColorE | old_color_e | ColorE | varchar；字节长度 20 | 是 | CharField |
| ColorRemarks | old_color_remarks | 用途 | varchar；字节长度 500 | 是 | CharField |
| OrderSheetNo | old_order_sheet_no | 本厂订单号 | varchar；字节长度 50 | 是 | CharField |
| Model1 | old_model1 | 款号 | varchar；字节长度 200 | 是 | CharField |
| PackRemarks | old_pack_remarks | 包装要求 | varchar；字节长度 -1 | 是 | TextField |
| jobattes9 | old_jobattes9 | jobattes9 | nvarchar；字节长度 200 | 是 | CharField |
| jobattes10 | old_jobattes10 | jobattes10 | nvarchar；字节长度 200 | 是 | CharField |
| BarCode | old_bar_code | 条码 | varchar；字节长度 30 | 是 | CharField |
| RollNo | old_roll_no | 箱号 | varchar；字节长度 20 | 否 | CharField |
| RealQty | old_real_qty | 磅重 | decimal(10,2) | 是 | DecimalField |
| ProdBarCode | old_prod_bar_code | 包装条码 | varchar；字节长度 200 | 是 | CharField |
| OutPacks | old_out_packs | 件数 | decimal(6,1) | 是 | DecimalField |
| NetKg | old_net_kg | 净重 | decimal(6,2) | 是 | DecimalField |
| PackBag | old_pack_bag | 包装重量 | decimal(7,3) | 是 | DecimalField |
| TubeWeight | old_tube_weight | 纸筒重 | decimal(7,3) | 是 | DecimalField |
| ProdCode | old_prod_code | 二维码字段 | varchar；字节长度 50 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 150 | 是 | CharField |
| YarnCategory | old_yarn_category | 纱类别 | varchar；字节长度 50 | 是 | CharField |
| LabelWareHouse | old_label_ware_house | 标签仓库 | varchar；字节长度 100 | 是 | CharField |
| LabelRemarks | old_label_remarks | 标签用途 | varchar；字节长度 500 | 是 | CharField |
| WindingID | old_winding_id | 络筒员工 | varchar；字节长度 30 | 是 | CharField |
| GradeID | old_grade_id | 等级 | varchar；字节长度 10 | 是 | CharField |
| FenTou | old_fen_tou | 分头 | decimal(6,2) | 是 | DecimalField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeProdOut`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ProdOutDetail → ProdOut；原界面主从 ProdOutDetailUpdate → ProdOutUpdate。

### SourceDyeProdOutPDARecord — 坯布半成品成品与仓储相关表（ProdOutPDARecord，待确认）

源表：`dye.ProdOutPDARecord`；新表：`src_dye_prodoutpdarecord`；原主键：BarCode。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| BarCode | old_bar_code | BarCode | varchar；字节长度 50 | 否 | CharField |
| CurrTime | old_curr_time | CurrTime | datetime | 是 | DateTimeField |
| Geter | old_geter | Geter | varchar；字节长度 10 | 是 | CharField |
| Status | old_status | Status | varchar；字节长度 1 | 是 | CharField |

### SourceDyeProdOutPriceAtte — 财务结算与成本相关表（ProdOutPriceAtte，待确认）

源表：`dye.ProdOutPriceAtte`；新表：`src_dye_prodoutpriceatte`；原主键：SheetSeries, DetailNo, FieldType, AtteCode。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细号 | varchar；字节长度 36 | 否 | CharField |
| AtteCode | old_atte_code | 事项代码 | varchar；字节长度 10 | 否 | CharField |
| Price | old_price | 单价 | decimal(8,2) | 是 | DecimalField |
| PriceUnit | old_price_unit | 计价单位 | tinyint | 是 | IntegerField |
| InPrice | old_in_price | 单价 | decimal(8,2) | 是 | DecimalField |
| FieldType | old_field_type | 要求类别 | varchar；字节长度 20 | 否 | CharField |
| AtteValue | old_atte_value | 事项内容 | varchar；字节长度 500 | 是 | CharField |
| Description | old_description | 描述 | varchar；字节长度 500 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeProdOutDetail`；原码 `SheetSeries, DetailNo` → 父表原码 `SheetSeries, DetailNo`；依据：原界面主从 ProdOutPriceAtte → ProdOutDetail。

### SourceDyeProdOutPriceProcess — 财务结算与成本相关表（ProdOutPriceProcess，待确认）

源表：`dye.ProdOutPriceProcess`；新表：`src_dye_prodoutpriceprocess`；原主键：SheetSeries, DetailNo, ProcessID。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 否 | CharField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 50 | 否 | CharField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 300 | 是 | CharField |
| InPrice | old_in_price | InPrice | decimal(8,2) | 是 | DecimalField |

### SourceDyeProdOutRecord — 坯布半成品成品与仓储相关表（ProdOutRecord，待确认）

源表：`dye.ProdOutRecord`；新表：`src_dye_prodoutrecord`；原主键：SheetSeries, RollNo, BarCode, DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 出库单流水号 | varchar；字节长度 20 | 否 | CharField |
| RollNo | old_roll_no | 箱号 | varchar；字节长度 20 | 否 | CharField |
| LengthQty | old_length_qty | 成品长度 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 毛重 | decimal(10,1) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 库位 | varchar；字节长度 10 | 是 | CharField |
| Status | old_status | 状态 | varchar；字节长度 1 | 是 | CharField |
| OutDetailNo | old_out_detail_no | OutDetailNo | varchar；字节长度 20 | 是 | CharField |
| BarCode | old_bar_code | 条码 | varchar；字节长度 50 | 否 | CharField |
| GradeID | old_grade_id | 色号等级 | varchar；字节长度 10 | 是 | CharField |
| GrayQty | old_gray_qty | 胚纱重量 | decimal(10,2) | 是 | DecimalField |
| AdjustQty | old_adjust_qty | AdjustQty | decimal(10,2) | 是 | DecimalField |
| DetailNo | old_detail_no | 出库明细号 | varchar；字节长度 36 | 否 | CharField |
| RealQty | old_real_qty | 实重 | decimal(10,2) | 是 | DecimalField |
| Meter | old_meter | 长度 | decimal(10,2) | 是 | DecimalField |
| Yard | old_yard | 胚纱长度 | decimal(10,2) | 是 | DecimalField |
| GrayBarCode | old_gray_bar_code | GrayBarCode | varchar；字节长度 100 | 是 | CharField |
| RollNo3 | old_roll_no3 | 箱号2 | varchar；字节长度 20 | 是 | CharField |
| GUnit | old_gunit | GUnit | tinyint | 是 | IntegerField |
| PUnit | old_punit | PUnit | tinyint | 是 | IntegerField |
| Rolls | old_rolls | 粒数 | decimal(5,1) | 是 | DecimalField |
| GKg | old_gkg | GKg | decimal(6,2) | 是 | DecimalField |
| GPound | old_gpound | GPound | decimal(6,2) | 是 | DecimalField |
| PKg | old_pkg | PKg | decimal(6,2) | 是 | DecimalField |
| PPound | old_ppound | PPound | decimal(6,2) | 是 | DecimalField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeProdOutDetail`；原码 `SheetSeries, DetailNo` → 父表原码 `SheetSeries, DetailNo`；依据：原界面主从 ProdOutRecord → ProdOutDetail；原界面主从 ProdOutRecordUpdate → ProdOutDetailUpdate。

### SourceDyeProdStock — 坯布半成品成品与仓储相关表（ProdStock，待确认）

源表：`dye.ProdStock`；新表：`src_dye_prodstock`；原主键：无主键。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| StockDate | old_stock_date | StockDate | datetime | 否 | DateTimeField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 否 | CharField |
| FactID | old_fact_id | FactID | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | WareHouseID | varchar；字节长度 10 | 否 | CharField |
| SalerGroupID | old_saler_group_id | SalerGroupID | varchar；字节长度 10 | 是 | CharField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 20 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 10 | 是 | CharField |
| BusinessKind | old_business_kind | BusinessKind | smallint | 是 | IntegerField |
| PreMonthRolls | old_pre_month_rolls | PreMonthRolls | decimal(10,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| CarryDate | old_carry_date | CarryDate | datetime | 否 | DateTimeField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| PreMonthLengthQty | old_pre_month_length_qty | PreMonthLengthQty | decimal(10,2) | 是 | DecimalField |
| PreMonthWeightQty | old_pre_month_weight_qty | PreMonthWeightQty | decimal(10,2) | 是 | DecimalField |

### SourceDyeProdStockAdjust — 坯布半成品成品与仓储相关表（ProdStockAdjust，待确认）

源表：`dye.ProdStockAdjust`；新表：`src_dye_prodstockadjust`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 类型 | smallint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 10 | 是 | CharField |
| BusinessKind | old_business_kind | 业务类型 | smallint | 是 | IntegerField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核 | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyeProdStockAdjustDetail — 坯布半成品成品与仓储相关表（ProdStockAdjustDetail，待确认）

源表：`dye.ProdStockAdjustDetail`；新表：`src_dye_prodstockadjustdetail`；原主键：SheetSeries, DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细号 | varchar；字节长度 36 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 20 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| PaperRolls | old_paper_rolls | 账面粒数 | decimal(10,2) | 是 | DecimalField |
| RealRolls | old_real_rolls | 实际粒数 | smallint | 是 | IntegerField |
| AdjustRolls | old_adjust_rolls | 调整粒数 | decimal(7,2) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(8,2) | 是 | DecimalField |
| StockUnit | old_stock_unit | 单位 | tinyint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| PaperLength | old_paper_length | 账面长度 | decimal(10,5) | 是 | DecimalField |
| PaperWeight | old_paper_weight | 账面重量 | decimal(10,5) | 是 | DecimalField |
| RealWeightQty | old_real_weight_qty | 实际重量 | decimal(10,2) | 是 | DecimalField |
| RealLengthQty | old_real_length_qty | 实际长度 | decimal(10,2) | 是 | DecimalField |
| AdjustLengthQty | old_adjust_length_qty | 调整长度 | decimal(10,2) | 是 | DecimalField |
| AdjustWeightQty | old_adjust_weight_qty | 调整重量 | decimal(10,2) | 是 | DecimalField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeProdStockAdjust`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ProdStockAdjustDetail → ProdStockAdjust。

### SourceDyeProdStockAllot — 坯布半成品成品与仓储相关表（ProdStockAllot，待确认）

源表：`dye.ProdStockAllot`；新表：`src_dye_prodstockallot`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| FromSaleGroupID | old_from_sale_group_id | 来源业务组别 | varchar；字节长度 10 | 是 | CharField |
| ToSalerGroupID | old_to_saler_group_id | 目标业务组别 | varchar；字节长度 10 | 是 | CharField |
| FromWareHouseID | old_from_ware_house_id | 来源仓库 | varchar；字节长度 10 | 是 | CharField |
| ToReceSheetNo | old_to_rece_sheet_no | 目标明细单号 | varchar；字节长度 20 | 是 | CharField |
| FromCustomerID | old_from_customer_id | 来源客户 | varchar；字节长度 10 | 是 | CharField |
| ToCustomerID | old_to_customer_id | 目标客户 | varchar；字节长度 10 | 是 | CharField |
| FromJobDetailNo | old_from_job_detail_no | 来源加工作业单号 | varchar；字节长度 20 | 是 | CharField |
| ToJobDetailNo | old_to_job_detail_no | 目标加工作业编号 | varchar；字节长度 20 | 是 | CharField |
| FromCheckNo | old_from_check_no | 来源订单号 | varchar；字节长度 20 | 是 | CharField |
| ToCheckNo | old_to_check_no | 目标订单号 | varchar；字节长度 20 | 是 | CharField |
| FromReceSheetNo | old_from_rece_sheet_no | 来源收纱单号 | varchar；字节长度 20 | 是 | CharField |
| ToWareHouseID | old_to_ware_house_id | 目标仓库 | varchar；字节长度 10 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 20 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| FromBusinessUnitID | old_from_business_unit_id | 源经营单位 | varchar；字节长度 10 | 是 | CharField |
| ToBusinessUnitID | old_to_business_unit_id | 目标经营单位 | varchar；字节长度 10 | 是 | CharField |
| FromFabricID | old_from_fabric_id | 来源产品编码 | varchar；字节长度 10 | 是 | CharField |
| ToFabricID | old_to_fabric_id | 目标产品编码 | varchar；字节长度 10 | 是 | CharField |
| FromLotNo | old_from_lot_no | 来源批号 | varchar；字节长度 50 | 是 | CharField |
| ToLotNo | old_to_lot_no | 目标批号 | varchar；字节长度 50 | 是 | CharField |
| FromPrice | old_from_price | 来源价格 | decimal(8,2) | 是 | DecimalField |
| ToPrice | old_to_price | 目标价格 | decimal(8,2) | 是 | DecimalField |
| FromSalerID | old_from_saler_id | 来源业务员 | varchar；字节长度 10 | 是 | CharField |
| ToSalerID | old_to_saler_id | 目标业务员 | varchar；字节长度 10 | 是 | CharField |
| FromSpec | old_from_spec | 来源规格 | varchar；字节长度 50 | 是 | CharField |
| ToSpec | old_to_spec | 目标规格 | varchar；字节长度 50 | 是 | CharField |
| FromStructure | old_from_structure | 来源组织 | varchar；字节长度 50 | 是 | CharField |
| ToStructure | old_to_structure | 目标组织 | varchar；字节长度 50 | 是 | CharField |
| StockUnit | old_stock_unit | 库存单位 | tinyint | 是 | IntegerField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| BusinessKind | old_business_kind | BusinessKind | smallint | 是 | IntegerField |
| LengthQty | old_length_qty | LengthQty | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | WeightQty | decimal(10,2) | 是 | DecimalField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyeProdStockBook — 成品库存流水

源表：`dye.ProdStockBook`；新表：`src_dye_prodstockbook`；原主键：BookNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| BookNo | old_book_no | BookNo | bigint | 否 | BigIntegerField |
| BookKind | old_book_kind | BookKind | tinyint | 是 | IntegerField |
| BookDate | old_book_date | BookDate | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| FactID | old_fact_id | FactID | varchar；字节长度 250 | 是 | CharField |
| WareHouseID | old_ware_house_id | WareHouseID | varchar；字节长度 10 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | StorageUnitIDs | varchar；字节长度 100 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 250 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 50 | 是 | CharField |
| SalerGroupID | old_saler_group_id | SalerGroupID | varchar；字节长度 10 | 是 | CharField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 是 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 是 | CharField |
| InRolls | old_in_rolls | InRolls | decimal(7,2) | 是 | DecimalField |
| OutRolls | old_out_rolls | OutRolls | decimal(7,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| BusinessKind | old_business_kind | BusinessKind | smallint | 是 | IntegerField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 10 | 是 | CharField |
| InLengthQty | old_in_length_qty | InLengthQty | decimal(10,2) | 是 | DecimalField |
| InWeightQty | old_in_weight_qty | InWeightQty | decimal(10,2) | 是 | DecimalField |
| InGrayQty | old_in_gray_qty | InGrayQty | decimal(10,2) | 是 | DecimalField |
| OutLengthQty | old_out_length_qty | OutLengthQty | decimal(10,2) | 是 | DecimalField |
| OutWeightQty | old_out_weight_qty | OutWeightQty | decimal(10,2) | 是 | DecimalField |
| OutGrayQty | old_out_gray_qty | OutGrayQty | decimal(10,2) | 是 | DecimalField |
| StockFlag | old_stock_flag | StockFlag | varchar；字节长度 1 | 是 | CharField |
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 是 | CharField |
| InMoney | old_in_money | InMoney | decimal(10,2) | 是 | DecimalField |
| OutMoney | old_out_money | OutMoney | decimal(10,2) | 是 | DecimalField |
| InNetKg | old_in_net_kg | InNetKg | decimal(10,2) | 是 | DecimalField |
| OutNetKg | old_out_net_kg | OutNetKg | decimal(10,2) | 是 | DecimalField |
| CurrDate | old_curr_date | CurrDate | datetime | 是 | DateTimeField |

### SourceDyeProdStockCheck — 质量检验与异常相关表（ProdStockCheck，待确认）

源表：`dye.ProdStockCheck`；新表：`src_dye_prodstockcheck`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | 经营单位代码 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库代码 | varchar；字节长度 10 | 是 | CharField |
| ProdKindID | old_prod_kind_id | 成品类别编码 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| BusinessKind | old_business_kind | BusinessKind | smallint | 是 | IntegerField |

### SourceDyeProdStockCheckDetail — 质量检验与异常相关表（ProdStockCheckDetail，待确认）

源表：`dye.ProdStockCheckDetail`；新表：`src_dye_prodstockcheckdetail`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 是 | CharField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 50 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 20 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 20 | 是 | CharField |
| PaperRolls | old_paper_rolls | PaperRolls | decimal(10,2) | 是 | DecimalField |
| PaperQty | old_paper_qty | PaperQty | decimal(10,2) | 是 | DecimalField |
| RealQty | old_real_qty | RealQty | decimal(10,2) | 是 | DecimalField |
| RealRolls | old_real_rolls | RealRolls | smallint | 是 | IntegerField |
| AdjustQty | old_adjust_qty | AdjustQty | decimal(10,2) | 是 | DecimalField |
| AdjustRolls | old_adjust_rolls | AdjustRolls | decimal(7,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| StockUnit | old_stock_unit | StockUnit | tinyint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |

### SourceDyeProdStorageAdjust — 坯布半成品成品与仓储相关表（ProdStorageAdjust，待确认）

源表：`dye.ProdStorageAdjust`；新表：`src_dye_prodstorageadjust`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单据号 | varchar；字节长度 20 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| SalerID | old_saler_id | 业务员 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | 调出仓库 | varchar；字节长度 10 | 是 | CharField |
| ToWareHouseID | old_to_ware_house_id | 调入仓库 | varchar；字节长度 10 | 是 | CharField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| CarryerID | old_carryer_id | 搬运工 | varchar；字节长度 20 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |

### SourceDyeProdStorageAdjustDetail — 坯布半成品成品与仓储相关表（ProdStorageAdjustDetail，待确认）

源表：`dye.ProdStorageAdjustDetail`；新表：`src_dye_prodstorageadjustdetail`；原主键：SheetSeries, DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细号 | varchar；字节长度 36 | 否 | CharField |
| FromInSheetNo | old_from_in_sheet_no | (调出)入库单号 | varchar；字节长度 50 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 20 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 200 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 200 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | 调出库位 | varchar；字节长度 100 | 是 | CharField |
| ToStorageUnitIDs | old_to_storage_unit_ids | 调入库位 | varchar；字节长度 100 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| StockUnit | old_stock_unit | 单位 | tinyint | 是 | IntegerField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 250 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 150 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 100 | 是 | CharField |
| OrderSheetDate | old_order_sheet_date | 订单日期 | datetime | 是 | DateTimeField |
| Weight | old_weight | 克重 | varchar；字节长度 50 | 是 | CharField |
| Width | old_width | 幅宽 | varchar；字节长度 50 | 是 | CharField |
| Structure | old_structure | 织厂 | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeProdStorageAdjust`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 ProdStorageAdjustDetail → ProdStorageAdjust。

### SourceDyeProdStorageAdjustRecord — 坯布半成品成品与仓储相关表（ProdStorageAdjustRecord，待确认）

源表：`dye.ProdStorageAdjustRecord`；新表：`src_dye_prodstorageadjustrecord`；原主键：SheetSeries, DetailNo, BarCode。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细号 | varchar；字节长度 36 | 否 | CharField |
| RollNo | old_roll_no | 箱号 | varchar；字节长度 20 | 否 | CharField |
| FromInSheetNo | old_from_in_sheet_no | (调出)入库单号 | varchar；字节长度 50 | 是 | CharField |
| BarCode | old_bar_code | 条码 | varchar；字节长度 50 | 否 | CharField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 调出库位 | varchar；字节长度 10 | 是 | CharField |
| ToStorageUnitID | old_to_storage_unit_id | 调入库位 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| GrayBarCode | old_gray_bar_code | GrayBarCode | varchar；字节长度 50 | 是 | CharField |
| GrayQty | old_gray_qty | GrayQty | decimal(8,2) | 是 | DecimalField |
| GUnit | old_gunit | GUnit | tinyint | 是 | IntegerField |
| PUnit | old_punit | PUnit | tinyint | 是 | IntegerField |
| Yard | old_yard | Yard | decimal(8,2) | 是 | DecimalField |
| RollNo3 | old_roll_no3 | RollNo3 | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeProdStorageAdjustDetail`；原码 `SheetSeries, DetailNo` → 父表原码 `SheetSeries, DetailNo`；依据：原界面主从 ProdStorageAdjustRecord → ProdStorageAdjustDetail。

### SourceDyeRecordYield — 产量/卷记录

源表：`dye.RecordYield`；新表：`src_dye_recordyield`；原主键：JobSheetNo, CheckNo, RollNo, Guid。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| Guid | old_guid | 唯一标识符 | varchar；字节长度 38 | 否 | CharField |
| BarCode | old_bar_code | 条码 | varchar；字节长度 100 | 是 | CharField |
| MachineID | old_machine_id | 机台 | varchar；字节长度 20 | 是 | CharField |
| RollNo | old_roll_no | 箱号 | varchar；字节长度 50 | 否 | CharField |
| Unit | old_unit | 单位 | varchar；字节长度 20 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,1) | 是 | DecimalField |
| Kg | old_kg | 重量 | decimal(10,2) | 是 | DecimalField |
| Meter | old_meter | 长度 | decimal(10,0) | 是 | DecimalField |
| Pound | old_pound | 镑数 | decimal(10,2) | 是 | DecimalField |
| Yard | old_yard | 码数 | decimal(10,2) | 是 | DecimalField |
| RealQty | old_real_qty | 缴库长度 | decimal(10,2) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 仓位代码 | varchar；字节长度 10 | 是 | CharField |
| DefectCount | old_defect_count | 疵点数 | smallint | 是 | IntegerField |
| Dots | old_dots | 扣分 | smallint | 是 | IntegerField |
| Status | old_status | 状态 | tinyint | 是 | IntegerField |
| GradeID | old_grade_id | 色号等级 | varchar；字节长度 10 | 是 | CharField |
| PackTime | old_pack_time | 包装时间 | datetime | 是 | DateTimeField |
| EmpID | old_emp_id | 员工编号 | varchar；字节长度 50 | 是 | CharField |
| TubeWeight | old_tube_weight | 筒管重 | decimal(7,3) | 是 | DecimalField |
| Tubes | old_tubes | 筒管数 | smallint | 是 | IntegerField |
| Thick | old_thick | 厚度 | decimal(6,2) | 是 | DecimalField |
| Width | old_width | 幅宽 | varchar；字节长度 50 | 是 | CharField |
| PackID | old_pack_id | 纱种编号 | varchar；字节长度 10 | 是 | CharField |
| Bowing | old_bowing | 纬斜 | decimal(5,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 150 | 否 | CharField |
| AddQty | old_add_qty | 补码 | decimal(10,2) | 是 | DecimalField |
| SampleQty | old_sample_qty | 样纱长度 | decimal(10,2) | 是 | DecimalField |
| CutQty | old_cut_qty | 开剪值 | decimal(10,2) | 是 | DecimalField |
| CutTimes | old_cut_times | 开剪次数 | smallint | 是 | IntegerField |
| FullWidth | old_full_width | 全幅 | decimal(6,2) | 是 | DecimalField |
| T1 | old_t1 | 厚度一 | decimal(6,2) | 是 | DecimalField |
| T2 | old_t2 | 厚度二 | decimal(6,2) | 是 | DecimalField |
| T3 | old_t3 | 厚度三 | decimal(6,2) | 是 | DecimalField |
| T4 | old_t4 | 厚度四 | decimal(6,2) | 是 | DecimalField |
| T5 | old_t5 | 厚度五 | decimal(6,2) | 是 | DecimalField |
| Q1 | old_q1 | 客纱种编码 | varchar；字节长度 50 | 是 | CharField |
| Q2 | old_q2 | 开卡粒数 | varchar；字节长度 10 | 是 | CharField |
| Q3 | old_q3 | 品质3级数 | varchar；字节长度 10 | 是 | CharField |
| Q4 | old_q4 | 品质4级数 | varchar；字节长度 10 | 是 | CharField |
| Q5 | old_q5 | 品质5级数 | varchar；字节长度 10 | 是 | CharField |
| Q6 | old_q6 | 品质6级数 | varchar；字节长度 10 | 是 | CharField |
| Q7 | old_q7 | 品质7级数 | varchar；字节长度 10 | 是 | CharField |
| Q8 | old_q8 | 品质8级数 | varchar；字节长度 10 | 是 | CharField |
| Q9 | old_q9 | 品质9级数 | varchar；字节长度 10 | 是 | CharField |
| Q10 | old_q10 | 品质10级数 | varchar；字节长度 10 | 是 | CharField |
| Q11 | old_q11 | 品质11级数 | varchar；字节长度 10 | 是 | CharField |
| Q12 | old_q12 | 品质12级数 | varchar；字节长度 100 | 是 | CharField |
| Q13 | old_q13 | 品质13级数 | varchar；字节长度 100 | 是 | CharField |
| Q14 | old_q14 | 品质14级数 | varchar；字节长度 100 | 是 | CharField |
| Q15 | old_q15 | 新利二维码 | varchar；字节长度 500 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 200 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 100 | 是 | CharField |
| InSheetNo | old_in_sheet_no | 入库单号 | varchar；字节长度 20 | 是 | CharField |
| CustQty | old_cust_qty | 客户数量 | decimal(10,1) | 是 | DecimalField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| LabelID | old_label_id | 标签号 | varchar；字节长度 10 | 是 | CharField |
| Weight | old_weight | 克重 | varchar；字节长度 50 | 是 | CharField |
| ColorDiff | old_color_diff | 色差 | int | 是 | IntegerField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| GradeReasonID | old_grade_reason_id | 降等 | varchar；字节长度 100 | 是 | CharField |
| StandardWidth | old_standard_width | 标准幅宽 | decimal(6,2) | 是 | DecimalField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 150 | 是 | CharField |
| OriDetailCustomer | old_ori_detail_customer | 原始客户 | varchar；字节长度 50 | 是 | CharField |
| OrderSheetNo | old_order_sheet_no | 发货订单 | varchar；字节长度 20 | 是 | CharField |
| OriOderSheetNo | old_ori_oder_sheet_no | 原始订单 | varchar；字节长度 20 | 是 | CharField |
| QCResultID | old_qcresult_id | QCResultID | varchar；字节长度 10 | 是 | CharField |
| MainNo | old_main_no | 主单号 | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 36 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 150 | 是 | CharField |
| DefectEmpID | old_defect_emp_id | DefectEmpID | varchar；字节长度 20 | 是 | CharField |
| GrayBarCode | old_gray_bar_code | 宝誉/丽业二维码组合 | varchar；字节长度 100 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 50 | 否 | CharField |
| InScanTime | old_in_scan_time | InScanTime | datetime | 是 | DateTimeField |
| InScaner | old_in_scaner | InScaner | varchar；字节长度 10 | 是 | CharField |
| OutScanTime | old_out_scan_time | OutScanTime | datetime | 是 | DateTimeField |
| OutScaner | old_out_scaner | OutScaner | varchar；字节长度 10 | 是 | CharField |
| OutPlanSheetNo | old_out_plan_sheet_no | OutPlanSheetNo | varchar；字节长度 20 | 是 | CharField |
| OutPlanDetailNo | old_out_plan_detail_no | OutPlanDetailNo | varchar；字节长度 20 | 是 | CharField |
| DlvSheetNo | old_dlv_sheet_no | DlvSheetNo | varchar；字节长度 20 | 是 | CharField |
| NetKg | old_net_kg | 净重 | decimal(10,1) | 是 | DecimalField |
| SumAssignedWeightQty | old_sum_assigned_weight_qty | 实发数量 | decimal(10,2) | 是 | DecimalField |
| SumAssignedRolls | old_sum_assigned_rolls | 实发粒数 | decimal(7,2) | 是 | DecimalField |
| Scroll | old_scroll | Scroll | nvarchar；字节长度 200 | 是 | CharField |
| PackBag | old_pack_bag | 包装重 | decimal(7,3) | 是 | DecimalField |
| AddWeight | old_add_weight | AddWeight | nvarchar；字节长度 100 | 是 | CharField |
| CustomerGrayName | old_customer_gray_name | CustomerGrayName | nvarchar；字节长度 400 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 150 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 500 | 是 | CharField |
| WidthSpec | old_width_spec | 幅宽（测量） | nvarchar；字节长度 256 | 是 | CharField |
| WeightSpec | old_weight_spec | 克重（测量） | varchar；字节长度 150 | 是 | CharField |
| Qty | old_qty | 张力 | decimal(12,6) | 是 | DecimalField |
| CountUnit | old_count_unit | CountUnit | nvarchar；字节长度 32 | 是 | CharField |
| JobDetailNo | old_job_detail_no | JobDetailNo | varchar；字节长度 150 | 是 | CharField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| CustSelfNo | old_cust_self_no | 制单号 | varchar；字节长度 500 | 是 | CharField |
| RedoLengthQty | old_redo_length_qty | RedoLengthQty | decimal(10,2) | 是 | DecimalField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 10 | 是 | CharField |
| Addkg | old_addkg | 加空重 | float | 是 | FloatField |
| ShiftID | old_shift_id | 班组 | varchar；字节长度 10 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| Kind | old_kind | Kind | varchar；字节长度 1 | 是 | CharField |
| SpecDefects | old_spec_defects | 特判 | varchar；字节长度 100 | 是 | CharField |
| GrayWeight | old_gray_weight | GrayWeight | decimal(6,2) | 是 | DecimalField |
| CombineSheetNos | old_combine_sheet_nos | CombineSheetNos | varchar；字节长度 200 | 是 | CharField |
| ContractNo | old_contract_no | 客户单号 | varchar；字节长度 500 | 是 | CharField |
| LotCheckNo | old_lot_check_no | LotCheckNo | varchar；字节长度 500 | 是 | CharField |
| DefectProcessID | old_defect_process_id | DefectProcessID | varchar；字节长度 50 | 是 | CharField |
| RollNoType | old_roll_no_type | RollNoType | varchar；字节长度 150 | 是 | CharField |
| StyleNo | old_style_no | StyleNo | varchar；字节长度 150 | 是 | CharField |
| RedoWeightQty | old_redo_weight_qty | RedoWeightQty | decimal(10,2) | 是 | DecimalField |
| LotDetailNo | old_lot_detail_no | LotDetailNo | varchar；字节长度 50 | 是 | CharField |
| SortNo | old_sort_no | SortNo | varchar；字节长度 10 | 是 | CharField |
| SkeWing1 | old_ske_wing1 | 宝誉条码 | varchar；字节长度 150 | 是 | CharField |
| SkeWing2 | old_ske_wing2 | SkeWing2 | varchar；字节长度 150 | 是 | CharField |
| RePeatcnt | old_re_peatcnt | RePeatcnt | varchar；字节长度 150 | 是 | CharField |
| RepeatFrontL | old_repeat_front_l | RepeatFrontL | decimal(10,2) | 是 | DecimalField |
| RepeatFrontM | old_repeat_front_m | RepeatFrontM | decimal(10,2) | 是 | DecimalField |
| RepeatFrontR | old_repeat_front_r | RepeatFrontR | decimal(10,2) | 是 | DecimalField |
| RepeatMiddleL | old_repeat_middle_l | RepeatMiddleL | decimal(10,2) | 是 | DecimalField |
| RepeatMiddleM | old_repeat_middle_m | RepeatMiddleM | decimal(10,2) | 是 | DecimalField |
| RepeatMiddleR | old_repeat_middle_r | RepeatMiddleR | decimal(10,2) | 是 | DecimalField |
| RepeatEndL | old_repeat_end_l | RepeatEndL | decimal(10,2) | 是 | DecimalField |
| RepeatEndM | old_repeat_end_m | RepeatEndM | decimal(10,2) | 是 | DecimalField |
| RepeatEndR | old_repeat_end_r | RepeatEndR | decimal(10,2) | 是 | DecimalField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| YardAvgdots | old_yard_avgdots | 百码扣分 | float | 是 | FloatField |
| OrderWeight | old_order_weight | 要求克重 | varchar；字节长度 20 | 是 | CharField |
| PAWeight | old_paweight | 克重（公式计算） | decimal(18,0) | 是 | DecimalField |
| PAYard | old_payard | 码数(公式计算) | decimal(18,0) | 是 | DecimalField |
| PAMeter | old_pameter | 米数(公式计算） | decimal(18,0) | 是 | DecimalField |
| WidthUnit | old_width_unit | 纱封单位 | nvarchar；字节长度 40 | 是 | CharField |
| OrderWidth | old_order_width | 要求幅宽 | varchar；字节长度 20 | 是 | CharField |
| CustColorNum | old_cust_color_num | CustColorNum | varchar；字节长度 100 | 是 | CharField |
| DB2Code | old_db2_code | DB2Code | varchar；字节长度 500 | 是 | CharField |
| AddWeigth | old_add_weigth | 成品加重 | varchar；字节长度 50 | 是 | CharField |
| LabelWeight | old_label_weight | LabelWeight | varchar；字节长度 100 | 是 | CharField |
| LabelLength | old_label_length | LabelLength | varchar；字节长度 100 | 是 | CharField |
| LabelRemarks | old_label_remarks | 标签备注 | varchar；字节长度 500 | 是 | CharField |
| FabricLoss | old_fabric_loss | 胚纱损耗 | decimal(18,2) | 是 | DecimalField |
| ShipMentType | old_ship_ment_type | 出货方式 | varchar；字节长度 50 | 是 | CharField |
| WeightQty | old_weight_qty | WeightQty | decimal(10,2) | 是 | DecimalField |
| ProdCode | old_prod_code | 成品编号 | varchar；字节长度 50 | 是 | CharField |
| Model1 | old_model1 | 款号 | varchar；字节长度 200 | 是 | CharField |
| ColorRemarks | old_color_remarks | 用途 | varchar；字节长度 500 | 是 | CharField |
| ColorE | old_color_e | ColorE | varchar；字节长度 20 | 是 | CharField |
| WeightUnit | old_weight_unit | WeightUnit | nvarchar；字节长度 40 | 是 | CharField |
| WeightKindID | old_weight_kind_id | WeightKindID | nvarchar；字节长度 40 | 是 | CharField |
| WidthKindID | old_width_kind_id | WidthKindID | nvarchar；字节长度 40 | 是 | CharField |
| ProdName | old_prod_name | 成品品名 | varchar；字节长度 500 | 是 | CharField |
| FabricNO2 | old_fabric_no2 | 计划单号 | varchar；字节长度 200 | 是 | CharField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| ProdUnit | old_prod_unit | 成品单位 | tinyint | 是 | IntegerField |
| LabelWareHouse | old_label_ware_house | 标签仓库 | varchar；字节长度 100 | 是 | CharField |
| WindingID | old_winding_id | 络筒员工 | varchar；字节长度 30 | 是 | CharField |
| LTSheetNo | old_ltsheet_no | LTSheetNo | varchar；字节长度 30 | 是 | CharField |
| FenTou | old_fen_tou | 分头 | decimal(6,2) | 是 | DecimalField |
| SheetDate | old_sheet_date | 络筒日期 | datetime | 是 | DateTimeField |
| PreField1 | old_pre_field1 | 捻度 | varchar；字节长度 50 | 是 | CharField |
| Long_CM | old_long_cm | 长(CM) | decimal(6,1) | 是 | DecimalField |
| Wide_CM | old_wide_cm | 宽(CM) | decimal(6,1) | 是 | DecimalField |
| High_CM | old_high_cm | 高(CM) | decimal(6,1) | 是 | DecimalField |
| Whether | old_whether | 是否 | bit | 是 | BooleanField |
| FixedQty | old_fixed_qty | 锭重 | decimal(5,2) | 是 | DecimalField |
| FabricKindID | old_fabric_kind_id | 胚纱类别 | varchar；字节长度 30 | 是 | CharField |

关联 `source_parent_1` → `erp_production.SourceDyeJobSheet`；原码 `JobSheetNo` → 父表原码 `SheetNo`；依据：原界面主从 JobRecordDetail → JobRecord。

### SourceDyeSemiAxisBook — 坯布半成品成品与仓储相关表（SemiAxisBook，待确认）

源表：`dye.SemiAxisBook`；新表：`src_dye_semiaxisbook`；原主键：AxisNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| AxisNo | old_axis_no | AxisNo | varchar；字节长度 20 | 否 | CharField |
| SequenceNo | old_sequence_no | SequenceNo | bigint | 是 | BigIntegerField |
| Flag | old_flag | Flag | tinyint | 是 | IntegerField |
| ReceSheetNo | old_rece_sheet_no | ReceSheetNo | varchar；字节长度 20 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 是 | CharField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| Vats | old_vats | Vats | decimal(7,1) | 是 | DecimalField |
| Rolls | old_rolls | Rolls | decimal(7,2) | 是 | DecimalField |
| Qty | old_qty | Qty | decimal(10,2) | 是 | DecimalField |
| StockUnit | old_stock_unit | StockUnit | tinyint | 是 | IntegerField |
| CurrTime | old_curr_time | CurrTime | datetime | 是 | DateTimeField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 10 | 是 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 10 | 是 | CharField |
| Status | old_status | Status | varchar；字节长度 1 | 是 | CharField |
| Place | old_place | Place | varchar；字节长度 100 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 是 | CharField |

### SourceDyeSemiAxisRemain — 坯布半成品成品与仓储相关表（SemiAxisRemain，待确认）

源表：`dye.SemiAxisRemain`；新表：`src_dye_semiaxisremain`；原主键：AxisNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| AxisNo | old_axis_no | AxisNo | varchar；字节长度 20 | 否 | CharField |
| SequenceNo | old_sequence_no | SequenceNo | bigint | 是 | BigIntegerField |
| ReceSheetNo | old_rece_sheet_no | ReceSheetNo | varchar；字节长度 20 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 是 | CharField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| Qty | old_qty | Qty | decimal(10,2) | 是 | DecimalField |
| StockUnit | old_stock_unit | StockUnit | tinyint | 是 | IntegerField |
| CurrTime | old_curr_time | CurrTime | datetime | 是 | DateTimeField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 10 | 是 | CharField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 10 | 是 | CharField |
| Place | old_place | Place | varchar；字节长度 100 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 100 | 是 | CharField |

### SourceDyeSemiIn — 半成品入库单

源表：`dye.SemiIn`；新表：`src_dye_semiin`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单据号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| SemiKindID | old_semi_kind_id | 半成品类别 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员 | varchar；字节长度 10 | 是 | CharField |
| StockUnit | old_stock_unit | 单位 | tinyint | 是 | IntegerField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库 | varchar；字节长度 50 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商 | varchar；字节长度 50 | 是 | CharField |
| GrayOutSheetNo | old_gray_out_sheet_no | 胚纱转仓出库单号 | varchar；字节长度 30 | 是 | CharField |
| A_A | old_a_a | 物料区域 | varchar；字节长度 50 | 是 | CharField |

### SourceDyeSemiInDetail — 半成品入库明细

源表：`dye.SemiInDetail`；新表：`src_dye_semiindetail`；原主键：ReceSheetNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 是 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 否 | CharField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 128 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 物料颜色 | varchar；字节长度 20 | 是 | CharField |
| InRolls | old_in_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| InQty | old_in_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 仓位 | varchar；字节长度 30 | 是 | CharField |
| OrderNo | old_order_no | 订单号 | varchar；字节长度 20 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| ShiftID | old_shift_id | 班组 | varchar；字节长度 10 | 是 | CharField |
| EmpID | old_emp_id | 员工 | varchar；字节长度 10 | 是 | CharField |
| MachineID | old_machine_id | 机台 | varchar；字节长度 20 | 是 | CharField |
| OriReceSheetNo | old_ori_rece_sheet_no | 原入库明细号 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| NewLotNo | old_new_lot_no | 新批号 | varchar；字节长度 200 | 是 | CharField |
| Width | old_width | Width | decimal(6,2) | 是 | DecimalField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| Area | old_area | 区域 | varchar；字节长度 30 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 200 | 是 | CharField |
| GrainQty | old_grain_qty | GrainQty | decimal(8,2) | 是 | DecimalField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(8,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度 | decimal(8,2) | 是 | DecimalField |
| Packs | old_packs | 件数 | decimal(7,2) | 是 | DecimalField |
| PCS | old_pcs | 粒/件 | int | 是 | IntegerField |
| FixedQty | old_fixed_qty | 锭重 | decimal(5,2) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(8,2) | 是 | DecimalField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |
| PreField2 | old_pre_field2 | PreField2 | varchar；字节长度 50 | 是 | CharField |
| PreField3 | old_pre_field3 | PreField3 | varchar；字节长度 50 | 是 | CharField |
| PreField4 | old_pre_field4 | PreField4 | varchar；字节长度 50 | 是 | CharField |
| PreField5 | old_pre_field5 | PreField5 | varchar；字节长度 200 | 是 | CharField |
| Amount | old_amount | 金额 | decimal(10,2) | 是 | DecimalField |
| PurDetailNo | old_pur_detail_no | 采购入库明细 | varchar；字节长度 50 | 是 | CharField |
| YarnCategory | old_yarn_category | 纱类别 | varchar；字节长度 30 | 是 | CharField |
| Classify | old_classify | 半成品分类 | varchar；字节长度 50 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| PurchaseOrders | old_purchase_orders | 采购单号 | varchar；字节长度 20 | 是 | CharField |
| A_A | old_a_a | 物料区域 | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | 物料等级 | varchar；字节长度 100 | 是 | CharField |
| TrunReceSheetNo | old_trun_rece_sheet_no | 转仓前入库明细单号 | varchar；字节长度 30 | 是 | CharField |
| InSheetKind | old_in_sheet_kind | 物料分类 | varchar；字节长度 20 | 是 | CharField |
| GrayOutDetailNo | old_gray_out_detail_no | 发外出库明细单号 | varchar；字节长度 30 | 是 | CharField |
| InputCode | old_input_code | 打包条码 | varchar；字节长度 30 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeSemiIn`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 PurSemiInDetail → PurSemiIn；原界面主从 CusReturnSemiInDetail → CusReturnSemiIn；原界面主从 TurnSemiInDetail → TurnSemiIn；原界面主从 MaterialSemiInDetail → MaterialSemiIn；原界面主从 SemiInDetail → SemiIn；原界面主从 SemiInDetailBack → SemiInBack；原界面主从 GrayOutToSemiInDetail → GrayOutToSemiIn。

### SourceDyeSemiInRecord — 坯布半成品成品与仓储相关表（SemiInRecord，待确认）

源表：`dye.SemiInRecord`；新表：`src_dye_semiinrecord`；原主键：ReceSheetNo, RollNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 否 | CharField |
| RollNo | old_roll_no | 箱号 | varchar；字节长度 20 | 否 | CharField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| DlvQty | old_dlv_qty | 交货数量 | decimal(10,2) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 仓位 | varchar；字节长度 10 | 是 | CharField |
| Defects | old_defects | 疵点 | varchar；字节长度 100 | 是 | CharField |
| Status | old_status | 状态 | varchar；字节长度 1 | 是 | CharField |
| BarCode | old_bar_code | 条码 | varchar；字节长度 50 | 是 | CharField |
| AssignedNo | old_assigned_no | 投胚流水号 | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| OriReceSheetNo | old_ori_rece_sheet_no | OriReceSheetNo | varchar；字节长度 20 | 是 | CharField |
| RollNo2 | old_roll_no2 | RollNo2 | varchar；字节长度 20 | 是 | CharField |
| GUnit | old_gunit | GUnit | tinyint | 是 | IntegerField |
| OriBarCode | old_ori_bar_code | OriBarCode | varchar；字节长度 50 | 是 | CharField |
| Remark | old_remark | 备注 | varchar；字节长度 300 | 是 | CharField |
| GraySpec | old_gray_spec | GraySpec | varchar；字节长度 50 | 是 | CharField |
| Num | old_num | Num | decimal(8,0) | 是 | DecimalField |
| CBz | old_cbz | CBz | varchar；字节长度 10 | 是 | CharField |
| Rolls | old_rolls | 粒数 | float | 是 | FloatField |
| Packs | old_packs | 件数 | decimal(4,1) | 是 | DecimalField |
| InputDetailCode | old_input_detail_code | 标签打印细码 | varchar；字节长度 100 | 是 | CharField |
| Kg | old_kg | 磅重 | decimal(10,2) | 是 | DecimalField |
| CustQty | old_cust_qty | 毛重 | decimal(10,1) | 是 | DecimalField |
| TubeWeight | old_tube_weight | 纸筒重 | decimal(6,2) | 是 | DecimalField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeSemiInDetail`；原码 `ReceSheetNo` → 父表原码 `ReceSheetNo`；依据：原界面主从 TurnSemiInRecord → TurnSemiInDetail；原界面主从 PurSemiInRecord → PurSemiInDetail；原界面主从 MaterialSemiInRecord → MaterialSemiInDetail；原界面主从 GrayOutToSemiInRecord → GrayOutToSemiInDetail；原界面主从 SemiInRecord → SemiInDetail；原界面主从 CusReturnSemiInRecord → CusReturnSemiInDetail；原界面主从 SemiInRecordBack → SemiInDetailBack。

### SourceDyeSemiOut — 半成品出库单

源表：`dye.SemiOut`；新表：`src_dye_semiout`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 出库日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| SemiKindID | old_semi_kind_id | 半成品类别 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户名称 | varchar；字节长度 10 | 是 | CharField |
| StockUnit | old_stock_unit | 库存单位 | tinyint | 是 | IntegerField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库 | varchar；字节长度 50 | 是 | CharField |

### SourceDyeSemiOutDetail — 半成品出库明细

源表：`dye.SemiOutDetail`；新表：`src_dye_semioutdetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 是 | CharField |
| AssignedNo | old_assigned_no | 投胚流水号 | varchar；字节长度 20 | 是 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 是 | CharField |
| FabricID | old_fabric_id | 客户规格 | varchar；字节长度 128 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 物料颜色 | varchar；字节长度 20 | 是 | CharField |
| StorageUnitID | old_storage_unit_id | 库位 | varchar；字节长度 10 | 是 | CharField |
| OutRolls | old_out_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| OutQty | old_out_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| OrderNo | old_order_no | 订单号 | varchar；字节长度 20 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| ShiftID | old_shift_id | 班组 | varchar；字节长度 10 | 是 | CharField |
| EmpID | old_emp_id | 员工 | varchar；字节长度 10 | 是 | CharField |
| MachineID | old_machine_id | 机台 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| Price | old_price | 单价 | decimal(8,2) | 是 | DecimalField |
| GrainQty | old_grain_qty | GrainQty | decimal(8,2) | 是 | DecimalField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(8,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度 | decimal(8,2) | 是 | DecimalField |
| Packs | old_packs | 件数 | decimal(7,2) | 是 | DecimalField |
| PCS | old_pcs | 件/粒 | int | 是 | IntegerField |
| FixedQty | old_fixed_qty | 锭重 | decimal(5,2) | 是 | DecimalField |
| Amount | old_amount | 金额 | decimal(10,2) | 是 | DecimalField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 200 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |
| PreField2 | old_pre_field2 | PreField2 | varchar；字节长度 50 | 是 | CharField |
| PreField3 | old_pre_field3 | PreField3 | varchar；字节长度 50 | 是 | CharField |
| PreField4 | old_pre_field4 | PreField4 | varchar；字节长度 50 | 是 | CharField |
| PreField5 | old_pre_field5 | PreField5 | varchar；字节长度 200 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库 | varchar；字节长度 50 | 是 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |
| SupplierID | old_supplier_id | 供应商 | varchar；字节长度 30 | 是 | CharField |
| PurchaseOrders | old_purchase_orders | 采购单号 | varchar；字节长度 20 | 是 | CharField |
| InSheetKind | old_in_sheet_kind | 物料分类 | varchar；字节长度 20 | 是 | CharField |
| A_A | old_a_a | 物料区域 | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | 物料等级 | varchar；字节长度 100 | 是 | CharField |
| InputCode | old_input_code | 打包条码 | varchar；字节长度 40 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeSemiOut`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 SemiOutDetail → SemiOut；原界面主从 SemiOutDetailTurn → SemiOutTurn；原界面主从 SemiOutSaleDetail → SemiOutSale；原界面主从 SemiOutWorkDetail → SemiOutWork；原界面主从 SemiOutDetailJob → SemiOutJob。

### SourceDyeSemiOutRecord — 坯布半成品成品与仓储相关表（SemiOutRecord，待确认）

源表：`dye.SemiOutRecord`；新表：`src_dye_semioutrecord`；原主键：AssignedNo, RollNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 工卡流水 | varchar；字节长度 20 | 是 | CharField |
| AssignedNo | old_assigned_no | 投胚流水号 | varchar；字节长度 20 | 否 | CharField |
| RollNo | old_roll_no | 箱号 | varchar；字节长度 20 | 否 | CharField |
| BarCode | old_bar_code | 胚纱条码 | varchar；字节长度 50 | 是 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 是 | CharField |
| LengthQty | old_length_qty | 长度数量 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量数量 | decimal(10,2) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 仓位代码 | varchar；字节长度 10 | 是 | CharField |
| Status | old_status | 状态 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| GUnit | old_gunit | GUnit | tinyint | 是 | IntegerField |
| Rolls | old_rolls | 粒数 | decimal(4,1) | 是 | DecimalField |
| Packs | old_packs | 件数 | decimal(4,1) | 是 | DecimalField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeSemiOutDetail`；原码 `AssignedNo` → 父表原码 `AssignedNo`；依据：原界面主从 SemiOutRecordTurn → SemiOutDetailTurn；原界面主从 SemiOutRecordJob → SemiOutDetailJob；原界面主从 SemiOutRecord → SemiOutDetail；原界面主从 SemiOutSaleRecord → SemiOutSaleDetail；原界面主从 SemiOutWorkRecord → SemiOutWorkDetail。

### SourceDyeSemiPostionUp — 坯布半成品成品与仓储相关表（SemiPostionUp，待确认）

源表：`dye.SemiPostionUp`；新表：`src_dye_semipostionup`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 36 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| InSheetKind | old_in_sheet_kind | 物料分类 | varchar；字节长度 20 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 200 | 是 | CharField |
| ColorID | old_color_id | 物料颜色 | varchar；字节长度 50 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |
| FixedQty | old_fixed_qty | 锭重 | decimal(5,2) | 是 | DecimalField |
| PurchaseOrders | old_purchase_orders | 采购单号 | varchar；字节长度 20 | 是 | CharField |
| A_A | old_a_a | 物料区域 | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | 物料等级 | varchar；字节长度 100 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量数量 | decimal(8,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度数量 | decimal(8,2) | 是 | DecimalField |
| Packs | old_packs | 件数 | decimal(7,2) | 是 | DecimalField |
| PCS | old_pcs | 粒/件 | int | 是 | IntegerField |
| Area | old_area | 原区域 | varchar；字节长度 100 | 是 | CharField |
| NewArea | old_new_area | 新区域 | varchar；字节长度 100 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| InDetailNo | old_in_detail_no | InDetailNo | varchar；字节长度 50 | 是 | CharField |

### SourceDyeSemiStock — 坯布半成品成品与仓储相关表（SemiStock，待确认）

源表：`dye.SemiStock`；新表：`src_dye_semistock`；原主键：StockDate, CustomerID, WareHouseID, SupplierID, ProdID, SalerID, ColorID, Spec, LotNo, ReceSheetNo, PreField1, PurchaseOrders, A_A, A_B, FixedQty。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| StockDate | old_stock_date | StockDate | datetime | 否 | DateTimeField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 否 | CharField |
| WareHouseID | old_ware_house_id | WareHouseID | varchar；字节长度 10 | 否 | CharField |
| GrayKindID | old_gray_kind_id | GrayKindID | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | SalerGroupID | varchar；字节长度 10 | 是 | CharField |
| SupplierID | old_supplier_id | SupplierID | varchar；字节长度 10 | 否 | CharField |
| BusinessKind | old_business_kind | BusinessKind | smallint | 是 | IntegerField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 50 | 否 | CharField |
| StockKind | old_stock_kind | StockKind | tinyint | 是 | IntegerField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 10 | 否 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 否 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 否 | CharField |
| PreMonthPacks | old_pre_month_packs | PreMonthPacks | decimal(10,2) | 是 | DecimalField |
| PreMonthRolls | old_pre_month_rolls | PreMonthRolls | decimal(10,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| CarryDate | old_carry_date | CarryDate | datetime | 是 | DateTimeField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| PreMonthWeightQty | old_pre_month_weight_qty | PreMonthWeightQty | decimal(10,2) | 是 | DecimalField |
| PreMonthLengthQty | old_pre_month_length_qty | PreMonthLengthQty | decimal(10,2) | 是 | DecimalField |
| StorageUnitIDs | old_storage_unit_ids | StorageUnitIDs | varchar；字节长度 100 | 是 | CharField |
| ReceSheetNo | old_rece_sheet_no | ReceSheetNo | varchar；字节长度 20 | 否 | CharField |
| PreField1 | old_pre_field1 | PreField1 | varchar；字节长度 50 | 否 | CharField |
| PurchaseOrders | old_purchase_orders | PurchaseOrders | varchar；字节长度 20 | 否 | CharField |
| A_A | old_a_a | A_A | varchar；字节长度 50 | 否 | CharField |
| A_B | old_a_b | A_B | varchar；字节长度 100 | 否 | CharField |
| FixedQty | old_fixed_qty | FixedQty | decimal(5,1) | 否 | DecimalField |
| ColorID | old_color_id | ColorID | varchar；字节长度 30 | 否 | CharField |

### SourceDyeSemiStockAdjust — 坯布半成品成品与仓储相关表（SemiStockAdjust，待确认）

源表：`dye.SemiStockAdjust`；新表：`src_dye_semistockadjust`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 10 | 是 | CharField |
| BusinessKind | old_business_kind | 业务类别 | smallint | 是 | IntegerField |
| GrayKindID | old_gray_kind_id | 胚纱类别 | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库代码 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 工作流节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyeSemiStockAdjustDetail — 坯布半成品成品与仓储相关表（SemiStockAdjustDetail，待确认）

源表：`dye.SemiStockAdjustDetail`；新表：`src_dye_semistockadjustdetail`；原主键：SheetSeries, DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 调整明细单号 | varchar；字节长度 36 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 物料颜色 | varchar；字节长度 20 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| PaperRolls | old_paper_rolls | 帐面粒数 | decimal(10,2) | 是 | DecimalField |
| RealRolls | old_real_rolls | 实际粒数 | decimal(16,2) | 是 | DecimalField |
| AdjustRolls | old_adjust_rolls | 调整粒数 | decimal(7,2) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(8,2) | 是 | DecimalField |
| StockUnit | old_stock_unit | 库存单位 | tinyint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| PaperLength | old_paper_length | 账面长度 | decimal(10,5) | 是 | DecimalField |
| PaperWeight | old_paper_weight | 账面重量 | decimal(10,5) | 是 | DecimalField |
| RealLengthQty | old_real_length_qty | 实际长度 | decimal(10,2) | 是 | DecimalField |
| RealWeightQty | old_real_weight_qty | 实际重量 | decimal(10,2) | 是 | DecimalField |
| AdjustLengthQty | old_adjust_length_qty | 调整长度 | decimal(10,2) | 是 | DecimalField |
| AdjustWeightQty | old_adjust_weight_qty | 调整重量 | decimal(10,2) | 是 | DecimalField |
| StorageUnitIDs | old_storage_unit_ids | 库位 | varchar；字节长度 100 | 是 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| InSheetKind | old_in_sheet_kind | 物料分类 | varchar；字节长度 20 | 是 | CharField |
| PurchaseOrders | old_purchase_orders | 采购单号 | varchar；字节长度 20 | 是 | CharField |
| A_A | old_a_a | 物料区域 | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | 物料等级 | varchar；字节长度 100 | 是 | CharField |
| FixedQty | old_fixed_qty | 锭重 | decimal(5,2) | 是 | DecimalField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeSemiStockAdjust`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 SemiStockAdjustDetail → SemiStockAdjust。

### SourceDyeSemiStockBook — 半成品库存流水

源表：`dye.SemiStockBook`；新表：`src_dye_semistockbook`；原主键：BookNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| BookNo | old_book_no | BookNo | bigint | 否 | BigIntegerField |
| BookKind | old_book_kind | BookKind | tinyint | 是 | IntegerField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 10 | 是 | CharField |
| SemiKindID | old_semi_kind_id | SemiKindID | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | WareHouseID | varchar；字节长度 10 | 是 | CharField |
| FabricID | old_fabric_id | FabricID | varchar；字节长度 128 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 128 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 是 | CharField |
| StorageUnitID | old_storage_unit_id | StorageUnitID | varchar；字节长度 10 | 是 | CharField |
| SalerGroupID | old_saler_group_id | SalerGroupID | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 10 | 是 | CharField |
| OrderNo | old_order_no | OrderNo | varchar；字节长度 20 | 是 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| CheckNo | old_check_no | CheckNo | varchar；字节长度 20 | 是 | CharField |
| InQty | old_in_qty | InQty | decimal(10,2) | 是 | DecimalField |
| InRolls | old_in_rolls | InRolls | decimal(7,2) | 是 | DecimalField |
| OutQty | old_out_qty | OutQty | decimal(10,2) | 是 | DecimalField |
| OutRolls | old_out_rolls | OutRolls | decimal(7,2) | 是 | DecimalField |
| StockUnit | old_stock_unit | StockUnit | tinyint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| BookDate | old_book_date | BookDate | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 是 | CharField |
| SheetKind | old_sheet_kind | SheetKind | varchar；字节长度 30 | 是 | CharField |
| CurrDate | old_curr_date | CurrDate | datetime | 是 | DateTimeField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 200 | 是 | CharField |
| ReceSheetNo | old_rece_sheet_no | ReceSheetNo | varchar；字节长度 50 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 50 | 是 | CharField |
| InPacks | old_in_packs | InPacks | decimal(7,2) | 是 | DecimalField |
| OutPacks | old_out_packs | OutPacks | decimal(7,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(8,2) | 是 | DecimalField |
| InWeightQty | old_in_weight_qty | InWeightQty | decimal(10,2) | 是 | DecimalField |
| InLengthQty | old_in_length_qty | InLengthQty | decimal(10,2) | 是 | DecimalField |
| InMoney | old_in_money | InMoney | decimal(10,2) | 是 | DecimalField |
| StorageUnitIDs | old_storage_unit_ids | StorageUnitIDs | varchar；字节长度 100 | 是 | CharField |
| OutWeightQty | old_out_weight_qty | OutWeightQty | decimal(10,2) | 是 | DecimalField |
| OutLengthQty | old_out_length_qty | OutLengthQty | decimal(10,2) | 是 | DecimalField |
| OutMoney | old_out_money | OutMoney | decimal(10,2) | 是 | DecimalField |
| SupplierID | old_supplier_id | SupplierID | varchar；字节长度 30 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 20 | 是 | CharField |
| InSheetKind | old_in_sheet_kind | InSheetKind | varchar；字节长度 20 | 是 | CharField |
| PurchaseOrders | old_purchase_orders | PurchaseOrders | varchar；字节长度 20 | 是 | CharField |
| FixedQty | old_fixed_qty | FixedQty | decimal(5,2) | 是 | DecimalField |
| A_A | old_a_a | A_A | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | A_B | varchar；字节长度 100 | 是 | CharField |
| PreField1 | old_pre_field1 | PreField1 | varchar；字节长度 50 | 是 | CharField |
| StockFlag | old_stock_flag | StockFlag | varchar；字节长度 10 | 是 | CharField |

### SourceDyeSemiStockSpecUp — 坯布半成品成品与仓储相关表（SemiStockSpecUp，待确认）

源表：`dye.SemiStockSpecUp`；新表：`src_dye_semistockspecup`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 出库日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| SalerGroupID | old_saler_group_id | 业务组别 | varchar；字节长度 10 | 是 | CharField |
| SalerID | old_saler_id | 业务员 | varchar；字节长度 10 | 是 | CharField |
| StockUnit | old_stock_unit | 库存单位 | tinyint | 是 | IntegerField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | nvarchar；字节长度 40 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库 | varchar；字节长度 50 | 是 | CharField |

### SourceDyeSemiStockSpecUpDetail — 坯布半成品成品与仓储相关表（SemiStockSpecUpDetail，待确认）

源表：`dye.SemiStockSpecUpDetail`；新表：`src_dye_semistockspecupdetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 是 | CharField |
| AssignedNo | old_assigned_no | 投胚流水号 | varchar；字节长度 20 | 是 | CharField |
| ReceSheetNo | old_rece_sheet_no | 入库明细号 | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |
| PCS | old_pcs | 粒/件 | int | 是 | IntegerField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| Packs | old_packs | 件数 | decimal(7,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(8,2) | 是 | DecimalField |
| CheckNo | old_check_no | 订单明细号 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Area | old_area | 区域 | varchar；字节长度 100 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | 库位 | varchar；字节长度 100 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库 | varchar；字节长度 20 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 30 | 是 | CharField |
| InSheetKind | old_in_sheet_kind | 物料分类 | varchar；字节长度 20 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 物料颜色 | varchar；字节长度 20 | 是 | CharField |
| FixedQty | old_fixed_qty | 锭重 | decimal(5,2) | 是 | DecimalField |
| SupplierID | old_supplier_id | 供应商 | varchar；字节长度 30 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度(H/S) | varchar；字节长度 50 | 是 | CharField |
| PurchaseOrders | old_purchase_orders | 采购单号 | varchar；字节长度 20 | 是 | CharField |
| A_A | old_a_a | 物料区域 | varchar；字节长度 50 | 是 | CharField |
| A_B | old_a_b | 物料等级 | varchar；字节长度 100 | 是 | CharField |
| UPCustomerID | old_upcustomer_id | 调整客户 | varchar；字节长度 30 | 是 | CharField |
| UPInSheetKind | old_upin_sheet_kind | 调整物料分类 | varchar；字节长度 20 | 是 | CharField |
| UPProdID | old_upprod_id | 调整规格 | varchar；字节长度 50 | 是 | CharField |
| UPLotNo | old_uplot_no | 调整批号 | varchar；字节长度 50 | 是 | CharField |
| UPColorID | old_upcolor_id | 调整物料颜色 | varchar；字节长度 20 | 是 | CharField |
| UPFixedQty | old_upfixed_qty | 调整锭重 | decimal(5,2) | 是 | DecimalField |
| UPPreField1 | old_uppre_field1 | 调整捻度(H/S) | varchar；字节长度 50 | 是 | CharField |
| UPPurchaseOrders | old_uppurchase_orders | 调整采购单号 | varchar；字节长度 20 | 是 | CharField |
| UPA_A | old_upa_a | 调整物料缸号 | varchar；字节长度 50 | 是 | CharField |
| UPA_B | old_upa_b | 调整物料等级 | varchar；字节长度 100 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeSemiStockSpecUp`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 SemiStockSpecUpDetail → SemiStockSpecUp。

### SourceDyeStuffStep — 染化料与称料库存相关表（Stuff_Step，待确认）

源表：`dye.Stuff_Step`；新表：`src_dye_stuff_step`；原主键：Code。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| Code | old_code | 编码 | varchar；字节长度 20 | 否 | CharField |
| Name | old_name | 备料步骤 | varchar；字节长度 100 | 否 | CharField |
| Reserved1 | old_reserved1 | Reserved1 | int | 是 | IntegerField |
| CodeNo | old_code_no | 步骤号 | int | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |

### SourceDyeStuffAllot — 染化料与称料库存相关表（StuffAllot，待确认）

源表：`dye.StuffAllot`；新表：`src_dye_stuffallot`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 36 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | 调出仓库 | varchar；字节长度 10 | 是 | CharField |
| DeptID | old_dept_id | 申领部门 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 50 | 是 | CharField |
| Keeper | old_keeper | 仓管员 | varchar；字节长度 100 | 是 | CharField |
| EmpID | old_emp_id | 领料人 | varchar；字节长度 50 | 是 | CharField |
| WeightSheetNo | old_weight_sheet_no | WeightSheetNo | varchar；字节长度 20 | 是 | CharField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | SheetStatus | varchar；字节长度 1 | 是 | CharField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | varchar；字节长度 20 | 是 | CharField |
| ToWareHouseID | old_to_ware_house_id | 调入仓库 | varchar；字节长度 10 | 是 | CharField |

### SourceDyeStuffAllotDetail — 染化料与称料库存相关表（StuffAllotDetail，待确认）

源表：`dye.StuffAllotDetail`；新表：`src_dye_stuffallotdetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 是 | CharField |
| DetailNo | old_detail_no | 表单明细号（子表） | varchar；字节长度 36 | 否 | CharField |
| PurDetailNo | old_pur_detail_no | 采购单明细号 | varchar；字节长度 20 | 是 | CharField |
| StuffID | old_stuff_id | 染化料代码 | varchar；字节长度 10 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 200 | 是 | CharField |
| Qty | old_qty | 数量 | decimal(12,6) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(16,6) | 是 | DecimalField |
| TaxPrice | old_tax_price | 含税价 | decimal(16,6) | 是 | DecimalField |
| TaxRate | old_tax_rate | 税率 | decimal(4,2) | 是 | DecimalField |
| TaxMoney | old_tax_money | 税金 | decimal(10,2) | 是 | DecimalField |
| Amount | old_amount | 金额 | decimal(16,2) | 是 | DecimalField |
| APDetailNo | old_apdetail_no | 应付单细号 | varchar；字节长度 20 | 是 | CharField |
| InDetailNo | old_in_detail_no | InDetailNo | varchar；字节长度 50 | 是 | CharField |
| DlvQty | old_dlv_qty | 交货数量 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| StockUnit | old_stock_unit | 单位 | varchar；字节长度 1 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeStuffAllot`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 StuffAllotDetail → StuffAllot。

### SourceDyeStuffChange — 染化料与称料库存相关表（StuffChange，待确认）

源表：`dye.StuffChange`；新表：`src_dye_stuffchange`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| StartTime | old_start_time | StartTime | char；字节长度 14 | 是 | CharField |
| Reason | old_reason | Reason | nvarchar；字节长度 512 | 是 | CharField |
| OriStuffID | old_ori_stuff_id | OriStuffID | varchar；字节长度 10 | 是 | CharField |
| OriLotNo | old_ori_lot_no | OriLotNo | varchar；字节长度 50 | 是 | CharField |
| RemainQty | old_remain_qty | RemainQty | decimal(10,2) | 是 | DecimalField |
| StuffID | old_stuff_id | StuffID | varchar；字节长度 10 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 是 | CharField |
| InQty | old_in_qty | InQty | decimal(10,2) | 是 | DecimalField |
| InDate | old_in_date | InDate | datetime | 是 | DateTimeField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |

### SourceDyeStuffIn — 染化料入库单

源表：`dye.StuffIn`；新表：`src_dye_stuffin`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| WareHouseID | old_ware_house_id | 仓库 | varchar；字节长度 10 | 是 | CharField |
| SupplierID | old_supplier_id | 供应商 | varchar；字节长度 10 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | SheetStatus | varchar；字节长度 1 | 是 | CharField |
| Keeper | old_keeper | 仓管员 | varchar；字节长度 10 | 是 | CharField |
| Reason | old_reason | Reason | nvarchar；字节长度 512 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| APMoney | old_apmoney | APMoney | decimal(10,2) | 是 | DecimalField |
| APQty | old_apqty | APQty | decimal(10,2) | 是 | DecimalField |
| UnClearQty | old_un_clear_qty | UnClearQty | decimal(10,2) | 是 | DecimalField |
| UnClearMoney | old_un_clear_money | UnClearMoney | decimal(10,2) | 是 | DecimalField |
| UnClearInvoiceQty | old_un_clear_invoice_qty | UnClearInvoiceQty | decimal(10,2) | 是 | DecimalField |
| UnClearInvoiceMoney | old_un_clear_invoice_money | UnClearInvoiceMoney | decimal(10,2) | 是 | DecimalField |
| Discount | old_discount | Discount | decimal(3,2) | 是 | DecimalField |
| DiscountMoney | old_discount_money | DiscountMoney | decimal(10,2) | 是 | DecimalField |
| Total | old_total | Total | decimal(10,2) | 是 | DecimalField |
| BuyerID | old_buyer_id | 采购员 | varchar；字节长度 50 | 是 | CharField |
| invoice | old_invoice | 发票单号 | varchar；字节长度 50 | 是 | CharField |

### SourceDyeStuffInDetail — 染化料入库明细

源表：`dye.StuffInDetail`；新表：`src_dye_stuffindetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | 表单明细号（子表） | varchar；字节长度 36 | 否 | CharField |
| PurDetailNo | old_pur_detail_no | 采购单明细号 | varchar；字节长度 20 | 是 | CharField |
| StuffID | old_stuff_id | 染化料代码 | varchar；字节长度 10 | 是 | CharField |
| Price | old_price | 单价 | decimal(16,6) | 是 | DecimalField |
| TaxPrice | old_tax_price | 含税价 | decimal(16,6) | 是 | DecimalField |
| TaxRate | old_tax_rate | 税率 | decimal(4,2) | 是 | DecimalField |
| TaxMoney | old_tax_money | 税金 | decimal(10,2) | 是 | DecimalField |
| Amount | old_amount | 金额 | decimal(10,2) | 是 | DecimalField |
| Qty | old_qty | 数量 | decimal(12,6) | 是 | DecimalField |
| APDetailNo | old_apdetail_no | 应付单细号 | varchar；字节长度 100 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 50 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| PackUnit | old_pack_unit | 包装单位 | varchar；字节长度 10 | 是 | CharField |
| PackQty | old_pack_qty | 包装数量 | decimal(10,2) | 是 | DecimalField |
| NewStuffID | old_new_stuff_id | NewStuffID | varchar；字节长度 20 | 是 | CharField |
| StuffType | old_stuff_type | StuffType | varchar；字节长度 1 | 是 | CharField |
| StuffKindID | old_stuff_kind_id | StuffKindID | varchar；字节长度 50 | 是 | CharField |
| StuffName | old_stuff_name | StuffName | varchar；字节长度 300 | 是 | CharField |
| OriInDetailNo | old_ori_in_detail_no | 原入库明细 | varchar；字节长度 30 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeStuffIn`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 SmallStuffInDetail → SmallStuffIn；原界面主从 StuffInDetail → StuffIn。

### SourceDyeStuffOut — 染化料出库单

源表：`dye.StuffOut`；新表：`src_dye_stuffout`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | 仓库 | varchar；字节长度 10 | 是 | CharField |
| DeptID | old_dept_id | 申领部门 | varchar；字节长度 10 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| Keeper | old_keeper | 仓管员 | varchar；字节长度 100 | 是 | CharField |
| EmpID | old_emp_id | 领料人 | varchar；字节长度 10 | 是 | CharField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | SheetStatus | varchar；字节长度 1 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| WeightSheetNo | old_weight_sheet_no | 称料单号 | varchar；字节长度 20 | 是 | CharField |
| InDetailNo | old_in_detail_no | InDetailNo | varchar；字节长度 50 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| OutDate | old_out_date | 出库日期 | datetime | 是 | DateTimeField |
| MachineID | old_machine_id | 机台号 | varchar；字节长度 255 | 是 | CharField |
| SQSheetNo | old_sqsheet_no | 申请单号 | varchar；字节长度 50 | 是 | CharField |
| FactID | old_fact_id | 领用分厂 | varchar；字节长度 50 | 是 | CharField |
| CombineSheetNos | old_combine_sheet_nos | 合染缸号 | varchar；字节长度 100 | 是 | CharField |
| ShiftID | old_shift_id | 班别 | varchar；字节长度 20 | 是 | CharField |

### SourceDyeStuffOutDetail — 染化料出库明细

源表：`dye.StuffOutDetail`；新表：`src_dye_stuffoutdetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | 表单明细号（子表） | varchar；字节长度 36 | 否 | CharField |
| PurDetailNo | old_pur_detail_no | 采购单明细号 | varchar；字节长度 20 | 是 | CharField |
| StuffID | old_stuff_id | 染化料代码 | varchar；字节长度 10 | 是 | CharField |
| Price | old_price | 单价 | decimal(16,6) | 是 | DecimalField |
| TaxPrice | old_tax_price | 含税价 | decimal(16,6) | 是 | DecimalField |
| TaxRate | old_tax_rate | 税率 | decimal(16,6) | 是 | DecimalField |
| TaxMoney | old_tax_money | 税金 | decimal(16,2) | 是 | DecimalField |
| Amount | old_amount | 金额 | decimal(16,2) | 是 | DecimalField |
| Qty | old_qty | 数量 | decimal(15,6) | 是 | DecimalField |
| APDetailNo | old_apdetail_no | 应付单细号 | varchar；字节长度 20 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 200 | 是 | CharField |
| DlvQty | old_dlv_qty | 交货数量 | decimal(12,6) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| InDetailNo | old_in_detail_no | InDetailNo | varchar；字节长度 50 | 是 | CharField |
| PhaseNo | old_phase_no | 染程号 | tinyint | 是 | IntegerField |
| PhaseID | old_phase_id | 染程 | varchar；字节长度 50 | 是 | CharField |
| StuffNo | old_stuff_no | 序号 | tinyint | 是 | IntegerField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeStuffOut`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 StuffOutDetail → StuffOut；原界面主从 DStuffOutDetail → DStuffOut；原界面主从 SmallStuffOutDetail → SmallStuffOut。

### SourceDyeStuffStock — 染化料与称料库存相关表（StuffStock，待确认）

源表：`dye.StuffStock`；新表：`src_dye_stuffstock`；原主键：StockDate, StuffID, WareHouseID, InDetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| StockDate | old_stock_date | StockDate | datetime | 否 | DateTimeField |
| StuffID | old_stuff_id | StuffID | varchar；字节长度 10 | 否 | CharField |
| WareHouseID | old_ware_house_id | WareHouseID | varchar；字节长度 10 | 否 | CharField |
| PreMonthQty | old_pre_month_qty | PreMonthQty | decimal(10,2) | 是 | DecimalField |
| Price | old_price | Price | decimal(10,4) | 是 | DecimalField |
| PreMonthMoney | old_pre_month_money | PreMonthMoney | decimal(10,2) | 是 | DecimalField |
| CarryDate | old_carry_date | CarryDate | datetime | 是 | DateTimeField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 是 | CharField |
| LastStockQty | old_last_stock_qty | LastStockQty | decimal(10,2) | 是 | DecimalField |
| LastStockMoney | old_last_stock_money | LastStockMoney | decimal(10,2) | 是 | DecimalField |
| InQty | old_in_qty | InQty | decimal(10,2) | 是 | DecimalField |
| InMoney | old_in_money | InMoney | decimal(10,2) | 是 | DecimalField |
| OutQty | old_out_qty | OutQty | decimal(10,2) | 是 | DecimalField |
| OutMoney | old_out_money | OutMoney | decimal(10,2) | 是 | DecimalField |
| InDetailNo | old_in_detail_no | InDetailNo | varchar；字节长度 50 | 否 | CharField |

### SourceDyeStuffStockAdjust — 染化料与称料库存相关表（StuffStockAdjust，待确认）

源表：`dye.StuffStockAdjust`；新表：`src_dye_stuffstockadjust`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| WareHouseID | old_ware_house_id | 仓库代码 | varchar；字节长度 10 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | nvarchar；字节长度 40 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 10 | 是 | CharField |

### SourceDyeStuffStockAdjustDetail — 染化料与称料库存相关表（StuffStockAdjustDetail，待确认）

源表：`dye.StuffStockAdjustDetail`；新表：`src_dye_stuffstockadjustdetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 关联单号 | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | 表单明细号 | varchar；字节长度 36 | 否 | CharField |
| StuffID | old_stuff_id | 染化料编码 | varchar；字节长度 10 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 200 | 是 | CharField |
| PaperQty | old_paper_qty | 账面数量 | decimal(12,6) | 是 | DecimalField |
| RealQty | old_real_qty | 实际数量 | decimal(12,6) | 是 | DecimalField |
| AdjustQty | old_adjust_qty | 调整数量 | decimal(12,6) | 是 | DecimalField |
| Price | old_price | 单价 | decimal(8,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| PaperMoney | old_paper_money | 账面金额 | decimal(14,6) | 是 | DecimalField |
| RealMoney | old_real_money | 实际金额 | decimal(14,6) | 是 | DecimalField |
| AdjustMoney | old_adjust_money | 调整金额 | decimal(14,6) | 是 | DecimalField |
| InDetailNo | old_in_detail_no | 入库明细单号 | varchar；字节长度 50 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeStuffStockAdjust`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 StuffStockAdjustDetail → StuffStockAdjust。

### SourceDyeStuffStockBook — 染化料库存流水

源表：`dye.StuffStockBook`；新表：`src_dye_stuffstockbook`；原主键：BookNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| BookNo | old_book_no | BookNo | bigint | 否 | BigIntegerField |
| BookDate | old_book_date | BookDate | datetime | 是 | DateTimeField |
| AccDate | old_acc_date | AccDate | datetime | 是 | DateTimeField |
| BookKind | old_book_kind | BookKind | tinyint | 是 | IntegerField |
| SupplierID | old_supplier_id | SupplierID | varchar；字节长度 10 | 是 | CharField |
| WareHouseID | old_ware_house_id | WareHouseID | varchar；字节长度 10 | 是 | CharField |
| StuffID | old_stuff_id | StuffID | varchar；字节长度 10 | 是 | CharField |
| StorageUnitIDs | old_storage_unit_ids | StorageUnitIDs | varchar；字节长度 100 | 是 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 20 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 是 | CharField |
| InQty | old_in_qty | InQty | decimal(12,6) | 是 | DecimalField |
| OutQty | old_out_qty | OutQty | decimal(15,6) | 是 | DecimalField |
| Price | old_price | Price | decimal(14,4) | 是 | DecimalField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 10 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 200 | 是 | CharField |
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 是 | CharField |
| StockFlag | old_stock_flag | StockFlag | varchar；字节长度 1 | 是 | CharField |
| InMoney | old_in_money | InMoney | decimal(10,2) | 是 | DecimalField |
| OutMoney | old_out_money | OutMoney | decimal(10,2) | 是 | DecimalField |
| CurrDate | old_curr_date | CurrDate | datetime | 是 | DateTimeField |
| InDetailNo | old_in_detail_no | InDetailNo | varchar；字节长度 20 | 是 | CharField |

### SourceDyeSwipeLabelPrint — 染色工艺与配方相关表（SwipeLabelPrint，待确认）

源表：`dye.SwipeLabelPrint`；新表：`src_dye_swipelabelprint`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | 制单单号 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| MachineID | old_machine_id | 机台 | varchar；字节长度 20 | 是 | CharField |
| GradeID | old_grade_id | 等级 | varchar；字节长度 20 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1000 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 审核状态 | smallint | 是 | IntegerField |
| RptID | old_rpt_id | 报表菜单 | varchar；字节长度 20 | 是 | CharField |
| PrintNumber | old_print_number | 打印份数 | int | 是 | IntegerField |
| PrintCount | old_print_count | 打印次数 | int | 是 | IntegerField |
| CheckNo | old_check_no | 订单明细 | varchar；字节长度 50 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 150 | 是 | CharField |
| CustSelfNo | old_cust_self_no | 制单 | nvarchar；字节长度 300 | 是 | CharField |
| ProdIDName | old_prod_idname | 本厂规格 | varchar；字节长度 150 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 150 | 是 | CharField |
| PreField1 | old_pre_field1 | 捻度 | varchar；字节长度 150 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 150 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 150 | 是 | CharField |
| CustomerRemarks | old_customer_remarks | 客户备注 | varchar；字节长度 150 | 是 | CharField |
| EmpID | old_emp_id | 员工编号 | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 150 | 是 | CharField |
| CustJobNo | old_cust_job_no | CustJobNo | varchar；字节长度 150 | 是 | CharField |

### SourceDyeUrgentInStruct — 其他或待确认相关表（UrgentInStruct，待确认）

源表：`dye.UrgentInStruct`；新表：`src_dye_urgentinstruct`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 否 | CharField |
| SheetNo | old_sheet_no | SheetNo | varchar；字节长度 36 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| SheetStatus | old_sheet_status | SheetStatus | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| RightStatus | old_right_status | RightStatus | smallint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 50 | 是 | CharField |
| DlvAddress | old_dlv_address | DlvAddress | varchar；字节长度 200 | 是 | CharField |
| CarNo | old_car_no | CarNo | varchar；字节长度 50 | 是 | CharField |
| Driver | old_driver | Driver | varchar；字节长度 50 | 是 | CharField |

### SourceDyeUrgentInStructDetail — 其他或待确认相关表（UrgentInStructDetail，待确认）

源表：`dye.UrgentInStructDetail`；新表：`src_dye_urgentinstructdetail`；原主键：DetailNo。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 50 | 是 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 50 | 是 | CharField |
| Rolls | old_rolls | Rolls | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | LengthQty | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | WeightQty | decimal(10,2) | 是 | DecimalField |
| StockUnit | old_stock_unit | StockUnit | varchar；字节长度 50 | 是 | CharField |
| ContractNo | old_contract_no | ContractNo | varchar；字节长度 20 | 是 | CharField |
| Spec | old_spec | Spec | varchar；字节长度 200 | 是 | CharField |
| Structure | old_structure | Structure | varchar；字节长度 200 | 是 | CharField |
| SalerID | old_saler_id | SalerID | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | CustSelfProduct | varchar；字节长度 250 | 是 | CharField |
| CustSelfNo | old_cust_self_no | CustSelfNo | varchar；字节长度 50 | 是 | CharField |
| OrderSheetNo | old_order_sheet_no | OrderSheetNo | varchar；字节长度 50 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 50 | 是 | CharField |
| CustColorNum | old_cust_color_num | CustColorNum | varchar；字节长度 50 | 是 | CharField |
| Weight | old_weight | Weight | varchar；字节长度 50 | 是 | CharField |
| Width | old_width | Width | varchar；字节长度 50 | 是 | CharField |
| DetailCustName | old_detail_cust_name | DetailCustName | varchar；字节长度 50 | 是 | CharField |
| OrderSheetDate | old_order_sheet_date | OrderSheetDate | datetime | 是 | DateTimeField |
| CurrProcessID | old_curr_process_id | CurrProcessID | varchar；字节长度 50 | 是 | CharField |
| CustJobNo | old_cust_job_no | CustJobNo | varchar；字节长度 50 | 是 | CharField |
| Jobattes1 | old_jobattes1 | Jobattes1 | varchar；字节长度 100 | 是 | CharField |
| RealLotNo | old_real_lot_no | RealLotNo | varchar；字节长度 50 | 是 | CharField |

### SourceDyeWareHouseProdCount — 坯布半成品成品与仓储相关表（WareHouseProdCount，待确认）

源表：`dye.WareHouseProdCount`；新表：`src_dye_warehouseprodcount`；原主键：SheetSeries。

归属依据：实物仓储/包装来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 20 | 是 | CharField |
| SheetKind | old_sheet_kind | 单据类别 | smallint | 是 | IntegerField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| Customer | old_customer | 客户 | varchar；字节长度 10 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 150 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量数量 | decimal(10,2) | 是 | DecimalField |
| Cargador1 | old_cargador1 | 装/配工 | varchar；字节长度 10 | 是 | CharField |
| Cargador2 | old_cargador2 | 装/配工 | varchar；字节长度 10 | 是 | CharField |
| Cargador3 | old_cargador3 | 装/配工 | varchar；字节长度 10 | 是 | CharField |
| Cargador4 | old_cargador4 | 装/配工 | varchar；字节长度 10 | 是 | CharField |
| Cargador5 | old_cargador5 | 装/配工 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |

### SourceDyeWeightTechInfo — 染化料与称料库存相关表（WeightTechInfo，待确认）

源表：`dye.WeightTechInfo`；新表：`src_dye_weighttechinfo`；原主键：DetailNo。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 30 | 否 | CharField |
| Tech | old_tech | Tech | varchar；字节长度 50 | 是 | CharField |
| ParameterNo | old_parameter_no | ParameterNo | varchar；字节长度 10 | 是 | CharField |
| ParameterID | old_parameter_id | ParameterID | varchar；字节长度 20 | 是 | CharField |
| ParameterName | old_parameter_name | ParameterName | varchar；字节长度 50 | 是 | CharField |
| ParameterValue | old_parameter_value | ParameterValue | decimal(10,2) | 是 | DecimalField |
| ProgId | old_prog_id | ProgId | int | 是 | IntegerField |

### SourceDyeWidthGramWeight — 染化料与称料库存相关表（WidthGramWeight，待确认）

源表：`dye.WidthGramWeight`；新表：`src_dye_widthgramweight`；原主键：Code。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| Code | old_code | Code | nvarchar；字节长度 40 | 否 | CharField |
| NameC | old_name_c | 名称 | nvarchar；字节长度 100 | 是 | CharField |
| NumValue | old_num_value | NumValue | decimal(18,2) | 是 | DecimalField |
| Creater | old_creater | Creater | varchar；字节长度 50 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | Modifyer | varchar；字节长度 50 | 是 | CharField |
| ModifyDate | old_modify_date | ModifyDate | datetime | 是 | DateTimeField |
| Kind | old_kind | 类型 | varchar；字节长度 50 | 是 | CharField |

## 质量管理

新增原表模型 25 个，原字段 627 个。

### SourceDyeCHECKEXACT — 质量检验与异常相关表（CHECKEXACT，待确认）

源表：`dye.CHECKEXACT`；新表：`src_dye_checkexact`；原主键：EXACTID。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| EXACTID | old_exactid | EXACTID | int | 否 | IntegerField |
| USERID | old_userid | USERID | int | 是 | IntegerField |
| CHECKTIME | old_checktime | CHECKTIME | datetime | 是 | DateTimeField |
| CHECKTYPE | old_checktype | CHECKTYPE | varchar；字节长度 2 | 是 | CharField |
| ISADD | old_isadd | ISADD | smallint | 是 | IntegerField |
| YUYIN | old_yuyin | YUYIN | varchar；字节长度 25 | 是 | CharField |
| ISMODIFY | old_ismodify | ISMODIFY | smallint | 是 | IntegerField |
| ISDELETE | old_isdelete | ISDELETE | smallint | 是 | IntegerField |
| INCOUNT | old_incount | INCOUNT | smallint | 是 | IntegerField |
| ISCOUNT | old_iscount | ISCOUNT | smallint | 是 | IntegerField |
| MODIFYBY | old_modifyby | MODIFYBY | varchar；字节长度 20 | 是 | CharField |
| DATE | old_date | DATE | datetime | 是 | DateTimeField |

### SourceDyeCHECKINOUT — 质量检验与异常相关表（CHECKINOUT，待确认）

源表：`dye.CHECKINOUT`；新表：`src_dye_checkinout`；原主键：USERID, CHECKTIME。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| USERID | old_userid | USERID | int | 否 | IntegerField |
| CHECKTIME | old_checktime | CHECKTIME | datetime | 否 | DateTimeField |
| CHECKTYPE | old_checktype | CHECKTYPE | varchar；字节长度 1 | 是 | CharField |
| VERIFYCODE | old_verifycode | VERIFYCODE | int | 是 | IntegerField |
| SENSORID | old_sensorid | SENSORID | varchar；字节长度 5 | 是 | CharField |
| Memoinfo | old_memoinfo | Memoinfo | varchar；字节长度 30 | 是 | CharField |
| WorkCode | old_work_code | WorkCode | varchar；字节长度 50 | 是 | CharField |
| sn | old_sn | sn | varchar；字节长度 20 | 是 | CharField |
| UserExtFmt | old_user_ext_fmt | UserExtFmt | smallint | 是 | IntegerField |
| mask_flag | old_mask_flag | mask_flag | int | 是 | IntegerField |
| temperature | old_temperature | temperature | float | 是 | FloatField |

### SourceDyeColoringCheck — 质量检验与异常相关表（ColoringCheck，待确认）

源表：`dye.ColoringCheck`；新表：`src_dye_coloringcheck`；原主键：ID。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | bigint | 否 | BigIntegerField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| Creater | old_creater | 登记人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 登记日期 | datetime | 是 | DateTimeField |
| ProcessID | old_process_id | 工序 | varchar；字节长度 20 | 是 | CharField |
| DefectID | old_defect_id | DefectID | varchar；字节长度 50 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 100 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 100 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 100 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 100 | 是 | CharField |
| Rolls | old_rolls | 粒数 | int | 是 | IntegerField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| EmpID | old_emp_id | 员工 | varchar；字节长度 20 | 是 | CharField |
| ShiftID | old_shift_id | 生产班组 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |
| DyeProcessID | old_dye_process_id | 完成步骤 | varchar；字节长度 100 | 是 | CharField |
| RealValue | old_real_value | RealValue | float | 是 | FloatField |
| CurveID | old_curve_id | 染色工序 | varchar；字节长度 10 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| WProcessNo | old_wprocess_no | 记录号 | varchar；字节长度 20 | 是 | CharField |
| Approver | old_approver | Approver | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |

### SourceDyeDefectiveIn — 质量检验与异常相关表（DefectiveIn，待确认）

源表：`dye.DefectiveIn`；新表：`src_dye_defectivein`；原主键：SheetSeries。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | Approver | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | ApproveDate | datetime | 是 | DateTimeField |
| PendOutSheetSeries | old_pend_out_sheet_series | PendOutSheetSeries | varchar；字节长度 50 | 是 | CharField |

### SourceDyeDefectiveInDetail — 质量检验与异常相关表（DefectiveInDetail，待确认）

源表：`dye.DefectiveInDetail`；新表：`src_dye_defectiveindetail`；原主键：SheetSeries, DetailNo。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 20 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 20 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 20 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 200 | 是 | CharField |
| CustomerProdName | old_customer_prod_name | 客户纱种 | varchar；字节长度 200 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 150 | 是 | CharField |
| Weight | old_weight | 克重 | varchar；字节长度 256 | 是 | CharField |
| Width | old_width | 幅宽 | varchar；字节长度 256 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 实重 | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| Description | old_description | 质量描述 | varchar；字节长度 512 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| QualityDeductionSheetNo | old_quality_deduction_sheet_no | 扣罚单号 | varchar；字节长度 32 | 是 | CharField |
| GrayQty | old_gray_qty | 胚重 | decimal(10,2) | 是 | DecimalField |
| qy | old_qy | 区域 | varchar；字节长度 150 | 是 | CharField |
| kw | old_kw | 库位 | varchar；字节长度 150 | 是 | CharField |

关联 `source_parent_1` → `erp_quality.SourceDyeDefectiveIn`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 DefectiveInDetail → DefectiveIn。

### SourceDyeDefectiveInRecord — 质量检验与异常相关表（DefectiveInRecord，待确认）

源表：`dye.DefectiveInRecord`；新表：`src_dye_defectiveinrecord`；原主键：SheetSeries, DetailNo, RollNo。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 50 | 否 | CharField |
| RollNo | old_roll_no | 箱号 | varchar；字节长度 20 | 否 | CharField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 毛重 | decimal(10,2) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 仓位 | varchar；字节长度 100 | 是 | CharField |
| Status | old_status | 状态 | varchar；字节长度 1 | 是 | CharField |
| OutDetailNo | old_out_detail_no | 出库明细单号 | varchar；字节长度 20 | 是 | CharField |
| BarCode | old_bar_code | 条码 | varchar；字节长度 50 | 否 | CharField |
| GradeID | old_grade_id | 色号等级 | varchar；字节长度 10 | 是 | CharField |
| GrayQty | old_gray_qty | GrayQty | decimal(10,2) | 是 | DecimalField |
| AdjustQty | old_adjust_qty | AdjustQty | decimal(10,2) | 是 | DecimalField |
| RealQty | old_real_qty | 实重 | decimal(10,2) | 是 | DecimalField |
| Meter | old_meter | 米数 | decimal(10,2) | 是 | DecimalField |
| Yard | old_yard | 码数 | decimal(10,2) | 是 | DecimalField |
| Note | old_note | 备注 | varchar；字节长度 50 | 是 | CharField |
| GrayBarCode | old_gray_bar_code | GrayBarCode | varchar；字节长度 100 | 是 | CharField |
| RollNo3 | old_roll_no3 | RollNo3 | varchar；字节长度 20 | 是 | CharField |
| GUnit | old_gunit | GUnit | tinyint | 是 | IntegerField |
| PUnit | old_punit | PUnit | tinyint | 是 | IntegerField |

### SourceDyeDefectiveOut — 质量检验与异常相关表（DefectiveOut，待确认）

源表：`dye.DefectiveOut`；新表：`src_dye_defectiveout`；原主键：SheetSeries。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |

### SourceDyeDefectiveOutDetail — 质量检验与异常相关表（DefectiveOutDetail，待确认）

源表：`dye.DefectiveOutDetail`；新表：`src_dye_defectiveoutdetail`；原主键：SheetSeries, DetailNo。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 明细单号 | varchar；字节长度 20 | 否 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 20 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 20 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 10 | 是 | CharField |
| CustomerProdName | old_customer_prod_name | 客户纱种 | nvarchar；字节长度 200 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 150 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 150 | 是 | CharField |
| Weight | old_weight | 克重 | varchar；字节长度 256 | 是 | CharField |
| Width | old_width | 幅宽 | varchar；字节长度 256 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度 | decimal(10,2) | 是 | DecimalField |
| Description | old_description | 描述 | varchar；字节长度 512 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| DefectiveInDetailNo | old_defective_in_detail_no | 次品入库明细 | varchar；字节长度 20 | 是 | CharField |
| GrayQty | old_gray_qty | 胚重 | decimal(8,2) | 是 | DecimalField |
| JingZhong | old_jing_zhong | 净重 | decimal(10,2) | 是 | DecimalField |
| ShiZhong | old_shi_zhong | 实重 | decimal(10,2) | 是 | DecimalField |
| ZhiTong | old_zhi_tong | 纸筒 | decimal(6,1) | 是 | DecimalField |
| KongJia | old_kong_jia | 空加 | decimal(6,1) | 是 | DecimalField |
| OrderSheetDate | old_order_sheet_date | OrderSheetDate | datetime | 是 | DateTimeField |

关联 `source_parent_1` → `erp_quality.SourceDyeDefectiveOut`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 DefectiveOutDetail → DefectiveOut。

### SourceDyeDefectiveOutRecord — 质量检验与异常相关表（DefectiveOutRecord，待确认）

源表：`dye.DefectiveOutRecord`；新表：`src_dye_defectiveoutrecord`；原主键：SheetSeries, DetailNo, BarCode, RollNo。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 出库单流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | 出库明细号 | varchar；字节长度 36 | 否 | CharField |
| BarCode | old_bar_code | 条码 | varchar；字节长度 50 | 否 | CharField |
| RollNo | old_roll_no | 箱号 | varchar；字节长度 20 | 否 | CharField |
| LengthQty | old_length_qty | 成品长度 | decimal(10,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 成品重量 | decimal(10,2) | 是 | DecimalField |
| StorageUnitID | old_storage_unit_id | 库位 | varchar；字节长度 100 | 是 | CharField |
| Status | old_status | 状态 | varchar；字节长度 1 | 是 | CharField |
| OutDetailNo | old_out_detail_no | OutDetailNo | varchar；字节长度 20 | 是 | CharField |
| GradeID | old_grade_id | 色号等级 | varchar；字节长度 10 | 是 | CharField |
| GrayQty | old_gray_qty | 胚纱重量 | decimal(10,2) | 是 | DecimalField |
| AdjustQty | old_adjust_qty | AdjustQty | decimal(10,2) | 是 | DecimalField |
| RealQty | old_real_qty | 实重 | decimal(10,2) | 是 | DecimalField |
| Meter | old_meter | 米数 | decimal(10,2) | 是 | DecimalField |
| Yard | old_yard | 胚纱长度 | decimal(10,2) | 是 | DecimalField |
| GrayBarCode | old_gray_bar_code | GrayBarCode | varchar；字节长度 100 | 是 | CharField |
| RollNo3 | old_roll_no3 | 箱号2 | varchar；字节长度 20 | 是 | CharField |
| GUnit | old_gunit | GUnit | tinyint | 是 | IntegerField |
| PUnit | old_punit | PUnit | tinyint | 是 | IntegerField |
| GKg | old_gkg | GKg | decimal(6,2) | 是 | DecimalField |
| GPound | old_gpound | GPound | decimal(6,2) | 是 | DecimalField |
| PKg | old_pkg | PKg | decimal(6,2) | 是 | DecimalField |
| PPound | old_ppound | PPound | decimal(6,2) | 是 | DecimalField |
| Rolls | old_rolls | Rolls | decimal(4,2) | 是 | DecimalField |

关联 `source_parent_1` → `erp_quality.SourceDyeDefectiveOutDetail`；原码 `SheetSeries, DetailNo` → 父表原码 `SheetSeries, DetailNo`；依据：原界面主从 DefectiveOutRecord → DefectiveOutDetail。

### SourceDyeDyeCheck — 质量检验与异常相关表（DyeCheck，待确认）

源表：`dye.DyeCheck`；新表：`src_dye_dyecheck`；原主键：ID。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ID | old_id | ID | bigint | 否 | BigIntegerField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 是 | CharField |
| DyePhaseID | old_dye_phase_id | DyePhaseID | varchar；字节长度 10 | 是 | CharField |
| Creater | old_creater | Creater | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | CreateDate | datetime | 是 | DateTimeField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 20 | 是 | CharField |

### SourceDyeDyeCheckout — 财务结算与成本相关表（dyeCheckout，待确认）

源表：`dye.dyeCheckout`；新表：`src_dye_dyecheckout`；原主键：无主键。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| WProcessNo | old_wprocess_no | WProcessNo | varchar；字节长度 50 | 是 | CharField |
| DAYS | old_days | DAYS | varchar；字节长度 10 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | JobSheetNo | varchar；字节长度 50 | 否 | CharField |
| ProdID | old_prod_id | ProdID | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | ColorID | varchar；字节长度 50 | 是 | CharField |
| ColorNum | old_color_num | ColorNum | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 50 | 是 | CharField |
| ShiftID | old_shift_id | ShiftID | varchar；字节长度 50 | 是 | CharField |
| Class | old_class | Class | varchar；字节长度 50 | 是 | CharField |
| ClassID | old_class_id | ClassID | varchar；字节长度 50 | 是 | CharField |
| StationID | old_station_id | StationID | varchar；字节长度 50 | 是 | CharField |
| EndTime | old_end_time | EndTime | datetime | 是 | DateTimeField |
| JobProdKind | old_job_prod_kind | JobProdKind | varchar；字节长度 50 | 是 | CharField |
| MachineID | old_machine_id | MachineID | varchar；字节长度 50 | 是 | CharField |
| ColorMatching | old_color_matching | ColorMatching | varchar；字节长度 50 | 是 | CharField |
| ZNum | old_znum | ZNum | int | 是 | IntegerField |
| JNum | old_jnum | JNum | int | 是 | IntegerField |
| JKg | old_jkg | JKg | float | 是 | FloatField |
| RNum | old_rnum | RNum | int | 是 | IntegerField |
| RTKg | old_rtkg | RTKg | float | 是 | FloatField |
| TNum | old_tnum | TNum | int | 是 | IntegerField |
| Rolls | old_rolls | Rolls | int | 是 | IntegerField |
| ClothQtyKg | old_cloth_qty_kg | ClothQtyKg | float | 是 | FloatField |
| NumNo | old_num_no | NumNo | varchar；字节长度 50 | 是 | CharField |
| ZKg | old_zkg | ZKg | float | 是 | FloatField |
| FBEmpID | old_fbemp_id | FBEmpID | varchar；字节长度 50 | 是 | CharField |
| StartTime | old_start_time | StartTime | datetime | 是 | DateTimeField |
| DTime | old_dtime | DTime | float | 是 | FloatField |
| JTimes | old_jtimes | JTimes | int | 是 | IntegerField |
| IsDown | old_is_down | IsDown | bit | 是 | BooleanField |
| dyeEmpID | old_dye_emp_id | dyeEmpID | varchar；字节长度 50 | 是 | CharField |
| dyeEmpName | old_dye_emp_name | dyeEmpName | varchar；字节长度 50 | 是 | CharField |
| ProcessID | old_process_id | ProcessID | varchar；字节长度 50 | 否 | CharField |
| ColorDepthID | old_color_depth_id | ColorDepthID | varchar；字节长度 50 | 是 | CharField |
| TMonth | old_tmonth | TMonth | varchar；字节长度 10 | 是 | CharField |
| AddNumber1 | old_add_number1 | AddNumber1 | int | 是 | IntegerField |
| AddNumber2 | old_add_number2 | AddNumber2 | int | 是 | IntegerField |
| WDNum | old_wdnum | WDNum | int | 是 | IntegerField |
| DefectClassID | old_defect_class_id | DefectClassID | varchar；字节长度 50 | 是 | CharField |
| DefectEmpID | old_defect_emp_id | DefectEmpID | varchar；字节长度 50 | 是 | CharField |

### SourceDyeInspectionLog — 质量检验与异常相关表（InspectionLog，待确认）

源表：`dye.InspectionLog`；新表：`src_dye_inspectionlog`；原主键：SheetSeries。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单号 | varchar；字节长度 20 | 是 | CharField |
| SheetDate | old_sheet_date | 巡检日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 巡检类型 | smallint | 是 | IntegerField |
| EmpID | old_emp_id | EmpID | varchar；字节长度 50 | 是 | CharField |
| InspectDetailNo | old_inspect_detail_no | InspectDetailNo | varchar；字节长度 50 | 是 | CharField |
| Inspector | old_inspector | 巡检人 | varchar；字节长度 20 | 是 | CharField |
| InspectorList | old_inspector_list | InspectorList | varchar；字节长度 200 | 是 | CharField |
| InspectDate | old_inspect_date | InspectDate | datetime | 是 | DateTimeField |
| InspectionSurvey | old_inspection_survey | 巡检概况 | nvarchar；字节长度 400 | 是 | CharField |
| Remarks | old_remarks | Remarks | nvarchar；字节长度 2000 | 是 | CharField |
| Creater | old_creater | 制单人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 制单日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| MachineID | old_machine_id | MachineID | varchar；字节长度 50 | 是 | CharField |
| MachineName | old_machine_name | MachineName | varchar；字节长度 50 | 是 | CharField |
| MachineLocation | old_machine_location | MachineLocation | varchar；字节长度 50 | 是 | CharField |

### SourceDyeInspectionLogDetail — 质量检验与异常相关表（InspectionLogDetail，待确认）

源表：`dye.InspectionLogDetail`；新表：`src_dye_inspectionlogdetail`；原主键：SheetSeries, DetailNo。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 否 | CharField |
| FaultSheetSeries | old_fault_sheet_series | 报修单流水号 | varchar；字节长度 20 | 是 | CharField |
| FaultSheetNo | old_fault_sheet_no | 报修单号 | varchar；字节长度 20 | 是 | CharField |
| FaultSheetDate | old_fault_sheet_date | 报修日期 | datetime | 是 | DateTimeField |
| FaultSheetKind | old_fault_sheet_kind | 报修类型 | varchar；字节长度 20 | 是 | CharField |
| MachineID | old_machine_id | 机台号 | varchar；字节长度 50 | 是 | CharField |
| EmpID | old_emp_id | 员工 | varchar；字节长度 50 | 是 | CharField |
| HappenTime | old_happen_time | 发生时间 | datetime | 是 | DateTimeField |
| ApplyTime | old_apply_time | 申请时间 | datetime | 是 | DateTimeField |
| DeptID | old_dept_id | 部门 | varchar；字节长度 20 | 是 | CharField |
| ShiftID | old_shift_id | 班别 | varchar；字节长度 20 | 是 | CharField |
| FaultID | old_fault_id | 故障 | nvarchar；字节长度 1024 | 是 | CharField |
| SeverityID | old_severity_id | 严重等级 | varchar；字节长度 20 | 是 | CharField |
| HandlerIDs | old_handler_ids | HandlerIDs | varchar；字节长度 100 | 是 | CharField |
| Handlers | old_handlers | Handlers | varchar；字节长度 100 | 是 | CharField |
| StartTime | old_start_time | 开始时间 | datetime | 是 | DateTimeField |
| EndTime | old_end_time | 结束时间 | datetime | 是 | DateTimeField |
| ResultID | old_result_id | 维修结果 | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | 审核日期 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 20 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | StepNo | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | PrintTimes | tinyint | 是 | IntegerField |
| Revisions | old_revisions | Revisions | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| HandleIdea | old_handle_idea | HandleIdea | varchar；字节长度 512 | 是 | CharField |
| PhotoAddress | old_photo_address | PhotoAddress | varchar；字节长度 512 | 是 | CharField |
| ApproveIdea | old_approve_idea | ApproveIdea | varchar；字节长度 200 | 是 | CharField |
| PatrolDetailNo | old_patrol_detail_no | PatrolDetailNo | varchar；字节长度 100 | 是 | CharField |
| SheetType | old_sheet_type | 报修类别 | varchar；字节长度 10 | 是 | CharField |
| StationID | old_station_id | 站别 | varchar；字节长度 30 | 是 | CharField |
| BusinessUnitID | old_business_unit_id | 经营单位 | varchar；字节长度 30 | 是 | CharField |
| FaultRemarks | old_fault_remarks | 报修备注 | varchar；字节长度 200 | 是 | CharField |
| MachineName | old_machine_name | MachineName | nvarchar；字节长度 128 | 是 | CharField |
| MachineLocation | old_machine_location | MachineLocation | nvarchar；字节长度 128 | 是 | CharField |
| Urgent | old_urgent | Urgent | int | 是 | IntegerField |
| FlowStatus | old_flow_status | FlowStatus | nvarchar；字节长度 40 | 是 | CharField |

关联 `source_parent_1` → `erp_quality.SourceDyeInspectionLog`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 InspectionLogDetail → InspectionLog。

### SourceDyeInspectionProject — 质量检验与异常相关表（InspectionProject，待确认）

源表：`dye.InspectionProject`；新表：`src_dye_inspectionproject`；原主键：SheetSeries, DetailNo。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | SheetSeries | varchar；字节长度 20 | 否 | CharField |
| DetailNo | old_detail_no | DetailNo | varchar；字节长度 36 | 否 | CharField |
| SortNo | old_sort_no | SortNo | int | 是 | IntegerField |
| SerialNum | old_serial_num | SerialNum | nvarchar；字节长度 20 | 是 | CharField |
| ProjectInfo | old_project_info | ProjectInfo | nvarchar；字节长度 400 | 是 | CharField |
| Value | old_value | Value | nvarchar；字节长度 200 | 是 | CharField |
| DefaultValue | old_default_value | DefaultValue | nvarchar；字节长度 200 | 是 | CharField |
| Remarks | old_remarks | Remarks | varchar；字节长度 512 | 是 | CharField |
| CaseDetailNo | old_case_detail_no | CaseDetailNo | varchar；字节长度 36 | 是 | CharField |
| Result | old_result | Result | int | 是 | IntegerField |
| IsInputText | old_is_input_text | IsInputText | bit | 是 | BooleanField |

### SourceDyePTestItem — 质量检验与异常相关表（p_TestItem，待确认）

源表：`dye.p_TestItem`；新表：`src_dye_p_testitem`；原主键：ItemID。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| ItemID | old_item_id | ItemID | varchar；字节长度 10 | 否 | CharField |
| ItemName | old_item_name | ItemName | varchar；字节长度 50 | 是 | CharField |
| FieldType | old_field_type | FieldType | tinyint | 是 | IntegerField |
| UnitStr | old_unit_str | UnitStr | varchar；字节长度 6 | 是 | CharField |
| Standard | old_standard | Standard | varchar；字节长度 50 | 是 | CharField |
| SortNo | old_sort_no | SortNo | smallint | 是 | IntegerField |
| IsStop | old_is_stop | IsStop | bit | 是 | BooleanField |
| Description | old_description | Description | varchar；字节长度 100 | 是 | CharField |

### SourceDyeProdTest — 质量检验与异常相关表（ProdTest，待确认）

源表：`dye.ProdTest`；新表：`src_dye_prodtest`；原主键：SheetSeries。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 表单编号 | varchar；字节长度 36 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | 单据类型 | smallint | 是 | IntegerField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 50 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 150 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 200 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 200 | 是 | CharField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 50 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 100 | 是 | CharField |
| Weight | old_weight | 克重 | decimal(6,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量数量 | decimal(10,2) | 是 | DecimalField |
| LengthQty | old_length_qty | 长度数量 | decimal(10,2) | 是 | DecimalField |
| ShiftID | old_shift_id | 班组代码 | varchar；字节长度 50 | 是 | CharField |
| Maker | old_maker | 测试人 | varchar；字节长度 50 | 是 | CharField |
| CheckResult | old_check_result | 检测意见 | varchar；字节长度 100 | 是 | CharField |
| ItemID01 | old_item_id01 | 测试项目01 | varchar；字节长度 10 | 是 | CharField |
| ItemName01 | old_item_name01 | 测试项目名称1 | varchar；字节长度 50 | 是 | CharField |
| Value01 | old_value01 | 标准值01 | varchar；字节长度 20 | 是 | CharField |
| ItemID02 | old_item_id02 | 测试项目02 | varchar；字节长度 10 | 是 | CharField |
| ItemName02 | old_item_name02 | 测试项目名称2 | varchar；字节长度 50 | 是 | CharField |
| Value02 | old_value02 | 标准值02 | varchar；字节长度 20 | 是 | CharField |
| ItemID03 | old_item_id03 | 测试项目03 | varchar；字节长度 10 | 是 | CharField |
| ItemName03 | old_item_name03 | 测试项目名称3 | varchar；字节长度 50 | 是 | CharField |
| Value03 | old_value03 | 标准值03 | varchar；字节长度 20 | 是 | CharField |
| ItemID04 | old_item_id04 | 测试项目04 | varchar；字节长度 10 | 是 | CharField |
| ItemName04 | old_item_name04 | 测试项目名称4 | varchar；字节长度 50 | 是 | CharField |
| Value04 | old_value04 | 标准值04 | varchar；字节长度 20 | 是 | CharField |
| ItemID05 | old_item_id05 | 测试项目05 | varchar；字节长度 10 | 是 | CharField |
| ItemName05 | old_item_name05 | ItemName05 | varchar；字节长度 50 | 是 | CharField |
| Value05 | old_value05 | 标准值05 | varchar；字节长度 20 | 是 | CharField |
| ItemID06 | old_item_id06 | 测试项目06 | varchar；字节长度 10 | 是 | CharField |
| ItemName06 | old_item_name06 | ItemName06 | varchar；字节长度 50 | 是 | CharField |
| Value06 | old_value06 | 标准值06 | varchar；字节长度 20 | 是 | CharField |
| ItemID07 | old_item_id07 | 测试项目07 | varchar；字节长度 10 | 是 | CharField |
| ItemName07 | old_item_name07 | ItemName07 | varchar；字节长度 50 | 是 | CharField |
| Value07 | old_value07 | 标准值07 | varchar；字节长度 20 | 是 | CharField |
| ItemID08 | old_item_id08 | 测试项目08 | varchar；字节长度 10 | 是 | CharField |
| ItemName08 | old_item_name08 | ItemName08 | varchar；字节长度 50 | 是 | CharField |
| Value08 | old_value08 | 标准值08 | varchar；字节长度 20 | 是 | CharField |
| ItemID09 | old_item_id09 | 测试项目09 | varchar；字节长度 10 | 是 | CharField |
| ItemName09 | old_item_name09 | ItemName09 | varchar；字节长度 50 | 是 | CharField |
| Value09 | old_value09 | 标准值09 | varchar；字节长度 20 | 是 | CharField |
| ItemID10 | old_item_id10 | 测试项目10 | varchar；字节长度 10 | 是 | CharField |
| ItemName10 | old_item_name10 | ItemName10 | varchar；字节长度 50 | 是 | CharField |
| Value10 | old_value10 | 标准值10 | varchar；字节长度 20 | 是 | CharField |
| ItemID11 | old_item_id11 | 测试项目11 | varchar；字节长度 10 | 是 | CharField |
| ItemName11 | old_item_name11 | ItemName11 | varchar；字节长度 50 | 是 | CharField |
| Value11 | old_value11 | 标准值11 | varchar；字节长度 500 | 是 | CharField |
| ItemID12 | old_item_id12 | 测试项目12 | varchar；字节长度 10 | 是 | CharField |
| ItemName12 | old_item_name12 | ItemName12 | varchar；字节长度 50 | 是 | CharField |
| Value12 | old_value12 | 标准值12 | varchar；字节长度 20 | 是 | CharField |
| ItemID13 | old_item_id13 | 测试项目13 | varchar；字节长度 10 | 是 | CharField |
| ItemName13 | old_item_name13 | ItemName13 | varchar；字节长度 50 | 是 | CharField |
| Value13 | old_value13 | 标准值13 | varchar；字节长度 20 | 是 | CharField |
| ItemID14 | old_item_id14 | 测试项目14 | varchar；字节长度 10 | 是 | CharField |
| ItemName14 | old_item_name14 | ItemName14 | varchar；字节长度 50 | 是 | CharField |
| Value14 | old_value14 | 标准值14 | varchar；字节长度 20 | 是 | CharField |
| ItemID15 | old_item_id15 | 测试项目15 | varchar；字节长度 10 | 是 | CharField |
| ItemName15 | old_item_name15 | ItemName15 | varchar；字节长度 50 | 是 | CharField |
| Value15 | old_value15 | 标准值15 | varchar；字节长度 20 | 是 | CharField |
| ItemID16 | old_item_id16 | 测试项目16 | varchar；字节长度 10 | 是 | CharField |
| ItemName16 | old_item_name16 | ItemName16 | varchar；字节长度 50 | 是 | CharField |
| Value16 | old_value16 | 标准值16 | varchar；字节长度 20 | 是 | CharField |
| ItemID17 | old_item_id17 | 测试项目17 | varchar；字节长度 10 | 是 | CharField |
| ItemName17 | old_item_name17 | ItemName17 | varchar；字节长度 50 | 是 | CharField |
| Value17 | old_value17 | 标准值17 | varchar；字节长度 20 | 是 | CharField |
| ItemID18 | old_item_id18 | 测试项目18 | varchar；字节长度 10 | 是 | CharField |
| ItemName18 | old_item_name18 | ItemName18 | varchar；字节长度 50 | 是 | CharField |
| Value18 | old_value18 | 标准值18 | varchar；字节长度 20 | 是 | CharField |
| ItemID19 | old_item_id19 | 测试项目19 | varchar；字节长度 10 | 是 | CharField |
| ItemName19 | old_item_name19 | ItemName19 | varchar；字节长度 50 | 是 | CharField |
| Value19 | old_value19 | 标准值19 | varchar；字节长度 20 | 是 | CharField |
| ItemID20 | old_item_id20 | 测试项目20 | varchar；字节长度 10 | 是 | CharField |
| ItemName20 | old_item_name20 | ItemName20 | varchar；字节长度 50 | 是 | CharField |
| Value20 | old_value20 | 标准值20 | varchar；字节长度 20 | 是 | CharField |
| ItemID21 | old_item_id21 | 测试项目21 | varchar；字节长度 10 | 是 | CharField |
| ItemName21 | old_item_name21 | ItemName21 | varchar；字节长度 50 | 是 | CharField |
| Value21 | old_value21 | 标准值21 | varchar；字节长度 20 | 是 | CharField |
| ItemID22 | old_item_id22 | 测试项目22 | varchar；字节长度 10 | 是 | CharField |
| ItemName22 | old_item_name22 | ItemName22 | varchar；字节长度 50 | 是 | CharField |
| Value22 | old_value22 | 标准值22 | varchar；字节长度 20 | 是 | CharField |
| ItemID23 | old_item_id23 | 测试项目23 | varchar；字节长度 10 | 是 | CharField |
| ItemName23 | old_item_name23 | ItemName23 | varchar；字节长度 50 | 是 | CharField |
| Value23 | old_value23 | 标准值23 | varchar；字节长度 20 | 是 | CharField |
| ItemID24 | old_item_id24 | 测试项目24 | varchar；字节长度 10 | 是 | CharField |
| ItemName24 | old_item_name24 | ItemName24 | varchar；字节长度 50 | 是 | CharField |
| Value24 | old_value24 | 标准值24 | varchar；字节长度 20 | 是 | CharField |
| ItemID25 | old_item_id25 | 测试项目25 | varchar；字节长度 10 | 是 | CharField |
| ItemName25 | old_item_name25 | ItemName25 | varchar；字节长度 50 | 是 | CharField |
| Value25 | old_value25 | 标准值25 | varchar；字节长度 20 | 是 | CharField |
| ItemID26 | old_item_id26 | 测试项目26 | varchar；字节长度 10 | 是 | CharField |
| ItemName26 | old_item_name26 | ItemName26 | varchar；字节长度 50 | 是 | CharField |
| Value26 | old_value26 | 标准值26 | varchar；字节长度 20 | 是 | CharField |
| ItemID27 | old_item_id27 | 测试项目27 | varchar；字节长度 10 | 是 | CharField |
| ItemName27 | old_item_name27 | ItemName27 | varchar；字节长度 50 | 是 | CharField |
| Value27 | old_value27 | 标准值27 | varchar；字节长度 20 | 是 | CharField |
| ItemID28 | old_item_id28 | 测试项目28 | varchar；字节长度 10 | 是 | CharField |
| ItemName28 | old_item_name28 | ItemName28 | varchar；字节长度 50 | 是 | CharField |
| Value28 | old_value28 | 标准值28 | varchar；字节长度 20 | 是 | CharField |
| ItemID29 | old_item_id29 | 测试项目29 | varchar；字节长度 10 | 是 | CharField |
| ItemName29 | old_item_name29 | 测试项目名称29 | varchar；字节长度 50 | 是 | CharField |
| Value29 | old_value29 | 标准值29 | varchar；字节长度 20 | 是 | CharField |
| ItemID30 | old_item_id30 | 测试项目30 | varchar；字节长度 10 | 是 | CharField |
| ItemName30 | old_item_name30 | ItemName30 | varchar；字节长度 50 | 是 | CharField |
| Value30 | old_value30 | 标准值30 | varchar；字节长度 20 | 是 | CharField |
| ItemID31 | old_item_id31 | 测试项目31 | varchar；字节长度 10 | 是 | CharField |
| ItemName31 | old_item_name31 | ItemName31 | varchar；字节长度 50 | 是 | CharField |
| Value31 | old_value31 | 标准值31 | varchar；字节长度 20 | 是 | CharField |
| ItemID32 | old_item_id32 | 测试项目32 | varchar；字节长度 10 | 是 | CharField |
| ItemName32 | old_item_name32 | 测试项目名称32 | varchar；字节长度 50 | 是 | CharField |
| Value32 | old_value32 | 标准值32 | varchar；字节长度 20 | 是 | CharField |
| ItemID33 | old_item_id33 | 测试项目33 | varchar；字节长度 10 | 是 | CharField |
| ItemName33 | old_item_name33 | 测试项目名称33 | varchar；字节长度 50 | 是 | CharField |
| Value33 | old_value33 | 标准值33 | varchar；字节长度 20 | 是 | CharField |
| ItemID34 | old_item_id34 | 测试项目34 | varchar；字节长度 10 | 是 | CharField |
| ItemName34 | old_item_name34 | 测试项目名称34 | varchar；字节长度 50 | 是 | CharField |
| Value34 | old_value34 | 标准值34 | varchar；字节长度 20 | 是 | CharField |
| ItemID35 | old_item_id35 | 测试项目35 | varchar；字节长度 10 | 是 | CharField |
| ItemName35 | old_item_name35 | 测试项目名称35 | varchar；字节长度 50 | 是 | CharField |
| Value35 | old_value35 | 标准值35 | varchar；字节长度 20 | 是 | CharField |
| ItemID36 | old_item_id36 | 测试项目36 | varchar；字节长度 10 | 是 | CharField |
| ItemName36 | old_item_name36 | 测试项目名称36 | varchar；字节长度 50 | 是 | CharField |
| Value36 | old_value36 | 标准值36 | varchar；字节长度 20 | 是 | CharField |
| ItemID37 | old_item_id37 | 测试项目37 | varchar；字节长度 10 | 是 | CharField |
| ItemName37 | old_item_name37 | 测试项目名称37 | varchar；字节长度 50 | 是 | CharField |
| Value37 | old_value37 | 标准值37 | varchar；字节长度 20 | 是 | CharField |
| ItemID38 | old_item_id38 | 测试项目38 | varchar；字节长度 10 | 是 | CharField |
| ItemName38 | old_item_name38 | 测试项目名称38 | varchar；字节长度 50 | 是 | CharField |
| Value38 | old_value38 | 加色类别 | varchar；字节长度 20 | 是 | CharField |
| ItemID39 | old_item_id39 | 测试项目39 | varchar；字节长度 10 | 是 | CharField |
| ItemName39 | old_item_name39 | 测试项目名称39 | varchar；字节长度 50 | 是 | CharField |
| Value39 | old_value39 | 机台 | varchar；字节长度 20 | 是 | CharField |
| ItemID40 | old_item_id40 | 测试项目40 | varchar；字节长度 10 | 是 | CharField |
| ItemName40 | old_item_name40 | 测试项目名称40 | varchar；字节长度 50 | 是 | CharField |
| Value40 | old_value40 | 染程 | varchar；字节长度 20 | 是 | CharField |
| SheetStatus | old_sheet_status | 单据状态 | smallint | 是 | IntegerField |
| StepNo | old_step_no | 流程节点号 | tinyint | 是 | IntegerField |
| PrintTimes | old_print_times | 打印次数 | tinyint | 是 | IntegerField |
| Revisions | old_revisions | 修改次数 | smallint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| EmpID | old_emp_id | 责任人 | varchar；字节长度 20 | 是 | CharField |
| DeptID | old_dept_id | DeptID | varchar；字节长度 50 | 是 | CharField |
| CheckNo | old_check_no | 检测单号 | varchar；字节长度 30 | 是 | CharField |
| StuffID | old_stuff_id | 样品名称 | varchar；字节长度 10 | 是 | CharField |
| CompareStuffID | old_compare_stuff_id | 对比名称 | varchar；字节长度 10 | 是 | CharField |
| SupplierID | old_supplier_id | 样品供方 | varchar；字节长度 10 | 是 | CharField |
| CompareSupplierID | old_compare_supplier_id | 对比供方 | varchar；字节长度 10 | 是 | CharField |
| CompareLotNo | old_compare_lot_no | 对比批号 | varchar；字节长度 100 | 是 | CharField |

### SourceDyeQualityAccident — 质量检验与异常相关表（QualityAccident，待确认）

源表：`dye.QualityAccident`；新表：`src_dye_qualityaccident`；原主键：SheetSeries。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 单据流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单据号 | varchar；字节长度 50 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 200 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 500 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 200 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 200 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 20 | 是 | CharField |
| Weight | old_weight | 克重 | varchar；字节长度 200 | 是 | CharField |
| Width | old_width | 幅宽 | varchar；字节长度 200 | 是 | CharField |
| SumAssignedWeightQty | old_sum_assigned_weight_qty | 实发数量 | decimal(10,2) | 是 | DecimalField |
| SumAssignedRolls | old_sum_assigned_rolls | 实发粒数 | decimal(10,2) | 是 | DecimalField |
| QualityDescription | old_quality_description | 质量描述 | varchar；字节长度 512 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| DepartMent | old_depart_ment | 责任部门 | varchar；字节长度 10 | 是 | CharField |
| Suggestion | old_suggestion | 处理意见 | varchar；字节长度 512 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |

### SourceDyeQualityDeduction — 质量检验与异常相关表（QualityDeduction，待确认）

源表：`dye.QualityDeduction`；新表：`src_dye_qualitydeduction`；原主键：SheetSeries。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 单据流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetNo | old_sheet_no | 单据号 | varchar；字节长度 50 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetKind | old_sheet_kind | SheetKind | smallint | 是 | IntegerField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 200 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 500 | 是 | CharField |
| CustSelfProduct | old_cust_self_product | 客户规格 | varchar；字节长度 50 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 200 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 200 | 是 | CharField |
| CustColorNum | old_cust_color_num | 客户色号 | varchar；字节长度 20 | 是 | CharField |
| Weight | old_weight | 克重 | varchar；字节长度 200 | 是 | CharField |
| Width | old_width | 幅宽 | varchar；字节长度 200 | 是 | CharField |
| SumAssignedWeightQty | old_sum_assigned_weight_qty | 实发数量 | decimal(10,2) | 是 | DecimalField |
| SumAssignedRolls | old_sum_assigned_rolls | 实发粒数 | decimal(10,2) | 是 | DecimalField |
| QualityDescription | old_quality_description | 质量描述 | varchar；字节长度 512 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| DepartMent | old_depart_ment | 责任部门 | varchar；字节长度 10 | 是 | CharField |
| DeductionMoney | old_deduction_money | 扣罚金额 | decimal(10,2) | 是 | DecimalField |
| AccidentPerson | old_accident_person | 责任人 | varchar；字节长度 10 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| LSheetSeries | old_lsheet_series | LSheetSeries | varchar；字节长度 32 | 是 | CharField |

### SourceDyeQualityRegister — 质量检验与异常相关表（QualityRegister，待确认）

源表：`dye.QualityRegister`；新表：`src_dye_qualityregister`；原主键：SheetSeries, AutoID。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 登记号 | varchar；字节长度 20 | 否 | CharField |
| SheetDate | old_sheet_date | 登记时间 | datetime | 是 | DateTimeField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | 客户 | varchar；字节长度 10 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 20 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 20 | 是 | CharField |
| ColorID | old_color_id | 颜色 | varchar；字节长度 20 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| WeightQty | old_weight_qty | 重量 | decimal(10,2) | 是 | DecimalField |
| Reason | old_reason | 原因 | nvarchar；字节长度 1024 | 是 | CharField |
| ShiftID | old_shift_id | 班组 | varchar；字节长度 20 | 是 | CharField |
| ProcessMethod | old_process_method | 处理方法 | nvarchar；字节长度 1024 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 1024 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 10 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| RightStatus | old_right_status | 状态 | smallint | 是 | IntegerField |
| AutoID | old_auto_id | 流水号 | varchar；字节长度 50 | 否 | CharField |
| EmpID | old_emp_id | 员工 | varchar；字节长度 10 | 是 | CharField |
| Description1 | old_description1 | Description1 | nvarchar；字节长度 1000 | 是 | CharField |
| Description2 | old_description2 | Description2 | nvarchar；字节长度 1000 | 是 | CharField |

### SourceDyeRecordDefect — 质量检验与异常相关表（RecordDefect，待确认）

源表：`dye.RecordDefect`；新表：`src_dye_recorddefect`；原主键：BarCode, DefectNo。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| BarCode | old_bar_code | 条码 | varchar；字节长度 20 | 否 | CharField |
| DefectNo | old_defect_no | 疵点顺序 | smallint | 否 | IntegerField |
| DefectID | old_defect_id | 疵点编码 | varchar；字节长度 10 | 是 | CharField |
| StartPos | old_start_pos | 开始位置 | decimal(8,2) | 是 | DecimalField |
| EndPos | old_end_pos | 结束位置 | decimal(8,2) | 是 | DecimalField |
| Speed | old_speed | 速度 | decimal(8,2) | 是 | DecimalField |
| IsContinuity | old_is_continuity | 是否连续疵点 | bit | 是 | BooleanField |
| IsRepairable | old_is_repairable | 是否可重修 | bit | 是 | BooleanField |
| Dots | old_dots | 疵点类型名称 | smallint | 是 | IntegerField |
| Times | old_times | 状态 | smallint | 是 | IntegerField |
| Qty | old_qty | 数量 | decimal(10,2) | 是 | DecimalField |
| Status | old_status | 疵点状态 | varchar；字节长度 1 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| LotNo | old_lot_no | LotNo | varchar；字节长度 50 | 是 | CharField |
| DefectGroupID | old_defect_group_id | 疵点类别 | varchar；字节长度 10 | 是 | CharField |
| CUTQTY | old_cutqty | CUTQTY | decimal(10,1) | 是 | DecimalField |
| DefectDot | old_defect_dot | 疵点分数 | varchar；字节长度 30 | 是 | CharField |
| SumDots | old_sum_dots | 疵点总扣分 | decimal(8,2) | 是 | DecimalField |
| BarCodeRollNo | old_bar_code_roll_no | 细码条码 | varchar；字节长度 20 | 是 | CharField |
| StatusDescription | old_status_description | 状态说明 | varchar；字节长度 50 | 是 | CharField |
| DefectType | old_defect_type | DefectType | varchar；字节长度 30 | 是 | CharField |

关联 `source_parent_1` → `erp_warehouse.SourceDyeRecordYield`；原码 `BarCode` → 父表原码 `Guid`；依据：原界面主从 QueryRecordDefect → QueryRecord。

### SourceDyeTestDetail — 质量检验与异常相关表（Test_Detail，待确认）

源表：`dye.Test_Detail`；新表：`src_dye_test_detail`；原主键：SheetSeries, DetailNo。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 50 | 否 | CharField |
| DetailNo | old_detail_no | 行号 | varchar；字节长度 50 | 否 | CharField |
| ColorID | old_color_id | 颜色号 | varchar；字节长度 50 | 是 | CharField |
| ColorNum | old_color_num | 颜色代码 | varchar；字节长度 50 | 是 | CharField |
| Remarks | old_remarks | 备注 | varchar；字节长度 -1 | 是 | TextField |

关联 `source_parent_1` → `erp_quality.SourceDyeTestMain`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 Test_Detail → Test_Main。

### SourceDyeTestMain — 质量检验与异常相关表（Test_Main，待确认）

源表：`dye.Test_Main`；新表：`src_dye_test_main`；原主键：SheetSeries。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 流水号 | varchar；字节长度 50 | 否 | CharField |
| CustomerID | old_customer_id | 客户名 | varchar；字节长度 50 | 是 | CharField |
| SalerID | old_saler_id | 业务员 | varchar；字节长度 50 | 是 | CharField |
| Remarks | old_remarks | 备注 | nvarchar；字节长度 -1 | 是 | TextField |

### SourceDyeWDefect — 质量检验与异常相关表（WDefect，待确认）

源表：`dye.WDefect`；新表：`src_dye_wdefect`；原主键：SheetSeries。

归属依据：目录业务域候选；用途可继续核实，字段已建模。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| SheetType | old_sheet_type | 类型 | smallint | 是 | IntegerField |
| SheetDate | old_sheet_date | 单据日期 | datetime | 是 | DateTimeField |
| SheetNo | old_sheet_no | 检验单号 | varchar；字节长度 36 | 是 | CharField |
| WDefectNo | old_wdefect_no | 质量流水号 | varchar；字节长度 20 | 是 | CharField |
| WProcessNo | old_wprocess_no | 刷卡流水号 | varchar；字节长度 20 | 是 | CharField |
| JobSheetNo | old_job_sheet_no | 缸号 | varchar；字节长度 50 | 是 | CharField |
| CustomerID | old_customer_id | 客户代码 | varchar；字节长度 50 | 是 | CharField |
| DetailCustName | old_detail_cust_name | 明细客户 | varchar；字节长度 150 | 是 | CharField |
| ColorID | old_color_id | 颜色编码 | varchar；字节长度 250 | 是 | CharField |
| ColorNum | old_color_num | 色号 | varchar；字节长度 100 | 是 | CharField |
| ProdID | old_prod_id | 本厂规格 | varchar；字节长度 50 | 是 | CharField |
| Spec | old_spec | 规格 | varchar；字节长度 200 | 是 | CharField |
| LotNo | old_lot_no | 批号 | varchar；字节长度 200 | 是 | CharField |
| Kind | old_kind | 类别 | varchar；字节长度 10 | 是 | CharField |
| MachineID | old_machine_id | 机台号 | varchar；字节长度 10 | 是 | CharField |
| DefectIDs | old_defect_ids | 疵点代码 | varchar；字节长度 -1 | 是 | TextField |
| Defects | old_defects | 疵点 | varchar；字节长度 100 | 是 | CharField |
| DefectDate | old_defect_date | 出疵时间 | datetime | 是 | DateTimeField |
| DefectDept | old_defect_dept | 责任部门 | varchar；字节长度 30 | 是 | CharField |
| DefectRolls | old_defect_rolls | 疵品粒数 | decimal(10,2) | 是 | DecimalField |
| DefectQty | old_defect_qty | 疵品数量 | decimal(10,2) | 是 | DecimalField |
| DefectLengthQty | old_defect_length_qty | 疵品长度 | decimal(10,2) | 是 | DecimalField |
| DefectShiftID | old_defect_shift_id | 出疵班组 | varchar；字节长度 10 | 是 | CharField |
| DefectEmpID | old_defect_emp_id | 出疵员工 | varchar；字节长度 20 | 是 | CharField |
| DefectProcessID | old_defect_process_id | 出疵工序 | varchar；字节长度 50 | 是 | CharField |
| AwardMoney | old_award_money | 奖金 | decimal(10,2) | 是 | DecimalField |
| ProcessNo | old_process_no | 工序号 | tinyint | 是 | IntegerField |
| ProcessID | old_process_id | 工序 | varchar；字节长度 10 | 是 | CharField |
| ShiftID | old_shift_id | 班组 | varchar；字节长度 10 | 是 | CharField |
| EmpID | old_emp_id | 员工 | varchar；字节长度 50 | 是 | CharField |
| Signer | old_signer | 签核人姓名 | varchar；字节长度 10 | 是 | CharField |
| SignedDate | old_signed_date | 签核日期 | datetime | 是 | DateTimeField |
| Status | old_status | 评定状态 | tinyint | 是 | IntegerField |
| Remarks | old_remarks | 备注 | varchar；字节长度 512 | 是 | CharField |
| StationID | old_station_id | 站别 | varchar；字节长度 10 | 是 | CharField |
| DefectStationID | old_defect_station_id | 出疵站别 | varchar；字节长度 50 | 是 | CharField |
| CheckDesc | old_check_desc | 初判 | varchar；字节长度 80 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建时间 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改时间 | datetime | 是 | DateTimeField |
| Approver | old_approver | 审核人 | varchar；字节长度 20 | 是 | CharField |
| ApproveDate | old_approve_date | 审核时间 | datetime | 是 | DateTimeField |
| Approved | old_approved | 已审核 | bit | 是 | BooleanField |
| FromRolls | old_from_rolls | 检验粒数 | decimal(7,2) | 是 | DecimalField |
| FromWeightQty | old_from_weight_qty | 检验重量 | decimal(10,2) | 是 | DecimalField |
| FromLengthQty | old_from_length_qty | 检验长度 | decimal(10,2) | 是 | DecimalField |
| Result | old_result | 评审结果 | varchar；字节长度 2000 | 是 | CharField |
| KindType | old_kind_type | 责任类别 | varchar；字节长度 10 | 是 | CharField |
| DefectKind | old_defect_kind | 质量问题 | varchar；字节长度 50 | 是 | CharField |
| DefectType | old_defect_type | 质量类型 | varchar；字节长度 20 | 是 | CharField |
| DefectFactory | old_defect_factory | 工厂分类 | varchar；字节长度 50 | 是 | CharField |
| DefectClassID | old_defect_class_id | DefectClassID | varchar；字节长度 50 | 是 | CharField |
| QCCD | old_qccd | 质检问题 | varchar；字节长度 150 | 是 | CharField |
| PiSheWenTi | old_pi_she_wen_ti | 批色问题 | varchar；字节长度 50 | 是 | CharField |
| Outputdeduction | old_outputdeduction | 产量扣除% | decimal(10,2) | 是 | DecimalField |

### SourceDyeWDefectPenalty — 旧质量责任及扣奖明细

源表：`dye.WDefectPenalty`；新表：`src_dye_wdefectpenalty`；原主键：SheetSeries, RowNo。

归属依据：原表包含疵点编号、责任类别、员工、件数及数量，归入质量责任业务；保留扣奖原值，不执行工资核算。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| SheetSeries | old_sheet_series | 表单流水号 | varchar；字节长度 20 | 否 | CharField |
| WDefectNo | old_wdefect_no | 质量流水号 | varchar；字节长度 20 | 是 | CharField |
| RowNo | old_row_no | 行号 | smallint | 否 | IntegerField |
| DutyKind | old_duty_kind | 责任类型 | varchar；字节长度 1 | 是 | CharField |
| EmpID | old_emp_id | 员工编号 | varchar；字节长度 50 | 是 | CharField |
| Name | old_name | 名称 | varchar；字节长度 60 | 是 | CharField |
| Rolls | old_rolls | 粒数 | decimal(7,2) | 是 | DecimalField |
| Qty | old_qty | 扣数量 | decimal(10,2) | 是 | DecimalField |
| Penalty | old_penalty | 扣款 | decimal(10,2) | 是 | DecimalField |
| Reward | old_reward | 奖励 | decimal(10,2) | 是 | DecimalField |
| Remarks | old_remarks | 备注 | varchar；字节长度 100 | 是 | CharField |
| SheetDate | old_sheet_date | SheetDate | datetime | 是 | DateTimeField |

关联 `source_parent_1` → `erp_quality.SourceDyeWDefect`；原码 `SheetSeries` → 父表原码 `SheetSeries`；依据：原界面主从 WDefectPenaltyOther → WDefectJudgeOther；原界面主从 WDefectPenaltyInterior → WDefectJudgeInterior；原界面主从 WDefectOtherDetail → WDefectOther；原界面主从 WDefectPayoutsDetail → WDefectPayouts；原界面主从 WDefectPenaltyBack → WDefectJudgeBack。

关联 `source_parent_2` → `erp_quality.SourceDyeWDefect`；原码 `WDefectNo` → 父表原码 `WDefectNo`；依据：原界面主从 WDefectPenalty → WDefect。

### SourceDyeZhijianwenti — 其他或待确认相关表（zhijianwenti，待确认）

源表：`dye.zhijianwenti`；新表：`src_dye_zhijianwenti`；原主键：FieldType, Code。

归属依据：明确质量/检验来源。

| 原列 | Django字段 | 中文标题 | 原类型/长度/精度 | 原表可空 | Django类型 |
|---|---|---|---|---|---|
| FieldType | old_field_type | 数据类型 | varchar；字节长度 20 | 否 | CharField |
| Code | old_code | 编码 | varchar；字节长度 20 | 否 | CharField |
| Name | old_name | 名称 | varchar；字节长度 100 | 否 | CharField |
| Mnemonic | old_mnemonic | 助记符 | varchar；字节长度 100 | 是 | CharField |
| NumValue | old_num_value | 数值值 | numeric(18,6) | 是 | DecimalField |
| SortValue | old_sort_value | 排序值 | smallint | 是 | IntegerField |
| DefectFactory | old_defect_factory | 工厂分类 | varchar；字节长度 100 | 是 | CharField |
| Reserved1 | old_reserved1 | 保留值1 | varchar；字节长度 1000 | 是 | CharField |
| Reserved2 | old_reserved2 | 保留值2 | varchar；字节长度 100 | 是 | CharField |
| Reserved3 | old_reserved3 | 保留值3 | varchar；字节长度 100 | 是 | CharField |
| Reserved4 | old_reserved4 | 保留值4 | varchar；字节长度 100 | 是 | CharField |
| Reserved5 | old_reserved5 | 保留值5 | varchar；字节长度 100 | 是 | CharField |
| StopDate | old_stop_date | 停用时间 | datetime | 是 | DateTimeField |
| ParentCode | old_parent_code | 父级代码 | varchar；字节长度 10 | 是 | CharField |
| Creater | old_creater | 创建人 | varchar；字节长度 10 | 是 | CharField |
| CreateDate | old_create_date | 创建日期 | datetime | 是 | DateTimeField |
| Modifyer | old_modifyer | 修改人 | varchar；字节长度 10 | 是 | CharField |
| ModifyDate | old_modify_date | 修改日期 | datetime | 是 | DateTimeField |
| IsStop | old_is_stop | 是否停用 | bit | 是 | BooleanField |
| BusinessUnitID | old_business_unit_id | BusinessUnitID | varchar；字节长度 20 | 是 | CharField |
| NumValueNo | old_num_value_no | NumValueNo | int | 是 | IntegerField |
| CustomerID | old_customer_id | CustomerID | varchar；字节长度 20 | 是 | CharField |
| Kind_01 | old_kind_01 | 异常分类 | varchar；字节长度 100 | 是 | CharField |
| Kind_02 | old_kind_02 | Kind_02 | varchar；字节长度 100 | 是 | CharField |
