"""Shared Whapi.Cloud HTTP client (copied into each plugin package for packaging)."""

from __future__ import annotations

import json
from typing import Any

import requests

DEFAULT_BASE_URL = "https://gate.whapi.cloud"
EVENT_METHODS = ("post", "put", "delete", "patch")


class WhapiError(Exception):
    def __init__(self, message: str, status_code: int | None = None, body: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class WhapiClient:
    def __init__(self, access_token: str, base_url: str = DEFAULT_BASE_URL):
        self.base_url = base_url.rstrip("/")
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
