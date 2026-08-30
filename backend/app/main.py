from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="ResolveAI API",
    version="0.1.0",
    description="Backend foundation for the ResolveAI support ticket copilot.",
)


class TicketCreate(BaseModel):
    subject: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=10, max_length=4000)
    customer_email: str


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tickets", status_code=201)
def create_ticket(ticket: TicketCreate) -> dict[str, object]:
    """Return a temporary ticket payload until persistence is added."""
    return {
        "message": "Ticket accepted",
        "ticket": ticket.model_dump(),
    }
