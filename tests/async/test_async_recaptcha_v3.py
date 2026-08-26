"""
Async solve() test for RecaptchaV3TaskProxyless.
Task serialization is covered once in tests/sync/test_recaptcha_v3.py.
"""

from unittest.mock import AsyncMock, patch

from captcha_sdk import AsyncCaptchaClient
from captcha_sdk.tasks import RecaptchaV3TaskProxyless


class TestAsyncRecaptchaV3:

    async def test_solve(self):
        client = AsyncCaptchaClient("test_key", polling_interval=0.1)
        task = RecaptchaV3TaskProxyless(websiteURL="https://example.com", websiteKey="test_key", minScore=0.3)

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 102},
                {"errorId": 0, "status": "ready", "solution": {"gRecaptchaResponse": "v3_token"}},
            ]
            result = await client.solve(task)

        assert result == {"gRecaptchaResponse": "v3_token"}
