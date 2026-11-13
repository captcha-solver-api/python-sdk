"""
Example: Solve a Tencent captcha challenge.

This example solves Tencent CAPTCHA through your own proxy. Obtain appId and any
custom captchaScript from the target page, provide the proxy details, and pass
the returned ticket and randstr to the page-specific callback. It uses
TencentTask and CaptchaClient.solve(); callback delivery alone is not proof of
server-side acceptance.

How it works:
STEP-01 - Configure CaptchaClient, Tencent parameters, and customer proxy credentials.
STEP-02 - Create TencentTask and call solve() through that proxy.
STEP-03 - Print ticket and randstr and explain their site-specific application.
STEP-04 - Report errors; page or server acceptance must be verified by the integration.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and appId with values from your target page.
    Pass captchaScript if the site uses a non-default script URL.
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
from captcha_solver_api.tasks import TencentTask

# STEP-01: Configure CaptchaClient, Tencent parameters, and customer proxy credentials.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")

solver = CaptchaClient(api_key)

# --- With proxy example ---
# Solves Tencent captcha through your own proxy.
# Use when the target site is geo-restricted or you need a consistent session.
try:
    # STEP-02: Create TencentTask and call solve() through that proxy.
    result = solver.solve(
        TencentTask(
            websiteURL="https://example.com/register",  # Full URL of the page with captcha
            appId="YOUR_APP_ID",  # appId from page source code (required)
            # --- Proxy parameters (replace with your own -- these are placeholders) ---
            proxyType="http",  # http, socks4, or socks5
            proxyAddress="1.2.3.4",  # Proxy IP address
            proxyPort=8080,  # Proxy port
            proxyLogin="user",  # Login for proxy authorization (optional)
            proxyPassword="password",  # Password for proxy authorization (optional)
            captchaScript="https://captchacdn.tencentcloudcs.com/TCaptcha-global.js",
        )
    )
    # STEP-03: Print ticket and randstr and explain their site-specific application.
    # Solution contains the same appid, ret, ticket, and randstr values.
    print("result: " + str(result))
except Exception as e:
    # STEP-04: Report errors; page or server acceptance must be verified by the integration.
    sys.exit(e)
