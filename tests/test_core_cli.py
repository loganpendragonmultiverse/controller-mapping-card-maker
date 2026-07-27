import json

import pytest

from controller_mapping_card.cli import main
from controller_mapping_card.core import load_layout, render_html, render_markdown


def layout():
    return {
        "version": 1,
        "game": "Sky Road",
        "platform": "PC",
        "controller": "Xbox",
        "mappings": [{"control": "A", "action": "Jump", "context": "On foot"}],
    }


def test_renderers_escape_content():
    data = layout()
    data["game"] = "Sky <Road>"
    data["notes"] = "Use <carefully>"
    assert "Sky &lt;Road&gt;" in render_html(data)
    assert "Use &lt;carefully&gt;" in render_html(data)
    assert "| A | Jump | On foot |" in render_markdown(data)


def test_load_validation(tmp_path):
    path = tmp_path / "layout.json"
    path.write_text(json.dumps(layout()), encoding="utf-8")
    assert load_layout(path)["controller"] == "Xbox"
    data = layout()
    data["mappings"].append({"control": "A", "action": "Use"})
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="unique"):
        load_layout(path)


@pytest.mark.parametrize(
    ("payload", "error"),
    [
        ({"version": 2}, ValueError),
        (
            {"version": 1, "game": "", "platform": "PC", "controller": "Pad", "mappings": []},
            ValueError,
        ),
        (
            {"version": 1, "game": "A", "platform": "PC", "controller": "Pad", "mappings": []},
            ValueError,
        ),
        (
            {"version": 1, "game": "A", "platform": "PC", "controller": "Pad", "mappings": [None]},
            TypeError,
        ),
        (
            {
                "version": 1,
                "game": "A",
                "platform": "PC",
                "controller": "Pad",
                "mappings": [{"control": "A", "action": ""}],
            },
            ValueError,
        ),
    ],
)
def test_rejects_invalid_layouts(tmp_path, payload, error):
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(error):
        load_layout(path)


def test_cli_writes_and_refuses_replace(tmp_path, capsys):
    source = tmp_path / "layout.json"
    source.write_text(json.dumps(layout()), encoding="utf-8")
    output = tmp_path / "card.html"
    assert main([str(source), "--output", str(output)]) == 0
    assert "Jump" in output.read_text(encoding="utf-8")
    assert main([str(source), "--output", str(output)]) == 2
    assert "already exists" in capsys.readouterr().err
