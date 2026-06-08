# Roadmap

## Current MVP

- CSV import with synthetic data
- Normalized conversation schema
- Simple dedupe placeholder
- Mock and OpenAI-compatible classification
- Dashboard pages
- Weekly Markdown reports
- Bug and feature request drafts
- Optional Slack and Feishu/Lark webhooks
- Intercom and Zendesk connector skeletons

## Near-Term Improvements

- Add dashboard CSV upload UI.
- Add filters by date, product area, item type, and severity.
- Replace keyword issue keys with embedding-assisted similarity.
- Add report preview/edit before webhook delivery.
- Add committed screenshot assets for GitHub.
- Expand backend tests for uploaded CSV and webhook validation.

## Connector Work

- Implement Intercom conversation fetch.
- Implement Zendesk ticket fetch.
- Map source metadata into the unified `Conversation` schema.
- Add connector-specific sync logs and error handling.

## Product Workflow

- Add triage states for VoC items.
- Add owner and due date fields for product actions.
- Add export to GitHub Issues, Linear, or Jira.
- Add review/approval states for generated drafts.

## Production Hardening

- Add authentication.
- Add workspace/project isolation.
- Move from SQLite to Postgres.
- Add background jobs for imports and report generation.
- Add observability and structured logging.
- Add data retention controls.

## Not Planned For The MVP

- Real customer data bundled in the repo
- Enterprise permissions
- Full BI analytics
- Fully autonomous product prioritization
