from ..levels import Level0, Level1, Level2, Level3, Level4, Level5
from ..models.Evidence import Evidence
from ..models.LevelResult import LevelResult


class LevelEvaluator:
    LEVELS = (Level0(), Level1(), Level2(), Level3(), Level4(), Level5())

    def evaluate(self, evidence: list[Evidence]) -> list[LevelResult]:
        results = []
        blocked_by = None
        for level in self.LEVELS:
            result = level.run(evidence, blocked_by)
            results.append(result)
            if result.status != "pass":
                blocked_by = result.level
        return results
