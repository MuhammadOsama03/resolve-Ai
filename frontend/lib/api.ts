export type TicketStatus = "open" | "in_progress" | "resolved";
export type TicketCategory = "billing" | "access" | "technical" | "account" | "general";
export type TicketPriority = "low" | "medium" | "high" | "urgent";

export type Ticket = {
  id: string;
  subject: string;
  description: string;
  customer_email: string;
  status: TicketStatus;
  category: TicketCategory;
  priority: TicketPriority;
  created_at: string;
};

export type TicketInput = {
  subject: string;
  description: string;
  customer_email: string;
};

export type KnowledgeDocument = {
  id: string;
  title: string;
  content: string;
  created_at: string;
};

export type KnowledgeInput = {
  title: string;
  content: string;
};

export type CopilotSuggestion = {
  suggestion: string;
  source_ids: string[];
  needs_review: boolean;
  ticket_context?: string | null;
  provider: "gemini" | "fallback" | string;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function parseResponse<T>(response: Response, message: string): Promise<T> {
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || message);
  }
  return response.json() as Promise<T>;
}

export async function getTickets(): Promise<Ticket[]> {
  const response = await fetch(`${API_URL}/tickets`, { cache: "no-store" });
  return parseResponse<Ticket[]>(response, "Unable to load tickets");
}

export async function createTicket(input: TicketInput): Promise<Ticket> {
  const response = await fetch(`${API_URL}/tickets`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  return parseResponse<Ticket>(response, "Unable to create ticket");
}

export async function updateTicketStatus(id: string, status: TicketStatus): Promise<Ticket> {
  const response = await fetch(`${API_URL}/tickets/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  return parseResponse<Ticket>(response, "Unable to update ticket");
}

export async function getKnowledge(): Promise<KnowledgeDocument[]> {
  const response = await fetch(`${API_URL}/knowledge`, { cache: "no-store" });
  return parseResponse<KnowledgeDocument[]>(response, "Unable to load knowledge documents");
}

export async function createKnowledgeDocument(input: KnowledgeInput): Promise<KnowledgeDocument> {
  const response = await fetch(`${API_URL}/knowledge`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  return parseResponse<KnowledgeDocument>(response, "Unable to create knowledge document");
}

export async function getTicketSuggestion(id: string): Promise<CopilotSuggestion> {
  const response = await fetch(`${API_URL}/tickets/${id}/suggestion`, {
    method: "POST",
  });
  return parseResponse<CopilotSuggestion>(response, "Unable to generate suggestion");
}
