from ...classification.LevelEvaluator import LevelEvaluator
from ...models.Evidence import Evidence


class MarkdownReportPreparationMixin:
    def prepare(self, audit: dict) -> dict:
        levels = audit.get("levels", [])
        if self._current(levels):
            return audit
        evidence = [Evidence(**item) for item in audit.get("evidence", [])]
        levels = [
            item.to_dict() for item in LevelEvaluator().evaluate(evidence)
        ]
        return {**audit, "levels": levels}

    def _current(self, levels: list[dict]) -> bool:
        by_level = {item["level"]: item for item in levels}
        if by_level.get(0, {}).get("checks"):
            return False
        blocked = False
        for level in LevelEvaluator.LEVELS[1:]:
            if not level.implemented or blocked:
                continue
            item = by_level.get(level.number, {})
            active = {check.name for check in level.checks}
            stored = {check["name"] for check in item.get("checks", [])}
            if not stored or not stored <= active:
                return False
            blocked = item.get("status") != "pass"
        return True
