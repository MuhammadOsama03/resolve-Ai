"use client";

import { FormEvent, useEffect, useState } from "react";

import { createTicket, getTickets, Ticket, TicketInput } from "../lib/api";

const emptyForm: TicketInput = {
  subject: "",
  description: "",
  customer_email: "",
};

export default function HomePage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [form, setForm] = useState<TicketInput>(emptyForm);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    getTickets()
      .then(setTickets)
      .catch(() => setError("Could not load tickets. Make sure the API is running."))
      .finally(() => setLoading(false));
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError("");

    try {
      const ticket = await createTicket(form);
      setTickets((current) => [ticket, ...current]);
      setForm(emptyForm);
    } catch {
      setError("Could not create the ticket. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main style={{ maxWidth: 1080, margin: "0 auto", padding: "48px 24px", fontFamily: "Arial, sans-serif" }}>
      <header style={{ marginBottom: 36 }}>
        <p style={{ fontWeight: 700, letterSpacing: 1 }}>ResolveAI</p>
        <h1 style={{ fontSize: 40, marginBottom: 12 }}>Support workspace</h1>
        <p style={{ maxWidth: 680, lineHeight: 1.6 }}>
          Capture customer requests, track their current state, and prepare clean ticket context for the AI assistance phase.
        </p>
      </header>

      <section style={{ display: "grid", gridTemplateColumns: "minmax(280px, 0.9fr) minmax(320px, 1.4fr)", gap: 28 }}>
        <form onSubmit={handleSubmit} style={{ border: "1px solid #ddd", borderRadius: 16, padding: 22, alignSelf: "start" }}>
          <h2 style={{ marginTop: 0 }}>New ticket</h2>
          <label style={{ display: "grid", gap: 6, marginBottom: 14 }}>
            Subject
            <input
              required
              minLength={3}
              value={form.subject}
              onChange={(event) => setForm({ ...form, subject: event.target.value })}
              style={{ padding: 10 }}
            />
          </label>
          <label style={{ display: "grid", gap: 6, marginBottom: 14 }}>
            Customer email
            <input
              required
              type="email"
              value={form.customer_email}
              onChange={(event) => setForm({ ...form, customer_email: event.target.value })}
              style={{ padding: 10 }}
            />
          </label>
          <label style={{ display: "grid", gap: 6, marginBottom: 16 }}>
            Description
            <textarea
              required
              minLength={10}
              rows={6}
              value={form.description}
              onChange={(event) => setForm({ ...form, description: event.target.value })}
              style={{ padding: 10, resize: "vertical" }}
            />
          </label>
          <button disabled={submitting} type="submit" style={{ padding: "10px 16px", cursor: "pointer" }}>
            {submitting ? "Creating…" : "Create ticket"}
          </button>
          {error && <p role="alert">{error}</p>}
        </form>

        <section>
          <h2>Tickets</h2>
          {loading ? (
            <p>Loading tickets…</p>
          ) : tickets.length === 0 ? (
            <p>No tickets yet. Create the first request from the form.</p>
          ) : (
            <div style={{ display: "grid", gap: 12 }}>
              {tickets.map((ticket) => (
                <article key={ticket.id} style={{ border: "1px solid #ddd", borderRadius: 12, padding: 18 }}>
                  <small>{ticket.customer_email} · {ticket.status.replace("_", " ")}</small>
                  <h3 style={{ margin: "8px 0" }}>{ticket.subject}</h3>
                  <p style={{ lineHeight: 1.5 }}>{ticket.description}</p>
                </article>
              ))}
            </div>
          )}
        </section>
      </section>
    </main>
  );
}
