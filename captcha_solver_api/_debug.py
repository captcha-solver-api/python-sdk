"""Internal, best-effort debug logging helpers."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

_MASKED_KEYS = {
    "authorization",
    "clientkey",
    "cookie",
    "cookies",
    "password",
    "proxyaddress",
    "proxylogin",
    "proxypassword",
}
_BASE64_KEYS = {"body", "image", "imginstructions"}
_handler: Optional[logging.Handler] = None


def _sanitize(value: Any, key: str = "") -> Any:
    """Return a sanitized copy suitable for diagnostic output."""
    normalized_key = key.lower()
    if normalized_key in _MASKED_KEYS:
        return "[MASKED]"
    if normalized_key in _BASE64_KEYS and isinstance(value, str):
        return f"[base64, {len(value)} chars]"
    if isinstance(value, dict):
        return {item_key: _sanitize(item, str(item_key)) for item_key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_sanitize(item) for item in value]
    if isinstance(value, str) and len(value) > 200:
        return f"{value[:40]}...[{len(value)} chars]...{value[-40:]}"
    return value


def _json(value: Any) -> str:
    return json.dumps(_sanitize(value), indent=2, ensure_ascii=False, default=repr)


def _timestamp() -> str:
    now = datetime.now().astimezone()
    offset = now.strftime("%z")
    offset = f"{offset[:3]}:{offset[3:]}"
    return now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + f" {offset}"


def _error_details(error: BaseException) -> str:
    details: List[str] = []
    current: Optional[BaseException] = error
    seen = set()
    while current is not None and len(details) < 4 and id(current) not in seen:
        seen.add(id(current))
        text = str(current).replace("\n", " ").strip()
        description = f"{type(current).__name__}: {text}" if text else type(current).__name__
        if not (details and text and str(error) == text):
            details.append(description)
        current = current.__cause__ or current.__context__
    return " <- ".join(details)


class DebugLogger:
    """Emit complete logical events while never affecting SDK behavior."""

    def __init__(self, enabled: bool, name: str) -> None:
        self.enabled = enabled
        self.name = name
        self.logger = logging.getLogger(f"captcha_solver_api.{name}")
        if enabled:
            self._ensure_default_handler()

    def _ensure_default_handler(self) -> None:
        global _handler
        if _handler is None:
            _handler = logging.StreamHandler()
            _handler.setFormatter(logging.Formatter("%(message)s"))
        if _handler not in self.logger.handlers:
            self.logger.addHandler(_handler)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

    def emit(self, message: str) -> None:
        if not self.enabled:
            return
        try:
            self.logger.debug(f"[{_timestamp()}] [{self.name}] {message}")
        except Exception:
            return

    def initialized(self, version: str, base_url: str, timeout: Any, polling: Any) -> None:
        self.emit(
            f"client initialized sdk=python-sdk/{version} baseUrl={base_url} "
            f"httpTimeout=30s timeout={timeout}s pollingInterval={polling}s"
        )

    def request_success(
        self,
        endpoint: str,
        url: str,
        payload: Dict[str, Any],
        data: Dict[str, Any],
        status: int,
        reason: str,
        elapsed_ms: int,
    ) -> None:
        try:
            summary = _summary(endpoint, payload, data)
            if endpoint == "getTaskResult" and data.get("status") == "processing":
                self.emit(f"{summary} ({elapsed_ms}ms)")
                return
            self.emit(
                f"{summary} ({elapsed_ms}ms)\n"
                f"REQUEST (POST {url}):\n{_json(payload)}\n"
                f"RESPONSE (HTTP {status} {reason}, {elapsed_ms}ms):\n{_json(data)}"
            )
        except Exception:
            return

    def request_failure(
        self,
        endpoint: str,
        url: str,
        payload: Dict[str, Any],
        error: BaseException,
        elapsed_ms: int,
        status: Optional[int] = None,
        reason: str = "",
        data: Optional[Any] = None,
        invalid_json: bool = False,
        body_missing: bool = False,
    ) -> None:
        try:
            context = _request_context(endpoint, payload)
            label = f"{endpoint} {context}".rstrip()
            detail = _error_details(error)
            if status is None:
                response = (
                    "RESPONSE: none - no response from the server "
                    f"({type(error).__name__}, {elapsed_ms}ms)"
                )
            elif body_missing:
                response = (
                    f"RESPONSE (HTTP {status} {reason}, {elapsed_ms}ms): "
                    f"body was not received ({type(error).__name__})"
                )
            elif invalid_json:
                response = (
                    f"RESPONSE (HTTP {status} {reason}, {elapsed_ms}ms): body is not valid JSON"
                )
            else:
                response = f"RESPONSE (HTTP {status} {reason}, {elapsed_ms}ms):\n{_json(data)}"
            self.emit(
                f"{label} -> failed: {detail} ({elapsed_ms}ms)\n"
                f"REQUEST (POST {url}):\n{_json(payload)}\n{response}"
            )
        except Exception:
            return

    def solve_summary(
        self,
        solved: bool,
        task_id: Optional[int],
        task_type: Optional[str],
        elapsed: float,
        polls: int,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[BaseException] = None,
    ) -> None:
        try:
            server_time: Optional[str] = None
            if result is not None:
                created = result.get("createTime")
                ended = result.get("endTime")
                if isinstance(created, (int, float)) and isinstance(ended, (int, float)):
                    server_time = f"{ended - created:g}s"
            lines = [
                "SOLVE SUMMARY:",
                f"  status:          {'solved' if solved else 'not solved'}",
                f"  taskId:          {task_id if task_id is not None else '- (task was not created)'}",
            ]
            if task_type:
                lines.append(f"  taskType:        {task_type}")
            lines.append(f"  elapsed:         {elapsed:.3f}s")
            if server_time is not None:
                lines.append(f"  serverSolveTime: {server_time}")
            lines.append(f"  polls:           {polls}")
            if error is not None:
                lines.append(f"  error:           {_error_details(error)}")
            self.emit("\n".join(lines))
        except Exception:
            return


def _request_context(endpoint: str, payload: Dict[str, Any]) -> str:
    if endpoint == "createTask":
        task = payload.get("task")
        return str(task.get("type", "unknown")) if isinstance(task, dict) else "unknown"
    if endpoint == "getTaskResult":
        return f"taskId={payload.get('taskId', 'unknown')}"
    return ""


def _summary(endpoint: str, payload: Dict[str, Any], data: Dict[str, Any]) -> str:
    context = _request_context(endpoint, payload)
    prefix = f"{endpoint} {context}".rstrip()
    if data.get("errorId", 0) != 0:
        code = data.get("errorCode", "UNKNOWN_ERROR")
        message = data.get("errorDescription", "Unknown API error.")
        return f"{prefix} -> failed: ApiError {code}: {message}"
    if endpoint == "createTask":
        return f"{prefix} -> taskId={data.get('taskId')}"
    if endpoint == "getTaskResult":
        return f"{prefix} -> {data.get('status', 'unknown')}"
    if endpoint == "getBalance":
        return f"{prefix} -> balance={data.get('balance')}"
    return f"{prefix} -> success"
