from ..checks.level1 import (
    ContentRelevantCheck,
    DnsResolvesCheck,
    DomainNotParkedCheck,
    HostingConfiguredCheck,
    HttpAvailableCheck,
    RedirectRelatedCheck,
    SiteNotDefacedCheck,
    TlsBrowserTrustedCheck,
    TlsHostnameMatchesCheck,
    TlsNotExpiredCheck,
)
from ..models.Evidence import Evidence
from ..models.LevelResult import LevelResult
from .Level import Level


class Level1(Level):
    # A certificate that has expired must still count against the score, but
    # it should not demote the site to Level 0: DNS, HTTP and identity may
    # all be substantiated while the certificate needs renewing. These checks
    # therefore remain failing rows in the report while the site itself stays
    # at Level 1.
    CERT_EXPIRY_CHECKS = {"tls_not_expired", "tls_browser_trusted"}

    def __init__(self):
        checks = (
            DnsResolvesCheck(),
            DomainNotParkedCheck(),
            SiteNotDefacedCheck(),
            ContentRelevantCheck(),
            HostingConfiguredCheck(),
            HttpAvailableCheck(),
            RedirectRelatedCheck(),
            TlsBrowserTrustedCheck(),
            TlsNotExpiredCheck(),
            TlsHostnameMatchesCheck(),
        )
        super().__init__(
            1,
            "To pass `Level 1`, the website must be available, usable, and "
            "clearly associated with the government institution. It must "
            "load reliably with valid DNS, HTTP, and TLS behavior.",
            checks,
        )

    def run(
        self, evidence: list[Evidence], blocked_by: int | None = None
    ) -> LevelResult:
        result = super().run(evidence, blocked_by)
        if blocked_by is not None or not self._certificate_expired(evidence):
            return result
        remaining = [
            item for item in result.checks if item.name not in self.CERT_EXPIRY_CHECKS
        ]
        if any(item.status == "fail" for item in remaining):
            return result
        return self._result(
            "pass",
            "TLS certificate expired but the site remains available; kept at Level 1",
            result.executed,
            result.checks,
        )

    def _certificate_expired(self, evidence: list[Evidence]) -> bool:
        return any(
            item.check == TlsNotExpiredCheck.FAILURE and item.status == "fail"
            for item in evidence
        )
