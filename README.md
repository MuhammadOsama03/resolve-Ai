# ResolveAI

ResolveAI is an end-to-end support ticket copilot that helps a support team triage incoming requests, retrieve trusted internal knowledge, and prepare grounded customer replies.

The project combines a **Next.js + TypeScript dashboard** with a **FastAPI backend**, automatic ticket classification, knowledge retrieval, optional Gemini generation, SQLite persistence, tests, Docker, and GitHub Actions CI.

## What it does

- Create and persist customer support tickets.
- Automatically classify each ticket by category and priority.
- Move tickets through `open`, `in_progress`, and `resolved` states.
- Build a trusted support knowledge base from internal notes and FAQs.
- Retrieve knowledge relevant to a ticket before generating a reply.
- Generate a grounded customer-response suggestion with Gemini when a key is configured.
- Fall back to a deterministic, source-aware response when no model key is available or the model request fails.
- Refuse to invent an answer when no relevant knowledge can be found.
- Show source count, model/fallback provider, and an explicit human-review requirement.
- Persist tickets and knowledge in SQLite so data survives backend restarts.
- Run the full stack locally with Docker Compose.
- Validate backend logic and frontend builds through GitHub Actions.

## Architecture

```text
Next.js dashboard
      |
      | REST
      v
FastAPI API
  |        |         |
  |        |         +--> Ticket classification
  |        +------------> Knowledge retrieval
  |                         |
  |                         +--> Gemini (optional)
  |                         +--> Safe fallback composer
  |
  +-----------------------> SQLite persistence
```

### Frontend

- Next.js 15
- React 19
- TypeScript
- Responsive custom CSS
- Typed API client

### Backend

- FastAPI
- Pydantic validation
- SQLite via Python's standard `sqlite3` module
- Deterministic category/priority classification
- Lexical knowledge retrieval with title weighting
- Optional Gemini REST integration
- Human-review-first fallback behavior

## Ticket intelligence

ResolveAI currently classifies tickets into:

- `billing`
- `access`
- `technical`
- `account`
- `general`

Priorities are assigned as:

- `low`
- `medium`
- `high`
- `urgent`

The classifier is deliberately deterministic so its behavior is transparent and testable. The generation layer is separate: Gemini can draft the final wording, while retrieval and source checks remain application-controlled.

## Grounded response workflow

1. A support ticket is created.
2. ResolveAI assigns a category and priority.
3. The ticket subject and description are used as the retrieval query.
4. Relevant knowledge documents are ranked.
5. If matching knowledge exists, the retrieved material is supplied to the copilot.
6. If `GEMINI_API_KEY` is configured, Gemini generates a constrained reply using the retrieved sources.
7. If Gemini is unavailable, ResolveAI produces a deterministic grounded fallback.
8. If no relevant source exists, ResolveAI refuses to produce an unsupported answer and requests manual review.

Every generated reply remains marked for human review before sending.

## Quick start with Docker

Docker Compose is the easiest way to run the complete project.

```bash
git clone https://github.com/MuhammadOsama03/resolve-Ai.git
cd resolve-Ai
cp .env.example .env
docker compose up --build
```

Then open:

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- FastAPI docs: `http://localhost:8000/docs`

SQLite data is stored in the Docker volume `resolveai-data` and survives container restarts.

## Run without Docker

### Backend

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment, then:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will run at `http://localhost:8000`.

### Frontend

In another terminal:

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

Open `http://localhost:3000`.

## Environment variables

### Backend

| Variable | Purpose | Default |
| --- | --- | --- |
| `RESOLVEAI_DB_PATH` | SQLite database location | `backend/resolveai.db` |
| `RESOLVEAI_CORS_ORIGINS` | Comma-separated allowed frontend origins | `http://localhost:3000` |
| `GEMINI_API_KEY` | Enables Gemini-generated replies | empty |
| `GEMINI_MODEL` | Gemini model name | `gemini-2.5-flash` |

The application does **not** require a Gemini key to run. Without one, grounded fallback responses remain available.

### Frontend

| Variable | Purpose | Default |
| --- | --- | --- |
| `NEXT_PUBLIC_API_URL` | ResolveAI backend URL | `http://localhost:8000` |

## API overview

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Service health/version |
| `GET` | `/tickets` | List tickets |
| `POST` | `/tickets` | Create and classify a ticket |
| `PATCH` | `/tickets/{ticket_id}` | Update ticket status |
| `POST` | `/tickets/{ticket_id}/suggestion` | Retrieve knowledge and draft a grounded reply |
| `GET` | `/knowledge` | List knowledge documents |
| `POST` | `/knowledge` | Add trusted knowledge |
| `GET` | `/knowledge/search` | Search/rank relevant knowledge |

Interactive request/response documentation is available through FastAPI at `/docs`.

## Tests

Backend tests cover:

- ticket classification
- knowledge retrieval ranking
- SQLite persistence and status updates
- grounded copilot fallback behavior
- Gemini/fallback provider selection

Run them with:

```bash
cd backend
python -m unittest discover -s tests -v
```

Frontend validation:

```bash
cd frontend
npm install
npm run typecheck
npm run build
```

The same backend and frontend checks run automatically in `.github/workflows/ci.yml` on pushes and pull requests to `main`.

## Project structure

```text
resolve-Ai/
├── .github/workflows/ci.yml
├── backend/
│   ├── app/
│   │   ├── classification.py
│   │   ├── config.py
│   │   ├── copilot.py
│   │   ├── llm.py
│   │   ├── main.py
│   │   ├── retrieval.py
│   │   └── storage.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/
│   ├── lib/api.ts
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Design decisions

**Grounding before generation.** ResolveAI retrieves support material first and only then drafts a response. A language model is not treated as the source of truth.

**Safe degradation.** External AI credentials are optional. The product still demonstrates the complete support workflow without a paid API or network dependency.

**Transparent first version of retrieval.** Retrieval is lexical and dependency-free rather than pretending to use embeddings. Its interface can later be replaced with pgvector, ChromaDB, or another vector store without changing the product workflow.

**Simple durable storage.** SQLite keeps the project easy to clone and demonstrate while providing real persistence. A production multi-user deployment could swap the storage layer for PostgreSQL/Supabase.

## Status

**Version 1.0 — complete portfolio release.**

The core end-to-end workflow is implemented: ticket intake, automated triage, persistent storage, knowledge retrieval, grounded response generation, human review cues, status management, responsive UI, automated tests, Docker setup, and CI.
