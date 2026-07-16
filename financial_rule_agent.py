from dataclasses import dataclass
from typing import Callable, Dict, List, Sequence


Transaction = Dict[str, float]
RuleCondition = Callable[[Transaction], bool]


@dataclass(frozen=True)
class FinancialRule:
    name: str
    description: str
    condition: RuleCondition

    def evaluate(self, transaction: Transaction) -> bool:
        return bool(self.condition(transaction))


class FinancialRuleAgent:
    def __init__(self, rules: Sequence[FinancialRule]) -> None:
        self._rules: List[FinancialRule] = list(rules)

    def evaluate_transaction(self, transaction: Transaction) -> Dict[str, List[str] | bool]:
        failed_rules = [
            rule.name for rule in self._rules if not rule.evaluate(transaction)
        ]
        return {
            "approved": len(failed_rules) == 0,
            "failed_rules": failed_rules,
        }
