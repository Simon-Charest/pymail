from io import TextIOWrapper
from pathlib import Path
from typing import Any


def generate_graph(
    items: list[dict[str, Any]],
    timeline_script_file: str,
    timeline_style_file: str,
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
    content = content.replace("%ITEMS%", str(items))

    # Write timeline
    stream: TextIOWrapper = open(output_file, "w", encoding=encoding)
    stream.write(content)
    stream.close()
