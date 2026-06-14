import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { AppShell } from "../components/AppShell";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import { SessionCreateForm } from "../features/sessions/SessionCreateForm";
import { SessionDetailPage } from "../features/sessions/SessionDetailPage";
import { SessionHistory } from "../features/sessions/SessionHistory";
import { listSessions } from "../lib/api";

export function App() {
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);
  const sessionsQuery = useQuery({ queryKey: ["sessions"], queryFn: listSessions });
  const selectedSession = useMemo(() => {
    if (!sessionsQuery.data?.length) return null;
    if (selectedSessionId) {
      return sessionsQuery.data.find((session) => session.id === selectedSessionId) ?? null;
    }
    return sessionsQuery.data[0];
  }, [selectedSessionId, sessionsQuery.data]);

  if (sessionsQuery.isLoading) {
    return <LoadingState label="Loading workspace" />;
  }

  if (sessionsQuery.isError) {
    return <ErrorState title="Could not load sessions" />;
  }

  return (
    <AppShell
      sidebar={
        <>
          <SessionCreateForm onCreated={setSelectedSessionId} />
          <SessionHistory
            sessions={sessionsQuery.data ?? []}
            selectedSessionId={selectedSession?.id ?? null}
            onSelect={setSelectedSessionId}
          />
        </>
      }
    >
      {selectedSession ? (
        <SessionDetailPage sessionId={selectedSession.id} />
      ) : (
        <EmptyState
          title="Create a research session"
          body="Add a company, website, and objective to generate a sales briefing."
        />
      )}
    </AppShell>
  );
}
