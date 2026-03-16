import { Dataset, Experiment, ExperimentRun, MetricsSummary, PromptVersion, TestCase } from "@/lib/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export const api = {
  listDatasets: () => request<Dataset[]>("/datasets"),
  createDataset: (payload: { name: string; description?: string }) =>
    request<Dataset>("/datasets", { method: "POST", body: JSON.stringify(payload) }),

  listTestCases: () => request<TestCase[]>("/test-cases"),
  createTestCase: (payload: {
    dataset_id: number;
    input_text: string;
    expected_output?: string;
    evaluation_type?: string;
  }) => request<TestCase>("/test-cases", { method: "POST", body: JSON.stringify(payload) }),

  listPromptVersions: () => request<PromptVersion[]>("/prompt-versions"),
  createPromptVersion: (payload: { name: string; version: string; prompt_text: string }) =>
    request<PromptVersion>("/prompt-versions", { method: "POST", body: JSON.stringify(payload) }),

  listExperiments: () => request<Experiment[]>("/experiments"),
  createExperiment: (payload: {
    name: string;
    dataset_id: number;
    prompt_version_id: number;
    model_name: string;
  }) => request<Experiment>("/experiments", { method: "POST", body: JSON.stringify(payload) }),

  listRuns: () => request<ExperimentRun[]>("/runs"),
  getMetricsSummary: () => request<MetricsSummary>("/metrics/summary"),
  triggerExperimentRun: (experimentId: number) =>
    request<{ experiment_id: number; created_runs: number; runs: ExperimentRun[] }>(
      `/experiments/${experimentId}/run`,
      { method: "POST" }
    ),
};
