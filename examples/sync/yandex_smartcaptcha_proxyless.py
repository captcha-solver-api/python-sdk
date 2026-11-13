"""
Example: Solve a Yandex SmartCaptcha challenge (token-based).

This example solves token-based Yandex SmartCaptcha without a customer proxy.
Supply the target page URL and sitekey from its widget or iframe; the returned
token must be submitted through the page's smart-token or backend flow and then
verified there. It uses YandexSmartCaptchaTaskProxyless and CaptchaClient.solve().

How it works:
STEP-01 - Configure CaptchaClient and obtain the page URL and SmartCaptcha site key.
STEP-02 - Create YandexSmartCaptchaTaskProxyless and call solve() without a customer proxy.
STEP-03 - Print the token and explain its site-specific application.
STEP-04 - Report errors; page acceptance must be verified by the integration.

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
from examples._cli import debug_enabled

# STEP-01: Configure CaptchaClient and obtain the page URL and SmartCaptcha site key.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")

solver = CaptchaClient(api_key, debug=debug_enabled())

# --- Proxyless example ---
# Solves Yandex SmartCaptcha without a proxy.
# The service's own proxies are used to solve the captcha.
# websiteKey is the sitekey value from the page code or captcha iframe.
try:
    # STEP-02: Create YandexSmartCaptchaTaskProxyless and call solve() without a customer proxy.
    result = solver.solve(
        YandexSmartCaptchaTaskProxyless(
            websiteURL="https://example.com/login",  # Full URL of the page using SmartCaptcha
            websiteKey="YOUR_WEBSITE_KEY",  # sitekey from that page
            # Optional fields:
            # userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',  # Browser User-Agent
            # cookies='session=abc123; token=xyz789',                     # Session cookies if needed
        )
    )
    # STEP-03: Print the token and explain its site-specific application.
    # Solution contains {"token": "dV9xNjYyNTU3NjkxO4k9OTQuNVMuMjkuMjM9..."}
    # Use solution.token in the smart-token field or pass to your site's backend.
    print("result: " + str(result))
except Exception as e:
    # STEP-04: Report errors; page acceptance must be verified by the integration.
    sys.exit(e)
