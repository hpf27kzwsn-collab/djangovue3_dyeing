# 第50至54批 Windows 复刻整改与验收

更新：2026-10-10T16:02:00.362623+08:00。第十轮确认的6组问题已按批修正并复验，正式8000已发布，版本 **1.0.0.1791618793779**，迁移 **0019_windows_parity_cleanup**。另外清理Role.admin及未实现登录方式标签。原项目目录未改；移动/mac与人工场景按用户要求跳过。

## 1. 改动及关联验收

| 批次 | 问题 | 最终行为与证据 |
| --- | --- | --- |
| 50 | TW-DP03、TW-A01 | 用户名普通CharField150/unique，不继承UnicodeUsernameValidator；两种管理员重置不清零pwd_change_count。新增5个实际Django/SQLite测试覆盖API创建、修改、登录、150长度/唯一、openpyxl模板导入更新、JSON初始化重复导入以及原计数0/4保留。旧test_reaudit断言从0改为4，因为改前断言验证的是本轮确认的错误行为；没有删除/跳过该用例。 |
| 51 | TW-UI01、TW-UI02 | 文件选择器增加页大小及limit请求，不加任意分页封顶；图片实际20行/总36及50行上限显示36、文件30行/总44，跨页选2项保持。标签按移除前索引进入右邻/最后项，保留fullPath/query、首页固定及缓存；非当前关闭保持当前页面。 |
| 52 | TW-UI03、TW-UI04 | 部门概况和两图由一个状态整体折叠；恢复按钮留在概况外，恢复重新挂载图表，含下级状态不丢。折叠前列表top614、后398；恢复两SVG。日志只隐藏UI删除入口，不改原有后端CRUD权限语义；两个页面详情/查询/导出实际操作，导出xlsx用openpyxl打开核对，分别1和13条。 |
| 53 | 无接线字段/选项 | 全部业务源码、示例及前端未消费AdminPermission；唯一另一个Role.admin使用在init_data默认值，已一并删除。迁移只清理system.Role/admin定义及其关联授权；普通admin角色、成员、菜单/按钮/其他字段授权仍保留。登录方式只展示已接入的账号密码，历史日志值不批量改写。 |
| 54 | 回归、打包与正式发布 | 默认配置102项：88通过、14扩展配置跳过；完整扩展配置106项全部通过。两套有重叠，不能相加当208独立场景。前端类型/构建通过，候选及正式包健康/版本/文件摘要/外键/数据保留检查通过。 |

## 2. 防御性编程与取舍

本批移除了已确认的额外用户名字符限制，没有新增任意字符白名单、文件大小/行数上限、分页封顶、密码复杂度、重试或吞异常。150长度/账号唯一、认证授权、xlsx格式和真实字段错误仍属于模型与功能本身。没有恢复原新增/修改接口额外50长度缩短。

没有为了兼容保留无用途Role.admin字段或给未来ERP增加占位功能。停用角色一致性、多角色数据并集修正、REST/模型/元数据等30条既定契约差异仍公开保留，**本次已知待改D=0不代表所有内容与旧源码逐字/逐像素/所有数据组合等价**。旧系统未装回老依赖运行，旧行为仍依据真实源码交叉对照；本轮运行验证的是新系统的指定场景。

## 3. 失败与纠正记录

第一次新增测试有两个错误：工作区临时目录PermissionError；测试在TestCase事务内打开SQLite schema_editor不被支持。前者在正常Windows权限下使用同一隔离用例重跑；后者改为直接调用仅操作数据的迁移函数，断言仍验证指定失效定义删除、其他授权完全保留。默认构建沙箱子进程spawn EPERM，在正常权限重跑；产品未添加绕过分支。

浏览器自动化出现一次内核超时、一次只读combo输入无法focus、一次自定义switch输入setChecked无效。按新状态用真实控件继续，未把失败动作计通过。内核重置前观察值从本轮工具结果单独重建并标注；后续实时记录另存。文件网格初次数量包含隐藏对话框，已限定可见对话框纠正为30/44；query邻项第一次选错场景，随后真实验证右邻query保留，未把错误场景写成功。

