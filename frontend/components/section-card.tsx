import type { ReactNode } from "react";

type SectionCardProps = {
  title: string;
  description?: string;
  children: ReactNode;
};

export function SectionCard({ title, description, children }: SectionCardProps) {
  return (
    <section className="card">
      <h2 className="section-title">{title}</h2>
      {description ? <p className="section-copy">{description}</p> : null}
      {children}
    </section>
  );
}
