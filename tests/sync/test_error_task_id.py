"""
Tests for the task_id attribute on errors raised by CaptchaClient.
"""

from unittest.mock import patch

import pytest

from captcha_solver_api import (
    ApiError,
    CaptchaClient,
    CaptchaError,
    CaptchaTimeoutError,
    NetworkError,
    ValidationError,
)
from captcha_solver_api.tasks import RecaptchaV2TaskProxyless

TASK = RecaptchaV2TaskProxyless(websiteURL="https://example.com", websiteKey="site-key")
CREATED = {"errorId": 0, "taskId": 100}
PROCESSING = {"errorId": 0, "status": "processing"}
API_ERROR = {
    "errorId": 1,
    "errorCode": "ERROR_CAPTCHA_UNSOLVABLE",
    "errorDescription": "Captcha could not be solved",
}


def make_client(**kwargs):
    return CaptchaClient("test_key", polling_interval=0.01, **kwargs)


def test_task_id_defaults_to_none():
    assert CaptchaError("boom").task_id is None
    assert ApiError("CODE", "description").task_id is None


def test_polling_timeout_has_task_id():
    client = make_client(timeout=0.05)

    with patch.object(client, "_request") as mock_request:
        mock_request.side_effect = [CREATED] + [PROCESSING] * 20
        with pytest.raises(CaptchaTimeoutError, match="Task 100") as exc_info:
            client.solve(TASK)

    assert exc_info.value.task_id == 100


def test_api_error_while_polling_has_task_id():
    client = make_client()

    with patch.object(client, "_request") as mock_request:
        mock_request.side_effect = [CREATED, API_ERROR]
        with pytest.raises(ApiError) as exc_info:
            client.solve(TASK)

    assert exc_info.value.task_id == 100
    assert exc_info.value.error_code == "ERROR_CAPTCHA_UNSOLVABLE"


def test_network_error_after_retries_has_task_id():
    client = make_client()
    client.poll_retries = 0

    with patch.object(client, "_request") as mock_request:
        mock_request.side_effect = [CREATED, NetworkError("connection reset")]
        with pytest.raises(NetworkError) as exc_info:
            client.solve(TASK)

    assert exc_info.value.task_id == 100


def test_ready_task_without_solution_object_has_task_id():
    client = make_client()

    with patch.object(client, "_request") as mock_request:
        mock_request.side_effect = [CREATED, {"errorId": 0, "status": "ready", "solution": "x"}]
        with pytest.raises(NetworkError) as exc_info:
            client.solve(TASK)

    assert exc_info.value.task_id == 100


def test_get_task_result_error_has_task_id():
    client = make_client()

    with patch.object(client, "_request", return_value=API_ERROR):
        with pytest.raises(ApiError) as exc_info:
            client.get_task_result(42)

    assert exc_info.value.task_id == 42


def test_errors_before_task_creation_have_no_task_id():
    client = make_client()

    with patch.object(client, "_request", return_value=API_ERROR):
        with pytest.raises(ApiError) as exc_info:
            client.solve(TASK)
    assert exc_info.value.task_id is None

    with pytest.raises(ValidationError) as validation_info:
        client.solve(RecaptchaV2TaskProxyless(websiteURL="", websiteKey="site-key"))
    assert validation_info.value.task_id is None
