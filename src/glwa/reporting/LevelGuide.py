from .WebsiteScore import WebsiteScore


class LevelGuide:
    def render(self, levels) -> str:
        rows = "\n".join(
            f"| {level.markdown_label} | "
            f"{'✅ Yes' if level.implemented else '❌ No'} | "
            f"{self._description(level, levels)} |"
            for level in levels
        )
        table = (
            "| Level | Implemented | Description |\n"
            "| --- | :---: | --- |\n"
            f"{rows}"
        )
        implemented = [
            level for level in levels if level.number and level.implemented
        ]
        maximum = WebsiteScore().maximum
        scoring = (
            f"The score is out of {maximum}. "
            f"{implemented[0].markdown_label} through "
            f"{implemented[-1].markdown_label} each contribute up to 1 point, "
            "calculated as passing checks divided by total checks. "
            f"{levels[0].markdown_label} contributes no points. The total is "
            "shown to one decimal place."
        )
        return f"## Levels and scoring\n\n{table}\n\n{scoring}"

    def _description(self, level, levels) -> str:
        prefix = f"To pass `Level {level.number}`, "
        description = level.description
        if description.startswith(prefix):
            description = description.removeprefix(prefix)
        for reference in levels:
            name = f"`Level {reference.number}`"
            description = description.replace(name, reference.markdown_label)
        return description[0].upper() + description[1:]
