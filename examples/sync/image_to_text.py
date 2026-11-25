"""Example: Recognize text in bundled local CAPTCHA images without a proxy.

What it does:
    This example shows how to recognize text in bundled local CAPTCHA images without a proxy. It uses ImageToTextTask and CaptchaClient.solve(), returning the recognized text.

How it works:
    STEP-01 - Configure CaptchaClient with the API key.
    STEP-02 - Obtain the task parameters. The images and answer-format hints come from examples/assets and this file.
    STEP-03 - Create ImageToTextTask and pass it to solver.solve(task), which creates and polls the task.
    STEP-04 - Print the recognized text. Applying the solution and verifying acceptance are target-specific.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Ready to run as-is: sample captcha images are bundled in examples/assets/.
    Use optional fields to give hints to the worker for faster solving.
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
assets_dir = os.path.join(repo_root, "examples", "assets")

from captcha_solver_api import CaptchaClient
from captcha_solver_api.tasks import ImageToTextTask

# in this example we store the API key inside environment variables that can be set like:
# export CAPTCHA_API_KEY=your_api_key on Linux or macOS
# set CAPTCHA_API_KEY=your_api_key on Windows
# you can just set the API key directly to its value like:
# api_key="your_api_key"

# STEP-01: Configure CaptchaClient with the API key.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")

# Create a solver instance with your API key.
# Image to Text tasks are usually fast. Default timeout is fine.
solver = CaptchaClient(api_key)

# STEP-02: Read the bundled images and answer-format hints.
# Basic scenario: recognize a digit-only CAPTCHA.
# Solves a simple 5-digit image captcha (examples/assets/captcha-digits.png)
# with character set hints.
try:
    # Read and encode the captcha image to base64.
    # The body must be a pure base64 string without the data:image/...;base64, prefix.
    with open(os.path.join(assets_dir, "captcha-digits.png"), "rb") as f:
        digits_body = b64encode(f.read()).decode("utf-8")

    # STEP-03: Create ImageToTextTask and call solve(), which creates and polls it.
    result = solver.solve(
        ImageToTextTask(
            body=digits_body,  # Base64-encoded image (required)
            numeric=1,  # 1 = digits only
            minLength=4,  # Minimum expected answer length
            maxLength=6,  # Maximum expected answer length
        )
    )
    # Solution contains {"text": "58204"}
    # Submit solution.text to the target form field.
    # STEP-04: Print the recognized text; applying it is target-specific.
    print("result: " + str(result))
except Exception as e:
    sys.exit(e)

# Alternative scenario: solve a math CAPTCHA with an instruction image.
# Solves a math captcha (examples/assets/captcha-math.png) with comment and
# instruction image (examples/assets/captcha-math-instructions.png).
try:
    with open(os.path.join(assets_dir, "captcha-math.png"), "rb") as f:
        math_body = b64encode(f.read()).decode("utf-8")

    # Read the hint image as base64.
    with open(os.path.join(assets_dir, "captcha-math-instructions.png"), "rb") as f:
        img_instructions = b64encode(f.read()).decode("utf-8")

    result = solver.solve(
        ImageToTextTask(
            body=math_body,  # Base64-encoded captcha image
            # Optional fields (pass only if needed by the captcha type)
            phrase=False,  # True if answer has multiple words
            case=True,  # True if answer is case-sensitive
            numeric=0,  # 0 = not specified, 1 = digits, 2 = letters, 3 = any with digits, 4 = any with letters
            math=True,  # True if image is a math expression to solve
            minLength=1,  # Minimum answer length
            maxLength=10,  # Maximum answer length
            comment="Enter the result of the equation",  # Text hint for the worker
            imgInstructions=img_instructions,  # Optional instruction image for the worker
        )
    )
    print("result: " + str(result))
except Exception as e:
    sys.exit(e)

# Alternative scenario: select a language-specific worker pool.
# The languagePool parameter selects the worker pool by language.
# Pass it to solve() as a top-level parameter, not inside the task.
# Accepted values: "en" (English) or "ru" (Russian).
try:
    result = solver.solve(
        ImageToTextTask(
            body=digits_body,
            numeric=1,
            minLength=4,
            maxLength=6,
        ),
        language_pool="en",  # Picks English-speaking worker pool
    )
    print("result: " + str(result))
except Exception as e:
    sys.exit(e)
