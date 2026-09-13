"""
The backend uses the `X-SDK` header to collect SDK usage stats. These tests
send real HTTP requests to a local server and check the header arrives.
"""

from captcha_sdk import AsyncCaptchaClient, CaptchaClient, __version__

EXPECTED_SDK_HEADER = f"python-sdk/{__version__}"


def test_sync_client_sends_sdk_header(api_server):
    with CaptchaClient("test_key", base_url=api_server.url) as client:
        assert client.get_balance() == 5.0

    assert len(api_server.requests) == 1
    request = api_server.requests[0]
    assert request["path"] == "/getBalance"
    assert request["headers"]["X-SDK"] == EXPECTED_SDK_HEADER


async def test_async_client_sends_sdk_header(api_server):
    async with AsyncCaptchaClient("test_key", base_url=api_server.url) as client:
        assert await client.get_balance() == 5.0

    assert len(api_server.requests) == 1
    request = api_server.requests[0]
    assert request["path"] == "/getBalance"
    assert request["headers"]["X-SDK"] == EXPECTED_SDK_HEADER
