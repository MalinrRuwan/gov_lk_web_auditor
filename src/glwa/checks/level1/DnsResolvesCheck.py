from ...models.CheckResult import CheckResult
from ...models.Evidence import Evidence
from ..Check import Check


class DnsResolvesCheck(Check):
    FAILURE = "dns_absent"

    def __init__(self):
        super().__init__("dns_resolves", 1)

    def run(self, evidence: list[Evidence]) -> CheckResult:
        failed = next(
            (item for item in evidence if item.check == self.FAILURE), None
        )
        if failed:
            return self.result("fail", failed.detail)
        dns = next((item for item in evidence if item.check == "dns"), None)
        if not dns:
            return self.result("inconclusive", "DNS check did not run")
        status = "pass" if dns.status == "pass" else "inconclusive"
        return self.result(status, dns.detail)
