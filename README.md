# Dify × Whapi.Cloud

Monorepo with two Dify plugins (parity with [n8n-nodes-whapi](https://github.com/Whapi-Cloud/n8n-nodes-whapi)):

| Package | Purpose |
|---------|---------|
| [`whapi-tool/`](whapi-tool/) | Outgoing API: send message, get message, check contact, **custom API request** |
| [`whapi-trigger/`](whapi-trigger/) | Incoming webhooks: **messages** and **groups** event families (auto `PATCH /settings`) |

Requires **Python 3.12** (Dify runner), `dify-plugin` SDK ≥ 0.6.0. Trigger plugin needs **Dify ≥ 1.10.0**.

## Quick start

1. Install [Dify Plugin CLI](https://docs.dify.ai/en/develop-plugin/getting-started/cli) (`dify` on `PATH`).
2. For each plugin folder:

```bash
cd whapi-tool   # or whapi-trigger
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# fill REMOTE_INSTALL_URL and REMOTE_INSTALL_KEY from Dify → Plugins → Debug
python -m main
```

3. In Dify, configure **Whapi** tool credentials (channel token from [Whapi Panel](https://panel.whapi.cloud/)).
4. For triggers, create a subscription with **Messages** / **Groups** — the plugin registers the Dify callback URL on your channel (same merge semantics as n8n).

## Shared code

[`shared/whapi_client.py`](shared/whapi_client.py) is the source of truth; each plugin ships a copy under `whapi_lib/client.py` for packaging.

## Package

```bash
dify plugin package ./whapi-tool
dify plugin package ./whapi-trigger
```
