import { ExternalLink } from "lucide-react";
import type { Report } from "../../lib/types";

const sectionLabels: Record<string, string> = {
  company_overview: "Company Overview",
  products_services: "Products & Services",
  target_customers: "Target Customers",
  business_signals: "Business Signals",
  risks_challenges: "Risks & Challenges",
  suggested_discovery_questions: "Suggested Discovery Questions",
  suggested_outreach_strategy: "Suggested Outreach Strategy",
  unknowns: "Unknowns"
};

type ReportViewProps = {
  report: Report | null;
};

function renderValue(value: unknown) {
  if (Array.isArray(value)) {
    return (
      <ul>
        {value.map((item, index) => (
          <li key={`${String(item)}-${index}`}>{String(item)}</li>
        ))}
      </ul>
    );
  }
  return <p>{String(value ?? "Not available")}</p>;
}

export function ReportView({ report }: ReportViewProps) {
  if (!report) {
    return (
      <section className="workspace-section">
        <div className="section-heading">
          <h3>Research report</h3>
        </div>
        <p className="muted">Run the workflow to generate the briefing.</p>
      </section>
    );
  }

  return (
    <section className="workspace-section">
      <div className="section-heading">
        <h3>Research report</h3>
        <span>{report.sources.length} sources</span>
      </div>
      <p className="report-summary">{report.summary}</p>
      <div className="report-grid">
        {Object.entries(sectionLabels).map(([key, label]) => (
          <article className="report-section" key={key}>
            <h4>{label}</h4>
            {renderValue(report.sections[key])}
          </article>
        ))}
      </div>
      <div className="sources-list">
        <h4>Sources</h4>
        {report.sources.map((source) => (
          <a href={source.url} key={source.url} rel="noreferrer" target="_blank">
            <span>{source.title}</span>
            <ExternalLink aria-hidden="true" size={14} />
          </a>
        ))}
      </div>
    </section>
  );
}

