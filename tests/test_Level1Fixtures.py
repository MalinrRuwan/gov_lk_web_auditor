import json
import unittest
from pathlib import Path

from glwa import Classifier, Evidence
from glwa.levels.Level1 import Level1


class TestLevel1Fixtures(unittest.TestCase):
    def test_all_failure_modes_have_stable_results(self):
        path = Path(__file__).parent / "fixtures" / "level1_cases.json"
        cases = json.loads(path.read_text(encoding="utf-8"))
        classifier = Classifier(Level1())
        for case in cases:
            with self.subTest(case=case["name"]):
                evidence = [Evidence(*item) for item in case["evidence"]]
                result = classifier.classify(evidence)
                self.assertEqual(case["expected"], result.status)


if __name__ == "__main__":
    unittest.main()
