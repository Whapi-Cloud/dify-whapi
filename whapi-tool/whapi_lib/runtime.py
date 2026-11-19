from __future__ import annotations

from typing import Any

from dify_plugin.entities.tool import ToolRuntime

from whapi_lib.client import WhapiClient


def client_from_runtime(runtime: ToolRuntime) -> WhapiClient:
    credentials: dict[str, Any] = runtime.credentials or {}
    token = credentials.get("access_token")
    if not token:
        raise ValueError("Missing access_token in credentials")
    return WhapiClient(str(token))