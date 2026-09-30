from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from .config import settings


def now():
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str]


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    permissions: Mapped[list] = mapped_column(JSON)
    scope: Mapped[str] = mapped_column(default="organization")


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    org_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    username: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    role_id: Mapped[str] = mapped_column(ForeignKey("roles.id"))
    password_hash: Mapped[str]


class LoginSession(Base):
    __tablename__ = "login_sessions"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)


class RecordMixin:
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    org_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Customer(RecordMixin, Base):
    __tablename__ = "customers"
    name: Mapped[str]
    contact: Mapped[str]
    phone: Mapped[str] = mapped_column(default="")
    source: Mapped[str] = mapped_column(default="manual")
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    level: Mapped[str] = mapped_column(default="B")
    tags: Mapped[list] = mapped_column(JSON, default=list)
    identities: Mapped[list] = mapped_column(JSON, default=list)


class Activity(RecordMixin, Base):
    __tablename__ = "activities"
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"), index=True)
    text: Mapped[str]
    actor_id: Mapped[str] = mapped_column(ForeignKey("users.id"))


class Product(RecordMixin, Base):
    __tablename__ = "products"
    name: Mapped[str]
    category: Mapped[str]
    attributes: Mapped[dict] = mapped_column(JSON)
    bom: Mapped[list] = mapped_column(JSON)
    routing: Mapped[list] = mapped_column(JSON)


class SKU(RecordMixin, Base):
    __tablename__ = "skus"
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), index=True)
    code: Mapped[str] = mapped_column(unique=True)
    attributes: Mapped[dict] = mapped_column(JSON)


class PriceRule(RecordMixin, Base):
    __tablename__ = "price_rules"
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), index=True)
    rule_version: Mapped[str] = mapped_column(unique=True)
    effective_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    priority: Mapped[int] = mapped_column(default=1)
    config: Mapped[dict] = mapped_column(JSON)


class Conversation(RecordMixin, Base):
    __tablename__ = "conversations"
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"))
    status: Mapped[str] = mapped_column(default="ai")
    messages: Mapped[list] = mapped_column(JSON, default=list)
    requirement: Mapped[dict] = mapped_column(JSON, default=dict)


class Quote(RecordMixin, Base):
    __tablename__ = "quotes"
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"), index=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"))
    status: Mapped[str] = mapped_column(default="draft")
    input: Mapped[dict] = mapped_column(JSON)
    calculation: Mapped[dict] = mapped_column(JSON)
    rule_snapshot: Mapped[dict] = mapped_column(JSON)
    rule_version: Mapped[str]
    creator_id: Mapped[str] = mapped_column(ForeignKey("users.id"))


class Contract(RecordMixin, Base):
    __tablename__ = "contracts"
    quote_id: Mapped[str] = mapped_column(ForeignKey("quotes.id"), unique=True)
    status: Mapped[str] = mapped_column(default="draft")
    content: Mapped[dict] = mapped_column(JSON)


class SalesOrder(RecordMixin, Base):
    __tablename__ = "sales_orders"
    quote_id: Mapped[str] = mapped_column(ForeignKey("quotes.id"), unique=True)
    contract_id: Mapped[str] = mapped_column(ForeignKey("contracts.id"))
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"))
    status: Mapped[str] = mapped_column(default="draft")
    source: Mapped[str] = mapped_column(default="quote")
    data: Mapped[dict] = mapped_column(JSON)


class ProductionPlan(RecordMixin, Base):
    __tablename__ = "production_plans"
    order_id: Mapped[str] = mapped_column(ForeignKey("sales_orders.id"), unique=True)
    status: Mapped[str] = mapped_column(default="draft")
    quantity: Mapped[int]
    due_date: Mapped[str]
    bom: Mapped[list] = mapped_column(JSON)


