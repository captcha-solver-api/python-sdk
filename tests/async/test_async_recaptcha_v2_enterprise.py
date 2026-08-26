"""
Async solve() test for RecaptchaV2EnterpriseTaskProxyless.
Task serialization is covered once in tests/sync/test_recaptcha_v2_enterprise.py.
"""

from unittest.mock import AsyncMock, patch

from captcha_sdk import AsyncCaptchaClient
from captcha_sdk.tasks import RecaptchaV2EnterpriseTaskProxyless


class TestAsyncRecaptchaV2Enterprise:

    async def test_solve(self):
        client = AsyncCaptchaClient("test_key", polling_interval=0.1)
        task = RecaptchaV2EnterpriseTaskProxyless(websiteURL="https://example.com", websiteKey="test_key")

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 101},
                {"errorId": 0, "status": "ready", "solution": {"gRecaptchaResponse": "enterprise_token"}},
            ]
            result = await client.solve(task)

        assert result == {"gRecaptchaResponse": "enterprise_token"}
