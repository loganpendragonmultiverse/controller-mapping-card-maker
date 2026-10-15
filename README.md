# Controller Mapping Card Maker

[![CI](https://github.com/loganpendragonmultiverse/controller-mapping-card-maker/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/controller-mapping-card-maker/actions/workflows/ci.yml)

Controller Mapping Card Maker creates printable and phone-friendly control refresher cards from an explicit local JSON layout. It is useful when returning to a game, documenting a custom mapping, or keeping different control contexts visible.

## Three-minute start

```bash
python -m pip install .
mapping-card examples/layout.json --output card.html
mapping-card examples/layout.json --format markdown
```

HTML output is a self-contained responsive page with print styles. Markdown output is portable and easy to edit. User-provided content is escaped in HTML, controls must be unique, and existing output files are refused.

## Boundaries

The tool does not detect mappings from games, controller software, screenshots, or manuals. Users must supply layouts they are allowed to use. It does not alter controller configuration.

Requires Python 3.10 or newer. Development checks are Ruff, pytest with branch coverage, and package builds.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).

## Named contexts and selected print cards

Legacy `mappings` layouts continue to work. For separate modes, replace `mappings` with a `contexts` list:

```json
{"version":1,"game":"Sky Road","platform":"PC","controller":"Pad","contexts":[{"name":"On foot","mappings":[{"control":"A","action":"Jump"}]},{"name":"Driving","mappings":[{"control":"A","action":"Brake"}]}]}
```

Controls must be unique within each context; the same control may have different actions in different contexts. Context names must be unique. Use `mapping-card layout.json --print-context "Driving" --output driving.html` to make a card containing only that context. Without selection, all contexts appear. The option also works with `--format markdown`. Unknown contexts are rejected. Cards remain self-contained with responsive single-column mobile layout and print styles; no scripts or game access are added.
