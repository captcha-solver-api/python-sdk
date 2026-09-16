"""The documented polling schedule applies to both clients, including the first poll."""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

import captcha_solver_api.client as sync_module
import captcha_solver_api.async_client as async_module
from captcha_solver_api import CaptchaClient, AsyncCaptchaClient, CaptchaTimeoutError
from captcha_solver_api.tasks import RecaptchaV2TaskProxyless


class Clock:
    def __init__(self):
        self.now = 0

    def monotonic(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


CASES = [
    (None, 25, [10, 20], False),
    (2, 20, [2, 4], False),
    (None, 3, [], True),
    (5, 7, [5], True),
]


@pytest.mark.parametrize('interval,timeout,expected_polls,times_out', CASES)
def test_sync_polling_schedule(monkeypatch, interval, timeout, expected_polls, times_out):
    clock = Clock()
    polls = []
    monkeypatch.setattr(sync_module, 'time', clock)

    def request(endpoint, payload):
        if endpoint == 'createTask':
            assert clock.now == 0
            return {'errorId': 0, 'taskId': 100}
        assert payload['taskId'] == 100
        polls.append(clock.now)
        if len(polls) == 2:
            return {'errorId': 0, 'status': 'ready', 'solution': {'token': 'done'}}
        return {'errorId': 0, 'status': 'processing'}

    options = {} if interval is None else {'polling_interval': interval}
    with CaptchaClient('test-key', **options) as client:
        monkeypatch.setattr(client, '_request', request)
        task = RecaptchaV2TaskProxyless('https://example.com', 'site-key')
        if times_out:
            with pytest.raises(CaptchaTimeoutError):
                client.solve(task, timeout=timeout)
            assert clock.now == timeout
        else:
            assert client.solve(task, timeout=timeout) == {'token': 'done'}
    assert polls == expected_polls


@pytest.mark.parametrize('interval,timeout,expected_polls,times_out', CASES)
async def test_async_polling_schedule(monkeypatch, interval, timeout, expected_polls, times_out):
    clock = Clock()
    polls = []
    monkeypatch.setattr(async_module, 'time', clock)
    monkeypatch.setattr(async_module, 'asyncio', SimpleNamespace(sleep=AsyncMock(side_effect=clock.sleep)))

    async def request(endpoint, payload):
        if endpoint == 'createTask':
            assert clock.now == 0
            return {'errorId': 0, 'taskId': 100}
        assert payload['taskId'] == 100
        polls.append(clock.now)
        if len(polls) == 2:
            return {'errorId': 0, 'status': 'ready', 'solution': {'token': 'done'}}
        return {'errorId': 0, 'status': 'processing'}

    options = {} if interval is None else {'polling_interval': interval}
    async with AsyncCaptchaClient('test-key', **options) as client:
        monkeypatch.setattr(client, '_request', request)
        task = RecaptchaV2TaskProxyless('https://example.com', 'site-key')
        if times_out:
            with pytest.raises(CaptchaTimeoutError):
                await client.solve(task, timeout=timeout)
            assert clock.now == timeout
        else:
            assert await client.solve(task, timeout=timeout) == {'token': 'done'}
    assert polls == expected_polls
