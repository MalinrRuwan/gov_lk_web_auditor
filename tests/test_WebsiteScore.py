import unittest

from glwa.reporting.WebsiteScore import WebsiteScore


class TestWebsiteScore(unittest.TestCase):
    def test_sums_level_check_scores_to_one_decimal(self):
        audit = {
            "levels": [
                self._level(0, []),
                self._level(1, ["pass", "pass", "fail", "fail"]),
                self._level(2, ["pass", "fail", "fail", "fail"]),
            ]
        }
        self.assertEqual(0.8, WebsiteScore().calculate(audit))

    def test_level_zero_has_no_score(self):
        audit = {"levels": [self._level(0, ["pass"])]}
        self.assertEqual(0.0, WebsiteScore().calculate(audit))

    def test_ignores_unimplemented_levels(self):
        audit = {"levels": [{"level": 5, "status": "pass", "checks": []}]}
        self.assertEqual(0.0, WebsiteScore().calculate(audit))

    def test_maximum_is_number_of_implemented_levels(self):
        self.assertEqual(3, WebsiteScore().maximum)

    def _level(self, number, statuses):
        return {
            "level": number,
            "status": "inconclusive",
            "checks": [{"status": status} for status in statuses],
        }


if __name__ == "__main__":
    unittest.main()
