"use client";

import { useEffect, useState } from "react";
import { ClipboardList } from "lucide-react";
import { api } from "@/lib/api";
import type { ProductAction } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function ActionsPage() {
  const [actions, setActions] = useState<ProductAction[]>([]);

  async function load() {
    setActions(await api.actions());
  }

  async function createDrafts() {
    const created = await api.createDrafts();
    setActions([...created, ...actions]);
  }

  useEffect(() => {
    load().catch(() => setActions([]));
  }, []);

  return (
    <div className="space-y-6 pb-16">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Product Actions</h1>
          <p className="text-sm text-muted-foreground">Bug and feature request drafts generated from classified VoC items.</p>
        </div>
        <Button onClick={createDrafts}>
          <ClipboardList className="h-4 w-4" />
          Generate drafts
        </Button>
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        {actions.map((action) => (
          <Card key={action.id}>
            <CardHeader>
              <CardTitle>{action.title}</CardTitle>
              <CardDescription>{action.draft_type.replace("_", " ")}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <pre className="max-h-72 overflow-auto rounded-md bg-muted p-4 text-sm whitespace-pre-wrap">{action.markdown}</pre>
              <div className="flex flex-wrap gap-1">
                {action.source_ticket_ids.map((id) => (
                  <Badge key={id}>{id}</Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
      {actions.length === 0 && <div className="rounded-lg border bg-white p-8 text-center text-sm text-muted-foreground">No product action drafts yet.</div>}
    </div>
  );
}
