"""
Example: Solve a Tencent captcha challenge.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and appId with values from your target page.
    Pass captchaScript if the site uses a non-default script URL.
"""

import os
import sys

from dotenv import load_dotenv

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(repo_root)
load_dotenv(os.path.join(repo_root, '.env'))

from captcha_sdk import CaptchaClient
from captcha_sdk.tasks import TencentTaskProxyless, TencentTask

api_key = os.getenv('CAPTCHA_API_KEY', 'YOUR_API_KEY')

solver = CaptchaClient(api_key)

# --- Proxyless example ---
# Solves Tencent captcha without a proxy.
# The service's own proxies are used to solve the captcha.
# appId is found in the page source code. captchaScript is optional if the site uses the default.
try:
    result = solver.solve(TencentTaskProxyless(
        websiteURL='https://example.com/register',  # Full URL of the page using Tencent captcha
        appId='YOUR_APP_ID',                        # appId from page source code (required)
        # Optional fields:
        captchaScript='https://captchacdn.tencentcloudcs.com/TCaptcha-global.js',  # Custom script URL if non-default
    ))
    # Solution contains {"appid": "...", "ret": 0, "ticket": "...", "randstr": "..."}
    # Pass all four values together into the page's captcha callback as-is.
    print('result: ' + str(result))
except Exception as e:
    sys.exit(e)

# --- With proxy example ---
# Solves Tencent captcha through your own proxy.
# Use when the target site is geo-restricted or you need a consistent session.
try:
    result = solver.solve(TencentTask(
        websiteURL='https://example.com/register',  # Full URL of the page with captcha
        appId='YOUR_APP_ID',                        # appId from page source code (required)
        # --- Proxy parameters (replace with your own -- these are placeholders) ---
        proxyType='http',           # http, socks4, or socks5
        proxyAddress='1.2.3.4',     # Proxy IP address
        proxyPort=8080,             # Proxy port
        proxyLogin='user',          # Login for proxy authorization (optional)
        proxyPassword='password',   # Password for proxy authorization (optional)
        captchaScript='https://captchacdn.tencentcloudcs.com/TCaptcha-global.js',
    ))
    # Solution contains the same appid, ret, ticket, and randstr values.
    print('result: ' + str(result))
except Exception as e:
    sys.exit(e)
