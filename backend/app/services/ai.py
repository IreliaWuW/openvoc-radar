from __future__ import annotations

import json
from typing import Any

import httpx
from pydantic import BaseModel, Field, ValidationError

from app.config import Settings
from app.models import ItemType, Severity


class ClassificationResult(BaseModel):
    title: str
    summary: str
    item_type: ItemType
    severity: Severity
    product_area: str
    sentiment: str
    confidence: float = Field(ge=0, le=1)


def mock_classify(subject: str, body: str, product_area: str | None) -> ClassificationResult:
    text = f"{subject} {body}".lower()
    if any(word in text for word in ["crash", "error", "bug", "broken", "failed", "timeout"]):
        item_type = ItemType.bug
    elif any(word in text for word in ["please add", "feature", "would like", "request"]):
        item_type = ItemType.feature_request
    elif any(word in text for word in ["confusing", "hard to", "unclear"]):
        item_type = ItemType.usability
    elif any(word in text for word in ["billing", "invoice", "pricing"]):
        item_type = ItemType.pricing
    else:
        item_type = ItemType.support_question

    severity = Severity.high if any(word in text for word in ["blocked", "cannot", "crash", "failed"]) else Severity.medium
    if any(word in text for word in ["minor", "nice to have", "question"]):
        severity = Severity.low

    title = subject[:80] or "Customer feedback"
    summary = body[:240].strip()
    return ClassificationResult(
        title=title,
        summary=summary,
        item_type=item_type,
        severity=severity,
        product_area=product_area or "General",
        sentiment="negative" if severity != Severity.low else "neutral",
        confidence=0.72,
    )


async def classify_text(settings: Settings, subject: str, body: str, product_area: str | None) -> ClassificationResult:
    api_key = (settings.openai_api_key or "").strip()
    if not api_key:
        return mock_classify(subject, body, product_area)

    schema = ClassificationResult.model_json_schema()
    payload: dict[str, Any] = {
        "model": settings.openai_model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Classify customer voice-of-customer feedback. "
                    "Return only JSON matching the provided schema. Do not invent facts."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "subject": subject,
                        "body": body,
                        "product_area_hint": product_area,
                        "schema": schema,
                    }
                ),
            },
        ],
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{settings.openai_base_url.rstrip('/')}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

    try:
        return ClassificationResult.model_validate_json(content)
    except (KeyError, TypeError, ValidationError, json.JSONDecodeError):
        return mock_classify(subject, body, product_area)
