import unittest

from financial_rule_agent import FinancialRule, FinancialRuleAgent


class FinancialRuleAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = FinancialRuleAgent(
            rules=[
                FinancialRule(
                    name="positive_amount",
                    description="Amount must be positive",
                    condition=lambda tx: tx.get("amount", 0) > 0,
                ),
                FinancialRule(
                    name="max_amount",
                    description="Amount must not exceed 10,000",
                    condition=lambda tx: tx.get("amount", 0) <= 10_000,
                ),
            ]
        )

    def test_approves_transaction_when_all_rules_pass(self) -> None:
        result = self.agent.evaluate_transaction({"amount": 1000})
        self.assertEqual({"approved": True, "failed_rules": []}, result)

    def test_rejects_transaction_when_any_rule_fails(self) -> None:
        result = self.agent.evaluate_transaction({"amount": -5})
        self.assertEqual(
            {"approved": False, "failed_rules": ["positive_amount"]},
            result,
        )

    def test_collects_multiple_failed_rules(self) -> None:
        result = self.agent.evaluate_transaction({"amount": 20_000})
        self.assertEqual(
            {"approved": False, "failed_rules": ["max_amount"]},
            result,
        )


if __name__ == "__main__":
    unittest.main()
