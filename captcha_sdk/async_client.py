"""
Async counterpart of captcha_sdk.client.CaptchaClient -- same endpoints
(createTask / getTaskResult / getBalance), same method names/arguments,
`await`ed. Requires httpx.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any, Dict, Optional

import httpx

from .exceptions import (
    ApiError,
    NetworkError,
    TimeoutError,
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

        self._client = httpx.AsyncClient(
            follow_redirects=True,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )

    async def aclose(self) -> None:
        """Closes the underlying connection pool. Call this when you're done with
        the client, or use it as an async context manager
        (`async with AsyncCaptchaClient(...) as c:`) to have it closed automatically."""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncCaptchaClient":
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
            raise TimeoutError("Request timed out.") from exc
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
        """See `captcha_sdk.client.CaptchaClient.create_task` -- same semantics, awaited."""
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
        """See `captcha_sdk.client.CaptchaClient.get_task_result` -- same semantics, awaited."""
        payload = {
            "clientKey": self.client_key,
            "taskId": task_id,
        }
        data = await self._request("getTaskResult", payload)
        self._ensure_success(data)
        return data

    async def get_balance(self) -> float:
        """See `captcha_sdk.client.CaptchaClient.get_balance` -- same semantics, awaited."""
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
        """See captcha_sdk.client.CaptchaClient.solve -- same semantics, awaited."""

        task_id = await self.create_task(task, language_pool=language_pool)

        deadline = time.time() + (timeout if timeout is not None else self.timeout)

        while time.time() < deadline:
            result = await self.get_task_result(task_id)

            if result.get("status") == "ready":
                return result["solution"]

            await asyncio.sleep(self.polling_interval)

        raise TimeoutError("Task solving timed out.")
