import os
from mistralai.client import Mistral
from dotenv import load_dotenv
import chromadb
from pypdf import PdfReader
load_dotenv()

#For read pdf file
reader = PdfReader("GenAi.pdf")
text=""
for page in reader.pages:
    text+=page.extract_text()
#chunk
def chunks_text(text,chunk_size=1000,overlap=200):
    start=0
    chunks=[]
    while start<len(text):
        chunks.append(text[start:start+chunk_size])
        start+=chunk_size-overlap
    return chunks
chunks=chunks_text(text)
#Embedding and store in chomadb 
client=chromadb.Client()
collection_name=client.create_collection("chatwithpdf")

collection_name.add(
    documents=chunks,
    ids=[str(i) for i in range(len(chunks))],
)

#Take input from user and search collection
user_input=input("Enter Your Question:")

relevant=collection_name.query(
    query_texts=[user_input],
    n_results=4
)
#print(relevant)
#print(relevant['documents'])
context=relevant['documents'][0]
#combine User input and relevant documents to create prompt

prompt = f"""
Give Answer using user input based on following context only:
{context}
only Give answer from context if not found in context then say "I don't know"
question: {user_input}
"""
client=Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
response=client.chat.complete(
    model="mistral-small-latest",
    temperature=0.7,
    messages=[
        {

            "role":"user",
            "content":prompt
        },
    ]
)
print(response.choices[0].message.content)