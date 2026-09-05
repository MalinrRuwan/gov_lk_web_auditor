from ..models.Evidence import Evidence
from ..network.MxResolver import MxResolver


class EmailDomainChecker:
    """Appends Level 2 email-domain evidence for the site's main email."""

    def __init__(self, mx_resolver: MxResolver | None = None):
        self.mx_resolver = mx_resolver or MxResolver()

    def collect(self, evidence: list[Evidence], site_host: str) -> list[Evidence]:
        main = self._main_email(evidence)
        if not main:
            return [
                self._new(
                    "email_in_site_domain",
                    "error",
                    "No published email address to compare",
                ),
                self._new(
                    "email_domain_has_mx",
                    "error",
                    "No published email address to check",
                ),
            ]
        domain = main.rsplit("@", 1)[1].strip().lower()
        site = site_host.strip().lower()
        on_site = self._on_site(domain, site)
        mx = self.mx_resolver.resolve(domain)
        return [
            self._new(
                "email_in_site_domain",
                "pass" if on_site else "fail",
                f"Email domain {domain} is "
                f"{'' if on_site else 'not '}part of the site domain {site}",
            ),
            self._new(
                "email_domain_has_mx",
                self._mx_status(mx.status),
                mx.detail,
            ),
        ]

    def _main_email(self, evidence: list[Evidence]) -> str | None:
        for item in evidence:
            if item.check != "email" or item.status != "pass":
                continue
            value = (item.data or {}).get("value")
            if isinstance(value, str) and "@" in value:
                return value
        return None

    def _on_site(self, domain: str, site: str) -> bool:
        if not site:
            return False
        return domain == site or domain.endswith(f".{site}")

    def _mx_status(self, status: str) -> str:
        return {"has_mx": "pass", "no_mx": "fail"}.get(status, "error")

    def _new(self, check: str, status: str, detail: str) -> Evidence:
        return Evidence(check, status, detail)
