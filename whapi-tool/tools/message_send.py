from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from whapi_lib.runtime import client_from_runtime
from whapi_lib.tool_output import normalize_send_response


class MessageSendTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        client = client_from_runtime(self.runtime)
        message_type = tool_parameters.get("message_type") or "text"
        path = client.message_type_to_path(str(message_type))

        payload: dict[str, Any] = {"to": tool_parameters["to"]}
        body = tool_parameters.get("body")
        if body:
            payload["body"] = body
        media = tool_parameters.get("media")
        if media:
            payload["media"] = media
        typing_time = tool_parameters.get("typing_time")
        if typing_time is not None and typing_time != "":
            payload["typing_time"] = typing_time
        caption = tool_parameters.get("caption")
        if caption:
            payload["caption"] = caption

        result = client.request("POST", f"/{path}", json_body=payload)
        if not isinstance(result, dict):
            yield self.create_json_message({"result": result})
            return
        yield self.create_json_message(normalize_send_response(result))
