"""
Task definitions for all supported CAPTCHA types.

Each class maps 1:1 to a `type` value accepted by the API's `createTask`
endpoint. Pass an instance to `CaptchaClient.solve()` (or `create_task()`);
`to_dict()` serializes it into the request body. Optional fields left as
`None` are omitted from the request rather than sent as `null`.

Every class's docstring lists the `solution` fields returned by `solve()`
once the task is `"ready"`.
"""

from __future__ import annotations

import inspect
from typing import Any, Dict, Optional

from .exceptions import ValidationError


class BaseTask:
    """Base class for all CAPTCHA tasks."""

    type: str

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the task to the dict shape expected by the `task` field
        of `createTask`, dropping any fields left as `None`."""
        self._validate_required_fields()
        result = {"type": self.type}
        for key, value in self.__dict__.items():
            if value is not None:
                result[key] = value
        return result

    def _validate_required_fields(self) -> None:
        """Reject missing values for constructor parameters without defaults."""
        parameters = inspect.signature(type(self).__init__).parameters
        missing = []
        for name, parameter in parameters.items():
            if name == "self" or parameter.default is not inspect.Parameter.empty:
                continue
            value = getattr(self, name, None)
            if value is None or (isinstance(value, str) and not value.strip()):
                missing.append(name)
        if missing:
            fields = ", ".join(missing)
            raise ValidationError(f"Missing required task parameter(s): {fields}")
        self._validate_specific_fields()

    def _validate_specific_fields(self) -> None:
        """Validate task-specific requirements that depend on other fields."""


class ProxyMixin:
    """Mixin that adds proxy fields to a task.

    Args (via `set_proxy`, or pass directly to the task's `__init__`):
        proxy_type: Required. `"http"`, `"socks4"`, or `"socks5"`.
        proxy_address: Required. Proxy IP address or hostname.
        proxy_port: Required. Proxy port.
        proxy_login: Optional. Proxy auth username, if required.
        proxy_password: Optional. Proxy auth password, if required.
    """

    proxyType: str
    proxyAddress: str
    proxyPort: int
    proxyLogin: Optional[str]
    proxyPassword: Optional[str]

    def set_proxy(
        self,
        proxy_type: str,
        proxy_address: str,
        proxy_port: int,
        proxy_login: Optional[str] = None,
        proxy_password: Optional[str] = None,
    ) -> None:
        """Sets the proxy fields on this task.

        Args:
            proxy_type: Required. `"http"`, `"socks4"`, or `"socks5"`.
            proxy_address: Required. Proxy IP address or hostname.
            proxy_port: Required. Proxy port.
            proxy_login: Optional. Proxy auth username, if required.
            proxy_password: Optional. Proxy auth password, if required.
        """
        self.proxyType = proxy_type
        self.proxyAddress = proxy_address
        self.proxyPort = proxy_port
        self.proxyLogin = proxy_login
        self.proxyPassword = proxy_password


class RecaptchaV2TaskProxyless(BaseTask):
    """reCAPTCHA v2 without proxy -- the service solves using its own IPs.

    Args:
        websiteURL: Required. Full URL of the page where the captcha is located.
        websiteKey: Required. Value of the widget's `data-sitekey` attribute.
        isInvisible: Optional. `True` for invisible reCAPTCHA v2.
        recaptchaDataSValue: Optional. The `data-s` value, found on Google Search/YouTube pages.
        apiDomain: Optional. Non-default domain the widget's script is served from, if any.
        userAgent: Optional. User-Agent to solve with. Recommended to match the agent that
            will submit the resulting token.
        cookies: Optional. Session cookies to use while solving, if the page requires them.

    Returns (`solution` from `solve()`):
        `gRecaptchaResponse` -- the token to submit as `g-recaptcha-response`.

    Example:
        from captcha_solver_api.tasks import RecaptchaV2TaskProxyless

        task = RecaptchaV2TaskProxyless(
            websiteURL="https://example.com",
            websiteKey="SITE_KEY",
        )
        solution = client.solve(task)
        answer = solution["gRecaptchaResponse"]

    Note:
        Optional arguments default to `None` and are omitted from the request.
    """

    type = "RecaptchaV2TaskProxyless"

    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        isInvisible: Optional[bool] = None,
        recaptchaDataSValue: Optional[str] = None,
        apiDomain: Optional[str] = None,
        userAgent: Optional[str] = None,
        cookies: Optional[str] = None,
    ) -> None:
        self.websiteURL = websiteURL
        self.websiteKey = websiteKey
        self.isInvisible = isInvisible
        self.recaptchaDataSValue = recaptchaDataSValue
        self.apiDomain = apiDomain
        self.userAgent = userAgent
        self.cookies = cookies


class RecaptchaV2Task(BaseTask, ProxyMixin):
    """reCAPTCHA v2 solved through your own proxy.

    Use this instead of `RecaptchaV2TaskProxyless` when the target site is
    geo-restricted or you need the solving session to share an IP with the
    browser/bot that will submit the token.

    Args:
        websiteURL: Required. Full URL of the page where the captcha is located.
        websiteKey: Required. Value of the widget's `data-sitekey` attribute.
        proxyType: Required. `"http"`, `"socks4"`, or `"socks5"`.
        proxyAddress: Required. Proxy IP address or hostname.
        proxyPort: Required. Proxy port.
        proxyLogin: Optional. Proxy auth username, if required.
        proxyPassword: Optional. Proxy auth password, if required.
        isInvisible: Optional. `True` for invisible reCAPTCHA v2.
        recaptchaDataSValue: Optional. The `data-s` value, found on Google Search/YouTube pages.
        apiDomain: Optional. Non-default domain the widget's script is served from, if any.
        userAgent: Optional. User-Agent to solve with.
        cookies: Optional. Session cookies to use while solving, if the page requires them.

    Returns (`solution` from `solve()`):
        `gRecaptchaResponse` -- the token to submit as `g-recaptcha-response`.

    Example:
        from captcha_solver_api.tasks import RecaptchaV2Task

        task = RecaptchaV2Task(
            websiteURL="https://example.com",
            websiteKey="SITE_KEY",
            proxyType="http",
            proxyAddress="proxy.example.com",
            proxyPort=8080,
        )
        solution = client.solve(task)
        answer = solution["gRecaptchaResponse"]

    Note:
        Optional arguments default to `None` and are omitted from the request.
    """

    type = "RecaptchaV2Task"

    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        proxyType: str,
        proxyAddress: str,
        proxyPort: int,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        isInvisible: Optional[bool] = None,
        recaptchaDataSValue: Optional[str] = None,
        apiDomain: Optional[str] = None,
        userAgent: Optional[str] = None,
        cookies: Optional[str] = None,
    ) -> None:
        self.websiteURL = websiteURL
        self.websiteKey = websiteKey
        self.proxyType = proxyType
        self.proxyAddress = proxyAddress
        self.proxyPort = proxyPort
        self.proxyLogin = proxyLogin
        self.proxyPassword = proxyPassword
        self.isInvisible = isInvisible
        self.recaptchaDataSValue = recaptchaDataSValue
        self.apiDomain = apiDomain
        self.userAgent = userAgent
        self.cookies = cookies


class RecaptchaV2EnterpriseTaskProxyless(BaseTask):
    """reCAPTCHA v2 Enterprise without proxy.

    Args:
        websiteURL: Required. Full URL of the page where the captcha is located.
        websiteKey: Required. Value of the widget's `data-sitekey` attribute.
        enterprisePayload: Optional. Extra parameters passed to `grecaptcha.enterprise.render`
            on the page, if any (e.g. `{"s": "..."}`).
        isInvisible: Optional. `True` for invisible reCAPTCHA v2 Enterprise.
        apiDomain: Optional. Non-default domain, defaults to `google.com`.
        userAgent: Optional. User-Agent to solve with.
        cookies: Optional. Session cookies to use while solving, if the page requires them.

    Returns (`solution` from `solve()`):
        `gRecaptchaResponse` -- the token to submit as `g-recaptcha-response`.

    Example:
        from captcha_solver_api.tasks import RecaptchaV2EnterpriseTaskProxyless

        task = RecaptchaV2EnterpriseTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="SITE_KEY",
        )
        solution = client.solve(task)
        answer = solution["gRecaptchaResponse"]

    Note:
        Optional arguments default to `None` and are omitted from the request.
    """

    type = "RecaptchaV2EnterpriseTaskProxyless"

    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        enterprisePayload: Optional[Dict[str, Any]] = None,
        isInvisible: Optional[bool] = None,
        apiDomain: Optional[str] = None,
        userAgent: Optional[str] = None,
        cookies: Optional[str] = None,
    ) -> None:
        self.websiteURL = websiteURL
        self.websiteKey = websiteKey
        self.enterprisePayload = enterprisePayload
        self.isInvisible = isInvisible
        self.apiDomain = apiDomain
        self.userAgent = userAgent
        self.cookies = cookies


class RecaptchaV2EnterpriseTask(BaseTask, ProxyMixin):
    """reCAPTCHA v2 Enterprise solved through your own proxy.

    Args:
        websiteURL: Required. Full URL of the page where the captcha is located.
        websiteKey: Required. Value of the widget's `data-sitekey` attribute.
        proxyType: Required. `"http"`, `"socks4"`, or `"socks5"`.
        proxyAddress: Required. Proxy IP address or hostname.
        proxyPort: Required. Proxy port.
        proxyLogin: Optional. Proxy auth username, if required.
        proxyPassword: Optional. Proxy auth password, if required.
        enterprisePayload: Optional. Extra parameters passed to `grecaptcha.enterprise.render`
            on the page, if any (e.g. `{"s": "..."}`).
        isInvisible: Optional. `True` for invisible reCAPTCHA v2 Enterprise.
        apiDomain: Optional. Non-default domain, defaults to `google.com`.
        userAgent: Optional. User-Agent to solve with.
        cookies: Optional. Session cookies to use while solving, if the page requires them.

    Returns (`solution` from `solve()`):
        `gRecaptchaResponse` -- the token to submit as `g-recaptcha-response`.

    Example:
        from captcha_solver_api.tasks import RecaptchaV2EnterpriseTask

        task = RecaptchaV2EnterpriseTask(
            websiteURL="https://example.com",
            websiteKey="SITE_KEY",
            proxyType="http",
            proxyAddress="proxy.example.com",
            proxyPort=8080,
        )
        solution = client.solve(task)
        answer = solution["gRecaptchaResponse"]

    Note:
        Optional arguments default to `None` and are omitted from the request.
    """

    type = "RecaptchaV2EnterpriseTask"

    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        proxyType: str,
        proxyAddress: str,
        proxyPort: int,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        enterprisePayload: Optional[Dict[str, Any]] = None,
        isInvisible: Optional[bool] = None,
        apiDomain: Optional[str] = None,
        userAgent: Optional[str] = None,
        cookies: Optional[str] = None,
    ) -> None:
        self.websiteURL = websiteURL
        self.websiteKey = websiteKey
        self.proxyType = proxyType
        self.proxyAddress = proxyAddress
        self.proxyPort = proxyPort
        self.proxyLogin = proxyLogin
        self.proxyPassword = proxyPassword
        self.enterprisePayload = enterprisePayload
        self.isInvisible = isInvisible
        self.apiDomain = apiDomain
        self.userAgent = userAgent
        self.cookies = cookies


class RecaptchaV3TaskProxyless(BaseTask):
    """reCAPTCHA v3. No proxy variant exists for this type -- v3 is score-based
    and invisible, so there's no widget/session to keep pinned to a proxy IP.

    Args:
        websiteURL: Required. Full URL of the page where the captcha is located.
        websiteKey: Required. Site key for the v3 widget.
        minScore: Required. Minimum acceptable token score to return, e.g. `0.3`, `0.7`, `0.9`.
        pageAction: Optional. The `action` parameter passed to `grecaptcha.execute()` on the page.
        isEnterprise: Optional. `True` if this is reCAPTCHA v3 Enterprise.
        apiDomain: Optional. Non-standard domain the widget's script is served from, if any.

    Returns (`solution` from `solve()`):
        `gRecaptchaResponse` -- the token to submit as `g-recaptcha-response`.

    Example:
        from captcha_solver_api.tasks import RecaptchaV3TaskProxyless

        task = RecaptchaV3TaskProxyless(
            websiteURL="https://example.com",
            websiteKey="SITE_KEY",
            minScore=0.3,
            pageAction="login",
        )
        solution = client.solve(task)
        answer = solution["gRecaptchaResponse"]

    Note:
        Optional arguments default to `None` and are omitted from the request.
    """

    type = "RecaptchaV3TaskProxyless"

    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        minScore: float,
        pageAction: Optional[str] = None,
        isEnterprise: Optional[bool] = None,
        apiDomain: Optional[str] = None,
    ) -> None:
        self.websiteURL = websiteURL
        self.websiteKey = websiteKey
        self.minScore = minScore
        self.pageAction = pageAction
        self.isEnterprise = isEnterprise
        self.apiDomain = apiDomain


class TurnstileTaskProxyless(BaseTask):
    """Cloudflare Turnstile without proxy.

    Args:
        websiteURL: Required. Full URL of the page where the widget is located.
        websiteKey: Required. Value of the widget's `data-sitekey` attribute.
        action: Optional. Value of the widget's `data-action` attribute, if set.
        data: Optional. Custom payload from the widget's `data-cdata` attribute, if set.
        pagedata: Optional. Value of the `chlPageData` parameter, needed for some Cloudflare
            challenge pages beyond the basic widget. Named lowercase (not `pageData`)
            to match the API field name exactly -- Cloudflare-specific fields are
            the one place this API doesn't camelCase.
        userAgent: Optional. User-Agent of the browser that loaded the challenge. Pass it
            together with `action`, `data`, and `pagedata` for Cloudflare
            Challenge pages. It is not needed for a standalone widget.

    Returns (`solution` from `solve()`):
        `token` -- the value to submit as `cf-turnstile-response`.
        `userAgent` -- for Cloudflare Challenge pages, switch the browser or HTTP
            client to this returned User-Agent before invoking the callback.

    Example:
        from captcha_solver_api.tasks import TurnstileTaskProxyless

        task = TurnstileTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="SITE_KEY",
        )
        solution = client.solve(task)
        answer = solution["token"]

    Note:
        Optional arguments default to `None` and are omitted from the request.
    """

    type = "TurnstileTaskProxyless"

    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        action: Optional[str] = None,
        data: Optional[str] = None,
        pagedata: Optional[str] = None,
        userAgent: Optional[str] = None,
    ) -> None:
        self.websiteURL = websiteURL
        self.websiteKey = websiteKey
        self.action = action
        self.data = data
        self.pagedata = pagedata
        self.userAgent = userAgent


class TurnstileTask(BaseTask, ProxyMixin):
    """Cloudflare Turnstile solved through your own proxy.

    Args:
        websiteURL: Required. Full URL of the page where the widget is located.
        websiteKey: Required. Value of the widget's `data-sitekey` attribute.
        proxyType: Required. `"http"`, `"socks4"`, or `"socks5"`.
        proxyAddress: Required. Proxy IP address or hostname.
        proxyPort: Required. Proxy port.
        proxyLogin: Optional. Proxy auth username, if required.
        proxyPassword: Optional. Proxy auth password, if required.
        action: Optional. Value of the widget's `data-action` attribute, if set.
        data: Optional. Custom payload from the widget's `data-cdata` attribute, if set.
        pagedata: Optional. Value of the `chlPageData` parameter, needed for some Cloudflare
            challenge pages beyond the basic widget. Named lowercase (not `pageData`)
            to match the API field name exactly.
        userAgent: Optional. User-Agent of the browser that loaded the challenge. Pass it
            for Cloudflare Challenge pages; it is not needed for a standalone
            widget.

    Returns (`solution` from `solve()`):
        `token` -- the value to submit as `cf-turnstile-response`.
        `userAgent` -- for Cloudflare Challenge pages, switch the browser or HTTP
            client to this returned User-Agent before invoking the callback.

    Example:
        from captcha_solver_api.tasks import TurnstileTask

        task = TurnstileTask(
            websiteURL="https://example.com",
            websiteKey="SITE_KEY",
            proxyType="http",
            proxyAddress="proxy.example.com",
            proxyPort=8080,
        )
        solution = client.solve(task)
        answer = solution["token"]

    Note:
        Optional arguments default to `None` and are omitted from the request.
    """

    type = "TurnstileTask"

    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        proxyType: str,
        proxyAddress: str,
        proxyPort: int,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        action: Optional[str] = None,
        data: Optional[str] = None,
        pagedata: Optional[str] = None,
        userAgent: Optional[str] = None,
    ) -> None:
        self.websiteURL = websiteURL
        self.websiteKey = websiteKey
        self.proxyType = proxyType
        self.proxyAddress = proxyAddress
        self.proxyPort = proxyPort
        self.proxyLogin = proxyLogin
        self.proxyPassword = proxyPassword
        self.action = action
        self.data = data
        self.pagedata = pagedata
        self.userAgent = userAgent


class ImageToTextTask(BaseTask):
    """Image-to-text recognition for classic distorted-text/number captchas.
    No proxy variant exists -- the image is submitted directly, no browser
    session or target site is involved.

    Args:
        body: Required. The captcha image, base64-encoded (no `data:image/...;base64,` prefix).
        phrase: Optional. `True` if the answer is multiple words.
        case: Optional. `True` if the answer is case-sensitive.
        numeric: Optional. Character set hint -- `0` unspecified, `1` digits only, `2` letters
            only, `3` any with digits, `4` any with letters.
        math: Optional. `True` if the image contains a math expression to evaluate rather
            than text to transcribe.
        minLength: Optional. Minimum expected answer length.
        maxLength: Optional. Maximum expected answer length.
        comment: Optional. Free-text hint for the worker (e.g. what kind of answer is expected).
        imgInstructions: Optional. Optional supplementary instruction image, base64-encoded.

    Returns (`solution` from `solve()`):
        `text` -- the recognized text/answer.

    Example:
        from captcha_solver_api.tasks import ImageToTextTask

        task = ImageToTextTask(
            body="BASE64_IMAGE",
        )
        solution = client.solve(task)
        answer = solution["text"]

    Note:
        Optional arguments default to `None` and are omitted from the request.
    """

    type = "ImageToTextTask"

    def __init__(
        self,
        body: str,
        phrase: Optional[bool] = None,
        case: Optional[bool] = None,
        numeric: Optional[int] = None,
        math: Optional[bool] = None,
        minLength: Optional[int] = None,
        maxLength: Optional[int] = None,
        comment: Optional[str] = None,
        imgInstructions: Optional[str] = None,
    ) -> None:
        self.body = body
        self.phrase = phrase
        self.case = case
        self.numeric = numeric
        self.math = math
        self.minLength = minLength
        self.maxLength = maxLength
        self.comment = comment
        self.imgInstructions = imgInstructions


def _validate_geetest_fields(task: Any) -> None:
    """Validate fields whose required status depends on the GeeTest version."""
    version = 3 if task.version is None else task.version
    if version not in (3, 4):
        raise ValidationError("GeeTest version must be 3 or 4")

    if version == 3:
        missing = [
            name
            for name in ("gt", "challenge")
            if not isinstance(getattr(task, name, None), str) or not getattr(task, name).strip()
        ]
        if missing:
            fields = ", ".join(missing)
            raise ValidationError(f"Missing required GeeTest v3 parameter(s): {fields}")
        return

    init_parameters = task.initParameters
    captcha_id = init_parameters.get("captcha_id") if isinstance(init_parameters, dict) else None
    if not isinstance(captcha_id, str) or not captcha_id.strip():
        raise ValidationError("Missing required GeeTest v4 parameter: initParameters.captcha_id")


class GeeTestTaskProxyless(BaseTask):
    """GeeTest v3 or v4 without proxy. Set `version=4` for v4 (and provide
    `initParameters["captcha_id"]`); v3 is the default and needs `gt`/`challenge`
    instead.

    Args:
        websiteURL: Required. Full URL of the page where the widget is located.
        version: Optional. `3` (default) or `4`.
        gt: Optional. Public key of the GeeTest widget. Required for v3.
        challenge: Optional. Session-specific challenge value from the page. Required for
            v3, and must be freshly fetched for every request -- it cannot be reused.
        initParameters: Optional. Extra parameters from the page's `initGeetest` call. For
            v4, must contain `captcha_id`.
        geetestApiServerSubdomain: Optional. Custom GeeTest API subdomain, if the site uses one.
        userAgent: Optional. User-Agent to solve with.
        risk_type: Optional. Value of the `risk_type` parameter from the captcha-loading
            request, if present. Dynamic, single-use, and time-limited.

    Returns (`solution` from `solve()`):
        v3: `challenge`, `validate`, `seccode`.
        v4: `captcha_id`, `lot_number`, `pass_token`, `gen_time`, `captcha_output`.

    Example:
        from captcha_solver_api.tasks import GeeTestTaskProxyless

        task = GeeTestTaskProxyless(
            websiteURL="https://example.com",
            version=4,
            initParameters={"captcha_id": "CAPTCHA_ID"},
        )
        solution = client.solve(task)
        answer = solution["captcha_output"]

    Note:
        Optional arguments default to `None` and are omitted from the request.
    """

    type = "GeeTestTaskProxyless"

    def _validate_specific_fields(self) -> None:
        _validate_geetest_fields(self)

    def __init__(
        self,
        websiteURL: str,
        version: Optional[int] = None,
        gt: Optional[str] = None,
        challenge: Optional[str] = None,
        initParameters: Optional[Dict[str, Any]] = None,
        geetestApiServerSubdomain: Optional[str] = None,
        userAgent: Optional[str] = None,
        risk_type: Optional[str] = None,
    ) -> None:
        self.websiteURL = websiteURL
        self.version = version
        self.gt = gt
        self.challenge = challenge
        self.initParameters = initParameters
        self.geetestApiServerSubdomain = geetestApiServerSubdomain
        self.userAgent = userAgent
        self.risk_type = risk_type


class GeeTestTask(BaseTask, ProxyMixin):
    """GeeTest v3 or v4 solved through your own proxy. See `GeeTestTaskProxyless`
    for the version-specific fields.

    Args:
        websiteURL: Required. Full URL of the page where the widget is located.
        proxyType: Required. `"http"`, `"socks4"`, or `"socks5"`.
        proxyAddress: Required. Proxy IP address or hostname.
        proxyPort: Required. Proxy port.
        proxyLogin: Optional. Proxy auth username, if required.
        proxyPassword: Optional. Proxy auth password, if required.
        version: Optional. `3` (default) or `4`.
        gt: Optional. Public key of the GeeTest widget. Required for v3.
        challenge: Optional. Session-specific challenge value from the page, must be fresh.
            Required for v3.
        initParameters: Optional. Extra parameters from the page's `initGeetest` call. For
            v4, must contain `captcha_id`.
        geetestApiServerSubdomain: Optional. Custom GeeTest API subdomain, if the site uses one.
        userAgent: Optional. User-Agent to solve with.
        risk_type: Optional. Value of the `risk_type` parameter from the captcha-loading
            request, if present. Dynamic, single-use, and time-limited.

    Returns (`solution` from `solve()`):
        v3: `challenge`, `validate`, `seccode`.
        v4: `captcha_id`, `lot_number`, `pass_token`, `gen_time`, `captcha_output`.

    Example:
        from captcha_solver_api.tasks import GeeTestTask

        task = GeeTestTask(
            websiteURL="https://example.com",
            version=4,
            initParameters={"captcha_id": "CAPTCHA_ID"},
            proxyType="http",
            proxyAddress="proxy.example.com",
            proxyPort=8080,
        )
        solution = client.solve(task)
        answer = solution["captcha_output"]

    Note:
        Optional arguments default to `None` and are omitted from the request.
    """

    type = "GeeTestTask"

    def _validate_specific_fields(self) -> None:
        _validate_geetest_fields(self)

    def __init__(
        self,
        websiteURL: str,
        proxyType: str,
        proxyAddress: str,
        proxyPort: int,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        version: Optional[int] = None,
        gt: Optional[str] = None,
        challenge: Optional[str] = None,
        initParameters: Optional[Dict[str, Any]] = None,
        geetestApiServerSubdomain: Optional[str] = None,
        userAgent: Optional[str] = None,
        risk_type: Optional[str] = None,
    ) -> None:
        self.websiteURL = websiteURL
        self.proxyType = proxyType
        self.proxyAddress = proxyAddress
        self.proxyPort = proxyPort
        self.proxyLogin = proxyLogin
        self.proxyPassword = proxyPassword
        self.version = version
        self.gt = gt
        self.challenge = challenge
        self.initParameters = initParameters
        self.geetestApiServerSubdomain = geetestApiServerSubdomain
        self.userAgent = userAgent
        self.risk_type = risk_type


class YandexSmartCaptchaTaskProxyless(BaseTask):
    """Yandex SmartCaptcha (token challenge) without proxy.

    Args:
        websiteURL: Required. Full URL of the page where the widget is located.
        websiteKey: Required. The `sitekey` value from the page source or captcha iframe.
        userAgent: Optional. User-Agent to solve with.
        cookies: Optional. Session cookies to use while solving, if the page requires them.

    Returns (`solution` from `solve()`):
        `token` -- the value to submit as the SmartCaptcha response token.

    Example:
        from captcha_solver_api.tasks import YandexSmartCaptchaTaskProxyless

        task = YandexSmartCaptchaTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="SITE_KEY",
        )
        solution = client.solve(task)
        answer = solution["token"]

    Note:
        Optional arguments default to `None` and are omitted from the request.
    """

    type = "YandexSmartCaptchaTaskProxyless"

    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        userAgent: Optional[str] = None,
        cookies: Optional[str] = None,
    ) -> None:
        self.websiteURL = websiteURL
        self.websiteKey = websiteKey
        self.userAgent = userAgent
        self.cookies = cookies


class YandexSmartCaptchaTask(BaseTask, ProxyMixin):
    """Yandex SmartCaptcha (token challenge) solved through your own proxy.

    Args:
        websiteURL: Required. Full URL of the page where the widget is located.
        websiteKey: Required. The `sitekey` value from the page source or captcha iframe.
        proxyType: Required. `"http"`, `"socks4"`, or `"socks5"`.
        proxyAddress: Required. Proxy IP address or hostname.
        proxyPort: Required. Proxy port.
        proxyLogin: Optional. Proxy auth username, if required.
        proxyPassword: Optional. Proxy auth password, if required.
        userAgent: Optional. User-Agent to solve with.
        cookies: Optional. Session cookies to use while solving, if the page requires them.

    Returns (`solution` from `solve()`):
        `token` -- the value to submit as the SmartCaptcha response token.

    Example:
        from captcha_solver_api.tasks import YandexSmartCaptchaTask

        task = YandexSmartCaptchaTask(
            websiteURL="https://example.com",
            websiteKey="SITE_KEY",
            proxyType="http",
            proxyAddress="proxy.example.com",
            proxyPort=8080,
        )
        solution = client.solve(task)
        answer = solution["token"]

    Note:
        Optional arguments default to `None` and are omitted from the request.
    """

    type = "YandexSmartCaptchaTask"

    def __init__(
        self,
        websiteURL: str,
        websiteKey: str,
        proxyType: str,
        proxyAddress: str,
        proxyPort: int,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        userAgent: Optional[str] = None,
        cookies: Optional[str] = None,
    ) -> None:
        self.websiteURL = websiteURL
        self.websiteKey = websiteKey
        self.proxyType = proxyType
        self.proxyAddress = proxyAddress
        self.proxyPort = proxyPort
        self.proxyLogin = proxyLogin
        self.proxyPassword = proxyPassword
        self.userAgent = userAgent
        self.cookies = cookies


class CoordinatesTask(BaseTask):
    """Coordinate-based (click) image captcha. No proxy variant -- the image
    is submitted directly.

    Args:
        body: Required. The captcha image, base64-encoded (no `data:image/...;base64,` prefix).
        comment: Optional. Hint for the worker, e.g. `"click on the green apple"`. Recommended
            for generic click captchas.
        imgInstructions: Optional. Optional instruction image, base64-encoded.
        minClicks: Optional. Minimum number of clicks expected (default `1`).
        maxClicks: Optional. Maximum number of clicks allowed.

    Returns (`solution` from `solve()`):
        `coordinates` -- a list of `{"x": int, "y": int}` pixel positions to click,
        in order.

    Example:
        from captcha_solver_api.tasks import CoordinatesTask

        task = CoordinatesTask(
            body="BASE64_IMAGE",
            comment="Click on the green apple",
        )
        solution = client.solve(task)
        answer = solution["coordinates"]

    Note:
        Optional arguments default to `None` and are omitted from the request.
    """

    type = "CoordinatesTask"

    def __init__(
        self,
        body: str,
        comment: Optional[str] = None,
        imgInstructions: Optional[str] = None,
        minClicks: Optional[int] = None,
        maxClicks: Optional[int] = None,
    ) -> None:
        self.body = body
        self.comment = comment
        self.imgInstructions = imgInstructions
        self.minClicks = minClicks
        self.maxClicks = maxClicks


class TencentTaskProxyless(BaseTask):
    """Tencent captcha without proxy.

    Args:
        websiteURL: Required. Full URL of the page where the captcha is located.
        appId: Required. Value of the `appId` parameter found in the page source.
        captchaScript: Optional. URL of the Tencent captcha script, if the page uses a
            non-default one.

    Returns (`solution` from `solve()`):
        `appid`, `ret`, `ticket`, `randstr` -- pass these to the page's Tencent
        captcha callback.

    Example:
        from captcha_solver_api.tasks import TencentTaskProxyless

        task = TencentTaskProxyless(
            websiteURL="https://example.com",
            appId="APP_ID",
        )
        solution = client.solve(task)
        answer = solution["ticket"]

    Note:
        Optional arguments default to `None` and are omitted from the request.
    """

    type = "TencentTaskProxyless"

    def __init__(
        self,
        websiteURL: str,
        appId: str,
        captchaScript: Optional[str] = None,
    ) -> None:
        self.websiteURL = websiteURL
        self.appId = appId
        self.captchaScript = captchaScript


class TencentTask(BaseTask, ProxyMixin):
    """Tencent captcha solved through your own proxy.

    Args:
        websiteURL: Required. Full URL of the page where the captcha is located.
        appId: Required. Value of the `appId` parameter found in the page source.
        proxyType: Required. `"http"`, `"socks4"`, or `"socks5"`.
        proxyAddress: Required. Proxy IP address or hostname.
        proxyPort: Required. Proxy port.
        proxyLogin: Optional. Proxy auth username, if required.
        proxyPassword: Optional. Proxy auth password, if required.
        captchaScript: Optional. URL of the Tencent captcha script, if the page uses a
            non-default one.

    Returns (`solution` from `solve()`):
        `appid`, `ret`, `ticket`, `randstr` -- pass these to the page's Tencent
        captcha callback.

    Example:
        from captcha_solver_api.tasks import TencentTask

        task = TencentTask(
            websiteURL="https://example.com",
            appId="APP_ID",
            proxyType="http",
            proxyAddress="proxy.example.com",
            proxyPort=8080,
        )
        solution = client.solve(task)
        answer = solution["ticket"]

    Note:
        Optional arguments default to `None` and are omitted from the request.
    """

    type = "TencentTask"

    def __init__(
        self,
        websiteURL: str,
        appId: str,
        proxyType: str,
        proxyAddress: str,
        proxyPort: int,
        proxyLogin: Optional[str] = None,
        proxyPassword: Optional[str] = None,
        captchaScript: Optional[str] = None,
    ) -> None:
        self.websiteURL = websiteURL
        self.appId = appId
        self.proxyType = proxyType
        self.proxyAddress = proxyAddress
        self.proxyPort = proxyPort
        self.proxyLogin = proxyLogin
        self.proxyPassword = proxyPassword
        self.captchaScript = captchaScript
