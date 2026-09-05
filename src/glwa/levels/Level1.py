from ..checks.level1 import (ContentRelevantCheck, DnsResolvesCheck,
                             DomainNotParkedCheck, HostingConfiguredCheck,
                             HttpAvailableCheck, RedirectRelatedCheck,
                             SiteNotDefacedCheck, TlsBrowserTrustedCheck,
                             TlsHostnameMatchesCheck, TlsNotExpiredCheck)
from .Level import Level


class Level1(Level):
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
