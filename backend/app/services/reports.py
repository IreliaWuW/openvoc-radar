from __future__ import annotations

from collections import Counter, defaultdict

from sqlmodel import Session, select

from app.models import ProductAction, Report, VocItem
from app.services.utils import join_ids, now_utc, split_ids


def generate_weekly_report(session: Session) -> Report:
    items = session.exec(select(VocItem).order_by(VocItem.created_at.desc())).all()
    source_ids: list[str] = []
    area_counter = Counter(item.product_area for item in items)
    severity_counter = Counter(item.severity.value for item in items)

    lines = [
        "# Weekly VoC Radar Report",
        "",
        "All insights below are derived from synthetic tickets and include source ticket IDs.",
        "",
        "## Summary",
        f"- Total VoC items: {len(items)}",
        f"- Product areas represented: {len(area_counter)}",
        f"- High severity items: {severity_counter.get('high', 0)}",
        "",
        "## Top Product Areas",
    ]
    if area_counter:
        for area, count in area_counter.most_common():
            lines.append(f"- {area}: {count}")
    else:
        lines.append("- No imported VoC items yet.")

    lines.extend(["", "## Open Issues"])
    for item in items:
        ids = split_ids(item.source_ticket_ids)
        source_ids.extend(ids)
        lines.append(
            f"- **{item.title}** ({item.item_type.value}, {item.severity.value}) "
            f"- {item.summary} Source tickets: {', '.join(ids)}"
        )

    report = Report(
        title="Weekly VoC Radar Report",
        markdown="\n".join(lines),
        source_ticket_ids=join_ids(source_ids),
        created_at=now_utc(),
    )
    session.add(report)
    session.commit()
    session.refresh(report)
    return report


def create_product_action_drafts(session: Session) -> list[ProductAction]:
    items = session.exec(select(VocItem).order_by(VocItem.created_at.desc())).all()
    existing = session.exec(select(ProductAction)).all()
    existing_keys = {(action.voc_item_id, action.draft_type) for action in existing}
    created: list[ProductAction] = []

    for item in items:
        if item.item_type.value not in {"bug", "feature_request"}:
            continue
        draft_type = "bug" if item.item_type.value == "bug" else "feature_request"
        if (item.id, draft_type) in existing_keys:
            continue

        ids = split_ids(item.source_ticket_ids)
        if draft_type == "bug":
            markdown = (
                f"## Bug Draft: {item.title}\n\n"
                f"**Problem**\n{item.summary}\n\n"
                f"**Severity**\n{item.severity.value}\n\n"
                f"**Source ticket IDs**\n{', '.join(ids)}\n"
            )
        else:
            markdown = (
                f"## Feature Request Draft: {item.title}\n\n"
                f"**Request**\n{item.summary}\n\n"
                f"**Product area**\n{item.product_area}\n\n"
                f"**Source ticket IDs**\n{', '.join(ids)}\n"
            )
        action = ProductAction(
            voc_item_id=item.id,
            draft_type=draft_type,
            title=item.title,
            markdown=markdown,
            source_ticket_ids=item.source_ticket_ids,
            created_at=now_utc(),
        )
        session.add(action)
        created.append(action)

    session.commit()
    for action in created:
        session.refresh(action)
    return created


def clusters(session: Session) -> list[dict]:
    items = session.exec(select(VocItem)).all()
    groups: dict[str, list[VocItem]] = defaultdict(list)
    for item in items:
        groups[item.cluster_key].append(item)

    output = []
    for key, group in groups.items():
        ids: list[str] = []
        for item in group:
            ids.extend(split_ids(item.source_ticket_ids))
        first = group[0]
        output.append(
            {
                "cluster_key": key,
                "title": first.title,
                "count": len(ids),
                "severity": first.severity,
                "product_area": first.product_area,
                "source_ticket_ids": list(dict.fromkeys(ids)),
            }
        )
    return sorted(output, key=lambda item: item["count"], reverse=True)
