"use client";

import { Server, Settings } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export default function SettingsPage() {
  return (
    <div className="space-y-6 pb-16">
      <div>
        <h1 className="text-2xl font-semibold">Settings</h1>
        <p className="text-sm text-muted-foreground">Local configuration for the MVP.</p>
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Server className="h-4 w-4" />
              API
            </CardTitle>
            <CardDescription>Frontend requests are sent here.</CardDescription>
          </CardHeader>
          <CardContent>
            <Input readOnly value={apiUrl} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Settings className="h-4 w-4" />
              Mock mode
            </CardTitle>
            <CardDescription>Leave OPENAI_API_KEY empty to use deterministic mock classification.</CardDescription>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Slack and Lark webhook URLs are optional. Webhook buttons return a clear message when they are not configured.
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
