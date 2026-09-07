from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.main import KnowledgeDocumentCreate, Ticket, TicketCreate, TicketStatus


def test_ticket_create_validates_customer_input():
    ticket = TicketCreate(
        subject="Cannot sign in",
        description="The customer cannot access the account after resetting the password.",
        customer_email="user@example.com",
    )
    assert ticket.subject == "Cannot sign in"

    with pytest.raises(ValidationError):
        TicketCreate(subject="No", description="too short", customer_email="invalid")


def test_ticket_model_accepts_supported_statuses():
    ticket = Ticket(
        id="ticket-1",
        subject="Billing issue",
        description="Customer was charged twice for the same monthly subscription.",
        customer_email="user@example.com",
        status=TicketStatus.IN_PROGRESS,
        created_at=datetime.now(timezone.utc),
    )
    assert ticket.status is TicketStatus.IN_PROGRESS


def test_knowledge_document_requires_useful_content():
    document = KnowledgeDocumentCreate(
        title="Password reset",
        content="Guide customers through the password reset flow and verify account ownership.",
    )
    assert document.title == "Password reset"

    with pytest.raises(ValidationError):
        KnowledgeDocumentCreate(title="KB", content="short")
