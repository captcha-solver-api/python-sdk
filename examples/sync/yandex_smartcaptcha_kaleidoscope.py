"""Example: Solve a Yandex SmartCaptcha Kaleidoscope puzzle.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    The sample image is bundled in examples/assets/.
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
from captcha_solver_api.tasks import YandexSmartCaptchaKaleidoscopeTask


def encode_image(filename: str) -> str:
    """Return an image from examples/assets as a Base64 string."""
    path = os.path.join(repo_root, "examples", "assets", filename)
    with open(path, "rb") as image_file:
        return b64encode(image_file.read()).decode("utf-8")


api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")
solver = CaptchaClient(api_key)

try:
    clicks = solver.solve(
        YandexSmartCaptchaKaleidoscopeTask(
            image=encode_image("yandex-smartcaptcha-kaleidoscope.jpg"),
            task="[7,15,14,0,11,6,6,0,11,15,6,10,1,14,3,12,9,0,15,1,5,1,8,11,12,11,0,12,1,10,1,4,14,6,10,6,10,8,3,0,5,9,7,8,0,3,8,0,9,12,12,11,3,0,8,10]",
        )
    )
    print("Slider arrow clicks: " + str(clicks))
except Exception as exc:
    sys.exit(exc)
