import { useCallback } from "react";
import { Play } from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ErrorState } from "../../components/ErrorState";
import { LoadingState } from "../../components/LoadingState";
import { getSession, startWorkflow, workflowStreamUrl } from "../../lib/api";
import { useEventStream } from "../../hooks/useEventStream";
import { FollowUpChat } from "../chat/FollowUpChat";
import { ReportView } from "../reports/ReportView";
import { WorkflowProgress } from "../workflow/WorkflowProgress";

type SessionDetailPageProps = {
  sessionId: string;
};

export function SessionDetailPage({ sessionId }: SessionDetailPageProps) {
  const queryClient = useQueryClient();
  const detailQuery = useQuery({
    queryKey: ["session", sessionId],
    queryFn: () => getSession(sessionId)
  });
  const refreshSession = useCallback(() => {
    void queryClient.invalidateQueries({ queryKey: ["session", sessionId] });
    void queryClient.invalidateQueries({ queryKey: ["sessions"] });
  }, [queryClient, sessionId]);
  const workflowMutation = useMutation({
    mutationFn: () => startWorkflow(sessionId),
    onSuccess: refreshSession
  });

  useEventStream({
    enabled: detailQuery.data?.status === "running",
    url: workflowStreamUrl(sessionId),
    onMessage: refreshSession
  });

  if (detailQuery.isLoading) return <LoadingState label="Loading session" />;
  if (detailQuery.isError || !detailQuery.data) {
    return <ErrorState title="Could not load session" />;
  }

  const session = detailQuery.data;
  const canRun = session.status === "created" || session.status === "failed" || session.status === "completed";

  return (
    <div className="detail-layout">
      <section className="detail-header">
        <div>
          <p className="eyebrow">{session.status.replace("_", " ")}</p>
          <h2>{session.company_name}</h2>
          <a href={session.website} rel="noreferrer" target="_blank">
            {session.website}
          </a>
          <p>{session.objective}</p>
        </div>
        <button
          className="primary-button detail-action"
          disabled={!canRun || workflowMutation.isPending}
          onClick={() => workflowMutation.mutate()}
          type="button"
        >
          <Play aria-hidden="true" size={18} />
          {workflowMutation.isPending ? "Running" : session.report ? "Rerun workflow" : "Run workflow"}
        </button>
      </section>

      {workflowMutation.isError ? (
        <ErrorState title="Workflow could not start" body={workflowMutation.error.message} />
      ) : null}

      <WorkflowProgress steps={session.workflow_steps} events={session.workflow_events} />
      <ReportView report={session.report} />
      <FollowUpChat session={session} onMessageSent={refreshSession} />
    </div>
  );
}
