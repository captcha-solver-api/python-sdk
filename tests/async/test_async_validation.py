from unittest.mock import AsyncMock, patch

import pytest

from captcha_solver_api import AsyncCaptchaClient, ValidationError
from captcha_solver_api.tasks import GeeTestTaskProxyless


@pytest.mark.asyncio
async def test_create_task_rejects_non_task_value():
    async with AsyncCaptchaClient("api-key") as client:
        with pytest.raises(ValidationError, match="task must be an instance of BaseTask"):
            await client.create_task(None)


def test_async_client_rejects_whitespace_client_key():
    with pytest.raises(ValidationError, match="client_key is required"):
        AsyncCaptchaClient("   ")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task, message",
    [
        (
            GeeTestTaskProxyless(websiteURL="https://example.com"),
            r"Missing required GeeTest v3 parameter\(s\): gt, challenge",
        ),
        (
            GeeTestTaskProxyless(
                websiteURL="https://example.com",
                version=4,
                initParameters={},
            ),
            r"Missing required GeeTest v4 parameter: initParameters\.captcha_id",
        ),
    ],
)
async def test_create_task_rejects_invalid_geetest_before_request(task, message):
    async with AsyncCaptchaClient("api-key") as client:
        with patch.object(client, "_request", new_callable=AsyncMock) as request:
            with pytest.raises(ValidationError, match=message):
                await client.create_task(task)

        request.assert_not_awaited()
