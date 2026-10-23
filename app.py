
import streamlit as st
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

st.title("AI STORY GENERATOR")
st.write("Generate a creative story using AI!")

topic = st.text_input("Enter your story topic")
genre = st.selectbox(
    "Choose story genre",
    ["Adventure", "Horror", "Comedy", "Fantasy", "Motivational"]
)

if st.button("Generate Story"):
    if not topic.strip():
        st.warning("Please enter a story topic.")
    elif not os.getenv("MISTRAL_API_KEY"):
        st.error("MISTRAL_API_KEY is missing from your .env file.")
    else:
        st.subheader("Your AI Story")

        try:
            with st.spinner("Creating your story..."):
                response = client.chat.stream(
                    model="mistral-small-latest",
                    temperature=0.7,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a creative story writer."
                        },
                        {
                            "role": "user",
                            "content": f"Write a short {genre} story about {topic}."
                        }
                    ]
                )

                def token_stream():
                    for chunk in response:
                        content = chunk.data.choices[0].delta.content
                        if content:
                            yield content

                st.write_stream(token_stream())

        except Exception as e:
            st.error(f"An error occurred: {e}")