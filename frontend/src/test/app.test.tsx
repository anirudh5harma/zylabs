import { render, screen, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../app/App";
import { createSession, listSessions } from "../lib/api";

vi.mock("../lib/api", () => ({
  listSessions: vi.fn(),
  createSession: vi.fn(),
  getSession: vi.fn(),
  startWorkflow: vi.fn(),
  askFollowUp: vi.fn(),
  workflowStreamUrl: vi.fn()
}));

const mockedListSessions = vi.mocked(listSessions);
const mockedCreateSession = vi.mocked(createSession);

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
    mockedCreateSession.mockResolvedValue({
      id: "session-1",
      company_name: "Acme Corp",
      website: "https://acme.example/",
      objective: "Prepare for a first discovery call",
      status: "created",
      created_at: "2026-06-14T00:00:00Z",
      updated_at: "2026-06-14T00:00:00Z",
      report_available: false
    });
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
});
