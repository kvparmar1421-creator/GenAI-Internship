
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Take input from the user
candidate_points = input("Enter candidate's key points: ")
job_description = input("Enter job description: ")

# Template with two main variables
prompt_template = """
Candidate's Key Points:
{candidate_points}

Job Description:
{job_description}

First, identify the candidate's relevant skills and experience
that match the job requirements. Then write a tailored cover letter.

Requirements:
- Use a professional tone.
- Highlight relevant skills and experience.
- Explain how the candidate can contribute to the role.
- Keep the letter clear, concise, and well-structured.
- Do not invent qualifications or work experience.
- Use placeholders for missing personal details.
- Return only the completed cover letter.
"""

response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.5,
    max_tokens=700,
    messages=[
        {
            "role": "system",
            "content": """
            You are an experienced career coach and professional
            cover letter writer.

            Your job is to help candidates apply for jobs by creating
            tailored cover letters.

            First, compare the candidate's skills and experience with
            the job requirements. Then use the strongest relevant
            matches to write the cover letter.

            Write in a professional, confident, and natural tone.
            Do not invent skills, qualifications, achievements,
            or experience that the candidate has not provided.
            Do not reveal internal reasoning.
            """
        },
        {
            "role": "user",
            "content": prompt_template.format(
                candidate_points=candidate_points,
                job_description=job_description
            )
        },
    ]
)

print("\n--- GENERATED COVER LETTER ---\n")
print(response.choices[0].message.content.strip())
