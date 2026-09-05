from ...models.CheckResult import CheckResult
from ...models.Evidence import Evidence
from ..Check import Check


class EvidenceCheck(Check):
    def __init__(self, name: str, label: str):
        super().__init__(name, 3)
        self.label = label

    def run(self, evidence: list[Evidence]) -> CheckResult:
        items = [item for item in evidence if item.check == self.name]
        failed = next((item for item in items if item.status == "fail"), None)
        if failed:
            return self.result("fail", failed.detail)
        passed = next((item for item in items if item.status == "pass"), None)
        if passed:
            return self.result("pass", passed.detail)
        reason = f"No passing {self.label.lower()} evidence found"
        return self.result("inconclusive", reason)
