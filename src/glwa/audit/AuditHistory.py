import json
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlsplit

from ..network.UrlNormalizer import UrlNormalizer
from ..time.SriLankaTime import SriLankaTime
from .Audit import Audit
from .AuditValidator import AuditValidator


class AuditHistory:
    def __init__(self, root: Path = Path("audit.output")):
        self.root = root
        self.normalizer = UrlNormalizer()

    def host(self, url: str) -> str:
        return urlsplit(url).hostname or "unknown"

    def folder(self, url: str, now: datetime | None = None) -> Path:
        current = SriLankaTime.normalize(now) if now else SriLankaTime.now()
        timestamp = current.strftime("%Y%m%d.%H%M")
        return self.root / self.host(url) / timestamp

    def fresh(self, url: str, now: datetime | None = None) -> bool:
        latest = self.latest(url)
        if not latest:
            return False
        current = SriLankaTime.normalize(now) if now else SriLankaTime.now()
        completed = SriLankaTime.parse(latest["completed_at"])
        return current - completed < timedelta(hours=24)

    def latest(self, url: str) -> dict | None:
        audits = []
        normalized = self.normalizer.normalize(url)
        folder = self.root / self.host(url)
        for path in folder.glob("*/audit.json"):
            audit = json.loads(path.read_text(encoding="utf-8"))
            if audit.get("normalized_url") == normalized:
                audits.append(audit)
        if not audits:
            return None
        return max(
            audits,
            key=lambda audit: SriLankaTime.parse(audit["completed_at"]),
        )

    def write(self, audit: Audit, output: Path) -> Path:
        output.mkdir(parents=True, exist_ok=True)
        AuditValidator().validate(audit)
        path = output / "audit.json"
        content = json.dumps(audit.to_dict(), indent=2, ensure_ascii=False)
        path.write_text(content + "\n", encoding="utf-8")
        return path
