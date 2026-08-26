"""
Async solve() test for RecaptchaV2TaskProxyless.
Task serialization is covered once in tests/sync/test_recaptcha_v2.py --
it doesn't depend on which client (sync/async) is used.
"""

from unittest.mock import AsyncMock, patch

from captcha_sdk import AsyncCaptchaClient
from captcha_sdk.tasks import RecaptchaV2TaskProxyless


class TestAsyncRecaptchaV2:

    async def test_solve(self):
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
