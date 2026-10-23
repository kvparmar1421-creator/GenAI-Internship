
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Take meeting transcript from the user
transcript = input("Paste meeting transcript: ")

response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.1,
    max_tokens=600,
    messages=[
        {
            "role": "system",
            "content": """
            You are a professional meeting assistant.
            Your task is to extract clear action items from meeting notes.

            First, review the transcript and identify tasks, owners,
            and deadlines. Then organize the tasks into a clean list.
            Do not show internal reasoning.

            Follow this output format:

            Action Items:
            1. Who: [Person's name]
               What: [Task to complete]
               Deadline: [Date or Not specified]

            Few-shot examples:

            Meeting note:
            "Rahul will prepare the report by Friday."

            Output:
            Action Items:
            1. Who: Rahul
               What: Prepare the report
               Deadline: Friday

            Meeting note:
            "Priya will contact the client. Amit needs to update
            the website by Monday."

            Output:
            Action Items:
            1. Who: Priya
               What: Contact the client
               Deadline: Not specified

            2. Who: Amit
               What: Update the website
               Deadline: Monday

            Rules:
            - Extract only tasks mentioned in the transcript.
            - Do not invent names, tasks, or deadlines.
            - If the owner is unknown, write "Not assigned".
            - If the deadline is unknown, write "Not specified".
            - Keep each task short and clear.
            - If no action items exist, say "No action items found".
            """
        },
        {
            "role": "user",
            "content": f"""
            Meeting transcript:
            {transcript}

            Identify and list all action items with who, what,
            and deadline.
            """
        },
    ]
)

print("\n--- MEETING ACTION ITEMS ---\n")
print(response.choices[0].message.content.strip())
