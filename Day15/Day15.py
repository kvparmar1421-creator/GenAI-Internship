
import os
import hashlib
import streamlit as st
import chromadb

from io import BytesIO
from dotenv import load_dotenv
from pypdf import PdfReader
from mistralai.client import Mistral

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# make persistant database in chroma db
db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_or_create_collection("hr_policies")

st.title("Company Knowledge Assistant")

# for you can upload multiple pdf file
files = st.file_uploader(
    "Upload HR Policy PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if files and st.button("Process Documents"):

    for file in files:

        reader = PdfReader(BytesIO(file.getvalue()))
        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

        # all content devide into small chunks
        chunks = [
            text[i:i + 1000]
            for i in range(0, len(text), 800)
        ]

        
        file_hash = hashlib.sha256(
            file.getvalue()
        ).hexdigest()

        ids = [f"{file_hash}_{i}" for i in range(len(chunks))]

        metadata = [
            {"source": file.name, "chunk": i}
            for i in range(len(chunks))
        ]

        # Storing all chunks in ChromaDB
        collection.upsert(
            documents=chunks,
            ids=ids,
            metadatas=metadata
        )

    st.success("All PDFs processed successfully!")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
         st.markdown(msg["content"])

question = st.chat_input("Ask an HR policy question")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.write(question)

    if collection.count() == 0:
        answer = "I don't know. Please upload policy documents."

    else:
        result = collection.query(
            query_texts=[question],
            n_results=min(3, collection.count()),
            include=["documents", "metadatas", "distances"]
        )

        docs = result["documents"][0]
        sources = result["metadatas"][0]
        distances = result["distances"][0]

        
        context = "\n\n".join(
            f"Source: {sources[i]['source']}\n{docs[i]}"
            for i in range(len(docs))
        )


        prompt = f"""
        Answer the question using ONLY the context.

        If the answer is not in the context, say:
        I don't know. 

        Context:
        {context}

        Question: {question}
        """

    
        response = client.chat.complete(
            model="mistral-small-latest",
            temperature=0.1,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.markdown(answer)

        
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
