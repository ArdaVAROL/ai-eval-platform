"use client";

import { useEffect, useState } from "react";

import { SectionCard } from "@/components/section-card";
import { SummaryCards } from "@/components/summary-cards";
import { api } from "@/lib/api";
import { buildSummary } from "@/lib/summary";
import { Experiment, ExperimentRun } from "@/lib/types";

export function RunsPage() {
  const [runs, setRuns] = useState<ExperimentRun[]>([]);
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const [runData, experimentData] = await Promise.all([api.listRuns(), api.listExperiments()]);
        setRuns(runData);
        setExperiments(experimentData);
      } catch (error) {
        setMessage(error instanceof Error ? error.message : "Failed to load runs");
      } finally {
        setLoading(false);
      }
    }

    void loadData();
  }, []);

  const stats = buildSummary(runs);

  return (
    <div className="page-grid">
      <SummaryCards stats={stats} />

      <SectionCard title="Runs" description="Recent local LLM run results with latency, token counts, and pass/fail scoring.">
        {message ? <p className="muted">{message}</p> : null}
        {loading ? (
          <p className="muted">Loading runs...</p>
        ) : (
          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>Experiment</th>
                  <th>Test Case</th>
                  <th>Latency</th>
                  <th>Tokens</th>
                  <th>Cost</th>
                  <th>Status</th>
                  <th>Output</th>
                </tr>
              </thead>
              <tbody>
                {runs.map((run) => {
                  const experiment = experiments.find((item) => item.id === run.experiment_id);
                  return (
                    <tr key={run.id}>
                      <td>{experiment?.name || run.experiment_id}</td>
                      <td>{run.test_case_id}</td>
                      <td>{run.latency_ms} ms</td>
                      <td>{run.total_tokens}</td>
                      <td>${run.cost_usd.toFixed(4)}</td>
                      <td>
                        <span className={`pill ${run.passed ? "success" : "fail"}`}>
                          {run.passed ? "Passed" : "Failed"}
                        </span>
                      </td>
                      <td>{run.output_text}</td>
                    </tr>
                  );
                })}
                {runs.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="muted">
                      No runs yet. Trigger a run from the Experiments page.
                    </td>
                  </tr>
                ) : null}
              </tbody>
            </table>
          </div>
        )}
      </SectionCard>
    </div>
  );
}
