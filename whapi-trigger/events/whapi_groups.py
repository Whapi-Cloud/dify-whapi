from collections.abc import Mapping
from typing import Any

from werkzeug import Request

from dify_plugin.entities.trigger import Variables
from dify_plugin.errors.trigger import EventIgnoreError
from dify_plugin.interfaces.trigger import Event


class WhapiGroupsEvent(Event):
    def _on_event(
        self, request: Request, parameters: Mapping[str, Any], payload: Mapping[str, Any]
    ) -> Variables:
        event_block = payload.get("event") or {}
        if event_block.get("type") != "groups":
            raise EventIgnoreError()

        groups = payload.get("groups") or payload.get("group") or []
        if not isinstance(groups, list):
            groups = [groups] if groups else []

        return Variables(
            variables={
                "channel_id": str(payload.get("channel_id") or ""),
                "event_type": str(event_block.get("type") or ""),
                "event_action": str(event_block.get("event") or ""),
                "groups": groups,
            }
        )
