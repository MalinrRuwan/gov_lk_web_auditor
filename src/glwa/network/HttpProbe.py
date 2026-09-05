import httpx

from ..models.HttpObservation import HttpObservation
from .SafeHttpClient import SafeHttpClient


class HttpProbe:
    def __init__(self, timeout: float = 30.0, max_bytes: int = 1_000_000):
        self.timeout = timeout
        self.max_bytes = max_bytes
        self.client = SafeHttpClient(timeout)

    def probe(self, url: str) -> HttpObservation:
        try:
            response = self.client.get(url, self.max_bytes)
            body = response.content.decode("utf-8", errors="replace")
            return HttpObservation(
                url,
                response.status_code,
                response.url,
                response.redirects,
                response.elapsed_ms,
                response.content_type,
                body,
                None,
            )
        except (httpx.HTTPError, ValueError) as error:
            return HttpObservation(
                url, None, None, [], None, None, "", str(error)
            )
