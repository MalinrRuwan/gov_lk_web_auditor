from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin, urlsplit


class Level2LinkParser(HTMLParser):
    TERMS = ("contact", "service", "department", "division", "office")

    def __init__(self):
        super().__init__()
        self.source = ""
        self.host = ""
        self.links = []

    def parse(self, body: str, source: str) -> list[str]:
        self.__init__()
        self.source = source
        self.host = self._host(source)
        self.feed(body)
        links = list(dict.fromkeys(self.links))
        return sorted(links, key=self._priority)

    def handle_starttag(self, tag: str, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if not href:
            return
        url = urldefrag(urljoin(self.source, href)).url
        parsed = urlsplit(url)
        if (
            parsed.scheme in {"http", "https"}
            and self._host(url) == self.host
            and url != self.source
        ):
            self.links.append(url)

    def _priority(self, url: str):
        path = urlsplit(url).path.lower()
        relevant = any(term in path for term in self.TERMS)
        return not relevant

    def _host(self, url: str) -> str:
        return (urlsplit(url).hostname or "").removeprefix("www.")
