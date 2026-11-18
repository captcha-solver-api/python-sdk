"""Example: Solve reCAPTCHA v2 enterprise without a proxy.

What it does:
    This example shows how to solve reCAPTCHA v2 Enterprise without a proxy. It uses RecaptchaV2EnterpriseTaskProxyless and CaptchaClient.solve(), returning a gRecaptchaResponse token.

How it works:
    STEP-01 - Configure CaptchaClient with the API key.
    STEP-02 - Obtain the task parameters. Extract websiteURL, websiteKey, and any enterprisePayload from the target page.
    STEP-03 - Create RecaptchaV2EnterpriseTaskProxyless and pass it to solver.solve(task), which creates and polls the task.
    STEP-04 - Print a gRecaptchaResponse token. Applying the solution and verifying acceptance are target-specific.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL and websiteKey with values from your target page.
    If the site uses enterprisePayload, extract and pass it or the token may be rejected.
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
from captcha_solver_api.tasks import RecaptchaV2EnterpriseTaskProxyless

# in this example we store the API key inside environment variables that can be set like:
# export CAPTCHA_API_KEY=your_api_key on Linux or macOS
# set CAPTCHA_API_KEY=your_api_key on Windows
# you can just set the API key directly to its value like:
# api_key="your_api_key"

api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")

# Create a solver instance with your API key.
solver = CaptchaClient(api_key)

# --- Proxyless example ---
# Solves reCAPTCHA v2 Enterprise without a proxy.
# Enterprise captchas are loaded via the reCAPTCHA Enterprise API.
# If the site passes extra parameters to grecaptcha.enterprise.render(),
# you must pass them as enterprisePayload or the token will be rejected.
try:
    result = solver.solve(
        RecaptchaV2EnterpriseTaskProxyless(
            websiteURL="https://example.com/login",  # Full URL of the Enterprise-protected page
            websiteKey="YOUR_WEBSITE_KEY",  # data-sitekey attribute value
            isInvisible=False,  # Set True for invisible reCAPTCHA
            # Optional fields (pass only if the target site requires them)
            # enterprisePayload={'s': 'value-from-page'},  # Extra params from grecaptcha.enterprise.render()
            # apiDomain='recaptcha.net',                    # Set if site loads captcha from recaptcha.net
            # userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',  # Browser User-Agent
            # cookies='session=abc123; token=xyz789',       # Session cookies if needed
        )
    )
    # Solution contains {"gRecaptchaResponse": "03AGdBq..."}
    # Pass this token to the g-recaptcha-response field or widget callback.
    print("result: " + str(result))
except Exception as e:
    sys.exit(e)
