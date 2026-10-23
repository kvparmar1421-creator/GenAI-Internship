import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


product = input("Enter product name: ")
features = input("Enter product features: ")
tone = input("Enter tone (professional / friendly / attractive / auto): ")


response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.3,
    max_tokens=350,
    messages=[
        {
                    "role": "system",
            "content": """
            You are a professional e-commerce product description writer.
            Write clear, attractive, and easy-to-understand product descriptions.
            Use only the product details provided by the user.
            Do not invent features or make false claims.
            If the tone is auto, choose the most suitable tone yourself.
            Include a short introduction, key features, and a closing sentence."""
        },
        {
            "role": "user",
            "content": f"""
            Product name: {product}
            Product features: {features}
            Tone: {tone}

            Write an engaging product description suitable for an
            e-commerce website.
            """
        },
    ]
)

print(response.choices[0].message.content.strip())