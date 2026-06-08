"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BarChart3,
  FileText,
  Gauge,
  GitBranch,
  KanbanSquare,
  ListChecks,
  Settings
} from "lucide-react";
import { cn } from "@/lib/utils";

const nav = [
  { href: "/overview", label: "Overview", icon: Gauge },
  { href: "/trends", label: "Trends", icon: BarChart3 },
  { href: "/clusters", label: "Issue Clusters", icon: GitBranch },
  { href: "/reports", label: "Reports", icon: FileText },
  { href: "/actions", label: "Product Actions", icon: KanbanSquare },
  { href: "/settings", label: "Settings", icon: Settings }
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  return (
    <div className="min-h-screen">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r bg-white lg:block">
        <div className="flex h-16 items-center gap-2 border-b px-5">
          <ListChecks className="h-6 w-6 text-primary" />
          <div>
            <div className="text-sm font-semibold">OpenVoC Radar</div>
            <div className="text-xs text-muted-foreground">Synthetic MVP</div>
          </div>
        </div>
        <nav className="space-y-1 p-3">
          {nav.map((item) => {
            const Icon = item.icon;
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex h-10 items-center gap-3 rounded-md px-3 text-sm text-muted-foreground hover:bg-muted hover:text-foreground",
                  active && "bg-muted text-foreground"
                )}
              >
                <Icon className="h-4 w-4" />
                {item.label}
              </Link>
            );
          })}
        </nav>
      </aside>
      <div className="lg:pl-64">
        <header className="sticky top-0 z-10 flex h-16 items-center justify-between border-b bg-white/95 px-4 lg:px-8">
          <div>
            <div className="text-sm font-semibold">Voice-of-customer radar</div>
            <div className="text-xs text-muted-foreground">Every insight keeps source ticket IDs attached.</div>
          </div>
        </header>
        <main className="px-4 py-6 lg:px-8">{children}</main>
      </div>
      <nav className="fixed inset-x-0 bottom-0 grid grid-cols-6 border-t bg-white lg:hidden">
        {nav.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              aria-label={item.label}
              className={cn("flex h-14 items-center justify-center text-muted-foreground", active && "text-primary")}
            >
              <Icon className="h-5 w-5" />
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
