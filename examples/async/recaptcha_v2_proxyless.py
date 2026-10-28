"""Example: Solve reCAPTCHA v2 without your own proxy using the async client."""

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
from captcha_solver_api.tasks import RecaptchaV2TaskProxyless

api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")
solver = AsyncCaptchaClient(api_key)


async def main():
    task = RecaptchaV2TaskProxyless(
        websiteURL="https://example.com/login",
        websiteKey="YOUR_WEBSITE_KEY",
    )
    try:
        result = await solver.solve(task)
    except Exception as exc:
        sys.exit(str(exc))
    else:
        print("result: " + str(result))


asyncio.run(main())
