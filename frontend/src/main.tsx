import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Activity,
  BarChart3,
  Bot,
  Boxes,
  CheckCircle2,
  ChevronRight,
  ClipboardList,
  Factory,
  FileText,
  LayoutDashboard,
  LogOut,
  Menu,
  Package,
  Plus,
  Search,
  Settings2,
  ShieldCheck,
  Users,
  X,
} from "lucide-react";
import { api, downloadPdf, Row, setToken } from "./api";
import "./styles.css";
import "./responsive-overrides.css";

type Page =
  | "dashboard"
  | "customers"
  | "ai-service"
  | "quotes"
  | "orders"
  | "production"
  | "products"
  | "channels"
  | "custom"
  | "approvals"
  | "audit";
const nav: { key: Page; label: string; icon: React.ElementType }[] = [
  { key: "dashboard", label: "经营总览", icon: LayoutDashboard },
  { key: "customers", label: "客户 CRM", icon: Users },
  { key: "ai-service", label: "AI 客服", icon: Bot },
  { key: "quotes", label: "报价与合同", icon: FileText },
  { key: "orders", label: "订单管理", icon: ClipboardList },
  { key: "production", label: "生产管理", icon: Factory },
  { key: "products", label: "产品主数据", icon: Package },
  { key: "channels", label: "渠道与素材", icon: Boxes },
  { key: "custom", label: "定制需求", icon: Settings2 },
  { key: "approvals", label: "审批中心", icon: CheckCircle2 },
  { key: "audit", label: "系统审计", icon: ShieldCheck },
];
const fmt = (n: any) => Number(n || 0).toLocaleString("zh-CN");
const money = (n: any) =>
  `¥ ${Number(n || 0).toLocaleString("zh-CN", { minimumFractionDigits: 2 })}`;
const statusLabel = (value: any) =>
  ({ draft: "草稿", pending_approval: "待审批", approved: "已批准", rejected: "已驳回", sent: "已发送", accepted: "已接受", expired: "已过期", cancelled: "已取消", submitted: "已提交生产", published: "已发布", ai: "AI 接待", human: "人工接管", closed: "已完成", pending: "待处理", invalidated: "已失效" } as Record<string, string>)[value] || value || "未设置";

function Login({ onLogin }: { onLogin: (x: any) => void }) {
  const [username, setUsername] = useState("admin"),
    [password, setPassword] = useState(""),
    [error, setError] = useState("");
  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const result = await api("auth/login", "POST", { username, password });
      setToken(result.token);
      onLogin(result.user);
    } catch (err: any) {
      setError(err.message);
    }
  };
  return (
    <main className="login-page">
      <div className="login-art">
        <div className="brand-mark">◇</div>
        <h1>
          钢制家具
          <br />
          <b>AI 业务平台</b>
        </h1>
        <p>让销售、订单与工厂，在同一条数据链上协同。</p>
        <div className="login-art-meta">
          <span>CRM</span>
          <span>AI WORKSPACE</span>
          <span>MES</span>
        </div>
      </div>
      <form className="login-form" onSubmit={submit}>
        <span className="eyebrow">SECURE WORKSPACE</span>
        <h2>欢迎回来</h2>
        <p className="muted">登录你的企业工作空间</p>
        <label>
          账号
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
          />
        </label>
        <label>
          密码
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            placeholder="请输入密码"
          />
        </label>
        {error && <div className="error">{error}</div>}
        <button className="primary wide">
          进入工作台 <ChevronRight size={17} />
        </button>
        <div className="login-note">
          演示账号：<b>admin</b> · 密码写在 backend/.env 的 SEED_PASSWORD 中
        </div>
      </form>
    </main>
  );
}

function Shell({ user, onLogout }: { user: Row; onLogout: () => void }) {
  const [page, setPage] = useState<Page>("dashboard"),
    [collapsed, setCollapsed] = useState(false);
  useEffect(() => {
    const navigate = (event: Event) =>
      setPage((event as CustomEvent<Page>).detail);
    window.addEventListener("app:navigate", navigate);
    return () => window.removeEventListener("app:navigate", navigate);
  }, []);
  return (
    <div className={"app-shell " + (collapsed ? "is-collapsed" : "")}>
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="brand-mark small">◇</div>
          <span>
            钢制家具 <b>AI</b>
            <small>业务平台</small>
          </span>
        </div>
        <div className="workspace-pill">
          <span className="status-dot" /> 演示企业 <ChevronRight size={14} />
        </div>
        <nav>
          {nav.map((item) => {
            const Icon = item.icon;
            return (
              <button
                className={page === item.key ? "active" : ""}
                key={item.key}
                onClick={() => setPage(item.key)}
              >
                <Icon size={17} />
                <span>{item.label}</span>
                {item.key === "ai-service" && <i>3</i>}
              </button>
            );
          })}
        </nav>
        <div className="sidebar-bottom">
          <button onClick={() => setPage("audit")}>
            <Settings2 size={17} />
            <span>系统设置</span>
          </button>
          <button onClick={onLogout}>
            <LogOut size={17} />
            <span>退出登录</span>
          </button>
        </div>
      </aside>
      <main className="main">
        <header>
          <button
            className="icon-btn menu"
            onClick={() => setCollapsed(!collapsed)}
            aria-label="折叠导航"
          >
            <Menu size={19} />
          </button>
          <div className="breadcrumbs">
            <span>工作台</span>
            <ChevronRight size={14} />
            <b>{nav.find((n) => n.key === page)?.label}</b>
          </div>
          <div className="header-actions">
            <span className="sync-dot" /> 数据已同步{" "}
            <div className="avatar">{user?.name?.slice(0, 1) || "管"}</div>
            <span className="user-name">{user?.name}</span>
          </div>
        </header>
        <div className="content">
          {page === "dashboard" && <Dashboard />}
          {page === "customers" && <Customers />}
          {page === "ai-service" && <AIService />}
          {page === "quotes" && <Quotes />}
          {page === "orders" && <Orders />}
          {page === "production" && <Production />}
          {page === "products" && <Products />}
          {page === "channels" && <Channels />}
          {page === "custom" && <CustomRequirements />}
          {page === "approvals" && <Approvals />}
          {page === "audit" && <Audit />}
        </div>
      </main>
    </div>
  );
}

