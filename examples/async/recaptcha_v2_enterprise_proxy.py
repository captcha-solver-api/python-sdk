"""
Example: Solve a reCAPTCHA v2 Enterprise challenge with the async client.

This example solves reCAPTCHA v2 Enterprise through your own proxy. Supply the
page URL, Enterprise key and payload, and proxy details; the returned
gRecaptchaResponse must be submitted and verified by the target integration.
It uses RecaptchaV2EnterpriseTask and AsyncCaptchaClient.solve().

How it works:
STEP-01 - Configure AsyncCaptchaClient, Enterprise parameters, and customer proxy credentials.
STEP-02 - Create RecaptchaV2EnterpriseTask and await solve() through that proxy.
STEP-03 - Print gRecaptchaResponse and explain its site-specific application.
STEP-04 - Report errors; page acceptance must be verified by the integration.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and websiteKey with values from your target page.
    If the site uses enterprisePayload, extract and pass it or the token may be rejected.
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
from captcha_solver_api.tasks import RecaptchaV2EnterpriseTask
from examples._cli import debug_enabled

# STEP-01: Configure AsyncCaptchaClient, Enterprise parameters, and customer proxy credentials.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")


async def main():
    async with AsyncCaptchaClient(api_key, debug=debug_enabled()) as solver:
        # --- With proxy example ---
        # Solves reCAPTCHA v2 Enterprise through your own proxy.
        # Use when the target site is geo-restricted or you need a consistent session.
        try:
            # STEP-02: Create RecaptchaV2EnterpriseTask and await solve() through that proxy.
            result = await solver.solve(
                RecaptchaV2EnterpriseTask(
                    websiteURL="https://example.com/login",  # Full URL of the Enterprise-protected page
                    websiteKey="YOUR_WEBSITE_KEY",  # data-sitekey attribute value
                    # --- Proxy parameters (replace with your own -- these are placeholders) ---
                    proxyType="http",  # http, socks4, or socks5
                    proxyAddress="1.2.3.4",  # Proxy IP address
                    proxyPort=8080,  # Proxy port
                    proxyLogin="user",  # Login for proxy authorization (optional)
                    proxyPassword="password",  # Password for proxy authorization (optional)
                    # --- Optional fields ---
                    isInvisible=False,
                    # enterprisePayload={'s': 'value-from-page'},  # Extra params from grecaptcha.enterprise.render()
                    userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...",  # Browser User-Agent
                    cookies="foo=bar; baz=1",  # Session cookies if needed
                )
            )
            # STEP-03: Print gRecaptchaResponse and explain its site-specific application.
            # Solution contains the same gRecaptchaResponse token.
            print("result: " + str(result))
        except Exception as e:
            # STEP-04: Report errors; page acceptance must be verified by the integration.
            sys.exit(e)


asyncio.run(main())
