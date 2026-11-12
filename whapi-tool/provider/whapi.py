from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from whapi_lib.client import DEFAULT_BASE_URL, WhapiClient, WhapiError


class WhapiProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        token = credentials.get("access_token")
        if not token:
            raise ToolProviderCredentialValidationError("Access token is required")
        try:
            WhapiClient(
                str(token),
                str(credentials.get("api_base_url") or DEFAULT_BASE_URL),
            ).validate_credentials()
        except WhapiError as exc:
            raise ToolProviderCredentialValidationError(str(exc)) from exc
        except Exception as exc:
            raise ToolProviderCredentialValidationError(str(exc)) from exc
