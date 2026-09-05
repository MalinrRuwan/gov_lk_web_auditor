import json
from pathlib import Path

from glwa import Directory


class DownloadUrls:
    def __init__(self, target=Path("static_data/urls.json")):
        self.target = target

    def run(self):
        urls = Directory().urls()
        content = json.dumps(urls, indent=2) + "\n"
        self.target.parent.mkdir(parents=True, exist_ok=True)
        self.target.write_text(content, encoding="utf-8")
        print(f"Wrote {len(urls)} URLs to {self.target}")
        return self.target


if __name__ == "__main__":
    DownloadUrls().run()
