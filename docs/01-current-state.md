# Current State

本仓库从空目录开始，未发现可复用的业务代码、数据库、认证、AI、生产或页面实现。首轮新增能力均为本项目新实现。

| 能力 | 状态 | 说明 |
| --- | --- | --- |
| PostgreSQL / migrations | REAL | PostgreSQL 17、Alembic、约束和索引 |
| JWT / RBAC / tenant | REAL | 同组织隔离，角色权限在数据库 |
| CRM / products / pricing | REAL | 持久化、确定性报价、规则回放 |
| AI extraction | MOCK | 本地规则 Provider，审计中保留 MOCK |
| Dify / MaxKB | STUB | 仅定义 Provider 边界，未配置外部服务 |
| Platform / webhook | MOCK | 签名、幂等、重试和死信接口可用 |
| Contract PDF | REAL | 本地草稿 PDF；电子签为 STUB |
| n8n / content / CAD | OUT OF SCOPE | 首轮不接入 |
