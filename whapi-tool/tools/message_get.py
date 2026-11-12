from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from whapi_lib.runtime import client_from_runtime
from whapi_lib.tool_output import normalize_get_response


class MessageGetTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        client = client_from_runtime(self.runtime)
        message_id = tool_parameters["message_id"]
        result = client.request("GET", f"/messages/{message_id}")
        if not isinstance(result, dict):
            yield self.create_json_message({"result": result})
            return
        yield self.create_json_message(normalize_get_response(result))
