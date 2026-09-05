from dataclasses import dataclass


@dataclass(frozen=True)
class FetchedPage:
    status_code: int
    url: str
    redirects: list[str]
    elapsed_ms: int
    content_type: str | None
    content: bytes
