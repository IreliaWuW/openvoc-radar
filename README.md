# OpenVoC Radar

An open-source local MVP for turning support conversations into evidence-backed voice-of-customer insights, reports, and product action drafts.

OpenVoC Radar is built for a realistic product feedback loop: import ticket data, normalize it, deduplicate repeated issues, classify themes, and keep every insight tied back to source ticket IDs. It is intentionally small enough to run on a laptop and inspect end to end.

## Why This Exists

Support teams often have the clearest signal about customer pain, but that signal is scattered across tickets, chat tools, and CRM notes. Product teams need a way to see patterns without losing the evidence behind them.

This project demonstrates a practical VoC workflow:

- Convert raw conversations into a consistent schema.
- Group repeated issues without pretending to have perfect clustering.
- Use AI classification in a controlled, structured way.
- Preserve source ticket IDs on every insight, report, and product draft.
- Keep webhooks and external AI optional so the demo works locally.

It is not a finished enterprise platform. It is a portfolio-quality MVP that shows product thinking, full-stack execution, and responsible AI workflow design.

## Key Features

- Synthetic CSV ticket import from `sample-data/tickets.csv`
- Unified conversation schema backed by SQLite
- Deduplication by same user, time window, and a simple similarity placeholder
- Structured VoC item classification
- Mock LLM mode when no API key is configured
- Dashboard pages for Overview, Trends, Issue Clusters, Reports, Product Actions, and Settings
- Weekly Markdown report generation
- Bug draft and feature request draft generation
- Source ticket IDs attached to every generated insight
- Optional Slack and Feishu/Lark webhook delivery
- Connector skeletons for Intercom and Zendesk

## Screenshots

Planned screenshot locations:

- Overview dashboard: `docs/screenshots/overview.png`
- Issue clusters: `docs/screenshots/issue-clusters.png`
- Weekly report: `docs/screenshots/weekly-report.png`
- Product action drafts: `docs/screenshots/product-actions.png`

No screenshots are committed yet.

## Demo Workflow

1. Start the FastAPI backend.
2. Start the Next.js frontend.
3. Open the dashboard at `http://localhost:3000`.
4. Click **Import sample CSV** on the Overview page.
5. Review the imported ticket count, deduped VoC items, and source ticket IDs.
6. Open Issue Clusters to explain repeated issue grouping.
7. Generate a weekly report from Reports.
8. Generate bug and feature drafts from Product Actions.
9. Try Slack or Lark delivery without webhook URLs configured to show safe optional behavior.

See [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md) for a presenter-friendly walkthrough.

## Architecture Overview

```text
sample-data/tickets.csv
        |
        v
FastAPI import endpoint
        |
        v
normalize -> dedupe -> classify -> persist
        |
        v
SQLite + SQLModel
        |
        v
Next.js dashboard + Recharts
        |
        v
Markdown reports, product drafts, optional webhooks
```

More detail: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Tech Stack

Frontend:

- Next.js
- React
- Tailwind CSS
- shadcn-style local UI primitives
- Recharts
- lucide-react icons

Backend:

- FastAPI
- Python
- SQLite
- SQLModel
- Pydantic settings
- pytest

AI and integrations:

- OpenAI-compatible Chat Completions endpoint
- Deterministic mock classifier when `OPENAI_API_KEY` is blank
- Slack incoming webhook
- Feishu/Lark bot webhook
- Intercom and Zendesk connector skeletons

## Quick Start: Windows PowerShell

From the project root:

```powershell
Copy-Item .env.example backend\.env
Copy-Item .env.example frontend\.env.local
```

Create and start the backend:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Start the frontend in a second terminal:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Open `http://localhost:3000`.

If `python` is not available on Windows, try `py -3 -m venv .venv`, or install Python 3.11+ and add it to PATH.

## Backend Commands

```powershell
cd backend
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Python 3.14.5 has been verified for this project. Python 3.11+ should also be suitable for this stack.

## Frontend Commands

```powershell
cd frontend
npm.cmd install
npm.cmd run check
npm.cmd run build
npm.cmd run dev
```

## Local URLs

- Frontend dashboard: `http://localhost:3000`
- Backend API health: `http://127.0.0.1:8000/api/health`
- Backend API docs: `http://127.0.0.1:8000/docs`

