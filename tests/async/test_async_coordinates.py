"""
Async solve() test for CoordinatesTask.
Task serialization is covered once in tests/sync/test_coordinates.py.
"""

from unittest.mock import AsyncMock, patch

from captcha_sdk import AsyncCaptchaClient
from captcha_sdk.tasks import CoordinatesTask


class TestAsyncCoordinates:

    async def test_solve(self):
        client = AsyncCaptchaClient("test_key", polling_interval=0.1)
        task = CoordinatesTask(body="base64string", comment="click on the green apple")

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 108},
                {"errorId": 0, "status": "ready", "solution": {"coordinates": [{"x": 358, "y": 268}]}},
            ]
            result = await client.solve(task)

        assert result == {"coordinates": [{"x": 358, "y": 268}]}
