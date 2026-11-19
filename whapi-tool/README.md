# Whapi.Cloud — Dify Tool Plugin

WhatsApp **outbound** tool plugin for [Dify](https://dify.ai) via [Whapi.Cloud](https://whapi.cloud/) — send/get/check plus **Custom API Request** for the rest of the [Whapi API](https://whapi.cloud/docs).

**Source:** https://github.com/Whapi-Cloud/dify-whapi (monorepo folder `whapi-tool/`).  
Dual-plugin overview (trigger + tool): https://github.com/Whapi-Cloud/dify-whapi#readme

## Requirements

- Dify workspace with **Plugins** enabled (minimum Dify **1.0.0** per this plugin’s `manifest.yaml`)
- [Whapi.Cloud](https://whapi.cloud/) account
- WhatsApp channel paired in [Whapi Panel](https://panel.whapi.cloud/) — scan the QR code the same way you link **WhatsApp Web**
- Channel **access token** from the panel

## Install

### From package (`.difypkg`)

1. Build the package (`dify plugin package ./whapi-tool` from the [repository](https://github.com/Whapi-Cloud/dify-whapi)) or use a release artifact.
2. Dify → **Plugins** → **Install plugin** → upload the `.difypkg` file.
3. The file name follows `author`, `name`, and `version` in `manifest.yaml` (currently `whapi-cloud` / `whapi` / `0.0.1`).

### Remote debug (development)

1. Install the [Dify Plugin CLI](https://docs.dify.ai/en/develop-plugin/getting-started/cli).
2. Copy `.env.example` → `.env`; set `REMOTE_INSTALL_URL` and `REMOTE_INSTALL_KEY` from Dify → **Plugins** → **Debug**.
3. `pip install -r requirements.txt`, then `python -m main`.
4. Attach the plugin from the Dify debug UI.

## Credentials

In Dify → **Plugins** → **Whapi** provider:

| Field | Description |
|-------|-------------|
| **Access Token** | Channel token from [Whapi Panel](https://panel.whapi.cloud/) |
| **Channel ID** | Optional metadata field |

All API traffic uses the official gateway **`https://gate.whapi.cloud` only** (not configurable in the plugin). Tools and **Custom API Request** use relative paths from the [API docs](https://whapi.cloud/docs). Credential validation uses `GET /limits`.

## Tools

| Tool | Description |
|------|-------------|
| **Send Message** | Text, image, video, audio, document, contact — see [Whapi messaging docs](https://whapi.cloud/docs) for IDs and media parameters |
| **Get Message** | Fetch by message ID |
| **Check Contact** | Check whether a phone number is registered on WhatsApp |
| **Custom API Request** | Call any endpoint from [whapi.cloud/docs](https://whapi.cloud/docs); see [safety notes](#custom-api-request-safety) below |

Dedicated tools cover the actions most workflows use daily. We do not add a separate Dify tool for every Whapi endpoint. **Custom API Request** is the supported way to call any other documented API on `https://gate.whapi.cloud`.

### Custom API Request (safety)

- **HTTP method** and **API path** are **workflow fields** (`form` in Dify) — you configure them in the tool node. The LLM must **not** pick the method or path on its own (reduces accidental destructive calls from agents).
- **Query JSON** and **Body JSON** can still be filled from workflow variables or the model when your design requires dynamic payloads — only enable that where you trust the prompt and data flow.
- **GET** — read-only against your channel (limits, messages, settings, etc.).
- **POST / PUT / PATCH** — can **create or change** messages, chats, groups, channel **settings** (including webhooks), and other objects described in the Whapi docs.
- **DELETE** — can **remove** messages and other resources where the API allows deletion.
- Channel **webhook registration** for Dify is handled by the [**Whapi Trigger** plugin](https://github.com/Whapi-Cloud/dify-whapi/tree/main/whapi-trigger); avoid ad-hoc `PATCH /settings` in Custom API unless you know how it interacts with existing webhooks.
- Use a dedicated tool (Send Message, etc.) when one exists. Reserve Custom API for endpoints not covered by built-in tools.
- **Send Message** and other built-in tools also perform write operations; limit which Whapi tools are exposed to each agent or workflow.

## Using tools in Dify

1. Install and authorize the plugin (credentials above).
2. In an **Agent** or **Workflow**, add a tool node and select **Whapi** tools, or let an agent call them via tool configuration.
3. For replies to inbound WhatsApp traffic, install the companion [**Whapi Trigger**](https://github.com/Whapi-Cloud/dify-whapi/tree/main/whapi-trigger) plugin (Dify **≥ 1.10.0**) and connect a workflow end-to-end.

## Privacy

See [PRIVACY.md](./PRIVACY.md). Whapi.Cloud policies:

- https://whapi.cloud/privacy  
- https://whapi.cloud/Data-Processing-Agreement.pdf  

## Support

- GitHub Issues: https://github.com/Whapi-Cloud/dify-whapi/issues  
- Email: care@whapi.cloud  
- Whapi API: https://whapi.cloud/docs  

## License

[MIT](./LICENSE)