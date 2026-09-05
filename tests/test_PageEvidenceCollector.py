import unittest

from glwa.audit.PageEvidenceCollector import PageEvidenceCollector
from glwa.models.HttpObservation import HttpObservation


class TestPageEvidenceCollector(unittest.TestCase):
    def test_collects_page_evidence_from_http_body(self):
        body = """
        <address>123 Parliament Road, Colombo 01</address>
        <a href="tel:+94 11 234 5678">Call</a>
        <a href="mailto:help@example.gov.lk">Email</a>
        <h2>Eligibility</h2>
        """
        item = HttpObservation(
            "https://example.gov.lk/",
            200,
            "https://example.gov.lk/",
            [],
            10,
            "text/html",
            body,
            None,
        )
        evidence = PageEvidenceCollector().collect([item], item.url)
        checks = {item.check for item in evidence}
        self.assertTrue({"postal_address", "phone", "email"} <= checks)
        self.assertIn("eligibility_criteria", checks)


if __name__ == "__main__":
    unittest.main()
