# AGENTS.md

Python SDK for the Captcha Solver API, published on PyPI as `captcha-sdk`.

## Project layout

- `captcha_sdk/` — package: `client.py` (sync), `async_client.py` (async), `tasks.py`, `exceptions.py`
- `tests/sync/`, `tests/async/` — pytest, HTTP is mocked
- `examples/sync/`, `examples/async/` — runnable examples
- `DEVELOPMENT.md` — setup, tests, release process

## Commands

```bash
python -m pip install -e ".[dev]"   # required: async tests need pytest-asyncio
python -m pytest -q
python -m build && python -m twine check --strict dist/*
```

## Rules

- The version is defined in two places and must match: `pyproject.toml` (`version`) and `captcha_sdk/__init__.py` (`__version__`).
- Supported Python is 3.9+; do not use syntax or stdlib features newer than 3.9.

## Commits

English, [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>: <short description in imperative mood>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`, `build`.

Examples:

```
feat: add Tencent captcha task
fix: handle empty solution in async client
docs: add DEVELOPMENT.md
chore: set version to 1.0.0
```
