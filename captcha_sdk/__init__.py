"""
Official Python SDK for the Captcha Solver API.

Example:
    from captcha_sdk import CaptchaClient
    from captcha_sdk.tasks import RecaptchaV2TaskProxyless

    client = CaptchaClient("YOUR_API_KEY")
    task = RecaptchaV2TaskProxyless(
        websiteURL="https://example.com",
        websiteKey="6Le-xxxxxxxxx"
    )
    result = client.solve(task)
"""

from .client import CaptchaClient
from .async_client import AsyncCaptchaClient
from .exceptions import (
    CaptchaError,
    ApiError,
    NetworkError,
    TimeoutError,
    ValidationError,
)

__version__ = "1.1.0"

__all__ = [
    "CaptchaClient",
    "AsyncCaptchaClient",
    "CaptchaError",
    "ApiError",
    "NetworkError",
    "TimeoutError",
    "ValidationError",
]
