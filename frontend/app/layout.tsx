import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";

import "./globals.css";

export const metadata: Metadata = {
  title: "AI Eval Platform",
  description: "Minimal MVP for evaluating prompt and model outputs.",
};

const navItems = [
  { href: "/", label: "Dashboard" },
  { href: "/datasets", label: "Datasets" },
  { href: "/prompt-versions", label: "Prompt Versions" },
  { href: "/experiments", label: "Experiments" },
  { href: "/runs", label: "Runs" },
];

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <div className="shell">
          <header className="topbar">
            <div>
              <div className="brand">AI Eval Platform</div>
              <div className="muted">Simple prompt evaluation MVP for datasets, experiments, and runs.</div>
            </div>
            <nav className="nav">
              {navItems.map((item) => (
                <Link key={item.href} href={item.href}>
                  {item.label}
                </Link>
              ))}
            </nav>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
