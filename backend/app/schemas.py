from datetime import datetime
from pydantic import BaseModel, Field

from app.models import ItemType, Severity, Status


class ImportResult(BaseModel):
    imported: int
    skipped_existing: int
    classified_items: int


class ConversationRead(BaseModel):
    id: int
    source: str
    external_id: str
    user_id: str
    user_email: str | None
    created_at: datetime
    subject: str
    body: str
    product_area: str | None
    tags: str | None


class VocItemRead(BaseModel):
    id: int
    conversation_id: int
    source_ticket_ids: list[str]
    cluster_key: str
    title: str
    summary: str
    item_type: ItemType
    severity: Severity
    product_area: str
    sentiment: str
    confidence: float
    status: Status
    created_at: datetime
    updated_at: datetime


class DashboardMetrics(BaseModel):
    total_tickets: int
    total_voc_items: int
    open_items: int
    high_severity_items: int


class TrendPoint(BaseModel):
    date: str
    count: int


class ClusterRead(BaseModel):
    cluster_key: str
    title: str
    count: int
    severity: Severity
    product_area: str
    source_ticket_ids: list[str]


class ReportRead(BaseModel):
    id: int
    title: str
    markdown: str
    source_ticket_ids: list[str]
    created_at: datetime


class ProductActionRead(BaseModel):
    id: int
    voc_item_id: int
    draft_type: str
    title: str
    markdown: str
    source_ticket_ids: list[str]
    created_at: datetime


class WebhookPushRequest(BaseModel):
    destination: str = Field(pattern="^(slack|lark)$")
    markdown: str


class WebhookPushResult(BaseModel):
    ok: bool
    destination: str
    message: str
