# Privacy Policy — Whapi Trigger Plugin for Dify

## Summary

This plugin connects **Whapi.Cloud** webhooks to **Dify** workflow trigger subscriptions. It may **register or remove a webhook URL** on your Whapi channel via the channel settings API. The plugin does not operate a separate datastore.

## Data sent to Whapi.Cloud (`https://gate.whapi.cloud`)

| Data | Purpose |
|------|---------|
| **Channel access token** (Bearer) | Read/update channel `webhooks` settings |
| **Dify callback URL** | Receive message and group events when a subscription is created |

## Data received from Whapi.Cloud

Incoming HTTPS webhook payloads (messages, groups, metadata such as `channel_id`, `event`, timestamps) are parsed and passed into your Dify workflow as trigger variables. Exact fields depend on the [Whapi webhook format](https://whapi.cloud/docs).

## Webhook registration behavior

When you create a subscription, the plugin **merges** your Dify callback URL into the channel webhook list (same approach as the official [n8n Whapi integration](https://github.com/Whapi-Cloud/n8n-nodes-whapi)). Removing the subscription removes **only** that callback URL.

## Data we do not collect

- No long-term storage of webhook bodies by this plugin code.
- No outbound calls to domains other than `gate.whapi.cloud` as declared in `manifest.yaml`.

## Credentials

Tokens are stored in **Dify’s credential store** for trigger subscriptions.

## Contact

https://github.com/Whapi-Cloud/dify-whapi/issues  

Source (`whapi-trigger/`): https://github.com/Whapi-Cloud/dify-whapi
