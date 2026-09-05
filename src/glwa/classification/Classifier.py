from ..levels.Level import Level
from ..models.Classification import Classification
from ..models.Evidence import Evidence


class Classifier:
    def __init__(self, level: Level):
        self.level = level

    def classify(self, evidence: list[Evidence]) -> Classification:
        result = self.level.run(evidence)
        confidence = 0.5 if result.status == "inconclusive" else 1.0
        reasons = [
            f"{item.name}: {item.reason}"
            for item in result.checks
            if item.status == result.status
        ]
        return Classification(result.status, confidence, reasons)
