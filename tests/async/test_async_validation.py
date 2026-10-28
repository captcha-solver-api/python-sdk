import pytest

from captcha_solver_api import AsyncCaptchaClient, ValidationError


@pytest.mark.asyncio
async def test_create_task_rejects_non_task_value():
    async with AsyncCaptchaClient("api-key") as client:
        with pytest.raises(ValidationError, match="task must be an instance of BaseTask"):
            await client.create_task(None)
