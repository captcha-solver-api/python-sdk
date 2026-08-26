"""
Example: Solve a GeeTest v3 challenge.

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
from dotenv import load_dotenv

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(repo_root)
load_dotenv(os.path.join(repo_root, '.env'))

from captcha_sdk import CaptchaClient
from captcha_sdk.tasks import GeeTestTaskProxyless, GeeTestTask

# in this example we store the API key inside environment variables that can be set like:
# export CAPTCHA_API_KEY=1abc234de56fab7c89012d34e56fa7b8 on Linux or macOS
# set CAPTCHA_API_KEY=1abc234de56fab7c89012d34e56fa7b8 on Windows
# you can just set the API key directly to its value like:
# api_key="1abc234de56fab7c89012d34e56fa7b8"

api_key = os.getenv('CAPTCHA_API_KEY', 'YOUR_API_KEY')

# Create a solver instance with your API key.
# GeeTest tasks may take longer. Increase timeout if needed.
solver = CaptchaClient(api_key, timeout=300, polling_interval=10)

"""
Important: the value of the 'challenge' parameter is dynamic.
For each request to the API you need to get a new value from the target page.
Below is an example of fetching it from a demo endpoint.
"""
# Fetch a fresh challenge value from the target page.
# In production, extract this from the page's initGeetest call or network requests.
# "target-site.com" is a placeholder -- point this at your real target before running.
resp = requests.get("https://target-site.com/path/to/geetest/init", timeout=30)
challenge = resp.json()['challenge']

# --- Proxyless example ---
# Solves GeeTest v3 without a proxy.
# v3 is the default version, so the version field can be omitted.
try:
    result = solver.solve(GeeTestTaskProxyless(
        websiteURL='https://example.com/login',    # Full URL of the page with GeeTest
        gt='f2ae6cadcf7886856696c46d84d109d1',     # Public key of the GeeTest widget
        challenge=challenge,                        # Session-specific value, must be fresh
        # Optional fields
        # geetestApiServerSubdomain='api-na.geetest.com',  # Custom API subdomain
        # initParameters={...},                              # Extra params from initGeetest call
        # userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',  # Browser User-Agent
    ))
    # Solution contains {"challenge": "...", "validate": "...", "seccode": "..."}
    # Pass solution.validate and solution.seccode to the page's GeeTest callback.
    print('result: ' + str(result))
except Exception as e:
    sys.exit(e)

# --- With proxy example ---
# Solves GeeTest v3 through your own proxy.
try:
    result = solver.solve(GeeTestTask(
        websiteURL='https://example.com/login',    # Full URL of the page with GeeTest
        gt='f2ae6cadcf7886856696c46d84d109d1',     # Public key of the GeeTest widget
        challenge=challenge,                        # Session-specific value, must be fresh
        # --- Proxy parameters (replace with your own -- these are placeholders) ---
        proxyType='http',           # http, socks4, or socks5
        proxyAddress='1.2.3.4',     # Proxy IP address
        proxyPort=8080,             # Proxy port
        proxyLogin='user',          # Login for proxy authorization (optional)
        proxyPassword='password',   # Password for proxy authorization (optional)
    ))
    print('result: ' + str(result))
except Exception as e:
    sys.exit(e)
