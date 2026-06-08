"use client";

import { useEffect, useState } from "react";
import { Database, RefreshCw, Upload } from "lucide-react";
import { api } from "@/lib/api";
import type { Metrics, VocItem } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function OverviewPage() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [items, setItems] = useState<VocItem[]>([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function load() {
    const [nextMetrics, nextItems] = await Promise.all([api.metrics(), api.items()]);
    setMetrics(nextMetrics);
    setItems(nextItems);
  }

  async function importSample() {
    setLoading(true);
    try {
      const result = await api.importSample();
      setMessage(`Imported ${result.imported} tickets, skipped ${result.skipped_existing}, created ${result.classified_items} VoC items.`);
      await load();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Import failed.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load().catch(() => setMessage("Start the FastAPI backend on port 8000, then refresh."));
  }, []);

  return (
    <div className="space-y-6 pb-16">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Overview</h1>
          <p className="text-sm text-muted-foreground">Synthetic ticket import and VoC item rollup.</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="icon" onClick={() => load()} aria-label="Refresh data" title="Refresh data">
            <RefreshCw className="h-4 w-4" />
          </Button>
          <Button onClick={importSample} disabled={loading}>
            <Upload className="h-4 w-4" />
            Import sample CSV
          </Button>
        </div>
      </div>

      {message && <div className="rounded-md border bg-white px-4 py-3 text-sm">{message}</div>}

      <div className="grid gap-4 md:grid-cols-4">
        <Metric label="Tickets" value={metrics?.total_tickets ?? 0} />
        <Metric label="VoC items" value={metrics?.total_voc_items ?? 0} />
        <Metric label="Open items" value={metrics?.open_items ?? 0} />
        <Metric label="High severity" value={metrics?.high_severity_items ?? 0} />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Latest VoC Items</CardTitle>
          <CardDescription>Each row shows the source synthetic ticket IDs behind the insight.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[760px] text-left text-sm">
              <thead className="border-b text-xs uppercase text-muted-foreground">
                <tr>
                  <th className="py-2 pr-4">Item</th>
                  <th className="py-2 pr-4">Type</th>
                  <th className="py-2 pr-4">Severity</th>
                  <th className="py-2 pr-4">Area</th>
                  <th className="py-2">Source tickets</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item) => (
                  <tr key={item.id} className="border-b last:border-0">
                    <td className="max-w-md py-3 pr-4">
                      <div className="font-medium">{item.title}</div>
                      <div className="line-clamp-2 text-muted-foreground">{item.summary}</div>
                    </td>
                    <td className="py-3 pr-4">{item.item_type.replace("_", " ")}</td>
                    <td className="py-3 pr-4">
                      <Badge>{item.severity}</Badge>
                    </td>
                    <td className="py-3 pr-4">{item.product_area}</td>
                    <td className="py-3">
                      <div className="flex flex-wrap gap-1">
                        {item.source_ticket_ids.map((id) => (
                          <Badge key={id}>{id}</Badge>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {items.length === 0 && (
              <div className="flex h-32 items-center justify-center gap-2 text-sm text-muted-foreground">
                <Database className="h-4 w-4" />
                Import the sample CSV to populate the radar.
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <Card>
      <CardHeader className="pb-2">
        <CardDescription>{label}</CardDescription>
        <CardTitle className="text-3xl">{value}</CardTitle>
      </CardHeader>
    </Card>
  );
}
