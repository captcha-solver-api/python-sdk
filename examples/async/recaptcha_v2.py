"""
Example: Solve reCAPTCHA v2 with the async client.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    httpx must be installed (it's a package dependency, so `pip install captcha-solver-api` covers it).
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(repo_root)
load_dotenv(os.path.join(repo_root, '.env'))

from captcha_solver_api import AsyncCaptchaClient
from captcha_solver_api.tasks import RecaptchaV2TaskProxyless

api_key = os.getenv('CAPTCHA_API_KEY', 'YOUR_API_KEY')

solver = AsyncCaptchaClient(api_key)


async def main():
    task = RecaptchaV2TaskProxyless(
        websiteURL='https://example.com/login',  # Full URL of the page with the captcha
        websiteKey='YOUR_WEBSITE_KEY',            # data-sitekey attribute value on that page
    )

    try:
        result = await solver.solve(task)
    except Exception as e:
        sys.exit(str(e))
    else:
        print('result: ' + str(result))


asyncio.run(main())
