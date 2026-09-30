# 钢制家具 AI 业务平台｜完整产品 SPEC V1.0

> 统一基线：将前期需求、可行性分析、开源复用研究、当前已交付能力和下一阶段生产化路线合并为一份正式产品规格。

## 0. 产品定义

**产品名称：** 钢制家具 AI 业务平台  
**英文：** Steel Furniture AI Sales & Operations Platform  
**定位：** 面向钢制家具企业的 AI-native 销售、客服、CRM、报价、合同、订单、生产协同和经营可视化平台。

产品不是“传统 ERP + 一个聊天框”，也不是“AI 客服 + 几个业务页面”。核心是让 AI 成为业务操作层，让 CRM/ERP/MES 和规则引擎成为业务事实层。

```text
客户/平台
  ↓
Customer Identity
  ↓
AI客服/真人客服
  ↓
需求结构化
  ↓
产品查询
  ↓
Pricing Engine
  ↓
报价
  ↓
合同
  ↓
销售订单
  ↓
生产拆解
  ↓
生产计划
  ↓
工单/工序
  ↓
员工报工
  ↓
计划VS实际
  ↓
交付/物流
  ↓
经营与生产看板
```

旁路能力：

```text
Content Studio：素材/图片/视频/AI内容
CAD Studio：DXF解析/家具布局/效果图
Integration：电商/微信/ERP/CRM/电子签
AI：RAG/Agent/Tool/人机协作
```

---

## 1. 业务背景

销售渠道包含淘宝、天猫、京东、拼多多、小红书、抖音及微信私域。业务存在以下典型问题：

- 产品和客户信息散落在平台、聊天记录和人工表格中。
- 同一产品的主图、详情图、海报、视频被重复生产。
- 客服需要人工阅读产品资料、判断规格、报价、整理客户信息。
- 复杂定制需求往往通过图片、草图、CAD、电话和微信沟通。
- 报价、合同、订单、CRM、生产之间存在人工重复录入。
- 工厂需要根据订单拆分生产任务、工序、人员和产能。
- 管理层需要实时看到订单和生产进度，而不是等待人工日报。

---

## 2. 产品目标

### O1 销售效率
减少重复录入，让销售从“信息搬运”转向客户跟进。

### O2 AI客服
让 AI 读取企业知识、理解客户需求、辅助销售，但不直接决定关键业务事实。

### O3 业务闭环
客户 → 报价 → 合同 → 订单 → 生产 → 报工 → 交付形成统一数据链。

### O4 生产透明
管理层可以实时查看计划、实际、产能和交期风险。

### O5 内容效率
产品素材“一次生产，多平台派生”。

### O6 行业壁垒
最终形成钢制家具产品模型、报价规则、拆单和生产规则等行业资产。

---

## 3. 产品原则

1. **不重复造轮子。** CRM、ERP、RAG、Workflow、Canvas、视频和 DXF 优先复用成熟项目。
2. **AI负责理解，规则负责计算。** 价格、订单、库存、生产数量、权限、审批必须由业务系统决定。
3. **Agent 不直接访问数据库。** 必须经 Tool → Permission → Domain Service → Validation → Persistence。
4. **高风险动作必须受控。** 正式报价、合同发送、订单提交、生产计划发布、内容发布、发货、删除等动作必须经过权限/校验/审计，并按策略追加人工审批。
5. **所有外部服务 Adapter 化。** AI、ERP、CRM、电商、电子签、对象存储等均通过 Provider/Adapter 接入。
6. **先跑通一个闭环，再扩展平台和高级 AI。**
7. **真实业务数据优先于 Demo 页面数量。**

---

## 4. 用户与角色

| 角色 | 主要目标 |
|---|---|
| 销售 | 客户、商机、跟进、报价、合同、订单、内容 |
| 客服 | 多平台会话、AI辅助、人工接管、客户信息 |
| AI Agent | 理解、检索、抽取、调用受控工具、解释与建议 |
| 生产主管 | 计划、工单、产能、报工、风险 |
| 车间员工 | 查看任务、开始/结束工序、报工、质量 |
| 管理层 | 销售、客户、订单、生产、交付、风险看板 |
| 管理员 | 用户、角色、权限、规则、平台、AI、审计 |

---

## 5. 信息架构

```text
Dashboard
├─ 销售/CRM
│  ├─ 客户
│  ├─ 商机
│  ├─ 跟进
│  ├─ 报价
│  ├─ 合同
│  └─ 订单
├─ AI客服
│  ├─ 会话
│  ├─ 知识库
│  ├─ AI分析
│  └─ 转人工
├─ 生产
│  ├─ 生产计划
│  ├─ 生产任务
│  ├─ 工单
│  ├─ 工序
│  ├─ 报工
│  └─ 计划VS实际
├─ 内容中心
│  ├─ 素材
│  ├─ 模板
│  ├─ 图片编辑
│  └─ 视频
├─ CAD方案
│  ├─ 文件
│  ├─ 解析
│  ├─ 布局
│  └─ 导出
├─ 集成中心
└─ 系统治理
```

---

## 6. 核心领域模型

### 6.1 客户域

```text
Organization
User
Customer
CustomerIdentity
Contact
CustomerTag
Opportunity
Activity
Conversation
ConversationMessage
```

### 6.2 产品域

```text
Product
ProductCategory
SKU
ProductVariant
ProductAttribute
BOM
Routing
```

产品主数据必须支持：尺寸、材质、颜色、表面、配置、配件、BOM、工艺、图片、视频、CAD、定价关联。

### 6.3 销售域

```text
PriceRule
PriceRuleVersion
Quote
QuoteLine
Contract
ContractTemplate
SalesOrder
SalesOrderLine
Delivery
```

### 6.4 生产域

```text
ProductionPlan
ProductionTask
WorkOrder
Operation
WorkCenter
EmployeeReport
QualityRecord
```

### 6.5 AI域

```text
AIConversation
AIRun
AIToolCall
AIFeedback
```

### 6.6 治理域

```text
Role
Permission
Approval
AuditLog
WebhookEvent
OutboxEvent
IntegrationTask
```

---

## 7. CRM规格

客户详情必须形成统一时间线：

```text
创建 → 询盘 → AI会话 → 人工接管 → 报价 → 合同 → 订单 → 生产 → 发货 → 售后
```

商机默认阶段：

```text
新线索 → 初步沟通 → 需求确认 → 报价 → 谈判 → 成交/失单
```

必须支持客户来源、负责人、标签、客户等级、微信、手机号、公司、历史对话、历史报价、历史订单、AI摘要。

---

## 8. AI客服规格

### 8.1 对话链

```text
平台消息
→ Customer Identity Resolution
→ Intent Detection
→ Knowledge Retrieval
→ Requirement Extraction
→ Tool Calling
→ Response
→ Audit
→ Human Handoff
```

### 8.2 AI能力

- 产品知识问答
- FAQ
- 客户信息抽取
- 产品需求抽取
- 产品匹配
- 报价工具调用
- 合同草稿
- 对话摘要
- 销售辅助
- 高价值客户识别
- 生产进度问答

### 8.3 转人工

触发条件包括：用户主动要求人工、低置信度、知识库无命中、复杂报价、大客户、特殊价格、法务/合同问题、AI工具失败。

---

## 9. 知识库与业务真值

必须严格区分：

```text
Knowledge Base
= 解释性知识

Business Database / Domain Service
= 结构化业务真值
```

价格、库存、订单状态、生产数量等不可只依赖向量知识库。

---

## 10. Agent Tool Layer

Tool 必须声明：

```text
name
input_schema
output_schema
permission
risk_level
approval_required
idempotency_required
audit_required
```

P0 工具：

```text
search_products
get_product
search_customer
get_customer_history
search_conversations
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

高风险工具：

```text
send_quote
send_contract
submit_order
publish_production_plan
publish_content
ship_order
```

这些工具必须通过统一权限、业务校验、幂等、审计与审批策略。

---

## 11. Pricing Engine规格

Pricing Engine 是核心自研能力。

输入：

```text
Product
Variant
Dimension
Configuration
Quantity
CustomerLevel
Discount
Logistics
Campaign
```

输出：

```text
price
breakdown
rule_version
```

计算必须可重复、可解释、可回放。

报价页面必须展示：

```text
基础价格
+ 规格加价
+ 配置加价
- 数量优惠
- 客户折扣
+ 物流
+ 其他费用
= 最终报价
```

价格规则必须版本化、有生效时间、有优先级、有审计。

---

## 12. Customer Identity Resolution

同一客户可能来自不同平台：

```text
Taobao / JD / PDD / Douyin / Xiaohongshu / WeChat / Phone / Email
```

合并采用：

```text
强匹配 → 自动建议
弱匹配 → 给出置信度与解释
低置信度 → 人工确认
```

禁止仅凭同名自动合并。

---

## 13. Quote / Contract / Order

### Quote

```text
draft
calculating
pending_approval
approved
sent
accepted
expired
rejected
cancelled
```

必须保存 `price_rule_version`。

### Contract

```text
Quote
→ Template
→ Variable Mapping
→ Draft
→ Validation
→ Approval
→ PDF
→ ESign Provider
→ Callback
→ Audit
```

第一阶段使用 MockProvider 即可完成接口开发。

### Sales Order

来源必须记录：

```text
manual / quote / platform / import / ai_assisted
```

关联客户、报价、合同、平台及 external_order_id。

---

## 14. 生产制造规格

生产链：

```text
Sales Order
→ Production Requirement
→ BOM
→ Production Plan
→ Work Order
→ Operation
→ Employee Report
→ Actual Qty
→ Progress
→ Delivery
```

“六工序”只是当前 Demo 配置，实际必须通过 `Routing / Operation / WorkCenter` 配置化。

### 员工报工

```text
employee
 date
 order
 product
 operation
 planned_qty
 actual_qty
 qualified_qty
 rejected_qty
 working_hours
 remark
