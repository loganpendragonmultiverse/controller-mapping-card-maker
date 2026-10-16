# Development

## 1.1.0 - 2026-10-15

Legacy `mappings` layouts continue to work. For separate modes, replace `mappings` with a `contexts` list:

```json
{"version":1,"game":"Sky Road","platform":"PC","controller":"Pad","contexts":[{"name":"On foot","mappings":[{"control":"A","action":"Jump"}]},{"name":"Driving","mappings":[{"control":"A","action":"Brake"}]}]}
```

Controls must be unique within each context; the same control may have different actions in different contexts. Context names must be unique. Use `mapping-card layout.json --print-context "Driving" --output driving.html` to make a card containing only that context. Without selection, all contexts appear. The option also works with `--format markdown`. Unknown contexts are rejected. Cards remain self-contained with responsive single-column mobile layout and print styles; no scripts or game access are added.

Merge and release require independent review and the repository CI gates.
