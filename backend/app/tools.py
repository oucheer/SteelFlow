from uuid import uuid4
from .providers import MockProvider
from .schemas import QuoteInput, TextInput
from .models import Product
from .services import Service, dump, fail

TOOLS = {
    "extract_customer_requirement": {"permission": "conversation.write", "risk_level": "low", "approval_required": False,
                                     "input_schema": TextInput.model_json_schema(), "output_schema": {"type": "object"}, "idempotency_required": True, "audit_required": True},
    "search_products": {"permission": "product.read", "risk_level": "low", "approval_required": False,
                        "input_schema": TextInput.model_json_schema(), "output_schema": {"type": "array"}, "idempotency_required": True, "audit_required": True},
    "create_quote_draft": {"permission": "quote.write", "risk_level": "medium", "approval_required": False,
                           "input_schema": QuoteInput.model_json_schema(), "output_schema": {"type": "object"}, "idempotency_required": True, "audit_required": True},
}


def execute(service: Service, name, arguments):
    if name not in TOOLS:
        fail(404, "TOOL_NOT_FOUND")
    agent = Service(service.db, service.user, service.request_id, "agent", str(uuid4()), str(uuid4()))
    agent.permission(TOOLS[name]["permission"])
    if name == "extract_customer_requirement":
        result = MockProvider().extract(TextInput.model_validate(arguments).text)
    elif name == "search_products":
        text = TextInput.model_validate(arguments).text
        result = [dump(p) for p in service.db.scalars(service.query(Product).where(Product.name.ilike(f"%{text}%")))]
    else:
        result = agent.quote(QuoteInput.model_validate(arguments).model_dump(mode="json"))
    agent.audit("tool", name, "executed", {"input": arguments, "output": result, "provider_mode": "MOCK"})
    return {"result": result, "agent_run_id": agent.run_id, "tool_call_id": agent.call_id, "mode": "MOCK"}
