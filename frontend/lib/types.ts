export type Dataset = {
  id: number;
  name: string;
  description: string | null;
  created_at: string;
};

export type TestCase = {
  id: number;
  dataset_id: number;
  input_text: string;
  expected_output: string | null;
  evaluation_type: string;
  created_at: string;
};

export type PromptVersion = {
  id: number;
  name: string;
  version: string;
  prompt_text: string;
  created_at: string;
};

export type Experiment = {
  id: number;
  name: string;
  dataset_id: number;
  prompt_version_id: number;
  model_name: string;
  created_at: string;
};

export type ExperimentRun = {
  id: number;
  experiment_id: number;
  test_case_id: number;
  output_text: string;
  latency_ms: number;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
  cost_usd: number;
  passed: boolean;
  score: number;
  created_at: string;
};

export type SummaryStats = {
  averageLatency: number;
  totalCost: number;
  passedCount: number;
  failedCount: number;
  totalRuns: number;
};

export type MetricsSummary = {
  dataset_count: number;
  test_case_count: number;
  prompt_version_count: number;
  experiment_count: number;
  run_count: number;
  average_latency_ms: number;
  total_cost_usd: number;
  passed_runs: number;
  failed_runs: number;
};
