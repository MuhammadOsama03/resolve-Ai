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
