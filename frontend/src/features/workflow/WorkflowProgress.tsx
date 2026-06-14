import { CheckCircle2, Circle, CircleAlert } from "lucide-react";
import type { WorkflowEvent, WorkflowStep } from "../../lib/types";

type WorkflowProgressProps = {
  steps: WorkflowStep[];
  events: WorkflowEvent[];
};

export function WorkflowProgress({ steps, events }: WorkflowProgressProps) {
  return (
    <section className="workspace-section">
      <div className="section-heading">
        <h3>Workflow progress</h3>
        <span>{events.length} events</span>
      </div>
      <div className="step-grid">
        {steps.length === 0 ? (
          <p className="muted">Run the workflow to see progress.</p>
        ) : (
          steps.map((step) => {
            const Icon = step.status === "completed" ? CheckCircle2 : step.status === "failed" ? CircleAlert : Circle;
            return (
              <article className="step-item" key={step.name}>
                <Icon aria-hidden="true" size={18} />
                <div>
                  <strong>{step.label}</strong>
                  <span>{step.detail ?? step.status}</span>
                </div>
              </article>
            );
          })
        )}
      </div>
      {events.length > 0 ? (
        <ol className="event-list">
          {events.slice(-6).map((event) => (
            <li key={event.id}>
              <span>{event.node}</span>
              <p>{event.message}</p>
            </li>
          ))}
        </ol>
      ) : null}
    </section>
  );
}

