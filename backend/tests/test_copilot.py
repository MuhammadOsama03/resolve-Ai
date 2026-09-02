import unittest
from unittest.mock import patch

from app.copilot import build_grounded_suggestion


class CopilotTests(unittest.TestCase):
    def test_refuses_to_draft_without_supporting_knowledge(self) -> None:
        result = build_grounded_suggestion(
            "Unknown issue",
            "The customer asks about an undocumented policy.",
            [],
        )
        self.assertTrue(result["needs_review"])
        self.assertEqual(result["source_ids"], [])
        self.assertEqual(result["provider"], "fallback")

    @patch("app.copilot.generate_gemini_reply", return_value=None)
    def test_fallback_reply_keeps_source_ids(self, _: object) -> None:
        result = build_grounded_suggestion(
            "Password reset",
            "Customer cannot sign in after forgetting their password.",
            [
                {
                    "id": "doc-1",
                    "title": "Password reset guide",
                    "content": "Use the account recovery screen to request a password reset link.",
                }
            ],
        )
        self.assertEqual(result["source_ids"], ["doc-1"])
        self.assertEqual(result["provider"], "fallback")
        self.assertIn("Password reset guide", result["suggestion"])

    @patch("app.copilot.generate_gemini_reply", return_value="Please use the account recovery screen.")
    def test_model_reply_is_marked_as_gemini(self, _: object) -> None:
        result = build_grounded_suggestion(
            "Password reset",
            "Customer cannot sign in.",
            [{"id": "doc-1", "title": "Reset", "content": "Use account recovery."}],
        )
        self.assertEqual(result["provider"], "gemini")
        self.assertEqual(result["suggestion"], "Please use the account recovery screen.")
        self.assertTrue(result["needs_review"])


if __name__ == "__main__":
    unittest.main()
