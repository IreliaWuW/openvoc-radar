import type { Cluster, Metrics, ProductAction, Report, TrendPoint, TrendSummary, VocItem } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers
    },
    cache: "no-store"
  });
  if (!response.ok) {
    throw new Error(await response.text());
  }
  return response.json() as Promise<T>;
}

export const api = {
  importSample: () => request<{ imported: number; skipped_existing: number; classified_items: number }>("/api/import/sample", { method: "POST" }),
  metrics: () => request<Metrics>("/api/metrics"),
  items: () => request<VocItem[]>("/api/items"),
  trends: () => request<TrendPoint[]>("/api/trends"),
  trendSummary: () => request<TrendSummary>("/api/trends/summary"),
  clusters: () => request<Cluster[]>("/api/clusters"),
  reports: () => request<Report[]>("/api/reports"),
  createReport: () => request<Report>("/api/reports/weekly", { method: "POST" }),
  actions: () => request<ProductAction[]>("/api/actions"),
  createDrafts: () => request<ProductAction[]>("/api/actions/drafts", { method: "POST" }),
  pushWebhook: (destination: "slack" | "lark", markdown: string) =>
    request<{ ok: boolean; message: string; destination: string }>("/api/webhooks/push", {
      method: "POST",
      body: JSON.stringify({ destination, markdown })
    })
};
