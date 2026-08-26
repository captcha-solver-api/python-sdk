"""
Async solve() test for TencentTaskProxyless.
Task serialization is covered once in tests/sync/test_tencent.py.
"""

from unittest.mock import AsyncMock, patch

from captcha_sdk import AsyncCaptchaClient
from captcha_sdk.tasks import TencentTaskProxyless


class TestAsyncTencent:

    async def test_solve(self):
        client = AsyncCaptchaClient("test_key", polling_interval=0.1)
        task = TencentTaskProxyless(websiteURL="https://example.com", appId="190014885")

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 109},
                {"errorId": 0, "status": "ready", "solution": {
                    "appid": "190014885", "ret": 0, "ticket": "t", "randstr": "r",
                }},
            ]
            result = await client.solve(task)

        assert result == {"appid": "190014885", "ret": 0, "ticket": "t", "randstr": "r"}
