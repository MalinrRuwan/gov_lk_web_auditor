import csv
import html
import json
from pathlib import Path

from ..audit.Audit import Audit
from ..audit.AuditValidator import AuditValidator
from ..time.SriLankaTime import SriLankaTime
from .LevelsCsvReport import LevelsCsvReport
from .MarkdownReport import MarkdownReport


class ReportWriter:
    def write(self, audit: Audit, output: Path) -> list[Path]:
        output.mkdir(parents=True, exist_ok=True)
        AuditValidator().validate(audit)
        paths = [
            self._json(audit, output),
            LevelsCsvReport().write(audit, output),
            self._csv(audit, output),
            self._html(audit, output),
            MarkdownReport().write(audit, output),
        ]
        return paths

    def _json(self, audit: Audit, output: Path) -> Path:
        path = output / "audit.json"
        path.write_text(
            json.dumps(audit.to_dict(), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return path

    def _csv(self, audit: Audit, output: Path) -> Path:
        path = output / "evidence.csv"
        with path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "check",
                    "status",
                    "detail",
                    "source",
                    "observed_at",
                ],
            )
            writer.writeheader()
            writer.writerows(self._evidence_rows(audit, writer.fieldnames))
        return path

    def _evidence_rows(self, audit, fieldnames):
        for item in audit.evidence:
            data = item.to_dict()
            if data.get("observed_at"):
                data["observed_at"] = SriLankaTime.iso(data["observed_at"])
            yield {key: data.get(key, "") for key in fieldnames}

    def _html(self, audit: Audit, output: Path) -> Path:
        level_rows = "".join(
            "<tr>"
            f"<td>Level {item.level}</td>"
            f"<td><span class='{item.status}'>{item.status}</span></td>"
            f"<td>{html.escape(item.reason)}</td>"
            "</tr>"
            for item in audit.levels
        )
        rows = "".join(
            "<tr>"
            f"<td>{html.escape(item.check)}</td>"
            f"<td><span class='{item.status}'>{item.status}</span></td>"
            f"<td>{html.escape(item.detail)}</td>"
            "</tr>"
            for item in audit.evidence
        )
        template_path = Path(__file__).parent / "templates" / "report.html"
        page = template_path.read_text(encoding="utf-8")
        replacements = {
            "{{URL}}": html.escape(audit.normalized_url),
            "{{STATUS}}": html.escape(audit.result.status),
            "{{CONFIDENCE}}": f"{audit.result.confidence:.0%}",
            "{{COMPLETED}}": html.escape(
                SriLankaTime.iso(audit.completed_at)
            ),
            "{{LEVEL_ROWS}}": level_rows,
            "{{ROWS}}": rows,
        }
        for key, value in replacements.items():
            page = page.replace(key, value)
        path = output / "report.html"
        path.write_text(page, encoding="utf-8")
        return path
