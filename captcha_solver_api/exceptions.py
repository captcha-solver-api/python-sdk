"""
Custom exceptions used by the Captcha Solver SDK.
"""

from typing import Optional


class CaptchaError(Exception):
    """Base exception for all SDK errors.

    Catch this to handle `ApiError`, `NetworkError`, `CaptchaTimeoutError`, and
    `ValidationError` together.

    Attributes:
        task_id: ID of the task the error relates to, or `None` if it was raised
            before a task was created (for example, by `createTask` or
            `getBalance`). Errors from `solve()` and `get_task_result()` set it,
            so you can keep polling the same task with `get_task_result()` or
            mention it when contacting support.

    Example:
        try:
            solution = client.solve(task)
        except CaptchaTimeoutError as exc:
            print("Task", exc.task_id, "is not ready yet")
    """

    def __init__(self, *args: object, task_id: Optional[int] = None) -> None:
        super().__init__(*args)
        self.task_id = task_id


class NetworkError(CaptchaError):
    """An HTTP request failed or the API returned an invalid response.

    Includes HTTP error statuses, non-JSON responses, unexpected response
    shapes, and ready tasks whose solution is not a dictionary.
    """


class CaptchaTimeoutError(CaptchaError):
    """An HTTP request timed out or the task's polling deadline was reached.

    `solve(timeout=...)` overrides the polling timeout; each HTTP request uses
    a separate 30-second timeout. `TimeoutError` is a deprecated alias of this
    class; prefer `CaptchaTimeoutError` to avoid shadowing Python's built-in.
    """


# Deprecated alias kept for backward compatibility. It shadows the built-in
# ``TimeoutError`` when imported by name, so prefer ``CaptchaTimeoutError``.
TimeoutError = CaptchaTimeoutError


class ApiError(CaptchaError):
    """The API returned a nonzero `errorId`.

    Args:
        error_code: Machine-readable API `errorCode`.
        error_description: Human-readable API `errorDescription`.

    Attributes:
        error_code: Error code to use when deciding how to handle the failure.
        error_description: Explanation supplied by the API.

    Example:
        try:
            solution = client.solve(task)
        except ApiError as exc:
            print(exc.error_code, exc.error_description)
    """

    def __init__(
        self,
        error_code: str,
        error_description: str,
        task_id: Optional[int] = None,
    ) -> None:
        self.error_code = error_code
        self.error_description = error_description
        super().__init__(f"{error_code}: {error_description}", task_id=task_id)


class ValidationError(CaptchaError):
    """Raised for client-side argument problems caught before any request is sent."""
