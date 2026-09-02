from enum import Enum


class TicketCategory(str, Enum):
    BILLING = "billing"
    ACCESS = "access"
    TECHNICAL = "technical"
    ACCOUNT = "account"
    GENERAL = "general"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


CATEGORY_KEYWORDS: dict[TicketCategory, set[str]] = {
    TicketCategory.BILLING: {"billing", "invoice", "refund", "charge", "payment"},
    TicketCategory.ACCESS: {"login", "password", "signin", "access", "locked"},
    TicketCategory.TECHNICAL: {"error", "bug", "crash", "broken", "timeout", "failed"},
    TicketCategory.ACCOUNT: {"account", "profile", "email", "subscription", "plan"},
}

URGENT_KEYWORDS = {"outage", "security", "breach", "down", "urgent", "critical"}
HIGH_KEYWORDS = {"blocked", "cannot", "can't", "failed", "payment", "locked"}
LOW_KEYWORDS = {"question", "suggestion", "feedback", "how to", "information"}


def _contains_any(text: str, keywords: set[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def _category_score(text: str, keywords: set[str]) -> int:
    """Count repeated keyword evidence instead of treating every match equally."""
    return sum(text.count(keyword) for keyword in keywords)


def classify_ticket(subject: str, description: str) -> tuple[TicketCategory, TicketPriority]:
    """Classify a ticket with transparent deterministic keyword rules."""
    text = f"{subject} {description}".lower()

    category = TicketCategory.GENERAL
    best_score = 0
    for candidate, keywords in CATEGORY_KEYWORDS.items():
        score = _category_score(text, keywords)
        if score > best_score:
            category = candidate
            best_score = score

    if _contains_any(text, URGENT_KEYWORDS):
        priority = TicketPriority.URGENT
    elif _contains_any(text, HIGH_KEYWORDS):
        priority = TicketPriority.HIGH
    elif _contains_any(text, LOW_KEYWORDS):
        priority = TicketPriority.LOW
    else:
        priority = TicketPriority.MEDIUM

    return category, priority
