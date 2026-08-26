"""
Tests for ImageToTextTask.
"""

from unittest.mock import patch

from captcha_sdk import CaptchaClient
from captcha_sdk.tasks import ImageToTextTask


class TestImageToText:

    def test_to_dict(self):
        task = ImageToTextTask(
            body="base64string",
            numeric=1,
            minLength=4,
            maxLength=6,
        )
        result = task.to_dict()

        assert result["body"] == "base64string"
        assert result["numeric"] == 1

    def test_solve(self):
        client = CaptchaClient("test_key", polling_interval=0.1)
        task = ImageToTextTask(body="base64string", numeric=1, minLength=4, maxLength=6)

        with patch.object(client, "_request") as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 104},
                {"errorId": 0, "status": "ready", "solution": {"text": "aB3fX9"}},
            ]
            result = client.solve(task)

        assert result == {"text": "aB3fX9"}
