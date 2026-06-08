from app.models import Conversation
from app.services.utils import parse_datetime


def normalize_ticket(row: dict[str, str]) -> Conversation:
    return Conversation(
        source=row.get("source", "csv").strip() or "csv",
        external_id=row["ticket_id"].strip(),
        user_id=row["user_id"].strip(),
        user_email=(row.get("user_email") or "").strip() or None,
        created_at=parse_datetime(row["created_at"].strip()),
        subject=row["subject"].strip(),
        body=row["body"].strip(),
        product_area=(row.get("product_area") or "").strip() or None,
        tags=(row.get("tags") or "").strip() or None,
    )
