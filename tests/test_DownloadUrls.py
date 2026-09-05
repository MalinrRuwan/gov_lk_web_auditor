import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from workflows.download_urls import DownloadUrls


class TestDownloadUrls(unittest.TestCase):
    @patch("workflows.download_urls.Directory")
    def test_writes_directory_urls_to_json(self, directory):
        directory.return_value.urls.return_value = ["one", "two"]
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "static_data" / "urls.json"
            self.assertEqual(target, DownloadUrls(target).run())
            self.assertEqual(
                ["one", "two"],
                json.loads(target.read_text(encoding="utf-8")),
            )


if __name__ == "__main__":
    unittest.main()
