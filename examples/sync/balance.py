"""Example: Check the current Captcha Solver account balance without creating a CAPTCHA task.

What it does:
    This example shows how to check the current Captcha Solver account balance without creating a CAPTCHA task. It uses CaptchaClient.get_balance() and returns the account balance.

How it works:
    STEP-01 - Configure CaptchaClient with the API key.
    STEP-02 - Call solver.get_balance(); this does not create or poll a CAPTCHA task.
    STEP-03 - Print the balance returned by the API.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
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

# in this example we store the API key inside environment variables that can be set like:
# export CAPTCHA_API_KEY=your_api_key on Linux or macOS
# set CAPTCHA_API_KEY=your_api_key on Windows
# you can just set the API key directly to its value like:
# api_key="your_api_key"

# STEP-01: Configure CaptchaClient with the API key.
api_key = os.getenv("CAPTCHA_API_KEY", "YOUR_API_KEY")

# Create a solver instance with your API key.
solver = CaptchaClient(api_key)

# Get the current account balance.
# Returns a float with the available amount in your account currency.
try:
    # STEP-02: Call solver.get_balance(); this does not create or poll a CAPTCHA task.
    balance = solver.get_balance()
    # STEP-03: Print the balance returned by the API.
    print("Balance: " + str(balance))
# Handle errors raised while requesting the balance.
except Exception as e:
    sys.exit(e)
