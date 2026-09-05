import tempfile
import unittest
from pathlib import Path

from glwa.classification.LevelEvaluator import LevelEvaluator
from glwa.reporting.MarkdownReport import MarkdownReport


class TestMarkdownReport(unittest.TestCase):
    def test_rejects_removed_check_from_stored_levels(self):
        levels = [
            self._level(0, "pass", "Fallback grade", []),
            self._level(
                1,
                "inconclusive",
                "Availability",
                [{"name": "domain_not_expired"}],
            ),
        ]
        self.assertFalse(MarkdownReport()._current(levels))

    def test_rejects_missing_implemented_level_checks(self):
        checks = [
            {"name": check.name} for check in LevelEvaluator.LEVELS[1].checks
        ]
        levels = [
            self._level(0, "pass", "Fallback grade", []),
            self._level(1, "pass", "Availability", checks),
            self._level(2, "inconclusive", "Contact information", []),
        ]
        self.assertFalse(MarkdownReport()._current(levels))

    def test_stops_after_failed_level(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "audit.md"
            MarkdownReport().write_data(self._audit(), path)
            markdown = path.read_text("utf-8")
            self.assertIn("- Completed: 2026-09-01 15:30", markdown)
            self.assertIn("- Overall result: ⚫ Level 0", markdown)
            self.assertIn("## ⚫ Level 0: ✅", markdown)
            self.assertIn("## 🔴 Level 1: ❌", markdown)
            self.assertIn("| dns_resolves | ❌ |", markdown)
            self.assertNotIn("## 🟠 Level 2", markdown)
            self.assertNotIn("## 🟢 Level 3", markdown)

    def test_formats_inline_level_references(self):
        report = MarkdownReport()
        self.assertEqual(
            "To pass `🔴 Level 1`, first pass ⚫ Level 0",
            report._references("To pass `Level 1`, first pass Level 0"),
        )

    def _audit(self):
        return {
            "normalized_url": "https://example.gov.lk/",
            "completed_at": "2026-09-01T10:00:00+00:00",
            "result": {"status": "fail"},
            "levels": [
                self._level(0, "pass", "Fallback grade", []),
                self._level(
                    1,
                    "fail",
                    "Availability",
                    [
                        {
                            "name": "dns_resolves",
                            "status": "fail",
                            "reason": "DNS absent",
                        }
                    ],
                ),
                self._level(2, "inconclusive", "Contact information", []),
            ],
        }

    def _level(self, number, status, description, checks):
        reason = "DNS absent" if status == "fail" else "Not run"
        return {
            "level": number,
            "description": description,
            "status": status,
            "reason": reason,
            "executed": status != "inconclusive",
            "checks": checks,
        }


if __name__ == "__main__":
    unittest.main()
