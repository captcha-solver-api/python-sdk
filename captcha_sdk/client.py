"""
Main API client for the Captcha Solver service.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional

import requests

from .exceptions import (
    ApiError,
    NetworkError,
    TimeoutError,
    ValidationError,
)


class CaptchaClient:
    """
    Main client for interacting with the Captcha Solver API.

    Example:
        client = CaptchaClient("YOUR_API_KEY")
    """

    def __init__(
        self,
        client_key: str,
        base_url: str = "https://api.captcha-solver.com",
        timeout: int = 120,
        polling_interval: int = 3,
        language_pool: Optional[str] = None,
    ) -> None:
        """
        Args:
            client_key: Your Captcha Solver API key.
            base_url: API base URL. Override only for self-hosted or staging
                deployments.
            timeout: Default max seconds `solve()` waits for a solution before
                raising `TimeoutError`. Can be overridden per call.
            polling_interval: Seconds to wait between `getTaskResult` polls
                inside `solve()`.
            language_pool: Default worker pool selector (e.g. `"en"` or `"ru"`)
                applied to every `create_task()`/`solve()` call that doesn't pass
                its own `language_pool`. Leave unset to use the account's default
                pool.

        Raises:
            ValidationError: `client_key` is empty.
        """
        if not client_key:
            raise ValidationError("client_key is required")

        self.client_key = client_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.polling_interval = polling_interval
        self.language_pool = language_pool

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def close(self) -> None:
        """Closes the underlying connection pool. Call this when you're done with
        the client, or use it as a context manager (`with CaptchaClient(...) as c:`)
        to have it closed automatically."""
        self.session.close()

    def __enter__(self) -> "CaptchaClient":
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.close()

    def _request(
        self,
        endpoint: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
        except requests.exceptions.Timeout as exc:
            raise TimeoutError("Request timed out.") from exc
        except requests.exceptions.RequestException as exc:
            raise NetworkError(str(exc)) from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise NetworkError(f"Non-JSON response from API: {response.text[:200]!r}") from exc

        return data

    def _ensure_success(self, data: Dict[str, Any]) -> None:
        if data.get("errorId", 0) != 0:
            raise ApiError(
                data.get("errorCode", "UNKNOWN_ERROR"),
                data.get("errorDescription", "Unknown API error."),
            )

    def create_task(self, task: Any, language_pool: Optional[str] = None) -> int:
        """Submits a captcha task and returns its task ID without waiting for a solution.

        Calls the `createTask` endpoint. Prefer `solve()` unless you need to manage
        polling yourself (e.g. to check on many tasks from a different process).

        Args:
            task: One of the task objects from `captcha_sdk.tasks` (e.g.
                `RecaptchaV2TaskProxyless`, `ImageToTextTask`).
            language_pool: Worker pool selector, e.g. `"en"` or `"ru"`. Falls back
                to the client's `language_pool` (set at construction) when omitted.

        Returns:
            The numeric task ID to pass to `get_task_result()`.

        Raises:
            ApiError: The API rejected the task (bad key, bad parameters, etc).
            NetworkError: The request failed at the transport level.
            TimeoutError: The HTTP request itself timed out (not the solve).
        """
        payload: Dict[str, Any] = {
            "clientKey": self.client_key,
            "task": task.to_dict(),
        }
        pool = language_pool if language_pool is not None else self.language_pool
        if pool:
            payload["languagePool"] = pool

        data = self._request("createTask", payload)
        self._ensure_success(data)
        return data["taskId"]

    def get_task_result(self, task_id: int) -> Dict[str, Any]:
        """Fetches the current status of a task created with `create_task()`.

        Calls the `getTaskResult` endpoint. This is a single poll, not a wait --
        call it repeatedly (as `solve()` does) until `status` is `"ready"`.

        Args:
            task_id: The ID returned by `create_task()`.

        Returns:
            The raw API response. Always has a `status` key (`"processing"` or
            `"ready"`); when `"ready"`, also has a `solution` dict whose shape
            depends on the task type (e.g. `{"gRecaptchaResponse": "..."}` for
            reCAPTCHA, `{"text": "..."}` for `ImageToTextTask`).

        Raises:
            ApiError: The API reports an error for this task (e.g. it expired).
            NetworkError: The request failed at the transport level.
        """
        payload = {
            "clientKey": self.client_key,
            "taskId": task_id,
        }
        data = self._request("getTaskResult", payload)
        self._ensure_success(data)
        return data

    def get_balance(self) -> float:
        """Fetches the account's current balance.

        Calls the `getBalance` endpoint.

        Returns:
            The available balance, in the account's currency.

        Raises:
            ApiError: The API key is invalid or the account can't be resolved.
            NetworkError: The request failed at the transport level.
        """
        payload = {"clientKey": self.client_key}
        data = self._request("getBalance", payload)
        self._ensure_success(data)
        return data["balance"]

    def solve(
        self,
        task: Any,
        language_pool: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Submits `task` and polls until it's solved. This is the main entry point --
        it wraps `create_task()` and `get_task_result()` so you don't have to poll
        by hand.

        Args:
            task: One of the task objects from `captcha_sdk.tasks`.
            language_pool: Worker pool selector, e.g. `"en"` or `"ru"`. Falls back
                to the client's `language_pool` (set at construction) when omitted.
            timeout: Overrides the client's default polling timeout for this call
                only (useful for captcha types that reliably take longer, e.g.
                classic reCAPTCHA v2), in seconds.

        Returns:
            The `solution` dict once `status` is `"ready"`. Its shape depends on
            the task type -- see the per-type docstrings in `captcha_sdk.tasks`
            or the README's method reference.

        Raises:
            ApiError: The API rejected the task or reported an error while solving.
            TimeoutError: No solution was ready before the deadline.
            NetworkError: A request failed at the transport level.
        """

        task_id = self.create_task(task, language_pool=language_pool)

        deadline = time.time() + (timeout if timeout is not None else self.timeout)

        while time.time() < deadline:
            result = self.get_task_result(task_id)

            if result.get("status") == "ready":
                return result["solution"]

            time.sleep(self.polling_interval)

        raise TimeoutError("Task solving timed out.")
