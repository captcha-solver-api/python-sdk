"""
Example: Solve a reCAPTCHA v2 challenge without a proxy with the async client.

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

api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")


async def main():
    # Optional: timeout (max seconds to wait for solution, default 120)
    # Optional: polling_interval (seconds before and between status checks, default 10)
    async with AsyncCaptchaClient(api_key) as solver:
        # --- Proxyless example ---
        # Solves reCAPTCHA v2 without a proxy. The service uses its own IP addresses.
        try:
            # solve() handles task creation, polling, and returns the solution dict.
            result = await solver.solve(
                RecaptchaV2TaskProxyless(
                    websiteURL="https://example.com/login",  # Full URL of the page with the captcha
                    websiteKey="YOUR_WEBSITE_KEY",  # data-sitekey attribute value on that page
                    isInvisible=False,  # Set True for invisible reCAPTCHA
                )
            )
            # Solution contains {"gRecaptchaResponse": "03AGdBq..."}
            # Pass this token to the g-recaptcha-response field or widget callback.
            print("result: " + str(result))
        except Exception as e:
            sys.exit(e)


asyncio.run(main())
