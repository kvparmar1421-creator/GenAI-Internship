
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Take code snippet from the user
code = input("Paste your code snippet: ")

response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.1,
    max_tokens=800,
    messages=[
        {
            "role": "system",
            "content": """
            You are a senior software engineer who helps junior developers
            understand legacy code.

            Your tasks:
            1. Explain what the code does in plain English.
            2. Explain each important part step by step.
            3. Describe the purpose of important variables, functions,
               loops, conditions, and other statements.
            4. Generate an improved version of the code with useful
               comments and docstrings, while preserving its behavior.

            Follow this output format:

            1. Overall Explanation:
               Explain the main purpose of the code.

            2. Step-by-Step Explanation:
               Explain each important part in simple language.

            3. Key Components:
               Explain important variables and functions.

            4. Code with Comments:
               Provide the original code with helpful comments
               and suitable docstrings.

            5. Summary:
               Summarize what a junior developer should understand.

            Rules:
            - Use simple, beginner-friendly English.
            - Explain the code in a clear, logical sequence.
            - Do not invent functionality that is not present.
            - Preserve the original code's behavior when adding comments.
            - Point out potential issues only when relevant.
            - Do not reveal private internal reasoning.
            """
        },
        {
            "role": "user",
            "content": f"""
            Please explain the following code and generate a commented
            version with docstrings where appropriate.

            Code snippet:
            {code}
            """
        },
    ]
)

print("\n--- LEGACY CODE EXPLANATION ---\n")
print(response.choices[0].message.content.strip())
