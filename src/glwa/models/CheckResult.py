from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class CheckResult:
    name: str
    level: int
    status: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