class WorkOrder(RecordMixin, Base):
    __tablename__ = "work_orders"
    plan_id: Mapped[str] = mapped_column(ForeignKey("production_plans.id"), index=True)
    operation: Mapped[str]
    sequence: Mapped[int]
    capacity: Mapped[int]
    employee_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    planned: Mapped[int]
    actual: Mapped[int] = mapped_column(default=0)
    qualified: Mapped[int] = mapped_column(default=0)
    rejected: Mapped[int] = mapped_column(default=0)


class EmployeeReport(RecordMixin, Base):
    __tablename__ = "employee_reports"
    work_order_id: Mapped[str] = mapped_column(ForeignKey("work_orders.id"), index=True)
    employee_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    actual: Mapped[int]
    qualified: Mapped[int]
    rejected: Mapped[int]
    hours: Mapped[str]
    remark: Mapped[str]
    date: Mapped[str]


class Approval(RecordMixin, Base):
    __tablename__ = "approvals"
    resource_type: Mapped[str]
    resource_id: Mapped[str] = mapped_column(index=True)
    resource_version: Mapped[int]
    requester_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    reviewer_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    status: Mapped[str] = mapped_column(default="pending")


class AuditLog(RecordMixin, Base):
    __tablename__ = "audit_logs"
    actor_id: Mapped[str]
    actor_type: Mapped[str]
    resource_type: Mapped[str]
    resource_id: Mapped[str]
    action: Mapped[str]
    before: Mapped[dict] = mapped_column(JSON, default=dict)
    after: Mapped[dict] = mapped_column(JSON, default=dict)
    request_id: Mapped[str]
    agent_run_id: Mapped[str | None] = mapped_column(nullable=True)
    tool_call_id: Mapped[str | None] = mapped_column(nullable=True)


class OutboxEvent(RecordMixin, Base):
    __tablename__ = "outbox_events"
    event_type: Mapped[str]
    payload: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(default="pending")


class Idempotency(Base):
    __tablename__ = "idempotency"
    __table_args__ = (UniqueConstraint("org_id", "user_id", "path", "key"),)
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    org_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"))
    user_id: Mapped[str]
    path: Mapped[str]
    key: Mapped[str]
    fingerprint: Mapped[str]
    response: Mapped[dict] = mapped_column(JSON)


class WebhookEvent(RecordMixin, Base):
    __tablename__ = "webhook_events"
    __table_args__ = (UniqueConstraint("org_id", "platform", "event_id"),)
    event_id: Mapped[str]
    platform: Mapped[str]
    event_type: Mapped[str]
    payload: Mapped[dict] = mapped_column(JSON)
    signature: Mapped[str]
    status: Mapped[str] = mapped_column(default="received")
    retry_count: Mapped[int] = mapped_column(default=0)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class ChannelAsset(RecordMixin, Base):
    __tablename__ = "channel_assets"
    channel: Mapped[str]
    asset_type: Mapped[str]
    title: Mapped[str]
    status: Mapped[str] = mapped_column(default="draft")
    url: Mapped[str] = mapped_column(default="")
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    provider_mode: Mapped[str] = mapped_column(default="MOCK")


class OrderSync(RecordMixin, Base):
    __tablename__ = "order_syncs"
    order_id: Mapped[str] = mapped_column(ForeignKey("sales_orders.id"), index=True)
    target: Mapped[str]
    status: Mapped[str] = mapped_column(default="pending")
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    provider_mode: Mapped[str] = mapped_column(default="MOCK")
    last_error: Mapped[str] = mapped_column(default="")


class CustomRequirement(RecordMixin, Base):
    __tablename__ = "custom_requirements"
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"), index=True)
    title: Mapped[str]
    brief: Mapped[str]
    dimensions: Mapped[dict] = mapped_column(JSON, default=dict)
    cad_mode: Mapped[str] = mapped_column(default="STUB")
    design_result: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(default="draft")
    ai_analysis: Mapped[dict] = mapped_column(JSON, default=dict)


engine = create_engine(settings.database_url, pool_pre_ping=True)
Session = sessionmaker(engine, expire_on_commit=False)
