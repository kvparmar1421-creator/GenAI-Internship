
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

email = input("Enter incoming email: ")

response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.2,
    max_tokens=400,
    messages=[
        {
            "role": "system",
            "content": """
            You are a professional e-commerce email support assistant.

            First classify the incoming email into one category:
            Urgent, Billing, General, or Spam.

            Examples:

            Email: "My account has been hacked. Help me immediately!"
            Category: Urgent

            Email: "I have not received my refund yet."
            Category: Billing

            Email: "Can I change my delivery address?"
            Category: General

            Email: "You won a free gift! Click this unknown link now!"
            Category: Spam

            Instructions:
            1. Classify the email first, then write a reply.
            2. For Urgent emails, show concern and suggest prompt assistance.
            3. For Billing emails, politely address the payment or refund issue.
            4. For General emails, provide a helpful answer.
            5. For Spam emails, label them as spam and do not engage.
            6. Use only the information provided in the email.
            7. Do not invent facts or promise unconfirmed actions.
            8. Do not reveal internal reasoning.

            Output format:
            Category: [Urgent / Billing / General / Spam]
            Reply: [Your appropriate response]
            """
        },
        {
            "role": "user",
            "content": f"""
            Incoming email:
            {email}

            First classify the email, then write an appropriate reply.
            """
        },
    ]
)

print("\n--- Email Support Result ---\n")
print(response.choices[0].message.content.strip())
