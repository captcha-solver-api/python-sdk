"""Tests for YandexSmartCaptchaImageTask."""

from captcha_solver_api.tasks import YandexSmartCaptchaImageTask


class TestYandexSmartCaptchaImage:
    def test_to_dict_uses_api_v2_task_type(self):
        task = YandexSmartCaptchaImageTask(
            image="captcha-image",
            imgInstructions="instruction-image",
            comment="click the symbols in the specified order",
        )

        assert task.to_dict() == {
            "type": "SmartCaptchaTask",
            "image": "captcha-image",
            "imgInstructions": "instruction-image",
            "comment": "click the symbols in the specified order",
        }

    def test_optional_comment_is_omitted(self):
        task = YandexSmartCaptchaImageTask("captcha-image", "instruction-image")
        assert "comment" not in task.to_dict()
