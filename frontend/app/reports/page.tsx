"use client";

import { useEffect, useState } from "react";
import { FileText, Send } from "lucide-react";
import { api } from "@/lib/api";
import type { Report } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function ReportsPage() {
  const [reports, setReports] = useState<Report[]>([]);
  const [message, setMessage] = useState("");

  async function load() {
    setReports(await api.reports());
  }

  async function generate() {
    const report = await api.createReport();
    setReports([report, ...reports]);
  }

  async function push(destination: "slack" | "lark", markdown: string) {
    const result = await api.pushWebhook(destination, markdown);
    setMessage(result.message);
  }

  useEffect(() => {
    load().catch(() => setReports([]));
  }, []);

  return (
    <div className="space-y-6 pb-16">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Reports</h1>
          <p className="text-sm text-muted-foreground">Weekly Markdown reports retain source ticket IDs.</p>
        </div>
        <Button onClick={generate}>
          <FileText className="h-4 w-4" />
          Generate weekly report
        </Button>
      </div>

      {message && <div className="rounded-md border bg-white px-4 py-3 text-sm">{message}</div>}

      <div className="space-y-4">
        {reports.map((report) => (
          <Card key={report.id}>
            <CardHeader>
              <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <CardTitle>{report.title}</CardTitle>
                  <CardDescription>{new Date(report.created_at).toLocaleString()}</CardDescription>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" onClick={() => push("slack", report.markdown)}>
                    <Send className="h-4 w-4" />
                    Slack
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => push("lark", report.markdown)}>
                    <Send className="h-4 w-4" />
                    Lark
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <pre className="max-h-96 overflow-auto rounded-md bg-muted p-4 text-sm whitespace-pre-wrap">{report.markdown}</pre>
              <div className="flex flex-wrap gap-1">
                {report.source_ticket_ids.map((id) => (
                  <Badge key={id}>{id}</Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
      {reports.length === 0 && <div className="rounded-lg border bg-white p-8 text-center text-sm text-muted-foreground">No reports generated yet.</div>}
    </div>
  );
}
