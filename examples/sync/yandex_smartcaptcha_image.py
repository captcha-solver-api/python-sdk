"""Example: Solve an image-based Yandex SmartCaptcha.

This example reads a local Yandex SmartCaptcha image and its instruction image,
encodes both as Base64, sends them directly without a proxy, and prints the
ordered click coordinates. It uses YandexSmartCaptchaImageTask and
CaptchaClient.solve().

How it works:
STEP-01 - Configure CaptchaClient and locate the bundled challenge images.
STEP-02 - Encode both images and create YandexSmartCaptchaImageTask.
STEP-03 - Call solve(), which creates the task and polls for its solution.
STEP-04 - Print the ordered coordinates to click, or report the error.

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
from captcha_solver_api.tasks import YandexSmartCaptchaImageTask


def encode_image(filename: str) -> str:
    """Return an image from examples/assets as a Base64 string."""
    path = os.path.join(repo_root, "examples", "assets", filename)
    with open(path, "rb") as image_file:
        return b64encode(image_file.read()).decode("utf-8")


# STEP-01: Configure CaptchaClient and locate the bundled challenge images.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")
solver = CaptchaClient(api_key)

# STEP-02: Encode both images and create YandexSmartCaptchaImageTask.
try:
    # STEP-03: Call solve(), which creates the task and polls for its solution.
    result = solver.solve(
        YandexSmartCaptchaImageTask(
            image=encode_image("yandex-smartcaptcha-image.png"),
            imgInstructions=encode_image("yandex-smartcaptcha-instructions.png"),
        )
    )
    # STEP-04: Print the ordered coordinates to click, or report the error.
    # Click the returned points on the captcha image in the listed order.
    # Example: {"coordinates": [{"x": 73, "y": 92}, ...]}
    print("result: " + str(result))
except Exception as exc:
    sys.exit(exc)
