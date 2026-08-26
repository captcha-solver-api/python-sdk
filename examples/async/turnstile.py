"""
Example: Solve a Cloudflare Turnstile challenge with the async client.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and websiteKey with values from your target page.
    For Cloudflare Challenge pages, also extract and pass action, data, and pagedata.
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(repo_root)
load_dotenv(os.path.join(repo_root, '.env'))

from captcha_sdk import AsyncCaptchaClient
from captcha_sdk.tasks import TurnstileTaskProxyless, TurnstileTask

api_key = os.getenv('CAPTCHA_API_KEY', 'YOUR_API_KEY')

solver = AsyncCaptchaClient(api_key)


async def main():
    # --- Proxyless example ---
    # Solves Cloudflare Turnstile without a proxy.
    # The token is tied to the User-Agent. If you pass userAgent, use the same
    # User-Agent in your browser or bot when submitting the token.
    try:
        result = await solver.solve(TurnstileTaskProxyless(
            websiteURL='https://example.com/login',    # Full URL of the page with a Turnstile widget
            websiteKey='YOUR_WEBSITE_KEY',               # data-sitekey attribute value
            # Optional fields (pass only if the target site sets them)
            # action='login',                           # Value of data-action attribute
            # data='custom-cdata-value',                # Value of data-cdata attribute
            # pagedata='chl-page-data-value',           # Value of chlPageData parameter
            # userAgent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...',  # Must match the browser submitting the token
        ))
        # Solution contains {"token": "0.zxcv..."}
        # Pass this token to the widget callback or cf-turnstile-response field.
        print('result: ' + str(result))
    except Exception as e:
        sys.exit(e)

    # --- With proxy example ---
    # Solves Cloudflare Turnstile through your own proxy.
    try:
        result = await solver.solve(TurnstileTask(
            websiteURL='https://example.com/login',    # Full URL of the page with Turnstile
            websiteKey='YOUR_WEBSITE_KEY',               # data-sitekey attribute value
            # --- Proxy parameters (replace with your own -- these are placeholders) ---
            proxyType='http',           # http, socks4, or socks5
            proxyAddress='1.2.3.4',     # Proxy IP address
            proxyPort=8080,             # Proxy port
            proxyLogin='user',          # Login for proxy authorization (optional)
            proxyPassword='password',   # Password for proxy authorization (optional)
            # --- Optional fields ---
            # action='login',
            # data='custom-cdata-value',
            # pagedata='chl-page-data-value',
            # userAgent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...',
        ))
        print('result: ' + str(result))
    except Exception as e:
        sys.exit(e)


asyncio.run(main())
