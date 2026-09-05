import unittest

from glwa.levels.Level3 import Level3
from glwa.models.Evidence import Evidence


class TestLevel3(unittest.TestCase):
    CHECKS = (
        "eligibility_criteria",
        "required_documents",
        "fees_and_payment",
        "legal_basis",
        "processing_time",
        "downloadable_form",
        "published_update_date",
    )

    def test_passes_complete_published_guidance(self):
        evidence = [
            Evidence(name, "pass", f"Published {name}")
            for name in self.CHECKS
        ]
        result = Level3().run(evidence)
        self.assertEqual("pass", result.status)
        self.assertEqual(7, len(result.checks))

    def test_is_inconclusive_when_guidance_is_missing(self):
        result = Level3().run([])
        self.assertEqual("inconclusive", result.status)


if __name__ == "__main__":
    unittest.main()
