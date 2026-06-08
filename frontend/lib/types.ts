export type Severity = "low" | "medium" | "high";
export type ItemType = "bug" | "feature_request" | "support_question" | "usability" | "pricing";

export type Metrics = {
  total_tickets: number;
  total_voc_items: number;
  open_items: number;
  high_severity_items: number;
};

export type VocItem = {
  id: number;
  conversation_id: number;
  source_ticket_ids: string[];
  cluster_key: string;
  title: string;
  summary: string;
  item_type: ItemType;
  severity: Severity;
  product_area: string;
  sentiment: string;
  confidence: number;
  status: string;
  created_at: string;
  updated_at: string;
};

export type TrendPoint = {
  date: string;
  count: number;
};

export type Cluster = {
  cluster_key: string;
  title: string;
  count: number;
  severity: Severity;
  product_area: string;
  source_ticket_ids: string[];
};

export type Report = {
  id: number;
  title: string;
  markdown: string;
  source_ticket_ids: string[];
  created_at: string;
};

export type ProductAction = {
  id: number;
  voc_item_id: number;
  draft_type: string;
  title: string;
  markdown: string;
  source_ticket_ids: string[];
  created_at: string;
};
