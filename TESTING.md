# Testing

Use Python 3.10 or later in a clean virtual environment:

```sh
python -m venv .venv
# Activate .venv with the command for your shell.
python -m pip install -e '.[dev]'
ruff format --check .
ruff check .
pytest
python -m build
```

The pytest configuration enforces the repository's existing 90% coverage floor. CI covers Python 3.10 and 3.14 on Linux, Windows, and macOS. New feature tests use synthetic input and do not require game files or personal data. Run the full suite before submitting a change; CLI regression tests preserve legacy input/output behavior.

## 1.1.2 qualification

Run the full configured Ruff, pytest branch-coverage and package-build checks. Output-safety regressions cover existing/source destinations, symlink destinations, concurrent creators and ordinary I/O failures. Install both the wheel and source distribution separately outside the checkout, verify the entry point and version, and compare packaged documentation with this source. CI must pass on its supported OS/Python matrix before merge.
