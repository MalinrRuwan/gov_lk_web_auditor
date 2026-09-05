import unittest

from glwa.audit.Level2EvidenceCollector import Level2EvidenceCollector


class TestLevel2EvidenceCollector(unittest.TestCase):
    def test_extracts_published_level_two_evidence(self):
        body = """
        <address>123 Parliament Road, Colombo 01</address>
        <a href="tel:+94 11 234 5678">Call us</a>
        <a href="mailto:help@example.gov.lk">Email us</a>
        <p>Responsible Officer: Director, Citizen Services Division</p>
        """
        evidence = Level2EvidenceCollector().collect(
            body, "https://example.gov.lk/contact"
        )
        by_check = {item.check: item for item in evidence}
        expected = {
            "postal_address",
            "phone",
            "email",
            "named_responsibility",
        }
        self.assertEqual(expected, set(by_check))
        self.assertTrue(all(item.status == "pass" for item in evidence))

    def test_extracts_treasury_contact_details(self):
        body = (
            "<p>Ministry of Finance</p><p>The Secretariat</p>"
            "<p>Colombo 01, Sri Lanka.</p>"
            "<p>Phone : +94 112 484 500</p>"
            "<p>Email : info@mo.treasury.gov.lk</p>"
        )
        evidence = Level2EvidenceCollector().collect(
            body, "https://www.treasury.gov.lk/contact-us"
        )
        by_check = {item.check: item for item in evidence}
        self.assertEqual("pass", by_check["postal_address"].status)
        self.assertEqual("pass", by_check["phone"].status)
        self.assertEqual("pass", by_check["email"].status)

    def test_ignores_pages_without_level_two_signals(self):
        evidence = Level2EvidenceCollector().collect(
            "<h1>Welcome</h1>", "https://example.gov.lk/"
        )
        self.assertEqual([], evidence)


if __name__ == "__main__":
    unittest.main()
