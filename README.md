# ResolveAI

ResolveAI is an AI-powered support ticket copilot designed to help support teams classify requests, retrieve relevant knowledge, and draft grounded responses faster.

## Day 1 scope

This first phase establishes the project structure and application foundations only. AI classification, retrieval, and response generation will be added in later phases.

## Planned architecture

- `frontend/` — Next.js + TypeScript interface for tickets and support workflows
- `backend/` — FastAPI service for ticket APIs and future AI orchestration
- PostgreSQL/Supabase — ticket and knowledge-base persistence
- Vector retrieval — pgvector or ChromaDB for grounded knowledge search

## Planned workflow

1. A support ticket is submitted.
2. The backend stores and exposes the ticket through an API.
3. Later phases will classify priority/category and retrieve supporting knowledge.
4. The copilot will suggest a grounded response with sources.

## Status

Day 1 — project foundation in progress.
