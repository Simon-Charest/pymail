from io import TextIOWrapper
from pathlib import Path
from typing import Any


def generate_timeline(
    items: list[dict[str, Any]],
    timeline_script_file: Path,
    timeline_style_file: Path,
    timeline_template_file: Path,
    output_file: Path,
    encoding: str = "utf-8"
) -> None:
    """Generates an HTML file containing a self-contained vis.js timeline."""

    # Read template
    stream: TextIOWrapper = open(timeline_template_file)
    content: str = stream.read()
    stream.close()

    # Add content
    content = content.replace("%TIMELINE_SCRIPT_FILE%", timeline_script_file)
    content = content.replace("%TIMELINE_STYLE_FILE%", timeline_style_file)
    content = content.replace("%ITEMS%", str(items).replace("'", '"'))

    # Write timeline
    stream: TextIOWrapper = open(output_file, "w", encoding=encoding)
    stream.write(content)
    stream.close()
