# Whapi.Cloud — Dify Tool Plugin

Official-style WhatsApp **outbound** integration for [Dify](https://dify.ai) via [Whapi.Cloud](https://whapi.cloud/).  
Feature parity with the [n8n Whapi node](https://github.com/Whapi-Cloud/n8n-nodes-whapi) for send/get/check and optional raw API calls.

Monorepo: [`Whapi-Cloud/dify-whapi`](https://github.com/Whapi-Cloud/dify-whapi) (this directory is `whapi-tool/`).

## Requirements

- Dify workspace with plugin support
- Whapi channel paired in [Whapi Panel](https://panel.whapi.cloud/)
- Channel **access token**

## Install

### From package (`.difypkg`)

1. Build or download `whapi-0.0.1.difypkg` (see repo root packaging instructions).
2. Dify → **Plugins** → **Install plugin** → upload the file.

### Remote debug (development)

1. [Dify Plugin CLI](https://docs.dify.ai/en/develop-plugin/getting-started/cli)
2. Copy `.env.example` → `.env`, set `REMOTE_INSTALL_URL` and `REMOTE_INSTALL_KEY` from Dify → Plugins → Debug.
3. `pip install -r requirements.txt` then `python -m main`.

## Credentials

| Field | Description |
|-------|-------------|
| **Access Token** | Channel token from Whapi Panel |
| **API base URL** | Default `https://gate.whapi.cloud` |

Validation uses `GET /limits` (same idea as n8n).

## Tools

| Tool | Description |
|------|-------------|
| **Send Message** | Text, image, video, audio, document, contact |
| **Get Message** | Fetch by message ID |
| **Check Contact** | WhatsApp registration check for a phone number |
| **Custom API Request** | Authenticated call to any path on `gate.whapi.cloud` |

## Privacy

See [PRIVACY.md](./PRIVACY.md).

## Source and support

- Repository: https://github.com/Whapi-Cloud/dify-whapi  
- Issues: https://github.com/Whapi-Cloud/dify-whapi/issues  
- Whapi API: https://whapi.cloud/docs  

For **inbound** webhooks, install the companion **Whapi Trigger** plugin (`whapi-trigger/` in the same repo; Dify ≥ 1.10.0).
