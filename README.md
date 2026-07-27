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