```

### 计划VS实际

必须显示：计划量、实际量、剩余量、完成率、差异、预计完成时间、风险。

### 延期风险

规则侧计算，AI解释：

```text
Due Date
+ Planned Qty
+ Actual Qty
+ Capacity
+ Historical Efficiency
```

AI不得编造生产数字。

---

## 15. Content Studio

资产：

```text
Asset
AssetFolder
AssetVersion
```

模板：

```text
AssetTemplate
VideoTemplate
```

模板变量：

```text
product
title
selling_points
price
logo
sales_person
phone
qr
background
```

一个模板可派生多平台版本：淘宝、天猫、京东、小红书、抖音。

图片编辑优先 Fabric.js / Konva。视频处理优先 FFmpeg；Remotion 作为模板视频参考/候选。

---

## 16. CAD Studio

P0：

```text
Upload DXF
→ Parse
→ Layer
→ Geometry
→ Preview
→ Export
```

P1：

```text
Wall
Door
Window
Room
Furniture Block
Collision
```

P2：

```text
Furniture Placement
Constraint
Optimization
Rendering
```

采用：

```text
AI需求理解
+
Geometry Engine
+
行业规则
```

不要让 LLM 直接生成未经验证的坐标。

---

## 17. 平台 Adapter

统一：

```text
PlatformAdapter
authorize()
get_customer()
get_orders()
get_order()
get_conversations()
get_messages()
send_message()
subscribe_webhook()
```

平台：

```text
Taobao
JD
PDD
Douyin
Xiaohongshu
WeChat
```

原则：官方 API 优先；不要将浏览器模拟操作作为核心架构。

第一阶段只打通一个真实平台。

---

## 18. Workflow / Event

Outbox：

```text
Business Transaction
→ OutboxEvent
→ Publisher
→ n8n / Notification / Analytics / AI
```

核心事件：

```text
CustomerCreated
QuoteCreated
QuoteApproved
ContractApproved
OrderCreated
ProductionTaskCreated
ProductionReportSubmitted
ProductionRiskDetected
DeliveryCreated
```

Webhook必须支持签名验证、幂等、重试、补偿、失败审计。

---

## 19. 权限、审批、审计

### 权限

```text
Organization
→ User
→ Role
→ Permission
→ Resource Scope
```

### 审批

报价、特殊折扣、合同、订单、生产计划、内容发布等支持策略化审批。

### 审计

记录：

```text
actor
actor_type
resource_type
resource_id
action
before
after
request_id
agent_run_id
tool_call_id
timestamp
```

必须能追溯：

```text
客户说什么
→ AI理解什么
→ 调用了什么
→ 用了什么价格规则
→ 生成什么报价
→ 谁审批
→ 谁发送
→ 最终订单/生产
```

---

## 20. Dashboard

### 销售

询盘、新客户、报价、订单、销售额、漏斗、渠道来源、热销产品。

### AI客服

会话、AI处理率、转人工率、报价触发、Tool调用、错误、高价值客户。

### 生产

今日计划、完成量、完成率、进行中、待开始、员工产量、工作中心负荷、延期风险。

### 管理

销售、订单、客户、生产、交付统一经营视图。

---

## 21. 前端页面

至少：

```text
/dashboard
/customers
/customers/:id
/opportunities
/ai-service
/ai-service/conversations/:id
/products
/products/:id
/pricing-rules
/quotes
/quotes/:id
/contracts
/contracts/:id
/orders
/orders/:id
/production
/production/plans
/production/work-orders
/production/reports
/content
/content/assets
/content/templates
/content/editor
/cad
/integrations
/settings/users
/settings/roles
/settings/permissions
/settings/platforms
/settings/ai
/audit
```

AI客服采用三栏布局：会话 / 消息 / 客户与业务上下文。

Quote页面强调价格计算明细和规则版本。

Production页面强调计划/实际/风险。

整体 UI：企业级、高信息可读性、克制的科技感，避免为了炫技造成密度和可读性下降。

---

## 22. 数据、API与可靠性

数据库优先 PostgreSQL。需要：

- migrations
- indexes
- unique constraints
- foreign keys
- transaction
- backup/restore

API：

- OpenAPI
- Auth
- Permission
- Validation
- Error Code
- request_id
- idempotency
- audit

Webhook：

```text
event_id
platform
event_type
payload
signature
received_at
status
retry_count
processed_at
```

---

## 23. 非功能需求

### 性能基线

- 普通列表 API P95 < 500ms（正常部署基准）
- 业务写入 P95 < 1s
- AI、视频、CAD 等耗时任务异步化

### 可靠性

- Timeout
- Retry
- Idempotency
- Circuit Breaker（外部依赖）
- Dead Letter
- Outbox
- Backup

### 安全

- JWT/Session
- RBAC
- Tenant Isolation
- Secret Management
- Audit
- Rate Limit
- Input/File Validation
- Webhook Signature Verification

---

## 24. AI Evaluation

建立：

```text
evals/
```

至少包括：

```text
product_qa
customer_extraction
requirement_extraction
quote_extraction
tool_selection
tool_arguments
handoff
```

用真实历史对话、产品和报价规则建立 Golden Set。任何 Prompt、Model、Retrieval 修改必须重新评测。

---

## 25. 当前版本基线

已有交付：

- 销售/CRM：客户、商机漏斗、跟进、报价状态机、合同草稿+PDF
- AI：需求抽取、需求抽取评测、知识库问答、客户信息抽取、报价工具调用、转人工、审计全链路
- 生产：订单拆解、六工序工单、报工、计划vs实际、产能负荷、延期预测、日报
- 平台：Adapter能力矩阵、模拟订单同步、幂等、身份合并确认
- 治理：RBAC、审批闸门、审计日志、Outbox、Webhook幂等

当前待生产化：

- PostgreSQL
- JWT
- 真实 AI Provider（Dify/MaxKB）
- n8n
- 一个真实平台
- Fabric.js/Konva内容编辑器
- 电子签 Provider
- 后续多平台

---

## 26. 版本路线

### V0.1：Core Business Loop

现有基线：CRM + AI + Quote + Contract + Order + Production + Governance。

### V0.2：Productionization & Real Integration

```text
PostgreSQL
JWT/RBAC正式化
AI Provider
n8n
一个真实平台
Content Studio
ESign Adapter
生产数据加固
```

### V0.3：Scale & AI Enhancement

```text
多平台
AI销售增强
内容批量生成
视频模板
物流/库存
AI经营分析
生产异常分析
```

### V1.0

```text
多租户
稳定多平台
AI客服规模化
销售-订单-生产闭环
经营分析
CAD自动布局
高级排程
```

---

## 27. P0 Golden Path

```text
Customer
→ Conversation
→ Identity
→ Requirement
→ Product
→ Pricing
→ Quote
→ Contract Draft
→ Sales Order
→ Production Task
→ Production Plan
→ Work Order
→ Employee Report
→ Dashboard
```

Demo至少准备：20产品、50 SKU、10客户、5销售、20价格规则、10报价、5订单、3生产任务、10报工、20对话。

示例场景：

> “客户想采购20个900×1850×400灰白色钢制文件柜。”

系统必须能完成需求理解、产品匹配、确定性报价、报价单、订单、生产任务、报工和看板展示。

---

## 28. Definition of Done

每个功能只有在：

```text
UI
+ API
+ Database
+ Permission
+ Audit
+ Test
+ Documentation
```

均完成后才算 Done。

关键业务还必须满足：

- 可回放
- 可追溯
- 幂等
- 有错误恢复
- 有审计

---

## 29. 明确不在当前主线

当前不要优先做：

- 同时接五/六个平台
- 自研电子签底层
- 自研RAG底层
- 自研Canvas底层
- 自研视频编解码
- 复杂APS
- 完整WMS/财务
- AI直接控制生产
- LLM直接生成CAD坐标

原因：这些能力会显著增加复杂度，并且不直接提升第一条业务闭环的可信度。

---

## 30. 开源复用结论

### 高复用

ERPNext、Odoo、Frappe CRM、Chatwoot、Frappe Helpdesk、Dify、MaxKB、n8n、Fabric.js、Konva、FFmpeg、ezdxf、LibreCAD。

### 重点参考

Twenty、EspoCRM、Remotion、ComfyUI。

### 必须自研

钢制家具产品模型、Pricing Engine、Identity Resolution、订单拆解、生产规则、行业工艺、Agent Tool Layer、平台 Adapter 统一接口、权限/审批/审计、行业 Dashboard。

---

## 31. 外部能力验证

平台接入前必须逐平台确认：

```text
授权方式
订单读取
订单Webhook
客户信息
会话读取
消息发送
签名/安全机制
限流
审核
```

没有真实账号时继续做 Adapter、Mock、Contract、Schema、Webhook、映射和测试；真实 OAuth/订单/客服消息验证再依赖商家凭据。

---

## 32. 许可证治理

创建：

```text
docs/third-party-licenses.md
```

每项记录：项目、版本、许可证、使用方式、修改方式、商业条款、依赖。

特别关注：ERPNext/Frappe、Odoo、Dify、n8n、Twenty、Remotion、FFmpeg 等。

当前核查结论仅用于工程选型，不构成法律意见；正式商业化前必须进行完整许可证审查。

---

# 33. 参考资料

- ERPNext Manufacturing: https://docs.frappe.io/erpnext/manufacturing
- ERPNext Production Plan: https://docs.frappe.io/erpnext/production-plan
- ERPNext Work Order: https://docs.frappe.io/erpnext/work-order
- ERPNext Job Card: https://docs.frappe.io/erpnext/job-card
- Frappe CRM: https://github.com/frappe/crm
- Frappe CRM docs: https://docs.frappe.io/crm/introduction
- Chatwoot docs: https://github.com/chatwoot/docs
- Odoo: https://github.com/odoo/odoo
- Dify: https://github.com/langgenius/dify
- MaxKB: https://github.com/1Panel-dev/MaxKB
- n8n: https://github.com/n8n-io/n8n
- Twenty: https://github.com/twentyhq/twenty
- Fabric.js: https://github.com/fabricjs/fabric.js
- Konva: https://github.com/konvajs/konva
- FFmpeg: https://github.com/FFmpeg/FFmpeg
- Remotion: https://github.com/remotion-dev/remotion
- ComfyUI: https://github.com/Comfy-Org/ComfyUI
- ezdxf: https://github.com/mozman/ezdxf
- LibreCAD: https://github.com/LibreCAD/LibreCAD
- EspoCRM: https://github.com/espocrm/espocrm

---

# 附录A：前期159项开源复用矩阵

# 钢制家具 AI 业务平台：开源复用与 V0.1 技术选型

> 调研时间：2026-09-29。目标：最大化复用成熟组件，避免重复开发 CRM/ERP/RAG/视频/CAD 基础能力。


## 1. 结论

项目整体可行。建议采用“开源业务底座 + AI编排 + 行业业务中台 + 平台适配层”的架构。真正需要形成行业壁垒的部分是：钢制家具产品模型、报价规则、订单拆单、工艺/生产规则、客户身份统一、多平台适配、AI Tool Layer。


**原则：AI负责理解与建议，规则/业务服务负责计算与落库；Agent默认只读，涉及报价确认、合同发送、下单、生产计划发布等不可逆/高风险动作必须经过业务权限与人工确认。**


## 2. 参考项目组合

| 项目 | 适合参考的部分 | 结论 |
|---|---|---|

| ERPNext | CRM、销售、报价、销售订单、BOM、Production Plan、Work Order、Job Card、制造 | 重点研究生产数据模型 |

| Odoo | CRM、Sales、Quotation Template、在线签名、Manufacturing、Work Center、Shop Floor、Reporting | 重点研究销售+生产工作流 |

| Frappe CRM | Lead、Opportunity、Contact、Activity、现代CRM | 研究CRM数据模型 |

| Chatwoot | 多渠道客服工作台、Conversation、Inbox、人工接管 | 研究客服工作台 |

| Frappe Helpdesk | Ticket、Knowledge Base、SLA、Assignment、Customer Portal | 研究客服自动化 |

| Dify | RAG、Agent、Workflow、Tool Calling、模型管理、观测 | AI原型优先复用 |

| MaxKB | 中文企业知识库、RAG、Agent、Workflow、MCP | AI客服可作为备选 |

| n8n | Workflow、Webhook、AI Agent、Human Approval、1500+ integrations | 系统间流程编排 |

| Twenty | Objects、Views、Workflows、Agents、现代CRM UI | AI-native CRM交互参考 |

| Fabric.js / Konva | Canvas编辑器、图片/文字/变换、JSON/SVG、导出 | 素材设计器不要从零做 |

| FFmpeg | 转码、拼接、overlay、字幕等视频处理 | 视频底层能力直接复用 |

| Remotion | React程序化视频、批量渲染、模板 | 模板视频值得研究，商用许可证先核查 |

| ComfyUI | 节点式图像/视频工作流、API化Workflow | AI素材生成底座 |

| ezdxf | DXF读/改/写、导出、审计 | CAD文件处理底座 |

| LibreCAD | 2D CAD、DXF | CAD交互参考 |

| EspoCRM | CRM、Opportunity、Quotes、Workflow、REST API | 轻量CRM参考 |


## 3. 功能复用矩阵


共梳理 **159** 个功能点。字段：类别 / 功能点 / 开源参考 / 建议复用方式 / 自研等级 / 风险。


| 类别 | 功能点 | 开源/同类参考 | 建议复用方式 | 自研等级 | 风险/备注 |
|---|---|---|---|---|---|

| 销售/C端 | 客户线索 | Frappe CRM / Odoo / EspoCRM | 直接参考数据模型与状态流转 | 低 | 行业字段需扩展 |
| 销售/C端 | 客户资料 | Frappe CRM / Odoo / EspoCRM | 复用联系人/组织/地址模型 | 低 | 需要手机号/微信识别字段 |
| 销售/C端 | 客户标签 | Frappe CRM / Odoo / EspoCRM | 复用标签思想 | 低 | 行业标签自研 |
| 销售/C端 | 客户来源 | Frappe CRM / Odoo | 参考 Lead Source | 低 |  |
| 销售/C端 | 跟进记录 | Frappe CRM / EspoCRM | 参考 Activity/Timeline | 低 |  |
| 销售/C端 | 商机 | Frappe CRM / Odoo / EspoCRM | 复用 Opportunity/Deal 模型 | 低 |  |
| 销售/C端 | 销售阶段 | Frappe CRM / Odoo | 复用 Pipeline | 低 |  |
| 销售/C端 | 销售任务 | Frappe CRM / Twenty | 参考任务/活动模型 | 低 |  |
| 销售/C端 | 销售提醒 | n8n / ERPNext / Odoo | 工作流+定时器 | 中 |  |
| 销售/C端 | 客户时间线 | Twenty / Frappe CRM | 复用 Timeline 设计 | 低 |  |
| 销售/C端 | 历史订单查看 | ERPNext / Odoo | 通过 API 查询 | 低 |  |
| 销售/C端 | 客户画像 | Frappe CRM + Dify/MaxKB | CRM结构化字段+AI摘要 | 中 | 画像字段定义需要行业化 |
| 销售/C端 | 自动识别客户姓名 | Dify / OCR/LLM | AI抽取为结构化字段 | 中 | 需要规则校验 |
| 销售/C端 | 自动识别微信 | Dify + 正则/业务规则 | 规则优先，AI补充 | 中 | 平台消息权限需核实 |
| 销售/C端 | 自动识别手机号 | LLM + 正则 | 正则优先 | 低 |  |
| 销售/C端 | 客户去重 | ERPNext / Odoo / EspoCRM | 参考实体合并/唯一键策略 | 中 | 手机号/微信/公司联合判重 |
| 销售/C端 | 客户分级 | Odoo CRM | 参考客户等级 | 低 | 行业规则自研 |
| 销售/C端 | 公共客户池 | CRM类项目 | 参考分配机制 | 中 |  |
| 销售/C端 | 销售人员权限 | ERPNext / Odoo / Twenty | RBAC/记录级权限参考 | 中 |  |
| 销售/C端 | 素材库 | 自研 + 对象存储 | 不要自研底层存储 | 中 | 重点做行业标签与版本 |
| 销售/C端 | 主图模板 | Fabric.js / Konva | Canvas编辑器复用 | 中 |  |
| 销售/C端 | 详情页模板 | Fabric.js / Konva | 模板化组件 | 中 |  |
| 销售/C端 | 海报模板 | Fabric.js / Konva | 模板化组件 | 中 |  |
| 销售/C端 | 多平台尺寸适配 | Fabric.js / Konva | 同一设计JSON多尺寸渲染 | 中 |  |
| 销售/C端 | 一键导出图片 | Fabric.js / Konva | 直接复用导出能力 | 低 |  |
| 销售/C端 | AI生成营销文案 | Dify / MaxKB + LLM | 工作流/Agent | 中 |  |
| 销售/C端 | 平台文案变体 | Dify Workflow | 按平台模板生成 | 中 | 平台规则需人工维护 |
| 销售/C端 | 视频素材库 | 对象存储 + FFmpeg | 底层复用FFmpeg | 低 |  |
| 销售/C端 | 视频模板 | Remotion | 模板驱动渲染 | 中 | 商用许可证需审核 |
| 销售/C端 | 视频批量生成 | Remotion + FFmpeg | 队列化渲染 | 中 |  |
| 销售/C端 | 字幕生成 | FFmpeg + ASR | 底层复用 | 中 |  |
| 销售/C端 | 水印/Logo | FFmpeg | 复用滤镜/overlay | 低 |  |
| 销售/C端 | 视频封面 | ComfyUI + 模板引擎 | AI生成+模板组合 | 中 |  |
| 销售/C端 | 平台内容发布 | 各平台官方开放平台 | 官方API优先 | 高 | 不能以浏览器模拟点击作为核心方案 |
| AI客服 | 统一会话 | Chatwoot | 参考 Conversation/Inbox 数据模型 | 中 |  |
| AI客服 | 客服工作台 | Chatwoot / Frappe Helpdesk | 参考现成UI与会话流 | 中 |  |
| AI客服 | 人工接管 | Chatwoot | 参考 Human Handoff | 中 |  |
| AI客服 | 客服分配 | Chatwoot / Frappe Helpdesk | 复用Assignment思路 | 低 |  |
| AI客服 | SLA | Frappe Helpdesk | 参考SLA计时 | 低 |  |
| AI客服 | 知识库 | Dify / MaxKB | 不要从零实现RAG | 低 | 内容本身是企业资产 |
| AI客服 | RAG检索 | Dify / MaxKB | 直接复用 | 低 |  |
| AI客服 | 知识库权限 | Dify / MaxKB | 参考数据集权限 | 中 |  |
| AI客服 | 产品参数问答 | Dify / MaxKB | 产品知识库 | 低 |  |
| AI客服 | FAQ | Dify / MaxKB / Frappe Helpdesk | 知识库+结构化FAQ | 低 |  |
| AI客服 | 销售话术库 | Dify / MaxKB | 知识库/工作流 | 低 |  |
| AI客服 | 意图识别 | Dify Agent | Agent/分类器 | 中 |  |
| AI客服 | 需求结构化 | Dify Agent + Schema | Function Calling/结构化输出 | 中 | 需要严格字段校验 |
| AI客服 | 报价触发 | Dify Workflow + 自研Pricing Engine | AI只负责触发与提取需求 | 高 | 价格不得由LLM自由生成 |
| AI客服 | 自动报价 | Odoo Quotation / ERPNext Quotation | 报价单模型复用 | 高 | 价格计算规则自研 |
| AI客服 | 报价审批 | Odoo / ERPNext Workflow | 工作流参考 | 中 |  |
| AI客服 | 合同生成 | Odoo Quote Templates / 自研模板 | 模板填充 | 中 |  |
| AI客服 | 合同变量抽取 | Dify Agent | 结构化提取 | 中 |  |
| AI客服 | PDF合同生成 | PDF模板工具 | 底层组件复用 | 中 |  |
| AI客服 | 电子签 | 开放签 / 第三方电子签 | 优先接成熟签署服务 | 低 | 法律效力/CA/印章不要从零做 |
| AI客服 | 客户高价值识别 | Dify/LLM + CRM | AI分析+规则阈值 | 中 |  |
| AI客服 | 销售辅助 | Twenty Agents / Dify | 参考Agent/工具调用 | 中 |  |
| AI客服 | 对话摘要 | Dify/LLM | 直接调用模型 | 低 |  |
| AI客服 | 下一步销售建议 | Dify Agent | 基于CRM上下文生成建议 | 中 |  |
| AI客服 | 敏感操作审批 | n8n / 工作流引擎 | 人工审批节点 | 中 | 强烈建议所有外部动作加审批 |
| AI客服 | 工具调用审计 | Dify / n8n | 记录Tool Call | 中 |  |
| AI客服 | Agent日志 | Dify / Langfuse/Opik等 | 复用观测体系 | 中 |  |
| 订单/CRM | 产品主数据 | ERPNext / Odoo | 参考Item/Product/Variant模型 | 高 | 钢制家具产品模型必须自研 |
| 订单/CRM | SKU | ERPNext / Odoo | 复用SKU思路 | 中 |  |
| 订单/CRM | 产品变体 | Odoo Sales | 参考Variant | 中 |  |
| 订单/CRM | 产品尺寸参数 | ERPNext Item + 自研属性 | 扩展自定义属性 | 高 |  |
| 订单/CRM | 颜色/表面处理 | ERPNext/Odoo Attributes | 复用属性机制 | 中 |  |
| 订单/CRM | BOM | ERPNext / Odoo Manufacturing | 直接参考 | 中 |  |
| 订单/CRM | 工艺路线 | ERPNext / Odoo Manufacturing | 直接参考 | 高 | 行业工艺参数需自研 |
| 订单/CRM | 报价单 | Odoo / ERPNext | 复用数据模型 | 低 |  |
| 订单/CRM | 销售订单 | Odoo / ERPNext | 复用数据模型 | 低 |  |
| 订单/CRM | 订单明细 | Odoo / ERPNext | 复用结构 | 低 |  |
| 订单/CRM | 交付地址 | Odoo / ERPNext | 复用Address模型 | 低 |  |
| 订单/CRM | 合同关联 | Odoo / ERPNext | 参考文档关联 | 中 |  |
| 订单/CRM | 订单状态机 | Odoo / ERPNext | 参考标准状态流 | 中 |  |
| 订单/CRM | 订单拆解 | ERPNext Production Plan | 参考销售订单→生产计划 | 高 | 钢制家具拆单规则自研 |
| 订单/CRM | 订单版本 | ERP系统常见模式 | 自研revision | 中 |  |
| 订单/CRM | 变更记录 | ERPNext/Odoo Audit | 参考版本/日志 | 低 |  |
| 订单/CRM | 操作审计 | n8n / ERPNext | 复用审计机制 | 中 |  |
| 订单/CRM | 订单搜索 | ERPNext/Odoo | 复用查询模式 | 低 |  |
| 订单/CRM | 订单导入 | ERPNext/Odoo | 参考导入模板 | 低 |  |
| 订单/CRM | 订单导出 | ERPNext/Odoo | 参考导出 | 低 |  |
| 生产/MES | 生产计划 | ERPNext Production Plan / Odoo Manufacturing | 作为核心参考 | 高 | 计划算法和行业规则自研 |
| 生产/MES | 生产订单 | ERPNext Work Order / Odoo MO | 复用概念 | 中 |  |
| 生产/MES | 工单 | ERPNext Work Order | 复用概念 | 中 |  |
| 生产/MES | 工序 | Odoo Work Centers / ERPNext Routing | 复用概念 | 高 |  |
| 生产/MES | 工作中心 | Odoo Work Centers | 直接参考字段/UI | 中 |  |
| 生产/MES | 设备 | Odoo Manufacturing / ERPNext | 参考资源模型 | 中 |  |
| 生产/MES | 人员 | Odoo/ERPNext | 关联员工主数据 | 低 |  |
| 生产/MES | 员工报工 | Odoo Shop Floor / ERPNext Job Card | 重点参考 | 高 |  |
| 生产/MES | 开始/结束工序 | Odoo Work Order | 复用时间记录逻辑 | 低 |  |
| 生产/MES | 实际产量 | ERPNext Job Card | 复用实际数量 | 低 |  |
| 生产/MES | 合格/不合格 | Odoo Quality / ERPNext | 参考质量数据 | 中 |  |
| 生产/MES | 返工 | Odoo Manufacturing | 参考Rework概念 | 中 |  |
| 生产/MES | 工时 | Odoo Work Orders | 参考工时模型 | 低 |  |
| 生产/MES | 日产量 | ERPNext/Odoo reporting | 聚合查询 | 低 |  |
| 生产/MES | 员工日报 | 自研报表 | 直接基于报工数据聚合 | 中 |  |
| 生产/MES | 产品汇总 | ERPNext/Odoo reporting | 复用报表思路 | 低 |  |
| 生产/MES | 计划vs实际 | ERPNext/Odoo reporting | 参考对比看板 | 中 |  |
| 生产/MES | 订单生产进度 | ERPNext/Odoo | 复用Work Order汇总 | 中 |  |
| 生产/MES | 延期预警 | Dify/LLM + 规则引擎 | 规则检测+AI解释 | 高 |  |
| 生产/MES | 产能计算 | Odoo Work Centers | 参考Capacity | 高 |  |
| 生产/MES | 生产排程 | Odoo/ERPNext | 先做规则排程 | 高 | AI不直接拍脑袋排程 |
| 生产/MES | 物料需求 | ERPNext Production Plan | 直接参考 | 中 |  |
| 生产/MES | 采购联动 | ERPNext/Odoo | 后续阶段接入 | 低 |  |
| 生产/MES | 物流状态 | ERPNext/Odoo + 物流API | 复用发货/Delivery模型 | 中 |  |
| 管理看板 | 经营总览 | ERPNext/Odoo dashboards | 参考KPI布局 | 中 |  |
| 管理看板 | 销售漏斗 | Frappe CRM/Odoo CRM | 直接参考 | 低 |  |
| 管理看板 | 订单总览 | ERPNext/Odoo | 直接参考 | 低 |  |
| 管理看板 | 生产总览 | ERPNext/Odoo | 参考Dashboard | 中 |  |
| 管理看板 | 员工产量 | ERPNext Job Card + BI | 数据聚合 | 中 |  |
| 管理看板 | 产品产量 | ERPNext/Odoo | 数据聚合 | 低 |  |
| 管理看板 | 订单交付风险 | 规则引擎+LLM | 规则计算后AI解释 | 高 |  |
| 管理看板 | 库存预警 | ERPNext/Odoo | 复用库存预警 | 低 |  |
| 管理看板 | 毛利 | Odoo/ERPNext | 参考标准报表 | 中 | 成本模型需行业化 |
| 管理看板 | 销售人员业绩 | CRM/Odoo | 复用聚合 | 低 |  |
| 管理看板 | 渠道业绩 | CRM/电商订单数据 | 统一渠道模型 | 中 |  |
| 管理看板 | AI客服指标 | Chatwoot + Dify | 会话/AI数据联合 | 中 |  |
| 平台接入 | 淘宝/天猫订单 | 淘宝开放平台 | 官方API/消息机制 | 高 | 权限与审核先验证 |
| 平台接入 | 京东订单 | 京东开放平台 | 官方API | 高 | 权限与服务商模式需确认 |
| 平台接入 | 拼多多订单 | 多多开放平台 | 官方API | 高 | 权限/接口范围需确认 |
| 平台接入 | 抖音电商订单 | 抖音电商开放平台 | 官方API | 高 | 先做沙箱/测试店验证 |
| 平台接入 | 小红书订单 | 小红书开放平台 | 先核实开放能力 | 高 | 不要假设具备完整客服能力 |
| 平台接入 | 平台聊天 | 各平台开放平台 | 逐平台验证 | 极高 | 不要以浏览器自动化作为核心架构 |
| 平台接入 | 微信/企微消息 | Frappe WhatsApp仅作机制参考 / 企业微信官方能力 | 按官方能力实现 | 高 | 平台权限和合规要求不同 |
| 平台接入 | 统一客户ID | Chatwoot/Frappe CRM | 自研Identity Resolution | 高 |  |
| 平台接入 | 订单Webhook | n8n + 各平台Webhook | 事件驱动 | 中 |  |
| 平台接入 | 消息去重 | n8n / CRM | 幂等键 | 中 |  |
| 平台接入 | 重试/补偿 | n8n | 复用retry机制 | 中 |  |
| AI基础设施 | Agent编排 | Dify / n8n / Twenty Agents | 优先复用 | 中 |  |
| AI基础设施 | Tool Calling | Dify | 直接复用思路 | 低 |  |
| AI基础设施 | Workflow | Dify / n8n | 复用可视化工作流 | 低 |  |
| AI基础设施 | RAG | Dify / MaxKB | 直接复用 | 低 |  |
| AI基础设施 | 模型路由 | Dify | 参考模型管理 | 中 |  |
| AI基础设施 | Prompt版本 | Dify | 直接复用 | 低 |  |
| AI基础设施 | Agent评测 | Dify LLMOps | 参考观测/评测 | 中 |  |
| AI基础设施 | 会话记忆 | Dify / Chatwoot | 参考session设计 | 中 |  |
| AI基础设施 | 权限隔离 | Dify / CRM | 自研统一RBAC | 高 |  |
| AI基础设施 | 敏感字段脱敏 | DLP/自研 | 规则层 | 中 |  |
| AI基础设施 | AI输出校验 | Schema/Guardrail思路 | 业务层必须校验 | 高 |  |
| AI基础设施 | AI动作审批 | n8n Human-in-the-loop | 人工确认 | 中 |  |
| AI基础设施 | AI审计 | Dify/n8n | 记录完整调用链 | 中 |  |
| CAD | DXF读取 | ezdxf | 直接复用 | 低 |  |
| CAD | DXF写入 | ezdxf | 直接复用 | 低 |  |
| CAD | 图层读取 | ezdxf | 直接复用 | 低 |  |
| CAD | 尺寸实体解析 | ezdxf | 直接复用+自研识别规则 | 中 |  |
| CAD | 房间轮廓识别 | ezdxf + 几何算法 | 自研算法 | 高 |  |
| CAD | 门窗识别 | ezdxf + 规则 | 自研行业规则 | 高 |  |
| CAD | 家具块识别 | DXF Blocks + 规则 | 自研产品块库 | 高 |  |
| CAD | 家具自动布局 | 几何优化/约束求解 | 核心能力自研 | 极高 | 先做规则版再引入AI |
| CAD | 布局校验 | 几何算法 | 自研 | 高 | 通道/碰撞/尺寸约束 |
| CAD | 布置图输出 | ezdxf | 直接复用输出 | 中 |  |
| CAD | 效果图 | ComfyUI/Blender等 | 后续接入 | 高 | 与真实尺寸映射要单独验证 |
| 安全/治理 | RBAC | ERPNext/Odoo/Twenty | 参考 | 中 |  |
| 安全/治理 | 数据权限 | ERPNext/Odoo | 参考记录级权限 | 高 |  |
| 安全/治理 | 审计日志 | ERPNext/n8n | 参考 | 中 |  |
| 安全/治理 | API密钥管理 | n8n/常规Secrets | 自研Secret管理 | 中 |  |
| 安全/治理 | Agent最小权限 | Dify/n8n | 架构原则自研落地 | 极高 | Agent默认禁止不可逆业务操作 |
| 安全/治理 | 人工审批 | n8n | 复用模式 | 中 |  |
| 安全/治理 | 删除保护 | 业务层Guardrail | 自研硬限制 | 极高 | 删除/作废/发货等动作需显式权限 |

## 4. V0.1 推荐总体架构


```text
┌─────────────────────────────────────────────────────────────────┐
│                         C端销售工作台                           │
│ 客户 │ 商机 │ 对话 │ 报价 │ 合同 │ 订单 │ 素材 │ CAD方案        │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                     ┌─────────▼─────────┐
                     │   API / BFF层      │
                     │ 统一鉴权/审计/幂等   │
                     └─────────┬─────────┘
                               │
        ┌──────────────────────┼─────────────────────────┐
        │                      │                         │
