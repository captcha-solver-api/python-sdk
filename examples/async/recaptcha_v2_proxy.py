"""
Example: Solve a reCAPTCHA v2 challenge through your own proxy with the async client.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and websiteKey with values from your target page.
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
from captcha_solver_api.tasks import RecaptchaV2Task

api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")

# Optional: timeout (max seconds to wait for solution, default 120)
# Optional: polling_interval (seconds before and between status checks, default 10)
solver = AsyncCaptchaClient(api_key)


async def main():
    # --- With proxy example ---
    # Solves reCAPTCHA v2 through your own proxy.
    # Use when the target site is geo-restricted or you need session consistency.
    try:
        result = await solver.solve(
            RecaptchaV2Task(
                websiteURL="https://example.com/login",  # Full URL of the page with captcha
                websiteKey="YOUR_WEBSITE_KEY",  # data-sitekey attribute value
                # --- Proxy parameters (replace with your own -- these are placeholders) ---
                proxyType="http",  # http, socks4, or socks5
                proxyAddress="1.2.3.4",  # Proxy IP address
                proxyPort=8080,  # Proxy port
                proxyLogin="user",  # Login for proxy authorization (optional)
                proxyPassword="password",  # Password for proxy authorization (optional)
            )
        )
        # Solution contains the same gRecaptchaResponse token.
        print("result: " + str(result))
    except Exception as e:
        sys.exit(e)


asyncio.run(main())
