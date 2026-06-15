import { render, screen, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../app/App";
import { createSession, getSession, listSessions, resumeWorkflow, startWorkflow } from "../lib/api";
import type { SessionDetail, SessionSummary } from "../lib/types";

vi.mock("../lib/api", () => ({
  listSessions: vi.fn(),
  createSession: vi.fn(),
  getSession: vi.fn(),
  resumeWorkflow: vi.fn(),
  startWorkflow: vi.fn(),
  askFollowUp: vi.fn(),
  workflowStreamUrl: vi.fn()
}));

const mockedListSessions = vi.mocked(listSessions);
const mockedCreateSession = vi.mocked(createSession);
const mockedGetSession = vi.mocked(getSession);
const mockedResumeWorkflow = vi.mocked(resumeWorkflow);
const mockedStartWorkflow = vi.mocked(startWorkflow);

const sessionSummary: SessionSummary = {
  id: "session-1",
  company_name: "Acme Corp",
  website: "https://acme.example/",
  objective: "Prepare for a first discovery call",
  status: "created",
  created_at: "2026-06-14T00:00:00Z",
  updated_at: "2026-06-14T00:00:00Z",
  report_available: false
};

function sessionDetail(overrides: Partial<SessionDetail> = {}): SessionDetail {
  return {
    ...sessionSummary,
    error_message: null,
    started_at: null,
    completed_at: null,
    workflow_steps: [],
    workflow_events: [],
    report: null,
    chat_messages: [],
    ...overrides
  };
}

function renderApp() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } }
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  );
}

describe("App", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockedListSessions.mockResolvedValue([]);
    mockedCreateSession.mockResolvedValue(sessionSummary);
    mockedGetSession.mockResolvedValue(sessionDetail());
    mockedStartWorkflow.mockResolvedValue({ session_id: "session-1", status: "completed" });
    mockedResumeWorkflow.mockResolvedValue({ session_id: "session-1", status: "completed" });
  });

  it("renders the empty workspace", async () => {
    renderApp();

    expect(await screen.findByText("Create a research session")).toBeInTheDocument();
    expect(screen.getByLabelText("Company")).toBeInTheDocument();
    expect(screen.getByText("No sessions yet.")).toBeInTheDocument();
  });

  it("submits a new session", async () => {
    const user = userEvent.setup();
    renderApp();

    await user.type(await screen.findByLabelText("Company"), "Acme Corp");
    await user.type(screen.getByLabelText("Website"), "https://acme.example");
    await user.type(screen.getByLabelText("Objective"), "Prepare for a first discovery call");
    await user.click(screen.getByRole("button", { name: /create session/i }));

    await waitFor(() => {
      expect(mockedCreateSession).toHaveBeenCalled();
      expect(mockedCreateSession.mock.calls[0][0]).toEqual({
        company_name: "Acme Corp",
        website: "https://acme.example",
        objective: "Prepare for a first discovery call"
      });
    });
  });

  it("resumes recoverable workflows from the detail action", async () => {
    const user = userEvent.setup();
    mockedListSessions.mockResolvedValue([{ ...sessionSummary, status: "failed" }]);
    mockedGetSession.mockResolvedValue(sessionDetail({ status: "failed" }));
    renderApp();

    await user.click(await screen.findByRole("button", { name: /resume workflow/i }));

    await waitFor(() => {
      expect(mockedResumeWorkflow).toHaveBeenCalledWith("session-1");
      expect(mockedStartWorkflow).not.toHaveBeenCalled();
    });
  });
});