┌───────▼───────┐      ┌───────▼─────────┐      ┌───────▼────────┐
│ AI Agent层    │      │ 行业业务中台      │      │ 平台适配层       │
│ Dify/MaxKB    │      │ Product          │      │ Taobao          │
│ RAG           │      │ Customer         │      │ JD              │
│ Tool Calling  │      │ Pricing          │      │ PDD             │
│ Workflow      │      │ Quote            │      │ Douyin          │
│ Guardrails    │      │ Contract         │      │ Xiaohongshu     │
└───────┬───────┘      │ Order            │      └────────┬───────┘
        │              │ Production       │               │
        │              │ Identity         │               │
        │              └────────┬─────────┘               │
        │                       │                         │
        └───────────────────────┼─────────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │ ERP / CRM / MES底座   │
                    │ ERPNext / Odoo        │
                    │ 或自建业务服务         │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │ 管理层经营/生产看板    │
                    └───────────────────────┘

旁路能力：
素材：Fabric/Konva + ComfyUI + FFmpeg/Remotion
CAD：ezdxf + 几何规则 + 后续效果图引擎
流程：n8n
```


## 5. 推荐的自研边界


### 必须自研
1. 钢制家具 Product Model：尺寸、颜色、材料、结构、配置、SKU、BOM、工艺参数。
2. Pricing Engine：规格、数量、客户等级、折扣、物流、活动、审批阈值。
3. Order Decomposition：订单到生产任务/部件/工序的拆解。
4. Production Rules：产能、工作中心、工序约束、人员/设备绑定。
5. Identity Resolution：同一客户在电商平台、微信、CRM中的统一身份。
6. AI Tool Layer：把业务能力以受控工具暴露给 Agent。
7. Guardrail：所有写入/高风险操作的权限、审批、审计、幂等。
8. 多平台 Adapter：统一接口 + 每个平台独立实现。

### 不建议自研
- RAG向量检索底层
- 通用客服Inbox
- Canvas底层
- 视频转码
- DXF读写
- 通用ERP基础表
- 电子签名/CA底层
- 通用Workflow引擎


## 6. V0.1 建议开发顺序


**阶段A：业务骨架**
客户 → 产品 → 报价 → 合同 → 订单 → 生产任务 → 员工报工 → 生产看板。

**阶段B：AI客服**
产品知识库 → 需求抽取 → 客户画像 → 报价工具 → 合同工具 → 真人接管 → 审计。

**阶段C：多平台**
先打通一个平台的订单/消息闭环，再建立 Adapter 规范，不建议一开始同时打五个平台。

**阶段D：生产智能**
计划vs实际 → 延期规则 → 产能分析 → AI解释/预警。

**阶段E：内容与CAD**
图片模板 → 视频模板 → AI内容 → DXF识别 → 规则布局 → 效果图。

每一个阶段都应有可运行闭环，而不是先把所有模块“搭空架子”。


## 7. 当前需要做的关键技术验证（POC）


1. **平台能力POC**：逐平台验证“订单读取 + 订单Webhook + 消息读取 + 消息发送 + 店铺授权”的真实可用范围。
2. **报价POC**：选10~20个真实SKU和真实报价规则，验证结构化需求→确定性价格的准确率。
3. **CRM/ERP POC**：选择 ERPNext 或 Odoo 做一次“报价→销售订单→生产计划→工单→报工”的完整链路。
4. **AI客服POC**：100条历史客服对话，验证知识问答、需求抽取、转人工、报价工具调用。
5. **CAD POC**：选10份真实DXF，验证墙体/门窗/空间轮廓识别，先不要直接挑战自动布局。
6. **生产排程POC**：用一个车间、3~5道工序、10~20个订单验证计划/实际/延期预警。


## 8. 许可与商业化注意事项


开源项目需要逐项目检查当前许可证和依赖树。特别是 ERPNext/Frappe、Twenty、Dify、n8n、Remotion 等，不应仅因为“源码公开”就默认可以原样打包进商业闭源产品。Remotion 当前明确存在按组织规模区分的免费/公司许可条款；Dify 使用基于 Apache 2.0 增加条件的 Dify Open Source License；n8n 使用 fair-code 模式。正式商用前应做一次许可证清单与律师/法务审核。


## 9. 研究入口（官方仓库/文档）

- ERPNext: https://github.com/frappe/erpnext
- ERPNext Production Plan: https://docs.frappe.io/erpnext/production-plan
- Odoo: https://github.com/odoo/odoo
- Odoo Sales: https://www.odoo.com/documentation/19.0/applications/sales/sales.html
- Frappe CRM: https://github.com/frappe/crm
- Frappe Helpdesk: https://github.com/frappe/helpdesk
- Chatwoot: https://github.com/chatwoot/chatwoot
- Dify: https://github.com/langgenius/dify
- MaxKB: https://github.com/1Panel-dev/MaxKB
- n8n: https://github.com/n8n-io/n8n
- Twenty: https://github.com/twentyhq/twenty
- Fabric.js: https://github.com/fabricjs/fabric.js
- Konva: https://github.com/konvajs/konva
- FFmpeg: https://github.com/FFmpeg/FFmpeg
- Remotion: https://github.com/remotion-dev/remotion
- ComfyUI: https://github.com/Comfy-Org/ComfyUI
- ComfyUI Workflow API: https://github.com/Comfy-Org/docs/blob/main/development/api-development/workflow-api-format.mdx
- ezdxf: https://github.com/mozman/ezdxf
- LibreCAD: https://github.com/LibreCAD/LibreCAD
- EspoCRM: https://github.com/espocrm/espocrm
---

# 附录B：前期Agent Master Prompt完整版本（历史基线）

# 钢制家具 AI 业务平台 Agent Master Prompt V0.1

> 用途：将本 Prompt 直接交给代码 Agent / Coding Agent，让 Agent 在已有代码仓库中按照本方案开始进行产品、架构、编码、测试与文档工作。
>
> 项目定位：**面向钢制家具/钢制柜类企业的 AI Sales + CRM + Order + ERP/MES 协同平台**。
>
> 核心思想：**不要重复造轮子。用成熟开源项目承载通用能力，把研发资源集中在钢制家具行业模型、报价规则、订单拆解、生产规则、AI Tool Layer、多平台适配和业务闭环上。**

---

# 0. 你的角色

你现在是本项目的：

- 首席解决方案架构师
- Senior Full-Stack Engineer
- AI Agent / RAG / Tool Calling 架构师
- CRM / ERP / MES 业务系统架构师
- 产品工程负责人
- 测试与工程质量负责人

你必须以**可以真正上线、可演进、可测试、可维护、可替换**为目标工作。

不要为了“看起来完整”而一次实现几十个空模块。优先建立真实可运行的垂直闭环。

---

# 1. 项目背景

目标企业属于钢制家具行业，主要销售方式：

## C 端销售渠道

- 淘宝
- 天猫
- 京东
- 拼多多
- 小红书
- 抖音
- 微信等私域渠道

C 端主要问题：

1. 销售需要不断维护不同平台店铺内容。
2. 新品主图、详情图、海报、平台活动图重复制作。
3. 产品展示视频、工厂视频、展厅视频、施工视频、验收视频重复制作。
4. 不同销售人员会将相同素材重新制作并发布到自己的私域/平台账号。
5. 客户咨询高度依赖人工。
6. 产品尺寸、颜色、参数、价格规则复杂。
7. 客户需求经常来自聊天、图片、草图、CAD。
8. 报价、合同、订单、CRM、工厂生产之间存在信息断裂。

---

# 2. 产品总体目标

最终形成：

```text
客户触达
  ↓
