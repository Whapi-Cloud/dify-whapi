from __future__ import annotations

from typing import Any


def _text_body(message: dict[str, Any]) -> str:
    text = message.get("text")
    if isinstance(text, dict):
        return str(text.get("body") or "")
    if isinstance(message.get("body"), str):
        return message["body"]
    return ""


def flatten_message(message: dict[str, Any]) -> dict[str, Any]:
    return {
        "message_id": str(message.get("id") or ""),
        "chat_id": str(message.get("chat_id") or ""),
        "status": str(message.get("status") or ""),
        "from_me": bool(message.get("from_me")),
        "from": str(message.get("from") or ""),
        "timestamp": message.get("timestamp"),
        "message_type": str(message.get("type") or ""),
        "text_body": _text_body(message),
        "source": str(message.get("source") or ""),
    }


def normalize_send_response(data: dict[str, Any]) -> dict[str, Any]:
    message = data.get("message")
    if not isinstance(message, dict):
        return data
    out = flatten_message(message)
    if data.get("sent") is not None:
        out["sent"] = data.get("sent")
    return out


def normalize_get_response(data: dict[str, Any]) -> dict[str, Any]:
    message = data.get("message")
    if isinstance(message, dict):
        return flatten_message(message)
    if data.get("id") and data.get("chat_id"):
        return flatten_message(data)
    return data
