"""Example: Solve reCAPTCHA v2 Enterprise through your own proxy.

What it does:
    This example shows how to solve reCAPTCHA v2 Enterprise through your own proxy. It uses RecaptchaV2EnterpriseTask and AsyncCaptchaClient.solve(), returning a gRecaptchaResponse token.

How it works:
    STEP-01 - Configure AsyncCaptchaClient with the API key.
    STEP-02 - Provide websiteURL, websiteKey, enterprisePayload when required, and proxy settings.
    STEP-03 - Create RecaptchaV2EnterpriseTask and pass it to await solver.solve(), which creates and polls the task.
    STEP-04 - Print the gRecaptchaResponse token; applying and verifying it are target-specific.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and websiteKey with values from your target page.
    If the site uses enterprisePayload, extract and pass it or the token may be rejected.
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
from captcha_solver_api.tasks import RecaptchaV2EnterpriseTask

# STEP-01: Configure AsyncCaptchaClient with the API key.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")


async def main():
    async with AsyncCaptchaClient(api_key) as solver:
        # Solves reCAPTCHA v2 Enterprise through your own proxy.
        # Use when the target site is geo-restricted or you need a consistent session.
        try:
            # STEP-02: Provide websiteURL, websiteKey, enterprisePayload when required, and proxy settings.
            # STEP-03: Create RecaptchaV2EnterpriseTask and pass it to await solver.solve(), which creates and polls the task.
            result = await solver.solve(
                RecaptchaV2EnterpriseTask(
                    websiteURL="https://example.com/login",  # Full URL of the Enterprise-protected page
                    websiteKey="YOUR_WEBSITE_KEY",  # data-sitekey attribute value
                    # Proxy connection used by the service; replace every placeholder.
                    proxyType="http",  # http, socks4, or socks5
                    proxyAddress="1.2.3.4",  # Proxy IP address
                    proxyPort=8080,  # Proxy port
                    proxyLogin="user",  # Login for proxy authorization (optional)
                    proxyPassword="password",  # Password for proxy authorization (optional)
                    # Optional task fields; pass only values required by the target page.
                    isInvisible=False,
                    # enterprisePayload={'s': 'value-from-page'},  # Extra params from grecaptcha.enterprise.render()
                    userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...",  # Browser User-Agent
                    cookies="foo=bar; baz=1",  # Session cookies if needed
                )
            )
            # Solution contains the same gRecaptchaResponse token.
            # STEP-04: Print the gRecaptchaResponse token; applying and verifying it are target-specific.
            print("result: " + str(result))
        # Handle errors raised while solving the CAPTCHA.
        except Exception as e:
            sys.exit(e)


asyncio.run(main())
