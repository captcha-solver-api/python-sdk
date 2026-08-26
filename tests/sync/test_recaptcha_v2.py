"""
Tests for RecaptchaV2TaskProxyless / RecaptchaV2Task.
"""

from unittest.mock import patch

from captcha_sdk import CaptchaClient
from captcha_sdk.tasks import RecaptchaV2TaskProxyless, RecaptchaV2Task


class TestRecaptchaV2:

    def test_proxyless_to_dict(self):
        task = RecaptchaV2TaskProxyless(
            websiteURL="https://example.com",
            websiteKey="test_key",
        )
        result = task.to_dict()

        assert result == {
            "type": "RecaptchaV2TaskProxyless",
            "websiteURL": "https://example.com",
            "websiteKey": "test_key",
        }

    def test_proxyless_with_optionals(self):
        task = RecaptchaV2TaskProxyless(
            websiteURL="https://example.com",
            websiteKey="test_key",
            isInvisible=True,
            userAgent="Mozilla/5.0",
        )
        result = task.to_dict()

        assert result["isInvisible"] is True
        assert result["userAgent"] == "Mozilla/5.0"

    def test_none_values_excluded(self):
        task = RecaptchaV2TaskProxyless(
            websiteURL="https://example.com",
            websiteKey="test_key",
        )
        result = task.to_dict()

        assert "isInvisible" not in result
        assert "userAgent" not in result

    def test_task_with_proxy_to_dict(self):
        task = RecaptchaV2Task(
            websiteURL="https://example.com",
            websiteKey="test_key",
            proxyType="http",
            proxyAddress="1.2.3.4",
            proxyPort=8080,
            proxyLogin="user",
            proxyPassword="pass",
        )
        result = task.to_dict()

        assert result["type"] == "RecaptchaV2Task"
        assert result["proxyType"] == "http"
        assert result["proxyAddress"] == "1.2.3.4"
        assert result["proxyLogin"] == "user"

    def test_solve(self):
        client = CaptchaClient("test_key", polling_interval=0.1)
        task = RecaptchaV2TaskProxyless(websiteURL="https://example.com", websiteKey="test_key")

        with patch.object(client, "_request") as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 100},
                {"errorId": 0, "status": "processing"},
                {"errorId": 0, "status": "ready", "solution": {"gRecaptchaResponse": "test_token"}},
            ]
            result = client.solve(task)

        assert result == {"gRecaptchaResponse": "test_token"}
        assert mock_request.call_count == 3
