from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest

from captcha_solver_api import AsyncCaptchaClient, CaptchaTimeoutError, NetworkError
from captcha_solver_api.tasks import ImageToTextTask


def messages(client):
    return [call.args[0] for call in client._debug.logger.debug.call_args_list]


async def test_async_debug_success_processing_summary_and_masking():
    client = AsyncCaptchaClient("async-secret", polling_interval=0, debug=True)
    client._debug.logger.debug = Mock()
    task = ImageToTextTask(body="A" * 300)
    responses = [
        httpx.Response(
            200, json={"errorId": 0, "taskId": 9}, request=httpx.Request("POST", "https://x")
        ),
        httpx.Response(
            200,
            json={"errorId": 0, "status": "processing"},
            request=httpx.Request("POST", "https://x"),
        ),
        httpx.Response(
            200,
            json={
                "errorId": 0,
                "status": "ready",
                "createTime": 2,
                "endTime": 5,
                "solution": {"text": "1234"},
            },
            request=httpx.Request("POST", "https://x"),
        ),
    ]
    client._client.post = AsyncMock(side_effect=responses)

    assert await client.solve(task) == {"text": "1234"}

    output = "\n".join(messages(client))
    assert "async-secret" not in output
    assert "[base64, 300 chars]" in output
    assert "getTaskResult taskId=9 -> processing" in output
    assert "SOLVE SUMMARY" in output
    assert "polls:           2" in output
    assert "serverSolveTime: 3s" in output
    await client.aclose()


async def test_async_debug_transport_timeout_and_isolation():
    client = AsyncCaptchaClient("secret", debug=True)
    client._debug.logger.debug = Mock()
    client._client.post = AsyncMock(side_effect=httpx.ConnectError("dns failed"))
    with pytest.raises(NetworkError):
        await client.get_balance()
    assert "RESPONSE: none - no response from the server" in messages(client)[0]

    client._debug.logger.debug = Mock()
    client._client.post = AsyncMock(side_effect=httpx.ReadTimeout("slow"))
    with pytest.raises(CaptchaTimeoutError):
        await client.get_balance()
    assert "Timeout" in messages(client)[0]

    client._debug.logger.debug = Mock(side_effect=RuntimeError("logger failed"))
    client._client.post = AsyncMock(
        return_value=httpx.Response(
            200, json={"errorId": 0, "balance": 1.25}, request=httpx.Request("POST", "https://x")
        )
    )
    assert await client.get_balance() == 1.25
    await client.aclose()


async def test_async_failed_solve_has_summary_when_task_not_created():
    client = AsyncCaptchaClient("secret", debug=True)
    client._debug.logger.debug = Mock()
    task = ImageToTextTask(body="image")
    with patch.object(client, "create_task", side_effect=NetworkError("offline")):
        with pytest.raises(NetworkError):
            await client.solve(task)
    summary = messages(client)[0]
    assert "status:          not solved" in summary
    assert "taskId:          - (task was not created)" in summary
    await client.aclose()
