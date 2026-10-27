import unittest
from app.retrieval import rank_documents


class RetrievalLimitTests(unittest.TestCase):
    def test_zero_limit_rejected(self):
        with self.assertRaises(ValueError):
            rank_documents("refund", [{"title": "refund", "content": "refund"}], limit=0)

    def test_negative_limit_rejected(self):
        with self.assertRaises(ValueError):
            rank_documents("refund", [{"title": "refund", "content": "refund"}], limit=-1)


if __name__ == "__main__":
    unittest.main()
