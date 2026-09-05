from ...models.CheckResult import CheckResult
from ...models.Evidence import Evidence
from ..Check import Check


class TlsHostnameMatchesCheck(Check):
    FAILURE = "tls_hostname"

    def __init__(self):
        super().__init__("tls_hostname_matches", 1)

    def run(self, evidence: list[Evidence]) -> CheckResult:
        failed = next(
            (item for item in evidence if item.check == self.FAILURE), None
        )
        if failed:
            return self.result("fail", failed.detail)
        tls = next((item for item in evidence if item.check == "tls"), None)
        if not tls:
            reason = "TLS hostname check did not run"
            return self.result("inconclusive", reason)
        status = "pass" if tls.status == "pass" else "inconclusive"
        return self.result(status, tls.detail)
