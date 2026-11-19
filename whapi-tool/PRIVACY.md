# Privacy Policy — Whapi.Cloud Tool Plugin for Dify

## Summary

This plugin is a client for the [Whapi.Cloud](https://whapi.cloud/) WhatsApp API. It runs inside your Dify plugin runtime. **We do not operate a separate backend** for this plugin and **do not persist** WhatsApp or Dify user data in plugin-owned storage beyond what Whapi.Cloud already processes for your channel.

## Personal data

Using this plugin can involve **personal data**, including phone numbers, WhatsApp chat IDs, message text, contact details, and media references you send through tools. Data is processed to run your Dify workflows and to call Whapi on your behalf. You are responsible for having a lawful basis to process this data in your jurisdiction and use case.

## Data sent to Whapi.Cloud (`https://gate.whapi.cloud`)

When you configure credentials and use tools, the plugin may send:

| Data | Purpose |
|------|---------|
| **Channel access token** (Bearer) | Authenticate API calls on your behalf |
| **Phone numbers and chat IDs** | Message delivery and contact checks |
| **Message text and media references** | Send text/media messages via the API |
| **API paths and JSON bodies** | Tool operations, including **Custom API Request** (`api_request`) for the method, path, and JSON you configure; mutating methods can change or delete data in your channel per [Whapi API](https://whapi.cloud/docs) semantics |

Responses from Whapi (message IDs, statuses, contact check results, etc.) are returned to your Dify workflow or agent.

## API host

All plugin outbound API traffic uses **only** the official Whapi gateway **`https://gate.whapi.cloud`** (hardcoded allowlist; declared under `network.domains` in `manifest.yaml`). You cannot point the plugin at another host.

## Data we do not collect

- The plugin does not write customer content to its own database or long-term storage.
- The plugin does not send credentials or API payloads to hosts other than `gate.whapi.cloud`.

## Credentials

Your Whapi channel token is stored using **Dify’s credential store** (encrypted at rest per your Dify deployment). The plugin reads credentials only at invocation time.

## Third party — Whapi.Cloud

WhatsApp delivery and channel operations are performed by **Whapi.Cloud** under your account.

- Privacy policy: https://whapi.cloud/privacy  
- Data Processing Agreement (PDF): https://whapi.cloud/Data-Processing-Agreement.pdf  
- API documentation: https://whapi.cloud/docs  

This plugin forwards the data you supply in Dify to Whapi according to your tool configuration. Whapi’s processing is governed by Whapi’s policies and your agreement with Whapi.

## Contact

- GitHub Issues: https://github.com/Whapi-Cloud/dify-whapi/issues  
- Email: care@whapi.cloud  

Source (this plugin): https://github.com/Whapi-Cloud/dify-whapi/tree/main/whapi-tool  