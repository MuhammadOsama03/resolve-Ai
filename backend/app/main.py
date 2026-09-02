from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

from .classification import TicketCategory, TicketPriority, classify_ticket
from .config import CORS_ORIGINS, DATABASE_PATH
from .copilot import build_grounded_suggestion
from .retrieval import rank_documents
from .storage import (
    get_row_by_id,
    initialize_database,
    insert_knowledge_document,
    insert_ticket,
    list_rows,
    update_ticket_status,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database(DATABASE_PATH)
    yield


app = FastAPI(
    title="ResolveAI API",
    version="1.0.0",
    description="API for the ResolveAI support ticket copilot.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


class TicketCreate(BaseModel):
    subject: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=10, max_length=4000)
    customer_email: EmailStr


class TicketUpdate(BaseModel):
    status: TicketStatus


class Ticket(BaseModel):
    id: str
    subject: str
    description: str
    customer_email: EmailStr
    status: TicketStatus = TicketStatus.OPEN
    category: TicketCategory = TicketCategory.GENERAL
    priority: TicketPriority = TicketPriority.MEDIUM
    created_at: datetime


class KnowledgeDocumentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    content: str = Field(min_length=20, max_length=10000)


class KnowledgeDocument(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime


class CopilotSuggestion(BaseModel):
    suggestion: str
    source_ids: list[str]
    needs_review: bool
    ticket_context: str | None = None
    provider: str = "fallback"


def get_ticket_or_404(ticket_id: str) -> Ticket:
    row = get_row_by_id(DATABASE_PATH, "tickets", ticket_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return Ticket.model_validate(row)


def get_knowledge_documents() -> list[KnowledgeDocument]:
    return [
        KnowledgeDocument.model_validate(row)
        for row in list_rows(DATABASE_PATH, "knowledge_documents")
    ]


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "version": app.version}


@app.get("/tickets", response_model=list[Ticket])
def list_tickets() -> list[Ticket]:
    return [Ticket.model_validate(row) for row in list_rows(DATABASE_PATH, "tickets")]


@app.post("/tickets", response_model=Ticket, status_code=201)
def create_ticket(ticket: TicketCreate) -> Ticket:
    category, priority = classify_ticket(ticket.subject, ticket.description)
    created = Ticket(
        id=str(uuid4()),
        created_at=datetime.now(timezone.utc),
        category=category,
        priority=priority,
        **ticket.model_dump(),
    )
    insert_ticket(DATABASE_PATH, created.model_dump(mode="json"))
    return created


@app.patch("/tickets/{ticket_id}", response_model=Ticket)
def update_ticket(ticket_id: str, payload: TicketUpdate) -> Ticket:
    if not update_ticket_status(DATABASE_PATH, ticket_id, payload.status.value):
        raise HTTPException(status_code=404, detail="Ticket not found")
    return get_ticket_or_404(ticket_id)


@app.post("/tickets/{ticket_id}/suggestion", response_model=CopilotSuggestion)
def create_ticket_suggestion(ticket_id: str) -> CopilotSuggestion:
    ticket = get_ticket_or_404(ticket_id)
    documents = get_knowledge_documents()
    query = f"{ticket.subject} {ticket.description}"
    ranked = rank_documents(
        query,
        [document.model_dump(mode="json") for document in documents],
        limit=3,
    )
    suggestion = build_grounded_suggestion(
        ticket.subject,
        ticket.description,
        ranked,
    )
    return CopilotSuggestion.model_validate(suggestion)


@app.get("/knowledge", response_model=list[KnowledgeDocument])
def list_knowledge_documents() -> list[KnowledgeDocument]:
    return get_knowledge_documents()


@app.get("/knowledge/search", response_model=list[KnowledgeDocument])
def search_knowledge(
    q: str = Query(min_length=2, max_length=500),
    limit: int = Query(default=3, ge=1, le=10),
) -> list[KnowledgeDocument]:
    documents = get_knowledge_documents()
    ranked = rank_documents(
        q,
        [document.model_dump(mode="json") for document in documents],
        limit=limit,
    )
    return [KnowledgeDocument.model_validate(document) for document in ranked]


@app.post("/knowledge", response_model=KnowledgeDocument, status_code=201)
def create_knowledge_document(payload: KnowledgeDocumentCreate) -> KnowledgeDocument:
    document = KnowledgeDocument(
        id=str(uuid4()),
        created_at=datetime.now(timezone.utc),
        **payload.model_dump(),
    )
    insert_knowledge_document(DATABASE_PATH, document.model_dump(mode="json"))
    return document
