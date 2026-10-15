from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import load_layout, render_html, render_markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a controller mapping refresher card.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--format", choices=("html", "markdown"), default="html")
    parser.add_argument("--print-context", help="Include only this named context in the card")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        data = load_layout(args.input)
        rendered = (
            render_html(data, args.print_context)
            if args.format == "html"
            else render_markdown(data, args.print_context)
        )
        if args.output:
            if args.output.exists():
                raise ValueError(f"output already exists: {args.output}")
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0
