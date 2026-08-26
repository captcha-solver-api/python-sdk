"""
Async solve() test for YandexSmartCaptchaTaskProxyless.
Task serialization is covered once in tests/sync/test_yandex_smartcaptcha.py.
"""

from unittest.mock import AsyncMock, patch

from captcha_sdk import AsyncCaptchaClient
from captcha_sdk.tasks import YandexSmartCaptchaTaskProxyless


class TestAsyncYandexSmartCaptcha:

    async def test_solve(self):
        client = AsyncCaptchaClient("test_key", polling_interval=0.1)
        task = YandexSmartCaptchaTaskProxyless(websiteURL="https://example.com", websiteKey="Y5Lh0ti...")

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 107},
                {"errorId": 0, "status": "ready", "solution": {"token": "yandex_token"}},
            ]
            result = await client.solve(task)

        assert result == {"token": "yandex_token"}
