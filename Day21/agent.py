import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()
client=Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
def run_agent(role,content):
    res=client.chat.complete(
        model="mistral-small-latest",
        temperature=0.4,
        messages=[{
            "role":"system",
            "content":role,
        },
        {
            "role":"user",
            "content":content
        }
        ]
        )
    return res.choices[0].message.content

topic=input("Enter Your Topic : ")
print("Agest strat work....")
result=run_agent("""
You are a professional email writing AI agent.
Create, correct, and improve professional emails.
Use clear, polite, and formal language.
""",f"write E-mail on {topic}"
)
print(result)