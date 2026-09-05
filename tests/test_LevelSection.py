import unittest

from glwa.levels.Level1 import Level1
from glwa.levels.Level4 import Level4
from glwa.reporting.LevelSection import LevelSection


class TestLevelSection(unittest.TestCase):
    def test_describes_levels_with_positive_checks(self):
        websites = ["| 1.0/3 | one |", "| 2.0/3 | two |"]
        content = LevelSection(Level1(), websites).render()
        self.assertIn("## `🔴 Level 1`", content)
        self.assertIn("**2 URLs at `🔴 Level 1`.**", content)
        self.assertIn("Checks used: DNS resolves", content)
        self.assertIn("| Score | URL |", content)
        self.assertIn("| 1.0/3 | one |", content)
        self.assertNotIn("To pass", content)

    def test_describes_unimplemented_level_with_notice(self):
        content = LevelSection(Level4(), []).render()
        self.assertEqual("", content)


if __name__ == "__main__":
    unittest.main()
