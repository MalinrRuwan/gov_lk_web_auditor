from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class DomainObservation:
    domain: str
    status: str
    expires_at: str | None
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
