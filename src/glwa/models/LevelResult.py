from dataclasses import asdict, dataclass
from typing import Any

from .CheckResult import CheckResult


@dataclass(frozen=True)
class LevelResult:
    level: int
    description: str
    status: str
    reason: str
    executed: bool
    checks: list[CheckResult]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
