"""
Tests for TencentTaskProxyless / TencentTask.
"""

from unittest.mock import patch

from captcha_sdk import CaptchaClient
from captcha_sdk.tasks import TencentTaskProxyless, TencentTask


class TestTencent:

    def test_proxyless_to_dict(self):
        task = TencentTaskProxyless(
            websiteURL="https://example.com",
            appId="190014885",
        )
        result = task.to_dict()

        assert result["type"] == "TencentTaskProxyless"
        assert result["websiteURL"] == "https://example.com"
        assert result["appId"] == "190014885"

    def test_proxyless_with_optionals(self):
        task = TencentTaskProxyless(
            websiteURL="https://example.com",
            appId="190014885",
            captchaScript="https://turing.captcha.qcloud.com/TCaptcha.js",
        )
        result = task.to_dict()

        assert result["captchaScript"] == "https://turing.captcha.qcloud.com/TCaptcha.js"

    def test_task_with_proxy(self):
        task = TencentTask(
            websiteURL="https://example.com",
            appId="190014885",
            proxyType="http",
            proxyAddress="1.2.3.4",
            proxyPort=8080,
            proxyLogin="user",
            proxyPassword="pass",
        )
        result = task.to_dict()

        assert result["type"] == "TencentTask"
        assert result["appId"] == "190014885"
        assert result["proxyType"] == "http"
        assert result["proxyAddress"] == "1.2.3.4"
        assert result["proxyLogin"] == "user"

    def test_solve(self):
        client = CaptchaClient("test_key", polling_interval=0.1)
        task = TencentTaskProxyless(websiteURL="https://example.com", appId="190014885")

        with patch.object(client, "_request") as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 109},
                {"errorId": 0, "status": "ready", "solution": {
                    "appid": "190014885", "ret": 0, "ticket": "t", "randstr": "r",
                }},
            ]
            result = client.solve(task)

        assert result == {"appid": "190014885", "ret": 0, "ticket": "t", "randstr": "r"}
