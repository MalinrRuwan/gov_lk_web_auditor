from datetime import datetime
from zoneinfo import ZoneInfo


class SriLankaTime:
    ZONE = ZoneInfo("Asia/Colombo")

    @classmethod
    def now(cls) -> datetime:
        return datetime.now(cls.ZONE)

    @classmethod
    def parse(cls, value: str) -> datetime:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=cls.ZONE)
        return parsed.astimezone(cls.ZONE)

    @classmethod
    def normalize(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=cls.ZONE)
        return value.astimezone(cls.ZONE)

    @classmethod
    def iso(cls, value: datetime | str) -> str:
        if isinstance(value, str):
            return cls.parse(value).isoformat()
        return cls.normalize(value).isoformat()
