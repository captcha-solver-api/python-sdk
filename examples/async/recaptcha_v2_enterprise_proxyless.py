"""
Example: Solve a reCAPTCHA v2 Enterprise challenge with the async client.

This example solves reCAPTCHA v2 Enterprise without a customer proxy. Supply
the page URL, Enterprise site key, and enterprisePayload when the page passes
one to grecaptcha.enterprise.render(); the returned gRecaptchaResponse still
requires site-specific submission and verification. It uses
RecaptchaV2EnterpriseTaskProxyless and AsyncCaptchaClient.solve().

How it works:
STEP-01 - Configure AsyncCaptchaClient and extract the Enterprise site key and payload.
STEP-02 - Create RecaptchaV2EnterpriseTaskProxyless and await solve() without a customer proxy.
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
from captcha_solver_api.tasks import RecaptchaV2EnterpriseTaskProxyless
from examples._cli import debug_enabled

# STEP-01: Configure AsyncCaptchaClient and extract the Enterprise site key and payload.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")


async def main():
    async with AsyncCaptchaClient(api_key, debug=debug_enabled()) as solver:
        # --- Proxyless example ---
        # Solves reCAPTCHA v2 Enterprise without a proxy.
        # Enterprise captchas are loaded via the reCAPTCHA Enterprise API.
        # If the site passes extra parameters to grecaptcha.enterprise.render(),
        # you must pass them as enterprisePayload or the token will be rejected.
        try:
            # STEP-02: Create RecaptchaV2EnterpriseTaskProxyless and await solve() without a customer proxy.
            result = await solver.solve(
                RecaptchaV2EnterpriseTaskProxyless(
                    websiteURL="https://example.com/login",  # Full URL of the Enterprise-protected page
                    websiteKey="YOUR_WEBSITE_KEY",  # data-sitekey attribute value
                    isInvisible=False,  # Set True for invisible reCAPTCHA
                    # Optional fields (pass only if the target site requires them)
                    # enterprisePayload={'s': 'value-from-page'},  # Extra params from grecaptcha.enterprise.render()
                    # apiDomain='recaptcha.net',                    # Set if site loads captcha from recaptcha.net
                    # userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',  # Browser User-Agent
                    # cookies='session=abc123; token=xyz789',       # Session cookies if needed
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
