
import streamlit as st
import os
import json
import re
import io

from dotenv import load_dotenv
from mistralai.client import Mistral

# Load API key
load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")

st.set_page_config(
    page_title="Smart Resume Screener",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Smart Resume Screener")
st.write("AI-powered resume screening and candidate evaluation")

# Initialize Mistral client
if not API_KEY:
    st.error("MISTRAL_API_KEY not found. Please check your .env file.")
    st.stop()

client = Mistral(api_key=API_KEY)


# Extract text from PDF
def extract_pdf_text(uploaded_file):
    try:
        pdf = PdfReader(io.BytesIO(uploaded_file.getvalue()))

        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""

        return text

    except Exception as e:
        st.error(f"Could not read PDF: {e}")
        return ""


# AI resume screening function
def screen_resume(resume_text, job_description):

    # Prompt template with two large variables
    prompt = """
You are an expert recruiter and ATS resume screening assistant.

Compare the candidate resume with the job description.

Follow these steps internally:
1. Identify the skills required by the job.
2. Compare them with skills explicitly supported by the resume.
3. Evaluate relevant work experience and qualifications.
4. Calculate a match score from 0 to 100.
5. Provide a fair recommendation based on job-related evidence.

Do not reveal private chain-of-thought. Return only the final result.

RESUME:
{resume}

JOB DESCRIPTION:
{job}

Return valid JSON only using this exact structure:
{{
    "match_score": 78,
    "matched_skills": ["Python", "SQL"],
    "missing_skills": ["Docker", "AWS"],
    "experience_fit": "good",
    "recommendation": "shortlist",
    "feedback": "A short paragraph explaining strengths and areas to improve."
}}

Rules:
- match_score must be an integer from 0 to 100.
- matched_skills must contain skills supported by the resume.
- missing_skills must contain relevant job requirements not demonstrated
  in the resume, not assumptions about the candidate.
- experience_fit must be one of: "good", "partial", "poor".
- recommendation must be one of: "shortlist", "review", "reject".
- Use job-related criteria only.
- Do not infer skills from personal details.
- Keep feedback professional and constructive.
"""

    # Inject resume and job description into template
    final_prompt = prompt.format(
        resume=resume_text,
        job=job_description
    )

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )

        result_text = response.choices[0].message.content

        if not isinstance(result_text, str):
            result_text = str(result_text)

        result = json.loads(result_text)

        # Validate AI output
        score = int(result["match_score"])

        if not 0 <= score <= 100:
            raise ValueError("Match score must be between 0 and 100.")

        if not isinstance(result["matched_skills"], list):
            raise ValueError("matched_skills must be a list.")

        if not isinstance(result["missing_skills"], list):
            raise ValueError("missing_skills must be a list.")

        if result["experience_fit"] not in [
            "good", "partial", "poor"
        ]:
            raise ValueError("Invalid experience_fit.")

        if result["recommendation"] not in [
            "shortlist", "review", "reject"
        ]:
            raise ValueError("Invalid recommendation.")

        if not isinstance(result["feedback"], str):
            raise ValueError("Feedback must be text.")

        return result

    except json.JSONDecodeError:
        st.error("AI returned invalid JSON. Please try again.")

    except KeyError as e:
        st.error(f"Missing field in AI response: {e}")

    except ValueError as e:
        st.error(f"Invalid AI response: {e}")

    except Exception as e:
        st.error(f"Screening failed: {e}")

    return None


# Display screening results
def display_result(result):

    score = result["match_score"]

    st.subheader("Screening Results")

    st.metric("Match Score", f"{score}/100")
    st.progress(score / 100)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matched Skills")

        if result["matched_skills"]:
            for skill in result["matched_skills"]:
                st.write(f"✅ {skill}")
        else:
            st.write("No matching skills identified.")

    with col2:
        st.subheader("❌ Missing Skills")

        if result["missing_skills"]:
            for skill in result["missing_skills"]:
                st.write(f"❌ {skill}")
        else:
            st.write("No missing required skills identified.")

    st.subheader("Experience Fit")
    st.write(result["experience_fit"].capitalize())

    st.subheader("Recommendation")

    recommendation = result["recommendation"]

    if recommendation == "shortlist":
        st.success("🟢 SHORTLIST")
    elif recommendation == "review":
        st.warning("🟡 REVIEW")
    else:
        st.error("🔴 REJECT")

    st.subheader("Candidate Feedback")
    st.write(result["feedback"])

    st.subheader("Structured JSON Output")
    st.json(result)


