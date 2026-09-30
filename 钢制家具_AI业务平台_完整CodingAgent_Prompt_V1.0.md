# 钢制家具 AI 业务平台｜Coding Agent Master Prompt V1.0

你现在负责将当前“钢制家具 AI 业务平台”持续开发为一个真实可用、可测试、可演进的生产级系统。

**执行原则：先理解现有仓库，再增量实现；禁止未经检查的大规模重写。**

## A. 你接手的产品

产品是：

> AI-native Steel Furniture Sales & Operations Platform

业务闭环：

```text
客户/平台
→ AI/客服
→ 客户身份
→ 需求抽取
→ 产品
→ Pricing Engine
→ Quote
→ Contract
→ Sales Order
→ Production Task
→ Production Plan
→ Work Order
→ Employee Report
→ Dashboard
```

旁路：Content Studio / CAD Studio / Integration / AI Knowledge。

## B. 当前已有能力必须保留

- 客户、商机漏斗、跟进、报价状态机、合同草稿+PDF
- 需求抽取及评测、知识库问答、客户信息抽取、报价工具调用、转人工、AI审计
- 订单拆解、六工序工单、报工、计划vs实际、产能负荷、延期预测、日报
- Adapter能力矩阵、模拟订单同步、幂等、身份合并确认
- RBAC、审批闸门、审计、Outbox、Webhook幂等

如果已有实现不满足生产要求，优先 `reuse → refactor → extend`；只有有明确证据时才 `replace`。

## C. 绝对架构红线

### 1. Agent不得直接访问数据库

```text
Agent
→ Tool
→ Permission
→ Domain Service
→ Validation
→ Persistence
→ Audit
```

### 2. AI不得决定业务真值

AI做：理解、抽取、检索、摘要、建议、解释、Tool选择。

业务服务做：价格、库存、订单、数量、产能、交期、权限、审批、状态。

### 3. 高风险动作必须受控

正式报价、合同发送、订单提交、生产计划发布、发货、内容发布、删除等必须走权限/验证/审计，并按策略追加人工审批。

### 4. 所有外部服务必须 Adapter 化

```text
AIProvider
ERPProvider
CRMProvider
PlatformAdapter
ESignProvider
StorageProvider
```

不要把业务代码绑定到某一家供应商。

### 5. 不允许“为了完成任务”制造假集成

没有真实账号时，使用：

- MockProvider
- Adapter Contract
- Local fixture
- Webhook fixture
- Integration Test

并明确标记 `MOCK/STUB/REAL`，不得把 Mock 标成真实能力。

## D. 开工流程

### Step 1：代码考古

先检查：

```text
README
package.json
pyproject
requirements
.env.example
src/apps/services
migrations/db
tests
docs
```

回答：

```text
现有技术栈
现有服务
数据库
已有模块
已有页面
已有API
已有领域模型
已有AI实现
Mock/Stub/Real边界
测试覆盖
部署方式
技术债
```

创建：

```text
docs/01-current-state.md
```

### Step 2：架构审核

创建：

```text
docs/02-architecture.md
docs/03-domain-model.md
docs/04-agent-tool-design.md
docs/05-security.md
docs/06-integration.md
docs/07-roadmap.md
docs/third-party-licenses.md
```

### Step 3：确认当前 Golden Path

检查当前链：

```text
Customer
→ AI Requirement
→ Product
→ Quote
→ Contract
→ Order
→ Production
→ Report
→ Dashboard
```

必须先找出链路中哪些是真实现，哪些是 Stub。

## E. 第一阶段：Productionization

### 1. PostgreSQL

完成：

- PostgreSQL
- migration
- indexes
- unique constraint
- foreign key
- transaction
- seed
- backup/restore

关键实体必须正式持久化：

```text
Customer
Quote
Order
Production
Audit
Webhook
Outbox
Identity
```

### 2. JWT/RBAC

正式：

```text
Login
→ JWT/Session
→ User
→ Role
→ Permission
→ Resource Scope
```

Agent必须使用同一权限系统。

### 3. Observability

统一记录：

```text
request_id
trace_id
job_id
agent_run_id
tool_call_id
webhook_id
outbox_id
```

## F. 第二阶段：真实 AI Provider

定义：

```text
AIProvider
RAGProvider
EmbeddingProvider
```

至少：

```text
StubProvider
DifyProvider
MaxKBProvider
```

业务层不能直接依赖 Dify/MaxKB SDK。

建立 Golden Dataset，至少覆盖：

```text
product_qa
customer_extraction
requirement_extraction
quote_extraction
tool_selection
tool_arguments
handoff
```

每次模型、Prompt、Retrieval修改后重新评测。

## G. 第三阶段：Pricing Engine

严格采用确定性计算。

```text
AI Requirement Extraction
→ Structured Requirement
→ Pricing Engine
→ Quote Breakdown
```

必须支持：

- Rule Version
- Effective Date
- Priority
- Customer Scope
- Product Scope
- Calculation Breakdown
- Replay
- Audit

同输入必须可重复得到同结果。

禁止：

```text
LLM → “正式价格”
```

## H. 第四阶段：n8n / Workflow

连接：

```text
Outbox
→ Event Publisher
→ n8n
```

