import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from .Audit import Audit


class AuditValidator:
    def validate(self, audit: Audit):
        name = f"audit-{audit.schema_version}.json"
        path = Path(__file__).parent / "schemas" / name
        schema = json.loads(path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(
            schema, format_checker=FormatChecker()
        )
        validator.validate(audit.to_dict())
