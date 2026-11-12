from __future__ import annotations

from typing import Any

from dify_plugin.entities.tool import ToolRuntime

from whapi_lib.client import DEFAULT_BASE_URL, WhapiClient


def client_from_runtime(runtime: ToolRuntime) -> WhapiClient:
    credentials: dict[str, Any] = runtime.credentials or {}
    token = credentials.get("access_token")
    if not token:
        raise ValueError("Missing access_token in credentials")
    base_url = credentials.get("api_base_url") or DEFAULT_BASE_URL
    return WhapiClient(str(token), str(base_url))