function SectionTitle({
  eyebrow,
  title,
  action,
}: {
  eyebrow?: string;
  title: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="section-title">
      <div>
        {eyebrow && <span className="eyebrow">{eyebrow}</span>}
        <h1>{title}</h1>
      </div>
      {action}
    </div>
  );
}
function Stat({
  label,
  value,
  trend,
  icon,
  color,
}: {
  label: string;
  value: any;
  trend?: string;
  icon: React.ReactNode;
  color: string;
}) {
  return (
    <div className="stat">
      <div className={"stat-icon " + color}>{icon}</div>
      <div>
        <span>{label}</span>
        <strong>{value}</strong>
        {trend && <small className="trend">↗ {trend}</small>}
      </div>
    </div>
  );
}
function Dashboard() {
  const [data, setData] = useState<Row | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    api("dashboard")
      .then(setData)
      .catch((e) => setError(e.message));
  }, []);
  if (error) return <Empty text={error} />;
  if (!data) return <Loading />;
  return (
    <>
      <SectionTitle
        eyebrow="MONITORING CENTER"
        title="经营总览"
        action={<div className="date-chip">实时数据</div>}
      />
      <div className="hero-strip">
        <div>
          <span className="eyebrow">今日业务概览</span>
          <h2>让每一笔订单，都可追溯到工厂。</h2>
          <p>AI 辅助理解需求，业务规则保证每一步准确。</p>
        </div>
        <div className="hero-actions">
          <button
            className="primary"
            onClick={() =>
              window.dispatchEvent(
                new CustomEvent("app:navigate", { detail: "ai-service" }),
              )
            }
          >
            打开 AI 客服 <ChevronRight size={16} />
          </button>
          <button
            className="ghost"
            onClick={() =>
              window.dispatchEvent(
                new CustomEvent("app:navigate", { detail: "production" }),
              )
            }
          >
            查看生产计划
          </button>
        </div>
      </div>
      <div className="stats-grid">
        <Stat
          label="客户总数"
          value={fmt(data.customers)}
          icon={<Users />}
          color="cyan"
        />
        <Stat
          label="报价单"
          value={fmt(data.quotes)}
          icon={<FileText />}
          color="orange"
        />
        <Stat
          label="销售订单"
          value={fmt(data.orders)}
          icon={<ClipboardList />}
          color="purple"
        />
        <Stat
          label="生产计划"
          value={fmt(data.planned)}
          icon={<Factory />}
          color="green"
        />
      </div>
      <div className="dashboard-grid">
        <div className="panel chart-panel">
          <div className="panel-head">
            <div>
              <h3>生产计划进度</h3>
              <span>基于已发布生产计划实时计算</span>
            </div>
            <span className="legend">
              <i />
              已完成 <i className="light" />
              剩余
            </span>
          </div>
          <div className="donut-wrap">
            <div
              className="donut"
              style={
                {
                  "--progress": `${data.completion_rate}%`,
                } as React.CSSProperties
              }
            >
              <div>
                <b>{data.completion_rate}%</b>
                <span>完成率</span>
              </div>
            </div>
            <div className="chart-meta">
              <div>
                <b>{fmt(data.completed)}</b>
                <span>已完成数量</span>
              </div>
              <div>
                <b>{fmt(data.remaining)}</b>
                <span>待生产数量</span>
              </div>
              <div>
                <b>{data.pending_approvals}</b>
                <span>待审批事项</span>
              </div>
            </div>
          </div>
        </div>
        <div className="panel risk-panel">
          <div className="panel-head">
            <div>
              <h3>生产计划与风险</h3>
              <span>计划、实际与交期风险</span>
            </div>
            <button
              className="text-btn"
              onClick={() =>
                window.dispatchEvent(
                  new CustomEvent("app:navigate", { detail: "production" }),
                )
              }
            >
              查看全部 <ChevronRight size={14} />
            </button>
          </div>
          {data.plans.length ? (
            data.plans.slice(0, 4).map((p: any) => (
              <div className="risk-row" key={p.id}>
                <div className="risk-label">
                  <b>{p.id.slice(0, 8).toUpperCase()}</b>
                  <span>{p.due_date} 交付</span>
                </div>
                <div className="progress">
                  <i style={{ width: `${p.completion_rate}%` }} />
                </div>
                <span
                  className={p.risk === "正常" ? "tag success" : "tag warning"}
                >
                  {p.risk}
                </span>
              </div>
            ))
          ) : (
            <Empty text="暂无生产计划" />
          )}
        </div>
      </div>
    </>
  );
}

