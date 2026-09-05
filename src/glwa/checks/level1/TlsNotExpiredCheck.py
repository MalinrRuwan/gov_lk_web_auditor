from ...models.CheckResult import CheckResult
from ...models.Evidence import Evidence
from ..Check import Check


class TlsNotExpiredCheck(Check):
    FAILURE = "tls_expired"

    def __init__(self):
        super().__init__("tls_not_expired", 1)

    def run(self, evidence: list[Evidence]) -> CheckResult:
        failed = next(
            (item for item in evidence if item.check == self.FAILURE), None
        )
        if failed:
            return self.result("fail", failed.detail)
        tls = next((item for item in evidence if item.check == "tls"), None)
        if not tls:
            return self.result("inconclusive", "TLS expiry check did not run")
        status = "pass" if tls.status == "pass" else "inconclusive"
        return self.result(status, tls.detail)
