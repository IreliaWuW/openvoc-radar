"use client";

import { useEffect, useState } from "react";
import { GitBranch } from "lucide-react";
import { api } from "@/lib/api";
import type { Cluster } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function ClustersPage() {
  const [clusters, setClusters] = useState<Cluster[]>([]);

  useEffect(() => {
    api.clusters().then(setClusters).catch(() => setClusters([]));
  }, []);

  return (
    <div className="space-y-6 pb-16">
      <div>
        <h1 className="text-2xl font-semibold">Issue Clusters</h1>
        <p className="text-sm text-muted-foreground">Deduplication uses same user, time window, and a similarity placeholder key.</p>
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        {clusters.map((cluster) => (
          <Card key={cluster.cluster_key}>
            <CardHeader>
              <div className="flex items-start justify-between gap-4">
                <div>
                  <CardTitle>{cluster.title}</CardTitle>
                  <CardDescription>{cluster.product_area}</CardDescription>
                </div>
                <Badge>{cluster.severity}</Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="text-sm">
                <span className="font-medium">{cluster.count}</span> linked source ticket{cluster.count === 1 ? "" : "s"}
              </div>
              <div className="flex flex-wrap gap-1">
                {cluster.source_ticket_ids.map((id) => (
                  <Badge key={id}>{id}</Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
      {clusters.length === 0 && (
        <div className="flex h-40 items-center justify-center gap-2 rounded-lg border bg-white text-sm text-muted-foreground">
          <GitBranch className="h-4 w-4" />
          No clusters yet.
        </div>
      )}
    </div>
  );
}