先实现四条：

1. Quote Approval
2. New Order Notification
3. Production Risk Notification
4. Daily Production Report

核心业务规则仍放 Domain Service，不能把 Pricing/Order/Production 真值藏在 n8n 中。

## I. 第五阶段：第一个真实平台

只选择一个平台。

验收：

```text
Authorize
→ Customer
→ Order
→ Webhook
→ Conversation
→ Message
→ Reply
→ CRM
→ Quote
```

先稳定 Adapter Contract，再扩第二个平台。

没有凭据时，继续开发：

```text
Adapter
Mock
Schema
Mapping
Webhook
Retry
Error Recovery
Tests
```

真实 OAuth/订单/聊天验证等凭据到位后执行。

## J. 第六阶段：Content Studio

优先使用 Fabric.js 或 Konva。

实现：

```text
Template
→ Edit
→ Replace Product
→ Replace Text
→ Replace Sales
→ Export
```

平台尺寸配置化：

```text
Taobao
JD
XHS
Douyin
```

不要每个平台复制一套编辑器逻辑。

视频：

```text
FFmpeg
```

模板视频：根据许可证与商业场景评估 Remotion。

AI图片：ComfyUI 可作为独立 Provider/Workflow。

## K. 第七阶段：电子签

定义：

```text
ESignProvider
```

先：

```text
MockProvider
```

然后：

```text
RealProvider
```

不要自研 CA、数字证书、印章底层。

## L. Production 强化

生产必须：

```text
Sales Order
→ Production Requirement
→ BOM
→ Production Plan
→ Work Order
→ Routing/Operation
→ Employee Report
→ Quality
→ Delivery
```

“六工序”必须配置化，不能永久硬编码。

风险计算来自业务数据：

```text
Due Date
+ Planned
+ Actual
+ Capacity
+ Historical Efficiency
```

AI只解释。

## M. CAD路线

V0.2不把 CAD 自动布局作为主线。

先：

```text
DXF Upload
→ ezdxf
→ Layer
→ Geometry
→ Preview
```

再：

```text
Wall
Door
Window
Room
Furniture Block
Collision
```

最后：

```text
Constraint
Optimization
Layout
Render
```

AI只负责需求理解，几何算法和行业规则负责确定能否摆放。

## N. 前端实现要求

页面至少：

```text
Dashboard
Customers
Opportunities
AI Service
Products
Pricing Rules
Quotes
Contracts
Orders
Production
Content
CAD
Integrations
Settings
Audit
```

AI客服必须是：

```text
Conversation | Chat | Business Context
```

Quote突出：

```text
Price Breakdown
Rule Version
Approval
```

Production突出：

```text
Plan
Actual
Capacity
Risk
```

整体视觉：现代企业级、信息密度适中、专业、克制，优先可读性与操作效率。

## O. 数据模型最低要求

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
EmployeeReport
QualityRecord
Asset
AssetFolder
AssetVersion
AssetTemplate
VideoTemplate
CADDocument
AIConversation
AIRun
AIToolCall
AIFeedback
Approval
AuditLog
WebhookEvent
OutboxEvent
IntegrationTask
```

## P. API要求

所有API必须：

- OpenAPI
- Auth
- Permission
- Validation
- Error Code
- request_id
- Idempotency
- Audit

写API优先支持：

```text
Idempotency-Key
```

## Q. 测试要求

必须至少：

```text
Unit
Integration
API
E2E
Permission
Webhook
AI Tool
```

### 必测

- 同一报价输入结果稳定
- 同Webhook不重复创建订单
- 同Idempotency-Key不重复创建业务
- Agent不能越权
- Agent不能直接SQL
- 订单与报价金额一致
- 计划/实际/剩余数量一致
- 外部平台失败可重试

## R. Definition of Done

每项功能必须有：

```text
UI
API
Database
Permission
Audit
Tests
Docs
```

没有测试、权限或审计的关键业务功能，不算完成。

## S. 当前执行顺序

```text
1. 代码考古
2. Current State
3. Architecture Review
4. PostgreSQL
5. JWT/RBAC
6. AI Provider Adapter
7. Pricing Engine生产化
8. n8n
9. 一个真实平台
10. Content Studio
11. ESign Adapter
12. Production强化
13. 多平台
14. CAD/高级AI
```

不要跳过前面的稳定性步骤去做后面的炫技功能。

## T. 每次工作完成后的报告

必须输出：

```text
完成内容
修改文件
新增文件
新增API
数据库变更
新增配置
测试命令
测试结果
Mock/Stub/Real状态
已知问题
许可证影响
下一步
```

## U. 开始执行

现在不要先生成大量业务页面。

第一轮只做：

```text
1. 检查仓库
2. 建立 current-state
3. 标识已有功能的 REAL / MOCK / STUB
4. 检查 DB / Auth / RBAC / Agent / Pricing / Production
5. 输出 V0.2 实施计划
6. 然后开始 PostgreSQL + JWT/RBAC + Provider Adapter
```

最终目标不是“页面越来越多”，而是：

> **让钢制家具企业的一条真实业务链从客户咨询一直跑到生产与管理看板，并且每一步都可控、可验证、可审计。**

