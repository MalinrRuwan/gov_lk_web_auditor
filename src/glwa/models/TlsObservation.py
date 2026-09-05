from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class TlsObservation:
    host: str
    status: str
    expires_at: str | None
    hostname_valid: bool | None
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
