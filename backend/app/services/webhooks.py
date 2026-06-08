from __future__ import annotations

import httpx

from app.config import Settings


async def push_webhook(destination: str, markdown: str, settings: Settings) -> tuple[bool, str]:
    url = settings.slack_webhook_url if destination == "slack" else settings.lark_webhook_url
    if not url:
        return False, f"No {destination} webhook configured. Add it to backend/.env."
    if not url.startswith("https://"):
        return False, f"The {destination} webhook must use HTTPS."
    if not markdown.strip():
        return False, "Report markdown is empty."

    if destination == "slack":
        payload = {"text": markdown[:30000]}
    else:
        payload = {"msg_type": "text", "content": {"text": markdown[:30000]}}

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(url, json=payload)
            if response.is_success:
                return True, "Webhook delivered."
            return False, f"Webhook returned HTTP {response.status_code}."
    except httpx.HTTPError as exc:
        return False, f"Webhook delivery failed: {exc.__class__.__name__}."
