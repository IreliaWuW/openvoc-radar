from __future__ import annotations

from contextlib import asynccontextmanager
from collections import Counter
from pathlib import Path
import tempfile

from fastapi import Depends, FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, func, select

from app.config import Settings, get_settings
from app.database import get_session, init_db
from app.models import Conversation, ProductAction, Report, VocItem
from app.schemas import (
    ClusterRead,
    DashboardMetrics,
    ImportResult,
    ProductActionRead,
    ReportRead,
    TrendPoint,
    VocItemRead,
    WebhookPushRequest,
    WebhookPushResult,
)
from app.services.ingest import import_csv
from app.services.reports import clusters, create_product_action_drafts, generate_weekly_report
from app.services.utils import split_ids
from app.services.webhooks import push_webhook


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="OpenVoC Radar API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def read_voc(item: VocItem) -> VocItemRead:
    return VocItemRead(
        **item.model_dump(exclude={"source_ticket_ids"}),
        source_ticket_ids=split_ids(item.source_ticket_ids),
    )


def read_report(report: Report) -> ReportRead:
    return ReportRead(
        **report.model_dump(exclude={"source_ticket_ids"}),
        source_ticket_ids=split_ids(report.source_ticket_ids),
    )


def read_action(action: ProductAction) -> ProductActionRead:
    return ProductActionRead(
        **action.model_dump(exclude={"source_ticket_ids"}),
        source_ticket_ids=split_ids(action.source_ticket_ids),
    )


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/import/sample", response_model=ImportResult)
async def import_sample(
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> ImportResult:
    if not settings.sample_csv_path.exists():
        raise HTTPException(status_code=404, detail="sample-data/tickets.csv was not found")
    return await import_csv(settings.sample_csv_path, session, settings)


@app.post("/api/import/csv", response_model=ImportResult)
async def import_uploaded_csv(
    file: UploadFile,
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> ImportResult:
    with tempfile.NamedTemporaryFile("wb", delete=False, suffix=".csv") as temp_file:
        temp_file.write(await file.read())
        temp_path = Path(temp_file.name)
    try:
        return await import_csv(temp_path, session, settings)
    finally:
        temp_path.unlink(missing_ok=True)


@app.get("/api/metrics", response_model=DashboardMetrics)
def metrics(session: Session = Depends(get_session)) -> DashboardMetrics:
    total_tickets = session.exec(select(func.count()).select_from(Conversation)).one()
    items = session.exec(select(VocItem)).all()
    return DashboardMetrics(
        total_tickets=total_tickets,
        total_voc_items=len(items),
        open_items=sum(1 for item in items if item.status.value != "closed"),
        high_severity_items=sum(1 for item in items if item.severity.value == "high"),
    )


@app.get("/api/items", response_model=list[VocItemRead])
def list_items(session: Session = Depends(get_session)) -> list[VocItemRead]:
    items = session.exec(select(VocItem).order_by(VocItem.created_at.desc())).all()
    return [read_voc(item) for item in items]


@app.get("/api/trends", response_model=list[TrendPoint])
def trends(session: Session = Depends(get_session)) -> list[TrendPoint]:
    items = session.exec(select(VocItem)).all()
    counts = Counter(item.created_at.date().isoformat() for item in items)
    return [TrendPoint(date=date, count=count) for date, count in sorted(counts.items())]


@app.get("/api/clusters", response_model=list[ClusterRead])
def list_clusters(session: Session = Depends(get_session)) -> list[ClusterRead]:
    return [ClusterRead(**cluster) for cluster in clusters(session)]


@app.post("/api/reports/weekly", response_model=ReportRead)
def create_weekly_report(session: Session = Depends(get_session)) -> ReportRead:
    return read_report(generate_weekly_report(session))


@app.get("/api/reports", response_model=list[ReportRead])
def list_reports(session: Session = Depends(get_session)) -> list[ReportRead]:
    reports = session.exec(select(Report).order_by(Report.created_at.desc())).all()
    return [read_report(report) for report in reports]


@app.post("/api/actions/drafts", response_model=list[ProductActionRead])
def create_drafts(session: Session = Depends(get_session)) -> list[ProductActionRead]:
    created = create_product_action_drafts(session)
    return [read_action(action) for action in created]


@app.get("/api/actions", response_model=list[ProductActionRead])
def list_actions(session: Session = Depends(get_session)) -> list[ProductActionRead]:
    actions = session.exec(select(ProductAction).order_by(ProductAction.created_at.desc())).all()
    return [read_action(action) for action in actions]


@app.post("/api/webhooks/push", response_model=WebhookPushResult)
async def push_report(
    request: WebhookPushRequest,
    settings: Settings = Depends(get_settings),
) -> WebhookPushResult:
    ok, message = await push_webhook(request.destination, request.markdown, settings)
    return WebhookPushResult(ok=ok, destination=request.destination, message=message)