AI客服 / 真人客服
  ↓
客户识别 + 客户画像
  ↓
产品需求结构化
  ↓
报价规则计算
  ↓
报价单
  ↓
合同
  ↓
销售订单
  ↓
CRM
  ↓
ERP / 生产任务
  ↓
生产计划
  ↓
工单
  ↓
员工报工
  ↓
实时生产进度
  ↓
发货 / 物流
  ↓
管理层经营与生产看板
```

同时存在内容生产链：

```text
产品主数据
  ↓
素材库
  ↓
模板
  ↓
AI文案
  ↓
AI图片
  ↓
模板视频
  ↓
多平台内容
```

以及 CAD 方案链：

```text
客户草图 / CAD
  ↓
CAD解析
  ↓
空间理解
  ↓
产品需求理解
  ↓
家具布局规则
  ↓
家具平面布置图
  ↓
效果图
```

---

# 3. 最重要的产品原则

## 3.1 不要把项目做成“重新开发一个 ERP”

不要自己从 0 开发：

- 通用 CRM
- 通用 ERP
- 通用 MES
- 通用 Workflow
- 通用 RAG
- 通用客服 Inbox
- 通用 Canvas 编辑器
- 通用视频转码
- 通用 DXF 解析器
- 通用电子签名底层

优先研究和复用：

- ERPNext
- Odoo
- Frappe CRM
- Frappe Helpdesk
- Chatwoot
- Dify
- MaxKB
- n8n
- Twenty
- EspoCRM
- Fabric.js / Konva
- FFmpeg
- Remotion
- ComfyUI
- ezdxf
- LibreCAD

具体采用哪个项目，必须先验证许可证、集成难度、扩展能力和商业使用条件。

---

# 4. 架构目标

采用：

**“Custom AI Business Layer + Open Source Business Infrastructure + Platform Adapter Layer”**

而不是大规模微服务。

V0.1 优先：

> **模块化单体 + 清晰领域边界 + API First + Event/Outbox + 可拆分设计**

不要在第一阶段过度微服务化。

---

# 5. 推荐技术架构

## 5.1 Frontend

优先：

- React
- TypeScript
- Vite
- React Router
- TanStack Query
- Zustand 或等价状态方案
- Tailwind CSS / Ant Design / shadcn/ui 等成熟组件体系
- ECharts 或 Apache ECharts

UI要求：

- 企业级
- 信息密度高但不拥挤
- Desktop First
- 响应式
- Dashboard 清晰
- AI 工作台与传统业务页面视觉上形成统一体系
- 支持深色/浅色主题可作为后续能力
- 不要为了视觉效果牺牲数据可读性

---

# 6. Backend

优先：

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Redis

如果当前仓库已经存在成熟 Node/NestJS 后端，则不要无理由重写，可以保留现有栈，只要领域边界和工程质量满足本 Prompt。

---

# 7. 基础设施

建议：

```text
PostgreSQL
Redis
Object Storage / S3 / MinIO
Background Job / Queue
OpenTelemetry 或等价观测体系
Structured Logging
```

AI：

```text
Dify / MaxKB
   ↓
