from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid")


class LoginInput(Input):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=200)


class CustomerInput(Input):
    name: str = Field(min_length=1, max_length=120)
    contact: str = Field(min_length=1, max_length=80)
    phone: str = Field(default="", max_length=30)
    source: str = Field(default="manual", max_length=30)
    level: Literal["A", "B", "C"] = "B"
    tags: list[str] = Field(default_factory=list, max_length=20)
    identities: list[dict] = Field(default_factory=list, max_length=20)


class ProductInput(Input):
    name: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=80)
    attributes: dict = Field(default_factory=dict)
    bom: list[dict] = Field(default_factory=list, max_length=100)
    routing: list[dict] = Field(default_factory=list, max_length=20)


class QuoteInput(Input):
    customer_id: str
    product_id: str
    quantity: int = Field(ge=1, le=100000)
    width: int = Field(default=900, ge=100, le=5000)
    height: int = Field(default=1850, ge=100, le=5000)
    depth: int = Field(default=400, ge=100, le=5000)
    color: str = Field(default="灰白", max_length=40)
    configuration: Literal["standard", "reinforced"] = "standard"
    logistics: Decimal = Field(default=Decimal("0"), ge=0, le=1000000)
    other: Decimal = Field(default=Decimal("0"), ge=0, le=1000000)


class ReportInput(Input):
    actual: int = Field(ge=1, le=100000)
    qualified: int = Field(ge=0, le=100000)
    rejected: int = Field(default=0, ge=0, le=100000)
    hours: Decimal = Field(gt=0, le=24)
    remark: str = Field(default="", max_length=1000)
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")


class TextInput(Input):
    text: str = Field(min_length=1, max_length=10000)


class ConversationInput(Input):
    customer_id: str


class DecisionInput(Input):
    approve: bool


class PlanInput(Input):
    due_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")


class ToolInput(Input):
    arguments: dict


class WebhookInput(Input):
    event_id: str = Field(min_length=1, max_length=100)
    event_type: Literal["conversation.message"]
    payload: dict


class ChannelAssetInput(Input):
    channel: Literal["淘宝", "天猫", "京东", "拼多多", "小红书", "抖音"]
    asset_type: Literal["sku_main", "detail", "poster", "video_template"]
    title: str = Field(min_length=1, max_length=160)
    url: str = Field(default="", max_length=500)
    metadata: dict = Field(default_factory=dict)


class CustomRequirementInput(Input):
    customer_id: str
    title: str = Field(min_length=1, max_length=160)
    brief: str = Field(min_length=1, max_length=10000)
    dimensions: dict = Field(default_factory=dict)


class SyncInput(Input):
    target: Literal["crm", "factory"]
