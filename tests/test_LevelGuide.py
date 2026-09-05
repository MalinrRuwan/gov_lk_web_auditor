import unittest

from glwa.classification.LevelEvaluator import LevelEvaluator
from glwa.reporting.LevelGuide import LevelGuide


class TestLevelGuide(unittest.TestCase):
    def test_explains_levels_and_scoring(self):
        content = LevelGuide().render(LevelEvaluator.LEVELS)
        self.assertIn("## Levels and scoring", content)
        self.assertIn("| Level | Implemented | Description |", content)
        self.assertIn("| `⚫ Level 0` | ✅ Yes |", content)
        self.assertIn("| `🟢 Level 3` | ✅ Yes |", content)
        self.assertIn("| `🟣 Level 5` | ❌ No |", content)
        self.assertIn("passing checks divided by total checks", content)
        self.assertIn("`⚫ Level 0` contributes no points", content)
        self.assertIn("The score is out of 3", content)
        self.assertIn("`🔴 Level 1` through `🟢 Level 3`", content)
        self.assertNotIn("To pass", content)


if __name__ == "__main__":
    unittest.main()
