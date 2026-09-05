from datetime import datetime, timedelta
from urllib.parse import urlsplit

from ...models.Evidence import Evidence
from ...time.SriLankaTime import SriLankaTime
from ..Level3PageParser import Level3PageParser
from .Level3EvidencePatternsMixin import Level3EvidencePatternsMixin


class Level3EvidenceCollector(Level3EvidencePatternsMixin):
    DATE_FORMATS = (
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d %B %Y",
        "%d %b %Y",
    )

    def collect(self, body: str, source: str) -> list[Evidence]:
        parser = Level3PageParser().parse(body, source)
        evidence = [
            self._signal(check, markers, parser.text, source)
            for check, markers in self.SIGNALS.items()
        ]
        evidence.extend(
            [
                self._fees(parser.text, source),
                self._time(parser.text, source),
                self._form(parser.links, source),
                self._date(parser.text, source),
            ]
        )
        return [item for item in evidence if item]

    def _signal(self, check, markers, text, source):
        value = next((item for item in markers if item in text.lower()), "")
        return self._new(check, value, source) if value else None

    def _fees(self, text, source):
        lowered = text.lower()
        money = self.MONEY.search(text)
        free = self.FREE.search(text)
        payment = any(item in lowered for item in self.PAYMENT)
        value = free.group(0) if free else money.group(0) if money else ""
        if value and (free or payment):
            return self._new("fees_and_payment", value, source)
        return None

    def _time(self, text, source):
        duration = self.DURATION.search(text)
        marker = any(item in text.lower() for item in self.TIME)
        if duration and marker:
            return self._new("processing_time", duration.group(0), source)
        return None

    def _form(self, links, source):
        for url, label in links:
            path = urlsplit(url).path.lower()
            named = "form" in label.lower() or "application" in label.lower()
            if named and path.endswith(self.FORM_EXTENSIONS):
                return self._new("downloadable_form", url, source)
        return None

    def _date(self, text, source):
        date = self.DATE.search(text)
        marker = any(item in text.lower() for item in self.UPDATED)
        if date and marker:
            value = date.group(0)
            observed = self._parse_date(value)
            if not observed:
                return None
            current = SriLankaTime.now().date() - timedelta(days=730)
            status = "pass" if observed.date() >= current else "fail"
            return self._new("published_update_date", value, source, status)
        return None

    def _parse_date(self, value):
        for date_format in self.DATE_FORMATS:
            try:
                return datetime.strptime(value, date_format)
            except ValueError:
                continue
        return None

    def _new(self, check, value, source, status="pass"):
        detail = f"Published {check.replace('_', ' ')}: {value}"
        return Evidence(check, status, detail, source, data={"value": value})
