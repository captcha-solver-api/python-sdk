"""
Custom exceptions used by the Captcha Solver SDK.
"""


class CaptchaError(Exception):
    """Base exception for all SDK errors."""


class NetworkError(CaptchaError):
    """Raised when a network request fails."""


class CaptchaTimeoutError(CaptchaError):
    """Raised when the operation exceeds the configured timeout."""


# Deprecated alias kept for backward compatibility. It shadows the built-in
# ``TimeoutError`` when imported by name, so prefer ``CaptchaTimeoutError``.
TimeoutError = CaptchaTimeoutError


class ApiError(CaptchaError):
    """Raised when the API returns an error."""

    def __init__(self, error_code: str, error_description: str) -> None:
        self.error_code = error_code
        self.error_description = error_description
        super().__init__(f"{error_code}: {error_description}")


class ValidationError(CaptchaError):
    """Raised for client-side argument problems caught before any request is sent."""
