import re
from html.parser import HTMLParser
from urllib.parse import unquote


class Level2PageParser(HTMLParser):
    EMAIL = re.compile(r"[\w.+-]+@[\w.-]+\.[a-z]{2,}", re.I)
    PHONE = re.compile(r"(?:\+94|0)[\s().-]*(?:\d[\s().-]*){9}")

    def __init__(self):
        super().__init__()
        self.parts = []
        self.address_depth = 0
        self.address_parts = []
        self.emails = set()
        self.phones = set()

    def parse(self, body: str):
        self.__init__()
        self.feed(body)
        self.emails.update(self.EMAIL.findall(self.text))
        self.phones.update(self.PHONE.findall(self.text))
        return self

    @property
    def text(self) -> str:
        return " ".join(self.parts)

    def handle_starttag(self, tag: str, attrs):
        if self.address_depth:
            self.address_depth += 1
        elif tag == "address":
            self.address_depth = 1
        href = dict(attrs).get("href", "")
        if href.startswith("mailto:"):
            self.emails.add(unquote(href[7:].split("?", 1)[0]).strip())
        elif href.startswith("tel:"):
            self.phones.add(unquote(href[4:]).strip())

    def handle_endtag(self, tag: str):
        if self.address_depth:
            self.address_depth -= 1

    def handle_data(self, data: str):
        value = " ".join(data.split())
        if value:
            self.parts.append(value)
            if self.address_depth:
                self.address_parts.append(value)