# Main application tabs
tab1, tab2 = st.tabs([
    "Single Resume Screening",
    "Batch Resume Screening"
])


# ---------------- SINGLE RESUME MODE ----------------
with tab1:

    st.subheader("Screen One Candidate")

    resume_text = st.text_area(
        "Paste Resume Text",
        height=220,
        placeholder="Paste the candidate's resume here..."
    )

    uploaded_pdf = st.file_uploader(
        "Or upload resume as PDF",
        type=["pdf"],
        key="single_pdf"
    )

    if uploaded_pdf:
        extracted_text = extract_pdf_text(uploaded_pdf)

        if extracted_text:
            st.success("PDF text extracted successfully.")
            with st.expander("Preview Extracted Resume"):
                st.text(extracted_text)

            resume_text = extracted_text

    job_description = st.text_area(
        "Job Description",
        height=220,
        placeholder="Paste the job requirements here..."
    )

    if st.button("🔍 Screen Resume", type="primary"):

        if not resume_text.strip():
            st.warning("Please enter resume text or upload a PDF.")

        elif not job_description.strip():
            st.warning("Please enter a job description.")

        else:
            with st.spinner("Analyzing resume with AI..."):
                result = screen_resume(
                    resume_text,
                    job_description
                )

            if result:
                display_result(result)


# ---------------- BATCH RESUME MODE ----------------
with tab2:

    st.subheader("Batch Resume Screening")
    st.write("Upload multiple PDF resumes to compare and rank candidates.")

    batch_files = st.file_uploader(
        "Upload multiple resumes",
        type=["pdf"],
        accept_multiple_files=True,
        key="batch_pdfs"
    )

    batch_job = st.text_area(
        "Job Description for Batch Screening",
        height=180,
        key="batch_job"
    )

    if st.button("🚀 Screen All Resumes", type="primary"):

        if not batch_files:
            st.warning("Please upload at least one resume.")

        elif not batch_job.strip():
            st.warning("Please enter the job description.")

        else:
            results = []

            progress = st.progress(0)
            status = st.empty()

            for index, file in enumerate(batch_files):

                status.write(
                    f"Screening {index + 1} of {len(batch_files)}: "
                    f"{file.name}"
                )

                resume = extract_pdf_text(file)

                if not resume.strip():
                    st.warning(
                        f"Could not extract text from {file.name}"
                    )
                    progress.progress(
                        (index + 1) / len(batch_files)
                    )
                    continue

                result = screen_resume(resume, batch_job)

                if result:
                    results.append({
                        "resume": file.name,
                        **result
                    })

                progress.progress(
                    (index + 1) / len(batch_files)
                )

            status.empty()

            if results:

                # Rank candidates by match score
                results.sort(
                    key=lambda item: item["match_score"],
                    reverse=True
                )

                st.success("Batch screening completed!")

                st.subheader("Candidate Ranking")

                for rank, candidate in enumerate(results, start=1):

                    with st.expander(
                        f"#{rank} — {candidate['resume']} | "
                        f"Score: {candidate['match_score']}/100"
                    ):

                        display_result(candidate)

                # Export results to JSON
                export_json = json.dumps(
                    results,
                    indent=4,
                    ensure_ascii=False
                )

                st.download_button(
                    label="Download Batch Results (JSON)",
                    data=export_json,
                    file_name="resume_screening_results.json",
                    mime="application/json"
                )

            else:
                st.error("No resumes could be screened successfully.")
