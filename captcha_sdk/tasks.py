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

from typing import Any, Dict, List, Optional


class BaseTask:
    """Base class for all CAPTCHA tasks."""

    type: str

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the task to the dict shape expected by the `task` field
        of `createTask`, dropping any fields left as `None`."""
        result = {"type": self.type}
        for key, value in self.__dict__.items():
            if value is not None:
                result[key] = value
        return result


class ProxyMixin:
    """Mixin that adds proxy fields to a task.

    Args (via `set_proxy`, or pass directly to the task's `__init__`):
        proxy_type: `"http"`, `"socks4"`, or `"socks5"`.
        proxy_address: Proxy IP address or hostname.
        proxy_port: Proxy port.
        proxy_login: Proxy auth username, if required.
        proxy_password: Proxy auth password, if required.
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
        self.proxyType = proxy_type
        self.proxyAddress = proxy_address
        self.proxyPort = proxy_port
        self.proxyLogin = proxy_login
        self.proxyPassword = proxy_password


class RecaptchaV2TaskProxyless(BaseTask):
    """reCAPTCHA v2 without proxy -- the service solves using its own IPs.

    Args:
        websiteURL: Full URL of the page where the captcha is located.
        websiteKey: Value of the widget's `data-sitekey` attribute.
        isInvisible: `True` for invisible reCAPTCHA v2.
        recaptchaDataSValue: The `data-s` value, found on Google Search/YouTube pages.
        apiDomain: Non-default domain the widget's script is served from, if any.
        userAgent: User-Agent to solve with. Recommended to match the agent that
            will submit the resulting token.
        cookies: Session cookies to use while solving, if the page requires them.

    Returns (`solution` from `solve()`):
        `gRecaptchaResponse` -- the token to submit as `g-recaptcha-response`.
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
        websiteURL: Full URL of the page where the captcha is located.
        websiteKey: Value of the widget's `data-sitekey` attribute.
        proxyType: `"http"`, `"socks4"`, or `"socks5"`.
        proxyAddress: Proxy IP address or hostname.
        proxyPort: Proxy port.
        proxyLogin: Proxy auth username, if required.
        proxyPassword: Proxy auth password, if required.
        isInvisible: `True` for invisible reCAPTCHA v2.
        recaptchaDataSValue: The `data-s` value, found on Google Search/YouTube pages.
        apiDomain: Non-default domain the widget's script is served from, if any.
        userAgent: User-Agent to solve with.
        cookies: Session cookies to use while solving, if the page requires them.

    Returns (`solution` from `solve()`):
        `gRecaptchaResponse` -- the token to submit as `g-recaptcha-response`.
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
        websiteURL: Full URL of the page where the captcha is located.
        websiteKey: Value of the widget's `data-sitekey` attribute.
        enterprisePayload: Extra parameters passed to `grecaptcha.enterprise.render`
            on the page, if any (e.g. `{"s": "..."}`).
        isInvisible: `True` for invisible reCAPTCHA v2 Enterprise.
        apiDomain: Non-default domain, defaults to `google.com`.
        userAgent: User-Agent to solve with.
        cookies: Session cookies to use while solving, if the page requires them.

    Returns (`solution` from `solve()`):
        `gRecaptchaResponse` -- the token to submit as `g-recaptcha-response`.
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
        websiteURL: Full URL of the page where the captcha is located.
        websiteKey: Value of the widget's `data-sitekey` attribute.
        proxyType: `"http"`, `"socks4"`, or `"socks5"`.
        proxyAddress: Proxy IP address or hostname.
        proxyPort: Proxy port.
        proxyLogin: Proxy auth username, if required.
        proxyPassword: Proxy auth password, if required.
        enterprisePayload: Extra parameters passed to `grecaptcha.enterprise.render`
            on the page, if any (e.g. `{"s": "..."}`).
        isInvisible: `True` for invisible reCAPTCHA v2 Enterprise.
        apiDomain: Non-default domain, defaults to `google.com`.
        userAgent: User-Agent to solve with.
        cookies: Session cookies to use while solving, if the page requires them.

    Returns (`solution` from `solve()`):
        `gRecaptchaResponse` -- the token to submit as `g-recaptcha-response`.
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
        websiteURL: Full URL of the page where the captcha is located.
        websiteKey: Site key for the v3 widget.
        minScore: Minimum acceptable token score to return, e.g. `0.3`, `0.7`, `0.9`.
        pageAction: The `action` parameter passed to `grecaptcha.execute()` on the page.
        isEnterprise: `True` if this is reCAPTCHA v3 Enterprise.
        apiDomain: Non-standard domain the widget's script is served from, if any.

    Returns (`solution` from `solve()`):
        `gRecaptchaResponse` -- the token to submit as `g-recaptcha-response`.
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
        websiteURL: Full URL of the page where the widget is located.
        websiteKey: Value of the widget's `data-sitekey` attribute.
        action: Value of the widget's `data-action` attribute, if set.
        data: Custom payload from the widget's `data-cdata` attribute, if set.
        pagedata: Value of the `chlPageData` parameter, needed for some Cloudflare
            challenge pages beyond the basic widget. Named lowercase (not `pageData`)
            to match the API field name exactly -- Cloudflare-specific fields are
            the one place this API doesn't camelCase.
        userAgent: User-Agent to solve with. The returned token is tied to it --
            submit it with the same User-Agent.

    Returns (`solution` from `solve()`):
        `token` -- the value to submit as `cf-turnstile-response`.
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
        websiteURL: Full URL of the page where the widget is located.
        websiteKey: Value of the widget's `data-sitekey` attribute.
        proxyType: `"http"`, `"socks4"`, or `"socks5"`.
        proxyAddress: Proxy IP address or hostname.
        proxyPort: Proxy port.
        proxyLogin: Proxy auth username, if required.
        proxyPassword: Proxy auth password, if required.
        action: Value of the widget's `data-action` attribute, if set.
        data: Custom payload from the widget's `data-cdata` attribute, if set.
        pagedata: Value of the `chlPageData` parameter, needed for some Cloudflare
            challenge pages beyond the basic widget. Named lowercase (not `pageData`)
            to match the API field name exactly.
        userAgent: User-Agent to solve with. The returned token is tied to it.

    Returns (`solution` from `solve()`):
        `token` -- the value to submit as `cf-turnstile-response`.
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
        body: The captcha image, base64-encoded (no `data:image/...;base64,` prefix).
        phrase: `True` if the answer is multiple words.
        case: `True` if the answer is case-sensitive.
        numeric: Character set hint -- `0` unspecified, `1` digits only, `2` letters
            only, `3` any with digits, `4` any with letters.
        math: `True` if the image contains a math expression to evaluate rather
            than text to transcribe.
        minLength: Minimum expected answer length.
        maxLength: Maximum expected answer length.
        comment: Free-text hint for the worker (e.g. what kind of answer is expected).
        imgInstructions: Optional supplementary instruction image, base64-encoded.

    Returns (`solution` from `solve()`):
        `text` -- the recognized text/answer.
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


class GeeTestTaskProxyless(BaseTask):
    """GeeTest v3 or v4 without proxy. Set `version=4` for v4 (and provide
    `initParameters["captcha_id"]`); v3 is the default and needs `gt`/`challenge`
    instead.

    Args:
        websiteURL: Full URL of the page where the widget is located.
        version: `3` (default) or `4`.
        gt: Public key of the GeeTest widget. Required for v3.
        challenge: Session-specific challenge value from the page. Required for
            v3, and must be freshly fetched for every request -- it cannot be reused.
        initParameters: Extra parameters from the page's `initGeetest` call. For
            v4, must contain `captcha_id`.
        geetestApiServerSubdomain: Custom GeeTest API subdomain, if the site uses one.
        userAgent: User-Agent to solve with.
        risk_type: Value of the `risk_type` parameter from the captcha-loading
            request, if present. Dynamic, single-use, and time-limited.

    Returns (`solution` from `solve()`):
        v3: `challenge`, `validate`, `seccode`.
        v4: `captcha_id`, `lot_number`, `pass_token`, `gen_time`, `captcha_output`.
    """

    type = "GeeTestTaskProxyless"

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
        websiteURL: Full URL of the page where the widget is located.
        proxyType: `"http"`, `"socks4"`, or `"socks5"`.
        proxyAddress: Proxy IP address or hostname.
        proxyPort: Proxy port.
        proxyLogin: Proxy auth username, if required.
        proxyPassword: Proxy auth password, if required.
        version: `3` (default) or `4`.
        gt: Public key of the GeeTest widget. Required for v3.
        challenge: Session-specific challenge value from the page, must be fresh.
            Required for v3.
        initParameters: Extra parameters from the page's `initGeetest` call. For
            v4, must contain `captcha_id`.
        geetestApiServerSubdomain: Custom GeeTest API subdomain, if the site uses one.
        userAgent: User-Agent to solve with.
        risk_type: Value of the `risk_type` parameter from the captcha-loading
            request, if present. Dynamic, single-use, and time-limited.

    Returns (`solution` from `solve()`):
        v3: `challenge`, `validate`, `seccode`.
        v4: `captcha_id`, `lot_number`, `pass_token`, `gen_time`, `captcha_output`.
    """

    type = "GeeTestTask"

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
    """Yandex SmartCaptcha (token challenge) without proxy. For the image
    challenge instead, use `CoordinatesTask` with `imgType="smart_captcha"`.

    Args:
        websiteURL: Full URL of the page where the widget is located.
        websiteKey: The `sitekey` value from the page source or captcha iframe.
        userAgent: User-Agent to solve with.
        cookies: Session cookies to use while solving, if the page requires them.

    Returns (`solution` from `solve()`):
        `token` -- the value to submit as the SmartCaptcha response token.
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
        websiteURL: Full URL of the page where the widget is located.
        websiteKey: The `sitekey` value from the page source or captcha iframe.
        proxyType: `"http"`, `"socks4"`, or `"socks5"`.
        proxyAddress: Proxy IP address or hostname.
        proxyPort: Proxy port.
        proxyLogin: Proxy auth username, if required.
        proxyPassword: Proxy auth password, if required.
        userAgent: User-Agent to solve with.
        cookies: Session cookies to use while solving, if the page requires them.

    Returns (`solution` from `solve()`):
        `token` -- the value to submit as the SmartCaptcha response token.
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
    """Coordinate-based (click) image captcha. Used both for generic
    "click on X" captchas and for Yandex SmartCaptcha's image challenge (set
    `imgType` accordingly). No proxy variant -- the image is submitted directly.

    Args:
        body: The captcha image, base64-encoded (no `data:image/...;base64,` prefix).
        comment: Hint for the worker, e.g. `"click on the green apple"`. Recommended
            for generic click captchas.
        imgInstructions: Optional instruction image, base64-encoded, showing what
            to click and in what order. Required when `imgType="smart_captcha"`.
        minClicks: Minimum number of clicks expected (default `1`).
        maxClicks: Maximum number of clicks allowed.
        imgType: Set to `"smart_captcha"` to solve a Yandex SmartCaptcha image
            challenge instead of a generic click captcha.

    Returns (`solution` from `solve()`):
        `coordinates` -- a list of `{"x": int, "y": int}` pixel positions to click,
        in order.
    """

    type = "CoordinatesTask"

    def __init__(
        self,
        body: str,
        comment: Optional[str] = None,
        imgInstructions: Optional[str] = None,
        minClicks: Optional[int] = None,
        maxClicks: Optional[int] = None,
        imgType: Optional[str] = None,
    ) -> None:
        self.body = body
        self.comment = comment
        self.imgInstructions = imgInstructions
        self.minClicks = minClicks
        self.maxClicks = maxClicks
        self.imgType = imgType


class TencentTaskProxyless(BaseTask):
    """Tencent captcha without proxy.

    Args:
        websiteURL: Full URL of the page where the captcha is located.
        appId: Value of the `appId` parameter found in the page source.
        captchaScript: URL of the Tencent captcha script, if the page uses a
            non-default one.

    Returns (`solution` from `solve()`):
        `appid`, `ret`, `ticket`, `randstr` -- pass these to the page's Tencent
        captcha callback.
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
        websiteURL: Full URL of the page where the captcha is located.
        appId: Value of the `appId` parameter found in the page source.
        proxyType: `"http"`, `"socks4"`, or `"socks5"`.
        proxyAddress: Proxy IP address or hostname.
        proxyPort: Proxy port.
        proxyLogin: Proxy auth username, if required.
        proxyPassword: Proxy auth password, if required.
        captchaScript: URL of the Tencent captcha script, if the page uses a
            non-default one.

    Returns (`solution` from `solve()`):
        `appid`, `ret`, `ticket`, `randstr` -- pass these to the page's Tencent
        captcha callback.
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
