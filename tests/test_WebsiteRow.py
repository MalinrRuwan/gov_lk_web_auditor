import unittest
from pathlib import Path

from glwa.reporting.WebsiteRow import WebsiteRow


class TestWebsiteRow(unittest.TestCase):
    def test_renders_score_to_one_decimal(self):
        audit, report = self._item("https://a.gov.lk", "pass")
        row = WebsiteRow(Path("README.md")).render(audit, report)
        self.assertEqual("| 1.0/3 | [https://a.gov.lk](audit.md) |", row)

    def test_sorts_by_score_ascending_then_url(self):
        audits = [
            self._item("https://b.gov.lk", "pass"),
            self._item("https://c.gov.lk", "fail"),
            self._item("https://a.gov.lk", "pass"),
        ]
        sorted_audits = WebsiteRow(Path("README.md")).sort(audits)
        self.assertEqual(
            ["https://c.gov.lk", "https://a.gov.lk", "https://b.gov.lk"],
            [item[0]["normalized_url"] for item in sorted_audits],
        )

    def _item(self, url, status):
        audit = {
            "normalized_url": url,
            "levels": [
                {"level": 1, "status": status, "checks": [{"status": status}]}
            ],
        }
        return audit, Path("audit.md")


if __name__ == "__main__":
    unittest.main()
