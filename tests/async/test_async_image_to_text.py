"""
Async solve() test for ImageToTextTask.
Task serialization is covered once in tests/sync/test_image_to_text.py.
"""

from unittest.mock import AsyncMock, patch

from captcha_sdk import AsyncCaptchaClient
from captcha_sdk.tasks import ImageToTextTask


class TestAsyncImageToText:

    async def test_solve(self):
        client = AsyncCaptchaClient("test_key", polling_interval=0.1)
        task = ImageToTextTask(body="base64string", numeric=1, minLength=4, maxLength=6)

        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 104},
                {"errorId": 0, "status": "ready", "solution": {"text": "aB3fX9"}},
            ]
            result = await client.solve(task)

        assert result == {"text": "aB3fX9"}
