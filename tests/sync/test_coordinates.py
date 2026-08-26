"""
Tests for CoordinatesTask (generic click captcha + Yandex SmartCaptcha image mode).
"""

from unittest.mock import patch

from captcha_sdk import CaptchaClient
from captcha_sdk.tasks import CoordinatesTask


class TestCoordinates:

    def test_to_dict(self):
        task = CoordinatesTask(
            body="base64string",
            comment="click on the green apple",
        )
        result = task.to_dict()

        assert result["type"] == "CoordinatesTask"
        assert result["body"] == "base64string"
        assert result["comment"] == "click on the green apple"

    def test_yandex_smartcaptcha_variant(self):
        task = CoordinatesTask(
            body="base64string",
            imgType="smart_captcha",
            imgInstructions="base64instructions",
            comment="select objects in the order of the instruction",
        )
        result = task.to_dict()

        assert result["imgType"] == "smart_captcha"
        assert result["imgInstructions"] == "base64instructions"

    def test_with_click_limits(self):
        task = CoordinatesTask(
            body="base64string",
            minClicks=1,
            maxClicks=5,
        )
        result = task.to_dict()

        assert result["minClicks"] == 1
        assert result["maxClicks"] == 5

    def test_solve(self):
        client = CaptchaClient("test_key", polling_interval=0.1)
        task = CoordinatesTask(body="base64string", comment="click on the green apple")

        with patch.object(client, "_request") as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 108},
                {"errorId": 0, "status": "ready", "solution": {"coordinates": [{"x": 358, "y": 268}]}},
            ]
            result = client.solve(task)

        assert result == {"coordinates": [{"x": 358, "y": 268}]}
