"""Example: Solve Tencent CAPTCHA through your own proxy.

What it does:
    This example shows how to solve Tencent CAPTCHA through your own proxy. It uses TencentTask and AsyncCaptchaClient.solve(), returning appid, ret, ticket, and randstr values.

How it works:
    STEP-01 - Configure AsyncCaptchaClient with the API key.
    STEP-02 - Obtain the task parameters. Extract websiteURL, appId, and any non-default captchaScript from the target page, then provide your proxy settings.
    STEP-03 - Create TencentTask and pass it to await solver.solve(task), which creates and polls the task.
    STEP-04 - Print appid, ret, ticket, and randstr values. Applying the solution and verifying acceptance are target-specific.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and appId with values from your target page.
    Pass captchaScript if the site uses a non-default script URL.
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
from captcha_solver_api.tasks import TencentTask

# STEP-01: Configure AsyncCaptchaClient with the API key.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")


async def main():
    async with AsyncCaptchaClient(api_key) as solver:
        # --- With proxy example ---
        # Solves Tencent captcha through your own proxy.
        # Use when the target site is geo-restricted or you need a consistent session.
        try:
            # STEP-02: Obtain the CAPTCHA parameters from the target page and this configuration.
            # STEP-03: Create the task and await solve(), which creates and polls it.
            result = await solver.solve(
                TencentTask(
                    websiteURL="https://example.com/register",  # Full URL of the page with captcha
                    appId="YOUR_APP_ID",  # appId from page source code (required)
                    # --- Proxy parameters (replace with your own -- these are placeholders) ---
                    proxyType="http",  # http, socks4, or socks5
                    proxyAddress="1.2.3.4",  # Proxy IP address
                    proxyPort=8080,  # Proxy port
                    proxyLogin="user",  # Login for proxy authorization (optional)
                    proxyPassword="password",  # Password for proxy authorization (optional)
                    captchaScript="https://captchacdn.tencentcloudcs.com/TCaptcha-global.js",
                )
            )
            # Solution contains the same appid, ret, ticket, and randstr values.
            # STEP-04: Print the solution; applying and verifying it are target-specific.
            print("result: " + str(result))
        except Exception as e:
            sys.exit(e)


asyncio.run(main())
