
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Get input from the user
job_role = input("Enter job role (e.g., Python Developer): ")
difficulty = input("Enter difficulty (Easy / Medium / Hard): ")

response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.3,
    max_tokens=1500,
    messages=[
        {
            "role": "system",
            "content": """
            You are an experienced technical interviewer and HR specialist.

            Your task is to create role-specific interview kits.

            Instructions:
            1. Analyze the job role and difficulty level.
            2. Select relevant interview topics for that role.
            3. Generate exactly 5 interview questions.
            4. Provide ideal answer points for every question.
            5. Match question complexity to the requested difficulty.
            6. Do not reveal private internal reasoning.

            Difficulty guidelines:
            Easy: Fundamental concepts and basic understanding.
            Medium: Practical applications and problem-solving.
            Hard: Advanced concepts, system design, and complex scenarios.

            Follow this exact output template:

            INTERVIEW KIT
            Job Role: [Job Role]
            Difficulty: [Difficulty Level]

            Question 1: [Interview question]
            Ideal Answer Points:
            - [Key point 1]
            - [Key point 2]
            - [Key point 3]

            Repeat the same format for Questions 2 through 5.

            Ensure questions are clear, relevant, and non-repetitive.
            Ideal answer points should help interviewers evaluate
            the candidate's knowledge and skills.
            """
        },
        {
            "role": "user",
            "content": f"""
            Generate an interview kit using these details:

            Job Role: {job_role}
            Difficulty Level: {difficulty}

            Analyze the role and difficulty first, then generate
            exactly 5 relevant interview questions and their
            ideal answer points using the required template.
            """
        }
    ]
)

print("\n--- GENERATED INTERVIEW KIT ---\n")
print(response.choices[0].message.content.strip())
