from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="ResolveAI API",
    version="0.3.0",
    description="Backend foundation for the ResolveAI support ticket copilot.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
    customer_email: str


class TicketUpdate(BaseModel):
    status: TicketStatus


class Ticket(BaseModel):
    id: str
    subject: str
    description: str
    customer_email: str
    status: TicketStatus = TicketStatus.OPEN
    created_at: datetime


class KnowledgeDocumentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    content: str = Field(min_length=20, max_length=10000)


class KnowledgeDocument(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime


tickets: list[Ticket] = []
knowledge_documents: list[KnowledgeDocument] = []


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tickets", response_model=list[Ticket])
def list_tickets() -> list[Ticket]:
    return tickets


@app.post("/tickets", response_model=Ticket, status_code=201)
def create_ticket(ticket: TicketCreate) -> Ticket:
    created = Ticket(
        id=str(uuid4()),
        created_at=datetime.now(timezone.utc),
        **ticket.model_dump(),
    )
    tickets.append(created)
    return created


@app.patch("/tickets/{ticket_id}", response_model=Ticket)
def update_ticket(ticket_id: str, payload: TicketUpdate) -> Ticket:
    for ticket in tickets:
        if ticket.id == ticket_id:
            ticket.status = payload.status
            return ticket
    raise HTTPException(status_code=404, detail="Ticket not found")


@app.get("/knowledge", response_model=list[KnowledgeDocument])
def list_knowledge_documents() -> list[KnowledgeDocument]:
    return knowledge_documents


@app.post("/knowledge", response_model=KnowledgeDocument, status_code=201)
def create_knowledge_document(payload: KnowledgeDocumentCreate) -> KnowledgeDocument:
    document = KnowledgeDocument(
        id=str(uuid4()),
        created_at=datetime.now(timezone.utc),
        **payload.model_dump(),
    )
    knowledge_documents.append(document)
    return document
