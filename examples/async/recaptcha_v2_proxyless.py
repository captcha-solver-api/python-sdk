"""
Example: Solve a reCAPTCHA v2 challenge without a proxy with the async client.

This example solves reCAPTCHA v2 without a customer proxy. Supply the target
page URL and the widget's data-sitekey; the service returns
gRecaptchaResponse, which your integration must submit and verify using the
page-specific flow. It uses RecaptchaV2TaskProxyless and AsyncCaptchaClient.solve().

How it works:
STEP-01 - Configure AsyncCaptchaClient and obtain the page URL and data-sitekey.
STEP-02 - Create RecaptchaV2TaskProxyless and await solve() without a customer proxy.
STEP-03 - Print gRecaptchaResponse and explain its site-specific application.
STEP-04 - Report errors; page acceptance must be verified by the integration.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and websiteKey with values from your target page.
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
from captcha_solver_api.tasks import RecaptchaV2TaskProxyless
from examples._cli import debug_enabled

# STEP-01: Configure AsyncCaptchaClient and obtain the page URL and data-sitekey.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")


async def main():
    # Optional: timeout (max seconds to wait for solution, default 120)
    # Optional: polling_interval (seconds before and between status checks, default 10)
    async with AsyncCaptchaClient(api_key, debug=debug_enabled()) as solver:
        # --- Proxyless example ---
        # Solves reCAPTCHA v2 without a proxy. The service uses its own IP addresses.
        try:
            # STEP-02: Create RecaptchaV2TaskProxyless and await solve() without a customer proxy.
            # solve() handles task creation, polling, and returns the solution dict.
            result = await solver.solve(
                RecaptchaV2TaskProxyless(
                    websiteURL="https://example.com/login",  # Full URL of the page with the captcha
                    websiteKey="YOUR_WEBSITE_KEY",  # data-sitekey attribute value on that page
                    isInvisible=False,  # Set True for invisible reCAPTCHA
                )
            )
            # STEP-03: Print gRecaptchaResponse and explain its site-specific application.
            # Solution contains {"gRecaptchaResponse": "03AGdBq..."}
            # Pass this token to the g-recaptcha-response field or widget callback.
            print("result: " + str(result))
        except Exception as e:
            # STEP-04: Report errors; page acceptance must be verified by the integration.
            sys.exit(e)


asyncio.run(main())
