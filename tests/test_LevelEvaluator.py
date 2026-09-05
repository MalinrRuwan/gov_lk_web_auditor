import unittest

from glwa.classification.LevelEvaluator import LevelEvaluator
from glwa.models.Evidence import Evidence


class TestLevelEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = LevelEvaluator()

    def test_failure_stops_all_higher_levels(self):
        evidence = [Evidence("dns_absent", "fail", "DNS absent")]
        levels = self.evaluator.evaluate(evidence)
        self.assertEqual("pass", levels[0].status)
        self.assertTrue(levels[0].executed)
        self.assertEqual("fail", levels[1].status)
        self.assertTrue(levels[1].executed)
        self.assertTrue(all(not item.executed for item in levels[2:]))
        self.assertTrue(
            all(item.status == "inconclusive" for item in levels[2:])
        )

    def test_healthy_site_passes_level_one(self):
        evidence = [
            Evidence("dns", "pass", "DNS resolved"),
            Evidence("domain_registration", "pass", "Domain registered"),
            Evidence("tls", "pass", "TLS valid"),
            Evidence("http", "pass", "HTTP available"),
        ]
        levels = self.evaluator.evaluate(evidence)
        self.assertEqual("pass", levels[0].status)
        self.assertEqual("pass", levels[1].status)
        self.assertEqual(list(range(6)), [item.level for item in levels])
        self.assertTrue(levels[1].description)
        self.assertEqual(10, len(levels[1].checks))

    def test_transient_level_one_is_inconclusive(self):
        evidence = [Evidence("http", "error", "Probe timed out")]
        levels = self.evaluator.evaluate(evidence)
        self.assertEqual("pass", levels[0].status)
        self.assertEqual("inconclusive", levels[1].status)
        self.assertFalse(levels[2].executed)
        self.assertEqual(
            "Not run because Level 1 did not pass", levels[2].reason
        )


if __name__ == "__main__":
    unittest.main()
