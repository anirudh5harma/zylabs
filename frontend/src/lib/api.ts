import type { ChatResponse, SessionCreatePayload, SessionDetail, SessionSummary } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {})
    },
    ...init
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    const message = payload?.detail?.message ?? "Request failed";
    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

export function listSessions() {
  return request<SessionSummary[]>("/sessions");
}

export function createSession(payload: SessionCreatePayload) {
  return request<SessionSummary>("/sessions", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function getSession(sessionId: string) {
  return request<SessionDetail>(`/sessions/${sessionId}`);
}

export function startWorkflow(sessionId: string) {
  return request<{ session_id: string; status: string }>(`/sessions/${sessionId}/workflow/start`, {
    method: "POST"
  });
}

export function askFollowUp(sessionId: string, message: string) {
  return request<ChatResponse>(`/sessions/${sessionId}/chat`, {
    method: "POST",
    body: JSON.stringify({ message })
  });
}

export function workflowStreamUrl(sessionId: string) {
  return `${API_BASE_URL}/sessions/${sessionId}/workflow/stream`;
}

