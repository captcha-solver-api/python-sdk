"""Tests for YandexSmartCaptchaKaleidoscopeTask."""

import pytest

from captcha_solver_api import ValidationError
from captcha_solver_api.tasks import YandexSmartCaptchaKaleidoscopeTask


class TestYandexSmartCaptchaKaleidoscope:
    def test_to_dict_uses_api_v2_task_type(self):
        task = YandexSmartCaptchaKaleidoscopeTask(
            image="captcha-image",
            task="[7,15,14,0]",
        )

        assert task.to_dict() == {
            "type": "PazlCaptchaTask",
            "image": "captcha-image",
            "task": "[7,15,14,0]",
        }

    @pytest.mark.parametrize(
        "image,task,missing",
        [("", "[7,15,14,0]", "image"), ("captcha-image", " ", "task")],
    )
    def test_required_fields_are_validated(self, image, task, missing):
        captcha = YandexSmartCaptchaKaleidoscopeTask(image=image, task=task)

        with pytest.raises(ValidationError, match=missing):
            captcha.to_dict()
