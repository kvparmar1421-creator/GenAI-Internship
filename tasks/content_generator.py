
import streamlit as st
import os
import re
from dotenv import load_dotenv
from mistralai import Mistral

# Load environment variables
load_dotenv()

# Initialize Mistral client
api_key = os.getenv("MISTRAL_API_KEY")

st.set_page_config(
    page_title="AI Content Studio",
    page_icon="✍️",
    layout="wide"
)

st.title("✍️ AI Content Studio")
st.write("Generate high-quality marketing content with live AI streaming.")

# Check API key
if not api_key:
    st.error("MISTRAL_API_KEY not found. Please add it to your .env file.")
    st.stop()

client = Mistral(api_key=api_key)

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar settings
st.sidebar.header("⚙️ Content Settings")

content_type = st.sidebar.selectbox(
    "Choose Content Type",
    [
        "Blog Introduction",
        "LinkedIn Post",
        "Product Description",
        "Email"
    ]
)

tone = st.sidebar.selectbox(
    "Choose Tone",
    [
        "Professional",
        "Friendly",
        "Creative",
        "Formal",
        "Persuasive",
        "Funny"
    ]
)

max_tokens = st.sidebar.slider(
    "Maximum Output Tokens",
    min_value=100,
    max_value=1500,
    value=500,
    step=100
)

temperature = st.sidebar.slider(
    "Creativity Level",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1
)

# Main input
topic = st.text_input(
    "Enter your topic",
    placeholder="e.g., Benefits of Artificial Intelligence"
)

# Function to generate content
def generate_content(topic, content_type, tone, max_tokens, temperature):
    prompt = f"""
You are an expert marketing copywriter.

Create content using the following requirements:

Topic: {topic}
Content Type: {content_type}
Tone: {tone}

Instructions:
- Write clear, engaging, useful content.
- Follow the selected content format.
- Use the selected tone consistently.
- Avoid unnecessary repetition.
- Return only the generated content.
"""

    response = client.chat.stream(
        model="mistral-small-latest",
        messages=[
            {
                "role": "system",
                "content": "You are a professional marketing copywriter."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )

    full_content = ""

    # Stream content live
    for chunk in response:
        if chunk.data.choices:
            delta = chunk.data.choices[0].delta
            text = delta.content

            if isinstance(text, str):
                full_content += text
                yield text

# Generate button
if st.button("🚀 Generate Content", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        st.subheader("✨ Generated Content")

        try:
            with st.spinner("Connecting to AI..."):
                # Live streaming output
                content = st.write_stream(
                    generate_content(
                        topic,
                        content_type,
                        tone,
                        max_tokens,
                        temperature
                    )
                )

            # Save generated content
            st.session_state.history.append({
                "topic": topic,
                "type": content_type,
                "tone": tone,
                "content": content
            })

            # Statistics
            word_count = len(content.split())
            estimated_tokens = len(content) // 4

            st.success("Content generated successfully!")

            col1, col2, col3 = st.columns(3)

            col1.metric("Word Count", word_count)
            col2.metric("Estimated Tokens", estimated_tokens)
            col3.metric("Max Output Tokens", max_tokens)

            st.caption(
                "Token count is approximate. Actual API usage may differ."
            )

            # Copy button
            st.code(content, language=None)

            st.download_button(
                "📥 Download Content",
                data=content,
                file_name="generated_content.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error generating content: {e}")

# Regenerate button
if st.button("🔄 Regenerate Content"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        try:
            st.subheader("🔄 Regenerated Content")

            content = st.write_stream(
                generate_content(
                    topic,
                    content_type,
                    tone,
                    max_tokens,
                    temperature
                )
            )

            st.session_state.history.append({
                "topic": topic,
                "type": content_type,
                "tone": tone,
                "content": content
            })

            st.metric("Word Count", len(content.split()))

        except Exception as e:
            st.error(f"Error regenerating content: {e}")

# A/B Testing
st.divider()
st.header("🧪 A/B Content Testing")
st.write("Generate two versions with different creativity levels.")

if st.button("Generate A/B Versions"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        col1, col2 = st.columns(2)

        try:
            with col1:
                st.subheader("Version A")
                version_a = st.write_stream(
                    generate_content(
                        topic, content_type, tone,
                        max_tokens, 0.3
                    )
                )
                st.caption(f"{len(version_a.split())} words")

            with col2:
                st.subheader("Version B")
                version_b = st.write_stream(
                    generate_content(
                        topic, content_type, tone,
                        max_tokens, 0.9
                    )
                )
                st.caption(f"{len(version_b.split())} words")

        except Exception as e:
            st.error(f"A/B generation failed: {e}")

# History section
st.divider()
st.header("📚 Content History")

if st.session_state.history:
    for i, item in enumerate(
        reversed(st.session_state.history), start=1
    ):
        with st.expander(
            f"{i}. {item['topic']} — {item['type']}"
        ):
            st.write("**Tone:**", item["tone"])
            st.write(item["content"])
else:
    st.info("Your generated content will appear here.")
