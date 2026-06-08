"use client";

import { useEffect, useMemo, useState } from "react";
import { Bar, BarChart, CartesianGrid, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "@/lib/api";
import type { TrendCategory, TrendSummary } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

const chartColors = ["#0f766e", "#be3455", "#b7791f", "#2563eb", "#6d5bd0", "#64748b"];

const labelStyles: Record<TrendCategory["trend_label"], string> = {
  New: "border-teal-200 bg-teal-50 text-teal-800",
  Rising: "border-rose-200 bg-rose-50 text-rose-800",
  Persistent: "border-amber-200 bg-amber-50 text-amber-800",
  Converging: "border-slate-200 bg-slate-50 text-slate-700"
};

export default function TrendsPage() {
  const [summary, setSummary] = useState<TrendSummary | null>(null);
  const [mounted, setMounted] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    setMounted(true);
    api
      .trendSummary()
      .then(setSummary)
      .catch(() => setMessage("Start the FastAPI backend and import sample data to review trends."));
  }, []);

  const categories = useMemo(() => {
    const names = new Set<string>();
    summary?.chart.forEach((row) => {
      Object.keys(row).forEach((key) => {
        if (key !== "period") {
          names.add(key);
        }
      });
    });
    return Array.from(names);
  }, [summary]);

  const currentPeriod = summary?.current_period ?? "Current period";
  const previousPeriod = summary?.previous_period ?? "Previous period";

  return (
    <div className="space-y-6 pb-16">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-semibold">Issue trends</h1>
        <p className="text-sm text-muted-foreground">
          Current period vs previous period. Counts come only from imported synthetic VoC items.
        </p>
      </div>

      {message && <div className="rounded-md border bg-white px-4 py-3 text-sm">{message}</div>}

      <div className="grid gap-4 lg:grid-cols-[1.15fr_0.85fr]">
        <Card className="min-w-0">
          <CardHeader>
            <CardTitle>VoC count by issue type</CardTitle>
            <CardDescription>Period-over-period view across the weeks present in the sample data.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[340px] w-full overflow-x-auto">
              {mounted && summary && summary.chart.length > 0 && (
                <BarChart width={680} height={320} data={summary.chart}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="period" tickLine={false} axisLine={false} />
                  <YAxis allowDecimals={false} tickLine={false} axisLine={false} />
                  <Tooltip />
                  {categories.map((category, index) => (
                    <Bar
                      key={category}
                      dataKey={category}
                      fill={chartColors[index % chartColors.length]}
                      radius={[4, 4, 0, 0]}
                    />
                  ))}
                </BarChart>
              )}
              {summary?.chart.length === 0 && (
                <div className="flex h-full items-center justify-center text-sm text-muted-foreground">
                  Import the sample CSV from Overview to populate trend data.
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Trend labels</CardTitle>
            <CardDescription>Simple labels for demo review, not forecasting.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-3 text-sm">
            <LabelNote label="New" text="Current period has items, previous period had none." />
            <LabelNote label="Rising" text="Current count is higher than previous count." />
            <LabelNote label="Persistent" text="Current and previous counts are the same." />
            <LabelNote label="Converging" text="Current count is lower than previous count." />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <CardTitle>Current vs previous period</CardTitle>
              <CardDescription>
                {currentPeriod} compared with {previousPeriod}; source ticket IDs are representative examples.
              </CardDescription>
            </div>
            <div className="text-sm font-medium text-muted-foreground">period-over-period</div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[860px] text-left text-sm">
              <thead className="border-b text-xs uppercase text-muted-foreground">
                <tr>
                  <th className="py-3 pr-4">Issue type</th>
                  <th className="py-3 pr-4">{currentPeriod}</th>
                  <th className="py-3 pr-4">{previousPeriod}</th>
                  <th className="py-3 pr-4">Change</th>
                  <th className="py-3 pr-4">Trend</th>
                  <th className="py-3 pr-4">High severity</th>
                  <th className="py-3">Source ticket IDs</th>
                </tr>
              </thead>
              <tbody>
                {summary?.categories.map((row) => (
                  <tr key={row.category} className="border-b last:border-0">
                    <td className="py-4 pr-4 font-medium">{row.category}</td>
                    <td className="py-4 pr-4 text-2xl font-semibold">{row.current_count}</td>
                    <td className="py-4 pr-4 text-lg text-muted-foreground">{row.previous_count}</td>
                    <td className="py-4 pr-4 font-medium">{formatChange(row.change_percent)}</td>
                    <td className="py-4 pr-4">
                      <Badge className={cn("font-semibold", labelStyles[row.trend_label])}>{row.trend_label}</Badge>
                    </td>
                    <td className="py-4 pr-4">{row.high_severity_count}</td>
                    <td className="py-4">
                      <div className="flex flex-wrap gap-1">
                        {row.source_ticket_ids.map((id) => (
                          <Badge key={id}>{id}</Badge>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {summary?.categories.length === 0 && (
              <div className="flex h-32 items-center justify-center text-sm text-muted-foreground">
                Import sample data to calculate issue trends.
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function formatChange(value: number | null) {
  if (value === null) {
    return "New";
  }
  if (value > 0) {
    return `+${value}%`;
  }
  if (value < 0) {
    return `${value}%`;
  }
  return "0%";
}

function LabelNote({ label, text }: { label: TrendCategory["trend_label"]; text: string }) {
  return (
    <div className="flex items-start gap-3 rounded-md border bg-white p-3">
      <Badge className={cn("font-semibold", labelStyles[label])}>{label}</Badge>
      <span className="text-muted-foreground">{text}</span>
    </div>
  );
}
