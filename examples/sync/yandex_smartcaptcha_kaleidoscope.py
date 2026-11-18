"""Example: Solve a Yandex smartcaptcha kaleidoscope puzzle from a bundled local image without a proxy.

What it does:
    This example shows how to solve a Yandex SmartCaptcha Kaleidoscope puzzle from a bundled local image without a proxy. It uses YandexSmartCaptchaKaleidoscopeTask and CaptchaClient.solve(), returning the number of slider-arrow clicks.

How it works:
    STEP-01 - Configure CaptchaClient with the API key.
    STEP-02 - Obtain the task parameters. The challenge image comes from examples/assets and the puzzle-step sequence is captured from the challenge.
    STEP-03 - Create YandexSmartCaptchaKaleidoscopeTask and pass it to solver.solve(task), which creates and polls the task.
    STEP-04 - Print the number of slider-arrow clicks. Applying the solution and verifying acceptance are target-specific.

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


# STEP-01: Configure CaptchaClient and locate the bundled challenge image.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")
solver = CaptchaClient(api_key)

try:
    # STEP-02: Encode the image and create a task with the captured puzzle steps.
    # STEP-03: Call solve(), which creates the task and polls for its solution.
    clicks = solver.solve(
        YandexSmartCaptchaKaleidoscopeTask(
            # Base64-encoded Kaleidoscope image (required).
            image=encode_image("yandex-smartcaptcha-kaleidoscope.jpg"),
            # JSON array string captured from this challenge (required).
            # Preserve the original order; the sequence is challenge-specific.
            task="[7,15,14,0,11,6,6,0,11,15,6,10,1,14,3,12,9,0,15,1,5,1,8,11,12,11,0,12,1,10,1,4,14,6,10,6,10,8,3,0,5,9,7,8,0,3,8,0,9,12,12,11,3,0,8,10]",
        )
    )
    # STEP-04: Print the slider-arrow click count, or report the error.
    # Unlike most SDK tasks, this task returns a plain string rather than a dict.
    # Click the Kaleidoscope slider arrow this many times to complete the puzzle.
    # Example: "8"
    print("Slider arrow clicks: " + str(clicks))
except Exception as exc:
    sys.exit(exc)
