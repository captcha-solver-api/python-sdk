"""Example: Solve Tencent captcha without a proxy.

What it does:
    This example shows how to solve Tencent CAPTCHA without a proxy. It uses TencentTaskProxyless and AsyncCaptchaClient.solve(), returning appid, ret, ticket, and randstr values.

How it works:
    STEP-01 - Configure AsyncCaptchaClient with the API key and debug logging.
    STEP-02 - Obtain the task parameters. Extract websiteURL, appId, and any non-default captchaScript from the target page.
    STEP-03 - Create TencentTaskProxyless and pass it to await solver.solve(task), which creates and polls the task.
    STEP-04 - Print appid, ret, ticket, and randstr values. Applying the solution and verifying acceptance are target-specific.

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

api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")


async def main():
    async with AsyncCaptchaClient(api_key, debug=True) as solver:
        # --- Proxyless example ---
        # Solves Tencent captcha without a proxy.
        # The service's own proxies are used to solve the captcha.
        # appId is found in the page source code. captchaScript is optional if the site uses the default.
        try:
            result = await solver.solve(
                TencentTaskProxyless(
                    websiteURL="https://example.com/register",  # Full URL of the page using Tencent captcha
                    appId="YOUR_APP_ID",  # appId from page source code (required)
                    # Optional fields:
                    captchaScript="https://captchacdn.tencentcloudcs.com/TCaptcha-global.js",  # Custom script URL if non-default
                )
            )
            # Solution contains {"appid": "...", "ret": 0, "ticket": "...", "randstr": "..."}
            # Pass all four values together into the page's captcha callback as-is.
            print("result: " + str(result))
        except Exception as e:
            sys.exit(e)


asyncio.run(main())
