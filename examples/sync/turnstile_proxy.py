"""Example: Solve Cloudflare Turnstile through your own proxy.

What it does:
    This example shows how to solve Cloudflare Turnstile through your own proxy. It uses TurnstileTask and CaptchaClient.solve(), returning a token.

How it works:
    STEP-01 - Configure CaptchaClient with the API key.
    STEP-02 - Provide websiteURL, websiteKey, Challenge data when required, and proxy settings.
    STEP-03 - Create TurnstileTask and pass it to solver.solve(), which creates and polls the task.
    STEP-04 - Print the Turnstile token; applying and verifying it are target-specific.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and websiteKey with values from your target page.
    For Cloudflare Challenge pages, also extract and pass action, data, and pagedata.
    Replace the proxy placeholders with your own proxy settings.
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
from captcha_solver_api.tasks import TurnstileTask

# in this example we store the API key inside environment variables that can be set like:
# export CAPTCHA_API_KEY=your_api_key on Linux or macOS
# set CAPTCHA_API_KEY=your_api_key on Windows
# you can just set the API key directly to its value like:
# api_key="your_api_key"

# STEP-01: Configure CaptchaClient with the API key.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")

# Create a solver instance with your API key.
solver = CaptchaClient(api_key)

# Solves Cloudflare Turnstile through your own proxy.
try:
    # STEP-02: Provide websiteURL, websiteKey, Challenge data when required, and proxy settings.
    # STEP-03: Create TurnstileTask and pass it to solver.solve(), which creates and polls the task.
    result = solver.solve(
        TurnstileTask(
            websiteURL="https://example.com/login",  # Full URL of the page with Turnstile
            websiteKey="YOUR_WEBSITE_KEY",  # data-sitekey attribute value
            # Proxy connection used by the service; replace every placeholder.
            proxyType="http",  # http, socks4, or socks5
            proxyAddress="1.2.3.4",  # Proxy IP address
            proxyPort=8080,  # Proxy port
            proxyLogin="user",  # Login for proxy authorization (optional)
            proxyPassword="password",  # Password for proxy authorization (optional)
            # Optional Challenge fields; pass only values extracted from the target page.
            # action='login',
            # data='custom-cdata-value',
            # pagedata='chl-page-data-value',
            # userAgent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...',
        )
    )
    # STEP-04: Print the Turnstile token; applying and verifying it are target-specific.
    print("result: " + str(result))
# Handle errors raised while solving the CAPTCHA.
except Exception as e:
    sys.exit(e)
