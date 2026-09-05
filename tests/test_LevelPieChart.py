import unittest

from glwa.classification.LevelEvaluator import LevelEvaluator
from glwa.reporting.LevelPieChart import LevelPieChart


class TestLevelPieChart(unittest.TestCase):
    def test_renders_level_colors_and_counts(self):
        levels = LevelEvaluator.LEVELS
        groups = {level.number: [] for level in levels}
        groups[0] = ["one", "two"]
        groups[1] = ["three"]
        chart = LevelPieChart().render(levels, groups)
        self.assertEqual(
            ["black", "red", "orange", "green", "blue", "purple"],
            [level.color for level in levels],
        )
        self.assertEqual(
            ["⚫", "🔴", "🟠", "🟢", "🔵", "🟣"],
            [level.emoji for level in levels],
        )
        self.assertEqual(
            [
                "⚫ Level 0",
                "🔴 Level 1",
                "🟠 Level 2",
                "🟢 Level 3",
                "🔵 Level 4",
                "🟣 Level 5",
            ],
            [level.label for level in levels],
        )
        self.assertEqual("`🟠 Level 2`", levels[2].markdown_label)
        self.assertIn('"pie1":"black"', chart)
        self.assertIn('"pie2":"red"', chart)
        self.assertIn('"pie3":"orange"', chart)
        self.assertIn('"⚫ Level 0" : 2', chart)
        self.assertIn('"🔴 Level 1" : 1', chart)
        self.assertIn('"🟠 Level 2" : 0', chart)


if __name__ == "__main__":
    unittest.main()
