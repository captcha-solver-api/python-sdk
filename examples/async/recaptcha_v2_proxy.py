"""
Example: Solve a reCAPTCHA v2 challenge through your own proxy with the async client.

This example solves reCAPTCHA v2 through your own proxy. Supply the page URL,
widget data-sitekey, and proxy connection details; the service returns
gRecaptchaResponse for site-specific submission and verification. It uses
RecaptchaV2Task and AsyncCaptchaClient.solve().

How it works:
STEP-01 - Configure AsyncCaptchaClient, page parameters, and customer proxy credentials.
STEP-02 - Create RecaptchaV2Task and await solve() through that proxy.
STEP-03 - Print gRecaptchaResponse and explain its site-specific application.
STEP-04 - Report errors; page acceptance must be verified by the integration.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and websiteKey with values from your target page.
    Replace the proxy placeholders with your own proxy settings.
"""

import asyncio
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

from captcha_solver_api import AsyncCaptchaClient
from captcha_solver_api.tasks import RecaptchaV2Task

# STEP-01: Configure AsyncCaptchaClient, page parameters, and customer proxy credentials.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")


async def main():
    # Optional: timeout (max seconds to wait for solution, default 120)
    # Optional: polling_interval (seconds before and between status checks, default 10)
    async with AsyncCaptchaClient(api_key) as solver:
        # --- With proxy example ---
        # Solves reCAPTCHA v2 through your own proxy.
        # Use when the target site is geo-restricted or you need session consistency.
        try:
            # STEP-02: Create RecaptchaV2Task and await solve() through that proxy.
            result = await solver.solve(
                RecaptchaV2Task(
                    websiteURL="https://example.com/login",  # Full URL of the page with captcha
                    websiteKey="YOUR_WEBSITE_KEY",  # data-sitekey attribute value
                    # --- Proxy parameters (replace with your own -- these are placeholders) ---
                    proxyType="http",  # http, socks4, or socks5
                    proxyAddress="1.2.3.4",  # Proxy IP address
                    proxyPort=8080,  # Proxy port
                    proxyLogin="user",  # Login for proxy authorization (optional)
                    proxyPassword="password",  # Password for proxy authorization (optional)
                )
            )
            # STEP-03: Print gRecaptchaResponse and explain its site-specific application.
            # Solution contains the same gRecaptchaResponse token.
            print("result: " + str(result))
        except Exception as e:
            # STEP-04: Report errors; page acceptance must be verified by the integration.
            sys.exit(e)


asyncio.run(main())
