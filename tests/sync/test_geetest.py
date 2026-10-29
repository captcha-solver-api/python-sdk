"""
Tests for GeeTestTaskProxyless / GeeTestTask (v3 and v4).
"""

from unittest.mock import patch

import pytest

from captcha_solver_api import CaptchaClient, ValidationError
from captcha_solver_api.tasks import GeeTestTask, GeeTestTaskProxyless


class TestGeeTest:
    @pytest.mark.parametrize(
        "task",
        [
            GeeTestTaskProxyless(websiteURL="https://example.com"),
            GeeTestTask(
                websiteURL="https://example.com",
                proxyType="http",
                proxyAddress="1.2.3.4",
                proxyPort=8080,
            ),
        ],
    )
    def test_v3_requires_gt_and_challenge(self, task):
        with pytest.raises(
            ValidationError,
            match=r"Missing required GeeTest v3 parameter\(s\): gt, challenge",
        ):
            task.to_dict()

    @pytest.mark.parametrize("init_parameters", [None, {}, {"captcha_id": " "}])
    def test_v4_requires_captcha_id(self, init_parameters):
        task = GeeTestTaskProxyless(
            websiteURL="https://example.com",
            version=4,
            initParameters=init_parameters,
        )

        with pytest.raises(
            ValidationError,
            match=r"Missing required GeeTest v4 parameter: initParameters\.captcha_id",
        ):
            task.to_dict()

    def test_rejects_unsupported_version(self):
        task = GeeTestTaskProxyless(
            websiteURL="https://example.com",
            version=5,
        )

        with pytest.raises(ValidationError, match="GeeTest version must be 3 or 4"):
            task.to_dict()

    def test_v3_to_dict(self):
        task = GeeTestTaskProxyless(
            websiteURL="https://example.com",
            gt="test_gt",
            challenge="test_challenge",
        )
        result = task.to_dict()

        assert result["gt"] == "test_gt"
        assert result["challenge"] == "test_challenge"

    def test_v4_to_dict(self):
        task = GeeTestTaskProxyless(
            websiteURL="https://example.com",
            version=4,
            initParameters={"captcha_id": "test_id"},
        )
        result = task.to_dict()

        assert result["version"] == 4
        assert result["initParameters"] == {"captcha_id": "test_id"}

    def test_risk_type_to_dict(self):
        task = GeeTestTaskProxyless(
            websiteURL="https://example.com",
            gt="test_gt",
            challenge="test_challenge",
            risk_type="test_risk_type",
        )
        result = task.to_dict()

        assert result["risk_type"] == "test_risk_type"

    def test_task_with_proxy_to_dict(self):
        task = GeeTestTask(
            websiteURL="https://example.com",
            gt="test_gt",
            challenge="test_challenge",
            proxyType="http",
            proxyAddress="1.2.3.4",
            proxyPort=8080,
        )
        result = task.to_dict()

        assert result["type"] == "GeeTestTask"
        assert result["proxyType"] == "http"
        assert result["proxyAddress"] == "1.2.3.4"

    def test_solve_v3(self):
        client = CaptchaClient("test_key", polling_interval=0.1)
        task = GeeTestTaskProxyless(
            websiteURL="https://example.com", gt="test_gt", challenge="test_challenge"
        )

        with patch.object(client, "_request") as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 105},
                {
                    "errorId": 0,
                    "status": "ready",
                    "solution": {
                        "challenge": "c",
                        "validate": "v",
                        "seccode": "s",
                    },
                },
            ]
            result = client.solve(task)

        assert result == {"challenge": "c", "validate": "v", "seccode": "s"}

    def test_solve_v4(self):
        client = CaptchaClient("test_key", polling_interval=0.1)
        task = GeeTestTaskProxyless(
            websiteURL="https://example.com",
            version=4,
            initParameters={"captcha_id": "test_id"},
        )

        with patch.object(client, "_request") as mock_request:
            mock_request.side_effect = [
                {"errorId": 0, "taskId": 106},
                {
                    "errorId": 0,
                    "status": "ready",
                    "solution": {
                        "captcha_id": "test_id",
                        "lot_number": "1",
                        "pass_token": "p",
                        "gen_time": "t",
                        "captcha_output": "o",
                    },
                },
            ]
            result = client.solve(task)

        assert result["captcha_output"] == "o"
