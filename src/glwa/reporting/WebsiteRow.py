import os
from pathlib import Path

from .WebsiteScore import WebsiteScore


class WebsiteRow:
    def __init__(self, read_me: Path):
        self.read_me = read_me

    def render(self, audit: dict, report: Path) -> str:
        target = os.path.relpath(report, self.read_me.parent)
        calculator = WebsiteScore()
        score = calculator.calculate(audit)
        url = audit["normalized_url"]
        return (
            f"| {score:.1f}/{calculator.maximum} | "
            f"[{url}]({Path(target).as_posix()}) |"
        )

    def sort(self, audits):
        return sorted(audits, key=self._sort_key)

    def _sort_key(self, item):
        audit = item[0]
        return WebsiteScore().calculate(audit), audit["normalized_url"]
