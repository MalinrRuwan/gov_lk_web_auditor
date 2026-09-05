class LevelSection:
    ACRONYMS = {"dns": "DNS", "http": "HTTP", "tls": "TLS"}

    def __init__(self, level, websites):
        self.level = level
        self.websites = websites

    def render(self) -> str:
        if not self.level.implemented:
            return ""
        lines = [
            f"## {self.level.markdown_label}",
            "",
            self._count(),
            "",
            self._checks(),
        ]
        if self.websites:
            lines.extend(
                ["", "| Score | URL |", "| ---: | --- |", *self.websites]
            )
        return "\n".join(lines)

    def _count(self) -> str:
        return (
            f"**{len(self.websites)} URLs at "
            f"{self.level.markdown_label}.**"
        )

    def _checks(self) -> str:
        if not self.level.checks:
            if self.level.number == 0:
                return "Checks used: Availability and usability checks."
            return "Checks used: ⚠️ Not implemented as yet."
        names = ", ".join(
            self._check_name(check) for check in self.level.checks
        )
        return f"Checks used: {names}."

    def _check_name(self, check) -> str:
        words = [
            self.ACRONYMS.get(word, word) for word in check.name.split("_")
        ]
        words[0] = words[0].capitalize() if words[0].islower() else words[0]
        return " ".join(words)
