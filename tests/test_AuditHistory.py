import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from glwa.audit.AuditHistory import AuditHistory


class TestAuditHistory(unittest.TestCase):
    def test_creates_timestamped_host_folder(self):
        now = datetime(2026, 9, 1, 10, 30, tzinfo=timezone.utc)
        history = AuditHistory(Path("audit.output"))
        folder = history.folder("https://example.gov.lk/path", now)
        expected = Path("audit.output/example.gov.lk/20260901.1600")
        self.assertEqual(expected, folder)

    def test_skips_only_audits_from_last_twenty_four_hours(self):
        now = datetime(2026, 9, 1, 10, 30, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as folder:
            history = AuditHistory(Path(folder))
            self._write(history, now - timedelta(hours=23))
            self.assertTrue(history.fresh("https://example.gov.lk", now))
            self.assertFalse(
                history.fresh("https://example.gov.lk/services", now)
            )
            self._write(history, now - timedelta(hours=25))
            recent = now + timedelta(hours=25)
            self.assertFalse(history.fresh("https://example.gov.lk", recent))

    def _write(self, history: AuditHistory, completed: datetime):
        folder = history.folder("https://example.gov.lk", completed)
        folder.mkdir(parents=True, exist_ok=True)
        audit = {
            "normalized_url": "https://example.gov.lk/",
            "completed_at": completed.isoformat(),
        }
        (folder / "audit.json").write_text(json.dumps(audit), "utf-8")


if __name__ == "__main__":
    unittest.main()
