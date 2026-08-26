"""
Example: Solve an image captcha with the async client.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Ready to run as-is: sample captcha image is bundled in examples/assets/.
"""

import asyncio
import os
import sys
from base64 import b64encode

from dotenv import load_dotenv

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(repo_root)
load_dotenv(os.path.join(repo_root, '.env'))
assets_dir = os.path.join(repo_root, 'examples', 'assets')

from captcha_sdk import AsyncCaptchaClient
from captcha_sdk.tasks import ImageToTextTask

api_key = os.getenv('CAPTCHA_API_KEY', 'YOUR_API_KEY')

solver = AsyncCaptchaClient(api_key)


async def main():
    # Base64 body must not include the data:image/...;base64, prefix.
    with open(os.path.join(assets_dir, 'captcha-digits.png'), 'rb') as f:
        body = b64encode(f.read()).decode('utf-8')

    task = ImageToTextTask(body=body, numeric=1, minLength=4, maxLength=6)

    try:
        result = await solver.solve(task)
    except Exception as e:
        sys.exit(str(e))
    else:
        # Solution contains {"text": "58204"}
        print('result: ' + str(result))


asyncio.run(main())
