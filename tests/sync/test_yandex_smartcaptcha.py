"""
Tests for YandexSmartCaptchaTaskProxyless / YandexSmartCaptchaTask.
"""

from unittest.mock import patch

from captcha_sdk import CaptchaClient
from captcha_sdk.tasks import YandexSmartCaptchaTaskProxyless, YandexSmartCaptchaTask


class TestYandexSmartCaptcha:

    def test_proxyless_to_dict(self):
        task = YandexSmartCaptchaTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="Y5Lh0ti...",
        )
        result = task.to_dict()

        assert result["type"] == "YandexSmartCaptchaTaskProxyless"
        assert result["websiteURL"] == "https://example.com"
        assert result["websiteKey"] == "Y5Lh0ti..."

    def test_proxyless_with_optionals(self):
        task = YandexSmartCaptchaTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="Y5Lh0ti...",
            userAgent="Mozilla/5.0",
            cookies="session=abc123",
        )
        result = task.to_dict()

        assert result["userAgent"] == "Mozilla/5.0"
        assert result["cookies"] == "session=abc123"

    def test_task_with_proxy(self):
        task = YandexSmartCaptchaTask(
            websiteURL="https://example.com",
            websiteKey="Y5Lh0ti...",
            proxyType="https",
            proxyAddress="1.2.3.4",
            proxyPort=8080,
            proxyLogin="user",
            proxyPassword="pass",
        )
        result = task.to_dict()

        assert result["proxyType"] == "https"
        assert result["proxyAddress"] == "1.2.3.4"
        assert result["proxyLogin"] == "user"

    def test_solve(self):
        client = CaptchaClient("test_key", polling_interval=0.1)
        task = YandexSmartCaptchaTaskProxyless(websiteURL="https://example.com", websiteKey="Y5Lh0ti...")

        with patch.object(client, "_request") as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 107},
                {"errorId": 0, "status": "ready", "solution": {"token": "yandex_token"}},
            ]
            result = client.solve(task)

        assert result == {"token": "yandex_token"}
