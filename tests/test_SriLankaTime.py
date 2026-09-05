import unittest
from datetime import datetime, timezone

from glwa.time.SriLankaTime import SriLankaTime


class TestSriLankaTime(unittest.TestCase):
    def test_converts_utc_to_sri_lanka_time(self):
        value = SriLankaTime.parse("2026-09-01T10:00:00+00:00")
        self.assertEqual("2026-09-01T15:30:00+05:30", value.isoformat())

    def test_serializes_datetime_in_sri_lanka_time(self):
        value = datetime(2026, 9, 1, 10, 0, tzinfo=timezone.utc)
        self.assertEqual("2026-09-01T15:30:00+05:30", SriLankaTime.iso(value))


if __name__ == "__main__":
    unittest.main()
