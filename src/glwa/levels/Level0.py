from ..models.LevelResult import LevelResult
from .Level import Level


class Level0(Level):
    def __init__(self):
        super().__init__(
            0,
            "A site is classified as `Level 0` when it is unavailable or "
            "unusable, or when there is not enough evidence to establish "
            "that it meets `Level 1`.",
        )

    def run(self, evidence, blocked_by=None) -> LevelResult:
        return LevelResult(
            self.number,
            self.description,
            "pass",
            "Baseline website grade",
            True,
            [],
        )
