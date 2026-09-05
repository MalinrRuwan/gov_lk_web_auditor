import unittest
from datetime import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

from glwa.audit.Level3EvidenceCollector import Level3EvidenceCollector


class TestLevel3EvidenceCollector(unittest.TestCase):
    def test_extracts_published_service_guidance(self):
        body = """
        <h2>Eligibility</h2><p>Citizens over 18 may apply.</p>
        <h2>Required documents</h2><p>Attach a certified ID copy.</p>
        <p>Fee: LKR 1,000 payable online.</p>
        <p>Legal basis: Services Act No. 1.</p>
        <p>Processing time: within 5 working days.</p>
        <a href="/forms/application.pdf">Application form</a>
        <p>Last updated: 2026-08-31</p>
        """
        evidence = Level3EvidenceCollector().collect(
            body, "https://example.gov.lk/services/licence"
        )
        self.assertEqual(
            {
                "eligibility_criteria",
                "required_documents",
                "fees_and_payment",
                "legal_basis",
                "processing_time",
                "downloadable_form",
                "published_update_date",
            },
            {item.check for item in evidence},
        )
        self.assertTrue(all(item.status == "pass" for item in evidence))

    def test_ignores_pages_without_service_guidance(self):
        evidence = Level3EvidenceCollector().collect(
            "<h1>Welcome</h1>", "https://example.gov.lk/"
        )
        self.assertEqual([], evidence)

    @patch(
        "glwa.audit.Level3EvidenceCollector."
        "Level3EvidenceCollector.SriLankaTime.now"
    )
    def test_fails_stale_update_date(self, now):
        now.return_value = datetime(
            2026, 9, 1, tzinfo=ZoneInfo("Asia/Colombo")
        )
        evidence = Level3EvidenceCollector().collect(
            "<p>Last updated: 2019-01-01</p>",
            "https://example.gov.lk/service",
        )
        self.assertEqual("fail", evidence[0].status)

    def test_ignores_invalid_update_date(self):
        evidence = Level3EvidenceCollector().collect(
            "<p>Last updated: 31 Foo 2026</p>",
            "https://example.gov.lk/service",
        )
        self.assertEqual([], evidence)


if __name__ == "__main__":
    unittest.main()
