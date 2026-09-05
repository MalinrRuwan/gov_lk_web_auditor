from ...models.CheckResult import CheckResult
from ...models.Evidence import Evidence
from ..Check import Check


class ReachableContactsCheck(Check):
    EVIDENCE_NAMES = ("phone", "email")

    def __init__(self):
        super().__init__("reachable_contacts", 2)

    def run(self, evidence: list[Evidence]) -> CheckResult:
        items = {
            name: [item for item in evidence if item.check == name]
            for name in self.EVIDENCE_NAMES
        }
        missing = [name for name, found in items.items() if not found]
        if missing:
            outcome = (
                "inconclusive",
                f"No {' or '.join(missing)} evidence found",
            )
        else:
            outcome = self._complete(items)
        return self.result(*outcome)

    def _complete(self, items) -> tuple[str, str]:
        if any(
            item.status == "fail"
            for found in items.values()
            for item in found
        ):
            return "fail", "A contact route was confirmed broken"
        if all(
            any(item.status == "pass" for item in found)
            for found in items.values()
        ):
            return "pass", self._published(items)
        return "inconclusive", "No passing phone and email evidence found"

    def _published(self, items) -> str:
        contacts = []
        for name in self.EVIDENCE_NAMES:
            values = [
                self._value(item).strip()
                for item in items[name]
                if item.status == "pass"
            ]
            unique = list(dict.fromkeys(values))
            contacts.append(self._contact(name, unique))
        return "; ".join(contacts)

    def _contact(self, name: str, values: list[str]) -> str:
        label = name.capitalize()
        if len(values) == 1:
            return f"{label}: {values[0]}"
        units = "phone numbers" if name == "phone" else "email addresses"
        return f"{label}: {values[0]} ({len(values)} {units} found)"

    def _value(self, item: Evidence) -> str:
        if item.data and item.data.get("value"):
            return str(item.data["value"])
        return item.detail
