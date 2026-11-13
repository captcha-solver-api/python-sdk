"""Run one Image to Text task with sanitized debug logging enabled.

This creates a real, paid CAPTCHA task. Set CAPTCHA_API_KEY in the environment
or in the repository's .env file before running it.

How it works:
STEP-01 - Read the bundled image and create CaptchaClient with debug enabled.
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

api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")
image_path = os.path.join(repo_root, "examples", "assets", "captcha-digits.png")

with open(image_path, "rb") as image_file:
    image_body = b64encode(image_file.read()).decode("utf-8")

with CaptchaClient(api_key, debug=True) as client:
    solution = client.solve(ImageToTextTask(body=image_body, numeric=1, minLength=4, maxLength=6))

# The SOLVE SUMMARY is emitted before solve() returns, so this is printed last.
print(f"Recognized text: {solution['text']}")
