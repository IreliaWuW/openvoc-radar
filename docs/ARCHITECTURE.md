# Architecture

## System Overview

OpenVoC Radar is a small monorepo with a FastAPI backend and a Next.js frontend.

```text
CSV sample data
    |
    v
FastAPI import endpoint
    |
    v
normalizer -> dedupe -> classifier
    |
    v
SQLite via SQLModel
    |
    v
Next.js dashboard
    |
    v
reports, drafts, optional webhooks
```

## Backend

Location: `backend/`

Main pieces:

- `app/main.py`: FastAPI app and API routes
- `app/models.py`: SQLModel tables
- `app/schemas.py`: API response/request models
- `app/services/normalizer.py`: CSV row to conversation normalization
- `app/services/dedupe.py`: same-user, time-window, keyword placeholder dedupe
- `app/services/ai.py`: mock and OpenAI-compatible classification
- `app/services/reports.py`: weekly report and product action draft generation
- `app/services/webhooks.py`: Slack and Feishu/Lark webhook delivery
- `app/connectors/`: Intercom and Zendesk skeletons

## Frontend

Location: `frontend/`

Main pieces:

- `app/overview`: import sample data and inspect latest VoC items
- `app/trends`: simple count trend chart
- `app/clusters`: issue cluster cards
- `app/reports`: weekly report generation and webhook actions
- `app/actions`: bug and feature request drafts
- `app/settings`: local configuration visibility
- `lib/api.ts`: typed API client

## Data Flow

1. The user clicks **Import sample CSV**.
2. The frontend calls `POST /api/import/sample`.
3. The backend reads `sample-data/tickets.csv`.
4. Each row is normalized into a `Conversation`.
5. Dedupe checks existing VoC items for the same issue key and time window.
6. New issues are classified with mock or OpenAI-compatible classification.
7. Results are stored in SQLite.
8. Dashboard endpoints return metrics, items, clusters, reports, and drafts.

## Dedupe Design

The MVP uses an explainable placeholder:

- keyword-derived issue key
- same user check
- configurable time window

This is intentionally simple. It proves the workflow without implying production-grade semantic similarity.

## AI Design

Mock mode is default and requires no network calls.

When an API key is present, the classifier calls an OpenAI-compatible Chat Completions endpoint and validates the structured response. If validation fails, it falls back to mock classification.

## Persistence

SQLite is used for local development. The database file is ignored by git.

## Integration Boundaries

Slack and Feishu/Lark are outbound-only webhook pushes. Intercom and Zendesk are connector skeletons and do not call external APIs yet.
