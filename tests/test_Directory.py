import json
import tempfile
import unittest
from pathlib import Path

from glwa import Directory


class TestDirectory(unittest.TestCase):
    def test_returns_unique_urls_in_json_order(self):
        websites = {
            "Category 1": {
                "Category 2": {
                    "One": "https://one.gov.lk",
                    "Two": "https://two.gov.lk",
                },
                "Other": {"Duplicate": "https://one.gov.lk"},
            }
        }
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "websites.json"
            source.write_text(json.dumps(websites), encoding="utf-8")
            self.assertEqual(
                ["https://one.gov.lk", "https://two.gov.lk"],
                Directory(source).urls(),
            )


if __name__ == "__main__":
    unittest.main()
