import { SummaryStats } from "@/lib/types";

type SummaryCardsProps = {
  stats: SummaryStats;
};

export function SummaryCards({ stats }: SummaryCardsProps) {
  const cards = [
    { label: "Average Latency", value: `${stats.averageLatency.toFixed(1)} ms` },
    { label: "Total Estimated Cost", value: `$${stats.totalCost.toFixed(4)}` },
    { label: "Passes", value: String(stats.passedCount) },
    { label: "Fails", value: String(stats.failedCount) },
  ];

  return (
    <div className="stats-grid">
      {cards.map((card) => (
        <div key={card.label} className="card">
          <div className="muted">{card.label}</div>
          <div className="stat-value">{card.value}</div>
        </div>
      ))}
    </div>
  );
}
