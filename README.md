# 钢制家具 AI 业务平台

首轮实现为 React + FastAPI + PostgreSQL 模块化单体，覆盖客户、AI 客服、产品、确定性报价、合同草稿、订单、生产计划、六工序报工、审批、审计和经营看板。

## 本机启动

1. 已安装 PostgreSQL 17 后运行 `scripts/setup-db.ps1`。脚本创建 `steel_business`、低权限 `steel_app` 账号，并将应用连接配置写入被忽略的 `backend/.env`。
2. 安装后端环境并迁移：

```powershell
cd backend
uv sync
uv run alembic upgrade head
uv run python -m app.seed
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

3. 新开终端启动前端：

```powershell
cd frontend
npm install
npm run dev
```

打开 http://127.0.0.1:5173。种子账号为 `admin`，密码保存在 `backend/.env` 的 `SEED_PASSWORD`，不会写进仓库。

## 验证

```powershell
cd backend
uv run pytest
cd ..\frontend
npm run build
```

真实 AI、电商平台、电子签、n8n、CAD 和内容编辑器均未接入，API 健康检查会明确返回 `MOCK`。
