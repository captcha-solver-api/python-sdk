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

Replace placeholder values such as `YOUR_WEBSITE_KEY`, `YOUR_APP_ID`, `YOUR_CAPTCHA_ID`, and proxy credentials before running token or proxy examples. Do not commit real API keys or proxy credentials.

## Directories

- [`sync`](sync) contains blocking examples using `CaptchaClient`.
- [`async`](async) contains asynchronous examples using `AsyncCaptchaClient`.
- [`assets`](assets) contains sample images used by image and coordinate examples.

Each supported CAPTCHA type has a matching sync and async script:

| CAPTCHA type | Sync | Async | Main result |
|---|---|---|---|
| Account balance | [balance.py](sync/balance.py) | [balance.py](async/balance.py) | `float` balance |
| reCAPTCHA v2 | [recaptcha_v2.py](sync/recaptcha_v2.py) | [recaptcha_v2.py](async/recaptcha_v2.py) | `gRecaptchaResponse` |
| reCAPTCHA v2 Enterprise | [recaptcha_v2_enterprise.py](sync/recaptcha_v2_enterprise.py) | [recaptcha_v2_enterprise.py](async/recaptcha_v2_enterprise.py) | `gRecaptchaResponse` |
| reCAPTCHA v3 | [recaptcha_v3.py](sync/recaptcha_v3.py) | [recaptcha_v3.py](async/recaptcha_v3.py) | `gRecaptchaResponse` |
| Cloudflare Turnstile | [turnstile.py](sync/turnstile.py) | [turnstile.py](async/turnstile.py) | `token` |
| Image to Text | [image_to_text.py](sync/image_to_text.py) | [image_to_text.py](async/image_to_text.py) | `text` |
| GeeTest v3 | [geetest_v3.py](sync/geetest_v3.py) | [geetest_v3.py](async/geetest_v3.py) | `challenge`, `validate`, `seccode` |
| GeeTest v4 | [geetest_v4.py](sync/geetest_v4.py) | [geetest_v4.py](async/geetest_v4.py) | `captcha_output` and related fields |
| Yandex SmartCaptcha token | [yandex_smartcaptcha.py](sync/yandex_smartcaptcha.py) | [yandex_smartcaptcha.py](async/yandex_smartcaptcha.py) | `token` |
| Yandex SmartCaptcha image | [yandex_smartcaptcha_image.py](sync/yandex_smartcaptcha_image.py) | [yandex_smartcaptcha_image.py](async/yandex_smartcaptcha_image.py) | `coordinates` |
| Coordinates / click captcha | [coordinates.py](sync/coordinates.py) | [coordinates.py](async/coordinates.py) | `coordinates` |
| Tencent | [tencent.py](sync/tencent.py) | [tencent.py](async/tencent.py) | `appid`, `ret`, `ticket`, `randstr` |

## Running an example

Run commands from the repository root so local imports and bundled assets resolve correctly:

```bash
python examples/sync/balance.py
python examples/sync/image_to_text.py
python examples/async/recaptcha_v2.py
```

Async scripts create an `AsyncCaptchaClient` and await the same operations as the synchronous client. For several captchas, see the parallel solving pattern in the main [README](../README.md#solving-multiple-captchas-in-parallel).

## Important notes

- Image examples can use the bundled files in `examples/assets`; they do not require a target website.
- Token examples use placeholder site keys and URLs. Replace them with values from a page you are authorized to test.
- `geetest_v3.py` needs a fresh `challenge` for every request; it expires quickly and must not be hardcoded.
- Files using `*Task` instead of `*TaskProxyless` demonstrate solving through your own proxy. Supply valid proxy settings for your account.
- For task parameters and response formats, see the [CAPTCHA type documentation](https://captcha-solver.com/en/docs/captcha-types).
- For client methods and errors, see the [main README](../README.md#client-reference).
