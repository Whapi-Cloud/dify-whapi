from collections.abc import Mapping
from typing import Any

from werkzeug import Request

from dify_plugin.entities.trigger import Variables
from dify_plugin.errors.trigger import EventIgnoreError
from dify_plugin.interfaces.trigger import Event


class WhapiMessagesEvent(Event):
    def _on_event(
        self, request: Request, parameters: Mapping[str, Any], payload: Mapping[str, Any]
    ) -> Variables:
        event_block = payload.get("event") or {}
        if event_block.get("type") != "messages":
            raise EventIgnoreError()

        messages = payload.get("messages") or []
        if not isinstance(messages, list):
            messages = []

        return Variables(
            variables={
                "channel_id": str(payload.get("channel_id") or ""),
                "event_type": str(event_block.get("type") or ""),
                "event_action": str(event_block.get("event") or ""),
                "messages": messages,
            }
        )
