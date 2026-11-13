"""
Example: Solve a GeeTest v4 challenge.

This example solves GeeTest v4 without a customer proxy. Obtain captcha_id from
the target's v4 loader and pass it in initParameters; the returned v4 fields
must be applied and verified through the target's own flow. It uses
GeeTestTaskProxyless with version 4 and CaptchaClient.solve().

How it works:
STEP-01 - Configure CaptchaClient and obtain captcha_id from the target's v4 loader.
STEP-02 - Create GeeTestTaskProxyless with version 4 and call solve().
STEP-03 - Print the returned v4 fields and explain their site-specific application.
STEP-04 - Report errors; page acceptance must be verified by the integration.

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
from examples._cli import debug_enabled

# in this example we store the API key inside environment variables that can be set like:
# export CAPTCHA_API_KEY=your_api_key on Linux or macOS
# set CAPTCHA_API_KEY=your_api_key on Windows
# you can just set the API key directly to its value like:
# api_key="your_api_key"

# STEP-01: Configure CaptchaClient and obtain captcha_id from the target's v4 loader.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")

# Create a solver instance with your API key.
# GeeTest v4 tasks may take longer. Increase timeout if needed.
solver = CaptchaClient(api_key, debug=debug_enabled(), timeout=300, polling_interval=10)

# --- Proxyless example ---
# Solves GeeTest v4 without a proxy.
# v4 drops gt/challenge. The widget is identified by captcha_id inside initParameters.
try:
    # STEP-02: Create GeeTestTaskProxyless with version 4 and call solve().
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
    # STEP-03: Print the returned v4 fields and explain their site-specific application.
    # Solution contains {"captcha_id": "...", "lot_number": "...", "pass_token": "...", "gen_time": "...", "captcha_output": "..."}
    # Pass these values together into the page's GeeTest v4 callback as-is.
    print("result: " + str(result))
except Exception as e:
    # STEP-04: Report errors; page acceptance must be verified by the integration.
    sys.exit(e)
