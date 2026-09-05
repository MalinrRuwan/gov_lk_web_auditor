import csv
from pathlib import Path

from ..audit.Audit import Audit


class LevelsCsvReport:
    FIELDS = ["level", "description", "status", "reason", "executed"]

    def write(self, audit: Audit, output: Path) -> Path:
        path = output / "levels.csv"
        with path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.FIELDS)
            writer.writeheader()
            writer.writerows(
                {key: item.to_dict()[key] for key in self.FIELDS}
                for item in audit.levels
            )
        return path
