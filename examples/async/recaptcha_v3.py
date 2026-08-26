"""
Example: Solve a reCAPTCHA v3 challenge with the async client.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL, websiteKey, and minScore with values from your target
    page, and pass pageAction if the site uses it -- this increases the
    chance of the token being accepted.
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(repo_root)
load_dotenv(os.path.join(repo_root, '.env'))

from captcha_sdk import AsyncCaptchaClient
from captcha_sdk.tasks import RecaptchaV3TaskProxyless

api_key = os.getenv('CAPTCHA_API_KEY', 'YOUR_API_KEY')

# reCAPTCHA v3 tasks may take longer to solve. Increase timeout if needed.
solver = AsyncCaptchaClient(api_key, timeout=180)


async def main():
    # reCAPTCHA v3 returns a score instead of a pass/fail challenge.
    # The higher the minScore you request, the harder and longer the task takes.
    # minScore values: 0.3 (fastest), 0.7 (balanced), 0.9 (highest, slowest).
    try:
        result = await solver.solve(RecaptchaV3TaskProxyless(
            websiteURL='https://example.com/login',      # Full URL of the page with the v3 widget
            websiteKey='YOUR_WEBSITE_KEY',                # Site key of the v3 widget on that page
            minScore=0.3,                               # Minimum acceptable score (0.3, 0.7, or 0.9)
            # Optional fields (pass if the site uses them, increases token acceptance)
            pageAction='homepage',                       # Action set by that page in grecaptcha.execute()
            # isEnterprise=True,                        # Set True for reCAPTCHA v3 Enterprise
            # apiDomain='www.recaptcha.net',            # Set if site loads from recaptcha.net
        ))
        # Solution contains {"gRecaptchaResponse": "03AGdBq..."}
        # Pass this token to the g-recaptcha-response field or grecaptcha callback.
        print('result: ' + str(result))
    except Exception as e:
        sys.exit(e)


asyncio.run(main())
