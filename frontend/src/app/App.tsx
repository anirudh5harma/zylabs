import { Activity, FileText, MessageSquare, Search } from "lucide-react";

const sections = [
  {
    icon: Search,
    title: "Create research sessions",
    copy: "Capture company, website, and meeting objective before the workflow starts."
  },
  {
    icon: Activity,
    title: "Track workflow progress",
    copy: "Show each research, analysis, quality, and report step as durable events."
  },
  {
    icon: FileText,
    title: "Review structured reports",
    copy: "Render company overview, products, customers, signals, risks, outreach, unknowns, and sources."
  },
  {
    icon: MessageSquare,
    title: "Ask follow-up questions",
    copy: "Continue from persisted report context after the briefing is generated."
  }
];

export function App() {
  return (
    <main className="app-shell">
      <section className="hero">
        <div>
          <p className="eyebrow">Research Copilot</p>
          <h1>Prepare sharper business meetings from one research session.</h1>
          <p className="hero-copy">
            A production-grade workspace for company research, workflow progress, structured
            briefings, and grounded follow-up.
          </p>
        </div>
      </section>

      <section className="feature-grid" aria-label="Planned product surfaces">
        {sections.map((section) => {
          const Icon = section.icon;
          return (
            <article className="feature-card" key={section.title}>
              <Icon aria-hidden="true" className="feature-icon" />
              <h2>{section.title}</h2>
              <p>{section.copy}</p>
            </article>
          );
        })}
      </section>
    </main>
  );
}

