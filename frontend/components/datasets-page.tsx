"use client";

import { FormEvent, useEffect, useState } from "react";

import { SectionCard } from "@/components/section-card";
import { api } from "@/lib/api";
import { Dataset, TestCase } from "@/lib/types";

export function DatasetsPage() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [testCases, setTestCases] = useState<TestCase[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  async function loadData() {
    setLoading(true);
    try {
      const [datasetData, testCaseData] = await Promise.all([api.listDatasets(), api.listTestCases()]);
      setDatasets(datasetData);
      setTestCases(testCaseData);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Failed to load datasets");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadData();
  }, []);

  async function handleDatasetSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setMessage(null);
    const formData = new FormData(event.currentTarget);

    try {
      await api.createDataset({
        name: String(formData.get("name")),
        description: String(formData.get("description") || ""),
      });
      event.currentTarget.reset();
      await loadData();
      setMessage("Dataset created.");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Failed to create dataset");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleTestCaseSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setMessage(null);
    const formData = new FormData(event.currentTarget);

    try {
      await api.createTestCase({
        dataset_id: Number(formData.get("dataset_id")),
        input_text: String(formData.get("input_text")),
        expected_output: String(formData.get("expected_output") || ""),
        evaluation_type: String(formData.get("evaluation_type") || "pass_fail"),
      });
      event.currentTarget.reset();
      await loadData();
      setMessage("Test case created.");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Failed to create test case");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="page-grid">
      <div className="two-col">
        <SectionCard title="Create Dataset" description="Add a dataset that groups test cases for evaluation.">
          <form className="form-grid" onSubmit={handleDatasetSubmit}>
            <label className="label">
              Name
              <input className="input" name="name" required placeholder="Support FAQ" />
            </label>
            <label className="label">
              Description
              <textarea className="textarea" name="description" placeholder="Short description of the dataset" />
            </label>
            <button className="button" type="submit" disabled={submitting}>
              Create Dataset
            </button>
          </form>
        </SectionCard>

        <SectionCard title="Create Test Case" description="Attach inputs and expected outputs to a dataset.">
          <form className="form-grid" onSubmit={handleTestCaseSubmit}>
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
              Input text
              <textarea className="textarea" name="input_text" required placeholder="User prompt or input" />
            </label>
            <label className="label">
              Expected output
              <textarea className="textarea" name="expected_output" placeholder="Expected answer" />
            </label>
            <label className="label">
              Evaluation type
              <input className="input" name="evaluation_type" defaultValue="pass_fail" />
            </label>
            <button className="button" type="submit" disabled={submitting || datasets.length === 0}>
              Create Test Case
            </button>
          </form>
        </SectionCard>
      </div>

      <SectionCard title="Datasets" description="Current datasets and how many test cases belong to each one.">
        {message ? <p className="muted">{message}</p> : null}
        {loading ? (
          <p className="muted">Loading datasets...</p>
        ) : (
          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Description</th>
                  <th>Test Cases</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {datasets.map((dataset) => (
                  <tr key={dataset.id}>
                    <td>{dataset.name}</td>
                    <td>{dataset.description || "No description"}</td>
                    <td>{testCases.filter((testCase) => testCase.dataset_id === dataset.id).length}</td>
                    <td>{new Date(dataset.created_at).toLocaleString()}</td>
                  </tr>
                ))}
                {datasets.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="muted">
                      No datasets yet.
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
