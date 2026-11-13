"""
Example: Solve an image captcha with the async client.

How it works:
STEP-01 - Configure AsyncCaptchaClient and locate the bundled images.
STEP-02 - Read an image as Base64 and create ImageToTextTask with answer hints.
STEP-03 - Await solve(), which creates the task and polls for its solution.
STEP-04 - Print the recognized text, or report the error.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Ready to run as-is: sample captcha images are bundled in examples/assets/.
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
assets_dir = os.path.join(repo_root, "examples", "assets")

from captcha_solver_api import AsyncCaptchaClient
from captcha_solver_api.tasks import ImageToTextTask

api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")


def encode_image(filename):
    """Read an image from examples/assets and return it as a base64 string.

    The body must be a pure base64 string without the data:image/...;base64, prefix.
    """
    with open(os.path.join(assets_dir, filename), "rb") as f:
        return b64encode(f.read()).decode("utf-8")


async def main():
    # STEP-01: Configure AsyncCaptchaClient and locate the bundled images.
    # Image to Text tasks are usually fast. Default timeout is fine.
    async with AsyncCaptchaClient(api_key) as solver:
        digits_body = encode_image("captcha-digits.png")

        # --- Basic example ---
        # Solves a simple 5-digit image captcha (examples/assets/captcha-digits.png)
        # with character set hints.
        try:
            # STEP-02: Read an image as Base64 and create ImageToTextTask with answer hints.
            # STEP-03: Await solve(), which creates the task and polls for its solution.
            result = await solver.solve(
                ImageToTextTask(
                    body=digits_body,  # Base64-encoded image (required)
                    numeric=1,  # 1 = digits only
                    minLength=4,  # Minimum expected answer length
                    maxLength=6,  # Maximum expected answer length
                )
            )
            # Solution contains {"text": "58204"}
            # Submit solution.text to the target form field.
            # STEP-04: Print the recognized text, or report the error.
            print("result: " + str(result))
        except Exception as e:
            sys.exit(e)

        # --- Advanced example ---
        # Solves a math captcha (examples/assets/captcha-math.png) with comment and
        # instruction image (examples/assets/captcha-math-instructions.png).
        try:
            result = await solver.solve(
                ImageToTextTask(
                    body=encode_image("captcha-math.png"),  # Base64-encoded captcha image
                    # Optional fields (pass only if needed by the captcha type)
                    phrase=False,  # True if answer has multiple words
                    case=True,  # True if answer is case-sensitive
                    numeric=0,  # 0 = not specified, 1 = digits, 2 = letters, 3 = any with digits, 4 = any with letters
                    math=True,  # True if image is a math expression to solve
                    minLength=1,  # Minimum answer length
                    maxLength=10,  # Maximum answer length
                    comment="Enter the result of the equation",  # Text hint for the worker
                    # Optional instruction image for the worker
                    imgInstructions=encode_image("captcha-math-instructions.png"),
                )
            )
            print("result: " + str(result))
        except Exception as e:
            sys.exit(e)

        # --- With language pool ---
        # The languagePool parameter selects the worker pool by language.
        # Pass it to solve() as a top-level parameter, not inside the task.
        # Accepted values: "en" (English) or "ru" (Russian).
        try:
            result = await solver.solve(
                ImageToTextTask(body=digits_body, numeric=1, minLength=4, maxLength=6),
                language_pool="en",  # Picks English-speaking worker pool
            )
            print("result: " + str(result))
        except Exception as e:
            sys.exit(e)


asyncio.run(main())
