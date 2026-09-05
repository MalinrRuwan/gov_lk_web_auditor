import re

from ..models.Evidence import Evidence
from .Level2PageParser import Level2PageParser


class Level2EvidenceCollector:
    ADDRESS = re.compile(r"\baddress\s*:?\s+(.{10,120})", re.I)
    LOCATION = re.compile(
        r"((?:[\w&'.,/-]+\s+){1,8}(?:colombo|kotte|kandy|galle)"
        r"\s*\d{0,2}\s*,?\s*sri lanka)",
        re.I,
    )
    RESPONSIBILITY = (
        "responsible officer",
        "officer in charge",
        "director",
        "division",
        "department",
    )
    PLACEHOLDERS = ("your-mail@", "your-awesome-website.com")

    def __init__(self):
        self.source = ""

    def collect(self, body: str, source: str) -> list[Evidence]:
        self.source = source
        parser = Level2PageParser().parse(body)
        evidence = [*self._contacts(parser)]
        evidence.extend(
            item
            for item in (
                self._address(parser),
                self._signal(
                    "named_responsibility", self.RESPONSIBILITY, parser.text
                ),
            )
            if item
        )
        return evidence

    def _contacts(self, parser: Level2PageParser) -> list[Evidence]:
        return [
            *[self._new("phone", "pass", value) for value in parser.phones],
            *[
                self._new("email", "pass", self._email(value))
                for value in parser.emails
                if not any(item in value for item in self.PLACEHOLDERS)
            ],
        ]

    def _address(self, parser: Level2PageParser) -> Evidence | None:
        value = " ".join(parser.address_parts)
        match = self.ADDRESS.search(parser.text)
        value = value or (match.group(1) if match else "")
        location = self.LOCATION.search(parser.text)
        value = value or (location.group(1) if location else "")
        if not value or "telephone number" in value.lower():
            return None
        return self._new("postal_address", "pass", value)

    def _signal(self, check: str, markers, text: str) -> Evidence | None:
        value = next(
            (marker for marker in markers if marker in text.lower()), ""
        )
        return self._new(check, "pass", value) if value else None

    def _email(self, value: str) -> str:
        return value.removeprefix("u003e")

    def _new(self, check: str, status: str, value: str) -> Evidence:
        detail = f"Published {check.replace('_', ' ')}: {value}"
        return Evidence(
            check, status, detail, self.source, data={"value": value}
        )
