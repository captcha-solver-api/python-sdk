from unittest.mock import Mock, patch

import pytest
import requests

from captcha_solver_api import ApiError, CaptchaClient, CaptchaTimeoutError, NetworkError
from captcha_solver_api.tasks import ImageToTextTask


def response(status=200, reason="OK", data=None):
    result = Mock(status_code=status, reason=reason, text="response text")
    result.json.return_value = data
    if status >= 400:
        error = requests.HTTPError(f"{status} {reason}", response=result)
        result.raise_for_status.side_effect = error
    return result


def debug_messages(client):
    return [call.args[0] for call in client._debug.logger.debug.call_args_list]


def test_debug_is_disabled_by_default():
    client = CaptchaClient("secret")
    assert client.debug is False
    assert client._debug.enabled is False


def test_debug_initialization_is_one_timestamped_event():
    with patch("logging.Logger.debug") as logger:
        CaptchaClient("secret", debug=True)

    logger.assert_called_once()
    message = logger.call_args.args[0]
    assert message.startswith("[")
    assert "] [CaptchaClient] initialized" in message
    assert "sdkVersion:" in message
    assert "baseUrl:" in message
    assert "pollingInterval:" in message


def test_success_masks_and_truncates_without_mutating_payload():
    client = CaptchaClient("api-secret", debug=True)
    client._debug.logger.debug = Mock()
    long_token = "x" * 250
    body = "Y" * 300
    payload = {
        "clientKey": "api-secret",
        "cookie": "session=secret",
        "proxyAddress": "127.0.0.1",
        "task": {"type": "ImageToTextTask", "body": body},
    }
    client.session.post = Mock(
        return_value=response(
            data={"errorId": 0, "taskId": 123, "solution": {"token": long_token}}
        )
    )

    result = client._request("createTask", payload)

    assert result["taskId"] == 123
    message = debug_messages(client)[0]
    assert "REQUEST (POST" in message and "RESPONSE (HTTP 200 OK" in message
    assert "api-secret" not in message
    assert "session=secret" not in message
    assert "127.0.0.1" not in message
    assert "[MASKED]" in message
    assert "[base64, 300 chars]" in message
    assert "[truncated, 250 chars]" in message
    assert payload["clientKey"] == "api-secret"
    assert payload["task"]["body"] == body


def test_processing_is_compact_single_line():
    client = CaptchaClient("secret", debug=True)
    client._debug.logger.debug = Mock()
    client.session.post = Mock(return_value=response(data={"errorId": 0, "status": "processing"}))

    client.get_task_result(42)

    message = debug_messages(client)[0]
    assert "getTaskResult taskId=42 -> processing" in message
    assert "REQUEST" not in message
    assert "\n" not in message


def test_api_and_http_errors_include_paired_request_response():
    client = CaptchaClient("secret", debug=True)
    client._debug.logger.debug = Mock()
    client.session.post = Mock(
        side_effect=[
            response(
                data={
                    "errorId": 1,
                    "errorCode": "ERROR_KEY_DOES_NOT_EXIST",
                    "errorDescription": "Account not found",
                }
            ),
            response(502, "Bad Gateway", {"message": "upstream failed"}),
        ]
    )

    with pytest.raises(ApiError):
        client.get_balance()
    with pytest.raises(NetworkError):
        client.get_balance()

    api_message, http_message = debug_messages(client)
    assert "failed: ApiError [ERROR_KEY_DOES_NOT_EXIST]" in api_message
    assert "REQUEST" in api_message and "RESPONSE (HTTP 200 OK" in api_message
    assert "failed: HTTPError" in http_message
    assert "RESPONSE (HTTP 502 Bad Gateway" in http_message
    assert "upstream failed" in http_message


def test_invalid_json_network_and_timeout_explain_missing_response():
    client = CaptchaClient("secret", debug=True)
    client._debug.logger.debug = Mock()
    invalid = response()
    invalid.json.side_effect = ValueError("bad json")
    client.session.post = Mock(
        side_effect=[invalid, requests.ConnectionError("dns failed"), requests.Timeout("slow")]
    )

    with pytest.raises(NetworkError):
        client.get_balance()
    with pytest.raises(NetworkError):
        client.get_balance()
    with pytest.raises(CaptchaTimeoutError):
        client.get_balance()

    invalid_message, network_message, timeout_message = debug_messages(client)
    assert "body is not valid JSON" in invalid_message
    assert "RESPONSE: none - no response from the server (ConnectionError" in network_message
    assert "RESPONSE: none - no response from the server (Timeout" in timeout_message


def test_solve_summary_reports_success_failure_and_poll_count():
    task = ImageToTextTask(body="image")
    client = CaptchaClient("secret", polling_interval=0, debug=True)
    client._debug.logger.debug = Mock()
    with patch.object(client, "_request") as request:
        request.side_effect = [
            {"errorId": 0, "taskId": 7},
            {"errorId": 0, "status": "processing"},
            {
                "errorId": 0,
                "status": "ready",
                "createTime": 10,
                "endTime": 18,
                "solution": {"text": "1234"},
            },
        ]
        assert client.solve(task) == {"text": "1234"}

    summary = debug_messages(client)[0]
    assert "SOLVE SUMMARY" in summary
    assert "status:          solved" in summary
    assert "taskId:          7" in summary
    assert "taskType:        ImageToTextTask" in summary
    assert "serverSolveTime: 8s" in summary
    assert "polls:           2" in summary

    client._debug.logger.debug.reset_mock()
    with patch.object(client, "create_task", side_effect=ApiError("BAD", "failed")):
        with pytest.raises(ApiError):
            client.solve(task)
    summary = debug_messages(client)[0]
    assert "status:          not solved" in summary
    assert "taskId:          - (task was not created)" in summary
    assert "error:" in summary


def test_debug_failure_does_not_change_result_or_exception():
    client = CaptchaClient("secret", debug=True)
    client._debug.logger.debug = Mock(side_effect=RuntimeError("logger failed"))
    client.session.post = Mock(return_value=response(data={"errorId": 0, "balance": 4.5}))
    assert client.get_balance() == 4.5

    client.session.post = Mock(side_effect=requests.ConnectionError("original failure"))
    with pytest.raises(NetworkError, match="original failure"):
        client.get_balance()
