import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

complaint = input("Enter customer complaint: ")
tone = input("Enter tone (polite / formal / friendly / auto): ")

response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.3,
    max_tokens=350,
    messages=[
        {
            "role": "system",
            "content": "You are a customer support agent for an online shopping company. First, decide how serious the complaint is: Low, Medium, or High. Then write a reply in the requested tone using only the details given in the complaint. If the tone is auto, check whether the customer sounds angry or calm and choose the best tone yourself."

        },
        {
            "role": "user",
            "content": f"Complaint: {complaint} Tone: {tone} First classify severity, then write reply."
        },
    ]
)

print(response.choices[0].message.content.strip())