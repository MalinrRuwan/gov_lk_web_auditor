from ..classification.LevelEvaluator import LevelEvaluator


class WebsiteScore:
    def __init__(self):
        self.levels = tuple(
            level.number
            for level in LevelEvaluator.LEVELS
            if level.number and level.implemented
        )

    @property
    def maximum(self) -> int:
        return len(self.levels)

    def calculate(self, audit: dict) -> float:
        levels = {item["level"]: item for item in audit.get("levels", [])}
        score = sum(self._level(levels.get(number)) for number in self.levels)
        return round(score, 1)

    def _level(self, level: dict | None) -> float:
        if not level:
            return 0
        checks = level.get("checks", [])
        if not checks:
            return 0
        passed = sum(check["status"] == "pass" for check in checks)
        return passed / len(checks)
