import json
from pathlib import Path

from ..classification.LevelEvaluator import LevelEvaluator
from .LevelGuide import LevelGuide
from .LevelPieChart import LevelPieChart
from .LevelSection import LevelSection
from .MarkdownReport import MarkdownReport
from .ReadMeHeader import ReadMeHeader
from .WebsiteRow import WebsiteRow


class ReadMe:
    def __init__(self, target: Path = Path("README.md")):
        self.target = target

    def update(
        self, audit_folder: Path = Path("latest_audit_reports")
    ) -> Path:
        audits = self._latest(audit_folder)
        groups = self._groups(audits)
        content = "\n\n".join(
            [
                ReadMeHeader().render(LevelEvaluator.LEVELS),
                LevelGuide().render(LevelEvaluator.LEVELS),
                LevelPieChart().render(LevelEvaluator.LEVELS, groups),
                "## Documentation\n\n"
                "- [Article](docs/article.md): The grading framework.\n"
                "- [Design](docs/design.md): Architecture and rules.\n"
                "- [Roadmap](docs/roadmap.md): Work completed and planned.",
                *self._levels(groups),
            ]
        )
        self.target.write_text(content + "\n", encoding="utf-8")
        return self.target

    def _latest(self, folder: Path) -> list[tuple[dict, Path]]:
        latest = []
        for path in folder.glob("*/audit.json"):
            audit = json.loads(path.read_text(encoding="utf-8"))
            audit = MarkdownReport().prepare(audit)
            latest.append((audit, path.with_name("audit.md")))
        return sorted(latest, key=lambda item: item[0]["normalized_url"])

    def _groups(
        self, audits: list[tuple[dict, Path]]
    ) -> dict[int, list[str]]:
        groups = {level.number: [] for level in LevelEvaluator.LEVELS}
        rows = WebsiteRow(self.target)
        for audit, path in rows.sort(audits):
            row = rows.render(audit, path)
            groups[self._level(audit)].append(row)
        return groups

    def _levels(self, groups: dict[int, list[str]]) -> list[str]:
        return [
            LevelSection(level, groups[level.number]).render()
            for level in LevelEvaluator.LEVELS
            if level.implemented
        ]

    def _level(self, audit: dict) -> int:
        statuses = self._statuses(audit)
        passed = [
            level for level, status in enumerate(statuses) if status == "pass"
        ]
        return max(passed, default=0)

    def _statuses(self, audit: dict) -> list[str]:
        if audit.get("levels"):
            by_level = {
                item["level"]: item["status"] for item in audit["levels"]
            }
            return [by_level.get(level, "inconclusive") for level in range(6)]
        result = audit["result"]
        if result["status"] in {"fail", "level_0_confirmed"}:
            level_one = "fail"
        elif (
            result["status"] in {"inconclusive", "likely_level_0"}
            or result["confidence"] < 0.5
        ):
            level_one = "inconclusive"
        else:
            level_one = "pass"
        return ["pass", level_one, *["inconclusive"] * 4]
