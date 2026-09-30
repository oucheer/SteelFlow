# Agent Tool Design

每个 Tool 定义 `permission`、`risk_level`、`approval_required`、`idempotency_required`、`audit_required` 和输入输出 schema。首轮 Tools 为产品搜索、需求抽取和报价草稿，Provider 模式显式标为 `MOCK`。

真实模型接入时实现 `DifyProvider` 或 `MaxKBProvider`，不得改变报价、订单和生产领域服务的真值边界。
