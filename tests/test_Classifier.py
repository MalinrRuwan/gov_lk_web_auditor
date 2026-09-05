import unittest

from glwa import Classifier, Evidence
from glwa.levels.Level1 import Level1


class TestClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = Classifier(Level1())

    def test_authoritative_dns_absence_fails_level_one(self):
        evidence = [Evidence("dns_absent", "fail", "DNS name does not exist")]
        result = self.classifier.classify(evidence)
        self.assertEqual("fail", result.status)

    def test_parked_content_fails_level_one(self):
        evidence = [Evidence("parked", "fail", "Parking template detected")]
        result = self.classifier.classify(evidence)
        self.assertEqual("fail", result.status)

    def test_expired_certificate_keeps_site_at_level_one(self):
        evidence = [Evidence("tls_expired", "fail", "Certificate expired")]
        result = self.classifier.classify(evidence)
        self.assertEqual("pass", result.status)

    def test_timeout_remains_inconclusive(self):
        evidence = [Evidence("https", "error", "Probe timed out")]
        result = self.classifier.classify(evidence)
        self.assertEqual("inconclusive", result.status)

    def test_healthy_site_passes_level_one(self):
        evidence = [
            Evidence("dns", "pass", "Public DNS resolved"),
            Evidence("domain_registration", "pass", "Domain registered"),
            Evidence("tls", "pass", "TLS certificate valid"),
            Evidence("http", "pass", "HTTPS returned 200"),
        ]
        result = self.classifier.classify(evidence)
        self.assertEqual("pass", result.status)


if __name__ == "__main__":
    unittest.main()
