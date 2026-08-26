"""
Example: Solve a Yandex SmartCaptcha image challenge.

Prerequisites:
    Set the CAPTCHA_API_KEY environment variable.
    Sample captcha images are bundled in examples/assets/.
    Use imgType="smart_captcha" to select objects by instruction.

NOTE: the bundled sample image (examples/assets/yandex-smartcaptcha-sample.jpg)
already has its click-order hint baked into the image itself (the small icon
row under "Нажмите в таком порядке"), which is why no separate imgInstructions
is passed here -- pass one yourself if your target site shows the instruction
as a separate image instead.
"""

import os
import sys
from base64 import b64encode

from dotenv import load_dotenv

repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(repo_root)
load_dotenv(os.path.join(repo_root, '.env'))
assets_dir = os.path.join(repo_root, 'examples', 'assets')

from captcha_sdk import CaptchaClient
from captcha_sdk.tasks import CoordinatesTask

api_key = os.getenv('CAPTCHA_API_KEY', 'YOUR_API_KEY')

solver = CaptchaClient(api_key)

# --- Selecting objects by instruction (smart_captcha) ---
# The worker selects objects on the captcha image, in the order shown by the
# instruction. imgInstructions is optional -- pass it when your target site
# shows the order as a separate image; this sample image already has the
# order icons baked into the same image, so comment alone is enough here.
try:
    # Read and encode the captcha image to base64.
    # The body must be a pure base64 string without the data:image/...;base64, prefix.
    with open(os.path.join(assets_dir, 'yandex-smartcaptcha-sample.jpg'), 'rb') as f:
        body = b64encode(f.read()).decode('utf-8')

    result = solver.solve(CoordinatesTask(
        body=body,                                                    # Base64-encoded captcha image (required)
        imgType='smart_captcha',                                      # smart_captcha for object selection
        comment='select objects in the order of the instruction',     # Text hint for the worker (recommended)
        # imgInstructions=...,                                        # Optional: pass a separate instruction image, base64-encoded
    ))
    # Solution contains coordinates for each object, in the instructed order, e.g.
    # {"coordinates": [{"x": 411, "y": 479}, {"x": 121, "y": 445}, {"x": 268, "y": 537}, {"x": 295, "y": 422}]}
    print('result: ' + str(result))
except Exception as e:
    sys.exit(e)
