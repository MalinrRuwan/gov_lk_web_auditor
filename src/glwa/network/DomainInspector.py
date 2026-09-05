import httpx

from ..models.DomainObservation import DomainObservation
from ..time.SriLankaTime import SriLankaTime


class DomainInspector:
    EXPIRED_STATUSES = {"pending delete", "redemption period"}

    def inspect(self, host: str) -> DomainObservation:
        domain = self._base_domain(host)
        try:
            response = httpx.get(
                f"https://rdap.org/domain/{domain}",
                follow_redirects=True,
                timeout=10,
            )
            if response.status_code == 404:
                return DomainObservation(
                    domain, "unknown", None, "Domain is absent from RDAP"
                )
            response.raise_for_status()
            return self._observation(domain, response.json())
        except (httpx.HTTPError, ValueError, TypeError) as error:
            return DomainObservation(domain, "unknown", None, str(error))

    def _observation(self, domain: str, data: dict) -> DomainObservation:
        statuses = {item.lower() for item in data.get("status", [])}
        expiration = next(
            (
                event.get("eventDate")
                for event in data.get("events", [])
                if event.get("eventAction") == "expiration"
            ),
            None,
        )
        expired = bool(statuses & self.EXPIRED_STATUSES)
        if expiration:
            date = SriLankaTime.parse(expiration)
            expiration = date.isoformat()
            expired = expired or date <= SriLankaTime.now()
        status = "expired" if expired else "registered"
        detail = (
            "Domain registration expired" if expired else "Domain registered"
        )
        return DomainObservation(domain, status, expiration, detail)

    def _base_domain(self, host: str) -> str:
        labels = host.rstrip(".").split(".")
        if host.endswith(".gov.lk") and len(labels) >= 3:
            return ".".join(labels[-3:])
        return ".".join(labels[-2:])
