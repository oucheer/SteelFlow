# Architecture

采用 FastAPI + SQLAlchemy + PostgreSQL 的模块化单体。浏览器只调用 `/api/v1`，所有写入在领域 Service 中执行。

```text
React UI -> FastAPI API -> Auth/RBAC -> Domain Service -> SQLAlchemy/PostgreSQL
                                      |-> AuditLog
                                      |-> OutboxEvent
                                      |-> Mock/Provider Adapter
```

Agent 只能调用声明式 Tool。Tool 经同一 RBAC、领域校验、事务、幂等和审计路径，不能直接使用数据库连接。
