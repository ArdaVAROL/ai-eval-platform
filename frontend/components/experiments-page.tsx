"use client";

import { FormEvent, useEffect, useState } from "react";

import { SectionCard } from "@/components/section-card";
import { api } from "@/lib/api";
import { Dataset, Experiment, PromptVersion } from "@/lib/types";

export function ExperimentsPage() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [promptVersions, setPromptVersions] = useState<PromptVersion[]>([]);
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [runLoadingId, setRunLoadingId] = useState<number | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  async function loadData() {
    setLoading(true);
    try {
      const [datasetData, promptVersionData, experimentData] = await Promise.all([
        api.listDatasets(),
        api.listPromptVersions(),
        api.listExperiments(),
      ]);
      setDatasets(datasetData);
      setPromptVersions(promptVersionData);
      setExperiments(experimentData);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Failed to load experiments");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadData();
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setMessage(null);
    const formData = new FormData(event.currentTarget);

    try {
      await api.createExperiment({
        name: String(formData.get("name")),
        dataset_id: Number(formData.get("dataset_id")),
        prompt_version_id: Number(formData.get("prompt_version_id")),
        model_name: String(formData.get("model_name")),
      });
      event.currentTarget.reset();
      await loadData();
      setMessage("Experiment created.");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Failed to create experiment");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleRun(experimentId: number) {
    setRunLoadingId(experimentId);
    setMessage(null);
    try {
      const result = await api.triggerExperimentRun(experimentId);
      setMessage(`Created ${result.created_runs} local LLM run records.`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Failed to trigger experiment run");
    } finally {
      setRunLoadingId(null);
    }
  }

  return (
    <div className="page-grid">
      <SectionCard title="Create Experiment" description="Connect a dataset, prompt version, and model name.">
        <form className="form-grid" onSubmit={handleSubmit}>
          <label className="label">
            Name
            <input className="input" name="name" required placeholder="FAQ evaluation - gpt-4.1-mini" />
          </label>
          <label className="label">
            Dataset
            <select className="select" name="dataset_id" required defaultValue="">
              <option value="" disabled>
                Select a dataset
              </option>
              {datasets.map((dataset) => (
                <option key={dataset.id} value={dataset.id}>
                  {dataset.name}
                </option>
              ))}
            </select>
          </label>
          <label className="label">
            Prompt version
            <select className="select" name="prompt_version_id" required defaultValue="">
              <option value="" disabled>
                Select a prompt version
              </option>
              {promptVersions.map((promptVersion) => (
                <option key={promptVersion.id} value={promptVersion.id}>
                  {promptVersion.name} ({promptVersion.version})
                </option>
              ))}
            </select>
          </label>
          <label className="label">
            Model name
            <input className="input" name="model_name" required placeholder="gpt-4.1-mini" />
          </label>
          <button
            className="button"
            type="submit"
            disabled={submitting || datasets.length === 0 || promptVersions.length === 0}
          >
            Create Experiment
          </button>
        </form>
      </SectionCard>

      <SectionCard title="Experiments" description="Run local Ollama evaluations and inspect experiment configuration.">
        {message ? <p className="muted">{message}</p> : null}
        {loading ? (
          <p className="muted">Loading experiments...</p>
        ) : (
          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Dataset</th>
                  <th>Prompt Version</th>
                  <th>Model</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {experiments.map((experiment) => {
                  const dataset = datasets.find((item) => item.id === experiment.dataset_id);
                  const promptVersion = promptVersions.find((item) => item.id === experiment.prompt_version_id);

                  return (
                    <tr key={experiment.id}>
                      <td>{experiment.name}</td>
                      <td>{dataset?.name || experiment.dataset_id}</td>
                      <td>
                        {promptVersion ? `${promptVersion.name} (${promptVersion.version})` : experiment.prompt_version_id}
                      </td>
                      <td>{experiment.model_name}</td>
                      <td>
                        <div className="inline-actions">
                          <button
                            className="button secondary"
                            type="button"
                            onClick={() => void handleRun(experiment.id)}
                            disabled={runLoadingId === experiment.id}
                          >
                            {runLoadingId === experiment.id ? "Running..." : "Run Experiment"}
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
                {experiments.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="muted">
                      No experiments yet.
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
