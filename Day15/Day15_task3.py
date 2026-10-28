
import os
import streamlit as st
import chromadb

from dotenv import load_dotenv
from pypdf import PdfReader
from mistralai.client import Mistral

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
MODEL = "mistral-small-latest"

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚"
)

st.title("📚 AI Study Assistant")
st.write("Upload a PDF and study with your AI tutor.")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Upload your filr
pdf = st.file_uploader(
    "Upload Textbook / Research Paper",
    type=["pdf"]
)

if pdf:

    reader = PdfReader(pdf)


    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text() or ""

        if page_text.strip():
            pages.append((page_number, page_text))

    # all content divide into small chunks
    chunks = []
    chunk_pages = []

    chunk_size = 1000
    overlap = 150

    for page_number, page_text in pages:

        for start in range(
            0,
            len(page_text),
            chunk_size - overlap
        ):

            chunk = page_text[start:start + chunk_size]

            if chunk.strip():
                chunks.append(chunk)
                chunk_pages.append(page_number)

    # make database in chromadb
    db = chromadb.Client()

    collection = db.get_or_create_collection(
        name="study_documents"
    )


    if chunks:

        collection.upsert(
            ids=[str(i) for i in range(len(chunks))],
            documents=chunks,
            metadatas=[
                {"page": page}
                for page in chunk_pages
            ]
        )

    st.success("PDF uploaded successfully!")

    # make three type of study mode: Ask, Quiz, Summarize
    mode = st.radio(
        "Choose Study Mode",
        ["Ask", "Quiz", "Summarize"],
        horizontal=True
    )


    if mode == "Ask":

        
        for message in st.session_state.messages:

            with st.chat_message(message["role"]):

                st.write(message["content"])

                if message.get("source"):
                    st.caption(message["source"])

        question = st.chat_input(
            "Ask a question from your PDF..."
        )

        if question and chunks:

            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

        
            results = collection.query(
                query_texts=[question],
                n_results=min(3, len(chunks))
            )

            docs = results["documents"][0]
            metadata = results["metadatas"][0]

            context = "\n\n".join(
                f"Page {meta['page']}:\n{doc}"
                for doc, meta in zip(docs, metadata)
            )

        
            prompt = f"""
You are a friendly AI tutor.

Answer the student's question using ONLY
the provided document context.

Explain in simple language.
Do not invent facts.

If the answer is not available, reply:
I couldn't find the answer in this document.

Document Context:
{context}

Student Question:
{question}
"""

            with st.spinner("Tutor is thinking..."):

                response = client.chat.complete(
                    model=MODEL,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2
                )

            answer = response.choices[0].message.content

            
            source_pages = sorted({
                meta["page"]
                for meta in metadata
            })

            source = "Source Pages: " + ", ".join(
                map(str, source_pages)
            )

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "source": source
            })

            st.rerun()

    
    elif mode == "Quiz":

        difficulty = st.selectbox(
            "Select Difficulty",
            ["Easy", "Medium", "Hard"]
        )

        if st.button("Generate 5 Quiz Questions"):

            
            context = "\n\n".join(chunks[:10])

            prompt = f"""
You are an educational quiz creator.

Generate exactly 5 multiple-choice questions
from the given document.

Difficulty: {difficulty}

Each question must contain:
1. Question
2. Four options (A, B, C, D)
3. Correct answer
4. Short explanation
5. Source page number

Use ONLY the document content.
Do not invent facts.

Document:
{context}
"""

            with st.spinner("Generating quiz..."):

                response = client.chat.complete(
                    model=MODEL,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3
                )

            st.subheader("Your Quiz")

            st.markdown(
                response.choices[0].message.content
            )

    elif mode == "Summarize":

        if st.button("Summarize Document"):

            summaries = []

            with st.spinner("Summarizing document..."):

                # Summarize long PDFs in batches
                for i in range(0, len(chunks), 5):

                    batch = "\n\n".join(
                        chunks[i:i + 5]
                    )

                    prompt = f"""
Summarize the following textbook content
in simple language.

Include:
- Main ideas
- Important definitions
- Key points
- Important examples

Use ONLY the given content.

Content:
{batch}
"""

                    response = client.chat.complete(
                        model=MODEL,
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.2
                    )

                    summaries.append(
                        response.choices[0].message.content
                    )

                # Combine batch summaries
                combined_summaries = "\n\n".join(
                    summaries
                )

                final_prompt = f"""
Create a clear and organized study summary
from the following summaries.

Include important concepts and definitions.
Avoid repetition.

Summaries:
{combined_summaries}
"""

                final_response = client.chat.complete(
                    model=MODEL,
                    messages=[
                        {
                            "role": "user",
                            "content": final_prompt
                        }
                    ],
                    temperature=0.2
                )

            st.subheader("Document Summary")

            st.markdown(
                final_response.choices[0].message.content
            )

else:

    st.info(
        "Upload a PDF to start studying."
    )
