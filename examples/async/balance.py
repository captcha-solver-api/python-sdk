"""
Example: Get account balance with the async client.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Returns the current available balance of your account.
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(repo_root)
load_dotenv(os.path.join(repo_root, '.env'))

from captcha_sdk import AsyncCaptchaClient

# in this example we store the API key inside environment variables that can be set like:
# export CAPTCHA_API_KEY=1abc234de56fab7c89012d34e56fa7b8 on Linux or macOS
# set CAPTCHA_API_KEY=1abc234de56fab7c89012d34e56fa7b8 on Windows
# you can just set the API key directly to its value like:
# api_key="1abc234de56fab7c89012d34e56fa7b8"

api_key = os.getenv('CAPTCHA_API_KEY', 'YOUR_API_KEY')

solver = AsyncCaptchaClient(api_key)


async def main():
    # Get the current account balance.
    # Returns a float with the available amount in your account currency.
    try:
        balance = await solver.get_balance()
        print('Balance: ' + str(balance))
    except Exception as e:
        sys.exit(e)


asyncio.run(main())
