"""Example: Solve GeeTest v4 without a proxy.

What it does:
    This example shows how to solve GeeTest v4 without a proxy. It uses GeeTestTaskProxyless and CaptchaClient.solve(), returning captcha_output and related validation fields.

How it works:
    STEP-01 - Configure CaptchaClient with the API key and debug logging.
    STEP-02 - Obtain the task parameters. Extract websiteURL and captcha_id from the target page.
    STEP-03 - Create GeeTestTaskProxyless and pass it to solver.solve(task), which creates and polls the task.
    STEP-04 - Print captcha_output and related validation fields. Applying the solution and verifying acceptance are target-specific.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and captcha_id with values from your target page.
    GeeTest v4 drops gt/challenge entirely. It uses captcha_id instead, which
    (unlike v3's challenge) is static per site, so it doesn't need to be
    re-fetched for every request.
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
from captcha_solver_api.tasks import GeeTestTaskProxyless

# in this example we store the API key inside environment variables that can be set like:
# export CAPTCHA_API_KEY=your_api_key on Linux or macOS
# set CAPTCHA_API_KEY=your_api_key on Windows
# you can just set the API key directly to its value like:
# api_key="your_api_key"

api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")

# Create a solver instance with your API key.
# GeeTest v4 tasks may take longer. Increase timeout if needed.
solver = CaptchaClient(api_key, timeout=300, polling_interval=10, debug=True)

# --- Proxyless example ---
# Solves GeeTest v4 without a proxy.
# v4 drops gt/challenge. The widget is identified by captcha_id inside initParameters.
try:
    result = solver.solve(
        GeeTestTaskProxyless(
            websiteURL="https://example.com/login",  # Full URL of the page with the GeeTest widget
            version=4,  # Required: must be 4 for this version
            initParameters={  # Required: must contain captcha_id
                "captcha_id": "YOUR_CAPTCHA_ID",  # Static site identifier, from that page
            },
            # Optional fields
            # userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',  # Browser User-Agent
        )
    )
    # Solution contains {"captcha_id": "...", "lot_number": "...", "pass_token": "...", "gen_time": "...", "captcha_output": "..."}
    # Pass these values together into the page's GeeTest v4 callback as-is.
    print("result: " + str(result))
except Exception as e:
    sys.exit(e)
