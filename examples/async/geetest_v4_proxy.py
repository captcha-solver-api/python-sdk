"""Example: Solve GeeTest v4 through your own proxy.

What it does:
    This example shows how to solve GeeTest v4 through your own proxy. It uses GeeTestTask and AsyncCaptchaClient.solve(), returning captcha_output and related validation fields.

How it works:
    STEP-01 - Configure AsyncCaptchaClient with the API key.
    STEP-02 - Obtain the task parameters. Extract websiteURL and captcha_id from the target page and provide your proxy settings.
    STEP-03 - Create GeeTestTask and pass it to await solver.solve(task), which creates and polls the task.
    STEP-04 - Print captcha_output and related validation fields. Applying the solution and verifying acceptance are target-specific.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and captcha_id with values from your target page.
    GeeTest v4 drops gt/challenge entirely. It uses captcha_id instead, which
    (unlike v3's challenge) is static per site, so it doesn't need to be
    re-fetched for every request.
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
from captcha_solver_api.tasks import GeeTestTask

# STEP-01: Configure AsyncCaptchaClient with the API key.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")


async def main():
    # GeeTest v4 tasks may take longer. Increase timeout if needed.
    async with AsyncCaptchaClient(api_key, timeout=300, polling_interval=10) as solver:
        # --- With proxy example ---
        # Solves GeeTest v4 through your own proxy.
        try:
            # STEP-02: Obtain the CAPTCHA parameters from the target page and this configuration.
            # STEP-03: Create the task and await solve(), which creates and polls it.
            result = await solver.solve(
                GeeTestTask(
                    websiteURL="https://example.com/login",  # Full URL of the page with the GeeTest widget
                    version=4,  # Required: must be 4 for this version
                    initParameters={  # Required: must contain captcha_id
                        "captcha_id": "YOUR_CAPTCHA_ID",  # Static site identifier, from that page
                    },
                    # --- Proxy parameters ---
                    proxyType="http",  # http, socks4, or socks5
                    proxyAddress="1.2.3.4",  # Proxy IP address
                    proxyPort=8080,  # Proxy port
                    proxyLogin="user",  # Login for proxy authorization (optional)
                    proxyPassword="password",  # Password for proxy authorization (optional)
                )
            )
            # STEP-04: Print the solution; applying and verifying it are target-specific.
            print("result: " + str(result))
        except Exception as e:
            sys.exit(e)


asyncio.run(main())
