from __future__ import annotations

import json
import time
from collections.abc import Mapping
from typing import Any

from werkzeug import Request, Response

from dify_plugin.entities.provider_config import CredentialType
from dify_plugin.entities.trigger import EventDispatch, Subscription, UnsubscribeResult
from dify_plugin.errors.trigger import (
    SubscriptionError,
    TriggerDispatchError,
    TriggerProviderCredentialValidationError,
    UnsubscribeError,
)
from dify_plugin.interfaces.trigger import Trigger, TriggerSubscriptionConstructor

from whapi_lib.client import DEFAULT_BASE_URL, WhapiClient, WhapiError

_SUBSCRIPTION_TTL_SECONDS = 30 * 24 * 60 * 60
_EVENT_TO_NAME = {
    "messages": "whapi_messages",
    "groups": "whapi_groups",
}


def _client_from_credentials(credentials: Mapping[str, Any]) -> WhapiClient:
    token = credentials.get("access_token")
    if not token:
        raise TriggerProviderCredentialValidationError("Access token is required")
    base = str(credentials.get("api_base_url") or DEFAULT_BASE_URL)
    return WhapiClient(str(token), base)


class WhapiTrigger(Trigger):
    def _dispatch_event(self, subscription: Subscription, request: Request) -> EventDispatch:
        payload = self._parse_payload(request)
        response = Response(
            response=json.dumps({"status": "ok"}),
            status=200,
            mimetype="application/json",
        )
        events = self._resolve_events(payload, subscription)
        return EventDispatch(events=events, response=response, payload=payload)

    @staticmethod
    def _parse_payload(request: Request) -> Mapping[str, Any]:
        try:
            data = request.get_json(force=True, silent=True)
        except Exception as exc:
            raise TriggerDispatchError(f"Failed to parse JSON body: {exc}") from exc
        if not data or not isinstance(data, dict):
            raise TriggerDispatchError("Empty or invalid JSON body")
        return data

    @staticmethod
    def _resolve_events(payload: Mapping[str, Any], subscription: Subscription) -> list[str]:
        subscribed = subscription.properties.get("event_families") or []
        event_block = payload.get("event") or {}
        family = event_block.get("type")
        if not family or family not in subscribed:
            return []
        name = _EVENT_TO_NAME.get(str(family))
        return [name] if name else []


class WhapiTriggerSubscriptionConstructor(TriggerSubscriptionConstructor):
    def _validate_api_key(self, credentials: dict[str, Any]) -> None:
        try:
            _client_from_credentials(credentials).validate_credentials()
        except WhapiError as exc:
            raise TriggerProviderCredentialValidationError(str(exc)) from exc

    def _create_subscription(
        self,
        endpoint: str,
        parameters: Mapping[str, Any],
        credentials: Mapping[str, Any],
        credential_type: CredentialType,
    ) -> Subscription:
        families = list(parameters.get("event_families") or [])
        if not families:
            raise SubscriptionError("Select at least one event family (messages or groups).")

        client = _client_from_credentials(credentials)
        try:
            client.upsert_webhook(endpoint, [str(f) for f in families])
        except WhapiError as exc:
            raise SubscriptionError(str(exc)) from exc

        return Subscription(
            expires_at=int(time.time()) + _SUBSCRIPTION_TTL_SECONDS,
            endpoint=endpoint,
            parameters=dict(parameters),
            properties={
                "event_families": [str(f) for f in families],
            },
        )

    def _delete_subscription(
        self,
        subscription: Subscription,
        credentials: Mapping[str, Any],
        credential_type: CredentialType,
    ) -> UnsubscribeResult:
        client = _client_from_credentials(credentials)
        try:
            client.remove_webhook(subscription.endpoint)
        except WhapiError as exc:
            raise UnsubscribeError(str(exc)) from exc
        return UnsubscribeResult(success=True, message="Whapi webhook removed.")

    def _refresh_subscription(
        self,
        subscription: Subscription,
        credentials: Mapping[str, Any],
        credential_type: CredentialType,
    ) -> Subscription:
        families = subscription.properties.get("event_families") or subscription.parameters.get(
            "event_families", []
        )
        client = _client_from_credentials(credentials)
        try:
            client.upsert_webhook(subscription.endpoint, [str(f) for f in families])
        except WhapiError as exc:
            raise SubscriptionError(str(exc)) from exc
        return Subscription(
            expires_at=int(time.time()) + _SUBSCRIPTION_TTL_SECONDS,
            endpoint=subscription.endpoint,
            parameters=subscription.parameters,
            properties=subscription.properties,
        )
