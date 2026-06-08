import asyncio

from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.database import init_db
from app.main import app
from app.models import ItemType
from app.services.ai import classify_text
from app.services.webhooks import push_webhook


def test_sample_import_report_and_drafts(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    get_settings.cache_clear()

    from app import database

    database.engine = database.create_engine(
        f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
    )
    init_db()

    client = TestClient(app)
    imported = client.post("/api/import/sample").json()
    assert imported["imported"] >= 8
    assert imported["classified_items"] >= 1

    metrics = client.get("/api/metrics").json()
    assert metrics["total_tickets"] == imported["imported"]
    assert metrics["total_voc_items"] == imported["classified_items"]

    report = client.post("/api/reports/weekly").json()
    assert "Source tickets:" in report["markdown"]
    assert report["source_ticket_ids"]

    drafts = client.post("/api/actions/drafts").json()
    assert drafts
    assert all(draft["source_ticket_ids"] for draft in drafts)


def test_mock_classifier_without_api_key():
    settings = Settings(openai_api_key="")
    result = asyncio.run(
        classify_text(settings, "CSV export fails", "The CSV export failed with an error.", "Analytics")
    )
    assert result.item_type == ItemType.bug
    assert result.product_area == "Analytics"


def test_webhook_is_optional_without_url():
    settings = Settings(slack_webhook_url="", lark_webhook_url="")
    ok, message = asyncio.run(push_webhook("slack", "# Report", settings))
    assert ok is False
    assert "No slack webhook configured" in message
