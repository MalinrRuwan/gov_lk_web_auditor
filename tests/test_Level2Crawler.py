import unittest
from types import SimpleNamespace

from glwa.audit.Level2Crawler import Level2Crawler


class Probe:
    def __init__(self):
        self.urls = []

    def probe(self, url):
        self.urls.append(url)
        return SimpleNamespace(body="contact", status_code=200, final_url=url)


class TestLevel2Crawler(unittest.TestCase):
    def test_crawls_same_site_level_two_links_once(self):
        probe = Probe()
        page = SimpleNamespace(
            final_url="https://www.example.gov.lk/",
            body=(
                '<a href="/contact#staff">Contact</a>'
                '<a href="https://example.gov.lk/services">Services</a>'
                '<a href="https://other.gov.lk/contact">Other</a>'
            ),
        )
        pages = Level2Crawler(probe).crawl([page, page])
        self.assertEqual(2, len(pages))
        self.assertEqual(
            [
                "https://www.example.gov.lk/contact",
                "https://example.gov.lk/services",
            ],
            probe.urls,
        )

    def test_follows_five_generic_language_page_links(self):
        probe = Probe()
        links = "".join(
            f'<a href="/page-{index}">Page</a>' for index in range(5)
        )
        page = SimpleNamespace(
            final_url="https://example.gov.lk/", body=links
        )
        pages = Level2Crawler(probe).crawl([page])
        self.assertEqual(5, len(pages))
        self.assertEqual(
            [f"https://example.gov.lk/page-{index}" for index in range(5)],
            probe.urls,
        )


if __name__ == "__main__":
    unittest.main()
