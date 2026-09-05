from urllib.parse import urlsplit, urlunsplit


class UrlNormalizer:
    def normalize(self, value: str) -> str:
        candidate = value.strip()
        if "://" not in candidate:
            candidate = f"https://{candidate}"
        parsed = urlsplit(candidate)
        if parsed.scheme.lower() not in {"http", "https"}:
            raise ValueError("Only HTTP and HTTPS URLs are supported")
        if not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("URL must contain a host and no credentials")
        host = parsed.hostname.encode("idna").decode("ascii").lower()
        port = f":{parsed.port}" if parsed.port else ""
        path = parsed.path or "/"
        return urlunsplit(
            (parsed.scheme.lower(), f"{host}{port}", path, parsed.query, "")
        )

    def variants(self, value: str) -> list[str]:
        parsed = urlsplit(self.normalize(value))
        return [
            urlunsplit((scheme, parsed.netloc, parsed.path, parsed.query, ""))
            for scheme in ("https", "http")
        ]
