# djangovue3

面向 ERP 研发的 Django / Vue3 管理框架，参考 `../django-vue3-admin-master` 实现；原目录未修改。

固定 Python **3.14.8**、Django **5.2.18**。默认 SQLite，可切换 PostgreSQL；表格导入/导出使用 openpyxl，只支持 xlsx。

2026-10-11 按用户要求取消桌面打包，移除 packaging 目录和专用依赖。当前 8000 直接运行源码，原正式数据库、账号、授权及附件已接回 backend。后续修改后端代码只需重启服务；前端发布时执行构建，不需要生成 exe。

## 目录

| 目录/文件 | 用途 |
| --- | --- |
| backend | Django 源码、默认 db.sqlite3、media 附件、staticfiles、logs |
| web | Vue 源码、package-lock.json、dist 前端构建结果 |
| scripts | 源码启动、初始化、前端构建、任务服务、数据库配置 |
| runtime | 本机 Python、Node、Redis，以及历史验证资料 |
| requirements.lock.txt | 可复现的 Python 依赖，不包含桌面/打包工具 |
| database.ini.example | SQLite / PostgreSQL 配置示例；真实 database.ini 不提交 |
| docs | 使用说明、审计台账、历史实施证据 |
| data-backups | 取消打包前保留的开发数据及去重后的历史数据库/附件，不需要随应用分发 |

## 启动

在 PowerShell 进入项目根目录：

```powershell
Set-Location H:\Project_python\django-vue3-admin\djangovue3_dyeing
.\scripts\start.ps1
```

访问 **http://127.0.0.1:8000**。新数据库初始账户为 `superadmin / admin123456`；已有数据库继续使用现有密码及改密状态。

异步导出、实时消息及定时任务分别在其他终端启动：

```powershell
.\scripts\tasks.ps1 redis
.\scripts\tasks.ps1 worker
.\scripts\tasks.ps1 beat
```

Redis 默认 127.0.0.1:6389，Celery 使用第 3 个逻辑库。业务数据、任务配置和任务结果保存在所选数据库。停止源码服务可在对应终端按 Ctrl+C。本次已在后台恢复这四个服务，日志位于 backend/logs；再次启动前先停止已有同端口服务。

前端开发运行 `scripts/dev.ps1`，访问 http://127.0.0.1:8080。API 文档位于 http://127.0.0.1:8000/api/docs/。

## 初始化和前端构建

```powershell
.\scripts\init.ps1
.\scripts\build.ps1
.\.venv\Scripts\python.exe backend\manage.py check
.\.venv\Scripts\python.exe backend\manage.py test system.tests --settings=system.tests.extension_settings --noinput
```

初始化执行迁移并生成菜单、权限和区域数据，重复初始化保留现有管理员密码。当前数据已到 system 0019，运行不需要重新初始化。前端构建只生成 web/dist 和静态资源，由 Django 托管。

## 复制到其他目录或电脑

复制源码、依赖清单和必要运行文件即可使用，不需要打包。请一并携带 `runtime/python`。启动、初始化、构建、worker 和 beat 脚本会根据自身位置识别项目根目录，先自动检查 Python 环境：目录改变时重建 `.venv` 的配置、解释器、激活脚本及 pip/Celery 等命令入口，保留兼容的已安装依赖；依赖缺失或版本不同才按锁定清单安装。环境就绪后再次启动不会重复重建。

```powershell
# 可单独检查/修复环境，不启动服务、不修改业务数据库
.\scripts\ensure-python.ps1
# 也可直接启动，脚本会先完成上述检查
.\scripts\start.ps1
```

运行现成网页时保留 web/dist；修改前端或需要重新构建时安装前端依赖：

```powershell
Push-Location web
..\runtime\node\npm.cmd ci
Pop-Location
.\scripts\build.ps1
```

携带已有数据时保留 backend/db.sqlite3、backend/media 和实际 database.ini。SQLite 相对路径随项目位置生效；PostgreSQL 仍需可连接的服务器。源码服务、worker 和 beat 使用同一配置。

复制到另一台兼容的 Windows 电脑时，没有 `.venv` 也会自动创建，但首次安装依赖需要网络或可用的本地包源。携带完整 `.venv` 且 Python 主次版本一致时，移动目录无需重新下载依赖。此机制在运行脚本时生效；直接运行复制后的 `.venv/Scripts/python.exe` 或使用 IDE 前，请先执行 `ensure-python.ps1`，并把 IDE 解释器设为新目录下的 `.venv/Scripts/python.exe`。环境准备失败时脚本停止启动；不自动迁移端口、Redis、Git 远程仓库或数据库中的业务配置。

