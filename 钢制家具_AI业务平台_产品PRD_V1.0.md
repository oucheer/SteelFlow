# 钢制家具 AI 业务平台《产品 PRD》V1.0

# 文档信息

文档名称：钢制家具 AI 业务平台 PRD V1.0

产品定位：AI-native 的钢制家具销售与运营系统

目标阶段：从当前核心业务 Demo 进入可生产化 V0.2，再逐步扩展到 V1.0。

文档用途：统一产品目标、范围、用户、业务流程、功能需求、交互要求、数据要求、权限与验收标准，作为产品、设计、研发、测试和 Agent 的共同基线。

# 产品概述

## 1.1 一句话定义

一个以 AI 为业务操作层、以 CRM/ERP/MES 为业务事实层、面向钢制家具企业的销售、客服、订单、生产和经营协同平台。

## 1.2 核心价值

- 让 AI 理解客户、产品和业务上下文；让确定性业务规则保证价格、订单、生产等核心事实正确；让销售到工厂形成同一条数据链。

## 1.3 核心业务闭环

```text
客户触达
→ 客户身份识别
→ AI/真人客服
→ 需求结构化
→ 产品查询
→ Pricing Engine
→ 报价
→ 合同
→ 销售订单
→ 生产需求拆解
→ 生产计划
→ 工单
→ 员工报工
→ 计划 vs 实际
→ 交付/物流
→ 管理看板
```

# 产品目标与成功标准

## 2.1 业务目标

- 降低销售重复录入和跨系统搬运。

- 统一客户、产品、报价、合同、订单和生产数据。

- 让 AI 能够参与真实销售业务，同时受到权限、规则和审计控制。

- 让管理层可视化看到销售、订单、生产和交付风险。

- 减少内容制作与重复素材生产。

## 2.2 成功标准

| 指标 | 目标/验收口径 |

| --- | --- |

| Golden Path | 客户→AI→需求→报价→合同草稿→订单→生产→报工→看板全链路跑通 |

| 报价正确性 | 同一结构化输入在相同规则版本下结果可重复；与人工基准数据可对账 |

| AI需求抽取 | 保持现有100%评测基线，并纳入持续回归集 |

| 订单幂等 | 相同Webhook/Idempotency-Key不会生成重复业务记录 |

| 审计追溯 | 能从客户会话追溯到AI Run、Tool、报价规则版本、订单与生产任务 |

| 生产可视化 | 计划、实际、剩余、完成率、风险可由真实业务数据计算 |

| 权限 | Agent与人类用户使用同一业务权限边界，不允许绕过权限直接写库 |



# 用户与角色

| 角色 | 核心目标 | 主要能力 |

| --- | --- | --- |

| 销售人员 | 成交效率 | 客户、商机、AI辅助、报价、合同、订单、素材 |

| 客服/售前 | 高效承接咨询 | 会话、AI建议、人工接管、客户资料 |

| AI客服Agent | 自动理解与辅助执行 | 知识检索、信息抽取、受控Tool调用、摘要、转人工 |

| 生产主管 | 按期交付 | 计划、工单、工序、人员、产能、风险 |

| 生产员工 | 准确报工 | 任务、工序开始/结束、产量、质量、工时 |

| 管理层 | 经营可见 | 销售、订单、客户、生产、交付、风险 |

| 系统管理员 | 治理和配置 | 用户、角色、权限、规则、集成、AI、审计 |



# 产品信息架构

```text
首页 / Dashboard
├─ 销售
│  ├─ 客户
│  ├─ 商机
│  ├─ 跟进
│  ├─ 报价
│  ├─ 合同
│  └─ 订单
├─ AI客服
│  ├─ 会话
│  ├─ 知识
│  ├─ AI分析
│  └─ 人工接管
├─ 生产
│  ├─ 生产计划
│  ├─ 生产任务
│  ├─ 工单
│  ├─ 工序
│  ├─ 员工报工
│  └─ 计划vs实际
├─ 内容中心
├─ CAD方案
├─ 集成
└─ 系统设置
```

# 核心业务流程 PRD

## 4.1 客户到订单

```text
平台消息/私域
→ Customer Identity Resolution
→ Conversation
→ AI理解
→ 需求结构化
→ Product Query
→ Pricing Engine
→ Quote Draft
→ 人工确认（按策略）
→ Contract Draft
→ Sales Order
```

## 4.2 订单到生产

```text
Sales Order
→ Production Requirement
→ BOM
→ Production Plan
→ Work Order
→ Operation
→ Employee Report
→ Quality
→ Completion
→ Delivery
```

## 4.3 生产风险

```text
计划 + 实际 + 剩余 + 产能 + 交期
→ 规则计算风险
→ AI解释
→ 通知/审批流程
```

# 功能需求

## 5.1 Dashboard

| 功能 | 需求 |

| --- | --- |

| 经营总览 | 销售额、询盘、新客户、报价、订单、生产任务、交付风险 |

| 销售漏斗 | 线索→沟通→需求→报价→谈判→成交 |

| AI客服 | 会话量、AI处理率、转人工率、Tool调用与异常 |

