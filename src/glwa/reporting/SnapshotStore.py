import hashlib
from pathlib import Path
from typing import Any

from ..models.HttpObservation import HttpObservation


class SnapshotStore:
    def save(
        self, observation: HttpObservation, folder: Path, index: int
    ) -> dict[str, Any]:
        folder.mkdir(parents=True, exist_ok=True)
        body = observation.body.encode("utf-8")
        digest = hashlib.sha256(body).hexdigest()
        path = folder / f"page-{index:02d}-{digest[:12]}.html"
        path.write_bytes(body)
        return {
            "url": observation.final_url,
            "path": str(path),
            "sha256": digest,
            "bytes": len(body),
        }
