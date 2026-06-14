export type SessionSummary = {
  id: string;
  company_name: string;
  website: string;
  objective: string;
  status: "created" | "running" | "completed" | "failed" | "needs_attention";
  created_at: string;
  updated_at: string;
  report_available: boolean;
};

export type WorkflowStep = {
  name: string;
  label: string;
  status: string;
  sequence: number;
  detail: string | null;
  started_at: string | null;
  completed_at: string | null;
};

export type WorkflowEvent = {
  id: number;
  node: string;
  event_type: string;
  message: string;
  payload: Record<string, unknown>;
  created_at: string;
};

export type ReportSource = {
  title: string;
  url: string;
  snippet: string;
};

export type Report = {
  id: string;
  summary: string;
  sections: Record<string, unknown>;
  quality_findings: string[];
  unknowns: string[];
  sources: ReportSource[];
  created_at: string;
};

export type ChatMessage = {
  id: string;
  role: "user" | "response";
  content: string;
  sources: Array<Record<string, string>>;
  created_at: string;
};

export type SessionDetail = SessionSummary & {
  error_message: string | null;
  started_at: string | null;
  completed_at: string | null;
  workflow_steps: WorkflowStep[];
  workflow_events: WorkflowEvent[];
  report: Report | null;
  chat_messages: ChatMessage[];
};

export type SessionCreatePayload = {
  company_name: string;
  website: string;
  objective: string;
};

export type ChatResponse = {
  user_message: ChatMessage;
  response_message: ChatMessage;
};

