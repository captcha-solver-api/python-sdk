"""
Custom exceptions used by the Captcha Solver SDK.
"""


class CaptchaError(Exception):
    """Base exception for all SDK errors."""

    pass


class NetworkError(CaptchaError):
    """Raised when a network request fails."""

    pass


class TimeoutError(CaptchaError):
    """Raised when the operation exceeds the configured timeout."""

    pass


class ApiError(CaptchaError):
    """Raised when the API returns an error."""

    def __init__(self, error_code: str, error_description: str) -> None:
        self.error_code = error_code
        self.error_description = error_description
        super().__init__(f"{error_code}: {error_description}")


class ValidationError(CaptchaError):
    """Raised for client-side argument problems caught before any request is sent."""

    pass