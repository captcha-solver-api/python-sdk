"""
Generic tests for CaptchaClient (transport, error handling, polling) --
not tied to any specific captcha type. See test_<captcha_type>.py in this
directory for per-type task serialization and solve() tests.
"""

from unittest.mock import patch

import pytest

from captcha_sdk import CaptchaClient, ApiError, TimeoutError, NetworkError, ValidationError
from captcha_sdk.tasks import RecaptchaV2TaskProxyless


class TestCaptchaClient:
    """Tests for CaptchaClient."""

    def test_create_task(self):
        client = CaptchaClient("test_key")
        task = RecaptchaV2TaskProxyless(
            websiteURL="https://example.com",
            websiteKey="test_key",
        )

        with patch.object(client, "_request") as mock_request:
            mock_request.return_value = {"errorId": 0, "taskId": 100}
            task_id = client.create_task(task)

        assert task_id == 100
        mock_request.assert_called_once_with(
            "createTask",
            {
                "clientKey": "test_key",
                "task": {
                    "type": "RecaptchaV2TaskProxyless",
                    "websiteURL": "https://example.com",
                    "websiteKey": "test_key",
                },
            },
        )

    def test_get_task_result_processing(self):
        client = CaptchaClient("test_key")

        with patch.object(client, "_request") as mock_request:
            mock_request.return_value = {"errorId": 0, "status": "processing"}
            result = client.get_task_result(100)

        assert result["status"] == "processing"

    def test_get_task_result_ready(self):
        client = CaptchaClient("test_key")

        with patch.object(client, "_request") as mock_request:
            mock_request.return_value = {
                "errorId": 0,
                "status": "ready",
                "solution": {"gRecaptchaResponse": "test_token"},
            }
            result = client.get_task_result(100)

        assert result["status"] == "ready"
        assert result["solution"]["gRecaptchaResponse"] == "test_token"

    def test_get_balance(self):
        client = CaptchaClient("test_key")

        with patch.object(client, "_request") as mock_request:
            mock_request.return_value = {"errorId": 0, "balance": 5.0}
            balance = client.get_balance()

        assert balance == 5.0

    def test_solve_success(self):
        client = CaptchaClient("test_key", polling_interval=0.1)
        task = RecaptchaV2TaskProxyless(
            websiteURL="https://example.com",
            websiteKey="test_key",
        )

        with patch.object(client, "_request") as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 100},
                {"errorId": 0, "status": "processing"},
                {"errorId": 0, "status": "ready", "solution": {"gRecaptchaResponse": "test_token"}},
            ]
            result = client.solve(task)

        assert result == {"gRecaptchaResponse": "test_token"}
        assert mock_request.call_count == 3

    def test_solve_timeout(self):
        client = CaptchaClient("test_key", timeout=1, polling_interval=0.5)
        task = RecaptchaV2TaskProxyless(
            websiteURL="https://example.com",
            websiteKey="test_key",
        )

        with patch.object(client, "_request") as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 100},
                {"errorId": 0, "status": "processing"},
                {"errorId": 0, "status": "processing"},
                {"errorId": 0, "status": "processing"},
            ]

            with pytest.raises(TimeoutError):
                client.solve(task)

    def test_api_error(self):
        client = CaptchaClient("test_key")

        with patch.object(client, "_request") as mock_request:
            mock_request.return_value = {
                "errorId": 1,
                "errorCode": "ERROR_KEY_DOES_NOT_EXIST",
                "errorDescription": "Account not found",
            }

            with pytest.raises(ApiError) as exc_info:
                client.get_balance()

        assert exc_info.value.error_code == "ERROR_KEY_DOES_NOT_EXIST"

    def test_network_error(self):
        client = CaptchaClient("test_key")

        with patch.object(client.session, "post") as mock_post:
            mock_post.side_effect = NetworkError("Connection failed")

            with pytest.raises(NetworkError):
                client.get_balance()

    def test_empty_client_key_raises_validation_error(self):
        with pytest.raises(ValidationError):
            CaptchaClient("")

    def test_solve_timeout_override(self):
        client = CaptchaClient("test_key", timeout=120, polling_interval=0.1)
        task = RecaptchaV2TaskProxyless(websiteURL="https://example.com", websiteKey="test_key")

        with patch.object(client, "_request") as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 100},
                {"errorId": 0, "status": "processing"},
                {"errorId": 0, "status": "processing"},
            ]

            with pytest.raises(TimeoutError):
                client.solve(task, timeout=0.15)

    def test_language_pool_client_default_applied(self):
        client = CaptchaClient("test_key", language_pool="en")
        task = RecaptchaV2TaskProxyless(websiteURL="https://example.com", websiteKey="test_key")

        with patch.object(client, "_request") as mock_request:
            mock_request.return_value = {"errorId": 0, "taskId": 100}
            client.create_task(task)

        assert mock_request.call_args[0][1]["languagePool"] == "en"

    def test_language_pool_per_call_overrides_client_default(self):
        client = CaptchaClient("test_key", language_pool="en")
        task = RecaptchaV2TaskProxyless(websiteURL="https://example.com", websiteKey="test_key")

        with patch.object(client, "_request") as mock_request:
            mock_request.return_value = {"errorId": 0, "taskId": 100}
            client.create_task(task, language_pool="ru")

        assert mock_request.call_args[0][1]["languagePool"] == "ru"

    def test_no_language_pool_by_default(self):
        client = CaptchaClient("test_key")
        task = RecaptchaV2TaskProxyless(websiteURL="https://example.com", websiteKey="test_key")

        with patch.object(client, "_request") as mock_request:
            mock_request.return_value = {"errorId": 0, "taskId": 100}
            client.create_task(task)

        assert "languagePool" not in mock_request.call_args[0][1]

    def test_context_manager_closes_session(self):
        client = CaptchaClient("test_key")

        with patch.object(client.session, "close") as mock_close:
            with client:
                mock_close.assert_not_called()

        mock_close.assert_called_once()
