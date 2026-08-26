"""
Example: Solve a GeeTest v4 challenge with the async client.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and captcha_id with values from your target page.
    GeeTest v4 drops gt/challenge entirely. It uses captcha_id instead, which
    (unlike v3's challenge) is static per site, so it doesn't need to be
    re-fetched for every request.
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(repo_root)
load_dotenv(os.path.join(repo_root, '.env'))

from captcha_sdk import AsyncCaptchaClient
from captcha_sdk.tasks import GeeTestTaskProxyless, GeeTestTask

api_key = os.getenv('CAPTCHA_API_KEY', 'YOUR_API_KEY')

# GeeTest v4 tasks may take longer. Increase timeout if needed.
solver = AsyncCaptchaClient(api_key, timeout=300, polling_interval=10)


async def main():
    # --- Proxyless example ---
    # Solves GeeTest v4 without a proxy.
    # v4 drops gt/challenge. The widget is identified by captcha_id inside initParameters.
    try:
        result = await solver.solve(GeeTestTaskProxyless(
            websiteURL='https://example.com/login',      # Full URL of the page with the GeeTest widget
            version=4,                                  # Required: must be 4 for this version
            initParameters={                            # Required: must contain captcha_id
                'captcha_id': 'YOUR_CAPTCHA_ID',          # Static site identifier, from that page
            },
            # Optional fields
            # userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',  # Browser User-Agent
        ))
        # Solution contains {"captcha_id": "...", "lot_number": "...", "pass_token": "...", "gen_time": "...", "captcha_output": "..."}
        # Pass these values together into the page's GeeTest v4 callback as-is.
        print('result: ' + str(result))
    except Exception as e:
        sys.exit(e)

    # --- With proxy example ---
    # Solves GeeTest v4 through your own proxy.
    try:
        result = await solver.solve(GeeTestTask(
            websiteURL='https://example.com/login',      # Full URL of the page with the GeeTest widget
            version=4,                                  # Required: must be 4 for this version
            initParameters={                            # Required: must contain captcha_id
                'captcha_id': 'YOUR_CAPTCHA_ID',          # Static site identifier, from that page
            },
            # --- Proxy parameters ---
            proxyType='http',           # http, socks4, or socks5
            proxyAddress='1.2.3.4',     # Proxy IP address
            proxyPort=8080,             # Proxy port
            proxyLogin='user',          # Login for proxy authorization (optional)
            proxyPassword='password',   # Password for proxy authorization (optional)
        ))
        print('result: ' + str(result))
    except Exception as e:
        sys.exit(e)


asyncio.run(main())
