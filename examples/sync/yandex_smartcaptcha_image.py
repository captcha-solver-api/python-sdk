"""Example: Solve an image-based Yandex SmartCaptcha from bundled local images without a proxy.

What it does:
    This example shows how to solve an image-based Yandex SmartCaptcha from bundled local images without a proxy. It uses YandexSmartCaptchaImageTask and CaptchaClient.solve(), returning pixel coordinates to click.

How it works:
    STEP-01 - Configure CaptchaClient with the API key.
    STEP-02 - Read and encode the bundled challenge and instruction images.
    STEP-03 - Create YandexSmartCaptchaImageTask and call solve(), which creates and polls it.
    STEP-04 - Print the click coordinates; applying them is target-specific.

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


# STEP-01: Configure CaptchaClient with the API key.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")
solver = CaptchaClient(api_key)

try:
    # STEP-02: Read and encode the bundled challenge and instruction images.
    # STEP-03: Create YandexSmartCaptchaImageTask and call solve(), which creates and polls it.
    result = solver.solve(
        YandexSmartCaptchaImageTask(
            image=encode_image("yandex-smartcaptcha-image.png"),
            imgInstructions=encode_image("yandex-smartcaptcha-instructions.png"),
        )
    )
    # Click the returned points on the captcha image in the listed order.
    # Example: {"coordinates": [{"x": 73, "y": 92}, ...]}
    # STEP-04: Print the click coordinates; applying them is target-specific.
    # Recalculate them if the displayed image is scaled or offset from the original.
    print("result: " + str(result))
# Handle errors raised while solving the image-based SmartCaptcha.
except Exception as exc:
    sys.exit(exc)
