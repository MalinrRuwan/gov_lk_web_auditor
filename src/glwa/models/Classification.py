from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Classification:
    status: str
    confidence: float
    reasons: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
