"""Example: Solve reCAPTCHA v2 without a proxy.

What it does:
    This example shows how to solve reCAPTCHA v2 without a proxy. It uses RecaptchaV2TaskProxyless and CaptchaClient.solve(), returning a gRecaptchaResponse token.

How it works:
    STEP-01 - Configure CaptchaClient with the API key and debug logging.
    STEP-02 - Obtain the task parameters. Extract websiteURL and websiteKey from the target page.
    STEP-03 - Create RecaptchaV2TaskProxyless and pass it to solver.solve(task), which creates and polls the task.
    STEP-04 - Print a gRecaptchaResponse token. Applying the solution and verifying acceptance are target-specific.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and websiteKey with values from your target page.
"""

import os
import sys

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
from captcha_solver_api.tasks import RecaptchaV2TaskProxyless

# in this example we store the API key inside environment variables that can be set like:
# export CAPTCHA_API_KEY=your_api_key on Linux or macOS
# set CAPTCHA_API_KEY=your_api_key on Windows
# you can just set the API key directly to its value like:
# api_key="your_api_key"

api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")

# Create a solver instance with your API key.
# Optional: timeout (max seconds to wait for solution, default 120)
# Optional: polling_interval (seconds before and between status checks, default 10)
solver = CaptchaClient(api_key, debug=True)

# --- Proxyless example ---
# Solves reCAPTCHA v2 without a proxy.
# The service uses its own IP addresses.
try:
    # Create a task and wait for the solution.
    # solve() handles task creation, polling, and returns the solution dict.
    result = solver.solve(
        RecaptchaV2TaskProxyless(
            websiteURL="https://example.com/login",  # Full URL of the page with the captcha
            websiteKey="YOUR_WEBSITE_KEY",  # data-sitekey attribute value on that page
            isInvisible=False,  # Set True for invisible reCAPTCHA
        )
    )
    # Solution contains {"gRecaptchaResponse": "03AGdBq..."}
    # Pass this token to the g-recaptcha-response field or widget callback.
    print("result: " + str(result))
except Exception as e:
    sys.exit(e)
