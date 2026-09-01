"use client";

import { FormEvent, useEffect, useState } from "react";

import {
  CopilotSuggestion,
  createKnowledgeDocument,
  createTicket,
  getKnowledge,
  getTicketSuggestion,
  getTickets,
  KnowledgeDocument,
  KnowledgeInput,
  Ticket,
  TicketInput,
} from "../lib/api";

const emptyTicket: TicketInput = {
  subject: "",
  description: "",
  customer_email: "",
};

const emptyKnowledge: KnowledgeInput = {
  title: "",
  content: "",
};

const cardStyle = {
  border: "1px solid #ddd",
  borderRadius: 16,
  padding: 22,
} as const;

export default function HomePage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [knowledge, setKnowledge] = useState<KnowledgeDocument[]>([]);
  const [ticketForm, setTicketForm] = useState<TicketInput>(emptyTicket);
  const [knowledgeForm, setKnowledgeForm] = useState<KnowledgeInput>(emptyKnowledge);
  const [suggestions, setSuggestions] = useState<Record<string, CopilotSuggestion>>({});
  const [loading, setLoading] = useState(true);
  const [submittingTicket, setSubmittingTicket] = useState(false);
  const [submittingKnowledge, setSubmittingKnowledge] = useState(false);
  const [suggestingTicket, setSuggestingTicket] = useState<string | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([getTickets(), getKnowledge()])
      .then(([ticketData, knowledgeData]) => {
        setTickets(ticketData);
        setKnowledge(knowledgeData);
      })
      .catch(() => setError("Could not load the workspace. Make sure the API is running."))
      .finally(() => setLoading(false));
  }, []);

  async function handleTicketSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmittingTicket(true);
    setError("");

    try {
      const ticket = await createTicket(ticketForm);
      setTickets((current) => [ticket, ...current]);
      setTicketForm(emptyTicket);
    } catch {
      setError("Could not create the ticket. Please try again.");
    } finally {
      setSubmittingTicket(false);
    }
  }

  async function handleKnowledgeSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmittingKnowledge(true);
    setError("");

    try {
      const document = await createKnowledgeDocument(knowledgeForm);
      setKnowledge((current) => [document, ...current]);
      setKnowledgeForm(emptyKnowledge);
    } catch {
      setError("Could not add the knowledge document. Please try again.");
    } finally {
      setSubmittingKnowledge(false);
    }
  }

  async function handleSuggestion(ticketId: string) {
    setSuggestingTicket(ticketId);
    setError("");

    try {
      const suggestion = await getTicketSuggestion(ticketId);
      setSuggestions((current) => ({ ...current, [ticketId]: suggestion }));
    } catch {
      setError("Could not generate a grounded suggestion for this ticket.");
    } finally {
      setSuggestingTicket(null);
    }
  }

  return (
    <main style={{ maxWidth: 1120, margin: "0 auto", padding: "48px 24px", fontFamily: "Arial, sans-serif" }}>
      <header style={{ marginBottom: 36 }}>
        <p style={{ fontWeight: 700, letterSpacing: 1 }}>ResolveAI</p>
        <h1 style={{ fontSize: 40, marginBottom: 12 }}>Support copilot workspace</h1>
        <p style={{ maxWidth: 720, lineHeight: 1.6 }}>
          Capture support tickets, add trusted company knowledge, and generate first-pass responses that stay tied to retrieved source material.
        </p>
      </header>

      {error && <p role="alert" style={{ padding: 12, border: "1px solid #c66", borderRadius: 10 }}>{error}</p>}

      <section style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: 24, marginBottom: 36 }}>
        <form onSubmit={handleTicketSubmit} style={cardStyle}>
          <h2 style={{ marginTop: 0 }}>New ticket</h2>
          <label style={{ display: "grid", gap: 6, marginBottom: 14 }}>
            Subject
            <input
              required
              minLength={3}
              value={ticketForm.subject}
              onChange={(event) => setTicketForm({ ...ticketForm, subject: event.target.value })}
              style={{ padding: 10 }}
            />
          </label>
          <label style={{ display: "grid", gap: 6, marginBottom: 14 }}>
            Customer email
            <input
              required
              type="email"
              value={ticketForm.customer_email}
              onChange={(event) => setTicketForm({ ...ticketForm, customer_email: event.target.value })}
              style={{ padding: 10 }}
            />
          </label>
          <label style={{ display: "grid", gap: 6, marginBottom: 16 }}>
            Description
            <textarea
              required
              minLength={10}
              rows={5}
              value={ticketForm.description}
              onChange={(event) => setTicketForm({ ...ticketForm, description: event.target.value })}
              style={{ padding: 10, resize: "vertical" }}
            />
          </label>
          <button disabled={submittingTicket} type="submit" style={{ padding: "10px 16px", cursor: "pointer" }}>
            {submittingTicket ? "Creating…" : "Create ticket"}
          </button>
        </form>

        <form onSubmit={handleKnowledgeSubmit} style={cardStyle}>
          <h2 style={{ marginTop: 0 }}>Knowledge base</h2>
          <p style={{ lineHeight: 1.5 }}>Add trusted support notes that the copilot can retrieve when preparing a response.</p>
          <label style={{ display: "grid", gap: 6, marginBottom: 14 }}>
            Document title
            <input
              required
              minLength={3}
              value={knowledgeForm.title}
              onChange={(event) => setKnowledgeForm({ ...knowledgeForm, title: event.target.value })}
              style={{ padding: 10 }}
            />
          </label>
          <label style={{ display: "grid", gap: 6, marginBottom: 16 }}>
            Support content
            <textarea
              required
              minLength={20}
              rows={7}
              value={knowledgeForm.content}
              onChange={(event) => setKnowledgeForm({ ...knowledgeForm, content: event.target.value })}
              style={{ padding: 10, resize: "vertical" }}
            />
          </label>
          <button disabled={submittingKnowledge} type="submit" style={{ padding: "10px 16px", cursor: "pointer" }}>
            {submittingKnowledge ? "Adding…" : "Add knowledge"}
          </button>
          <p style={{ marginBottom: 0, color: "#555" }}>{knowledge.length} document{knowledge.length === 1 ? "" : "s"} available</p>
        </form>
      </section>

      <section>
        <h2>Tickets</h2>
        {loading ? (
          <p>Loading workspace…</p>
        ) : tickets.length === 0 ? (
          <p>No tickets yet. Create the first request from the form.</p>
        ) : (
          <div style={{ display: "grid", gap: 16 }}>
            {tickets.map((ticket) => {
              const suggestion = suggestions[ticket.id];
              return (
                <article key={ticket.id} style={cardStyle}>
                  <small>{ticket.customer_email} · {ticket.status.replace("_", " ")}</small>
                  <h3 style={{ margin: "8px 0" }}>{ticket.subject}</h3>
                  <p style={{ lineHeight: 1.5 }}>{ticket.description}</p>
                  <button
                    type="button"
                    disabled={suggestingTicket === ticket.id}
                    onClick={() => handleSuggestion(ticket.id)}
                    style={{ padding: "9px 14px", cursor: "pointer" }}
                  >
                    {suggestingTicket === ticket.id ? "Retrieving context…" : "Generate grounded suggestion"}
                  </button>

                  {suggestion && (
                    <div style={{ marginTop: 16, padding: 16, background: "#f6f6f6", borderRadius: 12 }}>
                      <strong>Copilot suggestion</strong>
                      <p style={{ whiteSpace: "pre-wrap", lineHeight: 1.55 }}>{suggestion.suggestion}</p>
                      <small>
                        {suggestion.source_ids.length
                          ? `${suggestion.source_ids.length} knowledge source(s) used · Review before sending`
                          : "No matching source found · Manual review required"}
                      </small>
                    </div>
                  )}
                </article>
              );
            })}
          </div>
        )}
      </section>
    </main>
  );
}