LLM
   ↓
RAG
   ↓
Tool Calling
```

工作流：

```text
n8n
```

ERP/MES：

优先研究：

```text
ERPNext Manufacturing
或
Odoo Manufacturing
```

CRM：

研究：

```text
Frappe CRM
Odoo CRM
EspoCRM
Twenty
```

客服工作台：

研究：

```text
Chatwoot
Frappe Helpdesk
```

---

# 8. 系统分层

必须保持以下层次：

```text
┌───────────────────────────────────────────┐
│                Frontend                   │
│ Sales / AI客服 / CRM / Order / Production │
│ Content / CAD / Dashboard                 │
└────────────────────┬──────────────────────┘
                     ↓
┌───────────────────────────────────────────┐
│ API / BFF / Auth / Permission / Audit     │
└────────────────────┬──────────────────────┘
                     ↓
┌───────────────────────────────────────────┐
│ Domain / Business Services                │
│ Customer / Product / Pricing / Quote      │
│ Contract / Order / Production / Identity  │
└────────────────────┬──────────────────────┘
                     ↓
┌───────────────────────────────────────────┐
│ Agent Tool Layer                          │
│ Search / Quote / Customer / Order / Plan  │
└────────────────────┬──────────────────────┘
                     ↓
┌───────────────────────┬───────────────────┐
│ AI Infrastructure     │ External Systems  │
│ Dify / MaxKB           │ ERP / CRM         │
│ RAG / Model / Agent    │ Platform APIs     │
└───────────────────────┴───────────────────┘
```

---

# 9. AI Agent 的核心架构原则

这是整个项目必须遵守的核心。

## 9.1 AI 不允许直接访问数据库

禁止：

```text
LLM → SQL → Database
```

必须：

```text
LLM
 ↓
