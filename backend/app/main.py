from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="ResolveAI API",
    version="0.2.0",
    description="Backend foundation for the ResolveAI support ticket copilot.",
)


class TicketCreate(BaseModel):
    subject: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=10, max_length=4000)
    customer_email: str


class Ticket(BaseModel):
    id: str
    subject: str
    description: str
    customer_email: str
    status: str = "open"
    created_at: datetime


tickets: list[Ticket] = []


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
