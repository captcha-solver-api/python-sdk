"""
Tests for RecaptchaV2EnterpriseTaskProxyless / RecaptchaV2EnterpriseTask.
"""

from unittest.mock import patch

from captcha_sdk import CaptchaClient
from captcha_sdk.tasks import RecaptchaV2EnterpriseTaskProxyless, RecaptchaV2EnterpriseTask


class TestRecaptchaV2Enterprise:

    def test_proxyless_to_dict(self):
        task = RecaptchaV2EnterpriseTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="test_key",
        )
        result = task.to_dict()

        assert result == {
            "type": "RecaptchaV2EnterpriseTaskProxyless",
            "websiteURL": "https://example.com",
            "websiteKey": "test_key",
        }

    def test_proxyless_with_enterprise_payload(self):
        task = RecaptchaV2EnterpriseTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="test_key",
            enterprisePayload={"s": "data-s-value"},
            isInvisible=True,
        )
        result = task.to_dict()

        assert result["enterprisePayload"] == {"s": "data-s-value"}
        assert result["isInvisible"] is True

    def test_task_with_proxy_to_dict(self):
        task = RecaptchaV2EnterpriseTask(
            websiteURL="https://example.com",
            websiteKey="test_key",
            proxyType="http",
            proxyAddress="1.2.3.4",
            proxyPort=8080,
            proxyLogin="user",
            proxyPassword="pass",
        )
        result = task.to_dict()

        assert result["type"] == "RecaptchaV2EnterpriseTask"
        assert result["proxyType"] == "http"
        assert result["proxyAddress"] == "1.2.3.4"
        assert result["proxyLogin"] == "user"

    def test_solve(self):
        client = CaptchaClient("test_key", polling_interval=0.1)
        task = RecaptchaV2EnterpriseTaskProxyless(websiteURL="https://example.com", websiteKey="test_key")

        with patch.object(client, "_request") as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 101},
                {"errorId": 0, "status": "ready", "solution": {"gRecaptchaResponse": "enterprise_token"}},
            ]
            result = client.solve(task)

        assert result == {"gRecaptchaResponse": "enterprise_token"}
