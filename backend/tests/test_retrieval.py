import unittest

from app.retrieval import rank_documents, tokenize


class RetrievalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.documents = [
            {
                "id": "billing",
                "title": "Refund and billing policy",
                "content": "Refund requests are reviewed after a duplicate payment or incorrect charge.",
            },
            {
                "id": "access",
                "title": "Password reset guide",
                "content": "Locked users can reset their password from the sign-in page.",
            },
            {
                "id": "general",
                "title": "Office hours",
                "content": "Support agents are available on weekdays.",
            },
        ]

    def test_tokenize_normalizes_and_deduplicates_terms(self) -> None:
        self.assertEqual(tokenize("Refund REFUND payment!"), {"refund", "payment"})

    def test_title_matches_receive_stronger_ranking(self) -> None:
        results = rank_documents("refund billing payment", self.documents, limit=2)
        self.assertEqual(results[0]["id"], "billing")

    def test_irrelevant_query_returns_no_documents(self) -> None:
        self.assertEqual(rank_documents("satellite weather", self.documents), [])

    def test_limit_caps_number_of_results(self) -> None:
        results = rank_documents("support reset refund", self.documents, limit=1)
        self.assertEqual(len(results), 1)


if __name__ == "__main__":
    unittest.main()
