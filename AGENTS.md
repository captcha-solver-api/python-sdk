# AGENTS.md

Python SDK for the Captcha Solver API, published on PyPI as `captcha-sdk`.

## Project layout

- `captcha_sdk/` — package: `client.py` (sync), `async_client.py` (async), `tasks.py`, `exceptions.py`
- `tests/sync/`, `tests/async/` — unit tests, HTTP is mocked
- `tests/integration/` — real HTTP requests to a local stub server (`api_server` fixture)
- `examples/sync/`, `examples/async/` — runnable examples
- `DEVELOPMENT.md` — setup, tests, release process

## Commands

```bash
python -m pip install -e ".[dev]"   # required: async tests need pytest-asyncio
python -m pytest -q
python -m build && python -m twine check --strict dist/*
```

## Rules

- The version is defined only in `captcha_sdk/_version.py`; `pyproject.toml` reads it dynamically. Do not hardcode it elsewhere.
- Every request sends `X-SDK: python-sdk/<version>` so the backend can collect SDK usage stats. Keep it in both clients.
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
