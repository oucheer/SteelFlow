import hashlib
import hmac
import io
import time
from collections import defaultdict, deque
from datetime import timedelta
from uuid import uuid4

import jwt
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pwdlib import PasswordHash
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError

from .config import settings
from .models import *
from .providers import MockProvider
from .schemas import *
from .services import RESOURCES, Service, dump, fail
from .tools import TOOLS, execute

app = FastAPI(title="Steel Furniture Business API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=[settings.frontend_origin], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"], expose_headers=["X-Request-ID"])
passwords = PasswordHash.recommended()
login_attempts = defaultdict(deque)


@app.middleware("http")
async def correlation(request: Request, call_next):
    request.state.request_id = str(uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response


@app.exception_handler(HTTPException)
async def domain_error(request, error):
    return JSONResponse(status_code=error.status_code, content={"error": {"code": error.detail}, "request_id": request.state.request_id})


@app.exception_handler(RequestValidationError)
async def validation_error(request, error):
    return JSONResponse(status_code=422, content={"error": {"code": "VALIDATION_ERROR", "details": str(error)}, "request_id": request.state.request_id})


@app.exception_handler(IntegrityError)
async def integrity_error(request, error):
    return JSONResponse(status_code=409, content={"error": {"code": "DATABASE_CONSTRAINT_CONFLICT"}, "request_id": request.state.request_id})


def database():
    with Session() as db:
        yield db


def context(request: Request, authorization: str = Header(default=""), db=Depends(database)):
    try:
        token = jwt.decode(authorization.removeprefix("Bearer "), settings.jwt_secret, algorithms=["HS256"])
        session = db.get(LoginSession, token["sid"])
        if not session or session.revoked or session.expires_at <= now():
            fail(401, "SESSION_EXPIRED")
        user = db.get(User, token["sub"])
        if not user or session.user_id != user.id:
            fail(401, "INVALID_SESSION")
    except jwt.PyJWTError:
        fail(401, "INVALID_TOKEN")
    request.state.session_id = token["sid"]
    return Service(db, user, request.state.request_id)


def write(service, request, key, data, permission, action):
    service.permission(permission)
    return service.idem(request.url.path, key, data, action)


@app.get("/api/v1/health")
def health(db=Depends(database)):
    db.execute(__import__('sqlalchemy').text("SELECT 1"))
    return {"status": "ok", "database": "PostgreSQL", "ai": "MOCK", "platform": "MOCK"}


@app.post("/api/v1/auth/login")
def login(data: LoginInput, request: Request, db=Depends(database)):
    attempts = login_attempts[request.client.host]
    while attempts and attempts[0] < time.monotonic() - 60:
        attempts.popleft()
    if len(attempts) >= 20:
        fail(429, "LOGIN_RATE_LIMIT")
    attempts.append(time.monotonic())
    user = db.scalar(select(User).where(User.username == data.username))
    if not user or not passwords.verify(data.password, user.password_hash):
        fail(401, "INVALID_CREDENTIALS")
    session = LoginSession(id=str(uuid4()), user_id=user.id, expires_at=now() + timedelta(hours=8))
    db.add(session)
    service = Service(db, user, request.state.request_id)
    service.audit("session", session.id, "login", {})
    db.commit()
    token = jwt.encode({"sub": user.id, "sid": session.id, "exp": session.expires_at}, settings.jwt_secret, algorithm="HS256")
    return {"token": token, "user": dump(user), "permissions": db.get(Role, user.role_id).permissions}


@app.get("/api/v1/auth/me")
def me(s=Depends(context)):
    return {"user": dump(s.user), "permissions": s.db.get(Role, s.user.role_id).permissions}


@app.post("/api/v1/auth/logout")
def logout(request: Request, s=Depends(context)):
    s.db.get(LoginSession, request.state.session_id).revoked = True
    s.audit("session", request.state.session_id, "logout", {})
    s.db.commit()
    return {"revoked": True}


@app.get("/api/v1/dashboard")
def dashboard(s=Depends(context)):
    s.permission("dashboard.read")
    return s.dashboard()


@app.post("/api/v1/channel-assets")
def channel_asset(data: ChannelAssetInput, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    def action():
        row = ChannelAsset(org_id=s.user.org_id, channel=data.channel, asset_type=data.asset_type, title=data.title,
                           url=data.url, metadata_json=data.metadata, provider_mode="MOCK")
        s.db.add(row)
        s.event("channel_asset", row, "created")
        return dump(row)
    return write(s, request, idempotency_key, data.model_dump(), "product.write", action)


@app.post("/api/v1/custom-requirements")
def custom_requirement(data: CustomRequirementInput, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    def action():
        s.get(Customer, data.customer_id)
        analysis = {"summary": data.brief[:240], "sales_points": ["确认尺寸与材质", "确认交期与收货地址", "提供 CAD 平面图后复核"], "provider_mode": "MOCK"}
        row = CustomRequirement(org_id=s.user.org_id, customer_id=data.customer_id, title=data.title, brief=data.brief,
                                dimensions=data.dimensions, cad_mode="STUB", design_result={"status": "待上传 CAD 图纸", "provider_mode": "STUB"},
                                ai_analysis=analysis)
        s.db.add(row)
        s.event("custom_requirement", row, "created")
        return dump(row)
    return write(s, request, idempotency_key, data.model_dump(), "customer.write", action)


@app.post("/api/v1/orders/{identifier}/sync")
def sync_order(identifier: str, data: SyncInput, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    def action():
        order = s.get(SalesOrder, identifier)
        existing = s.db.scalar(s.query(OrderSync).where(OrderSync.order_id == order.id, OrderSync.target == data.target,
                                                        OrderSync.status == "processed"))
        if existing:
            return dump(existing)
        row = OrderSync(org_id=s.user.org_id, order_id=order.id, target=data.target, status="processed",
                        payload={"order_id": order.id, "customer_id": order.customer_id, "total": order.data.get("total"), "mode": "MOCK"},
                        provider_mode="MOCK")
        s.db.add(row)
        s.event("order_sync", row, "processed")
        return dump(row)
    return write(s, request, idempotency_key, data.model_dump(), "order.write", action)


@app.get("/api/v1/tools")
def tools(s=Depends(context)):
    s.permission("conversation.read")
    return TOOLS


@app.post("/api/v1/tools/{name}")
def tool(name: str, data: ToolInput, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    if name not in TOOLS:
        fail(404, "TOOL_NOT_FOUND")
    s.permission(TOOLS[name]["permission"])
    return s.idem(request.url.path, idempotency_key, data.model_dump(), lambda: execute(s, name, data.arguments))


@app.post("/api/v1/customers")
def customer(data: CustomerInput, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    return write(s, request, idempotency_key, data.model_dump(), "customer.write", lambda: s.customer(data.model_dump()))


@app.post("/api/v1/products")
def product(data: ProductInput, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    s.permission("product.write")
    def action():
        row = Product(org_id=s.user.org_id, **data.model_dump())
        s.db.add(row)
        s.event("product", row, "created")
        s.db.flush()
        return dump(row)
    return s.idem(request.url.path, idempotency_key, data.model_dump(), action)


@app.post("/api/v1/customers/{identifier}/activities")
def activity(identifier: str, data: TextInput, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    def action():
        s.get(Customer, identifier)
        row = Activity(org_id=s.user.org_id, customer_id=identifier, text=data.text, actor_id=s.user.id)
        s.db.add(row)
        s.event("activity", row, "created")
        return dump(row)
    return write(s, request, idempotency_key, data.model_dump(), "customer.write", action)


@app.get("/api/v1/customers/{identifier}/timeline")
def timeline(identifier: str, s=Depends(context)):
    s.permission("customer.read")
    s.get(Customer, identifier)
    records = [dump(a) for a in s.db.scalars(s.query(Activity).where(Activity.customer_id == identifier))]
    for model in (Quote, Conversation, SalesOrder):
        records += [{"id": r.id, "created_at": r.created_at.isoformat(), "text": f"{model.__tablename__}: {getattr(r, 'status', '')}"}
                    for r in s.db.scalars(s.query(model).where(model.customer_id == identifier))]
    return sorted(records, key=lambda r: r["created_at"], reverse=True)


@app.post("/api/v1/conversations")
def conversation(data: ConversationInput, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    def action():
        s.get(Customer, data.customer_id)
        row = Conversation(org_id=s.user.org_id, customer_id=data.customer_id)
        s.db.add(row)
        s.event("conversation", row, "created")
        return dump(row)
    return write(s, request, idempotency_key, data.model_dump(), "conversation.write", action)


@app.post("/api/v1/conversations/{identifier}/messages")
def message(identifier: str, data: TextInput, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    def action():
        row = s.get(Conversation, identifier, True)
        messages = row.messages + [{"role": "customer", "text": data.text, "timestamp": now().isoformat()}]
        if row.status == "ai":
            tool_result = execute(s, "extract_customer_requirement", {"text": data.text})
            row.requirement = tool_result["result"]
            if row.requirement.get("handoff"):
                row.status = "human"
            answer = row.requirement.get("reason", f"已提取 {row.requirement['quantity']} 件产品需求，请人工确认尺寸与配置后生成报价草稿。") if not row.requirement.get("handoff") else row.requirement["reason"]
            messages.append({"role": "assistant", "text": answer, "timestamp": now().isoformat(), "mode": "MOCK"})
        row.messages = messages
        row.version += 1
        s.event("conversation", row, "message_added")
        return dump(row)
    return write(s, request, idempotency_key, data.model_dump(), "conversation.write", action)


@app.post("/api/v1/conversations/{identifier}/handoff")
def handoff(identifier: str, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    def action():
        row = s.get(Conversation, identifier, True)
        row.status = "human"
        s.event("conversation", row, "handoff")
        return dump(row)
    return write(s, request, idempotency_key, {}, "conversation.write", action)


@app.post("/api/v1/quotes")
def quote(data: QuoteInput, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    return write(s, request, idempotency_key, data.model_dump(mode="json"), "quote.write", lambda: s.quote(data.model_dump(mode="json")))


@app.put("/api/v1/quotes/{identifier}")
def update_quote(identifier: str, data: QuoteInput, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    return write(s, request, idempotency_key, data.model_dump(mode="json"), "quote.write", lambda: s.quote(data.model_dump(mode="json"), identifier))


@app.get("/api/v1/quotes/{identifier}/replay")
def replay(identifier: str, s=Depends(context)):
    from .pricing import calculate
    s.permission("quote.read")
    quote = s.get(Quote, identifier)
    return calculate(quote.input, quote.rule_snapshot, quote.calculation["customer_level"], quote.rule_version)


@app.post("/api/v1/quotes/{identifier}/state/{target}")
def quote_state(identifier: str, target: str, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    return write(s, request, idempotency_key, {}, "quote.write", lambda: s.quote_state(identifier, target))


@app.post("/api/v1/quotes/{identifier}/contract")
def contract(identifier: str, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    return write(s, request, idempotency_key, {}, "contract.write", lambda: s.contract(identifier))


@app.get("/api/v1/contracts/{identifier}/pdf")
def contract_pdf(identifier: str, s=Depends(context)):
    s.permission("contract.read")
    contract = s.get(Contract, identifier)
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    stream = io.BytesIO()
    pdf = canvas.Canvas(stream)
    pdf.setFont("STSong-Light", 18)
    pdf.drawString(50, 790, "钢制家具购销合同（草稿）")
    pdf.setFont("STSong-Light", 12)
    lines = [f"客户：{contract.content['customer']}", f"报价单：{contract.quote_id}",
             f"数量：{contract.content['requirement']['quantity']} 件", f"合同金额：人民币 {contract.content['total']} 元",
             "合同模板版本：demo-1", "本文件为未签署草稿，请审核后使用。", "产品、交期、付款与验收条款需双方另行确认。"]
    for i, line in enumerate(lines):
        pdf.drawString(50, 740 - i * 35, line)
    pdf.save()
    s.audit("contract", identifier, "pdf_exported", {})
    s.db.commit()
    return Response(stream.getvalue(), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=contract-draft.pdf"})


@app.post("/api/v1/quotes/{identifier}/order")
def order(identifier: str, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    return write(s, request, idempotency_key, {}, "order.write", lambda: s.order(identifier))


@app.post("/api/v1/approval-requests/{kind}/{identifier}")
def approval(kind: str, identifier: str, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    return write(s, request, idempotency_key, {}, f"{kind}.write", lambda: s.approval(kind, identifier))


@app.post("/api/v1/approvals/{identifier}/decision")
def decision(identifier: str, data: DecisionInput, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    return s.idem(request.url.path, idempotency_key, data.model_dump(), lambda: s.decision(identifier, data.approve))


@app.post("/api/v1/orders/{identifier}/submit")
def submit(identifier: str, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    return write(s, request, idempotency_key, {}, "order.write", lambda: s.submit_order(identifier))


@app.put("/api/v1/production/plans/{identifier}")
def change_plan(identifier: str, data: PlanInput, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    def action():
        row = s.get(ProductionPlan, identifier, True)
        if row.status == "published":
            fail(409, "PUBLISHED_PLAN_IMMUTABLE")
        __import__('datetime').date.fromisoformat(data.due_date)
        row.due_date, row.status, row.version = data.due_date, "draft", row.version + 1
        for approval in s.db.scalars(s.query(Approval).where(Approval.resource_id == row.id)):
            approval.status = "invalidated"
        s.event("plan", row, "updated")
        return dump(row)
    return write(s, request, idempotency_key, data.model_dump(), "plan.write", action)


@app.post("/api/v1/production/plans/{identifier}/publish")
def publish(identifier: str, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    return write(s, request, idempotency_key, {}, "plan.write", lambda: s.publish(identifier))


@app.get("/api/v1/production/plans/{identifier}/progress")
def progress(identifier: str, s=Depends(context)):
    s.permission("production.read")
    return s.progress(s.get(ProductionPlan, identifier))


@app.post("/api/v1/production/work-orders/{identifier}/reports")
def report(identifier: str, data: ReportInput, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    return write(s, request, idempotency_key, data.model_dump(mode="json"), "report.write", lambda: s.report(identifier, data.model_dump(mode="json")))


def resource_permission(resource):
    return {"customers": "customer.read", "products": "product.read", "pricing-rules": "quote.read",
            "conversations": "conversation.read", "quotes": "quote.read", "contracts": "contract.read", "orders": "order.read",
            "production/plans": "production.read", "production/work-orders": "production.read", "production/reports": "production.read",
            "approvals": "approval.read", "audit": "audit.read", "outbox": "audit.read", "webhooks": "audit.read",
            "users": "user.read", "roles": "user.read", "channel-assets": "product.read", "order-syncs": "order.read",
            "custom-requirements": "customer.read"}[resource]


def add_list_route(resource, model):
    def listing(q: str = "", page: int = 1, page_size: int = 20, sort: str = "created_at", direction: str = "desc", status: str = "", s=Depends(context)):
        s.permission(resource_permission(resource))
        if page < 1 or not 1 <= page_size <= 200 or direction not in ("asc", "desc"):
            fail(422, "INVALID_PAGINATION")
        query = s.query(model)
        if q and model is Customer:
            query = query.where(or_(Customer.name.ilike(f"%{q}%"), Customer.contact.ilike(f"%{q}%"), Customer.phone.ilike(f"%{q}%")))
        elif q and hasattr(model, "name"):
            query = query.where(model.name.ilike(f"%{q}%"))
        if status and hasattr(model, "status"):
            query = query.where(model.status == status)
        sort_field = getattr(model, sort, None)
        if sort_field is None:
            sort_field = model.id
        total = s.db.scalar(select(func.count()).select_from(query.subquery()))
        query = query.order_by(sort_field.desc() if direction == "desc" else sort_field.asc(), model.id).offset((page - 1) * page_size).limit(page_size)
        rows = [dump(r) for r in s.db.scalars(query)]
        if model is Conversation:
            for row in rows:
                customer = s.get(Customer, row["customer_id"])
                row["customer_name"] = customer.name
                row["customer_contact"] = customer.contact
                row["last_message"] = row["messages"][-1] if row["messages"] else None
                row["message_count"] = len(row["messages"])
        if model is Approval:
            for row in rows:
                requester = s.db.get(User, row["requester_id"])
                row["requester_name"] = requester.name if requester else "未知用户"
                resource_model = {"quote": Quote, "order": SalesOrder, "plan": ProductionPlan}.get(row["resource_type"])
                if resource_model:
                    target = s.get(resource_model, row["resource_id"])
                    row["resource_status"] = target.status
                    row["resource_summary"] = dump(target)
        return {"items": rows, "total": total, "page": page, "page_size": page_size}
    listing.__name__ = resource.replace("/", "_") + "_list"
    app.get("/api/v1/" + resource)(listing)

    def detail(identifier: str, s=Depends(context)):
        s.permission(resource_permission(resource))
        result = dump(s.get(model, identifier))
        if model is Conversation:
            customer = s.get(Customer, result["customer_id"])
            result["customer_name"] = customer.name
            result["customer_contact"] = customer.contact
            result["last_message"] = result["messages"][-1] if result["messages"] else None
            result["message_count"] = len(result["messages"])
        if model is Product:
            result["skus"] = [dump(r) for r in s.db.scalars(s.query(SKU).where(SKU.product_id == identifier))]
        if model is Approval:
            requester = s.db.get(User, result["requester_id"])
            result["requester_name"] = requester.name if requester else "未知用户"
            resource_model = {"quote": Quote, "order": SalesOrder, "plan": ProductionPlan}.get(result["resource_type"])
            if resource_model:
                target = s.get(resource_model, result["resource_id"])
                result["resource_status"] = target.status
                result["resource_summary"] = dump(target)
        return result
    detail.__name__ = resource.replace("/", "_") + "_detail"
    app.get("/api/v1/" + resource + "/{identifier}")(detail)


for resource, model in RESOURCES.items():
    add_list_route(resource, model)


@app.post("/api/v1/platform/mock/webhook")
async def webhook(request: Request, x_signature: str = Header(default=""), db=Depends(database)):
    body = await request.body()
    if len(body) > 100000:
        fail(413, "PAYLOAD_TOO_LARGE")
    expected = hmac.new(settings.webhook_secret.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, x_signature):
        fail(401, "INVALID_WEBHOOK_SIGNATURE")
    data = WebhookInput.model_validate_json(body)
    user = db.scalar(select(User).where(User.username == "admin"))
    s = Service(db, user, request.state.request_id, "platform")
    def action():
        existing = db.scalar(s.query(WebhookEvent).where(WebhookEvent.event_id == data.event_id, WebhookEvent.platform == "mock"))
        if existing:
            return dump(existing)
        row = WebhookEvent(org_id=user.org_id, event_id=data.event_id, platform="mock", event_type=data.event_type,
                           payload=data.payload, signature=x_signature)
        db.add(row)
        process_webhook(s, row)
        s.event("webhook", row, row.status)
        return dump(row)
    return s.idem("mock-webhook", data.event_id, data.model_dump(), action)


def process_webhook(s, event):
    conversation_id, text = event.payload.get("conversation_id"), event.payload.get("text")
    row = s.db.scalar(s.query(Conversation).where(Conversation.id == conversation_id))
    if not row or not isinstance(text, str) or not 1 <= len(text) <= 10000:
        event.status = "failed"
        return
    s.db.refresh(row, with_for_update=True)
    row.messages = row.messages + [{"role": "customer", "text": text, "mode": "MOCK", "timestamp": now().isoformat()}]
    event.status, event.processed_at = "processed", now()


@app.post("/api/v1/webhooks/{identifier}/retry")
def retry_webhook(identifier: str, request: Request, idempotency_key: str = Header(default=""), s=Depends(context)):
    def action():
        row = s.get(WebhookEvent, identifier, True)
        if row.status == "processed":
            return dump(row)
        if row.retry_count >= 3:
            fail(409, "WEBHOOK_DEAD_LETTER")
        row.retry_count += 1
        process_webhook(s, row)
        if row.status == "failed" and row.retry_count >= 3:
            row.status = "dead_letter"
        s.event("webhook", row, "retried")
        return dump(row)
    return write(s, request, idempotency_key, {}, "integration.write", action)
