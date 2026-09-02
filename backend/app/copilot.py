from collections.abc import Iterable

from .llm import generate_gemini_reply


def _compact_excerpt(text: str, limit: int = 220) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[: limit - 1].rstrip()}…"


def _build_prompt(subject: str, description: str, sources: list[dict[str, object]]) -> str:
    evidence = "\n\n".join(
        f"SOURCE {index + 1} — {source.get('title', 'Support note')}\n"
        f"{str(source.get('content', ''))}"
        for index, source in enumerate(sources)
    )
    return (
        "You are a customer-support copilot. Draft a concise, professional reply to the ticket below. "
        "Use only facts supported by the supplied knowledge sources. If a requested fact is not in the sources, "
        "say that it needs manual confirmation. Do not invent policies, dates, prices, or actions.\n\n"
        f"TICKET SUBJECT: {subject}\n"
        f"TICKET DESCRIPTION: {description}\n\n"
        f"KNOWLEDGE SOURCES:\n{evidence}\n\n"
        "Return only the suggested customer reply."
    )


def build_grounded_suggestion(
    subject: str,
    description: str,
    documents: Iterable[dict[str, object]],
) -> dict[str, object]:
    """Compose a first-pass reply grounded in retrieved support material."""
    sources = list(documents)
    if not sources:
        return {
            "suggestion": (
                "I don't have enough matching knowledge-base context to draft a reliable "
                "answer yet. Please review this ticket manually or add relevant support documentation."
            ),
            "source_ids": [],
            "needs_review": True,
            "provider": "fallback",
        }

    source_ids = [str(source.get("id", "")) for source in sources]
    generated = generate_gemini_reply(_build_prompt(subject, description, sources))
    if generated:
        return {
            "suggestion": generated,
            "source_ids": source_ids,
            "needs_review": True,
            "ticket_context": _compact_excerpt(description, limit=280),
            "provider": "gemini",
        }

    evidence = [
        f"{source.get('title', 'Support note')}: "
        f"{_compact_excerpt(str(source.get('content', '')))}"
        for source in sources
    ]
    suggestion = (
        f"Regarding '{subject}', here is a response grounded in the available support material:\n\n"
        + "\n\n".join(evidence)
        + "\n\nPlease adapt the wording to the customer's exact situation before sending."
    )

    return {
        "suggestion": suggestion,
        "source_ids": source_ids,
        "needs_review": True,
        "ticket_context": _compact_excerpt(description, limit=280),
        "provider": "fallback",
    }
