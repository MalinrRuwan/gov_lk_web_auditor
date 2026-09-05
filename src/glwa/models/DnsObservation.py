from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class DnsObservation:
    host: str
    addresses: list[str]
    status: str
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
