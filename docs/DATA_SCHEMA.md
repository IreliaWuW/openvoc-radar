# Data Schema

OpenVoC Radar uses SQLite through SQLModel.

## Conversation

Represents a normalized source ticket or support conversation.

Fields:

- `id`: internal primary key
- `source`: source system, such as `csv`
- `external_id`: source ticket ID, unique
- `user_id`: synthetic user identifier
- `user_email`: optional synthetic user email
- `created_at`: conversation timestamp
- `subject`: ticket subject
- `body`: ticket body
- `product_area`: optional product area hint
- `tags`: optional comma-separated source tags

## VocItem

Represents a classified voice-of-customer item.

Fields:

- `id`: internal primary key
- `conversation_id`: first conversation associated with the item
- `source_ticket_ids`: comma-separated source ticket IDs
- `cluster_key`: dedupe and grouping key
- `title`: concise issue title
- `summary`: issue summary
- `item_type`: `bug`, `feature_request`, `support_question`, `usability`, or `pricing`
- `severity`: `low`, `medium`, or `high`
- `product_area`: product area
- `sentiment`: simple sentiment label
- `confidence`: classifier confidence
- `status`: `new`, `triaged`, `planned`, or `closed`
- `created_at`: source conversation timestamp
- `updated_at`: item update timestamp

## Report

Represents a generated weekly Markdown report.

Fields:

- `id`: internal primary key
- `title`: report title
- `markdown`: generated Markdown body
- `source_ticket_ids`: all source ticket IDs referenced in the report
- `created_at`: report timestamp

## ProductAction

Represents a generated bug or feature request draft.

Fields:

- `id`: internal primary key
- `voc_item_id`: source VoC item
- `draft_type`: `bug` or `feature_request`
- `title`: draft title
- `markdown`: generated Markdown body
- `source_ticket_ids`: source ticket IDs referenced in the draft
- `created_at`: draft timestamp

## Traceability Rule

Any generated insight must include source ticket IDs. This is the main data integrity rule of the project.
