# Examples

The examples show how to use the Captcha Solver Python SDK with both the synchronous and asynchronous clients.

## Before you start

Install the SDK dependencies from the repository root:

```bash
pip install -e .
```

Set `CAPTCHA_API_KEY` in the environment or in a `.env` file in the repository root. The examples load that file automatically when `python-dotenv` is installed:

```powershell
$env:CAPTCHA_API_KEY = "your_api_key"
```

```bash
export CAPTCHA_API_KEY=your_api_key
```

Environment variables work without `python-dotenv`. To use a `.env` file, install
the optional loader first:

```bash
python -m pip install python-dotenv
```

### Installed package or repository source

Both import methods are supported. For a regular installation of the local SDK,
use `python -m pip install .` instead of `pip install -e .`. The examples add
the repository root at the end of `sys.path`, so an installed package normally
takes precedence. To use only the source files, install `requests` and `httpx`
in a separate environment without installing the SDK. Existing `PYTHONPATH`
settings or preloaded modules can affect import selection.

To check the copy actually loaded by an example, print
`captcha_solver_api.__file__` after its SDK import. A regular installation points
to `site-packages`; the source import points to this repository's package folder.

Replace placeholder values such as `YOUR_WEBSITE_KEY`, `YOUR_APP_ID`, `YOUR_CAPTCHA_ID`, and proxy credentials before running token or proxy examples. Do not commit real API keys or proxy credentials.

## Directories

- [`sync`](sync) contains blocking examples using `CaptchaClient`.
- [`async`](async) contains asynchronous examples using `AsyncCaptchaClient`.
- [`assets`](assets) contains sample images used by image and coordinate examples.

Each supported CAPTCHA type has matching sync and async scripts. Types that can
use your own proxy have separate `*_proxyless.py` and `*_proxy.py` files so each
script demonstrates exactly one task variant.

| CAPTCHA type | Sync | Async | Main result |
|---|---|---|---|
| Account balance | [balance.py](sync/balance.py) | [balance.py](async/balance.py) | `float` balance |
| reCAPTCHA v2 (proxyless) | [recaptcha_v2_proxyless.py](sync/recaptcha_v2_proxyless.py) | [recaptcha_v2_proxyless.py](async/recaptcha_v2_proxyless.py) | `gRecaptchaResponse` |
| reCAPTCHA v2 (proxy) | [recaptcha_v2_proxy.py](sync/recaptcha_v2_proxy.py) | [recaptcha_v2_proxy.py](async/recaptcha_v2_proxy.py) | `gRecaptchaResponse` |
| reCAPTCHA v2 Enterprise (proxyless) | [recaptcha_v2_enterprise_proxyless.py](sync/recaptcha_v2_enterprise_proxyless.py) | [recaptcha_v2_enterprise_proxyless.py](async/recaptcha_v2_enterprise_proxyless.py) | `gRecaptchaResponse` |
| reCAPTCHA v2 Enterprise (proxy) | [recaptcha_v2_enterprise_proxy.py](sync/recaptcha_v2_enterprise_proxy.py) | [recaptcha_v2_enterprise_proxy.py](async/recaptcha_v2_enterprise_proxy.py) | `gRecaptchaResponse` |
| reCAPTCHA v3 | [recaptcha_v3.py](sync/recaptcha_v3.py) | [recaptcha_v3.py](async/recaptcha_v3.py) | `gRecaptchaResponse` |
| Cloudflare Turnstile (proxyless) | [turnstile_proxyless.py](sync/turnstile_proxyless.py) | [turnstile_proxyless.py](async/turnstile_proxyless.py) | `token` |
| Cloudflare Turnstile (proxy) | [turnstile_proxy.py](sync/turnstile_proxy.py) | [turnstile_proxy.py](async/turnstile_proxy.py) | `token` |
| Image to Text | [image_to_text.py](sync/image_to_text.py) | [image_to_text.py](async/image_to_text.py) | `text` |
| GeeTest v3 (proxyless / proxy) | [proxyless](sync/geetest_v3_proxyless.py) / [proxy](sync/geetest_v3_proxy.py) | [proxyless](async/geetest_v3_proxyless.py) / [proxy](async/geetest_v3_proxy.py) | `challenge`, `validate`, `seccode` |
| GeeTest v4 (proxyless / proxy) | [proxyless](sync/geetest_v4_proxyless.py) / [proxy](sync/geetest_v4_proxy.py) | [proxyless](async/geetest_v4_proxyless.py) / [proxy](async/geetest_v4_proxy.py) | `captcha_output` and related fields |
| Yandex SmartCaptcha (proxyless / proxy) | [proxyless](sync/yandex_smartcaptcha_proxyless.py) / [proxy](sync/yandex_smartcaptcha_proxy.py) | [proxyless](async/yandex_smartcaptcha_proxyless.py) / [proxy](async/yandex_smartcaptcha_proxy.py) | `token` |
| Coordinates / click captcha | [coordinates.py](sync/coordinates.py) | [coordinates.py](async/coordinates.py) | `coordinates` |
| Tencent (proxyless / proxy) | [proxyless](sync/tencent_proxyless.py) / [proxy](sync/tencent_proxy.py) | [proxyless](async/tencent_proxyless.py) / [proxy](async/tencent_proxy.py) | `appid`, `ret`, `ticket`, `randstr` |

## Running an example

Run commands from the repository root so local imports and bundled assets resolve correctly:

```bash
python examples/sync/balance.py
python examples/sync/image_to_text.py
python examples/async/recaptcha_v2_proxyless.py
```

Async scripts create an `AsyncCaptchaClient` and await the same operations as the synchronous client. For several captchas, see the parallel solving pattern in the main [README](../README.md#solving-multiple-captchas-in-parallel).

## Important notes

- Image examples can use the bundled files in `examples/assets`; they do not require a target website.
- Token examples use placeholder site keys and URLs. Replace them with values from a page you are authorized to test.
- `geetest_v3.py` needs a fresh `challenge` for every request; it expires quickly and must not be hardcoded.
- Files using `*Task` instead of `*TaskProxyless` demonstrate solving through your own proxy. Supply valid proxy settings for your account.
- For task parameters and response formats, see the [CAPTCHA type documentation](https://captcha-solver.com/en/docs/captcha-types).
- For client methods and errors, see the [main README](../README.md#client-reference).
- The default polling interval is 10 seconds, including the wait before the first poll. The default polling timeout is 120 seconds; use `solve(task, timeout=300)` for a longer wait. A timeout does not cancel the server's task.
