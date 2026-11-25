"""Example: Run one Image to Text task with sanitized debug logging enabled.

What it does:
    This example reads a bundled CAPTCHA image, enables debug mode explicitly,
    solves it with ImageToTextTask and CaptchaClient.solve(), and prints the
    recognized text after the diagnostic events and SOLVE SUMMARY.

How it works:
    STEP-01 - Configure CaptchaClient with debug=True and read the bundled image.
    STEP-02 - Encode the image and create ImageToTextTask.
    STEP-03 - Call solve(), which creates and polls the task while logging safely.
    STEP-04 - Inspect the sanitized logs and print the recognized text.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable or add it to the repository .env.
    This example creates a real, paid CAPTCHA task.
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
from captcha_solver_api.tasks import ImageToTextTask

# STEP-01: Configure CaptchaClient with debug mode and locate the bundled image.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")
image_path = os.path.join(repo_root, "examples", "assets", "captcha-digits.png")

# STEP-02: Encode the image and create ImageToTextTask.
with open(image_path, "rb") as image_file:
    image_body = b64encode(image_file.read()).decode("utf-8")

# STEP-03: Call solve(), which creates and polls the task while logging safely.
with CaptchaClient(api_key, debug=True) as client:
    solution = client.solve(ImageToTextTask(body=image_body, numeric=1, minLength=4, maxLength=6))

# STEP-04: Inspect the sanitized logs and print the recognized text.
print(f"Recognized text: {solution['text']}")
