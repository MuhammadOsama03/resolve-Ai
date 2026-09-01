export type TicketStatus = "open" | "in_progress" | "resolved";

export type Ticket = {
  id: string;
  subject: string;
  description: string;
  customer_email: string;
  status: TicketStatus;
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
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function getTickets(): Promise<Ticket[]> {
  const response = await fetch(`${API_URL}/tickets`, { cache: "no-store" });
  if (!response.ok) throw new Error("Unable to load tickets");
  return response.json();
}

export async function createTicket(input: TicketInput): Promise<Ticket> {
  const response = await fetch(`${API_URL}/tickets`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!response.ok) throw new Error("Unable to create ticket");
  return response.json();
}

export async function updateTicketStatus(id: string, status: TicketStatus): Promise<Ticket> {
  const response = await fetch(`${API_URL}/tickets/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  if (!response.ok) throw new Error("Unable to update ticket");
  return response.json();
}

export async function getKnowledge(): Promise<KnowledgeDocument[]> {
  const response = await fetch(`${API_URL}/knowledge`, { cache: "no-store" });
  if (!response.ok) throw new Error("Unable to load knowledge documents");
  return response.json();
}

export async function createKnowledgeDocument(input: KnowledgeInput): Promise<KnowledgeDocument> {
  const response = await fetch(`${API_URL}/knowledge`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!response.ok) throw new Error("Unable to create knowledge document");
  return response.json();
}

export async function getTicketSuggestion(id: string): Promise<CopilotSuggestion> {
  const response = await fetch(`${API_URL}/tickets/${id}/suggestion`, {
    method: "POST",
  });
  if (!response.ok) throw new Error("Unable to generate suggestion");
  return response.json();
}
