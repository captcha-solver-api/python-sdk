import pytest

from captcha_solver_api import CaptchaClient, ValidationError
from captcha_solver_api.tasks import RecaptchaV2Task, RecaptchaV2TaskProxyless


def test_task_rejects_empty_required_fields_before_request():
    task = RecaptchaV2TaskProxyless(websiteURL=" ", websiteKey="")

    with pytest.raises(
        ValidationError,
        match=r"Missing required task parameter\(s\): websiteURL, websiteKey",
    ):
        task.to_dict()


def test_proxy_task_rejects_empty_required_proxy_fields():
    task = RecaptchaV2Task(
        websiteURL="https://example.com",
        websiteKey="site-key",
        proxyType="",
        proxyAddress="",
        proxyPort=8080,
    )

    with pytest.raises(ValidationError, match="proxyType, proxyAddress"):
        task.to_dict()


def test_create_task_rejects_non_task_value():
    client = CaptchaClient("api-key")

    with pytest.raises(ValidationError, match="task must be an instance of BaseTask"):
        client.create_task(None)
