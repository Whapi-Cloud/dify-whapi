# Privacy Policy — Whapi Trigger Plugin for Dify

## Summary

This plugin connects **Whapi.Cloud** webhooks to **Dify** workflow trigger subscriptions. It may **register or remove a webhook URL** on your Whapi channel via the channel settings API. The plugin does not operate a separate datastore.

## Personal data

Webhook payloads can include **personal data**: phone numbers, chat and group IDs, participant identifiers, message text, timestamps, and related WhatsApp metadata. The plugin parses payloads and passes them into your Dify workflow as trigger variables. You are responsible for lawful processing in your environment and for how your workflow stores or forwards that data.

## Data sent to Whapi.Cloud (`https://gate.whapi.cloud`)

| Data | Purpose |
|------|---------|
| **Channel access token** (Bearer) | Read/update channel `webhooks` settings |
| **Dify callback URL** | Deliver message and group events to your workflow when a subscription is created |

## Data received from Whapi.Cloud

Incoming HTTPS webhook payloads (messages, groups, metadata such as `channel_id`, `event`, timestamps) are parsed and passed into your Dify workflow as trigger variables. Exact fields depend on the [Whapi webhook format](https://whapi.cloud/docs).

## Webhook registration behavior

When you create a subscription, the plugin **merges** your Dify callback URL into the channel webhook list. Removing the subscription removes **only** that callback URL.

## API host

Webhook registration uses the channel **API base URL** credential. Default and recommended: **`https://gate.whapi.cloud`**. Change only if Whapi support directs you to another gateway.

## Data we do not collect

- No long-term storage of webhook bodies by this plugin code.
- With the default API base URL, outbound API calls use only `gate.whapi.cloud` (declared in `manifest.yaml` under `network.domains`).

## Credentials

Tokens are stored in **Dify’s credential store** for trigger subscriptions.

## Third party — Whapi.Cloud

Whapi sends webhook events from your connected WhatsApp channel.

- Privacy policy: https://whapi.cloud/privacy  
- Data Processing Agreement (PDF): https://whapi.cloud/Data-Processing-Agreement.pdf  
- API and webhook documentation: https://whapi.cloud/docs  

## Contact

- GitHub Issues: https://github.com/Whapi-Cloud/dify-whapi/issues  
- Email: care@whapi.cloud  

Source (this plugin): https://github.com/Whapi-Cloud/dify-whapi/tree/main/whapi-trigger  