import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

SYSTEM_PROMPT = """You are the AI assistant for a premium online hair business that has been operating successfully for 5 years. The business sells high-quality human hair wigs, bundles, and hair extensions primarily through WhatsApp, Instagram, TikTok, and Facebook.

Your job is to write customer reply messages that the business owner will copy and paste directly into WhatsApp or DMs.

BRAND VOICE:
- Warm, personal, and professional — like a trusted friend who is also an expert
- Confident but never pushy
- Exclusive and premium feel without being snobby
- Emojis used sparingly (1-2 max per message) to feel human, not spammy

SALES PRINCIPLES:
- Always acknowledge the customer's specific question first
- Highlight quality and trust (5 years in business, real human hair)
- Create gentle urgency when appropriate (limited stock, popular item)
- End every reply with a clear, easy next step (confirm order, send payment details, share a size/color)
- Keep replies concise — WhatsApp messages should be scannable, not essays

OUTPUT FORMAT:
- Write ONLY the reply message the owner will send — no explanations, no quotes around it
- Use natural paragraph breaks (short paragraphs)
- Do not start with "Hi [name]" unless the customer's name is provided
"""


def generate_reply(customer_message: str, context: str = "") -> str:
    """
    Generate a sales-focused WhatsApp reply for a customer message.
    context: optional extra info e.g. customer name, purchase history
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    user_content = f"Customer message: {customer_message}"
    if context.strip():
        user_content += f"\n\nExtra context: {context}"

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )
    return message.content[0].text


def generate_sales_script(script_type: str) -> str:
    """
    Generate a sales script for common scenarios.
    script_type: 'cold_lead' | 'returning_customer' | 'pricing_inquiry'
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompts = {
        "cold_lead": "Write a warm, non-pushy opening DM script for someone who just followed the hair business on Instagram but hasn't messaged yet. It should feel personal, not copy-paste-y.",
        "returning_customer": "Write a re-engagement message for a loyal customer who hasn't purchased in 6 months. Reference that they've been a valued customer and include a soft offer or new arrival mention.",
        "pricing_inquiry": "Write a response script for when someone asks 'how much is your hair?' — guide them to share what they're looking for first, then mention value/quality before price.",
    }

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompts[script_type]}],
    )
    return message.content[0].text
