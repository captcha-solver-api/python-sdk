"""
Example: Solve a reCAPTCHA v2 challenge.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and websiteKey with values from your target page.
"""

import os
import sys

from dotenv import load_dotenv

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(repo_root)
load_dotenv(os.path.join(repo_root, '.env'))

from captcha_sdk import CaptchaClient
from captcha_sdk.tasks import RecaptchaV2TaskProxyless, RecaptchaV2Task

# in this example we store the API key inside environment variables that can be set like:
# export CAPTCHA_API_KEY=1abc234de56fab7c89012d34e56fa7b8 on Linux or macOS
# set CAPTCHA_API_KEY=1abc234de56fab7c89012d34e56fa7b8 on Windows
# you can just set the API key directly to its value like:
# api_key="1abc234de56fab7c89012d34e56fa7b8"

api_key = os.getenv('CAPTCHA_API_KEY', 'YOUR_API_KEY')

# Create a solver instance with your API key.
# Optional: timeout (max seconds to wait for solution, default 120)
# Optional: polling_interval (seconds between status checks, default 3)
solver = CaptchaClient(api_key)

# --- Proxyless example ---
# Solves reCAPTCHA v2 without a proxy.
# The service uses its own IP addresses.
try:
    # Create a task and wait for the solution.
    # solve() handles task creation, polling, and returns the solution dict.
    result = solver.solve(RecaptchaV2TaskProxyless(
        websiteURL='https://example.com/login',      # Full URL of the page with the captcha
        websiteKey='YOUR_WEBSITE_KEY',                # data-sitekey attribute value on that page
        isInvisible=False,                          # Set True for invisible reCAPTCHA
    ))
    # Solution contains {"gRecaptchaResponse": "03AGdBq..."}
    # Pass this token to the g-recaptcha-response field or widget callback.
    print('result: ' + str(result))
except Exception as e:
    sys.exit(e)

# --- With proxy example ---
# Solves reCAPTCHA v2 through your own proxy.
# Required when the target site is geo-restricted or you need session consistency.
try:
    result = solver.solve(RecaptchaV2Task(
        websiteURL='https://example.com/login',      # Full URL of the page with captcha
        websiteKey='YOUR_WEBSITE_KEY',                # data-sitekey attribute value
        # --- Proxy parameters (replace with your own -- these are placeholders) ---
        proxyType='http',           # http, socks4, or socks5
        proxyAddress='1.2.3.4',     # Proxy IP address
        proxyPort=8080,             # Proxy port
        proxyLogin='user',          # Login for proxy authorization (optional)
        proxyPassword='password',   # Password for proxy authorization (optional)
    ))
    # Solution contains the same gRecaptchaResponse token.
    print('result: ' + str(result))
except Exception as e:
    sys.exit(e)