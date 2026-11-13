"""
Example: Solve a Yandex SmartCaptcha challenge (token-based).

This example solves token-based Yandex SmartCaptcha through your own proxy.
Supply the page URL, sitekey, and proxy details; then submit and verify the
returned token through the target's site-specific flow. It uses
YandexSmartCaptchaTask and CaptchaClient.solve().

How it works:
STEP-01 - Configure CaptchaClient, SmartCaptcha parameters, and customer proxy credentials.
STEP-02 - Create YandexSmartCaptchaTask and call solve() through that proxy.
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
from captcha_solver_api.tasks import YandexSmartCaptchaTask

# STEP-01: Configure CaptchaClient, SmartCaptcha parameters, and customer proxy credentials.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")

solver = CaptchaClient(api_key)

# --- With proxy example ---
# Solves Yandex SmartCaptcha through your own proxy.
# Note: this is the only captcha type where an https proxy is accepted.
try:
    # STEP-02: Create YandexSmartCaptchaTask and call solve() through that proxy.
    result = solver.solve(
        YandexSmartCaptchaTask(
            websiteURL="https://example.com/login",  # Full URL of the page using SmartCaptcha
            websiteKey="YOUR_WEBSITE_KEY",  # sitekey from that page
            # --- Proxy parameters (replace with your own -- these are placeholders) ---
            proxyType="http",  # http, https, socks4, or socks5 (https is accepted only for this type)
            proxyAddress="1.2.3.4",  # Proxy IP address
            proxyPort=8080,  # Proxy port
            proxyLogin="user",  # Login for proxy authorization (optional)
            proxyPassword="password",  # Password for proxy authorization (optional)
            # Optional fields:
            # userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',  # Browser User-Agent
            # cookies='session=abc123; token=xyz789',                     # Session cookies if needed
        )
    )
    # STEP-03: Print the token and explain its site-specific application.
    # Solution contains the same token.
    print("result: " + str(result))
except Exception as e:
    # STEP-04: Report errors; page acceptance must be verified by the integration.
    sys.exit(e)
