import os
from groq import Groq
from mistralai.client import Mistral
from dotenv import load_dotenv



load_dotenv()
mistral_client=Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
groq_client=Groq(api_key=os.getenv("GROQ_API_KEY"))


question=input("BOT : ")

response=mistral_client.chat.complete(
    model="mistral-small-latest",
    temperature=0.5,
    messages=[
        {
        "role":"user",
        "content":question
    }]
    )
mistral_ans1=response.choices[0].message.content
print(f"MISTRAL OUTPUT : {mistral_ans1}")
def evaluate(que,ans):
    evl_prompt=f"""
    You are an expert Evaluator AI Agent responsible for analyzing outputs, checking accuracy, quality, relevance, and completeness.  
    Evaluate the given response, identify mistakes or missing information, assign a score out of 10, and provide clear improvement suggestions,also rate question : {que} and Answer : {ans}
    after evaluate return response with evaluate score and short summary 
    """
    groq_ans=groq_client.chat.completions.create(
        model="opnai/gpt-oss-20b",
        messages=[{
            "role":"user",
            "content":evl_prompt
        }]
    )
    return groq_ans.choices[0].message.content

evaluate_ans=evaluate(question,mistral_ans1)

print(f"EVLUATE : {evaluate_ans}")
    