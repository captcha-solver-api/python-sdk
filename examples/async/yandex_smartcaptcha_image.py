"""Example: Solve an image-based Yandex SmartCaptcha asynchronously.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    The sample captcha and instruction images are bundled in examples/assets/.
"""

import asyncio
import os
import sys
from base64 import b64encode

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
from captcha_solver_api.tasks import YandexSmartCaptchaImageTask


def encode_image(filename: str) -> str:
    """Return an image from examples/assets as a Base64 string."""
    path = os.path.join(repo_root, "examples", "assets", filename)
    with open(path, "rb") as image_file:
        return b64encode(image_file.read()).decode("utf-8")


async def main() -> None:
    api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")
    async with AsyncCaptchaClient(api_key) as solver:
        result = await solver.solve(
            YandexSmartCaptchaImageTask(
                image=encode_image("yandex-smartcaptcha-image.png"),
                imgInstructions=encode_image("yandex-smartcaptcha-instructions.png"),
            )
        )
    # Click the returned points on the captcha image in the listed order.
    # Example: {"coordinates": [{"x": 73, "y": 92}, ...]}
    print("result: " + str(result))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as exc:
        sys.exit(exc)
