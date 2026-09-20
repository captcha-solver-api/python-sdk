"""
Async counterpart of captcha_solver_api.client.CaptchaClient -- same endpoints
(createTask / getTaskResult / getBalance), same method names/arguments,
`await`ed. Requires httpx.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any, Dict, Optional

import httpx

from ._version import __version__
from .exceptions import (
    ApiError,
    CaptchaTimeoutError,
    NetworkError,
    ValidationError,
)


class AsyncCaptchaClient:
    """
    Async client for interacting with the Captcha Solver API.

    Holds a single, reused `httpx.AsyncClient` connection pool for the
    lifetime of the instance (created once, not per request), so repeated
    calls -- especially the `getTaskResult` polling inside `solve()` --
    reuse the same keep-alive connection instead of paying a fresh TCP/TLS
    handshake every time. Close it with `aclose()` when you're done, or use
    it as an async context manager:

    Example:
        async with AsyncCaptchaClient("YOUR_API_KEY") as client:
            result = await client.solve(task)
    """

    def __init__(
        self,
        client_key: str,
        base_url: str = "https://api.captcha-solver.com",
        timeout: int = 120,
        polling_interval: int = 10,
        language_pool: Optional[str] = None,
    ) -> None:
        """
        Args:
            client_key: Your Captcha Solver API key.
            base_url: API base URL. Override only for self-hosted or staging
                deployments.
            timeout: Default max seconds `solve()` waits for a solution before
                raising `CaptchaTimeoutError`. Can be overridden per call.
            polling_interval: Seconds to wait before the first `getTaskResult`
                poll and between subsequent polls inside `solve()`. Defaults
                to 10 seconds.
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

        self._client = httpx.AsyncClient(
            follow_redirects=True,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-SDK": f"python-sdk/{__version__}",
            },
        )

    async def aclose(self) -> None:
        """Closes the underlying connection pool. Call this when you're done with
        the client, or use it as an async context manager
        (`async with AsyncCaptchaClient(...) as c:`) to have it closed automatically."""
        await self._client.aclose()

    async def __aenter__(self) -> AsyncCaptchaClient:
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        await self.aclose()

    async def _request(
        self,
        endpoint: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = await self._client.post(url, json=payload, timeout=30)
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise CaptchaTimeoutError("Request timed out.") from exc
        except httpx.HTTPError as exc:
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

    async def create_task(self, task: Any, language_pool: Optional[str] = None) -> int:
        """Submit a CAPTCHA task and return its ID without waiting for a solution.

        This calls the API `createTask` endpoint. Use `solve()` for the usual
        submit-and-wait flow, or use this method when polling must be managed
        separately, for example when checking several tasks from another process.
        See the `createTask` and CAPTCHA type details in the
        `https://captcha-solver.com/en/docs/captcha-types` documentation.

        Args:
            task: A task object from `captcha_solver_api.tasks`.
            language_pool: Optional worker pool selector such as `"en"` or
                `"ru"`. Falls back to the client's configured pool.

        Returns:
            The numeric task ID to pass to `get_task_result()`.

        Raises:
            ApiError: The API rejected the task or its parameters.
            NetworkError: The request failed at the transport level.
            CaptchaTimeoutError: The HTTP request timed out.
        """
        payload: Dict[str, Any] = {
            "clientKey": self.client_key,
            "task": task.to_dict(),
        }
        pool = language_pool if language_pool is not None else self.language_pool
        if pool:
            payload["languagePool"] = pool

        data = await self._request("createTask", payload)
        self._ensure_success(data)
        return data["taskId"]

    async def get_task_result(self, task_id: int) -> Dict[str, Any]:
        """Fetch the current status of a previously submitted task.

        This performs one asynchronous poll of `getTaskResult`; it does not
        wait until the task is ready. Call it repeatedly until the response has
        `status == "ready"`, or use `solve()` to handle polling automatically.
        See `https://captcha-solver.com/en/docs/captcha-types` for the response
        fields returned by each CAPTCHA type.

        Args:
            task_id: The ID returned by `create_task()`.

        Returns:
            The raw API response with `status`; ready responses also contain a
            solution dictionary.

        Raises:
            ApiError: The API reports an error for the task.
            NetworkError: The request failed at the transport level.
            CaptchaTimeoutError: The HTTP request timed out.
        """
        payload = {
            "clientKey": self.client_key,
            "taskId": task_id,
        }
        data = await self._request("getTaskResult", payload)
        self._ensure_success(data)
        return data

    async def get_balance(self) -> float:
        """Fetch the account's current balance asynchronously.

        Calls the `getBalance` endpoint. See the API documentation at
        `https://captcha-solver.com/en/docs/captcha-types` for account and API
        requirements.

        Returns:
            The available balance in the account's currency.

        Raises:
            ApiError: The API key is invalid or the account cannot be resolved.
            NetworkError: The request failed at the transport level.
            CaptchaTimeoutError: The HTTP request timed out.
        """
        payload = {"clientKey": self.client_key}
        data = await self._request("getBalance", payload)
        self._ensure_success(data)
        return data["balance"]

    async def solve(
        self,
        task: Any,
        language_pool: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Submit a task and asynchronously poll until its solution is ready.

        This is the main entry point for the async client. It combines
        `create_task()` and repeated `get_task_result()` calls, waiting between
        polls without blocking the event loop. For several concurrent solves,
        create multiple coroutines and await them with `asyncio.gather()`.
        See the CAPTCHA-specific request and response formats at
        `https://captcha-solver.com/en/docs/captcha-types`.

        Args:
            task: A task object from `captcha_solver_api.tasks`.
            language_pool: Optional worker pool selector. Falls back to the
                client's configured pool.
            timeout: Maximum polling time for this call, in seconds. Overrides
                the client's default timeout.

        Returns:
            The solution dictionary once the task status becomes `"ready"`.

        Raises:
            ApiError: The API rejected the task or reported a solving error.
            CaptchaTimeoutError: No solution was ready before the deadline.
            NetworkError: A request failed at the transport level.
        """

        task_id = await self.create_task(task, language_pool=language_pool)

        deadline = time.monotonic() + (timeout if timeout is not None else self.timeout)

        while time.monotonic() < deadline:
            remaining = deadline - time.monotonic()
            await asyncio.sleep(min(self.polling_interval, max(0, remaining)))
            if time.monotonic() >= deadline:
                break
            result = await self.get_task_result(task_id)

            if result.get("status") == "ready":
                return result["solution"]

        raise CaptchaTimeoutError("Task solving timed out.")
