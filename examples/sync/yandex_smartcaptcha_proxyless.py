"""Example: Solve token-based Yandex smartcaptcha without a proxy.

What it does:
    This example shows how to solve token-based Yandex SmartCaptcha without a proxy. It uses YandexSmartCaptchaTaskProxyless and CaptchaClient.solve(), returning a token.

How it works:
    STEP-01 - Configure CaptchaClient with the API key and debug logging.
    STEP-02 - Obtain the task parameters. Extract websiteURL and websiteKey from the target page.
    STEP-03 - Create YandexSmartCaptchaTaskProxyless and pass it to solver.solve(task), which creates and polls the task.
    STEP-04 - Print a token. Applying the solution and verifying acceptance are target-specific.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and websiteKey with values from your target page.
"""

import os
import sys

try:
    from dotenv import load_dotenv
except ModuleNotFoundError as exc:
    if exc.name != "dotenv":
        raise
    load_dotenv = None

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(repo_root)
if load_dotenv is not None:
    load_dotenv(os.path.join(repo_root, ".env"))

from captcha_solver_api import CaptchaClient
from captcha_solver_api.tasks import YandexSmartCaptchaTaskProxyless

api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")

solver = CaptchaClient(api_key, debug=True)

# --- Proxyless example ---
# Solves Yandex SmartCaptcha without a proxy.
# The service's own proxies are used to solve the captcha.
# websiteKey is the sitekey value from the page code or captcha iframe.
try:
    result = solver.solve(
        YandexSmartCaptchaTaskProxyless(
            websiteURL="https://example.com/login",  # Full URL of the page using SmartCaptcha
            websiteKey="YOUR_WEBSITE_KEY",  # sitekey from that page
            # Optional fields:
            # userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',  # Browser User-Agent
            # cookies='session=abc123; token=xyz789',                     # Session cookies if needed
        )
    )
    # Solution contains {"token": "dV9xNjYyNTU3NjkxO4k9OTQuNVMuMjkuMjM9..."}
    # Use solution.token in the smart-token field or pass to your site's backend.
    print("result: " + str(result))
except Exception as e:
    sys.exit(e)