## Sample Data

The MVP uses only synthetic data in [sample-data/tickets.csv](sample-data/tickets.csv).

The sample includes:

- Repeated CSV export complaints from the same user
- Login, billing, mobile, search, notifications, reporting, and integration examples
- Intercom and Zendesk requests represented as synthetic tickets

The demo import creates 12 conversations and 11 VoC items because one repeated issue is deduplicated.

## Mock LLM Mode

Mock mode is the default. Leave `OPENAI_API_KEY` blank in `backend/.env` and the backend uses deterministic local classification logic.

To use an OpenAI-compatible endpoint:

```powershell
OPENAI_API_KEY=your-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

The classifier expects a Chat Completions-compatible API. If the response cannot be validated against the structured schema, the backend falls back to mock classification.

## Evidence-Backed Insight Design

OpenVoC Radar intentionally keeps source ticket IDs attached throughout the workflow:

- `VocItem.source_ticket_ids`
- issue cluster source IDs
- weekly report source IDs
- bug draft source IDs
- feature request draft source IDs

This avoids the common AI product failure mode where generated summaries are detached from the evidence a product manager or support lead needs to verify them.

The MVP does not invent revenue impact, customer counts, priority scores, or unsupported metrics. Counts shown in the dashboard are derived from imported synthetic rows and generated VoC items.

## Slack and Feishu/Lark Webhooks

Webhooks are optional. If no webhook URL is configured, the app returns a clear "not configured" response and does not pretend delivery happened.

Set one or both in `backend/.env`:

```powershell
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
LARK_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/...
# FEISHU_WEBHOOK_URL=... also works instead of LARK_WEBHOOK_URL
```

Webhook safety choices:

- HTTPS-only webhook URLs
- empty report bodies are rejected
- payload text is capped
- network errors return safe failure messages

## Intercom and Zendesk Connector Skeletons

Connector skeletons live in `backend/app/connectors/`.

They define a shared connector contract and placeholder `fetch_tickets()` methods for:

- Intercom conversations
- Zendesk tickets

The MVP does not call external connector APIs yet. The skeletons show where authenticated source integrations would plug into the same normalization and import pipeline.

## Privacy and Safety Notes

- The repository includes synthetic data only.
- No real customer data is required for the demo.
- Mock LLM mode avoids external AI calls.
- Webhooks are opt-in and fail closed when not configured.
- The app is designed for local development, not production deployment.
- If real ticket data is added later, scrub personal data before importing or sharing reports.

## Repository Topics

Suggested GitHub topics:

`voice-of-customer`, `product-feedback`, `support-ops`, `fastapi`, `nextjs`, `sqlite`, `sqlmodel`, `ai-workflows`, `openai-compatible`, `slack-webhook`, `lark-webhook`, `portfolio-project`

## Roadmap

Near-term:

- Add real embedding-based similarity for dedupe.
- Add CSV upload UI in the dashboard.
- Add source filters by product area and date.
- Add screenshot assets for the README.

Later:

- Implement Intercom and Zendesk connectors.
- Add authenticated multi-workspace support.
- Add review states for generated reports and drafts.
- Add export to GitHub Issues, Linear, or Jira.

See [docs/ROADMAP.md](docs/ROADMAP.md).

## Limitations

- Similarity is a placeholder, not semantic clustering.
- Mock classification is deterministic and simple.
- Real OpenAI-compatible API mode requires a valid API key.
- Slack and Feishu/Lark delivery require webhook URLs.
- SQLite is appropriate for the local MVP, not high-volume production use.

## Contributing

Contributions are welcome, especially around:

- connector implementations
- better dedupe logic
- test coverage
- documentation clarity
- UX improvements that keep the MVP simple

Please keep changes small and evidence-oriented. Generated insights should continue to include source ticket IDs.

## License

MIT is recommended for this repository. See [LICENSE](LICENSE).

## Portfolio / Interview Talking Points

- Shows full-stack MVP delivery with a clear product workflow.
- Demonstrates responsible AI design by preserving evidence and supporting mock mode.
- Uses pragmatic architecture: simple SQLite persistence, typed API boundaries, local-first demo.
- Models a realistic support-to-product feedback loop.
- Includes integration design without pretending external systems are already implemented.
- Keeps metrics honest and derived from imported data.
