from ..checks.Check import Check
from ..models.CheckResult import CheckResult
from ..models.Evidence import Evidence
from ..models.LevelResult import LevelResult


class Level:
    COLORS = ("black", "red", "orange", "green", "blue", "purple")
    EMOJIS = ("⚫", "🔴", "🟠", "🟢", "🔵", "🟣")

    def __init__(
        self, number: int, description: str, checks: tuple[Check, ...] = ()
    ):
        self.number = number
        self.color = self.COLORS[number]
        self.emoji = self.EMOJIS[number]
        self.description = description
        self.checks = checks

    @property
    def implemented(self) -> bool:
        return self.number == 0 or bool(self.checks)

    @property
    def label(self) -> str:
        return f"{self.emoji} Level {self.number}"

    @property
    def markdown_label(self) -> str:
        return f"`{self.label}`"

    def run(
        self, evidence: list[Evidence], blocked_by: int | None = None
    ) -> LevelResult:
        if blocked_by is not None:
            reason = f"Not run because Level {blocked_by} did not pass"
            return self._result("inconclusive", reason, False, [])
        results = [check.run(evidence) for check in self.checks]
        if not results:
            reason = f"Level {self.number} checks are not implemented"
            return self._result("inconclusive", reason, False, [])
        status = self._status(results)
        reasons = [item.reason for item in results if item.status == status]
        reason = "; ".join(reasons)
        if not reason:
            reason = "All Level %s checks passed" % self.number
        return self._result(status, reason, True, results)

    def _status(self, results: list[CheckResult]) -> str:
        statuses = {item.status for item in results}
        if "fail" in statuses:
            return "fail"
        if "inconclusive" in statuses:
            return "inconclusive"
        return "pass"

    def _result(self, status, reason, executed, checks):
        return LevelResult(
            self.number,
            self.description,
            status,
            reason,
            executed,
            checks,
        )
