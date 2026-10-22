import os
import json
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key = os.getenv("MISTRAL_API_KEY"))

response = client.chat.complete(
    model = "mistral-small-latest",
    temperature = 0.4,
    response_format = {"type":"json_object"},
    messages=[
        {
           "role": "system",
            "content": """
            Analyze the customer's feedback about a banking service.
            Return a JSON object containing:
            sentiment (positive, negative, or neutral),
            rating_score (out of 10),
            summarize (string).
            Return only valid JSON.
            """
        },
        {
            "role": "user",
            "content": "The mobile banking app is easy to use, but money transfers sometimes fail and customer support responds slowly."
        },
    ]
)

# print(response.choices[0].message.content)
raw = response.choices[0].message.content
print(raw)
try:
    data = json.loads(raw)
    print(data["sentiment"])
    print(data["rating_score"])
    print(data["summarize"])
except json.JSONDecodeError:
    print("Error while parse to json..")