第一次打包我误在Vite生成版本后改写后端版本，造成更新提示重复。浏览器复查发现后，重新由Vite统一版本并重新打包/发布；增加候选检查确认前端bundle内嵌版本与后端一致，正式首次改密页面已确认无更新提示。第一次构建、初次发布证据与两个备份均保留。第一次扩大账号指纹比较发现差异仅last_login来自正常验收登录；最终指纹保留其他全部账号字段，明确排除该正常登录时间戳，未忽略密码/计数/状态/资料变化。

## 4. 正式数据与版本

- 最终版本：`1.0.0.1791618793779`；exe SHA256：`57d651790f4fb0603ebda61608371ed1a995f177725f6f68219924c62f2384df`；首页SHA256：`fd17ee1ea63ee40ea92f9166af9c879a39e029367284a832c758a0c9c8f43777`。
- 原始旧包：`packaging/previous-tenth-20261010`；初次本批包：`packaging/previous-tenth-final-20261010`；正式包：`packaging/dist/djangovue3`。
- 迁移刻意清理字段定义id39及其字段授权id39各1条，证据见tenth-formal-update.json；除此之外角色/成员/菜单权限/按钮权限/字段授权、其余字段定义均摘要一致，账号资料/密码/计数/状态及3个附件文件均保留，测试库没有合并进正式库。
- 正式管理员原pwd_change_count=0，浏览器仍进入首次改密页面。这是保留原数据和正常配置的结果；本轮没有改它的密码或计数，也没有为验收关闭首次改密开关。凭据UI流程按用户要求跳过；相应API在隔离测试中完成验证。
- 源码开发库和正式库均迁移0019；独立24小时数据库未迁移或重启。正式冻结包不包含测试App/验收夹具，源码中的隔离测试代码保留。

## 5. 仍未完成的运行条件与证据边界

224条Windows相关基础记录：`{"C": 30, "I": 68, "K": 2, "O": 5, "S": 107, "U": 1, "V": 5, "X": 6}`，原236历史ID完整保留。只把本批7条D转I；其余S/I/V保持原证据含义，C30不伪装成原样复刻。

TASK-09仍为U：真实24小时验收从北京时间10-10 13:30:46运行至10-11 13:30:46并额外收集10秒，本文编写时仍running；源码/正式重启没有影响它。自然跨DST未发生，不计实测通过。OS休眠、Excel/WPS原生客户端、凭据UI更改、原生中键等按用户要求跳过，不再要求用户操作。移动/mac不纳入本次范围。

## 6. 证据文件

- [新增关联测试](H:/Project_python/django-vue3-admin/djangovue3/backend/system/tests/test_tenth_implementation.py)、[默认回归日志](H:/Project_python/django-vue3-admin/djangovue3/runtime/tenth-implementation-system-tests.log)、[完整扩展回归日志](H:/Project_python/django-vue3-admin/djangovue3/runtime/tenth-implementation-extension-full.log)。
- [实时浏览器记录](H:/Project_python/django-vue3-admin/djangovue3/docs/tenth-browser-live-records.json)、[内核重置前观察记录](H:/Project_python/django-vue3-admin/djangovue3/docs/tenth-browser-observed-before-reset.json)、[浏览器导出核对](H:/Project_python/django-vue3-admin/djangovue3/docs/tenth-browser-export-verification.json)。
- [最终候选验证](H:/Project_python/django-vue3-admin/djangovue3/docs/tenth-final-candidate-verification.json)、[最终正式验证](H:/Project_python/django-vue3-admin/djangovue3/docs/tenth-final-formal-verification.json)、[初次迁移数据保留](H:/Project_python/django-vue3-admin/djangovue3/docs/tenth-formal-update.json)、[最终替换记录](H:/Project_python/django-vue3-admin/djangovue3/docs/tenth-final-formal-update.json)。
- [当前Windows实施台账](H:/Project_python/django-vue3-admin/djangovue3/docs/tenth-windows-implementation-ledger.json)、[改前Windows审计台账](H:/Project_python/django-vue3-admin/djangovue3/docs/tenth-windows-audit-ledger.json)、[实施源码摘要](H:/Project_python/django-vue3-admin/djangovue3/docs/tenth-implementation-source-manifest.json)。

![整改后的登录日志页面（隔离Windows网页验收）](H:/Project_python/django-vue3-admin/djangovue3/docs/tenth-log-proof.png)

![部门概况整体恢复及含下级开关状态](H:/Project_python/django-vue3-admin/djangovue3/docs/tenth-department-proof.png)
