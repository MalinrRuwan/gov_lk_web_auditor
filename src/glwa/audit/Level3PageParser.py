from html.parser import HTMLParser
from urllib.parse import urljoin


class Level3PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.source = ""
        self.parts = []
        self.links = []
        self.href = ""
        self.anchor_parts = []

    def parse(self, body: str, source: str):
        self.__init__()
        self.source = source
        self.feed(body)
        return self

    @property
    def text(self) -> str:
        return " ".join(self.parts)

    def handle_starttag(self, tag: str, attrs):
        if tag == "a":
            self.href = dict(attrs).get("href", "")
            self.anchor_parts = []

    def handle_endtag(self, tag: str):
        if tag == "a" and self.href:
            text = " ".join(self.anchor_parts)
            self.links.append((urljoin(self.source, self.href), text))
            self.href = ""
            self.anchor_parts = []

    def handle_data(self, data: str):
        value = " ".join(data.split())
        if not value:
            return
        self.parts.append(value)
        if self.href:
            self.anchor_parts.append(value)