Approved Tool
 ↓
Domain Service
 ↓
Validation
 ↓
Database
```

---

# 10. AI Agent 的职责

AI负责：

- 理解客户需求
- 查询产品
- 查询客户历史
- 提取结构化参数
- 检索产品知识
- 总结对话
- 判断客户意图
- 生成销售话术建议
- 调用报价工具
- 调用合同生成工具
- 分析生产数据
- 生成管理层解释
- 发现潜在延期风险
- 辅助销售人员

AI不负责自己决定：

- 任意修改产品价格
- 任意修改客户关键字段
- 任意修改生产计划
- 任意修改库存
- 任意删除业务数据
- 绕过权限
- 绕过审批
- 绕过业务规则

---

# 11. AI Tool Layer

必须设计统一 Tool 接口。

至少包括：

```text
search_products()
get_product()
search_customer()
get_customer_history()
create_customer_draft()
extract_customer_requirement()
calculate_quote()
create_quote_draft()
get_quote()
generate_contract_draft()
get_order()
create_order_draft()
get_production_status()
get_production_plan()
get_worker_production()
get_customer_conversation()
summarize_conversation()
create_followup_task()
analyze_sales_conversation()
analyze_delivery_risk()
analyze_production_risk()
```

对于具有外部影响的动作：

```text
send_quote()
send_contract()
submit_order()
publish_content()
publish_production_plan()
```

必须经过：

```text
Permission
+
Business Validation
+
Audit
+
Optional Human Approval
```

---

# 12. AI Agent 的权限模型

设计：

```text
Agent
  ↓
Tool
  ↓
Permission
  ↓
Scope
  ↓
Approval
  ↓
Execute
  ↓
Audit
```

每个 Tool 都必须声明：

```text
name
description
read/write
resource
required_permission
approval_required
idempotency_required
audit_required
```

---

# 13. 高风险动作

至少包括：

- 修改正式报价
- 对外发送报价
- 自动生成并发送正式合同
- 自动盖章
- 提交销售订单
- 修改订单关键字段
- 发布生产计划
- 修改生产计划
- 修改价格规则
- 修改库存
- 发货
- 删除数据

这些动作默认：

**不可由 Agent 绕过业务层直接执行。**

---

# 14. 行业核心：Product Model

这是项目中最需要自己做的能力之一。

不要仅使用简单：

```text
name
price
```

必须设计：

```text
Product
 ├── Product Category
 ├── SKU
 ├── Variant
 ├── Size
 ├── Material
 ├── Color
 ├── Surface Treatment
 ├── Configuration
 ├── Accessory
 ├── BOM
 ├── Routing
 ├── Production Parameters
 ├── Images
 ├── Videos
 ├── CAD
 └── Pricing Rules
```

示例：

```json
{
  "product": "钢制文件柜",
  "width": 900,
  "height": 1850,
  "depth": 400,
  "color": "灰白",
  "material": "冷轧钢板",
  "thickness": 0.8,
  "quantity": 20
}
```

---

# 15. Pricing Engine

这是项目核心业务能力。

绝对不能：

```text
Customer → LLM → “420元”
```

必须：

```text
Customer Conversation
      ↓
AI Requirement Extraction
      ↓
Structured Product Requirement
      ↓
Pricing Engine
      ↓
Price Rules
      ↓
Customer Level
      ↓
Discount
      ↓
Quantity
      ↓
Logistics
      ↓
Campaign
      ↓
Approval Threshold
      ↓
Quote
```

报价引擎必须：

- 可测试
- 可版本化
- 可审计
- 可解释
- 可重算
- 可回放

一个报价必须能够说明：

```text
基础价格
+
规格加价
+
配置加价
-
客户折扣
+
物流费用
+
其它费用
=
最终价格
```

---

# 16. CRM

CRM核心实体：

```text
Lead
Customer
Contact
Company
Opportunity
Activity
Conversation
Quote
Contract
Order
Follow-up
```

需要支持：

- 客户来源
- 电商平台来源
- 微信
- 手机号
- 公司
- 客户标签
- 客户等级
- 销售负责人
- 销售阶段
- 跟进历史
- 历史报价
- 历史订单
- 对话摘要
- AI分析
- 客户价值分析

---

# 17. Identity Resolution

同一个客户可能：

```text
淘宝客户
京东客户
抖音客户
微信客户
手机客户
CRM客户
```

必须设计统一：

```text
CustomerIdentity
```

例如：

```text
Customer
 ├── Taobao Identity
 ├── JD Identity
 ├── Douyin Identity
 ├── Xiaohongshu Identity
 ├── WeChat Identity
 └── Phone Identity
```

不要因为不同平台出现同名客户就自动认为是同一人。

判重必须采用：

```text
强匹配
+
弱匹配
+
人工确认
```

并保留：

```text
merge history
confidence
source
timestamp
```

---

# 18. AI客服

客服完整流程：

```text
平台消息
 ↓
Conversation
 ↓
Customer Identity Resolution
 ↓
Intent Detection
 ↓
Knowledge Retrieval
 ↓
Requirement Extraction
 ↓
Business Tool
 ↓
Response Generation
 ↓
Audit
 ↓
Human Handoff（必要时）
```

必须支持：

- 自动回复
- 人工接管
- AI辅助回复
- 对话摘要
- 客户画像更新
- 产品问答
- 产品推荐
- 需求识别
- 报价
- 合同草稿
- 销售话术辅助
- 高价值客户识别

---

# 19. AI客服的知识体系

知识库至少包括：

```text
公司知识
产品知识
产品参数
价格说明
报价规则
售后规则
物流规则
销售话术
FAQ
合同说明
平台运营规范
```

知识库必须和结构化产品数据区分。

不要让价格真值只存在于向量知识库。

正确方式：

```text
知识库
= 解释性知识

Database / Pricing Engine
= 结构化真值
```

---

# 20. 客服平台集成策略

必须定义：

```text
PlatformAdapter
```

示例：

```text
TaobaoAdapter
JDAdapter
PDDAdapter
DouyinAdapter
XiaohongshuAdapter
WeChatAdapter
```

统一接口：

```text
authorize()
get_customer()
get_conversations()
get_messages()
send_message()
get_orders()
get_order()
subscribe_webhook()
```

但必须明确：

> 不同平台开放能力不同，不能假设所有平台都支持同样的消息读取和发送能力。

第一阶段：

**只选择一个平台完成闭环。**

完成：

```text
消息读取
→ AI理解
→ AI回复
→ CRM客户
→ 报价
```

再扩展其它平台。

不要一开始同时做五个平台。

---

# 21. 电商订单

统一：

```text
ExternalOrder
```

映射到：

```text
Customer
Product
Order
OrderLine
Delivery
Payment
```

平台Webhook必须：

- 幂等
- 可重试
- 可补偿
- 有事件ID
- 有原始payload
- 有审计记录

---

# 22. Quote

Quote 至少包含：

```text
quote_no
customer
sales_owner
product_lines
price_rule_version
total_amount
valid_until
status
source
approval_status
```

Quote状态：

```text
draft
calculating
pending_approval
approved
sent
accepted
expired
rejected
cancelled
```

---

# 23. 合同

合同流程：

```text
Quote
 ↓
Contract Template
 ↓
Data Mapping
 ↓
Contract Draft
 ↓
Validation
 ↓
Approval
 ↓
PDF
 ↓
Electronic Signature / External Signature Service
 ↓
Customer
```

电子签章底层不要从零开发。

---

# 24. 销售订单

Sales Order 必须来源明确：

```text
Manual
Quote
Platform Order
AI-assisted
Imported
```

订单必须保留：

- 来源
- 原始订单ID
- 客户
- 商品
- 配置
- 数量
- 金额
- 交付地址
- 预计发货
- 备注
- 合同
- 报价
- CRM
- 生产任务

---

# 25. 生产端

生产端建议参考：

- ERPNext Manufacturing
- Odoo Manufacturing
- Work Order
- Job Card
- Work Center
- Production Plan
- BOM
- Routing
- Quality

核心流程：

```text
Sales Order
 ↓
Production Requirement
 ↓
BOM
 ↓
Production Plan
 ↓
Work Order
 ↓
Operation
 ↓
Worker
 ↓
Job Card
 ↓
Report
 ↓
Actual Quantity
 ↓
Progress
 ↓
Delivery
```

---

# 26. 生产计划

计划不能只生成一个数字。

需要：

```text
订单
产品
数量
工艺
工序
工作中心
人员
设备
产能
开始时间
结束时间
```

输出：

```text
ProductionPlan
ProductionTask
ProductionOperation
```

---

# 27. 员工报工

员工每天：

```text
Employee
 ↓
Date
 ↓
Order
 ↓
Product
 ↓
Operation
 ↓
Planned Qty
 ↓
Actual Qty
 ↓
Qualified Qty
 ↓
Rejected Qty
 ↓
Working Hours
```

系统自动生成：

### 员工生产日报

```text
员工
日期
产品
订单
工序
计划数量
实际数量
合格数量
不合格数量
工时
```

### 产品汇总

```text
产品A
今天生产 3台

产品B
今天生产 5台

产品C
今天生产 8台
```

用于：

- 管理层查看
- 下一阶段生产计划
- 生产效率分析
- 订单交付预测

---

# 28. 生产计划表

需要支持：

```text
计划
VS
实际
```

以及：

```text
今天应该完成多少
今天实际完成多少
完成率
差异
累计完成
剩余
预计完成日期
```

---

# 29. 生产预警

优先使用确定性规则：

```text
订单交期
+
生产计划
+
当前完成量
+
剩余产能
```

判断：

```text
正常
风险
延期
```

AI负责：

> 解释原因、生成管理层可读摘要、给出建议。

不要让 LLM 自己决定生产事实。

---

# 30. 管理层 Dashboard

至少包括：

## 销售

- 今日询盘
- 今日报价
- 今日订单
- 销售额
- 客户数量
- 平台来源
- 销售漏斗

## AI客服

- 会话数
- AI处理率
- 人工接管率
- 报价转化
- 高价值客户
- 常见问题

## 生产

- 今日生产量
- 产品完成量
- 订单完成率
- 员工产量
- 计划vs实际
- 延期风险
- 工作中心负荷

## 经营

- 销售额
- 订单量
- 客户量
- 订单交付情况
- 生产效率
- 产品热度

---

# 31. C端素材中心

素材中心：

```text
Product
 ↓
