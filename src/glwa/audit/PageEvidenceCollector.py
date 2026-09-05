from ..classification.ContentDetector import ContentDetector
from .EvidenceBuilder import EvidenceBuilder
from .Level2EvidenceCollector import Level2EvidenceCollector
from .Level3EvidenceCollector import Level3EvidenceCollector


class PageEvidenceCollector:
    def __init__(self):
        self.detector = ContentDetector()
        self.builder = EvidenceBuilder()
        self.level2 = Level2EvidenceCollector()
        self.level3 = Level3EvidenceCollector()

    def collect(self, items, original):
        evidence = []
        for item in items:
            if not item.body or not item.final_url:
                continue
            evidence.extend(self.detector.detect(item.body, item.final_url))
            evidence.extend(self.level2.collect(item.body, item.final_url))
            evidence.extend(self.level3.collect(item.body, item.final_url))
            redirect = self.builder.redirect(original, item.final_url)
            if redirect:
                evidence.append(redirect)
        return evidence
