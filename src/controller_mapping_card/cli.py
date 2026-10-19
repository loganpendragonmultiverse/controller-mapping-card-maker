from __future__ import annotations

import argparse
import io
import json
import os
import sys
from pathlib import Path

from .core import load_layout, render_html, render_markdown


def _write_stdout(rendered: str) -> None:
    """Avoid retaining report bytes in a buffer after a closed-pipe failure."""
    try:
        descriptor = sys.stdout.fileno()
    except (AttributeError, io.UnsupportedOperation):
        sys.stdout.write(rendered)
        sys.stdout.flush()
        return
    pending = memoryview(
        rendered.encode(sys.stdout.encoding or "utf-8", sys.stdout.errors or "strict")
    )
    while pending:
        count = os.write(descriptor, pending)
        if count <= 0:
            raise OSError("stdout accepted no report bytes")
        pending = pending[count:]


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
            if os.path.lexists(args.output):
                raise ValueError(f"output already exists: {args.output}")
            with args.output.open("x", encoding="utf-8", newline="\n") as output:
                output.write(rendered)
        else:
            _write_stdout(rendered)
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0