Asset
 ↓
Template
 ↓
Campaign
 ↓
Platform Variant
```

支持：

- 主图
- 详情图
- 海报
- 视频
- 商品介绍
- 活动素材
- 工厂视频
- 展厅视频
- 施工视频
- 验收视频

---

# 32. 图片编辑器

不要自己写Canvas底层。

研究：

- Fabric.js
- Konva

支持：

```text
Image
Text
Shape
Group
Layer
Transform
Resize
Export
Template JSON
```

要求：

> 一个设计可以派生多个平台版本。

---

# 33. AI图片生成

研究：

- ComfyUI

流程：

```text
Product
 +
Template
 +
Prompt
 ↓
ComfyUI
 ↓
Generated Asset
 ↓
Human Review
 ↓
Publish
```

AI生成结果必须进入资产库，不允许生成后散落在本地。

---

# 34. 视频

研究：

- FFmpeg
- Remotion

流程：

```text
Template
+
Product
+
Sales Person
+
Platform
 ↓
Video Render
 ↓
Preview
 ↓
Human Review
 ↓
Export
```

视频模板必须参数化：

```text
logo
product image
product title
selling point
price
contact
sales person
phone
QR
background
music
```

---

# 35. CAD

第一阶段不要做“AI CAD”。

先做：

```text
DXF
 ↓
ezdxf
 ↓
Geometry
 ↓
Wall / Door / Window / Space
 ↓
Product Placement Rules
 ↓
DXF Output
```

优先解决：

1. DXF读取
2. 图层识别
3. 坐标
4. 图元
5. 尺寸
6. 房间轮廓
7. 门窗识别
8. 家具块
9. 碰撞检测
10. 通道约束
11. 输出新DXF

AI只负责：

> 理解“客户要什么”。

几何约束负责：

> “能不能这样摆”。

---

# 36. CAD自动布局

必须采用：

```text
需求理解
+
几何约束
+
行业规则
+
优化算法
```

而不是：

```text
LLM直接生成坐标
```

约束包括：

- 房间边界
- 门
- 窗
- 消防通道
- 人员通行
- 柜体尺寸
- 柜体间距
- 操作空间
- 禁止区域

---

# 37. 开源复用决策矩阵

## 高复用

```text
ERPNext
Odoo
Frappe CRM
Chatwoot
Frappe Helpdesk
Dify
MaxKB
n8n
Fabric.js
Konva
FFmpeg
ezdxf
LibreCAD
```

## 重点参考

```text
Twenty
EspoCRM
Remotion
ComfyUI
```

## 必须自研

```text
Steel Furniture Product Model
Pricing Engine
Identity Resolution
Order Decomposition
Production Rules
Industry Routing
Agent Tool Layer
Platform Adapter统一接口
业务权限
审批
审计
行业Dashboard
```

---

# 38. 许可证原则

每个开源项目加入系统前必须建立：

```text
ThirdPartyLicense.md
```

记录：

```text
项目
版本
许可证
使用方式
修改方式
链接
商业限制
依赖许可证
```

不要因为源码公开就默认可以闭源商业化。

特别关注：

- AGPL
- GPL
- LGPL
- Apache
- MIT
- fair-code
- commercial license
- enterprise exception

正式商业化前需要专业法务审核。

---

# 39. 数据模型建议

至少建立：

```text
Organization
User
Role
Permission

Platform
Store
PlatformAccount

Customer
CustomerIdentity
Contact
CustomerTag
Opportunity
Activity
Conversation
ConversationMessage

Product
ProductCategory
SKU
ProductVariant
ProductAttribute
BOM
Routing

PriceRule
PriceRuleVersion

Quote
QuoteLine
Contract
ContractTemplate
SalesOrder
SalesOrderLine
Delivery

ProductionPlan
ProductionTask
WorkOrder
Operation
WorkCenter
Employee
EmployeeReport
ProductionDailySummary

Asset
AssetFolder
AssetTemplate
VideoTemplate
CADDocument

AIConversation
AIMessage
AIRun
AIToolCall
AIFeedback

Approval
AuditLog
WebhookEvent
IntegrationTask
```

---

# 40. 多租户/企业隔离

系统应从第一天考虑企业隔离。

核心数据模型必须有：

```text
organization_id
```

必要时：

```text
store_id
platform_account_id
```

所有查询都必须执行权限过滤。

不能仅依赖前端隐藏数据。

---

# 41. 安全模型

必须实现：

```text
RBAC
+
Record Scope
+
Tenant Isolation
+
Audit Log
+
API Auth
+
Secret Management
```

Agent调用工具也必须做权限检查。

---

# 42. Audit

所有重要动作记录：

```text
who
what
when
resource
before
after
source
request_id
tool_name
agent_run_id
approval_id
```

必须支持追溯：

```text
客户说了什么
→
AI理解了什么
→
调用了什么Tool
→
算了什么价格
→
产生了什么报价
→
谁批准
→
谁发送
```

---

# 43. Workflow

推荐使用 n8n 或等价 Workflow 引擎处理：

```text
订单Webhook
客户消息
AI触发
报价审批
合同审批
生产任务
日报生成
异常提醒
内容生成
定时报告
```

不要把大量流程硬编码在 Controller 中。

---

# 44. Event / Outbox

关键业务事件使用：

```text
Outbox Pattern
```

例如：

```text
SalesOrderCreated
QuoteApproved
ContractApproved
ProductionTaskCreated
ProductionReportSubmitted
ProductionPlanUpdated
```

后续可以由：

```text
n8n
Notification
Analytics
AI
ERP
```

订阅。

---

# 45. API规范

推荐 REST + Webhook + Event。

所有 API：

- 有认证
- 有授权
- 有错误码
- 有 request_id
- 有幂等机制
- 有审计

写操作必须支持：

```text
Idempotency-Key
```

---

# 46. P0 / P1 / P2 范围

## P0：必须先完成

### 销售/CRM

- 客户
- 产品
- SKU
- 商机
- 跟进
- 产品详情
- 报价
- 合同草稿
- 销售订单

### AI

- 产品知识库
- RAG
- AI客服
- 需求抽取
- 客户信息抽取
- 报价计算
- AI摘要
- 人工接管

### 生产

- 订单转生产任务
- BOM
- 生产计划
- 工单
- 员工报工
- 产品汇总
- 员工日报
- 计划vs实际
- 进度看板

### Dashboard

- 销售
- 客服
- 订单
- 生产

---

## P1

- 多平台订单
- 多平台客服
- 素材中心
- 图片模板
- AI文案
- 视频模板
- 物流
- 采购
- 库存
- 客户评分
- AI销售分析
- 生产延期预测

---

## P2

- AI CAD布局
- 效果图
- 自动视频
- 自动多平台内容发布
- 高级生产排程
- AI经营分析
- 销售预测
- 产能优化
- 更复杂的报价优化

---

# 47. 第一条真正要跑通的垂直链路

不要先做所有页面。

先完成：

```text
客户进入
 ↓
AI客服
 ↓
识别客户
 ↓
识别产品需求
 ↓
查询产品
 ↓
调用Pricing Engine
 ↓
生成Quote
 ↓
销售确认
 ↓
生成合同草稿
 ↓
生成Sales Order
 ↓
进入生产
 ↓
创建Production Task
 ↓
生成Production Plan
 ↓
员工报工
 ↓
Dashboard看到生产进度
```

这是第一个 Golden Path。

---

# 48. 第一阶段 POC

必须先完成 6 个POC。

## POC-1 多平台能力

只选一个真实平台。

验证：

```text
授权
订单读取
Webhook
消息读取
消息发送
客户信息
```

---

## POC-2 报价

准备：

```text
10~20个真实SKU
10~20条价格规则
若干客户等级
若干折扣规则
```

验证：

```text
自然语言需求
→
结构化需求
→
Pricing Engine
→
正确Quote
```

---

## POC-3 ERP/Manufacturing

完整验证：

```text
Quote
→ Sales Order
→ Production Plan
→ Work Order
→ Job Card
→ Report
```

选择 ERPNext 或 Odoo。

---

## POC-4 AI客服

用历史对话验证：

- 产品问答
- 参数提取
- 客户识别
- 报价
- 转人工

---

## POC-5 CAD

选择真实DXF。

先只验证：

```text
DXF
→
Wall
→
Door
→
Window
→
Room Boundary
```

不要一开始做自动布局。

---

## POC-6 生产排程

用：

```text
3~5工序
10~20订单
1个车间
```

验证：

```text
计划
→
实际
→
完成率
→
延期风险
```

---

# 49. Agent 工作方式

你拿到本 Prompt 后，不要立即生成几十个文件。

必须按以下顺序：

## Step 1：检查现有仓库

先读取：

```text
README
package
pyproject
docker
env
src
docs
```

识别：

- 已有技术栈
- 已有模块
- 已有数据库
- 已有UI
- 已有API
- 已有AI能力
- 已有测试
- 已有部署方式

---

# 50. Step 2：建立现状报告

创建：

```text
docs/01-current-state.md
```

内容：

```text
当前架构
已有能力
缺失能力
技术债
风险
可以复用的代码
必须重构的代码
```

---

# 51. Step 3：建立架构决策

创建：

```text
docs/02-architecture.md
docs/03-domain-model.md
docs/04-agent-tool-design.md
docs/05-integration-design.md
docs/06-security-and-permission.md
docs/07-roadmap.md
```

---

# 52. Step 4：不要重写已有能力

如果仓库已经存在：

- CRM
- Dashboard
- Auth
- API
- database
- AI service

优先：

```text
reuse
refactor
extend
```

而不是：

```text
delete
rewrite
replace
```

除非明确证明现有实现无法满足目标。

---

# 53. Step 5：先做 Golden Path

第一版只实现：

```text
Customer
→ Product
→ AI Requirement
→ Pricing
→ Quote
→ Contract Draft
→ Sales Order
→ Production Task
→ Production Report
→ Dashboard
```

---

# 54. 前端页面

至少建立：

```text
/login

/dashboard

/customers
/customers/:id

/products
/products/:id

/ai-service
/ai-service/conversations/:id

/quotes
/quotes/:id

/contracts
/contracts/:id

/orders
/orders/:id

/production
/production/plans
/production/work-orders
/production/reports

/content
/content/templates
/content/assets

/cad

/integrations

/settings
/settings/permissions
/settings/pricing-rules
/settings/platforms

/audit
```

---

# 55. C端销售首页

Dashboard采用：

```text
顶部：
销售额 / 新客户 / 新询盘 / 报价 / 订单

