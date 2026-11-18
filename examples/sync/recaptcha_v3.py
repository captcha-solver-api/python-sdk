"""Example: Solve score-based reCAPTCHA v3 without a proxy.

What it does:
    This example shows how to solve score-based reCAPTCHA v3 without a proxy. It uses RecaptchaV3TaskProxyless and CaptchaClient.solve(), returning a gRecaptchaResponse token.

How it works:
    STEP-01 - Configure CaptchaClient with the API key and debug logging.
    STEP-02 - Obtain the task parameters. Extract websiteURL, websiteKey, pageAction, and the required minimum score from the target page.
    STEP-03 - Create RecaptchaV3TaskProxyless and pass it to solver.solve(task), which creates and polls the task.
    STEP-04 - Print a gRecaptchaResponse token. Applying the solution and verifying acceptance are target-specific.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL, websiteKey, and minScore with values from your target
    page, and pass pageAction if the site uses it -- this increases the
    chance of the token being accepted.
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
from captcha_solver_api.tasks import RecaptchaV3TaskProxyless

# in this example we store the API key inside environment variables that can be set like:
# export CAPTCHA_API_KEY=your_api_key on Linux or macOS
# set CAPTCHA_API_KEY=your_api_key on Windows
# you can just set the API key directly to its value like:
# api_key="your_api_key"

api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")

# Create a solver instance with your API key.
# reCAPTCHA v3 tasks may take longer to solve. Increase timeout if needed.
solver = CaptchaClient(api_key, timeout=180, debug=True)

# reCAPTCHA v3 returns a score instead of a pass/fail challenge.
# The higher the minScore you request, the harder and longer the task takes.
# minScore values: 0.3 (fastest), 0.7 (balanced), 0.9 (highest, slowest).
try:
    result = solver.solve(
        RecaptchaV3TaskProxyless(
            websiteURL="https://example.com/login",  # Full URL of the page with the v3 widget
            websiteKey="YOUR_WEBSITE_KEY",  # Site key of the v3 widget on that page
            minScore=0.3,  # Minimum acceptable score (0.3, 0.7, or 0.9)
            # Optional fields (pass if the site uses them, increases token acceptance)
            pageAction="homepage",  # Action set by that page in grecaptcha.execute()
            # isEnterprise=True,                        # Set True for reCAPTCHA v3 Enterprise
            # apiDomain='www.recaptcha.net',            # Set if site loads from recaptcha.net
        )
    )
    # Solution contains {"gRecaptchaResponse": "03AGdBq..."}
    # Pass this token to the g-recaptcha-response field or grecaptcha callback.
    print("result: " + str(result))
except Exception as e:
    sys.exit(e)
