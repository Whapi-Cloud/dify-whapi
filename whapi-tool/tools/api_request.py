from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from whapi_lib.client import parse_json_object
from whapi_lib.runtime import client_from_runtime


class ApiRequestTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        client = client_from_runtime(self.runtime)
        method = str(tool_parameters.get("method") or "GET").upper()
        path = str(tool_parameters.get("path") or "").strip()
        if not path.startswith("/"):
            raise ValueError("path must start with /")
        if "://" in path:
            raise ValueError("path must be relative to the Whapi API host")

        query = parse_json_object(tool_parameters.get("query_json"), "query_json")
        body = parse_json_object(tool_parameters.get("body_json"), "body_json")

        result = client.request(
            method,
            path,
            json_body=body if body else None,
            params=query if query else None,
        )
        yield self.create_json_message(result if isinstance(result, dict) else {"result": result})
