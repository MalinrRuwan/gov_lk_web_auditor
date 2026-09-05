from ...models.CheckResult import CheckResult
from ...models.Evidence import Evidence
from ..Check import Check


class TlsBrowserTrustedCheck(Check):
    FAILURE = "tls_browser_error"

    def __init__(self):
        super().__init__("tls_browser_trusted", 1)

    def run(self, evidence: list[Evidence]) -> CheckResult:
        for item in evidence:
            if item.check == self.FAILURE and item.status == "fail":
                return self.result("fail", item.detail)
        if any(
            item.check == "http" and item.status == "pass"
            for item in evidence
        ):
            return self.result("pass", "No browser-blocking TLS error found")
        return self.result(
            "inconclusive", "Browser TLS check did not complete"
        )
