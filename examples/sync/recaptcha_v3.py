"""
Example: Solve a reCAPTCHA v3 challenge.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Replace websiteURL, websiteKey, and minScore with values from your target
    page, and pass pageAction if the site uses it -- this increases the
    chance of the token being accepted.
"""

import os
import sys

from dotenv import load_dotenv

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(repo_root)
load_dotenv(os.path.join(repo_root, '.env'))

from captcha_sdk import CaptchaClient
from captcha_sdk.tasks import RecaptchaV3TaskProxyless

# in this example we store the API key inside environment variables that can be set like:
# export CAPTCHA_API_KEY=1abc234de56fab7c89012d34e56fa7b8 on Linux or macOS
# set CAPTCHA_API_KEY=1abc234de56fab7c89012d34e56fa7b8 on Windows
# you can just set the API key directly to its value like:
# api_key="1abc234de56fab7c89012d34e56fa7b8"

api_key = os.getenv('CAPTCHA_API_KEY', 'YOUR_API_KEY')

# Create a solver instance with your API key.
# reCAPTCHA v3 tasks may take longer to solve. Increase timeout if needed.
solver = CaptchaClient(api_key, timeout=180)

# reCAPTCHA v3 returns a score instead of a pass/fail challenge.
# The higher the minScore you request, the harder and longer the task takes.
# minScore values: 0.3 (fastest), 0.7 (balanced), 0.9 (highest, slowest).
try:
    result = solver.solve(RecaptchaV3TaskProxyless(
        websiteURL='https://example.com/login',      # Full URL of the page with the v3 widget
        websiteKey='YOUR_WEBSITE_KEY',                # Site key of the v3 widget on that page
        minScore=0.3,                               # Minimum acceptable score (0.3, 0.7, or 0.9)
        # Optional fields (pass if the site uses them, increases token acceptance)
        pageAction='homepage',                       # Action set by that page in grecaptcha.execute()
        # isEnterprise=True,                        # Set True for reCAPTCHA v3 Enterprise
        # apiDomain='www.recaptcha.net',            # Set if site loads from recaptcha.net
    ))
    # Solution contains {"gRecaptchaResponse": "03AGdBq..."}
    # Pass this token to the g-recaptcha-response field or grecaptcha callback.
    print('result: ' + str(result))
except Exception as e:
    sys.exit(e)
