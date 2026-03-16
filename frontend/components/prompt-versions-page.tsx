"use client";

import { FormEvent, useEffect, useState } from "react";

import { SectionCard } from "@/components/section-card";
import { api } from "@/lib/api";
import { PromptVersion } from "@/lib/types";

export function PromptVersionsPage() {
  const [promptVersions, setPromptVersions] = useState<PromptVersion[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  async function loadData() {
    setLoading(true);
    try {
      setPromptVersions(await api.listPromptVersions());
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Failed to load prompt versions");
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
      await api.createPromptVersion({
        name: String(formData.get("name")),
        version: String(formData.get("version")),
        prompt_text: String(formData.get("prompt_text")),
      });
      event.currentTarget.reset();
      await loadData();
      setMessage("Prompt version created.");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Failed to create prompt version");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="page-grid">
      <SectionCard
        title="Create Prompt Version"
        description="Store prompt templates and version labels that experiments can point to."
      >
        <form className="form-grid" onSubmit={handleSubmit}>
          <label className="label">
            Name
            <input className="input" name="name" required placeholder="Support prompt" />
          </label>
          <label className="label">
            Version
            <input className="input" name="version" required placeholder="v1" />
          </label>
          <label className="label">
            Prompt text
            <textarea className="textarea" name="prompt_text" required placeholder="You are a helpful assistant..." />
          </label>
          <button className="button" type="submit" disabled={submitting}>
            Create Prompt Version
          </button>
        </form>
      </SectionCard>

      <SectionCard title="Prompt Versions" description="Simple list of prompt definitions available to experiments.">
        {message ? <p className="muted">{message}</p> : null}
        {loading ? (
          <p className="muted">Loading prompt versions...</p>
        ) : (
          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Version</th>
                  <th>Prompt</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {promptVersions.map((promptVersion) => (
                  <tr key={promptVersion.id}>
                    <td>{promptVersion.name}</td>
                    <td>{promptVersion.version}</td>
                    <td>{promptVersion.prompt_text}</td>
                    <td>{new Date(promptVersion.created_at).toLocaleString()}</td>
                  </tr>
                ))}
                {promptVersions.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="muted">
                      No prompt versions yet.
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
