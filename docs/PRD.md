# Product Brief

## Product Name

OpenVoC Radar

## One-Line Summary

A local open-source MVP that turns synthetic support tickets into evidence-backed voice-of-customer insights, weekly reports, and product action drafts.

## Context

Customer feedback often lives in support tools, chat systems, and ticket queues. Product teams need to identify repeated issues and customer requests, but summaries lose trust when they are not tied back to source conversations.

## Target Users

- Product managers reviewing support themes
- Support leads preparing weekly feedback summaries
- Founders or small teams looking for lightweight VoC workflows
- Engineers evaluating AI-assisted product operations patterns

## MVP Goals

- Import synthetic ticket data from CSV.
- Normalize tickets into a consistent conversation schema.
- Deduplicate repeated issues with simple, explainable logic.
- Classify feedback into structured VoC items.
- Preserve source ticket IDs on every generated insight.
- Generate weekly Markdown reports.
- Generate bug and feature request drafts.
- Push reports to Slack or Feishu/Lark when webhooks are configured.
- Run locally without an API key through mock LLM mode.

## Non-Goals

- Production-grade semantic clustering
- Real customer data ingestion
- User authentication
- Multi-tenant workspace management
- Full Intercom or Zendesk integration
- Enterprise reporting or BI dashboards

## Key User Stories

- As a support lead, I can import a CSV of tickets and see a summary of customer issues.
- As a product manager, I can inspect issue clusters and verify the source tickets behind each insight.
- As a product manager, I can generate a bug draft or feature request draft with evidence attached.
- As a team lead, I can generate a weekly Markdown report and optionally push it to Slack or Feishu.
- As a developer, I can run the project locally without external AI credentials.

## Success Criteria

- A non-engineer can follow the demo flow locally with minimal setup.
- Every insight, report, and draft includes source ticket IDs.
- The project works without `OPENAI_API_KEY`.
- Optional webhook delivery fails safely when not configured.
- Backend tests and frontend build pass.

## Current Status

Verified local MVP. The workflow is intentionally constrained to synthetic data and local development.
