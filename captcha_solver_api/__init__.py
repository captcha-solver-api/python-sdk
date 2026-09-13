"""
Official Python SDK for the Captcha Solver API.

Example:
    from captcha_solver_api import CaptchaClient
    from captcha_solver_api.tasks import RecaptchaV2TaskProxyless

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
    CaptchaTimeoutError,
    TimeoutError,
    ValidationError,
)

from ._version import __version__

__all__ = [
    "CaptchaClient",
    "AsyncCaptchaClient",
    "CaptchaError",
    "ApiError",
    "NetworkError",
    "CaptchaTimeoutError",
    "TimeoutError",
    "ValidationError",
]
