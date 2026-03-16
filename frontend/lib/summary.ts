import { ExperimentRun, SummaryStats } from "@/lib/types";

export function buildSummary(runs: ExperimentRun[]): SummaryStats {
  if (runs.length === 0) {
    return {
      averageLatency: 0,
      totalCost: 0,
      passedCount: 0,
      failedCount: 0,
      totalRuns: 0,
    };
  }

  const totalLatency = runs.reduce((sum, run) => sum + run.latency_ms, 0);
  const totalCost = runs.reduce((sum, run) => sum + run.cost_usd, 0);
  const passedCount = runs.filter((run) => run.passed).length;

  return {
    averageLatency: totalLatency / runs.length,
    totalCost,
    passedCount,
    failedCount: runs.length - passedCount,
    totalRuns: runs.length,
  };
}
