"""
Generic tests for AsyncCaptchaClient (transport, error handling, polling) --
not tied to any specific captcha type. Mirrors tests/sync/test_client.py.
See test_async_<captcha_type>.py in this directory for per-type solve() tests.
"""

from unittest.mock import AsyncMock, patch

import httpx
import pytest

from captcha_sdk import AsyncCaptchaClient, ApiError, TimeoutError, ValidationError
from captcha_sdk.tasks import RecaptchaV2TaskProxyless


class TestAsyncCaptchaClient:
    """Tests for AsyncCaptchaClient."""

    def test_empty_client_key_raises_validation_error(self):
        with pytest.raises(ValidationError):
            AsyncCaptchaClient("")

    async def test_create_task(self):
        client = AsyncCaptchaClient("test_key")
        task = RecaptchaV2TaskProxyless(websiteURL="https://example.com", websiteKey="test_key")

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"errorId": 0, "taskId": 100}
            task_id = await client.create_task(task)

        assert task_id == 100
        mock_request.assert_called_once_with(
            "createTask",
            {
                "clientKey": "test_key",
                "task": {
                    "type": "RecaptchaV2TaskProxyless",
                    "websiteURL": "https://example.com",
                    "websiteKey": "test_key",
                },
            },
        )

    async def test_get_balance(self):
        client = AsyncCaptchaClient("test_key")

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"errorId": 0, "balance": 5.0}
            balance = await client.get_balance()

        assert balance == 5.0

    async def test_solve_success(self):
        client = AsyncCaptchaClient("test_key", polling_interval=0.1)
        task = RecaptchaV2TaskProxyless(websiteURL="https://example.com", websiteKey="test_key")

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 100},
                {"errorId": 0, "status": "processing"},
                {"errorId": 0, "status": "ready", "solution": {"gRecaptchaResponse": "test_token"}},
            ]
            result = await client.solve(task)

        assert result == {"gRecaptchaResponse": "test_token"}
        assert mock_request.call_count == 3

    async def test_solve_timeout(self):
        client = AsyncCaptchaClient("test_key", timeout=0.15, polling_interval=0.1)
        task = RecaptchaV2TaskProxyless(websiteURL="https://example.com", websiteKey="test_key")

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 100},
                {"errorId": 0, "status": "processing"},
                {"errorId": 0, "status": "processing"},
                {"errorId": 0, "status": "processing"},
            ]

            with pytest.raises(TimeoutError):
                await client.solve(task)

    async def test_api_error(self):
        client = AsyncCaptchaClient("test_key")

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {
                "errorId": 1,
                "errorCode": "ERROR_KEY_DOES_NOT_EXIST",
                "errorDescription": "Account not found",
            }

            with pytest.raises(ApiError) as exc_info:
                await client.get_balance()

        assert exc_info.value.error_code == "ERROR_KEY_DOES_NOT_EXIST"
        await client.aclose()

    async def test_language_pool_client_default_applied(self):
        client = AsyncCaptchaClient("test_key", language_pool="en")
        task = RecaptchaV2TaskProxyless(websiteURL="https://example.com", websiteKey="test_key")

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"errorId": 0, "taskId": 100}
            await client.create_task(task)

        assert mock_request.call_args[0][1]["languagePool"] == "en"
        await client.aclose()

    async def test_language_pool_per_call_overrides_client_default(self):
        client = AsyncCaptchaClient("test_key", language_pool="en")
        task = RecaptchaV2TaskProxyless(websiteURL="https://example.com", websiteKey="test_key")

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"errorId": 0, "taskId": 100}
            await client.create_task(task, language_pool="ru")

        assert mock_request.call_args[0][1]["languagePool"] == "ru"
        await client.aclose()

    async def test_no_language_pool_by_default(self):
        client = AsyncCaptchaClient("test_key")
        task = RecaptchaV2TaskProxyless(websiteURL="https://example.com", websiteKey="test_key")

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"errorId": 0, "taskId": 100}
            await client.create_task(task)

        assert "languagePool" not in mock_request.call_args[0][1]
        await client.aclose()

    async def test_context_manager_closes_client(self):
        client = AsyncCaptchaClient("test_key")

        with patch.object(client._client, "aclose", new_callable=AsyncMock) as mock_aclose:
            async with client:
                mock_aclose.assert_not_called()

        mock_aclose.assert_called_once()

    async def test_reuses_single_http_client_across_requests(self):
        """The whole point of holding a persistent httpx.AsyncClient is to avoid
        opening a fresh connection pool on every request -- verify create_task()
        and get_balance() both go through the exact same client instance."""
        client = AsyncCaptchaClient("test_key")
        first_client = client._client

        with patch.object(client._client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = httpx.Response(
                200, json={"errorId": 0, "balance": 5.0}, request=httpx.Request("POST", "https://x")
            )
            await client.get_balance()
            await client.get_balance()

        assert client._client is first_client
        assert mock_post.call_count == 2
        await client.aclose()
