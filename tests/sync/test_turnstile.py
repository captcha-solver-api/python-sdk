"""
Tests for TurnstileTaskProxyless / TurnstileTask.
"""

from unittest.mock import patch

from captcha_sdk import CaptchaClient
from captcha_sdk.tasks import TurnstileTaskProxyless, TurnstileTask


class TestTurnstile:

    def test_proxyless_to_dict(self):
        task = TurnstileTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="test_key",
        )
        result = task.to_dict()

        assert result["type"] == "TurnstileTaskProxyless"

    def test_task_with_proxy_to_dict(self):
        task = TurnstileTask(
            websiteURL="https://example.com",
            websiteKey="test_key",
            proxyType="http",
            proxyAddress="1.2.3.4",
            proxyPort=8080,
        )
        result = task.to_dict()

        assert result["type"] == "TurnstileTask"
        assert result["proxyType"] == "http"
        assert result["proxyAddress"] == "1.2.3.4"

    def test_solve(self):
        client = CaptchaClient("test_key", polling_interval=0.1)
        task = TurnstileTaskProxyless(websiteURL="https://example.com", websiteKey="test_key")

        with patch.object(client, "_request") as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 103},
                {"errorId": 0, "status": "ready", "solution": {"token": "turnstile_token"}},
            ]
            result = client.solve(task)

        assert result == {"token": "turnstile_token"}
