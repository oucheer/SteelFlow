# Domain Model

核心持久化实体包括 Organization、User、Role、Customer、Activity、Product、SKU、PriceRule、Conversation、Quote、Contract、SalesOrder、ProductionPlan、WorkOrder、EmployeeReport、Approval、AuditLog、OutboxEvent、Idempotency 和 WebhookEvent。

价格规则版本、报价输入快照和计算明细一起保存，支持 replay。生产工序来自 Product.routing 种子配置，可继续配置化；看板完成数量只读取计划最后工序的 `qualified`。
