from .Level2LinkParser import Level2LinkParser


class Level2Crawler:
    LIMIT = 10

    def __init__(self, probe):
        self.probe = probe

    def crawl(self, items):
        seen = {item.final_url for item in items if item.final_url}
        links = self._links(items)
        pages = []
        while links and len(pages) < self.LIMIT:
            link = links.pop(0)
            if link in seen:
                continue
            seen.add(link)
            page = self.probe.probe(link)
            if not self._usable(page):
                continue
            pages.append(page)
            links.extend(self._links([page]))
        return pages

    def _links(self, items):
        return list(
            dict.fromkeys(
                link
                for item in items
                if item.body and item.final_url
                for link in Level2LinkParser().parse(
                    item.body, item.final_url
                )
            )
        )

    def _usable(self, page):
        return page.body and page.status_code == 200
