import unittest

from glwa.audit.AuditReclassifier import AuditReclassifier


class TestAuditReclassifier(unittest.TestCase):
    def test_moves_stored_availability_failure_to_level_one(self):
        data = self._data()
        data["evidence"] = [
            {
                "check": "dns_absent",
                "status": "fail",
                "detail": "DNS name does not exist",
                "observed_at": "2026-09-01T10:00:30+00:00",
            }
        ]
        audit = AuditReclassifier().reclassify(data)
        self.assertEqual(
            ["pass", "fail"], [item.status for item in audit.levels[:2]]
        )
        self.assertEqual("2026-09-01T15:30:00+05:30", audit.started_at)
        self.assertEqual(
            "2026-09-01T15:30:30+05:30", audit.evidence[0].observed_at
        )

    def _data(self):
        return {
            "schema_version": "1.2.0",
            "audit_id": "audit-id",
            "url": "https://example.gov.lk",
            "normalized_url": "https://example.gov.lk/",
            "started_at": "2026-09-01T10:00:00+00:00",
            "completed_at": "2026-09-01T10:01:00+00:00",
            "result": {"status": "fail", "confidence": 1.0},
            "evidence": [],
            "observations": [],
            "snapshots": [],
            "reviewer_decisions": [],
            "levels": [],
        }


if __name__ == "__main__":
    unittest.main()
