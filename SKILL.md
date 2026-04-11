# AI Skills — Ivycandy Hair Hub

This document explains how the AI features work and how to get the best results from them.

---

## AI Reply Assistant

**Page:** AI Reply Assistant (also available as a quick widget on the Dashboard)

**What it does:** Takes a raw customer message and returns a polished, ready-to-send WhatsApp reply — written in the Ivycandy brand voice.

### How to use

1. Paste the customer's exact message into the input box
2. Optionally add context (e.g. customer name, what they bought before)
3. Click **Generate Reply**
4. Copy the output directly into WhatsApp or DMs — no editing needed

### Tips for better replies

| Situation | What to put in "Extra context" |
|---|---|
| Returning customer | `Returning customer, bought 22" straight bundles in March` |
| Known name | `Customer name: Chioma` |
| VIP / big spender | `Loyal customer, spent €400+ this year` |
| Specific stock issue | `26" body wave is out of stock, 24" available` |
| Negotiating customer | `She's been asking for a discount` |

### What the AI is trained to do

- Acknowledge the customer's specific question first
- Highlight quality and trust (5 years in business, real human hair)
- Create gentle urgency where appropriate (limited stock, popular item)
- End every reply with a clear next step (confirm order, send payment details)
- Keep messages short and scannable — not essays

---

## Sales Scripts

**Page:** Sales Scripts

**What it does:** Generates full conversation scripts for three common sales situations with one click.

### Available scripts

| Script | When to use |
|---|---|
| **Cold Lead** | Someone just followed you on Instagram but hasn't messaged. Use as an opening DM. |
| **Returning Customer** | A loyal customer hasn't bought in 6+ months. Use to re-engage. |
| **Pricing Inquiry** | A customer asks "how much is your hair?" — guides them to share what they want before you quote. |

### How to use

1. Go to **Sales Scripts** in the sidebar
2. Click the button for the script type you need
3. Read it through and personalise any placeholder details before sending
4. Copy and paste into WhatsApp, Instagram DMs, or TikTok messages

---

## AI Model

Both features use **Claude Sonnet 4.6** (`claude-sonnet-4-6`) via the Anthropic API.

- Max tokens per reply: 600 (Reply Assistant) / 500 (Sales Scripts)
- No conversation history is stored — each generation is independent
- The system prompt (brand voice, sales principles, output format) is defined in `ai_reply.py`

---

## Customising the AI Behaviour

All AI behaviour is controlled by the `SYSTEM_PROMPT` constant in `ai_reply.py`.

To change the brand voice, sales style, or output format:

```python
# ai_reply.py
SYSTEM_PROMPT = """
You are the AI assistant for ...
"""
```

Common customisations:
- **Different currency or region** — add to the system prompt: `Prices are in GBP. Shipping is UK-wide.`
- **Specific product range** — add: `We sell only lace front wigs and closures. We do not sell bundles.`
- **Different tone** — change: `Warm and professional` → `Bold and direct`
- **Language** — add: `Always reply in Nigerian Pidgin English.`
