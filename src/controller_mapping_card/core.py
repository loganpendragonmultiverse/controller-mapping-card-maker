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
    mappings = data.get("mappings")
    if not isinstance(mappings, list) or not mappings:
        raise ValueError("mappings must be a non-empty list")
    seen: set[str] = set()
    for item in mappings:
        if not isinstance(item, dict):
            raise TypeError("mapping must be an object")
        control = item.get("control")
        action = item.get("action")
        if not isinstance(control, str) or not control.strip() or control in seen:
            raise ValueError("controls must be non-empty and unique")
        if not isinstance(action, str) or not action.strip():
            raise ValueError(f"mapping {control} requires an action")
        seen.add(control)
    return data


def render_markdown(data: dict[str, Any]) -> str:
    lines = [
        f"# {data['game']} Controller Card",
        "",
        f"**{data['platform']} · {data['controller']}**",
        "",
        "| Control | Action | Context |",
        "|---|---|---|",
    ]
    for item in data["mappings"]:
        values = [
            str(item.get(key, "")).replace("|", "\\|") for key in ("control", "action", "context")
        ]
        lines.append(f"| {values[0]} | {values[1]} | {values[2]} |")
    if data.get("notes"):
        lines.extend(["", "## Notes", "", str(data["notes"])])
    return "\n".join(lines).rstrip() + "\n"


def render_html(data: dict[str, Any]) -> str:
    rows = "".join(
        f"<li><strong>{html.escape(str(item['control']))}</strong><span>{html.escape(str(item['action']))}</span>"
        f"<small>{html.escape(str(item.get('context', '')))}</small></li>"
        for item in data["mappings"]
    )
    notes = f"<p class=notes>{html.escape(str(data['notes']))}</p>" if data.get("notes") else ""
    title = html.escape(str(data["game"]))
    subtitle = html.escape(f"{data['platform']} · {data['controller']}")
    return f"""<!doctype html>
<html lang=en><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>{title} controller card</title><style>
:root{{font:16px system-ui;color:#16201c;background:#eef1ed}}body{{margin:0;padding:24px}}main{{max-width:760px;margin:auto;background:white;border:2px solid;padding:28px}}h1{{margin:0}}header p{{color:#52615a}}ul{{list-style:none;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:10px}}li{{display:grid;grid-template-columns:90px 1fr;padding:12px;border:1px solid}}small{{grid-column:2;color:#52615a}}.notes{{border-top:1px solid;padding-top:16px}}@media(max-width:560px){{ul{{grid-template-columns:1fr}}}}@media print{{body{{padding:0;background:white}}main{{border:0}}}}
</style><main><header><h1>{title}</h1><p>{subtitle}</p></header><ul>{rows}</ul>{notes}</main></html>\n"""
