import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

topic = input("Enter Story Topic: ")
genre = input("Enter Story Genre (Horror, Comedy, Adventure): ")
tone = input("Enter Story Tone: ")
length = input("Enter Story Length (Short, Medium, Long): ")

response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.7,
    max_tokens=1000,
    messages=[
        {
            "role": "system",
            "content": (
                "You are a creative AI Story Writer. "
                "Generate an original story based on the user's inputs. "
                "Follow the given topic, genre, tone, and length. "
                "Use simple and understandable language."
            )
        },
        {
            "role": "user",
            "content": (
                f"Write a story about {topic}. "
                f"Use the {genre} genre. "
                f"The tone should be {tone}. "
                f"The story length should be {length}."
            )
        }
    ]
)

print("\n===== Generated Story =====\n")
print(response.choices[0].message)