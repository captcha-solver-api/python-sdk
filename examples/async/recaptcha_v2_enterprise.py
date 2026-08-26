"""
Example: Solve a reCAPTCHA v2 Enterprise challenge with the async client.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and websiteKey with values from your target page.
    If the site uses enterprisePayload, extract and pass it or the token may be rejected.
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(repo_root)
load_dotenv(os.path.join(repo_root, '.env'))

from captcha_sdk import AsyncCaptchaClient
from captcha_sdk.tasks import RecaptchaV2EnterpriseTaskProxyless, RecaptchaV2EnterpriseTask

api_key = os.getenv('CAPTCHA_API_KEY', 'YOUR_API_KEY')

solver = AsyncCaptchaClient(api_key)


async def main():
    # --- Proxyless example ---
    # Solves reCAPTCHA v2 Enterprise without a proxy.
    # Enterprise captchas are loaded via the reCAPTCHA Enterprise API.
    # If the site passes extra parameters to grecaptcha.enterprise.render(),
    # you must pass them as enterprisePayload or the token will be rejected.
    try:
        result = await solver.solve(RecaptchaV2EnterpriseTaskProxyless(
            websiteURL='https://example.com/login',                 # Full URL of the Enterprise-protected page
            websiteKey='YOUR_WEBSITE_KEY',                          # data-sitekey attribute value
            isInvisible=False,                          # Set True for invisible reCAPTCHA
            # Optional fields (pass only if the target site requires them)
            # enterprisePayload={'s': 'value-from-page'},  # Extra params from grecaptcha.enterprise.render()
            # apiDomain='recaptcha.net',                    # Set if site loads captcha from recaptcha.net
            # userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',  # Browser User-Agent
            # cookies='session=abc123; token=xyz789',       # Session cookies if needed
        ))
        # Solution contains {"gRecaptchaResponse": "03AGdBq..."}
        # Pass this token to the g-recaptcha-response field or widget callback.
        print('result: ' + str(result))
    except Exception as e:
        sys.exit(e)

    # --- With proxy example ---
    # Solves reCAPTCHA v2 Enterprise through your own proxy.
    # Use when the target site is geo-restricted or you need a consistent session.
    try:
        result = await solver.solve(RecaptchaV2EnterpriseTask(
            websiteURL='https://example.com/login',                 # Full URL of the Enterprise-protected page
            websiteKey='YOUR_WEBSITE_KEY',                          # data-sitekey attribute value
            # --- Proxy parameters (replace with your own -- these are placeholders) ---
            proxyType='http',           # http, socks4, or socks5
            proxyAddress='1.2.3.4',     # Proxy IP address
            proxyPort=8080,             # Proxy port
            proxyLogin='user',          # Login for proxy authorization (optional)
            proxyPassword='password',   # Password for proxy authorization (optional)
            # --- Optional fields ---
            isInvisible=False,
            # enterprisePayload={'s': 'value-from-page'},  # Extra params from grecaptcha.enterprise.render()
            userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',  # Browser User-Agent
            cookies='foo=bar; baz=1',       # Session cookies if needed
        ))
        # Solution contains the same gRecaptchaResponse token.
        print('result: ' + str(result))
    except Exception as e:
        sys.exit(e)


asyncio.run(main())
