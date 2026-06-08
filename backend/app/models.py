from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class ItemType(str, Enum):
    bug = "bug"
    feature_request = "feature_request"
    support_question = "support_question"
    usability = "usability"
    pricing = "pricing"


class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Status(str, Enum):
    new = "new"
    triaged = "triaged"
    planned = "planned"
    closed = "closed"


class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    external_id: str = Field(index=True, unique=True)
    user_id: str = Field(index=True)
    user_email: str | None = None
    created_at: datetime = Field(index=True)
    subject: str
    body: str
    product_area: str | None = None
    tags: str | None = None


class VocItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    source_ticket_ids: str
    cluster_key: str = Field(index=True)
    title: str
    summary: str
    item_type: ItemType = Field(index=True)
    severity: Severity = Field(index=True)
    product_area: str = Field(index=True)
    sentiment: str
    confidence: float
    status: Status = Field(default=Status.new, index=True)
    created_at: datetime = Field(index=True)
    updated_at: datetime = Field(index=True)


class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    markdown: str
    source_ticket_ids: str
    created_at: datetime = Field(index=True)


class ProductAction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    voc_item_id: int = Field(foreign_key="vocitem.id", index=True)
    draft_type: str = Field(index=True)
    title: str
    markdown: str
    source_ticket_ids: str
    created_at: datetime = Field(index=True)
