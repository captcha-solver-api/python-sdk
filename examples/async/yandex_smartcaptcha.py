"""
Example: Solve a Yandex SmartCaptcha challenge (token-based) with the async client.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and websiteKey with values from your target page.
    This example uses the token-based method. For image-based solving, see yandex_smartcaptcha_image.py.
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(repo_root)
load_dotenv(os.path.join(repo_root, '.env'))

from captcha_sdk import AsyncCaptchaClient
from captcha_sdk.tasks import YandexSmartCaptchaTaskProxyless, YandexSmartCaptchaTask

api_key = os.getenv('CAPTCHA_API_KEY', 'YOUR_API_KEY')

solver = AsyncCaptchaClient(api_key)


async def main():
    # --- Proxyless example ---
    # Solves Yandex SmartCaptcha without a proxy.
    # The service's own proxies are used to solve the captcha.
    # websiteKey is the sitekey value from the page code or captcha iframe.
    try:
        result = await solver.solve(YandexSmartCaptchaTaskProxyless(
            websiteURL='https://example.com/login',                      # Full URL of the page using SmartCaptcha
            websiteKey='YOUR_WEBSITE_KEY',                                # sitekey from that page
            # Optional fields:
            # userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',  # Browser User-Agent
            # cookies='session=abc123; token=xyz789',                     # Session cookies if needed
        ))
        # Solution contains {"token": "dV9xNjYyNTU3NjkxO4k9OTQuNVMuMjkuMjM9..."}
        # Use solution.token in the smart-token field or pass to your site's backend.
        print('result: ' + str(result))
    except Exception as e:
        sys.exit(e)

    # --- With proxy example ---
    # Solves Yandex SmartCaptcha through your own proxy.
    # Note: this is the only captcha type where an https proxy is accepted.
    try:
        result = await solver.solve(YandexSmartCaptchaTask(
            websiteURL='https://example.com/login',                      # Full URL of the page using SmartCaptcha
            websiteKey='YOUR_WEBSITE_KEY',                                # sitekey from that page
            # --- Proxy parameters (replace with your own -- these are placeholders) ---
            proxyType='http',           # http, https, socks4, or socks5 (https is accepted only for this type)
            proxyAddress='1.2.3.4',     # Proxy IP address
            proxyPort=8080,             # Proxy port
            proxyLogin='user',          # Login for proxy authorization (optional)
            proxyPassword='password',   # Password for proxy authorization (optional)
            # Optional fields:
            # userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',  # Browser User-Agent
            # cookies='session=abc123; token=xyz789',                     # Session cookies if needed
        ))
        # Solution contains the same token.
        print('result: ' + str(result))
    except Exception as e:
        sys.exit(e)


asyncio.run(main())