| 生产总览 | 计划、完成、进行中、待开始、员工产量、工作中心负荷 |

| 延期风险 | 风险订单、风险原因、预计影响日期 |

| 快速入口 | AI客服、新建客户、新建报价、新建订单、生产计划、内容制作 |



## 5.2 客户/CRM

- 客户列表、详情、来源、负责人、等级、标签、联系人、微信、手机号、历史会话、历史报价、合同、订单、跟进记录。

- 客户详情必须提供统一 Timeline。

- 支持客户身份合并建议和人工确认。

## 5.3 商机/销售

- Opportunity阶段可配置：新线索、初步沟通、需求确认、报价、谈判、成交、失单。

- 每个商机必须有下一步动作和预计动作时间。

## 5.4 产品主数据

| 实体/能力 | 要求 |

| --- | --- |

| Product | 产品类别、SKU、变体、规格、图片、视频、CAD |

| 属性 | 宽、高、深、板厚、材料、颜色、表面处理、门型、锁具、层板、配件等 |

| 制造 | BOM、工艺路线、标准工时、工作中心 |

| 价格 | 价格规则、规则版本、有效期 |

| 素材 | 产品图、工厂图、展厅、施工、验收 |



## 5.5 AI客服工作台

- 左侧会话列表；中间聊天区；右侧客户、产品需求、报价、订单、AI分析。

- 支持AI建议回复、AI直接回复（受策略控制）、人工接管、摘要、需求抽取、产品推荐、报价工具。

- 人工接管条件：客户要求人工、低置信度、知识缺失、复杂报价、大客户、合同/法务、Tool异常。

## 5.6 报价

- Quote状态：draft、calculating、pending_approval、approved、sent、accepted、expired、rejected、cancelled。

- 报价页面展示完整计算明细和Price Rule Version。

```text
基础价 + 规格加价 + 配置加价 - 数量优惠 - 客户折扣 + 物流 + 其他费用 = 最终报价
```

## 5.7 合同

- 模板、变量映射、草稿、校验、审批、PDF、电子签Provider、回调、审计。

## 5.8 订单

- 来源支持manual、quote、platform、import、ai_assisted。关联客户、报价、合同、平台来源和external_order_id。

## 5.9 生产

- Production Plan、Production Task、Work Order、Operation、Work Center、Employee、Employee Report、Quality Record、Delivery。

- 当前六工序必须配置化，六工序只是默认Seed，不得永久硬编码。

- 员工报工包含：员工、日期、订单、产品、工序、计划量、实际量、合格量、不合格量、工时、备注。

## 5.10 内容中心

- 素材库、模板、图片编辑、视频模板、多平台尺寸派生。优先复用Fabric.js/Konva、FFmpeg、Remotion、ComfyUI。

## 5.11 CAD方案

- P0：上传、解析、图层、图元、尺寸、坐标、预览。P1：墙体/门窗/房间轮廓。P2：家具布局、碰撞、约束、优化、效果图。

## 5.12 平台集成

- 统一PlatformAdapter；先完成一个真实平台闭环，再扩展。禁止把浏览器模拟点击作为核心架构。

# AI Agent 产品规格

## 6.1 Agent职责

- 理解客户意图、提取结构化需求、检索知识、查询客户/产品、调用报价、生成合同草稿、摘要、建议、风险解释。

## 6.2 Tool规范

```text
Tool = name + description + input_schema + output_schema + permission + risk_level + approval_required + idempotency + audit
```

## 6.3 核心Tools

```text
search_products
get_product
search_customer
get_customer_history
extract_customer_requirement
calculate_quote
create_quote_draft
get_quote
generate_contract_draft
get_order
create_order_draft
get_production_status
get_production_plan
get_worker_production
summarize_conversation
create_followup_task
analyze_sales_conversation
analyze_delivery_risk
analyze_production_risk
```

## 6.4 AI安全边界

禁止Agent直接访问数据库；禁止绕过业务服务修改价格、订单、库存、生产计划等业务事实；高风险动作必须经过权限、业务校验、幂等、审计，并按策略增加人工审批。

# 权限、审批与审计

## 7.1 RBAC

```text
Organization → User → Role → Permission → Resource Scope
```

## 7.2 Action

read、create、update、approve、send、publish、delete。

## 7.3 高风险动作

- 正式报价、合同发送、订单提交、生产计划发布、内容发布、发货、删除。

## 7.4 审计要求

```text
actor / actor_type / resource_type / resource_id / action / before / after / request_id / agent_run_id / tool_call_id / timestamp
```

# 数据与集成规格

## 8.1 核心实体

```text
Organization, User, Role, Permission
Platform, Store, PlatformAccount
Customer, CustomerIdentity, Contact, CustomerTag, Opportunity, Activity, Conversation, ConversationMessage
Product, ProductCategory, SKU, ProductVariant, ProductAttribute, BOM, Routing
PriceRule, PriceRuleVersion
Quote, QuoteLine, Contract, ContractTemplate
SalesOrder, SalesOrderLine, Delivery
ProductionPlan, ProductionTask, WorkOrder, Operation, WorkCenter, Employee, EmployeeReport, QualityRecord
Asset, AssetFolder, AssetVersion, AssetTemplate, VideoTemplate, CADDocument
AIConversation, AIRun, AIToolCall, AIFeedback
Approval, AuditLog, WebhookEvent, OutboxEvent, IntegrationTask
```

