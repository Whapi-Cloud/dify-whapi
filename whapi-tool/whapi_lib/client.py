"""Shared Whapi.Cloud HTTP client (copied into each plugin package for packaging)."""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlparse

import requests

DEFAULT_BASE_URL = "https://gate.whapi.cloud"

# Official Whapi API gateway hosts only (Bearer token must not be sent elsewhere).
ALLOWED_API_HOSTS: frozenset[str] = frozenset({"gate.whapi.cloud"})

EVENT_METHODS = ("post", "put", "delete", "patch")


class WhapiError(Exception):
    def __init__(self, message: str, status_code: int | None = None, body: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


def resolve_base_url(base_url: str | None = None) -> str:
    """Return a normalized HTTPS base URL; only ALLOWED_API_HOSTS are permitted."""
    if base_url is None or not str(base_url).strip():
        return DEFAULT_BASE_URL

    raw = str(base_url).strip().rstrip("/")
    if not raw.startswith(("http://", "https://")):
        raw = f"https://{raw}"

    parsed = urlparse(raw)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("API base URL must use http or https")

    host = (parsed.hostname or "").lower()
    if host not in ALLOWED_API_HOSTS:
        allowed = ", ".join(sorted(ALLOWED_API_HOSTS))
        raise ValueError(f"API base URL host must be one of: {allowed}")

    if parsed.path not in ("", "/"):
        raise ValueError("API base URL must not include a path")
    if parsed.query or parsed.fragment:
        raise ValueError("API base URL must not include query or fragment")
    if parsed.username or parsed.password:
        raise ValueError("API base URL must not include user credentials")

    if parsed.scheme != "https":
        raise ValueError("API base URL must use https")

    port = parsed.port
    if port not in (None, 443):
        raise ValueError("API base URL must use the default HTTPS port")

    return f"https://{host}"


class WhapiClient:
    def __init__(self, access_token: str, base_url: str | None = None):
        self.base_url = resolve_base_url(base_url)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        timeout: int = 30,
    ) -> Any:
        if not path.startswith("/"):
            path = f"/{path}"
        if "://" in path:
            raise WhapiError("API path must be relative to the Whapi gateway host", status_code=None)
        url = f"{self.base_url}{path}"
        response = self.session.request(
            method=method.upper(),
            url=url,
            json=json_body if json_body else None,
            params=params,
            timeout=timeout,
        )
        if response.status_code >= 400:
            body: Any
            try:
                body = response.json()
            except ValueError:
                body = response.text
            raise WhapiError(
                f"Whapi API error {response.status_code}: {body}",
                status_code=response.status_code,
                body=body,
            )
        if not response.content:
            return {}
        try:
            return response.json()
        except ValueError:
            return {"text": response.text}

    def get_settings(self) -> dict[str, Any]:
        data = self.request("GET", "/settings")
        return data if isinstance(data, dict) else {}

    def patch_settings(self, settings: dict[str, Any]) -> dict[str, Any]:
        data = self.request("PATCH", "/settings", json_body=settings)
        return data if isinstance(data, dict) else {}

    @staticmethod
    def message_type_to_path(message_type: str) -> str:
        segment = message_type.replace("-", "/")
        return f"messages/{segment}"

    @staticmethod
    def build_webhook_events(event_families: list[str]) -> list[dict[str, str]]:
        events: list[dict[str, str]] = []
        for family in event_families:
            for method in EVENT_METHODS:
                events.append({"type": family, "method": method})
        return events

    def upsert_webhook(self, callback_url: str, event_families: list[str]) -> None:
        settings = self.get_settings()
        webhooks = list(settings.get("webhooks") or [])
        webhooks = [w for w in webhooks if w.get("url") != callback_url]
        webhooks.append(
            {
                "url": callback_url,
                "mode": "body",
                "events": self.build_webhook_events(event_families),
            }
        )
        settings["webhooks"] = webhooks
        self.patch_settings(settings)

    def remove_webhook(self, callback_url: str) -> None:
        settings = self.get_settings()
        webhooks = [w for w in (settings.get("webhooks") or []) if w.get("url") != callback_url]
        settings["webhooks"] = webhooks
        self.patch_settings(settings)

    def validate_credentials(self) -> None:
        self.request("GET", "/limits")


def parse_json_object(value: str | None, field_name: str) -> dict[str, Any]:
    if not value or not str(value).strip():
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{field_name} must be valid JSON") from exc
    if not isinstance(parsed, dict):
        raise ValueError(f"{field_name} must be a JSON object")
    return parsed