"""
Tests for retrying transient getTaskResult failures inside AsyncCaptchaClient.solve(). Mirrors tests/sync/test_polling_retries.py.
"""

from unittest.mock import AsyncMock, patch

import pytest

from captcha_solver_api import ApiError, AsyncCaptchaClient, CaptchaTimeoutError, NetworkError
from captcha_solver_api.tasks import RecaptchaV2TaskProxyless

TASK = RecaptchaV2TaskProxyless(websiteURL="https://example.com", websiteKey="site-key")
CREATED = {"errorId": 0, "taskId": 100}
READY = {"errorId": 0, "status": "ready", "solution": {"gRecaptchaResponse": "token"}}


def make_client():
    return AsyncCaptchaClient("test_key", timeout=5, polling_interval=0.01)


async def test_solve_retries_network_errors_and_http_timeouts_while_polling():
    client = make_client()

    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = [
            CREATED,
            NetworkError("502 Bad Gateway"),
            CaptchaTimeoutError("Request timed out."),
            READY,
        ]
        result = await client.solve(TASK)

    assert result == {"gRecaptchaResponse": "token"}
    assert mock_request.call_count == 4


async def test_solve_raises_after_too_many_consecutive_poll_failures():
    client = make_client()
    failures = [NetworkError("connection reset")] * (client.poll_retries + 1)

    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = [CREATED, *failures]
        with pytest.raises(NetworkError, match="connection reset"):
            await client.solve(TASK)

    assert mock_request.call_count == 1 + client.poll_retries + 1


async def test_successful_poll_resets_the_failure_counter():
    client = make_client()
    client.poll_retries = 1
    processing = {"errorId": 0, "status": "processing"}

    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = [
            CREATED,
            NetworkError("blip"),
            processing,
            NetworkError("blip"),
            READY,
        ]
        result = await client.solve(TASK)

    assert result == {"gRecaptchaResponse": "token"}


async def test_solve_does_not_retry_api_errors_while_polling():
    client = make_client()
    api_error = {
        "errorId": 1,
        "errorCode": "ERROR_CAPTCHA_UNSOLVABLE",
        "errorDescription": "Captcha could not be solved",
    }

    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = [CREATED, api_error, READY]
        with pytest.raises(ApiError):
            await client.solve(TASK)

    assert mock_request.call_count == 2


async def test_solve_does_not_retry_create_task():
    client = make_client()

    with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = [NetworkError("down"), CREATED, READY]
        with pytest.raises(NetworkError):
            await client.solve(TASK)

    assert mock_request.call_count == 1
