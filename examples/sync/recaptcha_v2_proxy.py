"""Example: Solve reCAPTCHA v2 through your own proxy.

What it does:
    This example shows how to solve reCAPTCHA v2 through your own proxy. It uses RecaptchaV2Task and CaptchaClient.solve(), returning a gRecaptchaResponse token.

How it works:
    STEP-01 - Configure CaptchaClient with the API key and debug logging.
    STEP-02 - Obtain the task parameters. Extract websiteURL and websiteKey from the target page and provide your proxy settings.
    STEP-03 - Create RecaptchaV2Task and pass it to solver.solve(task), which creates and polls the task.
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
from captcha_solver_api.tasks import RecaptchaV2Task

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

# --- With proxy example ---
# Solves reCAPTCHA v2 through your own proxy.
# Required when the target site is geo-restricted or you need session consistency.
try:
    result = solver.solve(
        RecaptchaV2Task(
            websiteURL="https://example.com/login",  # Full URL of the page with captcha
            websiteKey="YOUR_WEBSITE_KEY",  # data-sitekey attribute value
            # --- Proxy parameters (replace with your own -- these are placeholders) ---
            proxyType="http",  # http, socks4, or socks5
            proxyAddress="1.2.3.4",  # Proxy IP address
            proxyPort=8080,  # Proxy port
            proxyLogin="user",  # Login for proxy authorization (optional)
            proxyPassword="password",  # Password for proxy authorization (optional)
        )
    )
    # Solution contains the same gRecaptchaResponse token.
    print("result: " + str(result))
except Exception as e:
    sys.exit(e)
