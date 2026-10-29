"""Example: Solve an image-based Yandex SmartCaptcha.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    The sample captcha and instruction images are bundled in examples/assets/.
"""

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

from captcha_solver_api import CaptchaClient
from captcha_solver_api.tasks import CoordinatesTask


def encode_image(filename: str) -> str:
    """Return an image from examples/assets as a Base64 string."""
    path = os.path.join(repo_root, "examples", "assets", filename)
    with open(path, "rb") as image_file:
        return b64encode(image_file.read()).decode("utf-8")


api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")
solver = CaptchaClient(api_key)

try:
    result = solver.solve(
        CoordinatesTask(
            body=encode_image("yandex-smartcaptcha-image.png"),
            imgInstructions=encode_image("yandex-smartcaptcha-instructions.png"),
            minClicks=4,
            maxClicks=4,
        )
    )
    # Click the returned points on the captcha image in the listed order.
    # Example: {"coordinates": [{"x": 73, "y": 92}, ...]}
    print("result: " + str(result))
except Exception as exc:
    sys.exit(exc)
