# Security

- JWT 关联数据库 LoginSession，支持退出时撤销，令牌有效期 8 小时。
- 角色权限和组织范围在数据库读取；每个查询自动限制 `org_id`。
- 高风险报价发送、订单提交、生产发布需要审批；申请人不能自批，资源版本变化会使审批失效。
- 所有关键写入写入 AuditLog 和 OutboxEvent；写接口要求 Idempotency-Key。
- Webhook 使用 HMAC-SHA256、大小限制、事件唯一约束和最多三次重试。
- 示例密钥和数据库密码只写入被忽略的 `.env`，不进入仓库。
