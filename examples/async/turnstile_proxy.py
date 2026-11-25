"""Example: Solve Cloudflare Turnstile through your own proxy.

What it does:
    This example shows how to solve Cloudflare Turnstile through your own proxy. It uses TurnstileTask and AsyncCaptchaClient.solve(), returning a token.

How it works:
    STEP-01 - Configure AsyncCaptchaClient with the API key.
    STEP-02 - Obtain the task parameters. Extract websiteURL, websiteKey, and any Challenge-page action, data, and pagedata values, then provide your proxy settings.
    STEP-03 - Create TurnstileTask and pass it to await solver.solve(task), which creates and polls the task.
    STEP-04 - Print a token. Applying the solution and verifying acceptance are target-specific.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and websiteKey with values from your target page.
    For Cloudflare Challenge pages, also extract and pass action, data, and pagedata.
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
from captcha_solver_api.tasks import TurnstileTask

# STEP-01: Configure AsyncCaptchaClient with the API key.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")


async def main():
    async with AsyncCaptchaClient(api_key) as solver:
        # --- With proxy example ---
        # Solves Cloudflare Turnstile through your own proxy.
        try:
            # STEP-02: Obtain the CAPTCHA parameters from the target page and this configuration.
            # STEP-03: Create the task and await solve(), which creates and polls it.
            result = await solver.solve(
                TurnstileTask(
                    websiteURL="https://example.com/login",  # Full URL of the page with Turnstile
                    websiteKey="YOUR_WEBSITE_KEY",  # data-sitekey attribute value
                    # --- Proxy parameters (replace with your own -- these are placeholders) ---
                    proxyType="http",  # http, socks4, or socks5
                    proxyAddress="1.2.3.4",  # Proxy IP address
                    proxyPort=8080,  # Proxy port
                    proxyLogin="user",  # Login for proxy authorization (optional)
                    proxyPassword="password",  # Password for proxy authorization (optional)
                    # --- Optional fields ---
                    # action='login',
                    # data='custom-cdata-value',
                    # pagedata='chl-page-data-value',
                    # userAgent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...',
                )
            )
            # STEP-04: Print the solution; applying and verifying it are target-specific.
            print("result: " + str(result))
        except Exception as e:
            sys.exit(e)


asyncio.run(main())
