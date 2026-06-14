import { Clock3 } from "lucide-react";
import type { SessionSummary } from "../../lib/types";

type SessionHistoryProps = {
  sessions: SessionSummary[];
  selectedSessionId: string | null;
  onSelect: (sessionId: string) => void;
};

export function SessionHistory({ sessions, selectedSessionId, onSelect }: SessionHistoryProps) {
  return (
    <section className="history-panel" aria-label="Session history">
      <div className="panel-heading">
        <Clock3 aria-hidden="true" size={18} />
        <h2>Session history</h2>
      </div>
      {sessions.length === 0 ? (
        <p className="muted">No sessions yet.</p>
      ) : (
        <div className="session-list">
          {sessions.map((session) => (
            <button
              className={session.id === selectedSessionId ? "session-item is-active" : "session-item"}
              key={session.id}
              onClick={() => onSelect(session.id)}
              type="button"
            >
              <span>{session.company_name}</span>
              <small>{session.status.replace("_", " ")}</small>
            </button>
          ))}
        </div>
      )}
    </section>
  );
}

