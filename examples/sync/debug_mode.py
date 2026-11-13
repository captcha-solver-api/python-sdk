"""Run one Image to Text task with optional sanitized debug logging.

This example reads a bundled image as Base64, enables the SDK's opt-in debug
mode when run with --debug, solves the image task, and prints the recognized
text after the sanitized request/response events and SOLVE SUMMARY. It uses
ImageToTextTask and CaptchaClient.solve().

This creates a real, paid CAPTCHA task. Set CAPTCHA_API_KEY in the environment
or in the repository's .env file before running it.

How it works:
STEP-01 - Read the bundled image and create CaptchaClient with optional debug logging.
STEP-02 - Create ImageToTextTask and call solve().
STEP-03 - Inspect the sanitized debug events and SOLVE SUMMARY.
STEP-04 - Print the recognized text returned by the service.
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
from examples._cli import debug_enabled

# STEP-01: Read the bundled image and create CaptchaClient with debug enabled.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")
image_path = os.path.join(repo_root, "examples", "assets", "captcha-digits.png")

with open(image_path, "rb") as image_file:
    image_body = b64encode(image_file.read()).decode("utf-8")

with CaptchaClient(api_key, debug=debug_enabled()) as client:
    # STEP-02: Create ImageToTextTask and call solve().
    solution = client.solve(ImageToTextTask(body=image_body, numeric=1, minLength=4, maxLength=6))

# STEP-03: Inspect the sanitized debug events and SOLVE SUMMARY.
# STEP-04: Print the recognized text returned by the service.
# The SOLVE SUMMARY is emitted before solve() returns, so this is printed last.
print(f"Recognized text: {solution['text']}")
