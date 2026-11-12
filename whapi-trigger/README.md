# Whapi.Cloud — Dify Trigger Plugin

WhatsApp **inbound** webhooks for Dify **Integration Trigger** workflows via [Whapi.Cloud](https://whapi.cloud/).

Requires **Dify 1.10.0 or newer**.  
Companion to the **Whapi Tool** plugin in [`whapi-tool/`](../whapi-tool/).

Repository: https://github.com/Whapi-Cloud/dify-whapi

## Requirements

- Dify ≥ 1.10.0 with trigger subscriptions
- Whapi channel token
- Workflow with a **Whapi Trigger** start node

## Install

Upload `whapi_trigger-0.0.1.difypkg` via Dify → Plugins, or use remote debug (same as tool plugin; see `.env.example`).

## Subscription

1. Create a trigger subscription on provider **Whapi Trigger**.
2. Enter **Access Token** and select event families:
   - **Messages events**
   - **Groups events**
3. On save, the plugin registers Dify’s callback URL on your channel (`PATCH /settings`, merged webhooks — same semantics as [n8n Whapi Trigger](https://github.com/Whapi-Cloud/n8n-nodes-whapi)).

## Events

| Event | Output (high level) |
|-------|---------------------|
| **Whapi Messages** | `channel_id`, `event_type`, `event_action`, `messages[]` |
| **Whapi Groups** | `channel_id`, `event_type`, `event_action`, `groups[]` |

Use `messages[0].chat_id` and `messages[0].text.body` for typical auto-reply flows.

## Privacy

See [PRIVACY.md](./PRIVACY.md).

## Support

https://github.com/Whapi-Cloud/dify-whapi/issues
