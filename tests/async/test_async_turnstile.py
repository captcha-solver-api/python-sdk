"""
Async solve() test for TurnstileTaskProxyless.
Task serialization is covered once in tests/sync/test_turnstile.py.
"""

from unittest.mock import AsyncMock, patch

from captcha_sdk import AsyncCaptchaClient
from captcha_sdk.tasks import TurnstileTaskProxyless


class TestAsyncTurnstile:

    async def test_solve(self):
        client = AsyncCaptchaClient("test_key", polling_interval=0.1)
        task = TurnstileTaskProxyless(websiteURL="https://example.com", websiteKey="test_key")

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 103},
                {"errorId": 0, "status": "ready", "solution": {"token": "turnstile_token"}},
            ]
            result = await client.solve(task)

        assert result == {"token": "turnstile_token"}