运行所需的本机 runtime 文件是 python、redis、redis.conf；前端构建另外需要 node。历史验证目录、downloads、docs、data-backups、`.venv`、web/node_modules 均不是需要逐份分发的业务源码。`.env.example` 只是变量说明，不自动加载。

## 数据库切换

```powershell
.\.venv\Scripts\python.exe scripts\database.py show
.\.venv\Scripts\python.exe scripts\database.py postgresql --name djangovue3 --user djangovue3
.\.venv\Scripts\python.exe scripts\database.py sqlite --path db.sqlite3
```

密码隐藏输入。修改配置后重启网页、worker、beat；切换不会自动搬迁已有数据。建库、初始化、双向搬迁见 [数据库说明](H:/Project_python/django-vue3-admin/djangovue3/docs/数据库切换实施与使用说明.md)。

## ERP 接入与文档

本染色项目已接入基础信息、销售、采购、打样、生产、仓储、质量七个ERP应用，共660个模型，均含【旧erpID】；包括553个原表模型和本轮新增的内部自增序列模型。原表模型声明11,412个旧字段、161组明确关系，已接入主从整单事务、办理冻结、部分原公式及表头回写；全部旧业务联动及历史采用仍按逐项台账验收。当前进度见[七模块模型实施记录](docs/染色ERP七模块模型实施记录.md)，本轮差异见[复刻异常与合理实现说明](docs/旧ERP复刻异常与合理实现说明.md)。

按旧字段复刻的规则、已修正内容及无法直接复刻的合理处理见 [旧系统字段复刻与差异处理说明](H:/Project_python/django-vue3-admin/djangovue3_dyeing/docs/旧系统字段复刻与差异处理说明.md)，全部字段设置见 [旧系统字段逐项对照](H:/Project_python/django-vue3-admin/djangovue3_dyeing/docs/旧系统字段逐项对照.md)。

后续接口、页面、业务流程、数据迁移及分批验收安排见 [染色ERP后续开发方案](H:/Project_python/django-vue3-admin/djangovue3_dyeing/docs/染色ERP后续开发方案.md)。

基础信息 A 批已接入26个模型的接口、16个主档页面及10类从属资料，并实现路线版本审核、启用、停用和复制。登录后进入“染色ERP → 基础信息”，已有超级管理员可直接使用。普通账号可配置“基础资料维护”或“基础资料查询”角色。实际数据库已完成第26个ERP迁移，ERP业务表为空；验收样例使用独立数据库。字段处理及测试结果见 [基础信息A批实施记录](H:/Project_python/django-vue3-admin/djangovue3_dyeing/docs/基础信息A批实施记录.md)。

按普通 Django app 编写业务模型及迁移，在 backend/application/plugins.py 登记应用和路由；前端扩展放在 web/src/plugins。通用资源提供 CRUD、筛选、角色/API/数据范围/字段权限及 xlsx 模板导入导出；订单、库存、财务流程需继续开发。数据库切换不等同于企业隔离。

- [扩展与组件接入](H:/Project_python/django-vue3-admin/djangovue3/docs/框架扩展与组件接入.md)
- [多企业 ERP 接入核实](H:/Project_python/django-vue3-admin/djangovue3/docs/多企业ERP开发适用性核实与接入方案.md)
- [当前复刻台账与方案](H:/Project_python/django-vue3-admin/djangovue3/docs/全盘对照审计与后续整改方案.md)
- [依赖版本](H:/Project_python/django-vue3-admin/djangovue3/docs/依赖版本.md)
- [疑问与方案记录](H:/Project_python/django-vue3-admin/djangovue3/疑问与方案记录.md)

本次移除打包后107项完整扩展测试通过，25资源 metadata/list、网页版本和3附件通过。验证记录为 docs/source-only-tests.log、docs/source-only-verification.json。旧日期报告中的桌面包、托盘、打包路径是历史实施记录，当前不再提供这些功能。

2026-10-11 后续更新：默认使用单侧导航，已有浏览器布局偏好首次加载新版时一并更新。此前3个测试导出文件及相关测试日志已按用户要求备份并清理；上段附件保留结论为清理前历史记录。具体范围与验证见[默认隐藏分栏导航与测试残留清理](H:/Project_python/django-vue3-admin/djangovue3/docs/默认隐藏分栏导航与测试残留清理.md)。
