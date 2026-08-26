"""
Tests for RecaptchaV3TaskProxyless.
"""

from unittest.mock import patch

from captcha_sdk import CaptchaClient
from captcha_sdk.tasks import RecaptchaV3TaskProxyless


class TestRecaptchaV3:

    def test_to_dict(self):
        task = RecaptchaV3TaskProxyless(
            websiteURL="https://example.com",
            websiteKey="test_key",
            minScore=0.7,
            pageAction="login",
        )
        result = task.to_dict()

        assert result["minScore"] == 0.7
        assert result["pageAction"] == "login"

    def test_solve(self):
        client = CaptchaClient("test_key", polling_interval=0.1)
        task = RecaptchaV3TaskProxyless(websiteURL="https://example.com", websiteKey="test_key", minScore=0.3)

        with patch.object(client, "_request") as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 102},
                {"errorId": 0, "status": "ready", "solution": {"gRecaptchaResponse": "v3_token"}},
            ]
            result = client.solve(task)

        assert result == {"gRecaptchaResponse": "v3_token"}
