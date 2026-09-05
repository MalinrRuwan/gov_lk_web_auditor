import unittest

from glwa.network.UrlNormalizer import UrlNormalizer


class TestUrlNormalizer(unittest.TestCase):
    def setUp(self):
        self.normalizer = UrlNormalizer()

    def test_adds_https_and_root_path(self):
        self.assertEqual(
            "https://example.gov.lk/",
            self.normalizer.normalize("example.gov.lk#fragment"),
        )

    def test_rejects_credentials(self):
        with self.assertRaises(ValueError):
            self.normalizer.normalize("https://user:secret@example.gov.lk")

    def test_generates_https_and_http_variants(self):
        variants = self.normalizer.variants("http://example.gov.lk/services")
        self.assertEqual("https://example.gov.lk/services", variants[0])
        self.assertEqual("http://example.gov.lk/services", variants[1])


if __name__ == "__main__":
    unittest.main()
