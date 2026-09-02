import sqlite3
from collections.abc import Iterable
from pathlib import Path


def connect(database_path: Path) -> sqlite3.Connection:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(database_path: Path) -> None:
    with connect(database_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id TEXT PRIMARY KEY,
                subject TEXT NOT NULL,
                description TEXT NOT NULL,
                customer_email TEXT NOT NULL,
                status TEXT NOT NULL,
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS knowledge_documents (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )


def list_rows(database_path: Path, table: str) -> list[dict[str, object]]:
    allowed_tables = {"tickets", "knowledge_documents"}
    if table not in allowed_tables:
        raise ValueError("Unsupported table")

    with connect(database_path) as connection:
        rows = connection.execute(
            f"SELECT * FROM {table} ORDER BY created_at DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def insert_ticket(database_path: Path, ticket: dict[str, object]) -> None:
    with connect(database_path) as connection:
        connection.execute(
            """
            INSERT INTO tickets (
                id, subject, description, customer_email, status,
                category, priority, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ticket["id"],
                ticket["subject"],
                ticket["description"],
                ticket["customer_email"],
                ticket["status"],
                ticket["category"],
                ticket["priority"],
                ticket["created_at"],
            ),
        )


def update_ticket_status(database_path: Path, ticket_id: str, status: str) -> bool:
    with connect(database_path) as connection:
        cursor = connection.execute(
            "UPDATE tickets SET status = ? WHERE id = ?",
            (status, ticket_id),
        )
    return cursor.rowcount > 0


def insert_knowledge_document(database_path: Path, document: dict[str, object]) -> None:
    with connect(database_path) as connection:
        connection.execute(
            """
            INSERT INTO knowledge_documents (id, title, content, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                document["id"],
                document["title"],
                document["content"],
                document["created_at"],
            ),
        )


def get_row_by_id(database_path: Path, table: str, row_id: str) -> dict[str, object] | None:
    allowed_tables = {"tickets", "knowledge_documents"}
    if table not in allowed_tables:
        raise ValueError("Unsupported table")

    with connect(database_path) as connection:
        row = connection.execute(
            f"SELECT * FROM {table} WHERE id = ?",
            (row_id,),
        ).fetchone()
    return dict(row) if row else None


def replace_knowledge(database_path: Path, documents: Iterable[dict[str, object]]) -> None:
    with connect(database_path) as connection:
        connection.execute("DELETE FROM knowledge_documents")
        connection.executemany(
            """
            INSERT INTO knowledge_documents (id, title, content, created_at)
            VALUES (?, ?, ?, ?)
            """,
            [
                (document["id"], document["title"], document["content"], document["created_at"])
                for document in documents
            ],
        )
