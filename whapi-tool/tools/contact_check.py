from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from whapi_lib.runtime import client_from_runtime


class ContactCheckTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        client = client_from_runtime(self.runtime)
        result = client.request(
            "POST",
            "/contacts",
            json_body={
                "blocking": "wait",
                "contacts": [tool_parameters["contact"]],
            },
        )
        yield self.create_json_message(result if isinstance(result, dict) else {"result": result})
