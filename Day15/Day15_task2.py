
import os
import streamlit as st
import chromadb

from dotenv import load_dotenv
from pypdf import PdfReader
from mistralai.client import Mistral

load_dotenv()

client = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY")
)

MODEL = "mistral-small-latest"

st.set_page_config(
    page_title="SaaS Support Bot"
)

st.title("SaaS Product Support Bot")
st.write("Ask questions about your product documentation.")

if "messages" not in st.session_state:
    st.session_state.messages = []


if "feedback" not in st.session_state:
    st.session_state.feedback = None

# Upload your pdf
pdf = st.file_uploader(
    "Upload Product Manual",
    type=["pdf"]
)

if pdf:

    
    reader = PdfReader(pdf)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""


    chunk_size = 700
    overlap = 100

    chunks = []

    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]

        if chunk.strip():
            chunks.append(chunk)

    
    db = chromadb.Client()

    collection = db.get_or_create_collection(
        name="product_docs"
    )


    collection.upsert(
        ids=[str(i) for i in range(len(chunks))],
        documents=chunks
    )

    st.success("Product manual uploaded successfully!")

    
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])

            if message.get("source"):
                st.caption(
                    "Source: " + message["source"]
                )

    
    question = st.chat_input(
        "Ask your product question..."
    )

    if question:

        
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        
        results = collection.query(
            query_texts=[question],
            n_results=min(3, len(chunks))
        )

        docs = results["documents"][0]

        context = "\n\n".join(docs)


        prompt = f"""
You are an expert SaaS customer support assistant.

Answer the customer using ONLY the documentation below.

Rules:
1. Do not use outside knowledge.
2. Do not invent features or instructions.
3. Give clear and simple answers.
4. If the answer is not present in the documentation,
   reply exactly:
   I couldn't find that. Please contact support@company.com

Documentation:
{context}

Customer Question:
{question}

Answer:
"""

        
        with st.spinner("Finding your answer..."):

            response = client.chat.complete(
                model=MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1
            )

            answer = response.choices[0].message.content

        
        fallback = (
            "I couldn't find that. "
            "Please contact support@company.com"
        )

        
        source = ""

        if fallback not in answer and docs:
            source = docs[0]

        
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "source": source
        })

        st.rerun()

    
    if st.session_state.messages:

        last_message = st.session_state.messages[-1]

        if last_message["role"] == "assistant":

            st.subheader("Was this answer helpful?")

            col1, col2 = st.columns(2)

            with col1:

                if st.button(" Yes"):

                    st.session_state.feedback = "Helpful"

                    st.success(
                        "Thank you for your feedback!"
                    )

            with col2:

                if st.button("No"):

                    st.session_state.feedback = "Not Helpful"

                    st.info(
                        "Please contact support@company.com"
                    )

    
    st.subheader(" Related Questions")

    suggestions = [
        "How do I reset my password?",
        "How can I update my account settings?",
        "How do I contact customer support?"
    ]

    for suggestion in suggestions:

        if st.button(suggestion):

            st.session_state.messages.append({
                "role": "user",
                "content": suggestion
            })

            st.rerun()

else:

    st.info(
        "Please upload a product manual PDF to start chatting."
    )
