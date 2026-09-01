import re
from collections.abc import Iterable

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text: str) -> set[str]:
    """Normalize text into a small set of searchable terms."""
    return {token.lower() for token in TOKEN_PATTERN.findall(text) if len(token) > 2}


def rank_documents(
    query: str,
    documents: Iterable[dict[str, object]],
    limit: int = 3,
) -> list[dict[str, object]]:
    """Rank knowledge documents by simple lexical overlap.

    This intentionally stays dependency-free for the first retrieval phase.
    Embeddings/vector search can replace the scoring strategy later without
    changing the API contract.
    """
    query_terms = tokenize(query)
    if not query_terms:
        return []

    scored: list[tuple[float, dict[str, object]]] = []
    for document in documents:
        title = str(document.get("title", ""))
        content = str(document.get("content", ""))
        title_terms = tokenize(title)
        content_terms = tokenize(content)

        title_overlap = len(query_terms & title_terms)
        content_overlap = len(query_terms & content_terms)
        score = (title_overlap * 2.0) + content_overlap

        if score > 0:
            scored.append((score, document))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [document for _, document in scored[:limit]]
