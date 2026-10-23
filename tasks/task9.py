
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Take user text as input
user_text = input("Enter user content to moderate: ")

response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.1,
    max_tokens=300,
    messages=[
        {
            "role": "system",
            "content": """
            You are a professional content moderation assistant.

            Review user content and assign exactly one category:
            Safe, Needs Review, or Violates Policy.

            Moderation examples:

            Example 1:
            Text: "I enjoyed this movie. It was excellent!"
            Category: Safe
            Reason: This is a harmless personal opinion.

            Example 2:
            Text: "You are useless. I am going to report your comment."
            Category: Safe
            Reason: This is criticism without a credible threat.

            Example 3:
            Text: "I will find your home address and publish it."
            Category: Violates Policy
            Reason: This expresses an intention to expose private
            personal information.

            Example 4:
            Text: "Can someone explain how to make this dangerous substance?"
            Category: Needs Review
            Reason: The request is ambiguous and may involve harmful
            activity that requires further assessment.

            Instructions:
            1. Examine the text and identify relevant safety concerns.
            2. Decide the category based on the content.
            3. Give a short, clear reason for the decision.
            4. Do not reveal private internal reasoning.
            5. Do not flag harmless criticism or disagreement unfairly.
            6. Treat context and intent carefully.

            Output format:
            Category: [Safe / Needs Review / Violates Policy]
            Reason: [Brief explanation]
            """
        },
        {
            "role": "user",
            "content": f"""
            Moderate the following user content:

            {user_text}

            Return the category and a brief reason.
            """
        },
    ]
)

print("\n--- CONTENT MODERATION RESULT ---\n")
print(response.choices[0].message.content.strip())
