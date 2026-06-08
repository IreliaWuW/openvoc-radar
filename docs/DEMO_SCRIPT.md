# Demo Script

## Setup

Open two terminals.

Backend:

```powershell
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Frontend:

```powershell
cd frontend
npm.cmd run dev
```

Open:

```text
http://localhost:3000
```

## Talk Track

### 1. Position The Project

"OpenVoC Radar is a local MVP for turning support tickets into evidence-backed product feedback. The key design choice is that every generated insight keeps source ticket IDs attached."

### 2. Import Sample CSV

On the Overview page, click **Import sample CSV**.

Explain:

- The CSV is synthetic and lives in `sample-data/tickets.csv`.
- Each row becomes a normalized conversation.
- The import pipeline runs normalization, dedupe, and classification.
- With no API key, classification uses deterministic mock mode.

### 3. Explain Deduplication

Point to the imported count and VoC item count.

Expected demo behavior:

- 12 tickets imported
- 11 VoC items created

Explain:

"The sample includes two CSV export complaints from the same user inside the dedupe window. The MVP merges those into one VoC item while preserving both ticket IDs."

### 4. Explain Evidence-Backed Source IDs

On Overview or Issue Clusters, point to source ticket badges.

Explain:

"The app never shows an AI-generated insight without evidence. Source IDs travel through items, clusters, reports, and product drafts."

### 5. Issue Clusters

Open **Issue Clusters**.

Explain:

- Clusters group related ticket IDs under a simple issue key.
- This is a placeholder for future embedding-based similarity.
- The MVP keeps the method explainable for demo and review.

### 6. Weekly Report

Open **Reports** and click **Generate weekly report**.

Explain:

- The Markdown report is generated from stored VoC items.
- It includes derived counts only.
- Each open issue includes source ticket IDs.

### 7. Product Action Drafts

Open **Product Actions** and click **Generate drafts**.

Explain:

- Bug items become bug drafts.
- Feature request items become feature request drafts.
- Drafts include the source ticket IDs needed for product triage.

### 8. Slack and Feishu/Lark Webhooks

On Reports, click Slack or Lark without webhook URLs configured.

Explain:

"Webhooks are optional. In local demo mode, the app returns a safe not-configured message. If a webhook URL is added to `backend/.env`, the same report can be pushed out."

### 9. Close

"The project is intentionally not a finished platform. It is a verified MVP showing a practical support-to-product feedback loop, responsible AI fallback behavior, and evidence-backed outputs."

## Useful URLs

- Dashboard: `http://localhost:3000`
- API docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api/health`