## 8.2 Webhook

必须支持event_id、platform、event_type、payload、signature、status、retry_count、processed_at；重复事件不得重复创建业务。

## 8.3 Outbox

关键领域事件通过Outbox发布到n8n/通知/分析/AI等下游。

## 8.4 Adapter

AI、ERP、CRM、Platform、ESign、Storage、Workflow均尽可能通过Provider/Adapter隔离，防止业务代码被供应商锁定。

# 非功能需求

| 类别 | 要求 |

| --- | --- |

| 可靠性 | 幂等、重试、超时、死信/补偿、Outbox、备份恢复 |

| 安全 | JWT/Session、RBAC、租户隔离、Secret、审计、限流、文件校验、Webhook签名 |

| 性能 | 普通列表API目标P95<500ms；业务写入P95<1s；AI/CAD/视频任务异步化 |

| 可维护性 | 模块化、Typed Schema、Migration、Adapter、Provider、OpenAPI |

| 可观测 | request_id、trace_id、job_id、webhook_id、outbox_id、agent_run_id、tool_call_id |

| 可测试 | Unit、Integration、API、E2E、AI Tool、Webhook、Permission |



# 版本规划

## 10.1 V0.1 已交付基线

- Sales/CRM：客户、商机、跟进、报价状态机、合同草稿/PDF。

- AI：需求抽取及评测、知识问答、客户信息抽取、报价Tool、转人工、审计。

- Production：订单拆解、六工序工单、报工、计划vs实际、产能、延期预测、日报。

- Platform/Governance：Adapter矩阵、模拟订单同步、幂等、身份合并确认、RBAC、审批、审计、Outbox、Webhook。

## 10.2 V0.2 生产化

```text
PostgreSQL → JWT/RBAC → AI Provider → n8n → 一个真实平台 → Content Studio → E-Sign Adapter → 生产加固
```

## 10.3 V0.3

多平台、AI销售增强、内容批量、视频模板、物流、库存/采购、AI经营分析、生产异常分析。

## 10.4 V1.0

稳定多租户、多平台真实业务、AI客服规模化、销售/订单/生产全闭环、CAD自动布局、高级生产排程。

# 范围边界与非目标

- V0.2不同时实现五个平台的完整客服闭环。

- 不自研通用ERP、通用CRM、通用RAG、通用Workflow、通用Canvas、通用DXF底层。

- 不在早期实现复杂APS、完整财务、完整WMS、完整电子签CA体系。

- CAD自动布局和效果图作为后续阶段。

# 验收与测试用例

## 12.1 Golden Path

```text
客户进入 → AI客服 → 需求抽取 → 产品匹配 → Pricing Engine → 报价 → 合同草稿 → 销售订单 → 生产任务 → 生产计划 → 工单 → 员工报工 → Dashboard
```

## 12.2 关键测试

- 报价：相同输入+相同规则版本→结果一致。

- Webhook：同event_id重复到达→只生成一个业务结果。

- 订单：同Idempotency-Key重复请求→只创建一个订单。

- Agent：无权限Tool调用必须被拒绝并写审计。

- 生产：计划量、实际量、剩余量和完成率必须满足业务一致性。

# 开源复用策略

| 能力 | 参考/复用方向 |

| --- | --- |

| ERP/制造 | ERPNext / Odoo |

| CRM | Frappe CRM / Odoo / EspoCRM / Twenty |

| 客服 | Chatwoot / Frappe Helpdesk |

| AI Agent/RAG | Dify / MaxKB |

| Workflow | n8n |

| 图片编辑 | Fabric.js / Konva |

| 视频 | FFmpeg / Remotion |

| AI图像 | ComfyUI |

| CAD | ezdxf / LibreCAD |



原则：通用能力尽量复用，行业能力自己做；所有开源组件商用前必须完成许可证审查。

# 产品设计与UI规范

整体风格：高端、克制、现代企业 SaaS；以白/冷灰为底，深蓝作为主品牌色，青绿表示成功，橙色表示预警。信息可读性优先。

- Dashboard：指标卡 + 趋势图 + 待办 + 风险。

- AI客服：三栏布局，保持客户上下文常驻。

- 报价：左侧需求，右侧价格计算明细；突出规则版本和审批状态。

- 生产：计划/实际、订单/产品/员工/工序视图切换；风险用明确标签，不依赖纯颜色。

- 表格支持筛选、搜索、排序、分页、批量操作和导出。

# 实施要求

任何研发 Agent 在编码前必须先检查现有仓库，区分 REAL / MOCK / STUB；已有能力优先 reuse/refactor/extend。

大范围重构前必须记录问题、原因、影响和方案。

任何新增功能必须同时考虑 UI、API、数据库、权限、审计、测试和文档。

没有真实第三方账号时，可以完成 Adapter、Mock、契约、映射、错误处理和测试；只有真实认证/真实数据验证依赖外部资源。
