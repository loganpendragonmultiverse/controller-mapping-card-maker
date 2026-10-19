from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


def load_layout(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("layout must be a version 1 object")
    for key in ("game", "platform", "controller"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f"layout requires {key}")
    if "contexts" in data:
        if "mappings" in data:
            raise ValueError("use contexts or legacy mappings, not both")
        contexts = data["contexts"]
        if not isinstance(contexts, list) or not contexts:
            raise ValueError("contexts must be a non-empty list")
        names = set()
        for context in contexts:
            if not isinstance(context, dict):
                raise TypeError("context must be an object")
            name = context.get("name")
            if not isinstance(name, str) or not name.strip() or name in names:
                raise ValueError("context names must be non-empty and unique")
            names.add(name)
            validate_mappings(context.get("mappings"))
    else:
        validate_mappings(data.get("mappings"))
    return data


def validate_mappings(mappings: Any) -> None:
    if not isinstance(mappings, list) or not mappings:
        raise ValueError("mappings must be a non-empty list")
    seen: set[str] = set()
    for item in mappings:
        if not isinstance(item, dict):
            raise TypeError("mapping must be an object")
        control, action = item.get("control"), item.get("action")
        if not isinstance(control, str) or not control.strip() or control in seen:
            raise ValueError("controls must be non-empty and unique within each context")
        if not isinstance(action, str) or not action.strip():
            raise ValueError(f"mapping {control} requires an action")
        seen.add(control)


def selected_mappings(data: dict[str, Any], print_context: str | None) -> list[dict[str, Any]]:
    if "contexts" not in data:
        if print_context is not None:
            raise ValueError("print context requires a named-context layout")
        return data["mappings"]
    contexts = data["contexts"]
    if print_context is not None and print_context not in {c["name"] for c in contexts}:
        raise ValueError("unknown print context")
    return [
        {**item, "context": context["name"]}
        for context in contexts
        if print_context is None or context["name"] == print_context
        for item in context["mappings"]
    ]


def render_markdown(data: dict[str, Any], print_context: str | None = None) -> str:
    lines = [
        f"# {html.escape(str(data['game']))} Controller Card",
        "",
        f"**{html.escape(str(data['platform']))} · {html.escape(str(data['controller']))}**",
        "",
        "| Control | Action | Context |",
        "|---|---|---|",
    ]
    for item in selected_mappings(data, print_context):
        values = [
            html.escape(str(item.get(key, ""))).replace("|", "\\|")
            for key in ("control", "action", "context")
        ]
        lines.append(f"| {values[0]} | {values[1]} | {values[2]} |")
    if data.get("notes"):
        lines.extend(["", "## Notes", "", html.escape(str(data["notes"]))])
    return "\n".join(lines).rstrip() + "\n"


def render_html(data: dict[str, Any], print_context: str | None = None) -> str:
    rows = "".join(
        f"<li><strong>{html.escape(str(item['control']))}</strong><span>{html.escape(str(item['action']))}</span>"
        f"<small>{html.escape(str(item.get('context', '')))}</small></li>"
        for item in selected_mappings(data, print_context)
    )
    notes = f"<p class=notes>{html.escape(str(data['notes']))}</p>" if data.get("notes") else ""
    title = html.escape(str(data["game"]))
    subtitle = html.escape(f"{data['platform']} · {data['controller']}")
    return f"""<!doctype html>
<html lang=en><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>{title} controller card</title><style>
:root{{font:16px system-ui;color:#16201c;background:#eef1ed}}body{{margin:0;padding:24px}}main{{max-width:760px;margin:auto;background:white;border:2px solid;padding:28px}}h1{{margin:0}}header p{{color:#52615a}}ul{{list-style:none;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:10px}}li{{break-inside:avoid;display:grid;grid-template-columns:90px minmax(0,1fr);overflow-wrap:anywhere;padding:12px;border:1px solid}}small{{grid-column:2;color:#52615a}}.notes{{border-top:1px solid;padding-top:16px}}@media(max-width:560px){{ul{{grid-template-columns:1fr}}}}@media print{{body{{padding:0;background:white}}main{{border:0}}}}
</style><main><header><h1>{title}</h1><p>{subtitle}</p></header><ul>{rows}</ul>{notes}</main></html>\n"""
