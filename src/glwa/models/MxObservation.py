from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class MxObservation:
    domain: str
    status: str
    records: list[tuple[int, str]]
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
