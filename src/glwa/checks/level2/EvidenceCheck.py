from ...models.CheckResult import CheckResult
from ...models.Evidence import Evidence
from ..Check import Check


class EvidenceCheck(Check):
    def __init__(self, name: str, label: str):
        super().__init__(name, 2)
        self.label = label

    def run(self, evidence: list[Evidence]) -> CheckResult:
        items = [item for item in evidence if item.check == self.name]
        status, reason = self._outcome(items)
        return self.result(status, reason)

    def _outcome(self, items: list[Evidence]) -> tuple[str, str]:
        failed = next((item for item in items if item.status == "fail"), None)
        if failed:
            return "fail", failed.detail
        passed = next((item for item in items if item.status == "pass"), None)
        if passed:
            return "pass", passed.detail
        return (
            "inconclusive",
            f"No passing {self.label.lower()} evidence found",
        )
