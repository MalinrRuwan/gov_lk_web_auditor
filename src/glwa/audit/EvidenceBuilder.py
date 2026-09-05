from __future__ import annotations

from urllib.parse import urlsplit

from ..models.DnsObservation import DnsObservation
from ..models.DomainObservation import DomainObservation
from ..models.Evidence import Evidence
from ..models.HttpObservation import HttpObservation
from ..models.TlsObservation import TlsObservation
from ..time.SriLankaTime import SriLankaTime


class EvidenceBuilder:
    def domain(self, item: DomainObservation) -> Evidence:
        if item.status == "expired":
            return self._new("domain_expired", "fail", item.detail)
        status = "pass" if item.status == "registered" else "error"
        return self._new("domain_registration", status, item.detail)

    def dns(self, item: DnsObservation) -> Evidence:
        if item.status == "absent":
            return self._new("dns_absent", "fail", item.detail)
        if item.status == "resolved":
            return self._new("dns", "pass", item.detail)
        return self._new("dns", "error", item.detail)

    def tls(self, item: TlsObservation) -> Evidence:
        if item.status == "expired":
            return self._new("tls_expired", "fail", item.detail)
        if item.status == "hostname_error":
            return self._new("tls_hostname", "fail", item.detail)
        status = "pass" if item.status == "valid" else "error"
        return self._new("tls", status, item.detail)

    def http(self, item: HttpObservation, probe: int) -> Evidence:
        if item.error:
            if "certificate verify failed" in item.error.lower():
                return self._new(
                    "tls_browser_error",
                    "fail",
                    f"Probe {probe}: {item.error}",
                    item.url,
                )
            return self._new(
                "http", "error", f"Probe {probe}: {item.error}", item.url
            )
        status = (
            "pass" if item.status_code and item.status_code < 400 else "fail"
        )
        detail = f"Probe {probe}: HTTP {item.status_code} at {item.final_url}"
        return self._new("http", status, detail, item.url)

    def redirect(self, original: str, final: str) -> Evidence | None:
        source_host = urlsplit(original).hostname or ""
        final_host = urlsplit(final).hostname or ""
        if self._related(source_host, final_host):
            return None
        detail = (
            "Redirect left the expected domain: "
            f"{source_host} to {final_host}"
        )
        return self._new("redirect_unrelated", "fail", detail, original)

    def persistent_http(self, items: list[HttpObservation]) -> Evidence | None:
        codes = [item.status_code for item in items]
        if codes and all(code is not None and code >= 400 for code in codes):
            return self._new(
                "persistent_http_failure",
                "fail",
                f"Every repeated HTTP probe failed: {codes}",
            )
        return None

    def _new(
        self, check: str, status: str, detail: str, source=None
    ) -> Evidence:
        observed = SriLankaTime.now().isoformat()
        return Evidence(check, status, detail, source, observed)

    def _related(self, first: str, second: str) -> bool:
        if first == second or first.endswith(f".{second}"):
            return True
        if second.endswith(f".{first}"):
            return True
        return first.endswith(".gov.lk") and second.endswith(".gov.lk")
