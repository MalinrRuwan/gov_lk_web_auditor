from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class HttpObservation:
    url: str
    status_code: int | None
    final_url: str | None
    redirects: list[str]
    elapsed_ms: int | None
    content_type: str | None
    body: str
    error: str | None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("body")
        return data
