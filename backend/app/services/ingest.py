from __future__ import annotations

import csv
from pathlib import Path

from sqlmodel import Session, select

from app.config import Settings
from app.models import Conversation, VocItem
from app.schemas import ImportResult
from app.services.ai import classify_text
from app.services.dedupe import find_duplicate, issue_key, merge_source_ticket
from app.services.normalizer import normalize_ticket
from app.services.utils import now_utc


async def import_csv(path: Path, session: Session, settings: Settings) -> ImportResult:
    imported = 0
    skipped = 0
    classified = 0

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            conversation = normalize_ticket(row)
            existing = session.exec(
                select(Conversation).where(Conversation.external_id == conversation.external_id)
            ).first()
            if existing:
                skipped += 1
                continue

            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            imported += 1

            text = f"{conversation.subject} {conversation.body}"
            cluster_key = issue_key(text, conversation.product_area)
            duplicate = find_duplicate(session, conversation, cluster_key, settings.dedupe_window_hours)
            if duplicate:
                merge_source_ticket(duplicate, conversation.external_id)
                session.add(duplicate)
                session.commit()
                continue

            classification = await classify_text(
                settings,
                conversation.subject,
                conversation.body,
                conversation.product_area,
            )
            timestamp = now_utc()
            item = VocItem(
                conversation_id=conversation.id,
                source_ticket_ids=conversation.external_id,
                cluster_key=cluster_key,
                title=classification.title,
                summary=classification.summary,
                item_type=classification.item_type,
                severity=classification.severity,
                product_area=classification.product_area,
                sentiment=classification.sentiment,
                confidence=classification.confidence,
                created_at=conversation.created_at,
                updated_at=timestamp,
            )
            session.add(item)
            session.commit()
            classified += 1

    return ImportResult(imported=imported, skipped_existing=skipped, classified_items=classified)
