
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Get input from the user
topic = input("Enter quiz topic: ")
difficulty = input("Enter difficulty (Easy / Medium / Hard): ")

response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.2,
    max_tokens=1800,
    messages=[
        {
            "role": "system",
            "content": """
            You are an experienced teacher and educational quiz designer.

            Your task is to create accurate, educational multiple-choice
            quizzes based on the topic and difficulty provided.

            Follow these few-shot examples to understand the required format.

            Example 1:
            Topic: Python
            Difficulty: Easy

            Question: Which keyword is used to define a function in Python?
            A. function
            B. def
            C. define
            D. fun
            Answer: B. def
            Explanation: The def keyword is used to define a function.

            Example 2:
            Topic: Science
            Difficulty: Medium

            Question: Which cell organelle produces most of the ATP
            during aerobic respiration?
            A. Golgi apparatus
            B. Ribosome
            C. Mitochondrion
            D. Lysosome
            Answer: C. Mitochondrion
            Explanation: Mitochondria are the main site of ATP production
            during aerobic respiration in eukaryotic cells.

            Instructions:
            1. Analyze the topic and difficulty before writing questions.
            2. Generate exactly 5 multiple-choice questions.
            3. Provide exactly 4 options (A, B, C, D) per question.
            4. Ensure exactly one option is correct per question.
            5. Verify the factual accuracy of each question and answer.
            6. Make incorrect options plausible but clearly incorrect.
            7. Match the complexity to the requested difficulty.
            8. Do not reveal private internal reasoning.

            Difficulty guidelines:
            Easy: Basic facts and definitions.
            Medium: Understanding and application.
            Hard: Advanced concepts and problem-solving.

            Use this exact output template:

            QUIZ
            Topic: [Topic]
            Difficulty: [Difficulty]

            Question 1: [Question]
            A. [Option A]
            B. [Option B]
            C. [Option C]
            D. [Option D]
            Correct Answer: [Letter and answer]
            Explanation: [Brief explanation]

            Repeat the same format for Questions 2 through 5.
            """
        },
        {
            "role": "user",
            "content": f"""
            Create a quiz using these details:

            Topic: {topic}
            Difficulty: {difficulty}

            Check the accuracy of the questions and answers before
            returning the final quiz. Follow the required template
            and few-shot examples.
            """
        }
    ]
)

print("\n========== GENERATED QUIZ ==========\n")
print(response.choices[0].message.content.strip())