function Toolbar({
  placeholder = "搜索名称、编号或关键词",
  onSearch,
}: {
  placeholder?: string;
  onSearch: (v: string) => void;
}) {
  return (
    <div className="toolbar">
      <div className="search">
        <Search size={16} />
        <input
          placeholder={placeholder}
          onChange={(e) => onSearch(e.target.value)}
        />
      </div>
    </div>
  );
}
function Table({
  columns,
  rows,
  empty = "暂无数据",
}: {
  columns: {
    key: string;
    label: string;
    render?: (v: any, r: Row) => React.ReactNode;
  }[];
  rows: Row[];
  empty?: string;
}) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            {columns.map((c) => (
              <th key={c.key}>{c.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.length ? (
            rows.map((r, i) => (
              <tr key={r.id || i}>
                {columns.map((c) => (
                  <td key={c.key}>
                    {c.render ? c.render(r[c.key], r) : (r[c.key] ?? "-")}
                  </td>
                ))}
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={columns.length}>
                <Empty text={empty} />
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
function Modal({
  title,
  children,
  onClose,
}: {
  title: string;
  children: React.ReactNode;
  onClose: () => void;
}) {
  return (
    <div
      className="modal-backdrop"
      onMouseDown={(e) => e.target === e.currentTarget && onClose()}
    >
      <section className="modal">
        <div className="modal-head">
          <h2>{title}</h2>
          <button className="icon-btn" onClick={onClose} aria-label="关闭">
            <X size={17} />
          </button>
        </div>
        {children}
      </section>
    </div>
  );
}
function Customers() {
  const [rows, setRows] = useState<Row[]>([]),
    [loading, setLoading] = useState(true),
    [open, setOpen] = useState(false),
    [selected, setSelected] = useState<Row | null>(null),
    [timeline, setTimeline] = useState<Row[]>([]),
    [activity, setActivity] = useState(""),
    [error, setError] = useState("");
  const load = (query = "") => {
    setLoading(true);
    api(`customers?q=${encodeURIComponent(query)}`)
      .then((x) => setRows(x.items))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  };
  const openDetail = async (customer: Row) => {
    try {
      const history = await api(`customers/${customer.id}/timeline`);
      setSelected(customer);
      setTimeline(history);
    } catch (e: any) {
      setError(e.message);
    }
  };
  const addActivity = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!selected || !activity.trim()) return;
    try {
      await api(`customers/${selected.id}/activities`, "POST", { text: activity });
      setActivity("");
      setTimeline(await api(`customers/${selected.id}/timeline`));
    } catch (e: any) {
      setError(e.message);
    }
  };
  useEffect(() => {
    load();
  }, []);
  const create = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const d = new FormData(e.currentTarget);
    try {
      await api("customers", "POST", {
        name: d.get("name"),
        contact: d.get("contact"),
        phone: d.get("phone"),
        source: "manual",
        level: d.get("level"),
      });
      setOpen(false);
      load();
    } catch (e: any) {
      setError(e.message);
    }
  };
  return (
    <>
      <SectionTitle
        eyebrow="SALES / CRM"
        title="客户管理"
        action={
          <button className="primary" onClick={() => setOpen(true)}>
            <Plus size={16} /> 新建客户
          </button>
        }
      />
      <div className="kpi-inline">
        <div>
          <span>全部客户</span>
          <b>{rows.length}</b>
        </div>
        <div>
          <span>本页客户</span>
          <b className="blue">{rows.length}</b>
        </div>
        <div>
          <span>A 级客户</span>
          <b className="orange-text">
            {rows.filter((r) => r.level === "A").length}
          </b>
        </div>
        <div>
          <span>已登记联系人</span>
          <b className="green-text">{rows.filter((r) => r.phone).length}</b>
        </div>
      </div>
      <div className="panel table-panel">
        <Toolbar
          onSearch={(v) => load(v)}
          placeholder="搜索客户名称、联系人或手机号"
        />
        {error && <div className="error">{error}</div>}
        {loading ? (
          <Loading />
        ) : (
          <Table
            rows={rows}
            columns={[
              { key: "name", label: "客户名称", render: (v) => <b>{v}</b> },
              { key: "contact", label: "联系人" },
              { key: "phone", label: "手机号" },
              { key: "source", label: "来源" },
              {
                key: "level",
                label: "客户等级",
                render: (v) => <span className="tag blue-tag">{v}级客户</span>,
              },
              {
                key: "created_at",
                label: "创建时间",
                render: (v) => String(v).slice(0, 10),
              },
              {
                key: "id",
                label: "操作",
                render: (v, r) => (
                  <button className="text-btn" onClick={() => openDetail(r)}>
                    查看详情
                  </button>
                ),
              },
            ]}
          />
        )}
      </div>
      {open && (
        <Modal title="新建客户" onClose={() => setOpen(false)}>
          <form className="form-grid" onSubmit={create}>
            <label>
              客户名称
              <input name="name" required maxLength={120} />
            </label>
            <label>
              联系人
              <input name="contact" required maxLength={80} />
            </label>
            <label>
              联系电话
              <input name="phone" maxLength={30} />
            </label>
            <label>
              客户等级
              <select name="level">
                <option value="B">B 级</option>
                <option value="A">A 级</option>
                <option value="C">C 级</option>
              </select>
            </label>
            {error && <div className="error">{error}</div>}
            <button className="primary">保存客户</button>
          </form>
        </Modal>
      )}
      {selected && (
        <Modal title={`${selected.name} · 客户详情`} onClose={() => setSelected(null)}>
          <div className="customer-detail-head">
            <div><b>{selected.contact}</b><span>{selected.phone || "未登记手机号"} · {selected.level} 级客户</span></div>
            <span className="tag blue-tag">{selected.source === "manual" ? "人工登记" : selected.source}</span>
          </div>
          <form className="activity-form" onSubmit={addActivity}>
            <input value={activity} onChange={(e) => setActivity(e.target.value)} placeholder="记录一次跟进、报价沟通或客户反馈" maxLength={1000} />
            <button className="primary" disabled={!activity.trim()}>记录跟进</button>
          </form>
          <div className="timeline">
            {timeline.length ? timeline.map((item) => (
              <div className="timeline-item" key={`${item.id}-${item.created_at}`}>
                <i />
                <div><b>{item.text || item.action || "业务记录"}</b><span>{String(item.created_at || "").replace("T", " ").slice(0, 19)}</span></div>
              </div>
            )) : <Empty text="暂无客户时间线" />}
          </div>
        </Modal>
      )}
    </>
  );
}
function AIService() {
  const [rows, setRows] = useState<Row[]>([]),
    [selected, setSelected] = useState<Row | null>(null),
    [text, setText] = useState(""),
    [filter, setFilter] = useState("all"),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  const load = async (id?: string) => {
    const list = await api("conversations");
    setRows(list.items);
    const target = id || selected?.id || list.items[0]?.id;
    if (target) {
      const detail = await api(`conversations/${target}`);
      setSelected({
        ...list.items.find((r: Row) => r.id === target),
        ...detail,
      });
    } else setSelected(null);
  };
  useEffect(() => {
    load().catch((e) => setError(e.message));
  }, []);
  const choose = async (r: Row) => {
    try {
      setSelected({ ...r, ...(await api(`conversations/${r.id}`)) });
    } catch (e: any) {
      setError(e.message);
    }
  };
  const send = async () => {
    if (!selected || !text.trim() || busy) return;
    setBusy(true);
    try {
      await api(`conversations/${selected.id}/messages`, "POST", { text });
      setText("");
      await load(selected.id);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  };
  const handoff = async () => {
    if (!selected) return;
    setBusy(true);
    try {
      await api(`conversations/${selected.id}/handoff`, "POST", {});
      await load(selected.id);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  };
  const visible = rows.filter(
    (r) =>
      filter === "all" ||
      (filter === "human" ? r.status === "human" : r.status === "closed"),
  );
  const requirement = selected?.requirement || {};
  return (
    <>
      <SectionTitle
        eyebrow="AI WORKSPACE · MOCK PROVIDER"
        title="AI 客服"
        action={
          <span className="provider-badge">
            <i /> MOCK · 本地规则引擎
          </span>
        }
      />
      {error && <div className="error">{error}</div>}
      <div className="ai-layout panel">
        <div className="conversation-list">
          <div className="tabs">
            <button
              className={filter === "all" ? "tab-active" : ""}
              onClick={() => setFilter("all")}
            >
              全部 <em>{rows.length}</em>
            </button>
            <button
              className={filter === "human" ? "tab-active" : ""}
              onClick={() => setFilter("human")}
            >
              待接管 <em>{rows.filter((r) => r.status === "human").length}</em>
            </button>
            <button
              className={filter === "closed" ? "tab-active" : ""}
              onClick={() => setFilter("closed")}
            >
              已完成
            </button>
          </div>
          <div className="conversation-scroll">
            {visible.map((r) => (
              <button
                className={
                  "conversation-item " +
                  (selected?.id === r.id ? "selected" : "")
                }
                key={r.id}
                onClick={() => choose(r)}
              >
                <div className="contact-avatar">
                  {r.customer_name?.slice(0, 1) || "客"}
                </div>
                <div>
                  <b>{r.customer_name || "未知客户"}</b>
                  <span>{r.last_message?.text || "暂无消息"}</span>
                </div>
                <time>
                  {String(r.last_message?.timestamp || r.created_at || "")
                    .slice(5, 16)
                    .replace("T", " ")}
                </time>
              </button>
            ))}
          </div>
        </div>
        <div className="chat">
          <div className="chat-head">
            <div>
              <b>{selected?.customer_name || "选择一个会话"}</b>
              <span>
                <i />{" "}
                {selected?.status === "human"
                  ? "人工接管"
                  : selected?.status === "closed"
                    ? "已完成"
                    : "AI 自动处理"}
              </span>
            </div>
            <button
              className="ghost"
              disabled={!selected || selected.status === "human" || busy}
              onClick={handoff}
            >
              转人工
            </button>
          </div>
          <div className="messages">
            {selected?.messages?.map((m: any, i: number) => (
              <div
                className={
                  "message " + (m.role === "customer" ? "user" : m.role)
                }
                key={i}
              >
                <div className="message-avatar">
                  {m.role === "assistant" ? "AI" : "客"}
                </div>
                <div>
                  <small>
                    {m.role === "assistant" ? "AI 客服 · MOCK" : "客户"}
                  </small>
                  <p>{m.text}</p>
                </div>
              </div>
            ))}
          </div>
          <div className="composer">
            <input
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && send()}
              placeholder="输入消息，按 Enter 发送"
            />
            <button
              className="send"
              disabled={busy || !selected}
              onClick={send}
            >
              ↗
            </button>
          </div>
        </div>
        <aside className="business-context">
          <h3>业务上下文</h3>
          <div className="context-block">
            <span>客户 · 联系人</span>
            <b>{selected?.customer_name || "未选择"}</b>
            <span>{selected?.customer_contact || ""}</span>
          </div>
          <div className="context-block">
            <span>需求抽取</span>
            {requirement.quantity ? (
              <>
                <b>
                  {requirement.quantity} 件 · {requirement.width}×
                  {requirement.height}×{requirement.depth} mm
                </b>
                <span>
                  {requirement.color} ·{" "}
                  {requirement.configuration === "standard"
                    ? "标准配置"
                    : "加强配置"}
                </span>
              </>
            ) : (
              <em>等待客户描述需求</em>
            )}
          </div>
          <button
            className="primary wide"
            disabled={!selected || !requirement.quantity}
            onClick={() =>
              window.dispatchEvent(
                new CustomEvent("quote:create", {
                  detail: { customer_id: selected?.customer_id, requirement },
                }),
              )
            }
          >
            生成报价草稿
          </button>
          <div className="ai-audit">
            <CheckCircle2 size={16} />
            <span>会话记录与 Tool 调用均由服务端审计</span>
          </div>
        </aside>
      </div>
    </>
  );
}

function Quotes() {
  const [rows, setRows] = useState<Row[]>([]),
    [customers, setCustomers] = useState<Row[]>([]),
    [products, setProducts] = useState<Row[]>([]),
    [open, setOpen] = useState(false),
    [prefill, setPrefill] = useState<Row | null>(null),
    [error, setError] = useState("");
  const load = () =>
    api("quotes")
      .then((x) => setRows(x.items))
      .catch((e) => setError(e.message));
  useEffect(() => {
    load();
    api("customers").then((x) => setCustomers(x.items));
    api("products").then((x) => setProducts(x.items));
    const ev = (e: Event) => {
      setPrefill((e as CustomEvent<Row>).detail);
      setOpen(true);
    };
    window.addEventListener("quote:create", ev);
    return () => window.removeEventListener("quote:create", ev);
  }, []);
  const create = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const d = new FormData(e.currentTarget);
    try {
      await api("quotes", "POST", {
        customer_id: d.get("customer_id"),
        product_id: d.get("product_id"),
        quantity: Number(d.get("quantity")),
        width: Number(d.get("width")),
        height: Number(d.get("height")),
        depth: Number(d.get("depth")),
        color: String(d.get("color")),
        configuration: d.get("configuration"),
      });
      setOpen(false);
      setPrefill(null);
      load();
    } catch (e: any) {
      setError(e.message);
    }
  };
  const act = async (path: string) => {
    try {
      await api(path, "POST", {});
      load();
    } catch (e: any) {
      setError(e.message);
    }
  };
  return (
    <>
      <SectionTitle
        eyebrow="SALES / PRICING ENGINE"
        title="报价与合同"
        action={
          <button
            className="primary"
            onClick={() => {
              setPrefill(null);
              setOpen(true);
            }}
          >
            <Plus size={16} /> 新建报价
          </button>
        }
      />
      {error && <div className="error">{error}</div>}
      <div className="stats-grid small">
        <Stat
          label="报价总数"
          value={rows.length}
          icon={<FileText />}
          color="purple"
        />
        <Stat
          label="待审批"
          value={rows.filter((r) => r.status === "pending_approval").length}
          icon={<Activity />}
          color="orange"
        />
        <Stat
          label="已接受"
          value={rows.filter((r) => r.status === "accepted").length}
          icon={<CheckCircle2 />}
          color="green"
        />
      </div>
      <div className="panel table-panel">
        <Toolbar
          onSearch={(v) =>
            api(`quotes?q=${encodeURIComponent(v)}`).then((x) =>
              setRows(x.items),
            )
          }
        />
        <Table
          rows={rows}
          columns={[
            {
              key: "id",
              label: "报价单号",
              render: (v) => (
                <b className="mono">QT-{v.slice(0, 8).toUpperCase()}</b>
              ),
            },
            {
              key: "calculation",
              label: "报价金额",
              render: (v) => money(v?.total),
            },
            {
              key: "rule_version",
              label: "规则版本",
              render: (v) => <span className="rule-tag">{v}</span>,
            },
            {
              key: "status",
              label: "状态",
              render: (v) => (
                <span
                  className={
                    "tag " +
                    (v === "accepted"
                      ? "success"
                      : v.includes("approval")
                        ? "warning"
                        : "blue-tag")
                  }
                >
                  {statusLabel(v)}
                </span>
              ),
            },
            {
              key: "created_at",
              label: "创建时间",
              render: (v) => String(v).slice(0, 10),
            },
            {
              key: "id",
              label: "操作",
              render: (_, r) => (
                <div className="row-actions">
                  {r.status === "draft" && (
                    <button
                      className="text-btn"
                      onClick={() => act(`approval-requests/quote/${r.id}`)}
                    >
                      申请审批
                    </button>
                  )}
                  {r.status === "approved" && (
                    <button
                      className="text-btn"
                      onClick={() => act(`quotes/${r.id}/state/sent`)}
                    >
                      模拟发送
                    </button>
                  )}
                  {r.status === "accepted" && (
                    <>
                      <button
                        className="text-btn"
                        onClick={() =>
                          api(`quotes/${r.id}/contract`, "POST", {})
                            .then((x) => downloadPdf(x.id))
                            .catch((e) => setError(e.message))
                        }
                      >
                        合同 PDF
                      </button>
                      <button
                        className="text-btn"
                        onClick={() => act(`quotes/${r.id}/order`)}
                      >
                        生成订单
                      </button>
                    </>
                  )}
                </div>
              ),
            },
          ]}
        />
      </div>
      {open && (
        <Modal title="报价草稿" onClose={() => setOpen(false)}>
          <form className="form-grid" onSubmit={create}>
            <label>
              客户
              <select
                name="customer_id"
                required
                defaultValue={prefill?.customer_id || ""}
              >
                <option value="" disabled>
                  选择客户
                </option>
                {customers.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name} · {c.contact}
                  </option>
                ))}
              </select>
            </label>
            <label>
              产品
              <select name="product_id" required defaultValue={products[0]?.id}>
                {products.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name} ({p.attributes?.width}×{p.attributes?.height}×
                    {p.attributes?.depth})
                  </option>
                ))}
              </select>
            </label>
            {(["quantity", "width", "height", "depth"] as const).map((k, i) => (
              <label key={k}>
                {
                  (
                    {
                      quantity: "数量",
                      width: "宽度 mm",
                      height: "高度 mm",
                      depth: "深度 mm",
                    } as any
                  )[k]
                }
                <input
                  name={k}
                  type="number"
                  min="1"
                  required
                  defaultValue={
                    prefill?.requirement?.[k] || [1, 900, 1850, 400][i]
                  }
                />
              </label>
            ))}
            <label>
              颜色
              <input
                name="color"
                defaultValue={prefill?.requirement?.color || "灰白"}
              />
            </label>
            <label>
              配置
              <select
                name="configuration"
                defaultValue={prefill?.requirement?.configuration || "standard"}
              >
                <option value="standard">标准</option>
                <option value="reinforced">加强</option>
              </select>
            </label>
            {error && <div className="error">{error}</div>}
            <button className="primary">计算并保存报价</button>
          </form>
        </Modal>
      )}
    </>
  );
}
function Orders() {
  const [rows, setRows] = useState<Row[]>([]),
    [error, setError] = useState("");
  const load = () =>
    api("orders")
      .then((x) => setRows(x.items))
      .catch((e) => setError(e.message));
  useEffect(() => {
    load();
  }, []);
  const action = async (path: string, target?: string) => {
    try {
      await api(path, "POST", target ? { target } : {});
      load();
    } catch (e: any) {
      setError(e.message);
    }
  };
  return (
    <>
      <SectionTitle eyebrow="SALES / DELIVERY" title="订单管理" />
      <div className="stats-grid small">
        <Stat
          label="订单数"
          value={rows.length}
          icon={<ClipboardList />}
          color="cyan"
        />
        <Stat
          label="待审批"
          value={rows.filter((r) => r.status === "pending_approval").length}
          icon={<Activity />}
          color="orange"
        />
        <Stat
          label="已提交生产"
          value={rows.filter((r) => r.status === "submitted").length}
          icon={<CheckCircle2 />}
          color="green"
        />
      </div>
      {error && <div className="error">{error}</div>}
      <div className="panel table-panel">
        <Toolbar
          onSearch={(v) =>
            api(`orders?q=${encodeURIComponent(v)}`).then((x) =>
              setRows(x.items),
            )
          }
        />
        <Table
          rows={rows}
          columns={[
            {
              key: "id",
              label: "订单号",
              render: (v) => (
                <b className="mono">SO-{v.slice(0, 8).toUpperCase()}</b>
              ),
            },
            { key: "data", label: "订单金额", render: (v) => money(v?.total) },
            {
              key: "data",
              label: "数量",
              render: (v) => `${fmt(v?.requirement?.quantity)} 件`,
            },
            { key: "source", label: "来源" },
            {
              key: "status",
              label: "状态",
              render: (v) => (
                <span
                  className={
                    "tag " +
                    (v === "submitted"
                      ? "success"
                      : v.includes("approval")
                        ? "warning"
                        : "blue-tag")
                  }
                >
                  {statusLabel(v)}
                </span>
              ),
            },
            {
              key: "created_at",
              label: "创建时间",
              render: (v) => String(v).slice(0, 10),
            },
            {
              key: "id",
              label: "操作",
              render: (v, r) => (
                <div className="row-actions">
                  {r.status === "draft" && (
                    <button
                      className="text-btn"
                      onClick={() => action(`approval-requests/order/${v}`)}
                    >
                      申请审批
                    </button>
                  )}
                  {r.status === "approved" && (
                    <button
                      className="text-btn"
                      onClick={() => action(`orders/${v}/submit`)}
                    >
                      提交生产
                    </button>
                  )}
                  {r.status === "submitted" && <>
                    <button className="text-btn" onClick={() => action(`orders/${v}/sync`, "crm")}>同步 CRM</button>
                    <button className="text-btn" onClick={() => action(`orders/${v}/sync`, "factory")}>同步工厂</button>
                  </>}
                </div>
              ),
            },
          ]}
        />
      </div>
    </>
  );
}
function Production() {
  const [rows, setRows] = useState<Row[]>([]),
    [progress, setProgress] = useState<Row | null>(null),
    [error, setError] = useState(""),
    [report, setReport] = useState<Row | null>(null);
  const load = () =>
    api("production/plans")
      .then((x) => setRows(x.items))
      .catch((e) => setError(e.message));
  useEffect(() => {
    load();
  }, []);
  const openProgress = async (id: string) => {
    try {
      setProgress(await api(`production/plans/${id}/progress`));
    } catch (e: any) {
      setError(e.message);
    }
  };
  const action = async (path: string, target?: string) => {
    try {
      await api(path, "POST", target ? { target } : {});
      load();
      if (progress) openProgress(progress.id);
    } catch (e: any) {
      setError(e.message);
    }
  };
  const saveReport = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const d = new FormData(e.currentTarget);
    try {
      await api(`production/work-orders/${report?.id}/reports`, "POST", {
        actual: Number(d.get("actual")),
        qualified: Number(d.get("qualified")),
        rejected: Number(d.get("rejected")),
        hours: String(d.get("hours")),
        remark: String(d.get("remark")),
        date: new Date().toISOString().slice(0, 10),
      });
      setReport(null);
      if (progress) openProgress(progress.id);
    } catch (e: any) {
      setError(e.message);
    }
  };
  const completed = rows.reduce((n, r) => n + (r.completed || 0), 0);
  return (
    <>
      <SectionTitle
        eyebrow="MANUFACTURING / MES"
        title="生产管理"
        action={<span className="muted">由已提交订单自动生成计划</span>}
      />
      {error && <div className="error">{error}</div>}
      <div className="stats-grid small">
        <Stat
          label="计划总量"
          value={fmt(rows.reduce((a, r) => a + (r.quantity || 0), 0))}
          icon={<Factory />}
          color="cyan"
        />
        <Stat
          label="已完成（末工序）"
          value={fmt(completed)}
          icon={<CheckCircle2 />}
          color="green"
        />
        <Stat
          label="进行中计划"
          value={rows.filter((r) => r.status === "published").length}
          icon={<Activity />}
          color="orange"
        />
        <Stat
          label="待发布审批"
          value={rows.filter((r) => r.status === "pending_approval").length}
          icon={<BarChart3 />}
          color="purple"
        />
      </div>
      <div className="panel table-panel">
        <Toolbar
          onSearch={(v) =>
            api(`production/plans?q=${encodeURIComponent(v)}`).then((x) =>
              setRows(x.items),
            )
          }
        />
        <Table
          rows={rows}
          columns={[
            {
              key: "id",
              label: "计划编号",
              render: (v) => (
                <b className="mono">PP-{v.slice(0, 8).toUpperCase()}</b>
              ),
            },
            { key: "quantity", label: "计划量", render: (v) => `${fmt(v)} 件` },
            { key: "due_date", label: "交期" },
            {
              key: "status",
              label: "状态",
              render: (v) => (
                <span
                  className={
                    "tag " +
                    (v === "published"
                      ? "success"
                      : v.includes("approval")
                        ? "warning"
                        : "blue-tag")
                  }
                >
                  {statusLabel(v)}
                </span>
              ),
            },
            {
              key: "id",
              label: "进度与操作",
              render: (v, r) => (
                <div className="row-actions">
                  <button className="text-btn" onClick={() => openProgress(v)}>
                    查看进度
                  </button>
                  {r.status === "draft" && (
                    <button
                      className="text-btn"
                      onClick={() => action(`approval-requests/plan/${v}`)}
                    >
                      申请发布审批
                    </button>
                  )}
                  {r.status === "approved" && (
                    <button
                      className="text-btn"
                      onClick={() => action(`production/plans/${v}/publish`)}
                    >
                      发布计划
                    </button>
                  )}
                </div>
              ),
            },
          ]}
        />
      </div>
      {progress && (
        <Modal title="生产计划进度" onClose={() => setProgress(null)}>
          <div className="progress-detail">
            <b>
              {progress.completion_rate}% · {progress.risk}
            </b>
            <span>
              计划 {fmt(progress.quantity)} 件 · 已完成{" "}
              {fmt(progress.completed)} · 剩余 {fmt(progress.remaining)}
            </span>
            <span>
              交期 {progress.due_date} · 预计完成 {progress.estimated_date}
            </span>
            <h3>工序报工</h3>
            {progress.work_orders?.map((w: Row) => (
              <div className="work-row" key={w.id}>
                <div>
                  <b>{w.operation}</b>
                  <span>
                    计划 {fmt(w.planned)} · 实际 {fmt(w.actual)} · 合格{" "}
                    {fmt(w.qualified)} · 不合格 {fmt(w.rejected)}
                  </span>
                </div>
                {progress.status === "published" && (
                  <button className="text-btn" onClick={() => setReport(w)}>
                    报工
                  </button>
                )}
              </div>
            ))}
          </div>
        </Modal>
      )}
      {report && (
        <Modal
          title={`报工 · ${report.operation}`}
          onClose={() => setReport(null)}
        >
          <form className="form-grid" onSubmit={saveReport}>
            <label>
              实际完成
              <input
                name="actual"
                type="number"
                min="1"
                max={report.planned - report.actual}
                required
              />
            </label>
            <label>
              合格数
              <input name="qualified" type="number" min="0" required />
            </label>
            <label>
              不合格数
              <input
                name="rejected"
                type="number"
                min="0"
                defaultValue="0"
                required
              />
            </label>
            <label>
              工时
              <input
                name="hours"
                type="number"
                min="0.1"
                max="24"
                step="0.1"
                required
              />
            </label>
            <label className="full-field">
              备注
              <input name="remark" />
            </label>
            <button className="primary">提交报工</button>
          </form>
        </Modal>
      )}
    </>
  );
}
function Channels() {
  const [rows, setRows] = useState<Row[]>([]), [open, setOpen] = useState(false), [error, setError] = useState("");
  const load = () => api("channel-assets").then((x) => setRows(x.items)).catch((e) => setError(e.message));
  useEffect(() => { load(); }, []);
  const create = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); const d = new FormData(e.currentTarget);
    try { await api("channel-assets", "POST", { channel: String(d.get("channel")), asset_type: String(d.get("asset_type")), title: String(d.get("title")), url: String(d.get("url") || ""), metadata: { demo: true } }); setOpen(false); load(); }
    catch (e: any) { setError(e.message); }
  };
  return <><SectionTitle eyebrow="CHANNEL / CONTENT MOCK" title="渠道与素材" action={<button className="primary" onClick={() => setOpen(true)}><Plus size={16} />登记素材</button>} />
    <div className="hero-strip"><div><span className="eyebrow">MOCK PLATFORM ADAPTER</span><h2>多平台商品素材统一管理</h2><p>淘宝、天猫、京东、拼多多、小红书、抖音素材登记与发布准备，平台发布能力当前为 MOCK。</p></div><span className="provider-badge"><i /> MOCK</span></div>
    {error && <div className="error">{error}</div>}<div className="panel table-panel"><Table rows={rows} empty="暂无渠道素材" columns={[{key:"channel",label:"平台"},{key:"asset_type",label:"素材类型",render:(v)=>(({sku_main:"SKU 主图",detail:"详情页",poster:"活动海报",video_template:"视频模板"} as any)[v]||v)},{key:"title",label:"标题",render:(v)=><b>{v}</b>},{key:"status",label:"状态",render:(v)=><span className="tag blue-tag">{statusLabel(v)}</span>},{key:"provider_mode",label:"接入状态",render:(v)=><span className="tag success">{v}</span>},{key:"created_at",label:"登记时间",render:(v)=>String(v).slice(0,10)}]} /></div>
    {open && <Modal title="登记渠道素材" onClose={() => setOpen(false)}><form className="form-grid" onSubmit={create}><label>平台<select name="channel" defaultValue="淘宝"><option>淘宝</option><option>天猫</option><option>京东</option><option>拼多多</option><option>小红书</option><option>抖音</option></select></label><label>素材类型<select name="asset_type" defaultValue="sku_main"><option value="sku_main">SKU 主图</option><option value="detail">详情页</option><option value="poster">活动海报</option><option value="video_template">视频模板</option></select></label><label className="full-field">标题<input name="title" required placeholder="例如：900宽钢制文件柜主图" /></label><label className="full-field">素材地址<input name="url" placeholder="对象存储或素材管理地址，可留空" /></label><button className="primary">保存 MOCK 素材</button></form></Modal>}</>;
}
function CustomRequirements() {
  const [rows, setRows] = useState<Row[]>([]), [customers, setCustomers] = useState<Row[]>([]), [open, setOpen] = useState(false), [error, setError] = useState("");
  const load = () => api("custom-requirements").then((x) => setRows(x.items)).catch((e) => setError(e.message));
  useEffect(() => { load(); api("customers?page_size=100").then((x) => setCustomers(x.items)); }, []);
  const create = async (e: React.FormEvent<HTMLFormElement>) => { e.preventDefault(); const d = new FormData(e.currentTarget); try { await api("custom-requirements", "POST", { customer_id: String(d.get("customer_id")), title: String(d.get("title")), brief: String(d.get("brief")), dimensions: { width: Number(d.get("width")), height: Number(d.get("height")), depth: Number(d.get("depth")), source: "manual" } }); setOpen(false); load(); } catch (e: any) { setError(e.message); } };
  return <><SectionTitle eyebrow="B-SIDE / CUSTOM SALES" title="定制需求" action={<button className="primary" onClick={() => setOpen(true)}><Plus size={16} />登记定制需求</button>} /><div className="hero-strip"><div><span className="eyebrow">AI SALES ASSIST · MOCK</span><h2>从客户草图到可报价需求</h2><p>记录客户尺寸、材质、场景与 CAD 资料，生成销售跟进建议；CAD 自动布局当前为 STUB。</p></div><span className="provider-badge"><i /> AI MOCK / CAD STUB</span></div>{error && <div className="error">{error}</div>}<div className="panel table-panel"><Table rows={rows} empty="暂无定制需求" columns={[{key:"title",label:"需求名称",render:(v)=><b>{v}</b>},{key:"customer_id",label:"客户",render:(v)=>customers.find((c)=>c.id===v)?.name||v},{key:"dimensions",label:"尺寸",render:(v)=>v?.width?`${v.width}×${v.height}×${v.depth} mm`:"待确认"},{key:"cad_mode",label:"CAD",render:(v)=><span className="tag warning">{v}</span>},{key:"ai_analysis",label:"销售建议",render:(v)=>v?.sales_points?.[0]||"待分析"},{key:"status",label:"状态",render:(v)=><span className="tag blue-tag">{statusLabel(v)}</span>}]} /></div>{open&&<Modal title="登记 B 端定制需求" onClose={()=>setOpen(false)}><form className="form-grid" onSubmit={create}><label>客户<select name="customer_id" required>{customers.map((c)=><option key={c.id} value={c.id}>{c.name}</option>)}</select></label><label>需求名称<input name="title" required defaultValue="定制钢制收纳柜" /></label><label>宽度 mm<input name="width" type="number" defaultValue="1200" /></label><label>高度 mm<input name="height" type="number" defaultValue="2000" /></label><label>深度 mm<input name="depth" type="number" defaultValue="500" /></label><label className="full-field">需求描述<textarea name="brief" required defaultValue="客户提供场景草图，需要定制尺寸、颜色与内部隔断。" /></label><button className="primary">保存并生成 MOCK 建议</button></form></Modal>}</>;
}
function Products() {
  const [rows, setRows] = useState<Row[]>([]),
    [open, setOpen] = useState(false),
    [error, setError] = useState("");
  const load = () => api("products").then((x) => setRows(x.items)).catch((e) => setError(e.message));
  useEffect(() => {
    load();
  }, []);
  const create = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const d = new FormData(e.currentTarget);
    try {
      await api("products", "POST", {
        name: String(d.get("name")), category: String(d.get("category")),
        attributes: { width: Number(d.get("width")), height: Number(d.get("height")), depth: Number(d.get("depth")), thickness: Number(d.get("thickness")), material: String(d.get("material")), color: String(d.get("color")) },
        bom: [{ name: "钢板", quantity: 1, unit: "套" }],
        routing: ["开料", "冲压", "折弯", "焊接", "喷涂", "组装"].map((name, sequence) => ({ name, sequence, capacity: 100 })),
      });
      setOpen(false); setError(""); load();
    } catch (e: any) { setError(e.message); }
  };
  return (
    <>
      <SectionTitle
        eyebrow="PRODUCT MASTER DATA"
        title="产品主数据"
        action={
          <button className="primary" onClick={() => setOpen(true)}>
            <Plus size={16} /> 新建产品
          </button>
        }
      />
      {error && <div className="error">{error}</div>}
      <div className="panel table-panel">
        <Toolbar onSearch={(v) => api(`products?q=${encodeURIComponent(v)}`).then((x) => setRows(x.items)).catch((e) => setError(e.message))} />
        <Table
          rows={rows}
          columns={[
            { key: "name", label: "产品名称", render: (v) => <b>{v}</b> },
            { key: "category", label: "品类" },
            {
              key: "attributes",
              label: "规格",
              render: (v) => `${v?.width}×${v?.height}×${v?.depth} mm`,
            },
            {
              key: "id",
              label: "产品 ID",
              render: (v) => <span className="mono">{v}</span>,
            },
            {
              key: "created_at",
              label: "更新时间",
              render: (v) => String(v).slice(0, 10),
            },
          ]}
        />
      </div>
      {open && <Modal title="新建产品主数据" onClose={() => setOpen(false)}><form className="form-grid" onSubmit={create}>
        <label>产品名称<input name="name" required defaultValue="钢制文件柜" /></label>
        <label>品类<input name="category" required defaultValue="文件柜" /></label>
        <label>宽度 mm<input name="width" type="number" min="100" required defaultValue="900" /></label>
        <label>高度 mm<input name="height" type="number" min="100" required defaultValue="1850" /></label>
        <label>深度 mm<input name="depth" type="number" min="100" required defaultValue="400" /></label>
        <label>板厚 mm<input name="thickness" type="number" min="0.1" step="0.1" required defaultValue="0.8" /></label>
        <label>材质<input name="material" required defaultValue="冷轧钢板" /></label>
        <label>颜色<input name="color" required defaultValue="灰白" /></label>
        <button className="primary">保存产品</button>
      </form></Modal>}
    </>
  );
}
function Approvals() {
  const [rows, setRows] = useState<Row[]>([]), [filter, setFilter] = useState("pending"), [error, setError] = useState("");
  const load = () => api(`approvals?page_size=100${filter === "pending" ? "&status=pending" : ""}`).then((x) => setRows(x.items)).catch((e) => setError(e.message));
  useEffect(() => { load(); }, [filter]);
  const decide = async (id: string, approve: boolean) => {
    try { await api(`approvals/${id}/decision`, "POST", { approve }); load(); }
    catch (e: any) { setError(e.message); }
  };
  return <>
    <SectionTitle eyebrow="GOVERNANCE / WORKFLOW" title="审批中心" action={<span className="muted">关键业务动作需审批后生效</span>} />
    {error && <div className="error">{error}</div>}
    <div className="stats-grid small"><Stat label="待处理" value={rows.filter((r) => r.status === "pending").length} icon={<Activity />} color="orange" /><Stat label="已批准" value={rows.filter((r) => r.status === "approved").length} icon={<CheckCircle2 />} color="green" /><Stat label="已驳回/失效" value={rows.filter((r) => ["rejected", "invalidated"].includes(r.status)).length} icon={<ShieldCheck />} color="purple" /></div>
    <div className="panel table-panel"><div className="approval-filters"><button className={filter === "pending" ? "filter-active" : ""} onClick={() => setFilter("pending")}>待处理</button><button className={filter === "all" ? "filter-active" : ""} onClick={() => setFilter("all")}>全部历史</button></div><Table rows={rows} empty="暂无审批记录" columns={[
      { key: "resource_type", label: "业务类型", render: (v) => ({ quote: "报价", order: "订单", plan: "生产计划" } as any)[v] || v },
      { key: "resource_summary", label: "业务摘要", render: (v) => v ? (v.calculation ? money(v.calculation.total) : v.quantity ? `${fmt(v.quantity)} 件` : "业务记录") : "-" },
      { key: "requester_name", label: "申请人" },
      { key: "resource_status", label: "业务状态", render: (v) => <span className="tag blue-tag">{statusLabel(v)}</span> },
      { key: "status", label: "审批状态", render: (v) => <span className={"tag " + (v === "pending" ? "warning" : v === "approved" ? "success" : "blue-tag")}>{statusLabel(v)}</span> },
      { key: "id", label: "操作", render: (v, r) => r.status === "pending" ? <div className="row-actions"><button className="text-btn" onClick={() => decide(v, true)}>批准</button><button className="text-btn danger-btn" onClick={() => decide(v, false)}>驳回</button></div> : <span className="muted">已处理</span> },
    ]} /></div>
  </>;
}
function Audit() {
  const [rows, setRows] = useState<Row[]>([]);
  useEffect(() => {
    api("audit").then((x) => setRows(x.items));
  }, []);
  return (
    <>
      <SectionTitle eyebrow="GOVERNANCE" title="系统审计" />
      <div className="panel table-panel">
        <Toolbar onSearch={() => {}} />
        <Table
          rows={rows}
          columns={[
            {
              key: "created_at",
              label: "时间",
              render: (v) => String(v).replace("T", " ").slice(0, 19),
            },
            { key: "actor_type", label: "执行者" },
            { key: "action", label: "动作" },
            { key: "resource_type", label: "资源" },
            {
              key: "request_id",
              label: "Request ID",
              render: (v) => <span className="mono">{v?.slice(0, 12)}</span>,
            },
          ]}
        />
      </div>
    </>
  );
}
function Loading() {
  return (
    <div className="loading">
      <span />
      正在加载数据
    </div>
  );
}
function Empty({ text }: { text: string }) {
  return (
    <div className="empty">
      <Boxes size={24} />
      <span>{text}</span>
    </div>
  );
}
function App() {
  const [user, setUser] = useState<Row | null>(null);
  useEffect(() => {
    if (sessionStorage.getItem("steel-token"))
      api("auth/me")
        .then((x) => setUser(x.user))
        .catch(() => setToken(""));
  }, []);
  if (!user) return <Login onLogin={setUser} />;
  return (
    <Shell
      user={user}
      onLogout={() => {
        api("auth/logout", "POST", {}).finally(() => {
          setToken("");
          setUser(null);
        });
      }}
    />
  );
}
createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
