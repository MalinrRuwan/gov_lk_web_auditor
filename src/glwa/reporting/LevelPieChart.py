import json


class LevelPieChart:
    def render(self, levels, groups) -> str:
        levels = [level for level in levels if level.implemented]
        colors = {
            f"pie{index}": level.color
            for index, level in enumerate(levels, start=1)
        }
        theme = json.dumps({"themeVariables": colors}, separators=(",", ":"))
        slices = "\n".join(
            f'    "{level.label}" : {len(groups[level.number])}'
            for level in levels
        )
        return (
            "## Sites by level\n\n"
            "```mermaid\n"
            f"%%{{init: {theme}}}%%\n"
            "pie showData\n"
            "    title Sites by level\n"
            f"{slices}\n"
            "```"
        )
