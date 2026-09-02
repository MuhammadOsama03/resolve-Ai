"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";

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
  TicketStatus,
  updateTicketStatus,
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

const statuses: TicketStatus[] = ["open", "in_progress", "resolved"];

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
  const [updatingTicket, setUpdatingTicket] = useState<string | null>(null);
  const [error, setError] = useState("");

  const metrics = useMemo(() => {
    const unresolved = tickets.filter((ticket) => ticket.status !== "resolved").length;
    const urgent = tickets.filter((ticket) => ticket.priority === "urgent").length;
    return {
      total: tickets.length,
      unresolved,
      urgent,
      knowledge: knowledge.length,
    };
  }, [tickets, knowledge]);

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
      setError("Could not create the ticket. Check the form values and try again.");
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

  async function handleStatusChange(ticketId: string, status: TicketStatus) {
    setUpdatingTicket(ticketId);
    setError("");

    try {
      const updated = await updateTicketStatus(ticketId, status);
      setTickets((current) =>
        current.map((ticket) => (ticket.id === ticketId ? updated : ticket)),
      );
    } catch {
      setError("Could not update the ticket status.");
    } finally {
      setUpdatingTicket(null);
    }
  }

  return (
    <main className="workspace">
      <header className="hero">
        <span className="eyebrow">ResolveAI</span>
        <h1>Support ticket copilot</h1>
        <p>
          Triage incoming requests, maintain a trusted knowledge base, and draft grounded customer replies with source-aware AI assistance.
        </p>
      </header>

      <section className="metrics" aria-label="Workspace metrics">
        <div className="metric"><strong>{metrics.total}</strong><span>Total tickets</span></div>
        <div className="metric"><strong>{metrics.unresolved}</strong><span>Needs action</span></div>
        <div className="metric"><strong>{metrics.urgent}</strong><span>Urgent</span></div>
        <div className="metric"><strong>{metrics.knowledge}</strong><span>Knowledge docs</span></div>
      </section>

      {error && <p role="alert" className="alert">{error}</p>}

      <section className="composer-grid">
        <form onSubmit={handleTicketSubmit} className="card form-stack">
          <div>
            <h2>New ticket</h2>
            <p className="knowledge-count">Category and priority are assigned automatically.</p>
          </div>
          <label>
            Subject
            <input
              required
              minLength={3}
              maxLength={120}
              value={ticketForm.subject}
              onChange={(event) => setTicketForm({ ...ticketForm, subject: event.target.value })}
              placeholder="Customer cannot access account"
            />
          </label>
          <label>
            Customer email
            <input
              required
              type="email"
              value={ticketForm.customer_email}
              onChange={(event) => setTicketForm({ ...ticketForm, customer_email: event.target.value })}
              placeholder="customer@example.com"
            />
          </label>
          <label>
            Description
            <textarea
              required
              minLength={10}
              maxLength={4000}
              rows={5}
              value={ticketForm.description}
              onChange={(event) => setTicketForm({ ...ticketForm, description: event.target.value })}
              placeholder="Describe the request and any useful context."
            />
          </label>
          <button disabled={submittingTicket} type="submit">
            {submittingTicket ? "Creating…" : "Create ticket"}
          </button>
        </form>

        <form onSubmit={handleKnowledgeSubmit} className="card form-stack">
          <div>
            <h2>Knowledge base</h2>
            <p className="knowledge-count">{knowledge.length} trusted document{knowledge.length === 1 ? "" : "s"} available for retrieval.</p>
          </div>
          <label>
            Document title
            <input
              required
              minLength={3}
              maxLength={160}
              value={knowledgeForm.title}
              onChange={(event) => setKnowledgeForm({ ...knowledgeForm, title: event.target.value })}
              placeholder="Password reset policy"
            />
          </label>
          <label>
            Support content
            <textarea
              required
              minLength={20}
              maxLength={10000}
              rows={7}
              value={knowledgeForm.content}
              onChange={(event) => setKnowledgeForm({ ...knowledgeForm, content: event.target.value })}
              placeholder="Add verified support instructions, policies, or FAQ content."
            />
          </label>
          <button disabled={submittingKnowledge} type="submit">
            {submittingKnowledge ? "Adding…" : "Add knowledge"}
          </button>
        </form>
      </section>

      <section>
        <div className="section-head">
          <div>
            <h2>Ticket queue</h2>
            <p>Review automated triage, update workflow state, and request a grounded draft.</p>
          </div>
        </div>

        {loading ? (
          <p className="empty">Loading workspace…</p>
        ) : tickets.length === 0 ? (
          <p className="empty">No tickets yet. Create the first support request above.</p>
        ) : (
          <div className="ticket-list">
            {tickets.map((ticket) => {
              const suggestion = suggestions[ticket.id];
              return (
                <article key={ticket.id} className="card">
                  <div className="ticket-head">
                    <div>
                      <div className="ticket-meta">
                        <span>{ticket.customer_email}</span>
                        <span>•</span>
                        <span>{new Date(ticket.created_at).toLocaleString()}</span>
                      </div>
                      <h3>{ticket.subject}</h3>
                    </div>
                    <div className="badges">
                      <span className="badge">{ticket.category}</span>
                      <span className={`badge priority-${ticket.priority}`}>{ticket.priority}</span>
                    </div>
                  </div>

                  <p className="ticket-description">{ticket.description}</p>

                  <div className="ticket-actions">
                    <select
                      aria-label={`Status for ${ticket.subject}`}
                      className="status-select"
                      value={ticket.status}
                      disabled={updatingTicket === ticket.id}
                      onChange={(event) => handleStatusChange(ticket.id, event.target.value as TicketStatus)}
                    >
                      {statuses.map((status) => (
                        <option key={status} value={status}>{status.replace("_", " ")}</option>
                      ))}
                    </select>
                    <button
                      type="button"
                      className="secondary-button"
                      disabled={suggestingTicket === ticket.id}
                      onClick={() => handleSuggestion(ticket.id)}
                    >
                      {suggestingTicket === ticket.id ? "Retrieving context…" : "Generate grounded reply"}
                    </button>
                  </div>

                  {suggestion && (
                    <div className="suggestion">
                      <div className="ticket-head">
                        <strong>Copilot suggestion</strong>
                        <span className="badge">{suggestion.provider === "gemini" ? "Gemini" : "Safe fallback"}</span>
                      </div>
                      <p>{suggestion.suggestion}</p>
                      <small>
                        {suggestion.source_ids.length
                          ? `${suggestion.source_ids.length} source(s) used · Human review required before sending.`
                          : "No matching knowledge source found · Manual review required."}
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
