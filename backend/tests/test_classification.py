import unittest

from app.classification import TicketCategory, TicketPriority, classify_ticket


class TicketClassificationTests(unittest.TestCase):
    def test_billing_failure_is_high_priority(self) -> None:
        category, priority = classify_ticket(
            "Payment failed",
            "My card was charged but the payment failed and I cannot continue.",
        )
        self.assertEqual(category, TicketCategory.BILLING)
        self.assertEqual(priority, TicketPriority.HIGH)

    def test_security_issue_is_urgent(self) -> None:
        category, priority = classify_ticket(
            "Account security breach",
            "I think my account was accessed by someone else.",
        )
        self.assertEqual(category, TicketCategory.ACCOUNT)
        self.assertEqual(priority, TicketPriority.URGENT)

    def test_general_question_is_low_priority(self) -> None:
        category, priority = classify_ticket(
            "Product question",
            "I have a question about how to use this feature.",
        )
        self.assertEqual(category, TicketCategory.GENERAL)
        self.assertEqual(priority, TicketPriority.LOW)


if __name__ == "__main__":
    unittest.main()
