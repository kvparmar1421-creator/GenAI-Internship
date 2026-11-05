import os,json
from mistralai.client import Mistral
from dotenv import load_dotenv
load_dotenv()

client=Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def run_agent(role,content):

    response = client.chat.complete(
        model="mistral-small-latest",
        temperature=0.3,
        messages=[{
            "role":"system",
            "content":role
        },
        {
            "role":"user",
            "content":content
        }]
    )
    return response.choices[0].message.content
subject=input("Enter the subject of the email : ")
email=input("Enter the email message : ")

# agent 1
print("Agent 1 is start work....")
analysis=run_agent( "You are a Professional Email Analyzer. "
    "Understand the email and identify its main purpose, "
    "important information and sender's intention. "
    "Do not invent missing information.",

    f"Subject: {subject}\nEmail: {email}"


)
print("agent 1,Analysis completed")

#Email classifier
print("Agent 2,Classification start...")
classification=run_agent(
    "You are a Professional Email Classification Agent. "
    "Classify the email into one category: "
    "Work, Personal, Urgent, Billing, General or Spam. "
    "Also identify priority as High, Medium or Low. "
    "Explain your classification briefly.",

    f"Subject: {subject}\n"
    f"Email: {email}\n"
    f"Analysis: {analysis}"
)
print("agent 2,classifiaction  completed")

#Agent 3 Reply generator
print("Reply GEneration Start...")
reply=run_agent(
    "You are a Professional Email Reply Writer. "
    "Generate a polite, professional and meaningful reply "
    "based on the original email. "
    "Do not invent facts or make unverified promises. "
    "If the email is spam, do not generate a reply; "
    "recommend not responding.",

    f"Subject: {subject}\n"
    f"Email: {email}\n"
    f"Classification: {classification}")
print("Agent 3 Reply Generation Completed")
#last output
print("\nEMAIL SUBJECT:")
print(subject)

print("\nEMAIL ANALYSIS:")
print(analysis)

print("\nEMAIL CLASSIFICATION:")
print(classification)

print("\nSUGGESTED EMAIL REPLY:")
print(reply)
