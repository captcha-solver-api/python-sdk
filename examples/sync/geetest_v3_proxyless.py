"""Example: Solve GeeTest v3 without a proxy.

What it does:
    This example shows how to solve GeeTest v3 without a proxy. It uses GeeTestTaskProxyless and CaptchaClient.solve(), returning challenge, validate, and seccode values.

How it works:
    STEP-01 - Configure CaptchaClient with the API key.
    STEP-02 - Fetch a fresh challenge and supply websiteURL and gt.
    STEP-03 - Create GeeTestTaskProxyless and pass it to solver.solve(), which creates and polls the task.
    STEP-04 - Print challenge, validate, and seccode; applying and verifying them are target-specific.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL, gt, and challenge with values from your target page.
    Important: the challenge value is dynamic. Fetch a fresh one for each request.

    NOTE: "https://target-site.com/path/to/geetest/init" below is a PLACEHOLDER, not a
    real endpoint -- this script will not run end-to-end as-is. Replace it with a request
    to your actual target page (or wherever it exposes a fresh `challenge` value) before
    running this example. It's here only to illustrate where that fetch belongs in the flow.
"""

import os
import sys

import requests

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

# STEP-01: Configure CaptchaClient with the API key.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")

# Create a solver instance with your API key.
# GeeTest tasks may take longer. Increase timeout if needed.
solver = CaptchaClient(api_key, timeout=300, polling_interval=10)

"""
Important: the value of the 'challenge' parameter is dynamic.
For each request to the API you need to get a new value from the target page.
Below is an example of fetching it from a demo endpoint.
"""
# STEP-02: Fetch a fresh challenge and supply websiteURL and gt.
# In production, extract this from the page's initGeetest call or network requests.
# "target-site.com" is a placeholder -- point this at your real target before running.
resp = requests.get("https://target-site.com/path/to/geetest/init", timeout=30)
challenge = resp.json()["challenge"]

# Solves GeeTest v3 without a proxy.
# v3 is the default version, so the version field can be omitted.
try:
    # STEP-03: Create GeeTestTaskProxyless and pass it to solver.solve(), which creates and polls the task.
    result = solver.solve(
        GeeTestTaskProxyless(
            websiteURL="https://example.com/login",  # Full URL of the page with GeeTest
            gt="f2ae6cadcf7886856696c46d84d109d1",  # Public key of the GeeTest widget
            challenge=challenge,  # Session-specific value, must be fresh
            # Optional fields
            # geetestApiServerSubdomain='api-na.geetest.com',  # Custom API subdomain
            # initParameters={...},                              # Extra params from initGeetest call
            # userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',  # Browser User-Agent
        )
    )
    # Solution contains {"challenge": "...", "validate": "...", "seccode": "..."}
    # Pass solution.validate and solution.seccode to the page's GeeTest callback.
    # STEP-04: Print challenge, validate, and seccode; applying and verifying them are target-specific.
    print("result: " + str(result))
# Handle errors raised while solving the CAPTCHA.
except Exception as e:
    sys.exit(e)
