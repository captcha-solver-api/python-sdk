"""
Example: Solve a click-based image captcha using CoordinatesTask.

This example reads local challenge and instruction images, encodes them as
Base64, describes what the worker should click, and prints the ordered
coordinates returned by the service. No proxy or target page is involved. It
uses CoordinatesTask and CaptchaClient.solve().

How it works:
STEP-01 - Configure CaptchaClient and locate the bundled images.
STEP-02 - Read the image data and create CoordinatesTask without a proxy.
STEP-03 - Call solve(), which creates the task and polls for its solution.
STEP-04 - Print the coordinates to click in the same order, or report the error.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Ready to run as-is: sample captcha images are bundled in examples/assets/.
    Use comment to tell the worker what to click on the image.
    No proxy is required. The image is submitted directly to the service.
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
from captcha_solver_api.tasks import CoordinatesTask

# in this example we store the API key inside environment variables that can be set like:
# export CAPTCHA_API_KEY=your_api_key on Linux or macOS
# set CAPTCHA_API_KEY=your_api_key on Windows
# you can just set the API key directly to its value like:
# api_key="your_api_key"

# STEP-01: Configure CaptchaClient and locate the bundled images.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")

# Create a solver instance with your API key.
solver = CaptchaClient(api_key)

# --- Basic example ---
# Solves a simple click-based captcha (examples/assets/fruit-click.png) with
# a hint for the worker. The worker will click on the specified points on the image.
try:
    # STEP-02: Read the image data and create CoordinatesTask without a proxy.
    # Read and encode the captcha image to base64.
    # The body must be a pure base64 string without the data:image/...;base64, prefix.
    with open(os.path.join(assets_dir, "fruit-click.png"), "rb") as f:
        body = b64encode(f.read()).decode("utf-8")

    # STEP-03: Call solve(), which creates the task and polls for its solution.
    result = solver.solve(
        CoordinatesTask(
            body=body,  # Base64-encoded captcha image (required)
            comment="click on the green apple",  # Text hint for the worker
        )
    )
    # Solution contains {"coordinates": [{"x": 140, "y": 110}]}
    # Click on each coordinate in order. Coordinates are pixel positions.
    # STEP-04: Print the coordinates to click in the same order, or report the error.
    print("result: " + str(result))
except Exception as e:
    sys.exit(e)

# --- Advanced example ---
# Solves a captcha (examples/assets/traffic-lights.png) with instruction image
# and click count limits.
try:
    with open(os.path.join(assets_dir, "traffic-lights.png"), "rb") as f:
        body = b64encode(f.read()).decode("utf-8")

    # Read and encode an optional instruction image.
    # This image helps the worker understand what to click.
    with open(os.path.join(assets_dir, "traffic-lights-instructions.png"), "rb") as f:
        img_instructions = b64encode(f.read()).decode("utf-8")

    result = solver.solve(
        CoordinatesTask(
            body=body,  # Base64-encoded captcha image
            comment="click on all traffic lights",  # Text hint for the worker
            imgInstructions=img_instructions,  # Optional instruction image
            minClicks=1,  # Minimum number of clicks (default 1)
            maxClicks=3,  # Maximum number of clicks allowed
        )
    )
    # Solution contains coordinates for all requested clicks, e.g.
    # {"coordinates": [{"x": 110, "y": 150}, {"x": 430, "y": 130}]}
    print("result: " + str(result))
except Exception as e:
    sys.exit(e)
