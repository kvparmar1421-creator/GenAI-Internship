
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Take input from the user
text = input("Enter message to translate: ")
language = input("Enter target language: ")
formality = input("Enter formality (formal / casual): ")

# Template: text + target language + formality
prompt_template = """
Translate the following message into {language}.

Original message:
{text}

Formality: {formality}

Instructions:
- Keep the original meaning.
- Use correct grammar and natural wording.
- If formality is formal, use polite and professional language.
- If formality is casual, use friendly and conversational language.
- Do not add extra information.
- Return only the translated message.
"""

response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.2,
    max_tokens=400,
    messages=[
        {
            "role": "system",
            "content": """
            You are a professional translator working for a global company.
            Translate messages accurately into the requested language.
            Follow the requested formality level.
            Preserve the original meaning, names, numbers, and important
            details. Do not add explanations or unrelated information.
            """
        },
        {
            "role": "user",
            "content": prompt_template.format(
                text=text,
                language=language,
                formality=formality
            )
        },
    ]
)

print("\n--- TRANSLATED MESSAGE ---\n")
print(response.choices[0].message.content.strip())
