from ...models.CheckResult import CheckResult
from ...models.Evidence import Evidence
from ..Check import Check


class ContentRelevantCheck(Check):
    FAILURE = "unrelated"

    def __init__(self):
        super().__init__("content_relevant", 1)

    def run(self, evidence: list[Evidence]) -> CheckResult:
        for item in evidence:
            if item.check == self.FAILURE and item.status == "fail":
                return self.result("fail", item.detail)
        if any(
            item.check == "http" and item.status == "pass"
            for item in evidence
        ):
            return self.result("pass", "No unrelated-content marker found")
        return self.result("inconclusive", "No usable page was inspected")
