# Privacy Policy — Whapi.Cloud Tool Plugin for Dify

## Summary

This plugin is a client for the [Whapi.Cloud](https://whapi.cloud/) WhatsApp API. It runs inside your Dify plugin runtime. **We do not operate a separate backend** for this plugin and **do not persist** WhatsApp or Dify user data on Whapi-owned servers beyond what Whapi.Cloud already processes for your channel.

## Data sent to Whapi.Cloud (`https://gate.whapi.cloud`)

When you configure credentials and use tools, the plugin may send:

| Data | Purpose |
|------|---------|
| **Channel access token** (Bearer) | Authenticate API calls on your behalf |
| **Phone numbers and chat IDs** | Message delivery and contact checks |
| **Message text and media references** | Send text/media messages via the API |
| **Arbitrary API paths and JSON bodies** | Only when you use the **Custom API Request** tool (`api_request`) |

Responses from Whapi (message IDs, statuses, contact check results, etc.) are returned to your Dify workflow or agent.

## Data we do not collect

- The plugin does not write customer content to its own database or long-term storage.
- The plugin does not send data to hosts other than those declared in `manifest.yaml` (`gate.whapi.cloud`).

## Credentials

Your Whapi channel token is stored using **Dify’s credential store** (encrypted at rest per your Dify deployment). The plugin reads credentials only at invocation time.

## Third party

WhatsApp message delivery and channel operations are handled by **Whapi.Cloud** under your account. See Whapi’s documentation and terms for how they process channel data.

## Contact

Issues and privacy questions for this integration:  
https://github.com/Whapi-Cloud/dify-whapi/issues

Source code (this plugin lives in `whapi-tool/`):  
https://github.com/Whapi-Cloud/dify-whapi
