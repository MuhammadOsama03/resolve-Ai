const sampleTickets = [
  { id: "T-104", subject: "Cannot reset account password", status: "open", priority: "high" },
  { id: "T-103", subject: "Invoice shows duplicate charge", status: "in progress", priority: "medium" },
  { id: "T-102", subject: "How do I export my workspace?", status: "resolved", priority: "low" },
];

export default function HomePage() {
  return (
    <main style={{ maxWidth: 1080, margin: "0 auto", padding: "48px 24px", fontFamily: "Arial, sans-serif" }}>
      <header style={{ marginBottom: 36 }}>
        <p style={{ fontWeight: 700, letterSpacing: 1 }}>ResolveAI</p>
        <h1 style={{ fontSize: 40, marginBottom: 12 }}>Support workspace</h1>
        <p style={{ maxWidth: 680, lineHeight: 1.6 }}>
          Review incoming customer requests, track resolution status, and prepare the workspace for grounded AI assistance.
        </p>
      </header>

      <section style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 16, marginBottom: 36 }}>
        <article><strong>12</strong><p>Open tickets</p></article>
        <article><strong>5</strong><p>In progress</p></article>
        <article><strong>28</strong><p>Resolved this week</p></article>
      </section>

      <section>
        <h2>Recent tickets</h2>
        <div style={{ display: "grid", gap: 12 }}>
          {sampleTickets.map((ticket) => (
            <article key={ticket.id} style={{ border: "1px solid #ddd", borderRadius: 12, padding: 18 }}>
              <small>{ticket.id} · {ticket.priority} priority</small>
              <h3 style={{ margin: "8px 0" }}>{ticket.subject}</h3>
              <span>{ticket.status}</span>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
