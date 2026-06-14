import { render, screen } from "@testing-library/react";
import { ReportView } from "../features/reports/ReportView";
import type { Report } from "../lib/types";

const report: Report = {
  id: "report-1",
  summary: "A structured briefing summary.",
  created_at: "2026-06-14T00:00:00Z",
  quality_findings: [],
  unknowns: ["Budget owner"],
  sources: [{ title: "Company profile", url: "https://example.com/profile", snippet: "Profile" }],
  sections: {
    company_overview: "Overview",
    products_services: "Products",
    target_customers: "Customers",
    business_signals: ["Hiring"],
    risks_challenges: ["Stale source"],
    suggested_discovery_questions: ["What changed this quarter?"],
    suggested_outreach_strategy: "Lead with a pain hypothesis.",
    unknowns: ["Budget owner"]
  }
};

describe("ReportView", () => {
  it("renders every required report section", () => {
    render(<ReportView report={report} />);

    expect(screen.getByText("Company Overview")).toBeInTheDocument();
    expect(screen.getByText("Products & Services")).toBeInTheDocument();
    expect(screen.getByText("Target Customers")).toBeInTheDocument();
    expect(screen.getByText("Business Signals")).toBeInTheDocument();
    expect(screen.getByText("Risks & Challenges")).toBeInTheDocument();
    expect(screen.getByText("Suggested Discovery Questions")).toBeInTheDocument();
    expect(screen.getByText("Suggested Outreach Strategy")).toBeInTheDocument();
    expect(screen.getByText("Unknowns")).toBeInTheDocument();
    expect(screen.getByText("Sources")).toBeInTheDocument();
  });
});

