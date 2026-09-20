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

from ._version import __version__
from .async_client import AsyncCaptchaClient
from .client import CaptchaClient
from .exceptions import (
    ApiError,
    CaptchaError,
    CaptchaTimeoutError,
    NetworkError,
    TimeoutError,
    ValidationError,
)

__all__ = [
    "ApiError",
    "AsyncCaptchaClient",
    "CaptchaClient",
    "CaptchaError",
    "CaptchaTimeoutError",
    "NetworkError",
    "TimeoutError",
    "ValidationError",
    "__version__",
]
