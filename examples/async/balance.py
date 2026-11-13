"""
Example: Get account balance with the async client.

This example creates AsyncCaptchaClient, requests the current account balance
without creating a CAPTCHA task, and prints the returned amount. It uses
AsyncCaptchaClient.get_balance().

How it works:
STEP-01 - Configure the API key and create AsyncCaptchaClient.
STEP-02 - Request the balance with get_balance() without creating a CAPTCHA task.
STEP-03 - Print the returned amount or report the error.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Returns the current available balance of your account.
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
from examples._cli import debug_enabled

# in this example we store the API key inside environment variables that can be set like:
# export CAPTCHA_API_KEY=your_api_key on Linux or macOS
# set CAPTCHA_API_KEY=your_api_key on Windows
# you can just set the API key directly to its value like:
# api_key="your_api_key"

# STEP-01: Configure the API key and create AsyncCaptchaClient.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")


async def main():
    async with AsyncCaptchaClient(api_key, debug=debug_enabled()) as solver:
        # STEP-02: Request the balance with get_balance() without creating a CAPTCHA task.
        # Get the current account balance.
        # Returns a float with the available amount in your account currency.
        try:
            balance = await solver.get_balance()
            # STEP-03: Print the returned amount or report the error.
            print("Balance: " + str(balance))
        except Exception as e:
            sys.exit(e)


asyncio.run(main())
