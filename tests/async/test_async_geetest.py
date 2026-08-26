"""
Async solve() tests for GeeTestTaskProxyless (v3 and v4).
Task serialization is covered once in tests/sync/test_geetest.py.
"""

from unittest.mock import AsyncMock, patch

from captcha_sdk import AsyncCaptchaClient
from captcha_sdk.tasks import GeeTestTaskProxyless


class TestAsyncGeeTest:

    async def test_solve_v3(self):
        client = AsyncCaptchaClient("test_key", polling_interval=0.1)
        task = GeeTestTaskProxyless(websiteURL="https://example.com", gt="test_gt", challenge="test_challenge")

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 105},
                {"errorId": 0, "status": "ready", "solution": {
                    "challenge": "c", "validate": "v", "seccode": "s",
                }},
            ]
            result = await client.solve(task)

        assert result == {"challenge": "c", "validate": "v", "seccode": "s"}

    async def test_solve_v4(self):
        client = AsyncCaptchaClient("test_key", polling_interval=0.1)
        task = GeeTestTaskProxyless(
            websiteURL="https://example.com", version=4, initParameters={"captcha_id": "test_id"},
        )

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 106},
                {"errorId": 0, "status": "ready", "solution": {
                    "captcha_id": "test_id", "lot_number": "1", "pass_token": "p",
                    "gen_time": "t", "captcha_output": "o",
                }},
            ]
            result = await client.solve(task)

        assert result["captcha_output"] == "o"