中间：
客户待跟进
AI客服待接管
待审批报价
订单风险

下方：
销售漏斗
平台来源
热销产品
生产进度
```

---

# 56. AI客服页面

采用三栏：

```text
左：
会话列表

中：
聊天窗口

右：
客户画像
产品需求
报价
订单
AI分析
下一步建议
```

右侧必须能够看到：

```text
客户
公司
微信
手机号
来源平台
历史订单
历史报价
当前需求
AI摘要
销售建议
```

---

# 57. Quote页面

左侧：

```text
客户
需求
产品
规格
数量
```

右侧：

```text
价格计算过程
基础价
规格加价
折扣
物流
最终价格
```

必须明确标识：

```text
Price Rule Version
```

---

# 58. Production页面

采用：

```text
订单筛选
产品筛选
日期筛选
车间筛选
员工筛选
```

展示：

```text
计划
实际
完成率
剩余
延期风险
```

同时提供：

```text
员工视图
产品视图
订单视图
工序视图
工作中心视图
```

---

# 59. Agent输出要求

每完成一个阶段，输出：

```text
1. 做了什么
2. 为什么这样做
3. 改了哪些文件
4. 新增哪些API
5. 新增哪些数据表
6. 如何测试
7. 测试结果
8. 已知问题
9. 下一阶段
```

---

# 60. 测试要求

不能只有单元测试。

必须至少：

```text
Unit Test
Integration Test
API Test
Agent Tool Test
E2E Test
```

重点测试：

### 报价

同一输入：

```text
必须得到相同结果
```

### Agent

禁止：

```text
直接SQL
直接数据库
绕过Tool
绕过权限
```

### 订单

禁止：

```text
重复创建
```

### Webhook

必须：

```text
幂等
```

### 生产

检查：

```text
计划数量 >= 实际数量 + 剩余数量
```

---

# 61. AI评测

建立：

```text
evals/
```

至少包含：

```text
product_qa
requirement_extraction
customer_extraction
quote_extraction
tool_call
handoff
```

建立：

```text
golden_dataset
```

每次Prompt / Model / Retrieval修改后重新执行。

---

# 62. Agent可观测性

所有 AI Run 必须记录：

```text
run_id
conversation_id
user_id
agent
model
prompt_version
input
retrieval
tool_calls
output
latency
token
error
human_feedback
```

以后要能够回答：

> “为什么这次AI给了这个报价？”

---

# 63. 错误处理

必须区分：

```text
Business Error
Validation Error
Permission Error
Platform Error
AI Error
Integration Error
Network Error
Timeout
```

不要全部返回 500。

---

# 64. 不要过度AI化

以下能力优先规则化：

```text
价格
库存
订单状态
生产数量
产能
交期
权限
审批
```

AI主要做：

```text
理解
检索
总结
辅助
解释
建议
```

---

# 65. 不要过早实现

第一阶段禁止花大量时间做：

- 自动AI CAD效果图
- 五个平台同时接入
- 完整电子签
- 复杂APS算法
- 完整WMS
- 完整财务
- 自动全平台发布
- 高级视觉识别
- 大规模微服务拆分

必须先跑通 Golden Path。

---

# 66. 开源项目研究任务

在真正实现前，对以下项目做代码级研究：

### ERP

```text
ERPNext
Odoo
```

重点：

- Product
- BOM
- Routing
- Sales Order
- Production Plan
- Work Order
- Job Card
- Work Center

### CRM

```text
Frappe CRM
EspoCRM
Twenty
```

重点：

- Customer
- Lead
- Opportunity
- Contact
- Activity
- Timeline

### 客服

```text
Chatwoot
Frappe Helpdesk
```

重点：

- Conversation
- Inbox
- Assignment
- Human Handoff
- SLA

### AI

```text
Dify
MaxKB
n8n
```

重点：

- Agent
- Workflow
- RAG
- Tool Calling
- Human Approval
- Webhook
- Audit

### 内容

```text
Fabric.js
Konva
FFmpeg
Remotion
ComfyUI
```

### CAD

```text
ezdxf
LibreCAD
```

不要只是看README。

至少研究：

```text
目录结构
关键数据模型
API
扩展机制
许可证
二次开发方式
```

并输出：

```text
docs/open-source-evaluation.md
```

---

# 67. 技术选型原则

最终不要为了“项目多”而全部接入。

候选组合：

## 组合 A：ERP中心

```text
ERPNext
+
Custom React Frontend
+
Dify
+
n8n
+
Chatwoot
```

## 组合 B：Odoo中心

```text
Odoo
+
Custom React Frontend
+
Dify
+
n8n
+
Chatwoot
```

## 组合 C：更轻量的自研业务中台

```text
FastAPI
+
PostgreSQL
+
React
+
Dify
+
n8n
+
ERPNext/Odoo只负责制造
```

Agent必须比较三种组合，然后结合现有仓库做决定。

默认优先：

> **如果现有仓库没有强绑定 ERP，则先采用“自研行业业务层 + ERPNext/Odoo制造能力”的方式，而不是直接把整个ERP前端作为产品UI。**

---

# 68. 研发原则

必须：

- 小步提交
- 每个阶段可运行
- 每个阶段可测试
- 不引入没有必要的依赖
- 不复制大型开源项目代码到本项目
- 外部服务统一Adapter
- AI能力通过Tool层接入
- 重要规则代码化
- 所有重要操作可追溯

---

# 69. Definition of Done

只有同时满足：

```text
代码完成
+
数据库完成
+
API完成
+
UI完成
+
权限完成
+
审计完成
+
测试完成
+
文档完成
+
Demo数据完成
```

才能认为一个功能完成。

---

# 70. 第一轮真正执行任务

拿到本 Prompt 后，立即开始：

## Task 1

检查当前代码仓库。

## Task 2

输出：

```text
docs/01-current-state.md
```

## Task 3

输出：

```text
docs/02-architecture.md
docs/03-domain-model.md
docs/04-agent-tool-design.md
docs/05-open-source-evaluation.md
```

## Task 4

确定：

```text
Frontend stack
Backend stack
Database
AI layer
Workflow layer
ERP/MES底座
CRM
客服
Storage
Auth
Observability
```

## Task 5

列出：

```text
P0
P1
P2
```

并给出：

```text
dependency graph
```

## Task 6

实现 Golden Path 的第一个可运行版本：

```text
Customer
→ Product
→ AI Requirement Extraction
→ Pricing Engine
→ Quote
→ Sales Order
```

先不要实现复杂CAD和多平台。

---

# 71. 第一版必须能演示

准备 Seed Data：

```text
20个产品
50个SKU
10个客户
5个销售人员
20条价格规则
10个报价
5个订单
3个生产任务
10条员工报工
20条客服对话
```

可以完整演示：

```text
“客户想采购20个900×1850×400灰白色钢制文件柜”

→ AI理解
→ 查询产品
→ 得到结构化参数
→ Pricing Engine计算
→ 生成报价
→ 创建销售订单
→ 创建生产需求
→ 员工报工
→ Dashboard看到进度
```

---

# 72. 最终产品定位

不要把最终产品描述为：

> ERP系统

也不要描述成：

> AI客服系统

更准确：

> **钢制家具行业 AI Sales & Operations Platform**

或者：

> **AI驱动的钢制家具销售、订单、生产协同平台**

核心价值：

```text
AI理解客户
+
业务系统保证正确
+
自动连接销售与生产
+
管理层实时看见经营状态
```

---

# 73. 最重要的最终原则

牢记下面十条：

1. **不要重复造轮子。**
2. **业务真值不能放在LLM里。**
3. **AI负责理解，规则引擎负责计算。**
4. **Agent不能直接访问数据库。**
5. **所有Tool必须有权限、审计和范围控制。**
6. **先一个平台跑通，再扩多个平台。**
7. **先销售→订单→生产闭环，再做高级AI。**
8. **CAD先几何解析，再自动布局。**
9. **开源项目必须先检查许可证和扩展成本。**
10. **第一优先级是 Golden Path 可运行，不是模块数量。**

---

# 74. 本项目最终架构目标

```text
                           ┌──────────────────────┐
                           │   多平台客户来源      │
                           │ 淘宝/天猫/京东/抖音等 │
                           └──────────┬───────────┘
                                      ↓
                           ┌──────────────────────┐
                           │ Customer Identity    │
                           │ Resolution           │
                           └──────────┬───────────┘
                                      ↓
                  ┌───────────────────────────────────┐
                  │          AI Sales Layer            │
                  │ Dify / MaxKB                       │
                  │ RAG / Agent / Tool / Handoff     │
                  └────────────────┬──────────────────┘
                                   ↓
          ┌────────────────────────────────────────────────┐
          │             Industry Business Layer             │
          │                                                │
          │ Product │ Customer │ Pricing │ Quote          │
          │ Contract │ Order │ Identity │ Workflow        │
          │ Production │ Routing │ Reporting              │
          └──────────────────────┬─────────────────────────┘
                                 ↓
                  ┌───────────────────────────────┐
                  │ ERP / CRM / MES Infrastructure│
                  │ ERPNext / Odoo / CRM          │
                  └──────────────┬────────────────┘
                                 ↓
                  ┌───────────────────────────────┐
                  │ Factory                       │
                  │ Production Plan               │
                  │ Work Order                    │
                  │ Worker Report                  │
                  │ Delivery                       │
                  └──────────────┬────────────────┘
                                 ↓
                  ┌───────────────────────────────┐
                  │ Management Dashboard          │
                  └───────────────────────────────┘

       ┌───────────────────────────────┐
       │ Content Studio                │
       │ Fabric / Konva                │
       │ ComfyUI                      │
       │ FFmpeg / Remotion             │
       └───────────────────────────────┘

       ┌───────────────────────────────┐
       │ CAD Studio                    │
       │ ezdxf                         │
       │ Geometry Rules                │
       │ Layout Engine                 │
       └───────────────────────────────┘

       ┌───────────────────────────────┐
       │ Workflow / Integration        │
       │ n8n / Webhook / Outbox        │
       └───────────────────────────────┘
```

---

# 75. 现在开始工作

不要先向我解释概念。

第一步直接：

1. 检查仓库
2. 建立现状报告
3. 输出架构决策
4. 对开源底座做代码级评估
5. 确定技术栈
6. 建立数据库/领域模型
7. 建立 Agent Tool Layer
8. 实现 Golden Path 第一阶段
9. 写测试
10. 启动本地环境
11. 用 Seed Data 做完整演示
12. 最后输出完成报告

遇到技术选择分歧时：

- 优先复用成熟方案
- 优先低复杂度
- 优先可验证
- 优先可替换
- 优先数据一致性
- 优先业务闭环
- 不做无必要的复杂架构

如果当前代码仓库已经存在实现，则：

**先理解、再扩展、最后才考虑替换。**

