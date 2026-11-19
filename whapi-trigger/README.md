# Whapi.Cloud — Dify Trigger Plugin

WhatsApp **inbound** webhooks for Dify **Integration Trigger** workflows via [Whapi.Cloud](https://whapi.cloud/).

Requires **Dify 1.10.0 or newer** (trigger subscriptions).  
Works with the [**Whapi Tool**](https://github.com/Whapi-Cloud/dify-whapi/tree/main/whapi-tool) plugin for outbound replies.

**Source:** https://github.com/Whapi-Cloud/dify-whapi (monorepo folder `whapi-trigger/`).  
Dual-plugin overview: https://github.com/Whapi-Cloud/dify-whapi#readme

## Requirements

- Dify **≥ 1.10.0** with **Integration Trigger** / trigger subscriptions
- [Whapi.Cloud](https://whapi.cloud/) account and a paired channel in [Whapi Panel](https://panel.whapi.cloud/) (QR pairing, same idea as **WhatsApp Web**)
- Channel **access token**
- A Dify **Workflow** app you can publish (production URL for the trigger callback)

## Install

### From package (`.difypkg`)

1. Build the package (`dify plugin package ./whapi-trigger` from the [repository](https://github.com/Whapi-Cloud/dify-whapi)) or use a release artifact.
2. Dify → **Plugins** → **Install plugin** → upload the `.difypkg` file.
3. File name follows `manifest.yaml` (`whapi-cloud` / `whapi_trigger` / version).

### Remote debug (development)

1. [Dify Plugin CLI](https://docs.dify.ai/en/develop-plugin/getting-started/cli).
2. Copy `.env.example` → `.env`; set `REMOTE_INSTALL_URL` and `REMOTE_INSTALL_KEY` from Dify → **Plugins** → **Debug**.
3. `pip install -r requirements.txt`, then `python -m main`.

## Credentials (subscription)

When you create a trigger **subscription** for provider **Whapi Trigger**:

| Field | Description |
|-------|-------------|
| **Access Token** | Channel token from [Whapi Panel](https://panel.whapi.cloud/) |
| **API base URL** | **`https://gate.whapi.cloud`** — default and recommended; used when registering webhooks on your channel. Leave unchanged unless Whapi support directs otherwise. |

## Workflow setup (typical auto-reply)

1. Create a **Workflow** application in Dify.
2. Add an **Integration Trigger** start node and choose **Whapi Trigger** → event (**Whapi Messages** and/or **Whapi Groups**).
3. **Publish** the workflow so Dify has a production callback URL (use the test URL only for debugging).
4. In Dify → trigger **Subscriptions**, create a subscription for **Whapi Trigger**:
   - Enter **Access Token** (and base URL if needed).
   - Under **Trigger on**, select **Messages events** and/or **Groups events**.
5. On save, the plugin calls Whapi `PATCH /settings` and **merges** Dify’s callback URL into your channel webhooks.
6. Add workflow steps (LLM, logic, etc.). To send a WhatsApp reply, use the [**Whapi Tool**](https://github.com/Whapi-Cloud/dify-whapi/tree/main/whapi-tool) plugin in a later node.

## Events

| Event | Output (high level) |
|-------|---------------------|
| **Whapi Messages** | `channel_id`, `event_type`, `event_action`, `messages[]` |
| **Whapi Groups** | `channel_id`, `event_type`, `event_action`, `groups[]` |

Field shapes follow the [Whapi webhook format](https://whapi.cloud/docs). For a simple text auto-reply, common paths include `messages[0].chat_id` and, when the payload is a text message, `messages[0].text.body`. Media and other message types use different fields — inspect the webhook payload or docs.

## Uninstall / subscription removal

Deleting the subscription removes **only** this plugin’s callback URL from the channel webhook list, not your other Whapi webhooks.

## Privacy

See [PRIVACY.md](./PRIVACY.md). Whapi.Cloud policies:

- https://whapi.cloud/privacy  
- https://whapi.cloud/Data-Processing-Agreement.pdf  

## Support

- GitHub Issues: https://github.com/Whapi-Cloud/dify-whapi/issues  
- Email: care@whapi.cloud  
- Outbound sends: [Whapi Tool plugin](https://github.com/Whapi-Cloud/dify-whapi/tree/main/whapi-tool)

## License

[MIT](./LICENSE)