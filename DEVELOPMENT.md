# Development

## Setup

Requires Python 3.9+.

```bash
git clone https://github.com/captcha-solver-api/python-sdk
cd python-sdk
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

The `dev` extra installs `pytest`, `pytest-asyncio`, `pytest-mock` and `python-dotenv`.
Without `pytest-asyncio` every test in `tests/async/` fails.

## Tests

```bash
python -m pytest -q                 # all tests
python -m pytest tests/sync -v      # sync client only
python -m pytest tests/async -v     # async client only
python -m pytest tests/integration  # real HTTP requests to a local stub server
python -m pytest -k turnstile       # filter by name
```

No API key or internet access is needed:

- `tests/sync/`, `tests/async/` — unit tests, HTTP calls are mocked.
- `tests/integration/` — the client sends real HTTP requests to a server started on
  `127.0.0.1` by the `api_server` fixture, which records path, headers and body.
  Use it to check what actually goes over the wire (e.g. the `X-SDK` header).

CI (`.github/workflows/tests.yml`) runs the suite on Python 3.9–3.13 for every push
and pull request and checks that the package builds.

## Editor documentation

Keep Google-style docstrings on public clients, methods, task classes, and
exceptions. Document every argument by its exact signature name, including
defaults, units, accepted values, and whether `None` omits an API field. Methods
should describe their return value and raised SDK exceptions; task classes should
describe the solution fields returned by `solve()`.

Keep constructor settings on the client class as well as `__init__`, so class
hover and constructor signature help both have useful documentation. Include
short examples and keep sync/async documentation aligned (`await` for async
calls). Examples using `client`, `task`, or `task_id` assume those already exist;
async examples belong inside an `async def` function.

Type annotations and `captcha_solver_api/py.typed` must remain in the wheel and
source distribution. To review an editor-facing change, install the built wheel
in a separate environment, inspect `help(CaptchaClient.solve)` and
`help(RecaptchaV2TaskProxyless)`, and check hover/signature help with that environment
selected in the editor.

## Building locally

```bash
python -m pip install build twine
python -m build
python -m twine check --strict dist/*
```

## Releasing

Publishing to PyPI is done by `.github/workflows/publish.yml` using Trusted Publishing
(OIDC), so no API token is stored in the repository.

1. Bump `__version__` in `captcha_solver_api/_version.py`. This is the only place:
   `pyproject.toml`, `captcha_solver_api.__version__` and the `X-SDK` request header read it from there.
2. Commit and push to `main`, wait for the Tests workflow to pass.
3. Tag and push:

   ```bash
   git tag v1.2.0
   git push origin v1.2.0
   ```

4. The workflow runs tests, verifies that the tag matches `captcha_solver_api/_version.py`, builds and
   uploads to PyPI (GitHub environment `pypi`).

A PyPI version cannot be re-uploaded. If a release is broken, publish a new patch version.

To dry-run without publishing: Actions → Publish to PyPI → Run workflow. Manual runs
test and build only.

### One-time PyPI setup

On https://pypi.org/manage/account/publishing/ add a trusted publisher:

| Field | Value |
|---|---|
| PyPI Project Name | `captcha-solver-api` |
| Owner | `captcha-solver-api` |
| Repository name | `python-sdk` |
| Workflow name | `publish.yml` |
| Environment name | `pypi` |
