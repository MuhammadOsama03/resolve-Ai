import tempfile
import unittest
from pathlib import Path

from app.storage import (
    get_row_by_id,
    initialize_database,
    insert_knowledge_document,
    insert_ticket,
    list_rows,
    update_ticket_status,
)


class StorageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "test.db"
        initialize_database(self.database_path)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_ticket_round_trip_and_status_update(self) -> None:
        ticket = {
            "id": "ticket-1",
            "subject": "Cannot sign in",
            "description": "The customer is locked out of their account.",
            "customer_email": "customer@example.com",
            "status": "open",
            "category": "access",
            "priority": "high",
            "created_at": "2026-09-02T09:00:00+00:00",
        }
        insert_ticket(self.database_path, ticket)

        stored = get_row_by_id(self.database_path, "tickets", "ticket-1")
        self.assertIsNotNone(stored)
        self.assertEqual(stored["category"], "access")

        self.assertTrue(update_ticket_status(self.database_path, "ticket-1", "resolved"))
        updated = get_row_by_id(self.database_path, "tickets", "ticket-1")
        self.assertEqual(updated["status"], "resolved")

    def test_knowledge_documents_are_persisted(self) -> None:
        document = {
            "id": "doc-1",
            "title": "Password reset guide",
            "content": "Users can reset passwords from the account recovery screen.",
            "created_at": "2026-09-02T09:10:00+00:00",
        }
        insert_knowledge_document(self.database_path, document)

        rows = list_rows(self.database_path, "knowledge_documents")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["title"], "Password reset guide")

    def test_unknown_table_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            list_rows(self.database_path, "unsafe_table")


if __name__ == "__main__":
    unittest.main()
