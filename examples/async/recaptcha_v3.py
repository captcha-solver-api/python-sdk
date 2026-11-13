"""
Example: Solve a reCAPTCHA v3 challenge with the async client.

This example solves score-based reCAPTCHA v3 without a customer proxy. Extract
the site key and page action from grecaptcha.execute(), choose the required
minimum score, and submit the returned gRecaptchaResponse through the target's
own flow. It uses RecaptchaV3TaskProxyless and AsyncCaptchaClient.solve().

How it works:
STEP-01 - Configure AsyncCaptchaClient and extract the key and action from grecaptcha.execute().
STEP-02 - Create RecaptchaV3TaskProxyless with the required score and await solve().
STEP-03 - Print gRecaptchaResponse and explain its site-specific application.
STEP-04 - Report errors; page acceptance must be verified by the integration.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL, websiteKey, and minScore with values from your target
    page, and pass pageAction if the site uses it -- this increases the
    chance of the token being accepted.
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
from captcha_solver_api.tasks import RecaptchaV3TaskProxyless
from examples._cli import debug_enabled

# STEP-01: Configure AsyncCaptchaClient and extract the key and action from grecaptcha.execute().
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")


async def main():
    # reCAPTCHA v3 tasks may take longer to solve. Increase timeout if needed.
    async with AsyncCaptchaClient(api_key, debug=debug_enabled(), timeout=180) as solver:
        # reCAPTCHA v3 returns a score instead of a pass/fail challenge.
        # The higher the minScore you request, the harder and longer the task takes.
        # minScore values: 0.3 (fastest), 0.7 (balanced), 0.9 (highest, slowest).
        try:
            # STEP-02: Create RecaptchaV3TaskProxyless with the required score and await solve().
            result = await solver.solve(
                RecaptchaV3TaskProxyless(
                    websiteURL="https://example.com/login",  # Full URL of the page with the v3 widget
                    websiteKey="YOUR_WEBSITE_KEY",  # Site key of the v3 widget on that page
                    minScore=0.3,  # Minimum acceptable score (0.3, 0.7, or 0.9)
                    # Optional fields (pass if the site uses them, increases token acceptance)
                    pageAction="homepage",  # Action set by that page in grecaptcha.execute()
                    # isEnterprise=True,                        # Set True for reCAPTCHA v3 Enterprise
                    # apiDomain='www.recaptcha.net',            # Set if site loads from recaptcha.net
                )
            )
            # STEP-03: Print gRecaptchaResponse and explain its site-specific application.
            # Solution contains {"gRecaptchaResponse": "03AGdBq..."}
            # Pass this token to the g-recaptcha-response field or grecaptcha callback.
            print("result: " + str(result))
        except Exception as e:
            # STEP-04: Report errors; page acceptance must be verified by the integration.
            sys.exit(e)


asyncio.run(main())
