import hashlib
import json
from datetime import date, timedelta
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import select

from .models import *
from .pricing import calculate

RESOURCES = {"customers": Customer, "products": Product, "pricing-rules": PriceRule, "conversations": Conversation,
             "quotes": Quote, "contracts": Contract, "orders": SalesOrder, "production/plans": ProductionPlan,
             "production/work-orders": WorkOrder, "production/reports": EmployeeReport, "approvals": Approval,
             "audit": AuditLog, "outbox": OutboxEvent, "webhooks": WebhookEvent, "users": User, "roles": Role,
             "channel-assets": ChannelAsset, "order-syncs": OrderSync, "custom-requirements": CustomRequirement}


def fail(status, code):
    raise HTTPException(status, code)


def dump(row):
    return {c.name: getattr(row, c.name).isoformat() if isinstance(getattr(row, c.name), datetime) else getattr(row, c.name)
            for c in row.__table__.columns if c.name != "password_hash"}


class Service:
    def __init__(self, db, user, request_id, actor_type="human", run_id=None, call_id=None):
        self.db, self.user, self.request_id = db, user, request_id
        self.actor_type, self.run_id, self.call_id = actor_type, run_id, call_id

    def permission(self, name):
        role = self.db.get(Role, self.user.role_id)
        if "*" not in role.permissions and name not in role.permissions:
            self.audit("permission", name, "denied", {})
            self.db.commit()
            fail(403, "PERMISSION_DENIED")

    def query(self, model):
        query = select(model)
        if hasattr(model, "org_id"):
            query = query.where(model.org_id == self.user.org_id)
        role = self.db.get(Role, self.user.role_id)
        if role.scope == "assigned" and model is WorkOrder:
            query = query.where(WorkOrder.employee_id == self.user.id)
        if role.scope == "assigned" and model is EmployeeReport:
            query = query.where(EmployeeReport.employee_id == self.user.id)
        return query

    def get(self, model, identifier, lock=False):
        query = self.query(model).where(model.id == identifier)
        if lock:
            query = query.with_for_update()
        row = self.db.scalar(query)
        if row is None:
            fail(404, "RESOURCE_NOT_FOUND")
        return row

    def audit(self, kind, identifier, action, after, before=None):
        self.db.add(AuditLog(org_id=self.user.org_id, actor_id=self.user.id, actor_type=self.actor_type,
                             resource_type=kind, resource_id=identifier, action=action, before=before or {}, after=after,
                             request_id=self.request_id, agent_run_id=self.run_id, tool_call_id=self.call_id))

    def event(self, kind, row, action):
        self.db.flush()
        self.audit(kind, row.id, action, dump(row))
        self.db.add(OutboxEvent(org_id=self.user.org_id, event_type=f"{kind}.{action}", payload={"id": row.id, "request_id": self.request_id}))

    def idem(self, path, key, data, action):
        if not key or len(key) > 200:
            fail(400, "IDEMPOTENCY_KEY_REQUIRED")
        fingerprint = hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()
        lock = f"{self.user.org_id}:{self.user.id}:{path}:{key}"
        self.db.execute(__import__('sqlalchemy').text("SELECT pg_advisory_xact_lock(hashtextextended(:key, 0))"), {"key": lock})
        existing = self.db.scalar(select(Idempotency).where(Idempotency.org_id == self.user.org_id,
                                  Idempotency.user_id == self.user.id, Idempotency.path == path, Idempotency.key == key))
        if existing:
            if existing.fingerprint != fingerprint:
                fail(409, "IDEMPOTENCY_CONFLICT")
            return existing.response
        result = action()
        self.db.add(Idempotency(org_id=self.user.org_id, user_id=self.user.id, path=path, key=key,
                                fingerprint=fingerprint, response=result))
        self.db.commit()
        return result

    def customer(self, data):
        row = Customer(org_id=self.user.org_id, owner_id=self.user.id, **data)
        self.db.add(row)
        self.event("customer", row, "created")
        return dump(row)

    def quote(self, data, identifier=None):
        customer = self.get(Customer, data["customer_id"])
        self.get(Product, data["product_id"])
        rule = self.db.scalar(self.query(PriceRule).where(PriceRule.product_id == data["product_id"], PriceRule.effective_at <= now())
                              .order_by(PriceRule.priority.desc(), PriceRule.effective_at.desc()))
        if not rule:
            fail(422, "NO_EFFECTIVE_PRICE_RULE")
        result = calculate(data, rule.config, customer.level, rule.rule_version)
        if identifier:
            row = self.get(Quote, identifier, True)
            if row.status not in ("draft", "pending_approval", "approved", "rejected"):
                fail(409, "QUOTE_NOT_EDITABLE")
            row.version += 1
            row.status = "draft"
            for approval in self.db.scalars(self.query(Approval).where(Approval.resource_id == row.id)):
                approval.status = "invalidated"
            row.customer_id, row.product_id = customer.id, data["product_id"]
        else:
            row = Quote(org_id=self.user.org_id, customer_id=customer.id, product_id=data["product_id"], creator_id=self.user.id)
            self.db.add(row)
        row.input, row.calculation, row.rule_snapshot, row.rule_version = data, result, rule.config, rule.rule_version
        self.event("quote", row, "updated" if identifier else "created")
        return dump(row)

    def contract(self, quote_id):
        quote = self.get(Quote, quote_id)
        if quote.status not in ("approved", "sent", "accepted"):
            fail(409, "QUOTE_NOT_APPROVED")
        existing = self.db.scalar(self.query(Contract).where(Contract.quote_id == quote.id))
        if existing:
            return dump(existing)
        customer = self.get(Customer, quote.customer_id)
        row = Contract(org_id=self.user.org_id, quote_id=quote.id, content={"customer": customer.name,
                       "quote_version": quote.version, "requirement": quote.input, "total": quote.calculation["total"],
                       "template_version": "demo-1", "notice": "合同草稿，未经签署，不构成已签合同"})
        self.db.add(row)
        self.event("contract", row, "draft_created")
        return dump(row)

    def order(self, quote_id):
        quote = self.get(Quote, quote_id, True)
        if quote.status != "accepted":
            fail(409, "QUOTE_NOT_ACCEPTED")
        contract = self.db.scalar(self.query(Contract).where(Contract.quote_id == quote_id))
        if not contract or contract.content["quote_version"] != quote.version:
            fail(409, "CURRENT_CONTRACT_REQUIRED")
        if self.db.scalar(self.query(SalesOrder).where(SalesOrder.quote_id == quote_id)):
            fail(409, "ORDER_ALREADY_EXISTS")
        row = SalesOrder(org_id=self.user.org_id, quote_id=quote.id, contract_id=contract.id, customer_id=quote.customer_id,
                         data={"requirement": quote.input, "total": quote.calculation["total"], "rule_version": quote.rule_version})
        self.db.add(row)
        self.event("order", row, "draft_created")
        return dump(row)

    def approval(self, kind, identifier):
        model = {"quote": Quote, "order": SalesOrder, "plan": ProductionPlan}.get(kind)
        if not model:
            fail(422, "INVALID_APPROVAL_RESOURCE")
        row = self.get(model, identifier, True)
        if row.status != "draft":
            fail(409, "INVALID_STATE")
        existing = self.db.scalar(self.query(Approval).where(
            Approval.resource_type == kind,
            Approval.resource_id == row.id,
            Approval.status == "pending",
        ))
        if existing:
            fail(409, "APPROVAL_ALREADY_PENDING")
        row.status = "pending_approval"
        approval = Approval(org_id=self.user.org_id, resource_type=kind, resource_id=row.id,
                            resource_version=row.version, requester_id=self.user.id)
        self.db.add(approval)
        self.event(kind, row, "approval_requested")
        self.db.flush()
        return dump(approval)

    def decision(self, identifier, approve):
        item = self.get(Approval, identifier, True)
        self.permission(f"{item.resource_type}.approve")
        if item.requester_id == self.user.id:
            fail(403, "SELF_APPROVAL_FORBIDDEN")
        row = self.get({"quote": Quote, "order": SalesOrder, "plan": ProductionPlan}[item.resource_type], item.resource_id, True)
        if item.status != "pending" or row.version != item.resource_version or row.status != "pending_approval":
            fail(409, "STALE_APPROVAL")
        item.status, item.reviewer_id = ("approved" if approve else "rejected"), self.user.id
        row.status = "approved" if approve else "draft"
        self.event(item.resource_type, row, item.status)
        return dump(item)

    def quote_state(self, identifier, target):
        transitions = {"sent": ("approved",), "accepted": ("sent",), "expired": ("sent",),
                       "rejected": ("sent",), "cancelled": ("draft", "approved", "sent")}
        quote = self.get(Quote, identifier, True)
        if target not in transitions or quote.status not in transitions[target]:
            fail(409, "INVALID_QUOTE_TRANSITION")
        if target == "sent":
            valid = self.db.scalar(self.query(Approval).where(Approval.resource_id == identifier, Approval.status == "approved",
                                                              Approval.resource_version == quote.version))
            if not valid:
                fail(409, "APPROVAL_REQUIRED")
        quote.status = target
        self.event("quote", quote, "mock_sent" if target == "sent" else target)
        return dump(quote)

    def submit_order(self, identifier):
        order = self.get(SalesOrder, identifier, True)
        if order.status != "approved":
            fail(409, "APPROVAL_REQUIRED")
        quote = self.get(Quote, order.quote_id)
        product = self.get(Product, quote.product_id)
        order.status = "submitted"
        plan = ProductionPlan(org_id=self.user.org_id, order_id=order.id, quantity=quote.input["quantity"],
                              due_date=(date.today() + timedelta(days=7)).isoformat(), bom=product.bom)
        self.db.add(plan)
        self.db.flush()
        worker = self.db.scalar(select(User).where(User.org_id == self.user.org_id, User.role_id == "worker"))
        for sequence, operation in enumerate(product.routing):
            self.db.add(WorkOrder(org_id=self.user.org_id, plan_id=plan.id, operation=operation["name"], sequence=sequence,
                                  capacity=operation["capacity"], employee_id=worker.id, planned=plan.quantity))
        self.event("order", order, "submitted")
        self.event("production", plan, "created")
        return dump(plan)

    def publish(self, identifier):
        plan = self.get(ProductionPlan, identifier, True)
        if plan.status != "approved":
            fail(409, "APPROVAL_REQUIRED")
        plan.status = "published"
        self.event("production", plan, "published")
        return dump(plan)

    def report(self, identifier, data):
        work = self.get(WorkOrder, identifier, True)
        plan = self.get(ProductionPlan, work.plan_id, True)
        if plan.status != "published":
            fail(409, "PLAN_NOT_PUBLISHED")
        if data["qualified"] + data["rejected"] != data["actual"]:
            fail(422, "QUALITY_QUANTITY_MISMATCH")
        if work.actual + data["actual"] > work.planned:
            fail(409, "REPORT_EXCEEDS_PLAN")
        date.fromisoformat(data["date"])
        previous = self.db.scalar(self.query(WorkOrder).where(WorkOrder.plan_id == plan.id, WorkOrder.sequence == work.sequence - 1))
        if previous and work.actual + data["actual"] > previous.qualified:
            fail(409, "INSUFFICIENT_UPSTREAM_QUANTITY")
        work.actual += data["actual"]
        work.qualified += data["qualified"]
        work.rejected += data["rejected"]
        report = EmployeeReport(org_id=self.user.org_id, work_order_id=work.id, employee_id=work.employee_id, **data)
        self.db.add(report)
        self.event("report", report, "submitted")
        return dump(report)

    def progress(self, plan):
        works = list(self.db.scalars(self.query(WorkOrder).where(WorkOrder.plan_id == plan.id).order_by(WorkOrder.sequence)))
        completed = works[-1].qualified if works else 0
        remaining = plan.quantity - completed
        days = max((w.planned - w.qualified) / max(w.capacity, 1) for w in works) if works else 0
        predicted = date.today() + timedelta(days=__import__('math').ceil(days))
        return {**dump(plan), "completed": completed, "remaining": remaining, "completion_rate": round(completed / plan.quantity * 100, 1),
                "estimated_date": predicted.isoformat(), "risk": "延期风险" if remaining and predicted.isoformat() > plan.due_date else "正常",
                "work_orders": [dump(w) for w in works]}

    def dashboard(self):
        orders = list(self.db.scalars(self.query(SalesOrder)))
        plans = [self.progress(p) for p in self.db.scalars(self.query(ProductionPlan))]
        total = sum(p["quantity"] for p in plans)
        complete = sum(p["completed"] for p in plans)
        from decimal import Decimal
        return {"sales": str(sum((Decimal(o.data["total"]) for o in orders if o.status == "submitted"), Decimal(0))),
                "customers": len(list(self.db.scalars(self.query(Customer)))), "quotes": len(list(self.db.scalars(self.query(Quote)))),
                "orders": len(orders), "planned": total, "completed": complete, "remaining": total - complete,
                "completion_rate": round(complete / total * 100, 1) if total else 0, "plans": plans,
                "pending_approvals": len(list(self.db.scalars(self.query(Approval).where(Approval.status == "pending"))))}
