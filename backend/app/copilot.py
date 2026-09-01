from collections.abc import Iterable


def _compact_excerpt(text: str, limit: int = 220) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[: limit - 1].rstrip()}…"


def build_grounded_suggestion(
    subject: str,
    description: str,
    documents: Iterable[dict[str, object]],
) -> dict[str, object]:
    """Compose a safe first-pass reply from retrieved support material.

    This phase deliberately avoids inventing facts. If retrieval finds no
    relevant source, the copilot returns a review-needed response instead of
    pretending it has supporting knowledge.
    """
    sources = list(documents)
    if not sources:
        return {
            "suggestion": (
                "I don't have enough matching knowledge-base context to draft a reliable "
                "answer yet. Please review this ticket manually or add relevant support documentation."
            ),
            "source_ids": [],
            "needs_review": True,
        }

    evidence = []
    source_ids: list[str] = []
    for source in sources:
        source_ids.append(str(source.get("id", "")))
        evidence.append(
            f"{source.get('title', 'Support note')}: "
            f"{_compact_excerpt(str(source.get('content', '')))}"
        )

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
    }
