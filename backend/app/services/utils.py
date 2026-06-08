from __future__ import annotations

from datetime import datetime, timezone


def split_ids(value: str | None) -> list[str]:
    if not value:
        return []
    return [item for item in value.split(",") if item]


def join_ids(values: list[str]) -> str:
    return ",".join(dict.fromkeys(values))


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def parse_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed
