"""
Example: Solve a Yandex SmartCaptcha image challenge.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Sample captcha images are bundled in examples/assets/.
    Use imgType="smart_captcha" to select objects by instruction.

The API documentation requires imgInstructions for smart_captcha. The bundled
screenshot contains both the captcha and its visual instruction, so this example
uses it for both fields. For a target page with a separate instruction image,
encode that image and pass it as imgInstructions instead.
"""

import os
import sys
from base64 import b64encode

try:
    from dotenv import load_dotenv
except ModuleNotFoundError as exc:
    if exc.name != 'dotenv':
        raise
    load_dotenv = None

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(repo_root)
if load_dotenv is not None:
    load_dotenv(os.path.join(repo_root, '.env'))
assets_dir = os.path.join(repo_root, 'examples', 'assets')

from captcha_solver_api import CaptchaClient
from captcha_solver_api.tasks import CoordinatesTask

api_key = os.getenv('CAPTCHA_API_KEY', 'YOUR_API_KEY')

solver = CaptchaClient(api_key)

# --- Selecting objects by instruction (smart_captcha) ---
# The worker selects objects in the order shown by the instruction.
# This screenshot includes the instruction row below the captcha.
try:
    # Read and encode the captcha image to base64.
    # The body must be a pure base64 string without the data:image/...;base64, prefix.
    with open(os.path.join(assets_dir, 'yandex-smartcaptcha-sample.jpg'), 'rb') as f:
        body = b64encode(f.read()).decode('utf-8')

    result = solver.solve(CoordinatesTask(
        body=body,                                                    # Base64-encoded captcha image (required)
        imgType='smart_captcha',                                      # smart_captcha for object selection
        comment='select objects in the order of the instruction',     # Text hint for the worker (recommended)
        imgInstructions=body,                                        # The sample screenshot also contains the instruction
    ))
    # Solution contains coordinates for each object, in the instructed order, e.g.
    # {"coordinates": [{"x": 411, "y": 479}, {"x": 121, "y": 445}, {"x": 268, "y": 537}, {"x": 295, "y": 422}]}
    print('result: ' + str(result))
except Exception as e:
    sys.exit(e)
