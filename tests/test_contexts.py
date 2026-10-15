import json

import pytest

from controller_mapping_card.cli import main
from controller_mapping_card.core import load_layout, render_html, render_markdown


def named():
    return {
        "version": 1,
        "game": "Game",
        "platform": "PC",
        "controller": "Pad",
        "contexts": [
            {"name": "Walk <safe>", "mappings": [{"control": "A", "action": "Jump"}]},
            {"name": "Drive", "mappings": [{"control": "A", "action": "Brake"}]},
        ],
    }


def test_same_control_contexts_selection_escaping_and_print_styles(tmp_path, capsys):
    source = tmp_path / "layout.json"
    source.write_text(json.dumps(named()))
    data = load_layout(source)
    all_cards = render_html(data)
    assert "Jump" in all_cards and "Brake" in all_cards
    assert "Walk &lt;safe&gt;" in all_cards and "<safe>" not in all_cards
    assert "@media(max-width:560px)" in all_cards and "@media print" in all_cards
    assert "break-inside:avoid" in all_cards
    assert "Brake" not in render_html(data, "Walk <safe>")
    assert "Walk &lt;safe&gt;" in render_markdown(data)
    assert "Jump" not in render_markdown(data, "Drive")
    assert main([str(source), "--print-context", "Drive"]) == 0
    assert "Jump" not in capsys.readouterr().out
    assert main([str(source), "--print-context", "unknown"]) == 2


@pytest.mark.parametrize("change", ["duplicate", "empty", "names", "mixed", "badcontext"])
def test_invalid_contexts(tmp_path, change):
    data = named()
    if change == "duplicate":
        data["contexts"][0]["mappings"] *= 2
    elif change == "empty":
        data["contexts"] = []
    elif change == "names":
        data["contexts"][1]["name"] = data["contexts"][0]["name"]
    elif change == "mixed":
        data["mappings"] = []
    else:
        data["contexts"] = [None]
    source = tmp_path / "layout.json"
    source.write_text(json.dumps(data))
    with pytest.raises((ValueError, TypeError)):
        load_layout(source)


def test_legacy_selection_is_explicitly_rejected():
    with pytest.raises(ValueError, match="named-context"):
        render_html({"mappings": []}, "Drive")
