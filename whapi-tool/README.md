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
| **API base URL** | **`https://gate.whapi.cloud`** — default and recommended for every standard Whapi.Cloud channel. Leave unchanged unless Whapi support directs otherwise. |
| **Channel ID** | Optional metadata field |

All tools and **Custom API Request** call this host (path + method from the [API docs](https://whapi.cloud/docs)). Credential validation uses `GET /limits`.

## Tools

| Tool | Description |
|------|-------------|
| **Send Message** | Text, image, video, audio, document, contact — see [Whapi messaging docs](https://whapi.cloud/docs) for IDs and media parameters |
| **Get Message** | Fetch by message ID |
| **Check Contact** | Check whether a phone number is registered on WhatsApp |
| **Custom API Request** | Call any endpoint from [whapi.cloud/docs](https://whapi.cloud/docs) (HTTP method, path, JSON body) |

Dedicated tools cover the actions most workflows use daily. We do not add a separate Dify tool for every Whapi endpoint. **Custom API Request** is the supported way to call any documented API: use your credentials, set method/path/body per the reference, and the plugin sends the request to `https://gate.whapi.cloud`.

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