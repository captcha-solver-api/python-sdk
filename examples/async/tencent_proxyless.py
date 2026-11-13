"""
Example: Solve a Tencent captcha challenge with the async client.

This example solves Tencent CAPTCHA without a customer proxy. Obtain appId and
any custom captchaScript from the target page, then deliver the returned ticket
and randstr to its registered callback and verify acceptance separately. It uses
TencentTaskProxyless and AsyncCaptchaClient.solve().

How it works:
STEP-01 - Configure AsyncCaptchaClient and obtain appId from the page's Tencent setup.
STEP-02 - Create TencentTaskProxyless and await solve() without a customer proxy.
STEP-03 - Print ticket and randstr and explain their site-specific application.
STEP-04 - Report errors; page or server acceptance must be verified by the integration.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and appId with values from your target page.
    Pass captchaScript if the site uses a non-default script URL.
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
from captcha_solver_api.tasks import TencentTaskProxyless
from examples._cli import debug_enabled

# STEP-01: Configure AsyncCaptchaClient and obtain appId from the page's Tencent setup.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")


async def main():
    async with AsyncCaptchaClient(api_key, debug=debug_enabled()) as solver:
        # --- Proxyless example ---
        # Solves Tencent captcha without a proxy.
        # The service's own proxies are used to solve the captcha.
        # appId is found in the page source code. captchaScript is optional if the site uses the default.
        try:
            # STEP-02: Create TencentTaskProxyless and await solve() without a customer proxy.
            result = await solver.solve(
                TencentTaskProxyless(
                    websiteURL="https://example.com/register",  # Full URL of the page using Tencent captcha
                    appId="YOUR_APP_ID",  # appId from page source code (required)
                    # Optional fields:
                    captchaScript="https://captchacdn.tencentcloudcs.com/TCaptcha-global.js",  # Custom script URL if non-default
                )
            )
            # STEP-03: Print ticket and randstr and explain their site-specific application.
            # Solution contains {"appid": "...", "ret": 0, "ticket": "...", "randstr": "..."}
            # Pass all four values together into the page's captcha callback as-is.
            print("result: " + str(result))
        except Exception as e:
            # STEP-04: Report errors; page or server acceptance must be verified by the integration.
            sys.exit(e)


asyncio.run(main())
