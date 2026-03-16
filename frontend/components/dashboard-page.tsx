"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { SectionCard } from "@/components/section-card";
import { SummaryCards } from "@/components/summary-cards";
import { api } from "@/lib/api";
import { Dataset, Experiment, MetricsSummary, PromptVersion } from "@/lib/types";

export function DashboardPage() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [promptVersions, setPromptVersions] = useState<PromptVersion[]>([]);
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [metrics, setMetrics] = useState<MetricsSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const [datasetData, promptVersionData, experimentData, metricsData] = await Promise.all([
          api.listDatasets(),
          api.listPromptVersions(),
          api.listExperiments(),
          api.getMetricsSummary(),
        ]);
        setDatasets(datasetData);
        setPromptVersions(promptVersionData);
        setExperiments(experimentData);
        setMetrics(metricsData);
      } catch (error) {
        setMessage(error instanceof Error ? error.message : "Failed to load dashboard");
      } finally {
        setLoading(false);
      }
    }

    void loadData();
  }, []);

  const stats = {
    averageLatency: metrics?.average_latency_ms ?? 0,
    totalCost: metrics?.total_cost_usd ?? 0,
    passedCount: metrics?.passed_runs ?? 0,
    failedCount: metrics?.failed_runs ?? 0,
    totalRuns: metrics?.run_count ?? 0,
  };

  return (
    <div className="page-grid">
      <section className="card hero">
        <h1 className="section-title">Evaluation dashboard</h1>
        <p className="section-copy">
          Track datasets, prompt versions, experiments, and local Ollama runs from one place.
        </p>
        <div className="inline-actions">
          <Link className="button" href="/datasets">
            Manage Datasets
          </Link>
          <Link className="button secondary" href="/experiments">
            Open Experiments
          </Link>
        </div>
      </section>

      <SummaryCards stats={stats} />

      <div className="two-col">
        <SectionCard title="Platform Snapshot" description="Counts for the main resources in the MVP.">
          {loading ? (
            <p className="muted">Loading snapshot...</p>
          ) : (
            <div className="stats-grid">
              <div>
                <div className="muted">Datasets</div>
                <div className="stat-value">{datasets.length}</div>
              </div>
              <div>
                <div className="muted">Prompt Versions</div>
                <div className="stat-value">{promptVersions.length}</div>
              </div>
              <div>
                <div className="muted">Experiments</div>
                <div className="stat-value">{experiments.length}</div>
              </div>
              <div>
                <div className="muted">Runs</div>
                <div className="stat-value">{metrics?.run_count ?? 0}</div>
              </div>
            </div>
          )}
        </SectionCard>

        <SectionCard title="What this MVP measures" description="A lightweight summary for demos and interviews.">
          <p className="muted">Latency comes from real local Ollama calls stored per test case.</p>
          <p className="muted">Cost stays at zero for local runs, while token counts are stored when Ollama returns them.</p>
          <p className="muted">Pass/fail uses a simple deterministic string-based comparison against expected output.</p>
          {message ? <p className="muted">{message}</p> : null}
        </SectionCard>
      </div>
    </div>
  );
}
