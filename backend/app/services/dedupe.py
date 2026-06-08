from __future__ import annotations

import re
from datetime import timedelta

from sqlmodel import Session, select

from app.models import Conversation, VocItem
from app.services.utils import split_ids, join_ids, now_utc


KEYWORDS = {
    "login": ["login", "sign in", "password", "sso"],
    "csv_export": ["csv", "export", "download"],
    "billing": ["billing", "invoice", "plan", "pricing"],
    "notifications": ["notification", "email", "alert"],
    "mobile": ["mobile", "ios", "android"],
    "performance": ["slow", "timeout", "loading", "latency"],
}


def issue_key(text: str, product_area: str | None) -> str:
    lower = text.lower()
    for key, words in KEYWORDS.items():
        if any(word in lower for word in words):
            return f"{product_area or 'general'}:{key}"
    tokens = re.findall(r"[a-z0-9]+", lower)
    placeholder = "-".join(tokens[:3]) if tokens else "uncategorized"
    return f"{product_area or 'general'}:{placeholder}"


def find_duplicate(
    session: Session,
    conversation: Conversation,
    cluster_key: str,
    window_hours: int,
) -> VocItem | None:
    start = conversation.created_at - timedelta(hours=window_hours)
    end = conversation.created_at + timedelta(hours=window_hours)
    statement = (
        select(VocItem)
        .where(VocItem.cluster_key == cluster_key)
        .where(VocItem.created_at >= start)
        .where(VocItem.created_at <= end)
    )
    for item in session.exec(statement).all():
        ids = split_ids(item.source_ticket_ids)
        first_conversation = session.get(Conversation, item.conversation_id)
        if first_conversation and first_conversation.user_id == conversation.user_id:
            return item
        if conversation.external_id in ids:
            return item
    return None


def merge_source_ticket(item: VocItem, ticket_id: str) -> None:
    item.source_ticket_ids = join_ids([*split_ids(item.source_ticket_ids), ticket_id])
    item.updated_at = now_utc()
